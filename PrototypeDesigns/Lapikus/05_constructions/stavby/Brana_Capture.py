"""Brana_Capture.py - ulozi rucni upravy premosteni a zatarasu pred vychodni branou z levelu do constructions_edits.json
(zejmena posun a natoceni celeho actoru Brana_Zataras kolem svisle osy). Pustit v UE po posunuti a pred dalsim buildem.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Brana_Capture.py
entities: [Brana]
docs: [navrh_brana_prikop, stav_brana]
build_step: 05_constructions
domains: structures"""
MODE = "capture"
STAVBY = ["Brana_Most_Kamen",
          "Brana_Most",
          "Brana_Zataras"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.constructions(STAVBY, MODE)
