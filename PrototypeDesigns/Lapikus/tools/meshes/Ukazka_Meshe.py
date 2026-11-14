"""Ukazka_Meshe.py - v UE postavi ukazku knihovnich meshi s materialy (kontrola tvaru, slotu, textur).
Unreal: Tools -> Execute Python Script -> tools/meshes/Ukazka_Meshe.py

Kulatina (ROUND_MESHES) v radach podle upravy dreva slotu Wood (FINISHES), za ni rada ostatnich knihovnich meshi
(LIB_MESHES: kura, prouti a mazanina, lano, ovazani, ukazka plachty) s jejich zakladnim materialem. Vse podel X.
Actory maji tag Ukazka_Meshe, Outliner slozka Ukazka/Meshe. MODE = "clear" ukazku smaze. Level zriceniny ani stavby nemeni.
Meshe a textury naimportuje sam (stejne jako build) a chybejici materialy vytvori. Import a materialy se delaji MIMO
transakci: Undo (Ctrl+Z) vrati jen actory ukazky.
"""
MODE = "build"                              # "build" = postavit ukazku, "clear" = smazat
ORIGIN = (3600.0, -3400.0, 3500.0)          # cm, levy predni roh ukazky (posun podle potreby, napr. vedle Player Startu)
FINISHES = ["peeled", "raw", "tar"]         # uprava dreva slotu Wood kulatiny v radach (zrlib/config.py WOOD_FINISH)
TAG = "Ukazka_Meshe"
OLD_TAGS = ["Ukazka_Kulatina"]              # starsi ukazky se smazou taky

import os, sys


def _boot():
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    if root in sys.path: sys.path.remove(root)
    sys.path.insert(0, root)
    for k in [k for k in sys.modules if k.split(".")[0] == "zrlib"]: del sys.modules[k]
    return root


def run():
    import unreal
    root = _boot()
    from zrlib import ue_assets, ue_actors
    from zrlib.config import CUBE_MESH, LIB_MESHES, MESH_SRC, ROUND_MESHES, WOOD_FINISH
    from zrlib.stones import Stone
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    if MODE != "clear":
        mats = ue_assets.all_materials(unreal)
        meshes = ue_assets.ensure_stone_meshes(unreal, os.path.join(root, MESH_SRC))
        cube = unreal.load_asset(CUBE_MESH)
    with unreal.ScopedEditorTransaction("Ukazka meshi"):
        n_del = sum(ue_actors.destroy_tagged(eas, t) for t in [TAG] + OLD_TAGS)
        if MODE == "clear":
            unreal.log("Ukazka meshi: smazano %d actoru" % n_del); return
        n = 0; row_x = ORIGIN[0]
        def place(name, nom, cat, folder, bark, y):
            nonlocal n
            if name not in meshes: unreal.log_warning("Ukazka meshi: chybi mesh %s" % name); return
            s = Stone("ukazka|%s|%s" % (folder, name), cat, row_x + nom[0] / 2, y + nom[1] / 2, ORIGIN[2] + nom[2] / 2, 0.0,
                      nom[0], nom[1], nom[2], bark=bark)
            s.mesh = name
            act = ue_actors.spawn_loose(unreal, eas, s, cube, meshes, [TAG], "Ukazka/Meshe/" + folder, mats.get(cat))
            if act: act.set_actor_label("%s_%s" % (name, folder)); n += 1
        for fin in FINISHES:                                  # kulatina: rada na upravu dreva
            cat = WOOD_FINISH[fin]; y = ORIGIN[1]; row_len = 0.0
            for pref, (nom, vs, _sl) in ROUND_MESHES.items():
                for v in vs:
                    place("%s_%s" % (pref, v), nom, cat, "Kulatina_" + fin, "Bark" in pref, y)
                    y += nom[1] + 40.0; row_len = max(row_len, nom[0])
            row_x += row_len + 80.0
        y = ORIGIN[1]; row_len = 0.0                          # ostatni knihovni meshe
        for pref, (nom, vs, _cat, _sl, base) in LIB_MESHES.items():
            for v in vs:
                place("%s_%s" % (pref, v), nom, base, "Knihovna", False, y)
                y += nom[1] + 40.0; row_len = max(row_len, nom[0])
    unreal.log("Ukazka meshi: %d actoru (kulatina %s + knihovna), slozka Ukazka/Meshe, tag %s" % (n, ", ".join(FINISHES), TAG))


run()
