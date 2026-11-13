"""kamenna dostavba (typ stone_addon): jednoradove zdi z kamene rozvalin na korunach zriceniny az pod strechu krovu,
otvory s drevenym nadprazim, maltove jadro. Vysky bere z krovu (krov.ostroh_geom)."""
import math, random
from zrlib.config import WOOD_FINISH
from zrlib.geom import crc
from zrlib.stones import Stone
from .krov import ostroh_geom, roof_under
from .podlaha import floor_top

MIN_H = 6.0              # cm: nizsi kus kamene se nepostavi (sousedni rada ho dorovna)
SILL_MIN = 15.0          # cm: tensi kamen pod oknem se nepostavi (parapet = koruna pod nim)
TOP_FILL = 12.0          # cm: kdyz by nad radou pod strechou zbylo mene, rada se dorovna az pod strechu
MORTAR_DEFAULT = 0.10    # m: maltove jadro uprostred zdi, kdyz ho data neuvadeji (addons[...]["mortar"])


def build_stone_addon(ad, P, walls, terr, frames, cache=None, addons=()):
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
    grid = {}; grid_st = []
    for w in walls.values():
        for s in w["stones"] + w.get("loose", []):
            if s.cat not in ("face", "core", "crown", "frame"): continue
            grid_st.append(s)
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
        def mortar(mid_, p0, p1, z0, z1, open0, open1, top_open):
            """maltove jadro kusu dostavby: pres spary k sousedum (o 0.2 cm za pulku spary), volny konec a volny vrch
            (otvor, konec zdi, strecha) o 1.5 cm uvnitr kamene"""
            a_ = p0 * 100 + (1.5 if open0 else -0.2); b_ = p1 * 100 - (1.5 if open1 else -0.2)
            zt_m = z1 - (2.0 if top_open else 0.0)
            if b_ - a_ < 2 or zt_m - z0 < 2: return
            xm, ym, yaw_, _ = at((a_ + b_) / 200, 0.0)
            out.append(Stone(mid_, "core", xm, ym, (z0 + zt_m) / 2, yaw_, b_ - a_, MORTAR, zt_m - z0))
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
            if o.get("sill_crown"):                                     # parapet = koruna zriceniny pod oknem (zadny kamen dostavby pod oknem)
                o["zs"] = min(bt[idx(o["x0"]):idx(o["x1"]) + 1]) + 1.0
        if ad.get("lintel", {}).get("half"):
            # nadprazi o pul rady vys: spodek v pulce rady (pod konci nadprazi pulene kameny), vrch v pulce dalsi rady
            # (nad nadprazim pulene kameny do dalsi rady)
            for o in ops:
                k = next((i for i, c in enumerate(crs) if abs(c[0] - o["zt"]) < 0.5), None)
                if k is None or k + 1 >= len(crs): continue
                o["zt"] = (crs[k][0] + crs[k][1]) / 2; o["zl"] = (crs[k + 1][0] + crs[k + 1][1]) / 2
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
                            # malta: jadro uprostred tloustky, pres spary k sousedum; u otvoru, na konci zdi a pod strechou /
                            # pod parapetem zustava uvnitr kamene (nevylezá)
                            e0 = p0 < 0.005 or any(abs(p0 - h1) < 0.005 for _, h1 in holes)
                            e1 = p1 > L - 0.005 or any(abs(p1 - h0) < 0.005 for h0, _ in holes)
                            top_open = z1q < cz1 - 0.5 or cz1 > zt_ - TOP_FILL or \
                                any(abs(cz1 - o["zs"]) < 1 and p1 > o["x0"] and p0 < o["x1"] for o in ops)
                            zm0 = z0
                            if abs(z0 - zb_) < 0.5 and min(bt[i0:i1 + 1]) >= zb_ - 5.0:
                                zm0 = min(bt[i0:i1 + 1]) - 1.0                # spara pod dostavbou nad korunou zriceniny (do 5 cm)
                            mortar(sid + ".m", p0, p1, zm0, z1q, e0, e1, top_open)
                bi += 1
        # malta az do zeme (jen vybrane dostavby, mortar_down = jmena zdi): maltove jadro pokracuje pod dostavbou ve zdi
        # zriceniny az k terenu. Kde v rovine malty stoji licovy kamen zriceniny, je malta v teto rovine (vidi se ve sparach);
        # kde chybi, jde malta do prostredni vrstvy zdi (mid_off = osa zdi zriceniny), at zdi neprosvita
        md = ad.get("mortar_down", [])
        if MORTAR > 0 and (md is True or w["name"] in md):
            # jen uvnitr kamenu zriceniny a ve sparach mezi nimi (pres spary, at zdi neprosvita): nenaklonene kusy
            # (lic, jadro, koruna); odkryty vrch (koruna) jen do pulky vysky (zvetraly / lomovy tvar je nahore mensi nez blok)
            solid = [st for st in grid_st if st.cat in ("face", "core", "crown") and abs(st.pitch) < 6 and abs(st.roll) < 6]
            fg = {}
            for st in solid:
                r = max(st.sx, st.sy) / 2
                for gx in range(int(math.floor((st.x - r) / 100)), int(math.floor((st.x + r) / 100)) + 1):
                    for gy in range(int(math.floor((st.y - r) / 100)), int(math.floor((st.y + r) / 100)) + 1):
                        fg.setdefault((gx, gy), []).append(st)
            def inside(x, y, z, u, crown_full=True, jx=2.5, hm=None):
                """malta (tloustka MORTAR napric zdi) v bode x, y, z cela uvnitr jednoho kamene zriceniny, nebo ve svisle
                spare vedle nej (do JX cm podel zdi); svisle presne. u = smer zdi."""
                hm = MORTAR / 2 if hm is None else hm; nx_, ny_ = -u[1], u[0]
                for st in fg.get((int(math.floor(x / 100)), int(math.floor(y / 100))), ()):
                    tz = abs(math.sin(math.radians(st.pitch))) * st.sx / 2 + abs(math.sin(math.radians(st.roll))) * st.sy / 2   # mirne naklonene
                    ztop = st.z if st.cat == "crown" and not crown_full else st.z + st.sz / 2 - tz   # koruna pod dostavbou cela
                    if not (st.z - st.sz / 2 + tz <= z <= ztop): continue
                    ya = math.radians(st.yaw); ca, sa = math.cos(ya), math.sin(ya)
                    for d in (0.0, jx, -jx):
                        ok = True
                        for e_ in (hm, -hm):
                            px_, py_ = x + nx_ * e_ + u[0] * d - st.x, y + ny_ * e_ + u[1] * d - st.y
                            if abs(px_ * ca + py_ * sa) > st.sx / 2 or abs(-px_ * sa + py_ * ca) > st.sy / 2: ok = False; break
                        if ok: return True
                return False
            mid = w.get("mid_off", 0.0) * 100
            add_sp = [st.span for st in out if st.cat == "face" and st.span and st.id.startswith("%s|%s|" % (ad["name"], w["name"]))]
            # sloupce po 5 cm podel zdi (svisle useky malty uvnitr kamenu), sousedni sloupce se stejnym usekem se slouci
            # do jednoho souvisleho kusu (bez mezer mezi sloupci)
            STEP = 0.05; nm = max(1, int(round(L / STEP))); DZ = 2.0; GAP = 4.0     # GAP: svisla spara mezi radami (cm)
            JX = 2.5                                                              # vodorovne pres svislou sparu (cm)
            JX_MID, GAP_MID, MORTAR_MID = 4.0, 6.0, 6.0                           # v jadru (lomove kusy): spary a tloustka malty (cm)
            MERGE = 1.5                                                           # sloucit sloupce, kdyz se konce useku lisi do 1.5 cm
            LAYERS = ((0.0, "", JX, GAP, MORTAR, None), (mid, "j", JX_MID, GAP_MID, MORTAR_MID, 0.0))
            active = {tag: [] for _, tag, *_r in LAYERS}; done = {tag: [] for _, tag, *_r in LAYERS}
            for mi in range(nm + 1):
                cols = {tag: [] for _, tag, *_r in LAYERS}
                if mi < nm:
                    p0, p1 = L * mi / nm, L * (mi + 1) / nm; pm = (p0 + p1) / 2
                    skip = any(o["kind"] == "door" and p1 > o["x0"] and p0 < o["x1"] for o in ops)
                    if not skip:
                        zlo = min(terr.z(*at(q_, 0.0)[:2]) for q_ in (p0, pm, p1)) - 5
                        zhi = max(bt[idx(p0):idx(p1) + 1]); cf = True
                        for o in ops:
                            if o["kind"] == "window" and p1 > o["x0"] and p0 < o["x1"]: zhi = min(zhi, o["zs"] - 1); cf = False   # odkryta koruna v okne
                        _, _, yd_, kseg = at(pm, 0.0); ya_ = math.radians(yd_); u_ = (math.cos(ya_), math.sin(ya_))
                        for lat_, tag, jx_, gap_, th_, hm_ in LAYERS:
                            # jadro (lomove kusy ruzne zapustene a uzsi nez jadro): sirsi spary, tensi malta, staci osa malty v kameni
                            qs = [at(q_, lat_)[:2] for q_ in (p0 + 0.003, pm, p1 - 0.003)]
                            ins = lambda zz_: all(inside(qx, qy, zz_, u_, cf, jx_, hm_) for qx, qy in qs)
                            runs = []; zz = zlo
                            while zz <= zhi + DZ:
                                if ins(zz):
                                    if runs and zz - runs[-1][1] <= gap_: runs[-1][1] = zz
                                    else: runs.append([zz, zz])
                                zz += DZ
                            for r_ in runs:                                       # konce useku presne k hrane kamene (po 0.5 cm)
                                while r_[1] + 0.5 <= zhi + DZ and ins(r_[1] + 0.5): r_[1] += 0.5
                                while r_[0] - 0.5 >= zlo and ins(r_[0] - 0.5): r_[0] -= 0.5
                            if lat_ == 0.0 and runs:
                                # spara mezi korunou zriceniny a dostavbou: malta az ke spodku dostavby (kdyz je spara do 5 cm)
                                za_add = [sp_[2] * 1.0 for sp_ in add_sp if sp_[1] > p0 + 0.003 and sp_[0] < p1 - 0.003]
                                if za_add and 0 < min(za_add) - runs[-1][1] <= 5.0: runs[-1][1] = min(za_add) + 0.5
                            cols[tag] = [(za, zb_, p0, p1, kseg) for za, zb_ in runs if zb_ - za >= 4]
                for lat_, tag, jx_, gap_, th_, hm_ in LAYERS:
                    nxt = []
                    for za, zb_, p0, p1, kseg in cols[tag]:
                        m_ = next((r for r in active[tag] if r[4] == kseg and abs(r[3] - p0) < 1e-6
                                   and abs(r[0] - za) <= MERGE and abs(r[1] - zb_) <= MERGE), None)
                        if m_: active[tag].remove(m_); nxt.append([max(m_[0], za), min(m_[1], zb_), m_[2], p1, kseg])
                        else: nxt.append([za, zb_, p0, p1, kseg])
                    done[tag] += active[tag]; active[tag] = nxt
            for lat_, tag, jx_, gap_, th_, hm_ in LAYERS:
                for ri, (za, zb_, s0_, s1_, kseg) in enumerate(sorted(done[tag], key=lambda r: (r[2], r[0]))):
                    if zb_ - za < 4: continue
                    x, y, yaw, k = at((s0_ + s1_) / 2, lat_)
                    out.append(Stone("%s|%s|M%d.%d%s" % (ad["name"], w["name"], int(round(s0_ * 100)), int(za), tag), "core", x, y, (za + zb_) / 2, yaw,
                                     (s1_ - s0_) * 100 + 0.2, th_, zb_ - za))
        # pulene kameny u nadprazi: rada, kterou otvor / nadprazi zabira jen zcasti -> volna cast rady se doplni
        # (pod konci nadprazi az k jeho spodku, nad nadprazim od jeho vrchu do konce rady)
        for ci, (cz0, cz1) in enumerate(crs):
            for oi, o in enumerate(ops):
                for (h0, h1), (b0, b1) in (((o["x0"] - bear, o["x0"]), (o["zt"], o["zl"])), ((o["x1"], o["x1"] + bear), (o["zt"], o["zl"])),
                                           ((o["x0"], o["x1"]), (o["zs"], o["zl"]))):
                    if not (cz1 > b0 + 1 and cz0 < b1 - 1): continue        # rada tu neni dotcena
                    for f0, f1 in ((cz0, min(cz1, b0)), (max(cz0, b1), cz1)):
                        if f1 - f0 < MIN_H: continue
                        h0_, h1_ = max(h0, 0.0), min(h1, L)
                        if h1_ - h0_ < 0.06: continue
                        i0, i1 = idx(h0_ + 0.02), idx(h1_ - 0.02)
                        rr = ru[i0:i1 + 1]
                        if any(r is None for r in rr) or f1 > min(rr) + 0.5: continue
                        if f0 < max(bt[i0:i1 + 1]) - 0.5: continue           # pod tim je koruna zriceniny
                        n_ = max(1, int(round((h1_ - h0_) / ((lmin + lmax) / 2))))
                        for q in range(n_):
                            p0, p1 = h0_ + (h1_ - h0_) * q / n_, h0_ + (h1_ - h0_) * (q + 1) / n_
                            sid = "%s|%s|%d|H%d%s%d" % (ad["name"], w["name"], ci, oi, "lrm"[[(o["x0"] - bear, o["x0"]), (o["x1"], o["x1"] + bear)].index((h0, h1))] if h1 - h0 < o["x1"] - o["x0"] - 1e-6 else "m", q)
                            sr = random.Random(crc(sid)); x, y, yaw, k = at((p0 + p1) / 2, sr.uniform(-1.0, 1.0))
                            out.append(Stone(sid, "face", x, y, (f0 + f1) / 2, yaw + sr.uniform(-1.0, 1.0),
                                             (p1 - p0) * 100 - jn, t - 1.0, (f1 - f0) - jn * 0.7, seg=k))
                            out[-1].span = (p0, p1, f0, f1)
                            if MORTAR > 0:
                                below = f1 <= o["zt"] + 0.5                       # pod koncem nadprazi: konec u otvoru je volny
                                mortar(sid + ".m", p0, p1, f0, f1, below and abs(p0 - o["x1"]) < 0.005, below and abs(p1 - o["x0"]) < 0.005, False)
        # drevena nadprazi
        for oi, o in enumerate(ops):
            x, y, yaw, k = at(o["s"])
            ln = (o["x1"] - o["x0"] + 2 * bear) * 100
            out.append(Stone("%s|%s|N%d" % (ad["name"], w["name"], oi), WC("lintels"), x, y, (o["zt"] + o["zl"]) / 2, yaw,
                             ln, t - 2.0, o["zl"] - o["zt"] - 0.5))
    if ad.get("threshold"): out += _threshold(ad, ad["threshold"], terr, addons, WC)
    return out


def _threshold(ad, th, terr, addons, WC):
    """drevany prah ve dverich dostavby (samostatny actor -> vyska se da doladit rucne a ulozit pres capture):
    v linii dostavby pres celou jeji tloustku, od zeme (zapusteny) kousek nad podlahu"""
    (x, y), yaw = th["pos"], th["yaw"]; ln, dp = th["len"] * 100, th["depth"] * 100
    ux, uy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    zs_ = [terr.z(x + ux * ln / 2 * i - uy * dp / 2 * j, y + uy * ln / 2 * i + ux * dp / 2 * j) for i in (-1, 0, 1) for j in (-1, 0, 1)]
    fl = next((a for a in addons if a.get("name") == th.get("floor")), None)
    ztop = floor_top(fl, terr) if fl else None
    if ztop is None: ztop = max(zs_) + th.get("h", 0.15) * 100
    ztop += th.get("over", 0.015) * 100; zbot = min(zs_) - th.get("sink", 0.05) * 100
    st = Stone("%s|Prah" % ad["name"], WC("threshold"), x, y, (ztop + zbot) / 2, yaw, ln, dp, ztop - zbot); st.loose = True
    return [st]


def addon_polygon(ad):
    """obrys obytne casti z os dostaveb (pro uklizeni suti uvnitr)"""
    if "walls" not in ad: return None
    ws = {w["name"]: w["pts"] for w in ad["walls"]}
    if not all(k in ws for k in ("V", "S", "H")): return None
    return ws["V"] + ws["S"] + ws["H"][::-1]
