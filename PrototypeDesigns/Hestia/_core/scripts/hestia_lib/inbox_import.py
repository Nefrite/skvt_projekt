"""Příkaz inbox_import: import položek ze souboru výměny do `Inbox/` (zadání 13 kap. 10.12; zadání 0.16).

Čtení zdroje je mimo core (síť, konektory); agent ho podle modulu `inbox_import` uloží do souboru výměny
`Maintenance/import/<zdroj>_RRRR-MM-DD.json`: `source`, `source_query`, `exported`, `items` s `{ref, title, created,
type, tags, content, content_format}`. Příkaz z něj deterministicky zapíše scratch podle `tpl_scratch` (07 kap. 4):

- jméno souboru z `title` (bez diakritiky, mezery → `_`, jen `[A-Za-z0-9_]`); kolize s existující poznámkou vaultu →
  přípona `_<source>`, kolize v dávce → `_2`, `_3`; prázdný titul → `<source>_<datum vytvoření>`;
- `category` z `type` i `tags` přes `tag_map` (sjednocení bez duplicit); nenamapovaná hodnota = upozornění;
- `content_format: notion-md` se převede (`notion_md.notion_md_to_markdown`, zadání 0.17.2; kontejnery, tabulka
  převodů, kontrola věrnosti `struktura`), `markdown` se zapíše beze změny;
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
from .notion_md import FENCE, notion_md_to_markdown  # noqa: F401  (převod 13 kap. 10.12, zadání 0.17.2)
from .util import as_date, as_list, today
from .vault import Vault

INBOX = "Inbox"
IMPORT_DIR = "Maintenance/import"
CHANGES_REL = "Maintenance/changes.md"
ROLE = "Curator"                          # import do Inbox/ dělá Curator (05 kap. 3, zadání 0.16)
FORMATS = ("markdown", "notion-md")
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
