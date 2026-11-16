"""capture_furnishing.py - ulozi rucni upravy VSEHO vybaveni (vsechny skupiny ve furnishing.json) z levelu do
furnishing.json: posun, otoceni, Scale, smazane kusy (removed), kopie actoru (novy kus <id>_2, manual); zaloha
furnishing.json.bak. Skupina, ktera v levelu nema zadny actor, se preskoci. Na konci vypise posuny proti specu.
Unreal: Tools -> Execute Python Script -> 06_furnishing/capture_furnishing.py
Jedna skupina: vybaveni/<Skupina>_Capture.py. Postavit vse znovu: build_furnishing.py.
Jen po buildu se stejnymi meshi (KNOWHOW_hrad.md kap. 5.3). Logika: build_furnishing.py (pres zrlib/pipeline.py)."""
import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby", "furn_data")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.furnishing(None, "capture")
