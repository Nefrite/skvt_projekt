"""03 zed z kamennych bloku. Stavba jedne zdi po krocich:
  prepare_wall   geometrie zdi, profil rozpadu, rady kamene, strany (vnitrni / vnejsi lic)
  snap_openings  otvory zarovnane na rady (parapet, nadprazi, vyklenek strilny), rozmery osteni
  forbidden      useky rady, kam nesmi blok zdi (svetlost otvoru, osteni, oblouk, vyklenek)
  lay_courses    rady kamenu ve trech vrstvach (lic, jadro, lic), rozebirani lice, podpora, narozni kvadry
  build_frames   opracovane osteni, nadprazi, parapety, oblouky, vyklenky strilen
  finish_wall    rozpadle jadro, zlabky, koruna pod strechou, koruna (zvetrale kameny), z_offset
"""
import math, random, zlib
from .decay import blob_noise, blob_q, courses, edit_applies, wall_profile
from .prep import apply_plinth, apply_ref_z, resolve_protect_to
from zrlib.config import CROWN_WEATHER
from zrlib.geom import interp
from zrlib.stones import Stone


from .post import cut_notches, roof_clear, rough_core, mark_crown
from types import SimpleNamespace


def build_wall_stones(wd, P, terr, layout, edits, removed, centroid):
    """zed z layoutu -> (kameny, stavy otvoru, delka zdi m)"""
    w = prepare_wall(wd, P, terr, layout, edits, centroid)
    snap_openings(w)
    stones = lay_courses(w)
    build_frames(w, stones)
    return finish_wall(w, stones, removed)


def prepare_wall(wd, P, terr, layout, edits, centroid):
    """pripravena zed: lomena cara (prodlouzena o pul tloustky), profil rozpadu, otvory, rady, strany zdi"""
    wd = resolve_protect_to(wd, terr, layout.get("walls", []))
    wd = apply_ref_z(apply_plinth(wd), terr)
    rng = random.Random(wd.get("seed", 1) * 4093 + P["SEED"])
    pts = [list(p) for p in wd["points"]]
    # roh: kazda zed se na zacatku prodlouzi o pul tloustky -> rohy budou plne (u uzavrenych obrysu)
    if wd.get("extend_start", True):
        dx, dy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]; dl = math.hypot(dx, dy) or 1
        e = wd["thickness"] * 50
        pts[0] = [pts[0][0] - dx / dl * e, pts[0][1] - dy / dl * e]
    shift = wd["thickness"] / 2 if wd.get("extend_start", True) else 0.0   # s v JSON plati od puvodniho bodu
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) / 100 for i in range(len(pts) - 1)]
    cum = [0.0]
    for s in seg: cum.append(cum[-1] + s)
    L = cum[-1]
    corners = list(wd.get("corners", [])) + cum[1:-1]
    sh = lambda lst, keys: [dict(d, **{k: d[k] + shift for k in keys if k in d}) for d in lst]
    xs, h, states = wall_profile(L, wd["H0"], wd["access"], [c + shift for c in corners[:len(wd.get("corners", []))]] + corners[len(wd.get("corners", [])):],
                                 sh(wd.get("openings", []), ["s"]), sh(wd.get("breaches", []), ["s0", "s1"]),
                                 sh(wd.get("protect", []), ["s0", "s1"]), [a + shift for a in wd.get("access_points", [])], wd.get("seed", 1), P,
                                 mid=wd.get("mid", 0.88))
    edits = [dict(e, **{k: e[k] + shift for k in ("s0", "s1") if k in e}) if e["op"] in ("cut", "set_height", "restore") else e for e in edits]
    # datove upravy vysky
    for e in edits:
        if e["op"] in ("set_height", "restore") and edit_applies(e, wd["name"]):
            for i, x in enumerate(xs):
                if e["s0"] <= x <= e["s1"]:
                    h[i] = e["h"] if e["op"] == "set_height" else max(h[i], e["h"])
    # zvyseni useku zdi (m) nad vysledek rozpadu, na krajich plynule (1 m)
    for r in wd.get("raise", []):
        r0, r1 = r["s0"] + shift, r["s1"] + shift
        for i, x in enumerate(xs):
            wgt = max(0.0, min(1.0, (x - r0) + 0.5, (r1 - x) + 0.5))
            if wgt > 0: h[i] = min(h[i] + r["dh"] * wgt, wd["H0"] + r["dh"])
    access_arr = [wd["access"]] * len(xs)
    for ap in wd.get("access_points", []):
        access_arr = [a + P["ACCESS_BOOST"] * math.exp(-((x - ap) / P["ACCESS_RADIUS"]) ** 2) for a, x in zip(access_arr, xs)]
    T = wd["thickness"] * 100
    face_d = min(P["FACE_DEPTH"] * 100, T * 0.4)
    core_w = max(T - 2 * face_d, 10)
    zref = layout["plateau_z_cm"]
    # pata a koruna v absolutnich cm podel zdi
    def at(s):
        k = 0
        while k < len(seg) - 1 and s > cum[k + 1]: k += 1
        p, q = pts[k], pts[k + 1]; f = (s - cum[k]) / max(seg[k], 1e-6)
        x = p[0] + (q[0] - p[0]) * f; y = p[1] + (q[1] - p[1]) * f
        yaw = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        nx, ny = -(q[1] - p[1]) / (seg[k] * 100), (q[0] - p[0]) / (seg[k] * 100)
        return x, y, yaw, nx, ny, k
    zlo = min(terr.z(*at(s)[:2]) for s in [i * 0.5 for i in range(int(L / 0.5) + 1)]) - 120
    zhi = zref + wd["H0"] * 100 + 200
    if wd.get("course_grid"):                     # pevne rady (vez): vsechny zdi maji spary ve stejne vysce jako patra
        g0, gh = wd["course_grid"][0], wd["course_grid"][1] * 100
        k0 = int(math.floor((zlo - g0) / gh)); k1 = int(math.ceil((zhi - g0) / gh))
        crs = [(g0 + k * gh, g0 + (k + 1) * gh) for k in range(k0, k1)]
    else:
        crs = courses(zlo, zhi, rng, P)
    # ktera strana je vnitrni (k tezisti hradu): +1 = levy lic (normala), -1 = pravy
    xm, ym, _, nxm, nym, _ = at(L / 2)
    inner = 1 if (xm + nxm * 100 - centroid[0]) ** 2 + (ym + nym * 100 - centroid[1]) ** 2 < (xm - centroid[0]) ** 2 + (ym - centroid[1]) ** 2 else -1
    if wd.get("inside_pt"):                        # vnitrek mistnosti (vez): strana pro kapsy a vyklenky strilen
        ip = wd["inside_pt"]
        inside = 1 if (ip[0] - xm) * nxm + (ip[1] - ym) * nym > 0 else -1
    else:
        inside = inner
    rside = wd.get("rubble", "both")
    robbed_sides = {"out": [inner], "in": [inner], "both": [1, -1]}.get(rside, [1, -1])  # vnejsi lic nad utesem se nerozebira
    # zlomy lomene zdi: znamenkovy uhel (+ = zatacka doleva), prodlouzeni / zkraceni kamenu u zlomu
    bend = []
    for i_ in range(1, len(pts) - 1):
        d1 = (pts[i_][0] - pts[i_ - 1][0], pts[i_][1] - pts[i_ - 1][1]); d2 = (pts[i_ + 1][0] - pts[i_][0], pts[i_ + 1][1] - pts[i_][1])
        bend.append((cum[i_], math.atan2(d1[0] * d2[1] - d1[1] * d2[0], d1[0] * d2[0] + d1[1] * d2[1])))
    def corner_ext(th, layer):
        t_ = math.tan(min(abs(th), math.radians(80)) / 2)
        if layer == 0: return core_w / 200 * t_
        convex = (th > 0 and layer == -1) or (th < 0 and layer == 1)
        return (T / 200 * t_) if convex else -(T / 200 * t_)
    return SimpleNamespace(wd=wd, P=P, terr=terr, rng=rng, pts=pts, shift=shift, seg=seg, cum=cum, L=L, xs=xs, h=h, states=states, edits=edits, access_arr=access_arr, T=T, face_d=face_d, core_w=core_w, at=at, crs=crs, inner=inner, inside=inside, robbed_sides=robbed_sides, bend=bend, corner_ext=corner_ext)


def snap_openings(w):
    """otvory zarovnat na rady kamene (parapet a nadprazi lezi na sparach) + rozmery osteni po radach"""
    crs, states, terr, at, inside = w.crs, w.states, w.terr, w.at, w.inside
    bounds = [c0 for c0, c1 in crs] + [crs[-1][1]]
    def snap(zab): return min(bounds, key=lambda b: abs(b - zab))
    for st in states:
        sm_ = (st["x0"] + st["x1"]) / 2
        zb_o = terr.z(*at(sm_)[:2]); st["zb"] = zb_o
        h0 = st["top"] - st["sill"]
        if st["sill"] > 0.05: st["sill"] = (snap(zb_o + st["sill"] * 100) - zb_o) / 100
        top = (snap(zb_o + st["top"] * 100) - zb_o) / 100
        st["top"] = top if top - st["sill"] >= 0.6 * h0 else st["sill"] + h0
        st["inside"] = inside
        if st.get("splay"):
            sp = st["splay"]
            st["niche"] = (snap(zb_o + sp["floor"] * 100), snap(zb_o + sp["top"] * 100)); st["w_in"] = sp.get("w_in", 1.6)
            # preklad vyklenku = presne jedna rada nad vyklenkem (vrch na spare) -> nad nim zadna mezera ("kapsa")
            up = [b_ for b_ in bounds if b_ > st["niche"][1] + 1]
            st["niche_lt"] = up[0] if up else st["niche"][1] + 35
        fr = st["frame"]
        st["framed"] = fr > 0 and not (st["robbed"] == "both" and not (st["arch"] and not st["lintel_lost"]))
        if st["arch"]:
            r = (st["x1"] - st["x0"]) / 2
            jb = st["sill"] + st.get("jamb_h", 0); jt = st["top"] - r
        else:
            jb, jt = st["sill"], st["top"]
        st["jamb_z"] = (zb_o + jb * 100, zb_o + jt * 100)
        st["lintel_z"] = st["sill_z"] = None
        if st["framed"] and not st["arch"] and st["kind"] in ("okno", "dvere", "strilna") and not st["lintel_lost"]:
            z0 = zb_o + st["top"] * 100; z1 = z0
            for c0, c1 in crs:                       # nadprazi = 1-2 rady nad otvorem (vyska >= 1.2 * osteni)
                if c0 >= z0 - 1 and z1 - z0 < fr * 120: z1 = c1
            st["lintel_z"] = (z0, z1)
            if st["sill"] > 0.05:
                cb = [c for c in crs if abs(c[1] - (zb_o + st["sill"] * 100)) < 1]
                if cb: st["sill_z"] = cb[0]


def forbidden(w, cz0, cz1, layer=1):
    """useky s (m) v teto rade (cz0..cz1 absolutni cm), kam nesmi zadny blok zdi: svetlost otvoru
    + osteni/nadprazi/parapet/oblouk (ty postavi opracovane kvadry). Bloky se v techto mistech rozdeli
    -> otvor je vzdy pruhledny."""
    states, wd = w.states, w.wd
    out = []
    e = 1.0                                       # cm
    for st in states:
        x0, x1, fr = st["x0"], st["x1"], st["frame"]
        z0r = (cz0 - st["zb"]) / 100; z1r = (cz1 - st["zb"]) / 100
        if st["kind"] == "kapsa":                  # kapsa: jen vnitrni lic (outer=True: jen vnejsi lic, napr. po podeste)
            if layer == (-st["inside"] if st.get("outer") else st["inside"]) and z1r > st["sill"] + 0.01 and z0r < st["top"] - 0.01:
                out.append((x0, x1))
            continue
        if st.get("niche") and layer in (0, st["inside"]):
            # vyklenek strilny zevnitr: siroky prostor (do nej se postavi sikme boky) + preklad nad nim
            n0, n1 = st["niche"]; c = (x0 + x1) / 2; wi = st["w_in"] / 2
            if cz1 > n0 + e and cz0 < n1 - e: out.append((c - wi - 0.05, c + wi + 0.05))
            elif cz1 > n1 + e and cz0 < st["niche_lt"] - e: out.append((c - wi - 0.25, c + wi + 0.25))
        if st.get("ragged") and layer != 0 and z1r > st["sill"] + 0.01 and z0r < st["top"] + 0.2:
            # rozbitejsi okraje pruchodu: lic kolem otvoru nahodne vylamany (jadro zustava)
            rr_ = random.Random(zlib.crc32(("%s|%d|%d" % (wd["name"], round(cz0), layer)).encode()))
            out.append((x0 - rr_.uniform(0, st["ragged"]), x0)); out.append((x1, x1 + rr_.uniform(0, st["ragged"])))
        framed = st["framed"]
        okL = st["arch"] or st["robbed"] != "one" or st.get("wl", 0) == 0
        okR = st["arch"] or st["robbed"] != "one" or st.get("wr", 0) == 0
        jz = st["jamb_z"]
        if framed and cz1 > jz[0] + e and cz0 < jz[1] - e:
            if okL: out.append((x0 - fr, x0))
            if okR: out.append((x1, x1 + fr))
        if st["arch"]:
            r = (x1 - x0) / 2; c = (x0 + x1) / 2; spring = st["top"] - r
            # vylomene opracovane kameny ostění: kdyz oblouk stoji, zustane za nimi jadro (nese oblouk)
            if st["jamb_h"] > 0 and z1r > st["sill"] + 0.01 and z0r < st["sill"] + st["jamb_h"] - 0.01 \
               and (layer != 0 or st["lintel_lost"]):
                if st["wl"] > 0: out.append((x0 - st["wl"], x0))
                if st["wr"] > 0: out.append((x1, x1 + st["wr"]))
            rr = r + (fr if framed and not st["lintel_lost"] else 0.0)
            if z1r > st["sill"] + 0.01 and z0r < spring + rr - 0.01:
                if z1r <= spring + 0.01:
                    out.append((x0, x1))               # pod patkou oblouku jen svetlost (paty nese zdivo / jadro)
                else:
                    zl = max(z0r, spring)
                    hw = math.sqrt(max(rr * rr - (zl - spring) ** 2, 0.0))
                    out.append((c - hw, c + hw))
        else:
            if z1r > st["sill"] + 0.01 and z0r < st["top"] - 0.01:
                if layer != 0 or st["lintel_lost"]:
                    out.append((x0 - st["wl"], x1 + st["wr"]))
                else:                                  # nadprazi stoji -> jadro za vylomenym ostěním ho nese
                    out.append((x0, x1))
            for zz in (st["lintel_z"], st["sill_z"]):
                if zz and cz1 > zz[0] + e and cz0 < zz[1] - e:
                    out.append((x0 - fr, x1 + fr))
    return out


def lay_courses(w):
    """rady kamenu ve trech vrstvach (levy lic +1, jadro 0, pravy lic -1) -> [Stone]"""
    wd, P, terr, rng, shift, seg, cum, L, xs, h, states, edits, access_arr, T, face_d, core_w, at, crs, inner, inside, robbed_sides, bend, corner_ext = w.wd, w.P, w.terr, w.rng, w.shift, w.seg, w.cum, w.L, w.xs, w.h, w.states, w.edits, w.access_arr, w.T, w.face_d, w.core_w, w.at, w.crs, w.inner, w.inside, w.robbed_sides, w.bend, w.corner_ext
    stones = []
    def subtract(s0, s1, bad):
        pieces = [(s0, s1)]
        for a, b in bad:
            nxt = []
            for p0, p1 in pieces:
                if b <= p0 or a >= p1: nxt.append((p0, p1)); continue
                if a > p0: nxt.append((p0, a))
                if b < p1: nxt.append((b, p1))
            pieces = nxt
        return [p for p in pieces if p[1] - p[0] >= 0.12]
    def cut_hit(x, y, z0, z1, s0, s1, z0r, z1r):
        for e in edits:
            if not edit_applies(e, wd["name"]): continue
            if e["op"] == "cut" and s1 > e["s0"] and s0 < e["s1"] and z1r > e["z0"] and z0r < e["z1"]: return True
            if e["op"] == "cut_box":
                b = e["box"]
                if b[0] <= x <= b[3] and b[1] <= y <= b[4] and z1 > b[2] and z0 < b[5]: return True
        return False
    prev = {1: None, 0: None, -1: None}           # obsazene useky predchozi rady (podpora)
    caps = [(c["s0"] + shift, c["s1"] + shift, c["z"] - wd.get("z_offset", 0.0) * 100) for c in wd.get("cap", [])]
    def cap_at(s_):
        """cap = cilene snizeny a zarovnany usek zdi (abs. vyska vrchu, cm), jinak None"""
        for a_, b_, z_ in caps:
            if a_ <= s_ <= b_: return z_
        return None
    def bridged(s0, s1, below, row):
        """klenuti / malta: kamen nad mezerou do BRIDGE m drzi, kdyz lezi obema konci (levy konec muze drzet i soused v rade)"""
        BR = P.get("BRIDGE", 0.6); e_ = min(0.25, (s1 - s0) / 2)
        sup = sorted((max(s0, b0), min(s1, b1)) for b0, b1 in below if b1 > s0 and b0 < s1)
        left = any(b0 < s0 + e_ and b1 > s0 + 0.04 for b0, b1 in sup) or any(abs(r1 - s0) < 0.05 for _, r1 in row)
        right = any(b1 > s1 - e_ and b0 < s1 - 0.04 for b0, b1 in sup)
        if not (left and right): return False
        x_ = s0; gap = 0.0
        for b0, b1 in sup:
            gap = max(gap, b0 - x_); x_ = max(x_, b1)
        return max(gap, s1 - x_) <= BR
    def lintel_over(s0, s1, z0r):
        for st in states:
            if st["lintel_lost"] or st["frame"] <= 0: continue
            if st["robbed"] == "both" and not st["arch"]: continue
            if s1 > st["x0"] - st["frame"] and s0 < st["x1"] + st["frame"] and z0r >= st["top"] - 0.05: return True
        return False
    for ci, (cz0, cz1) in enumerate(crs):
        cur = {1: [], 0: [], -1: []}
        # tri vrstvy: levy lic (+1), jadro (0), pravy lic (-1)
        for layer in (1, 0, -1):
            off = (T / 2 - face_d / 2) * layer if layer else 0.0
            depth = face_d if layer else core_w
            lmin, lmax = (P["STONE_MIN"], P["STONE_MAX"]) if layer else (P["CORE_MIN"], P["CORE_MAX"])
            s = -rng.uniform(0, lmax) if ci % 2 else 0.0           # prevazba
            if wd.get("extend_start", True) and layer == 0: s = face_d / 100     # jadro az za nárožním kvádrem
            bi = 0
            while s < L:
                ln = rng.uniform(lmin, lmax); s0 = max(s, 0.0); s1 = min(s + ln, L); s = s + ln
                sid = "%s|%d|%d|%d" % (wd["name"], ci, layer, bi); bi += 1
                srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])   # nahoda vazana na blok -> upravy neposunou ostatni
                # blok pres zlom zdi se rozdeli na dva kusy (kazdy rovne podel sveho useku)
                bnds = [s0] + [kc for kc in cum[1:-1] if s0 + 0.01 < kc < s1 - 0.01] + [s1]
                pieces = []
                for a_, b_ in zip(bnds[:-1], bnds[1:]):
                    if b_ - a_ >= 0.12: pieces += subtract(a_, b_, forbidden(w, cz0, cz1, layer))
                if not pieces: continue
                sid0 = sid; os0, os1 = s0, s1
                for pi, (s0, s1) in enumerate(pieces):
                    # nerozdeleny blok si necha puvodni id (rucni upravy plati dal), kusy dostanou .a/.b
                    sid = sid0 if len(pieces) == 1 else "%s.%s" % (sid0, "abcdefgh"[pi])
                    if sid != sid0: srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
                    sc = (s0 + s1) / 2
                    x, y, yaw, nx, ny, k = at(sc)
                    zb = terr.z(x, y)
                    top_abs = zb + interp(sc, xs, h) * 100
                    cp = cap_at(sc)
                    if cp is not None:                    # cilene snizena a zarovnana zed: jen cele rady pod vyskou cap
                        if cz1 > cp + 1: continue
                        part = 99.0
                    if cz0 >= top_abs: continue
                    part = (top_abs - cz0) / (cz1 - cz0) if cp is None else part
                    if part < 1 and srng.random() > part * 1.15: continue      # rozvolnena koruna
                    if cz1 < zb - 140: continue                              # hluboko pod terenem
                    z0r = (cz0 - zb) / 100; z1r = (cz1 - zb) / 100
                    # rozebrany lic (odkryje jadro): hlavne shora pod korunou (kameny se berou odshora), u paty jen
                    # mensi hloucky tam, kam se dosahne. Plynuly sum -> hloucky sousednich kamenu, ne jednotlive dirky
                    if layer in robbed_sides and layer != 0 and part >= 1 and cp is None:
                        a = interp(sc, xs, access_arr)
                        wseed = zlib.crc32(wd["name"].encode()) ^ P["SEED"]
                        zr_side = z0r
                        if wd.get("ref_z") and layer == inside: zr_side = (cz0 - wd["ref_z"]) / 100   # vnitrek veze: od podlahy
                        dc = (top_abs - cz1) / 100                                   # hloubka rady pod korunou (m)
                        p_top = P.get("TOP_ROB", 0.55) * (0.5 + 0.5 * a) * math.exp(-max(dc, 0) / P.get("TOP_ROB_D", 0.7))
                        if blob_noise(sc, dc, wseed * 3 + layer, 0.9, 0.5) < blob_q(p_top): continue
                        H_ = P["FACE_ROB_H"]
                        if 0 <= zr_side < H_:
                            p_base = min(0.5, a * P["FACE_ROB"] * P.get("FACE_ROB_BASE", 0.45) * (1 - zr_side / H_) ** 1.5)
                            if blob_noise(sc, zr_side, wseed * 5 + layer, 0.7, 0.45) < blob_q(p_base): continue
                    cx = x + nx * off; cy = y + ny * off
                    if cut_hit(cx, cy, cz0, cz1, s0, s1, z0r, z1r): continue
                    # podpora: blok musi lezet na necem (predchozi rada v teze nebo vedlejsi vrstve, nebo nadprazi)
                    if z0r > 0.2 and prev[layer] is not None:
                        # lic musi lezet na licovem kameni (ne jen na jadru) -> zadne kameny lice visici nad vybranou mezerou;
                        # jadro se opira o cokoli pod sebou
                        below = prev[layer] if layer else prev[0] + prev[1] + prev[-1]
                        ov = sum(max(0, min(s1, b1) - max(s0, b0)) for b0, b1 in below)
                        if ov < 0.3 * (s1 - s0) and not lintel_over(s0, s1, z0r) \
                           and not (layer and bridged(s0, s1, below, cur[layer])): continue
                    cur[layer].append((s0, s1))
                    # zchatrale: u koruny pootocene a vysunute bloky (u otvoru jen nepatrne, at nezasahuji do svetlosti)
                    loose = part < 1.6 and layer != 0
                    if abs(s0 - os0) > 1e-6 or abs(s1 - os1) > 1e-6: loose = False   # kus u otvoru: drzi lic
                    yaw2 = yaw + (srng.uniform(-6, 6) if loose else srng.uniform(-0.8, 0.8))
                    pitch = srng.uniform(-4, 4) if loose else 0.0
                    push = srng.uniform(0, 4) * layer if loose else 0.0
                    gapw = P["JOINT"] * 100
                    cxx = cx + nx * push; cyy = cy + ny * push
                    if layer == 0: gapw = 0.0                # jadro bez spar (je skryte) -> zed neni skrz pruhledna
                    # na zlomu zdi: vnejsi (vypukla) strana se prodlouzi az do spolecne hrany licu, vnitrni se zkrati
                    e0 = e1 = 0.0
                    for kc, th in bend:
                        if abs(s1 - kc) < 1e-6: e1 = corner_ext(th, layer)
                        if abs(s0 - kc) < 1e-6: e0 = corner_ext(th, layer)
                    lenc = (s1 - s0 + e0 + e1) * 100 - gapw
                    if lenc < 8: continue
                    if e0 or e1:
                        ya = math.radians(yaw); dsh = (e1 - e0) * 50
                        cxx += math.cos(ya) * dsh; cyy += math.sin(ya) * dsh
                    stones.append(Stone(sid, "core" if layer == 0 else "face", cxx, cyy, (cz0 + cz1) / 2, yaw2,
                                        lenc, depth - gapw, (cz1 - cz0) - gapw * 0.7, pitch, seg=k))
                    stones[-1].span = (s0 - e0, s1 + e1, z0r, z1r)  # pro kontrolu (test_openings.py)
        # narozni kvadr na zacatku zdi (zakryje prurez zdi v rohu)
        if wd.get("extend_start", True):
            sc = face_d / 200
            x, y, yaw, nx, ny, k = at(sc); zb = terr.z(x, y)
            top_abs = zb + interp(sc, xs, h) * 100
            z0r = (cz0 - zb) / 100; z1r = (cz1 - zb) / 100
            sid = "%s|%d|Q" % (wd["name"], ci)
            if cz1 <= top_abs and cz1 > zb - 140 and not cut_hit(x, y, cz0, cz1, 0, sc * 2, z0r, z1r) \
               and (z0r <= 0.2 or prev[1] is None or any(b0 < sc * 2 for b0, b1 in prev[1] + prev[-1])):
                # narozi z vice kamenu pres tloustku zdi: u vnejsiho rohu strida dlouhy a kratky kvadr (vazba narozi),
                # zbytek tloustky lomove kameny bezne delky
                qr = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
                first = qr.uniform(1.0, 1.35) if ci % 2 == 0 else qr.uniform(0.45, 0.7)
                lens = [first]
                while sum(lens) < T / 100 - 0.01:
                    rest = T / 100 - sum(lens)
                    l_ = qr.uniform(P["STONE_MIN"], P["STONE_MAX"])
                    if rest - l_ < P["STONE_MIN"]: l_ = rest
                    lens.append(min(l_, rest))
                out_s = -inner                                   # vnejsi strana zdi (od teziste hradu)
                t = out_s * T / 2                                 # zacit u vnejsiho rohu
                for qi, l_ in enumerate(lens):
                    tc = t - out_s * l_ * 50
                    qid = sid if qi == 0 else "%s.%d" % (sid, qi)
                    stones.append(Stone(qid, "face", x + nx * tc, y + ny * tc, (cz0 + cz1) / 2, yaw + 90.0 + qr.uniform(-0.6, 0.6),
                                        l_ * 100 - P["JOINT"] * 100, face_d - 1.5, (cz1 - cz0) - 1.0, seg=k))
                    t -= out_s * l_ * 100
                cur[1].append((0, sc * 2)); cur[-1].append((0, sc * 2))
        prev = cur
    return stones


def build_frames(w, stones):
    """osteni a oblouky intaktnich otvoru (opracovane kvadry, cela tloustka zdi); prida do stones"""
    wd, P, terr, seg, L, xs, h, states, T, face_d, at, crs, inside = w.wd, w.P, w.terr, w.seg, w.L, w.xs, w.h, w.states, w.T, w.face_d, w.at, w.crs, w.inside
    SPLIT = P.get("FRAME_SPLIT", 1.1) * 100                # kvadr delsi nez toto (cm) se v hloubce rozdeli na vic kamenu
    def put_frame(sid, x, y, z, yaw, sx, sy, sz, pitch=0.0, seg=0, along="y"):
        """opracovany kamen; pres silnou zed (nebo dlouhy bok vyklenku) z vice kusu ruzne delky, spary strida"""
        L_ = sy if along == "y" else sx
        if L_ <= SPLIT:
            stones.append(Stone(sid, "frame", x, y, z, yaw, sx, sy, sz, pitch, seg=seg)); return
        r_ = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
        lens = []; tot = L_ / 100
        first = r_.uniform(0.75, 1.0) if r_.random() < 0.5 else r_.uniform(0.4, 0.6)
        while sum(lens) < tot - 0.01:
            rest = tot - sum(lens); l_ = first if not lens else r_.uniform(0.5, 1.0)
            if rest - l_ < 0.35: l_ = rest
            lens.append(min(l_, rest))
        a = math.radians(yaw)
        ax_, ay_ = ((-math.sin(a), math.cos(a)) if along == "y" else (math.cos(a), math.sin(a)))
        t = -L_ / 2
        for i, l_ in enumerate(lens):
            tc = t + l_ * 50
            w_ = l_ * 100 - (1.0 if i < len(lens) - 1 else 0.0)
            stones.append(Stone(sid if i == 0 else "%s.%d" % (sid, i), "frame", x + ax_ * tc, y + ay_ * tc, z,
                                yaw + r_.uniform(-0.4, 0.4), w_ if along == "x" else sx, w_ if along == "y" else sy, sz, pitch, seg=seg))
            t += l_ * 100
    for oi, st in enumerate(states):
        if st["frame"] <= 0: continue
        if st["robbed"] == "both" and not (st["arch"] and not st["lintel_lost"]): continue
        fr = st["frame"]; sm_ = (st["x0"] + st["x1"]) / 2
        x, y, yaw, nx, ny, k = at(sm_); zb = terr.z(x, y)
        wall_top = min(interp(s_, xs, h) for s_ in (st["x0"] - fr, sm_, st["x1"] + fr))
        sp_out = -st["inside"] if st.get("niche") else 0      # strilna s vyklenkem: osteni jen ve vnejsim lici
        def add(sid, s0, s1, z0r, z1r, rot_extra=0.0, sxo=None):
            if z1r > min(interp(s0, xs, h), interp(s1, xs, h)) + 0.05: return
            xx, yy, yw, nnx, nny, kk = at((s0 + s1) / 2)
            dep = (face_d - 1) if sp_out else (T - 2)
            o_ = (T / 2 - face_d / 2) * sp_out
            # o 2 cm presah do sousednich bloku -> zadna pruhledna spara kolem osteni
            put_frame(sid, xx + nnx * o_, yy + nny * o_, zb + (z0r + z1r) / 2 * 100, yw, sxo or (s1 - s0) * 100 + 2,
                      dep, (z1r - z0r) * 100 - 0.5, rot_extra, seg=kk)
        if st.get("niche"):
            # vyklenek: sikme boky (kónické rozsireni zevnitr k uzkemu pruzoru), preklad nahore
            n0, n1 = st["niche"]; c = sm_; wi = st["w_in"] / 2; wo = (st["x1"] - st["x0"]) / 2 + fr
            dep_in = T - face_d                                   # hloubka od vnitrniho lice k vnejsimu lici
            for side in (-1, 1):
                a_s = c + side * wo; b_s = c + side * wi              # s na vnejsim lici / na vnitrnim lici
                a_n = (T / 2 - face_d) * (-st["inside"]); b_n = (T / 2) * st["inside"]
                ax_, ay_, _, nnx, nny, kk = at(a_s); bx_, by_, _, _, _, _ = at(b_s)
                A = (ax_ + nnx * a_n, ay_ + nny * a_n); Bp = (bx_ + nnx * b_n, by_ + nny * b_n)
                dx_, dy_ = Bp[0] - A[0], Bp[1] - A[1]; ln = math.hypot(dx_, dy_)
                px_, py_ = -dy_ / ln, dx_ / ln                       # kolmo na bok; ven z vyklenku
                tx_, ty_ = at(c)[0] - (A[0] + Bp[0]) / 2, at(c)[1] - (A[1] + Bp[1]) / 2
                if px_ * tx_ + py_ * ty_ > 0: px_, py_ = -px_, -py_
                mx_, my_ = (A[0] + Bp[0]) / 2 + px_ * 15, (A[1] + Bp[1]) / 2 + py_ * 15
                yw_ = math.degrees(math.atan2(dy_, dx_))
                j = 0
                for c0, c1 in crs:
                    if c0 < n0 - 1 or c1 > n1 + 1: continue
                    if (c1 - zb) / 100 > min(interp(a_s, xs, h), interp(b_s, xs, h)) + 0.05: break
                    put_frame("%s|F%d|N%s%d" % (wd["name"], oi, "L" if side < 0 else "R", j), mx_, my_, (c0 + c1) / 2,
                              yw_, ln + 8, 30, (c1 - c0) - 0.5, seg=kk, along="x")
                    j += 1
            lz0 = n1; lz1 = st["niche_lt"]
            if (lz1 - zb) / 100 <= min(interp(c - wi, xs, h), interp(c + wi, xs, h)) + 0.05:
                xx, yy, yw, nnx, nny, kk = at(c); o_ = (face_d / 2) * st["inside"]
                put_frame("%s|F%d|NT" % (wd["name"], oi), xx + nnx * o_, yy + nny * o_, (lz0 + lz1) / 2, yw,
                          (2 * wi + 0.5) * 100, dep_in - 1, (lz1 - lz0) - 0.5, seg=kk)
        okL = st["arch"] or st["robbed"] != "one" or st.get("wl", 0) == 0
        okR = st["arch"] or st["robbed"] != "one" or st.get("wr", 0) == 0
        jz0, jz1 = st["jamb_z"]
        j = 0
        for c0, c1 in crs:                                   # ostění po radach zdi
            z0 = max(c0, jz0); z1 = min(c1, jz1)
            if z1 - z0 < 3: continue
            z0r = (z0 - zb) / 100; z1r = (z1 - zb) / 100
            if okL: add("%s|F%d|L%d" % (wd["name"], oi, j), st["x0"] - fr, st["x0"], z0r, z1r)
            if okR: add("%s|F%d|R%d" % (wd["name"], oi, j), st["x1"], st["x1"] + fr, z0r, z1r)
            j += 1
        if st["lintel_z"]:
            add("%s|F%d|T" % (wd["name"], oi), st["x0"] - fr, st["x1"] + fr, (st["lintel_z"][0] - zb) / 100, (st["lintel_z"][1] - zb) / 100)
        if st["sill_z"]:
            add("%s|F%d|B" % (wd["name"], oi), st["x0"] - fr, st["x1"] + fr, (st["sill_z"][0] - zb) / 100, (st["sill_z"][1] - zb) / 100)
        if st["arch"] and not st["lintel_lost"]:
            r = (st["x1"] - st["x0"]) / 2; spring = st["top"] - r
            n = max(5, int(math.pi * (r + fr / 2) / 0.32))
            for q in range(n):
                a0 = math.pi * q / n; a1 = math.pi * (q + 1) / n; am = (a0 + a1) / 2
                rm = r + fr / 2
                s_c = sm_ - rm * math.cos(am); z_c = spring + rm * math.sin(am)
                if z_c + fr / 2 > interp(s_c, xs, h) + 0.15: continue
                xx, yy, yw, _, _, kk = at(s_c)
                sid = "%s|F%d|A%d" % (wd["name"], oi, q)
                # klinovy kamen: delka po oblouku, natoceny kolem normaly zdi (roll)
                put_frame(sid, xx, yy, zb + z_c * 100, yw, rm * (a1 - a0) * 100 - 1.5, T - 2, fr * 100,
                          pitch=90.0 - math.degrees(am), seg=kk)


def finish_wall(w, stones, removed):
    """dodatecne upravy kamenu zdi -> (kameny, stavy otvoru, delka)"""
    wd, P, shift, seg, L, states, T, face_d, core_w = w.wd, w.P, w.shift, w.seg, w.L, w.states, w.T, w.face_d, w.core_w
    # odkryte jadro: kde chybi lic, rozpadne se jadro na lomove kameny ruzne zapustene (ne hladka tmava stena s ostrou hranou)
    if P.get("CORE_ROUGH", True): stones = rough_core(stones, wd, P, face_d, core_w, T, removed)
    # zlabky v korune pro tramy (dodatecne vysekane): kameny horni rady v miste zlabku o d nizsi
    if wd.get("notches"): stones = cut_notches(stones, [dict(n_, s=n_["s"] + shift) for n_ in wd["notches"]], P)
    if wd.get("roof_clear") and wd.get("notches"):
        stones = roof_clear(stones, dict(wd["roof_clear"], s0=wd["roof_clear"]["s0"] + shift, s1=wd["roof_clear"]["s1"] + shift),
                            [dict(n_, s=n_["s"] + shift) for n_ in wd["notches"]], T, face_d)
    # koruna: odkryte horni kameny (nic na nich nelezi) -> zvetrale tvary a material koruny
    if CROWN_WEATHER: mark_crown(stones)
    # useky lomene cary seskupene do actoru (zaoblene zlomy: oblouk patri k sousednim rovnym usekum)
    sg = wd.get("seg_group")
    if sg:
        for st_ in stones: st_.seg = sg[min(st_.seg, len(sg) - 1)]
    # svisly posun cele zdi (m), napr. zapusteni do terenu; kameny pod terenem nejsou videt
    off = wd.get("z_offset", 0.0) * 100
    if off:
        for st_ in stones: st_.z += off
        for st_ in states: st_["zb"] += off
    return stones, states, L
