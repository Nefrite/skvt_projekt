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
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from . import CORE_ROOT
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
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, str(CORE_ROOT / "scripts" / "hestia.py"), step, "--vault", str(vault_root),
                        "--apply", "--json"], capture_output=True, text=True, encoding="utf-8", env=env)
    try:
        data = json.loads(r.stdout) if r.stdout.strip() else None
    except ValueError:
        data = None
    return r.returncode, data, (r.stderr or "").strip()


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
    lines += ["", f"## Doporučené kroky ({who})", ""]
    health = (results.get("health") or (None, None, ""))[1] or {}
    steps = [f"{s['title']}: {s['step']}" for s in health.get("sections") or [] if s.get("status") == "pozor"]
    audit = (results.get("audit") or (None, None, ""))[1] or {}
    errors = sum(1 for f in audit.get("findings") or [] if f.get("severity") == "error")
    if errors:
        steps.append(f"audit: {errors} chyb (G6, G7) – oprav podle reportu auditu")
    lines += [f"- {s}" for s in steps] or ["- nic"]
    return "\n".join(lines) + "\n"


def _run_all(vault_root: Path) -> dict:
    return {step: run_step(vault_root, step) for step in STEPS}


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
        lines.append("--work-copy: kroky v pracovní kopii, zpět jen Maintenance/ a změny uvnitř generovaných bloků.")
    prev_name, _c = previous_audit(vault, day)
    lines.append(f"Srovnání nálezů s {prev_name or '– (žádný dřívější audit)'}.")
    return "\n".join(lines)


def run(args, vault: Vault) -> tuple[int, dict, str]:
    work_copy = getattr(args, "work_copy", None)
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
               "steps": {s: code for s, (code, _d, _e) in results.items()}, "failed": failed, "work_copy": wc}
    out = [f"weekly: kroky {', '.join(STEPS)}" + (f"; selhaly: {', '.join(failed)}" if failed else "; v pořádku"),
           f"Report {rel} zapsán."]
    if wc is not None:
        out.append(f"Pracovní kopie {wc['dir']}: zpět {len(wc['written'])} souborů"
                   + (f", kolize {len(wc['collisions'])}: {', '.join(wc['collisions'][:5])}" if wc["collisions"] else "")
                   + (f", přeskočeno (obsah mimo generované bloky) {len(wc['skipped'])}" if wc["skipped"] else ""))
    for s in failed:
        out.append(f"Chyba kroku {s}: {results[s][2].splitlines()[-1] if results[s][2] else 'bez výpisu'}")
    return (EXIT_FINDINGS if failed or (wc and wc["collisions"]) else EXIT_OK), payload, "\n".join(out)


# ---------------------------------------------------------------- pracovní kopie

def run_work_copy(args, vault: Vault, work_arg: str, day) -> tuple[int, dict, str]:
    from . import workcopy
    home = vault.home
    work = Path(work_arg).resolve() if work_arg else Path(tempfile.mkdtemp(prefix="hestia_weekly_"))
    work.mkdir(parents=True, exist_ok=True)
    print(f"weekly --work-copy: pracovní adresář {work}", file=sys.stderr)
    workcopy.phase_copy(vault, work, lambda _m: None)
    snapshot = json.loads(read_text(work / workcopy.SNAPSHOT))
    (work / WORK_MARKER).write_text(json.dumps({"vault": home.name, "origin": str(home), "mode": "weekly"},
                                               ensure_ascii=False), encoding="utf-8")
    copy = work / home.name
    results = _run_all(copy)
    cv = Vault.load(copy)
    text, counts, prev = _finish(cv, results, day)
    rp = copy / report_rel(day)
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(text, encoding="utf-8", newline="\n")
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
    wc = {"dir": to_posix(work), "written": sorted(written), "collisions": sorted(collisions),
          "skipped": sorted(skipped)}
    if not collisions and not getattr(args, "keep_work_copy", False):
        shutil.rmtree(work, ignore_errors=True)
    return _result(results, report_rel(day), counts, prev, wc)
