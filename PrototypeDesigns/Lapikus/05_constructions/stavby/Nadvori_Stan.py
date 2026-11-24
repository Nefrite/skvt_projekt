"""Nadvori_Stan.py - postavi jen stan na nadvori (etapa 1, sada site, typ tent): stojky, hreben, ovazani,
plachta SM_RuinCanvasTent_A, 13 obvodovych koliku, 6 napinacich snur s kotvicimi koliky.
Stavba ma pile=True (jeden actor s pivotem dole uprostred): v UE lze cely stan posunout nebo otocit kolem svisle osy
a ulozit polohu pres Nadvori_Stan_Capture.py.
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Nadvori_Stan.py
Ostatni stavby se nesmazou ani neprestavi. Logika: ../build_constructions.py (zrlib/pipeline.py), data: ../constructions.json.
Rozmery: tools/ruin/nadvori_spec.py -> stan(). Vybaveni stanu (06): 06_furnishing/vybaveni/Nadvori_Stan.py.
Kontrola: tools/checks/run_checks.py --only stan; prepnuti etapy: Etapa.py.
entities: [Nadvori_Stan]
docs: [navrh_nadvori_stan, 05_constructions]
build_step: 05_constructions
domains: structures"""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni posun stanu do constructions_edits.json
STAVBA = ["Nadvori_Stan"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.constructions(STAVBA, MODE)
