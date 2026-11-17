"""platenny pristresek (typ canvas_shelter): pultova strecha z platna na kulatine s kurou. Kuly s hlavou rozsochy stoji
na prknech patra, ve vidlicich lezi hreben (z kusu, preplatovany), okapova tyc lezi na podkladnich kamenech na korune zdi,
krokvove tyce na hrebeni a okapove tyci, dve vzpery od hrebene do podlahy. Plachta a stit jsou meshe na miru
(tools/meshes/mesh_textile.canvas_vez -> meshes/textile/<mesh>.obj + .json se stredem a rozmerem v lokalnich osach).
Lana pres plachtu ke kamenum na korune, ovazani spoju, zatezove kameny na lemu. Kameny (podklady, zateze, kotvy)
jsou samostatne actory (loose): da se doladit rucne a ulozit pres capture.

Data (constructions.json -> addons, generuje tools/constructions/gen_constructions.py z tools/ruin/tower_spec.pristresek):
  origin, u, v     ram veze (UE cm, jednotkove vektory; v je v UE osa u otocena o -90 st.), polohy u, v v m
  z_ref            vyska, od ktere se meri h (UE cm, VEZ_F); vsechny vysky h v m od z_ref
  floor_top        vrch prken patra (paty kulu a vzper)
  posts            u (polohy), v, d, fork_k (skala hlavy rozsochy), seat (osa hrebene nad stredem hlavy pred skalovanim, cm, podle varianty)
  ridge            pieces [(u0, u1)], v, top (vrch), d
  eave             u (u0, u1), v, bottom (spodek), d
  pads             u, band_v (pas koruny pod podkladem), size (podel u, podel v m), two_over (nad tuto vysku dva kameny)
  weights          u, v, size (m)
  rafters          u, d, v (v0, v1); osa: h = vrch okapove tyce + d/2 + slope * (v - eave.v)
  slope            sklon krokvi (tg)
  braces           u, d, foot_v, head_dv (hlava za osou hrebene k severu), head_h
  canvas, gable    mesh (jmeno meshe na miru), lift (platno nad krokvemi), hem (tycka v lemu stitu: v, h, d)
  ropes            [dict(ridge_u, edge_u, anchor (u, v))], rope (d, lift, link), anchor_size (m)
  walls            zdi zriceniny, na kterych lezi kameny (koruna)"""
import json, math, os
from zrlib.config import LIB_MESHES, LIB_SHAPES, WOOD_FINISH
from zrlib.stones import Stone, round_mesh_name
from zr_stavby.zdivo import frame_box

SUPPORT = 0.03                   # kamen (podklad, kotva) lezi na kameni koruny, ktery pod nim zasahuje aspon 3 cm v obou smerech
FORK_OVERLAP = 8.0               # kul konci 8 cm uvnitr kmene hlavy rozsochy (pred skalovanim), jako u okapu
MESH_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "meshes", "textile"))


def fitted(mesh):
    """stred a rozmer meshe na miru v lokalnich osach stavby (cm) z <mesh>.json (zapisuje tools/meshes/gen_meshes.py)"""
    p = os.path.join(MESH_DIR, mesh + ".json")
    if not os.path.exists(p):
        raise RuntimeError("Chybi %s - spust python tools/meshes/gen_meshes.py textile" % p)
    with open(p) as f: d = json.load(f)
    return d["center"], d["size"]


def build_canvas_shelter(ad, walls, terr=None):
    out = []; name = ad["name"]; O, U, V = ad["origin"], ad["u"], ad["v"]
    if U[0] * V[1] - U[1] * V[0] > 0:
        raise ValueError("%s: ram s v = u otocena o +90 st. neumim (meshe na miru maji Y = -v)" % name)
    Z0 = ad["z_ref"]
    W = lambda u, v, h: (O[0] + (U[0] * u + V[0] * v) * 100, O[1] + (U[1] * u + V[1] * v) * 100, Z0 + h * 100)
    yaw_u = math.degrees(math.atan2(U[1], U[0]))
    fin = ad.get("finish", "raw"); wc = WOOD_FINISH.get(fin, "wood"); bark = ad.get("bark", True)

    def seg(sid, p0, p1, d, shape="round", cat=None, bk=bark):
        """dilec podel osy p0 -> p1 (u, v, h); X = osa"""
        (x0, y0, z0), (x1, y1, z1) = W(*p0), W(*p1)
        hl = math.hypot(x1 - x0, y1 - y0); L = math.hypot(hl, z1 - z0)
        s = Stone("%s|%s" % (name, sid), cat or wc, (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2,
                  math.degrees(math.atan2(y1 - y0, x1 - x0)) if hl > 0.1 else yaw_u, L, d * 100, d * 100,
                  pitch=math.degrees(math.atan2(z1 - z0, hl)), shape=shape, bark=bk)
        out.append(s); return s

    def lash(sid, p, axis_dir, d):
        """ovazani kolem tyce O d (m) v bode p, osa podel axis_dir (du, dv, dh)"""
        du, dv, dh = axis_dir; n = math.sqrt(du * du + dv * dv + dh * dh); du, dv, dh = du / n, dv / n, dh / n
        nx, ny, nz = LIB_MESHES[LIB_SHAPES["lashing"]][0]; k = d * 100 / 8.0
        a = (p[0] - du * 0.01, p[1] - dv * 0.01, p[2] - dh * 0.01); b = (p[0] + du * 0.01, p[1] + dv * 0.01, p[2] + dh * 0.01)
        s = seg(sid, a, b, 0.01, shape="lashing", cat="rope", bk=False); s.sx, s.sy, s.sz = nx * k, ny * k, nz * k
        return s

    # koruna zriceniny v ramu: (a0, a1, c0, c1), vrch (UE cm)
    ruin = []
    for wn in ad.get("walls", list(walls)):
        for st in walls[wn]["stones"] + walls[wn].get("loose", []):
            hz = st.sz / 2 * abs(math.cos(math.radians(st.pitch))) + st.sx / 2 * abs(math.sin(math.radians(st.pitch)))
            ruin.append((frame_box(st, O, U, V), st.z + hz))

    def crown(u0, u1, v0, v1, m=SUPPORT):
        """vrch nejvyssiho kamene zriceniny, ktery do obdelniku zasahuje aspon m (m) v obou smerech (h m od z_ref);
        kamen zasahujici jen rohem nebo hranou kamen na sobe neudrzi"""
        t = [z for (b, z) in ruin if min(b[1], u1) - max(b[0], u0) >= m and min(b[3], v1) - max(b[2], v0) >= m]
        return (max(t) - Z0) / 100 if t else None

    def stone(sid, u, v, h0, size):
        """volny kamen z rozvalin: stred pudorysu (u, v), spodek h0, size = (podel u, podel v, vyska) m"""
        x, y, z = W(u, v, h0)
        s = Stone("%s|%s" % (name, sid), "face", x, y, z + size[2] * 50, yaw_u, size[0] * 100, size[1] * 100, size[2] * 100)
        s.loose = True; out.append(s); return s

    # --- kuly s hlavou rozsochy, hreben
    po, rg = ad["posts"], ad["ridge"]; rv = rg["v"]; r_axis = rg["top"] - rg["d"] / 2; k = po.get("fork_k", 1.0)
    yaw_f = math.degrees(math.atan2(-V[0], V[1]))                    # lokalni Y hlavy (ramena vidlice) = v, X nahoru
    from zrlib.config import ROUND_MESHES
    fl, fw, fh = ROUND_MESHES["SM_RuinForkHead"][0]
    for i, u in enumerate(po["u"]):
        x, y, _ = W(u, rv, 0)
        f = Stone("%s|H%d" % (name, i), wc, x, y, 0.0, yaw_f, fl * k, fw * k, fh * k, pitch=90.0, shape="fork", bark=True)
        f.z = Z0 + r_axis * 100 - po["seat"][round_mesh_name(f)[-1]] * k
        out.append(f)
        top = (f.z - fl * k / 2 + FORK_OVERLAP * k - Z0) / 100
        seg("K%d" % i, (u, rv, ad["floor_top"]), (u, rv, top), po["d"]).pitch = 90.0
    for i, (u0, u1) in enumerate(rg["pieces"]):
        seg("R%d" % i, (u0, rv, r_axis), (u1, rv, r_axis), rg["d"])
    # --- okapova tyc na podkladnich kamenech
    ev = ad["eave"]; e_axis = ev["bottom"] + ev["d"] / 2
    seg("E", (ev["u"][0], ev["v"], e_axis), (ev["u"][1], ev["v"], e_axis), ev["d"])
    pd = ad["pads"]; sa, sb = pd["size"]
    for i, u in enumerate(pd["u"]):
        c = crown(u - sa / 2, u + sa / 2, pd["band_v"][0], pd["band_v"][1])
        if c is None: continue
        h = ev["bottom"] - c
        if h > pd["two_over"]:                                       # vysoko: dva kameny na sobe
            h1 = round(h * 0.47, 3)
            stone("P%da" % i, u, ev["v"], c, (sa, sb, h1)); stone("P%db" % i, u + 0.02, ev["v"] - 0.01, c + h1, (sa * 0.9, sb * 0.9, h - h1))
        elif h > 0.04:
            stone("P%d" % i, u, ev["v"], c, (sa, sb, h))
    # --- krokvove tyce, vzpery
    rf = ad["rafters"]; e_top = ev["bottom"] + ev["d"]; sl = ad["slope"]
    ax = lambda v: e_top + rf["d"] / 2 + sl * (v - ev["v"])
    for i, u in enumerate(rf["u"]):
        seg("T%d" % i, (u, rf["v"][0], ax(rf["v"][0])), (u, rf["v"][1], ax(rf["v"][1])), rf["d"])
        lash("LT%d" % i, (u, rv, ax(rv)), (0, 1, sl), rf["d"])        # krokev x hreben
        lash("LE%d" % i, (u, ev["v"], ax(ev["v"])), (0, 1, sl), rf["d"])   # krokev x okapova tyc
    br = ad["braces"]
    for i, u in enumerate(br["u"]):
        hv, hh = rv + br["head_dv"], br["head_h"]; fv = br["foot_v"]
        tilt = math.atan2(fv - hv, hh - ad["floor_top"])                 # odklon od svisle
        s = seg("V%d" % i, (u, hv, hh), (u, fv, ad["floor_top"] + br["d"] / 2 * math.sin(tilt)), br["d"])
        dv, dh = fv - hv, ad["floor_top"] - hh
        lash("LV%d" % i, (u, hv + dv * 0.04, hh + dh * 0.04), (0, dv, dh), br["d"])
    for i, u in enumerate(po["u"]):                                      # hreben x vidlice
        lash("LR%d" % i, (u + 0.12, rv, r_axis), (1, 0, 0), rg["d"])
    (_, a1), (b0, _) = rg["pieces"][0], rg["pieces"][1]
    lash("LP", ((a1 + b0) / 2 + 0.14, rv, r_axis), (1, 0, 0), rg["d"])  # preplatovani hrebene
    # --- plachta a stit (meshe na miru), tycka v lemu stitu
    for sid, key in (("C", "canvas"), ("G", "gable")):
        mesh = ad[key]["mesh"]; c, sz = fitted(mesh)
        x, y, z = W(c[0] / 100, -c[1] / 100, c[2] / 100)
        out.append(Stone("%s|%s" % (name, sid), "canvas", x, y, z, yaw_u, max(sz[0], 0.5), sz[1], sz[2], shape=LIB_SHAPE_OF[mesh]))
    hm = ad["gable"]["hem"]; gu = ad["gable"]["u"]
    seg("GH", (gu + 0.005, hm["v"][0], hm["h"]), (gu + 0.005, hm["v"][1], hm["h"]), hm["d"])
    # --- zatezove kameny na lemu, kotevni kameny a lana
    cv = ad["canvas"]; ch = lambda v: e_top + rf["d"] + cv["lift"] + sl * (v - ev["v"])
    wt = ad["weights"]; wa, wb, wh = wt["size"]
    for i, u in enumerate(wt["u"]):
        stone("W%d" % i, u, wt["v"], ch(wt["v"]) - 0.02, (wa, wb, wh))
    rp = ad["rope"]; an = ad["anchor_size"]; (v0, v1) = cv["v"]
    for j, r in enumerate(ad["ropes"]):
        au, av = r["anchor"]
        c = crown(au - an[0] / 2, au + an[0] / 2, av - an[1] / 2, av + an[1] / 2)
        if c is None: continue
        stone("A%d" % j, au, av, c, an)
        pts = [(r["ridge_u"], rv + 0.08, r_axis), (r["ridge_u"], v1, ch(v1) + rp["lift"]), (r["edge_u"], v0, ch(v0) + rp["lift"]),
               (au, av + an[1] / 2 + 0.01, c + an[2] * 0.6)]
        n = 0
        for p0, p1 in zip(pts[:-1], pts[1:]):
            L = math.dist(W(*p0), W(*p1)) / 100; m = max(1, math.ceil(L / rp["link"]))
            for q in range(m):
                a_ = [p0[t] + (p1[t] - p0[t]) * q / m for t in range(3)]; b_ = [p0[t] + (p1[t] - p0[t]) * (q + 1) / m for t in range(3)]
                seg("N%d_%02d" % (j, n), a_, b_, rp["d"], shape="rope", cat="rope", bk=False); n += 1
    return out


LIB_SHAPE_OF = {"SM_RuinCanvasVez_A": "canvas_vez", "SM_RuinCanvasVezGable_A": "canvas_vez_gable"}
