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
MAT_FACE  = "/Game/StarterContent/Materials/M_Brick_Hewn_Stone.M_Brick_Hewn_Stone"    # lic (lomove kvadry)
MAT_CORE  = "/Game/StarterContent/Materials/M_Concrete_Grime.M_Concrete_Grime"        # jadro (lom + malta)
MAT_FRAME = "/Game/StarterContent/Materials/M_Rock_Sandstone.M_Rock_Sandstone"        # osteni, oblouky (opracovany kamen)
BLOCK_BP  = "/Game/Skvt/Lapikus/Ruin/BP_RuinBlocks"   # zalozni Blueprint s InstancedStaticMesh (kdyz nejde pridat komponentu)
ONLY_WALLS = None                        # napr. ["Brana_V", "Brana_J"] = postavit jen tyto zdi (rychle ladeni)

OPENING_TYPES = {
    "strilna":    dict(frame=0.20, lintel="kamen",  value=0.6),
    "okno":       dict(frame=0.25, lintel="kamen",  value=1.0),
    "okno_drevo": dict(frame=0.00, lintel="drevo",  value=0.0),
    "dvere":      dict(frame=0.30, lintel="kamen",  value=1.0),
    "portal":     dict(frame=0.35, lintel="oblouk", value=1.2),
    "brana":      dict(frame=0.45, lintel="oblouk", value=1.2),
    "prulom":     dict(frame=0.00, lintel="oblouk", value=0.0),   # pozdeji vybourany otvor: bez osteni, nepravidelny "oblouk"
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
    st = dict(kind=o.get("kind"), robbed=robbed, arch=arch, sill=sill, top=top, x0=x0, x1=x1, wl=wl, wr=wr, frame=fr)
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
        h = [min(hi, b["floor"] + max(0, abs(x - c) - w)) for hi, x in zip(h, xs)]
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
    __slots__ = ("id", "cat", "x", "y", "z", "yaw", "pitch", "roll", "sx", "sy", "sz")
    def __init__(self, sid, cat, x, y, z, yaw, sx, sy, sz, pitch=0.0, roll=0.0):
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

def build_wall_stones(wd, P, terr, layout, edits, removed, centroid):
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
    crs = courses(zlo, zhi, rng, P)
    # ktera strana je vnitrni (k tezisti hradu): +1 = levy lic (normala), -1 = pravy
    xm, ym, _, nxm, nym, _ = at(L / 2)
    inner = 1 if (xm + nxm * 100 - centroid[0]) ** 2 + (ym + nym * 100 - centroid[1]) ** 2 < (xm - centroid[0]) ** 2 + (ym - centroid[1]) ** 2 else -1
    rside = wd.get("rubble", "both")
    robbed_sides = {"out": [inner], "in": [inner], "both": [1, -1]}.get(rside, [1, -1])  # vnejsi lic nad utesem se nerozebira
    stones = []
    def gap_hit(s0, s1, z0r, z1r):
        for st in states:
            for sx in (s0 + 0.03, (s0 + s1) / 2, s1 - 0.03):
                g = opening_gap(st, sx)
                if g and z1r > g[0] + 0.02 and z0r < g[1] - 0.02: return True
        return False
    def frame_band(s0, s1, z0r, z1r):
        """blok v pasu osteni intaktniho otvoru -> nahradi ho opracovany kvadr osteni"""
        for st in states:
            if st["frame"] <= 0: continue
            if st["robbed"] == "both" and not (st["arch"] and not st["lintel_lost"]): continue
            fr = st["frame"]
            for (a, b, on) in ((st["x0"] - fr, st["x0"], st["robbed"] != "one" or st.get("wl", 0) == 0),
                               (st["x1"], st["x1"] + fr, st["robbed"] != "one" or st.get("wr", 0) == 0)):
                if on and s1 > a and s0 < b and z0r < st["top"] + (0 if st["arch"] else fr) and z1r > st["sill"]:
                    return True
        return False
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
                sc = (s0 + s1) / 2
                x, y, yaw, nx, ny, k = at(sc)
                zb = terr.z(x, y)
                top_abs = zb + interp(sc, xs, h) * 100
                if cz0 >= top_abs: continue
                part = (top_abs - cz0) / (cz1 - cz0)
                if part < 1 and srng.random() > part * 1.15: continue      # rozvolnena koruna
                if cz1 < zb - 140: continue                              # hluboko pod terenem
                z0r = (cz0 - zb) / 100; z1r = (cz1 - zb) / 100
                if gap_hit(s0, s1, z0r, z1r): continue
                if layer and frame_band(s0, s1, z0r, z1r): continue
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
                # zchatrale: u koruny pootocene a vysunute bloky
                loose = part < 1.6 and layer != 0
                yaw2 = yaw + (srng.uniform(-6, 6) if loose else srng.uniform(-0.8, 0.8))
                pitch = srng.uniform(-4, 4) if loose else 0.0
                push = srng.uniform(0, 4) * layer if loose else 0.0
                gapw = P["JOINT"] * 100
                cxx = cx + nx * push; cyy = cy + ny * push
                stones.append(Stone(sid, "core" if layer == 0 else "face", cxx, cyy, (cz0 + cz1) / 2, yaw2,
                                    (s1 - s0) * 100 - gapw, depth - gapw, (cz1 - cz0) - gapw * 0.7, pitch))
        # narozni kvadr na zacatku zdi (zakryje prurez zdi v rohu)
        if wd.get("extend_start", True):
            sc = face_d / 200
            x, y, yaw, nx, ny, k = at(sc); zb = terr.z(x, y)
            top_abs = zb + interp(sc, xs, h) * 100
            z0r = (cz0 - zb) / 100; z1r = (cz1 - zb) / 100
            sid = "%s|%d|Q" % (wd["name"], ci)
            if cz1 <= top_abs and cz1 > zb - 140 and not cut_hit(x, y, cz0, cz1, 0, sc * 2, z0r, z1r) \
               and (z0r <= 0.2 or prev[1] is None or any(b0 < sc * 2 for b0, b1 in prev[1] + prev[-1])):
                stones.append(Stone(sid, "face", x, y, (cz0 + cz1) / 2, yaw + 90.0, T - 1.5, face_d - 1.5, (cz1 - cz0) - 1.0))
                cur[1].append((0, sc * 2)); cur[-1].append((0, sc * 2))
        prev = cur
    # osteni a oblouky intaktnich otvoru (opracovane kvadry, cela tloustka zdi)
    for oi, st in enumerate(states):
        if st["frame"] <= 0: continue
        if st["robbed"] == "both" and not (st["arch"] and not st["lintel_lost"]): continue
        fr = st["frame"]; sm_ = (st["x0"] + st["x1"]) / 2
        x, y, yaw, nx, ny, k = at(sm_); zb = terr.z(x, y)
        wall_top = min(interp(s_, xs, h) for s_ in (st["x0"] - fr, sm_, st["x1"] + fr))
        def add(sid, s0, s1, z0r, z1r, rot_extra=0.0, sxo=None):
            if z1r > min(interp(s0, xs, h), interp(s1, xs, h)) + 0.05: return
            xx, yy, yw, *_ = at((s0 + s1) / 2)
            stones.append(Stone(sid, "frame", xx, yy, zb + (z0r + z1r) / 2 * 100, yw, sxo or (s1 - s0) * 100 - 1,
                                T - 2, (z1r - z0r) * 100 - 1, rot_extra))
        jamb_top = st["top"] - ((st["x1"] - st["x0"]) / 2 if st["arch"] else 0)
        z = st["sill"] if not st["arch"] else st["sill"] + st.get("jamb_h", 0)
        j = 0
        while z < jamb_top - 0.05:
            hh = min(rng.uniform(0.35, 0.55), jamb_top - z)
            okL = st["arch"] or st["robbed"] != "one" or st.get("wl", 0) == 0
            okR = st["arch"] or st["robbed"] != "one" or st.get("wr", 0) == 0
            if okL: add("%s|F%d|L%d" % (wd["name"], oi, j), st["x0"] - fr, st["x0"], z, z + hh)
            if okR: add("%s|F%d|R%d" % (wd["name"], oi, j), st["x1"], st["x1"] + fr, z, z + hh)
            z += hh; j += 1
        if st["kind"] in ("okno", "dvere", "strilna") and not st["lintel_lost"]:
            add("%s|F%d|T" % (wd["name"], oi), st["x0"] - fr, st["x1"] + fr, st["top"], st["top"] + fr * 1.2)
            if st["sill"] > 0.05:
                add("%s|F%d|B" % (wd["name"], oi), st["x0"] - fr * 0.6, st["x1"] + fr * 0.6, st["sill"] - fr * 0.6, st["sill"])
        if st["arch"] and not st["lintel_lost"]:
            r = (st["x1"] - st["x0"]) / 2; spring = st["top"] - r
            n = max(5, int(math.pi * (r + fr / 2) / 0.32))
            for q in range(n):
                a0 = math.pi * q / n; a1 = math.pi * (q + 1) / n; am = (a0 + a1) / 2
                rm = r + fr / 2
                s_c = sm_ - rm * math.cos(am); z_c = spring + rm * math.sin(am)
                if z_c + fr / 2 > interp(s_c, xs, h) + 0.15: continue
                xx, yy, yw, *_ = at(s_c)
                sid = "%s|F%d|A%d" % (wd["name"], oi, q)
                # klinovy kamen: delka po oblouku, natoceny kolem normaly zdi (roll)
                stones.append(Stone(sid, "frame", xx, yy, zb + z_c * 100, yw, rm * (a1 - a0) * 100 - 1.5, T - 2, fr * 100,
                                    pitch=90.0 - math.degrees(am)))
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
    for name, w in out.items():
        w["stones"] = [st for st in w["stones"] if st.id not in removed]
        # rucne posunute bloky a rozlozeni na samostatne kameny
        for st in w["stones"] + w.get("rubble", []):
            m = moved.get(st.id)
            if m: st.x, st.y, st.z, st.roll, st.pitch, st.yaw = m
        w["loose"] = [st for st in w["stones"] + w.get("rubble", []) if st.id in moved or any(in_box(st, b) for b in explode)]
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

def _ism_actor(unreal, eas, name, folder, mesh, material, transforms, tag):
    """Actor s InstancedStaticMeshComponent. Zkusi pridat komponentu pres SubobjectDataSubsystem,
    jinak pouzije Blueprint BLOCK_BP (Actor s komponentou InstancedStaticMesh)."""
    comp = None; actor = None
    try:
        actor = eas.spawn_actor_from_class(unreal.Actor, unreal.Vector(0, 0, 0))
        sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
        root = sds.k2_gather_subobject_data_for_instance(actor)[0]
        prm = unreal.AddNewSubobjectParams(parent_handle=root, new_class=unreal.InstancedStaticMeshComponent, blueprint_context=None)
        handle, fail = sds.add_new_subobject(prm)
        comp = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle))
        if not isinstance(comp, unreal.InstancedStaticMeshComponent): raise RuntimeError("komponenta nevznikla")
    except Exception as ex:
        if actor: eas.destroy_actor(actor)
        bp = unreal.load_asset(BLOCK_BP)
        if not bp:
            raise RuntimeError("Nejde pridat InstancedStaticMeshComponent (%s) a chybi Blueprint %s. "
                               "Vytvor ho podle README_bloky.md kap. 1." % (ex, BLOCK_BP))
        actor = eas.spawn_actor_from_object(bp, unreal.Vector(0, 0, 0), unreal.Rotator())
        comp = actor.get_component_by_class(unreal.InstancedStaticMeshComponent)
    comp.set_static_mesh(mesh)
    if material: comp.set_material(0, material)
    comp.add_instances(transforms, False, True)
    actor.tags = [tag, unreal.Name("RuinBlocks")]
    actor.set_folder_path(folder)
    actor.set_actor_label(name)
    return actor

def build_in_unreal():
    import unreal
    layout = load_layout(); removed, moved = load_manual()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    vols = gather_volumes(unreal, eas)
    data, P = compute_blocks(layout, removed, moved, vols)
    cube = unreal.load_asset(CUBE_MESH)
    mats = {c: (unreal.load_asset(p) if p else None) for c, p in (("face", MAT_FACE), ("core", MAT_CORE), ("frame", MAT_FRAME))}
    tag = unreal.Name(RUIN_TAG); n_total = 0
    with unreal.ScopedEditorTransaction("Build ruin (blocks)"):
        old = [a for a in eas.get_all_level_actors() if tag in a.tags
               and (not ONLY_WALLS or any(a.get_actor_label().startswith(w + "_") for w in ONLY_WALLS))]
        if old: eas.destroy_actors(old)
        with unreal.ScopedSlowTask(len(data), "Stavim zriceninu z bloku...") as task:
            task.make_dialog(True)
            for name, w in data.items():
                task.enter_progress_frame(1, name)
                groups = {"face": [], "core": [], "frame": []}
                for s in w["stones"] + w.get("rubble", []):
                    groups[s.cat].append(s)
                for cat, sts in groups.items():
                    if not sts: continue
                    tr = [unreal.Transform(location=unreal.Vector(s.x, s.y, s.z),
                                           rotation=unreal.Rotator(roll=s.roll, pitch=s.pitch, yaw=s.yaw),
                                           scale=unreal.Vector(max(s.sx, 2) / 100, max(s.sy, 2) / 100, max(s.sz, 2) / 100)) for s in sts]
                    _ism_actor(unreal, eas, "%s_%s" % (name, {"face": "Lic", "core": "Jadro", "frame": "Osteni"}[cat]),
                               w["folder"], cube, mats[cat], tr, tag)
                    n_total += len(sts)
                # samostatne kameny (Ruin_Explode / rucne posunute): kazdy vlastni actor, ID v tagu
                for s in w.get("loose", []):
                    act = eas.spawn_actor_from_object(cube, unreal.Vector(s.x, s.y, s.z), unreal.Rotator(roll=s.roll, pitch=s.pitch, yaw=s.yaw))
                    if not act: continue
                    act.set_actor_scale3d(unreal.Vector(max(s.sx, 2) / 100, max(s.sy, 2) / 100, max(s.sz, 2) / 100))
                    act.tags = [tag, unreal.Name("RuinStone"), unreal.Name("id:" + s.id)]
                    act.set_folder_path(w["folder"] + "/Kameny")
                    act.set_actor_label("Kamen_" + s.id.replace("|", "_"))
                    if mats[s.cat]: act.static_mesh_component.set_material(0, mats[s.cat])
                    n_total += 1
    unreal.log("Zricenina z bloku (%s): %d bloku ve %d zdech, objemu %d, samostatnych kamenu %d, rucne smazanych %d, posunutych %d." % (
        P["_AGE"], n_total, len(data), len(vols), sum(len(w.get("loose", [])) for w in data.values()), len(removed), len(moved)))

def capture_manual_edits():
    """Ulozi rucni upravy do manual_edits.json:
       - smazane bloky (chybi v Instanced Static Mesh nebo chybi samostatny kamen)
       - posunute / pootocene samostatne kameny (Ruin_Explode)"""
    import unreal
    layout = load_layout(); removed, moved = load_manual(); removed = set(removed)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    data, P = compute_blocks(layout, removed, moved, gather_volumes(unreal, eas))
    present = set(); loose_now = {}
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        if RUIN_TAG not in tags: continue
        ids = [t[3:] for t in tags if t.startswith("id:")]
        if ids:
            loc = a.get_actor_location(); rot = a.get_actor_rotation()
            loose_now[ids[0]] = [loc.x, loc.y, loc.z, rot.roll, rot.pitch, rot.yaw]
            continue
        comp = a.get_component_by_class(unreal.InstancedStaticMeshComponent)
        if not comp: continue
        for i in range(comp.get_instance_count()):
            res = comp.get_instance_transform(i, True)
            tr = res[-1] if isinstance(res, tuple) else res
            t = tr.translation
            present.add((round(t.x), round(t.y), round(t.z)))
    n_rem = 0; n_mov = 0
    for name, w in data.items():
        for s in w["stones"] + w.get("rubble", []):
            if (round(s.x), round(s.y), round(s.z)) not in present:
                removed.add(s.id); n_rem += 1
        for s in w.get("loose", []):
            cur = loose_now.get(s.id)
            if cur is None:
                removed.add(s.id); moved.pop(s.id, None); n_rem += 1
            elif any(abs(a - b) > 0.5 for a, b in zip(cur, [s.x, s.y, s.z, s.roll, s.pitch, s.yaw])):
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
            c = {"face": 0, "core": 0, "frame": 0}
            for s in w["stones"]: c[s.cat] += 1
            tot += sum(c.values()) + len(w.get("rubble", []))
            print("  %-18s lic %5d  jadro %4d  osteni %3d  sut %3d" % (n, c["face"], c["core"], c["frame"], len(w.get("rubble", []))))
        print("stari:", P["_AGE"], " bloku celkem:", tot)
