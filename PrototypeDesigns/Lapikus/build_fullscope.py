"""build_fullscope.py - oprava: smaze vsechno generovane a postavi znovu cely hrad (03_ruin) i stavby (05_constructions).
Unreal: Tools -> Execute Python Script -> build_fullscope.py     (trva nekolik minut: import vsech meshi)

Oproti build_normal.py navic na zacatku:
  - smaze vsechny generovane actory (tagy Zricenina_Ruin, Zricenina_Stavby, ukazky Ukazka_Meshe),
  - smaze knihovni meshe SM_Ruin* (Ruin/Stones, Wood, Wattle, Textile, Props) a docasne slozky importu a testu,
  - textury naimportuje znovu a meshe vytvori jako nove assety (bez priznaku bDoFastBuild, viz zrlib/ue_assets.py),
  - s MATERIALY = True smaze i generovane materialy (M_Ruin*, MI_Ruin*, PM_Ruin*) a build je vytvori znovu
    s vychozim vzhledem z zrlib/config.py - rucni ladeni v nich se ztrati.
Rucni upravy levelu ulozene pres capture (manual_edits.json, constructions_edits.json) zustavaji a plati.
Co nesmaze: landscape, reku, les, objemy Ruin_* (Trigger Boxy) a nic mimo slozku Ruin.
Po behu nepouzivej Undo (Ctrl+Z): vratilo by actory s odkazy na smazane meshe.
Logika: zrlib/pipeline.py (build_all), zrlib/ue_assets.py (repair_assets)."""
MATERIALY = False             # True = smazat a znovu vytvorit i generovane materialy (rucni ladeni se ztrati)

import os, sys
_root = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [_root] + [p for p in sys.path if p != _root]
for _k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_ruin", "zr_stavby")]: del sys.modules[_k]
from zrlib import pipeline
pipeline.build_all(repair=True, reset_materials=MATERIALY)
