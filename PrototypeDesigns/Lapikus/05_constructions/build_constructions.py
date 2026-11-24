"""
build_constructions.py - dodatecne stavby zriceniny ("druhe zabydleni"), Unreal Editor 5.8

Stavi zvlast od zriceniny (03_ruin/blocks/build_ruin_blocks.py), takze se da ladit bez pregenerovani hradu:
  - drevene vestavby: tramy v kapsach, prkna, pruvlak se sloupy, provizorni schody, podesta (constructions.json -> floors)
  - krov u ostrohu: sloupy, pricka (hreben), vejir tramu a tramy dokola pricky, krytina (constructions.json -> frames)
  - kamenne dostavby z kamene rozvalin (constructions.json -> addons): jednoradove zdi na korunach zriceniny az pod strechu
  - prkenne podlahy na podvalech (constructions.json -> addons, typ plank_floor)
  - pultove strechy na sloupech (constructions.json -> frames, typ pult_roof): pristresek kovarny v palaci
  - ohniste / vyhne (constructions.json -> addons, typ hearth): kamenny stul, zidka, dymnik a komin z prouti a hliny
  - zdivo z kamene rozvalin (constructions.json -> addons, typ stone_fill): srovnani korun zdi, zazdeni otvoru, podezdivky
  - steny z prouti a hliny (addons, typ wattle_wall): dilce mezi sloupy, kuly na spojich
  - okapy (addons, typ gutter): vydlabany zlab na rozsochach pod okapem, sud na destovou vodu (samostatny actor)
  - vybaveni (addons, typ props): hotove props rozmistene jako samostatne actory (rucni doladeni pres capture)
  - sruby (addons, typ log_wall): steny z loupane kulatiny v radach, otvory, prkenne stity pod pultovou strechu
  - podesty (addons, typ platform): tramy z kulatiny v kapsach / na korune zdi, prkna, zabradli (strazni stanoviste nad branami)
  - platenne pristresky (addons, typ canvas_shelter): kuly s rozsochou, hreben, okapova tyc, krokvove tyce, plachta a stit
    na miru, lana, ovazani, kameny (pristresek hlidky na vezi)
  - etapy: stavba se "stage" v datech stavi actory po sadach (base / final / site) s tagem stage:<sada> (zrlib/config.py)
  - hranice materialu (data "pile": true): cela stavba je jeden actor s pivotem dole uprostred (tag pile:<jmeno>); posun a
    natoceni kolem svisle osy v levelu ulozi capture do constructions_edits.json (moved["pile:<jmeno>"]) a build pak posune
    celou hranici; naklon actoru se neuklada
  - prah dveri v dostavbe: samostatny actor (soucast Ostroh_Dostavba), vyska se doladi rucne a ulozi pres capture
  - volna sut na zemi u zdi (samostatne actory, lze posouvat a mazat); v obyvane casti u ostrohu uklizena
Zricenina zustava ve 03: zdi, otvory, kapsy pro tramy, kamenna dlazba. Dostavby ji nemeni, jen na ni stoji.

Pouziti v UE: Tools -> Execute Python Script ->
  - stavby/<Stavba>.py      jen jedna stavba (Vez_Patra.py, Ostroh_Krov.py, Ostroh_Dostavba.py, Ostroh_Podlaha.py,
                            Palac_Kovarna_Pristresek.py, Palac_Kovarna_Vyhen.py, Palac_Kovarna_Stena.py, Palac_Kovarna_Okap.py,
                            Palac_Obydli_Kamen.py,
                            Palac_Obydli_Ohniste.py, Palac_Obydli_Krov.py, Palac_Obydli_Srub.py,
                            Palac_Obydli_Stavenisko.py (+ _Capture.py), Sut.py) - ostatni se nesmazou ani neprestavi
  - build_constructions.py  vsechny stavby najednou
  - ../build_normal.py      cely hrad (03) + vsechny stavby; ../build_fullscope.py = oprava (smaze generovane actory a meshe, vse znovu)
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
                           dostavba (kamenna dostavba), podlaha (prkenna podlaha), pult (pultova strecha na sloupech),
                           ohniste (ohniste / vyhen s dymnikem a kominem), zdivo (zdivo z kamene rozvalin),
                           stena (stena z prouti), okap (zlab, rozsochy, sud), vybaveni (props), srub (srubove steny, stity),
                           podesta (tramy, prkna, zabradli), kryty (kryt z kulatiny na korune zdi),
                           pristresek (platenny pristresek na kulatine)
  ../zrlib/                sdilena knihovna s 03 (config = materialy, drevo, fyzika; geom, stones, ue_assets, ue_actors)
Nova stavba: modul v zr_stavby s funkci build, zaznam v TYPES (+ REQUIRED), polozka v constructions.json,
kopie launcheru ve stavby/ se jmenem stavby.
"""
import json, math, os, sys


def _boot():
    """sdilena knihovna zrlib (koren repozitare) a typy staveb zr_stavby; v UE pri kazdem spusteni nactene znovu
    (ne kdyz skript nacita zrlib/pipeline.py jako knihovnu - sys._zr_keep, moduly zahodil uz vstupni skript)"""
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.normpath(os.path.join(here, ".."))
    if not os.path.isdir(os.path.join(root, "zrlib")):
        raise RuntimeError("Chybi slozka zrlib vedle 05_constructions (%s) - zkopiruj ji z repozitare." % root)
    for p in (root, here):
        if p in sys.path: sys.path.remove(p)
        sys.path.insert(0, p)
    if not getattr(sys, "_zr_keep", False):
        for k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_stavby")]: del sys.modules[k]
_boot()

from zrlib.config import CONSTR_TAG, CUBE_MESH, STAGE_TAG, STAGES
from zrlib.geom import inside_poly
from zrlib import pipeline, ue_assets, ue_actors, validate
from zr_stavby import vez, krov, dostavba, podlaha, pult, ohniste, zdivo, stena, okap, vybaveni, srub, podesta, kryty, pristresek
from zr_stavby.krov import ostroh_geom, roof_under, build_fan_roof, _pt          # noqa: F401  (pro nastroje)
from zr_stavby.dostavba import build_stone_addon, addon_polygon                 # noqa: F401
from zr_stavby.podlaha import build_plank_floor                                 # noqa: F401
from zr_stavby.vez import build_tower_floor                                     # noqa: F401
from zr_stavby.pult import build_pult_roof, pult_geom                          # noqa: F401

# ------------------------------------------------------------------ nastaveni
MODE = "build"
DATA_PATH = None                         # None = constructions.json vedle skriptu
RUIN_DIR = None                          # None = ../03_ruin/blocks (vedle slozky 05_constructions)
ONLY = None                              # napr. ["Vez_Patra"], ["Ostroh_Dostavba"] nebo ["Sut"] = postavit jen tuto cast
ROOF_COVER = True                        # krov u ostrohu a pultove strechy s krytinou (late, prkna, listy, hreben, lemovani); False = jen kostra
RUBBLE_PHYSICS = True                    # kameny suti maji trvalou fyziku (hmotnost podle objemu); False = staticke

# ------------------------------------------------------------------ typy staveb
# typ -> funkce(spec, ctx) -> [Stone]; ctx: P (parametry zriceniny), walls (kameny zriceniny), terr (teren),
# data (cely constructions.json), geom (cache spolecne geometrie, napr. krov pro dostavbu)
TYPES = {
    "tower_floor": lambda s, c: vez.build_tower_floor(s, c["P"], c["walls"], c["terr"]),
    "fan_roof":    lambda s, c: krov.build_fan_roof(s, c["P"], c["walls"], c["terr"], c["geom"], cover=ROOF_COVER),
    "stone_addon": lambda s, c: dostavba.build_stone_addon(s, c["P"], c["walls"], c["terr"], c["data"].get("frames", []), c["geom"],
                                                   addons=c["data"].get("addons", [])),
    "plank_floor": lambda s, c: podlaha.build_plank_floor(s, c["P"], c["walls"], c["terr"]),
    "pult_roof":   lambda s, c: pult.build_pult_roof(s, c["P"], c["walls"], c["terr"], c["geom"], cover=ROOF_COVER),
    "hearth":      lambda s, c: ohniste.build_hearth(s, c["terr"], c["data"].get("frames", []), c["geom"]),
    "stone_fill":  lambda s, c: zdivo.build_stone_fill(s, c["walls"], c["terr"]),
    "wattle_wall": lambda s, c: stena.build_wattle_wall(s, c["terr"]),
    "gutter":      lambda s, c: okap.build_gutter(s, c["terr"], c["data"].get("frames", []), c["geom"]),
    "props":       lambda s, c: vybaveni.build_props(s, c["terr"], c["data"].get("frames", []), c["geom"]),
    "log_wall":    lambda s, c: srub.build_log_wall(s, c["terr"], c["data"].get("frames", []), c["geom"]),
    "platform":    lambda s, c: podesta.build_platform(s, c["terr"]),
    "palisade":    lambda s, c: kryty.build_palisade(s, c["walls"], c["terr"]),
    "canvas_shelter": lambda s, c: pristresek.build_canvas_shelter(s, c["walls"], c["terr"]),
}
# povinne klice dat (kontrola se srozumitelnou chybou misto KeyError uprostred vypoctu)
REQUIRED = {
    "tower_floor": ["name", "origin", "u", "v", "inner", "ref_z", "storey"],
    "fan_roof":    ["name", "posts", "beams", "notches", "wall", "wall_t", "beam", "rise", "crossbeam", "n", "u"],
    "stone_addon": ["name", "roof", "walls"],
    "plank_floor": ["name", "outline", "u", "n"],
    "pult_roof":   ["name", "origin", "u", "v", "supports", "rafters"],
    "hearth":      ["name", "origin", "u", "v", "table"],
    "stone_fill":  ["name", "origin", "u", "v", "parts"],
    "wattle_wall": ["name", "origin", "u", "v", "a", "c", "h", "t"],
    "gutter":      ["name", "origin", "u", "v", "roof", "a", "c", "d"],
    "props":       ["name", "origin", "u", "v", "items"],
    "log_wall":    ["name", "origin", "u", "v", "ref", "walls"],
    "platform":    ["name", "origin", "u", "v", "z", "beams", "planks"],
    "palisade":    ["name", "origin", "u", "v", "lines"],
    "canvas_shelter": ["name", "origin", "u", "v", "z_ref", "floor_top", "posts", "ridge", "eave", "rafters", "canvas", "gable"],
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
    """nacte generator zriceniny jako knihovnu (nic nepostavi); sdili s nim jednu kopii zrlib"""
    return pipeline.load_ruin(_ruin_dir())


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
            if spec.get("stage"):                                  # stavba s etapami: dilce bez vlastni sady patri do sady stavby
                if spec["stage"] not in STAGES: raise ValueError("%s: neznama sada etapy %s (STAGES v zrlib/config.py)" % (spec["name"], spec["stage"]))
                for s in st: s.stage = s.stage or spec["stage"]
            st = [s for s in st if s.id not in removed]
            pv = _pile(spec["name"], st, moved) if spec.get("pile") else None
            # loose = samostatne actory (rucne posunute se ulozi pres capture), jinak Instanced Static Mesh
            out[spec["name"]] = dict(folder=spec.get("folder", "Stavby"), stones=[s for s in st if not s.loose], loose=[s for s in st if s.loose])
            if pv: out[spec["name"]]["pile"] = pv
    rb = data.get("rubble", {})
    if rb.get("enabled", True) and (not ONLY or "Sut" in ONLY):
        out.update(_rubble(R, data, rb, walls, P, terr, removed))
    for g in out.values():
        if g.get("pile"): continue                                 # hranice se posouva jen jako celek (_pile)
        for s in g["stones"] + g["loose"]:
            m = moved.get(s.id)
            if m: s.x, s.y, s.z, s.roll, s.pitch, s.yaw = m
    return out, P


PILE_KEY = "pile:"                       # klic v constructions_edits.json -> moved a tag actoru hranice materialu


def _pile(name, sts, moved):
    """hranice materialu / slozeny objekt (data "pile": true): vsechny kusy do jednoho actoru (Instanced Static Mesh) s pivotem dole uprostred.
    Poloha z levelu moved["pile:<jmeno>"] = [x, y, z, roll, pitch, yaw] (ulozi capture) posune pivot a natoci celou hranici
    kolem svisle osy (naklon se nebere). -> pivot [x, y, z, yaw] pro build"""
    if not sts: return None
    for s in sts: s.loose = False
    px = sum(s.x for s in sts) / len(sts); py = sum(s.y for s in sts) / len(sts)
    hz = lambda s: (s.sx / 2 * abs(math.sin(math.radians(s.pitch)))) if s.shape == "stake2" and s.pitch else s.sz / 2
    pz = min(s.z - hz(s) for s in sts)
    m = moved.get(PILE_KEY + name)
    if not m: return [round(px, 2), round(py, 2), round(pz, 2), 0.0]
    x, y, z, yaw = m[0], m[1], m[2], m[5]; c, sn = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    for s in sts:                                               # yaw UE: osa X k +Y (stejne jako s.yaw kusu)
        dx, dy = s.x - px, s.y - py
        s.x, s.y, s.z = x + c * dx - sn * dy, y + sn * dx + c * dy, s.z - pz + z; s.yaw += yaw
    return [x, y, z, yaw]


def _rubble(R, data, rb, walls, P, terr, removed):
    """volna sut u zdi (samostatne actory s fyzikou); v obyvanych castech (dostavby, podlahy) uklizena"""
    clear = [p for p in (addon_polygon(ad) for ad in data.get("addons", []) if ad.get("clear_rubble") and ad.get("type") == "stone_addon") if p]
    clear += [[tuple(q) for q in ad["outline"]] for ad in data.get("addons", []) if ad.get("type") == "plank_floor"]   # na podlaze sut neni
    clear += [[tuple(q) for q in ad["clear_poly"]] for sec in ("frames", "addons") for ad in data.get(sec, []) if ad.get("clear_poly")]   # uklizeny pudorys stavby
    out = {}
    for name, r in R.make_rubble(walls, P, terr, removed).items():
        sts = [s for s in r["stones"] if not any(inside_poly(p, s.x, s.y) for p in clear)]
        if not sts: continue
        out[name + "_Sut"] = dict(folder="%s/%s" % (rb.get("folder", "Stavby/Sut"), r["folder"].split("/")[-1]),
                                  stones=[], loose=sts, stavba="Sut", physics=True)
    return out


# ------------------------------------------------------------------ Unreal
CNAME = {"wood": "Drevo", "wood_tar": "Drevo_Dehet", "wood_oil": "Drevo_Olej", "wood_blood": "Drevo_Krev",
         "wood_old": "Drevo_Stare", "wood_peeled": "Drevo_Loupane", "floor": "Podlaha", "face": "Kamen", "core": "Malta", "frame": "Kvadr",
         "daub": "Mazanina", "charcoal": "Uhli", "iron": "Zelezo"}


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
            bycat = {}                                              # actor = material x sada etapy (prepinani etap podle tagu stage:<sada>)
            for s in g["stones"]: bycat.setdefault((s.cat, s.stage or ""), []).append(s)
            for (cat, stage), sts in sorted(bycat.items()):
                label = "%s_%s%s" % (name, CNAME.get(cat, cat), "_" + stage.capitalize() if stage else "")
                n += ue_actors.place_ism(unreal, eas, label, g["folder"], sts, cube, meshes, mats.get(cat), tag,
                                         [st_tag] + ([STAGE_TAG + stage] if stage else []) + ([PILE_KEY + name] if g.get("pile") else []),
                                         pivot=g.get("pile"))
            for s in g["loose"]:
                act = ue_actors.spawn_loose(unreal, eas, s, cube, meshes, [tag, "RuinStone", "id:" + s.id, st_tag] + ([STAGE_TAG + s.stage] if s.stage else []),
                                            g["folder"], mats.get(s.cat))
                if act is None: continue
                if RUBBLE_PHYSICS and g.get("physics"):                     # fyzika jen u suti
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
    for name, g in groups.items():
        if g.get("pile"):                                          # hranice materialu: poloha celeho actoru, ne jednotlivych kusu
            key = PILE_KEY + name
            a = next((a for a in eas.get_all_level_actors() if key in [str(t) for t in a.tags]), None)
            if a is None:                                          # hranice smazana
                removed.update(s.id for s in g["stones"]); moved.pop(key, None); n_rem += len(g["stones"]); continue
            l, r = a.get_actor_location(), a.get_actor_rotation(); pv = g["pile"]
            cur = [round(l.x, 2), round(l.y, 2), round(l.z, 2), round(-r.roll, 2), round(r.pitch, 2), round(r.yaw, 2)]
            if any(abs(p - q) >= 1.0 for p, q in zip(cur[:3], pv[:3])) or abs(((cur[5] - pv[3]) + 180) % 360 - 180) >= 0.5:
                moved[key] = cur; n_mov += 1
            continue
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
