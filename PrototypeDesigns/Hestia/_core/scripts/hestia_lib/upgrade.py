"""Manifest `hestia/upgrade.yaml` a kroky po aktualizaci core (zadání 0.15; 13 kap. 10.6, 10.6a; 11 kap. 6).

- `load_manifest`, `plan`: záznamy verzí (stará, nová] sečtené: automatické kroky v pevném pořadí
  `asset_index` → `hubs` → `doc_index` → `compose_role` (každý jednou), ruční úkoly, CR k ověření, migrace.
- `run_after` (`update_core --after-only`): běží vždy v **novém** core (`_core/` po výměně; řídicí skript ho po
  `--apply` spustí jako podproces). Spustí automatické kroky s `--apply`, pak `lint --all` a `audit` jen
  v dry-run se souhrnem; ruční úkoly zapíše do `queue.md` jako `T-…` s klíčem `update_core:<verze>:<id>`
  (opakovaný běh je nezakládá znovu); report `Maintenance/reports/update_core_RRRR-MM-DD.md`.
  Selže-li krok, další kroky se nespouští, návratový kód 1 a výpis zbývajících kroků.
- Rozsah verzí: `--since` (předává řídicí skript), jinak poslední řádek `structure_version.md`
  „core <aktuální> | aktualizace z <stará>“; bez něj všechny automatické kroky bez ručních úkolů.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .errors import EXIT_FINDINGS, EXIT_OK, UsageError
from .fileio import atomic_write, file_hash, read_text
from .logs import QueueItem, next_id, parse_queue, upgrade_queue, write_queue
from .taxonomy import load_yaml
from .util import today
from .vault import Vault

MANIFEST = "upgrade.yaml"
AFTER_ORDER = ("asset_index", "hubs", "doc_index", "compose_role")
VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
SV_RE = re.compile(r"\|\s*core (\d+\.\d+\.\d+)\s*\|\s*aktualizace z (\d+\.\d+\.\d+)")
QUEUE_REL = "Maintenance/queue.md"
SV_REL = "Maintenance/structure_version.md"


def vt(v: str) -> tuple[int, int, int]:
    m = VERSION_RE.match(str(v or "").strip())
    if not m:
        raise UsageError(f"Neplatná verze {v!r} v {MANIFEST} (MAJOR.MINOR.PATCH)")
    return tuple(int(x) for x in m.groups())


@dataclass
class Plan:
    versions: list[str] = field(default_factory=list)
    after: list[str] = field(default_factory=list)
    manual: list[dict] = field(default_factory=list)       # {version, id, text, key}
    crs: list[str] = field(default_factory=list)
    migrations: list[str] = field(default_factory=list)
    missing: bool = False                                  # nový core manifest nemá (verze před 0.14.0)

    def as_dict(self) -> dict:
        return {"versions": self.versions, "after": self.after, "manual": self.manual, "crs": self.crs,
                "migrations": self.migrations, "manifest_missing": self.missing}


def load_manifest(core: Path) -> list[dict] | None:
    """Záznamy manifestu; None = core manifest nemá. Chyba formátu = chyba použití (kód 2)."""
    p = Path(core) / MANIFEST
    if not p.is_file():
        return None
    data = load_yaml(p) or {}
    if not isinstance(data, dict) or data.get("upgrade") != 1:
        raise UsageError(f"{p}: neznámý formát manifestu (čekám upgrade: 1)")
    out = []
    for e in data.get("versions") or []:
        if not isinstance(e, dict):
            raise UsageError(f"{p}: záznam verze není mapa: {e!r}")
        ver = str(e.get("version"))
        vt(ver)
        after = list(e.get("after") or [])
        bad = [s for s in after if s not in AFTER_ORDER]
        if bad:
            raise UsageError(f"{p}: verze {ver}: neznámý krok {', '.join(map(str, bad))} "
                             f"(povolené: {', '.join(AFTER_ORDER)})")
        manual = []
        for m in e.get("manual") or []:
            if not isinstance(m, dict) or not m.get("id") or not str(m.get("text") or "").strip():
                raise UsageError(f"{p}: verze {ver}: ruční úkol potřebuje id a text: {m!r}")
            manual.append({"id": str(m["id"]), "text": str(m["text"]).strip()})
        out.append({"version": ver, "after": after, "manual": manual,
                    "crs": [str(c) for c in e.get("crs") or []], "migration": e.get("migration")})
    return out


def plan(core: Path, old: str, new: str) -> Plan:
    entries = load_manifest(core)
    if entries is None:
        return Plan(missing=True)
    lo, hi = vt(old), vt(new)
    sel = sorted((e for e in entries if lo < vt(e["version"]) <= hi), key=lambda e: vt(e["version"]))
    return Plan(versions=[e["version"] for e in sel],
                after=[s for s in AFTER_ORDER if any(s in e["after"] for e in sel)],
                manual=[{"version": e["version"], "id": m["id"], "text": m["text"],
                         "key": f"update_core:{e['version']}:{m['id']}"} for e in sel for m in e["manual"]],
                crs=list(dict.fromkeys(c for e in sel for c in e["crs"])),
                migrations=[str(e["migration"]) for e in sel if e.get("migration")])


def plan_lines(pl: Plan) -> list[str]:
    """Výpis plánu pro dry-run (řídicí skript i --after-only)."""
    if pl.missing:
        return ["Manifest upgrade.yaml v novém core chybí (verze před 0.14.0); kroky po aktualizaci podle CHANGELOG.md ručně."]
    out = [f"Kroky po aktualizaci (verze {', '.join(pl.versions) or '–'}): "
           + (" → ".join(pl.after) if pl.after else "žádné automatické") + "; pak lint --all a audit (dry-run)"]
    if pl.manual:
        out.append("Ruční úkoly (do queue.md):")
        out += [f"  {m['key']}: {m['text']}" for m in pl.manual]
    if pl.crs:
        out.append("CR k ověření v instanci (in_pilot): " + ", ".join(pl.crs))
    return out


def last_upgrade_from(vault: Vault, current: str) -> str | None:
    """Stará verze z posledního řádku „core <current> | aktualizace z <stará>“ v structure_version.md."""
    p = vault.root / SV_REL
    if not p.is_file():
        return None
    found = None
    for m in SV_RE.finditer(read_text(p)):
        if m.group(1) == current:
            found = m.group(2)
    return found


def _run_cli(core: Path, vault: Vault, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, "-I", str(core / "scripts" / "hestia.py"), *args,
                           "--vault", str(vault.root), "--json"],
                          capture_output=True, text=True, encoding="utf-8", env=env)


def _tail(r: subprocess.CompletedProcess) -> str:
    lines = [l for l in (r.stderr or "").splitlines() if l.strip()] or \
            [l for l in (r.stdout or "").splitlines() if l.strip()]
    return lines[-1].strip() if lines else f"návratový kód {r.returncode}"


def run_checks(core: Path, vault: Vault) -> dict:
    """lint --all a audit v dry-run; souhrn nálezů podle závažnosti."""
    out = {}
    for name, args in (("lint", ("lint", "--all")), ("audit", ("audit",))):
        r = _run_cli(core, vault, *args)
        if r.returncode not in (0, 1):
            out[name] = {"error": _tail(r)}
            continue
        try:
            data = json.loads(r.stdout or "null")
        except json.JSONDecodeError:
            out[name] = {"error": "nečitelný výstup"}
            continue
        if isinstance(data, list):
            counts = {s: sum(1 for f in data if f.get("severity") == s) for s in ("error", "warning", "info")}
        else:
            counts = dict((data or {}).get("counts") or {})
        out[name] = {"counts": counts}
    return out


def check_text(checks: dict) -> list[str]:
    out = []
    for name, c in checks.items():
        if "error" in c:
            out.append(f"{name}: neproběhl ({c['error']})")
        else:
            n = c["counts"]
            out.append(f"{name}: chyby {n.get('error', 0)}, upozornění {n.get('warning', 0)}, informace {n.get('info', 0)}")
    return out


def write_tasks(vault: Vault, manual: list[dict], day) -> tuple[list[str], list[str], str]:
    """Ruční úkoly do queue.md (T-…); vrací (nová ID, klíče už ve frontě, poznámka)."""
    p = vault.root / QUEUE_REL
    if not manual:
        return [], [], ""
    if not p.is_file():
        return [], [], "queue.md chybí; ruční úkoly jen v reportu"
    original = read_text(p)
    text = upgrade_queue(original)
    items = parse_queue(text)
    have = {it.code for it in items if it.kind == "task"}
    first = int(next_id(items, "task").split("-")[1])
    new, dup = [], []
    for m in manual:
        if m["key"] in have:
            dup.append(m["key"])
            continue
        new.append(QueueItem(f"T-{first + len(new):04d}", "medium", "task", m["key"], f"core {m['version']}",
                             m["text"], "open"))
    if new:
        atomic_write(p, write_queue(text, {}, new, today=day), expected_hash=file_hash(p))
    return [it.id for it in new], dup, ""


def report_md(day, old: str | None, new: str, swapped: bool, pl: Plan, steps: list[dict], remaining: list[str],
              checks: dict, task_ids: list[str], dup: list[str], note: str) -> str:
    lines = ["---", "type: report", f"updated: {day.isoformat()}", "---",
             f"# Aktualizace core {day.isoformat()}", "", "## Souhrn"]
    if swapped and old:
        lines.append(f"- Verze: {old} → {new}; starý core v `_to_delete/_core_{old}/`, řádek v `structure_version.md`.")
    else:
        lines.append(f"- Verze: {new}; jen kroky po aktualizaci (`update_core --after-only`"
                     + (f", rozsah od {old}" if old else ", rozsah neznámý: všechny automatické kroky") + ").")
    lines.append(f"- Záznamy manifestu: {', '.join(pl.versions) or '–'}.")
    lines += ["", "## Automatické kroky"]
    lines += [f"- `{s['step']}`: {'v pořádku' if s['ok'] else 'selhal: ' + s['message']}" for s in steps] or ["_Žádné._"]
    if remaining:
        lines.append(f"- Zbývá: {', '.join(remaining)} (doběhne `update_core --after-only --apply`).")
    lines += ["", "## Kontroly (dry-run)"] + [f"- {x}" for x in check_text(checks)]
    lines += ["", "## Ruční úkoly"]
    rows = []
    for m in pl.manual:
        state = "už ve frontě" if m["key"] in dup else ("ve frontě" if task_ids else "jen zde")
        rows.append(f"- `{m['key']}` ({state}): {m['text']}")
    lines += rows or ["_Žádné._"]
    if note:
        lines.append(f"- Upozornění: {note}")
    lines += ["", "## CR k ověření", *([f"- {c} (ověřit v instanci, do *Průběhu* `in_pilot`)" for c in pl.crs]
                                       or ["_Žádné._"])]
    return "\n".join(lines) + "\n"


def run_after(args, vault: Vault) -> tuple[int, dict, str]:
    core = vault.root / "_core"
    vp = core / "VERSION"
    if not vp.is_file():
        raise UsageError(f"Chybí {vp}; --after-only potřebuje nainstalovaný core")
    current = read_text(vp).strip()
    since = getattr(args, "since", None) or last_upgrade_from(vault, current)
    swapped = bool(getattr(args, "since", None))
    if since:
        pl = plan(core, since, current)
        if pl.missing:
            pl = Plan(after=list(AFTER_ORDER), missing=True)
    else:
        pl = Plan(after=list(AFTER_ORDER))
    day = today()
    payload = {"command": "update_core", "after_only": True, "applied": bool(args.apply), "version": current,
               "since": since, "upgrade": pl.as_dict()}
    if not args.apply:
        lines = [f"update_core --after-only: core {current}" + (f", rozsah od {since}" if since else
                 ", rozsah neznámý (structure_version.md): všechny automatické kroky") + " (dry-run, spusť s --apply)"]
        lines += plan_lines(pl)
        return EXIT_OK, payload, "\n".join(lines)

    steps, remaining = [], []
    for s in pl.after:
        if remaining:
            remaining.append(s)
            continue
        r = _run_cli(core, vault, s, "--apply")
        ok = r.returncode == 0
        steps.append({"step": s, "ok": ok, "code": r.returncode, "message": "" if ok else _tail(r)})
        if not ok:
            remaining.append(s)
    checks = run_checks(core, vault)
    task_ids, dup, note = write_tasks(vault, pl.manual, day)
    rep = vault.root / "Maintenance" / "reports" / f"update_core_{day.isoformat()}.md"
    text = report_md(day, since, current, swapped, pl, steps, remaining, checks, task_ids, dup, note)
    atomic_write(rep, text, expected_hash=file_hash(rep) if rep.exists() else None)
    payload.update({"steps": steps, "remaining": remaining, "checks": checks, "tasks": task_ids,
                    "tasks_existing": dup, "report": f"Maintenance/reports/{rep.name}"})
    lines = [f"Kroky po aktualizaci (core {current}" + (f", od {since}" if since else "") + "):"]
    lines += [f"  {s['step']}: {'v pořádku' if s['ok'] else 'selhal: ' + s['message']}" for s in steps] \
        or ["  žádné automatické kroky"]
    lines += [f"  {x}" for x in check_text(checks)]
    if task_ids:
        lines.append(f"Ruční úkoly do queue.md: {', '.join(task_ids)}")
    if dup:
        lines.append(f"Ruční úkoly už ve frontě: {', '.join(dup)}")
    if note:
        lines.append(f"Upozornění: {note}")
    if pl.crs:
        lines.append("CR k ověření v instanci (in_pilot): " + ", ".join(pl.crs))
    lines.append(f"Report: Maintenance/reports/{rep.name}")
    code = EXIT_OK
    if remaining:
        lines.append(f"Chyba: krok {remaining[0]} selhal; zbývá {', '.join(remaining)}. _core/ zůstává nový; "
                     f"po opravě doběhne update_core --after-only --apply")
        code = EXIT_FINDINGS
    return code, payload, "\n".join(lines)
