"""stena z prouti a hliny (typ wattle_wall): dilce SM_RuinWattlePanel mezi sloupy, na spojich dilcu kuly.
Stena stoji v jedne linii (a = konst.) od c0 do c1, sloupy v ni preskakuje (dilce konci u sloupu). Dilec 1 x 1 m
(rovne okraje, sklada se vedle sebe a nad sebe) se skaluje na rozmer pole; kuly na svislych spojich zakryji spary
a nahore presahuji nad stenu (vyplet je na ne naveden).

Data (constructions.json -> addons, generuje tools/constructions/gen_constructions.py z tools/ruin/palac_spec.py):
  origin, u, v     ram stavby (UE cm, jednotkove vektory), rozmery v m: a = podel u, c = podel v
  a, c (c0, c1)    linie steny a jeji rozsah
  h, t, sink       vyska nad terenem, tloustka, zapusteni do zeme (m)
  gap              mezera od zdi na koncich a od sloupu (m)
  posts            sloupy v linii steny: [dict(c, w (strana m), pad = dict(w, top) patni kamen: strana, vrch nad terenem)];
                   spodni pas steny (do vrchu patnich kamenu) konci u patnich kamenu, vys u sloupu
  tile             nejvetsi dilec (sirka, vyska m)
  stake            kuly na spojich: dict(d (prumer), over (presah nad stenu), sink (v zemi)); None = bez kulu
  finish           uprava dreva: stakes"""
import math
from zrlib.config import WOOD_FINISH
from zrlib.stones import Stone


def wall_segments(ad, pads=False):
    """pole steny mezi sloupy (pads = True: mezi patnimi kameny sloupu): [(c0, c1)] v m"""
    g = ad.get("gap", 0.005); segs = [(ad["c"][0] + g, ad["c"][1] - g)]
    for p in ad.get("posts", []):
        w = max(p["w"], p["pad"]["w"]) if pads and p.get("pad") else p["w"]; h = w / 2 + g
        segs = [q for (s0, s1) in segs for q in ((s0, min(s1, p["c"] - h)), (max(s0, p["c"] + h), s1)) if q[1] - q[0] > 0.03]
    return segs


def build_wattle_wall(ad, terr):
    out = []; name = ad["name"]
    O, U, V = ad["origin"], ad["u"], ad["v"]
    P = lambda a, c: (O[0] + (U[0] * a + V[0] * c) * 100, O[1] + (U[1] * a + V[1] * c) * 100)
    yaw_c = math.degrees(math.atan2(V[1], V[0]))
    fin = ad.get("finish", {}); WC = lambda part: WOOD_FINISH.get(fin.get(part, "raw"), "wood")
    a = ad["a"]; h, t, sink = ad["h"], ad["t"], ad.get("sink", 0.03); tw, th = ad.get("tile", (1.1, 1.05))
    st = ad.get("stake"); zg = terr.z(*P(a, sum(ad["c"]) / 2))
    # vodorovne pasy: spodni do vrchu patnich kamenu (mezi nimi), nad nim dilce az k vysce steny (mezi sloupy)
    pad_top = max((p["pad"]["top"] for p in ad.get("posts", []) if p.get("pad")), default=None)
    bands = []
    if pad_top is not None and -sink < pad_top < h:
        bands.append((-sink, pad_top + ad.get("gap", 0.005), True)); z_lo = bands[-1][1]
    else: z_lo = -sink
    nr = max(1, int(math.ceil((h - z_lo) / th - 1e-6))); hh = (h - z_lo) / nr
    bands += [(z_lo + hh * r, z_lo + hh * (r + 1), False) for r in range(nr)]
    for r, (b0, b1, low) in enumerate(bands):
        for k, (c0, c1) in enumerate(wall_segments(ad, pads=low)):
            nc = max(1, int(math.ceil((c1 - c0) / tw - 1e-6))); w = (c1 - c0) / nc
            for i in range(nc):
                x, y = P(a, c0 + w * (i + 0.5))
                out.append(Stone("%s|W%d.%d.%d" % (name, k, i, r), "daub", x, y, zg + (b0 + b1) / 2 * 100, yaw_c,
                                 w * 100, t * 100, (b1 - b0) * 100, shape="wattle_panel"))
    if st:                                                         # kuly na svislych spojich dilcu (pole mezi sloupy)
        for k, (c0, c1) in enumerate(wall_segments(ad)):
            nc = max(1, int(math.ceil((c1 - c0) / tw - 1e-6))); w = (c1 - c0) / nc
            for i in range(1, nc):
                x, y = P(a, c0 + w * i); z0 = zg - st.get("sink", 0.3) * 100; z1 = zg + (h + st.get("over", 0.06)) * 100
                out.append(Stone("%s|K%d.%d" % (name, k, i), WC("stakes"), x, y, (z0 + z1) / 2, yaw_c, z1 - z0, st["d"] * 100, st["d"] * 100,
                                 pitch=90.0, shape="round", bark=False))
    return out
