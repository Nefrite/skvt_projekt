"""Obvod.py - postavi jen tuto cast zriceniny: vez, obvodove hradby (Hradba_Z_S, Hradba_V), brany, dlazba veze.
Unreal: Tools -> Execute Python Script -> 03_ruin/blocks/casti/Obvod.py
Smaze a postavi jen actory teto casti (tag cast:Obvod), ostatni casti hradu zustanou, jak jsou.
Pocita se vzdy cely hrad (navaznosti zdi, teren z levelu), stavi se jen tato cast.
Logika je ve spolecnem ../build_ruin_blocks.py, data v ../ruin_layout.json a ../manual_edits.json.
Rozdeleni zdi do casti: CASTI v build_ruin_blocks.py."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucne smazane / posunute bloky (vzdy cely hrad)
CAST = ["Obvod"]

import importlib.util, os, sys
_here = os.path.dirname(os.path.abspath(__file__))
sys._ruin_import_only = True
try:
    _sp = importlib.util.spec_from_file_location("build_ruin_blocks", os.path.join(_here, "..", "build_ruin_blocks.py"))
    _R = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_R)
finally:
    sys._ruin_import_only = False
_R.run(CAST, MODE)
