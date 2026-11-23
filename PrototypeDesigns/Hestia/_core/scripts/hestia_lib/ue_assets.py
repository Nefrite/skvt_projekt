"""Stav knihovních assetů v Unrealu, etapa C (zadání 13 kap. 10.19; 0.26; CR-028, CR-029 bod 6).

**Jen čtení**, stejný mechanismus jako čtení actorů (kap. 10.11): `ue_query --assets --emit` vygeneruje čtecí skript
se seznamem assetů ze sekce `library` v `asset_index.json` (výchozí karty od `generated`; `--category`, `--asset`,
`--all-library`); `hestia_ue.collect_assets` v editoru zjistí `does_asset_exist` a u existujícího assetu
`get_metadata_tag` pro každý `ue_tag` z manifestu (`versions`, `global_versions`), nic neukládá. `ue_query --import`
výsledek assetů uloží do `Maintenance/reports/ue_assets.json`: na asset `ue_path`, existuje, tagy, verze v kódu
a stav `current` / `outdated` / `missing`. Assety, které nový výsledek nečetl, zůstanou v reportu se svým datem.

Dál: blok *Stav v UE* v kartě (`card_block`, `hubs`), G15 z Unrealu (`g15`; stáří podle data čtení `read` každého assetu, zadání 0.26.1), počet `outdated` pro souhrn
v `## Assety` hubu a `doc_index` (`outdated_names`). Stav karty se nemění.
"""
from __future__ import annotations

import datetime as _dt
import json

from .errors import UsageError
from .fileio import read_text
from .util import today

REPORT_REL = "Maintenance/reports/ue_assets.json"
REQUEST_ID = "assets"
UE_HEADING = "Stav v UE"
UE_MARK = "<!-- hestia:asset_ue -->"
STATES = ("current", "outdated", "missing")
FROM_GENERATED = {"generated", "imported", "verified"}


# ---------------------------------------------------------------- report

def load_report(vault) -> dict | None:
    p = vault.root / REPORT_REL
    try:
        data = json.loads(read_text(p)) if p.is_file() else None
    except ValueError:
        return None
    return data if isinstance(data, dict) and isinstance(data.get("assets"), dict) else None


def report_date(rep: dict | None) -> _dt.date | None:
    try:
        return _dt.date.fromisoformat(str((rep or {}).get("generated") or "")[:10])
    except ValueError:
        return None


def read_date(rec: dict, rep: dict | None = None) -> _dt.date | None:
    """Datum čtení assetu (`read`; starší záznam bez něj = `generated` reportu)."""
    try:
        return _dt.date.fromisoformat(str(rec.get("read") or (rep or {}).get("generated") or "")[:10])
    except ValueError:
        return None


def report_days(vault) -> int:
    return int(vault.config.get("ue_report_days") or 14)


def is_old(vault, d: _dt.date | None, day: _dt.date | None = None) -> bool:
    """Čtení starší než `ue_report_days` (po assetech, zadání 0.26.1)."""
    return d is None or ((day or today()) - d).days > report_days(vault)


def _int(value):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def state(rec: dict, entry: dict | None, globals_: dict) -> tuple[str, list[str]]:
    """Stav assetu z čtení UE proti kódu: (`current`/`outdated`/`missing`, důvody). Tag, který v UE chybí, znamená
    neznámou verzi = `outdated` (čeká na import)."""
    if not rec.get("exists"):
        return "missing", ["v UE chybí"]
    tags = rec.get("tags") or {}
    why = []
    if entry and entry.get("version_tag") and entry.get("version") is not None:
        ue_v, code_v = _int(tags.get(entry["version_tag"])), _int(entry["version"])
        if code_v is not None and (ue_v is None or ue_v < code_v):
            why.append(f"`{entry['version_tag']}` {ue_v if ue_v is not None else 'bez tagu'} < {code_v}")
    for var, g in sorted(globals_.items()):
        tag = g.get("ue_tag")
        code_v = _int(g.get("value"))
        if not tag or code_v is None:
            continue
        ue_v = _int(tags.get(tag))
        if ue_v is None or ue_v < code_v:
            why.append(f"`{tag}` {ue_v if ue_v is not None else 'bez tagu'} < `{var}` {code_v}")
    return ("outdated" if why else "current"), why


def _index(vault) -> dict:
    from . import asset_index as ai
    idx = ai.load_json(vault)
    if idx is None or not isinstance(idx.get("library"), list):
        raise UsageError("ue_query --assets: asset_index.json nemá sekci library; nejdřív asset_sources.yaml "
                         "a asset_index --apply (13 kap. 10.18)")
    return idx


def select(vault, idx: dict, category: str | None, asset: str | None, all_library: bool) -> list[dict]:
    """Assety ke čtení: výchozí karty od `generated`, `--all-library` všechny; `--category`, `--asset` zúží."""
    from . import assets
    status = {c.rel: c.status for c in assets.cards(vault)}
    names_of_card = {c.name: [c.name, *c.variants] for c in assets.cards(vault)}
    out = []
    for e in idx["library"]:
        if not all_library and not asset and status.get(e.get("card") or "") not in FROM_GENERATED:
            continue
        if category and e.get("category") != category:
            continue
        if asset and e["name"] != asset and e["name"] not in names_of_card.get(asset, []):
            continue
        out.append(e)
    return out


def request(vault, args) -> dict:
    from .ue import FORMAT, PATH_STAGE1
    idx = _index(vault)
    picked = select(vault, idx, args.category, args.asset, args.all_library)
    if not picked:
        raise UsageError("ue_query --assets: výběr je prázdný (výchozí: karty od generated; zkus --all-library, "
                         "--category nebo --asset)")
    if any(not e.get("ue_path") for e in picked):
        missing = ", ".join(e["name"] for e in picked if not e.get("ue_path"))
        raise UsageError(f"ue_query --assets: bez odvozené ue_path: {missing} (ue_root, ue_dirs v asset_sources.yaml)")
    tags = []
    for g in (idx.get("library_globals") or {}).values():
        if g.get("ue_tag"):
            tags.append(str(g["ue_tag"]))
    tags += [str(e["version_tag"]) for e in picked if e.get("version_tag")]
    return {"hestia_ue": FORMAT, "kind": "assets", "id": REQUEST_ID, "path": PATH_STAGE1,
            "assets": [{"name": e["name"], "ue_path": e["ue_path"]} for e in picked],
            "tags": sorted(dict.fromkeys(tags))}


def build_report(vault, raw: dict, old: dict | None) -> tuple[dict, list[str]]:
    """Report assetů z výsledku `hestia_ue.collect_assets`; assety mimo výsledek zůstanou ze starého reportu."""
    from . import asset_index as ai
    if not isinstance(raw.get("assets"), dict):
        raise UsageError("ue_query --import: výsledek assetů nemá assets")
    idx = ai.load_json(vault) or {}
    lib = {e["name"]: e for e in idx.get("library") or []}
    globals_ = idx.get("library_globals") or {}
    warnings = []
    assets = dict((old or {}).get("assets") or {})
    for name, rec in sorted(raw["assets"].items()):
        entry = lib.get(name)
        if entry is None:
            warnings.append(f"asset {name} není v sekci library asset_index.json; stav jen podle existence")
        st, why = state(rec, entry, globals_)
        assets[name] = {"ue_path": rec.get("ue_path"), "exists": bool(rec.get("exists")),
                        "tags": rec.get("tags") or {}, "code_version": (entry or {}).get("version"),
                        "version_tag": (entry or {}).get("version_tag"), "state": st, "why": why,
                        "read": raw.get("generated")}
    rep = {"generated": raw.get("generated"), "unreal_version": raw.get("unreal_version"),
           "path": raw.get("path"), "globals": globals_, "assets": dict(sorted(assets.items()))}
    return rep, warnings


# ---------------------------------------------------------------- karta, souhrn, G15

def _current(vault) -> tuple[dict, dict]:
    from . import asset_index as ai
    idx = ai.load_json(vault) or {}
    return {e["name"]: e for e in idx.get("library") or []}, idx.get("library_globals") or {}


def card_states(card, rep: dict | None, lib: dict, globals_: dict) -> list[tuple[str, dict, str, list[str]]]:
    """(jméno, záznam reportu, stav, důvody) pro jméno karty a `variants`; stav proti současnému kódu."""
    if rep is None:
        return []
    out = []
    for n in [card.name, *card.variants]:
        rec = rep["assets"].get(n)
        if rec is not None:
            st, why = state(rec, lib.get(n), globals_ or rep.get("globals") or {})
            out.append((n, rec, st, why))
    return out


def card_block(vault, card, rep: dict | None, lib: dict, globals_: dict, day: _dt.date) -> str | None:
    """Obsah bloku *Stav v UE* v kartě (13 kap. 10.19); None = asset v reportu není (ruční text zůstává)."""
    rows = card_states(card, rep, lib, globals_)
    if not rows:
        return None
    head = f"Čtení z UE: `{REPORT_REL}` · {rep.get('path') or '–'} (datum čtení u každého assetu)"
    lines = [UE_MARK, head, ""]
    gl = globals_ or rep.get("globals") or {}
    for name, rec, st, why in rows:
        d = read_date(rec, rep)
        when = f"čteno {d.isoformat() if d else '–'}"
        if is_old(vault, d, day):
            when += f" · **staré čtení** (víc než {report_days(vault)} dní)"
        if st == "missing":
            lines.append(f"- `{name}` ({when}): v UE chybí (`{rec.get('ue_path')}`) · **missing**")
            continue
        tags = rec.get("tags") or {}
        parts = [f"v UE ano (`{rec.get('ue_path')}`)"]
        entry = lib.get(name) or {}
        vt = entry.get("version_tag") or rec.get("version_tag")
        if vt:
            cv = entry.get("version", rec.get("code_version"))
            parts.append(f"`{vt}` {tags.get(vt) if tags.get(vt) is not None else 'bez tagu'} (kód {cv})")
        for var, g in sorted(gl.items()):
            if g.get("ue_tag"):
                tv = tags.get(g["ue_tag"])
                parts.append(f"`{g['ue_tag']}` {tv if tv is not None else 'bez tagu'} (`{var}` {g.get('value')})")
        parts.append("**outdated**, čeká na import" if st == "outdated" else "current")
        lines.append(f"- `{name}` ({when}): " + " · ".join(parts))
    return "\n".join(lines)


def has_block(text: str) -> bool:
    from .blocks import block_content
    content = block_content(text, UE_HEADING)
    return bool(content and content.strip())


def outdated_names(vault, rep: dict | None = None) -> set[str] | None:
    """Jména assetů `outdated` proti současnému kódu; None = report assetů neexistuje."""
    rep = rep if rep is not None else load_report(vault)
    if rep is None:
        return None
    lib, globals_ = _current(vault)
    return {n for n, rec in rep["assets"].items()
            if state(rec, lib.get(n), globals_ or rep.get("globals") or {})[0] == "outdated"}


def g15(vault, cards: list, day: _dt.date) -> list[tuple[str, str, str, str]]:
    """G15 z Unrealu (13 kap. 10.19): imported/verified a v reportu missing (upozornění), outdated (informace),
    assety čtené před víc než `ue_report_days` dny podle `read` (informace, jeden řádek s počtem; zadání 0.26.1)."""
    rep = load_report(vault)
    if rep is None:
        return []
    lib, globals_ = _current(vault)
    out = []
    old = sorted(n for n, rec in rep["assets"].items() if is_old(vault, read_date(rec, rep), day))
    if old:                                     # stáří po assetech podle `read`, jeden řádek (zadání 0.26.1)
        out.append(("info", "ue_assets", vault.project_rel(vault.root / REPORT_REL),
                    f"{len(old)} assetů čteno z UE před víc než {report_days(vault)} dny: {', '.join(old)}; "
                    "`ue_query --assets --emit`"))
    for c in cards:
        note = vault.notes.get(c.rel)
        if note is None:
            continue
        f = vault.project_rel(note.path)
        for name, _rec, st, why in card_states(c, rep, lib, globals_):
            if st == "missing" and c.status in ("imported", "verified"):
                out.append(("warning", c.name, f, f"karta {c.status}, ale {name} v posledním čtení UE chybí"))
            elif st == "outdated":
                out.append(("info", c.name, f, f"{name}: verze v UE starší než v kódu ({'; '.join(why)}); "
                                               "čeká na import"))
    return out
