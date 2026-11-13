"""kamenna dostavba (typ stone_addon): jednoradove zdi z kamene rozvalin na korunach zriceniny az pod strechu krovu,
otvory s drevenym nadprazim, maltove jadro. Vysky bere z krovu (krov.ostroh_geom)."""
import math, random
from zrlib.config import WOOD_FINISH
from zrlib.geom import crc
from zrlib.stones import Stone
from .krov import ostroh_geom, roof_under

MIN_H = 6.0              # cm: nizsi kus kamene se nepostavi (sousedni rada ho dorovna)
SILL_MIN = 15.0          # cm: tensi kamen pod oknem se nepostavi (parapet = koruna pod nim)
TOP_FILL = 12.0          # cm: kdyz by nad radou pod strechou zbylo mene, rada se dorovna az pod strechu
MORTAR_DEFAULT = 0.10    # m: maltove jadro uprostred zdi, kdyz ho data neuvadeji (addons[...]["mortar"])


def build_stone_addon(ad, P, walls, terr, frames, cache=None):
    """provizorni dostavba na korunach zdi zriceniny az pod strechu krovu: jedna rada kamenu pres celou tloustku,
    spodek kopiruje korunu zdi pod ni (nebo teren), vrch lici pod late / pod spodek tramu, tramy prochazi zdivem.
    Otvory: dvere (od zeme) a okna s drevenym nadprazim. Zricenina (03) se nemeni."""
    out = []
    fr = next((f for f in frames if f["name"] == ad.get("roof")), None)
    G = ostroh_geom(fr, walls, cache) if fr else None
    if not G: return out
    fin = ad.get("finish", {}); WC = lambda part: WOOD_FINISH.get(fin.get(part, "old"), "wood_old")
    sp = ad.get("stone", {}); t = sp.get("t", 0.45) * 100; jn = sp.get("joint", 0.015) * 100
    lmin, lmax = sp.get("len", (0.25, 0.5)); cmin, cmax = sp.get("course", (0.17, 0.27))
    bear = ad.get("lintel", {}).get("bear", 0.25)
    MORTAR = ad.get("mortar", MORTAR_DEFAULT) * 100                # cm: maltove jadro uprostred zdi (zastavi svetlo ve sparach)
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
        pts = w["pts"]; rng = random.Random(crc("%s|%s" % (ad["name"], w["name"])))
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
                    sr = random.Random(crc(sid))
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


def addon_polygon(ad):
    """obrys obytne casti z os dostaveb (pro uklizeni suti uvnitr)"""
    if "walls" not in ad: return None
    ws = {w["name"]: w["pts"] for w in ad["walls"]}
    if not all(k in ws for k in ("V", "S", "H")): return None
    return ws["V"] + ws["S"] + ws["H"][::-1]
