"""Brana_Straz.py - postavi cele strazni stanoviste nad branami najednou (zatim vyrovnani koruny Brana_J, podesta a
vychodni kryt z kulatiny; dalsi kryty, pristresek z kury a zataras pribudou do seznamu STAVBY, jak budou hotove); volitelne i cast
zriceniny Obvod (03) a sut.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Brana_Straz.py
Kod se neduplikuje: seznam staveb je jen tady, stavi je stejna logika jako jednotlive spoustece Brana_Straz_*.py
(zrlib/pipeline.py -> ../build_constructions.py). Ostatni stavby se nesmazou ani neprestavi.
Etapy: stavi se vzdy vsechny sady actoru (tagy stage:base / stage:final / stage:site); prepnuti v editoru: Etapa.py."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy vsech casti stanoviste
RUIN = False                  # True = nejdriv prestavet cast zriceniny Obvod (03: kapsy pro tramy podesty v Brana_V);
                              # potreba po zmene tools/ruin/brana_spec.py (B_BEAM_Z, B_BEAM, B_POCKET), jinak zbytecne (dlouhe)
SUT = False                   # True = prestavet i volnou sut (stavi se pro cely hrad)
VYBAVENI = True               # True = nakonec postavit (capture: ulozit) i vybaveni stanoviste (06_furnishing/vybaveni/Brana_Straz.py)
STAVBY = ["Brana_Straz_Kamen",          # vyrovnani koruny Brana_J pod tramy (base)
          "Brana_Straz_Podesta",        # tramy a prkna (base); zabradli do hradu se nestavi
          "Brana_Straz_Kryty"]          # vychodni kryt z kulatiny na korune Brana_V (base)
# dalsi v poradi (navrh_brana_straz.md kap. 0): severni a jizni kryt, Brana_Straz_Pristresek, Brana_Zataras

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
if RUIN and MODE == "build": pipeline.ruin(["Obvod"], MODE)
pipeline.constructions(STAVBY + (["Sut"] if SUT and MODE != "capture" else []), MODE)
if VYBAVENI and MODE in ("build", "capture"): pipeline.furnishing(["Brana_Straz_Vybaveni"], MODE)
