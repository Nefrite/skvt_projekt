"""zdivo z kamene rozvalin (typ stone_fill): srovnani koruny zdi zriceniny na danou vysku (vcetne zazdeni otvoru)
a nizke podezdivky na zemi. Kameny v radach, vice kamenu pres tloustku; spodek kazdeho kamene kopiruje zriceninu
pod nim (po 5 cm podel zdi: nejvyssi kamen zriceniny, kameny se v miste skoku deli), kde zed chybi, stoji na terenu.

Data (constructions.json -> addons, generuje tools/constructions/gen_constructions.py z tools/ruin/palac_spec.py):
  origin, u, v   ram stavby (UE cm, jednotkove vektory), rozmery v m: a = podel u, c = podel v
  ref            bod (a, c), od jehoz terenu se pocitaji vysky
  parts          [dict(id, a (a0, a1), c (c0, c1), top (vrch m nad terenem) nebo top_abs (vrch absolutne, UE cm), bottom_abs (nejnizsi spodek absolutne: nad otvorem ve zdi), gaps [(osa "a" / "c", od, do)] = mezery (dvere))]
  stone          dict(len (min, max), course (min, max), joint, row (sirka jednoho kamene pres tloustku), sink (zapusteni do zeme))
  mortar         tloustka maltoveho jadra (m) v ose zdi: vyspraveni stare zdi - jadro jde od zeme az pod vrch pres nove
                 zdivo i pres zriceninu pod nim (jen uvnitr kamenu a ve sparach do 6 cm), takze zdi neprosvita
  stage          sada actoru pro prepinani etap (base / final / site)"""
import math, random
from zrlib.geom import crc
from zrlib.stones import Stone


def frame_box(st, O, U, V):
    """obalka pudorysu kamene v ramu stavby (m): a0, a1, c0, c1"""
    y = math.radians(st.yaw); ax = (math.cos(y), math.sin(y)); bx = (-ax[1], ax[0])
    sx = st.sx * abs(math.cos(math.radians(st.pitch))) + st.sz * abs(math.sin(math.radians(st.pitch)))
    aa = []; cc = []
    for i, j in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x = st.x + i * ax[0] * sx / 2 + j * bx[0] * st.sy / 2 - O[0]; yy = st.y + i * ax[1] * sx / 2 + j * bx[1] * st.sy / 2 - O[1]
        aa.append((x * U[0] + yy * U[1]) / 100); cc.append((x * V[0] + yy * V[1]) / 100)
    return min(aa), max(aa), min(cc), max(cc)


def _mortar(name, pt, new, ruin, P, yaw_a, along_a, segs, qm, zb, ztop, mt, SL=0.05, GAP=12.0, END=0.02):
    """maltove jadro v ose zdi (kostky s materialem jadra zriceniny): po krocich SL podel zdi svisle useky, kde je kamen -
    nove zdivo teto casti a kameny zriceniny v tloustce zdi (lic i jadro: kde jadro chybi, malta vyplni dutinu mezi lici =
    vyspraveni); spary a mezery do GAP cm se prekleni, ve vetsi dire skrz zed malta neni.
    Konci END m pred koncem zdi a dveri a 2 cm pod vrchem; sousedni kroky se stejnymi useky se slouci do jednoho kusu."""
    out = []
    hw = abs((pt["c"][1] - pt["c"][0]) if along_a else (pt["a"][1] - pt["a"][0])) / 2
    rr = [((b[0], b[1]) if along_a else (b[2], b[3]), lo, t) for (b, t, lo) in ruin
          if (b[2] if along_a else b[0]) < qm + hw - 0.03 and (b[3] if along_a else b[1]) > qm - hw + 0.03 and t > zb]   # kameny v tloustce zdi
    nn = []
    for s in new:                                                    # nove zdivo: obalka podel zdi a vyska (rady pres tloustku se v ose stykaji)
        y = math.radians(s.yaw - yaw_a); half = abs(math.cos(y)) * s.sx / 200 + abs(math.sin(y)) * s.sy / 200
        ox, oy = P(0, 0); ua = (P(1, 0)[0] - ox, P(1, 0)[1] - oy); uc = (P(0, 1)[0] - ox, P(0, 1)[1] - oy)
        a = ((s.x - ox) * ua[0] + (s.y - oy) * ua[1]) / 1e4; c = ((s.x - ox) * uc[0] + (s.y - oy) * uc[1]) / 1e4
        half = (s.sx if (abs(math.cos(y)) > 0.7) == along_a else s.sy) / 200
        p = a if along_a else c
        nn.append(((p - half - 0.01, p + half + 0.01), s.z - s.sz / 2, s.z + s.sz / 2))
    for si, (s0, s1) in enumerate(segs):
        a0, a1 = s0 + END, s1 - END; n_sl = max(1, int(round((a1 - a0) / SL))); sl = (a1 - a0) / n_sl
        cols = []
        for m in range(n_sl):
            pc = a0 + (m + 0.5) * sl
            iv = sorted((max(lo, zb), min(t, ztop - 2.0)) for (r, lo, t) in rr + nn if r[0] <= pc <= r[1])
            merged = []
            for lo, hi in iv:
                if hi - lo < 1.0: continue
                if merged and lo - merged[-1][1] <= GAP: merged[-1][1] = max(merged[-1][1], hi)
                else: merged.append([lo, hi])
            cols.append([(round(lo / 1.5), round(hi / 1.5), lo, hi) for lo, hi in merged if hi - lo >= 4.0])
        m = 0; i = 0
        while m < n_sl:
            e = m + 1
            while e < n_sl and [c[:2] for c in cols[e]] == [c[:2] for c in cols[m]]: e += 1
            pa, pb = a0 + m * sl, a0 + e * sl
            for k, (_, _, lo, hi) in enumerate(cols[m]):
                x, y = P(*(((pa + pb) / 2, qm) if along_a else (qm, (pa + pb) / 2)))
                out.append(Stone("%s|%s|M%d.%d.%d" % (name, pt["id"], si, i, k), "core", x, y, (lo + hi) / 2,
                                 yaw_a + (0.0 if along_a else 90.0), (pb - pa) * 100, mt, hi - lo))
            m = e; i += 1
    return out


def build_stone_fill(ad, walls, terr):
    out = []; name = ad["name"]; O, U, V = ad["origin"], ad["u"], ad["v"]
    P = lambda a, c: (O[0] + (U[0] * a + V[0] * c) * 100, O[1] + (U[1] * a + V[1] * c) * 100)
    yaw_a = math.degrees(math.atan2(U[1], U[0]))
    sp = ad.get("stone", {}); j = sp.get("joint", 0.015); lmin, lmax = sp.get("len", (0.35, 0.6))
    cmin, cmax = sp.get("course", (0.25, 0.4)); roww = sp.get("row", 0.42); sink = sp.get("sink", 0.10)
    parts = ad["parts"]
    ref = ad.get("ref") or [sum(parts[0]["a"]) / 2, sum(parts[0]["c"]) / 2]
    z0 = terr.z(*P(*ref))
    A0 = min(p["a"][0] for p in parts) - 1.5; A1 = max(p["a"][1] for p in parts) + 1.5
    C0 = min(p["c"][0] for p in parts) - 1.5; C1 = max(p["c"][1] for p in parts) + 1.5
    ruin = []                                                        # kameny zriceniny v okoli: (obalka v ramu, vrch, spodek)
    for w in walls.values():
        for st in w["stones"] + w.get("loose", []):
            b = frame_box(st, O, U, V)
            if b[1] < A0 or b[0] > A1 or b[3] < C0 or b[2] > C1: continue
            hz = st.sz / 2 * abs(math.cos(math.radians(st.pitch))) + st.sx / 2 * abs(math.sin(math.radians(st.pitch)))
            ruin.append((b, st.z + hz, st.z - hz))
    mt = ad.get("mortar", 0.0) * 100
    for pt in parts:
        n_before = len(out)
        rng = random.Random(crc("%s|%s" % (name, pt["id"])))
        (a0, a1), (c0, c1) = pt["a"], pt["c"]; along_a = (a1 - a0) >= (c1 - c0)
        (p0, p1), (q0, q1) = ((a0, a1), (c0, c1)) if along_a else ((c0, c1), (a0, a1))     # p = podel zdi, q = pres tloustku
        gaps = sorted((g[1], g[2]) for g in pt.get("gaps", []) if (g[0] == "a") == along_a)
        segs = []; x = p0
        for g0, g1 in gaps:
            if g0 > x: segs.append((x, g0))
            x = max(x, g1)
        if x < p1: segs.append((x, p1))
        nq = max(1, int(round((q1 - q0) / roww))); qw = (q1 - q0) / nq
        zg = min(terr.z(*P(*( (p, (q0 + q1) / 2) if along_a else ((q0 + q1) / 2, p) ))) for p in (p0, (p0 + p1) / 2, p1))
        zb = zg - sink * 100; ztop = pt["top_abs"] if "top_abs" in pt else z0 + pt["top"] * 100   # top_abs = absolutni Z (cm)
        if "bottom_abs" in pt: zb = max(zb, pt["bottom_abs"])          # zdivo az od teto vysky (vyrovnani koruny nad otvorem, ne jeho zazdeni)
        rows = []; z = zb
        while z < ztop - 1:
            h = rng.uniform(cmin, cmax) * 100
            if ztop - (z + h) < cmin * 100 * 0.6: h = ztop - z            # posledni rada az do vrchu (ne tenky zbytek)
            rows.append((z, z + h)); z += h
        SL = 0.05                                                     # krok podel zdi (m): spodek se urcuje po 5 cm
        for r, (rz0, rz1) in enumerate(rows):
            for k in range(nq):
                qa, qb = q0 + qw * k, q0 + qw * (k + 1)
                # kameny zriceniny, ktere zasahuji do pasu teto rady (pres tloustku aspon 3 cm) a zacinaji pod jejim vrchem
                near = [((b[0], b[1]) if along_a else (b[2], b[3]), t) for (b, t, lo) in ruin if lo < rz1 - 1
                        and min(qb, b[3] if along_a else b[1]) - max(qa, b[2] if along_a else b[0]) > 0.03]
                for si, (s0, s1) in enumerate(segs):
                    n_sl = max(1, int(round((s1 - s0) / SL))); sl = (s1 - s0) / n_sl
                    # spodek kamene v kazdem kroku = nejvyssi kamen zriceniny pod nim (+ spara), jinak spodek rady
                    bots = [max([rz0] + [t + 2.0 for (iv, t) in near if iv[1] > s0 + m * sl + 0.005 and iv[0] < s0 + (m + 1) * sl - 0.005]) for m in range(n_sl)]
                    m = 0; i = 0
                    want = rng.uniform(lmin * 0.5, lmax) if (r + k) % 2 else rng.uniform(lmin, lmax)   # prevazba mezi radami
                    while m < n_sl:
                        if rz1 - bots[m] < 8.0: m += 1; continue                   # zricenina saha az sem: nic se nestavi
                        e = m + 1
                        while e < n_sl and abs(bots[e] - bots[m]) < 1.0 and (e - m) * sl < want: e += 1
                        if n_sl - e < int(lmin * 0.6 / sl) and e < n_sl and all(abs(bots[x] - bots[m]) < 1.0 for x in range(e, n_sl)): e = n_sl   # zbytek do konce
                        pa, pb = s0 + m * sl, s0 + e * sl; bot = bots[m]
                        if pb - pa >= 0.10:                                        # kratsi nez 10 cm se nepostavi
                            fa0, fa1, fc0, fc1 = (pa, pb, qa, qb) if along_a else (qa, qb, pa, pb)
                            cx, cy = P((fa0 + fa1) / 2, (fc0 + fc1) / 2)
                            out.append(Stone("%s|%s|%d.%d.%d.%d" % (name, pt["id"], r, k, si, i), "face", cx, cy, (bot + rz1 - j * 70) / 2,
                                             yaw_a + (0.0 if along_a else 90.0), (pb - pa - j) * 100, (qw - j) * 100, rz1 - bot - j * 70))
                            i += 1
                        m = e; want = rng.uniform(lmin, lmax)
        if mt > 0: out += _mortar(name, pt, out[n_before:], ruin, P, yaw_a, along_a, segs, (q0 + q1) / 2, zb, ztop, mt)
    return out
