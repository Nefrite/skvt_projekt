"""
build_constructions.py - dodatecne stavby zriceniny ("druhe zabydleni"), Unreal Editor 5.8

Stavi zvlast od zriceniny (03_ruin/blocks/build_ruin_blocks.py), takze se da ladit bez pregenerovani hradu:
  - drevene vestavby: tramy v kapsach, prkna, pruvlak se sloupy, provizorni schody, podesta (constructions.json -> floors)
  - krov u ostrohu: sloupy, pricka, paprskovite a bocni tramy, krytina (constructions.json -> frames)
  - kamenne dostavby z kamene rozvalin (constructions.json -> addons): jednoradove zdi na korunach zriceniny az pod strechu
  - prkenne podlahy na podvalech (constructions.json -> addons, typ plank_floor)
  - volna sut na zemi u zdi (samostatne actory, lze posouvat a mazat); v obyvane casti u ostrohu uklizena
Zricenina zustava ve 03: zdi, otvory, kapsy pro tramy, kamenna dlazba. Dostavby ji nemeni, jen na ni stoji.

Pouziti v UE: Tools -> Execute Python Script ->
  - stavby/<Stavba>.py      jen jedna stavba (Vez_Patra.py, Ostroh_Krov.py, Ostroh_Dostavba.py, Ostroh_Podlaha.py, Sut.py) - ostatni se nesmazou ani neprestavi
  - build_constructions.py  vsechny stavby najednou
  - MODE = "build"   postavit (smaze jen sve actory s tagem Zricenina_Stavby)
  - MODE = "capture" ulozit rucne smazane / posunute kusy do constructions_edits.json
  - MODE = "freeze"  (volitelne) sut bez fyziky, staticka
Sut ma trvalou fyziku (RUBBLE_PHYSICS), hrac s ni muze hnout; hmotnost podle objemu kamene (STONE_PHYSICS v build_ruin_blocks.py).
Usazeni: Simulate (Alt+S), vyber kameny (tag Ruin_Physics), K = Keep Simulation Changes, capture.
Usazene kameny (ulozena poloha) ve hre spi, dokud do nich nekdo nestrci.
Potrebuje: 03_ruin/blocks (build_ruin_blocks.py, ruin_layout.json, terrain_from_level.json po buildu zriceniny).
Mimo UE: python build_constructions.py  -> statistika
"""
import importlib.util, json, os, sys

# ------------------------------------------------------------------ nastaveni
MODE = "build"
DATA_PATH = None                         # None = constructions.json vedle skriptu
RUIN_DIR = None                          # None = ../03_ruin/blocks (vedle slozky 05_constructions)
CONSTR_TAG = "Zricenina_Stavby"
MAT_WOOD = ["/Game/StarterContent/Materials/M_Wood_Oak.M_Wood_Oak", "/Game/StarterContent/Materials/M_Wood_Pine.M_Wood_Pine"]
ONLY = None                              # napr. ["Vez_Patra"], ["Ostroh_Dostavba"] nebo ["Sut"] = postavit jen tuto cast
RUBBLE_PHYSICS = True                    # kameny suti maji trvalou fyziku (hmotnost podle objemu); False = staticke


def _here():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.path.dirname(DATA_PATH) if DATA_PATH else os.getcwd()


def _ruin_dir():
    if RUIN_DIR: return RUIN_DIR
    for c in (os.path.join(_here(), "..", "03_ruin", "blocks"), os.path.join(_here(), "..", "blocks")):
        if os.path.exists(os.path.join(c, "build_ruin_blocks.py")): return os.path.abspath(c)
    raise RuntimeError("Nenasel jsem 03_ruin/blocks/build_ruin_blocks.py - nastav RUIN_DIR nahore ve skriptu.")


def load_ruin():
    """nacte generator zriceniny jako knihovnu (nic nepostavi)"""
    d = _ruin_dir()
    sys._ruin_import_only = True
    try:
        sp = importlib.util.spec_from_file_location("build_ruin_blocks", os.path.join(d, "build_ruin_blocks.py"))
        R = importlib.util.module_from_spec(sp); sp.loader.exec_module(R)
    finally:
        sys._ruin_import_only = False
    R.LAYOUT_PATH = os.path.join(d, "ruin_layout.json")
    return R


def load_data():
    with open(DATA_PATH or os.path.join(_here(), "constructions.json"), encoding="utf-8") as f: return json.load(f)


def edits_path():
    return os.path.join(os.path.dirname(DATA_PATH) if DATA_PATH else _here(), "constructions_edits.json")


def load_edits():
    p = edits_path()
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f: d = json.load(f)
        return set(d.get("removed", [])), d.get("moved", {})
    return set(), {}


def compute(R, data, removed=(), moved=None, volumes=None):
    """-> {skupina: dict(folder, stones (Instanced Static Mesh), loose (samostatne actory))}, P"""
    moved = moved or {}
    layout = R.cached_level_terrain(R.load_layout())          # stejny teren jako posledni build zriceniny
    rr, rm = R.load_manual()
    walls, P = R.compute_blocks(layout, rr, rm, volumes)       # zdi zriceniny (kvuli kapsam a podpore tramu)
    terr = R.Terrain(layout["terrain"])
    out = {}
    for fs in data.get("floors", []):
        if ONLY and fs["name"] not in ONLY: continue
        st = R.build_floor_stones(fs, P, walls, terr); R.assign_meshes(st)
        out[fs["name"]] = dict(folder=fs.get("folder", "Stavby"), stones=[s for s in st if s.id not in removed], loose=[])
    for fr in data.get("frames", []):
        if ONLY and fr["name"] not in ONLY: continue
        if fr.get("type") == "fan_roof":
            st = build_fan_roof(R, fr, P, walls, terr); R.assign_meshes(st)
            out[fr["name"]] = dict(folder=fr.get("folder", "Stavby"), stones=[s for s in st if s.id not in removed], loose=[])
    for ad in data.get("addons", []):
        if ONLY and ad["name"] not in ONLY: continue
        if ad.get("type") in ("stone_addon", "plank_floor"):
            st = build_stone_addon(R, ad, P, walls, terr, data.get("frames", [])) if ad["type"] == "stone_addon" else build_plank_floor(R, ad, P, walls, terr)
            R.assign_meshes(st)
            out[ad["name"]] = dict(folder=ad.get("folder", "Stavby"), stones=[s for s in st if s.id not in removed], loose=[])
    rb = data.get("rubble", {})
    if rb.get("enabled", True) and (not ONLY or "Sut" in ONLY):
        clear = [p for p in (addon_polygon(ad) for ad in data.get("addons", []) if ad.get("clear_rubble")) if p]
        clear += [[tuple(q) for q in ad["outline"]] for ad in data.get("addons", []) if ad.get("type") == "plank_floor"]   # na podlaze sut neni
        for name, r in R.make_rubble(walls, P, terr, removed).items():
            sts = [s for s in r["stones"] if not any(_inside(p, s.x, s.y) for p in clear)]   # obyvana cast: sut uklizena
            if not sts: continue
            out[name + "_Sut"] = dict(folder="%s/%s" % (rb.get("folder", "Stavby/Sut"), r["folder"].split("/")[-1]),
                                      stones=[], loose=sts, stavba="Sut")
    for g in out.values():
        for s in g["stones"] + g["loose"]:
            m = moved.get(s.id)
            if m: s.x, s.y, s.z, s.roll, s.pitch, s.yaw = m
    return out, P


def ostroh_geom(R, fr, walls):
    """spolecna geometrie krovu u ostrohu pro krov (Ostroh_Krov) i kamennou dostavbu (Ostroh_Dostavba):
    vyska koruny hradby WT, vrch pricky ct, tramy (vejir + bocni) a pole krytiny s rovinami.
    Tram lezi spodkem na pricce a ve zlabku: u vnitrniho lice hradby je dno zlabku (vrch zdi - d), ven klesa ve sklonu tramu
    a za vnejsim licem tram presahuje (okap). Bocni tramy (sides) jsou rovnobezne s krajnim tramem vejire, zacinaji
    v dostavbe ZBudova_V (spodek ve vysce ct) a konci na hradbe / na ZBudova_S."""
    import math
    key = id(walls), fr["name"]
    if key in _GEOM: return _GEOM[key]
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
        sectors.append(dict(g1=g1, g2=g2, e1=e1, e2=e2, plane=_plane_fit(pts)))
    G = dict(WT=WT, ct=ct, d=d, bw=bw, bh=bh, lh=lh, geo=geo, main=main, sectors=sectors)
    _GEOM[key] = G
    return G


_GEOM = {}
MIN_SLOPE = 0.06                         # nejmensi spad bocnich tramu (krytina musi odvodnit)


def _pt(g, a):
    """bod na ose tramu ve vzdalenosti a (cm, vodorovne od zacatku tramu na pricce)"""
    return (g["S"][0] + g["D"][0] * a, g["S"][1] + g["D"][1] * a)


def roof_under(G, x, y, margin=3.0):
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


def build_fan_roof(R, fr, P, walls, terr):
    """zastreseni u ostrohu: 2 sloupy, pricka (vaznice), paprskovite tramy na snizenou hradbu (ve zlabcich koruny),
    bocni tramy nad kliny u ZBudova_V a krytina. Data z ostroh_spec.py a gen_constructions.py (constructions.json -> frames)."""
    import math
    Stone = R.Stone; out = []
    fin = fr.get("finish", {}); WC = lambda part: R.WOOD_FINISH.get(fin.get(part, "tar"), "wood_tar")
    G = ostroh_geom(R, fr, walls)
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
        out += _fan_roof_cover(R, fr, G, WC)
    return out


def _fan_roof_cover(R, fr, G, WC):
    """krytina krovu: latě napric tramy, dehtovana prkna po spadu (rovnobezne pasy v kazdem poli mezi tramy, krajni
    kratsi do klinu), listy pres spary, kryci prkno pres kazdy tram."""
    import math
    Stone = R.Stone; out = []; rf = fr["roof"]
    lh, lw = rf.get("lath", (0.05, 0.06)); lh *= 100; lw *= 100
    bt = rf.get("board_t", 0.035) * 100; bwmin, bwmax = rf.get("board_w", (0.22, 0.30)); gap = rf.get("gap", 0.015) * 100
    btw, bth = rf.get("batten", (0.06, 0.035)); btw *= 100; bth *= 100
    rng = __import__("random").Random(zlib_crc("%s|roof" % fr["name"]))
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


# ------------------------------------------------------------------ kamenna dostavba (jednoradova zed z kamene rozvalin)
def build_stone_addon(R, ad, P, walls, terr, frames):
    """provizorni dostavba na korunach zdi zriceniny az pod strechu krovu: jedna rada kamenu pres celou tloustku,
    spodek kopiruje korunu zdi pod ni (nebo teren), vrch lici pod late / pod spodek tramu, tramy prochazi zdivem.
    Otvory: dvere (od zeme) a okna s drevenym nadprazim. Zricenina (03) se nemeni."""
    import math, random
    Stone = R.Stone; out = []
    fr = next((f for f in frames if f["name"] == ad.get("roof")), None)
    G = ostroh_geom(R, fr, walls) if fr else None
    if not G: return out
    fin = ad.get("finish", {}); WC = lambda part: R.WOOD_FINISH.get(fin.get(part, "old"), "wood_old")
    sp = ad.get("stone", {}); t = sp.get("t", 0.45) * 100; jn = sp.get("joint", 0.015) * 100
    lmin, lmax = sp.get("len", (0.25, 0.5)); cmin, cmax = sp.get("course", (0.17, 0.27))
    bear = ad.get("lintel", {}).get("bear", 0.25)
    MIN_H = 6.0                                                    # cm: nizsi kus se nepostavi (sousedni rada ho dorovna)
    SILL_MIN = 15.0                                                # cm: tensi kamen pod oknem se nepostavi (parapet = koruna pod nim)
    MORTAR = ad.get("mortar", 0.10) * 100                          # cm: maltove jadro uprostred zdi (zastavi svetlo ve sparach)
    TOP_FILL = 12.0                                                # cm: kdyz by nad radou pod strechou zbylo mene, rada se dorovna az pod strechu
    # kameny zriceniny (koruny zdi), mrizka 1 m
    grid = {}
    for w in walls.values():
        for s in w["stones"] + w.get("loose", []):
            if s.cat not in ("face", "core", "crown", "frame"): continue
            r = max(s.sx, s.sy) / 2
            for gx in range(int(math.floor((s.x - r) / 100)), int(math.floor((s.x + r) / 100)) + 1):
                for gy in range(int(math.floor((s.y - r) / 100)), int(math.floor((s.y + r) / 100)) + 1):
                    grid.setdefault((gx, gy), []).append(s)
    def base_top(x, y):
        best = terr.z(x, y)
        for s in grid.get((int(math.floor(x / 100)), int(math.floor(y / 100))), ()):
            ya = math.radians(s.yaw); lx = (x - s.x) * math.cos(ya) + (y - s.y) * math.sin(ya); ly = -(x - s.x) * math.sin(ya) + (y - s.y) * math.cos(ya)
            if abs(lx) <= s.sx / 2 + 1 and abs(ly) <= s.sy / 2 + 1:
                r_, p_ = math.radians(s.roll), math.radians(s.pitch)        # natocene kusy (rozpadle jadro): skutecny vrch
                best = max(best, s.z + abs(math.sin(p_)) * s.sx / 2 + abs(math.sin(r_)) * s.sy / 2 + abs(math.cos(p_) * math.cos(r_)) * s.sz / 2)
        return best
    for w in ad["walls"]:
        pts = w["pts"]; rng = random.Random(zlib_crc("%s|%s" % (ad["name"], w["name"])))
        seg = [math.hypot(b[0] - a[0], b[1] - a[1]) / 100 for a, b in zip(pts[:-1], pts[1:])]
        cum = [0.0]
        for s_ in seg: cum.append(cum[-1] + s_)
        L = cum[-1]
        def at(s_, lat=0.0):
            k = 0
            while k < len(seg) - 1 and s_ > cum[k + 1]: k += 1
            a, b = pts[k], pts[k + 1]; f = (s_ - cum[k]) / max(seg[k], 1e-6)
            ux, uy = (b[0] - a[0]) / (seg[k] * 100), (b[1] - a[1]) / (seg[k] * 100)
            return a[0] + (b[0] - a[0]) * f - uy * lat, a[1] + (b[1] - a[1]) * f + ux * lat, math.degrees(math.atan2(uy, ux)), k
        NL = 7; lats = [-t / 2 + 1 + (t - 2) * i / (NL - 1) for i in range(NL)]   # podelne cary pres tloustku dostavby
        # profil koruny pod dostavbou a stropu (krov) po 5 cm, pro kazdou caru zvlast
        n = int(L / 0.05) + 1; ss = [min(i * 0.05, L) for i in range(n)]
        btl = [[base_top(*at(s_, la)[:2]) for s_ in ss] for la in lats]
        rul = [[roof_under(G, *at(s_, la)[:2]) for s_ in ss] for la in lats]
        bt = [max(btl[j][i] for j in range(NL)) for i in range(n)]
        ru = [None if any(rul[j][i] is None for j in range(NL)) else min(rul[j][i] for j in range(NL)) for i in range(n)]
        idx = lambda s_: min(max(int(round(s_ / 0.05)), 0), n - 1)
        # otvory (abs. cm): dvere od zeme, okno od parapetu; vrch a nadprazi zarovnane na rady
        ops = []
        for o in w.get("openings", []):
            zg = terr.z(*at(o["s"])[:2])
            ops.append(dict(o, x0=o["s"] - o["w"] / 2, x1=o["s"] + o["w"] / 2, zg=zg))
        z_lo = min(bt[i] for i in range(n) if not any(o["kind"] == "door" and o["x0"] <= ss[i] <= o["x1"] for o in ops))
        z_hi = max(r for r in ru if r is not None)
        crs = []; z = z_lo
        while z < z_hi:
            h = rng.uniform(cmin, cmax) * 100; crs.append((z, z + h)); z += h
        bnd = [c[0] for c in crs] + [crs[-1][1]]
        snap = lambda zz: min(bnd, key=lambda b_: abs(b_ - zz))
        for o in ops:
            o["zt"] = snap(o["zg"] + o["top"] * 100)                    # vrch otvoru = spodek nadprazi
            nxt = [b_ for b_ in bnd if b_ > o["zt"] + 1]
            o["zl"] = nxt[0] if nxt else o["zt"] + 18                    # nadprazi pres jednu radu
            o["zs"] = -1e9 if o["kind"] == "door" else snap(o["zg"] + o.get("sill", 0) * 100)
        for o in ops:                                                   # nadprazi ve stejne vysce jako u jineho otvoru (align = jeho index)
            if o.get("align") is not None: o["zt"], o["zl"] = ops[o["align"]]["zt"], ops[o["align"]]["zl"]
        # nucene hranice kusu: zlomy, otvory a nadprazi, tramy, schody koruny pod dostavbou
        brk = set(cum[1:-1])
        for o in ops: brk.update((o["x0"], o["x1"], o["x0"] - bear, o["x1"] + bear))
        for g in G["geo"]:
            for k in range(len(seg)):
                a, b = pts[k], pts[k + 1]; ex, ey = b[0] - a[0], b[1] - a[1]
                den = g["D"][0] * ey - g["D"][1] * ex
                if abs(den) < 1e-6: continue
                tt = ((a[0] - g["S"][0]) * ey - (a[1] - g["S"][1]) * ex) / den
                f = ((a[0] - g["S"][0]) * g["D"][1] - (a[1] - g["S"][1]) * g["D"][0]) / den
                if 0 <= f <= 1 and g["at"] - 20 <= tt <= g["a1"]:
                    sn = abs(den) / (seg[k] * 100); hw = (G["bw"] / 2 + 1.5) / max(sn, 0.3) / 100
                    sc_ = cum[k] + f * seg[k]; brk.update((sc_ - hw, sc_ + hw))
        for i in range(1, n):
            if abs(bt[i] - bt[i - 1]) > 4: brk.add(ss[i] - 0.025)
            if ru[i] is not None and ru[i - 1] is not None and abs(ru[i] - ru[i - 1]) > 8: brk.add(ss[i] - 0.025)
        brk = sorted(b_ for b_ in brk if 0 < b_ < L)
        for ci, (cz0, cz1) in enumerate(crs):
            holes = []
            for o in ops:
                if cz1 > o["zs"] + 1 and cz0 < o["zt"] - 1: holes.append((o["x0"], o["x1"]))
                if cz1 > o["zt"] + 1 and cz0 < o["zl"] - 1: holes.append((o["x0"] - bear, o["x1"] + bear))
            s = -rng.uniform(0, lmax) if ci % 2 else 0.0; bi = 0
            while s < L:
                ln = rng.uniform(lmin, lmax); a0, a1 = max(s, 0.0), min(s + ln, L); s += ln
                cuts = [a0] + [b_ for b_ in brk if a0 + 0.01 < b_ < a1 - 0.01] + [a1]
                pieces = []
                for p0, p1 in zip(cuts[:-1], cuts[1:]):
                    parts = [(p0, p1)]
                    for h0, h1 in holes:
                        parts = [q for q0, q1 in parts for q in ((q0, min(q1, h0)), (max(q0, h1), q1)) if q[1] - q[0] > 0.005] \
                            if any(h1 > q0 and h0 < q1 for q0, q1 in parts) else parts
                    pieces += parts
                # kousky kratsi nez 15 cm pripojit k sousedovi (ne pres otvor)
                merged = []
                for q in pieces:
                    if merged and q[1] - q[0] < 0.15 and abs(merged[-1][1] - q[0]) < 1e-6: merged[-1] = (merged[-1][0], q[1])
                    elif merged and merged[-1][1] - merged[-1][0] < 0.15 and abs(merged[-1][1] - q[0]) < 1e-6: merged[-1] = (merged[-1][0], q[1])
                    else: merged.append(q)
                for pi, (p0, p1) in enumerate(merged):
                    if p1 - p0 < 0.06: continue
                    i0, i1 = idx(p0 + 0.02), idx(p1 - 0.02)
                    zb_ = max(bt[i0:i1 + 1])
                    rr = [r for r in ru[i0:i1 + 1]]
                    if any(r is None for r in rr): continue
                    zt_ = min(rr); zt_hi = max(min(rul[j][i0:i1 + 1]) for j in range(NL))
                    if cz1 <= zb_ + MIN_H or cz0 >= zt_hi - TOP_FILL: continue
                    z0 = zb_ if cz0 < zb_ + MIN_H else cz0
                    z1 = zt_ if cz1 > zt_ - TOP_FILL else cz1
                    thin_sill = False
                    for o in ops:                                     # nad otvorem a pod parapetem okna presne na radach
                        if p1 > o["x0"] - bear and p0 < o["x1"] + bear and abs(cz0 - o["zl"]) < 1: z0 = cz0
                        if p1 > o["x0"] and p0 < o["x1"] and abs(cz1 - o["zs"]) < 1:
                            z1 = cz1
                            if z1 - z0 < SILL_MIN: thin_sill = True    # tenky kamen pod parapetem: pryc, okno sahá az na korunu
                    if thin_sill: continue
                    sid = "%s|%s|%d|%d%s" % (ad["name"], w["name"], ci, bi, "" if len(merged) == 1 else "abcdefghij"[min(pi, 9)])
                    sr = random.Random(zlib_crc(sid))
                    # pod sikmym tramem by cely kamen musel pod jeho spodek -> u koruny kamen rozdelit pres tloustku na 3 (kazdy po svuj strop)
                    parts = [(0, NL - 1, z1)]
                    if cz1 > zt_ - TOP_FILL and zt_hi - zt_ > 5:
                        parts = []
                        for q, (j0, j1) in enumerate(((0, 2), (2, 4), (4, 6))):
                            ztq = min(min(rul[j][i0:i1 + 1]) for j in range(j0, j1 + 1))
                            z1q = ztq if cz1 > ztq - TOP_FILL else cz1
                            parts.append((j0, j1, z1q))
                    for q, (j0, j1, z1q) in enumerate(parts):
                        if z1q - z0 < MIN_H: continue
                        la = (lats[j0] + lats[j1]) / 2 + (sr.uniform(-1.0, 1.0) if len(parts) == 1 else 0.0)
                        dep = (t - 1.0) if len(parts) == 1 else (t / 3 - 0.8)
                        x, y, yaw, k = at((p0 + p1) / 2, la)
                        out.append(Stone(sid if len(parts) == 1 else "%s.%d" % (sid, q), "face", x, y, (z0 + z1q) / 2, yaw + sr.uniform(-1.0, 1.0),
                                         (p1 - p0) * 100 - jn, dep, (z1q - z0) - jn * 0.7, seg=k))
                        out[-1].span = (p0, p1, z0, z1q)
                        if MORTAR > 0 and (len(parts) == 1 or q == 1):
                            # malta: jadro uprostred tloustky, pres spary (o pul spary delsi na kazdou stranu, cela vyska rady)
                            xm, ym, _, _ = at((p0 + p1) / 2, 0.0)
                            out.append(Stone(sid + ".m", "core", xm, ym, (z0 + z1q) / 2, yaw, (p1 - p0) * 100 + 0.4, MORTAR, z1q - z0))
                bi += 1
        # drevena nadprazi
        for oi, o in enumerate(ops):
            x, y, yaw, k = at(o["s"])
            ln = (o["x1"] - o["x0"] + 2 * bear) * 100
            out.append(Stone("%s|%s|N%d" % (ad["name"], w["name"], oi), WC("lintels"), x, y, (o["zt"] + o["zl"]) / 2, yaw,
                             ln, t - 2.0, o["zl"] - o["zt"] - 0.5))
    return out


def build_plank_floor(R, fl, P, walls, terr):
    """prkenna podlaha uvnitr obrysu (vnitrni lice zdi): podvaly (napric, na zemi, kopiruji teren), prkna podel u
    s presazenymi spoji na podvalech. Prkna se vyriznou kolem sloupu a kamenu zriceniny, ktere zasahuji do podlahy."""
    import math, random
    Stone = R.Stone; out = []
    fin = fl.get("finish", {}); WC = lambda part: R.WOOD_FINISH.get(fin.get(part, "raw"), "wood")
    ux, uy = fl["u"]; nx, ny = fl["n"]
    poly = [tuple(p) for p in fl["outline"]]
    sp, pp = fl.get("sleepers", {}), fl.get("planks", {})
    sw, sh, sstep, sseg = sp.get("w", 0.14) * 100, sp.get("h", 0.10) * 100, sp.get("step", 0.8) * 100, sp.get("seg", 1.2) * 100
    pt_, (pwmin, pwmax), pgap, (plmin, plmax) = pp.get("t", 0.045) * 100, pp.get("w", (0.22, 0.32)), pp.get("gap", 0.006) * 100, pp.get("len", (2.4, 4.5))
    ins = fl.get("inset", 0.02) * 100
    rng = random.Random(zlib_crc(fl["name"]))
    O = poly[0]
    U = lambda x, y: (x - O[0]) * ux + (y - O[1]) * uy
    V = lambda x, y: (x - O[0]) * nx + (y - O[1]) * ny
    XY = lambda u, v: (O[0] + ux * u + nx * v, O[1] + uy * u + ny * v)
    pu = [(U(*q), V(*q)) for q in poly]
    def span(v):
        """useky u (cm), kde primka v = konst. lezi uvnitr obrysu (o ins od zdi)"""
        xs = []
        for (u0, v0), (u1, v1) in zip(pu, pu[1:] + pu[:1]):
            if (v0 > v) != (v1 > v): xs.append(u0 + (u1 - u0) * (v - v0) / (v1 - v0))
        xs.sort(); return [(a + ins, b - ins) for a, b in zip(xs[::2], xs[1::2]) if b - a > 2 * ins]
    def inter(A, B):
        return [(max(a0, b0), min(a1, b1)) for a0, a1 in A for b0, b1 in B if min(a1, b1) > max(a0, b0)]
    vs = [q[1] for q in pu]; v_lo, v_hi = min(vs), max(vs)
    us = [q[0] for q in pu]; u_lo, u_hi = min(us), max(us)
    # vyska podlahy: nad nejvyssim terenem v obrysu (podvaly dorovnaji nizsi mista)
    zg = []
    for i in range(int((u_hi - u_lo) / 25) + 1):
        for j in range(int((v_hi - v_lo) / 25) + 1):
            u, v = u_lo + i * 25, v_lo + j * 25
            if any(a <= u <= b for a, b in span(v)): zg.append(terr.z(*XY(u, v)))
    if not zg: return out
    z_sl = max(zg) + sh                                     # vrch podvalu = spodek prken
    # kameny zriceniny, ktere zasahuji do vysky podlahy (vylomene lice, rozpadle jadro u paty)
    near = []
    for w in walls.values():
        for st in w["stones"] + w.get("loose", []):
            if st.z - st.sz / 2 < z_sl + pt_ + 1 and st.z + st.sz / 2 > z_sl - sh and u_lo - 100 < U(st.x, st.y) < u_hi + 100 \
               and v_lo - 100 < V(st.x, st.y) < v_hi + 100: near.append(st)
    def blocked(x, y, pad=1.0):
        for st in near:
            ya = math.radians(st.yaw); lx = (x - st.x) * math.cos(ya) + (y - st.y) * math.sin(ya); ly = -(x - st.x) * math.sin(ya) + (y - st.y) * math.cos(ya)
            if abs(lx) <= st.sx / 2 + pad and abs(ly) <= st.sy / 2 + pad: return True
        return False
    posts = [p for grp in fl.get("avoid", []) for p in grp]; ph = fl.get("post", 0.28) * 50 + 2
    def free(v0, v1, ivs):
        """useky bez sloupu a kamenu zriceniny (pres celou sirku pasu v0..v1)"""
        out_ = []
        for a, b in ivs:
            cuts = []
            for (px, py) in posts:
                pu_, pv_ = U(px, py), V(px, py)
                if pv_ + ph > v0 and pv_ - ph < v1: cuts.append((pu_ - ph, pu_ + ph))
            u = a; run0 = None
            while u <= b + 0.1:                              # kameny po 5 cm na obou hranach pasu a uprostred
                bad = any(blocked(*XY(u, vv)) for vv in (v0 + 1, (v0 + v1) / 2, v1 - 1)) or any(c0 <= u <= c1 for c0, c1 in cuts)
                if not bad and run0 is None: run0 = u
                if bad and run0 is not None:
                    if u - 5 - run0 > 30: out_.append((run0, u - 5))
                    run0 = None
                u += 5
            if run0 is not None and b - run0 > 30: out_.append((run0, b))
        return out_
    # podvaly napric (smer v), po sstep podel u; kusy po sseg, spodek na terenu
    k0 = int(math.floor(u_lo / sstep)); k1 = int(math.ceil(u_hi / sstep)); sl_u = []
    for k in range(k0, k1 + 1):
        u = k * sstep
        # kde je podval uvnitr: rozsah v pres vsechny pasy
        vv = [v_lo + j * 5 for j in range(int((v_hi - v_lo) / 5) + 1)]
        pc = [(U(px, py), V(px, py)) for px, py in posts]
        inside = [v for v in vv if any(a + sw / 2 <= u <= b - sw / 2 for a, b in span(v))
                  and not any(abs(u - pu_) < ph + sw / 2 and abs(v - pv_) < ph for pu_, pv_ in pc)       # podval kolem sloupu prerusen
                  and not any(blocked(*XY(u + du, v)) for du in (-sw / 2, sw / 2))]                        # ani pod kamenem zriceniny
        if not inside: continue
        sl_u.append(u)
        runs = []; r0 = inside[0]; prev = inside[0]
        for v in inside[1:] + [None]:
            if v is None or v - prev > 6: runs.append((r0, prev)); r0 = v
            if v is not None: prev = v
        for r0, r1 in runs:
            n = max(1, int(round((r1 - r0) / sseg)))
            for q in range(n):
                a, b = r0 + (r1 - r0) * q / n + 1, r0 + (r1 - r0) * (q + 1) / n - 1
                if b - a < 20: continue
                x, y = XY(u, (a + b) / 2)
                zgr = min(terr.z(*XY(u, a)), terr.z(*XY(u, b)), terr.z(x, y)) - 3       # zapusteno 3 cm do zeme
                sid = "%s|P%d|%d" % (fl["name"], k, q)
                out.append(Stone(sid, WC("sleepers"), x, y, (zgr + z_sl) / 2, math.degrees(math.atan2(ny, nx)), b - a, sw, z_sl - zgr))
    # prkna podel u, pasy pres v; spoje presazene na podvalech
    v = v_lo + ins; j = 0
    while v < v_hi - ins:
        w_ = rng.uniform(pwmin, pwmax) * 100; v0, v1 = v, v + w_; v = v1 + pgap; j += 1
        # pas az ke zdi i v oblouku (podle vzdalenejsi hrany pasu); kde je kamen zriceniny, prkno konci pred nim
        sa, sb = span(v0 + 0.5), span(v1 - 0.5)
        ivs = free(v0, v1, [(min(a0, b0), max(a1, b1)) for a0, a1 in sa for b0, b1 in sb if min(a1, b1) > max(a0, b0)])
        for a, b in ivs:
            u = a; q = 0
            while b - u > 30:
                ln = rng.uniform(plmin, plmax) * 100; e = u + ln
                if e < b - 60:                                 # spoj na nejblizsim podvalu (ne kratky zbytek na konci)
                    cand = [s_ for s_ in sl_u if u + 120 < s_ < b - 60]
                    if cand: e = min(cand, key=lambda s_: abs(s_ - e))
                else: e = b
                x, y = XY((u + e) / 2, (v0 + v1) / 2)
                sid = "%s|K%d|%d" % (fl["name"], j, q); r_ = random.Random(zlib_crc(sid))
                out.append(Stone(sid, WC("planks"), x, y, z_sl + pt_ / 2 + r_.uniform(-0.3, 0.3), math.degrees(math.atan2(uy, ux)) + r_.uniform(-0.3, 0.3),
                                 e - u - 0.4, w_ - 0.3, pt_))
                u = e; q += 1
    return out


def addon_polygon(ad):
    """obrys obytne casti z os dostaveb (pro uklizeni suti uvnitr)"""
    if "walls" not in ad: return None
    ws = {w["name"]: w["pts"] for w in ad["walls"]}
    if not all(k in ws for k in ("V", "S", "H")): return None
    return ws["V"] + ws["S"] + ws["H"][::-1]


def _inside(poly, x, y):
    c = False
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        if (ay > y) != (by > y) and x < ax + (bx - ax) * (y - ay) / (by - ay): c = not c
    return c


def _plane_fit(P):
    """nejmensi ctverce z = c0 + cx*x + cy*y pres body [((x, y), z)] - ciste v Pythonu (normalni rovnice, Cramer)"""
    mx = sum(q[0] for q, _ in P) / len(P); my = sum(q[1] for q, _ in P) / len(P); mz = sum(z for _, z in P) / len(P)
    sxx = sum((q[0] - mx) ** 2 for q, _ in P); syy = sum((q[1] - my) ** 2 for q, _ in P)
    sxy = sum((q[0] - mx) * (q[1] - my) for q, _ in P)
    sxz = sum((q[0] - mx) * (z - mz) for q, z in P); syz = sum((q[1] - my) * (z - mz) for q, z in P)
    det = sxx * syy - sxy * sxy
    if abs(det) < 1e-9: return mz, 0.0, 0.0
    cx = (sxz * syy - syz * sxy) / det; cy = (syz * sxx - sxz * sxy) / det
    return mz - cx * mx - cy * my, cx, cy


def zlib_crc(s):
    import zlib
    return zlib.crc32(s.encode())


# ------------------------------------------------------------------ Unreal
def _materials(unreal, R):
    mats = R.ensure_materials(unreal)
    mats["floor"] = mats.get("frame")
    if not mats.get("wood"):       # MI_RuinWood (+ _Tar, _Oil) vytvori ensure_materials; zaloha StarterContent
        mats["wood"] = next((unreal.load_asset(p) for p in MAT_WOOD if unreal.EditorAssetLibrary.does_asset_exist(p.split(".")[0])), None)
    for wc in R.WOOD_MI: mats[wc] = mats.get(wc) or mats["wood"]
    return mats


def build_in_unreal():
    import unreal
    R = load_ruin(); data = load_data(); removed, moved = load_edits()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    groups, P = compute(R, data, removed, moved, R.gather_volumes(unreal, eas))
    cube = unreal.load_asset(R.CUBE_MESH); mats = _materials(unreal, R); meshes = R.ensure_stone_meshes(unreal)
    tag = unreal.Name(CONSTR_TAG); n = 0; n_phys = 0
    with unreal.ScopedEditorTransaction("Build constructions"):
        def mine(a):
            """patri actor ke stavbe z ONLY? podle tagu stavba:<jmeno>, u starsich buildu podle jmena / id"""
            if not ONLY: return True
            tg = [str(t) for t in a.tags]
            st_ = [t[7:] for t in tg if t.startswith("stavba:")]
            if st_: return st_[0] in ONLY
            lab = a.get_actor_label()
            if any(lab.startswith(o) for o in ONLY): return True
            return "Sut" in ONLY and ("_Sut" in lab or any(t.startswith("id:") and "|R" in t for t in tg))
        old = [a for a in eas.get_all_level_actors() if tag in a.tags and mine(a)]
        if old: eas.destroy_actors(old)
        for name, g in groups.items():
            bycat = {}
            for s in g["stones"]: bycat.setdefault(s.cat, []).append(s)
            for cat, sts in sorted(bycat.items()):
                bym = {}
                for s in sts:
                    m, nom = R._resolve(unreal, s, cube, meshes)
                    bym.setdefault(m.get_path_name(), [m, []])[1].append(R.stone_transform(unreal, s, m, nom))
                cname = {"wood": "Drevo", "wood_tar": "Drevo_Dehet", "wood_oil": "Drevo_Olej", "wood_blood": "Drevo_Krev",
                         "wood_old": "Drevo_Stare", "floor": "Podlaha", "face": "Kamen", "core": "Malta",
                         "frame": "Kvadr"}.get(cat, cat)
                for a_ in R._ism_actor(unreal, eas, "%s_%s" % (name, cname), g["folder"], [tuple(v) for _, v in sorted(bym.items())], mats.get(cat), tag):
                    a_.tags = list(a_.tags) + [unreal.Name("stavba:" + g.get("stavba", name))]
                n += len(sts)
            for s in g["loose"]:
                m, nom = R._resolve(unreal, s, cube, meshes)
                act = eas.spawn_actor_from_object(m, unreal.Vector(s.x, s.y, s.z), unreal.Rotator(roll=s.roll, pitch=s.pitch, yaw=s.yaw))
                if not act: continue
                act.set_actor_transform(R.stone_transform(unreal, s, m, nom), False, False)
                act.tags = [tag, unreal.Name("RuinStone"), unreal.Name("id:" + s.id), unreal.Name("stavba:" + g.get("stavba", name))]
                act.set_folder_path(g["folder"])
                act.set_actor_label("Kamen_" + s.id.replace("|", "_"))
                if mats.get(s.cat): act.static_mesh_component.set_material(0, mats[s.cat])
                if RUBBLE_PHYSICS:
                    R.stone_physics(unreal, act, s, asleep=s.id in moved)
                    act.tags = list(act.tags) + [unreal.Name("Ruin_Physics")]; n_phys += 1
                n += 1
    unreal.log("Stavby: %d kusu ve %d skupinach (%s), rucne smazanych %d, posunutych %d, s fyzikou %d%s." % (
        n, len(groups), ", ".join(groups), len(removed), len(moved), n_phys,
        " (usazeni: Simulate, vyber tag Ruin_Physics, K, pak MODE=capture)" if n_phys else ""))


def freeze():
    """vypne fyziku suti (kameny zustanou, kde lezi, staticke); dalsi build ji zase zapne, pokud RUBBLE_PHYSICS = True"""
    import unreal
    R = load_ruin()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem); n = 0
    with unreal.ScopedEditorTransaction("Freeze rubble"):
        for a in eas.get_all_level_actors():
            tags = [str(t) for t in a.tags]
            if "Ruin_Physics" in tags and isinstance(a, unreal.StaticMeshActor):
                R.stone_physics(unreal, a, None, on=False); a.tags = [t for t in a.tags if str(t) != "Ruin_Physics"]; n += 1
    unreal.log("Stavby: fyzika vypnuta u %d kamenu suti." % n)


def capture_edits():
    """ulozi rucne smazane kusy (chybi v Instanced Static Mesh / smazany actor) a posunute samostatne kameny"""
    import unreal
    R = load_ruin(); data = load_data(); removed, moved = load_edits()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    groups, P = compute(R, data, removed, moved, R.gather_volumes(unreal, eas))
    cube = unreal.load_asset(R.CUBE_MESH); meshes = R.ensure_stone_meshes(unreal)
    present = set(); loose_now = {}
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        if CONSTR_TAG not in tags: continue
        ids = [t[3:] for t in tags if t.startswith("id:")]
        if ids: loose_now[ids[0]] = a; continue
        for comp in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
            for i in range(comp.get_instance_count()):
                res = comp.get_instance_transform(i, True)
                t = (res[-1] if isinstance(res, tuple) else res).translation
                present.add((round(t.x), round(t.y), round(t.z)))
    n_rem = n_mov = 0
    for g in groups.values():
        for s in g["stones"]:
            m, nom = R._resolve(unreal, s, cube, meshes); t = R.stone_transform(unreal, s, m, nom).translation
            if (round(t.x), round(t.y), round(t.z)) not in present: removed.add(s.id); n_rem += 1
        for s in g["loose"]:
            a = loose_now.get(s.id)
            if a is None: removed.add(s.id); moved.pop(s.id, None); n_rem += 1; continue
            m, nom = R._resolve(unreal, s, cube, meshes)
            st_t = unreal.MathLibrary.compose_transforms(unreal.MathLibrary.invert_transform(R._fix_unit(unreal, s, m, nom)),
                                                         R._unit(unreal, a.get_actor_transform()))
            loc, rot, _ = unreal.MathLibrary.break_transform(st_t)
            cur = [loc.x, loc.y, loc.z, rot.roll, rot.pitch, rot.yaw]
            same = all(abs(p - q) < 1.0 for p, q in zip(cur[:3], [s.x, s.y, s.z])) and \
                   all(abs(((p - q) + 180) % 360 - 180) < 1.0 for p, q in zip(cur[3:], [s.roll, s.pitch, s.yaw]))
            if not same: moved[s.id] = [round(v, 2) for v in cur]; n_mov += 1
    with open(edits_path(), "w", encoding="utf-8") as f:
        json.dump({"removed": sorted(removed), "moved": moved}, f, ensure_ascii=False, indent=1)
    unreal.log("constructions_edits.json: smazano %d (nove %d), posunuto %d (nove %d)." % (len(removed), n_rem, len(moved), n_mov))


def _has_unreal():
    try:
        import unreal  # noqa
        return True
    except ImportError:
        return False


def run(only=None, mode=None):
    """spusteni z UE pro vybrane stavby (stavby/<Stavba>.py): only = seznam jmen ze constructions.json (+ "Sut"),
    mode = "build" / "capture" / "freeze"; ruzne stavby se navzajem nesmazou ani neprestavi"""
    global ONLY, MODE
    ONLY = list(only) if only else None
    MODE = mode or MODE
    {"capture": capture_edits, "freeze": freeze}.get(MODE, build_in_unreal)()


if (__name__ == "__main__" or "unreal" in sys.modules) and not getattr(sys, "_constr_import_only", False):
    if _has_unreal():
        run(ONLY, MODE)
    else:
        if len(sys.argv) > 1: DATA_PATH = sys.argv[1]
        if len(sys.argv) > 2: RUIN_DIR = sys.argv[2]
        R = load_ruin()
        if len(sys.argv) > 3: R.LAYOUT_PATH = sys.argv[3]
        groups, P = compute(R, load_data(), *load_edits())
        for n, g in groups.items():
            c = {}
            for s in g["stones"] + g["loose"]: c[s.cat] = c.get(s.cat, 0) + 1
            print("  %-22s %-24s %s" % (n, g["folder"], ", ".join("%s %d" % kv for kv in sorted(c.items()))))
