"""Příkaz health: kontrola zdraví instance (zadání 13 kap. 10.20, 05 kap. 3.2b; zadání 0.28, fáze 11).

Jen čte vault a projekt; nic nemění a nezakládá položky fronty. S `--apply` zapíše report
`Maintenance/reports/health_RRRR-MM-DD.md` (report je výstup kontroly, ne obsah; bez `--apply` jen výpis).
Sekce, každá se stavem `ok` / `pozor` a doporučeným krokem:

- `prostredi`: výstup `doctor` (chyba nebo upozornění = pozor);
- `verze_core`: `_core/VERSION` proti nejnovější značce `vX.Y.Z` ve zdroji `core_source`; nedostupný zdroj
  = informace (stav ok), novější značka = pozor s `update_core --latest` (dry-run, jen na pokyn GameDesignera);
- `kompilaty`: kompiláty rolí, které by nové složení změnilo (jako G5 v auditu);
- `rucni_ukoly`: otevřené ruční úkoly `update_core:*` ve frontě a jejich stáří (první commit řádku v gitu);
- `podnety`: otevřené podněty `proposal` s `code: hestia` ve frontě, které nepřevedl `feedback_log`;
- `outbox`: záznamy `structure_log.md` bez vyplněné buňky `cr` (čekají na `export_cr`) a soubory
  v `Maintenance/outbox/` mimo `sent/` (čekají na odeslání), se stářím;
- `unreal`: stáří reportů z Unrealu (`ue_<entita>.json`, `ue_assets.json`) proti `ue_report_days`.
Lokální odchylky přijdou ve druhé verzi role (podklad `steward` kap. 5).
"""
from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, field
from pathlib import Path

from .changeset import ChangeSet
from .errors import EXIT_OK
from .fileio import read_text, to_posix
from .util import as_date, today
from .vault import Vault

REPORTS = "Maintenance/reports"
OUTBOX = "Maintenance/outbox"
SENT = "sent"
QUEUE_REL = "Maintenance/queue.md"
LOG_REL = "Maintenance/structure_log.md"
OK, ATTN = "ok", "pozor"
TAG_RE = re.compile(r"^v\d+\.\d+\.\d+$")


@dataclass
class Section:
    id: str
    title: str
    status: str = OK
    lines: list[str] = field(default_factory=list)
    step: str = ""                       # doporučený krok (u pozor)

    def as_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "status": self.status, "lines": self.lines, "step": self.step}


def _vt(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.lstrip("v").split("."))


def section_env(vault: Vault) -> Section:
    from . import doctor
    s = Section("prostredi", "Prostředí (doctor)")
    items = doctor.checks(str(vault.home))
    bad = [c for c in items if c["status"] != doctor.OK]
    s.lines = [f"{doctor.STATUS_CZ[c['status']]} {c['name']}: {c['message']}" for c in bad] or \
              [f"{len(items)} kontrol v pořádku"]
    if bad:
        s.status = ATTN
        s.step = next((c["help"].split("\n")[0] for c in bad if c["help"]), "projdi výstup doctor")
    return s


def section_version(vault: Vault) -> Section:
    from . import gitinfo
    s = Section("verze_core", "Verze core")
    ver_p = vault.root / "_core" / "VERSION"
    core_v = read_text(ver_p).strip() if ver_p.is_file() else ""
    cs = vault.config.get("core_source")
    repo = (vault.home / str(cs)).resolve() if cs else None
    tags = gitinfo.tags(repo) if repo is not None and repo.is_dir() else None
    tags = sorted((t for t in tags or [] if TAG_RE.match(t)), key=_vt) if tags is not None else None
    if not tags:
        why = ("core_source v config.yaml chybí" if not cs else
               f"zdroj core {cs} nedostupný (není složka, git repozitář nebo nemá značky)")
        s.lines = [f"_core/VERSION {core_v or '–'}; {why} (informace)"]
        return s
    latest = tags[-1]
    s.lines = [f"_core/VERSION {core_v or '–'}, nejnovější značka {latest}"]
    if core_v and re.fullmatch(r"\d+\.\d+\.\d+", core_v) and _vt(latest) > _vt(core_v):
        s.status = ATTN
        s.step = (f"novější core {latest}: update_core --latest (dry-run), hlášení GameDesignerovi, --apply jen "
                  "po schválení (modul core_update)")
    return s


def section_compiled(vault: Vault) -> Section:
    from . import compose
    s = Section("kompilaty", "Kompiláty rolí")
    d = vault.root / compose.COMPILED_DIR
    stale = []
    files = sorted(d.glob(f"*{compose.COMPILED_SUFFIX}.md")) if d.is_dir() else []
    for p in files:
        role = p.stem.removesuffix(compose.COMPILED_SUFFIX)
        try:
            if compose.plan(vault, [role])[0].status != "unchanged":
                stale.append(p.name)
        except Exception:  # noqa: BLE001 – profil zmizel nebo je chybný
            stale.append(p.name)
    s.lines = [f"starší než zdroje: {', '.join(stale)}"] if stale else [f"{len(files)} kompilátů aktuálních"]
    if stale:
        s.status, s.step = ATTN, "compose_role --apply; do Claude Projectu nahraj jen changed"
    return s


def _queue(vault: Vault):
    from .logs import parse_queue
    p = vault.root / QUEUE_REL
    return (parse_queue(read_text(p)) if p.is_file() else []), p


def _age(day: _dt.date, d) -> str:
    d = as_date(d)
    return f"{(day - d).days} dní" if d else "stáří neznámé"


def section_manual(vault: Vault, day: _dt.date) -> Section:
    from . import gitinfo
    s = Section("rucni_ukoly", "Ruční úkoly z aktualizací core")
    items, qp = _queue(vault)
    tasks = [it for it in items if it.is_open and it.code.startswith("update_core:")]
    first = gitinfo.first_seen(qp, [t.id for t in tasks]) if tasks else {}
    for t in tasks:
        s.lines.append(f"{t.id} {t.code} ({_age(day, (first or {}).get(t.id))}): {t.proposal[:120]}")
    if tasks:
        s.status, s.step = ATTN, "projdi ruční úkoly s GameDesignerem, hotové uzavři ve frontě (modul core_update)"
    else:
        s.lines = ["žádné otevřené"]
    return s


def section_proposals(vault: Vault) -> Section:
    from .feedback import is_hestia_code
    s = Section("podnety", "Podněty pro Hestii ve frontě")
    items, _qp = _queue(vault)
    props = [it for it in items if it.kind == "proposal" and is_hestia_code(it.code)
             and it.state_value not in ("done", "rejected")]
    s.lines = [f"{p.id} {p.code}: {p.proposal[:120]}" for p in props] or ["žádné nepřevedené"]
    if props:
        s.status, s.step = ATTN, "feedback_log (dry-run, pak --apply), potom export_cr"
    return s


def section_outbox(vault: Vault, day: _dt.date) -> Section:
    from .logs import cr_cell, log_entries
    s = Section("outbox", "Change requesty a hlášení pro HearthLore")
    lp = vault.root / LOG_REL
    waiting = []
    if lp.is_file():
        for row in log_entries(read_text(lp)):
            row = (row + [""] * 6)[:6]
            if cr_cell(row[5])[0] in ("empty", "invalid"):
                waiting.append(row)
    if waiting:
        oldest = min((as_date(r[0]) for r in waiting if as_date(r[0])), default=None)
        s.lines.append(f"structure_log bez cr (čekají na export_cr): {len(waiting)}"
                       + (f", nejstarší {(day - oldest).days} dní" if oldest else ""))
    out = vault.root / OUTBOX
    pending = sorted(p for p in out.rglob("*") if p.is_file() and not p.name.startswith(".")
                     and SENT not in p.relative_to(out).parts) \
        if out.is_dir() else []
    for p in pending:
        d = _dt.date.fromtimestamp(p.stat().st_mtime)
        s.lines.append(f"neodesláno: {to_posix(p.relative_to(vault.root))} ({(day - d).days} dní)")
    if waiting or pending:
        s.status = ATTN
        s.step = ("export_cr (dry-run, pak --apply)" if waiting else "") + \
                 (" a " if waiting and pending else "") + \
                 ("odeslat outbox/ do HearthLore (člověk), odeslané přesunout do outbox/sent/" if pending else "")
    else:
        s.lines = ["nic nečeká"]
    return s


def section_unreal(vault: Vault, day: _dt.date) -> Section:
    from . import ue, ue_assets
    s = Section("unreal", "Reporty z Unrealu")
    d = vault.root / REPORTS
    limit = ue_assets.report_days(vault)
    old, seen = [], 0
    for p in sorted(d.glob("ue_*.json")) if d.is_dir() else []:
        if p.name == Path(ue_assets.REPORT_REL).name:
            rep = ue_assets.load_report(vault)
            reads = [ue_assets.read_date(r, rep) for r in ((rep or {}).get("assets") or {}).values()]
            reads = [x for x in reads if x]
            when = min(reads) if reads else ue_assets.report_date(rep)
        else:
            import json
            try:
                rep = json.loads(read_text(p))
            except ValueError:
                rep = None
            when = ue.report_date(rep) if isinstance(rep, dict) else None
        seen += 1
        if when is None or (day - when).days > limit:
            old.append(f"{p.name} ({'datum neznámé' if when is None else str((day - when).days) + ' dní'})")
    if not seen:
        s.lines = ["žádný report (čtení z Unrealu se nepoužívá, nebo ještě neproběhlo)"]
    elif old:
        s.status = ATTN
        s.lines = [f"starší než ue_report_days {limit}: {', '.join(old)}"]
        s.step = "čtecí dotaz do Unrealu (ue_query --emit, běží-li editor; modul ue_lookup)"
    else:
        s.lines = [f"{seen} reportů, všechny čerstvé"]
    return s


def check(vault: Vault, day: _dt.date | None = None) -> list[Section]:
    day = day or today()
    return [section_env(vault), section_version(vault), section_compiled(vault), section_manual(vault, day),
            section_proposals(vault), section_outbox(vault, day), section_unreal(vault, day)]


def report_rel(day: _dt.date) -> str:
    return f"{REPORTS}/health_{day.isoformat()}.md"


def render(vault: Vault, sections: list[Section], day: _dt.date) -> str:
    steward = bool(vault.config.get("steward_active", False))
    lines = ["---", "type: report", f"updated: {day.isoformat()}", "---", f"# Zdraví instance {day.isoformat()}", "",
             "Kontrola `health` (13 kap. 10.20): jen čte, nic nemění. "
             + ("Kroky dělá Steward." if steward else "Steward není aktivní (`steward_active: false`): "
                "export_cr dělá Curator, `weekly` spouští člověk."), "",
             "| sekce | stav | doporučený krok |", "|---|---|---|"]
    lines += [f"| {s.title} | {s.status} | {s.step or '–'} |" for s in sections]
    for s in sections:
        lines += ["", f"## {s.title}", ""] + [f"- {x}" for x in s.lines]
    return "\n".join(lines) + "\n"


def run(args, vault: Vault) -> tuple[int, dict, str]:
    day = today()
    sections = check(vault, day)
    rel = report_rel(day)
    cs = ChangeSet(vault.project_root)
    cs.write(vault.root / rel, render(vault, sections, day))
    if args.apply:
        cs.apply()
    attn = [s for s in sections if s.status == ATTN]
    payload = {"command": "health", "applied": bool(args.apply), "report": rel, "status": ATTN if attn else OK,
               "steward_active": bool(vault.config.get("steward_active", False)),
               "sections": [s.as_dict() for s in sections]}
    out = [f"health: {len(attn)} z {len(sections)} sekcí pozor"]
    for s in sections:
        out.append(f"[{s.status}] {s.title}: " + "; ".join(s.lines[:3]) + (f" → {s.step}" if s.step else ""))
    out.append(f"Report {rel}: " + ("zapsán" if args.apply else "zapsal by se (dry-run, zapiš s --apply)"))
    return EXIT_OK, payload, "\n".join(out)
