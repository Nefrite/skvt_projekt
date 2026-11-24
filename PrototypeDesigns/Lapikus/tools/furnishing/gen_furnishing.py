"""gen_furnishing.py - vytvori 06_furnishing/furnishing.json pro build_furnishing.py (vybaveni = prenosne props).
Polohy a seznam kusu jsou ve specech staveb (tools/ruin/*_spec.py), sem patri jen sestaveni skupin.
  - Palac_Kovarna_Vybaveni: vybaveni kovarny (palac_spec.kovarna_vybaveni), ram palace, lano paky visi z krokve
    strechy Palac_Kovarna_Pristresek (05)
  - Guesthouse_Vybaveni: vybaveni pokoje hosta u ostrohu (ostroh_spec.guesthouse_vybaveni), ram podlahy Ostroh_Podlaha,
    vysky od vrchu prken podlahy (spocitane z terenu jako pri buildu podlahy; po zmene terenu nebo podlahy pregenerovat)
  - Brana_Straz_Vybaveni: vybaveni strazniho stanoviste nad branami (brana_spec.brana_straz_vybaveni), ram brany,
    vysky od vrchu prken podesty Brana_Straz_Podesta (deck_z)

python gen_furnishing.py [<vystup furnishing.json>] [<03_ruin/blocks/ruin_layout.json>]
Po zmene spolecneho specu (palac_spec.py) pregeneruj i tools/constructions/gen_constructions.py.

furnishing.json je jediny zdroj poloh vybaveni: capture v UE do nej zapisuje polohy z levelu. Generator proto data
neprepisuje, ale slouci (06_furnishing/furn_data.py -> merge): kusy s ulozenou polohou (captured), smazane (removed)
a rucne pridane (manual) zustanou, nove kusy ze specu pribudou, kusy bez specu se jen vypisou. Predchozi verze -> .bak.
Na polohu podle specu se kus vraci pres MODE = "reset" (build_furnishing.py / vybaveni/<Skupina>.py)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "ruin"))
sys.path.insert(0, os.path.join(ROOT, "06_furnishing"))
import furn_data
from palac_spec import frame as palac_frame, kovarna_vybaveni
from ostroh_spec import guesthouse_vybaveni, GH_REF
from brana_spec import straz as brana_straz_spec, brana_straz_vybaveni, B_FURN_REF
from nadvori_spec import stan_frame as nadvori_stan_frame, stan_vybaveni as nadvori_stan_vybaveni


def palac(LAY):
    F = palac_frame(LAY["walls"])
    return [dict(name="Palac_Kovarna_Vybaveni", type="props", folder="Vybaveni/Palac/Kovarna", origin=F["origin"], u=F["s"], v=F["n"],
                 roof="Palac_Kovarna_Pristresek",                    # lano paky mechu visi z krokve (05)
                 items=kovarna_vybaveni(LAY["walls"]))]


def guesthouse():
    """skupina Guesthouse_Vybaveni: ram a vyska podlahy Ostroh_Podlaha z 05_constructions/constructions.json, teren jako
    pri buildu (cache terenu z levelu, stejne jako tools/checks)"""
    for p in (ROOT, os.path.join(ROOT, "05_constructions")):
        if p not in sys.path: sys.path.insert(0, p)
    from zrlib import pipeline
    from zr_stavby.podlaha import floor_top
    with open(os.path.join(ROOT, "05_constructions", "constructions.json"), encoding="utf-8") as f: C = json.load(f)
    fl = next(a for a in C["addons"] if a["name"] == "Ostroh_Podlaha")
    R = pipeline.load_ruin(); terr = R.Terrain(R.cached_level_terrain(R.load_layout())["terrain"])
    O, U, V = fl["outline"][0], fl["u"], fl["n"]
    ref = (O[0] + (U[0] * GH_REF[0] + V[0] * GH_REF[1]) * 100, O[1] + (U[1] * GH_REF[0] + V[1] * GH_REF[1]) * 100)
    fz = (floor_top(fl, terr) - terr.z(*ref)) / 100
    return [dict(name="Guesthouse_Vybaveni", type="props", folder="Vybaveni/Ostroh/Guesthouse", origin=O, u=U, v=V,
                 items=guesthouse_vybaveni(fz))]


def brana(LAY):
    """skupina Brana_Straz_Vybaveni: ram brany a vyska podlahy podesty deck_z z brana_spec.straz(), teren z cache levelu"""
    for p in (ROOT, os.path.join(ROOT, "05_constructions")):
        if p not in sys.path: sys.path.insert(0, p)
    from zrlib import pipeline
    S = brana_straz_spec(LAY["walls"]); F = S["frame"]
    R = pipeline.load_ruin(); terr = R.Terrain(R.cached_level_terrain(R.load_layout())["terrain"])
    O, U, V = F["origin"], F["u"], F["d"]
    ref = (O[0] + (U[0] * B_FURN_REF[0] + V[0] * B_FURN_REF[1]) * 100, O[1] + (U[1] * B_FURN_REF[0] + V[1] * B_FURN_REF[1]) * 100)
    fz = (S["deck_z"] - terr.z(*ref)) / 100
    return [dict(name="Brana_Straz_Vybaveni", type="props", folder="Vybaveni/Brana/Straz", origin=O, u=U, v=V,
                 items=brana_straz_vybaveni(fz))]


def nadvori_stan(LAY):
    """skupina Nadvori_Stan_Vybaveni: ram stanu (nadvori_spec.stan_frame), etapa 1 (stage='site')"""
    F = nadvori_stan_frame(LAY["walls"])
    return [dict(name="Nadvori_Stan_Vybaveni", type="props", folder="Vybaveni/Nadvori/Stan", stage="site",
                 origin=F["origin"], u=F["u"], v=F["v"], items=nadvori_stan_vybaveni())]


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "06_furnishing", "furnishing.json")
    with open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "03_ruin", "blocks", "ruin_layout.json"), encoding="utf-8") as f: LAY = json.load(f)
    old = furn_data.load(out) if os.path.exists(out) else None
    groups, msgs = furn_data.merge(old, palac(LAY) + guesthouse() + brana(LAY) + nadvori_stan(LAY))
    furn_data.save(out, dict(version=2, units="UE cm (pozice), m (rozmery v ramu skupiny)",
                             note="Vybaveni (prenosne props). Stavby jsou v 05_constructions/constructions.json. Polohy z levelu zapisuje "
                                  "capture primo sem (captured / removed / manual), generator je pri slouceni zachova.",
                             groups=groups))
    for m in msgs: print("  !", m)
    print("vybaveni:", ", ".join("%s (%d kusu, z levelu %d, smazanych %d, pridanych %d)" % (
        g["name"], len(g["items"]), sum(1 for i in g["items"] if i.get("captured")),
        sum(1 for i in g["items"] if i.get("removed")), sum(1 for i in g["items"] if i.get("manual"))) for g in groups))
