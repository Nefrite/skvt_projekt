"""
build_constructions.py - dodatecne stavby zriceniny ("druhe zabydleni"), Unreal Editor 5.8

Stavi zvlast od zriceniny (03_ruin/blocks/build_ruin_blocks.py), takze se da ladit bez pregenerovani hradu:
  - drevene vestavby: tramy v kapsach, prkna, pruvlak se sloupy, provizorni schody, podesta (constructions.json -> floors)
  - krov u ostrohu: sloupy, pricka, paprskovite a bocni tramy, krytina (constructions.json -> frames)
  - kamenne dostavby z kamene rozvalin (constructions.json -> addons): jednoradove zdi na korunach zriceniny az pod strechu
  - prkenne podlahy na podvalech (constructions.json -> addons, typ plank_floor)
  - volna sut na zemi u zdi (samostatne actory, lze posouvat a mazat); v obyvane casti u ostrohu uklizena
Zricenina zustava ve 03: zdi, otvory, kapsy pro tramy, kamenna dlazba. Dostavby ji nemeni, jen na ni stoji.

Pouziti v UE: Tools -> Execute Python Script ->
  - stavby/<Stavba>.py      jen jedna stavba (Vez_Patra.py, Ostroh_Krov.py, Ostroh_Dostavba.py, Ostroh_Podlaha.py, Sut.py) - ostatni se nesmazou ani neprestavi
  - build_constructions.py  vsechny stavby najednou
  - MODE = "build"   postavit (smaze jen sve actory s tagem Zricenina_Stavby)
  - MODE = "capture" ulozit rucne smazane / posunute kusy do constructions_edits.json
  - MODE = "freeze"  (volitelne) sut bez fyziky, staticka
Sut ma trvalou fyziku (RUBBLE_PHYSICS), hrac s ni muze hnout; hmotnost podle objemu kamene (STONE_PHYSICS v zrlib/config.py).
Usazeni: Simulate (Alt+S), vyber kameny (tag Ruin_Physics), K = Keep Simulation Changes, capture.
Usazene kameny (ulozena poloha) ve hre spi, dokud do nich nekdo nestrci.
Potrebuje: 03_ruin/blocks (build_ruin_blocks.py, ruin_layout.json, terrain_from_level.json po buildu zriceniny).
Mimo UE: python build_constructions.py  -> statistika

Kod (od 11/2026):
  build_constructions.py   tento soubor: nastaveni, data, registr typu staveb (TYPES), build / capture / freeze v Unrealu
  zr_stavby/               typy staveb: vez (drevo ve vezi), krov (krov u ostrohu + spolecna geometrie),
                           dostavba (kamenna dostavba), podlaha (prkenna podlaha)
  ../zrlib/                sdilena knihovna s 03 (config = materialy, drevo, fyzika; geom, stones, ue_assets, ue_actors)
Nova stavba: modul v zr_stavby s funkci build, zaznam v TYPES (+ REQUIRED), polozka v constructions.json,
kopie launcheru ve stavby/ se jmenem stavby.
"""
import importlib.util, json, os, sys


def _boot():
    """sdilena knihovna zrlib (koren repozitare) a typy staveb zr_stavby; v UE pri kazdem spusteni nactene znovu"""
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.normpath(os.path.join(here, ".."))
    if not os.path.isdir(os.path.join(root, "zrlib")):
        raise RuntimeError("Chybi slozka zrlib vedle 05_constructions (%s) - zkopiruj ji z repozitare." % root)
    for p in (root, here):
        if p in sys.path: sys.path.remove(p)
        sys.path.insert(0, p)
    for k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_stavby")]: del sys.modules[k]
_boot()

from zrlib.config import CONSTR_TAG, CUBE_MESH
from zrlib.geom import inside_poly
from zrlib import ue_assets, ue_actors, validate
from zr_stavby import vez, krov, dostavba, podlaha
from zr_stavby.krov import ostroh_geom, roof_under, build_fan_roof, _pt          # noqa: F401  (pro nastroje)
from zr_stavby.dostavba import build_stone_addon, addon_polygon                 # noqa: F401
from zr_stavby.podlaha import build_plank_floor                                 # noqa: F401
from zr_stavby.vez import build_tower_floor                                     # noqa: F401

# ------------------------------------------------------------------ nastaveni
MODE = "build"
DATA_PATH = None                         # None = constructions.json vedle skriptu
RUIN_DIR = None                          # None = ../03_ruin/blocks (vedle slozky 05_constructions)
ONLY = None                              # napr. ["Vez_Patra"], ["Ostroh_Dostavba"] nebo ["Sut"] = postavit jen tuto cast
RUBBLE_PHYSICS = True                    # kameny suti maji trvalou fyziku (hmotnost podle objemu); False = staticke

# ------------------------------------------------------------------ typy staveb
# typ -> funkce(spec, ctx) -> [Stone]; ctx: P (parametry zriceniny), walls (kameny zriceniny), terr (teren),
# data (cely constructions.json), geom (cache spolecne geometrie, napr. krov pro dostavbu)
TYPES = {
    "tower_floor": lambda s, c: vez.build_tower_floor(s, c["P"], c["walls"], c["terr"]),
    "fan_roof":    lambda s, c: krov.build_fan_roof(s, c["P"], c["walls"], c["terr"], c["geom"]),
    "stone_addon": lambda s, c: dostavba.build_stone_addon(s, c["P"], c["walls"], c["terr"], c["data"].get("frames", []), c["geom"]),
    "plank_floor": lambda s, c: podlaha.build_plank_floor(s, c["P"], c["walls"], c["terr"]),
}
# povinne klice dat (kontrola se srozumitelnou chybou misto KeyError uprostred vypoctu)
REQUIRED = {
    "tower_floor": ["name", "origin", "u", "v", "inner", "ref_z", "storey"],
    "fan_roof":    ["name", "posts", "beams", "notches", "wall", "wall_t", "beam", "rise", "crossbeam", "n", "u"],
    "stone_addon": ["name", "roof", "walls"],
    "plank_floor": ["name", "outline", "u", "n"],
}
SECTIONS = (("floors", "tower_floor"), ("frames", None), ("addons", None))   # sekce constructions.json a vychozi typ


def _here():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.path.dirname(DATA_PATH) if DATA_PATH else os.getcwd()


def _ruin_dir():
    if RUIN_DIR: return RUIN_DIR
    for c in (os.path.join(_here(), "..", "03_ruin", "blocks"), os.path.join(_here(), "..", "blocks")):
        if os.path.exists(os.path.join(c, "build_ruin_blocks.py")): return os.path.abspath(c)
    raise RuntimeError("Nenasel jsem 03_ruin/blocks/build_ruin_blocks.py - nastav RUIN_DIR nahore ve skriptu.")


def load_ruin():
    """nacte generator zriceniny jako knihovnu (nic nepostavi)"""
    d = _ruin_dir()
    sys._ruin_import_only = True
    try:
        sp = importlib.util.spec_from_file_location("build_ruin_blocks", os.path.join(d, "build_ruin_blocks.py"))
        R = importlib.util.module_from_spec(sp); sp.loader.exec_module(R)
    finally:
        sys._ruin_import_only = False
    R.LAYOUT_PATH = os.path.join(d, "ruin_layout.json")
    return R


def load_data():
    with open(DATA_PATH or os.path.join(_here(), "constructions.json"), encoding="utf-8") as f: return json.load(f)


def edits_path():
    return os.path.join(os.path.dirname(DATA_PATH) if DATA_PATH else _here(), "constructions_edits.json")


def load_edits():
    p = edits_path()
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f: d = json.load(f)
        return set(d.get("removed", [])), d.get("moved", {})
    return set(), {}


def compute(R, data, removed=(), moved=None, volumes=None):
    """-> {skupina: dict(folder, stones (Instanced Static Mesh), loose (samostatne actory))}, P"""
    moved = moved or {}
    layout = R.cached_level_terrain(R.load_layout())          # stejny teren jako posledni build zriceniny
    rr, rm = R.load_manual()
    walls, P = R.compute_blocks(layout, rr, rm, volumes)       # zdi zriceniny (kvuli kapsam a podpore tramu)
    terr = R.Terrain(layout["terrain"])
    ctx = dict(P=P, walls=walls, terr=terr, data=data, geom={})
    out = {}
    for sec, default in SECTIONS:
        for spec in data.get(sec, []):
            if ONLY and spec["name"] not in ONLY: continue
            typ = spec.get("type", default)
            if typ not in TYPES: continue
            validate.require(spec, REQUIRED.get(typ, []), "constructions.json -> %s -> %s (%s)" % (sec, spec.get("name"), typ))
            st = TYPES[typ](spec, ctx); R.assign_meshes(st)
            out[spec["name"]] = dict(folder=spec.get("folder", "Stavby"), stones=[s for s in st if s.id not in removed], loose=[])
    rb = data.get("rubble", {})
    if rb.get("enabled", True) and (not ONLY or "Sut" in ONLY):
        out.update(_rubble(R, data, rb, walls, P, terr, removed))
    for g in out.values():
        for s in g["stones"] + g["loose"]:
            m = moved.get(s.id)
            if m: s.x, s.y, s.z, s.roll, s.pitch, s.yaw = m
    return out, P


def _rubble(R, data, rb, walls, P, terr, removed):
    """volna sut u zdi (samostatne actory s fyzikou); v obyvanych castech (dostavby, podlahy) uklizena"""
    clear = [p for p in (addon_polygon(ad) for ad in data.get("addons", []) if ad.get("clear_rubble")) if p]
    clear += [[tuple(q) for q in ad["outline"]] for ad in data.get("addons", []) if ad.get("type") == "plank_floor"]   # na podlaze sut neni
    out = {}
    for name, r in R.make_rubble(walls, P, terr, removed).items():
        sts = [s for s in r["stones"] if not any(inside_poly(p, s.x, s.y) for p in clear)]
        if not sts: continue
        out[name + "_Sut"] = dict(folder="%s/%s" % (rb.get("folder", "Stavby/Sut"), r["folder"].split("/")[-1]),
                                  stones=[], loose=sts, stavba="Sut")
    return out


# ------------------------------------------------------------------ Unreal
CNAME = {"wood": "Drevo", "wood_tar": "Drevo_Dehet", "wood_oil": "Drevo_Olej", "wood_blood": "Drevo_Krev",
         "wood_old": "Drevo_Stare", "floor": "Podlaha", "face": "Kamen", "core": "Malta", "frame": "Kvadr"}


def build_in_unreal():
    import unreal
    R = load_ruin(); data = load_data(); removed, moved = load_edits()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    groups, P = compute(R, data, removed, moved, R.gather_volumes(unreal, eas))
    cube = unreal.load_asset(CUBE_MESH); mats = ue_assets.all_materials(unreal); meshes = R.ensure_stone_meshes(unreal)
    tag = unreal.Name(CONSTR_TAG); n = 0; n_phys = 0
    with unreal.ScopedEditorTransaction("Build constructions"):
        # stavba podle tagu stavba:<jmeno>; actor bez tagu smaze jen build vsech staveb
        ue_actors.destroy_tagged(eas, tag, lambda a: not ONLY or ue_actors.tag_value(a, "stavba:") in ONLY)
        for name, g in groups.items():
            st_tag = "stavba:" + g.get("stavba", name)
            bycat = {}
            for s in g["stones"]: bycat.setdefault(s.cat, []).append(s)
            for cat, sts in sorted(bycat.items()):
                n += ue_actors.place_ism(unreal, eas, "%s_%s" % (name, CNAME.get(cat, cat)), g["folder"], sts, cube, meshes, mats.get(cat), tag, [st_tag])
            for s in g["loose"]:
                act = ue_actors.spawn_loose(unreal, eas, s, cube, meshes, [tag, "RuinStone", "id:" + s.id, st_tag], g["folder"], mats.get(s.cat))
                if act is None: continue
                if RUBBLE_PHYSICS:
                    ue_assets.stone_physics(unreal, act, s, asleep=s.id in moved)
                    act.tags = list(act.tags) + [unreal.Name("Ruin_Physics")]; n_phys += 1
                n += 1
    unreal.log("Stavby: %d kusu ve %d skupinach (%s), rucne smazanych %d, posunutych %d, s fyzikou %d%s." % (
        n, len(groups), ", ".join(groups), len(removed), len(moved), n_phys,
        " (usazeni: Simulate, vyber tag Ruin_Physics, K, pak MODE=capture)" if n_phys else ""))


def freeze():
    """vypne fyziku suti (kameny zustanou, kde lezi, staticke); dalsi build ji zase zapne, pokud RUBBLE_PHYSICS = True"""
    import unreal
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem); n = 0
    with unreal.ScopedEditorTransaction("Freeze rubble"):
        for a in eas.get_all_level_actors():
            tags = [str(t) for t in a.tags]
            if "Ruin_Physics" in tags and isinstance(a, unreal.StaticMeshActor):
                ue_assets.stone_physics(unreal, a, None, on=False); a.tags = [t for t in a.tags if str(t) != "Ruin_Physics"]; n += 1
    unreal.log("Stavby: fyzika vypnuta u %d kamenu suti." % n)


def capture_edits():
    """ulozi rucne smazane kusy (chybi v Instanced Static Mesh / smazany actor) a posunute samostatne kameny"""
    import unreal
    R = load_ruin(); data = load_data(); removed, moved = load_edits()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    groups, P = compute(R, data, removed, moved, R.gather_volumes(unreal, eas))
    cube = unreal.load_asset(CUBE_MESH); meshes = R.ensure_stone_meshes(unreal)
    present, loose_now = ue_actors.scan_level(unreal, eas, CONSTR_TAG)
    n_rem = n_mov = 0
    for g in groups.values():
        for s in g["stones"]:
            if ue_actors.instance_key(unreal, s, cube, meshes) not in present: removed.add(s.id); n_rem += 1
        for s in g["loose"]:
            a = loose_now.get(s.id)
            if a is None: removed.add(s.id); moved.pop(s.id, None); n_rem += 1; continue
            cur, same = ue_actors.loose_pose(unreal, s, cube, meshes, a)
            if not same: moved[s.id] = [round(v, 2) for v in cur]; n_mov += 1
    with open(edits_path(), "w", encoding="utf-8") as f:
        json.dump({"removed": sorted(removed), "moved": moved}, f, ensure_ascii=False, indent=1)
    unreal.log("constructions_edits.json: smazano %d (nove %d), posunuto %d (nove %d)." % (len(removed), n_rem, len(moved), n_mov))


def _has_unreal():
    try:
        import unreal  # noqa
        return True
    except ImportError:
        return False


def run(only=None, mode=None):
    """spusteni z UE pro vybrane stavby (stavby/<Stavba>.py): only = seznam jmen ze constructions.json (+ "Sut"),
    mode = "build" / "capture" / "freeze"; ruzne stavby se navzajem nesmazou ani neprestavi"""
    global ONLY, MODE
    ONLY = list(only) if only else None
    MODE = mode or MODE
    {"capture": capture_edits, "freeze": freeze}.get(MODE, build_in_unreal)()


if (__name__ == "__main__" or "unreal" in sys.modules) and not getattr(sys, "_constr_import_only", False):
    if _has_unreal():
        run(ONLY, MODE)
    else:
        if len(sys.argv) > 1: DATA_PATH = sys.argv[1]
        if len(sys.argv) > 2: RUIN_DIR = sys.argv[2]
        R = load_ruin()
        if len(sys.argv) > 3: R.LAYOUT_PATH = sys.argv[3]
        groups, P = compute(R, load_data(), *load_edits())
        for n, g in groups.items():
            c = {}
            for s in g["stones"] + g["loose"]: c[s.cat] = c.get(s.cat, 0) + 1
            print("  %-22s %-24s %s" % (n, g["folder"], ", ".join("%s %d" % kv for kv in sorted(c.items()))))
