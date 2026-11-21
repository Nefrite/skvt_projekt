"""Palac_Obydli_Stavenisko.py - postavi jen staveniste domu posadky (etapa 1, sada site): vzpery a zebrik a tri hranice
materialu na nadvori (kulatina, tramy, prkna, kozy s rozpracovanou kulatinou), kazda jako samostatna stavba = jeden actor (pivot dole uprostred): v UE ji
posunes nebo natocis kolem svisle osy jako celek a ulozis pres Palac_Obydli_Stavenisko_Capture.py (naklon se neuklada).
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Palac_Obydli_Stavenisko.py
Ostatni stavby se nesmazou ani neprestavi. Logika je ve spolecnem ../build_constructions.py (spousti ho zrlib/pipeline.py), data v ../constructions.json.
Rozmery: tools/ruin/palac_spec.py -> D_SITE, obydli_stavenisko (delky a pocty kusu v hranicich z dat sady final).
Kontrola: tools/checks/run_checks.py --only obydli (kontroly etapy 1); prepnuti etapy: Etapa.py.
entities: [Palac_Obydli]
docs: [navrh_palac_obydli_stred, stav_palac_obydli]
build_step: 05_constructions
domains: structures"""
MODE = "build"                # "build" = postavit, "capture" = ulozit rucni upravy jen teto stavby
STAVBA = ["Palac_Obydli_Stavenisko",            # vzpery V1-V4, zebrik (uklid suti pod hranicemi)
          "Palac_Obydli_Stavenisko_Kulatina",   # S3 srubova kulatina sine
          "Palac_Obydli_Stavenisko_Tramy",      # S4 krokve, pozednice, vaznice
          "Palac_Obydli_Stavenisko_Prkna",      # S5 prkna krytiny (jedna vyssi hranice, D_SITE boards.variant)
          "Palac_Obydli_Stavenisko_Kozy"]       # S6 kozy s rozpracovanou kulatinou (castecne oloupana, SM_RuinLogPeeling)

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.constructions(STAVBA, MODE)
