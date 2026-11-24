"""Nadvori_Stan_Capture.py - ulozi rucni posun / natoceni stanu na nadvori (Nadvori_Stan, pile=True) z levelu
do ../constructions_edits.json. Pustit po posunuti stanu v UE a pred dalsim buildem.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Nadvori_Stan_Capture.py
Ostatni stavby se nesmazou ani neprestavi. Logika: ../build_constructions.py (zrlib/pipeline.py).
entities: [Nadvori_Stan]
docs: [navrh_nadvori_stan, 05_constructions]
build_step: 05_constructions
domains: structures"""
MODE = "capture"
STAVBA = ["Nadvori_Stan"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.constructions(STAVBA, MODE)
