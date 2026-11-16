"""Palac_Kovarna.py (06) - vybaveni kovarny v palaci: kovadlina se spalky, kalici sud, hrebovnice, mechy s pakou a lany,
slapaci brus se stolickou, ponk, truhlik s vikem, kos, lista s naradim, pruty, hranice dreva.
Unreal: Tools -> Execute Python Script -> 06_furnishing/vybaveni/Palac_Kovarna.py
Kusy jsou samostatne actory: posun / otoc / zvets (Scale) / smaz / duplikuj je v levelu a spust s MODE = "capture" -
stav se zapise primo do ../furnishing.json a dalsi build (i po pregenerovani dat) ho zachova. Logika: ../build_furnishing.py (pres zrlib/pipeline.py).
Stavbu kovarny (05) stavi 05_constructions/stavby/Palac_Kovarna.py (umi postavit i toto vybaveni, VYBAVENI = True)."""
MODE = "build"                # "build" / "capture" (zapsat stav levelu do furnishing.json) / "list" (posuny proti specu) / "reset" (vratit na spec)
ITEMS = None                  # MODE reset: jen tyto kusy, napr. ["Kovadlina", "KaliciSud"] (i jejich kopie); None = vsechny
SKUPINY = ["Palac_Kovarna_Vybaveni"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.furnishing(SKUPINY, MODE, items=ITEMS)
