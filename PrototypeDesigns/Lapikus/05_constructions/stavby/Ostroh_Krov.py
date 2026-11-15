"""Ostroh_Krov.py - postavi jen tuto stavbu (krov u ostrohu: sloupy, pricka, paprskovite tramy, krytina).
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Ostroh_Krov.py
Ostatni stavby se nesmazou ani neprestavi. Logika je ve spolecnem ../build_constructions.py (spousti ho zrlib/pipeline.py), data v ../constructions.json."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy jen teto stavby
STAVBA = ["Ostroh_Krov"]
KRYTINA = False               # False = jen sloupy, pricka a tramy (ladeni tramovi a dostavby); True = i late, prkna, listy a hreben

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.constructions(STAVBA, MODE, ROOF_COVER=KRYTINA)
