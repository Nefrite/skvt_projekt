"""Čtecí modul Hestia pro Python v Unrealu (zadání 13 kap. 10.11, 12 kap. 3b.8; zadání 0.14, 0.14.2).

Samostatný: jen standardní knihovna a modul `unreal`, bez `hestia_lib` (běží Pythonem editoru, UE 5.8 = 3.11).
**Jen čtení:** nic nezapisuje do levelu ani assetů. Výsledek (JSON) zapíše do souboru, který určí požadavek.

Požadavek (vygeneruje `hestia.py ue_query --emit`):
    {"hestia_ue": 1, "id": ..., "map": ..., "stage_tag_prefix": "stage:", "limit": 500, "path": ...,
     "targets": [entity, ...], "rules": {entity: [{"tags": [vzor, ...], "folders": [složka, ...]}, ...]}}
- vzor tagu: `*` = libovolný konec (fnmatch); složka v Outlineru: shoda celé cesty nebo jejího začátku;
- v jedné položce víc podmínek = průnik (tag i složka), víc položek k entitě = sjednocení;
- actor patří entitě s **nejdelší shodou vzoru** (délka vzoru bez `*`), takže `stavba:Palac_Kovarna*`
  vyhraje nad `stavba:Palac*`.
Výsledek: na entitu `count`, `stats` (signály realizace přes všechny actory: třídy, zástupné meshe
`/Engine/BasicShapes/`, výchozí materiály, fáze podle tagů, bounds) a nejvýš `limit` actorů se jménem, třídou,
meshem, materiály, tagy, složkou a bounds. Úroveň realizace se neodhaduje (posoudí agent nebo GameDesigner).
Dotaz „původ“ (actory podle skriptu) v etapě 1 není.
"""
from __future__ import annotations

import datetime
import fnmatch
import json

try:                                    # v editoru; testy dodají zástupný modul
    import unreal
except ImportError:                     # pragma: no cover – mimo editor jen import pro kontrolu syntaxe
    unreal = None

FORMAT = 1
PLACEHOLDER_MESH = "/Engine/BasicShapes/"
DEFAULT_MATERIALS = ("/Engine/EngineMaterials/", "/Engine/BasicShapes/BasicShapeMaterial")
KINDS = ("static_mesh", "blueprint", "bsp", "other")


# ---------------------------------------------------------------- čtení z editoru

def _s(value) -> str:
    return str(value) if value is not None else ""


def level_actors() -> list:
    return list(unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors())


def map_path() -> str:
    try:
        world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
        return _s(world.get_path_name()).split(".", 1)[0]
    except Exception:                   # noqa: BLE001 – mapa jen pro informaci
        return ""


def engine_version() -> str:
    try:
        return _s(unreal.SystemLibrary.get_engine_version())
    except Exception:                   # noqa: BLE001
        return ""


def actor_kind(class_name: str) -> str:
    if class_name == "StaticMeshActor":
        return "static_mesh"
    if class_name.endswith("_C"):       # třída vygenerovaná z Blueprintu
        return "blueprint"
    if class_name == "Brush":           # BSP geometrie (objemy jsou jiné třídy, patří do ostatních)
        return "bsp"
    return "other"


def actor_record(actor) -> dict:
    cls = _s(actor.get_class().get_name())
    meshes, materials = [], []
    for comp in actor.get_components_by_class(unreal.StaticMeshComponent) or []:
        mesh = getattr(comp, "static_mesh", None)
        if mesh is not None:
            meshes.append(_s(mesh.get_path_name()))
        materials += [_s(m.get_path_name()) for m in (comp.get_materials() or []) if m is not None]
    origin, extent = actor.get_actor_bounds(False)
    return {"name": _s(actor.get_actor_label()), "class": cls, "kind": actor_kind(cls),
            "mesh": meshes[0] if meshes else None, "meshes": meshes, "materials": sorted(set(materials)),
            "tags": [_s(t) for t in (actor.tags or [])], "folder": _s(actor.get_folder_path()),
            "bounds": {"origin": [origin.x, origin.y, origin.z], "extent": [extent.x, extent.y, extent.z]}}


# ---------------------------------------------------------------- pravidla

def _tag_score(patterns: list, tags: list) -> int:
    best = -1
    for p in patterns:
        if any(fnmatch.fnmatchcase(t, p) for t in tags):
            best = max(best, len(p.replace("*", "")))
    return best


def _folder_score(folders: list, folder: str) -> int:
    best = -1
    for f in folders:
        f = f.strip("/")
        if folder == f or folder.startswith(f + "/") or fnmatch.fnmatchcase(folder, f):
            best = max(best, len(f))
    return best


def item_score(item: dict, rec: dict) -> int:
    """Skóre položky pravidla (délka nejdelší shody); -1 = položka neplatí (průnik podmínek)."""
    scores = []
    if item.get("tags"):
        scores.append(_tag_score(item["tags"], rec["tags"]))
    if item.get("folders"):
        scores.append(_folder_score(item["folders"], rec["folder"].strip("/")))
    if not scores or min(scores) < 0:
        return -1
    return max(scores)


def assign(rules: dict, rec: dict) -> str | None:
    """Entita s nejdelší shodou vzoru (při shodě délky abecedně první)."""
    best = None
    for entity in sorted(rules):
        score = max((item_score(it, rec) for it in rules[entity]), default=-1)
        if score >= 0 and (best is None or score > best[0]):
            best = (score, entity)
    return best[1] if best else None


def stats(records: list, stage_prefix: str) -> dict:
    by_kind = {k: 0 for k in KINDS}
    stages: dict = {}
    lo, hi = None, None
    placeholder = default_mat = 0
    for r in records:
        by_kind[r["kind"]] += 1
        if any(m.startswith(PLACEHOLDER_MESH) for m in r["meshes"]):
            placeholder += 1
        if any(m.startswith(DEFAULT_MATERIALS) for m in r["materials"]):
            default_mat += 1
        for t in r["tags"]:
            if stage_prefix and t.startswith(stage_prefix):
                name = t[len(stage_prefix):]
                stages[name] = stages.get(name, 0) + 1
        o, e = r["bounds"]["origin"], r["bounds"]["extent"]
        a = [o[i] - e[i] for i in range(3)]
        b = [o[i] + e[i] for i in range(3)]
        lo = a if lo is None else [min(lo[i], a[i]) for i in range(3)]
        hi = b if hi is None else [max(hi[i], b[i]) for i in range(3)]
    return {"actors": len(records), "by_kind": by_kind, "placeholder_meshes": placeholder,
            "default_materials": default_mat, "stages": dict(sorted(stages.items())),
            "bounds": {"min": lo, "max": hi} if lo is not None else None}


# ---------------------------------------------------------------- běh

def collect(request: dict) -> dict:
    rules = request.get("rules") or {}
    targets = request.get("targets") or sorted(rules)
    limit = int(request.get("limit") or 500)
    prefix = request.get("stage_tag_prefix") or ""
    owned: dict = {e: [] for e in targets}
    for actor in level_actors():
        rec = actor_record(actor)
        e = assign(rules, rec)
        if e in owned:
            owned[e].append(rec)
    entities = {}
    for e in targets:
        recs = sorted(owned[e], key=lambda r: r["name"])
        entities[e] = {"rule": rules.get(e, []), "count": len(recs), "truncated": len(recs) > limit,
                       "stats": stats(recs, prefix), "actors": recs[:limit]}
    loaded = map_path()
    return {"hestia_ue": FORMAT, "id": request.get("id"), "path": request.get("path") or "editor",
            "generated": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "unreal_version": engine_version(), "map": loaded, "expected_map": request.get("map") or "",
            "map_mismatch": bool(request.get("map")) and loaded != request.get("map"),
            "entities": entities}


def run(request: dict, out_path: str) -> dict:
    """Přečte stav podle požadavku a zapíše výsledek JSON do `out_path` (jen čtení v editoru)."""
    result = collect(request)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
        f.write("\n")
    total = sum(v["count"] for v in result["entities"].values())
    msg = f"hestia_ue: {len(result['entities'])} entit, {total} actorů → {out_path}"
    if result["map_mismatch"]:
        msg += f" (pozor: otevřená mapa {result['map']} není {result['expected_map']})"
    try:
        unreal.log(msg)
    except Exception:                   # noqa: BLE001 – výpis je jen informace, výsledek už je zapsaný
        try:
            print(msg)
        except UnicodeEncodeError:
            print(msg.encode("ascii", "replace").decode("ascii"))
    return result
