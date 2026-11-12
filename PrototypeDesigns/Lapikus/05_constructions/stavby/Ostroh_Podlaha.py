"""Ostroh_Podlaha.py - postavi jen tuto stavbu (prkenna podlaha v obytne casti u ostrohu: dehtovane podvaly na zemi,
prkna bez upravy podel ZBudova_V, vyriznuta kolem sloupu krovu a kamenu zriceniny). Zricenina se nemeni.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Ostroh_Podlaha.py
Ostatni stavby se nesmazou ani neprestavi. Logika je ve spolecnem ../build_constructions.py, data v ../constructions.json."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy jen teto stavby
STAVBA = ["Ostroh_Podlaha"]

import importlib.util, os, sys
_here = os.path.dirname(os.path.abspath(__file__))
sys._constr_import_only = True
try:
    _sp = importlib.util.spec_from_file_location("build_constructions", os.path.join(_here, "..", "build_constructions.py"))
    _B = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_B)
finally:
    sys._constr_import_only = False
_B.run(STAVBA, MODE)
