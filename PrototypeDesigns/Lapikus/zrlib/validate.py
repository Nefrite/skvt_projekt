"""kontrola dat (ruin_layout.json, constructions.json): chybejici klic = srozumitelna chyba se jmenem zdi / stavby"""


def require(spec, keys, where):
    miss = [k for k in keys if k not in spec]
    if miss:
        raise ValueError("%s: chybi %s (pregeneruj data generatorem v tools/, nebo dopln rucne)" % (where, ", ".join(miss)))


LAYOUT_WALL = ["name", "points", "thickness", "H0", "access", "folder"]
LAYOUT_FLOOR = ["name", "origin", "u", "v", "inner", "ref_z"]


def layout(lay):
    """zakladni kontrola ruin_layout.json"""
    require(lay, ["params", "walls", "terrain", "plateau_z_cm"], "ruin_layout.json")
    for w in lay["walls"]: require(w, LAYOUT_WALL, "ruin_layout.json -> walls -> %s" % w.get("name"))
    for f in lay.get("floors", []): require(f, LAYOUT_FLOOR, "ruin_layout.json -> floors -> %s" % f.get("name"))
