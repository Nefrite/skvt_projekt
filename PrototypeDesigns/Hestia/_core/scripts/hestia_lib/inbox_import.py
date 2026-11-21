"""Příkaz inbox_import: import položek ze souboru výměny do `Inbox/` (zadání 13 kap. 10.12; zadání 0.16).

Čtení zdroje je mimo core (síť, konektory); agent ho podle modulu `inbox_import` uloží do souboru výměny
`Maintenance/import/<zdroj>_RRRR-MM-DD.json`: `source`, `source_query`, `exported`, `items` s `{ref, title, created,
type, tags, content, content_format}`. Příkaz z něj deterministicky zapíše scratch podle `tpl_scratch` (07 kap. 4):

- jméno souboru z `title` (bez diakritiky, mezery → `_`, jen `[A-Za-z0-9_]`); kolize s existující poznámkou vaultu →
  přípona `_<source>`, kolize v dávce → `_2`, `_3`; prázdný titul → `<source>_<datum vytvoření>`;
- `category` z `type` i `tags` přes `tag_map` (sjednocení bez duplicit); nenamapovaná hodnota = upozornění;
- `content_format: notion-md` se převede (`notion_md_to_markdown`), `markdown` se zapíše beze změny;
- duplicita = `ref` už nese `source_ref` některé poznámky (nebo se v souboru opakuje) → přeskočit a vypsat;
- po `--apply`: `lint` zapsaných souborů (chyba = kód 1, soubory zůstanou), `doc_index`, řádek `changes.md`.
Výstup: `written`, `skipped`, `unmapped`, `needs_review`, `errors`; podle `written` agent mění stav ve zdroji.
Návratové kódy: 0 v pořádku (i s upozorněními), 1 chyba položky nebo `lint`, 2 chyba použití.
"""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from .changeset import ChangeSet
from .errors import EXIT_FINDINGS, EXIT_OK, UsageError
from .fileio import read_text, to_posix
from .frontmatter import format_value
from .logs import append_lines, format_line
from .util import as_date, as_list, today
from .vault import Vault

INBOX = "Inbox"
IMPORT_DIR = "Maintenance/import"
CHANGES_REL = "Maintenance/changes.md"
ROLE = "Curator"                          # import do Inbox/ dělá Curator (05 kap. 3, zadání 0.16)
FORMATS = ("markdown", "notion-md")
FENCE = "notion-md"

# ---------------------------------------------------------------- převod notion-md → Markdown

_TAG_RE = re.compile(r"<(/?)([A-Za-z][\w-]*)((?:\s[^<>]*?)?)(/?)>")
_LIST_TAG_RE = re.compile(r"<(/?)(ul|ol|li)(?:\s[^<>]*)?>", re.I)
_INLINE = {"b": "**", "strong": "**", "i": "*", "em": "*"}
_A_RE = re.compile(r"""<a\s+[^<>]*?href=(["'])(.*?)\1[^<>]*>(.*?)</a>""", re.I | re.S)
_EMPTY_BLOCK_RE = re.compile(r"^\s*<empty-block\s*/>\s*$")
# druhy nepřevedených bloků pro výstup (needs_review); neznámý tag = jeho jméno
_KINDS = {"img": "image", "image": "image", "video": "video", "audio": "audio", "file": "file", "pdf": "file",
          "table": "table", "tr": "table", "td": "table", "details": "toggle", "summary": "toggle",
          "callout": "callout", "database": "database", "data-source": "database", "page": "page",
          "columns": "columns", "column": "columns", "embed": "embed", "synced_block": "synced_block"}
_SUPPORTED = {"ul", "ol", "li", "b", "strong", "i", "em", "a"}


def _kind(tag: str) -> str:
    tag = tag.lower()
    if tag.startswith("mention"):
        return "mention"
    return _KINDS.get(tag, tag)


def _segments(lines: list[str]) -> list[tuple[bool, list[str]]]:
    """Úseky obsahu: (je_úsek, řádky). Úsek = řádky mezi prázdnými řádky; neuzavřený blokový tag (seznam, tabulka,
    toggle …) úsek prodlužuje i přes prázdný řádek. Prázdné řádky mimo úseky zůstávají, jak jsou."""
    out: list[tuple[bool, list[str]]] = []
    cur: list[str] = []
    depth = 0
    for line in lines:
        if not line.strip() and depth <= 0:
            if cur:
                out.append((True, cur))
                cur = []
            out.append((False, [line]))
            continue
        cur.append(line)
        for m in _TAG_RE.finditer(line):
            closing, name, _attrs, selfclose = m.groups()
            name = name.lower()
            if name in _INLINE or name in ("a", "span", "u", "s", "code", "br", "img") or name.startswith("mention") \
                    or selfclose:
                continue
            depth += -1 if closing else 1
    if cur:
        out.append((True, cur))
    return out


def _inline(text: str) -> str:
    text = _A_RE.sub(lambda m: f"[{m.group(3)}]({m.group(2)})", text)
    for tag, mark in _INLINE.items():
        text = re.sub(rf"</?{tag}>", mark, text, flags=re.I)
    return text


def _lists(text: str) -> list[str]:
    """Seznamy `<ul>`, `<ol>`, `<li>` (i vnořené) na odrážky s odsazením dvou mezer; prázdná položka zůstane."""
    out: list[str] = []
    stack: list[list] = []                  # [druh, počítadlo]
    item: list[str] | None = None           # text rozpracované položky
    item_prefix = ""

    def flush_item() -> None:
        nonlocal item
        if item is not None:
            body = " ".join(part.strip() for part in "".join(item).split("\n") if part.strip())
            out.append((item_prefix + " " + body).rstrip())
            item = None

    def text_out(chunk: str) -> None:
        if item is not None:
            item.append(chunk)
        else:
            out.extend(line for line in chunk.split("\n") if line.strip())

    pos = 0
    for m in _LIST_TAG_RE.finditer(text):
        text_out(text[pos:m.start()])
        pos = m.end()
        closing, tag = m.group(1), m.group(2).lower()
        if tag in ("ul", "ol"):
            flush_item()
            if closing:
                if stack:
                    stack.pop()
            else:
                stack.append([tag, 0])
        elif not closing:                    # <li>
            flush_item()
            depth = max(len(stack) - 1, 0)
            if stack and stack[-1][0] == "ol":
                stack[-1][1] += 1
                marker = f"{stack[-1][1]}."
            else:
                marker = "-"
            item_prefix = "  " * depth + marker
            item = []
        else:                                # </li>
            flush_item()
    text_out(text[pos:])
    flush_item()
    return out


def notion_md_to_markdown(content: str) -> tuple[str, list[str]]:
    """Převod Notion-flavored Markdownu (13 kap. 10.12). Odstavce, nadpisy, tučné, kurzíva, odkazy a vnořené seznamy;
    text bez značek zůstane znak po znaku stejný. Úsek s jiným blokem (obrázek, soubor, tabulka, toggle, callout,
    zmínka, databáze …) se nepřevádí: zapíše se v původní podobě v ohrazení ```notion-md a vrátí se jeho druh."""
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    kinds: list[str] = []
    for is_seg, seg in _segments(lines):
        if not is_seg:
            out.extend(seg)
            continue
        text = "\n".join(seg)
        if all(_EMPTY_BLOCK_RE.match(line) for line in seg):   # prázdný odstavec Notion
            out.extend("" for _ in seg)
            continue
        found = sorted({_kind(m.group(2)) for m in _TAG_RE.finditer(text) if m.group(2).lower() not in _SUPPORTED})
        if re.search(r"!\[[^\]]*\]\(", text):
            found = sorted(set(found) | {"image"})
        if found:
            kinds.extend(k for k in found if k not in kinds)
            out += [f"```{FENCE}", *seg, "```"]
            continue
        if not _TAG_RE.search(text):
            out.extend(seg)                                     # beze značek: beze změny
            continue
        out.extend(_lists(_inline(text)) if _LIST_TAG_RE.search(text) else _inline(text).split("\n"))
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out), kinds


# ---------------------------------------------------------------- plán importu

def slug(title: str) -> str:
    s = unicodedata.normalize("NFKD", title or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\s+", "_", s.strip())
    s = re.sub(r"[^A-Za-z0-9_]", "", s)
    return re.sub(r"_+", "_", s).strip("_")


@dataclass
class Plan:
    source: str
    file: str
    written: list[dict] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)
    unmapped: list[str] = field(default_factory=list)
    needs_review: list[dict] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)
    texts: dict[str, str] = field(default_factory=dict)     # rel -> obsah scratch


def load_exchange(path: Path, vault: Vault) -> dict:
    if not path.is_file():
        raise UsageError(f"inbox_import: soubor výměny {path} neexistuje")
    try:
        data = json.loads(read_text(path))
    except ValueError as exc:
        raise UsageError(f"inbox_import: {path.name} není platný JSON ({exc})") from exc
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise UsageError(f"inbox_import: {path.name} nemá seznam items (13 kap. 10.12)")
    known = (vault.taxonomy.enums.get("source") or {}).get("values") or []
    source = data.get("source")
    if not isinstance(source, str) or source not in known:
        raise UsageError(f"inbox_import: neznámý source {source!r} (výčet source: {', '.join(known)})")
    return data


def _created(value) -> str:
    d = as_date(str(value)[:10]) if value else None
    return d.isoformat() if d else (str(value).strip() if value else "")


def _link(ref: str) -> str:
    return f"<{ref}>" if re.search(r"[\s()<>]", ref) else ref


def scratch_text(source: str, ref: str, title: str, created: str, categories: list[str], body: str) -> str:
    lines = ["---", "# orchestrace", "type: scratch", "intake: raw", f"source: {format_value(source)}",
             f"source_ref: {json.dumps(ref, ensure_ascii=False)}", "validity: valid",
             f"updated: {today().isoformat()}", "# hra", f"category: {format_value(categories)}", 'entity: ""',
             "---", f"# {title}", "",
             f"Zdroj: [{source}]({_link(ref)})" + (f", vytvořeno {created}" if created else ""), ""]
    if body.strip():
        lines += [body, ""]
    lines += ["## Předzpracování (doplní Knihovník)", "- Kategorie:", "- Souvisí s:",
              "- Návrh zařazení: (doména / crosscut / nic)", ""]
    return "\n".join(lines)


def plan(vault: Vault, data: dict, file_label: str) -> Plan:
    source = data["source"]
    pl = Plan(source=source, file=file_label)
    tag_map = vault.taxonomy.tag_map
    existing_refs = {}
    for n in vault.notes.values():
        ref = (n.fm or {}).get("source_ref") if n.fm else None
        if ref not in (None, ""):
            existing_refs[str(ref).strip()] = n.rel
    in_vault = {n.name.lower() for n in vault.notes.values()}
    in_batch: set[str] = set()
    batch_refs: dict[str, str] = {}
    for idx, it in enumerate(data["items"], 1):
        if not isinstance(it, dict):
            pl.errors.append({"ref": None, "item": idx, "error": "položka není objekt"})
            continue
        ref = str(it.get("ref") or "").strip()
        if not ref:
            pl.errors.append({"ref": None, "item": idx, "error": "položka bez ref"})
            continue
        fmt = it.get("content_format")
        if fmt not in FORMATS:
            pl.errors.append({"ref": ref, "item": idx, "error": f"neznámý content_format {fmt!r} ({', '.join(FORMATS)})"})
            continue
        content = it.get("content")
        if content is not None and not isinstance(content, str):
            pl.errors.append({"ref": ref, "item": idx, "error": "content není text"})
            continue
        if ref in existing_refs:
            pl.skipped.append({"ref": ref, "path": existing_refs[ref], "reason": "už importováno (source_ref)"})
            continue
        if ref in batch_refs:
            pl.skipped.append({"ref": ref, "path": batch_refs[ref], "reason": "ref se v souboru výměny opakuje"})
            continue
        title = str(it.get("title") or "").strip()
        created = _created(it.get("created"))
        # kategorie
        cats: list[str] = []
        for value in [*as_list(it.get("type")), *as_list(it.get("tags"))]:
            value = str(value).strip()
            if not value:
                continue
            cat = tag_map.get(value)
            if cat:
                if cat not in cats:
                    cats.append(cat)
            elif value not in pl.unmapped:
                pl.unmapped.append(value)
        # jméno souboru
        # kolize s existující poznámkou vaultu → _<source>; kolize v dávce (i po příponě) → _2, _3
        base = slug(title) or f"{source}_{created or today().isoformat()}"
        stem = f"{base}_{source}" if base.lower() in in_vault else base
        name, n = stem, 2
        while name.lower() in in_vault or name.lower() in in_batch:
            name = f"{stem}_{n}"
            n += 1
        in_batch.add(name.lower())
        rel = f"{INBOX}/{name}.md"
        # obsah
        body = (content or "").replace("\r\n", "\n").rstrip()
        if fmt == "notion-md":
            body, kinds = notion_md_to_markdown(body)
            if kinds:
                pl.needs_review.append({"ref": ref, "path": rel, "kinds": kinds})
        pl.texts[rel] = scratch_text(source, ref, title or name, created, cats, body)
        pl.written.append({"ref": ref, "path": rel, "title": title})
        batch_refs[ref] = rel
    return pl


def _exchange_path(arg: str, vault: Vault) -> Path:
    p = Path(arg)
    if p.is_absolute():
        return p
    for base in (Path.cwd(), vault.root):
        if (base / p).is_file():
            return base / p
    return Path.cwd() / p


def _label(path: Path, vault: Vault) -> str:
    try:
        return to_posix(path.resolve().relative_to(vault.root.resolve()))
    except ValueError:
        return to_posix(path)


def run(args, vault: Vault) -> tuple[int, dict, str]:
    if not args.source_file:
        raise UsageError("inbox_import: chybí --from <soubor výměny>")
    path = _exchange_path(args.source_file, vault)
    data = load_exchange(path, vault)
    pl = plan(vault, data, _label(path, vault))
    lint_out: list[dict] = []
    applied = bool(args.apply and pl.written)
    if applied:
        cs = ChangeSet(vault.project_root)
        for rel, text in pl.texts.items():
            cs.write(vault.root / rel, text)
        cpath = vault.root / CHANGES_REL
        ctext = cs.current(cpath)
        if ctext is None:
            raise UsageError(f"{CHANGES_REL} neexistuje")
        day = today().isoformat()
        rows = [format_line([day, ROLE, Path(w["path"]).stem, "nová položka inboxu (intake: raw)",
                             f"import {pl.source}"]) for w in pl.written]
        cs.write(cpath, append_lines(ctext, rows, today=today()))
        cs.apply()
        from . import doc_index
        from .lint import lint
        fresh = Vault.load(vault.root)
        for f in lint(fresh, [str(fresh.root / w["path"]) for w in pl.written]):
            lint_out.append({"severity": f.severity, "code": f.code, "file": f.file, "message": f.message})
        dcs = ChangeSet(fresh.project_root)
        if doc_index.plan(fresh, dcs):
            dcs.apply()
    lint_errors = [f for f in lint_out if f["severity"] == "error"]
    code = EXIT_FINDINGS if (pl.errors or lint_errors) else EXIT_OK
    payload = {"command": "inbox_import", "applied": applied, "source": pl.source, "file": pl.file,
               "written": pl.written, "skipped": pl.skipped, "unmapped": pl.unmapped,
               "needs_review": pl.needs_review, "errors": pl.errors, "lint": lint_out}
    verb = "zapsáno" if applied else ("zapsalo by se (dry-run, zapiš s --apply)" if pl.written else "k zápisu")
    lines = [f"inbox_import {pl.file} ({pl.source}): {len(pl.written)} {verb}, {len(pl.skipped)} přeskočeno, "
             f"{len(pl.needs_review)} k ruční kontrole, {len(pl.errors)} chyb"]
    lines += [f"  zapsáno: {w['ref']} → {w['path']}" for w in pl.written]
    lines += [f"  přeskočeno: {s['ref']} ({s['path']}): {s['reason']}" for s in pl.skipped]
    lines += [f"  vyžaduje ruční kontrolu: {r['path']} ({', '.join(r['kinds'])})" for r in pl.needs_review]
    if pl.unmapped:
        lines.append(f"  bez tag_map (kategorie nedoplněna): {', '.join(pl.unmapped)}")
    lines += [f"  chyba položky {e.get('ref') or '#' + str(e['item'])}: {e['error']}" for e in pl.errors]
    lines += [f"  lint {f['severity']} {f['code']} {f['file']}: {f['message']}" for f in lint_out]
    if applied:
        lines.append("  po zápisu: lint, doc_index, changes.md; stav ve zdroji měň jen u zapsaných položek")
    return code, payload, "\n".join(lines)
