"""Brana_Zataras.py - postavi jen spanelskeho jezdce na predmosti brany (jeden actor s pivotem dole uprostred v u=17.20, d=3.10, Z=3040 cm).
V UE ho lze posunout/natocit jako celek a ulozit pres Brana_Capture.py (nebo zmenou MODE = "capture" tady).
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Brana_Zataras.py
entities: [Brana]
docs: [navrh_brana_prikop, stav_brana]
build_step: 05_constructions
domains: structures"""
MODE = "build"
STAVBA = ["Brana_Zataras"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.constructions(STAVBA, MODE)
