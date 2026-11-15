"""run_checks.py - kontroly zriceniny a staveb bez Unrealu (stejny stav jako v UE: teren z levelu, rucni upravy).
python run_checks.py [--layout <ruin_layout.json>] [--only openings,floating,ostroh,palac,obydli]

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
        rep("kovadlina %.2f m pred vyhni (0,9-1,1)" % d_an, 0.9 <= d_an <= 1.1)
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
    new = g["stones"] + g["loose"]; hg = groups.get("Palac_Obydli_Ohniste", {}); hearth = hg.get("stones", []) + hg.get("loose", [])
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
    for gname in ("Palac_Obydli_Kamen", "Palac_Obydli_Ohniste"):
        st = groups.get(gname, {}).get("stones", []) + groups.get(gname, {}).get("loose", [])
        sets = sorted(set(str(s.stage) for s in st))
        rep("%s: sady etap %s" % (gname, ", ".join(sets)), st and all(s.stage in ("base", "final", "site") for s in st))
    return ok


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--layout"); ap.add_argument("--only")
    a = ap.parse_args()
    only = a.only.split(",") if a.only else ["openings", "floating", "ostroh", "palac", "obydli"]
    S = common.state(a.layout, with_constructions=bool({"ostroh", "palac", "obydli"} & set(only)))
    res = {}
    if "openings" in only: res["openings"] = check_openings(S)
    if "floating" in only: res["floating"] = check_floating(S)
    if "ostroh" in only: res["ostroh"] = check_ostroh(S)
    if "palac" in only: res["palac"] = check_palac(S)
    if "obydli" in only: res["obydli"] = check_obydli(S)
    print("\nSOUHRN: " + ", ".join("%s %s" % (k, "OK" if v else "CHYBA") for k, v in res.items()))
    sys.exit(0 if all(res.values()) else 1)


if __name__ == "__main__":
    main()
