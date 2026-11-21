"""Guesthouse.py (06) - vybaveni pokoje hosta u ostrohu (Guesthouse): zatim GRAYBOX (kvadry, MI_PrototypeGrid_Gray): postel, pracovni
stul, stolicka, truhla, prazdne stojany na brneni a na zbrane, regal, hromadka dreva a zastupce pece (05, stavitel). Polohy: tools/ruin/ostroh_spec.py -> guesthouse_vybaveni().
Unreal: Tools -> Execute Python Script -> 06_furnishing/vybaveni/Guesthouse.py
Kusy jsou samostatne actory: posun / otoc / zvets (Scale) / smaz / duplikuj je v levelu a spust s MODE = "capture"
(nebo Guesthouse_Capture.py) - stav se zapise primo do ../furnishing.json a dalsi build ho zachova.
Logika: ../build_furnishing.py (pres zrlib/pipeline.py). Stavby u ostrohu (05): 05_constructions/stavby/Ostroh_*.py.
entities: [Guesthouse]
docs: [navrh_guesthouse_vybaveni, stav_guesthouse, 06_furnishing]
build_step: 06_furnishing
domains: structures"""
MODE = "build"                # "build" / "capture" (zapsat stav levelu do furnishing.json) / "list" (posuny proti specu) / "reset" (vratit na spec)
ITEMS = None                  # MODE reset: jen tyto kusy, napr. ["Postel"] (i jejich kopie); None = vsechny
SKUPINY = ["Guesthouse_Vybaveni"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.furnishing(SKUPINY, MODE, items=ITEMS)
