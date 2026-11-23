"""Příkaz agenda: co čeká na roli (zadání 13 kap. 10.13, 12 kap. 3; zadání 0.21).

`agenda --role <Role>`: aktivní předání (`Handovers/` mimo `_archive/`, `validity` není neplatná) s `for_role`
obsahujícím roli a zvlášť předání bez `for_role` (cesta, titul, entita, `updated`, počet otevřených otázek
`- [ ]` v sekci `## Otevřené otázky`). Předání pro jiné role se nevypisují. U role core navíc její část:
Knihovník (`Librarian`) počet položek Inboxu `intake: raw`, Curator otevřené podněty `code: hestia` a ostatní
otevřené návrhy (`proposal`) ve frontě, Steward otevřené úkoly `update_core:*`. Nic nečte za roli, jen vypíše
seznam; `--json` pro skripty.

Od zadání 0.23 i karty assetů (modul `assets`, 13 kap. 10.16); od zadání 0.24 otevřené úkoly pro roli z fronty
(`code: role:<Role>`, 13 kap. 10.17) podle priority a ID; `agenda` bez role vypíše úkoly seskupené podle role.
"""
from __future__ import annotations

import re

from . import assets
from .errors import EXIT_OK
from .fileio import read_text
from .links import headings, section_text
from .logs import parse_queue
from .model import INACTIVE_VALIDITY, Model
from .util import as_date, as_list
from .vault import Note, Vault

HANDOVERS = "Handovers/"
ARCHIVE = "Handovers/_archive/"
QUEUE_REL = "Maintenance/queue.md"
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
_OPEN_Q_RE = re.compile(r"^\s*[-*]\s+\[ \]", re.M)


def _title(note: Note) -> str:
    h1 = [t for lvl, t, _ in headings(note.body) if lvl == 1]
    return h1[0] if h1 else note.name


def open_questions(note: Note) -> int:
    sec = section_text(note.body, "Otevřené otázky")
    return len(_OPEN_Q_RE.findall(sec)) if sec else 0


def handovers(vault: Vault, m: Model, role: str) -> tuple[list[dict], list[dict]]:
    """(předání pro roli, předání bez for_role)."""
    mine, anyone = [], []
    key = role.casefold()
    for rel, n in sorted(vault.notes.items()):
        if not rel.startswith(HANDOVERS) or rel.startswith(ARCHIVE) or n.type != "handover":
            continue
        fm = n.fm or {}
        if fm.get("validity") in INACTIVE_VALIDITY:
            continue
        roles = [str(r) for r in as_list(fm.get("for_role")) if r]
        d = as_date(fm.get("updated"))
        rec = {"path": rel, "title": _title(n), "entity": m.entities_of(n), "for_role": roles,
               "updated": d.isoformat() if d else None, "open_questions": open_questions(n)}
        if not roles:
            anyone.append(rec)
        elif key in {r.casefold() for r in roles}:
            mine.append(rec)
    return mine, anyone


def core_part(vault: Vault, role: str) -> dict | None:
    """Část role core (a Stewarda): co čeká v Inboxu nebo ve frontě."""
    r = role.casefold()
    if r == "librarian":
        raw = sorted(rel for rel, n in vault.notes.items()
                     if rel.startswith("Inbox/") and (n.fm or {}).get("intake") == "raw")
        return {"kind": "inbox_raw", "label": "Inbox `intake: raw`", "count": len(raw), "items": raw}
    if r not in ("curator", "steward"):
        return None
    p = vault.root / QUEUE_REL
    items = [i for i in parse_queue(read_text(p)) if i.is_open] if p.is_file() else []
    def row(i):
        return {"id": i.id, "kind": i.kind, "code": i.code, "target": i.target, "proposal": i.proposal,
                "state": i.state_value}
    if r == "curator":
        from .feedback import is_hestia_code                 # i `hestia:<kategorie>` (zadání 0.22)
        hestia = [row(i) for i in items if i.kind == "proposal" and is_hestia_code(i.code)]
        other = [row(i) for i in items if i.kind == "proposal" and not is_hestia_code(i.code)]
        return {"kind": "queue", "label": "podněty `code: hestia`", "count": len(hestia), "items": hestia,
                "proposals": other}
    tasks = [row(i) for i in items if i.kind == "task" and i.code.startswith("update_core:")]
    return {"kind": "queue", "label": "úkoly `update_core:*`", "count": len(tasks), "items": tasks}


def _line(h: dict) -> str:
    ent = f" · {', '.join(h['entity'])}" if h["entity"] else ""
    q = f" · otázky: {h['open_questions']}" if h["open_questions"] else ""
    return f"- {h['path']} — {h['title']}{ent} · updated {h['updated'] or '–'}{q}"


def role_tasks(vault: Vault, role: str | None = None) -> list[dict]:
    """Otevřené úkoly pro roli (`kind: task`, `code: role:<Role>`; 13 kap. 10.17, zadání 0.24) podle priority
    a ID; bez role všechny úkoly s cílovou rolí."""
    p = vault.root / QUEUE_REL
    items = [i for i in parse_queue(read_text(p)) if i.is_open and i.role] if p.is_file() else []
    if role is not None:
        items = [i for i in items if i.role.casefold() == role.casefold()]
    items.sort(key=lambda i: (PRIORITY_ORDER.get(i.priority.strip().lower(), 9), i.id))
    return [{"id": i.id, "role": i.role, "priority": i.priority, "target": i.target, "proposal": i.proposal,
             "state": i.state_value} for i in items]


def _task_line(t: dict) -> str:
    return f"- {t['id']} · {t['priority'] or '–'} · {t['target'] or '–'}: {t['proposal']}"


def run_all(vault: Vault) -> tuple[int, dict, str]:
    """`agenda` bez role: úkoly z fronty seskupené podle cílové role (13 kap. 10.17)."""
    tasks = role_tasks(vault)
    groups: dict[str, list[dict]] = {}
    for t in tasks:
        groups.setdefault(t["role"], []).append(t)
    payload = {"command": "agenda", "role": None, "tasks_by_role": groups}
    lines = [f"agenda: otevřené úkoly pro role ve frontě ({len(tasks)}); pro předání a část role zadej --role <Role>"]
    for r in sorted(groups, key=str.casefold):
        lines.append(f"{r} ({len(groups[r])}):")
        lines += [_task_line(t) for t in groups[r]]
    if not groups:
        lines.append("  žádné")
    return EXIT_OK, payload, "\n".join(lines)


def run(args, vault: Vault) -> tuple[int, dict, str]:
    role = (args.role or "").strip()
    if not role:
        return run_all(vault)
    m = Model(vault)
    mine, anyone = handovers(vault, m, role)
    tasks = role_tasks(vault, role)                                 # úkoly pro roli z fronty (zadání 0.24)
    part = core_part(vault, role)
    asset_part = assets.agenda_part(vault, role, m)                 # karty assetů (13 kap. 10.16, zadání 0.23)
    payload = {"command": "agenda", "role": role, "handovers": mine, "handovers_any": anyone, "tasks": tasks,
               "core": part, "assets": asset_part}
    lines = [f"agenda {role}:", f"Předání pro {role} ({len(mine)}):"]
    lines += [_line(h) for h in mine] or ["  žádné"]
    lines.append(f"Předání bez for_role ({len(anyone)}):")
    lines += [_line(h) for h in anyone] or ["  žádné"]
    lines.append(f"Úkoly pro {role} ve frontě ({len(tasks)}; podle priority a ID):")
    lines += [_task_line(t) for t in tasks] or ["  žádné"]
    if asset_part is not None:
        if asset_part["work"] is not None:
            lines.append(f"Karty assetů k výrobě ({len(asset_part['work'])}; požadavky a rozpracované, "
                         f"podle priority a data):")
            lines += [assets.card_line(c, with_owner=True) for c in asset_part["work"]] or ["  žádné"]
        if asset_part["requests"]:
            lines.append(f"Moje požadavky na assety ({len(asset_part['requests'])}):")
            lines += [assets.card_line(c, with_owner=True) for c in asset_part["requests"]]
    if part is not None:
        lines.append(f"{part['label']}: {part['count']}")
        for i in part["items"][:20]:
            lines.append(f"- {i}" if isinstance(i, str) else f"- {i['id']} {i['code']} {i['target']}: {i['proposal']}")
        if part.get("proposals"):
            lines.append(f"Ostatní otevřené návrhy: {len(part['proposals'])}")
    return EXIT_OK, payload, "\n".join(lines)
