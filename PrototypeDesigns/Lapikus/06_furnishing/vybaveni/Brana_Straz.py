"""Brana_Straz.py (06) - vybaveni strazniho stanoviste nad branami (Brana_Straz_Vybaveni): v 1. navrhu vse GRAYBOX
(kvadry, MI_PrototypeGrid_Gray): stolicka, prevracena bedna, sada nastroju na vyrobu sipu na bedne, toulec u bedny,
pohotovostni toulec a luk u SZ sloupku strisky + 4 docasni zastupci sloupku strisky z kury (05).
Polohy: tools/ruin/brana_spec.py -> brana_straz_vybaveni().
Unreal: Tools -> Execute Python Script -> 06_furnishing/vybaveni/Brana_Straz.py
Kusy jsou samostatne actory: posun / otoc / zvets (Scale) / smaz / duplikuj je v levelu a spust s MODE = "capture"
(nebo Brana_Straz_Capture.py) - stav se zapise primo do ../furnishing.json a dalsi build ho zachova.
Logika: ../build_furnishing.py (pres zrlib/pipeline.py). Stavby brany (05): 05_constructions/stavby/Brana_Straz.py.
entities: [Brana_Straz]
docs: [navrh_brana_straz, stav_brana_straz, 06_furnishing]
build_step: 06_furnishing
domains: structures"""
MODE = "build"                # "build" / "capture" (zapsat stav levelu do furnishing.json) / "list" (posuny proti specu) / "reset" (vratit na spec)
ITEMS = None                  # MODE reset: jen tyto kusy, napr. ["Stolicka"] (i jejich kopie); None = vsechny
SKUPINY = ["Brana_Straz_Vybaveni"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.furnishing(SKUPINY, MODE, items=ITEMS)
