"""Ukazka_Kulatina.py - v UE postavi ukazku vsech meshi kulatiny s materialy (kontrola tvaru, slotu, textur).
Unreal: Tools -> Execute Python Script -> tools/meshes/Ukazka_Kulatina.py
Undo (Ctrl+Z) vrati jen actory ukazky; import meshi, textur a materialy se delaji mimo transakci (jako v buildech).

Rady podle upravy dreva slotu Wood (FINISHES), sloupce = meshe a varianty, vse lezi podel X. Actory maji tag
Ukazka_Kulatina, Outliner slozka Ukazka/Kulatina. MODE = "clear" ukazku smaze. Level zriceniny ani stavby nemeni.
Meshe a textury naimportuje sam (stejne jako build), materialy MI_RuinBark, MI_RuinWood_EndGrain, MI_RuinWood_Peeled vytvori.
"""
MODE = "build"                              # "build" = postavit ukazku, "clear" = smazat
ORIGIN = (3600.0, -3400.0, 3500.0)          # cm, levy predni roh ukazky (posun podle potreby, napr. vedle Player Startu)
FINISHES = ["peeled", "raw", "tar"]         # uprava dreva slotu Wood v radach (zrlib/config.py WOOD_FINISH)
TAG = "Ukazka_Kulatina"

import importlib, os, sys


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
    from zrlib.config import CUBE_MESH, MESH_SRC, ROUND_MESHES, WOOD_FINISH
    from zrlib.stones import Stone
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    if MODE != "clear":
        # assety (import meshi a textur, materialy) MIMO transakci: Undo ma vratit jen actory ukazky.
        # Undo uprav cerstve naimportovanych meshi (kolize, Nanite) a jejich nasledny preimport shodil editor.
        mats = ue_assets.all_materials(unreal)
        meshes = ue_assets.ensure_stone_meshes(unreal, os.path.join(root, MESH_SRC))
        cube = unreal.load_asset(CUBE_MESH)
    with unreal.ScopedEditorTransaction("Ukazka kulatiny"):
        n_del = ue_actors.destroy_tagged(eas, TAG)
        if MODE == "clear":
            unreal.log("Ukazka kulatiny: smazano %d actoru" % n_del); return
        n = 0; row_x = ORIGIN[0]
        for fin in FINISHES:
            cat = WOOD_FINISH[fin]; y = ORIGIN[1]; row_len = 0.0
            for pref, (nom, vs) in ROUND_MESHES.items():
                for v in vs:
                    name = "%s_%s" % (pref, v)
                    if name not in meshes: unreal.log_warning("Ukazka kulatiny: chybi mesh %s" % name); continue
                    s = Stone("ukazka|%s|%s" % (fin, name), cat, row_x + nom[0] / 2, y + nom[1] / 2, ORIGIN[2] + nom[2] / 2, 0.0,
                              nom[0], nom[1], nom[2], bark="Bark" in pref)
                    s.mesh = name
                    act = ue_actors.spawn_loose(unreal, eas, s, cube, meshes, [TAG], "Ukazka/Kulatina/" + fin, mats.get(cat))
                    if act: act.set_actor_label("%s_%s" % (name, fin)); n += 1
                    y += nom[1] + 40.0; row_len = max(row_len, nom[0])
            row_x += row_len + 80.0
    unreal.log("Ukazka kulatiny: %d actoru (%s), slozka Ukazka/Kulatina, tag %s" % (n, ", ".join(FINISHES), TAG))


run()
