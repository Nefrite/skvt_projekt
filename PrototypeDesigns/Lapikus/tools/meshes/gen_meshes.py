"""gen_meshes.py - generator knihovnich meshi zriceniny a dostaveb (OBJ, cm, Z nahoru). Potrebuje numpy.

    python tools/meshes/gen_meshes.py [vystupni slozka] [kategorie ...] [--only PREFIX,PREFIX ...]

--only: zapise jen meshe s danym prefixem (SM_RuinCanvasTent -> SM_RuinCanvasTent_A.obj + .json); bez kategorii
projde vsechny. Ostatni OBJ ve slozce zustanou, jak jsou. Kompletni podklady = bez --only.

Kazda kategorie se zapise do <vystupni slozka>/<kategorie>/*.obj. Bez slozky do meshes/ v koreni
(odtud je build sam naimportuje do UE, do /Game/Skvt/Lapikus/Ruin/<MESH_DIRS[kategorie]>).
Kategorie (bez udani vsechny): viz CATEGORIES. Kazda kategorie = jeden modul mesh_<kategorie>.py s funkci build(out).

Nova kategorie:
  1. modul mesh_<kategorie>.py s funkci build(out) (spolecne funkce: mesh_common.py),
  2. zaznam v CATEGORIES (tady),
  3. slozka v UE: MESH_DIRS v zrlib/config.py, jmena meshi: _needed_meshes v zrlib/ue_assets.py.

Po zmene tvaru zvys verzi v zrlib/config.py -> STONE_MESH_VERSION, jinak UE stary mesh neprenacte.
"""
import inspect, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import mesh_stone, mesh_wood, mesh_wattle, mesh_textile, mesh_props          # noqa: E402

# poradi = poradi generovani a vypisu
CATEGORIES = {
    "stone": mesh_stone.build,        # lomove, zvetrale a opracovane kameny, kvadr
    "wood":  mesh_wood.build,         # tramy, sloupy, prkna, kulatina (mesh_log), pasy kury (mesh_bark)
    "wattle": mesh_wattle.build,      # prouti a mazanina: dilec steny, dymnik, komin
    "textile": mesh_textile.build,    # lano, ovazani, ukazka plachty (make_canvas pro stavby na miru)
    "props": mesh_props.build,        # vlastni props (kovarna, spalek, ponk, hranice, kos, zebrik ...)
}
DEFAULT_OUT = os.path.normpath(os.path.join(HERE, "..", "..", "meshes"))      # = MESH_SRC v zrlib/config.py


def _match(name, only):
    """jmeno meshe (bez pripony) patri k nekteremu prefixu: <prefix> nebo <prefix>_<varianta>"""
    return any(name == p or name.startswith(p + "_") for p in only)


def _build_only(fn, d, only):
    """kategorie jen s vybranymi meshi: modul s parametrem only ho dostane, jinak se generuje do docasne slozky
    a prekopiruji se jen vybrane soubory (OBJ i .json)"""
    if "only" in inspect.signature(fn).parameters:
        return fn(d, only=only)
    tmp = tempfile.mkdtemp(prefix="gen_meshes_")
    try:
        made = [m for m in fn(tmp) if _match(m[0], only)]
        for f in os.listdir(tmp):
            if _match(os.path.splitext(f)[0], only): shutil.copy2(os.path.join(tmp, f), os.path.join(d, f))
        return made
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(out=None, cats=None, only=None):
    out = out or DEFAULT_OUT
    cats = list(cats) if cats else list(CATEGORIES)
    bad = [c for c in cats if c not in CATEGORIES]
    if bad:
        raise SystemExit("neznama kategorie: %s (znam: %s)" % (", ".join(bad), ", ".join(CATEGORIES)))
    made = []
    for c in CATEGORIES:                      # vzdy v poradi CATEGORIES
        if c in cats:
            d = os.path.join(out, c); os.makedirs(d, exist_ok=True)
            made += CATEGORIES[c](d) if only is None else _build_only(CATEGORIES[c], d, only)
    if only is not None and not made:
        print("--only %s: zadny mesh neodpovida" % ",".join(only))
    for m in made: print("%-24s vrcholu %5d  trojuhelniku %5d" % m)
    return made


if __name__ == "__main__":
    a = sys.argv[1:]; only = None
    if "--only" in a:
        i = a.index("--only"); only = [p for p in ",".join(a[i + 1:]).split(",") if p]; a = a[:i]
    out = a.pop(0) if a and a[0] not in CATEGORIES else None
    main(out, a, only)
