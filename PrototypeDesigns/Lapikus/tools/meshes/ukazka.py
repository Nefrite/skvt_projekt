"""ukazka.py - ukazka knihovnich meshi v UE po tematech (kontrola tvaru, slotu, textur).

Kazde tema = spoustec v tools/meshes/ukazka/Ukazka_<Tema>.py (v UE: Tools -> Execute Python Script). Naimportuje jen
meshe sveho tematu (ue_assets.ensure_stone_meshes(only=...)), postavi je do vlastniho pasu (ORIGIN + pas tematu v Y)
s tagem Ukazka_Meshe_<tema> a ve slozce Outlineru Ukazka/Meshe/<tema>. MODE = "clear" smaze jen sve tema.
Spolu se smaze i starsi ukazka vseho (tag Ukazka_Meshe, Ukazka_Kulatina), ktera lezi na stejnem miste.
tools/meshes/Ukazka_Meshe.py postavi vsechna temata najednou (meshe mimo temata do tematu "ostatni").

Nove tema: zaznam v UKAZKY (+ poradi pasu v PASY) a spoustec v tools/meshes/ukazka/ (kopie jineho, zmenit TEMA).
Novy mesh: pridat prefix do tematu (muze byt ve vic tematech). Level zriceniny ani stavby nemeni; import a materialy
se delaji mimo transakci, Undo vrati jen actory ukazky.
"""
import os, sys

ORIGIN = (3600.0, -3400.0, 3500.0)          # cm, levy predni roh pasu prvniho tematu (posun podle potreby)
PAS = 2500.0                                # cm, sirka pasu jednoho tematu v Y (temata stoji vedle sebe)
GAP_Y, GAP_X = 40.0, 80.0                   # mezera mezi meshi v rade (Y) a mezi radami (X)
FINISHES = ["peeled", "raw", "tar"]         # uprava dreva v radach temat s finishes=True (zrlib/config.py WOOD_FINISH)
TAG = "Ukazka_Meshe"                        # tag tematu = TAG + "_" + tema
OLD_TAGS = ["Ukazka_Meshe", "Ukazka_Kulatina"]   # starsi ukazka vseho (lezi na ORIGIN)

# tema -> dict(src = "round" | "wood" | "lib", prefixes = [...] (pro round/wood None = vse), finishes = rady podle upravy dreva)
UKAZKY = {
    "kulatina":    dict(src="round", prefixes=None, finishes=True),
    "drevo":       dict(src="wood", prefixes=None, finishes=True),
    "kura_prouti": dict(src="lib", prefixes=["SM_RuinBarkStrip", "SM_RuinWattlePanel", "SM_RuinSmokeHood", "SM_RuinChimney",
                                             "SM_RuinOvenDome"]),
    "textil":      dict(src="lib", prefixes=["SM_RuinRope", "SM_RuinLashing", "SM_RuinCanvasSample", "SM_RuinCanvasVez",
                                             "SM_RuinCanvasVezGable", "SM_RuinCanvasTent"]),
    "kovarna":     dict(src="lib", prefixes=["SM_RuinAnvil", "SM_RuinBellows", "SM_RuinBarrel", "SM_RuinGrindstone",
                                             "SM_RuinGrindstoneTreadle", "SM_RuinWorkbench", "SM_RuinTongs", "SM_RuinHammer",
                                             "SM_RuinChisel", "SM_RuinNailHeader", "SM_RuinCoalBox", "SM_RuinCoalBoxLid",
                                             "SM_RuinIronBars", "SM_RuinStump"]),
    "naradi":      dict(src="lib", prefixes=["SM_RuinMallet", "SM_RuinNailHammer", "SM_RuinBroadaxe", "SM_RuinAxe",
                                             "SM_RuinCrosscutSaw"]),
    "obydli":      dict(src="lib", prefixes=["SM_RuinBed", "SM_RuinBedFolded", "SM_RuinTable", "SM_RuinChest", "SM_RuinShelf",
                                             "SM_RuinDoor", "SM_RuinShutter", "SM_RuinOvenDoor", "SM_RuinStool", "SM_RuinWoodpile",
                                             "SM_RuinBasket", "SM_RuinLadder"]),
    "stan":        dict(src="lib", prefixes=["SM_RuinCanvasTent", "SM_RuinCampBed", "SM_RuinCampBedFolded", "SM_RuinChestSmall", "SM_RuinBundle", "SM_RuinStump"]),          # doplnit s etapami stanu
    "guesthouse":  dict(src="lib", prefixes=["SM_RuinBedLarge", "SM_RuinChestLocked", "SM_RuinArmorStand", "SM_RuinStool", "SM_RuinOvenDoor"]),            # doplnit s etapami guesthouse
    "ohniste":     dict(src="lib", prefixes=["SM_RuinCampfire"]),
}
PASY = list(UKAZKY) + ["ostatni"]           # poradi pasu v Y (pevne, at temata stoji vzdy na stejnem miste)


def _boot():
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    if root in sys.path: sys.path.remove(root)
    sys.path.insert(0, root)
    for k in [k for k in sys.modules if k.split(".")[0] == "zrlib"]: del sys.modules[k]
    return root


def _items(tema, cfg):
    """[(rada, [(prefix, nom, varianty, cat, bark)])] pro tema; rada = jmeno podslozky v Outlineru"""
    from zrlib.config import LIB_MESHES, ROUND_MESHES, WOOD_NOMINAL, WOOD_FINISH
    src = cfg["src"]; want = cfg.get("prefixes")
    if src == "round":
        base = [(p, nom, vs, "Bark" in p) for p, (nom, vs, _s) in ROUND_MESHES.items() if want is None or p in want]
    elif src == "wood":
        base = [(p, nom, "ABC", False) for p, nom in WOOD_NOMINAL.items() if want is None or p in want]
    else:
        miss = [p for p in want if p not in LIB_MESHES]
        if miss: print("Ukazka %s: v LIB_MESHES chybi %s (preskoceno)" % (tema, ", ".join(miss)))
        rows = [("%s" % tema, [(p, LIB_MESHES[p][0], LIB_MESHES[p][1], LIB_MESHES[p][4], False) for p in want if p in LIB_MESHES])]
        return rows
    if cfg.get("finishes"):
        return [("%s_%s" % (tema, f), [(p, nom, vs, WOOD_FINISH[f], bk) for p, nom, vs, bk in base]) for f in FINISHES]
    return [(tema, [(p, nom, vs, "wood", bk) for p, nom, vs, bk in base])]


def ostatni():
    """prefixy LIB_MESHES, ktere nejsou v zadnem tematu"""
    from zrlib.config import LIB_MESHES
    used = {p for c in UKAZKY.values() if c["src"] == "lib" for p in c["prefixes"]}
    return [p for p in LIB_MESHES if p not in used]


def run(temata, mode="build"):
    """postavi (mode "build") nebo smaze ("clear") ukazku zadanych temat; temata = seznam jmen z UKAZKY (+ "ostatni")"""
    import unreal
    root = _boot()
    from zrlib import ue_assets, ue_actors
    from zrlib.config import CUBE_MESH, MESH_SRC
    from zrlib.stones import Stone
    cfgs = {}
    for t in temata:
        if t == "ostatni":
            rest = ostatni()
            if rest: cfgs[t] = dict(src="lib", prefixes=rest)
        elif t in UKAZKY: cfgs[t] = UKAZKY[t]
        else: unreal.log_warning("Ukazka: nezname tema %s (znam: %s)" % (t, ", ".join(PASY)))
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    rows = {t: _items(t, c) for t, c in cfgs.items()}
    if mode != "clear":
        names = sorted({p for rr in rows.values() for _r, its in rr for p, *_ in its})
        mats = ue_assets.all_materials(unreal)
        meshes = ue_assets.ensure_stone_meshes(unreal, os.path.join(root, MESH_SRC), only=names)
        cube = unreal.load_asset(CUBE_MESH)
    with unreal.ScopedEditorTransaction("Ukazka meshi " + ", ".join(cfgs)):
        n_del = sum(ue_actors.destroy_tagged(eas, t) for t in OLD_TAGS + ["%s_%s" % (TAG, t) for t in cfgs])
        if mode == "clear":
            unreal.log("Ukazka meshi (%s): smazano %d actoru" % (", ".join(cfgs), n_del)); return
        n = 0
        for t, rr in rows.items():
            y0 = ORIGIN[1] + PASY.index(t) * PAS; row_x = ORIGIN[0]; tag = "%s_%s" % (TAG, t)
            for rada, its in rr:
                y = y0; row_len = 0.0
                for pref, nom, vs, cat, bark in its:
                    for v in vs:
                        name = "%s_%s" % (pref, v)
                        if name not in meshes: unreal.log_warning("Ukazka meshi: chybi mesh %s" % name); continue
                        s = Stone("ukazka|%s|%s" % (rada, name), cat, row_x + nom[0] / 2, y + nom[1] / 2, ORIGIN[2] + nom[2] / 2,
                                  0.0, nom[0], nom[1], nom[2], bark=bark)
                        s.mesh = name
                        act = ue_actors.spawn_loose(unreal, eas, s, cube, meshes, [tag], "Ukazka/Meshe/" + rada, mats.get(cat))
                        if act: act.set_actor_label("%s_%s" % (name, rada)); n += 1
                        y += nom[1] + GAP_Y; row_len = max(row_len, nom[0])
                if y - y0 > PAS: unreal.log_warning("Ukazka %s: rada %s je delsi nez pas (%.0f > %.0f cm), prekryje dalsi tema" % (t, rada, y - y0, PAS))
                row_x += row_len + GAP_X
    unreal.log("Ukazka meshi: %d actoru, temata %s, slozka Ukazka/Meshe, tagy %s_<tema>" % (n, ", ".join(cfgs), TAG))
