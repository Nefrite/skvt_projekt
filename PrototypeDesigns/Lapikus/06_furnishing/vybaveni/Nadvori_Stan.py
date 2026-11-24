"""Nadvori_Stan.py (06) - vybaveni stanu na nadvori (Nadvori_Stan_Vybaveni, etapa 1, sada site):
dve luzka (SM_RuinCampBed_A, SM_RuinCampBedFolded_A) podel boku uvnitr stanu, truhlicka (SM_RuinChestSmall_A),
vak (SM_RuinBundle_A) a spalek k sezeni (SM_RuinStump_A) pred vchodem.
Polohy: tools/ruin/nadvori_spec.py -> stan_vybaveni().
Unreal: Tools -> Execute Python Script -> 06_furnishing/vybaveni/Nadvori_Stan.py
Kusy jsou samostatne actory (s tagem stage:site pro Etapa.py): posun / otoc / smaz / duplikuj v levelu a spust
Nadvori_Stan_Capture.py - stav se zapise primo do ../furnishing.json.
Logika: ../build_furnishing.py (zrlib/pipeline.py). Stavba stanu (05): 05_constructions/stavby/Nadvori_Stan.py.
entities: [Nadvori_Stan]
docs: [navrh_nadvori_stan, 06_furnishing]
build_step: 06_furnishing
domains: structures"""
MODE = "build"                # "build" / "capture" / "list" / "reset"
ITEMS = None
SKUPINY = ["Nadvori_Stan_Vybaveni"]

import os, sys
_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.furnishing(SKUPINY, MODE, items=ITEMS)
