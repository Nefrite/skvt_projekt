"""Brana.py - postavi premosteni sijoveho prikopu a zataras pred vychodni branou najednou:
vyrovnani koruny pilire a opery (Brana_Most_Kamen), drevenou mostni lavku (Brana_Most) a spanelskeho jezdce
na predmosti (Brana_Zataras, jeden actor s pivotem dole uprostred); volitelne i cast zriceniny Obvod (03) a sut.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Brana.py
Ulozeni rucniho posunu/natoceni zatarasu v UE: Brana_Capture.py.
entities: [Brana]
docs: [navrh_brana_prikop, stav_brana]
build_step: 05_constructions
domains: structures"""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy (viz Brana_Capture.py)
RUIN = False                  # True = nejdriv prestavet cast zriceniny Obvod (03: Brana_Pilir, Brana_Opera, ozub v Brana_V)
SUT = False                   # True = prestavet i volnou sut (stavi se pro cely hrad, uklidi predmosti)
STAVBY = ["Brana_Most_Kamen",           # vyrovnani koruny Brana_Pilir a Brana_Opera na Z 3011 cm (base)
          "Brana_Most",                 # drevena mostni lavka pres 2 pole prikopu, vrch Z 3040 cm (base)
          "Brana_Zataras"]              # spanelsky jezdec na predmosti jako jeden actor (base, pile)

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
if RUIN and MODE == "build": pipeline.ruin(["Obvod"], MODE)
pipeline.constructions(STAVBY + (["Sut"] if SUT and MODE != "capture" else []), MODE)
