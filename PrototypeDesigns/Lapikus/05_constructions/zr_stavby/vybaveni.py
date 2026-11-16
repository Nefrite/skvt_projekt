"""vybaveni (typ props): hotove props a jednoduche dilce rozmistene jako samostatne actory (da se doladit rucne
a ulozit pres capture). Generator jen rozmisti, tvary jsou v knihovne meshi (LIB_MESHES, ROUND_MESHES).

Data (constructions.json -> addons, generuje tools/constructions/gen_constructions.py z tools/ruin/palac_spec.py):
  origin, u, v     ram stavby (UE cm, jednotkove vektory), polohy v m: a = podel u, c = podel v
  roof             jmeno strechy (typ pult_roof) pro dilce zavesene na krokvich (p1 = "rafter")
  items            seznam dilcu, dva zpusoby zadani:
    a) poloha:  dict(id, shape, a, c (stred pudorysu bounding boxu), z (spodek m nad terenem) nebo zc (stred m nad terenem),
                x = (da, dc) smer lokalni osy X v ramu (vychozi (1, 0)), pitch, roll (st.), size (sx, sy, sz cm; vychozi jmenovity
                rozmer meshe), scale (nasobky jmenovitych rozmeru))
    b) usek:    dict(id, shape ("round", "stake", "rope"), d (prumer m), p0, p1 = (a, c, z) konce osy X (stake: spicka na p1);
                p1 = (a, c, "rafter") = k ose nejblizsi krokve strechy roof v miste a; lano ji obepina)
    spolecne:   finish (uprava dreva, vychozi "raw"), bark, cat (material, kdyz to neni prop)
  Lokalni osa Y je osa X otocena v UE o +90 st. (v ramu palace: X = +u -> Y = -v, X = +v -> Y = +u)."""
import math
from zrlib.config import LIB_MESHES, LIB_SHAPES, ROUND_MESHES, ROUND_SHAPES, WOOD_FINISH
from zrlib.stones import Stone
from zr_stavby.pult import pult_geom


def nominal(shape):
    """jmenovity rozmer meshe (cm) a zakladni material podle tvaru"""
    if shape in LIB_SHAPES:
        nom, _, _, _, cat = LIB_MESHES[LIB_SHAPES[shape]]; return nom, cat
    if shape in ROUND_SHAPES: return ROUND_MESHES[ROUND_SHAPES[shape][0]][0], "wood"
    return None, None


def build_props(ad, terr, frames, cache=None):
    out = []; name = ad["name"]; O, U, V = ad["origin"], ad["u"], ad["v"]
    P = lambda a, c: (O[0] + (U[0] * a + V[0] * c) * 100, O[1] + (U[1] * a + V[1] * c) * 100)
    fr = next((f for f in frames if f["name"] == ad.get("roof")), None)
    G = pult_geom(fr, terr, cache) if fr else None
    for it in ad["items"]:
        shape = it.get("shape"); nom, cat = nominal(shape)
        cat = it.get("cat") or cat or "wood"
        if cat == "wood": cat = WOOD_FINISH.get(it.get("finish", "raw"), "wood")
        if "p0" in it:                                               # usek mezi dvema body (tyc, kul, lano)
            a0, c0, z0 = it["p0"]; a1, c1, z1 = it["p1"]
            x0, y0 = P(a0, c0); zg0 = terr.z(x0, y0); Z0 = zg0 + z0 * 100
            x1, y1 = P(a1, c1)
            if z1 == "rafter":                                       # svisle k ose nejblizsi krokve (lano ji obepina)
                g = min(G["geo"], key=lambda g: abs(g["c"] - c1)); x1, y1 = P(a1, g["c"])
                Z1 = G["under"](a1) + G["vert"] / 2
            else: Z1 = terr.z(x1, y1) + z1 * 100
            hl = math.hypot(x1 - x0, y1 - y0); L = math.hypot(hl, Z1 - Z0); d = it["d"] * 100
            yaw = math.degrees(math.atan2(y1 - y0, x1 - x0)) if hl > 0.1 else 0.0
            st = Stone("%s|%s" % (name, it["id"]), cat, (x0 + x1) / 2, (y0 + y1) / 2, (Z0 + Z1) / 2, yaw, L, d, d,
                       pitch=math.degrees(math.atan2(Z1 - Z0, hl)), shape=shape, bark=bool(it.get("bark")))
        else:
            sx, sy, sz = it.get("size") or nom
            k = it.get("scale", (1.0, 1.0, 1.0)); sx, sy, sz = sx * k[0], sy * k[1], sz * k[2]
            da, dc = it.get("x", (1.0, 0.0)); dx, dy = U[0] * da + V[0] * dc, U[1] * da + V[1] * dc
            x, y = P(it["a"], it["c"]); zg = terr.z(x, y)
            zc = zg + it["zc"] * 100 if "zc" in it else zg + it.get("z", 0.0) * 100 + sz / 2
            st = Stone("%s|%s" % (name, it["id"]), cat, x, y, zc, math.degrees(math.atan2(dy, dx)), sx, sy, sz,
                       pitch=it.get("pitch", 0.0), roll=it.get("roll", 0.0), shape=shape, bark=bool(it.get("bark")))
        st.loose = it.get("loose", True); out.append(st)
    return out
