"""run_checks.py - kontroly zriceniny a staveb bez Unrealu (stejny stav jako v UE: teren z levelu, rucni upravy).
python run_checks.py [--layout <ruin_layout.json>] [--only openings,floating,ostroh,palac,obydli,brana,vez]

  openings  zadny blok lice / jadra ve svetlosti otvoru (kolize: 0)
  floating  kameny zdi bez podpory (pod nimi nic, nejsou na osteni / nadprazi)
  ostroh    krov, dostavba a podlaha u ostrohu: pruniky se zriceninou a mezi sebou, pokryti krytinou, mezery pod strechou
  palac     kovarna v palaci: pruniky dreva se zriceninou, sloupy na patnich kamenech, krokve na pozednicich, sklon,
            vule komina od krokvi a pozednic, svetla vyska, pokryti krytinou, lemovani; vyhen; stena z prouti; okap a sud
  obydli    dum v prostredni mistnosti palace: nove zdivo mimo zriceninu, srovnane koruny pricek, podezdivky, pruchody, sady etap
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
    # vybaveni Guesthouse (06, Guesthouse_Vybaveni): pruniky, kusy na podlaze, volny pruchod u dveri
    vg = S.get("furn", {}).get("Guesthouse_Vybaveni")
    if vg:
        V = vg["loose"]; others = [s for s in dost if s.cat != "core"] + krov
        for name, A, B in (("vybaveni x zricenina", V, ruin), ("vybaveni x dostavba a krov", V, others)):
            c = common.collisions(A, B, 1.0)
            print("ostroh: %-26s %3d%s" % (name, len(c), "  " + str(c[:3]) if c else "")); ok &= not c
        c = [x for x in common.collisions(V, V, 1.0) if x[1] < x[2]]
        print("ostroh: %-26s %3d%s" % ("vybaveni mezi sebou", len(c), "  " + str(c[:3]) if c else "")); ok &= not c
        ftop = max(s.z + s.sz / 2 for s in podl if "|K" not in s.id) if podl else None
        planks = [s for s in podl if s.sz < 6]; ftop = max(s.z + s.sz / 2 for s in planks) if planks else ftop
        if ftop is not None:
            d_ = max(abs(s.z - s.sz / 2 - ftop) for s in V)
            print("ostroh: vybaveni stoji na podlaze (odchylka nejvys %.1f cm)" % d_); ok &= d_ < 1.0
        fl = next((a for a in S["data"].get("addons", []) if a["name"] == "Ostroh_Podlaha"), None)
        if fl:
            O, U, N = fl["outline"][0], fl["u"], fl["n"]
            sn = lambda q: (((q[0] - O[0]) * U[0] + (q[1] - O[1]) * U[1]) / 100, ((q[0] - O[0]) * N[0] + (q[1] - O[1]) * N[1]) / 100)
            bad = [s.id.split("|")[-1] for s in V for q in common.footprint(s) if 5.8 < sn(q)[0] < 8.1 and sn(q)[1] < 2.0]
            print("ostroh: pruchod u dveri (s 5,8 - 8,1; n 0 - 2 m) volny %s" % ("OK" if not bad else "CHYBA " + str(sorted(set(bad)))))
            ok &= not bad
    return ok


def check_palac(S):
    """pristresek kovarny (Palac_Kovarna_Pristresek, typ pult_roof): kriteria z new_designs/navrh_palac_kovarna.md kap. 7"""
    groups, walls, BC = S["groups"], S["walls"], S["BC"]
    fr = next((f for f in S["data"].get("frames", []) if f["name"] == "Palac_Kovarna_Pristresek"), None)
    g = groups.get("Palac_Kovarna_Pristresek")
    if not fr or not g: print("palac: Palac_Kovarna_Pristresek neni v datech"); return False
    st = g["stones"] + g["loose"]; by = {s.id: s for s in st}; n = fr["name"]; ok = True
    def rep(txt, good):
        nonlocal ok
        print("palac: %-58s %s" % (txt, "OK" if good else "CHYBA")); ok &= bool(good)
    ruin = [s for w in walls.values() for s in w["stones"] + w.get("loose", [])]
    wood = [s for s in st if s.cat.startswith("wood")]
    c = common.collisions(wood, ruin, 1.0)
    rep("drevo x zricenina: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
    c = common.collisions([s for s in st if s.loose], ruin, 1.0)
    rep("patni kameny x zricenina: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
    G = BC.pult_geom(fr, S["terr"]); P = G["P"]; z0 = G["z0"]
    gaps = []; n_post = 0
    for s in fr["supports"]:
        pl = by["%s|%s" % (n, s["id"])]
        for j, cpos in enumerate(s["posts"]):
            p = by["%s|%s|P%d" % (n, s["id"], j)]; k = by["%s|%s|K%d" % (n, s["id"], j)]; n_post += 1
            zg = S["terr"].z(*P(s["at"], cpos))
            gaps += [abs((p.z - p.sz / 2) - (k.z + k.sz / 2)), abs((p.z + p.sz / 2) - (pl.z - pl.sz / 2))]
            if not (k.z - k.sz / 2 < zg < k.z + k.sz / 2): gaps.append(99.0)            # patni kamen lezi v terenu / na terenu
    rep("sloupy (%d): patni kamen na terenu, sloup na kameni, pozednice na sloupu (max. mezera %.1f cm)" % (n_post, max(gaps)), max(gaps) < 0.5)
    # pozednice bez sloupu na konci musi byt ulozena ve zdi (kapsa v 03): konec aspon 20 cm za vnitrnim licem Palac_J
    n_in = next(w["thickness"] for w in S["layout"]["walls"] if w["name"] == "Palac_J") / 2
    for s in fr["supports"]:
        if min(s["posts"]) - s["span"][0] > 0.5:
            bear = n_in - s["span"][0]; pl = by["%s|%s" % (n, s["id"])]
            c = common.collisions([pl], ruin, 0.2)
            rep("pozednice %s: jizni konec %.0f cm v kapse Palac_J (>= 20), pruniku se zdivem %d" % (s["id"], bear * 100, len(c)), bear >= 0.20 and not c)
    ang = math.degrees(G["ang"]); seat = fr["rafters"].get("seat", 0) * 100; worst = 0.0
    rafters = [by["%s|%s" % (n, b["id"])] for b in G["geo"]]
    for r, b in zip(rafters, G["geo"]):
        for s in fr["supports"]:
            a = (s["at"] - G["a_hi"]) * G["sg"] * 100                                   # vodorovne od horniho konce krokve (cm)
            if not (0 <= a <= b["a1"]) or not (s["span"][0] <= b["c"] <= s["span"][1]): worst = 99.0; continue
            # spodek krokve nad osou pozednice z polohy dilce (nezavisle na pult_geom): stred, sklon, prumer
            zu = r.z + (b["a1"] / 2 - a) * math.tan(math.radians(r.pitch)) - r.sz / 2 / math.cos(math.radians(r.pitch))
            worst = max(worst, abs(zu - (z0 + s["top"] * 100 - seat)))
    rep("krokve (%d) lezi na vsech pozednicich (odchylka %.1f cm, osedlani %.0f cm)" % (len(rafters), worst, seat), worst < 0.5)
    rep("sklon strechy %.1f st. (20 +- 1)" % ang, 19 <= ang <= 21)
    for o in fr.get("openings", []):
        if o.get("kind") != "chimney": continue
        h = o["w"] / 2
        d_r = min(abs(b["c"] - o["c"]) - h - G["rw"] / 200 for b in G["geo"])
        d_p = min(abs(s["at"] - o["a"]) - h - s["sec"][0] / 2 for s in fr["supports"] if s["span"][0] - h < o["c"] < s["span"][1] + h)
        rep("komin: vule od krokvi %.0f cm, od pozednic %.0f cm (>= 10)" % (d_r * 100, d_p * 100), d_r >= 0.10 and d_p >= 0.10)
    sys.path.insert(0, os.path.join(common.ROOT, "tools", "ruin")); import palac_spec
    a_s, a_n = palac_spec.K_ANVIL; hh = (G["under"](a_s) - z0) / 100
    rep("svetla vyska pod krokvemi nad kovadlinou %.2f m (>= 3,0)" % hh, hh >= 3.0)
    lo = (G["under"](G["a_lo"]) - z0) / 100
    rep("spodek krokvi u okapu %.2f m (pruchod postavy >= 2,0)" % lo, lo >= 2.0)
    # vyhen (Palac_Kovarna_Vyhen, typ hearth): kamen a mazanina mimo zriceninu, komin a dymnik mimo drevo strechy
    hg = groups.get("Palac_Kovarna_Vyhen"); ad = next((a for a in S["data"].get("addons", []) if a["name"] == "Palac_Kovarna_Vyhen"), None)
    if hg and ad:
        hs = hg["stones"] + hg["loose"]
        c = common.collisions(hs, ruin, 1.0)
        rep("vyhen x zricenina: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        stone = [s for s in hs if s.cat == "face"]
        c = common.collisions(stone, stone, 1.0)
        rep("vyhen: kameny mezi sebou: pruniku %d %s" % (len(c), c[:2] if c else ""), not c)
        tube = [s for s in hs if s.shape in ("smoke_hood", "chimney")]
        c = common.collisions(tube, wood, 0.5)
        rep("komin a dymnik x drevo pristresku: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        tr = [s for s in hs if "|X" in s.id]; ch = next(s for s in hs if s.shape == "chimney")
        c = common.collisions(tr + [s for s in hs if "|H" in s.id], [ch], 0.5)
        rep("vymeny (%d) a zavesne tyce x komin: pruniku %d" % (len(tr), len(c)), len(tr) == 2 and not c)
        seated = all(len(common.collisions([t], rafters, 0.5)) == 2 for t in tr)
        rep("vymeny ulozene v obou sousednich krokvich", seated)
        if fr.get("roof"):                                   # vrch krytiny (prkna + lista) na horni hrane prostupu komina
            Lr = BC.pult.roof_layers(fr, G); h_ = BC.pult.roof_holes(fr)[0]; a_up = h_[1] if G["sg"] < 0 else h_[0]
            roof_top = (Lr["board"](a_up) + fr["roof"]["batten"][1] * 100 / math.cos(G["ang"]) - z0) / 100
        else: roof_top = (G["under"](ad["chimney"]["a"]) - z0 + G["vert"]) / 100 + 0.13          # + late a prkna krytiny
        over = ad["chimney"]["top"] - roof_top
        rep("komin %.2f m nad krytinou na horni hrane prostupu (>= 0,8)" % over, over >= 0.8)
        # komin presahuje korunu Palac_J v okruhu 1,5 m (kameny zdi, jejichz pudorys je do 1,5 m od osy komina)
        cx, cy = P(ad["chimney"]["a"], ad["chimney"]["c"])
        near = [s for s in walls["Palac_J"]["stones"] + walls["Palac_J"].get("loose", []) if math.hypot(s.x - cx, s.y - cy) < 150 + s.sx / 2]
        crown = max((s.z + s.sz / 2 - z0) / 100 for s in near)
        rep("komin (vrch %.1f m) presahuje korunu Palac_J v okruhu 1,5 m o %.2f m (>= 0,3)" % (ad["chimney"]["top"], ad["chimney"]["top"] - crown),
            ad["chimney"]["top"] - crown >= 0.3)
        hd = ad["hood"]; pit = ad["pit"]
        cov = abs(hd["a"] - pit["a"]) + pit["w"] / 2 <= hd["size"][0] / 2 and abs(hd["c"] - pit["c"]) + pit["w"] / 2 <= hd["size"][1] / 2
        rep("dymnik (spodni okraj %.1f m) kryje cele ohniste" % hd["bottom"], cov)
        d_an = math.hypot(a_s - ad["table"]["a"][0], 0) - 0.25                              # hrana stolu -> okraj spalku O 0,5 m
        g0, g1 = getattr(palac_spec, "K_ANVIL_GAP", (0.9, 1.1))
        rep("kovadlina %.2f m pred vyhni (%.1f-%.1f)" % (d_an, g0, g1), g0 <= d_an <= g1)
    # krytina (late, prkna, listy, lemovani): pokryti pudorysu strechy mimo prostup komina, lemovani na krytine
    cover = [s for s in st if "|R|" in s.id]
    if fr.get("roof"):
        pl = fr["plan"]; holes = BC.pult.roof_holes(fr)
        fps = [common.footprint(s) for s in cover if s.id.split("|")[-1][0] in "KLF"]
        n_in = n_hole = 0; step = 0.04
        for i in range(int((pl["a"][1] - pl["a"][0]) / step)):
            for j in range(int((pl["c"][1] - pl["c"][0]) / step)):
                a_, c_ = pl["a"][0] + step * (i + 0.5), pl["c"][0] + step * (j + 0.5)
                if any(h[0] <= a_ <= h[1] and h[2] <= c_ <= h[3] for h in holes): continue
                n_in += 1; x, y = P(a_, c_)
                if not any(BC.inside_poly(f, x, y) for f in fps): n_hole += 1
        cov = 100 - 100 * n_hole / max(n_in, 1)
        rep("krytina (%d dilcu) pokryva %.2f %% pudorysu mimo prostup komina (>= 99)" % (len(cover), cov), cov >= 99.0)
        fl = [s for s in cover if "|R|F" in s.id]
        rep("lemovani u veze a podel Palac_J (%d prkna)" % len(fl), len(fl) == len(fr.get("flashing", [])))
        L = BC.pult.roof_layers(fr, G); worst = 0.0
        for f in fl:
            for q in (-0.4, 0.0, 0.4):                       # spodni hrana lemovani na krytine (3 body podel delky)
                ya = math.radians(f.yaw); pa_ = math.radians(f.pitch); h_ = q * f.sx
                px, py = f.x + math.cos(ya) * math.cos(pa_) * h_, f.y + math.sin(ya) * math.cos(pa_) * h_
                zb = f.z + math.sin(pa_) * h_ - f.sz / 2 / math.cos(pa_)
                O_, A_ = fr["origin"], fr["u"]; a_ = ((px - O_[0]) * A_[0] + (py - O_[1]) * A_[1]) / 100
                worst = max(worst, abs(zb - L["board"](a_)))
        rep("lemovani lezi na krytine (odchylka %.1f cm)" % worst, worst < 1.5)
    # stena z prouti (Palac_Kovarna_Stena, typ wattle_wall)
    sg_ = groups.get("Palac_Kovarna_Stena"); sd = next((a for a in S["data"].get("addons", []) if a["name"] == "Palac_Kovarna_Stena"), None)
    if sg_ and sd:
        ws = sg_["stones"] + sg_["loose"]
        c = common.collisions(ws, ruin, 1.0)
        rep("stena x zricenina: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        c = common.collisions(ws, st, 0.5)
        rep("stena x pristresek (sloupy, patni kameny, pozednice): pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        pan = [s for s in ws if s.shape == "wattle_panel"]
        zg = S["terr"].z(*P(sd["a"], sum(sd["c"]) / 2)); top = max(s.z + s.sz / 2 for s in pan) - zg
        rep("stena vysoka %.2f m, pod zapadni pozednici volny pruh %.2f m" % (top / 100, (z0 + fr["supports"][1]["top"] * 100 - fr["supports"][1]["sec"][1] * 100 - zg - top) / 100),
            abs(top / 100 - sd["h"]) < 0.01)
        # zaplneni linie steny ve vysce 1 m (mimo sloupy)
        gp = sd.get("gap", 0.005) + 0.002; n_ = gap_ = 0          # mezery u zdi a u sloupu jsou zamerne
        posts = [(p["c"] - p["w"] / 2 - gp, p["c"] + p["w"] / 2 + gp) for p in sd.get("posts", [])]
        for k in range(int((sd["c"][1] - sd["c"][0] - 2 * gp) / 0.02)):
            c_ = sd["c"][0] + gp + 0.02 * (k + 0.5)
            if any(p0 <= c_ <= p1 for p0, p1 in posts): continue
            n_ += 1
            cn = lambda s: ((s.x - fr["origin"][0]) * fr["v"][0] + (s.y - fr["origin"][1]) * fr["v"][1]) / 100
            if not any(abs(cn(s) - c_) <= s.sx / 200 and s.z - s.sz / 2 <= zg + 100 <= s.z + s.sz / 2 for s in pan): gap_ += 1
        rep("stena zaplnuje linii mezi sloupy (diry %d z %d bodu po 2 cm)" % (gap_, n_), gap_ == 0)
    # okap (Palac_Kovarna_Okap, typ gutter): zlab pod okapovou hranou se spadem k sudu, na rozsochach
    og = groups.get("Palac_Kovarna_Okap"); od = next((a for a in S["data"].get("addons", []) if a["name"] == "Palac_Kovarna_Okap"), None)
    if og and od:
        os_ = og["stones"] + og["loose"]
        c = common.collisions(os_, ruin, 1.0)
        rep("okap x zricenina: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        oth = st + (sg_["stones"] if sg_ else [])
        c = common.collisions(os_, oth, 0.5)
        rep("okap x pristresek a stena: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        gu = next(s for s in os_ if s.shape == "gutter")
        a_e = G["a_lo"] + G["sg"] * fr["roof"].get("eave_over", 0.10)
        rep("okapova hrana krytiny (s = %.2f) nad zlabem (osa %.2f, O %.0f cm)" % (a_e, od["a"], od["d"] * 100), abs(a_e - od["a"]) <= od["d"] / 2 - 0.03)
        _, ztop, _ = BC.okap.gutter_line(od, S["terr"], S["data"]["frames"])
        L = BC.pult.roof_layers(fr, G); cl = min(L["lath"](a_e) - ztop(c_) for c_ in od["c"])
        drop = (ztop(od["c"][0]) - ztop(od["c"][1])) / 100
        rep("zlab: spad k severu %.1f cm na %.1f m, vrch %.0f-%.0f cm pod krytinou" % (drop * 100, od["c"][1] - od["c"][0], cl, max(L["lath"](a_e) - ztop(c_) for c_ in od["c"])),
            drop > 0 and cl >= 5)
        br = next((s for s in os_ if s.shape == "barrel"), None)
        if br:
            ex, ey = P(od["a"], od["c"][1]); d_ = math.hypot(ex - br.x, ey - br.y)
            rep("zlab konci nad sudem (%.0f cm od osy sudu, polomer %.0f)" % (d_, br.sx / 2), d_ < br.sx / 2 - 8)
            zg = S["terr"].z(br.x, br.y); rep("sud stoji na zemi (mezera %.1f cm)" % (br.z - br.sz / 2 - zg), abs(br.z - br.sz / 2 - zg) < 0.5)
        forks = [s for s in os_ if s.shape == "fork"]; posts = [s for s in os_ if "|P" in s.id]
        bad = [p.id for p in posts if p.z - p.sx / 2 > S["terr"].z(p.x, p.y) - 10]
        rep("rozsochy (%d) nesou zlab, kuly %d cm v zemi" % (len(forks), od.get("sink", 0.4) * 100), len(forks) == len(od.get("forks", [])) and not bad)
    # vybaveni (Palac_Kovarna_Vybaveni, typ props): pruniky, mechy v otvoru zidky, vzdalenosti, pruchody, sut v mistnosti
    # vybaveni je v 06_furnishing (prenosne kusy), kul u dreva v 05 (Palac_Kovarna_Kul)
    vg = S.get("furn", {}).get("Palac_Kovarna_Vybaveni"); kg = groups.get("Palac_Kovarna_Kul")
    if vg:
        V = vg["loose"]; by_ = {s.id.split("|")[-1]: s for s in V}
        kul = (kg["stones"] + kg["loose"]) if kg else []; by_.update({s.id.split("|")[-1]: s for s in kul})
        sn = lambda s: (((s.x - fr["origin"][0]) * fr["u"][0] + (s.y - fr["origin"][1]) * fr["u"][1]) / 100,
                        ((s.x - fr["origin"][0]) * fr["v"][0] + (s.y - fr["origin"][1]) * fr["v"][1]) / 100)
        pegs = [s for s in V if s.id.split("|")[-1].startswith("Kolik")]
        c = common.collisions([s for s in V if s not in pegs], ruin, 1.0)
        rep("vybaveni x zricenina: pruniku %d %s (koliky listy jsou ve sparach zdi)" % (len(c), c[:3] if c else ""), not c)
        others = st + (sg_["stones"] if sg_ else []) + (og["stones"] + og["loose"] if og else []) + (hs if hg else []) + kul
        # zamerne dotyky: mechy (kvadr) s bocni zidkou (vyfucna v otvoru), lano paky kolem krokve
        skip = lambda a, b: (a.shape == "bellows" and "|Z|" in b.id) or (a.shape == "rope" and b in rafters)
        c = common.collisions(V, others, 1.0, skip=skip)
        rep("vybaveni x stavby kovarny: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        pairs = {("Kovadlina", "Spalek"), ("Hrebovnice", "Spalek2"), ("Truhlik", "Truhlik_Viko"), ("Lista", "Kolik0"), ("Lista", "Kolik1"),
                 ("Mechy", "Mechy_Lano"), ("Mechy_Lano", "Paka"), ("Paka", "Paka_Lano")}
        pairs = {tuple(sorted(p_)) for p_ in pairs}
        c = [x for x in common.collisions(V, V, 1.0) if tuple(sorted((x[1].split("|")[-1], x[2].split("|")[-1]))) not in pairs
             and x[1] < x[2]]
        rep("vybaveni mezi sebou (mimo zamerne ulozeni): pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        # vyfucna mechu v otvoru bocni zidky: spicka 105 cm od stredu kvadru po ose X, ve vysce 0,91 m
        me = by_["Mechy"]; ya = math.radians(me.yaw); tx, ty = me.x + math.cos(ya) * 105, me.y + math.sin(ya) * 105
        O_ = fr["origin"]; ta = ((tx - O_[0]) * fr["u"][0] + (ty - O_[1]) * fr["u"][1]) / 100; tc = ((tx - O_[0]) * fr["v"][0] + (ty - O_[1]) * fr["v"][1]) / 100
        zw = next(w for w in ad["walls"]) if hg and ad else None
        if zw:
            ho = zw["hole"]; tz = (me.z - me.sz / 2 - S["terr"].z(tx, ty)) / 100 + 0.91
            ok_ = abs(ta - ho["a"]) < ho["w"] / 2 - 0.02 and zw["c"][0] < tc < zw["c"][1] and ho["z"][0] + 0.02 < tz < ho["z"][1] - 0.02
            rep("vyfucna mechu v otvoru bocni zidky (s %.2f, n %.2f, z %.2f m)" % (ta, tc, tz), ok_)
        an, sk = sn(by_["Kovadlina"]), sn(by_["KaliciSud"]); tb = ad["table"] if ad else None
        if tb:
            fx = (min(max(sk[0], tb["a"][0]), tb["a"][1]), min(max(sk[1], tb["c"][0]), tb["c"][1]))
            d1 = math.hypot(sk[0] - an[0], sk[1] - an[1]); d2 = math.hypot(sk[0] - fx[0], sk[1] - fx[1])
            qm = getattr(palac_spec, "K_QUENCH_MAX", 1.5)
            rep("kalici sud %.2f m od kovadliny a %.2f m od vyhne (<= %.1f)" % (d1, d2, qm), d1 <= qm and d2 <= qm)
        # pruchody (pudorysy kvadru): od severu mezi brusem a mechy, k ponku mezi kalicim sudem a brusem
        def gap(A, B):
            ba = [sn(type("p", (), dict(x=q[0], y=q[1]))) for q in common.footprint(A)]; bb = [sn(type("p", (), dict(x=q[0], y=q[1]))) for q in common.footprint(B)]
            ra = (min(q[0] for q in ba), max(q[0] for q in ba), min(q[1] for q in ba), max(q[1] for q in ba))
            rb = (min(q[0] for q in bb), max(q[0] for q in bb), min(q[1] for q in bb), max(q[1] for q in bb))
            dx = max(rb[0] - ra[1], ra[0] - rb[1], 0); dy = max(rb[2] - ra[3], ra[2] - rb[3], 0); return math.hypot(dx, dy)
        g1, g2 = gap(by_["Brus"], by_["Mechy"]), gap(by_["KaliciSud"], by_["Brus"])
        rep("pruchod od severu brus - mechy %.2f m, k ponku sud - brus %.2f m (>= 1,2)" % (g1, g2), g1 >= 1.2 and g2 >= 1.2)
        # drevo pod presahem strechy, pruchod podel Palac_J ke strilne s = 25
        wood = [s for s in V if s.shape == "woodpile"]; a_e = G["a_lo"] + G["sg"] * fr["roof"].get("eave_over", 0.10)
        under = all(min(q[0] for q in [sn(type("p", (), dict(x=x, y=y))) for x, y in common.footprint(w)]) > a_e for w in wood)
        free = min(sn(type("p", (), dict(x=x, y=y)))[1] for w in wood + [by_["Kul"]] for x, y in common.footprint(w)) - fr["plan"]["c"][0]
        rep("drevo pod presahem strechy (%d hranice), od Palac_J volno %.2f m" % (len(wood), free), under and free >= 1.4)
        poly = [tuple(q) for q in fr.get("clear_poly", [])]
        sut = [s for n_, gg in groups.items() if n_.endswith("_Sut") for s in gg["loose"] if poly and BC.inside_poly(poly, s.x, s.y)]
        rep("sut ve vychodni mistnosti uklizena (zbyva %d kamenu)" % len(sut), not sut)
    return ok


def check_obydli(S):
    """dum posadky (Palac_Obydli_*): kamenne casti; kriteria z new_designs/navrh_palac_obydli_stred.md"""
    groups, walls, BC = S["groups"], S["walls"], S["BC"]
    ad = next((a for a in S["data"].get("addons", []) if a["name"] == "Palac_Obydli_Kamen"), None); g = groups.get("Palac_Obydli_Kamen")
    if not ad or not g: print("obydli: Palac_Obydli_Kamen neni v datech"); return False
    ok = True
    def rep(txt, good):
        nonlocal ok
        print("obydli: %-66s %s" % (txt, "OK" if good else "CHYBA")); ok &= bool(good)
    sys.path.insert(0, os.path.join(common.ROOT, "05_constructions")); from zr_stavby.zdivo import frame_box
    O, U, V = ad["origin"], ad["u"], ad["v"]; P = lambda a, c: (O[0] + (U[0] * a + V[0] * c) * 100, O[1] + (U[1] * a + V[1] * c) * 100)
    z0 = S["terr"].z(*P(*ad["ref"]))
    ruin = [s for w in walls.values() for s in w["stones"] + w.get("loose", [])]
    allst = g["stones"] + g["loose"]; new = [s for s in allst if s.cat != "core"]; mortar = [s for s in allst if s.cat == "core"]
    hg = groups.get("Palac_Obydli_Ohniste", {}); hearth = hg.get("stones", []) + hg.get("loose", [])
    c = common.collisions(new + hearth, ruin, 1.5)
    rep("nove zdivo a ohniste x zricenina: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
    c = common.collisions(new, new, 1.0) + common.collisions(hearth, new, 1.0)
    rep("nove zdivo mezi sebou a s ohnistem: pruniku %d %s" % (len(c), c[:2] if c else ""), not c)
    boxes = [(frame_box(s, O, U, V), (s.z + s.sz / 2 - z0) / 100, (s.z - s.sz / 2 - z0) / 100) for s in new + ruin
             if abs(s.x - P(*ad["ref"])[0]) < 1500 and abs(s.y - P(*ad["ref"])[1]) < 1500]
    def top_at(a, c_):
        return max([t for (b, t, lo) in boxes if b[0] - 0.03 <= a <= b[1] + 0.03 and b[2] - 0.03 <= c_ <= b[3] + 0.03] + [-9.0])   # spary do 3 cm nevadi
    for pt in ad["parts"]:
        (a0, a1), (c0, c1) = pt["a"], pt["c"]; along_a = (a1 - a0) >= (c1 - c0)
        gaps = [(g_[1], g_[2]) for g_ in pt.get("gaps", [])]
        n_ok = n_all = 0; worst = 9.0; free = True
        p0, p1 = (a0, a1) if along_a else (c0, c1); q0, q1 = (c0, c1) if along_a else (a0, a1)
        for i in range(int((p1 - p0) / 0.05) + 1):
            p = p0 + 0.025 + i * 0.05
            if p > p1: break
            for q in (q0 + (q1 - q0) * 0.25, q0 + (q1 - q0) * 0.75):
                t = top_at(*((p, q) if along_a else (q, p)))
                if any(g0 + 0.03 < p < g1 - 0.03 for g0, g1 in gaps):
                    free &= t < 0.12; continue                                # v pruchodu nic vyssiho nez prah
                if any(g0 - 0.03 <= p <= g1 + 0.03 for g0, g1 in gaps): continue
                n_all += 1; n_ok += t >= pt["top"] - 0.03; worst = min(worst, t)
        over = max([(s.z + s.sz / 2 - z0) / 100 for s in new if "|%s|" % pt["id"] in s.id] + [0])
        rep("cast %s: vrch %.2f m na %.1f %% delky (nejniz %.2f), nove zdivo nejvys %.2f%s" % (
            pt["id"], pt["top"], 100.0 * n_ok / max(n_all, 1), worst, over, ", pruchod volny" if gaps else ""),
            n_ok / max(n_all, 1) >= 0.97 and over <= pt["top"] + 0.005 and free)
    # maltove jadro: zdi neprosvita (bod v ose zdi je v malte nebo v kameni, ktery osu protina) a malta neni videt
    # (u kazdeho rohu kusu malty je ve stejne vysce kamen teto zdi: malta je v kameni, ve spare nebo v dutine mezi lici)
    if ad.get("mortar"):
        mb = [(frame_box(s, O, U, V), (s.z + s.sz / 2 - z0) / 100, (s.z - s.sz / 2 - z0) / 100) for s in mortar]
        solid = boxes
        for pt in ad["parts"]:
            (a0, a1), (c0, c1) = pt["a"], pt["c"]; along_a = (a1 - a0) >= (c1 - c0)
            p0, p1 = (a0, a1) if along_a else (c0, c1); qm = ((c0 + c1) if along_a else (a0 + a1)) / 2
            gaps = [(g_[1], g_[2]) for g_ in pt.get("gaps", [])]
            n_all = n_hole = 0
            for i in range(int((p1 - p0 - 0.1) / 0.05)):
                p = p0 + 0.075 + i * 0.05
                if any(g0 - 0.05 <= p <= g1 + 0.05 for g0, g1 in gaps): continue
                a, c_ = (p, qm) if along_a else (qm, p)
                for kz in range(1, int(pt["top"] / 0.05) - 1):
                    z = kz * 0.05; n_all += 1
                    hit = any(b[0] <= a <= b[1] and b[2] <= c_ <= b[3] and lo <= z <= t for (b, t, lo) in mb) or \
                          any(b[0] <= a <= b[1] and b[2] + 0.02 <= c_ <= b[3] - 0.02 and lo <= z <= t for (b, t, lo) in solid)
                    n_hole += not hit
            rep("cast %s: zdi neprosvita, v ose pokryto %.1f %% (der %d z %d bodu)" % (pt["id"], 100 - 100.0 * n_hole / max(n_all, 1), n_hole, n_all),
                n_hole / max(n_all, 1) <= 0.01)
        bad = 0
        for (b, t, lo) in mb:
            for a in (b[0] + 0.01, b[1] - 0.01):
                for z in (lo + 0.01, t - 0.01):
                    c_ = (b[2] + b[3]) / 2
                    if not any(sb[0] - 0.3 <= a <= sb[1] + 0.3 and sb[2] - 0.3 <= c_ <= sb[3] + 0.3 and slo - 0.12 <= z <= st + 0.12 for (sb, st, slo) in solid): bad += 1   # vedle je kamen zdi
        rep("malta (%d kusu) lezi uvnitr zdi (kamen, spara, dutina mezi lici): rohu mimo %d" % (len(mb), bad), bad == 0)
    # --- krov (bez krytiny) a srub: sklon, podpory krokvi podle sad etap, sloupy, pruniky, otvory, neprosvita
    fr = next((f for f in S["data"].get("frames", []) if f["name"] == "Palac_Obydli_Krov"), None)
    lw = next((a for a in S["data"].get("addons", []) if a["name"] == "Palac_Obydli_Srub"), None)
    if fr and lw:
        kg, sg_ = groups["Palac_Obydli_Krov"], groups["Palac_Obydli_Srub"]
        kr = kg["stones"] + kg["loose"]; sr = sg_["stones"] + sg_["loose"]
        fb = lambda s: frame_box(s, O, U, V); zr = lambda s: ((s.z - s.sz / 2 - z0) / 100, (s.z + s.sz / 2 - z0) / 100)
        sup = sorted(fr["supports"], key=lambda q: -q["top"]); hi, lo_ = sup[0], sup[-1]
        deg = math.degrees(math.atan((hi["top"] - lo_["top"]) / abs(lo_["at"] - hi["at"])))
        rep("krov: sklon %.1f st. (16 +- 1)" % deg, 15 <= deg <= 17)
        rf = fr["rafters"]; nb = sum(q == "base" for q in rf["stages"])
        okst = lambda need, have: have == "base" or need == "final"          # zakladni dilec smi lezet jen na zakladnim
        topn = len(lw["walls"][0]["z"]) - 2; bad = []
        for i, (c_, stg) in enumerate(zip(rf["pos"], rf["stages"])):
            hv = [s for s in kr if "|VH." in s.id and fb(s)[0] <= c_ <= fb(s)[1] and okst(stg, s.stage)]
            sv = [s for s in kr if "|VS." in s.id and fb(s)[0] <= c_ <= fb(s)[1] and okst(stg, s.stage)]
            nv = [s for s in sr if "|N|" in s.id and int(s.id.split("|")[-1].split(".")[1]) == topn and fb(s)[0] <= c_ <= fb(s)[1] and okst(stg, s.stage)]
            if not (hv and sv and nv): bad.append(i)
        rep("krov: %d krokvi (%d v etape 1), kazda na 3 podporach sve etapy; bez podpory %s" % (len(rf["pos"]), nb, bad), not bad and nb >= 6)
        bad = []
        for s in kr:
            if "|VH." in s.id:
                b = fb(s); n_ = sum(1 for p in kr if "|VH|P" in p.id and b[0] - 0.01 <= (fb(p)[0] + fb(p)[1]) / 2 <= b[1] + 0.01)
                if n_ < 2: bad.append(s.id)
            if "|VS." in s.id:
                b = fb(s); st_ = [p for p in kr if "|VS|S" in p.id and b[0] - 0.11 <= (fb(p)[0] + fb(p)[1]) / 2 <= b[1] + 0.11 and okst(s.stage, p.stage)]
                if len(st_) < 2: bad.append(s.id)
        rep("krov: kazdy kus pozednice na 2+ sloupech, kazdy kus vaznice na 2 spalcich sve etapy %s" % bad, not bad)
        bad = []
        for p in kr:
            if "|VS|S" not in p.id: continue
            b = fb(p); a_, cc = (b[0] + b[1]) / 2, (b[2] + b[3]) / 2
            under = [s for s in sr if fb(s)[0] <= a_ <= fb(s)[1] and fb(s)[2] <= cc <= fb(s)[3] and abs(zr(s)[1] - zr(p)[0]) < 0.02 and okst(p.stage, s.stage)]
            if not under: bad.append(p.id)
        rep("krov: spalky vaznice stoji na vrchni rade srubu sve etapy %s" % bad, not bad)
        niches = [(13.35, 14.65), (18.35, 19.65)]; hb = [fb(s) for s in hearth]
        posts = [fb(p) for p in kr if "|VH|P" in p.id or "|VH|K" in p.id]
        bad = [b for b in posts if any(b[0] < n1 and b[1] > n0 for n0, n1 in niches) or any(b[0] < h[1] and b[1] > h[0] and b[2] < h[3] and b[3] > h[2] for h in hb)]
        rep("krov: sloupy a patni kameny mimo vyklenky strilen a ohniste", not bad)
        wood = kr + sr
        c = common.collisions(wood, ruin + new + hearth, 1.5)
        rep("drevo x zricenina, nove zdivo, ohniste: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        c = [q for q in common.collisions([s for s in kr if "|B" not in s.id and "|Z" not in s.id], [s for s in sr if "|G" not in s.id], 1.0)]
        rep("sloupy, pozednice, vaznice x srub: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        c = common.collisions([s for s in sr if "|G" in s.id], kr, 0.5)
        rep("prkenne stity x krov: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        allb = [(fb(s), zr(s)) for s in wood + new]
        blocked = lambda a0, a1, c0, c1, z0_, z1_: [1 for (b, (zl, zh)) in allb if b[0] < a1 and b[1] > a0 and b[2] < c1 and b[3] > c0 and zl < z1_ and zh > z0_]
        dn, dp = lw["walls"][0]["openings"][0], lw["walls"][1]["openings"][0]
        hN = min(z for z in lw["walls"][0]["z"] if z >= dn["z"][1] - 0.12); hP = min(z for z in lw["walls"][1]["z"] if z >= dp["z"][1] - 0.12)
        freeN = not blocked(dn["span"][0] + 0.01, dn["span"][1] - 0.01, lw["walls"][0]["at"] - 0.4, lw["walls"][0]["at"] + 0.4, 0.05, hN - 0.02)
        freeP = not blocked(lw["walls"][1]["at"] - 0.4, lw["walls"][1]["at"] + 0.4, dp["span"][0] + 0.01, dp["span"][1] - 0.01, 0.05, hP - 0.02)
        rep("vchod %.1f x %.2f m a dvere v pricce %.1f x %.2f m volne" % (dn["span"][1] - dn["span"][0], hN, dp["span"][1] - dp["span"][0], hP),
            freeN and freeP and hN >= 2.2 and hP >= 2.1)
        from zr_stavby.srub import row_pieces
        holes = n_all = 0
        for w in lw["walls"]:
            logs = [(fb(s), zr(s)) for s in sr if "|%s|" % w["id"] in s.id]
            for seg in w["segs"]:
                for k in range(seg["rows"][0], seg["rows"][1] + 1):
                    for (p0, p1) in row_pieces(w, seg, k):
                        for i in range(int((p1 - p0 - 0.1) / 0.1) + 1):
                            p = p0 + 0.05 + i * 0.1
                            for z in (w["z"][k] + 0.002, (w["z"][k] + w["z"][k + 1]) / 2, w["z"][k + 1] - 0.002):
                                a_, cc = (p, w["at"]) if w["dir"] == "a" else (w["at"], p); n_all += 1
                                holes += not any(b[0] <= a_ <= b[1] and b[2] <= cc <= b[3] and zl <= z <= zh for (b, (zl, zh)) in logs)
        rep("srub: steny souvisle od podezdivky po vrch mimo otvory (der %d z %d bodu)" % (holes, n_all), holes == 0)
        wb = max([zr(s)[1] for s in sr if "|N|" in s.id and s.stage == "base" and fb(s)[1] <= lw["walls"][1]["at"] + 0.01] + [0])
        rep("etapa 1: srub sine do %.2f m, svetnice v plne vysce, stity az v etape 2" % wb,
            wb < 1.25 and all(s.stage == "final" for s in sr if "|G" in s.id) and all(s.stage == "base" for s in sr if "|P|" in s.id or "|E|" in s.id))
        pu = next(q for q in fr["supports"] if q["id"] == "VS")
        rep("svetla vyska pod stredni vaznici %.2f m (>= 2.7)" % (pu["top"] - pu["sec"][1]), pu["top"] - pu["sec"][1] >= 2.7)
    # --- staveniste a etapa 1 (sestava base + site; navrh_palac_obydli_stred.md kap. 9.4)
    SITE = lambda n: n.startswith("Palac_Obydli_Stavenisko")    # vzpery a zebrik + hranice na nadvori (kazda samostatna stavba)
    sads = [a for a in S["data"].get("addons", []) if SITE(a["name"])]
    sa = dict(items=[q for a in sads for q in a["items"]]) if sads else None
    site = [s for n, g_ in groups.items() if SITE(n) for s in g_["stones"] + g_["loose"]]
    if sa and site and fr and lw:
        terr = S["terr"]; fb = lambda s: frame_box(s, O, U, V)
        pile = lambda s: s.id.split("|")[1] if s.id.count("|") >= 2 else ""            # S3, S4, S5a, S5b; vzpery a zebrik ""
        def zext(s):                                                # spodek a vrch dilce (m nad terenem pod jeho stredem)
            sp, cp = abs(math.sin(math.radians(s.pitch))), abs(math.cos(math.radians(s.pitch)))
            h = sp * s.sx / 2 + cp * s.sz / 2; zg = terr.z(s.x, s.y)
            return (s.z - h - zg) / 100, (s.z + h - zg) / 100
        ov = lambda a, b, m=0.0: a[0] < b[1] + m and a[1] > b[0] - m and a[2] < b[3] + m and a[3] > b[2] - m
        hang = []
        for s in site:
            lo, _ = zext(s)
            if abs(lo) <= 0.03: continue
            if not any(q is not s and pile(q) == pile(s) != "" and ov(fb(s), fb(q)) and
                       (lo - 0.03 <= zext(q)[1] <= lo + 0.06 or (abs(q.pitch) > 20 and zext(q)[0] < lo < zext(q)[1]))   # na kusu, nebo ve vidlici sikmych tyci (kozy)
                       for q in site): hang.append(s.id.split("|", 1)[1])
        rep("staveniste: nic nevisi (na terenu +-3 cm, na kusu sve hranice, ve vidlici koz) %s" % hang[:4], not hang)
        VH = next(q for q in fr["supports"] if q["id"] == "VH"); hp = VH["post"] / 2; post_top = VH["top"] - VH["sec"][1]
        free_posts = [ps for ps in VH["posts"] if not any(pc["stage"] == "base" and pc["span"][0] - 0.01 <= ps <= pc["span"][1] + 0.01 for pc in VH["pieces"])]
        braces = [q for q in sa["items"] if q["id"].startswith("V") and "p0" in q]
        def touches(q, ps):                                         # horni konec osy vzpery na lici sloupu (<= 2 cm), v jeho vysce
            a, c, z = q["p0"]
            if z > post_top: return False
            on_n = abs(c - (VH["at"] + hp)) <= 0.02 and abs(a - ps) <= hp
            on_s = abs(a - (ps + hp)) <= 0.02 and abs(c - VH["at"]) <= hp
            return on_n or on_s
        nbr = {ps: sum(1 for q in braces if touches(q, ps)) for ps in free_posts}
        rep("vzpery: sloupy bez pozednice base %s maji po 2 vzperach na lici %s" % (free_posts, nbr), free_posts and all(v == 2 for v in nbr.values()))
        others = [s for gname, g_ in groups.items() if not SITE(gname) for s in g_["stones"] + g_["loose"]
                  if not (gname.startswith("Palac_Obydli") and s.stage != "base")]          # v etape 1 stoji jen base (a vse bez etap)
        fu = S.get("furn") or {}                                    # vybaveni 06 (kovarna): skupiny jako u staveb
        others += [s for g_ in (fu.values() if isinstance(fu, dict) else []) for s in g_.get("stones", []) + g_.get("loose", [])]
        brace_post = lambda a, b: (a.id.split("|")[-1].startswith("V") and "|VH|P" in b.id)   # vzpera k lici sloupu = zamerny dotyk
        c = common.collisions(site, ruin + others, 1.5, skip=brace_post)
        rep("staveniste x zricenina, base, ostatni stavby a vybaveni: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        c = common.collisions(site, site, 1.0, skip=lambda a, b: pile(a) == pile(b) != "")
        rep("staveniste mezi sebou (mimo styk vrstev v hranici): pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
        zones = dict(sin=((10.95, 14.8), (3.2, 5.95)), zaprazi=((10.9, 21.4), (6.43, 8.8)), prulom=((14.5, 17.5), (8.8, 12.5)),
                     portal=((3.2, 5.8), (10.2, 12.5)), dvere_V=((25.9, 28.1), (10.2, 12.5)))
        blk = {k: [s.id.split("|", 1)[1] for s in site if ov(fb(s), (z[0][0], z[0][1], z[1][0], z[1][1])) and zext(s)[0] < 2.0] for k, z in zones.items()}
        rep("trasy a volne pasy (>= 1.2 m) bez staveniste: %s" % {k: v[:2] for k, v in blk.items() if v}, not any(blk.values()))
        piles = sorted(set(pile(s) for s in site) - {""}); tr = {}; nin = []
        for pn in piles:
            ps_ = [s for s in site if pile(s) == pn]; zs = []
            for s in ps_:
                for q in common.footprint(s): zs.append(terr.z(*q))
            tr[pn] = round((max(zs) - min(zs)) / 100, 3)
            if min(fb(s)[2] for s in ps_) < 10.25: nin.append(pn)
        rep("hranice na nadvori: teren pod hranici %s m (<= 0.15), od lice Palac_S %s" % (tr, "OK" if not nin else nin), all(v <= 0.15 for v in tr.values()) and not nin)
        RF = fr["rafters"]; want = dict(K=sum(q == "final" for q in RF["stages"]),
                                        Pozednice=sum(pc["stage"] == "final" for pc in VH["pieces"]),
                                        Vaznice=sum(pc["stage"] == "final" for pc in next(q for q in fr["supports"] if q["id"] == "VS")["pieces"]))
        fl = sorted(round(sg["span"][1] - sg["span"][0], 2) for w in lw["walls"] for sg in w["segs"] if sg.get("stage") == "final"
                    for k in range(sg["rows"][0], sg["rows"][1] + 1) if k not in w.get("half", []))
        fh = sum(1 for w in lw["walls"] for sg in w["segs"] if sg.get("stage") == "final" for k in range(sg["rows"][0], sg["rows"][1] + 1) if k in w.get("half", []))
        have = dict(K=sum(1 for s in site if "|S4|K" in s.id), Pozednice=sum(1 for s in site if s.id.endswith("|S4|Pozednice")),
                    Vaznice=sum(1 for s in site if s.id.endswith("|S4|Vaznice")))
        hl = sorted(round(s.sx / 100, 2) for s in site if "|S3|L" in s.id); hh = sum(1 for s in site if "|S3|H" in s.id)
        bd = {pn: sum(1 for s in site if s.id.split("|")[1:2] == [pn] and s.id.split("|")[-1][:1] == "P" and s.id.split("|")[-1][1:2].isdigit()) for pn in piles if pn.startswith("S5")}
        sys.path.insert(0, os.path.join(common.ROOT, "tools", "ruin")); import palac_spec
        nrow = palac_spec.obydli_stavenisko(S["layout"]["walls"])["counts"]["boards"]      # prken v jedne rade krytiny po spadu
        rep("pocty v hranicich = chybejici dilce final: %s, srub %d + %d pultramy (delky sedi: %s), prkna %s (kazda hranice >= %d)" % (have, len(hl), hh, hl == fl, bd, nrow),
            have == want and hl == fl and hh == fh and bd and all(v >= nrow for v in bd.values()))
        wrong = [s.id for s in site if s.stage != "site"] + [s.id for gname, g_ in groups.items() if not SITE(gname) for s in g_["stones"] + g_["loose"] if s.stage == "site"]
        uh = [s.stage for s in hearth if s.id.endswith("|U")]
        rep("etapa 2 (base + final) bez staveniste; uhli pod plotnou final %s" % uh, not wrong and uh == ["final"])
    for gname in ("Palac_Obydli_Kamen", "Palac_Obydli_Ohniste", "Palac_Obydli_Krov", "Palac_Obydli_Srub", "Palac_Obydli_Stavenisko",
                  "Palac_Obydli_Stavenisko_Kulatina", "Palac_Obydli_Stavenisko_Tramy", "Palac_Obydli_Stavenisko_Prkna",
                  "Palac_Obydli_Stavenisko_Kozy"):
        st = groups.get(gname, {}).get("stones", []) + groups.get(gname, {}).get("loose", [])
        sets = sorted(set(str(s.stage) for s in st))
        rep("%s: sady etap %s" % (gname, ", ".join(sets)), st and all(s.stage in ("base", "final", "site") for s in st))
    return ok


def check_brana(S):
    """strazni stanoviste nad branami (Brana_Straz_*): tramy v kapsach Brana_V a na vyrovnane korune Brana_J, podesta, zabradli;
    kriteria z new_designs/navrh_brana_straz.md, vysky absolutne (tools/ruin/brana_spec.py)"""
    groups, walls = S["groups"], S["walls"]
    ad = next((a for a in S["data"].get("addons", []) if a["name"] == "Brana_Straz_Podesta"), None)
    if not ad or "Brana_Straz_Podesta" not in groups: print("brana: Brana_Straz_Podesta neni v datech"); return False
    ok = True
    def rep(txt, good):
        nonlocal ok
        print("brana: %-70s %s" % (txt, "OK" if good else "CHYBA")); ok &= bool(good)
    sys.path.insert(0, os.path.join(common.ROOT, "05_constructions")); from zr_stavby.zdivo import frame_box
    from zr_stavby.podesta import deck_top
    sys.path.insert(0, os.path.join(common.ROOT, "tools", "ruin")); import brana_spec
    F = brana_spec.frame(S["layout"]["walls"]); O, U, V = ad["origin"], ad["u"], ad["v"]; fb = lambda s: frame_box(s, O, U, V)
    ruin = [s for n, w in walls.items() if n.startswith("Brana") or n.startswith("Hradba_V") for s in w["stones"] + w.get("loose", [])]
    pg = groups["Brana_Straz_Podesta"]; pod = pg["stones"] + pg["loose"]
    kg = groups.get("Brana_Straz_Kamen", {}); kam = kg.get("stones", []) + kg.get("loose", [])
    beams = [s for s in pod if "|B" in s.id]; planks = [s for s in pod if "|P" in s.id]; rails = [s for s in pod if "|Z" in s.id]
    z = ad["z"]; zt = deck_top(ad)
    c = common.collisions(pod + kam, ruin, 1.5)
    rep("podesta a vyrovnani x zricenina: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
    onwall = [s for s in beams if fb(s)[1] < F["face_v"]]                 # tram lezici na korune Brana_S (nesaha do Brana_V)
    pocket = [s for s in beams if s not in onwall]
    bad = [s.id for s in pocket if fb(s)[1] < F["face_v"] + 0.25 or fb(s)[1] > F["face_v"] + 0.38]
    rep("tramy: %d v kapsach Brana_V (ulozeni 0.25-0.38 m), %d na korune Brana_S %s" % (len(pocket), len(onwall), bad),
        not bad and len(beams) == len(ad["beams"]["pos"]))
    sl = [(fb(k), k.z + k.sz / 2) for k in kam if "|S|" in k.id] + [(fb(k), k.z + k.sz / 2) for k in walls["Brana_S"]["stones"]]
    gapw = []
    for s in onwall:
        b = fb(s); cc = (b[2] + b[3]) / 2; n_ = m_ = 0
        for i in range(int((b[1] - b[0]) / 0.2)):
            a_ = b[0] + 0.1 + i * 0.2; n_ += 1
            m_ += any(q[0] - 0.03 <= a_ <= q[1] + 0.03 and q[2] - 0.05 <= cc <= q[3] + 0.05 and z - 4 <= t <= z + 2 for (q, t) in sl)
        if m_ < n_ * 0.8: gapw.append((s.id, m_, n_))
    rep("tram na korune Brana_S lezi na kameni na 80+ %% delky %s" % gapw, not gapw)
    # nad a pod kapsou je kamen vnitrniho lice Brana_V (tram nelezi ve vzduchu ani v dire po celou vysku zdi)
    face = [(fb(s), s.z - s.sz / 2, s.z + s.sz / 2) for s in walls["Brana_V"]["stones"] + [k for k in kam if "|V|" in k.id]
            if s.cat in ("face", "frame", "crown") and fb(s)[0] < F["face_v"] + 0.3]
    bad = []
    for s in pocket:
        cc = (fb(s)[2] + fb(s)[3]) / 2
        under = max([t for (b, lo, t) in face if b[2] - 0.05 <= cc <= b[3] + 0.05 and t <= z + 2] + [0])
        if z - under > 4: bad.append((s.id, round(z - under)))
    rep("pod kazdym tramem je v Brana_V kamen lice nebo podlozeni (mezera cm) %s" % bad, not bad)
    lv = [(fb(s), s.z + s.sz / 2) for s in kam] + [(fb(s), s.z + s.sz / 2) for s in walls["Brana_J"]["stones"]]
    bad = []
    for s in beams:
        cc = (fb(s)[2] + fb(s)[3]) / 2
        tops = [t for (b, t) in lv if b[2] - 0.03 <= cc <= b[3] + 0.03 and b[1] > 0.2 and b[0] < 0.65 and t <= z + 2]
        if not tops or z - max(tops) > 4: bad.append((s.id, round(z - max(tops)) if tops else None))
    rep("zapadni konec kazdeho tramu lezi na vyrovnane korune Brana_J (mezera cm) %s" % bad, not bad)
    tops = [s.z + s.sz / 2 for s in planks]
    rep("podlaha vodorovna, vrch Z %.0f (prken %d)" % (zt, len(planks)), tops and max(abs(t - zt) for t in tops) < 0.5)
    (a0, a1), (c0, c1) = ad["planks"]["a"], ad["planks"]["c"]; miss = n_all = 0
    pb = [fb(s) for s in planks]
    for i in range(int((a1 - a0) / 0.1)):
        for j in range(int((c1 - c0 - 0.1) / 0.2)):
            a_, c_ = a0 + 0.05 + i * 0.1, c0 + 0.1 + j * 0.2; n_all += 1
            miss += not any(b[0] - 0.012 <= a_ <= b[1] + 0.012 and b[2] - 0.012 <= c_ <= b[3] + 0.012 for b in pb)   # spary do 2,4 cm nevadi
    rep("prkna pokryvaji podestu %.1f x %.1f m (mezer %d z %d bodu)" % (a1 - a0, c1 - c0, miss, n_all), miss <= n_all * 0.005)
    low = [s.id for s in pod + kam if "|Z" not in s.id and s.z - s.sz / 2 < brana_spec.B_LEVEL["bottom"] - 1]
    rep("prujezd pod podestou volny (nic pod Z %.0f)" % brana_spec.B_LEVEL["bottom"], not low)
    arch = max(s.z + s.sz / 2 for n in ("Brana_V", "Brana_J") for s in walls[n]["stones"] if s.cat == "frame")
    rep("spodek tramu Z %.0f je nad oblouky bran (vrch Z %.0f)" % (z, arch), z > arch + 1.5)
    rl = ad.get("rail"); posts = [s for s in rails if "|S" in s.id]
    if ad.get("rails"):
        rep("zabradli: %d sloupku, vrch %.2f m nad podlahou, sada %s" % (len(posts), rl["h"], sorted(set(str(s.stage) for s in rails))),
            posts and all(abs(s.z + s.sx / 2 - (zt + rl["h"] * 100)) < 3 for s in posts) and all(s.stage == "final" for s in rails))
    else: rep("zabradli do hradu se nestavi (v datech zadne)", not rails)
    # kryty z kulatiny: kuly stoji na kameni koruny, mezery, vrch, pruzory
    kd = next((a for a in S["data"].get("addons", []) if a["name"] == "Brana_Straz_Kryty"), None)
    if kd:
        kr = groups["Brana_Straz_Kryty"]["stones"] + groups["Brana_Straz_Kryty"]["loose"]
        for ln in kd["lines"]:
            st = sorted([s for s in kr if "|%s|K" % ln["id"] in s.id], key=lambda s: fb(s)[2] if ln["p0"][0] == ln["p1"][0] else fb(s)[0])
            along = (lambda s: (fb(s)[2], fb(s)[3])) if ln["p0"][0] == ln["p1"][0] else (lambda s: (fb(s)[0], fb(s)[1]))
            rb = [(fb(s), s.z + s.sz / 2) for n in ln["on"] for s in walls[n]["stones"]]
            hang = []; fl = ln.get("floor")
            for s in st:
                b = fb(s); a_, c_ = (b[0] + b[1]) / 2, (b[2] + b[3]) / 2; foot = s.z - s.sx / 2
                tops = [t for (q, t) in rb if q[0] - 0.08 <= a_ <= q[1] + 0.08 and q[2] - 0.08 <= c_ <= q[3] + 0.08] + ([fl] if fl is not None else [])
                if not tops or foot > max(tops) + 1: hang.append(s.id)
            gaps = [round(along(st[i + 1])[0] - along(st[i])[1], 3) for i in range(len(st) - 1)]
            big = [g_ for g_ in gaps if g_ > 0.03]
            full = [s for s in st if s.shape == "stake"]; slit = [s for s in st if s.shape != "stake"]
            hts = [(s.z + s.sx / 2 - zt) / 100 for s in full]; want = (ln["top"] - zt) / 100
            rep("kryt %s: %d kulu, vsechny stoji na kameni koruny nebo na podlaze %s" % (ln["id"], len(st), hang[:3]), st and not hang)
            rep("kryt %s: vrch %.2f-%.2f m nad podlahou (ma byt %.2f), pruzoru %d (rovne seriznute), mezer nad 3 cm %d" % (
                ln["id"], min(hts), max(hts), want, len(slit), len(big)),
                abs(min(hts) - want) < 0.07 and abs(max(hts) - want) < 0.07 and len(slit) == len(ln.get("slits", [])) and not big)
            rl_ = [s for s in kr if "|%s|R" % ln["id"] in s.id]
            sb = min([q["bottom"] for q in ln.get("slits", [])] + [9e9])
            c = common.collisions(rl_, ruin + pod, 2.0)
            rep("kryt %s: rahna (%d) pod pruzory a mimo kameny a podestu %s" % (ln["id"], len(rl_), c[:2] if c else ""),
                rl_ and not c and all(s.z + s.sz / 2 < sb - 1 for s in rl_))
            rep("kryt %s: sada %s" % (ln["id"], sorted(set(str(s.stage) for s in st))), all(s.stage == ln.get("stage") for s in st))
    for gname in ("Brana_Straz_Kamen", "Brana_Straz_Podesta"):
        st = groups.get(gname, {}).get("stones", []) + groups.get(gname, {}).get("loose", [])
        rep("%s: sady etap %s" % (gname, ", ".join(sorted(set(str(s.stage) for s in st)))), st and all(s.stage in ("base", "final", "site") for s in st))
    return ok


def check_vez(S):
    """platenny pristresek hlidky ve 2. patre veze (Vez_Pristresek, typ canvas_shelter): ulozeni kulatiny, kameny na korune,
    vule nad korunou, sklon, svetla vyska, pruhled strilnou, pruchody; kriteria z new_designs/navrh_vez_pristresek.md kap. 8"""
    groups, walls = S["groups"], S["walls"]
    ad = next((a for a in S["data"].get("addons", []) if a["name"] == "Vez_Pristresek"), None)
    if not ad or "Vez_Pristresek" not in groups: print("vez: Vez_Pristresek neni v datech"); return False
    ok = True
    def rep(txt, good):
        nonlocal ok
        print("vez: %-78s %s" % (txt, "OK" if good else "CHYBA")); ok &= bool(good)
    sys.path.insert(0, os.path.join(common.ROOT, "05_constructions")); from zr_stavby.zdivo import frame_box
    O, U, V = ad["origin"], ad["u"], ad["v"]; Z0 = ad["z_ref"]; fb = lambda s: frame_box(s, O, U, V)
    H = lambda z: (z - Z0) / 100
    g = groups["Vez_Pristresek"]; st = g["stones"] + g["loose"]; part = lambda k: [s for s in st if s.id.split("|")[1].startswith(k)]
    ruin = [s for n in ("Vez_J", "Vez_V", "Vez_S", "Vez_Z") for s in walls[n]["stones"] + walls[n].get("loose", [])]
    pat = groups["Vez_Patra"]["stones"] + groups["Vez_Patra"]["loose"]
    hz = lambda s: s.sz / 2 * abs(math.cos(math.radians(s.pitch))) + s.sx / 2 * abs(math.sin(math.radians(s.pitch)))
    RB = [(fb(s), H(s.z + hz(s))) for s in ruin]
    RB = [(b, z) for (b, z) in RB if b[1] > 0.5 and b[0] < 8.5 and b[3] > -1.0 and b[2] < 5.5 and z > 8.0]   # koruna pod pristreskem
    wood = [s for s in st if s.cat.startswith("wood")]; stones_ = [s for s in st if s.cat == "face"]
    ropes = [s for s in st if s.shape == "rope"]; canvas = [s for s in st if s.cat == "canvas"]
    ft = ad["floor_top"]
    c = common.collisions(wood + stones_, ruin, 1.0)
    rep("drevo a kameny x zricenina veze: pruniku nad 1 cm %d %s" % (len(c), c[:3] if c else ""), not c)
    feet = lambda a, b: (a.pitch > 60 or "|V" in a.id) and "|P" in b.id                  # paty kulu a vzper na prknech
    c = common.collisions(wood, pat, 1.0, skip=feet)
    rep("drevo x Vez_Patra (mimo pat na prknech): pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
    c = common.collisions(ropes, ruin + pat + wood, 1.0)
    rep("lana x zricenina, Vez_Patra a drevo: pruniku %d %s" % (len(c), c[:3] if c else ""), not c)
    # kuly a paty vzper nad stropnim tramem
    BV = groups and next(f for f in S["data"]["floors"] if f["name"] == "Vez_Patra")["beams"]["v"]
    posts = part("K"); braces = part("V")
    pv = [(s.id, round((fb(s)[2] + fb(s)[3]) / 2, 3)) for s in posts]
    bv = []
    for s in braces:
        b = fb(s); bv.append((s.id, round(b[3] - ad["braces"]["d"] / 2, 3)))
    bad = [(i, v) for i, v in pv + bv if min(abs(v - q) for q in BV) > 0.13]
    rep("kuly (%d) a paty vzper (%d) nad stropnim tramem (|v - tram| <= 0,13) %s" % (len(posts), len(braces), bad), not bad and posts and braces)
    low = [s.id for s in posts + braces if abs(H(s.z - (s.sx / 2) * math.sin(math.radians(s.pitch)) - ad["braces"]["d"] * 0) - ft) > 0.08 and s in posts]
    rep("paty kulu na prknech (vrch %.2f m)" % ft, not low)
    # hreben ve vidlicich, krokve na hrebeni a okapove tyci
    ridge = part("R"); eave = part("E"); raf = part("T"); heads = part("H")
    r_axis = ad["ridge"]["top"] - ad["ridge"]["d"] / 2
    rep("hreben: %d kusy, vrch %.2f m, %d hlav rozsochy" % (len(ridge), max(H(s.z) for s in ridge) + ad["ridge"]["d"] / 2, len(heads)),
        len(ridge) == len(ad["ridge"]["pieces"]) and all(abs(H(s.z) - r_axis) < 0.005 for s in ridge) and len(heads) == len(posts))
    # podkladni kameny: okapova tyc na nich, vrch = spodek tyce, ne ve vzduchu
    pads = part("P"); ev = ad["eave"]; e_bot = ev["bottom"]
    tops = {}
    for s in pads:
        k_ = s.id.split("|")[1][:2].rstrip("ab"); tops.setdefault(k_, []).append(s)
    under = []; high = []; onrod = 0
    for k_, ss in tops.items():
        topz = max(H(s.z + s.sz / 2) for s in ss); bot = min(ss, key=lambda s: s.z); b = fb(bot)
        cr = [z for (q, z) in RB if min(q[1], b[1]) - max(q[0], b[0]) >= 0.03 and min(q[3], b[3]) - max(q[2], b[2]) >= 0.03]
        gap = H(bot.z - bot.sz / 2) - max(cr) if cr else 9
        if abs(gap) > 0.02: under.append((k_, round(gap, 3)))
        hh = sum(s.sz for s in ss) / 100
        if hh > ad["pads"].get("max_h", 0.6): high.append((k_, round(hh, 2)))
        onrod += abs(topz - e_bot) < 0.005
    rep("okapova tyc lezi na %d podkladech (>= 4), vyska podkladu %s m" % (onrod, ", ".join("%.2f" % (sum(s.sz for s in v) / 100) for v in tops.values())),
        onrod >= 4 and not high)
    rep("podkladni kameny lezi na korune (kamen pod nimi zasahuje >= 3 cm; mezera nad 2 cm %s)" % under, not under)
    # vule nad korunou: krokve a platno
    def crown_at(u, v, r=0.03):
        t = [z for (q, z) in RB if q[0] - r <= u <= q[1] + r and q[2] - r <= v <= q[3] + r]
        return max(t) if t else None
    rf = ad["rafters"]; sl = ad["slope"]; e_top = ev["bottom"] + ev["d"]
    ax = lambda v: e_top + rf["d"] / 2 + sl * (v - ev["v"])
    gaps = []
    for u in rf["u"]:
        for i in range(int((rf["v"][1] - rf["v"][0]) / 0.02) + 1):
            v = rf["v"][0] + i * 0.02
            for du in (-rf["d"] / 2, 0, rf["d"] / 2):
                cz = crown_at(u + du, v, 0.0)
                if cz is not None: gaps.append((ax(v) - rf["d"] / 2 - cz, u, round(v, 2)))
    mg = min(gaps); cvd = ad["canvas"]
    ch = lambda v: e_top + rf["d"] + cvd["lift"] + sl * (v - ev["v"]) - cvd["sag"]
    cg = []
    for i in range(int((cvd["u"][1] - cvd["u"][0]) / 0.05) + 1):
        for j in range(int((cvd["v"][1] - cvd["v"][0]) / 0.05) + 1):
            u, v = cvd["u"][0] + i * 0.05, cvd["v"][0] + j * 0.05; cz = crown_at(u, v, 0.0)
            if cz is not None: cg.append((ch(v) - cz, round(u, 2), round(v, 2)))
    mc = min(cg)
    rep("vule nad korunou: krokve %.0f cm (u %.2f, v %.2f), platno (s prevesem %.0f cm) %.0f cm (u %.2f, v %.2f) (>= 5)" % (
        mg[0] * 100, mg[1], mg[2], cvd["sag"] * 100, mc[0] * 100, mc[1], mc[2]), mg[0] >= 0.05 and mc[0] >= 0.05)
    rep("sklon platna %.1f st. (>= 22)" % math.degrees(math.atan(sl)), math.degrees(math.atan(sl)) >= 22)
    rep("svetla vyska pod okapovou tyci %.2f m (>= 2,6)" % (e_bot - ft), e_bot - ft >= 2.6)
    # pokryti: plachta (mesh na miru) v pudorysu u 1,30-7,30, v 1,25-4,68
    cs = next(s for s in canvas if "|C" in s.id); b = fb(cs)
    a0, a1, c0, c1 = 1.30, 7.30, 1.25, ad["ridge"]["v"]
    cov = max(0, min(b[1], a1) - max(b[0], a0)) * max(0, min(b[3], c1) - max(b[2], c0)) / ((a1 - a0) * (c1 - c0))
    rep("plachta pokryva %.1f %% pudorysu u %.2f-%.2f, v %.2f-%.2f (>= 95)" % (cov * 100, a0, a1, c0, c1), cov >= 0.95)
    # pruhled strilnou Vez_J ve 2. patre: u = 5,5; h 9,45-10,5 od vnitrniho lice ven
    def inside(s, p):
        (c_, R, e) = common.obb(s); d = [p[i] - c_[i] for i in range(3)]
        return all(abs(sum(d[i] * R[k][i] for i in range(3))) <= e[k] for k in range(3))
    Wp = lambda u, v, h: (O[0] + (U[0] * u + V[0] * v) * 100, O[1] + (U[1] * u + V[1] * v) * 100, Z0 + h * 100)
    hit = set()
    for hh in (9.45, 9.8, 10.15, 10.5):
        for i in range(31):
            v = 3.0 - i * 0.1; p = Wp(5.5, v, hh)
            hit |= {s.id for s in st if s.cat != "canvas" and inside(s, p)}
    rep("pruhled strilnou Vez_J (u 5,5; h 9,45-10,5; v 3,0 az -0,0) nekrizi nic %s" % sorted(hit), not hit)
    # pruchody
    pu = sorted((fb(s)[0], fb(s)[1]) for s in posts); bu = sorted((fb(s)[0], fb(s)[1]) for s in braces)
    inner_v = TSI = next(f for f in S["data"]["floors"] if f["name"] == "Vez_Patra")["inner"]
    p1 = pu[2][0] - pu[1][1]; p2 = inner_v[1] - pu[2][1]; p3 = bu[1][0] - bu[0][1]
    hatch = next(f for f in S["data"]["floors"] if f["name"] == "Vez_Patra")["hatches"]["2"]
    rep("pruchody: prostredni-vychodni kul %.2f, vychodni kul-Vez_V %.2f, mezi vzperami %.2f m (>= 1,2); pata vzpery k otvoru schodu %.2f m" % (
        p1, p2, p3, hatch[0] - bu[1][1]), min(p1, p2, p3) >= 1.2 and bu[1][1] < hatch[0])
    # stit: od lice Vez_Z, horni okraj na krajni krokvi
    gs = next(s for s in canvas if "|G" in s.id); gb = fb(gs)
    top_ok = abs(H(gs.z + gs.sz / 2) - (ax(ad["gable"]["v"][1]) - rf["d"] / 2)) < 0.02
    rep("stit %.0f cm od vnitrniho lice Vez_Z (>= 5), horni okraj na spodku krajni krokve %s" % ((gb[0] - inner_v[0]) * 100, "ano" if top_ok else "ne"),
        gb[0] - inner_v[0] >= 0.05 and top_ok)
    # ovazani krokvi pod platnem (platno lezi pres ne), kotevni kameny lan na korune
    ch0 = lambda v: e_top + rf["d"] + cvd["lift"] + sl * (v - ev["v"])
    lsh = [s for s in st if s.shape == "lashing" and s.id.split("|")[1][:2] in ("LT", "LE")]
    over = [(s.id, round((H(s.z) + s.sz / 200 - ch0((fb(s)[2] + fb(s)[3]) / 2)) * 100, 1)) for s in lsh]
    over = [o for o in over if o[1] > 0]
    rep("ovazani krokvi (%d) pod platnem (vycniva nad platno %s)" % (len(lsh), over), lsh and not over)
    anc = part("A"); bad = []
    for s in anc:
        b = fb(s); cr = [z for (q, z) in RB if min(q[1], b[1]) - max(q[0], b[0]) >= 0.03 and min(q[3], b[3]) - max(q[2], b[2]) >= 0.03]
        if not cr or abs(H(s.z - s.sz / 2) - max(cr)) > 0.02: bad.append(s.id)
    rep("kotevni kameny lan (%d) lezi na korune Vez_J %s, lan %d" % (len(anc), bad, len(ad["ropes"])), len(anc) == len(ad["ropes"]) and not bad)
    rep("sady etap: %s" % sorted(set(str(s.stage) for s in st)), all(s.stage == "base" for s in st))
    return ok


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--layout"); ap.add_argument("--only")
    a = ap.parse_args()
    only = a.only.split(",") if a.only else ["openings", "floating", "ostroh", "palac", "obydli", "brana", "vez"]
    S = common.state(a.layout, with_constructions=bool({"ostroh", "palac", "obydli", "brana", "vez"} & set(only)))
    res = {}
    if "openings" in only: res["openings"] = check_openings(S)
    if "floating" in only: res["floating"] = check_floating(S)
    if "ostroh" in only: res["ostroh"] = check_ostroh(S)
    if "palac" in only: res["palac"] = check_palac(S)
    if "obydli" in only: res["obydli"] = check_obydli(S)
    if "brana" in only: res["brana"] = check_brana(S)
    if "vez" in only: res["vez"] = check_vez(S)
    print("\nSOUHRN: " + ", ".join("%s %s" % (k, "OK" if v else "CHYBA") for k, v in res.items()))
    sys.exit(0 if all(res.values()) else 1)


if __name__ == "__main__":
    main()
