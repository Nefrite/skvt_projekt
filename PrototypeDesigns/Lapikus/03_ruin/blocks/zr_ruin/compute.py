"""03 vypocet cele zriceniny: vsechny zdi a podlahy -> kameny"""
from .decay import params
from .floor import build_floor_stones
from .prep import apply_volumes
from .rubble import make_rubble
from .wall import build_wall_stones
from zrlib.geom import Terrain
from zrlib.stones import assign_meshes, in_box


def compute_blocks(layout, removed=(), moved=None, volumes=None, rubble=False, detached=(), only_walls=None, age=None, override=None):
    """detached = id kamenu oddelenych od zdi (detach_stones.py): vzdy samostatne actory, i mimo Ruin_Explode
    only_walls = jen tyto zdi (ladeni), age / override = stari a prepis parametru (viz decay.params)"""
    ONLY_WALLS = only_walls
    P = params(layout, age, override); terr = Terrain(layout["terrain"])
    vols = list(layout.get("volumes", [])) + list(volumes or [])
    layout, explode = apply_volumes(layout, vols, terr)
    removed = set(removed); moved = moved or {}; detached = set(detached or ())
    edits = list(layout.get("edits", []))
    allpts = [p for w in layout["walls"] for p in w["points"]]
    centroid = (sum(p[0] for p in allpts) / len(allpts), sum(p[1] for p in allpts) / len(allpts))
    out = {}
    for wd in layout["walls"]:
        if ONLY_WALLS and wd["name"] not in ONLY_WALLS: continue
        stones, states, L = build_wall_stones(wd, P, terr, layout, edits, removed | detached, centroid)   # oddeleny lic = odkryte jadro
        out[wd["name"]] = dict(folder=wd["folder"], stones=stones)
    for fs in layout.get("floors", []):
        if ONLY_WALLS and fs["name"] not in ONLY_WALLS and not any(w in ONLY_WALLS for w in fs.get("walls", [])): continue
        out[fs["name"]] = dict(folder=fs.get("folder", "Ruin"), stones=build_floor_stones(fs, P, out, terr))
    # sut na zemi: od 11/2026 ve 05_constructions (build_constructions.py); rubble=True ji prida i sem (stary zpusob)
    if rubble:
        for name, r in make_rubble(out, P, terr, removed).items():
            out[name]["rubble"] = r["stones"]
    for w in out.values():
        assign_meshes(w["stones"] + w.get("rubble", []))
    for name, w in out.items():
        w["stones"] = [st for st in w["stones"] if st.id not in removed and st.id.split(".r")[0] not in removed]
        # rucne posunute bloky a rozlozeni na samostatne kameny
        # samostatne kameny = jen ty v boxu Ruin_Explode (podle puvodni i posunute polohy);
        # posunute kameny mimo box se vrati do Instanced Static Mesh na nove misto ("slouceni")
        loose_ids = set()
        for st in w["stones"] + w.get("rubble", []):
            if any(in_box(st, b) for b in explode) or st.id in detached: loose_ids.add(st.id)
            m = moved.get(st.id)
            if m:
                st.x, st.y, st.z, st.roll, st.pitch, st.yaw = m
                if any(in_box(st, b) for b in explode): loose_ids.add(st.id)
        loose_ids.update(st.id for st in w.get("rubble", []))      # kameny na zemi vzdy samostatne
        w["loose"] = [st for st in w["stones"] + w.get("rubble", []) if st.id in loose_ids]
        lid = set(id(st) for st in w["loose"])
        w["stones"] = [st for st in w["stones"] if id(st) not in lid]
        w["rubble"] = [st for st in w.get("rubble", []) if id(st) not in lid]
    return out, P
