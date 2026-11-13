"""
build_ruin_blocks.py - zricenina z jednotlivych kamennych bloku (Unreal Editor 5.8)

Zed = vodorovne rady kamene. Kazda rada ma dva lice z lomovych kvadru (ruzne delky, prevazba)
a mezi nimi jadro z lomu a malty. Model rozpadu (stejny jako build_ruin.py) urci dochovanou vysku;
bloky nad ni zmizi, u paty se rozebira lic (odkryje se jadro), otvory se vyriznou, intaktni osteni
a oblouky se postavi z opracovanych kvadru.

Uprava zriceniny:
  - v levelu objemy (TriggerBox s tagem) -> pregenerovat:
        Ruin_Cut, Ruin_Opening:<okno|dvere|portal|brana|strilna|prulom> (+Ruin_Intact, Ruin_Protect),
        Ruin_Keep, Ruin_Explode (bloky jako samostatne actory k rucnimu posunu / mazani)
  - v datech (ruin_layout.json -> "edits"): cut / cut_box / set_height / restore  -> pregenerovat
  - rucne: v levelu smazat jednotlive bloky (instance), pak spustit capture_manual_edits()
           -> smazane bloky se zapisi do manual_edits.json a pri pregenerovani zustanou smazane

Pouziti v UE: Tools -> Execute Python Script -> build_ruin_blocks.py      (cely hrad)
                                            -> casti/<Cast>.py           (jen jedna cast: Obvod, Palac, Ostroh)
  (ruin_layout.json a manual_edits.json vedle skriptu, nebo nastav LAYOUT_PATH)
  Cast smaze a postavi jen sve actory (tag cast:<Cast>), ostatni casti zustanou. Pocita se vzdy cely hrad
  (navaznosti mezi zdmi, teren), stavi se jen vybrana cast.
Mimo UE: python build_ruin_blocks.py [ruin_layout.json]  -> statistika (pocet bloku)

Kod je rozdeleny (od 11/2026):
  build_ruin_blocks.py   tento soubor: nastaveni behu, soubory (layout, manual_edits), build a capture v Unrealu
  zr_ruin/               vnitrni moduly zriceniny: decay (rozpad, otvory), prep (priprava zdi), wall (zed z bloku),
                         post (koruna pod strechou, zlabky, jadro), floor (dlazba), rubble (sut), compute (cely hrad)
  ../../zrlib/           sdilena knihovna 03 + 05 + tools: config (MATERIALY, MESHE, DREVO, FYZIKA - nastaveni vzhledu),
                         geom, stones, ue_assets, ue_actors, level
"""
import json, math, os, random, sys, zlib


def _boot():
    """najde sdilenou knihovnu zrlib (koren repozitare) a vnitrni moduly zr_ruin. Moduly se pri kazdem spusteni
    nactou znovu (Python v Unrealu si je jinak drzi v pameti a po uprave souboru by bezel stary kod)."""
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.normpath(os.path.join(here, "..", ".."))
    if not os.path.isdir(os.path.join(root, "zrlib")):
        raise RuntimeError("Chybi slozka zrlib vedle 03_ruin (%s) - zkopiruj ji z repozitare." % root)
    for p in (root, here):
        if p in sys.path: sys.path.remove(p)
        sys.path.insert(0, p)
    for k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin")]: del sys.modules[k]
_boot()

from zrlib.config import *                                   # noqa: F401,F403  (nastaveni vzhledu - zrlib/config.py)
from zrlib import geom, stones, ue_assets, ue_actors, level, validate  # noqa: F401
from zrlib.geom import smooth, interp, Terrain, _pt_on, _wall_len                                    # noqa: F401
from zrlib.stones import Stone, stone_mesh_name, assign_meshes, in_box, stone_mass_kg               # noqa: F401
from zrlib.ue_assets import (ensure_materials, stone_transform, _unit, _fix_unit, _resolve,          # noqa: F401
                             ensure_phys_material, stone_physics, _fix_collision, _mesh_fix)
from zrlib.ue_actors import _new_actor, _add_ism, _ism_actor                                         # noqa: F401
from zrlib.level import gather_volumes                                                               # noqa: F401
from zr_ruin.decay import OPENING_TYPES, opening_state, opening_gap, wall_profile, params, blob_noise, blob_q, courses   # noqa: F401
from zr_ruin.prep import apply_plinth, apply_ref_z, opening_top_abs, resolve_protect_to, apply_volumes, wall_box_hits   # noqa: F401
from zr_ruin.wall import build_wall_stones                                                           # noqa: F401
from zr_ruin.post import roof_clear, cut_notches, rough_core                                         # noqa: F401
from zr_ruin.floor import build_floor_stones                                                         # noqa: F401
from zr_ruin.rubble import make_rubble                                                               # noqa: F401
from zr_ruin import compute as _compute

# ------------------------------------------------------------------ nastaveni behu (vzhled, materialy, meshe: zrlib/config.py)
LAYOUT_PATH = None                       # None = ruin_layout.json vedle skriptu
AGE = None                               # None = podle JSON ("1650"); nebo "1540" / "1650"
OVERRIDE = {}                            # prepis parametru, napr. {"ROBBING": 6}
TERRAIN_FROM_LEVEL = True                # True = vysky terenu se pri buildu zmeri primo z landscapu v levelu (line trace)
                                         #   a ulozi do terrain_from_level.json (capture_manual_edits pouzije tento ulozeny stav)
                                         # False = vysky z ruin_layout.json (puvodni heightmapa)
ONLY_WALLS = None                        # napr. ["Brana_V", "Brana_J"] = postavit jen tyto zdi (rychle ladeni)
CAST = None                              # None = cely hrad; nebo ["Palac"], ["Ostroh"], ["Obvod"] (spousti casti/<Cast>.py)
# casti hradu, ktere se stavi zvlast (zdi a podlahy podle jmena; plati prvni shoda, Obvod = vsechno ostatni)
CASTI = {"Palac": ["Palac_*"],                          # vnitrni: palac
         "Ostroh": ["ZBudova_*"],                       # vnitrni: zapadni budova u ostrohu
         "Obvod": ["*"]}                                # vez, obvodove hradby, brany, dlazba veze


def cast_of(name):
    """do ktere casti hradu patri zed / podlaha"""
    import fnmatch
    for c, pats in CASTI.items():
        if any(fnmatch.fnmatch(name, p) for p in pats): return c
    return "Obvod"



# ------------------------------------------------------------------ vypocet (obal s nastavenim behu)
def compute_blocks(layout, removed=(), moved=None, volumes=None, rubble=False, detached=()):
    """cela zricenina -> {zed: dict(folder, stones, loose)}, P  (zr_ruin.compute s ONLY_WALLS, AGE, OVERRIDE odsud)"""
    validate.layout(layout)
    return _compute.compute_blocks(layout, removed, moved, volumes, rubble, detached, only_walls=ONLY_WALLS, age=AGE, override=OVERRIDE)


# ------------------------------------------------------------------ soubory
def _script_dir():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.path.dirname(LAYOUT_PATH) if LAYOUT_PATH else os.getcwd()

def load_layout():
    path = LAYOUT_PATH or os.path.join(_script_dir(), "ruin_layout.json")
    with open(path, encoding="utf-8") as f: return json.load(f)

def edits_path():
    return os.path.join(os.path.dirname(LAYOUT_PATH) if LAYOUT_PATH else _script_dir(), "manual_edits.json")

def load_manual():
    p = edits_path()
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f: d = json.load(f)
        return d.get("removed", []), d.get("moved", {})
    return [], {}

def load_detached():
    """id kamenu oddelenych od zdi (detach_stones.py) z manual_edits.json"""
    p = edits_path()
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f: return set(json.load(f).get("detached", []))
    return set()

def save_manual(removed, moved, detached):
    with open(edits_path(), "w", encoding="utf-8") as f:
        json.dump({"removed": sorted(removed), "moved": moved, "detached": sorted(detached)}, f, ensure_ascii=False, indent=1)

def load_removed():
    return load_manual()[0]

def _terrain_cache_path():
    return os.path.join(os.path.dirname(os.path.abspath(LAYOUT_PATH)) if LAYOUT_PATH else _script_dir(), "terrain_from_level.json")

def ensure_stone_meshes(unreal):
    """meshe kamenu a dreva (import ze stones/*.obj vedle skriptu)"""
    return ue_assets.ensure_stone_meshes(unreal, os.path.join(_script_dir(), "stones"))


def sample_level_terrain(unreal, layout):
    return level.sample_level_terrain(unreal, layout, _terrain_cache_path())


def cached_level_terrain(layout):
    return level.cached_level_terrain(layout, _terrain_cache_path(), TERRAIN_FROM_LEVEL)


# ------------------------------------------------------------------ Unreal
CNAME = {"face": "Lic", "core": "Jadro", "frame": "Osteni", "wood": "Drevo", "wood_tar": "Drevo_Dehet", "wood_oil": "Drevo_Olej",
         "wood_blood": "Drevo_Krev", "wood_old": "Drevo_Stare", "floor": "Podlaha", "crown": "Koruna"}   # jmena actoru podle kategorie


def build_in_unreal():
    import unreal
    layout = load_layout(); removed, moved = load_manual()
    if TERRAIN_FROM_LEVEL:
        try:
            layout = sample_level_terrain(unreal, layout)
        except Exception as ex:
            unreal.log_warning("Ruin: mereni terenu z levelu selhalo (%s) - pouziji vysky z ruin_layout.json" % ex)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    vols = gather_volumes(unreal, eas)
    detached = load_detached()
    data, P = compute_blocks(layout, removed, moved, vols, detached=detached)
    cube = unreal.load_asset(CUBE_MESH)
    mats = ue_assets.all_materials(unreal)
    meshes = ensure_stone_meshes(unreal)
    tag = unreal.Name(RUIN_TAG); n_total = 0
    with unreal.ScopedEditorTransaction("Build ruin (blocks)"):
        def mine(a):
            """patri actor k vybrane casti / zdi? podle tagu cast:<Cast> a zed:<jmeno> (actor bez nich maze jen build celeho hradu)"""
            if not CAST and not ONLY_WALLS: return True
            c_, z_ = ue_actors.tag_value(a, "cast:"), ue_actors.tag_value(a, "zed:")
            if c_ is None or z_ is None: return False
            return (not CAST or c_ in CAST) and (not ONLY_WALLS or z_ in ONLY_WALLS)
        ue_actors.destroy_tagged(eas, tag, mine)
        data = {n: w for n, w in data.items() if not CAST or cast_of(n) in CAST}
        with unreal.ScopedSlowTask(len(data), "Stavim zriceninu z bloku...") as task:
            task.make_dialog(True)
            for name, w in data.items():
                task.enter_progress_frame(1, name)
                groups = {}
                for s in w["stones"] + w.get("rubble", []):
                    groups.setdefault((s.seg, s.cat), []).append(s)
                nseg = len(set(k[0] for k in groups))
                part_tags = ["cast:" + cast_of(name), "zed:" + name]
                for (seg, cat), sts in sorted(groups.items()):
                    label = ("%s_%02d_%s" % (name, seg + 1, CNAME[cat])) if nseg > 1 else ("%s_%s" % (name, CNAME[cat]))
                    n_total += ue_actors.place_ism(unreal, eas, label, w["folder"] + ("/%s" % name if nseg > 1 else ""), sts, cube, meshes,
                                                   mats.get(cat), tag, part_tags)
                # samostatne kameny (sut, Ruin_Explode / rucne posunute): kazdy vlastni actor, ID v tagu
                for s in w.get("loose", []):
                    act = ue_actors.spawn_loose(unreal, eas, s, cube, meshes,
                                                [tag, "RuinStone", "id:" + s.id] + part_tags + (["Ruin_Detached"] if s.id in detached else []),
                                                w["folder"] + ("/Sut" if "|R" in s.id else "/Odpadle" if s.id in detached else "/Kameny"), mats.get(s.cat))
                    if act is None: continue
                    if DETACHED_PHYSICS and s.id in detached:
                        stone_physics(unreal, act, s, asleep=s.id in moved)
                    n_total += 1
    unreal.log(("Cast %s: " % ", ".join(CAST) if CAST else "") + "Zricenina z bloku (%s): %d bloku ve %d zdech, objemu %d, samostatnych kamenu %d, rucne smazanych %d, posunutych %d, zaoblenych meshu %d." % (
        P["_AGE"], n_total, len(data), len(vols), sum(len(w.get("loose", [])) for w in data.values()), len(removed), len(moved), len(meshes)))

def capture_manual_edits():
    """Ulozi rucni upravy do manual_edits.json:
       - smazane bloky (chybi v Instanced Static Mesh nebo chybi samostatny kamen)
       - posunute / pootocene samostatne kameny (Ruin_Explode)"""
    import unreal
    layout = cached_level_terrain(load_layout()); removed, moved = load_manual(); removed = set(removed)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    detached = load_detached()
    data, P = compute_blocks(layout, removed, moved, gather_volumes(unreal, eas), detached=detached)
    cube = unreal.load_asset(CUBE_MESH)
    meshes = ensure_stone_meshes(unreal)
    present, loose_now = ue_actors.scan_level(unreal, eas, RUIN_TAG)
    n_rem = 0; n_mov = 0
    for name, w in data.items():
        for s in w["stones"] + w.get("rubble", []):
            if ue_actors.instance_key(unreal, s, cube, meshes) not in present:
                removed.add(s.id); n_rem += 1
        for s in w.get("loose", []):
            a = loose_now.get(s.id)
            if a is None:
                removed.add(s.id); moved.pop(s.id, None); detached.discard(s.id); n_rem += 1; continue
            # poloha "kamene" = transformace actoru bez lokalni korekce meshe (F = otoceni os + posun pivotu, meritko 1)
            cur, same = ue_actors.loose_pose(unreal, s, cube, meshes, a)
            if not same:
                moved[s.id] = [round(v, 2) for v in cur]; n_mov += 1
    save_manual(removed, moved, detached)
    unreal.log("manual_edits.json: oddeleno %d, smazano %d (nove %d), posunuto %d (nove %d)." % (len(detached), len(removed), n_rem, len(moved), n_mov))

def _has_unreal():
    try:
        import unreal  # noqa
        return True
    except ImportError:
        return False

MODE = "build"        # "build" = postavit, "capture" = ulozit rucne smazane bloky


def run(cast=None, mode=None):
    """spusteni z UE pro vybrane casti hradu (casti/<Cast>.py): cast = seznam jmen z CASTI, mode = "build" / "capture"
    (capture vzdy porovna cely hrad, ulozi rucni upravy vsech casti)"""
    global CAST, MODE
    CAST = list(cast) if cast else None
    MODE = mode or MODE
    capture_manual_edits() if MODE == "capture" else build_in_unreal()


if (__name__ == "__main__" or "unreal" in sys.modules) and not getattr(sys, "_ruin_import_only", False):
    if _has_unreal():
        run(CAST, MODE)
    else:
        if len(sys.argv) > 1: LAYOUT_PATH = sys.argv[1]
        lay = load_layout(); rm, mv = load_manual(); data, P = compute_blocks(lay, rm, mv, detached=load_detached())
        tot = 0
        for n, w in data.items():
            if CAST and cast_of(n) not in CAST: continue
            c = {"face": 0, "core": 0, "frame": 0, "wood": 0, "floor": 0, "crown": 0}
            for s in w["stones"] + w.get("loose", []): c["wood" if s.cat in WOOD_MI else s.cat] = c.get("wood" if s.cat in WOOD_MI else s.cat, 0) + 1
            tot += sum(c.values()) + len(w.get("rubble", []))
            print("  %-7s %-18s lic %5d  jadro %4d  osteni %3d  sut %3d" % (cast_of(n), n, c["face"], c["core"], c["frame"], len(w.get("rubble", [])))
                  + ("  koruna %4d" % c["crown"]) + ("  drevo %4d  dlazba %3d" % (c["wood"], c["floor"]) if c["wood"] or c["floor"] else ""))
        print("stari:", P["_AGE"], " bloku celkem:", tot)
