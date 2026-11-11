"""
build_ruin_blocks.py - zricenina z jednotlivych kamennych bloku (Unreal Editor 5.8)

Zed = vodorovne rady kamene. Kazda rada ma dva lice z lomovych kvadru (ruzne delky, prevazba)
a mezi nimi jadro z lomu a malty. Model rozpadu (stejny jako build_ruin.py) urci dochovanou vysku;
bloky nad ni zmizi, u paty se rozebira lic (odkryje se jadro), otvory se vyriznou, intaktni osteni
a oblouky se postavi z opracovanych kvadru.

Uprava zriceniny:
  - v levelu objemy (TriggerBox s tagem) -> pregenerovat:
        Ruin_Cut, Ruin_Opening:<okno|dvere|portal|brana|strilna|prulom> (+Ruin_Intact, Ruin_Protect),
        Ruin_Keep, Ruin_Explode (bloky jako samostatne actory k rucnimu posunu / mazani)
  - v datech (ruin_layout.json -> "edits"): cut / cut_box / set_height / restore  -> pregenerovat
  - rucne: v levelu smazat jednotlive bloky (instance), pak spustit capture_manual_edits()
           -> smazane bloky se zapisi do manual_edits.json a pri pregenerovani zustanou smazane

Pouziti v UE: Tools -> Execute Python Script -> build_ruin_blocks.py
  (ruin_layout.json a manual_edits.json vedle skriptu, nebo nastav LAYOUT_PATH)
Mimo UE: python build_ruin_blocks.py [ruin_layout.json]  -> statistika (pocet bloku)
"""
import json, math, os, random, sys, zlib

# ------------------------------------------------------------------ nastaveni
LAYOUT_PATH = None                       # None = ruin_layout.json vedle skriptu
AGE = None                               # None = podle JSON ("1650"); nebo "1540" / "1650"
OVERRIDE = {}                            # prepis parametru, napr. {"ROBBING": 6}
RUIN_TAG = "Zricenina_Ruin"
CUBE_MESH = "/Engine/BasicShapes/Cube.Cube"
# --- materialy: None = skript si sam vytvori M_RuinStone + MI_RuinFace/Core/Frame v MAT_DIR (textury ze StarterContent);
#     nebo cesta k vlastnimu materialu, napr. "/Game/Megascans/.../MI_Rock.MI_Rock"
MAT_FACE  = None                         # lic (lomove kameny)
MAT_CORE  = None                         # jadro (lom + malta)
MAT_FRAME = None                         # osteni, oblouky (opracovany kamen)
MAT_DIR   = "/Game/Skvt/Lapikus/Ruin/Materials"
TEXTURES = {   # kandidati (BaseColor, Normal) - pouzije se prvni existujici
    "face":  [("/Game/StarterContent/Textures/T_Rock_Slate_D", "/Game/StarterContent/Textures/T_Rock_Slate_N"),
              ("/Game/StarterContent/Textures/T_Rock_Basalt_D", "/Game/StarterContent/Textures/T_Rock_Basalt_N")],
    "core":  [("/Game/StarterContent/Textures/T_Rock_Basalt_D", "/Game/StarterContent/Textures/T_Rock_Basalt_N"),
              ("/Game/StarterContent/Textures/T_Concrete_Grime_D", None)],
    "frame": [("/Game/StarterContent/Textures/T_Rock_Sandstone_D", "/Game/StarterContent/Textures/T_Rock_Sandstone_N"),
              ("/Game/StarterContent/Textures/T_Rock_Slate_D", "/Game/StarterContent/Textures/T_Rock_Slate_N")],
}
# vzhled instanci materialu (lze pak menit primo v MI_* v editoru): tint A..B (nahodne na kamen), meritko textury, drsnost
MAT_LOOK = {
    "face":  dict(TintA=(0.62, 0.58, 0.52), TintB=(0.95, 0.90, 0.80), Tiling=0.9, Roughness=0.9),
    "core":  dict(TintA=(0.55, 0.52, 0.47), TintB=(0.75, 0.71, 0.64), Tiling=1.6, Roughness=0.95),
    "frame": dict(TintA=(0.85, 0.80, 0.70), TintB=(1.00, 0.95, 0.85), Tiling=0.7, Roughness=0.85),
}
# --- zaoblene zvetrale kameny lice (gen_stones.py -> stones/*.obj vedle skriptu; skript je sam naimportuje)
USE_STONE_MESHES = True                  # False = vsude kostky (Cube) jako drive
STONE_DIR   = "/Game/Skvt/Lapikus/Ruin/Stones"
STONE_RATIOS = [1.2, 1.8, 2.6, 3.4]      # pomer delka/vyska variant (SM_RuinStone_R12_A ...)
STONE_VARIANTS = "ABC"
STONE_NOMINAL = (30.0, 45.0, 30.0)        # vyska, hloubka (cm) jmenoviteho kamene; delka = vyska * pomer
STONE_OVERSIZE = 1.04                    # zaobleny kamen o kousek vetsi nez blok -> spary nejsou az moc hluboke
ASHLAR_MESH = "SM_RuinAshlar"
MAT_WOOD = ["/Game/StarterContent/Materials/M_Wood_Oak.M_Wood_Oak", "/Game/StarterContent/Materials/M_Wood_Pine.M_Wood_Pine"]   # tramy a prkna (prvni existujici)            # osteni a oblouky: lehce srazene hrany
BLOCK_BP  = "/Game/Skvt/Lapikus/Ruin/BP_RuinBlocks"   # zalozni Blueprint s InstancedStaticMesh (kdyz nejde pridat komponentu)
TERRAIN_FROM_LEVEL = True                # True = vysky terenu se pri buildu zmeri primo z landscapu v levelu (line trace)
                                         #   a ulozi do terrain_from_level.json (capture_manual_edits pouzije tento ulozeny stav)
                                         # False = vysky z ruin_layout.json (puvodni heightmapa)
ONLY_WALLS = None                        # napr. ["Brana_V", "Brana_J"] = postavit jen tyto zdi (rychle ladeni)

OPENING_TYPES = {
    "strilna":    dict(frame=0.20, lintel="kamen",  value=0.6),
    "okno":       dict(frame=0.25, lintel="kamen",  value=1.0),
    "okno_drevo": dict(frame=0.00, lintel="drevo",  value=0.0),
    "dvere":      dict(frame=0.30, lintel="kamen",  value=1.0),
    "portal":     dict(frame=0.35, lintel="oblouk", value=1.2),
    "brana":      dict(frame=0.45, lintel="oblouk", value=1.2),
    "prulom":     dict(frame=0.00, lintel="oblouk", value=0.0),   # pozdeji vybourany otvor: bez osteni, nepravidelny "oblouk"
    "kapsa":      dict(frame=0.00, lintel="kamen",  value=0.0),   # kapsa pro tram: jen ve vnitrnim lici (ne skrz zed)
}

# ------------------------------------------------------------------ pomocne
def smooth(v, k):
    n = len(v); h = k // 2; out = []
    for i in range(n):
        s = 0.0
        for j in range(i - h, i - h + k):
            s += v[min(max(j, 0), n - 1)]
        out.append(s / k)
    return out

def interp(xq, xs, ys):
    if xq <= xs[0]: return ys[0]
    if xq >= xs[-1]: return ys[-1]
    lo, hi = 0, len(xs) - 1
    while hi - lo > 1:
        m = (lo + hi) // 2
        if xs[m] <= xq: lo = m
        else: hi = m
    t = (xq - xs[lo]) / (xs[hi] - xs[lo]); return ys[lo] + (ys[hi] - ys[lo]) * t

class Terrain:
    def __init__(self, t): self.t = t
    def z(self, x, y):     # cm
        t = self.t; fx = (x - t["x0"]) / t["step"]; fy = (y - t["y0"]) / t["step"]
        ix = min(max(int(math.floor(fx)), 0), t["nx"] - 2); iy = min(max(int(math.floor(fy)), 0), t["ny"] - 2)
        ax = min(max(fx - ix, 0), 1); ay = min(max(fy - iy, 0), 1); Z = t["z"]
        return (Z[iy][ix] * (1 - ax) + Z[iy][ix + 1] * ax) * (1 - ay) + (Z[iy + 1][ix] * (1 - ax) + Z[iy + 1][ix + 1] * ax) * ay

# ------------------------------------------------------------------ rozpad
def opening_state(o, a_loc, rng, P):
    t = OPENING_TYPES[o.get("kind", "okno")]
    x0 = o["s"] - o["w"] / 2; x1 = o["s"] + o["w"] / 2; sill = o["sill"]; top = sill + o["h"]
    f_h = min(1.0, P["REACH"] / (sill + 1.5))
    score = a_loc * t["value"] * f_h * P.get("FRAME_ROB", 1.0) + rng.gauss(0, 0.06)
    robbed = "none" if (score < 0.25 or t["frame"] == 0) else ("one" if score < 0.42 else "both")
    robbed = o.get("robbed", robbed)
    side = o.get("side", "l" if rng.random() < 0.5 else "r")
    fr = t["frame"]
    wl = fr + rng.uniform(0, 0.15) if robbed == "both" or (robbed == "one" and side == "l") else 0.0
    wr = fr + rng.uniform(0, 0.15) if robbed == "both" or (robbed == "one" and side == "r") else 0.0
    arch = t["lintel"] == "oblouk"
    st = dict(kind=o.get("kind"), robbed=robbed, arch=arch, sill=sill, top=top, x0=x0, x1=x1, wl=wl, wr=wr, frame=fr,
              splay=o.get("splay"), ragged=o.get("ragged", 0.0), s=o["s"])
    if arch:
        st["jamb_h"] = min(P["FRAME_REACH"], top - (x1 - x0) / 2) if robbed != "none" else 0.0
        st["lintel_lost"] = robbed == "both" and not o.get("protect", False)
    else:
        st["jamb_h"] = 0.0
        if robbed == "both" and sill > 0: st["sill"] = max(0.0, sill - 0.3)
        st["lintel_lost"] = t["lintel"] == "drevo" or robbed == "both" or o.get("lintel_lost", False)
    return st

def opening_gap(st, x):
    """Vrati (spodek, vrsek) otvoru v miste x (m), nebo None."""
    x0, x1 = st["x0"], st["x1"]
    if st["arch"]:
        if x0 - st["wl"] <= x < x0 or x1 < x <= x1 + st["wr"]:
            return (st["sill"], st["sill"] + st["jamb_h"]) if st["jamb_h"] > 0 else None
        if x0 <= x <= x1:
            r = (x1 - x0) / 2; c = (x0 + x1) / 2; spring = st["top"] - r
            return (st["sill"], spring + math.sqrt(max(r * r - (x - c) ** 2, 0)))
        return None
    if x0 - st["wl"] <= x <= x1 + st["wr"]:
        return (st["sill"], st["top"])
    return None

def wall_profile(L, H0, access, corners, openings, breaches, protect, access_points, seed, P, mid=0.88, jag=0.45):
    rng = random.Random(seed * 7919 + P["SEED"])
    step = 0.25; n = int(L / step) + 1; xs = [i * step for i in range(n)]
    # dostupnost
    a = [access] * n
    for ap in access_points:
        a = [ai + P["ACCESS_BOOST"] * math.exp(-((x - ap) / P["ACCESS_RADIUS"]) ** 2) for ai, x in zip(a, xs)]
    a = smooth([min(max(v, 0), 1) for v in a], 9)
    orng = random.Random(seed * 104729 + P["SEED"])
    states = [opening_state(o, interp(o["s"], xs, a), orng, P) for o in openings]
    # 1) prirodni rozpad
    cs = sorted(set([0.0, L] + list(corners)))
    span = max(cs[i + 1] - cs[i] for i in range(len(cs) - 1))
    sc = max(1.5, min(6.0, span / 3)); cst = P["CORNER_STRENGTH"]
    noise = smooth([rng.gauss(0, 1) for _ in range(n)], 7)
    h = []
    for x, nz in zip(xs, noise):
        t = min(min(abs(x - c) for c in cs) / sc, 1.0)
        prof = 1.0 - (1.0 - mid) * (0.5 - 0.5 * math.cos(math.pi * t))
        h.append(H0 * P["WEATHER"] * prof * (1 + cst * (1 - t)) / (1 + cst) + jag * P.get("JAG", 1.0) * nz * 1.6)
    for st in states:
        if st["lintel_lost"]:
            c = (st["x0"] + st["x1"]) / 2; w = (st["x1"] - st["x0"]) / 2; k = math.tan(math.radians(57))
            h = [min(hi, max(st["top"] - 0.3 + max(0, abs(x - c) - w) * k, st["top"] - 0.3)) for hi, x in zip(h, xs)]
    for b in breaches:
        c = (b["s0"] + b["s1"]) / 2; w = (b["s1"] - b["s0"]) / 2
        kl = b.get("slope_l", b.get("slope", 1.0)); kr = b.get("slope_r", b.get("slope", 1.0))   # strmost boku (1 = 45 st.)
        pl = b.get("power_l", b.get("power", 1.0)); pr = b.get("power_r", b.get("power", 1.0))   # >1 = bok se ke koruně zvedá strměji (zaoblená linie)
        h = [min(hi, b["floor"] + max(0, (c - w) - x) ** pl * kl + max(0, x - (c + w)) ** pr * kr) for hi, x in zip(h, xs)]
    # 2) rozebirani podle dostupnosti a vysky
    R = P["REACH"]; work = smooth([rng.gauss(0, 1) for _ in range(n)], 15)
    out = []
    for hi, ai, wk in zip(h, a, work):
        A = P["ROBBING"] * ai; h0 = max(hi, 0.0)
        if h0 <= R: hr = h0 - A
        else:
            t1 = (h0 * h0 - R * R) / (2 * R * max(A, 1e-6))
            hr = math.sqrt(max(h0 * h0 - 2 * R * A, 0)) if t1 >= 1 else R - A * (1 - t1)
        out.append(hr + wk * 0.5 * ai if hr < hi else hi)
    # zbytek u paty: spodni rady zasypane zeminou a suti se nevyplati rozebirat
    rem = smooth([rng.uniform(0, 1) for _ in range(n)], 11)
    h = [max(o, min(hi, P.get("REMAIN", 0.0) * (0.6 + 0.8 * r))) for o, hi, r in zip(out, h, rem)]
    for pr in protect:
        h = [max(hi, pr["min"]) if pr["s0"] <= x <= pr["s1"] else hi for hi, x in zip(h, xs)]
    c = P["COURSE"]
    h = [math.floor(min(max(hi, 0.3), H0) / c) * c for hi in h]
    return xs, h, states


# ------------------------------------------------------------------ parametry a stari
def params(layout):
    P = dict(layout["params"])
    age = AGE or layout.get("age", "1540")
    P.update(layout.get("presets", {}).get(age, {}))
    P.update(OVERRIDE)
    P["_AGE"] = age
    return P

# ------------------------------------------------------------------ bloky
class Stone:
    __slots__ = ("id", "cat", "x", "y", "z", "yaw", "pitch", "roll", "sx", "sy", "sz", "seg", "span", "mesh")
    def __init__(self, sid, cat, x, y, z, yaw, sx, sy, sz, pitch=0.0, roll=0.0, seg=0):
        self.span = None; self.mesh = None
        self.seg = seg   # usek zdi (index rovneho useku mezi zlomy)
        self.id = sid; self.cat = cat; self.x = x; self.y = y; self.z = z; self.yaw = yaw
        self.sx = sx; self.sy = sy; self.sz = sz; self.pitch = pitch; self.roll = roll

def courses(zmin, zmax, rng, P):
    """Vodorovne rady (cm) spolecne pro celou zed."""
    out = []; z = zmin
    while z < zmax:
        hgt = rng.uniform(P["COURSE_MIN"], P["COURSE_MAX"]) * 100
        out.append((z, z + hgt)); z += hgt
    return out

def edit_applies(e, wname):
    w = e.get("wall")
    return w is None or w == wname or (isinstance(w, list) and wname in w)

def apply_plinth(wd):
    """podstavba (m): zed stoji na nizsim terenu -> vyska, parapety otvoru, ochrana a sesuvy se zvednou"""
    pl = wd.get("plinth", 0.0)
    if not pl: return wd
    wd = dict(wd, H0=wd["H0"] + pl)
    wd["openings"] = [dict(o, sill=o["sill"] + pl) for o in wd.get("openings", [])]
    wd["protect"] = [dict(p, min=p["min"] + pl) for p in wd.get("protect", [])]
    wd["breaches"] = [dict(b, floor=b["floor"] + pl) for b in wd.get("breaches", [])]
    return wd

def _pt_on(points, s):
    """bod na lomene care ve vzdalenosti s (m) od prvniho bodu"""
    c = 0.0
    for i in range(len(points) - 1):
        p, q = points[i], points[i + 1]; ln = math.hypot(q[0] - p[0], q[1] - p[1]) / 100
        if s <= c + ln or i == len(points) - 2:
            f = (s - c) / max(ln, 1e-6); return p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f
        c += ln

def apply_ref_z(wd, terr):
    """ref_z (absolutni cm, napr. podlaha veze): vysky otvoru (sill, splay floor/top) jsou zadane od ni,
    ne od paty zdi -> prevedou se na vysky od mistni paty."""
    ref = wd.get("ref_z")
    if ref is None: return wd
    ops = []
    for o in wd.get("openings", []):
        zb = terr.z(*_pt_on(wd["points"], o["s"]))
        o = dict(o, sill=(ref + o["sill"] * 100 - zb) / 100)
        if o.get("splay"):
            sp = o["splay"]; o["splay"] = dict(sp, floor=(ref + sp["floor"] * 100 - zb) / 100, top=(ref + sp["top"] * 100 - zb) / 100)
        ops.append(o)
    return dict(wd, openings=ops)

def build_wall_stones(wd, P, terr, layout, edits, removed, centroid):
    wd = apply_ref_z(apply_plinth(wd), terr)
    rng = random.Random(wd.get("seed", 1) * 4093 + P["SEED"])
    pts = [list(p) for p in wd["points"]]
    # roh: kazda zed se na zacatku prodlouzi o pul tloustky -> rohy budou plne (u uzavrenych obrysu)
    if wd.get("extend_start", True):
        dx, dy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]; dl = math.hypot(dx, dy) or 1
        e = wd["thickness"] * 50
        pts[0] = [pts[0][0] - dx / dl * e, pts[0][1] - dy / dl * e]
    shift = wd["thickness"] / 2 if wd.get("extend_start", True) else 0.0   # s v JSON plati od puvodniho bodu
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) / 100 for i in range(len(pts) - 1)]
    cum = [0.0]
    for s in seg: cum.append(cum[-1] + s)
    L = cum[-1]
    corners = list(wd.get("corners", [])) + cum[1:-1]
    sh = lambda lst, keys: [dict(d, **{k: d[k] + shift for k in keys if k in d}) for d in lst]
    xs, h, states = wall_profile(L, wd["H0"], wd["access"], [c + shift for c in corners[:len(wd.get("corners", []))]] + corners[len(wd.get("corners", [])):],
                                 sh(wd.get("openings", []), ["s"]), sh(wd.get("breaches", []), ["s0", "s1"]),
                                 sh(wd.get("protect", []), ["s0", "s1"]), [a + shift for a in wd.get("access_points", [])], wd.get("seed", 1), P,
                                 mid=wd.get("mid", 0.88))
    edits = [dict(e, **{k: e[k] + shift for k in ("s0", "s1") if k in e}) if e["op"] in ("cut", "set_height", "restore") else e for e in edits]
    # datove upravy vysky
    for e in edits:
        if e["op"] in ("set_height", "restore") and edit_applies(e, wd["name"]):
            for i, x in enumerate(xs):
                if e["s0"] <= x <= e["s1"]:
                    h[i] = e["h"] if e["op"] == "set_height" else max(h[i], e["h"])
    access_arr = [wd["access"]] * len(xs)
    for ap in wd.get("access_points", []):
        access_arr = [a + P["ACCESS_BOOST"] * math.exp(-((x - ap) / P["ACCESS_RADIUS"]) ** 2) for a, x in zip(access_arr, xs)]
    T = wd["thickness"] * 100
    face_d = min(P["FACE_DEPTH"] * 100, T * 0.4)
    core_w = max(T - 2 * face_d, 10)
    zref = layout["plateau_z_cm"]
    # pata a koruna v absolutnich cm podel zdi
    def at(s):
        k = 0
        while k < len(seg) - 1 and s > cum[k + 1]: k += 1
        p, q = pts[k], pts[k + 1]; f = (s - cum[k]) / max(seg[k], 1e-6)
        x = p[0] + (q[0] - p[0]) * f; y = p[1] + (q[1] - p[1]) * f
        yaw = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        nx, ny = -(q[1] - p[1]) / (seg[k] * 100), (q[0] - p[0]) / (seg[k] * 100)
        return x, y, yaw, nx, ny, k
    zlo = min(terr.z(*at(s)[:2]) for s in [i * 0.5 for i in range(int(L / 0.5) + 1)]) - 120
    zhi = zref + wd["H0"] * 100 + 200
    if wd.get("course_grid"):                     # pevne rady (vez): vsechny zdi maji spary ve stejne vysce jako patra
        g0, gh = wd["course_grid"][0], wd["course_grid"][1] * 100
        k0 = int(math.floor((zlo - g0) / gh)); k1 = int(math.ceil((zhi - g0) / gh))
        crs = [(g0 + k * gh, g0 + (k + 1) * gh) for k in range(k0, k1)]
    else:
        crs = courses(zlo, zhi, rng, P)
    # ktera strana je vnitrni (k tezisti hradu): +1 = levy lic (normala), -1 = pravy
    xm, ym, _, nxm, nym, _ = at(L / 2)
    inner = 1 if (xm + nxm * 100 - centroid[0]) ** 2 + (ym + nym * 100 - centroid[1]) ** 2 < (xm - centroid[0]) ** 2 + (ym - centroid[1]) ** 2 else -1
    if wd.get("inside_pt"):                        # vnitrek mistnosti (vez): strana pro kapsy a vyklenky strilen
        ip = wd["inside_pt"]
        inside = 1 if (ip[0] - xm) * nxm + (ip[1] - ym) * nym > 0 else -1
    else:
        inside = inner
    rside = wd.get("rubble", "both")
    robbed_sides = {"out": [inner], "in": [inner], "both": [1, -1]}.get(rside, [1, -1])  # vnejsi lic nad utesem se nerozebira
    stones = []
    # --- otvory zarovnat na rady kamene (parapet a nadprazi lezi na sparach) + rozmery osteni po radach
    bounds = [c0 for c0, c1 in crs] + [crs[-1][1]]
    def snap(zab): return min(bounds, key=lambda b: abs(b - zab))
    for st in states:
        sm_ = (st["x0"] + st["x1"]) / 2
        zb_o = terr.z(*at(sm_)[:2]); st["zb"] = zb_o
        h0 = st["top"] - st["sill"]
        if st["sill"] > 0.05: st["sill"] = (snap(zb_o + st["sill"] * 100) - zb_o) / 100
        top = (snap(zb_o + st["top"] * 100) - zb_o) / 100
        st["top"] = top if top - st["sill"] >= 0.6 * h0 else st["sill"] + h0
        st["inside"] = inside
        if st.get("splay"):
            sp = st["splay"]
            st["niche"] = (snap(zb_o + sp["floor"] * 100), snap(zb_o + sp["top"] * 100)); st["w_in"] = sp.get("w_in", 1.6)
        fr = st["frame"]
        st["framed"] = fr > 0 and not (st["robbed"] == "both" and not (st["arch"] and not st["lintel_lost"]))
        if st["arch"]:
            r = (st["x1"] - st["x0"]) / 2
            jb = st["sill"] + st.get("jamb_h", 0); jt = st["top"] - r
        else:
            jb, jt = st["sill"], st["top"]
        st["jamb_z"] = (zb_o + jb * 100, zb_o + jt * 100)
        st["lintel_z"] = st["sill_z"] = None
        if st["framed"] and not st["arch"] and st["kind"] in ("okno", "dvere", "strilna") and not st["lintel_lost"]:
            z0 = zb_o + st["top"] * 100; z1 = z0
            for c0, c1 in crs:                       # nadprazi = 1-2 rady nad otvorem (vyska >= 1.2 * osteni)
                if c0 >= z0 - 1 and z1 - z0 < fr * 120: z1 = c1
            st["lintel_z"] = (z0, z1)
            if st["sill"] > 0.05:
                cb = [c for c in crs if abs(c[1] - (zb_o + st["sill"] * 100)) < 1]
                if cb: st["sill_z"] = cb[0]
    def forbidden(cz0, cz1, layer=1):
        """useky s (m) v teto rade (cz0..cz1 absolutni cm), kam nesmi zadny blok zdi: svetlost otvoru
        + osteni/nadprazi/parapet/oblouk (ty postavi opracovane kvadry). Bloky se v techto mistech rozdeli
        -> otvor je vzdy pruhledny."""
        out = []
        e = 1.0                                       # cm
        for st in states:
            x0, x1, fr = st["x0"], st["x1"], st["frame"]
            z0r = (cz0 - st["zb"]) / 100; z1r = (cz1 - st["zb"]) / 100
            if st["kind"] == "kapsa":                  # kapsa: jen vnitrni lic
                if layer == st["inside"] and z1r > st["sill"] + 0.01 and z0r < st["top"] - 0.01:
                    out.append((x0, x1))
                continue
            if st.get("niche") and layer in (0, st["inside"]):
                # vyklenek strilny zevnitr: siroky prostor (do nej se postavi sikme boky) + preklad nad nim
                n0, n1 = st["niche"]; c = (x0 + x1) / 2; wi = st["w_in"] / 2
                if cz1 > n0 + e and cz0 < n1 - e: out.append((c - wi - 0.05, c + wi + 0.05))
                elif cz1 > n1 + e and cz0 < n1 + 36: out.append((c - wi - 0.25, c + wi + 0.25))
            if st.get("ragged") and layer != 0 and z1r > st["sill"] + 0.01 and z0r < st["top"] + 0.2:
                # rozbitejsi okraje pruchodu: lic kolem otvoru nahodne vylamany (jadro zustava)
                rr_ = random.Random(zlib.crc32(("%s|%d|%d" % (wd["name"], round(cz0), layer)).encode()))
                out.append((x0 - rr_.uniform(0, st["ragged"]), x0)); out.append((x1, x1 + rr_.uniform(0, st["ragged"])))
            framed = st["framed"]
            okL = st["arch"] or st["robbed"] != "one" or st.get("wl", 0) == 0
            okR = st["arch"] or st["robbed"] != "one" or st.get("wr", 0) == 0
            jz = st["jamb_z"]
            if framed and cz1 > jz[0] + e and cz0 < jz[1] - e:
                if okL: out.append((x0 - fr, x0))
                if okR: out.append((x1, x1 + fr))
            if st["arch"]:
                r = (x1 - x0) / 2; c = (x0 + x1) / 2; spring = st["top"] - r
                # vylomene opracovane kameny ostění: kdyz oblouk stoji, zustane za nimi jadro (nese oblouk)
                if st["jamb_h"] > 0 and z1r > st["sill"] + 0.01 and z0r < st["sill"] + st["jamb_h"] - 0.01 \
                   and (layer != 0 or st["lintel_lost"]):
                    if st["wl"] > 0: out.append((x0 - st["wl"], x0))
                    if st["wr"] > 0: out.append((x1, x1 + st["wr"]))
                rr = r + (fr if framed and not st["lintel_lost"] else 0.0)
                if z1r > st["sill"] + 0.01 and z0r < spring + rr - 0.01:
                    if z1r <= spring + 0.01:
                        out.append((x0, x1))               # pod patkou oblouku jen svetlost (paty nese zdivo / jadro)
                    else:
                        zl = max(z0r, spring)
                        hw = math.sqrt(max(rr * rr - (zl - spring) ** 2, 0.0))
                        out.append((c - hw, c + hw))
            else:
                if z1r > st["sill"] + 0.01 and z0r < st["top"] - 0.01:
                    if layer != 0 or st["lintel_lost"]:
                        out.append((x0 - st["wl"], x1 + st["wr"]))
                    else:                                  # nadprazi stoji -> jadro za vylomenym ostěním ho nese
                        out.append((x0, x1))
                for zz in (st["lintel_z"], st["sill_z"]):
                    if zz and cz1 > zz[0] + e and cz0 < zz[1] - e:
                        out.append((x0 - fr, x1 + fr))
        return out
    def subtract(s0, s1, bad):
        pieces = [(s0, s1)]
        for a, b in bad:
            nxt = []
            for p0, p1 in pieces:
                if b <= p0 or a >= p1: nxt.append((p0, p1)); continue
                if a > p0: nxt.append((p0, a))
                if b < p1: nxt.append((b, p1))
            pieces = nxt
        return [p for p in pieces if p[1] - p[0] >= 0.12]
    def cut_hit(x, y, z0, z1, s0, s1, z0r, z1r):
        for e in edits:
            if not edit_applies(e, wd["name"]): continue
            if e["op"] == "cut" and s1 > e["s0"] and s0 < e["s1"] and z1r > e["z0"] and z0r < e["z1"]: return True
            if e["op"] == "cut_box":
                b = e["box"]
                if b[0] <= x <= b[3] and b[1] <= y <= b[4] and z1 > b[2] and z0 < b[5]: return True
        return False
    prev = {1: None, 0: None, -1: None}           # obsazene useky predchozi rady (podpora)
    def lintel_over(s0, s1, z0r):
        for st in states:
            if st["lintel_lost"] or st["frame"] <= 0: continue
            if st["robbed"] == "both" and not st["arch"]: continue
            if s1 > st["x0"] - st["frame"] and s0 < st["x1"] + st["frame"] and z0r >= st["top"] - 0.05: return True
        return False
    for ci, (cz0, cz1) in enumerate(crs):
        cur = {1: [], 0: [], -1: []}
        # tri vrstvy: levy lic (+1), jadro (0), pravy lic (-1)
        for layer in (1, 0, -1):
            off = (T / 2 - face_d / 2) * layer if layer else 0.0
            depth = face_d if layer else core_w
            lmin, lmax = (P["STONE_MIN"], P["STONE_MAX"]) if layer else (P["CORE_MIN"], P["CORE_MAX"])
            s = -rng.uniform(0, lmax) if ci % 2 else 0.0           # prevazba
            if wd.get("extend_start", True) and layer == 0: s = face_d / 100     # jadro az za nárožním kvádrem
            bi = 0
            while s < L:
                ln = rng.uniform(lmin, lmax); s0 = max(s, 0.0); s1 = min(s + ln, L); s = s + ln
                sid = "%s|%d|%d|%d" % (wd["name"], ci, layer, bi); bi += 1
                srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])   # nahoda vazana na blok -> upravy neposunou ostatni
                # bloky nedelit pres roh polygonu
                for kc in cum[1:-1]:
                    if s0 < kc < s1:
                        if kc - s0 > s1 - kc: s1 = kc
                        else: s0 = kc
                if s1 - s0 < 0.12: continue
                zb0 = terr.z(*at((s0 + s1) / 2)[:2])
                pieces = subtract(s0, s1, forbidden(cz0, cz1, layer))
                sid0 = sid; os0, os1 = s0, s1
                for pi, (s0, s1) in enumerate(pieces):
                    # nerozdeleny blok si necha puvodni id (rucni upravy plati dal), kusy dostanou .a/.b
                    sid = sid0 if len(pieces) == 1 else "%s.%s" % (sid0, "abcdefgh"[pi])
                    if sid != sid0: srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
                    sc = (s0 + s1) / 2
                    x, y, yaw, nx, ny, k = at(sc)
                    zb = terr.z(x, y)
                    top_abs = zb + interp(sc, xs, h) * 100
                    if cz0 >= top_abs: continue
                    part = (top_abs - cz0) / (cz1 - cz0)
                    if part < 1 and srng.random() > part * 1.15: continue      # rozvolnena koruna
                    if cz1 < zb - 140: continue                              # hluboko pod terenem
                    z0r = (cz0 - zb) / 100; z1r = (cz1 - zb) / 100
                    # rozebrany lic u paty (odkryje jadro)
                    if layer in robbed_sides and layer != 0 and 0 <= z0r < P["FACE_ROB_H"] and part >= 1:
                        a = interp(sc, xs, access_arr)
                        if srng.random() < min(0.92, a * P["FACE_ROB"] * (1 - z0r / P["FACE_ROB_H"])): continue
                    cx = x + nx * off; cy = y + ny * off
                    if cut_hit(cx, cy, cz0, cz1, s0, s1, z0r, z1r): continue
                    # podpora: blok musi lezet na necem (predchozi rada v teze nebo vedlejsi vrstve, nebo nadprazi)
                    if z0r > 0.2 and prev[layer] is not None:
                        below = prev[layer] + (prev[0] if layer else prev[1] + prev[-1])
                        ov = sum(max(0, min(s1, b1) - max(s0, b0)) for b0, b1 in below)
                        if ov < 0.3 * (s1 - s0) and not lintel_over(s0, s1, z0r): continue
                    cur[layer].append((s0, s1))
                    # zchatrale: u koruny pootocene a vysunute bloky (u otvoru jen nepatrne, at nezasahuji do svetlosti)
                    loose = part < 1.6 and layer != 0
                    if abs(s0 - os0) > 1e-6 or abs(s1 - os1) > 1e-6: loose = False   # kus u otvoru: drzi lic
                    yaw2 = yaw + (srng.uniform(-6, 6) if loose else srng.uniform(-0.8, 0.8))
                    pitch = srng.uniform(-4, 4) if loose else 0.0
                    push = srng.uniform(0, 4) * layer if loose else 0.0
                    gapw = P["JOINT"] * 100
                    cxx = cx + nx * push; cyy = cy + ny * push
                    if layer == 0: gapw = 0.0                # jadro bez spar (je skryte) -> zed neni skrz pruhledna
                    stones.append(Stone(sid, "core" if layer == 0 else "face", cxx, cyy, (cz0 + cz1) / 2, yaw2,
                                        (s1 - s0) * 100 - gapw, depth - gapw, (cz1 - cz0) - gapw * 0.7, pitch, seg=k))
                    stones[-1].span = (s0, s1, z0r, z1r)           # pro kontrolu (test_openings.py)
        # narozni kvadr na zacatku zdi (zakryje prurez zdi v rohu)
        if wd.get("extend_start", True):
            sc = face_d / 200
            x, y, yaw, nx, ny, k = at(sc); zb = terr.z(x, y)
            top_abs = zb + interp(sc, xs, h) * 100
            z0r = (cz0 - zb) / 100; z1r = (cz1 - zb) / 100
            sid = "%s|%d|Q" % (wd["name"], ci)
            if cz1 <= top_abs and cz1 > zb - 140 and not cut_hit(x, y, cz0, cz1, 0, sc * 2, z0r, z1r) \
               and (z0r <= 0.2 or prev[1] is None or any(b0 < sc * 2 for b0, b1 in prev[1] + prev[-1])):
                stones.append(Stone(sid, "face", x, y, (cz0 + cz1) / 2, yaw + 90.0, T - 1.5, face_d - 1.5, (cz1 - cz0) - 1.0, seg=k))
                cur[1].append((0, sc * 2)); cur[-1].append((0, sc * 2))
        prev = cur
    # osteni a oblouky intaktnich otvoru (opracovane kvadry, cela tloustka zdi)
    for oi, st in enumerate(states):
        if st["frame"] <= 0: continue
        if st["robbed"] == "both" and not (st["arch"] and not st["lintel_lost"]): continue
        fr = st["frame"]; sm_ = (st["x0"] + st["x1"]) / 2
        x, y, yaw, nx, ny, k = at(sm_); zb = terr.z(x, y)
        wall_top = min(interp(s_, xs, h) for s_ in (st["x0"] - fr, sm_, st["x1"] + fr))
        sp_out = -st["inside"] if st.get("niche") else 0      # strilna s vyklenkem: osteni jen ve vnejsim lici
        def add(sid, s0, s1, z0r, z1r, rot_extra=0.0, sxo=None):
            if z1r > min(interp(s0, xs, h), interp(s1, xs, h)) + 0.05: return
            xx, yy, yw, nnx, nny, kk = at((s0 + s1) / 2)
            dep = (face_d - 1) if sp_out else (T - 2)
            o_ = (T / 2 - face_d / 2) * sp_out
            # o 2 cm presah do sousednich bloku -> zadna pruhledna spara kolem osteni
            stones.append(Stone(sid, "frame", xx + nnx * o_, yy + nny * o_, zb + (z0r + z1r) / 2 * 100, yw, sxo or (s1 - s0) * 100 + 2,
                                dep, (z1r - z0r) * 100 - 0.5, rot_extra, seg=kk))
        if st.get("niche"):
            # vyklenek: sikme boky (kónické rozsireni zevnitr k uzkemu pruzoru), preklad nahore
            n0, n1 = st["niche"]; c = sm_; wi = st["w_in"] / 2; wo = (st["x1"] - st["x0"]) / 2 + fr
            dep_in = T - face_d                                   # hloubka od vnitrniho lice k vnejsimu lici
            for side in (-1, 1):
                a_s = c + side * wo; b_s = c + side * wi              # s na vnejsim lici / na vnitrnim lici
                a_n = (T / 2 - face_d) * (-st["inside"]); b_n = (T / 2) * st["inside"]
                ax_, ay_, _, nnx, nny, kk = at(a_s); bx_, by_, _, _, _, _ = at(b_s)
                A = (ax_ + nnx * a_n, ay_ + nny * a_n); Bp = (bx_ + nnx * b_n, by_ + nny * b_n)
                dx_, dy_ = Bp[0] - A[0], Bp[1] - A[1]; ln = math.hypot(dx_, dy_)
                px_, py_ = -dy_ / ln, dx_ / ln                       # kolmo na bok; ven z vyklenku
                tx_, ty_ = at(c)[0] - (A[0] + Bp[0]) / 2, at(c)[1] - (A[1] + Bp[1]) / 2
                if px_ * tx_ + py_ * ty_ > 0: px_, py_ = -px_, -py_
                mx_, my_ = (A[0] + Bp[0]) / 2 + px_ * 15, (A[1] + Bp[1]) / 2 + py_ * 15
                yw_ = math.degrees(math.atan2(dy_, dx_))
                j = 0
                for c0, c1 in crs:
                    if c0 < n0 - 1 or c1 > n1 + 1: continue
                    if (c1 - zb) / 100 > min(interp(a_s, xs, h), interp(b_s, xs, h)) + 0.05: break
                    stones.append(Stone("%s|F%d|N%s%d" % (wd["name"], oi, "L" if side < 0 else "R", j), "frame", mx_, my_, (c0 + c1) / 2,
                                        yw_, ln + 8, 30, (c1 - c0) - 0.5, seg=kk))
                    j += 1
            lz0 = n1; lz1 = n1 + 35
            if (lz1 - zb) / 100 <= min(interp(c - wi, xs, h), interp(c + wi, xs, h)) + 0.05:
                xx, yy, yw, nnx, nny, kk = at(c); o_ = (face_d / 2) * st["inside"]
                stones.append(Stone("%s|F%d|NT" % (wd["name"], oi), "frame", xx + nnx * o_, yy + nny * o_, (lz0 + lz1) / 2, yw,
                                    (2 * wi + 0.5) * 100, dep_in - 1, (lz1 - lz0) - 0.5, seg=kk))
        okL = st["arch"] or st["robbed"] != "one" or st.get("wl", 0) == 0
        okR = st["arch"] or st["robbed"] != "one" or st.get("wr", 0) == 0
        jz0, jz1 = st["jamb_z"]
        j = 0
        for c0, c1 in crs:                                   # ostění po radach zdi
            z0 = max(c0, jz0); z1 = min(c1, jz1)
            if z1 - z0 < 3: continue
            z0r = (z0 - zb) / 100; z1r = (z1 - zb) / 100
            if okL: add("%s|F%d|L%d" % (wd["name"], oi, j), st["x0"] - fr, st["x0"], z0r, z1r)
            if okR: add("%s|F%d|R%d" % (wd["name"], oi, j), st["x1"], st["x1"] + fr, z0r, z1r)
            j += 1
        if st["lintel_z"]:
            add("%s|F%d|T" % (wd["name"], oi), st["x0"] - fr, st["x1"] + fr, (st["lintel_z"][0] - zb) / 100, (st["lintel_z"][1] - zb) / 100)
        if st["sill_z"]:
            add("%s|F%d|B" % (wd["name"], oi), st["x0"] - fr, st["x1"] + fr, (st["sill_z"][0] - zb) / 100, (st["sill_z"][1] - zb) / 100)
        if st["arch"] and not st["lintel_lost"]:
            r = (st["x1"] - st["x0"]) / 2; spring = st["top"] - r
            n = max(5, int(math.pi * (r + fr / 2) / 0.32))
            for q in range(n):
                a0 = math.pi * q / n; a1 = math.pi * (q + 1) / n; am = (a0 + a1) / 2
                rm = r + fr / 2
                s_c = sm_ - rm * math.cos(am); z_c = spring + rm * math.sin(am)
                if z_c + fr / 2 > interp(s_c, xs, h) + 0.15: continue
                xx, yy, yw, _, _, kk = at(s_c)
                sid = "%s|F%d|A%d" % (wd["name"], oi, q)
                # klinovy kamen: delka po oblouku, natoceny kolem normaly zdi (roll)
                stones.append(Stone(sid, "frame", xx, yy, zb + z_c * 100, yw, rm * (a1 - a0) * 100 - 1.5, T - 2, fr * 100,
                                    pitch=90.0 - math.degrees(am), seg=kk))
    # svisly posun cele zdi (m), napr. zapusteni do terenu; kameny pod terenem nejsou videt
    off = wd.get("z_offset", 0.0) * 100
    if off:
        for st_ in stones: st_.z += off
        for st_ in states: st_["zb"] += off
    return stones, states, L

def _clip_segment_box(p, q, x0, y0, x1, y1):
    """Liang-Barsky: cast usecky p->q uvnitr obdelniku, vrati (t0, t1) nebo None."""
    dx, dy = q[0] - p[0], q[1] - p[1]; t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0: return None
        else:
            r = qq / pp
            if pp < 0: t0 = max(t0, r)
            else: t1 = min(t1, r)
    return (t0, t1) if t0 < t1 else None

def wall_box_hits(wd, box, terr):
    """Kde box (x0,y0,z0,x1,y1,z1 v cm) protina osu zdi: [(s0, s1, sill_m, top_m)], s od prvniho bodu zdi."""
    pts = wd["points"]; hits = []; cum = 0.0
    pad = wd["thickness"] * 50
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]; ln = math.hypot(q[0] - p[0], q[1] - p[1]) / 100
        r = _clip_segment_box(p, q, box[0] - pad * 0.2, box[1] - pad * 0.2, box[3] + pad * 0.2, box[4] + pad * 0.2)
        if r:
            t0, t1 = r; tm = (t0 + t1) / 2
            zb = terr.z(p[0] + (q[0] - p[0]) * tm, p[1] + (q[1] - p[1]) * tm)
            hits.append((cum + t0 * ln, cum + t1 * ln, (box[2] - zb) / 100, (box[5] - zb) / 100))
        cum += ln
    return hits

def apply_volumes(layout, volumes, terr):
    """Prevede objemy z levelu (TriggerBox s tagem) na upravy:
       Ruin_Cut            -> cut_box (vyrizne vse uvnitr)
       Ruin_Opening:<typ>  -> novy otvor ve zdi (okno, dvere, portal, brana, strilna, prulom) s plnou logikou rozpadu
                              + Ruin_Intact (osteni cele) / Ruin_Protect (oblouk se nezrouti)
       Ruin_Keep           -> restore: zdi v boxu alespon do vysky vrsku boxu
       Ruin_Explode        -> bloky uvnitr jako samostatne actory (rucni posun / mazani)"""
    walls = [dict(w, openings=list(w.get("openings", []))) for w in layout["walls"]]
    edits = list(layout.get("edits", [])); explode = []
    for v in volumes:
        tags = v["tags"]; box = v["box"]
        if "Ruin_Cut" in tags:
            edits.append({"op": "cut_box", "box": box})
        if "Ruin_Explode" in tags:
            explode.append(box)
        kinds = [t.split(":", 1)[1] for t in tags if t.startswith("Ruin_Opening:")]
        keep = "Ruin_Keep" in tags
        if not kinds and not keep: continue
        for w in walls:
            for s0, s1, sill, top in wall_box_hits(w, box, terr):
                if s1 - s0 < 0.1: continue
                if keep:
                    edits.append({"op": "restore", "wall": w["name"], "s0": s0, "s1": s1, "h": top})
                for kind in kinds:
                    o = dict(kind=kind if kind in OPENING_TYPES else "prulom", s=(s0 + s1) / 2, w=s1 - s0,
                             sill=max(0.0, sill), h=max(0.3, top - max(0.0, sill)))
                    if "Ruin_Intact" in tags: o["robbed"] = "none"
                    if "Ruin_Protect" in tags: o["protect"] = True
                    w["openings"].append(o)
    return dict(layout, walls=walls, edits=edits), explode

def in_box(s, box):
    return box[0] <= s.x <= box[3] and box[1] <= s.y <= box[4] and box[2] <= s.z <= box[5]

def stone_mesh_name(st):
    """Varianta zaobleneho kamene podle pomeru delka/vyska bloku (deterministicky podle id)."""
    if not USE_STONE_MESHES: return None
    if st.cat in ("frame", "floor"): return ASHLAR_MESH
    if st.cat != "face": return None
    r = max(st.sx, 1) / max(st.sz, 1)
    best = min(STONE_RATIOS, key=lambda q: abs(math.log(r / q)))
    v = STONE_VARIANTS[zlib.crc32(st.id.encode()) % len(STONE_VARIANTS)]
    return "SM_RuinStone_R%02d_%s" % (round(best * 10), v)

def assign_meshes(stones):
    for st in stones:
        st.mesh = stone_mesh_name(st)
        if st.mesh and st.cat == "face" and (zlib.crc32(st.id.encode()) >> 8) & 1:
            st.yaw += 180.0          # otoceni kamene o 180 st. = dalsi varianta vzhledu (rozmer sedi)

def build_floor_stones(fs, P, walls_out):
    """Podlahy ve vezi (layout["floors"]): kamenna dlazba prizemi + tramy v kapsach a hrube prkna v patrech.
    Souradnice v ramu veze: u (m) podel fs["u"], v (m) podel fs["v"] od fs["origin"]."""
    rng = random.Random(zlib.crc32(fs["name"].encode()) ^ P["SEED"])
    ox, oy = fs["origin"]; ux, uy = fs["u"]; vx, vy = fs["v"]
    u0, u1, v0, v1 = fs["inner"]
    W = lambda u, v: (ox + (u * ux + v * vx) * 100, oy + (u * uy + v * vy) * 100)
    yaw_u = math.degrees(math.atan2(uy, ux)); yaw_v = math.degrees(math.atan2(vy, vx))
    ref = fs["ref_z"]; out = []
    # --- kamenna podlaha prizemi (horni plocha = ref_z)
    sf = fs.get("stone_floor")
    if sf:
        t = sf.get("thickness", 0.18) * 100; v = v0; r = 0
        while v < v1 - 0.05:
            dv = min(rng.uniform(0.45, 0.8), v1 - v); u = u0 - rng.uniform(0, 0.4) * (r % 2); c = 0
            while u < u1 - 0.05:
                du = rng.uniform(0.5, 1.0); a, b = max(u, u0), min(u + du, u1)
                sid = "%s|P|%d|%d" % (fs["name"], r, c); c += 1; u += du
                if b - a < 0.15: continue
                srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
                if srng.random() < sf.get("missing", 0.07): continue
                x, y = W((a + b) / 2, v + dv / 2)
                tilt = srng.random() < 0.12
                out.append(Stone(sid, "floor", x, y, ref - t / 2 + (srng.uniform(0, 3) if tilt else 0), yaw_u + srng.uniform(-1.5, 1.5),
                                 (b - a) * 100 - 1.5, dv * 100 - 1.5, t, pitch=srng.uniform(-3, 3) if tilt else 0.0,
                                 roll=srng.uniform(-3, 3) if tilt else 0.0))
            v += dv; r += 1
    # --- patra: tramy v kapsach, prkna na tramech (horni plocha prken = ref_z + n * storey)
    bm = fs["beams"]; pk = fs.get("planks", {}); hatch = fs.get("hatch")
    def wall_stands(x, y, zmin):
        for wn in fs.get("walls", []):
            for s_ in walls_out.get(wn, {}).get("stones", []):
                if abs(s_.x - x) < 130 and abs(s_.y - y) < 130 and s_.z > zmin: return True
        return False
    for lvl in fs.get("levels", []):
        zt = ref + lvl * fs["storey"] * 100
        bh = bm.get("h", 0.28) * 100; bw = bm.get("w", 0.26) * 100; brg = bm.get("bearing", 0.33)
        ok_v = []
        for i, vb in enumerate(bm["v"]):
            ea = W(u0 - brg / 2, vb); eb = W(u1 + brg / 2, vb)
            if not (wall_stands(ea[0], ea[1], zt + 30) and wall_stands(eb[0], eb[1], zt + 30)): continue   # zed u kapsy spadla -> tram chybi
            sid = "%s|B%d|%d" % (fs["name"], lvl, i); srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
            x, y = W((u0 + u1) / 2, vb + srng.uniform(-0.02, 0.02))
            out.append(Stone(sid, "wood", x, y, zt - 6 - bh / 2, yaw_u + srng.uniform(-0.4, 0.4), (u1 - u0 + 2 * brg) * 100 - 4, bw, bh,
                             pitch=srng.uniform(-0.3, 0.3)))
            ok_v.append(vb)
        if len(ok_v) < 2: continue
        t = pk.get("t", 0.05) * 100; u = u0; r = 0
        while u < u1 - 0.05:
            w_ = min(rng.uniform(pk.get("wmin", 0.2), pk.get("wmax", 0.34)), u1 - u)
            uc = u + w_ / 2; u += w_ + rng.uniform(0.005, 0.02); r += 1
            if w_ < 0.08: continue
            # prkno z kusu, spoje vzdy nad tramem (2-3 pole na kus), prvni a posledni kus az ke zdi
            joints = [ok_v[0] - 0.75 if ok_v[0] - 0.75 > v0 else v0]
            k = rng.randint(1, 2)
            while k < len(ok_v) - 1:
                joints.append(ok_v[k]); k += rng.randint(2, 3)
            joints.append(v1)
            for j in range(len(joints) - 1):
                a, b = joints[j], joints[j + 1]
                if j == 0: a = v0
                pieces = [(a, b)]
                if hatch and hatch[0] < uc < hatch[1]:
                    pieces = [(p0, min(p1, hatch[2])) for p0, p1 in pieces if p0 < hatch[2]] + \
                             [(max(p0, hatch[3]), p1) for p0, p1 in pieces if p1 > hatch[3]]
                for q, (pa, pb) in enumerate(pieces):
                    if pb - pa < 0.3: continue
                    sid = "%s|K%d|%d|%d%s" % (fs["name"], lvl, r, j, "abc"[q])
                    srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
                    if srng.random() < pk.get("missing", 0.04): continue
                    x, y = W(uc + srng.uniform(-0.01, 0.01), (pa + pb) / 2)
                    out.append(Stone(sid, "wood", x, y, zt - 1 - t / 2 + srng.uniform(-0.4, 0.4), yaw_v + srng.uniform(-1.0, 1.0),
                                     (pb - pa) * 100 - 1, w_ * 100 - 0.5, t, roll=srng.uniform(-0.6, 0.6)))
    return out

def compute_blocks(layout, removed=(), moved=None, volumes=None):
    P = params(layout); terr = Terrain(layout["terrain"])
    vols = list(layout.get("volumes", [])) + list(volumes or [])
    layout, explode = apply_volumes(layout, vols, terr)
    removed = set(removed); moved = moved or {}
    edits = list(layout.get("edits", []))
    allpts = [p for w in layout["walls"] for p in w["points"]]
    centroid = (sum(p[0] for p in allpts) / len(allpts), sum(p[1] for p in allpts) / len(allpts))
    out = {}
    for wd in layout["walls"]:
        if ONLY_WALLS and wd["name"] not in ONLY_WALLS: continue
        stones, states, L = build_wall_stones(wd, P, terr, layout, edits, removed, centroid)
        out[wd["name"]] = dict(folder=wd["folder"], stones=stones)
    for fs in layout.get("floors", []):
        if ONLY_WALLS and fs["name"] not in ONLY_WALLS and not any(w in ONLY_WALLS for w in fs.get("walls", [])): continue
        out[fs["name"]] = dict(folder=fs.get("folder", "Ruin"), stones=build_floor_stones(fs, P, out))
    # trocha suti z bloku (vetsinu lide odvezli)
    rub = []
    for name, w in out.items():
        rng = random.Random(zlib.crc32(name.encode()) ^ (P["SEED"] * 977))
        faces = [s for s in w["stones"] if s.cat == "face"]
        if not faces: continue
        n = int(len(faces) * P["RUBBLE_BLOCKS"])
        for i in range(n):
            s = rng.choice(faces); d = rng.choice((-1, 1)) * rng.uniform(80, 300)
            yaw = math.radians(s.yaw); nx, ny = -math.sin(yaw), math.cos(yaw)
            x = s.x + nx * d + rng.uniform(-60, 60); y = s.y + ny * d + rng.uniform(-60, 60)
            z = terr.z(x, y) + 8
            rub.append(Stone("%s|R%d" % (name, i), "face", x, y, z, rng.uniform(0, 360), s.sx, s.sy, s.sz,
                             rng.uniform(-25, 25), rng.uniform(-25, 25)))
        w["rubble"] = [r for r in rub if r.id.startswith(name + "|") and r.id not in removed]
    for w in out.values():
        assign_meshes(w["stones"] + w.get("rubble", []))
    for name, w in out.items():
        w["stones"] = [st for st in w["stones"] if st.id not in removed]
        # rucne posunute bloky a rozlozeni na samostatne kameny
        # samostatne kameny = jen ty v boxu Ruin_Explode (podle puvodni i posunute polohy);
        # posunute kameny mimo box se vrati do Instanced Static Mesh na nove misto ("slouceni")
        loose_ids = set()
        for st in w["stones"] + w.get("rubble", []):
            if any(in_box(st, b) for b in explode): loose_ids.add(st.id)
            m = moved.get(st.id)
            if m:
                st.x, st.y, st.z, st.roll, st.pitch, st.yaw = m
                if any(in_box(st, b) for b in explode): loose_ids.add(st.id)
        loose_ids.update(st.id for st in w.get("rubble", []))      # kameny na zemi vzdy samostatne
        w["loose"] = [st for st in w["stones"] + w.get("rubble", []) if st.id in loose_ids]
        lid = set(id(st) for st in w["loose"])
        w["stones"] = [st for st in w["stones"] if id(st) not in lid]
        w["rubble"] = [st for st in w.get("rubble", []) if id(st) not in lid]
    return out, P

# ------------------------------------------------------------------ Unreal
def _script_dir():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.path.dirname(LAYOUT_PATH) if LAYOUT_PATH else os.getcwd()

def load_layout():
    path = LAYOUT_PATH or os.path.join(_script_dir(), "ruin_layout.json")
    with open(path, encoding="utf-8") as f: return json.load(f)

def edits_path():
    return os.path.join(os.path.dirname(LAYOUT_PATH) if LAYOUT_PATH else _script_dir(), "manual_edits.json")

def load_manual():
    p = edits_path()
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f: d = json.load(f)
        return d.get("removed", []), d.get("moved", {})
    return [], {}

def load_removed():
    return load_manual()[0]

def gather_volumes(unreal, eas):
    """TriggerBoxy (nebo jine actory) s tagy Ruin_Cut / Ruin_Opening:<typ> / Ruin_Keep / Ruin_Explode."""
    vols = []
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        if not any(t.startswith(("Ruin_Cut", "Ruin_Opening", "Ruin_Keep", "Ruin_Explode")) for t in tags): continue
        origin, ext = a.get_actor_bounds(False)
        vols.append(dict(tags=tags, name=a.get_actor_label(),
                         box=[origin.x - ext.x, origin.y - ext.y, origin.z - ext.z, origin.x + ext.x, origin.y + ext.y, origin.z + ext.z]))
    return vols

def _asset_path(folder, name): return "%s/%s.%s" % (folder, name, name)

def ensure_materials(unreal):
    """Vrati {"face": mat, "core": mat, "frame": mat}. Chybejici M_RuinStone / MI_Ruin* vytvori (jen poprve,
    pak je muzes upravovat v editoru - skript je neprepise)."""
    eal = unreal.EditorAssetLibrary
    mats = {}
    user = {"face": MAT_FACE, "core": MAT_CORE, "frame": MAT_FRAME}
    if all(user.values()):
        return {c: unreal.load_asset(p) for c, p in user.items()}
    def pick(cat):
        for d, n in TEXTURES[cat]:
            if eal.does_asset_exist(d): return unreal.load_asset(d), (unreal.load_asset(n) if n and eal.does_asset_exist(n) else None)
        return None, None
    at = unreal.AssetToolsHelpers.get_asset_tools(); mel = unreal.MaterialEditingLibrary
    mpath = _asset_path(MAT_DIR, "M_RuinStone")
    if eal.does_asset_exist(mpath):
        master = unreal.load_asset(mpath)
    else:
        d0, n0 = pick("face")
        if not d0:
            unreal.log_warning("Ruin: nenalezeny textury pro material (StarterContent?) - nastav MAT_FACE/MAT_CORE/MAT_FRAME.")
            return {c: (unreal.load_asset(p) if p else None) for c, p in user.items()}
        master = at.create_asset("M_RuinStone", MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
        for prop in ("used_with_instanced_static_meshes", "used_with_nanite"):
            try: master.set_editor_property(prop, True)
            except Exception: pass
        E = lambda cls, x, y: mel.create_material_expression(master, cls, x, y)
        tc = E(unreal.MaterialExpressionTextureCoordinate, -1400, 0)
        pir = E(unreal.MaterialExpressionPerInstanceRandom, -1400, 200)
        k = E(unreal.MaterialExpressionConstant, -1400, 300); k.set_editor_property("r", 7.31)
        mul = E(unreal.MaterialExpressionMultiply, -1200, 250)
        mel.connect_material_expressions(pir, "", mul, "A"); mel.connect_material_expressions(k, "", mul, "B")
        add = E(unreal.MaterialExpressionAdd, -1000, 100)          # nahodny posun UV na kamen -> kazdy kamen jinak
        mel.connect_material_expressions(tc, "", add, "A"); mel.connect_material_expressions(mul, "", add, "B")
        til = E(unreal.MaterialExpressionScalarParameter, -1000, 300)
        til.set_editor_property("parameter_name", "Tiling"); til.set_editor_property("default_value", 1.0)
        uv = E(unreal.MaterialExpressionMultiply, -800, 150)
        mel.connect_material_expressions(add, "", uv, "A"); mel.connect_material_expressions(til, "", uv, "B")
        tx = E(unreal.MaterialExpressionTextureSampleParameter2D, -550, -100)
        tx.set_editor_property("parameter_name", "BaseColor"); tx.set_editor_property("texture", d0)
        mel.connect_material_expressions(uv, "", tx, "UVs")
        ta = E(unreal.MaterialExpressionVectorParameter, -550, 200); ta.set_editor_property("parameter_name", "TintA")
        ta.set_editor_property("default_value", unreal.LinearColor(0.62, 0.58, 0.52, 1))
        tb = E(unreal.MaterialExpressionVectorParameter, -550, 400); tb.set_editor_property("parameter_name", "TintB")
        tb.set_editor_property("default_value", unreal.LinearColor(0.95, 0.90, 0.80, 1))
        lp = E(unreal.MaterialExpressionLinearInterpolate, -300, 300)
        mel.connect_material_expressions(ta, "", lp, "A"); mel.connect_material_expressions(tb, "", lp, "B")
        mel.connect_material_expressions(pir, "", lp, "Alpha")
        bc = E(unreal.MaterialExpressionMultiply, -100, 0)
        mel.connect_material_expressions(tx, "RGB", bc, "A"); mel.connect_material_expressions(lp, "", bc, "B")
        mel.connect_material_property(bc, "", unreal.MaterialProperty.MP_BASE_COLOR)
        ro = E(unreal.MaterialExpressionScalarParameter, -300, 600)
        ro.set_editor_property("parameter_name", "Roughness"); ro.set_editor_property("default_value", 0.9)
        mel.connect_material_property(ro, "", unreal.MaterialProperty.MP_ROUGHNESS)
        if n0:
            nx = E(unreal.MaterialExpressionTextureSampleParameter2D, -550, 800)
            nx.set_editor_property("parameter_name", "Normal"); nx.set_editor_property("texture", n0)
            nx.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
            mel.connect_material_expressions(uv, "", nx, "UVs")
            mel.connect_material_property(nx, "RGB", unreal.MaterialProperty.MP_NORMAL)
        mel.recompile_material(master)
        eal.save_loaded_asset(master)
        unreal.log("Ruin: vytvoren material %s" % mpath)
    for cat, mi_name in (("face", "MI_RuinFace"), ("core", "MI_RuinCore"), ("frame", "MI_RuinFrame")):
        if user[cat]:
            mats[cat] = unreal.load_asset(user[cat]); continue
        ip = _asset_path(MAT_DIR, mi_name)
        if eal.does_asset_exist(ip):
            mats[cat] = unreal.load_asset(ip); continue
        mi = at.create_asset(mi_name, MAT_DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
        mel.set_material_instance_parent(mi, master)
        d, n = pick(cat)
        if d: mel.set_material_instance_texture_parameter_value(mi, "BaseColor", d)
        if n:
            try: mel.set_material_instance_texture_parameter_value(mi, "Normal", n)
            except Exception: pass
        lk = MAT_LOOK[cat]
        for pn in ("TintA", "TintB"):
            c = lk[pn]; mel.set_material_instance_vector_parameter_value(mi, pn, unreal.LinearColor(c[0], c[1], c[2], 1))
        for pn in ("Tiling", "Roughness"):
            mel.set_material_instance_scalar_parameter_value(mi, pn, lk[pn])
        mel.update_material_instance(mi)
        eal.save_loaded_asset(mi)
        mats[cat] = mi
    return mats

def _needed_meshes():
    names = ["SM_RuinStone_R%02d_%s" % (round(r * 10), v) for r in STONE_RATIOS for v in STONE_VARIANTS]
    return names + [ASHLAR_MESH]

def ensure_stone_meshes(unreal):
    """Nacte zaoblene kameny z STONE_DIR; chybejici naimportuje ze stones/*.obj vedle skriptu
    (box kolize + Nanite). Vrati {jmeno: StaticMesh}; co chybi, nahradi se kostkou."""
    if not USE_STONE_MESHES: return {}
    eal = unreal.EditorAssetLibrary
    missing = [n for n in _needed_meshes() if not eal.does_asset_exist(_asset_path(STONE_DIR, n))]
    src = os.path.join(_script_dir(), "stones")
    tasks = []
    for n in missing:
        f = os.path.join(src, n + ".obj")
        if not os.path.exists(f): continue
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", f); t.set_editor_property("destination_path", STONE_DIR)
        t.set_editor_property("destination_name", n)
        t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True)
        t.set_editor_property("save", True)
        tasks.append(t)
    if tasks:
        unreal.log("Ruin: importuji %d kamenu z %s" % (len(tasks), src))
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    out = {}
    sms = None
    try: sms = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    except Exception: pass
    for n in _needed_meshes():
        pth = _asset_path(STONE_DIR, n)
        if not eal.does_asset_exist(pth):
            # Interchange obcas pojmenuje asset jinak (napr. podle objektu v OBJ) - zkus najit podle jmena
            hits = [a for a in eal.list_assets(STONE_DIR, recursive=True) if a.split(".")[-1].startswith(n)] \
                if eal.does_directory_exist(STONE_DIR) else []
            if not hits: continue
            pth = hits[0]
        sm = unreal.load_asset(pth)
        if not isinstance(sm, unreal.StaticMesh): continue
        if n in [t.get_editor_property("destination_name") for t in tasks] and sms:
            try:      # jednoducha kolize = kvadr (hrac nepropadne)
                sms.remove_collisions(sm); sms.add_simple_collisions(sm, unreal.ScriptCollisionShapeType.BOX)
            except Exception as ex: unreal.log_warning("Ruin: kolize %s: %s (pridej rucne Collision -> Add Box)" % (n, ex))
            try:
                ns = sm.get_editor_property("nanite_settings"); ns.set_editor_property("enabled", True)
                sms.set_nanite_settings(sm, ns, True)
            except Exception as ex: unreal.log_warning("Ruin: Nanite %s: %s (zapni rucne v meshi)" % (n, ex))
            eal.save_loaded_asset(sm)
        out[n] = sm
    lost = [n for n in _needed_meshes() if n not in out]
    if lost:
        unreal.log_warning("Ruin: chybi %d kamenu (%s...) -> pouziji se kostky. Zkopiruj slozku stones/ vedle skriptu." % (len(lost), lost[0]))
    return out

_FIX = {}
def _mesh_fix(unreal, mesh, nominal):
    """Lokalni transformace meshe: posun pivotu do stredu, prohozeni os (kdyz import otocil osy) a rozmer.
    Vrati (Transform rotace+posun pro jednotkove meritko, extent po osach meshe, role os)."""
    key = mesh.get_path_name()
    if key in _FIX: return _FIX[key]
    bb = mesh.get_bounding_box()
    mn, mx = bb.min, bb.max
    ext = [max(mx.x - mn.x, 0.01), max(mx.y - mn.y, 0.01), max(mx.z - mn.z, 0.01)]
    c = [(mx.x + mn.x) / 2, (mx.y + mn.y) / 2, (mx.z + mn.z) / 2]
    import itertools
    em = max(ext); nm = max(nominal)
    best = min(itertools.permutations(range(3)),
               key=lambda pr: sum(abs(ext[i] / em - nominal[pr[i]] / nm) for i in range(3)))
    # sloupce rotace: osa meshe i -> svetova role best[i]; liche permutace -> zrcadleni jedne osy (det = +1)
    cols = []
    for i in range(3):
        v = [0.0, 0.0, 0.0]; v[best[i]] = 1.0; cols.append(v)
    inv = sum(1 for i in range(3) for j in range(i + 1, 3) if best[i] > best[j])
    if inv % 2: cols[0] = [-q for q in cols[0]]
    V = lambda q: unreal.Vector(q[0], q[1], q[2])
    rot = unreal.MathLibrary.make_rotation_from_axes(V(cols[0]), V(cols[1]), V(cols[2]))
    _FIX[key] = (rot, ext, best, c)
    return _FIX[key]

def stone_transform(unreal, s, mesh, nominal):
    """Transformace instance: mesh naskalovany presne na rozmer bloku (s.sx, s.sy, s.sz)."""
    rot, ext, role, c = _mesh_fix(unreal, mesh, nominal)
    k = STONE_OVERSIZE if s.mesh and s.cat == "face" else 1.0
    dims = [max(s.sx, 2) * k, max(s.sy, 2) * k, max(s.sz, 2) * k]
    sc = [dims[role[i]] / ext[i] for i in range(3)]
    local = unreal.Transform(location=unreal.Vector(-c[0] * sc[0], -c[1] * sc[1], -c[2] * sc[2]),
                             rotation=unreal.Rotator(0, 0, 0), scale=unreal.Vector(sc[0], sc[1], sc[2]))
    fix = unreal.Transform(location=unreal.Vector(0, 0, 0), rotation=rot, scale=unreal.Vector(1, 1, 1))
    st = unreal.Transform(location=unreal.Vector(s.x, s.y, s.z), rotation=unreal.Rotator(roll=s.roll, pitch=s.pitch, yaw=s.yaw),
                          scale=unreal.Vector(1, 1, 1))
    cm = unreal.MathLibrary.compose_transforms
    return cm(cm(local, fix), st)

def _unit(unreal, t):
    loc, rot, _ = unreal.MathLibrary.break_transform(t)
    return unreal.Transform(location=loc, rotation=rot, scale=unreal.Vector(1, 1, 1))

def _fix_unit(unreal, s, mesh, nominal):
    """Korekce meshe bez meritka: actor = F * kamen (presne invertovatelne)."""
    rot, ext, role, c = _mesh_fix(unreal, mesh, nominal)
    full = stone_transform(unreal, s, mesh, nominal)
    st = unreal.Transform(location=unreal.Vector(s.x, s.y, s.z), rotation=unreal.Rotator(roll=s.roll, pitch=s.pitch, yaw=s.yaw),
                          scale=unreal.Vector(1, 1, 1))
    return unreal.MathLibrary.compose_transforms(_unit(unreal, full), unreal.MathLibrary.invert_transform(st))

def _resolve(unreal, s, cube, meshes):
    m = meshes.get(s.mesh) if s.mesh else None
    if m is None: return cube, (100.0, 100.0, 100.0)
    if s.mesh == ASHLAR_MESH: return m, (100.0, 100.0, 100.0)
    r = float(s.mesh.rsplit("_R", 1)[1][:2]) / 10
    h, d = STONE_NOMINAL[0], STONE_NOMINAL[1]
    return m, (h * r, d, h)

def _new_actor(unreal, eas):
    actor = eas.spawn_actor_from_class(unreal.Actor, unreal.Vector(0, 0, 0))
    sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    root = sds.k2_gather_subobject_data_for_instance(actor)[0]
    return actor, sds, root

def _add_ism(unreal, sds, root):
    prm = unreal.AddNewSubobjectParams(parent_handle=root, new_class=unreal.InstancedStaticMeshComponent, blueprint_context=None)
    handle, fail = sds.add_new_subobject(prm)
    comp = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle))
    if not isinstance(comp, unreal.InstancedStaticMeshComponent): raise RuntimeError("komponenta nevznikla")
    return comp

def _ism_actor(unreal, eas, name, folder, parts, material, tag):
    """Actor s InstancedStaticMeshComponent pro kazdy mesh v parts [(mesh, [Transform])].
    Komponenty pres SubobjectDataSubsystem, jinak Blueprint BLOCK_BP (pak jeden actor na mesh)."""
    actors = []
    try:
        actor, sds, root = _new_actor(unreal, eas)
        try:
            comps = [_add_ism(unreal, sds, root) for _ in parts]
        except Exception:
            eas.destroy_actor(actor); raise
        for comp, (mesh, trs) in zip(comps, parts):
            comp.set_static_mesh(mesh)
            if material: comp.set_material(0, material)
            comp.add_instances(trs, False, True)
        actors.append(actor)
    except Exception as ex:
        bp = unreal.load_asset(BLOCK_BP)
        if not bp:
            raise RuntimeError("Nejde pridat InstancedStaticMeshComponent (%s) a chybi Blueprint %s. "
                               "Vytvor ho podle README_bloky.md kap. 1." % (ex, BLOCK_BP))
        for mesh, trs in parts:
            actor = eas.spawn_actor_from_object(bp, unreal.Vector(0, 0, 0), unreal.Rotator())
            comp = actor.get_component_by_class(unreal.InstancedStaticMeshComponent)
            comp.set_static_mesh(mesh)
            if material: comp.set_material(0, material)
            comp.add_instances(trs, False, True)
            actors.append(actor)
    for i, actor in enumerate(actors):
        actor.tags = [tag, unreal.Name("RuinBlocks")]
        actor.set_folder_path(folder)
        actor.set_actor_label(name if i == 0 else "%s_%d" % (name, i + 1))
    return actors

def _terrain_cache_path():
    return os.path.join(os.path.dirname(os.path.abspath(LAYOUT_PATH)) if LAYOUT_PATH else _script_dir(), "terrain_from_level.json")

def sample_level_terrain(unreal, layout):
    """Zmeri vysky landscapu v mrizce layout["terrain"] (line trace shora, ignoruje vse krome landscapu).
    Vysledek ulozi do terrain_from_level.json a vrati upraveny layout."""
    t = layout["terrain"]
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    x0, y0, st, nx, ny = t["x0"], t["y0"], t["step"], t["nx"], t["ny"]
    x1, y1 = x0 + (nx - 1) * st, y0 + (ny - 1) * st
    ignore = []
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.LandscapeProxy): continue
        try:
            o, e = a.get_actor_bounds(False)
            if o.x + e.x < x0 or o.x - e.x > x1 or o.y + e.y < y0 or o.y - e.y > y1: continue
        except Exception:
            pass
        ignore.append(a)
    Z = [row[:] for row in t["z"]]; hits = 0
    with unreal.ScopedSlowTask(ny, "Merim teren z landscapu...") as task:
        task.make_dialog(True)
        for j in range(ny):
            task.enter_progress_frame(1)
            for i in range(nx):
                x, y = x0 + i * st, y0 + j * st
                res = unreal.SystemLibrary.line_trace_single(world, unreal.Vector(x, y, 200000), unreal.Vector(x, y, -200000),
                                                            unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ignore,
                                                            unreal.DrawDebugTrace.NONE, True)
                hit = res[-1] if isinstance(res, tuple) else res
                if hit is None: continue
                try: vals = list(unreal.GameplayStatics.break_hit_result(hit))
                except Exception: vals = list(hit.to_tuple())
                if not vals or not vals[0]: continue
                act = next((v for v in vals if isinstance(v, unreal.Actor)), None)
                loc = next((v for v in vals if isinstance(v, unreal.Vector)), None)
                if loc is None or (act is not None and not isinstance(act, unreal.LandscapeProxy)): continue
                Z[j][i] = round(loc.z); hits += 1
    layout = dict(layout, terrain=dict(t, z=Z))
    with open(_terrain_cache_path(), "w", encoding="utf-8") as f:
        json.dump(dict(t, z=Z, hits=hits), f)
    unreal.log("Ruin: teren z levelu - %d / %d bodu zasahlo landscape (ulozeno terrain_from_level.json)" % (hits, nx * ny))
    if hits < nx * ny * 0.5:
        unreal.log_warning("Ruin: landscape zasazen jen v %d bodech - zbytek z ruin_layout.json. Ma landscape kolizi?" % hits)
    return layout

def cached_level_terrain(layout):
    p = _terrain_cache_path()
    if TERRAIN_FROM_LEVEL and os.path.exists(p):
        t = json.load(open(p, encoding="utf-8")); t.pop("hits", None)
        if (t["x0"], t["y0"], t["nx"], t["ny"]) == (layout["terrain"]["x0"], layout["terrain"]["y0"], layout["terrain"]["nx"], layout["terrain"]["ny"]):
            return dict(layout, terrain=t)
    return layout

def build_in_unreal():
    import unreal
    layout = load_layout(); removed, moved = load_manual()
    if TERRAIN_FROM_LEVEL:
        try:
            layout = sample_level_terrain(unreal, layout)
        except Exception as ex:
            unreal.log_warning("Ruin: mereni terenu z levelu selhalo (%s) - pouziji vysky z ruin_layout.json" % ex)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    vols = gather_volumes(unreal, eas)
    data, P = compute_blocks(layout, removed, moved, vols)
    cube = unreal.load_asset(CUBE_MESH)
    mats = ensure_materials(unreal)
    mats["floor"] = mats.get("frame")
    mats["wood"] = next((unreal.load_asset(p) for p in MAT_WOOD if unreal.EditorAssetLibrary.does_asset_exist(p.split(".")[0])), None)
    meshes = ensure_stone_meshes(unreal)
    tag = unreal.Name(RUIN_TAG); n_total = 0
    with unreal.ScopedEditorTransaction("Build ruin (blocks)"):
        old = [a for a in eas.get_all_level_actors() if tag in a.tags
               and (not ONLY_WALLS or any(a.get_actor_label().startswith(w + "_") for w in ONLY_WALLS))]
        if old: eas.destroy_actors(old)
        with unreal.ScopedSlowTask(len(data), "Stavim zriceninu z bloku...") as task:
            task.make_dialog(True)
            for name, w in data.items():
                task.enter_progress_frame(1, name)
                groups = {}
                for s in w["stones"] + w.get("rubble", []):
                    groups.setdefault((s.seg, s.cat), []).append(s)
                nseg = len(set(k[0] for k in groups))
                for (seg, cat), sts in sorted(groups.items()):
                    bym = {}
                    for s in sts:
                        m, nom = _resolve(unreal, s, cube, meshes)
                        bym.setdefault(m.get_path_name(), [m, []])[1].append(stone_transform(unreal, s, m, nom))
                    cname = {"face": "Lic", "core": "Jadro", "frame": "Osteni", "wood": "Drevo", "floor": "Podlaha"}[cat]
                    label = ("%s_%02d_%s" % (name, seg + 1, cname)) if nseg > 1 else ("%s_%s" % (name, cname))
                    _ism_actor(unreal, eas, label, w["folder"] + ("/%s" % name if nseg > 1 else ""),
                               [tuple(v) for _, v in sorted(bym.items())], mats.get(cat), tag)
                    n_total += len(sts)
                # samostatne kameny (sut, Ruin_Explode / rucne posunute): kazdy vlastni actor, ID v tagu
                for s in w.get("loose", []):
                    m, nom = _resolve(unreal, s, cube, meshes)
                    act = eas.spawn_actor_from_object(m, unreal.Vector(s.x, s.y, s.z), unreal.Rotator(roll=s.roll, pitch=s.pitch, yaw=s.yaw))
                    if not act: continue
                    act.set_actor_transform(stone_transform(unreal, s, m, nom), False, False)
                    act.tags = [tag, unreal.Name("RuinStone"), unreal.Name("id:" + s.id)]
                    act.set_folder_path(w["folder"] + ("/Sut" if "|R" in s.id else "/Kameny"))
                    act.set_actor_label("Kamen_" + s.id.replace("|", "_"))
                    if mats.get(s.cat): act.static_mesh_component.set_material(0, mats[s.cat])
                    n_total += 1
    unreal.log("Zricenina z bloku (%s): %d bloku ve %d zdech, objemu %d, samostatnych kamenu %d, rucne smazanych %d, posunutych %d, zaoblenych meshu %d." % (
        P["_AGE"], n_total, len(data), len(vols), sum(len(w.get("loose", [])) for w in data.values()), len(removed), len(moved), len(meshes)))

def capture_manual_edits():
    """Ulozi rucni upravy do manual_edits.json:
       - smazane bloky (chybi v Instanced Static Mesh nebo chybi samostatny kamen)
       - posunute / pootocene samostatne kameny (Ruin_Explode)"""
    import unreal
    layout = cached_level_terrain(load_layout()); removed, moved = load_manual(); removed = set(removed)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    data, P = compute_blocks(layout, removed, moved, gather_volumes(unreal, eas))
    cube = unreal.load_asset(CUBE_MESH)
    meshes = ensure_stone_meshes(unreal)
    present = set(); loose_now = {}
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        if RUIN_TAG not in tags: continue
        ids = [t[3:] for t in tags if t.startswith("id:")]
        if ids:
            loose_now[ids[0]] = a
            continue
        for comp in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
            for i in range(comp.get_instance_count()):
                res = comp.get_instance_transform(i, True)
                tr = res[-1] if isinstance(res, tuple) else res
                t = tr.translation
                present.add((round(t.x), round(t.y), round(t.z)))
    n_rem = 0; n_mov = 0
    for name, w in data.items():
        for s in w["stones"] + w.get("rubble", []):
            m, nom = _resolve(unreal, s, cube, meshes)
            t = stone_transform(unreal, s, m, nom).translation
            if (round(t.x), round(t.y), round(t.z)) not in present:
                removed.add(s.id); n_rem += 1
        for s in w.get("loose", []):
            a = loose_now.get(s.id)
            if a is None:
                removed.add(s.id); moved.pop(s.id, None); n_rem += 1; continue
            # poloha "kamene" = transformace actoru bez lokalni korekce meshe (F = otoceni os + posun pivotu, meritko 1)
            m, nom = _resolve(unreal, s, cube, meshes)
            st_t = unreal.MathLibrary.compose_transforms(unreal.MathLibrary.invert_transform(_fix_unit(unreal, s, m, nom)),
                                                         _unit(unreal, a.get_actor_transform()))
            loc, rot, _ = unreal.MathLibrary.break_transform(st_t)
            cur = [loc.x, loc.y, loc.z, rot.roll, rot.pitch, rot.yaw]
            same = all(abs(p - q) < 1.0 for p, q in zip(cur[:3], [s.x, s.y, s.z])) and \
                   all(abs(((p - q) + 180) % 360 - 180) < 1.0 for p, q in zip(cur[3:], [s.roll, s.pitch, s.yaw]))
            if not same:
                moved[s.id] = [round(v, 2) for v in cur]; n_mov += 1
    with open(edits_path(), "w", encoding="utf-8") as f:
        json.dump({"removed": sorted(removed), "moved": moved}, f, ensure_ascii=False, indent=1)
    unreal.log("manual_edits.json: smazano %d (nove %d), posunuto %d (nove %d)." % (len(removed), n_rem, len(moved), n_mov))

def _has_unreal():
    try:
        import unreal  # noqa
        return True
    except ImportError:
        return False

MODE = "build"        # "build" = postavit, "capture" = ulozit rucne smazane bloky

if __name__ == "__main__" or "unreal" in sys.modules:
    if _has_unreal():
        capture_manual_edits() if MODE == "capture" else build_in_unreal()
    else:
        if len(sys.argv) > 1: LAYOUT_PATH = sys.argv[1]
        lay = load_layout(); rm, mv = load_manual(); data, P = compute_blocks(lay, rm, mv)
        tot = 0
        for n, w in data.items():
            c = {"face": 0, "core": 0, "frame": 0, "wood": 0, "floor": 0}
            for s in w["stones"] + w.get("loose", []): c[s.cat] = c.get(s.cat, 0) + 1
            tot += sum(c.values()) + len(w.get("rubble", []))
            print("  %-18s lic %5d  jadro %4d  osteni %3d  sut %3d" % (n, c["face"], c["core"], c["frame"], len(w.get("rubble", [])))
                  + ("  drevo %4d  dlazba %3d" % (c["wood"], c["floor"]) if c["wood"] or c["floor"] else ""))
        print("stari:", P["_AGE"], " bloku celkem:", tot)
