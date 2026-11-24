"""Manifest `hestia/upgrade.yaml` a kroky po aktualizaci core (zadání 0.15; 13 kap. 10.6, 10.6a; 11 kap. 6).

- `load_manifest`, `plan`: záznamy verzí (stará, nová] sečtené: automatické kroky v pevném pořadí
  `asset_index` → `hubs` → `doc_index` → `compose_role` (každý jednou), ruční úkoly, CR k ověření, migrace.
- `with_compose`: `compose_role` při každé změně verze, jsou-li ve vaultu kompiláty (zadání 0.15.1).
- `run_after` (`update_core --after-only`): běží vždy v **novém** core (`_core/` po výměně; řídicí skript ho po
  `--apply` spustí jako podproces). Spustí automatické kroky s `--apply`, pak `lint --all` a `audit` jen
  v dry-run se souhrnem; ruční úkoly zapíše do `queue.md` jako `T-…` s klíčem `update_core:<verze>:<id>`
  (opakovaný běh je nezakládá znovu); report `Maintenance/reports/update_core_RRRR-MM-DD.md`.
  Selže-li krok, další kroky se nespouští, návratový kód 1 a výpis zbývajících kroků.
- Rozsah verzí: `--since` (předává řídicí skript), jinak poslední řádek `structure_version.md`
  „core <aktuální> | aktualizace z <stará>“; bez něj všechny automatické kroky bez ručních úkolů.
- Report (zadání 0.15.3): v reportu dne **oddíl na přechod** `## Přechod <stará> → <nová>`, další se připíše.
  Řídicí skript ho založí hned po výměně `_core/` (`start_section`, stav „kroky po aktualizaci neproběhly“),
  `run_after` ho přepisuje po každém kroku (stav, výsledky; u `asset_index` změny přiřazení, u ostatních počty);
  chybí-li (výměnu řídil starší core), založí ho. `--after-only` bez `--since` doplní oddíl posledního přechodu
  ze `structure_version.md` (report dne toho přechodu). Průběh kroků jde hned na stderr (flush).
- `unfinished`: přechod ze `structure_version.md`, jehož oddíl v reportu není „dokončeno“ (dry-run ho ohlásí).
- Příznak `roles` (zadání 0.17): verze, která mění základ projektových rolí, přidá ruční úkol
  `update_core:<verze>:role_base`; oddíl reportu *Základ projektových rolí* nese text příznaku, rozdíl `tpl_role`
  (starý core z `_to_delete/_core_<stará>/`) a profily v `Roles/` s `role_base` starším než verze příznaku.
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
SV_RE = re.compile(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*core (\d+\.\d+\.\d+)\s*\|\s*aktualizace z (\d+\.\d+\.\d+)")
QUEUE_REL = "Maintenance/queue.md"
SV_REL = "Maintenance/structure_version.md"
REPORTS_REL = "Maintenance/reports"
STATE_DONE = "dokončeno"
STATE_NOT_RUN = "kroky po aktualizaci neproběhly"
FIRST_WITH_REPORT = (0, 14, 0)          # verze, od které update_core píše report


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
    roles: list[dict] = field(default_factory=list)       # {version, text}: změny základu rolí (zadání 0.17)
    missing: bool = False                                  # nový core manifest nemá (verze před 0.14.0)

    def as_dict(self) -> dict:
        return {"versions": self.versions, "after": self.after, "manual": self.manual, "crs": self.crs,
                "migrations": self.migrations, "roles": self.roles, "manifest_missing": self.missing}


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
        roles = e.get("roles")
        if roles is not None and not (isinstance(roles, str) and roles.strip()):
            raise UsageError(f"{p}: verze {ver}: roles je krátký popis změny základu rolí (text): {roles!r}")
        out.append({"version": ver, "after": after, "manual": manual,
                    "crs": [str(c) for c in e.get("crs") or []], "migration": e.get("migration"),
                    "roles": roles.strip() if roles else None})
    return out


ROLE_BASE_ID = "role_base"


def roles_versions(core: Path, upto: str | None = None) -> list[dict]:
    """Záznamy s příznakem `roles` (zadání 0.17, 13 kap. 10.6a), vzestupně; `upto` = nanejvýš tato verze."""
    entries = load_manifest(core) or []
    sel = [e for e in entries if e.get("roles") and (upto is None or vt(e["version"]) <= vt(upto))]
    return [{"version": e["version"], "text": e["roles"]} for e in sorted(sel, key=lambda e: vt(e["version"]))]


def role_profiles(vault: Vault) -> list[dict]:
    """Profily projektových rolí `Roles/<Role>.md` (`type: role`) s hodnotou `role_base` (None = chybí)."""
    out = []
    for n in vault.notes.values():
        if n.type != "role" or not re.fullmatch(r"Roles/[^/]+\.md", n.rel):
            continue
        raw = n.fm.get("role_base")
        out.append({"role": n.name, "file": n.rel, "role_base": str(raw).strip() if raw not in (None, "") else None})
    return sorted(out, key=lambda x: x["role"])


def role_base_behind(value: str | None, version: str) -> str | None:
    """Důvod, proč profil není srovnaný se základem `version`; None = srovnaný."""
    if value is None:
        return "role_base chybí"
    if not VERSION_RE.match(value):
        return f"role_base {value!r} není verze MAJOR.MINOR.PATCH"
    if vt(value) < vt(version):
        return f"role_base {value} je starší než {version}"
    return None


def plan(core: Path, old: str, new: str) -> Plan:
    entries = load_manifest(core)
    if entries is None:
        return Plan(missing=True)
    lo, hi = vt(old), vt(new)
    sel = sorted((e for e in entries if lo < vt(e["version"]) <= hi), key=lambda e: vt(e["version"]))
    manual = []
    for e in sel:
        manual += [{"version": e["version"], "id": m["id"], "text": m["text"],
                    "key": f"update_core:{e['version']}:{m['id']}"} for m in e["manual"]]
        if e.get("roles"):        # příznak roles: ruční úkol srovnat profily (13 kap. 10.6a, zadání 0.17)
            manual.append({"version": e["version"], "id": ROLE_BASE_ID,
                           "text": f"Srovnat profily projektových rolí se základem {e['version']} ({e['roles']}); "
                                   f"po schválení GameDesignerem nastavit role_base: {e['version']} a spustit "
                                   f"compose_role (12 kap. 2.1, 13 kap. 10.6a)",
                           "key": f"update_core:{e['version']}:{ROLE_BASE_ID}"})
    return Plan(versions=[e["version"] for e in sel],
                after=[s for s in AFTER_ORDER if any(s in e["after"] for e in sel)],
                manual=manual,
                crs=list(dict.fromkeys(c for e in sel for c in e["crs"])),
                migrations=[str(e["migration"]) for e in sel if e.get("migration")],
                roles=[{"version": e["version"], "text": e["roles"]} for e in sel if e.get("roles")])


def has_compiled(vault: Vault) -> bool:
    d = vault.root / "Roles" / "_compiled"
    return d.is_dir() and any(d.glob("*_compiled.md"))


def with_compose(pl: Plan, vault: Vault, old: str | None, new: str) -> Plan:
    """`compose_role` při každé změně verze, jsou-li ve vaultu kompiláty, i bez záznamu v manifestu: hlavička
    kompilátu nese verzi core (13 kap. 10.6, 10.6a; zadání 0.15.1, CR_2026-11-21_compose_role_po_kazde_aktualizaci)."""
    if old and old != new and "compose_role" not in pl.after and has_compiled(vault):
        pl.after = [s for s in AFTER_ORDER if s in pl.after or s == "compose_role"]
    return pl


def plan_lines(pl: Plan) -> list[str]:
    """Výpis plánu pro dry-run (řídicí skript i --after-only)."""
    if pl.missing:
        return ["Manifest upgrade.yaml v novém core chybí (verze před 0.14.0); kroky po aktualizaci podle CHANGELOG.md ručně."]
    out = [f"Kroky po aktualizaci (verze {', '.join(pl.versions) or '–'}): "
           + (" → ".join(pl.after) if pl.after else "žádné automatické") + "; pak lint --all a audit (dry-run)"]
    if pl.manual:
        out.append("Ruční úkoly (do queue.md):")
        out += [f"  {m['key']}: {m['text']}" for m in pl.manual]
    if pl.roles:
        out.append("Změna základu projektových rolí: "
                   + "; ".join(f"{r['version']}: {r['text']}" for r in pl.roles))
    if pl.crs:
        out.append("CR k ověření v instanci (in_pilot): " + ", ".join(pl.crs))
    return out


def last_upgrade(vault: Vault, current: str) -> tuple[str, str] | None:
    """(datum, stará verze) z posledního řádku „core <current> | aktualizace z <stará>“ v structure_version.md."""
    p = vault.root / SV_REL
    if not p.is_file():
        return None
    found = None
    for m in SV_RE.finditer(read_text(p)):
        if m.group(2) == current:
            found = (m.group(1), m.group(3))
    return found


def last_upgrade_from(vault: Vault, current: str) -> str | None:
    last = last_upgrade(vault, current)
    return last[1] if last else None


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


def step_details(step: str, data) -> list[str]:
    """Podstatný výstup kroku do reportu: u `asset_index` změny přiřazení, u ostatních nanejvýš počty (0.15.3)."""
    if not isinstance(data, dict):
        return []
    if step == "asset_index":
        moved = data.get("reassigned") or []
        return [f"Změna přiřazení: {m.get('path')}: {m.get('from') or '–'} → {m.get('to') or '–'} "
                f"({m.get('rule') or '–'})" for m in moved] or ["bez změn přiřazení"]
    if step == "hubs":
        return [f"změněné soubory: {len(data.get('changed') or [])}"]
    if step == "doc_index":
        return ["index změněn" if data.get("changed") else "index beze změny"]
    if step == "compose_role":                      # changed nahrát, unchanged ne (zadání 0.28, CR-034)
        roles = data.get("roles") or []
        n = sum(1 for r in roles if r.get("status") in ("new", "changed"))
        changed = data.get("changed") or []
        unchanged = data.get("unchanged") or []
        return [f"změněné kompiláty: {n} z {len(roles)}",
                "changed (nahrát do Claude Projectu): " + (", ".join(changed) or "žádný"),
                "unchanged (nenahrávat): " + (", ".join(unchanged) or "žádný")]
    return []


def report_path(vault: Vault, day: str) -> Path:
    return vault.root / REPORTS_REL / f"update_core_{day}.md"


def section_heading(old: str | None, new: str) -> str:
    return f"## Přechod {old} → {new}" if old else f"## Kroky po aktualizaci (core {new})"


def find_trash(vault: Vault, old: str) -> str | None:
    """Poslední `_to_delete/_core_<stará>[_N]/` (update_core volí první volné N)."""
    d = vault.root / "_to_delete"
    best = None
    for p in d.glob(f"_core_{old}*") if d.is_dir() else []:
        m = re.fullmatch(rf"_core_{re.escape(old)}(?:_(\d+))?", p.name)
        if m and p.is_dir():
            n = int(m.group(1) or 1)
            if best is None or n > best[0]:
                best = (n, p.name)
    return f"_to_delete/{best[1]}/" if best else None


TPL_ROLE_REL = "templates/tpl_role.md"


def roles_info(vault: Vault, core: Path, swap: str | None, pl: Plan) -> dict | None:
    """Podklad k příznaku `roles` do reportu (13 kap. 10.6a): text příznaku, rozdíl `tpl_role` mezi starým
    (`_to_delete/_core_<stará>/`) a novým core, profily v `Roles/` s `role_base` starším než verze příznaku."""
    if not pl.roles:
        return None
    import difflib
    target = pl.roles[-1]["version"]
    old_tpl = vault.root / swap / TPL_ROLE_REL if swap else None
    new_tpl = core / TPL_ROLE_REL
    diff = None
    if old_tpl is not None and old_tpl.is_file() and new_tpl.is_file():
        diff = list(difflib.unified_diff(read_text(old_tpl).replace("\r\n", "\n").splitlines(),
                                         read_text(new_tpl).replace("\r\n", "\n").splitlines(),
                                         "tpl_role (starý core)", "tpl_role (nový core)", lineterm=""))
    profiles = [dict(p, reason=why) for p in role_profiles(vault)
                if (why := role_base_behind(p["role_base"], target))]
    return {"version": target, "changes": pl.roles, "tpl_role_diff": diff, "profiles": profiles}


def roles_md(info: dict) -> list[str]:
    lines = ["", "### Základ projektových rolí"]
    lines += [f"- Změna v {r['version']}: {r['text']}" for r in info["changes"]]
    d = info["tpl_role_diff"]
    if d is None:
        lines.append("- Rozdíl `tpl_role`: starý core nenalezen, porovnej s `_core/templates/tpl_role.md` ručně.")
    elif not d:
        lines.append("- Rozdíl `tpl_role`: beze změny šablony.")
    else:
        lines += ["- Rozdíl `tpl_role`:", "", "```diff", *d, "```", ""]
    if info["profiles"]:
        lines.append(f"- Profily nesrovnané se základem {info['version']} (ruční úkol `role_base`):")
        lines += [f"  - `{p['file']}`: {p['reason']}" for p in info["profiles"]]
    else:
        lines.append(f"- Profily v `Roles/`: všechny mají `role_base` {info['version']} nebo novější.")
    return lines


def roles_lines(info: dict | None) -> list[str]:
    """Krátký textový výpis k příznaku `roles` (rozdíl `tpl_role` je jen v reportu)."""
    if not info:
        return []
    out = [f"Změna základu projektových rolí ({info['version']}): "
           + "; ".join(r["text"] for r in info["changes"]) + " (rozdíl tpl_role v reportu)"]
    if info["profiles"]:
        out.append("Profily nesrovnané se základem: "
                   + ", ".join(f"{p['role']} ({p['reason']})" for p in info["profiles"]))
    return out


def instruction_lines(vault: Vault, old_core: Path | None, new_core: Path) -> list[str]:
    """Oddíl *Změny instrukcí* (13 kap. 10.6, zadání 0.21): změněné sekce instrukcí a role, které je používají."""
    from . import instructions
    changes = instructions.changes_between(old_core, new_core)
    roles = instructions.usage(vault, new_core, changes) if changes else None
    return instructions.section_md(changes, roles)


def section_md(old: str | None, new: str, state: str, swap: str | None, pl: Plan, steps: list[dict],
               remaining: list[str], checks: dict | None, tasks: tuple | None, roles: dict | None = None,
               instr: list[str] | None = None) -> str:
    """Oddíl přechodu v reportu; swap None = bez výměny (rozsah neznámý), "" = starý core nenalezen."""
    lines = [section_heading(old, new), f"- Stav: {state}"]
    if swap is not None:
        lines.append(f"- Výměna `_core/`: starý core v `{swap}`; řádek v `structure_version.md`." if swap
                     else "- Výměna `_core/`: starý core v `_to_delete/` nenalezen.")
    lines.append(f"- Záznamy manifestu: {', '.join(pl.versions) or '–'}.")
    lines += ["", "### Automatické kroky"]
    done = {s["step"] for s in steps}
    for s in steps:
        lines.append(f"- `{s['step']}`: {'v pořádku' if s['ok'] else 'selhal: ' + s['message']}")
        lines += [f"  - {d}" for d in s.get("details") or []]
    if remaining:
        lines.append(f"- Zbývá: {', '.join(remaining)} (doběhne `update_core --after-only --apply`).")
    else:
        lines += [f"- `{s}`: neproběhl" for s in pl.after if s not in done]
    if not pl.after and not steps:
        lines.append("_Žádné._")
    lines += ["", "### Kontroly (dry-run)"]
    lines += [f"- {x}" for x in check_text(checks)] if checks is not None else ["_Zatím neproběhly._"]
    lines += ["", "### Ruční úkoly"]
    task_ids, dup, note = tasks if tasks is not None else (None, [], "")
    for m in pl.manual:
        state_m = ("čeká na kroky po aktualizaci" if task_ids is None else
                   "už ve frontě" if m["key"] in dup else "ve frontě" if task_ids else "jen zde")
        lines.append(f"- `{m['key']}` ({state_m}): {m['text']}")
    if not pl.manual:
        lines.append("_Žádné._")
    if note:
        lines.append(f"- Upozornění: {note}")
    if roles:
        lines += roles_md(roles)
    if instr:
        lines += instr
    lines += ["", "### CR k ověření", *([f"- {c} (ověřit v instanci, do *Průběhu* `in_pilot`)" for c in pl.crs]
                                        or ["_Žádné._"])]
    return "\n".join(lines) + "\n"


def write_section(vault: Vault, day: str, text: str) -> Path:
    """Oddíl přechodu do reportu dne: existující oddíl se stejným nadpisem (poslední) přepíše, jinak připíše."""
    p = report_path(vault, day)
    heading = text.split("\n", 1)[0]
    if not p.is_file():
        atomic_write(p, "\n".join(["---", "type: report", f"updated: {day}", "---", f"# Aktualizace core {day}",
                                   "", text]))
        return p
    cur = read_text(p).replace("\r\n", "\n")
    found = list(re.finditer(rf"^{re.escape(heading)}\n.*?(?=^## |\Z)", cur, re.M | re.S))
    if found:
        m = found[-1]
        rest = cur[m.end():]
        new = cur[:m.start()] + text + ("\n" + rest if rest else "")
    else:
        new = cur.rstrip("\n") + "\n\n" + text
    atomic_write(p, new, expected_hash=file_hash(p))
    return p


def start_section(vault: Vault, old: str, new: str, pl: Plan, instr: list[str] | None = None) -> Path:
    """Řídicí skript hned po výměně `_core/`: oddíl přechodu se stavem „kroky po aktualizaci neproběhly“;
    `instr` = oddíl *Změny instrukcí* spočtený před výměnou (starý a nový core vedle sebe)."""
    return write_section(vault, today().isoformat(),
                         section_md(old, new, STATE_NOT_RUN, find_trash(vault, old) or "", pl, [], [], None, None,
                                    instr=instr))


def unfinished(vault: Vault, current: str) -> dict | None:
    """Poslední přechod na `current` ze `structure_version.md`, jehož oddíl v reportu není „dokončeno“."""
    if vt(current) < FIRST_WITH_REPORT:
        return None
    last = last_upgrade(vault, current)
    if not last:
        return None
    day, old = last
    p = report_path(vault, day)
    text = read_text(p).replace("\r\n", "\n") if p.is_file() else ""
    states = re.findall(rf"^{re.escape(section_heading(old, current))}\n- Stav: (.*)$", text, re.M)
    if states:
        if states[-1].startswith(STATE_DONE):
            return None
        state = states[-1]
    elif f"Verze: {old} → {current}" in text or f"rozsah od {old}" in text:     # report před 0.14.3
        return None
    else:
        state = "bez reportu"
    return {"from": old, "to": current, "date": day, "state": state, "report": f"{REPORTS_REL}/{p.name}"}


def unfinished_line(u: dict) -> str:
    return (f"Nedokončený přechod {u['from']} → {u['to']} ({u['date']}, {u['state']}): "
            f"kroky po aktualizaci nedoběhly; spusť update_core --after-only --apply")


def run_after(args, vault: Vault) -> tuple[int, dict, str]:
    core = vault.root / "_core"
    vp = core / "VERSION"
    if not vp.is_file():
        raise UsageError(f"Chybí {vp}; --after-only potřebuje nainstalovaný core")
    current = read_text(vp).strip()
    last = last_upgrade(vault, current)
    since = getattr(args, "since", None) or (last[1] if last else None)
    swapped = bool(getattr(args, "since", None))
    if since:
        pl = plan(core, since, current)
        if pl.missing:
            pl = Plan(after=list(AFTER_ORDER), missing=True)
        with_compose(pl, vault, since, current)
    else:
        pl = Plan(after=list(AFTER_ORDER))
    day = today()
    # oddíl přechodu: z řídicího skriptu dnes, jinak v reportu dne posledního přechodu (structure_version.md)
    rep_day = last[0] if (not swapped and since and last) else day.isoformat()
    payload = {"command": "update_core", "after_only": True, "applied": bool(args.apply), "version": current,
               "since": since, "upgrade": pl.as_dict()}
    if not args.apply:
        lines = [f"update_core --after-only: core {current}" + (f", rozsah od {since}" if since else
                 ", rozsah neznámý (structure_version.md): všechny automatické kroky") + " (dry-run, spusť s --apply)"]
        lines += plan_lines(pl)
        return EXIT_OK, payload, "\n".join(lines)

    quiet = getattr(args, "quiet", False)

    def progress(msg: str) -> None:
        if not quiet:
            print(msg, file=sys.stderr, flush=True)

    swap = (find_trash(vault, since) or "") if since else None
    steps, remaining = [], []
    roles = roles_info(vault, core, swap, pl)
    instr = instruction_lines(vault, vault.root / swap if swap else None, core) if swap is not None else None

    def save(state: str, checks: dict | None = None, tasks: tuple | None = None) -> Path:
        return write_section(vault, rep_day, section_md(since, current, state, swap, pl, steps, remaining,
                                                        checks, tasks, roles, instr))

    save("kroky probíhají")
    for s in pl.after:
        if remaining:
            remaining.append(s)
            continue
        progress(f"update_core: {s} …")
        r = _run_cli(core, vault, s, "--apply")
        ok = r.returncode == 0
        try:
            data = json.loads(r.stdout or "null")
        except json.JSONDecodeError:
            data = None
        details = step_details(s, data) if ok else []
        steps.append({"step": s, "ok": ok, "code": r.returncode, "message": "" if ok else _tail(r),
                      "details": details})
        progress(f"update_core: {s}: " + ("v pořádku" if ok else "selhal: " + _tail(r))
                 + "".join(f"\n  {d}" for d in details))
        if not ok:
            remaining.append(s)
        save("kroky probíhají" if ok else f"krok {s} selhal")
    progress("update_core: kontroly lint --all a audit (dry-run) …")
    checks = run_checks(core, vault)
    task_ids, dup, note = write_tasks(vault, pl.manual, day)
    state = STATE_DONE if not remaining else \
        f"krok {remaining[0]} selhal; zbývá {', '.join(remaining)} (doběhne `update_core --after-only --apply`)"
    rep = save(state, checks, (task_ids, dup, note))
    rep_rel = f"{REPORTS_REL}/{rep.name}"
    payload.update({"steps": steps, "remaining": remaining, "checks": checks, "tasks": task_ids,
                    "tasks_existing": dup, "report": rep_rel, "report_section": section_heading(since, current)[3:],
                    "roles": roles})
    lines = [f"Kroky po aktualizaci (core {current}" + (f", od {since}" if since else "") + "):"]
    for s in steps:
        lines.append(f"  {s['step']}: {'v pořádku' if s['ok'] else 'selhal: ' + s['message']}")
        lines += [f"    {d}" for d in s["details"]]
    if not steps:
        lines.append("  žádné automatické kroky")
    lines += [f"  {x}" for x in check_text(checks)]
    if task_ids:
        lines.append(f"Ruční úkoly do queue.md: {', '.join(task_ids)}")
    if dup:
        lines.append(f"Ruční úkoly už ve frontě: {', '.join(dup)}")
    if note:
        lines.append(f"Upozornění: {note}")
    lines += roles_lines(roles)
    if pl.crs:
        lines.append("CR k ověření v instanci (in_pilot): " + ", ".join(pl.crs))
    lines.append(f"Report: {rep_rel} (oddíl {section_heading(since, current)[3:]})")
    code = EXIT_OK
    if remaining:
        lines.append(f"Chyba: krok {remaining[0]} selhal; zbývá {', '.join(remaining)}. _core/ zůstává nový; "
                     f"po opravě doběhne update_core --after-only --apply")
        code = EXIT_FINDINGS
    return code, payload, "\n".join(lines)
