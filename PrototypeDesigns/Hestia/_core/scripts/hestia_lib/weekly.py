"""Příkaz weekly: naplánovaný týdenní běh (zadání 13 kap. 10.20, 05 kap. 6; zadání 0.28, fáze 11).

Kroky v pořadí `doc_index`, `asset_index`, `hubs`, `audit`, `health` (každý jako samostatný příkaz core
s `--apply --json`, stejný interpret). Bez `--apply` jen vypíše plán a nic nespustí ani nezapíše.
S `--apply` zapíše jen generované výstupy a reporty (indexy, generované bloky, report auditu a fronta nálezů,
`health`) a report `Maintenance/reports/weekly_RRRR-MM-DD.md`: odkazy na report auditu a `health`, počty nálezů
podle kódu proti poslednímu dřívějšímu auditu, doporučené kroky (pro Stewarda, bez něj pro člověka).
Obsah vaultu (text dokumentů mimo generované bloky) se nemění.

`--work-copy [ADRESÁŘ]` (připojená složka, jako `update_core --work-copy`): kopie vaultu do pracovního adresáře
(bez hodnoty dočasný `hestia_weekly_*`), kroky v kopii, zápis zpět jen souborů pod `Maintenance/`
a poznámek změněných jen uvnitř generovaných bloků, a jen když se originál od kopie nezměnil (jinak se soubor
přeskočí a vypíše jako kolize). Pracovní adresář se po úspěchu smaže (`--keep-work-copy` ne).
Fáze `--work-phase copy|run|back` jako u `update_core` (zadání 0.29, CR-033): každá fáze v jednom volání, další
běh pokračuje od nedokončené fáze (stav a výsledky kroků ve značce `hestia_work.json`), zápis zpět podle snímku.
Začátek a konec každého kroku a fáze se hned vypíše na stderr (modul `profiling`).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from . import CORE_ROOT, profiling
from .blocks import strip_generated
from .changeset import ChangeSet
from .errors import EXIT_FINDINGS, EXIT_OK, UsageError
from .fileio import read_text, to_posix
from .util import today
from .vault import WORK_MARKER, Vault

STEPS = ["doc_index", "asset_index", "hubs", "audit", "health"]
REPORTS = "Maintenance/reports"
WRITE_BACK_PREFIXES = ("Maintenance/",)        # reporty, indexy, fronta nálezů, stav auditu


def report_rel(day) -> str:
    return f"{REPORTS}/weekly_{day.isoformat()}.md"


def run_step(vault_root: Path, step: str) -> tuple[int, dict | None, str]:
    with profiling.child(step, dict(os.environ, PYTHONIOENCODING="utf-8")) as (env, extra):  # zadání 0.29.2
        r = subprocess.run([sys.executable, str(CORE_ROOT / "scripts" / "hestia.py"), step, "--vault",
                            str(vault_root), "--apply", "--json", *extra],
                           capture_output=True, text=True, encoding="utf-8", env=env)
    try:
        data = json.loads(r.stdout) if r.stdout.strip() else None
    except ValueError:
        data = None
    return r.returncode, data, profiling.without_progress(r.stderr or "").strip()


def _counts(findings) -> dict[str, int]:
    out: dict[str, int] = {}
    for f in findings or []:
        code = f.get("code") if isinstance(f, dict) else None
        if code:
            out[code] = out.get(code, 0) + 1
    return out


def previous_audit(vault: Vault, day) -> tuple[str | None, dict[str, int] | None]:
    """Poslední report auditu před dneškem (`audit_RRRR-MM-DD.json`) a jeho počty podle kódu."""
    d = vault.root / REPORTS
    older = sorted(p for p in d.glob("audit_*.json") if p.stem[len("audit_"):] < day.isoformat()) \
        if d.is_dir() else []
    if not older:
        return None, None
    try:
        return older[-1].stem, _counts(json.loads(read_text(older[-1])))
    except ValueError:
        return older[-1].stem, None


def render(vault: Vault, day, results: dict, prev: tuple, now_counts: dict[str, int]) -> str:
    steward = bool(vault.config.get("steward_active", False))
    who = "Steward" if steward else "člověk (Steward není aktivní, `steward_active: false`)"
    prev_name, prev_counts = prev
    lines = ["---", "type: report", f"updated: {day.isoformat()}", "---", f"# Týdenní běh {day.isoformat()}", "",
             "Naplánovaný běh `weekly` (13 kap. 10.20): indexy, huby, audit a kontrola zdraví bez zásahu do obsahu.",
             "", "## Kroky", "", "| krok | výsledek |", "|---|---|"]
    for step in STEPS:
        code, _data, err = results.get(step, (None, None, ""))
        state = "neproběhl" if code is None else ("v pořádku" if code in (0, 1) else f"chyba (kód {code})")
        lines.append(f"| `{step}` | {state}{(': ' + err.splitlines()[-1]) if code not in (0, 1, None) and err else ''} |")
    lines += ["", "## Reporty", "", f"- audit: [[audit_{day.isoformat()}]]", f"- zdraví: [[health_{day.isoformat()}]]",
              "", "## Nálezy proti minulému týdnu", ""]
    codes = sorted(set(now_counts) | set(prev_counts or {}), key=lambda c: (len(c), c))
    if codes:
        lines += [f"Srovnání s {prev_name or '– (první běh)'}.", "", "| kód | teď | minule | změna |", "|---|---|---|---|"]
        for c in codes:
            n, p = now_counts.get(c, 0), (prev_counts or {}).get(c)
            lines.append(f"| {c} | {n} | {'–' if p is None else p} | {'–' if p is None else f'{n - p:+d}'} |")
    else:
        lines.append("Bez nálezů.")
    replaced = replaced_findings(results)
    if replaced:                              # G5 nahrazeného dokumentu před obnovou indexu (zadání 0.29.2)
        lines += ["", "## Změněné nahrazené dokumenty (G5)", ""]
        lines += [f"- `{f.get('file')}`: {f.get('message')}" for f in replaced]
    lines += ["", f"## Doporučené kroky ({who})", ""]
    health = (results.get("health") or (None, None, ""))[1] or {}
    steps = [f"{s['title']}: {s['step']}" for s in health.get("sections") or [] if s.get("status") == "pozor"]
    audit = (results.get("audit") or (None, None, ""))[1] or {}
    errors = sum(1 for f in audit.get("findings") or [] if f.get("severity") == "error")
    if errors:
        steps.append(f"audit: {errors} chyb (G6, G7) – oprav podle reportu auditu")
    if replaced:
        steps.append(f"G5: {len(replaced)} nahrazených dokumentů se změněným tělem – obsah přesuň do nástupce")
    lines += [f"- {s}" for s in steps] or ["- nic"]
    return "\n".join(lines) + "\n"


def replaced_findings(results: dict) -> list[dict]:
    """G5 nahrazených dokumentů z výsledků kroků (`replaced`), bez duplicit. Krok `doc_index` je hlásí před
    obnovou indexu, další kroky už proti obnovenému indexu nic nevidí; report weekly je proto zachová
    (zadání 0.29.2, 13 kap. 10.22)."""
    out, seen = [], set()
    for step in STEPS:
        data = (results.get(step) or (None, None, ""))[1]
        for f in (data or {}).get("replaced") or [] if isinstance(data, dict) else []:
            key = (f.get("file"), f.get("message"))
            if key not in seen:
                seen.add(key)
                out.append(f)
    return out


def _run_all(vault_root: Path) -> dict:
    out = {}
    for step in STEPS:                       # průběžný výstup kroků (zadání 0.29, CR-033)
        with profiling.step(step):
            out[step] = run_step(vault_root, step)
    return out


def _finish(vault: Vault, results: dict, day) -> tuple[str, dict, str]:
    """Report weekly do vaultu `vault` (originál nebo kopie)."""
    audit = results.get("audit", (None, None, ""))[1] or {}
    now_counts = _counts(audit.get("findings"))
    prev = previous_audit(vault, day)
    return render(vault, day, results, prev, now_counts), now_counts, prev[0] or ""


def plan_text(vault: Vault, work_copy: bool) -> str:
    day = today()
    lines = [f"weekly (dry-run, spusť s --apply): kroky {', '.join(STEPS)}",
             f"Zapíše jen generované výstupy a reporty; report {report_rel(day)}."]
    if work_copy:
        lines.append("--work-copy: kroky v pracovní kopii, zpět jen Maintenance/ a změny uvnitř generovaných bloků; "
                     "fáze copy, run, back (--work-phase jen jedna, další běh pokračuje od nedokončené).")
    prev_name, _c = previous_audit(vault, day)
    lines.append(f"Srovnání nálezů s {prev_name or '– (žádný dřívější audit)'}.")
    return "\n".join(lines)


def run(args, vault: Vault) -> tuple[int, dict, str]:
    work_copy = getattr(args, "work_copy", None)
    if getattr(args, "work_phase", None) and work_copy is None:
        raise UsageError("--work-phase jen s --work-copy")
    if work_copy is not None and vault.origin is not None:
        raise UsageError("weekly --work-copy nad pracovní kopií nejde; spusť ho nad originálem vaultu")
    if not args.apply:
        payload = {"command": "weekly", "applied": False, "steps": STEPS, "work_copy": work_copy is not None}
        return EXIT_OK, payload, plan_text(vault, work_copy is not None)
    day = today()
    if work_copy is not None:
        return run_work_copy(args, vault, work_copy, day)
    results = _run_all(vault.root)
    v2 = Vault.load(vault.root)
    text, counts, prev = _finish(v2, results, day)
    cs = ChangeSet(v2.project_root)
    cs.write(v2.root / report_rel(day), text)
    cs.apply()
    return _result(results, report_rel(day), counts, prev, None)


def _result(results: dict, rel: str, counts: dict, prev: str, wc: dict | None) -> tuple[int, dict, str]:
    failed = [s for s, (code, _d, _e) in results.items() if code not in (0, 1)]
    payload = {"command": "weekly", "applied": True, "report": rel, "findings": counts, "previous": prev or None,
               "steps": {s: code for s, (code, _d, _e) in results.items()}, "failed": failed, "work_copy": wc,
               "replaced": replaced_findings(results)}
    out = [f"weekly: kroky {', '.join(STEPS)}" + (f"; selhaly: {', '.join(failed)}" if failed else "; v pořádku"),
           f"Report {rel} zapsán."]
    if wc is not None:
        out.append(f"Pracovní kopie {wc['dir']}: zpět {len(wc['written'])} souborů"
                   + (f", kolize {len(wc['collisions'])}: {', '.join(wc['collisions'][:5])}" if wc["collisions"] else "")
                   + (f", přeskočeno (obsah mimo generované bloky) {len(wc['skipped'])}" if wc["skipped"] else ""))
    if payload["replaced"]:
        out.append(f"Upozornění G5: {len(payload['replaced'])} nahrazených dokumentů se změněným tělem (viz report)")
    for s in failed:
        out.append(f"Chyba kroku {s}: {results[s][2].splitlines()[-1] if results[s][2] else 'bez výpisu'}")
    return (EXIT_FINDINGS if failed or (wc and wc["collisions"]) else EXIT_OK), payload, "\n".join(out)


# ---------------------------------------------------------------- pracovní kopie

PHASES = ("copy", "run", "back")
TMP_PREFIX = "hestia_weekly_"


def load_wstate(work: Path) -> dict | None:
    """Stav pracovní kopie `weekly` ve značce `hestia_work.json` (`mode: weekly`); None = není."""
    p = work / WORK_MARKER
    try:
        data = json.loads(read_text(p)) if p.is_file() else None
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("mode") == "weekly" else None


def save_wstate(work: Path, state: dict) -> None:
    (work / WORK_MARKER).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _same(state: dict, home: Path) -> bool:
    try:
        return Path(state.get("origin") or "").resolve() == home.resolve()
    except OSError:
        return False


def find_unfinished(home: Path) -> list[Path]:
    out = []
    for d in sorted(Path(tempfile.gettempdir()).glob(TMP_PREFIX + "*")):
        st = load_wstate(d) if d.is_dir() else None
        if st and _same(st, home) and st.get("status") not in ("done", "collision"):
            out.append(d)
    return out


def resolve_work(work_arg: str, home: Path, phase: str | None) -> tuple[Path, dict | None]:
    """Pracovní adresář `weekly --work-copy` a uložený stav (None = nový běh); jako `update_core` (zadání 0.29)."""
    if work_arg:
        work = Path(work_arg).resolve()
        if work == home.resolve() or home.resolve() in work.parents:
            raise UsageError(f"--work-copy {work}: pracovní adresář musí být mimo vault")
        state = load_wstate(work) if work.is_dir() else None
        if state is not None:
            if not _same(state, home):
                raise UsageError(f"--work-copy {work}: pracovní kopie jiného vaultu ({state.get('origin')})")
            return work, state
        if work.is_dir() and any(work.iterdir()):
            raise UsageError(f"--work-copy {work}: adresář není prázdný ani neobsahuje pracovní kopii weekly")
        if phase in ("run", "back"):
            raise UsageError(f"--work-phase {phase}: v {work} není pracovní kopie (nejdřív --work-phase copy)")
        return work, None
    found = find_unfinished(home)
    if len(found) > 1:
        raise UsageError("Víc nedokončených pracovních kopií weekly; zadej --work-copy <adresář>: "
                         + ", ".join(str(d) for d in found))
    if found:
        return found[0], load_wstate(found[0])
    if phase in ("run", "back"):
        raise UsageError(f"--work-phase {phase}: nedokončená pracovní kopie nenalezena; zadej --work-copy <adresář>")
    return Path(tempfile.mkdtemp(prefix=TMP_PREFIX)), None


def write_back(home: Path, copy: Path, snapshot: dict) -> tuple[list[str], list[str], list[str]]:
    """Zápis zpět podle snímku: celé `Maintenance/` a poznámky změněné jen uvnitř generovaných bloků; soubor,
    který se v originálu od kopie změnil, se přeskočí jako kolize (CR-023, zadání 0.28.1)."""
    from . import workcopy
    written, collisions, skipped = [], [], []
    for rel, entry in workcopy.scan(copy).items():
        before = snapshot.get(rel)
        if before and before["hash"] == entry["hash"]:
            continue
        src = copy / rel
        if not rel.startswith(WRITE_BACK_PREFIXES):
            if before is None or not rel.endswith(".md"):
                skipped.append(rel)
                continue
            old = (home / rel).read_bytes().decode("utf-8", "replace").replace("\r\n", "\n")
            new = src.read_bytes().decode("utf-8", "replace").replace("\r\n", "\n")
            if strip_generated(old) != strip_generated(new):
                skipped.append(rel)
                continue
        dst = home / rel
        cur = dst.read_bytes() if dst.is_file() else None
        cur_hash = workcopy._sha(cur) if cur is not None else None
        if cur_hash != (before or {}).get("hash"):
            collisions.append(rel)                    # originál se od kopie změnil
            continue
        workcopy._write_in_place(dst, src.read_bytes())
        written.append(rel)
    return sorted(written), sorted(collisions), sorted(skipped)


def run_work_copy(args, vault: Vault, work_arg: str, day) -> tuple[int, dict, str]:
    """`weekly --work-copy` po fázích `copy`, `run`, `back` (zadání 0.29, CR-033): bez `--work-phase` všechny,
    další běh se stejným adresářem (nebo nalezeným nedokončeným `hestia_weekly_*`) pokračuje od nedokončené fáze;
    stav fází a výsledky kroků jsou ve značce `hestia_work.json`, zápis zpět podle snímku originálu."""
    from . import workcopy
    home = vault.home
    phase = getattr(args, "work_phase", None)
    work, state = resolve_work(work_arg or "", home, phase)
    work.mkdir(parents=True, exist_ok=True)
    print(f"weekly --work-copy: pracovní adresář {work}", file=sys.stderr, flush=True)
    state = state or {"vault": home.name, "origin": str(home), "mode": "weekly", "done": [], "day": day.isoformat()}
    if phase:
        if phase in state["done"]:
            todo = []
        else:
            need = PHASES[PHASES.index(phase) - 1] if phase != "copy" else None
            if need and need not in state["done"]:
                raise UsageError(f"--work-phase {phase}: nejdřív fáze {need} ({work})")
            todo = [phase]
    else:
        todo = [p for p in PHASES if p not in state["done"]]
    copy = work / home.name
    wc = None
    for ph in todo:
        with profiling.step(f"fáze {ph}"):
            if ph == "copy":
                workcopy.phase_copy(vault, work, lambda _m: None)
            elif ph == "run":
                results = _run_all(copy)
                cv = Vault.load(copy)
                text, _counts_now, _prev = _finish(cv, results, date_of(state, day))
                rp = copy / report_rel(date_of(state, day))
                rp.parent.mkdir(parents=True, exist_ok=True)
                rp.write_text(text, encoding="utf-8", newline="\n")
                state["results"] = {s: list(r) for s, r in results.items()}
            else:
                snapshot = json.loads(read_text(work / workcopy.SNAPSHOT))
                written, collisions, skipped = write_back(home, copy, snapshot)
                wc = {"dir": to_posix(work), "written": written, "collisions": collisions, "skipped": skipped}
                state["status"] = "collision" if collisions else "done"
                state["back"] = wc
            state["done"].append(ph)
            save_wstate(work, state)
    results = {s: tuple(r) for s, r in (state.get("results") or {}).items()}
    if "back" not in state["done"]:                     # další fáze v dalším volání (limit volání)
        nxt = next(p for p in PHASES if p not in state["done"])
        payload = {"command": "weekly", "applied": True, "work_copy": {"dir": to_posix(work), "done": state["done"],
                                                                        "next": nxt}}
        lines = ([f"Fáze {phase} už proběhla."] if phase and not todo else []) + [
            f"weekly --work-copy: hotové fáze {', '.join(state['done']) or '–'} ({work}).",
            f"Další: weekly --work-copy {work} --work-phase {nxt} --apply (nebo bez --work-phase všechny zbývající)."]
        return EXIT_OK, payload, "\n".join(lines)
    if wc is None:                                      # back proběhl dřív, jen znovu ohlásit
        wc = state.get("back") or {"dir": to_posix(work), "written": [], "collisions": [], "skipped": []}
    audit = (results.get("audit") or (None, None, ""))[1] or {}
    counts = _counts(audit.get("findings"))
    prev = previous_audit(vault, date_of(state, day))[0] or ""
    if not wc["collisions"] and not getattr(args, "keep_work_copy", False):
        shutil.rmtree(work, ignore_errors=True)
    return _result(results, report_rel(date_of(state, day)), counts, prev, wc)


def date_of(state: dict, day):
    import datetime as _dt
    try:
        return _dt.date.fromisoformat(state.get("day") or "")
    except ValueError:
        return day
