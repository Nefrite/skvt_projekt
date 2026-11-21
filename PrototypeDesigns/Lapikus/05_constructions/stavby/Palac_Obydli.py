"""Palac_Obydli.py - postavi cely dum posadky v prostredni mistnosti palace najednou (zatim kamenne casti, zaklad
ohniste, krov bez krytiny, srub a staveniste; dalsi stavby pribudou do seznamu STAVBY, jak budou hotove); volitelne i sut.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Palac_Obydli.py
Kod se neduplikuje: seznam staveb je jen tady, stavi je stejna logika jako jednotlive spoustece Palac_Obydli_*.py
(zrlib/pipeline.py -> ../build_constructions.py). Jednu cast domu staci postavit jejim vlastnim spoustecem.
Ostatni stavby (kovarna, ostroh, vez) se nesmazou ani neprestavi.
Etapy: stavi se vzdy vsechny sady actoru (tagy stage:base, stage:final, stage:site; zrlib/config.py STAGES). Prepnuti
etapy ve hre = zobrazit / skryt actory podle tagu: etapa 1 = base + site, etapa 2 = base + final.
Zricenina se kvuli domu nemeni (cast Palac prestavuje jen kovarna: Palac_Kovarna.py, RUIN = True)."""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy vsech casti domu (nejdriv, pred dalsim buildem)
SUT = True                    # True = prestavet i volnou sut (v dome a na zaprazi uklizena); sut se stavi pro cely hrad
STAVBY = ["Palac_Obydli_Kamen",         # srovnani pricek, podezdivky (base)
          "Palac_Obydli_Krov",          # sloupy, pozednice, vaznice, krokve bez krytiny (nad svetnici base, nad sini final)
          "Palac_Obydli_Ohniste",       # kamenny zaklad ohniste (base); dymnik a komin (final) prijdou s krytinou
          "Palac_Obydli_Srub",          # srubove steny (svetnice base, sin 3 rady base + zbytek final), prkenne stity (final)
          "Palac_Obydli_Stavenisko",    # staveniste (site): vzpery, zebrik; vysky z krovu a srubu
          "Palac_Obydli_Stavenisko_Kulatina", "Palac_Obydli_Stavenisko_Tramy", "Palac_Obydli_Stavenisko_Prkna",
          "Palac_Obydli_Stavenisko_Kozy"]   # hranice a kozy na nadvori (site)
# dalsi v poradi stavby (navrh_palac_obydli_stred.md kap. 0.4): krytina, _Strop, _Podlaha, _Okap, _Vybaveni

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.constructions(STAVBY + (["Sut"] if SUT and MODE != "capture" else []), MODE)
