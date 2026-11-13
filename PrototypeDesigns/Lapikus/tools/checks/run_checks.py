"""run_checks.py - kontroly zriceniny a staveb bez Unrealu (stejny stav jako v UE: teren z levelu, rucni upravy).
python run_checks.py [--layout <ruin_layout.json>] [--only openings,floating,ostroh]

  openings  zadny blok lice / jadra ve svetlosti otvoru (kolize: 0)
  floating  kameny zdi bez podpory (pod nimi nic, nejsou na osteni / nadprazi)
  ostroh    krov, dostavba a podlaha u ostrohu: pruniky se zriceninou a mezi sebou, pokryti krytinou, mezery pod strechou
Vysledek: souhrn na konci; nenulovy navratovy kod, kdyz neco neproslo."""
import argparse, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common


def check_openings(S):
    R, lay = S["R"], S["layout"]
    P = R.params(lay, R.AGE, R.OVERRIDE); terr = S["terr"]
    pts = [p for w in lay["walls"] for p in w["points"]]; cen = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    bad = 0; n = 0
    for wd in lay["walls"]:
        stones, states, L = R.build_wall_stones(wd, P, terr, lay, [], set(), cen)
        n += len(states)
        for s in stones:
            if not s.span: continue
            s0, s1, _, _ = s.span
            for st in states:
                z0 = (s.z - s.sz / 2 - st["zb"]) / 100; z1 = (s.z + s.sz / 2 - st["zb"]) / 100
                for k in range(21):
                    xx = s0 + 0.02 + (s1 - s0 - 0.04) * k / 20
                    g = R.opening_gap(st, xx)
                    core = (s.cat == "core") or (s.cat == "crown" and s.id.count("|") >= 3 and s.id.split("|")[2] == "0")
                    if st["kind"] == "kapsa" and int(s.id.split("|")[2]) != (-st["inside"] if st.get("outer") else st["inside"]): g = None
                    if core and not st["lintel_lost"] and not (st["x0"] <= xx <= st["x1"]): g = None
                    if g and z1 - 0.03 > g[0] and z0 + 0.03 < g[1]:
                        bad += 1; print("   ", wd["name"], s.id, st["kind"], round(xx, 2)); break
    print("openings: otvoru %d, kolizi %d" % (n, bad))
    return bad == 0


def check_floating(S, known=3):
    R, lay = S["R"], S["layout"]
    P = R.params(lay, R.AGE, R.OVERRIDE); terr = S["terr"]
    pts = [p for w in lay["walls"] for p in w["points"]]; cen = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    tot = 0
    for wd in lay["walls"]:
        st, states, L = R.build_wall_stones(wd, P, terr, lay, [], set(), cen)
        sp = [s for s in st if s.span]
        for s in sp:
            z0 = s.z - s.sz / 2
            if s.span[2] < 0.3: continue
            below = [b for b in sp if abs((b.z + b.sz / 2) - z0) < 3]
            ov = sum(max(0, min(s.span[1], b.span[1]) - max(s.span[0], b.span[0])) for b in below)
            frames = [f for f in st if f.cat == "frame" and abs(f.x - s.x) < 150 and abs(f.y - s.y) < 150 and f.z < s.z]
            if ov < 0.3 * (s.span[1] - s.span[0]) and not frames: tot += 1; print("   ", wd["name"], s.id)
    print("floating: kamenu bez podpory %d (znamych %d)" % (tot, known))
    return tot <= known


def check_ostroh(S):
    groups, walls = S["groups"], S["walls"]
    krov = groups.get("Ostroh_Krov", {}).get("stones", []); dost = groups.get("Ostroh_Dostavba", {}).get("stones", [])
    podl = groups.get("Ostroh_Podlaha", {}).get("stones", [])
    ruin = [s for n in ("Hradba_Z_S", "ZBudova_V", "ZBudova_S") for s in walls[n]["stones"] + walls[n].get("loose", [])]
    stone = [s for s in dost if s.cat == "face"]; wood_d = [s for s in dost if s.cat.startswith("wood")]
    ok = True
    for name, A, B, tol, lim in (("tramy krovu x zricenina", [s for s in krov if "|R" not in s.id], ruin, 3, 0),
                                 ("krytina x zricenina", [s for s in krov if "|R" in s.id], ruin, 2, 0),
                                 ("dostavba x krov", stone, krov, 2, 0),
                                 ("dostavba x zricenina", stone + wood_d, ruin, 2, 1),
                                 ("nadprazi x dostavba", wood_d, stone, 1, 0),
                                 ("podlaha x zricenina", podl, ruin, 2, 0),
                                 ("podlaha x dostavba", podl, [s for s in dost if s.cat != "core"], 2, 0),
                                 ("podlaha x sloupy krovu", podl, [s for s in krov if "|P" in s.id], 2, 0)):
        c = common.collisions(A, B, tol)
        print("ostroh: %-26s %3d%s" % (name, len(c), "  " + str(c[:3]) if c else "")); ok &= len(c) <= lim
    # pokryti krytinou uvnitr obytne casti (body po 4 cm)
    BC = S["BC"]; ad = next((a for a in S["data"].get("addons", []) if a.get("type") == "stone_addon"), None)
    if ad:
        poly = BC.addon_polygon(ad)
        boards = [common.footprint(s) for s in krov if "|R" in s.id and s.id.split("|")[-1][0] in "KSL"]
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]; n_in = n_hole = 0
        for i in range(int(min(xs)), int(max(xs)), 4):
            for j in range(int(min(ys)), int(max(ys)), 4):
                if not BC.inside_poly(poly, i, j): continue
                n_in += 1
                if not any(BC.inside_poly(b, i, j) for b in boards): n_hole += 1
        print("ostroh: pokryti krytinou %.2f %% (nepokryto %d z %d bodu)" % (100 - 100 * n_hole / max(n_in, 1), n_hole, n_in))
        ok &= n_hole / max(n_in, 1) < 0.005
    return ok


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--layout"); ap.add_argument("--only")
    a = ap.parse_args()
    only = a.only.split(",") if a.only else ["openings", "floating", "ostroh"]
    S = common.state(a.layout, with_constructions="ostroh" in only)
    res = {}
    if "openings" in only: res["openings"] = check_openings(S)
    if "floating" in only: res["floating"] = check_floating(S)
    if "ostroh" in only: res["ostroh"] = check_ostroh(S)
    print("\nSOUHRN: " + ", ".join("%s %s" % (k, "OK" if v else "CHYBA") for k, v in res.items()))
    sys.exit(0 if all(res.values()) else 1)


if __name__ == "__main__":
    main()
