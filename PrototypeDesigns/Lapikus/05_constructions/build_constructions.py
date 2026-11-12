"""
build_constructions.py - dodatecne stavby zriceniny ("druhe zabydleni"), Unreal Editor 5.8

Stavi zvlast od zriceniny (03_ruin/blocks/build_ruin_blocks.py), takze se da ladit bez pregenerovani hradu:
  - drevene vestavby: tramy v kapsach, prkna, pruvlak se sloupy, provizorni schody, podesta (constructions.json -> floors)
  - volna sut na zemi u zdi (samostatne actory, lze posouvat a mazat)
Zricenina zustava ve 03: zdi, otvory, kapsy pro tramy, kamenna dlazba.

Pouziti v UE: Tools -> Execute Python Script -> build_constructions.py
  - MODE = "build"   postavit (smaze jen sve actory s tagem Zricenina_Stavby)
  - MODE = "capture" ulozit rucne smazane / posunute kusy do constructions_edits.json
  - MODE = "freeze"  (volitelne) sut bez fyziky, staticka
Sut ma trvalou fyziku (RUBBLE_PHYSICS), hrac s ni muze hnout; hmotnost podle objemu kamene (STONE_PHYSICS v build_ruin_blocks.py).
Usazeni: Simulate (Alt+S), vyber kameny (tag Ruin_Physics), K = Keep Simulation Changes, capture.
Usazene kameny (ulozena poloha) ve hre spi, dokud do nich nekdo nestrci.
Potrebuje: 03_ruin/blocks (build_ruin_blocks.py, ruin_layout.json, terrain_from_level.json po buildu zriceniny).
Mimo UE: python build_constructions.py  -> statistika
"""
import importlib.util, json, os, sys

# ------------------------------------------------------------------ nastaveni
MODE = "build"
DATA_PATH = None                         # None = constructions.json vedle skriptu
RUIN_DIR = None                          # None = ../03_ruin/blocks (vedle slozky 05_constructions)
CONSTR_TAG = "Zricenina_Stavby"
MAT_WOOD = ["/Game/StarterContent/Materials/M_Wood_Oak.M_Wood_Oak", "/Game/StarterContent/Materials/M_Wood_Pine.M_Wood_Pine"]
ONLY = None                              # napr. ["Vez_Patra"] nebo ["Sut"] = postavit jen tuto cast
RUBBLE_PHYSICS = True                    # kameny suti maji trvalou fyziku (hmotnost podle objemu); False = staticke


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
    out = {}
    for fs in data.get("floors", []):
        if ONLY and fs["name"] not in ONLY: continue
        st = R.build_floor_stones(fs, P, walls, terr); R.assign_meshes(st)
        out[fs["name"]] = dict(folder=fs.get("folder", "Stavby"), stones=[s for s in st if s.id not in removed], loose=[])
    rb = data.get("rubble", {})
    if rb.get("enabled", True) and (not ONLY or "Sut" in ONLY):
        for name, r in R.make_rubble(walls, P, terr, removed).items():
            if not r["stones"]: continue
            out[name + "_Sut"] = dict(folder="%s/%s" % (rb.get("folder", "Stavby/Sut"), r["folder"].split("/")[-1]),
                                      stones=[], loose=r["stones"])
    for g in out.values():
        for s in g["stones"] + g["loose"]:
            m = moved.get(s.id)
            if m: s.x, s.y, s.z, s.roll, s.pitch, s.yaw = m
    return out, P


# ------------------------------------------------------------------ Unreal
def _materials(unreal, R):
    mats = R.ensure_materials(unreal)
    mats["floor"] = mats.get("frame")
    if not mats.get("wood"):       # MI_RuinWood (+ _Tar, _Oil) vytvori ensure_materials; zaloha StarterContent
        mats["wood"] = next((unreal.load_asset(p) for p in MAT_WOOD if unreal.EditorAssetLibrary.does_asset_exist(p.split(".")[0])), None)
    for wc in R.WOOD_MI: mats[wc] = mats.get(wc) or mats["wood"]
    return mats


def build_in_unreal():
    import unreal
    R = load_ruin(); data = load_data(); removed, moved = load_edits()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    groups, P = compute(R, data, removed, moved, R.gather_volumes(unreal, eas))
    cube = unreal.load_asset(R.CUBE_MESH); mats = _materials(unreal, R); meshes = R.ensure_stone_meshes(unreal)
    tag = unreal.Name(CONSTR_TAG); n = 0; n_phys = 0
    with unreal.ScopedEditorTransaction("Build constructions"):
        old = [a for a in eas.get_all_level_actors() if tag in a.tags
               and (not ONLY or any(a.get_actor_label().startswith(o) or ("Sut" in ONLY and "_Sut" in a.get_actor_label()) for o in ONLY))]
        if old: eas.destroy_actors(old)
        for name, g in groups.items():
            bycat = {}
            for s in g["stones"]: bycat.setdefault(s.cat, []).append(s)
            for cat, sts in sorted(bycat.items()):
                bym = {}
                for s in sts:
                    m, nom = R._resolve(unreal, s, cube, meshes)
                    bym.setdefault(m.get_path_name(), [m, []])[1].append(R.stone_transform(unreal, s, m, nom))
                cname = {"wood": "Drevo", "wood_tar": "Drevo_Dehet", "wood_oil": "Drevo_Olej", "wood_blood": "Drevo_Krev",
                         "wood_old": "Drevo_Stare", "floor": "Podlaha", "face": "Kamen",
                         "frame": "Kvadr"}.get(cat, cat)
                R._ism_actor(unreal, eas, "%s_%s" % (name, cname), g["folder"], [tuple(v) for _, v in sorted(bym.items())], mats.get(cat), tag)
                n += len(sts)
            for s in g["loose"]:
                m, nom = R._resolve(unreal, s, cube, meshes)
                act = eas.spawn_actor_from_object(m, unreal.Vector(s.x, s.y, s.z), unreal.Rotator(roll=s.roll, pitch=s.pitch, yaw=s.yaw))
                if not act: continue
                act.set_actor_transform(R.stone_transform(unreal, s, m, nom), False, False)
                act.tags = [tag, unreal.Name("RuinStone"), unreal.Name("id:" + s.id)]
                act.set_folder_path(g["folder"])
                act.set_actor_label("Kamen_" + s.id.replace("|", "_"))
                if mats.get(s.cat): act.static_mesh_component.set_material(0, mats[s.cat])
                if RUBBLE_PHYSICS:
                    R.stone_physics(unreal, act, s, asleep=s.id in moved)
                    act.tags = list(act.tags) + [unreal.Name("Ruin_Physics")]; n_phys += 1
                n += 1
    unreal.log("Stavby: %d kusu ve %d skupinach (%s), rucne smazanych %d, posunutych %d, s fyzikou %d%s." % (
        n, len(groups), ", ".join(groups), len(removed), len(moved), n_phys,
        " (usazeni: Simulate, vyber tag Ruin_Physics, K, pak MODE=capture)" if n_phys else ""))


def freeze():
    """vypne fyziku suti (kameny zustanou, kde lezi, staticke); dalsi build ji zase zapne, pokud RUBBLE_PHYSICS = True"""
    import unreal
    R = load_ruin()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem); n = 0
    with unreal.ScopedEditorTransaction("Freeze rubble"):
        for a in eas.get_all_level_actors():
            tags = [str(t) for t in a.tags]
            if "Ruin_Physics" in tags and isinstance(a, unreal.StaticMeshActor):
                R.stone_physics(unreal, a, None, on=False); a.tags = [t for t in a.tags if str(t) != "Ruin_Physics"]; n += 1
    unreal.log("Stavby: fyzika vypnuta u %d kamenu suti." % n)


def capture_edits():
    """ulozi rucne smazane kusy (chybi v Instanced Static Mesh / smazany actor) a posunute samostatne kameny"""
    import unreal
    R = load_ruin(); data = load_data(); removed, moved = load_edits()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    groups, P = compute(R, data, removed, moved, R.gather_volumes(unreal, eas))
    cube = unreal.load_asset(R.CUBE_MESH); meshes = R.ensure_stone_meshes(unreal)
    present = set(); loose_now = {}
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        if CONSTR_TAG not in tags: continue
        ids = [t[3:] for t in tags if t.startswith("id:")]
        if ids: loose_now[ids[0]] = a; continue
        for comp in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
            for i in range(comp.get_instance_count()):
                res = comp.get_instance_transform(i, True)
                t = (res[-1] if isinstance(res, tuple) else res).translation
                present.add((round(t.x), round(t.y), round(t.z)))
    n_rem = n_mov = 0
    for g in groups.values():
        for s in g["stones"]:
            m, nom = R._resolve(unreal, s, cube, meshes); t = R.stone_transform(unreal, s, m, nom).translation
            if (round(t.x), round(t.y), round(t.z)) not in present: removed.add(s.id); n_rem += 1
        for s in g["loose"]:
            a = loose_now.get(s.id)
            if a is None: removed.add(s.id); moved.pop(s.id, None); n_rem += 1; continue
            m, nom = R._resolve(unreal, s, cube, meshes)
            st_t = unreal.MathLibrary.compose_transforms(unreal.MathLibrary.invert_transform(R._fix_unit(unreal, s, m, nom)),
                                                         R._unit(unreal, a.get_actor_transform()))
            loc, rot, _ = unreal.MathLibrary.break_transform(st_t)
            cur = [loc.x, loc.y, loc.z, rot.roll, rot.pitch, rot.yaw]
            same = all(abs(p - q) < 1.0 for p, q in zip(cur[:3], [s.x, s.y, s.z])) and \
                   all(abs(((p - q) + 180) % 360 - 180) < 1.0 for p, q in zip(cur[3:], [s.roll, s.pitch, s.yaw]))
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


if __name__ == "__main__" or "unreal" in sys.modules:
    if _has_unreal():
        {"capture": capture_edits, "freeze": freeze}.get(MODE, build_in_unreal)()
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
