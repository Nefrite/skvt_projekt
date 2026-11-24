"""Příkaz task_close: uzavření tasku za minutu (zadání 13 kap. 10.5, 12 kap. 5).

1. Dotčené entity se odvodí samy: změněné soubory (git, nebo zadané argumentem) -> `asset_index.json`
   (kód, data) a pole `entity` změněných poznámek; plus `--entity`.
2. Řádek do `changes.md` za každou entitu (`--change ENTITA="text"` má přednost před `--note`); řádek, který už
   v souboru je (datum, role bez ohledu na velikost písmen, entita, text), se znovu nepřidá (zadání 0.18.1, 0.19.1);
   `updated` u změněných poznámek; `--archive-handover` archivuje splněné předání bez otevřených otázek (jinak jen s `--force`).
3. [R5] `hubs` pro dotčené entity, `doc_index` (jen při změně dokumentů, zadání 0.18.1), `lint` změněných souborů,
   G11 pro dotčené entity.
4. Kontrolní seznam toho, co skript neudělá, ale nesmí se zapomenout.
Dry-run vypíše diff a výsledky kontrol; `--apply` zapíše (změny, pak huby nad novým stavem).
Návratový kód 1, když lint najde chybu ve změněných souborech (task není hotový, 13 kap. 3); upozornění 0.

Výkon (zadání 0.28, CR-033; 13 kap. 10.21): vault se načítá líně; entity a změny se odvodí jen z dotčených
souborů (existence entity = její hub), po zápisu se vault čte jednou pro huby, `doc_index` i kontroly. Po každém
kroku (`writes`, `hubs`, `doc_index`, `checks`) se hlídá `task_close_seconds` (výchozí 150): po překročení
příkaz skončí s výpisem nedokončených kroků a uloží `Maintenance/task_close_resume.json`; `task_close --resume`
je dokončí. Každý krok se zapíše celý (sada změn), nic napůl.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from . import asset_index as ai
from . import doc_index
from . import gitinfo
from .audit import Auditor, load_state
from .blocks import strip_generated
from .changeset import ChangeSet
from .errors import EXIT_FINDINGS, EXIT_OK, UsageError
from .findings import has_errors, sort_findings, to_text
from .frontmatter import set_field
from .fileio import to_posix
from .hubs import Hubs
from .lint import header_findings, split_targets
from .logs import format_line
from .model import LinkResolver, Model
from .util import today, uniq
from .validate import run_checks
from .vault import LINT_EXCLUDE_PREFIXES, Vault

CHANGES_REL = "Maintenance/changes.md"
RESUME_REL = "Maintenance/task_close_resume.json"
STEPS = ["writes", "hubs", "doc_index", "checks"]
ARCHIVE_DIR = "Handovers/_archive"
# poznámky, které task_close nebere jako „změněný dokument“ (logy, fronta, generované přehledy)
SKIP_NOTES = ("Maintenance/", "Dashboard/Index.md")
QUESTION_RE = re.compile(r"^\s*[-*]\s+\[ \]\s+(.+)$")


def parse_changes(items: list[str]) -> dict[str, str]:
    out = {}
    for raw in items:
        if "=" not in raw:
            raise UsageError(f'--change očekává ENTITA="text", je {raw!r}')
        k, v = raw.split("=", 1)
        if not k.strip() or not v.strip():
            raise UsageError(f'--change očekává ENTITA="text", je {raw!r}')
        out[k.strip()] = v.strip()
    return out


class TaskClose:
    def __init__(self, vault: Vault, args):
        self.v = vault
        self.args = args
        self.day = today()
        self.links = LinkResolver(vault)             # bez čtení celého vaultu (zadání 0.28, CR-033)
        self.index = ai.load_json(vault)
        self.warnings: list[str] = []
        self.checklist: list[str] = []
        self.skipped: list[str] = []                 # řádky changes.md, které už v souboru jsou

    # ------------------------------------------------------------ 1. dotčené soubory a entity
    def changed(self) -> tuple[list, list[Path]]:
        if self.args.files:
            paths = [(Path(f) if Path(f).is_absolute() else Path.cwd() / f).resolve() for f in self.args.files]
        else:
            paths = gitinfo.changed_files(self.v.project_root)
            if paths is None:
                self.warnings.append("projekt není v gitu; dotčené entity jen z --entity a zadaných souborů")
                paths = []
        notes, code = split_targets(self.v, paths, strict=bool(self.args.files))
        notes = [n for n in notes if not n.rel.startswith(SKIP_NOTES)]
        if not self.args.files:
            notes = [n for n in notes if not self.only_generated(n)]
        return notes, code

    @staticmethod
    def only_generated(n) -> bool:
        """Změna jen uvnitř bloků hestia:generated (skript hubs) není změna dokumentu."""
        old = gitinfo.head_text(n.path)
        if old is None:
            return False
        return strip_generated(old.replace("\r\n", "\n")) == strip_generated(n.text.replace("\r\n", "\n"))

    def entities_of(self, notes, code) -> list[str]:
        out: list[str] = []
        by_path = {f["path"]: f for f in (self.index or {}).get("files") or []}
        if code and self.index is None:
            self.warnings.append("asset_index.json chybí; entity z kódu nejde odvodit (spusť asset_index)")
        for p in code:
            f = by_path.get(self.v.project_rel(p))
            if f is None:
                if self.index is not None:
                    self.warnings.append(f"{self.v.project_rel(p)} není v asset_index.json (spusť asset_index)")
                continue
            out += f.get("entities") or []
        for n in notes:
            if n.type == "entity":
                out.append(n.name)
            else:
                out += [e for e in self.links.link_names((n.fm or {}).get("entity")) if self.is_entity(e)]
        for e in self.args.entity:
            if not self.is_entity(e):
                raise UsageError(f"--entity {e}: entita neexistuje")
            out.append(e)
        return uniq(out)

    def is_entity(self, name: str) -> bool:
        """Entita existuje: poznámka toho jména je hub (`type: entity`); čte se jen ona (zadání 0.28)."""
        n = self.v.note_by_name(name)
        return n is not None and n.name == name and n.type == "entity" \
            and not n.rel.startswith(LINT_EXCLUDE_PREFIXES)

    # ------------------------------------------------------------ 2. zápisy
    def plan_writes(self, cs: ChangeSet, notes, entities: list[str]) -> list[str]:
        per = parse_changes(self.args.change)
        unknown = [e for e in per if e not in entities]
        if unknown:
            raise UsageError(f"--change pro entitu, která není dotčená (doplň --entity): {', '.join(unknown)}")
        missing = [e for e in entities if e not in per and not self.args.note]
        if missing:
            raise UsageError(f"Chybí popis změny (--note nebo --change) pro: {', '.join(missing)}")
        lines = [format_line([self.day.isoformat(), self.args.role, e, per.get(e, self.args.note), self.args.source])
                 for e in entities]
        for name in self.args.archive_handover:
            lines.append(self.plan_archive(cs, name))
        from .logs import append_lines, log_entries, split_row
        cpath = self.v.root / CHANGES_REL
        text = cs.current(cpath)
        if text is None:
            raise UsageError(f"{CHANGES_REL} neexistuje")
        # řádek, který už v changes.md je (datum, role, entita, text), se nezdvojí: druhé uzavření téhož stavu
        # (Knihovník, pak orchestrační agent) s jiným zdrojem (12 kap. 5, 13 kap. 10.5; zadání 0.18.1); roli porovná
        # bez ohledu na velikost písmen, aby se sloučily i starší ruční řádky `librarian` (zadání 0.19.1)
        def key(row: list[str]) -> tuple:
            row = (row + [""] * 4)[:4]
            return (row[0], row[1].casefold(), row[2], row[3])

        present = {key(row) for row in log_entries(text)}
        self.skipped = [ln for ln in lines if key(split_row(ln)) in present]
        lines = [ln for ln in lines if ln not in self.skipped]
        cs.write(cpath, append_lines(text, lines, today=self.day))
        for n in notes:
            if n.fm is None or str(n.fm.get("updated")) == self.day.isoformat():
                continue
            if n.path.resolve() in {s for s, _d, _h in cs.moves}:
                continue                      # archivované předání: updated nastavil plan_archive
            cur = cs.current(n.path)
            cs.write(n.path, set_field(cur, "updated", self.day, section="orchestration"))
        return lines

    def plan_archive(self, cs: ChangeSet, name: str) -> str:
        n = self.v.note_by_name(name)
        if n is None or not n.fm or n.fm.get("type") != "handover":
            raise UsageError(f"--archive-handover {name}: předání nenalezeno")
        if n.rel.startswith(ARCHIVE_DIR + "/"):
            raise UsageError(f"--archive-handover {name}: už je archivované")
        reasons = []
        if not Model.handover_fulfilled(n):
            reasons.append("sekce Zbývá má otevřené položky" if Model.has_remaining(n)
                           else "sekce Zbývá je prázdná")
        questions = Model.open_questions(n)
        if questions:                                        # 12 kap. 5 krok 2 (zadání 0.11.2)
            reasons.append(f"otevřené otázky bez odpovědi ({len(questions)}): zodpověz je, nebo přenes "
                           "do navazujícího předání")
        if reasons and not self.args.force:
            raise UsageError(f"--archive-handover {name}: {'; '.join(reasons)} (archivuj s --force)")
        text = set_field(cs.current(n.path), "validity", "archived", section="orchestration")
        text = set_field(text, "updated", self.day, section="orchestration")
        dst = self.v.root / ARCHIVE_DIR / n.path.name
        cs.move(n.path, dst)
        cs.write(dst, text)
        return format_line([self.day.isoformat(), self.args.role, name, "předání archivováno", self.args.source])

    # ------------------------------------------------------------ 3. a 4. kontroly
    def checks(self, vault: Vault, notes, code, entities: list[str], changes_text: str | None,
               model: Model | None = None):
        model = model or Model(vault)
        rels = {n.rel for n in notes}
        fresh = [vault.notes[r] for r in rels if r in vault.notes and not r.startswith(LINT_EXCLUDE_PREFIXES)]
        lint_f = sort_findings((run_checks(vault, fresh) if fresh else []) + header_findings(vault, code))
        aud = Auditor(vault, self.day, model)
        aud.g11((ai.load_json(vault) or {}).get("files") or [], load_state(vault), changes_text)
        ent = set(entities)
        related = {t for (t, _p), ents in aud.g11_entities.items() if ent & set(ents)}
        g11 = [f for f in aud.r.findings if f.target in ent or f.target in related]
        self.warnings += [w for w in aud.r.warnings if w not in self.warnings]
        # kontrolní seznam
        states = {e for n in model.notes if n.type == "state" and n.fm.get("validity") == "valid"
                  for e in model.entities_of(n)}
        for e in entities:
            n = model.entities.get(e)
            if n and n.fm.get("status") in ("built", "verified") and e not in states:
                self.checklist.append(f"{e}: status {n.fm.get('status')} bez platného state – založ nebo doplň stav")
            for h in model.docs_of(e):
                if model.is_active_handover(h) and h.name not in self.args.archive_handover:
                    q = len(model.open_questions(h))
                    if not model.has_remaining(h):              # zadání 0.28, CR-038
                        done = "sekce Zbývá je prázdná: doplň zbývající kroky, nebo předání archivuj"
                    elif not model.handover_fulfilled(h):
                        done = "zůstává aktivní; aktualizuj Zbývá"
                    elif q:
                        done = f"splněné, ale {q} otevřených otázek: zodpověz nebo přenes, pak archivuj"
                    else:
                        done = "splněné, archivovat (--archive-handover)?"
                    self.checklist.append(f"{e}: aktivní předání {h.name} – {done}")
        by_path = {f["path"]: f for f in (self.index or {}).get("files") or []}
        for p in code:
            f = by_path.get(vault.project_rel(p)) or {}
            if f.get("role") == "spec":
                self.checklist.append(f"změněný spec {f['path']}: uprav Souhrn specifikace v "
                                      f"{', '.join(f.get('docs') or []) or 'dokumentech entit'}")
            if f.get("role") == "library":
                self.checklist.append(f"změněná knihovna {f['path']}: zkontroluj Kdo používá v "
                                      f"{', '.join(f.get('docs') or []) or 'dokumentu sdíleného kódu'}")
        for n in notes:
            added = gitinfo.added_lines(n.path) or []
            for line in added:
                m = QUESTION_RE.match(line)
                if m:
                    self.checklist.append(f"nová otevřená otázka v {n.name}: {m.group(1).strip()}")
        return lint_f, g11


def limit_seconds(vault: Vault) -> float:
    v = vault.config.get("task_close_seconds")
    try:
        return 150.0 if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return 150.0


def _args_state(args) -> dict:
    return {k: getattr(args, k) for k in ("role", "source", "note", "change", "entity", "archive_handover", "files",
                                         "force")}


def save_resume(vault: Vault, state: dict) -> None:
    from .fileio import atomic_write, file_hash
    p = vault.root / RESUME_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(p, json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                 expected_hash=file_hash(p) if p.is_file() else None)


def load_resume(vault: Vault) -> dict | None:
    from .fileio import read_text
    p = vault.root / RESUME_REL
    if not p.is_file():
        return None
    try:
        data = json.loads(read_text(p))
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def run(args, vault: Vault) -> tuple[int, dict, str]:
    start = time.monotonic()
    limit = limit_seconds(vault)
    if getattr(args, "resume", False):
        return resume(args, vault, start, limit)
    missing = [f"--{k}" for k in ("role", "source") if not getattr(args, k, None)]
    if missing:
        raise UsageError(f"task_close: chybí {', '.join(missing)} (bez nich jen --resume)")
    tc = TaskClose(vault, args)
    notes, code = tc.changed()
    entities = tc.entities_of(notes, code)
    if not entities and not args.archive_handover:
        raise UsageError("Žádná dotčená entita (změněné soubory ani --entity); není co uzavřít")
    cs = ChangeSet(vault.project_root)
    lines = tc.plan_writes(cs, notes, entities)
    diff = cs.diff()
    changes_text = cs.current(vault.root / CHANGES_REL)
    state = {"version": 1, "day": tc.day.isoformat(), "args": _args_state(args), "entities": entities,
             "notes": [n.rel for n in notes], "code": [str(p) for p in code], "lines": lines,
             "skipped": tc.skipped, "writes": cs.summary(), "done": ["writes"], "remaining": STEPS[1:],
             "hubs": [], "doc_index": False}
    old = load_resume(vault)
    if old and old.get("remaining"):
        tc.warnings.append(f"nedokončený běh z {old.get('day')} ({', '.join(old['remaining'])}): "
                           "dokonči ho task_close --resume; tento běh ho přepíše, jen když sám nedoběhne")
    if args.apply:
        cs.apply()
        vault = Vault.load(vault.root, lazy=True)      # po zápisu se vault čte jednou (zadání 0.28)
        notes = [vault.notes[r] for r in state["notes"] if r in vault.notes]
    return finish(args, vault, tc, notes, code, state, start, limit, diff, changes_text)


def resume(args, vault: Vault, start: float, limit: float) -> tuple[int, dict, str]:
    state = load_resume(vault)
    if state is None or not state.get("remaining"):
        payload = {"command": "task_close", "resume": True, "remaining": []}
        return EXIT_OK, payload, "task_close --resume: žádný nedokončený běh (Maintenance/task_close_resume.json)"
    import argparse
    a = argparse.Namespace(**(state.get("args") or {}))
    a.apply, a.resume = True, True
    for k, d in (("change", []), ("entity", []), ("archive_handover", []), ("files", []), ("force", False)):
        if getattr(a, k, None) is None:
            setattr(a, k, d)
    tc = TaskClose(vault, a)
    tc.skipped = list(state.get("skipped") or [])
    notes = [vault.notes[r] for r in state.get("notes") or [] if r in vault.notes]
    code = [Path(p) for p in state.get("code") or []]
    return finish(a, vault, tc, notes, code, state, start, limit, "", None)


def finish(args, vault: Vault, tc: TaskClose, notes, code, state: dict, start: float, limit: float,
           diff: str, changes_text: str | None) -> tuple[int, dict, str]:
    entities = state["entities"]
    lint_f, g11 = [], []
    model = None
    over = False
    for step in list(state["remaining"]):
        if time.monotonic() - start > limit:           # krok se nezačne po překročení limitu (zadání 0.28)
            over = True
            break
        if step == "hubs":
            model = Model(vault)
            hcs = ChangeSet(vault.project_root)
            hres = Hubs(vault, model).plan(hcs, [e for e in entities if e in model.entities])
            state["hubs"] = hres.changed
            if args.apply:
                hcs.apply()
                if not hcs.empty:
                    vault.refresh(list(hcs.edits))
                    model = None
        elif step == "doc_index":
            # doc_index nad novým stavem: zapíše se jen při novém, změněném nebo přejmenovaném dokumentu
            # (zadání 0.18.1); dry-run: odhad ze současného stavu, `updated` se projeví až při --apply
            model = model or Model(vault)
            dcs = ChangeSet(vault.project_root)
            state["doc_index"] = doc_index.plan(vault, dcs, model)
            if args.apply:
                dcs.apply()
        elif step == "checks":
            model = model or Model(vault)
            lint_f, g11 = tc.checks(vault, notes, code, entities, None if args.apply else changes_text, model)
        state["done"].append(step)
        state["remaining"].remove(step)
    if args.apply and (over or state.get("resume_saved")):
        state["resume_saved"] = True
        save_resume(vault, state)                      # i dokončený běh: remaining [] (soubor se nemaže)
    payload = {"command": "task_close", "applied": bool(args.apply), "entities": entities, "changes": state["lines"],
               "changes_present": tc.skipped,
               "files": [to_posix(vault.project_rel(n.path)) for n in notes] + [vault.project_rel(Path(p)) for p in code],
               "writes": state["writes"], "hubs": state["hubs"], "doc_index": state["doc_index"],
               "lint": [f.as_dict() for f in lint_f],
               "g11": [f.as_dict() for f in g11], "checklist": tc.checklist, "warnings": tc.warnings,
               "done": state["done"], "remaining": state["remaining"]}
    out = [f"task_close: dotčené entity: {', '.join(entities) or '–'}"]
    if getattr(args, "resume", False):
        out.append(f"Dokončení přerušeného běhu ({state.get('day')}): kroky {', '.join(s for s in STEPS if s in state['done'] and s != 'writes')}")
    elif args.apply:
        written = uniq(c.get("path") or c.get("to") for c in state["writes"])
        out.append(f"Zapsáno: {', '.join(written)}" if written else "Zápisy: beze změny (už uzavřeno)")
    else:
        out += ["Změny (dry-run, zapiš s --apply):", diff.rstrip()]
    out += [f"changes.md: řádek už je v souboru, nezdvojuje se: {ln}" for ln in tc.skipped]
    if "hubs" in state["done"]:
        out.append(f"hubs: {', '.join(state['hubs']) if state['hubs'] else 'beze změny'}"
                   + ("" if args.apply or not state["hubs"] else " (dry-run)"))
    if "doc_index" in state["done"]:
        out.append("doc_index: " + (("obnoven" if args.apply else "obnoví se (dry-run)") if state["doc_index"]
                                    else "beze změny"))
    if "checks" in state["done"]:
        out += ["lint změněných souborů:", "  " + to_text(lint_f).replace("\n", "\n  ")]
        out.append("G11 dotčených entit: " + ("bez nálezů" if not g11 else ""))
        out += [f"  {f.target}: {f.message}" for f in g11]
        out.append("Kontrolní seznam (skript neudělá):")
        out += [f"  - [ ] {c}" for c in tc.checklist] or ["  – nic"]
    out += [f"Upozornění: {w}" for w in tc.warnings]
    if over:
        out.append(f"Limit task_close_seconds ({limit:g} s) překročen; nedokončené kroky: {', '.join(state['remaining'])}. "
                   + ("Dokonči: python _core/scripts/hestia.py task_close --resume" if args.apply
                      else "Spusť s --apply (zápisy jsou celé) a pak task_close --resume."))
        return EXIT_OK, payload, "\n".join(out)
    if has_errors(lint_f):
        out.append("Task není hotový: lint našel ve změněných souborech chybu (12 kap. 5); oprav a spusť znovu.")
        return EXIT_FINDINGS, payload, "\n".join(out)
    return EXIT_OK, payload, "\n".join(out)
