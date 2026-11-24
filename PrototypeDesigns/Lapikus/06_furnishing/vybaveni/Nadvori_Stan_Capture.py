"""Nadvori_Stan_Capture.py (06) - ulozi rucni upravy vybaveni stanu na nadvori (Nadvori_Stan_Vybaveni)
z levelu do ../furnishing.json (capture).
Unreal: Tools -> Execute Python Script -> 06_furnishing/vybaveni/Nadvori_Stan_Capture.py
Logika: ../build_furnishing.py (zrlib/pipeline.py). Postavit znovu: Nadvori_Stan.py.
entities: [Nadvori_Stan]
docs: [navrh_nadvori_stan, 06_furnishing]
build_step: 06_furnishing
domains: structures"""
SKUPINY = ["Nadvori_Stan_Vybaveni"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby", "furn_data")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.furnishing(SKUPINY, "capture")
