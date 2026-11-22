"""Příkaz agenda: co čeká na roli (zadání 13 kap. 10.13, 12 kap. 3; zadání 0.21).

`agenda --role <Role>`: aktivní předání (`Handovers/` mimo `_archive/`, `validity` není neplatná) s `for_role`
obsahujícím roli a zvlášť předání bez `for_role` (cesta, titul, entita, `updated`, počet otevřených otázek
`- [ ]` v sekci `## Otevřené otázky`). Předání pro jiné role se nevypisují. U role core navíc její část:
Knihovník (`Librarian`) počet položek Inboxu `intake: raw`, Curator otevřené podněty `code: hestia` a ostatní
otevřené návrhy (`proposal`) ve frontě, Steward otevřené úkoly `update_core:*`. Nic nečte za roli, jen vypíše
seznam; `--json` pro skripty.
"""
from __future__ import annotations

import re

from .errors import EXIT_OK, UsageError
from .fileio import read_text
from .links import headings, section_text
from .logs import parse_queue
from .model import INACTIVE_VALIDITY, Model
from .util import as_date, as_list
from .vault import Note, Vault

HANDOVERS = "Handovers/"
ARCHIVE = "Handovers/_archive/"
QUEUE_REL = "Maintenance/queue.md"
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


def run(args, vault: Vault) -> tuple[int, dict, str]:
    role = (args.role or "").strip()
    if not role:
        raise UsageError("agenda: zadej --role <Role>")
    m = Model(vault)
    mine, anyone = handovers(vault, m, role)
    part = core_part(vault, role)
    payload = {"command": "agenda", "role": role, "handovers": mine, "handovers_any": anyone, "core": part}
    lines = [f"agenda {role}:", f"Předání pro {role} ({len(mine)}):"]
    lines += [_line(h) for h in mine] or ["  žádné"]
    lines.append(f"Předání bez for_role ({len(anyone)}):")
    lines += [_line(h) for h in anyone] or ["  žádné"]
    if part is not None:
        lines.append(f"{part['label']}: {part['count']}")
        for i in part["items"][:20]:
            lines.append(f"- {i}" if isinstance(i, str) else f"- {i['id']} {i['code']} {i['target']}: {i['proposal']}")
        if part.get("proposals"):
            lines.append(f"Ostatní otevřené návrhy: {len(part['proposals'])}")
    return EXIT_OK, payload, "\n".join(lines)
