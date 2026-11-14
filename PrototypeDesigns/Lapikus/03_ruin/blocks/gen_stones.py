"""gen_stones.py - PRESUNUTO do tools/meshes/gen_meshes.py (kameny: mesh_stone.py, drevo: mesh_wood.py).

Zustava kvuli starym navodum, vola novy generator:

    python gen_stones.py [vystupni slozka]     (potrebuje numpy; bez slozky meshes/ v koreni, OBJ v podslozkach stone/, wood/)
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "tools", "meshes")))
import gen_meshes          # noqa: E402

if __name__ == "__main__":
    gen_meshes.main(sys.argv[1] if len(sys.argv) > 1 else None, ["stone", "wood"])
