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
meshem, materiály, tagy, složkou a bounds.
- `placeholder_ignore` (zadání 0.22, CR-024): požadavek nese `placeholder_ignore` (seznam cest meshů pro všechny
  entity) a `placeholder_ignore_items` ({entita: [cesty]}); takové meshe se do zástupných nepočítají a actor,
  který by jinak zástupný byl, se započte do `placeholder_ignored`.
- ISM (zadání 0.22, CR-025 bod 1): actor, který by jinak patřil mezi ostatní a má `InstancedStaticMeshComponent`
  (i hierarchickou), je druh `ism`; `ism_instances` = součet instancí; meshe instancí jdou do signálu zástupných
  meshů. Úroveň realizace se neodhaduje (posoudí agent nebo GameDesigner).
- Rozsah z geometrie (zadání 0.22.1, CR-025 bod 2, ověřeno T-0020): `bounds` actoru = sjednocení rozsahů komponent
  s geometrií (statické meshe přes `SystemLibrary.get_component_bounds`, každá instance ISM v jejím světovém
  umístění: rozsah meshe transformovaný `get_instance_transform(i, True)`); kořen a komponenty bez meshe se
  nezapočítají. Actor bez geometrie (BSP, světla) nebo s nečitelnou geometrií má rozsah z `get_actor_bounds`
  (`bounds_from: actor`). `pivot_offset` = vzdálenost kořene (`get_actor_location`) od středu rozsahu v cm;
  souhrn `pivot_far` = počet actorů s `pivot_offset` nad `pivot_far_cm` z požadavku (výchozí 500).
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
KINDS = ("static_mesh", "ism", "blueprint", "bsp", "other")
PIVOT_FAR_CM = 500


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


def _mesh_and_materials(comp, meshes: list, materials: list) -> None:
    mesh = getattr(comp, "static_mesh", None)
    if mesh is not None:
        path = _s(mesh.get_path_name())
        if path not in meshes:
            meshes.append(path)
    materials += [_s(m.get_path_name()) for m in (comp.get_materials() or []) if m is not None]


def _vec(v) -> list:
    return [float(v.x), float(v.y), float(v.z)]


def _union(box, lo: list, hi: list):
    if box is None:
        return [list(lo), list(hi)]
    return [[min(box[0][i], lo[i]) for i in range(3)], [max(box[1][i], hi[i]) for i in range(3)]]


def _component_box(comp):
    """(min, max) světového rozsahu statické mesh komponenty."""
    res = unreal.SystemLibrary.get_component_bounds(comp)
    o, e = _vec(res[0]), _vec(res[1])
    return [o[i] - e[i] for i in range(3)], [o[i] + e[i] for i in range(3)]


def _transform(res):
    """Výsledek get_instance_transform: Transform, (bool, Transform) nebo None."""
    if isinstance(res, tuple):
        ok = [x for x in res if not isinstance(x, bool)]
        if any(x is False for x in res) or not ok:
            return None
        return ok[-1]
    return res


def _instances_box(comp, count: int):
    """Sjednocení rozsahů instancí ISM ve světových souřadnicích (rohy rozsahu meshe přes transformaci instance)."""
    b = comp.static_mesh.get_bounds()
    o, e = _vec(b.origin), _vec(b.box_extent)
    corners = [unreal.Vector(o[0] + sx * e[0], o[1] + sy * e[1], o[2] + sz * e[2])
               for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    box = None
    for i in range(count):
        t = _transform(comp.get_instance_transform(i, True))
        if t is None:
            continue
        pts = [_vec(t.transform_location(c)) for c in corners]
        box = _union(box, [min(q[k] for q in pts) for k in range(3)], [max(q[k] for q in pts) for k in range(3)])
    return box


def geometry_bounds(static: list, ism: list, counts: list):
    """Rozsah z komponent s geometrií [min, max], nebo None (bez geometrie nebo nečitelná)."""
    box = None
    try:
        for comp in static:
            if getattr(comp, "static_mesh", None) is not None:
                box = _union(box, *_component_box(comp))
        for comp, n in zip(ism, counts):
            if getattr(comp, "static_mesh", None) is None or not n:
                continue
            ib = _instances_box(comp, n)
            if ib is not None:
                box = _union(box, *ib)
    except Exception:                   # noqa: BLE001 – API editoru jinak; rozsah z actoru
        return None
    return box


def actor_record(actor) -> dict:
    cls = _s(actor.get_class().get_name())
    meshes, materials = [], []
    ism_cls = getattr(unreal, "InstancedStaticMeshComponent", None)       # HISM je podtřída
    ism = list(actor.get_components_by_class(ism_cls) or []) if ism_cls is not None else []
    static = [c for c in actor.get_components_by_class(unreal.StaticMeshComponent) or []
              if not any(c is i for i in ism)]
    for comp in static:
        _mesh_and_materials(comp, meshes, materials)
    instances, counts = 0, []
    for comp in ism:                                     # meshe instancí do signálu zástupných meshů
        _mesh_and_materials(comp, meshes, materials)
        try:
            n = int(comp.get_instance_count())
        except Exception:               # noqa: BLE001 – počet instancí jen pro informaci
            n = 0
        counts.append(n)
        instances += n
    kind = actor_kind(cls)
    if kind == "other" and ism:
        kind = "ism"
    box = geometry_bounds(static, ism, counts)
    if box is not None:
        origin = [(box[0][i] + box[1][i]) / 2 for i in range(3)]
        extent = [(box[1][i] - box[0][i]) / 2 for i in range(3)]
        source = "geometry"
    else:
        o, e = actor.get_actor_bounds(False)
        origin, extent, source = _vec(o), _vec(e), "actor"
    rec = {"name": _s(actor.get_actor_label()), "class": cls, "kind": kind,
           "mesh": meshes[0] if meshes else None, "meshes": meshes, "materials": sorted(set(materials)),
           "tags": [_s(t) for t in (actor.tags or [])], "folder": _s(actor.get_folder_path()),
           "bounds": {"origin": origin, "extent": extent}, "bounds_from": source}
    try:
        root = _vec(actor.get_actor_location())
        rec["pivot_offset"] = round(sum((root[i] - origin[i]) ** 2 for i in range(3)) ** 0.5, 1)
    except Exception:                   # noqa: BLE001 – poloha kořene jen pro signál
        pass
    if ism:
        rec["ism_instances"] = instances
    return rec


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


def _ignored(mesh: str, ignore) -> bool:
    """Mesh ze seznamu placeholder_ignore (shoda celé cesty, i bez přípony objektu `.Jmeno`)."""
    base = mesh.split(".", 1)[0]
    return any(mesh == i or base == i.split(".", 1)[0] for i in ignore)


def stats(records: list, stage_prefix: str, ignore=(), pivot_far_cm: float = PIVOT_FAR_CM) -> dict:
    by_kind = {k: 0 for k in KINDS}
    stages: dict = {}
    lo, hi = None, None
    placeholder = default_mat = ignored = instances = pivot_far = 0
    for r in records:
        if float(r.get("pivot_offset") or 0) > pivot_far_cm:
            pivot_far += 1
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
        instances += int(r.get("ism_instances") or 0)
        ph = [m for m in r["meshes"] if m.startswith(PLACEHOLDER_MESH)]
        if any(not _ignored(m, ignore) for m in ph):
            placeholder += 1
        elif ph:
            ignored += 1
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
    return {"actors": len(records), "by_kind": by_kind, "ism_instances": instances,
            "placeholder_meshes": placeholder, "placeholder_ignored": ignored, "default_materials": default_mat,
            "pivot_far": pivot_far, "pivot_far_cm": pivot_far_cm, "stages": dict(sorted(stages.items())),
            "bounds": {"min": lo, "max": hi} if lo is not None else None}


# ---------------------------------------------------------------- běh

def collect(request: dict) -> dict:
    rules = request.get("rules") or {}
    targets = request.get("targets") or sorted(rules)
    limit = int(request.get("limit") or 500)
    prefix = request.get("stage_tag_prefix") or ""
    ignore_all = list(request.get("placeholder_ignore") or [])
    ignore_items = request.get("placeholder_ignore_items") or {}
    pivot_far_cm = float(request.get("pivot_far_cm") or PIVOT_FAR_CM)
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
                       "stats": stats(recs, prefix, ignore_all + list(ignore_items.get(e) or []), pivot_far_cm),
                       "actors": recs[:limit]}
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
