"""Sut.py - postavi jen tuto stavbu (volna sut u zdi (fyzika)).
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Sut.py
Ostatni stavby se nesmazou ani neprestavi. Logika je ve spolecnem ../build_constructions.py, data v ../constructions.json."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy jen teto stavby, "freeze" = sut bez fyziky
STAVBA = ["Sut"]

import importlib.util, os, sys
_here = os.path.dirname(os.path.abspath(__file__))
sys._constr_import_only = True
try:
    _sp = importlib.util.spec_from_file_location("build_constructions", os.path.join(_here, "..", "build_constructions.py"))
    _B = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_B)
finally:
    sys._constr_import_only = False
_B.run(STAVBA, MODE)
