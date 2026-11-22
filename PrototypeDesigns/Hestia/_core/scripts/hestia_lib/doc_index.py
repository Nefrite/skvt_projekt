"""Příkaz doc_index: index dokumentů pro Knihovníka (zadání 13 kap. 10.10, 12 kap. 3b.5).

`Maintenance/doc_index.json` (generovaný, needitovat): záznam na poznámku vaultu mimo `_core/`, `Maintenance/`,
`Roles/_compiled/` (a `_to_delete/`). Pole: `path`, `title`, `aliases`, `type`, `validity`, `status`, `updated`,
`entity`, `domain`, `domains`, `depth`, `build_step`, `master`, `headings` (`##` a `###`), `links_out` (existující
poznámky, na které dokument odkazuje), `chars` (znaky těla) a `sections` (`{heading, level, line, end_line, chars}`
pro `##` a `###`, řádky souboru od 1, `end_line` včetně; zadání 0.21, příkaz `section`). Index obnovují i `hubs` a `audit`; zapisuje se jen při změně obsahu
(čas `generated` změnu nedělá).
"""
from __future__ import annotations

import datetime as _dt
import json
import re

from .changeset import ChangeSet
from .errors import EXIT_OK
from .fileio import read_text
from .links import extract_links, headings, links_in_value
from .model import Model
from .section import body_chars, outline
from .util import as_date, as_list, today
from .vault import Vault

JSON_REL = "Maintenance/doc_index.json"
EXCLUDE_PREFIXES = ("_core/", "Maintenance/", "Roles/_compiled/", "_to_delete/")


def _date(value) -> str | None:
    d = as_date(value)
    return d.isoformat() if d else (str(value) if value not in (None, "") else None)


def _title(note) -> str:
    h1 = [t for lvl, t, _ in headings(note.body) if lvl == 1]
    return h1[0] if h1 else note.name


def record(vault: Vault, m: Model, note) -> dict:
    fm = note.fm or {}
    links = []
    for target in links_in_value(fm) + [l.target for l in extract_links(note.body)]:
        rel, status = vault.resolve(target)
        if status == "ok" and rel and rel != note.rel and rel in vault.notes:
            links.append(vault.notes[rel].name)
    return {
        "path": note.rel, "title": _title(note), "aliases": [str(a) for a in as_list(fm.get("aliases")) if a],
        "type": fm.get("type"), "validity": fm.get("validity"), "status": fm.get("status"),
        "updated": _date(fm.get("updated")),
        "entity": m.entities_of(note) if fm.get("type") != "entity" else [],
        "domain": fm.get("domain"), "domains": [str(d) for d in as_list(fm.get("domains"))],
        "depth": fm.get("depth"), "build_step": fm.get("build_step"), "master": fm.get("master"),
        "headings": [t for lvl, t, _ in headings(note.body) if lvl in (2, 3)],
        "links_out": sorted(dict.fromkeys(links)),
        "chars": body_chars(note), "sections": outline(note),
    }


def build(vault: Vault, model: Model | None = None) -> list[dict]:
    m = model or Model(vault)
    return [record(vault, m, n) for rel, n in sorted(vault.notes.items())
            if not rel.startswith(EXCLUDE_PREFIXES) and n.fm is not None]


def render(records: list[dict], generated: str) -> str:
    rows = ",\n".join("  " + json.dumps(r, ensure_ascii=False, default=str) for r in records)
    body = f"\n{rows}\n" if rows else ""
    return f'{{"generated": {json.dumps(generated)}, "notes": [{body}]}}\n'


def _strip_time(text: str | None) -> str | None:
    return re.sub(r'"generated": "[^"]*"', '"generated": ""', text) if text else text


def plan(vault: Vault, cs: ChangeSet, model: Model | None = None, records: list[dict] | None = None) -> bool:
    """Naplánuje zápis indexu do sady změn; False, když se obsah nemění."""
    records = build(vault, model) if records is None else records
    p = vault.root / JSON_REL
    now = _dt.datetime.combine(today(), _dt.datetime.now().time()).replace(microsecond=0)
    new = render(records, now.isoformat())
    old = cs.current(p)
    if old is not None and _strip_time(old) == _strip_time(new):
        return False
    cs.write(p, new)
    return True


def load(vault: Vault) -> list[dict] | None:
    p = vault.root / JSON_REL
    try:
        return json.loads(read_text(p)).get("notes") if p.is_file() else None
    except (ValueError, AttributeError):
        return None


def run(args, vault: Vault) -> tuple[int, dict, str]:
    records = build(vault)
    cs = ChangeSet(vault.project_root)
    changed = plan(vault, cs, records=records)
    if args.apply and changed:
        cs.apply()
    state = ("zapsáno" if args.apply else "zapsalo by se (dry-run, zapiš s --apply)") if changed else "beze změny"
    payload = {"command": "doc_index", "applied": bool(args.apply and changed), "changed": changed,
               "notes": len(records)}
    return EXIT_OK, payload, f"doc_index: {len(records)} poznámek; {JSON_REL} {state}"
