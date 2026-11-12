"""
build_constructions.py - dodatecne stavby zriceniny ("druhe zabydleni"), Unreal Editor 5.8

Stavi zvlast od zriceniny (03_ruin/blocks/build_ruin_blocks.py), takze se da ladit bez pregenerovani hradu:
  - drevene vestavby: tramy v kapsach, prkna, pruvlak se sloupy, provizorni schody, podesta (constructions.json -> floors)
  - volna sut na zemi u zdi (samostatne actory, lze posouvat a mazat)
Zricenina zustava ve 03: zdi, otvory, kapsy pro tramy, kamenna dlazba.

Pouziti v UE: Tools -> Execute Python Script ->
  - stavby/<Stavba>.py      jen jedna stavba (Vez_Patra.py, Ostroh_Krov.py, Sut.py) - ostatni se nesmazou ani neprestavi
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
ONLY = None                              # napr. ["Vez_Patra"] nebo ["Sut"] = postavit jen tuto cast
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
    rb = data.get("rubble", {})
    if rb.get("enabled", True) and (not ONLY or "Sut" in ONLY):
        for name, r in R.make_rubble(walls, P, terr, removed).items():
            if not r["stones"]: continue
            out[name + "_Sut"] = dict(folder="%s/%s" % (rb.get("folder", "Stavby/Sut"), r["folder"].split("/")[-1]),
                                      stones=[], loose=r["stones"], stavba="Sut")
    for g in out.values():
        for s in g["stones"] + g["loose"]:
            m = moved.get(s.id)
            if m: s.x, s.y, s.z, s.roll, s.pitch, s.yaw = m
    return out, P


def build_fan_roof(R, fr, P, walls, terr):
    """zastreseni u ostrohu: 2 sloupy, pricka (vaznice), paprskovite tramy na snizenou hradbu (ve zlabcich koruny).
    Tram lezi spodkem na pricce a ve zlabku: u vnitrniho lice hradby je dno zlabku (vrch zdi - d), ven klesa ve sklonu tramu
    a za vnejsim licem tram presahuje (okap). Data z ostroh_spec.py (constructions.json -> frames)."""
    import math
    Stone = R.Stone; out = []
    fin = fr.get("finish", {}); WC = lambda part: R.WOOD_FINISH.get(fin.get(part, "tar"), "wood_tar")
    bw, bh = fr["beam"][0] * 100, fr["beam"][1] * 100; T = fr["wall_t"] * 100
    wall_st = walls.get(fr["wall"], {}).get("stones", [])
    if not wall_st: return out
    # vrch snizene hradby u kazdeho tramu (bez kamenu snizenych ve zlabku)
    tops = []
    for b in fr["beams"]:
        ex, ey = b["wall_pt"]
        near = [s for s in wall_st if s.cat in ("face", "core", "crown") and ".n1" not in s.id
                and math.hypot(s.x - ex, s.y - ey) < T / 2 + 80]
        tops.append(max(s.z + s.sz / 2 for s in near) if near else None)
    ok = [t for t in tops if t is not None]
    if not ok: return out
    WT = max(set(round(t) for t in ok), key=[round(t) for t in ok].count)      # zarovnana koruna: nejcastejsi vyska
    d = fr["notches"][0]["d"] * 100
    nb_in = WT - d                                    # dno zlabku u vnitrniho lice
    ct = nb_in + fr["rise"] * 100                      # vrch pricky = spodek tramu u pricky
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
    so = fr.get("start_over", 0.3) * 100; oh = fr.get("overhang", 0.6) * 100
    geo = []                                          # tramy pro krytinu: (start, smer, sklon, konec za zdi, delka do vnitr. lice)
    for i, (b, wt) in enumerate(zip(fr["beams"], tops)):
        if wt is None: continue                       # hradba u konce tramu chybi
        sx_, sy_ = b["start"]; ex, ey = b["wall_pt"]
        dx, dy = ex - sx_, ey - sy_; dl = math.hypot(dx, dy); dx, dy = dx / dl, dy / dl
        sl = b["slope"]                               # pokles spodku tramu na 1 m (od pricky ke zdi)
        d_in = b["d_in"] * 100
        # spodek: u pricky ct, u vnitrniho lice nb_in (= ct - sl * d_in), dal klesa stejne
        a0 = -so; a1 = dl + (T / 2) / max(b.get("sin", 1.0), 0.35) + oh        # od pricky (cm) pres zed az za vnejsi lic
        z0 = ct + sl * so; z1 = ct - sl * a1
        mx, my = sx_ + dx * (a0 + a1) / 2, sy_ + dy * (a0 + a1) / 2
        ang = math.atan(sl); L = math.hypot(a1 - a0, z0 - z1)
        zc = (z0 + z1) / 2 + bh / 2 / math.cos(ang)
        yaw_b = math.degrees(math.atan2(-dy, -dx))     # osa X kamene: od zdi (nize) k pricce (vys) -> pitch kladny
        out.append(Stone("%s|B%d" % (fr["name"], i), WC("beams"), mx, my, zc, yaw_b, L, bw, bh, pitch=math.degrees(ang)))
        geo.append(dict(S=(sx_, sy_), D=(dx, dy), sl=sl, a1=a1, top=lambda a, sl=sl, ang=ang: ct - sl * a + bh / math.cos(ang)))
    if fr.get("roof") and len(geo) >= 2:
        out += _fan_roof_cover(R, fr, geo, ct, bh, so, WC)
    return out


def _fan_roof_cover(R, fr, geo, ct, bh, so, WC):
    """krytina krovu: latě napric tramy, dehtovana prkna po spadu (rovnobezne pasy v kazdem poli mezi tramy, krajni
    kratsi do klinu), listy pres spary a pres tramy, lemovani u pricky (kryci prkno + celni prkno)."""
    import math
    Stone = R.Stone; out = []; rf = fr["roof"]
    lh, lw = rf.get("lath", (0.05, 0.06)); lh *= 100; lw *= 100
    bt = rf.get("board_t", 0.035) * 100; bwmin, bwmax = rf.get("board_w", (0.22, 0.30)); gap = rf.get("gap", 0.015) * 100
    btw, bth = rf.get("batten", (0.06, 0.035)); btw *= 100; bth *= 100
    a_top = -rf.get("top_over", 0.2) * 100                  # horni okraj krytiny (za prickou smerem ke vstupu)
    rng = __import__("random").Random(zlib_crc("%s|roof" % fr["name"]))
    def pt(g, a):                                        # bod na ose tramu ve vzdalenosti a (cm, vodorovne od pricky)
        return (g["S"][0] + g["D"][0] * a, g["S"][1] + g["D"][1] * a)
    def isect(p, d, q, e):                                # parametr t na primce p + t*d, kde protne primku q + u*e
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-9: return None
        return ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
    zb = lambda g, a: g["top"](a) + lh                      # spodek prken nad trámem (na latich)
    for k in range(len(geo) - 1):
        g1, g2 = geo[k], geo[k + 1]
        e1, e2 = g1["a1"] - 5, g2["a1"] - 5                # okap (konce tramu)
        P = [(pt(g1, a_top), zb(g1, a_top)), (pt(g2, a_top), zb(g2, a_top)), (pt(g1, e1), zb(g1, e1)), (pt(g2, e2), zb(g2, e2))]
        # rovina pole z = c0 + cx*x + cy*y (nejmensi ctverce pres 4 rohy)
        c0, cx, cy = _plane_fit(P)                        # bez numpy (Python v Unrealu ho nema)
        zpl = lambda x, y: c0 + cx * x + cy * y
        dx, dy = g1["D"][0] + g2["D"][0], g1["D"][1] + g2["D"][1]; dl = math.hypot(dx, dy); d = (dx / dl, dy / dl); l = (-d[1], d[0])
        O = ((g1["S"][0] + g2["S"][0]) / 2, (g1["S"][1] + g2["S"][1]) / 2)
        pitch = math.degrees(math.atan(cx * d[0] + cy * d[1])); roll = math.degrees(math.atan(cx * l[0] + cy * l[1]))
        yaw = math.degrees(math.atan2(d[1], d[0]))
        topP, topE = pt(g1, a_top), (pt(g2, a_top)[0] - pt(g1, a_top)[0], pt(g2, a_top)[1] - pt(g1, a_top)[1])
        eavP, eavE = pt(g1, e1), (pt(g2, e2)[0] - pt(g1, e1)[0], pt(g2, e2)[1] - pt(g1, e1)[1])
        lat = lambda q: (q[0] - O[0]) * l[0] + (q[1] - O[1]) * l[1]
        side1 = 1 if lat(pt(g1, e1)) > 0 else -1            # na ktere strane pole lezi tram k
        def run(c, w_=0.0):
            """rozsah t podel d pro pas se stredem v bocni vzdalenosti c (cm) a sirce w_ - pas zacina, jakmile se do pole
            dostane jeho VNITRNI hrana (jinak mezi krajnim prknem a tramem zustane klinova dira); na tramu ho prekryje
            kryci prkno"""
            p0 = (O[0] + l[0] * c, O[1] + l[1] * c)
            g = g1 if (c > 0) == (side1 > 0) else g2
            ci = c - (w_ / 2 if c > 0 else -w_ / 2) if c else 0.0
            pi = (O[0] + l[0] * ci, O[1] + l[1] * ci)
            ti = isect(pi, d, g["S"], g["D"])
            ts = [isect(p0, d, topP, topE), ti]
            t0 = max(t for t in ts if t is not None); t1 = isect(p0, d, eavP, eavE)
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
            out.append(Stone("%s|R%d|K%d" % (fr["name"], k, j), WC("roof_boards"), x, y, zpl(x, y) + bt / 2 + lift, yaw,
                             t1 - t0, w_ - 0.5, bt, pitch, roll))
        # listy pres spary mezi prkny (prekryv sousednich pasu)
        for j in range(len(boards) - 1):
            ca, wa, pa, ta0, ta1 = boards[j]; cb, wb, pb, tb0, tb1 = boards[j + 1]
            c = (ca + wa / 2 + cb - wb / 2) / 2; t0, t1 = max(ta0, tb0), min(ta1, tb1)
            if t1 - t0 < 40: continue
            p0 = (O[0] + l[0] * c, O[1] + l[1] * c); tm = (t0 + t1) / 2; x, y = p0[0] + d[0] * tm, p0[1] + d[1] * tm
            out.append(Stone("%s|R%d|L%d" % (fr["name"], k, j), WC("roof_battens"), x, y, zpl(x, y) + bt + bth / 2 + lift, yaw,
                             t1 - t0, btw, bth, pitch, roll))
        # latě pod prkny napric polem (na tramech): u horniho okraje, dve uprostred, u zdi a u okapu
        for r_, f in enumerate(rf.get("lath_rows", (0.04, 0.35, 0.65, 0.9, 1.0))):
            a1_ = a_top + 15 + (min(e1, e2) - 25 - a_top - 15) * f
            q1, q2 = pt(g1, a1_), pt(g2, a1_ + (e2 - e1) * f)
            x, y = (q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2; ln = math.hypot(q2[0] - q1[0], q2[1] - q1[1]) + 25
            ylat = math.degrees(math.atan2(q2[1] - q1[1], q2[0] - q1[0]))
            out.append(Stone("%s|R%d|T%d" % (fr["name"], k, r_), WC("roof_laths"), x, y, (zb(g1, a1_) + zb(g2, a1_ + (e2 - e1) * f)) / 2 - lh / 2,
                             ylat, ln, lw, lh))
    # lista pres kazdy tram (spoj dvou poli)
    for i, g in enumerate(geo):
        a0, a1_ = a_top, g["a1"] - 5; L = a1_ - a0
        q = pt(g, (a0 + a1_) / 2); ang = math.atan(g["sl"])
        cw = rf.get("cover_w", 0.36) * 100            # kryci prkno pres tram (spoj dvou poli a prekryv krajnich prken)
        out.append(Stone("%s|R|S%d" % (fr["name"], i), WC("roof_battens"), q[0], q[1], g["top"]((a0 + a1_) / 2) + lh + 2 * bt + bt / 2,
                         math.degrees(math.atan2(-g["D"][1], -g["D"][0])), L / math.cos(ang), cw, bt, math.degrees(ang)))
    # lemovani u pricky: kryci prkno pres horni konce prken a celni prkno k vstupu
    fl = rf.get("flashing")
    if fl:
        (p1x, p1y), (p2x, p2y) = fr["posts"]; ux, uy = p1x - p2x, p1y - p2y; ul = math.hypot(ux, uy); ux, uy = ux / ul, uy / ul
        nx, ny = fr["n"]                                  # dovnitr (ke hradbe)
        Lc = ul + 2 * fr.get("crossbeam_over", 0.45) * 100 + 30
        cx, cy = (p1x + p2x) / 2, (p1y + p2y) / 2
        sl_m = sum(g["sl"] for g in geo) / len(geo); ang = math.atan(sl_m)
        w_ = fl.get("w", 0.40) * 100; a_c = a_top + w_ / 2 - 5
        x, y = cx + nx * a_c, cy + ny * a_c
        ztop = ct + bh + lh + bt + bth + 1 - sl_m * a_c
        yn = -uy * nx + ux * ny                           # lokalni Y kryciho prkna miri dovnitr (+1) nebo ven (-1)
        out.append(Stone("%s|R|F" % fr["name"], WC("roof_flashing"), x, y, ztop + bt / 2, math.degrees(math.atan2(uy, ux)), Lc, w_, bt,
                         roll=-math.degrees(ang) * (1 if yn > 0 else -1)))
        h_ = fl.get("fascia", 0.25) * 100
        x, y = cx + nx * (a_top - bt / 2), cy + ny * (a_top - bt / 2)
        out.append(Stone("%s|R|C" % fr["name"], WC("roof_flashing"), x, y, ct + bh + lh + bt - h_ / 2 + 6, math.degrees(math.atan2(uy, ux)), Lc, bt, h_))
    return out


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
                         "wood_old": "Drevo_Stare", "floor": "Podlaha", "face": "Kamen",
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
