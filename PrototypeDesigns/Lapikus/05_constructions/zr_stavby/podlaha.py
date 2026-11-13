"""prkenna podlaha (typ plank_floor): podvaly na zemi, prkna s presazenymi spoji, vyrez kolem sloupu a kamenu zriceniny."""
import math, random
from zrlib.config import WOOD_FINISH
from zrlib.geom import crc
from zrlib.stones import Stone


def floor_top(fl, terr):
    """vrch prken podlahy (abs. cm), nebo None (pro prah dveri v dostavbe)"""
    z = _sleeper_top(fl, terr)
    return None if z is None else z + fl.get("planks", {}).get("t", 0.045) * 100


def _sleeper_top(fl, terr):
    """vrch podvalu = spodek prken: nad nejvyssim terenem v obrysu (podvaly dorovnaji nizsi mista)"""
    ux, uy = fl["u"]; nx, ny = fl["n"]; poly = [tuple(p) for p in fl["outline"]]
    sh = fl.get("sleepers", {}).get("h", 0.10) * 100; ins = fl.get("inset", 0.02) * 100
    O = poly[0]
    pu = [((q[0] - O[0]) * ux + (q[1] - O[1]) * uy, (q[0] - O[0]) * nx + (q[1] - O[1]) * ny) for q in poly]
    XY = lambda u, v: (O[0] + ux * u + nx * v, O[1] + uy * u + ny * v)
    vs = [q[1] for q in pu]; us = [q[0] for q in pu]; v_lo, v_hi, u_lo, u_hi = min(vs), max(vs), min(us), max(us)
    zg = []
    for j in range(int((v_hi - v_lo) / 25) + 1):
        v = v_lo + j * 25; xs = []
        for (u0, v0), (u1, v1) in zip(pu, pu[1:] + pu[:1]):
            if (v0 > v) != (v1 > v): xs.append(u0 + (u1 - u0) * (v - v0) / (v1 - v0))
        xs.sort(); sp_ = [(a + ins, b - ins) for a, b in zip(xs[::2], xs[1::2]) if b - a > 2 * ins]
        for i in range(int((u_hi - u_lo) / 25) + 1):
            u = u_lo + i * 25
            if any(a <= u <= b for a, b in sp_): zg.append(terr.z(*XY(u, v)))
    return max(zg) + sh if zg else None


def build_plank_floor(fl, P, walls, terr):
    """prkenna podlaha uvnitr obrysu (vnitrni lice zdi): podvaly (napric, na zemi, kopiruji teren), prkna podel u
    s presazenymi spoji na podvalech. Prkna se vyriznou kolem sloupu a kamenu zriceniny, ktere zasahuji do podlahy."""
    out = []
    fin = fl.get("finish", {}); WC = lambda part: WOOD_FINISH.get(fin.get(part, "raw"), "wood")
    ux, uy = fl["u"]; nx, ny = fl["n"]
    poly = [tuple(p) for p in fl["outline"]]
    sp, pp = fl.get("sleepers", {}), fl.get("planks", {})
    sw, sh, sstep, sseg = sp.get("w", 0.14) * 100, sp.get("h", 0.10) * 100, sp.get("step", 0.8) * 100, sp.get("seg", 1.2) * 100
    pt_, (pwmin, pwmax), pgap, (plmin, plmax) = pp.get("t", 0.045) * 100, pp.get("w", (0.22, 0.32)), pp.get("gap", 0.006) * 100, pp.get("len", (2.4, 4.5))
    ins = fl.get("inset", 0.02) * 100
    rng = random.Random(crc(fl["name"]))
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
    z_sl = _sleeper_top(fl, terr)                           # vrch podvalu = spodek prken
    if z_sl is None: return out
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
                sid = "%s|K%d|%d" % (fl["name"], j, q); r_ = random.Random(crc(sid))
                out.append(Stone(sid, WC("planks"), x, y, z_sl + pt_ / 2 + r_.uniform(-0.3, 0.3), math.degrees(math.atan2(uy, ux)) + r_.uniform(-0.3, 0.3),
                                 e - u - 0.4, w_ - 0.3, pt_))
                u = e; q += 1
    return out
