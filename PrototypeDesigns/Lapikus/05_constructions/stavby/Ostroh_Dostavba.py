"""Ostroh_Dostavba.py - postavi jen tuto stavbu (kamenna dostavba u ostrohu: jednoradove zdi na korunach zriceniny az pod strechu,
dvere v pruchodu ZBudova_V, okno severne od nich, drevena nadprazi). Vysku bere z krovu (Ostroh_Krov), zricenina se nemeni.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Ostroh_Dostavba.py
Ostatni stavby se nesmazou ani neprestavi. Logika je ve spolecnem ../build_constructions.py (spousti ho zrlib/pipeline.py), data v ../constructions.json."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy jen teto stavby
STAVBA = ["Ostroh_Dostavba"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.constructions(STAVBA, MODE)
