"""Obvod.py - postavi jen tuto cast zriceniny: vez, obvodove hradby (Hradba_Z_S, Hradba_V), brany, dlazba veze.
Unreal: Tools -> Execute Python Script -> 03_ruin/blocks/casti/Obvod.py
Smaze a postavi jen actory teto casti (tag cast:Obvod), ostatni casti hradu zustanou, jak jsou.
Pocita se vzdy cely hrad (navaznosti zdi, teren z levelu), stavi se jen tato cast.
Logika je ve spolecnem ../build_ruin_blocks.py (spousti ho zrlib/pipeline.py), data v ../ruin_layout.json a ../manual_edits.json.
Rozdeleni zdi do casti: CASTI v build_ruin_blocks.py."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucne smazane / posunute bloky (vzdy cely hrad)
CAST = ["Obvod"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.ruin(CAST, MODE)
