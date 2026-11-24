"""Příkaz doc_index: index dokumentů pro Knihovníka (zadání 13 kap. 10.10, 12 kap. 3b.5).

`Maintenance/doc_index.json` (generovaný, needitovat): záznam na poznámku vaultu mimo `_core/`, `Maintenance/`,
`Roles/_compiled/` (a `_to_delete/`). Pole: `path`, `title`, `aliases`, `type`, `validity`, `status`, `updated`,
`entity`, `domain`, `domains`, `depth`, `build_step`, `master`, `headings` (`##` a `###`), `links_out` (existující
poznámky, na které dokument odkazuje), `chars` (znaky těla) a `sections` (`{heading, level, line, end_line, chars}`
pro `##` a `###`, řádky souboru od 1, `end_line` včetně; zadání 0.21, příkaz `section`), `for_role` a `text_hash`
(otisk textu souboru; zadání 0.28, CR-033). Index obnovují i `hubs` a `audit`; zapisuje se jen při změně obsahu
(čas `generated` změnu nedělá).

Mezipaměť textu `Maintenance/doc_index_text.json` (generovaná, zadání 0.28, CR-033): celý text souboru u dokumentů
pod `doc_split_chars` (`{"generated", "texts": {cesta: text}}`); zapisuje se spolu s indexem. `fresh()` vrátí
záznamy a texty pro `section` a `find` bez čtení vaultu: soubor se čte jen u poznámky, která v indexu chybí nebo
má `mtime` novější než `doc_index.json`; záznam bez souboru vypadne.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
from dataclasses import dataclass, field

from .changeset import ChangeSet
from .errors import EXIT_OK
from .fileio import read_text
from .links import extract_links, headings, links_in_value
from .model import LinkResolver, Model
from .section import body_chars, outline
from .util import as_date, as_list, today
from .vault import Vault

JSON_REL = "Maintenance/doc_index.json"
TEXT_REL = "Maintenance/doc_index_text.json"
EXCLUDE_PREFIXES = ("_core/", "Maintenance/", "Roles/_compiled/", "_to_delete/")


def _date(value) -> str | None:
    d = as_date(value)
    return d.isoformat() if d else (str(value) if value not in (None, "") else None)


def _title(note) -> str:
    h1 = [t for lvl, t, _ in headings(note.body) if lvl == 1]
    return h1[0] if h1 else note.name


def text_hash(text: str) -> str:
    """Otisk textu souboru (konce řádků sjednocené), pro platnost mezipaměti textu."""
    return hashlib.sha1(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()[:16]


def split_limit(vault: Vault) -> int:
    return int(vault.config.get("doc_split_chars") or 20000)


def record(vault: Vault, m: LinkResolver, note) -> dict:
    fm = note.fm or {}
    links = []
    for target in links_in_value(fm) + [l.target for l in extract_links(note.body)]:
        rel, status = vault.resolve(target)
        if status == "ok" and rel and rel != note.rel and rel in vault.notes:
            links.append(vault.notes[rel].name)
    rec = {
        "path": note.rel, "title": _title(note), "aliases": [str(a) for a in as_list(fm.get("aliases")) if a],
        "type": fm.get("type"), "validity": fm.get("validity"), "status": fm.get("status"),
        "updated": _date(fm.get("updated")),
        "entity": m.entities_of(note) if fm.get("type") != "entity" else [],
        "domain": fm.get("domain"), "domains": [str(d) for d in as_list(fm.get("domains"))],
        "depth": fm.get("depth"), "build_step": fm.get("build_step"), "master": fm.get("master"),
        "headings": [t for lvl, t, _ in headings(note.body) if lvl in (2, 3)],
        "links_out": sorted(dict.fromkeys(links)),
        "chars": body_chars(note), "sections": outline(note),
        "for_role": [str(r) for r in as_list(fm.get("for_role")) if r], "text_hash": text_hash(note.text),
    }
    if fm.get("type") == "asset":           # karta assetu: entity z used_by, stav (13 kap. 10.16, zadání 0.23)
        rec["entity"] = m.link_names(fm.get("used_by"))
        rec["asset_status"] = fm.get("asset_status")
    return rec


def build(vault: Vault, model: Model | None = None) -> list[dict]:
    from . import assets, ue_assets
    m = model or Model(vault)
    cards = assets.cards(vault, m) if vault.game_layer else []
    outdated = ue_assets.outdated_names(vault) if cards else None
    out = []
    for rel, n in sorted(vault.notes.items()):
        if rel.startswith(EXCLUDE_PREFIXES) or n.fm is None:
            continue
        rec = record(vault, m, n)
        if cards and rec["type"] == "entity":     # souhrn assetů entity jako u bloku ## Assety (13 kap. 10.19)
            s = assets.entity_summary(n.name, cards, outdated)
            if s:
                rec["assets"] = s
        out.append(rec)
    return out


def render(records: list[dict], generated: str) -> str:
    rows = ",\n".join("  " + json.dumps(r, ensure_ascii=False, default=str) for r in records)
    body = f"\n{rows}\n" if rows else ""
    return f'{{"generated": {json.dumps(generated)}, "notes": [{body}]}}\n'


def render_texts(texts: dict[str, str], generated: str) -> str:
    rows = ",\n".join(f"  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}"
                       for k, v in sorted(texts.items()))
    body = f"\n{rows}\n" if rows else ""
    return f'{{"generated": {json.dumps(generated)}, "texts": {{{body}}}}}\n'


def texts_for(vault: Vault, records: list[dict], texts: dict[str, str] | None = None) -> dict[str, str]:
    """Texty dokumentů pod `doc_split_chars` pro mezipaměť (z `texts`, jinak ze souboru)."""
    limit = split_limit(vault)
    out = {}
    for r in records:
        if (r.get("chars") or 0) >= limit:
            continue
        t = (texts or {}).get(r["path"])
        out[r["path"]] = t if t is not None else vault.notes[r["path"]].text
    return out


def _strip_time(text: str | None) -> str | None:
    return re.sub(r'"generated": "[^"]*"', '"generated": ""', text) if text else text


def plan(vault: Vault, cs: ChangeSet, model: Model | None = None, records: list[dict] | None = None,
         texts: dict[str, str] | None = None) -> bool:
    """Naplánuje zápis indexu a mezipaměti textu do sady změn; False, když se obsah nemění."""
    records = build(vault, model) if records is None else records
    now = _dt.datetime.combine(today(), _dt.datetime.now().time()).replace(microsecond=0).isoformat()
    changed = False
    for rel, new in ((JSON_REL, render(records, now)),
                     (TEXT_REL, render_texts(texts_for(vault, records, texts), now))):
        p = vault.root / rel
        old = cs.current(p)
        if old is not None and _strip_time(old) == _strip_time(new):
            continue
        cs.write(p, new)
        changed = True
    return changed


def load(vault: Vault) -> list[dict] | None:
    p = vault.root / JSON_REL
    try:
        return json.loads(read_text(p)).get("notes") if p.is_file() else None
    except (ValueError, AttributeError):
        return None


def load_texts(vault: Vault) -> dict[str, str]:
    p = vault.root / TEXT_REL
    try:
        data = json.loads(read_text(p)) if p.is_file() else {}
        return dict(data.get("texts") or {}) if isinstance(data, dict) else {}
    except (ValueError, AttributeError, TypeError):
        return {}


@dataclass
class Fresh:
    """Záznamy indexu a texty pro čtecí příkazy (section, find); `read` = poznámky čtené ze souboru."""
    records: list[dict]
    texts: dict[str, str]
    read: list[str] = field(default_factory=list)
    rebuilt: bool = False                       # index chyběl, záznamy z celého vaultu

    def by_path(self) -> dict[str, dict]:
        return {r["path"]: r for r in self.records}


def fresh(vault: Vault) -> Fresh:
    """Záznamy z `doc_index.json` a texty z mezipaměti; znovu se čte jen poznámka, která v indexu chybí nebo má
    `mtime` novější než index (zadání 0.28, CR-033). Bez indexu záznamy celého vaultu (čte vše)."""
    p = vault.root / JSON_REL
    old = load(vault)
    if old is None:
        records = build(vault)
        return Fresh(records, {r["path"]: vault.notes[r["path"]].text for r in records},
                     [r["path"] for r in records], True)
    stamp = p.stat().st_mtime
    cached = load_texts(vault)
    prev = {r.get("path"): r for r in old if isinstance(r, dict)}
    resolver = LinkResolver(vault)
    records, texts, read = [], {}, []
    for rel, n in sorted(vault.notes.items()):
        if rel.startswith(EXCLUDE_PREFIXES):
            continue
        r = prev.get(rel)
        try:
            newer = n.path.stat().st_mtime > stamp
        except OSError:
            continue
        if r is not None and not newer:
            records.append(r)
            t = cached.get(rel)
            if t is not None and text_hash(t) == r.get("text_hash"):
                texts[rel] = t
            continue
        read.append(rel)
        if n.fm is None:
            continue
        rec = record(vault, resolver, n)
        if r is not None and "assets" in r and rec["type"] == "entity":
            rec["assets"] = r["assets"]          # souhrn assetů ze starého indexu (karty se nečtou)
        records.append(rec)
        texts[rel] = n.text
    return Fresh(records, texts, read)


def text_of(vault: Vault, fr: Fresh, rel: str) -> str:
    """Text poznámky z mezipaměti, jinak ze souboru (velké dokumenty se do mezipaměti nedávají)."""
    t = fr.texts.get(rel)
    if t is None:
        t = vault.notes[rel].text
        fr.texts[rel] = t
    return t


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
