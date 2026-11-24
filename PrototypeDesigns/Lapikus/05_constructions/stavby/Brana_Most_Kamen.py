"""Brana_Most_Kamen.py - postavi jen vyrovnavaci zdivo koruny mostniho pilire Brana_Pilir a opery Brana_Opera (Z 3011 cm).
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Brana_Most_Kamen.py
entities: [Brana]
docs: [navrh_brana_prikop, stav_brana]
build_step: 05_constructions
domains: structures"""
MODE = "build"
STAVBA = ["Brana_Most_Kamen"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.constructions(STAVBA, MODE)
