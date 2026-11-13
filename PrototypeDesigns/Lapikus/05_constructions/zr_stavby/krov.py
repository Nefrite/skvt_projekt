"""krov u ostrohu (typ fan_roof): sloupy, pricka, vejir tramu na snizenou hradbu, bocni tramy, krytina.
ostroh_geom = spolecna geometrie (vyska koruny, tramy, pole krytiny) i pro kamennou dostavbu (dostavba.py)."""
import math, random
from zrlib.config import WOOD_FINISH
from zrlib.geom import crc, plane_fit
from zrlib.stones import Stone

MIN_SLOPE = 0.06                         # nejmensi spad bocnich tramu (krytina musi odvodnit)
ROOF_MARGIN = 3.0                        # cm: zdivo pod strechou zustava o tolik pod vrchem tramu (late lezi na tramech)


def ostroh_geom(fr, walls, cache=None):
    """spolecna geometrie krovu u ostrohu pro krov (Ostroh_Krov) i kamennou dostavbu (Ostroh_Dostavba):
    vyska koruny hradby WT, vrch pricky ct, tramy (vejir + bocni) a pole krytiny s rovinami.
    Tram lezi spodkem na pricce a ve zlabku: u vnitrniho lice hradby je dno zlabku (vrch zdi - d), ven klesa ve sklonu tramu
    a za vnejsim licem tram presahuje (okap). Bocni tramy (sides) jsou rovnobezne s krajnim tramem vejire, zacinaji
    v dostavbe ZBudova_V (spodek ve vysce ct) a konci na hradbe / na ZBudova_S."""
    if cache is not None and fr["name"] in cache: return cache[fr["name"]]
    bw, bh = fr["beam"][0] * 100, fr["beam"][1] * 100; T = fr["wall_t"] * 100
    wall_st = walls.get(fr["wall"], {}).get("stones", [])
    if not wall_st: return None
    # vrch snizene hradby u kazdeho tramu (bez kamenu snizenych ve zlabku)
    tops = []
    for b in fr["beams"]:
        ex, ey = b["wall_pt"]
        near = [s for s in wall_st if s.cat in ("face", "core", "crown") and ".n1" not in s.id
                and math.hypot(s.x - ex, s.y - ey) < T / 2 + 80]
        tops.append(max(s.z + s.sz / 2 for s in near) if near else None)
    ok = [t for t in tops if t is not None]
    if not ok: return None
    WT = max(set(round(t) for t in ok), key=[round(t) for t in ok].count)      # zarovnana koruna: nejcastejsi vyska
    d = fr["notches"][0]["d"] * 100
    nb_in = WT - d                                    # dno zlabku u vnitrniho lice
    ct = nb_in + fr["rise"] * 100                      # vrch pricky = spodek tramu u pricky
    so = fr.get("start_over", 0.3) * 100; oh = fr.get("overhang", 0.6) * 100
    tl = fr.get("top_line")
    def a_top(S, D):
        """kde tram (a krytina) zacina: na hornim okraji krytiny rovnobeznem se ZBudova_V, jinak so pred prickou"""
        if not tl: return -so
        (px, py), (nx, ny) = tl["p"], tl["n"]
        o_s = (S[0] - px) * nx + (S[1] - py) * ny; dn = D[0] * nx + D[1] * ny
        return (tl["off"] * 100 - o_s) / dn if abs(dn) > 0.2 else -so
    ruin = [st for w in walls.values() for st in w["stones"] + w.get("loose", []) if st.cat in ("face", "core", "crown", "frame")]
    def fit(sx_, sy_, dx, dy, sl, a1):
        """bocni tram lezi na koruně zriceniny (ta se pro nej nesnizuje): sklon nejvys sl, ale spodek tramu nad vsemi kameny
        pod nim; kdyz by musel byt skoro vodorovny (kamen vys nez pricka), tram skonci pred tim kamenem"""
        lx, ly = -dy, dx; hw = bw / 2 + 2.0; need = []
        for st in ruin:
            rx, ry = st.x - sx_, st.y - sy_
            if abs(rx * dx + ry * dy - a1 / 2) > a1 / 2 + 150 or abs(rx * lx + ry * ly) > 150: continue
            ya = math.radians(st.yaw); c, s_ = math.cos(ya), math.sin(ya)
            cs = [(rx + c * i * st.sx / 2 - s_ * j * st.sy / 2, ry + s_ * i * st.sx / 2 + c * j * st.sy / 2) for i, j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            la = [q[0] * lx + q[1] * ly for q in cs]; aa = [q[0] * dx + q[1] * dy for q in cs]
            if max(la) < -hw or min(la) > hw or max(aa) < 0 or min(aa) > a1: continue
            r_, p_ = math.radians(st.roll), math.radians(st.pitch)
            top = st.z + abs(math.sin(p_)) * st.sx / 2 + abs(math.sin(r_)) * st.sy / 2 + abs(math.cos(p_) * math.cos(r_)) * st.sz / 2
            need.append((min(aa), max(aa), top))
        for a0_, am, top in sorted(need):
            if a0_ > a1: break
            if am <= 1: continue
            s_need = (ct - 2.0 - top) / am
            if s_need >= MIN_SLOPE: sl = min(sl, s_need)
            else: a1 = min(a1, max(a0_ - 3.0, 0.0))                  # vyssi kamen: tram konci pred nim
        return sl, a1
    def beam(gid, b, Tw, side=False):
        sx_, sy_ = b["start"]; ex, ey = b["wall_pt"]
        dx, dy = ex - sx_, ey - sy_; dl = math.hypot(dx, dy); dx, dy = dx / dl, dy / dl
        sl = b["slope"]
        a1 = dl + (Tw / 2) / max(b.get("sin", 1.0), 0.35) + oh                 # od pricky (cm) pres zed az za vnejsi lic
        if side: sl, a1 = fit(sx_, sy_, dx, dy, sl, a1)
        ang = math.atan(sl)
        return dict(id=gid, S=(sx_, sy_), D=(dx, dy), sl=sl, at=a_top((sx_, sy_), (dx, dy)), a1=a1,
                    bottom=lambda a, sl=sl: ct - sl * a, top=lambda a, sl=sl, ang=ang: ct - sl * a + bh / math.cos(ang))
    main = [beam("B%d" % i, b, T) for i, (b, wt) in enumerate(zip(fr["beams"], tops)) if wt is not None]   # hradba u konce chybi -> bez tramu
    geo = list(main)
    for sd in fr.get("sides", []):
        sg = [beam("%s%d" % (sd["id"], j), b, b.get("wall_t", fr["wall_t"]) * 100, side=True) for j, b in enumerate(sd["beams"])]
        geo = (sg[::-1] + geo) if sd.get("ref", 0) == 0 else (geo + sg)   # poradi v prostoru: sever ... vejir ... jih
    # pole krytiny mezi sousednimi tramy: rovina spodku prken z = c0 + cx*x + cy*y
    rf = fr.get("roof") or {}
    lh = rf.get("lath", (0.05, 0.06))[0] * 100
    sectors = []
    for k in range(len(geo) - 1):
        g1, g2 = geo[k], geo[k + 1]
        e1, e2 = g1["a1"] - 5, g2["a1"] - 5
        pts = [(_pt(g1, g1["at"]), g1["top"](g1["at"]) + lh), (_pt(g2, g2["at"]), g2["top"](g2["at"]) + lh),
               (_pt(g1, e1), g1["top"](e1) + lh), (_pt(g2, e2), g2["top"](e2) + lh)]
        sectors.append(dict(g1=g1, g2=g2, e1=e1, e2=e2, plane=plane_fit(pts)))
    G = dict(WT=WT, ct=ct, d=d, bw=bw, bh=bh, lh=lh, geo=geo, main=main, sectors=sectors)
    if cache is not None: cache[fr["name"]] = G
    return G


def _pt(g, a):
    """bod na ose tramu ve vzdalenosti a (cm, vodorovne od zacatku tramu na pricce)"""
    return (g["S"][0] + g["D"][0] * a, g["S"][1] + g["D"][1] * a)


def roof_under(G, x, y, margin=ROOF_MARGIN):
    """vyska (cm), pod kterou musi zustat zdivo pod strechou v bode x, y: pod vrchem tramu v poli krytiny (late lezi
    na tramech), v miste tramu pod jeho spodkem. Mimo krov None."""
    cr = lambda g: g["D"][0] * (y - g["S"][1]) - g["D"][1] * (x - g["S"][0])
    best = None
    for sc in G["sectors"]:
        c1, c2 = cr(sc["g1"]), cr(sc["g2"])
        if c1 * c2 <= 0: best = sc; break
        dd = min(abs(c1), abs(c2))
        if best is None or dd < best[0]: best = (dd, sc)
    if best is None: return None
    sc = best if isinstance(best, dict) else best[1]
    c0, cx, cy = sc["plane"]
    z = c0 + cx * x + cy * y - G["lh"] - margin
    for g in G["geo"]:
        a = (x - g["S"][0]) * g["D"][0] + (y - g["S"][1]) * g["D"][1]
        if g["at"] - 2 <= a <= g["a1"] + 2 and abs(cr(g)) < G["bw"] / 2 + 1.5:
            z = min(z, g["bottom"](a) - 1.0)
    return z


def build_fan_roof(fr, P, walls, terr, cache=None):
    """zastreseni u ostrohu: 2 sloupy, pricka (vaznice), paprskovite tramy na snizenou hradbu (ve zlabcich koruny),
    bocni tramy nad kliny u ZBudova_V a krytina. Data z ostroh_spec.py a gen_constructions.py (constructions.json -> frames)."""
    out = []
    fin = fr.get("finish", {}); WC = lambda part: WOOD_FINISH.get(fin.get(part, "tar"), "wood_tar")
    G = ostroh_geom(fr, walls, cache)
    if not G: return out
    ct, bw, bh = G["ct"], G["bw"], G["bh"]
    ch_w, ch_h = fr["crossbeam"][0] * 100, fr["crossbeam"][1] * 100
    (p1x, p1y), (p2x, p2y) = fr["posts"]
    ux, uy = p1x - p2x, p1y - p2y; ul = math.hypot(ux, uy); ux, uy = ux / ul, uy / ul
    yaw_c = math.degrees(math.atan2(uy, ux)); ov = fr.get("crossbeam_over", 0.45) * 100
    cx, cy = (p1x + p2x) / 2, (p1y + p2y) / 2
    out.append(Stone("%s|C" % fr["name"], WC("crossbeam"), cx, cy, ct - ch_h / 2, yaw_c, ul + 2 * ov, ch_w, ch_h))
    ps = fr.get("post", 0.28) * 100; kn = fr.get("knee", {})
    for j, (px, py) in enumerate(fr["posts"]):
        zg = terr.z(px, py) - 10; ztop = ct - ch_h
        out.append(Stone("%s|P%d" % (fr["name"], j), WC("posts"), px, py, (zg + ztop) / 2, yaw_c, ps, ps, ztop - zg))
        if kn:     # sikma vzpera sloup -> pricka (45 st., v rovine pricky, ke stredu nebo ven)
            l_ = kn.get("l", 0.7) * 100; w_ = kn.get("w", 0.14) * 100; sg = -1 if j == 0 else 1
            if kn.get("out"): sg = -sg                  # vzpera ven pod presah pricky
            kx, ky = px + ux * sg * l_ / 2, py + uy * sg * l_ / 2
            yaw_k = yaw_c + (0 if sg > 0 else 180)
            out.append(Stone("%s|K%d" % (fr["name"], j), WC("knee"), kx, ky, ztop - l_ / 2 + w_ * 0.2, yaw_k, l_ * 1.41 + w_ * 0.5, w_, w_, pitch=45.0))
    for g in G["geo"]:
        sl = g["sl"]; a0, a1 = g["at"], g["a1"]
        z0, z1 = g["bottom"](a0), g["bottom"](a1)
        mx, my = _pt(g, (a0 + a1) / 2)
        ang = math.atan(sl); L = math.hypot(a1 - a0, z0 - z1)
        zc = (z0 + z1) / 2 + bh / 2 / math.cos(ang)
        yaw_b = math.degrees(math.atan2(-g["D"][1], -g["D"][0]))     # osa X kamene: od zdi (nize) k pricce (vys) -> pitch kladny
        out.append(Stone("%s|%s" % (fr["name"], g["id"]), WC("beams"), mx, my, zc, yaw_b, L, bw, bh, pitch=math.degrees(ang)))
    if fr.get("roof") and len(G["geo"]) >= 2:
        out += _fan_roof_cover(fr, G, WC)
    return out


def _fan_roof_cover(fr, G, WC):
    """krytina krovu: latě napric tramy, dehtovana prkna po spadu (rovnobezne pasy v kazdem poli mezi tramy, krajni
    kratsi do klinu), listy pres spary, kryci prkno pres kazdy tram."""
    out = []; rf = fr["roof"]
    lh, lw = rf.get("lath", (0.05, 0.06)); lh *= 100; lw *= 100
    bt = rf.get("board_t", 0.035) * 100; bwmin, bwmax = rf.get("board_w", (0.22, 0.30)); gap = rf.get("gap", 0.015) * 100
    btw, bth = rf.get("batten", (0.06, 0.035)); btw *= 100; bth *= 100
    rng = random.Random(crc("%s|roof" % fr["name"]))
    def isect(p, d, q, e):                                # parametr t na primce p + t*d, kde protne primku q + u*e
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-9: return None
        return ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
    zb = lambda g, a: g["top"](a) + lh                      # spodek prken nad trámem (na latich)
    for k, sc in enumerate(G["sectors"]):
        g1, g2, e1, e2 = sc["g1"], sc["g2"], sc["e1"], sc["e2"]
        c0, cx, cy = sc["plane"]
        zpl = lambda x, y: c0 + cx * x + cy * y
        dx, dy = g1["D"][0] + g2["D"][0], g1["D"][1] + g2["D"][1]; dl = math.hypot(dx, dy); d = (dx / dl, dy / dl); l = (-d[1], d[0])
        O = ((g1["S"][0] + g2["S"][0]) / 2, (g1["S"][1] + g2["S"][1]) / 2)
        pitch = math.degrees(math.atan(cx * d[0] + cy * d[1])); roll = math.degrees(math.atan(cx * l[0] + cy * l[1]))
        yaw = math.degrees(math.atan2(d[1], d[0]))
        t1p, t2p = _pt(g1, g1["at"]), _pt(g2, g2["at"])
        topP, topE = t1p, (t2p[0] - t1p[0], t2p[1] - t1p[1])
        eavP, eavE = _pt(g1, e1), (_pt(g2, e2)[0] - _pt(g1, e1)[0], _pt(g2, e2)[1] - _pt(g1, e1)[1])
        mid = [sum(q[i] for q in (t1p, t2p, _pt(g1, e1), _pt(g2, e2))) / 4 for i in (0, 1)]
        crs = lambda g, q: g["D"][0] * (q[1] - g["S"][1]) - g["D"][1] * (q[0] - g["S"][0])
        sig = {id(g): (1 if crs(g, mid) > 0 else -1) for g in (g1, g2)}
        def run(c, w_=0.0):
            """rozsah t podel d pro pas se stredem v bocni vzdalenosti c (cm) a sirce w_ - pas zacina, jakmile se do pole
            dostane jeho VNITRNI hrana (jinak mezi krajnim prknem a tramem zustane klinova dira); na tramu ho prekryje
            kryci prkno. Plati i pro rovnobezne tramy (bocni pole)."""
            p0 = (O[0] + l[0] * c, O[1] + l[1] * c)
            ci = c - (w_ / 2 if c > 0 else -w_ / 2) if c else 0.0
            pi = (O[0] + l[0] * ci, O[1] + l[1] * ci)
            t0, t1 = isect(p0, d, topP, topE), isect(p0, d, eavP, eavE)
            if t0 is None or t1 is None: return p0, 0.0, None
            for g in (g1, g2):                               # vnitrni hrana pasu na vnitrni strane obou tramu
                f0 = crs(g, pi) * sig[id(g)]; f1 = (g["D"][0] * d[1] - g["D"][1] * d[0]) * sig[id(g)]
                if abs(f1) < 1e-6:
                    if f0 < 0: return p0, 0.0, None
                elif f1 > 0: t0 = max(t0, -f0 / f1)
                else: t1 = min(t1, -f0 / f1)
            return p0, t0, t1
        # pasy prken od stredu pole na obe strany
        boards = []
        w0 = rng.uniform(bwmin, bwmax) * 100
        p0, t0, t1 = run(0.0, w0)
        if t1 is not None and t1 - t0 >= 40: boards.append((0.0, w0, p0, t0, t1))
        for sg in (1, -1):
            edge = w0 / 2 + gap
            while edge < 600:
                w_ = rng.uniform(bwmin, bwmax) * 100; cc = sg * (edge + w_ / 2)
                p0, t0, t1 = run(cc, w_)
                if t1 is None or t1 - t0 < 40: break           # pas uz je mimo pole (za tramem)
                boards.append((cc, w_, p0, t0, t1)); edge += w_ + gap
        boards.sort()
        lift = bt if k % 2 else 0.0                      # sousedni pole se u tramu prekryvaji -> liche pole o tloustku prkna vys
        for j, (cc, w_, p0, t0, t1) in enumerate(boards):
            tm = (t0 + t1) / 2; x, y = p0[0] + d[0] * tm, p0[1] + d[1] * tm
            out.append(Stone("%s|R%s|K%d" % (fr["name"], _sid(sc), j), WC("roof_boards"), x, y, zpl(x, y) + bt / 2 + lift, yaw,
                             t1 - t0, w_ - 0.5, bt, pitch, roll))
        # listy pres spary mezi prkny (prekryv sousednich pasu)
        for j in range(len(boards) - 1):
            ca, wa, pa, ta0, ta1 = boards[j]; cb, wb, pb, tb0, tb1 = boards[j + 1]
            c = (ca + wa / 2 + cb - wb / 2) / 2; t0, t1 = max(ta0, tb0), min(ta1, tb1)
            if t1 - t0 < 40: continue
            p0 = (O[0] + l[0] * c, O[1] + l[1] * c); tm = (t0 + t1) / 2; x, y = p0[0] + d[0] * tm, p0[1] + d[1] * tm
            out.append(Stone("%s|R%s|L%d" % (fr["name"], _sid(sc), j), WC("roof_battens"), x, y, zpl(x, y) + bt + bth / 2 + lift, yaw,
                             t1 - t0, btw, bth, pitch, roll))
        # latě pod prkny napric polem (na tramech): u horniho okraje, dve uprostred, u zdi a u okapu
        for r_, f in enumerate(rf.get("lath_rows", (0.04, 0.35, 0.65, 0.9, 1.0))):
            a1_ = g1["at"] + 15 + (e1 - 25 - g1["at"] - 15) * f; a2_ = g2["at"] + 15 + (e2 - 25 - g2["at"] - 15) * f
            q1, q2 = _pt(g1, a1_), _pt(g2, a2_)
            x, y = (q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2; ln = math.hypot(q2[0] - q1[0], q2[1] - q1[1]) + 25
            ylat = math.degrees(math.atan2(q2[1] - q1[1], q2[0] - q1[0]))
            out.append(Stone("%s|R%s|T%d" % (fr["name"], _sid(sc), r_), WC("roof_laths"), x, y, (zb(g1, a1_) + zb(g2, a2_)) / 2 - lh / 2,
                             ylat, ln, lw, lh))
    # kryci prkno pres kazdy tram (spoj dvou poli a prekryv krajnich prken)
    cw = rf.get("cover_w", 0.36) * 100
    for g in G["geo"]:
        a0, a1_ = g["at"], g["a1"] - 5; L = a1_ - a0
        q = _pt(g, (a0 + a1_) / 2); ang = math.atan(g["sl"])
        out.append(Stone("%s|R|S%s" % (fr["name"], g["id"]), WC("roof_battens"), q[0], q[1], g["top"]((a0 + a1_) / 2) + lh + 2 * bt + bt / 2,
                         math.degrees(math.atan2(-g["D"][1], -g["D"][0])), L / math.cos(ang), cw, bt, math.degrees(ang)))
    return out


def _sid(sc):
    return "%s-%s" % (sc["g1"]["id"], sc["g2"]["id"])
