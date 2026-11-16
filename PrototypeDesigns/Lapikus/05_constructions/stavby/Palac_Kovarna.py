"""Palac_Kovarna.py - postavi celou kovarnu ve vychodni mistnosti palace najednou: pristresek (s krytinou), vyhen, stenu
z prouti, okap se sudem a vybaveni; volitelne i cast zriceniny Palac (03) a sut.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Palac_Kovarna.py
Kod se neduplikuje: seznam staveb je jen tady, stavi je stejna logika jako jednotlive spoustece Palac_Kovarna_*.py
(zrlib/pipeline.py -> ../build_constructions.py). Jednu cast kovarny staci postavit jejim vlastnim spoustecem.
Ostatni stavby (dum, ostroh, vez) se nesmazou ani neprestavi."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy vsech casti kovarny (nejdriv, pred dalsim buildem)
KRYTINA = True                # False = pristresek jen jako kostra (sloupy, pozednice, krokve)
RUIN = False                  # True = nejdriv prestavet cast zriceniny Palac (03: zanorena Palac_J, kapsa, rozebrana koruna u veze);
                              # potreba jen po zmene palac_spec.py J_* / kapsy, jinak zbytecne (dlouhe)
SUT = True                    # True = prestavet i volnou sut (ve vychodni mistnosti uklizena); sut se stavi pro cely hrad
STAVBY = ["Palac_Kovarna_Pristresek",   # kostra a krytina (vyhen, okap a vybaveni z ni berou vysky)
          "Palac_Kovarna_Vyhen",        # vymeny u komina mezi krokvemi
          "Palac_Kovarna_Stena",
          "Palac_Kovarna_Okap",         # zlab pod okapovou hranou krytiny
          "Palac_Kovarna_Vybaveni"]     # samostatne actory (rucni doladeni pres MODE = "capture")

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
if RUIN and MODE == "build": pipeline.ruin(["Palac"], MODE)
pipeline.constructions(STAVBY + (["Sut"] if SUT and MODE != "capture" else []), MODE, ROOF_COVER=KRYTINA)
