"""podesta z kulatiny a prken (typ platform): tramy z loupane kulatiny (v kapsach / na korune zdi), prkna kolmo na tramy,
zabradli z tyci s kurou. Vysky jsou absolutni (UE cm): podesta lezi na zdech, ktere maji kazda jinou patu.

Data (constructions.json -> addons, generuje tools/constructions/gen_constructions.py z tools/ruin/brana_spec.py):
  origin, u, v   ram stavby (UE cm, jednotkove vektory), rozmery v m: a = podel u, c = podel v
  z              spodek tramu (UE cm, absolutne)
  beams          dict(d (prumer m), pos [c ...], a (a0, a1), spans [(a0, a1) pro kazdy tram, None = a], bark, stage)
  planks         dict(t, w (min, max), gap, a (a0, a1), c (c0, c1), max_len (m), stage) - prkna podel c (kolmo na tramy), vedle sebe
                 podel a; delsi nez max_len jsou ze dvou kusu se sparou nad nekterym vnitrnim tramem (stridave)
  rail           zabradli: dict(h (vrch nad podlahou), post_d, post_step, rail_d, levels [vysky tyci], stage)
  rails          useky zabradli: [dict(id, p0 (a, c), p1 (a, c))]
  finish         uprava dreva: beams, planks, rails"""
import math, random
from zrlib.config import WOOD_FINISH
from zrlib.geom import crc
from zrlib.stones import Stone


def deck_top(ad):
    """vrch podlahy (UE cm)"""
    return ad["z"] + ad["beams"]["d"] * 100 + ad["planks"]["t"] * 100


def build_platform(ad, terr=None):
    out = []; name = ad["name"]
    O, U, V = ad["origin"], ad["u"], ad["v"]
    P = lambda a, c: (O[0] + (U[0] * a + V[0] * c) * 100, O[1] + (U[1] * a + V[1] * c) * 100)
    yaw_a = math.degrees(math.atan2(U[1], U[0])); yaw_c = math.degrees(math.atan2(V[1], V[0]))
    fin = ad.get("finish", {}); WC = lambda part: WOOD_FINISH.get(fin.get(part, "raw"), "wood")
    def add(st, stage):
        st.stage = stage; out.append(st)
    bm = ad["beams"]; d = bm["d"] * 100
    for i, c in enumerate(bm["pos"]):
        a0, a1 = (bm.get("spans") or [None] * len(bm["pos"]))[i] or bm["a"]
        rng = random.Random(crc("%s|B%d" % (name, i))); e0 = rng.uniform(-0.04, 0.04)          # volny konec nahodne delsi / kratsi
        x, y = P((a0 + e0 + a1) / 2, c)
        add(Stone("%s|B%d" % (name, i), WC("beams"), x, y, ad["z"] + d / 2, yaw_a, (a1 - a0 - e0) * 100, d, d, shape="round", bark=bool(bm.get("bark"))),
            bm.get("stage"))
    pk = ad["planks"]; t = pk["t"] * 100; (p0, p1), (q0, q1) = pk["a"], pk["c"]; wmin, wmax = pk.get("w", (0.22, 0.32)); gap = pk.get("gap", 0.006)
    rng = random.Random(crc("%s|planks" % name))
    n = max(1, int(round((p1 - p0) / ((wmin + wmax) / 2 + gap)))); ws = [rng.uniform(wmin, wmax) for _ in range(n)]
    f = (p1 - p0 - gap * (n - 1)) / sum(ws); x_ = p0; zt = ad["z"] + d
    for i, w in enumerate(ws):
        w *= f; j0, j1 = rng.uniform(-0.03, 0.03), rng.uniform(-0.03, 0.03)                   # konce prken nejsou v jedne primce
        e0, e1 = q0 + j0, q1 + j1; inner = [c for c in sorted(bm["pos"])[1:-1] if e0 + 1.0 < c < e1 - 1.0]
        cuts = [e0, e1] if (e1 - e0 <= pk.get("max_len", 4.6) or not inner) else [e0, inner[(i + rng.randrange(2)) % len(inner)], e1]
        for j in range(len(cuts) - 1):
            x, y = P(x_ + w / 2, (cuts[j] + cuts[j + 1]) / 2)
            add(Stone("%s|P%d.%d" % (name, i, j), WC("planks"), x, y, zt + t / 2, yaw_c, (cuts[j + 1] - cuts[j]) * 100 - (0.4 if len(cuts) > 2 else 0), w * 100, t),
                pk.get("stage"))
        x_ += w + gap
    rl = ad.get("rail"); z_deck = zt + t
    if rl:
        pd = rl["post_d"] * 100; rd = rl["rail_d"] * 100; h = rl["h"] * 100
        for seg in ad.get("rails", []):
            (sa, sc), (ea, ec) = seg["p0"], seg["p1"]; L = math.hypot(ea - sa, ec - sc)
            npost = max(2, int(math.ceil(L / rl["post_step"] - 1e-6)) + 1)
            for k in range(npost):
                q = k / (npost - 1); x, y = P(sa + (ea - sa) * q, sc + (ec - sc) * q)
                add(Stone("%s|Z%s|S%d" % (name, seg["id"], k), WC("rails"), x, y, z_deck + h / 2 - 2, yaw_a, h + 4, pd, pd, pitch=90.0,
                          shape="round", bark=True), rl.get("stage"))
            (x0, y0), (x1, y1) = P(sa, sc), P(ea, ec); yaw = math.degrees(math.atan2(y1 - y0, x1 - x0))
            # tyce z vnejsi strany sloupku (privazane), mirne presahuji
            nx, ny = -(y1 - y0), (x1 - x0); nl = math.hypot(nx, ny) or 1; side = seg.get("side", 1.0) * (pd + rd) / 2
            for m, lv in enumerate(rl["levels"]):
                add(Stone("%s|Z%s|T%d" % (name, seg["id"], m), WC("rails"), (x0 + x1) / 2 + nx / nl * side, (y0 + y1) / 2 + ny / nl * side,
                          z_deck + lv * 100, yaw, L * 100 + 30, rd, rd, shape="round", bark=True), rl.get("stage"))
    return out
