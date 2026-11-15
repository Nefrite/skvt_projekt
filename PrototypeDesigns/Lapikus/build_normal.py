"""build_normal.py - postavi cely hrad (03_ruin) a vsechny stavby (05_constructions) v jednom behu. Aditivni build.
Unreal: Tools -> Execute Python Script -> build_normal.py

Assety jen doplnuje: naimportuje chybejici nebo zastarale meshe a textury (verze v zrlib/config.py), chybejici
materialy vytvori, existujici necha (i s rucnim ladenim). Actory zriceniny a staveb smaze a postavi znovu podle dat
(ruin_layout.json, constructions.json) a ulozenych rucnich uprav (manual_edits.json, constructions_edits.json).
Totez co 03_ruin/blocks/build_ruin_blocks.py a po nem 05_constructions/build_constructions.py; jen cast hradu nebo
jednu stavbu stavi 03_ruin/blocks/casti/*.py a 05_constructions/stavby/*.py.
Kdyz jsou assety poskozene (NaN v bounds, InverseFast v logu, naruby, prazdne nahledy), pouzij build_fullscope.py.
Logika: zrlib/pipeline.py (build_all)."""
import os, sys
_root = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.build_all(repair=False)
