"""Vez.py - postavi vsechny stavby ve vezi najednou (drevo v patrech, platenny pristresek hlidky ve 2. patre); volitelne
i cast zriceniny Obvod (03: vez se skodami z dobyvani) a sut.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Vez.py
Kod se neduplikuje: seznam staveb je jen tady, stavi je stejna logika jako jednotlive spoustece (zrlib/pipeline.py ->
../build_constructions.py). Ostatni stavby se nesmazou ani neprestavi."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy vsech staveb ve vezi
RUIN = False                  # True = nejdriv prestavet cast zriceniny Obvod (03: prulomy Vez_V, Vez_J, koruny Vez_S, Vez_Z);
                              # potreba po zmene tools/ruin/tower_spec.ruin_edits, jinak zbytecne (dlouhe)
SUT = False                   # True = prestavet i volnou sut (stavi se pro cely hrad)
STAVBY = ["Vez_Patra",                  # tramy, prkna, pruvlak, schody, ochoz
          "Vez_Pristresek"]             # platenny pristresek hlidky (stoji na prknech 2. patra a na korune Vez_J)

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
if RUIN and MODE == "build": pipeline.ruin(["Obvod"], MODE)
pipeline.constructions(STAVBY + (["Sut"] if SUT and MODE != "capture" else []), MODE)
