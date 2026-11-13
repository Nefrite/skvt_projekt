"""03 rozpad: typy otvoru, stav otvoru, profil vysky zdi, parametry stari, sum rozebirani, rady"""
import math, random
from zrlib.geom import _hash01, interp, smooth


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
              splay=o.get("splay"), ragged=o.get("ragged", 0.0), s=o["s"], outer=o.get("outer", False))
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

def params(layout, age=None, override=None):
    """parametry rozpadu z layoutu + preset stari (age: None = podle layoutu) + rucni prepis (override)"""
    P = dict(layout["params"])
    age = age or layout.get("age", "1540")
    P.update(layout.get("presets", {}).get(age, {}))
    P.update(override or {})
    P["_AGE"] = age
    return P

def blob_noise(s, z, seed, cs=0.8, czz=0.6):
    """plynuly 2D sum 0..1 (mrizka cs x czz m, smoothstep) -> sousedni kameny se rozebiraji ve hloucich"""
    u = s / cs; v = z / czz; i = math.floor(u); j = math.floor(v); fu = u - i; fv = v - j
    fu = fu * fu * (3 - 2 * fu); fv = fv * fv * (3 - 2 * fv)
    a = _hash01(seed, i, j); b = _hash01(seed, i + 1, j); c = _hash01(seed, i, j + 1); d = _hash01(seed, i + 1, j + 1)
    return (a + (b - a) * fu) * (1 - fv) + (c + (d - c) * fu) * fv

_BQ = [(0.0, 0.0), (0.02, 0.073), (0.05, 0.118), (0.1, 0.176), (0.2, 0.25), (0.3, 0.319), (0.4, 0.4), (0.5, 0.499),
       (0.6, 0.597), (0.7, 0.679), (0.8, 0.75), (0.9, 0.823), (1.0, 1.0)]

def blob_q(p):
    """prah sumu blob_noise, pod kterym lezi podil p plochy (rozlozeni sumu neni rovnomerne)"""
    p = min(max(p, 0.0), 1.0)
    for (p0, q0), (p1, q1) in zip(_BQ[:-1], _BQ[1:]):
        if p <= p1: return q0 + (q1 - q0) * (p - p0) / max(p1 - p0, 1e-9)
    return 1.0

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
