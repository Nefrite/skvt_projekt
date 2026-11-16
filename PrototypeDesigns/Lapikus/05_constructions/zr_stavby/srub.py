"""srub (typ log_wall): steny z loupane kulatiny v radach, otvory, prkenne stity pod pultovou strechu.
Kazda stena ma vlastni vysky rad (z). Rada oznacena v half je pultram (hraneny, polovicni): steny, ktere jim zacinaji a
konci, maji rady o pul rady posunute proti krizici stene, takze se v narozi stridaji jako u skutecneho srubu (zhlavi
presahuji za narozi). Kulatina je o lap tlustsi nez rada (prekryv v drazce), zdi tak neprosvita.
Otvor vynecha rady, ktere maji stred v jeho vysce (otvory jsou zarovnane na rady).

Data (constructions.json -> addons, generuje tools/constructions/gen_constructions.py z tools/ruin/palac_spec.py):
  origin, u, v   ram stavby (UE cm, jednotkove vektory), rozmery v m: a = podel u, c = podel v
  ref            bod (a, c), od jehoz terenu se pocitaji vysky
  lap, half_w    prekryv kulatiny (m), sirka pultramu (m)
  jit            nahodne +- delky volnych koncu (zhlavi) v m
  walls          [dict(id, dir ("a" / "c" = smer steny), at (poloha na druhe ose), z [hranice rad, m nad terenem],
                 half [indexy rad = pultram], openings [dict(span (r0, r1), z (z0, z1))],
                 segs [dict(rows (k0, k1 vcetne), span (r0, r1), free (zacatek, konec = volne zhlavi), stage)])]
  gables         prkenne stity: [dict(id, at (rovina na ose a), c (c0, c1), base (spodek, m), t, board_w (min, max),
                 cuts [dict(c (c0, c1), z (z0, z1))] = vyrezy pro pozednici a vaznici, stage)]; vrch = vrch krokvi strechy
  roof           jmeno strechy (typ pult_roof, osa spadu v) pro stity
  finish         uprava dreva: logs, gables"""
import math, random
from zrlib.config import WOOD_FINISH
from zrlib.geom import crc
from zrlib.stones import Stone
from zr_stavby.pult import pult_geom


def log_rows(w):
    """rady steny: [(k, spodek, vrch, pultram)] v m nad terenem"""
    hv = set(w.get("half", []))
    return [(k, w["z"][k], w["z"][k + 1], k in hv) for k in range(len(w["z"]) - 1)]


def row_pieces(w, seg, k):
    """useky rady k v useku steny seg bez otvoru (bez nahodneho zhlavi): [(r0, r1)]"""
    zc = (w["z"][k] + w["z"][k + 1]) / 2; pcs = [tuple(seg["span"])]
    for o in w.get("openings", []):
        if o["z"][0] < zc < o["z"][1]:
            pcs = [q for (p0, p1) in pcs for q in ((p0, min(p1, o["span"][0])), (max(p0, o["span"][1]), p1)) if q[1] - q[0] > 0.15]
    return pcs


def build_log_wall(ad, terr, frames, cache=None):
    out = []; name = ad["name"]
    O, U, V = ad["origin"], ad["u"], ad["v"]
    P = lambda a, c: (O[0] + (U[0] * a + V[0] * c) * 100, O[1] + (U[1] * a + V[1] * c) * 100)
    yaw_a = math.degrees(math.atan2(U[1], U[0])); yaw_c = math.degrees(math.atan2(V[1], V[0]))
    fin = ad.get("finish", {}); WC = lambda part: WOOD_FINISH.get(fin.get(part, "raw"), "wood")
    z0 = terr.z(*P(*ad["ref"])); lap = ad.get("lap", 0.012); hw = ad.get("half_w", 0.22); jit = ad.get("jit", 0.0)
    for w in ad["walls"]:
        along_a = w["dir"] == "a"; yaw = yaw_a if along_a else yaw_c
        for si, seg in enumerate(w["segs"]):
            free = seg.get("free", (0, 0))
            for k in range(seg["rows"][0], seg["rows"][1] + 1):
                zb, zt = w["z"][k], w["z"][k + 1]; half = k in w.get("half", [])
                rng = random.Random(crc("%s|%s|%d.%d" % (name, w["id"], si, k)))
                j0, j1 = rng.uniform(-jit, jit) * free[0], rng.uniform(-jit, jit) * free[1]
                for i, (p0, p1) in enumerate(row_pieces(w, seg, k)):
                    if p0 == seg["span"][0]: p0 -= j0
                    if p1 == seg["span"][1]: p1 += j1
                    pm = (p0 + p1) / 2; x, y = P(pm, w["at"]) if along_a else P(w["at"], pm)
                    sid = "%s|%s|%d.%d.%d" % (name, w["id"], si, k, i)
                    if half: st = Stone(sid, WC("logs"), x, y, z0 + (zb + zt) * 50, yaw, (p1 - p0) * 100, hw * 100, (zt - zb) * 100)
                    else:
                        d = (zt - zb + lap) * 100
                        st = Stone(sid, WC("logs"), x, y, z0 + (zb + zt) * 50, yaw, (p1 - p0) * 100, d, d, shape="round", bark=False)
                    st.stage = seg.get("stage"); out.append(st)
    gb = ad.get("gables", [])
    fr = next((f for f in frames if f["name"] == ad.get("roof")), None)
    if gb and fr:
        G = pult_geom(fr, terr, cache); top = lambda c: G["under"](c) + G["vert"]       # vrch krokve (cm) v miste c (osa spadu = v)
        for g in gb:
            rng = random.Random(crc("%s|%s" % (name, g["id"]))); c0, c1 = g["c"]; bmin, bmax = g.get("board_w", (0.2, 0.28))
            n = max(1, int(round((c1 - c0) / ((bmin + bmax) / 2)))); ws = [rng.uniform(bmin, bmax) for _ in range(n)]
            f = (c1 - c0) / sum(ws); x_ = c0; zb0 = z0 + g["base"] * 100
            for i, bw in enumerate(ws):
                b0, b1 = x_, x_ + bw * f; x_ = b1; zt = min(top(b0), top(b1))      # rovny vrch prkna pod vrchem krokvi (nezasahuje do lati)
                parts = [(zb0, zt)]
                for ct in g.get("cuts", []):                       # vyrez pro tram, ktery stitem prochazi
                    if ct["c"][1] <= b0 or ct["c"][0] >= b1: continue
                    q0, q1 = z0 + ct["z"][0] * 100, z0 + ct["z"][1] * 100
                    parts = [q for (s0, s1) in parts for q in ((s0, min(s1, q0)), (max(s0, q1), s1))]
                for j, (s0, s1) in enumerate(parts):
                    if s1 - s0 < 4: continue
                    x, y = P(g["at"], (b0 + b1) / 2)
                    st = Stone("%s|%s|%d.%d" % (name, g["id"], i, j), WC("gables"), x, y, (s0 + s1) / 2, yaw_a, s1 - s0, (b1 - b0) * 100 - 0.3, g["t"] * 100, pitch=90.0)   # prkno na stojato
                    st.stage = g.get("stage"); out.append(st)
    return out
