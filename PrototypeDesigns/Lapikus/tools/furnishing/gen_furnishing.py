"""gen_furnishing.py - vytvori 06_furnishing/furnishing.json pro build_furnishing.py (vybaveni = prenosne props).
Polohy a seznam kusu jsou ve specech staveb (tools/ruin/*_spec.py), sem patri jen sestaveni skupin.
  - Palac_Kovarna_Vybaveni: vybaveni kovarny (palac_spec.kovarna_vybaveni), ram palace, lano paky visi z krokve
    strechy Palac_Kovarna_Pristresek (05)

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


def palac(LAY):
    F = palac_frame(LAY["walls"])
    return [dict(name="Palac_Kovarna_Vybaveni", type="props", folder="Vybaveni/Palac/Kovarna", origin=F["origin"], u=F["s"], v=F["n"],
                 roof="Palac_Kovarna_Pristresek",                    # lano paky mechu visi z krokve (05)
                 items=kovarna_vybaveni(LAY["walls"]))]


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "06_furnishing", "furnishing.json")
    with open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "03_ruin", "blocks", "ruin_layout.json"), encoding="utf-8") as f: LAY = json.load(f)
    old = furn_data.load(out) if os.path.exists(out) else None
    groups, msgs = furn_data.merge(old, palac(LAY))
    furn_data.save(out, dict(version=2, units="UE cm (pozice), m (rozmery v ramu skupiny)",
                             note="Vybaveni (prenosne props). Stavby jsou v 05_constructions/constructions.json. Polohy z levelu zapisuje "
                                  "capture primo sem (captured / removed / manual), generator je pri slouceni zachova.",
                             groups=groups))
    for m in msgs: print("  !", m)
    print("vybaveni:", ", ".join("%s (%d kusu, z levelu %d, smazanych %d, pridanych %d)" % (
        g["name"], len(g["items"]), sum(1 for i in g["items"] if i.get("captured")),
        sum(1 for i in g["items"] if i.get("removed")), sum(1 for i in g["items"] if i.get("manual"))) for g in groups))
