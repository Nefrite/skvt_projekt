"""Příkaz frontmatter: migrace existující dokumentace podle mapovacího souboru (zadání 13 kap. 10.1, 06 kap. 3–4).

Mapovací soubor (`--map`) je zároveň schvalovací podklad [R1]: jedna položka = jedna schválená změna.
Postup jednoho běhu (dry-run vypíše vše, `--apply` provede):
1. přesuny (jen s `--move` a jen položky s `target`): bez přepsání cíle, řádek do `changes.md` (zdroj: migrace);
2. frontmatter: doplnit chybějící klíče, existující hodnoty jen s `--force`; řádkový zápis; `updated` z mtime
   při prvním doplnění; tělo se nemění;
3. převod odkazů `` `soubor.md` `` / `` `..\\cesta\\soubor.md` `` na wikilinky, už proti novým umístěním;
   jen existující a jednoznačné cíle, mimo bloky kódu; ostatní beze změny do reportu;
   jméno se hledá i v `aliases` (včetně nastavených mapou); cesta, která od složky souboru nevede, se zkusí
   jako jedinečné jméno; existující soubor mimo vault = „cíl mimo vault“ (zadání 0.13.6);
   obrázky a `[text](cesta)` na ne-MD soubory: cíl ve vaultu → `![[jméno]]`, cíl mimo vault → relativní
   cesta od nového umístění dokumentu a report „mimo vault“ (02 kap. 7, pravidlo 6);
   zmínka ne-MD souboru v backtickách: soubor přesunutý mapou → odkaz `[[jméno]]` (i náhradně jedinečným
   jménem, když cesta nevede), u kódu text + report (0.13.7, 0.13.8);
4. report: přesunuté, doplněné klíče, nejednoznačné odkazy, položky `split` jako úkoly.
Pravidla mapy (zadání 0.13.4): každý `source` jen jednou (jinak chyba mapy, kód 2); `split: true` s `target`
= běžný přesun a frontmatter + úkol rozpadu, `split: true` bez `target` = zůstává na místě, jen úkol.
Ne-MD položky (zadání 0.13.6): jen přesun do `Attachments/`, bez frontmatteru (jinak chyba mapy).
Opakované spuštění nic nemění (přesunutá položka se pozná podle existujícího cíle a chybějícího zdroje).
"""
from __future__ import annotations

import datetime as _dt
import os
import posixpath
import re
from urllib.parse import quote, unquote
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from .changeset import ChangeSet
from .errors import EXIT_OK, UsageError, WriteConflict
from .fileio import detect_newline, to_posix
from .frontmatter import FrontmatterError, format_value, parse, set_field
from .logs import append_lines, format_line
from .taxonomy import load_yaml
from .util import today
from .vault import Vault

CHANGES_REL = "Maintenance/changes.md"
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_MD_REF_RE = re.compile(r"`([^`\n]*?\.md)`")
_CODE_SPAN_RE = re.compile(r"(`[^`\n]*`)")
_MD_LINK_RE = re.compile(r'(!?)\[([^\]\n]*)\]\(\s*(<[^>\n]+>|[^)\s]+)(\s+"[^"\n]*")?\s*\)')
_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
ATTACHMENTS = "Attachments"
OUTSIDE = "mimo vault, Obsidian ho nevykreslí"
OUTSIDE_MENTION = "mimo vault, zmínka zůstává textem"
_FILE_MENTION_RE = re.compile(r"`([^`\s]+\.[A-Za-z0-9]{1,8})`")
_PROJECT_SKIP = {".git", ".obsidian", ".trash", "__pycache__", "_to_delete", "node_modules"}


def is_md(path: str) -> bool:
    return path.strip().lower().endswith(".md")


def _as_list(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    return [str(v) for v in value] if isinstance(value, list) else []


@dataclass
class ItemReport:
    source: str
    target: str | None
    path: Path | None = None
    moved: bool = False
    added: list = field(default_factory=list)
    replaced: list = field(default_factory=list)
    kept: list = field(default_factory=list)            # existující hodnoty, které mapa chtěla změnit (bez --force)
    links: list = field(default_factory=list)           # převedené odkazy
    unresolved: list = field(default_factory=list)      # (odkaz, důvod)
    outside: list = field(default_factory=list)         # (cesta v textu, nový text, důvod): ne-MD soubor mimo vault
    note: str = ""
    problem: str = ""


def source_key(source: str) -> str:
    """Normalizovaný zdroj pro porovnání položek (oddělovače, `./`, `..`, úvodní `/`)."""
    return posixpath.normpath(source.strip().replace("\\", "/").lstrip("/"))


def load_map(path: Path) -> list[dict]:
    if not path.is_file():
        raise UsageError(f"Mapovací soubor neexistuje: {path}")
    data = load_yaml(path) or {}
    if not isinstance(data, dict) or data.get("hestia_migration") != 1:
        raise UsageError(f"{path}: očekávám hestia_migration: 1")
    items = data.get("items")
    if not isinstance(items, list):
        raise UsageError(f"{path}: klíč items musí být seznam")
    for i, it in enumerate(items, 1):
        if not isinstance(it, dict) or not isinstance(it.get("source"), str) or not it["source"].strip():
            raise UsageError(f"{path}: položka {i} nemá source")
        if it.get("frontmatter") is not None and not isinstance(it["frontmatter"], dict):
            raise UsageError(f"{path}: položka {i}: frontmatter musí být mapa")
        if not is_md(it["source"]):                      # ne-MD položka: jen přesun do Attachments/ (0.13.6)
            if it.get("frontmatter"):
                raise UsageError(f"{path}: položka {i}: ne-MD soubor nemá frontmatter ({it['source']})")
            tgt = source_key(str(it.get("target") or ""))
            if it.get("target") and not tgt.startswith(ATTACHMENTS + "/"):
                raise UsageError(f"{path}: položka {i}: ne-MD soubor patří do {ATTACHMENTS}/ ({it['target']})")
    seen: dict[str, int] = {}
    for i, it in enumerate(items, 1):
        key = source_key(it["source"])
        if key in seen:
            raise UsageError(f"{path}: položka {i}: source už je v položce {seen[key]} ({it['source']})")
        seen[key] = i
    return items


class Migration:
    def __init__(self, vault: Vault, items: list[dict], move: bool, force: bool):
        self.v = vault
        self.items = items
        self.move = move
        self.force = force
        self.day = today()
        self.tx = vault.taxonomy
        self.cs = ChangeSet(vault.project_root)
        self.reports: list[ItemReport] = []
        self.tasks: list[str] = []
        self.log_lines: list[str] = []
        self.location: dict[Path, Path] = {}             # původní cesta -> nová (pro převod odkazů)
        self.aliases: dict[str, list[Path]] = {}         # lower(alias) -> [cesty .md ve vaultu po přesunech]
        self._vault_files: dict[str, list[Path]] | None = None    # lower(jméno s příponou) -> [cesty]
        self._project_files: set[str] | None = None      # lower(jméno s příponou) souborů projektu mimo vault
        self._mapped: dict[str, list[Path]] | None = None          # ne-MD soubory přesunuté mapou do vaultu

    # ------------------------------------------------------------ cesty
    def project_path(self, p: str) -> Path:
        return (self.v.project_root / p.replace("\\", "/").lstrip("/")).resolve()

    def vault_path(self, p: str) -> Path:
        return (self.v.root / p.replace("\\", "/").lstrip("/")).resolve()

    def vault_names(self) -> dict[str, list[Path]]:
        """Jména .md ve vaultu po přesunech: lower(jméno) -> [cesty]."""
        names: dict[str, list[Path]] = {}
        moved_from = {s for s, _d, _h in self.cs.moves}
        paths = [n.path.resolve() for n in self.v.notes.values() if n.path.resolve() not in moved_from]
        paths += [d for _s, d, _h in self.cs.moves if self.v.root.resolve() in d.parents and is_md(d.name)]
        for p in paths:
            names.setdefault(p.stem.lower(), []).append(p)
        return names

    def in_vault(self, p: Path) -> bool:
        return self.v.root.resolve() in p.parents

    def vault_aliases(self, by_src: dict) -> dict[str, list[Path]]:
        """`aliases` dokumentů ve vaultu po přesunech, včetně nastavených mapou v témže běhu (06 kap. 4)."""
        out: dict[str, list[Path]] = {}
        moved = {s: d for s, d, _h in self.cs.moves}

        def add(values, p: Path) -> None:
            for a in _as_list(values):
                key = a.strip()
                key = (key[:-3] if is_md(key) else key).lower()
                if key and p not in out.setdefault(key, []):
                    out[key].append(p)
        for n in self.v.notes.values():
            p = moved.get(n.path.resolve(), n.path.resolve())
            if isinstance(n.fm, dict) and self.in_vault(p):
                add(n.fm.get("aliases"), p)
        for rep in self.reports:
            if rep.path is None or not is_md(rep.path.name) or not self.in_vault(rep.path):
                continue
            add((by_src[self.project_path(rep.source)].get("frontmatter") or {}).get("aliases"), rep.path)
            try:
                fm, _sp = parse(self.cs.current(rep.path) or "")
            except FrontmatterError:
                fm = None
            if isinstance(fm, dict):
                add(fm.get("aliases"), rep.path)
        return out

    def vault_files(self) -> dict[str, list[Path]]:
        """Všechny soubory vaultu po přesunech: lower(jméno s příponou) -> [cesty] (pro `![[jméno]]`)."""
        if self._vault_files is None:
            moved_from = {s for s, _d, _h in self.cs.moves}
            paths = [p for p in (self.v.root / f for f in self.v.files) if p.resolve() not in moved_from]
            paths += [d for _s, d, _h in self.cs.moves if self.in_vault(d)]
            self._vault_files = {}
            for p in paths:
                self._vault_files.setdefault(p.name.lower(), []).append(p.resolve())
        return self._vault_files

    def project_files(self) -> set[str]:
        """Jména souborů projektu mimo vault, které se nepřesouvají: lower(jméno s příponou)."""
        if self._project_files is None:
            root, vroot = self.v.project_root.resolve(), self.v.root.resolve()
            moved_from = {s for s, _d, _h in self.cs.moves}
            self._project_files = set()
            for d, dirs, files in os.walk(root):
                dirs[:] = [x for x in dirs if x not in _PROJECT_SKIP and (Path(d) / x).resolve() != vroot]
                for f in files:
                    if (Path(d) / f).resolve() not in moved_from:
                        self._project_files.add(f.lower())
        return self._project_files

    def project_md(self) -> set[str]:
        """Jména .md souborů projektu mimo vault, které se nepřesouvají (důvod „cíl mimo vault“)."""
        return {f[:-3] for f in self.project_files() if is_md(f)}

    def mapped_files(self) -> dict[str, list[Path]]:
        """Ne-MD soubory, které do vaultu přesunula mapa (v tomto nebo dřívějším běhu): lower(jméno) -> [cesty].
        Jediný cíl zmínky ne-MD souboru v backtickách (06 kap. 4, zadání 0.13.8)."""
        if self._mapped is None:
            self._mapped = {}
            for rep in self.reports:
                if rep.path is not None and not is_md(rep.path.name) and self.in_vault(rep.path):
                    self._mapped.setdefault(rep.path.name.lower(), []).append(rep.path.resolve())
        return self._mapped

    # ------------------------------------------------------------ 1. přesuny
    def plan_moves(self) -> None:
        for it in self.items:
            src = self.project_path(it["source"])
            rep = ItemReport(it["source"], it.get("target") or None, note=str(it.get("note") or ""))
            self.reports.append(rep)
            if it.get("split"):
                self.tasks.append(f"rozpad {it['source']}: {it.get('note') or 'rozdělit podle mapy'}")
                if not it.get("target"):                 # bez cíle zůstává na místě, jen úkol
                    rep.problem = "split: rozpad dělá člověk nebo agent"
                    continue
            tgt = self.vault_path(it["target"]) if it.get("target") else None
            if tgt is not None and self.move:
                if src.is_file() and not tgt.exists():
                    try:
                        self.cs.move(src, tgt)
                    except WriteConflict as exc:
                        rep.problem = str(exc)
                        continue
                    rep.moved = True
                    self.location[src] = tgt
                    self.log_lines.append(format_line([self.day.isoformat(), "migrace",
                                                       to_posix(tgt.relative_to(self.v.root)),
                                                       f"přesun z {it['source']}", "migrace"]))
                    rep.path = tgt
                elif tgt.is_file() and not src.exists():
                    rep.path = tgt                       # už přesunuto dřívějším během
                    self.location[src] = tgt
                elif src.is_file() and tgt.exists():
                    rep.problem = f"cíl už existuje, nepřesouvám: {it['target']}"
                    rep.path = src
                else:
                    rep.problem = f"zdroj neexistuje: {it['source']}"
            elif tgt is not None and not src.exists() and tgt.is_file():
                rep.path = tgt
                self.location[src] = tgt
            elif src.is_file():
                rep.path = src
                if tgt is not None:
                    rep.problem = "target bez --move: zůstává na místě"
            else:
                rep.problem = f"zdroj neexistuje: {it['source']}"

    # ------------------------------------------------------------ 2. frontmatter
    def section_of(self, key: str, fm_type: str | None) -> str:
        fd, _d = self.tx.field_for_key(key)
        return fd.section_for(fm_type or "") if fd else "game"

    def apply_frontmatter(self, rep: ItemReport, wanted: dict, text: str) -> str:
        try:
            fm, sp = parse(text)
        except FrontmatterError as exc:
            rep.problem = f"neplatný frontmatter, přeskakuji: {exc}"
            return text
        wanted = dict(wanted)
        if fm is None or "updated" not in fm:
            if "updated" not in wanted:
                src = self.cs._moved_to.get(rep.path, rep.path)
                wanted["updated"] = _dt.date.fromtimestamp(src.stat().st_mtime)
        if fm is None:
            return self.new_frontmatter(rep, wanted, text)
        t = wanted.get("type") if "type" not in fm or self.force else fm.get("type")
        for key, value in wanted.items():
            if key in fm and fm[key] not in (None, "", []):
                if fm[key] == value or (str(fm[key]) == str(value)):
                    continue
                if not self.force:
                    rep.kept.append(key)
                    continue
                rep.replaced.append(key)
            else:
                rep.added.append(key)
            text = set_field(text, key, value, section=self.section_of(key, t))
        return text

    def new_frontmatter(self, rep: ItemReport, wanted: dict, text: str) -> str:
        nl = detect_newline(text)
        t = wanted.get("type")
        orch = [k for k in wanted if self.section_of(k, t) == "orchestration"]
        game = [k for k in wanted if k not in orch]
        lines = ["---", "# orchestrace"] + [f"{k}: {format_value(wanted[k])}".rstrip() for k in orch]
        if game:
            lines += ["# hra"] + [f"{k}: {format_value(wanted[k])}".rstrip() for k in game]
        lines.append("---")
        rep.added += list(wanted)
        bom = "﻿" if text.startswith("﻿") else ""
        return bom + nl.join(lines) + nl + text[len(bom):]

    # ------------------------------------------------------------ 3. odkazy
    def resolve_ref(self, ref: str, orig: Path, names: dict) -> tuple[str | None, str]:
        raw = ref.strip().replace("\\", "/")
        name = PurePosixPath(raw).stem
        if "/" in raw or raw.startswith(".."):
            cand = (orig.parent / raw).resolve()
            cand = self.location.get(cand, cand)
            if cand.is_file() or self.cs.exists(cand):
                if not self.in_vault(cand):
                    return None, "cíl mimo vault"
                return self.wikilink(cand, names), "ok"
            # cesta od složky souboru nevede (např. od kořene prototypu): jedinečné jméno (zadání 0.13.6)
        hits = list(dict.fromkeys(names.get(name.lower(), []) + self.aliases.get(name.lower(), [])))
        if len(hits) == 1:
            return self.wikilink(hits[0], names), "ok"
        if hits:
            return None, "nejednoznačný název: " + ", ".join(sorted(to_posix(h.relative_to(self.v.root))
                                                                    for h in hits))
        if (orig.parent / raw).resolve().is_file() or name.lower() in self.project_md():
            return None, "cíl mimo vault"
        return None, "cíl neexistuje"

    def wikilink(self, path: Path, names: dict) -> str:
        """`[[jméno]]`, je-li jméno souboru ve vaultu jedinečné, jinak cesta od kořene vaultu."""
        if len(names.get(path.stem.lower(), [])) == 1:
            return f"[[{path.stem}]]"
        return f"[[{to_posix(path.relative_to(self.v.root.resolve()))[:-3]}]]"

    def convert_file_link(self, rep: ItemReport, mm: re.Match, bases: list[Path]) -> str:
        """Obrázek nebo `[text](cesta)` na ne-MD soubor (06 kap. 4; 02 kap. 7, pravidlo 6)."""
        bang, label, target, title = mm.group(1), mm.group(2), mm.group(3), mm.group(4) or ""
        angle = target.startswith("<")
        raw = target[1:-1] if angle else target
        if _SCHEME_RE.match(raw) or raw.startswith(("#", "/")) or "#" in raw or is_md(raw):
            return mm.group(0)
        cand = self.find_file(unquote(raw), bases)
        if cand is None:
            rep.unresolved.append((raw, "cíl neexistuje"))
            return mm.group(0)
        if self.in_vault(cand):
            name = self.file_name(cand)
            link = f"![[{name}]]" if bang else (f"[[{name}|{label}]]" if label else f"[[{name}]]")
            rep.links.append(f"{mm.group(0)} -> {link}")
            return link
        new = to_posix(Path(os.path.relpath(cand, rep.path.parent)))
        new = f"<{new}>" if angle else quote(new, safe="/.-_~()!$&'*+,;=:@")
        rep.outside.append((raw, new, OUTSIDE))
        return f"{bang}[{label}]({new}{title})"

    def find_file(self, raw: str, bases: list[Path]) -> Path | None:
        """Soubor podle cesty od `bases` (po přesunech), jinak None."""
        rel = raw.strip().replace("\\", "/")
        for base in bases:
            c = (base / rel).resolve()
            c = self.location.get(c, c)
            if self.cs.exists(c):
                return c
        return None

    def file_name(self, path: Path) -> str:
        """Jméno ne-MD souboru ve vaultu pro wikilink: jedinečné jméno s příponou, jinak cesta od kořene."""
        if len(self.vault_files().get(path.name.lower(), [])) == 1:
            return path.name
        return to_posix(path.relative_to(self.v.root.resolve()))

    def convert_file_mention(self, rep: ItemReport, span: str, bases: list[Path]) -> str:
        """Zmínka ne-MD souboru v backtickách (06 kap. 4, zadání 0.13.7, 0.13.8): soubor přesunutý mapou do
        vaultu → odkaz `[[jméno]]` (ne vložení); jiný soubor vaultu (např. `_core/`) se nehledá; soubor u kódu →
        beze změny a do reportu; jiný text (kód, neexistující soubor) beze změny."""
        mm = _FILE_MENTION_RE.fullmatch(span)
        if not mm or is_md(mm.group(1)) or _SCHEME_RE.match(mm.group(1)):
            return span
        raw = mm.group(1)
        mapped = self.mapped_files()
        moved = {p for ps in mapped.values() for p in ps}
        cand = self.find_file(raw, bases)
        if cand is not None and self.in_vault(cand) and cand not in moved:
            cand = None                                  # soubor vaultu, který migrace nepřesunula
        if cand is None:                                 # cesta nevede (i s `\`): jedinečné jméno mezi přesunutými
            name = PurePosixPath(raw.replace("\\", "/")).name.lower()
            hits = mapped.get(name, [])
            if len(hits) == 1:
                cand = hits[0]
            elif hits:
                rep.unresolved.append((raw, "nejednoznačný název: " + ", ".join(
                    sorted(to_posix(h.relative_to(self.v.root.resolve())) for h in hits))))
                return span
            elif name in self.project_files():           # soubor toho jména u kódu
                rep.outside.append((raw, span, OUTSIDE_MENTION))
                return span
            else:
                return span
        if self.in_vault(cand):
            link = f"[[{self.file_name(cand)}]]"
            rep.links.append(f"{span} -> {link}")
            return link
        rep.outside.append((raw, span, OUTSIDE_MENTION))
        return span

    def convert_links(self, rep: ItemReport, text: str, orig: Path, names: dict) -> str:
        sp_text = text
        try:
            _fm, sp = parse(text)
            head = text[:len(text) - len(sp.body)] if sp.has_frontmatter else ""
            body = sp.body if sp.has_frontmatter else text
        except FrontmatterError:
            head, body = "", sp_text
        # ne-MD soubory jen u dokumentu ve vaultu; text je relativní k původnímu umístění, při opakovaném
        # běhu (dokument přesunut dřív) k současnému – zkusí se obojí
        files = self.in_vault(rep.path)
        bases = [orig.parent, rep.path.parent] if rep.moved else [rep.path.parent, orig.parent]
        out, fence = [], None
        for line in body.splitlines(keepends=True):
            m = _FENCE_RE.match(line)
            if fence:
                fence = None if (m and m.group(1) == fence) else fence
                out.append(line)
                continue
            if m:
                fence = m.group(1)
                out.append(line)
                continue

            def repl(mm):
                link, status = self.resolve_ref(mm.group(1), orig, names)
                if status == "ok":
                    rep.links.append(f"{mm.group(0)} -> {link}")
                    return link
                rep.unresolved.append((mm.group(1), status))
                return mm.group(0)
            parts = _CODE_SPAN_RE.split(line)           # liché části = `…` (odkazy na .md), sudé = text
            for i, part in enumerate(parts):
                if i % 2:
                    parts[i] = _MD_REF_RE.sub(repl, part)
                    if files and parts[i] == part:
                        parts[i] = self.convert_file_mention(rep, part, bases)
                elif files:
                    parts[i] = _MD_LINK_RE.sub(lambda mm: self.convert_file_link(rep, mm, bases), part)
            out.append("".join(parts))
        return head + "".join(out)

    # ------------------------------------------------------------ běh
    def plan(self) -> None:
        self.plan_moves()
        names = self.vault_names()
        by_src = {self.project_path(it["source"]): it for it in self.items}
        self.aliases = self.vault_aliases(by_src)
        for rep in self.reports:
            if rep.path is None or not is_md(rep.path.name):   # ne-MD položka: jen přesun
                continue
            it = by_src[self.project_path(rep.source)]
            text = self.cs.current(rep.path)
            if text is None:
                continue
            new = self.apply_frontmatter(rep, it.get("frontmatter") or {}, text)
            new = self.convert_links(rep, new, self.project_path(rep.source), names)
            self.cs.write(rep.path, new)
        if self.log_lines:
            cpath = self.v.root / CHANGES_REL
            cur = self.cs.current(cpath)
            if cur is None:
                raise UsageError(f"{CHANGES_REL} neexistuje")
            self.cs.write(cpath, append_lines(cur, self.log_lines, today=self.day))


def run(args, vault: Vault) -> tuple[int, dict, str]:
    items = load_map(Path(args.map))
    mig = Migration(vault, items, args.move, args.force)
    mig.plan()
    if args.apply and not mig.cs.empty:
        mig.cs.apply()
    reps = mig.reports
    payload = {"command": "frontmatter", "applied": bool(args.apply and not mig.cs.empty),
               "items": [{"source": r.source, "path": mig.cs.rel(r.path) if r.path else None, "moved": r.moved,
                          "added": r.added, "replaced": r.replaced, "kept": r.kept, "links": r.links,
                          "unresolved": [{"ref": a, "reason": b} for a, b in r.unresolved],
                          "outside": [{"ref": a, "link": b, "reason": c} for a, b, c in r.outside],
                          "problem": r.problem} for r in reps],
               "tasks": mig.tasks, "writes": mig.cs.summary()}
    lines = [f"frontmatter: {len(reps)} položek, přesunuto {sum(r.moved for r in reps)}, "
             f"soubory se změnou {len(mig.cs.edits)}" + ("" if args.apply else " (dry-run, zapiš s --apply)")]
    for r in reps:
        where = mig.cs.rel(r.path) if r.path else "–"
        bits = []
        if r.moved:
            bits.append("přesun")
        if r.added:
            bits.append("doplněno: " + ", ".join(r.added))
        if r.replaced:
            bits.append("přepsáno (--force): " + ", ".join(r.replaced))
        if r.kept:
            bits.append("ponecháno (jiná hodnota, bez --force): " + ", ".join(r.kept))
        if r.links:
            bits.append(f"odkazy {len(r.links)}")
        lines.append(f"- {r.source} -> {where}: {'; '.join(bits) or 'beze změny'}"
                     + (f" [{r.problem}]" if r.problem else ""))
        lines += [f"    nepřevedený odkaz {a}: {b}" for a, b in r.unresolved]
        lines += [f"    soubor {a}" + (f" -> {b}" if c == OUTSIDE else "") + f": {c}" for a, b, c in r.outside]
    if mig.tasks:
        lines.append("Úkoly (skript neprovádí):")
        lines += [f"  - [ ] {t}" for t in mig.tasks]
    if not args.apply and not mig.cs.empty:
        lines += ["Diff:", mig.cs.diff(full_new=True).rstrip()]
    return EXIT_OK, payload, "\n".join(lines)
