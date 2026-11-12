"""Ostroh_Dostavba.py - postavi jen tuto stavbu (kamenna dostavba u ostrohu: jednoradove zdi na korunach zriceniny az pod strechu,
dvere v pruchodu ZBudova_V, okno severne od nich, drevena nadprazi). Vysku bere z krovu (Ostroh_Krov), zricenina se nemeni.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Ostroh_Dostavba.py
Ostatni stavby se nesmazou ani neprestavi. Logika je ve spolecnem ../build_constructions.py, data v ../constructions.json."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy jen teto stavby
STAVBA = ["Ostroh_Dostavba"]

import importlib.util, os, sys
_here = os.path.dirname(os.path.abspath(__file__))
sys._constr_import_only = True
try:
    _sp = importlib.util.spec_from_file_location("build_constructions", os.path.join(_here, "..", "build_constructions.py"))
    _B = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_B)
finally:
    sys._constr_import_only = False
_B.run(STAVBA, MODE)
