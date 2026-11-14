"""gen_meshes.py - generator knihovnich meshi zriceniny a dostaveb (OBJ, cm, Z nahoru). Potrebuje numpy.

    python tools/meshes/gen_meshes.py [vystupni slozka] [kategorie ...]

Kazda kategorie se zapise do <vystupni slozka>/<kategorie>/*.obj. Bez slozky do meshes/ v koreni
(odtud je build sam naimportuje do UE, do /Game/Skvt/Lapikus/Ruin/<MESH_DIRS[kategorie]>).
Kategorie (bez udani vsechny): viz CATEGORIES. Kazda kategorie = jeden modul mesh_<kategorie>.py s funkci build(out).

Nova kategorie:
  1. modul mesh_<kategorie>.py s funkci build(out) (spolecne funkce: mesh_common.py),
  2. zaznam v CATEGORIES (tady),
  3. slozka v UE: MESH_DIRS v zrlib/config.py, jmena meshi: _needed_meshes v zrlib/ue_assets.py.

Po zmene tvaru zvys verzi v zrlib/config.py -> STONE_MESH_VERSION, jinak UE stary mesh neprenacte.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import mesh_stone, mesh_wood, mesh_wattle, mesh_textile          # noqa: E402

# poradi = poradi generovani a vypisu
CATEGORIES = {
    "stone": mesh_stone.build,        # lomove, zvetrale a opracovane kameny, kvadr
    "wood":  mesh_wood.build,         # tramy, sloupy, prkna, kulatina (mesh_log), pasy kury (mesh_bark)
    "wattle": mesh_wattle.build,      # prouti a mazanina: dilec steny, dymnik, komin
    "textile": mesh_textile.build,    # lano, ovazani, ukazka plachty (make_canvas pro stavby na miru)
}
DEFAULT_OUT = os.path.normpath(os.path.join(HERE, "..", "..", "meshes"))      # = MESH_SRC v zrlib/config.py


def main(out=None, cats=None):
    out = out or DEFAULT_OUT
    cats = list(cats) if cats else list(CATEGORIES)
    bad = [c for c in cats if c not in CATEGORIES]
    if bad:
        raise SystemExit("neznama kategorie: %s (znam: %s)" % (", ".join(bad), ", ".join(CATEGORIES)))
    made = []
    for c in CATEGORIES:                      # vzdy v poradi CATEGORIES
        if c in cats:
            d = os.path.join(out, c); os.makedirs(d, exist_ok=True)
            made += CATEGORIES[c](d)
    for m in made: print("%-24s vrcholu %5d  trojuhelniku %5d" % m)
    return made


if __name__ == "__main__":
    a = sys.argv[1:]
    out = a.pop(0) if a and a[0] not in CATEGORIES else None
    main(out, a)
