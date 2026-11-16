"""build_normal.py - postavi cely hrad (03_ruin) vsechny stavby (05_constructions) a vybaveni (06_furnishing) v jednom behu. Aditivni build.
Unreal: Tools -> Execute Python Script -> build_normal.py

Assety jen doplnuje: naimportuje chybejici nebo zastarale meshe a textury (verze v zrlib/config.py), chybejici
materialy vytvori, existujici necha (i s rucnim ladenim). Actory zriceniny a staveb smaze a postavi znovu podle dat
(ruin_layout.json, constructions.json, furnishing.json) a ulozenych rucnich uprav (manual_edits.json,
constructions_edits.json; polohy vybaveni z levelu jsou primo ve furnishing.json).
Totez co 03_ruin/blocks/build_ruin_blocks.py a po nem 05_constructions/build_constructions.py; jen cast hradu nebo
jednu stavbu stavi 03_ruin/blocks/casti/*.py a 05_constructions/stavby/*.py.
Kdyz jsou assety poskozene (NaN v bounds, InverseFast v logu, naruby, prazdne nahledy), pouzij build_fullscope.py.
Vybaveni (06): VYBAVENI = False ho vynecha; CAPTURE_VYBAVENI = True nejdriv ulozi rucni upravy vybaveni z levelu
(jako 06_furnishing/capture_furnishing.py) - jinak se neulozene posuny buildem ztrati.
Logika: zrlib/pipeline.py (build_all)."""
VYBAVENI = True               # True = postavit i vybaveni (06_furnishing, furnishing.json)
CAPTURE_VYBAVENI = False      # True = pred buildem ulozit rucni upravy vybaveni z levelu (jen kdyz se nemenily meshe props)

import os, sys
_root = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby", "furn_data")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.build_all(repair=False, vybaveni=VYBAVENI, capture_vybaveni=CAPTURE_VYBAVENI)
