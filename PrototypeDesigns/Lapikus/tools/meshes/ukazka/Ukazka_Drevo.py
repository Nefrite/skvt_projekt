"""Ukazka_Drevo.py - v UE ukazka knihovnich meshi tematu "drevo" (seznam meshi: UKAZKY v tools/meshes/ukazka.py).
Unreal: Tools -> Execute Python Script -> tools/meshes/ukazka/Ukazka_Drevo.py
Naimportuje jen meshe tematu, postavi je do pasu tematu (tag Ukazka_Meshe_drevo, Outliner Ukazka/Meshe). MODE = "clear" smaze jen toto tema.
"""
MODE = "build"                              # "build" = postavit ukazku, "clear" = smazat
TEMA = "drevo"

import os, sys
_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
if _dir not in sys.path: sys.path.insert(0, _dir)
sys.modules.pop("ukazka", None)
import ukazka                               # noqa: E402
ukazka.run([TEMA], MODE)
