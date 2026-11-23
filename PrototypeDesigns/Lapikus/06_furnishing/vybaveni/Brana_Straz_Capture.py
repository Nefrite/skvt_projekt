"""Brana_Straz_Capture.py (06) - ulozi rucni upravy vybaveni strazniho stanoviste nad branami (Brana_Straz_Vybaveni)
z levelu do ../furnishing.json (capture).
Unreal: Tools -> Execute Python Script -> 06_furnishing/vybaveni/Brana_Straz_Capture.py
Pred spustenim: kusy v levelu posun, otoc, zmen jim Scale, smaz nebo zkopiruj (Alt+tah, Ctrl+D). Skript zapise polohy,
otoceni a velikosti (v ramu brany), smazane kusy (removed) a kopie (novy kus <id>_2, manual); predchozi verze dat ->
furnishing.json.bak. Na konci vypise posuny proti specu (jako MODE = "list").
Jen po buildu se stejnymi meshi (KNOWHOW_hrad.md kap. 5.3). Postavit znovu: Brana_Straz.py (MODE = "build").
entities: [Brana_Straz]
docs: [navrh_brana_straz, stav_brana_straz, 06_furnishing]
build_step: 06_furnishing
domains: structures"""
SKUPINY = ["Brana_Straz_Vybaveni"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby", "furn_data")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.furnishing(SKUPINY, "capture")
