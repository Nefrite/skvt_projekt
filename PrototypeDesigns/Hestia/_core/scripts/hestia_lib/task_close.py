"""Příkaz task_close: uzavření tasku za minutu (zadání 13 kap. 10.5, 12 kap. 5).

1. Dotčené entity se odvodí samy: změněné soubory (git, nebo zadané argumentem) -> `asset_index.json`
   (kód, data) a pole `entity` změněných poznámek; plus `--entity`.
2. Řádek do `changes.md` za každou entitu (`--change ENTITA="text"` má přednost před `--note`);
   `updated` u změněných poznámek; `--archive-handover` archivuje splněné předání bez otevřených otázek (jinak jen s `--force`).
3. [R5] `hubs` pro dotčené entity, `lint` změněných souborů, G11 pro dotčené entity.
4. Kontrolní seznam toho, co skript neudělá, ale nesmí se zapomenout.
Dry-run vypíše diff a výsledky kontrol; `--apply` zapíše (změny, pak huby nad novým stavem).
Návratový kód 1, když lint najde chybu ve změněných souborech (task není hotový, 13 kap. 3); upozornění 0.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import asset_index as ai
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
from .model import Model
from .util import today, uniq
from .validate import run_checks
from .vault import LINT_EXCLUDE_PREFIXES, Vault

CHANGES_REL = "Maintenance/changes.md"
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
        self.m = Model(vault)
        self.index = ai.load_json(vault)
        self.warnings: list[str] = []
        self.checklist: list[str] = []

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
                out += [e for e in self.m.link_names((n.fm or {}).get("entity")) if e in self.m.entities]
        for e in self.args.entity:
            if e not in self.m.entities:
                raise UsageError(f"--entity {e}: entita neexistuje")
            out.append(e)
        return uniq(out)

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
        from .logs import append_lines
        cpath = self.v.root / CHANGES_REL
        text = cs.current(cpath)
        if text is None:
            raise UsageError(f"{CHANGES_REL} neexistuje")
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
        if not self.m.handover_fulfilled(n):
            reasons.append("sekce Zbývá má otevřené položky")
        questions = self.m.open_questions(n)
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
    def checks(self, vault: Vault, notes, code, entities: list[str], changes_text: str | None):
        model = Model(vault)
        rels = {n.rel for n in notes}
        fresh = [vault.notes[r] for r in rels if r in vault.notes and not r.startswith(LINT_EXCLUDE_PREFIXES)]
        lint_f = sort_findings((run_checks(vault, fresh) if fresh else []) + header_findings(vault, code))
        aud = Auditor(vault, self.day)
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
                    if not model.handover_fulfilled(h):
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


def run(args, vault: Vault) -> tuple[int, dict, str]:
    tc = TaskClose(vault, args)
    notes, code = tc.changed()
    entities = tc.entities_of(notes, code)
    if not entities and not args.archive_handover:
        raise UsageError("Žádná dotčená entita (změněné soubory ani --entity); není co uzavřít")
    cs = ChangeSet(vault.project_root)
    lines = tc.plan_writes(cs, notes, entities)
    diff = cs.diff()
    changes_text = cs.current(vault.root / CHANGES_REL)
    hubs_changed: list[str] = []
    if args.apply:
        cs.apply()
        vault2 = Vault.load(vault.root)
        notes2 = [vault2.notes[n.rel] for n in notes if n.rel in vault2.notes]
        hcs = ChangeSet(vault2.project_root)
        hres = Hubs(vault2).plan(hcs, [e for e in entities if e in Model(vault2).entities])
        hcs.apply()
        hubs_changed = hres.changed
        lint_f, g11 = tc.checks(vault2, notes2, code, entities, None)
    else:
        hcs = ChangeSet(vault.project_root)
        hres = Hubs(vault).plan(hcs, entities)
        hubs_changed = hres.changed
        lint_f, g11 = tc.checks(vault, notes, code, entities, changes_text)
    payload = {"command": "task_close", "applied": bool(args.apply), "entities": entities, "changes": lines,
               "files": [to_posix(vault.project_rel(n.path)) for n in notes] + [vault.project_rel(p) for p in code],
               "writes": cs.summary(), "hubs": hubs_changed, "lint": [f.as_dict() for f in lint_f],
               "g11": [f.as_dict() for f in g11], "checklist": tc.checklist, "warnings": tc.warnings}
    out = [f"task_close: dotčené entity: {', '.join(entities) or '–'}"]
    if args.apply:
        written = uniq(c.get("path") or c.get("to") for c in cs.summary())
        out.append(f"Zapsáno: {', '.join(written)}" if written else "Zápisy: beze změny (už uzavřeno)")
    else:
        out += ["Změny (dry-run, zapiš s --apply):", diff.rstrip()]
    out.append(f"hubs: {', '.join(hubs_changed) if hubs_changed else 'beze změny'}"
               + ("" if args.apply or not hubs_changed else " (dry-run)"))
    out += ["lint změněných souborů:", "  " + to_text(lint_f).replace("\n", "\n  ")]
    out.append("G11 dotčených entit: " + ("bez nálezů" if not g11 else ""))
    out += [f"  {f.target}: {f.message}" for f in g11]
    out.append("Kontrolní seznam (skript neudělá):")
    out += [f"  - [ ] {c}" for c in tc.checklist] or ["  – nic"]
    out += [f"Upozornění: {w}" for w in tc.warnings]
    if has_errors(lint_f):
        out.append("Task není hotový: lint našel ve změněných souborech chybu (12 kap. 5); oprav a spusť znovu.")
        return EXIT_FINDINGS, payload, "\n".join(out)
    return EXIT_OK, payload, "\n".join(out)
