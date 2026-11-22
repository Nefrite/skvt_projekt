"""Příkaz asset_index: kód a data napojené na entity bez zásahu do kódu (zadání 10 kap. 6–9, 13 kap. 7 a 10.2).

Prochází `code_roots` (od kořene projektu), vynechá `ignore` z konfigurace, vault, `_to_delete/`,
`__pycache__/`, `generated/` (jen počet) a soubory podle .gitignore. Pravidla propojení v pořadí 10 kap. 7:
1. hlavička (`hestia:`, `entities`, `docs`, `build_step`, `domains`, `role`),
2. jméno souboru: přesná shoda jména nebo prefixu `<Jméno>_<Part>` s aliasem entity (`rule: alias`, zadání 0.14),
   jinak ID entity nebo její nejdelší prefix (`Palac_Kovarna_Okap.py` -> `Palac_Kovarna`, `rule: name`);
   alias u dvou entit = upozornění a použije se prefix,
3. složka podle `taxonomy_local/folder_map.yaml` (nejdelší shodná cesta),
4. krok ze `build_steps.code` nebo ze složky se jménem kroku,
5. odkaz z dokumentu (`assets:` v dokumentu nebo hubu).
Hlavní entita = první shoda; `entities` = sjednocení hlavičky, jména a tabulky *Kdo používá* sdíleného kódu.
Výstup: `Maintenance/asset_index.json` (pro skripty) a `asset_index.md` (pro člověka) jedním během;
přepisují se jen při změně obsahu (čas `generated` změnu nedělá). Report vypíše změny přiřazení hlavní entity
proti předchozímu indexu (13 kap. 10.2).
"""
from __future__ import annotations

import datetime as _dt
import fnmatch
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import gitinfo
from .changeset import ChangeSet
from .errors import EXIT_OK
from .findings import Finding, sort_findings, to_text
from .fileio import read_text, to_posix
from .headers import read_header
from .links import extract_links, section_text
from .model import Model
from .util import as_list, today, uniq
from .vault import Vault

JSON_REL = "Maintenance/asset_index.json"
MD_REL = "Maintenance/asset_index.md"
ALWAYS_SKIP_DIRS = {".git", "__pycache__", "_to_delete", ".hestia_tmp"}
DATA_SUFFIXES = {".json", ".csv", ".tsv", ".png", ".jpg", ".jpeg", ".exr", ".raw", ".r16", ".tif", ".tiff",
                 ".txt", ".yaml", ".yml", ".xml", ".obj", ".fbx"}
UE_SUFFIXES = {".uasset", ".umap"}
STEP_SCRIPT_RE = re.compile(r"^(step|build_.*)$", re.I)
SHARED_TABLE_HEADER = ["Typ nebo funkce", "Entity", "Kroky"]
ROLE_ORDER = ["spec", "entry", "generator", "data"]


@dataclass
class IndexResult:
    files: list[dict] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    generated_count: int = 0
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------- pomocné čtení

def shared_users(model: Model, note) -> list[str]:
    """Entity z tabulky *Kdo používá* (13 kap. 10.2: pevné záhlaví)."""
    sec = section_text(note.body.replace("\r\n", "\n"), "Kdo používá")
    if not sec:
        return []
    out: list[str] = []
    rows = [line for line in sec.split("\n") if line.strip().startswith("|")]
    if not rows:
        return out
    from .logs import split_row
    if split_row(rows[0]) != SHARED_TABLE_HEADER:
        return out
    for line in rows[2:]:
        cells = split_row(line)
        if len(cells) >= 2:
            out += [l.target for l in extract_links(cells[1])]
    return uniq(model.link_name(f"[[{t}]]") for t in out)


def _norm_dir(p: str) -> str:
    p = p.replace("\\", "/").strip().lstrip("/")
    return p if not p or p.endswith("/") else p + "/"


def guess_role(rel: str) -> str:
    p = Path(rel)
    parts = [x.lower() for x in p.parts]
    suf = p.suffix.lower()
    if "generated" in parts:
        return "output"
    if suf in UE_SUFFIXES or "content" in parts[:-1] and suf in UE_SUFFIXES:
        return "ue_asset"
    if suf in (".py", ".pyw"):
        stem = p.stem.lower()
        if stem == "spec" or stem.endswith("_spec"):
            return "spec"
        if "lib" in parts[:-1]:
            return "library"
        if "generators" in parts[:-1]:
            return "generator"
        if "checks" in parts[:-1]:
            return "check"
        return "entry"
    return "data"


# ---------------------------------------------------------------- sestavení

class Indexer:
    def __init__(self, vault: Vault, model: Model | None = None):
        self.v = vault
        self.m = model or Model(vault)
        self.tx = vault.taxonomy
        self.cfg = vault.config
        self.entities = set(self.m.entities)
        self.entities_lower = {e.lower(): e for e in self.entities}
        self.notes_by_name = {n.name: n for n in vault.notes.values()}
        self.folder_map = sorted(self.tx.folder_map, key=lambda it: -len(_norm_dir(str(it.get("path", "")))))
        self.steps = self.tx.build_steps
        self.doc_refs: dict[str, list] = {}           # cesta od kořene projektu -> [poznámky]
        for n in self.m.notes:
            for a in as_list(n.fm.get("assets")):
                if isinstance(a, str) and a.startswith("/"):
                    self.doc_refs.setdefault(a, []).append(n)
        self.shared = {n.name: shared_users(self.m, n) for n in self.m.notes
                       if n.type == "step" and n.fm.get("step_kind") == "shared"}
        self.aliases, self.alias_warnings = self.entity_aliases()

    def entity_aliases(self) -> tuple[dict[str, str], list[str]]:
        """`aliases` hubů: lower(alias) -> entita; alias u dvou entit se vynechá s upozorněním (10 kap. 4)."""
        seen: dict[str, list[str]] = {}
        for name, n in sorted(self.m.entities.items()):
            for a in as_list(n.fm.get("aliases")):
                key = str(a).strip().lower()
                if key and key != name.lower() and name not in seen.setdefault(key, []):
                    seen[key].append(name)
        out, warnings = {}, []
        for key, ents in sorted(seen.items()):
            if len(ents) == 1:
                out[key] = ents[0]
            else:
                warnings.append(f"alias {key} je u entit {', '.join(ents)}; použije se prefix jména")
        return out, warnings

    # ------------------------------------------------------------ výběr souborů
    def candidates(self) -> tuple[list[Path], int, list[str]]:
        root = self.v.project_root
        warnings = []
        roots = [r for r in as_list(self.cfg.get("code_roots")) if isinstance(r, str)]
        if not roots:
            warnings.append("code_roots v config.yaml je prázdné; index je prázdný")
        patterns = [p for p in as_list(self.cfg.get("ignore")) if isinstance(p, str)]
        vault_roots = {self.v.root.resolve(), self.v.home.resolve()}     # u pracovní kopie i originál
        files, generated = [], 0
        for r in roots:
            base = (root / r).resolve()
            if not base.is_dir():
                warnings.append(f"code_roots: složka neexistuje: {r}")
                continue
            for p in sorted(base.rglob("*")):
                if not p.is_file():
                    continue
                if any(vr == p or vr in p.parents for vr in vault_roots):
                    continue
                rel = to_posix(p.relative_to(root))
                parts = set(Path(rel).parts)
                if parts & ALWAYS_SKIP_DIRS or p.suffix in (".pyc", ".md"):
                    continue
                if "generated" in parts:
                    generated += 1
                    continue
                if any(fnmatch.fnmatch("/" + rel, pat) or fnmatch.fnmatch(rel, pat) for pat in patterns):
                    continue
                files.append(p)
        ign = gitinfo.ignored(root, files)
        return [f for f in uniq(files) if f.resolve() not in ign], generated, warnings

    # ------------------------------------------------------------ jeden soubor
    def step_from_path(self, prel: str) -> str | None:
        """Krok ze `build_steps.code` (nejdelší prefix) nebo ze složky se jménem kroku."""
        best = None
        for sid, st in self.steps.items():
            for c in as_list(st.get("code")):
                c = "/" + _norm_dir(str(c))
                if prel.startswith(c) and (best is None or len(c) > best[0]):
                    best = (len(c), sid)
        if best:
            return best[1]
        for part in Path(prel).parts[:-1]:
            if part in self.steps:
                return part
        return None

    def alias_entity(self, stem: str) -> str | None:
        """Přesná shoda jména souboru nebo jeho prefixu `<Jméno>_<Part>` s aliasem entity (nejdelší první)."""
        parts = stem.split("_")
        for i in range(len(parts), 0, -1):
            hit = self.aliases.get("_".join(parts[:i]).lower())
            if hit:
                return hit
        return None

    def name_entity(self, stem: str) -> str | None:
        parts = stem.split("_")
        for i in range(len(parts), 0, -1):
            cand = "_".join(parts[:i]).lower()
            if cand in self.entities_lower:
                return self.entities_lower[cand]
        return None

    def entry(self, path: Path, out: IndexResult) -> dict:
        prel = self.v.project_rel(path)
        rel = prel.lstrip("/")
        h = read_header(path)
        problems: list[tuple[str, str, str]] = []           # (kód, cíl, zpráva)
        entity, rule = None, None
        entities: list[str] = []
        docs: list[str] = []
        connected_by = None

        # 1) hlavička
        main = h.get("hestia")
        if isinstance(main, str) and main:
            if main in self.entities:
                entity, rule = main, "header"
            elif main in self.notes_by_name:
                docs.append(main)
                connected_by = connected_by or "header"
            else:
                problems.append(("G6", prel, f"hlavička hestia: {main} – entita ani dokument neexistuje"))
        for e in h.list("entities"):
            if e in self.entities:
                entities.append(e)
                connected_by = connected_by or "header"
            else:
                problems.append(("G6", prel, f"hlavička entities: {e} – entita neexistuje"))
        for d in h.list("docs") + h.legacy_docs:
            if d in self.notes_by_name:
                docs.append(d)
                connected_by = connected_by or "header"
            elif d in h.list("docs"):
                problems.append(("G6", prel, f"hlavička docs: {d} – dokument neexistuje"))

        # 2) jméno souboru
        if entity is None and not STEP_SCRIPT_RE.match(path.stem):
            e = self.alias_entity(path.stem)
            if e:
                entity, rule = e, "alias"
            else:
                e = self.name_entity(path.stem)
                if e:
                    entity, rule = e, "name"

        # 3) složka (folder_map)
        fm_item = next((it for it in self.folder_map
                        if rel.startswith(_norm_dir(str(it.get("path", ""))))), None)
        if fm_item and entity is None and fm_item.get("entity") in self.entities:
            entity, rule = fm_item["entity"], "folder"

        # 4) krok
        path_step = (fm_item or {}).get("build_step") or self.step_from_path(prel)
        header_step = h.get("build_step") or None
        if header_step and header_step not in self.steps:
            problems.append(("G7", prel, f"hlavička build_step: {header_step} není v build_steps.yaml"))
        if header_step and path_step and header_step != path_step:
            problems.append(("G7", prel, f"hlavička build_step: {header_step} odporuje složce ({path_step})"))
        step = header_step or path_step
        if step and not connected_by and entity is None:
            connected_by = "step"

        # 5) odkaz z dokumentu
        refs = self.doc_refs.get(prel, [])
        for n in refs:
            if n.type == "entity":
                if entity is None:
                    entity, rule = n.name, "doc"
            else:
                docs.append(n.name)
                ent = self.m.entity_of(n)
                if entity is None and ent in self.entities:
                    entity, rule = ent, "doc"

        # role
        role = h.get("role") or (fm_item or {}).get("role") or guess_role(rel)
        if role not in self.tx.enum_values("asset_role"):
            problems.append(("G7", prel, f"hlavička role: {role} mimo výčet asset_role"))

        # seznam dotčených entit: hlavička, jméno (hlavní entita), Kdo používá sdíleného kódu
        shared = [u for d in docs for u in self.shared.get(d, [])]
        entities = uniq(entities + [entity] + shared)

        domains = h.list("domains") or list((fm_item or {}).get("domains") or [])
        if not domains and step in self.steps:
            cat = self.tx.build_step_catalog.get(self.steps[step].get("type")) or {}
            domains = list(cat.get("domains") or [])
        for d in domains:
            if d not in self.tx.domains:
                problems.append(("G7", prel, f"hlavička domains: {d} mimo výčet domén"))

        if rule is None:
            rule = connected_by if (entities or docs or step) else None
        for code, target, msg in problems:
            out.findings.append(Finding(code, self.tx.severity(code), target, prel, msg))
        return {"path": prel, "role": role, "entity": entity, "entities": entities,
                "build_step": step, "domains": uniq(domains), "rule": rule, "docs": uniq(docs)}

    def build(self) -> IndexResult:
        out = IndexResult()
        files, out.generated_count, out.warnings = self.candidates()
        out.warnings += self.alias_warnings
        out.files = [self.entry(p, out) for p in files]
        out.files.sort(key=lambda f: f["path"])
        return out


def build(vault: Vault, model: Model | None = None) -> IndexResult:
    return Indexer(vault, model).build()


def reassigned(old: dict | None, res: IndexResult) -> list[dict]:
    """Soubory, kterým se proti předchozímu indexu změnila hlavní entita (13 kap. 10.2)."""
    if not old:
        return []
    before = {f.get("path"): f.get("entity") for f in old.get("files") or [] if isinstance(f, dict)}
    return [{"path": f["path"], "from": before[f["path"]], "to": f["entity"], "rule": f["rule"]}
            for f in res.files if f["path"] in before and before[f["path"]] != f["entity"]]


def load_json(vault: Vault) -> dict | None:
    p = vault.root / JSON_REL
    if not p.is_file():
        return None
    try:
        return json.loads(read_text(p))
    except ValueError:
        return None


# ---------------------------------------------------------------- výstupy

def render_json(res: IndexResult, generated: str) -> str:
    rows = ",\n".join("  " + json.dumps(f, ensure_ascii=False) for f in res.files)
    body = f"\n{rows}\n" if rows else ""
    return (f'{{"generated": {json.dumps(generated)}, "project_root": "/", '
            f'"generated_files": {res.generated_count}, "files": [{body}]}}\n')


def _cell(v) -> str:
    if v is None or v == []:
        return "–"
    if isinstance(v, list):
        return ", ".join(v)
    return str(v).replace("|", "\\|")


def render_md(res: IndexResult, day: _dt.date) -> str:
    lines = ["---", "# orchestrace", "type: reference", "validity: valid", f"updated: {day.isoformat()}", "---",
             "# Asset index", "",
             "Generuje skript `asset_index` (zadání 10, kap. 8); **needitovat**. Skripty čtou `asset_index.json`.",
             f"Soubory ve `generated/`: {res.generated_count} (jen počet).", "",
             "| path | role | entity | entities | build_step | domains | rule | docs |",
             "|---|---|---|---|---|---|---|---|"]
    for f in res.files:
        lines.append("| `" + f["path"] + "` | " + " | ".join(_cell(f[k]) for k in
                     ("role", "entity", "entities", "build_step", "domains", "rule", "docs")) + " |")
    return "\n".join(lines) + "\n"


def _strip_generated_time(text: str | None) -> str | None:
    return re.sub(r'"generated": "[^"]*"', '"generated": ""', text) if text else text


def plan(vault: Vault, res: IndexResult, cs: ChangeSet, now: _dt.datetime | None = None) -> bool:
    """Naplánuje zápis obou výstupů; False, když se obsah nemění."""
    jp, mp = vault.root / JSON_REL, vault.root / MD_REL
    day = today()
    now = now or _dt.datetime.combine(day, _dt.datetime.now().time()).replace(microsecond=0)
    new_json = render_json(res, now.isoformat())
    old_json = cs.current(jp)
    if old_json is not None and _strip_generated_time(old_json) == _strip_generated_time(new_json):
        return False
    cs.write(jp, new_json)
    old_md = cs.current(mp)
    new_md = render_md(res, day)
    if old_md is not None and old_md.split("---", 2)[-1] == new_md.split("---", 2)[-1]:
        new_md = old_md
    cs.write(mp, new_md)
    return True


def run(args, vault: Vault) -> tuple[int, dict, str]:
    res = build(vault)
    moved = reassigned(load_json(vault), res)
    cs = ChangeSet(vault.project_root)
    changed = plan(vault, res, cs)
    if args.apply and changed:
        cs.apply()
    findings = sort_findings(res.findings)
    payload = {"command": "asset_index", "applied": bool(args.apply and changed), "changed": changed,
               "files": len(res.files), "generated_files": res.generated_count,
               "unlinked": [f["path"] for f in res.files if not f["entities"] and not f["docs"]],
               "reassigned": moved, "findings": [f.as_dict() for f in findings], "warnings": res.warnings}
    roles: dict = {}
    for f in res.files:
        roles[f["role"]] = roles.get(f["role"], 0) + 1
    state = ("zapsáno" if args.apply else "zapsalo by se (dry-run, zapiš s --apply)") if changed else "beze změny"
    lines = [f"asset_index: {len(res.files)} souborů ({', '.join(f'{k} {v}' for k, v in sorted(roles.items()))}); "
             f"{JSON_REL} a .md {state}"]
    if payload["unlinked"]:
        lines.append("Bez napojení na entitu ani dokument: " + ", ".join(payload["unlinked"]))
    lines += [f"Změna přiřazení: {m['path']}: {m['from'] or '–'} -> {m['to'] or '–'} ({m['rule'] or '–'})"
              for m in moved]
    lines += [f"Upozornění: {w}" for w in res.warnings]
    if findings:
        lines.append(to_text(findings))
    return EXIT_OK, payload, "\n".join(lines)          # nálezy hlaviček hlásí lint a audit
