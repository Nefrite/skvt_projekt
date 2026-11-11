"""
detach_stones.py - dodatecne oddeleni casti kamenu od zdi zriceniny, bez prestavby (Unreal Editor 5.8)

Kameny uvnitr Trigger Boxu s tagem Ruin_Detach se vyjmou z Instanced Static Meshe zdi a postavi se jako
samostatne actory (presne na stejnem miste, stejny mesh i material). Zbytek zdi zustane, jak je.
Oddelene kameny se zapisou do manual_edits.json ("detached"), takze je dalsi build zriceniny postavi
zase jako samostatne kameny (i s polohou po simulaci, kdyz ji ulozis capture).

Postup v UE:
  1. Do levelu dej Trigger Box pres cast zdi, ktera ma odpadnout, a pridej mu tag  Ruin_Detach.
     (Kdyz mas vybrane nejake Trigger Boxy, pouziji se jen vybrane.)
  2. Tools -> Execute Python Script -> detach_stones.py   (MODE = "detach")
     Kameny dostanou fyziku (SIMULATE = True), zatim stoji na miste.
  3. Spust Simulate (Alt+S). Kameny spadnou. Az se usadi, vyber je (Outliner: slozka .../Odpadle,
     nebo tag Ruin_Detached) a stiskni K (Keep Simulation Changes). Simulaci ukonci.
  4. build_ruin_blocks.py s MODE = "capture" -> nove polohy se ulozi do manual_edits.json.
  Fyzika zustava (i po dalsim buildu): hrac do kamenu muze strcit, tezky kamen se ale posune jen malo.
  Usazene kameny (ulozena poloha) ve hre spi, dokud do nich nekdo nestrci.
  5. (volitelne) detach_stones.py s MODE = "freeze" -> kameny bez fyziky (staticke); dalsi build ji zase zapne,
     pokud v build_ruin_blocks.py neni DETACHED_PHYSICS = False.
  Trigger Box s Ruin_Detach pak muzes smazat (oddeleni uz je ulozene).

Rozpadle jadro za odpadlym licem (lomove kameny) se dopocita az pri dalsim buildu zriceniny.
MODE = "undo": kameny v boxech s Ruin_Detach vrati zpet do zdi (az po dalsim buildu zriceniny).
Neni potreba zadny build. Skript cte stejny stav jako capture (terrain_from_level.json, manual_edits.json).
"""
import importlib.util, json, os, sys

MODE = "detach"            # "detach" | "freeze" | "undo"
SIMULATE = True            # oddelene kameny dostanou trvalou fyziku (spadnou v Simulate / PIE, hrac s nimi muze hnout);
                           # hmotnost podle objemu a ostatni nastaveni: STONE_PHYSICS v build_ruin_blocks.py
DETACH_TAG = "Ruin_Detach"
CATS = ("face", "crown", "core", "frame")   # ktere kameny lze oddelit (lic, koruna, jadro, osteni)
RUIN_DIR = None            # None = slozka tohoto skriptu (vedle build_ruin_blocks.py)


def _here():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return RUIN_DIR or os.getcwd()


def load_ruin():
    d = RUIN_DIR or _here()
    sys._ruin_import_only = True
    try:
        sp = importlib.util.spec_from_file_location("build_ruin_blocks", os.path.join(d, "build_ruin_blocks.py"))
        R = importlib.util.module_from_spec(sp); sp.loader.exec_module(R)
    finally:
        sys._ruin_import_only = False
    R.LAYOUT_PATH = os.path.join(d, "ruin_layout.json")
    return R


def _boxes(unreal, eas):
    sel = [a for a in eas.get_selected_level_actors() if DETACH_TAG in [str(t) for t in a.tags]]
    acts = sel or [a for a in eas.get_all_level_actors() if DETACH_TAG in [str(t) for t in a.tags]]
    out = []
    for a in acts:
        o, e = a.get_actor_bounds(False)
        out.append([o.x - e.x, o.y - e.y, o.z - e.z, o.x + e.x, o.y + e.y, o.z + e.z])
    return out


def _key(t):
    return (round(t.x), round(t.y), round(t.z))


def detach():
    import unreal
    R = load_ruin()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    boxes = _boxes(unreal, eas)
    if not boxes:
        unreal.log_warning("detach_stones: zadny Trigger Box s tagem %s." % DETACH_TAG); return
    layout = R.cached_level_terrain(R.load_layout()); removed, moved = R.load_manual(); detached = R.load_detached()
    data, P = R.compute_blocks(layout, set(removed), moved, R.gather_volumes(unreal, eas), detached=detached)
    cube = unreal.load_asset(R.CUBE_MESH); meshes = R.ensure_stone_meshes(unreal)
    # kameny zdi v boxech -> poloha instance (jako capture) -> id
    want = {}
    for name, w in data.items():
        for s in w["stones"]:
            if s.cat not in CATS or not any(R.in_box(s, b) for b in boxes): continue
            m, nom = R._resolve(unreal, s, cube, meshes)
            want[_key(R.stone_transform(unreal, s, m, nom).translation)] = (s, w["folder"])
    if not want:
        unreal.log_warning("detach_stones: v boxech nejsou zadne kameny zdi."); return
    tag = unreal.Name(R.RUIN_TAG); n = 0; new_ids = []
    with unreal.ScopedEditorTransaction("Detach ruin stones"):
        for a in eas.get_all_level_actors():
            if tag not in a.tags or any(str(t).startswith("id:") for t in a.tags): continue
            for comp in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
                hits = []
                for i in range(comp.get_instance_count()):
                    res = comp.get_instance_transform(i, True)
                    tr = res[-1] if isinstance(res, tuple) else res
                    k = _key(tr.translation)
                    if k in want: hits.append((i, tr, want.pop(k)))
                if not hits: continue
                mesh = comp.static_mesh; mat = comp.get_material(0)
                for i, tr, (s, folder) in hits:
                    act = eas.spawn_actor_from_object(mesh, tr.translation, tr.rotation.rotator())
                    if not act: continue
                    act.set_actor_transform(tr, False, False)
                    act.tags = [tag, unreal.Name("RuinStone"), unreal.Name("id:" + s.id), unreal.Name("Ruin_Detached")]
                    act.set_folder_path(folder + "/Odpadle")
                    act.set_actor_label("Kamen_" + s.id.replace("|", "_"))
                    smc = act.static_mesh_component
                    if mat: smc.set_material(0, mat)
                    if SIMULATE: R.stone_physics(unreal, act, s)
                    new_ids.append(s.id); n += 1
                for i, _, _ in sorted(hits, key=lambda h: -h[0]):      # od konce, at se indexy neposouvaji
                    comp.remove_instance(i)
    detached.update(new_ids)
    R.save_manual(set(removed), moved, detached)
    unreal.log("detach_stones: oddeleno %d kamenu (celkem oddelenych %d)%s. %s" % (
        n, len(detached), ", nenalezeno v levelu %d" % len(want) if want else "",
        "Spust Simulate, vyber kameny (tag Ruin_Detached), K = Keep Simulation Changes, pak capture." if SIMULATE else ""))


def freeze():
    """vypne fyziku oddelenych kamenu (po Keep Simulation Changes a capture)"""
    import unreal
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem); n = 0
    with unreal.ScopedEditorTransaction("Freeze detached stones"):
        for a in eas.get_all_level_actors():
            if "Ruin_Detached" in [str(t) for t in a.tags] and isinstance(a, unreal.StaticMeshActor):
                R.stone_physics(unreal, a, None, on=False); n += 1
    unreal.log("detach_stones: fyzika vypnuta u %d kamenu. Velikost se srovna pri dalsim buildu zriceniny." % n)


def undo():
    """kameny v boxech s Ruin_Detach vrati do zdi (z manual_edits.json zmizi oddeleni i posun) - projevi se po buildu"""
    import unreal
    R = load_ruin()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    boxes = _boxes(unreal, eas)
    layout = R.cached_level_terrain(R.load_layout()); removed, moved = R.load_manual(); detached = R.load_detached()
    data, P = R.compute_blocks(layout, set(removed), {}, R.gather_volumes(unreal, eas), detached=detached)   # puvodni polohy
    back = [s.id for w in data.values() for s in w.get("loose", []) if s.id in detached and any(R.in_box(s, b) for b in boxes)]
    for i in back:
        detached.discard(i); moved.pop(i, None)
    R.save_manual(set(removed), moved, detached)
    unreal.log("detach_stones: %d kamenu vraceno do zdi (spust build_ruin_blocks.py)." % len(back))


if __name__ == "__main__" or "unreal" in sys.modules:
    try:
        import unreal  # noqa
        {"detach": detach, "freeze": freeze, "undo": undo}[MODE]()
    except ImportError:
        print("detach_stones.py se spousti v Unreal Editoru (Tools -> Execute Python Script).")
