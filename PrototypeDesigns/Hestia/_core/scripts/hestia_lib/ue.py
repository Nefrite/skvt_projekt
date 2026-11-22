"""Příkaz ue_query: čtení stavu v Unrealu, etapa 1 (zadání 13 kap. 10.11, 12 kap. 3b.8; zadání 0.14, 0.14.2).

**Jen čtení.** Core nedodává žádný dotaz, který zapisuje do levelu nebo assetů.

- `ue_query --emit --entity X` / `--all`: z `taxonomy_local/ue_map.yaml` vygeneruje čtecí skript do
  `Maintenance/ue/ue_query_<id>.py` (pracovní složka, přepisuje se). GameDesigner ho spustí v editoru
  (*Execute Python Script*); skript přes `_core/scripts/hestia_ue.py` zapíše surový výsledek
  `Maintenance/ue/ue_result_<id>.json`. U `--entity` se čtou i potomci s pravidlem (součet za potomky).
  Skript je přenosný (zadání 0.15.4): cesty k `_core/scripts` a k výsledku odvozuje z `__file__`, absolutní cestu
  stroje, kde běží core, neobsahuje; výpis pro editor uvádí cestu relativně ke kořeni projektu.
- `ue_query --import [soubor]`: ověří výsledek, doplní souhrn (vlastní actory, za potomky) a uloží report na entitu
  `Maintenance/reports/ue_<entita>.json`. Novější report starším nepřepíše.
Pravidla: jmenovité položky (`items`) mají přednost před `defaults` podle `kind` (`{entity}` = ID entity); actor
patří entitě s nejdelší shodou vzoru (počítá `hestia_ue.py`, proto dostane pravidla všech entit).
Záloha bez editoru (`UnrealEditor-Cmd … -run=pythonscript -script=<skript>`) jen v README; core ji nespouští.
Úroveň realizace se automaticky neodhaduje; hub a audit ukazují jen měřitelné signály a G10.
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

from .changeset import ChangeSet
from .errors import EXIT_OK, UsageError
from .fileio import read_text, to_posix
from .model import Model
from .util import today
from .vault import Vault

UE_DIR = "Maintenance/ue"
REPORTS = "Maintenance/reports"
LIMIT = 500
FORMAT = 1
PATH_STAGE1 = "etapa 1 (skript v editoru)"


# ---------------------------------------------------------------- pravidla a reporty

def rules(vault: Vault, m: Model) -> dict[str, list[dict]]:
    """Pravidla po entitách: jmenovité položky, jinak defaults podle kind. Bez ue_map.yaml prázdné."""
    um = vault.taxonomy.ue_map
    if um is None:
        return {}
    out: dict[str, list[dict]] = {}
    for it in um["items"]:
        if it["entity"] in m.entities:
            out.setdefault(it["entity"], []).append({k: list(v) for k, v in it.items() if k != "entity"})
    for name, n in sorted(m.entities.items()):
        rule = um["defaults"].get(n.fm.get("kind"))
        if name not in out and rule:
            out[name] = [{k: [x.replace("{entity}", name) for x in v] for k, v in rule.items()}]
    return dict(sorted(out.items()))


def report_rel(entity: str) -> str:
    return f"{REPORTS}/ue_{entity}.json"


def load_report(vault: Vault, entity: str) -> dict | None:
    p = vault.root / report_rel(entity)
    try:
        return json.loads(read_text(p)) if p.is_file() else None
    except ValueError:
        return None


def report_date(rep: dict) -> _dt.date | None:
    try:
        return _dt.date.fromisoformat(str(rep.get("generated") or "")[:10])
    except ValueError:
        return None


def is_stale(vault: Vault, rep: dict, day: _dt.date | None = None) -> bool:
    d = report_date(rep)
    limit = int(vault.config.get("ue_report_days") or 14)
    return d is None or ((day or today()) - d).days > limit


def total_actors(rep: dict) -> int:
    s = rep.get("summary") or {}
    return int((s.get("own") or {}).get("actors") or 0) + int((s.get("descendants") or {}).get("actors") or 0)


def state_behind(m: Model, entity: str, rep: dict) -> tuple | None:
    """`state` za reportem (G10, zadání 0.19): entita má v reportu aspoň jednoho actora a nejnovější platný `state`
    má `updated` starší než `generated` reportu → (state, datum state, datum reportu). Porovnávají se jen data (po
    dnech), text `state` se nečte; entita bez platného `state` → None (řeší G4)."""
    rdate = report_date(rep)
    if rdate is None or total_actors(rep) == 0:
        return None
    states = []
    for n in m.notes:
        if n.type == "state" and (n.fm or {}).get("validity") == "valid" and entity in m.entities_of(n):
            try:
                d = _dt.date.fromisoformat(str(n.fm.get("updated") or "")[:10])
            except ValueError:
                d = None
            states.append((d or _dt.date.min, n))
    if not states:
        return None
    sdate, note = max(states, key=lambda x: (x[0], x[1].rel))
    return (note, sdate, rdate) if sdate < rdate else None


def state_behind_text(behind: tuple) -> str:
    note, sdate, rdate = behind
    s = sdate.isoformat() if sdate != _dt.date.min else "bez data"
    return f"`state` {note.name} ({s}) je starší než čtení z UE ({rdate.isoformat()}); ověř § *V levelu*"


def hub_block(vault: Vault, m: Model, entity: str, rule_map: dict, day: _dt.date | None = None) -> str:
    """Obsah generovaného bloku v `## Stav v UE`; bez pravidla nebo reportu prázdný (13 kap. 10.3, 10.11)."""
    rep = load_report(vault, entity) if entity in rule_map else None
    if rep is None:
        return ""
    s = rep.get("summary") or {}
    own, desc = s.get("own") or {}, s.get("descendants") or {}
    d = report_date(rep)
    head = (f"Poslední čtení: {d.isoformat() if d else '–'} · `{report_rel(entity)}` · {rep.get('path') or '–'}"
            f" · mapa `{rep.get('map') or '–'}`")
    if is_stale(vault, rep, day):
        head += f" · **starý** (víc než {int(vault.config.get('ue_report_days') or 14)} dní)"
    lines = [head, ""]
    actors = f"- Actory: {own.get('actors', 0)} vlastních"
    if desc.get("entities"):
        actors += f", {desc.get('actors', 0)} za potomky ({', '.join(sorted(desc['entities']))})"
    if rep.get("truncated"):
        actors += "; výpis v reportu zkrácen"
    lines.append(actors)
    bk = own.get("by_kind") or {}
    lines.append(f"- Třídy: StaticMesh {bk.get('static_mesh', 0)}, Blueprint {bk.get('blueprint', 0)}, "
                 f"BSP {bk.get('bsp', 0)}, ostatní {bk.get('other', 0)}")
    lines.append(f"- Zástupné meshe (`/Engine/BasicShapes/`): {own.get('placeholder_meshes', 0)}; "
                 f"výchozí materiály: {own.get('default_materials', 0)}")
    stages = own.get("stages") or {}
    lines.append("- Fáze: " + (", ".join(f"{k} {v}" for k, v in stages.items()) if stages else "–"))
    b = own.get("bounds")
    if b and b.get("min") and b.get("max"):
        size = [b["max"][i] - b["min"][i] for i in range(3)]
        lines.append(f"- Rozsah: {size[0]:.0f} × {size[1]:.0f} × {size[2]:.0f} cm")
    fm = m.entities[entity].fm
    depths = [f"{dom} {fm.get(f'depth_{dom}')}" for dom in vault.taxonomy.domains
              if fm.get(f"depth_{dom}") not in (None, "") and m.mode(entity, dom) == "build"]
    lines.append("- Pro srovnání `depth_*`: " + (", ".join(depths) if depths else "–")
                 + "; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)")
    behind = state_behind(m, entity, rep)
    if behind:                                          # G10, zadání 0.19: jen data, text state se nečte
        lines.append(f"- Pozor: {state_behind_text(behind)}; report potvrzuje jen „v levelu je“, vzhled a funkci "
                     "§ *Vizuálně ověřeno*")
    return "\n".join(lines)


# ---------------------------------------------------------------- emit a import

def request(vault: Vault, m: Model, entity: str | None, all_: bool) -> dict:
    um = vault.taxonomy.ue_map
    if um is None:
        raise UsageError("ue_query: Maintenance/taxonomy_local/ue_map.yaml chybí; Unreal se nečte (13 kap. 10.11)")
    rmap = rules(vault, m)
    if all_ == bool(entity):
        raise UsageError("ue_query: zadej právě jedno z --entity, --all")
    if entity:
        if entity not in m.entities:
            raise UsageError(f"ue_query: entita {entity} neexistuje")
        if entity not in rmap:
            raise UsageError(f"ue_query: entita {entity} nemá pravidlo v ue_map.yaml (items ani defaults podle kind)")
        targets = [entity] + [e for e in m.subtree(entity)[1:] if e in rmap]
    else:
        if not rmap:
            raise UsageError("ue_query: ue_map.yaml nemá žádné pravidlo pro existující entitu")
        targets = list(rmap)
    return {"hestia_ue": FORMAT, "id": entity or "all", "map": um["map"], "stage_tag_prefix": um["stage_tag_prefix"],
            "limit": LIMIT, "path": PATH_STAGE1, "targets": targets, "rules": rmap}


def script_text(req: dict, result_name: str) -> str:
    """Přenosný skript (zadání 0.15.4, CR_2026-11-21_ue_query_cesty_ve_skriptu): žádná absolutní cesta stroje, kde
    běží core; `_core/scripts` a výsledek odvodí ze svého umístění `<Hestia>/Maintenance/ue/` (`__file__`)."""
    return "\n".join([
        "# hestia:ue_query – vygenerovaný čtecí skript, needitovat (zadání 13, kap. 10.11). Jen čtení.",
        f"# Entita: {req['id']}. Spusť v editoru Unreal: Tools → Execute Python Script. Výsledek načti:",
        f"#   python <Hestia>/_core/scripts/hestia.py ue_query --import --"
        + ("all" if req["id"] == "all" else f"entity {req['id']}") + " --apply",
        "# Cesty se odvozují z umístění skriptu (<Hestia>/Maintenance/ue/); skript je přenosný mezi stroji.",
        "import json",
        "import sys",
        "from pathlib import Path",
        "",
        "try:",
        "    HERE = Path(__file__).resolve().parent",
        "except NameError:",
        "    raise SystemExit('hestia:ue_query: skript spusť jako soubor (Execute Python Script), chybí __file__')",
        "VAULT = HERE.parents[1]",
        "sys.path.insert(0, str(VAULT / '_core' / 'scripts'))",
        "import hestia_ue  # noqa: E402",
        "",
        f"REQUEST = json.loads({json.dumps(req, ensure_ascii=False)!r})",
        f"hestia_ue.run(REQUEST, str(HERE / {result_name!r}))",
        "",
    ])


def editor_path(vault: Vault, path: Path) -> str:
    """Cesta pro pokyn do editoru relativně ke kořeni projektu (bez absolutní cesty stroje, kde běží core)."""
    for base in (vault.project_root, vault.root.parent):
        try:
            return to_posix(path.resolve().relative_to(base.resolve()))
        except ValueError:
            continue
    return f"{vault.root.name}/{to_posix(path.relative_to(vault.root))}"


def build_reports(vault: Vault, m: Model, raw: dict) -> tuple[dict[str, dict], list[str]]:
    """Reporty na entitu z výsledku hestia_ue (souhrn: vlastní actory a za potomky)."""
    if not isinstance(raw, dict) or raw.get("hestia_ue") != FORMAT or not isinstance(raw.get("entities"), dict):
        raise UsageError("ue_query --import: soubor není výsledek hestia_ue (hestia_ue: 1, entities)")
    warnings = []
    if raw.get("map_mismatch"):
        warnings.append(f"otevřená mapa {raw.get('map')} není mapa z ue_map.yaml ({raw.get('expected_map')})")
    ents = raw["entities"]
    out = {}
    for e, data in sorted(ents.items()):
        if e not in m.entities:
            warnings.append(f"entita {e} ve výsledku neexistuje; report nevzniká")
            continue
        desc = {d: int((ents[d].get("stats") or {}).get("actors") or 0) for d in m.subtree(e)[1:] if d in ents}
        out[e] = {"generated": raw.get("generated"), "unreal_version": raw.get("unreal_version"),
                  "map": raw.get("map"), "path": raw.get("path"), "query": data.get("rule") or [],
                  "truncated": bool(data.get("truncated")),
                  "summary": {"own": data.get("stats") or {}, "descendants": {"actors": sum(desc.values()),
                                                                             "entities": desc}},
                  "actors": data.get("actors") or []}
    return out, warnings


def _result_file(vault: Vault, arg: str, entity: str | None, all_: bool) -> Path:
    if arg:
        p = Path(arg)
        return p if p.is_absolute() else (Path.cwd() / p)
    d = vault.root / UE_DIR
    if entity or all_:
        return d / f"ue_result_{entity or 'all'}.json"
    cands = sorted(d.glob("ue_result_*.json"), key=lambda p: p.stat().st_mtime) if d.is_dir() else []
    if not cands:
        raise UsageError(f"ue_query --import: v {UE_DIR}/ není žádný výsledek; nejdřív --emit a spuštění v editoru")
    return cands[-1]


def run(args, vault: Vault) -> tuple[int, dict, str]:
    m = Model(vault)
    cs = ChangeSet(vault.project_root)
    if bool(args.emit) == (args.import_file is not None):
        raise UsageError("ue_query: zadej právě jedno z --emit, --import")
    if args.emit:
        req = request(vault, m, args.entity, args.all)
        script = vault.root / UE_DIR / f"ue_query_{req['id']}.py"
        result = vault.root / UE_DIR / f"ue_result_{req['id']}.json"
        cs.write(script, script_text(req, result.name))
        if args.apply and not cs.empty:
            cs.apply()
        warnings = []
        if not (vault.root / "_core" / "scripts" / "hestia_ue.py").is_file():
            warnings.append("ve vaultu chybí _core/scripts/hestia_ue.py; skript v editoru ho nenajde (aktualizuj core)")
        rel = editor_path(vault, script)
        verb = "zapsán" if args.apply else "zapsal by se (dry-run, zapiš s --apply)"
        lines = [f"ue_query --emit {req['id']}: čtecí skript {verb} → {UE_DIR}/{script.name} "
                 f"({len(req['targets'])} entit: {', '.join(req['targets'])})",
                 f"V editoru Unreal: Tools → Execute Python Script → {rel} (relativně ke kořeni projektu; "
                 "v dialogu ho vyber ve složce projektu)",
                 f"Pak: hestia.py ue_query --import --{'all' if req['id'] == 'all' else 'entity ' + req['id']} --apply"]
        lines += [f"upozornění: {w}" for w in warnings]
        payload = {"command": "ue_query", "mode": "emit", "applied": bool(args.apply), "id": req["id"],
                   "script": f"{UE_DIR}/{script.name}", "result": f"{UE_DIR}/{result.name}", "editor_path": rel,
                   "targets": req["targets"], "warnings": warnings}
        return EXIT_OK, payload, "\n".join(lines)

    src = _result_file(vault, args.import_file, args.entity, args.all)
    if not src.is_file():
        raise UsageError(f"ue_query --import: výsledek neexistuje: {src}")
    try:
        raw = json.loads(read_text(src))
    except ValueError:
        raise UsageError(f"ue_query --import: výsledek není platný JSON: {src}")
    reports, warnings = build_reports(vault, m, raw)
    written, skipped = [], []
    for e, rep in reports.items():
        old = load_report(vault, e)
        if old and str(old.get("generated") or "") > str(rep.get("generated") or ""):
            skipped.append(e)
            warnings.append(f"{report_rel(e)}: existující report je novější ({old.get('generated')}); nepřepisuji")
            continue
        text = json.dumps(rep, ensure_ascii=False, indent=1) + "\n"
        if cs.write(vault.root / report_rel(e), text):
            written.append(e)
    if args.apply and not cs.empty:
        cs.apply()
    verb = "zapsáno" if args.apply else "zapsalo by se (dry-run, zapiš s --apply)"
    lines = [f"ue_query --import {to_posix(src.name)}: reporty {verb}: " + (", ".join(report_rel(e) for e in written)
                                                                            or "beze změny")]
    lines += [f"- {e}: {reports[e]['summary']['own'].get('actors', 0)} vlastních actorů, "
              f"{reports[e]['summary']['descendants']['actors']} za potomky" for e in reports]
    lines += [f"Upozornění: {w}" for w in warnings]
    lines.append("Blok ## Stav v UE v hubech obnoví hestia.py hubs --apply.")
    payload = {"command": "ue_query", "mode": "import", "applied": bool(args.apply and written), "written": written,
               "skipped": skipped, "warnings": warnings, "source": to_posix(src)}
    return EXIT_OK, payload, "\n".join(lines)
