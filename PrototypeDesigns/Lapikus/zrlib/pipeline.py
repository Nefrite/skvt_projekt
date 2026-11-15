"""Spolecne spousteni buildu v Unrealu: nacteni skriptu 03 / 05 jako knihoven, build casti a staveb (spoustece
casti/*.py, stavby/*.py), build vseho (build_normal.py) a oprava (build_fullscope.py).

Jedna sada modulu na beh: vstupni skript (spoustec) na zacatku zahodi moduly z minuleho behu (Python v Unrealu si je
drzi v pameti, po uprave souboru by bezel stary kod) a vsechno dalsi se nacita pres load_script, ktery uz nic
nezahazuje. zrlib tak existuje v jedne kopii a jeji stav (ue_assets.SLOT_MATS, _OBJ_BOX, _FIX) vidi 03 i 05 stejne.
Zacatek spoustece (cesta ke koreni podle polohy souboru):
    import os, sys
    _root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    sys.path[:] = [_root] + [p for p in sys.path if p != _root]
    for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
    from zrlib import pipeline
"""
import importlib.util, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # koren (vedle zrlib: 03_ruin, 05_constructions, meshes)
RUIN_DIR = os.path.join(ROOT, "03_ruin", "blocks")
CONSTR_DIR = os.path.join(ROOT, "05_constructions")
SHOW_TAGS = ("Ukazka_Meshe", "Ukazka_Kulatina")          # actory ukazek (tools/meshes/Ukazka_Meshe.py): fullscope je smaze taky


def load_script(path, name, flag):
    """nacte skript jako knihovnu: flag (sys._ruin_import_only / sys._constr_import_only) = nic nestavet,
    sys._zr_keep = nezahazovat nactene moduly (zustane jedna kopie zrlib)"""
    keep = getattr(sys, "_zr_keep", False)
    setattr(sys, flag, True); sys._zr_keep = True
    try:
        sp = importlib.util.spec_from_file_location(name, path)
        m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    finally:
        setattr(sys, flag, False); sys._zr_keep = keep
    return m


def load_ruin(ruin_dir=None):
    """generator zriceniny (03_ruin/blocks/build_ruin_blocks.py) jako knihovna"""
    d = ruin_dir or RUIN_DIR
    R = load_script(os.path.join(d, "build_ruin_blocks.py"), "build_ruin_blocks", "_ruin_import_only")
    R.LAYOUT_PATH = os.path.join(d, "ruin_layout.json")
    return R


def load_constructions():
    """stavby (05_constructions/build_constructions.py) jako knihovna"""
    return load_script(os.path.join(CONSTR_DIR, "build_constructions.py"), "build_constructions", "_constr_import_only")


def ruin(cast=None, mode="build"):
    """03: cast = seznam casti hradu (CASTI v build_ruin_blocks.py) nebo None = cely hrad; mode "build" / "capture" """
    R = load_ruin(); R.run(cast, mode)
    return R


def constructions(only=None, mode="build", **opts):
    """05: only = seznam staveb (constructions.json, + "Sut") nebo None = vsechny; mode "build" / "capture" / "freeze";
    opts = prepis nastaveni behu build_constructions.py (napr. ROOF_COVER=False)"""
    B = load_constructions()
    for k, v in opts.items():
        if not hasattr(B, k): raise RuntimeError("build_constructions.py nema nastaveni %s" % k)
        setattr(B, k, v)
    B.run(only, mode)
    return B


def clear_level(unreal):
    """smaze vsechny generovane actory (zricenina, stavby, ukazky). Bez transakce: Undo by vratilo actory s odkazy
    na meshe, ktere se vzapeti mazou."""
    from .config import RUIN_TAG, CONSTR_TAG
    from . import ue_actors
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    return sum(ue_actors.destroy_tagged(eas, unreal.Name(t)) for t in (RUIN_TAG, CONSTR_TAG) + SHOW_TAGS)


def build_all(repair=False, reset_materials=False):
    """Postavi cely hrad (03) a vsechny stavby (05) v jednom behu.
    repair=False (build_normal.py): aditivni - doimportuje jen chybejici nebo zastarale meshe a textury, materialy
        necha, actory zriceniny a staveb postavi znovu podle dat a ulozenych rucnich uprav.
    repair=True (build_fullscope.py): oprava - nejdriv smaze vsechny generovane actory a knihovni meshe (+ docasne
        slozky importu a testu), textury naimportuje znovu a meshe vytvori jako nove assety; pak stavi stejne jako normal.
        reset_materials=True smaze i generovane materialy (M_Ruin*, MI_Ruin*, PM_Ruin*) - rucni ladeni v nich se ztrati.
    Rucni upravy (manual_edits.json, constructions_edits.json) plati v obou rezimech."""
    import unreal
    from . import ue_assets
    from .config import MESH_SRC
    if repair:
        n_act = clear_level(unreal)
        rep = ue_assets.repair_assets(unreal, os.path.join(ROOT, MESH_SRC), reset_materials)
        unreal.log("Fullscope: smazano %d actoru, %d meshu%s; textury a meshe naimportovany znovu (%d meshu)." % (
            n_act, rep["deleted_meshes"], ", %d materialu" % rep["deleted_materials"] if reset_materials else "", rep["meshes"]))
    ruin(None, "build")
    constructions(None, "build")
    unreal.log("Build %s hotov: zricenina (03) + stavby (05).%s" % (
        "fullscope" if repair else "normal", " Undo (Ctrl+Z) po fullscope nepouzivej - vratilo by actory se smazanymi meshi." if repair else ""))
