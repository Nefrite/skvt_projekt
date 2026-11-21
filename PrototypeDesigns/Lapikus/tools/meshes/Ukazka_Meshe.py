"""Ukazka_Meshe.py - v UE postavi ukazku VSECH knihovnich meshi s materialy (vsechna temata z tools/meshes/ukazka.py).
Unreal: Tools -> Execute Python Script -> tools/meshes/Ukazka_Meshe.py

Jednotliva temata (rychlejsi, importuje jen sve meshe): tools/meshes/ukazka/Ukazka_<Tema>.py.
Kazde tema ma svuj pas v Y od ORIGIN (ukazka.py), tag Ukazka_Meshe_<tema> a slozku Outlineru Ukazka/Meshe/<rada>.
Meshe z LIB_MESHES mimo temata jsou v pasu "ostatni". MODE = "clear" ukazku smaze (i starsi ukazky Ukazka_Meshe
a Ukazka_Kulatina). Import a materialy se delaji MIMO transakci: Undo (Ctrl+Z) vrati jen actory ukazky.
"""
MODE = "build"                              # "build" = postavit ukazku, "clear" = smazat

import os, sys
_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path: sys.path.insert(0, _dir)
sys.modules.pop("ukazka", None)
import ukazka                               # noqa: E402
ukazka.run(ukazka.PASY, MODE)
