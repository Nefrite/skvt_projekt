"""mesh_props - vlastni props ve stylu hradu (OBJ, cm, Z nahoru). Kategorie props (v UE Ruin/Props).

Procedurni modely z primitiv (hranol s nerovnostmi, valec, rotacni teleso, vytazeny profil) a kulatiny (mesh_log.tube).
Vse trochu nakrivo a osoupane, zadne ostre "CAD" hrany. Pivot ve stredu bounding boxu, bounding box = NOMINAL.
Sloty (podle potreby kazdeho meshe, poradi SLOTS): Wood (material podle upravy dilce), EndGrain, Bark, Iron, Leather,
Sandstone, Water, Charcoal, Wattle, IronClean, Straw, Wool - materialy SLOT_MI v zrlib/config.py.
Zelezo: Iron = s patinou rzi (kovani, obruce, osy, pruty), IronClean = bez rzi (naradi a kovadlina).

Kovarna: SM_RuinAnvil (kovadlina), SM_RuinBellows (mech na ramu s vyfucnou), SM_RuinBarrel (kalici sud s vodou),
SM_RuinGrindstone (brus na kliku), SM_RuinGrindstoneTreadle (slapaci brus: klikova paka, ojnice, slapadlo),
SM_RuinStool (trinoha stolicka k brusu), SM_RuinTongs, SM_RuinHammer, SM_RuinChisel (naradi),
SM_RuinNailHeader (hrebovnice), SM_RuinCoalBox (truhlik s drevenym uhlim), SM_RuinCoalBoxLid (volne viko), SM_RuinIronBars (svazek prutu).
Sdilene: SM_RuinStump (spalek), SM_RuinWorkbench (ponk se sverakem), SM_RuinWoodpile (hranice stipanych polen),
SM_RuinBasket (proutny kos), SM_RuinLadder (zebrik z tyci s kurou).
Tesarske naradi: SM_RuinMallet (palice), SM_RuinNailHammer (kladivo na hrebiky), SM_RuinBroadaxe (sirocina),
SM_RuinAxe (sekera na stipani), SM_RuinCrosscutSaw (dvoumuzna pila).
Obydli: SM_RuinBed (A houne pres slamu, B slozena), SM_RuinTable, SM_RuinChest, SM_RuinShelf, SM_RuinDoor, SM_RuinShutter.
"""
import math, os
import numpy as np

from mesh_common import waves, noise, smooth_normals, write_obj_slots
import mesh_log

SLOTS = ("Wood", "EndGrain", "Bark", "Iron", "Leather", "Sandstone", "Water", "Charcoal", "Wattle", "IronClean", "Straw", "Wool")
WOOD, END, BARK, IRON, LEATHER, SAND, WATER, COAL, WATTLE, CLEAN, STRAW, WOOL = range(12)      # IRON = s patinou rzi, CLEAN = bez rzi (naradi)


def rot(yaw=0.0, pitch=0.0, roll=0.0):
    """matice natoceni (stupne): yaw kolem Z, pitch kolem Y, roll kolem X"""
    a, b, c = (math.radians(v) for v in (yaw, pitch, roll))
    Rz = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rx = np.array([[1, 0, 0], [0, math.cos(c), -math.sin(c)], [0, math.sin(c), math.cos(c)]])
    return Rz @ Ry @ Rx


class PM:
    """skladani propu: vrcholy (skupina hladkych normal), plochy se slotem a cilovou normalou (orientace se srovna na konci)"""
    def __init__(self):
        self.P, self.UV, self.G, self.F, self.S, self.T = [], [], [], [], [], []; self.n = 0; self.g = 0
    def verts(self, P, UV):
        P = np.asarray(P, float).reshape(-1, 3); i0 = self.n
        self.P.append(P); self.UV.append(np.asarray(UV, float).reshape(-1, 2)); self.G.append(np.full(len(P), self.g))
        self.n += len(P); self.g += 1
        return i0
    def tri(self, a, b, c, slot, target):
        self.F.append((a, b, c)); self.S.append(slot); self.T.append(target)
    def merge(self, M, slot_map=None):
        """prida dil z mesh_log.Mesh (kulatina); slot_map prevede sloty mesh_log (WOOD, END, BARK) na sloty propu"""
        P, UV, G, F, S = M.arrays()
        i0 = self.verts(P, UV); self.G[-1] = G + self.g; self.g += int(G.max()) + 1
        fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
        for f, s, t in zip(F, S, fn):
            self.F.append(tuple(f + i0)); self.S.append(slot_map[s] if slot_map else s); self.T.append(t)
    def arrays(self):
        P = np.concatenate(self.P); UV = np.concatenate(self.UV); G = np.concatenate(self.G)
        F = np.array(self.F, int); S = np.array(self.S, int); T = np.array(self.T, float)
        fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
        flip = (fn * T).sum(1) < 0
        F[flip] = F[flip][:, ::-1]
        keep = np.linalg.norm(fn, axis=1) > 1e-5
        return P, UV, G, F[keep], S[keep]


def add_box(M, c, size, slot, R=None, sub=3, rough=0.25, seed=0, round_=0.6):
    """hranol (stred c, rozmer size), kazda stena mrizka sub x sub s nerovnostmi (rough cm) a ohlazenymi hranami.
    Zaobleni je funkce polohy (bod se promitne na zaobleny kvadr s polomerem round_), takze sousedni steny
    sdili hranu presne - zadne prekryvajici se lemy (driv se lem kazde steny posouval po jeji normale)."""
    R = np.eye(3) if R is None else R; c = np.asarray(c, float); h = np.asarray(size, float) / 2
    W1 = waves(seed + 11, 6, 6, 25)
    rr = min(round_, 0.45 * float(h.min()) * 2); hin = h - rr
    for ax in range(3):
        for sg in (-1, 1):
            a1, a2 = [i for i in range(3) if i != ax]
            n1 = max(1, int(round(sub * size[a1] / max(size) + 1))); n2 = max(1, int(round(sub * size[a2] / max(size) + 1)))
            u = np.linspace(-1, 1, n1 + 1); v = np.linspace(-1, 1, n2 + 1)
            U, V = np.meshgrid(u, v, indexing="ij")
            p = np.zeros(U.shape + (3,)); p[..., ax] = sg * h[ax]; p[..., a1] = U * h[a1]; p[..., a2] = V * h[a2]
            edge = np.maximum(np.abs(U), np.abs(V)) ** 8
            if rr > 0:                                                        # ohlazena hrana (zaobleny kvadr)
                qn = np.clip(p, -hin, hin); dv = p - qn; ln = np.linalg.norm(dv, axis=-1, keepdims=True)
                p = qn + rr * dv / np.maximum(ln, 1e-9)
            q = (p.reshape(-1, 3) @ R.T) + c
            d = rough * noise(q, W1).reshape(U.shape) * (1 - edge)
            p[..., ax] += sg * d
            Pw = p.reshape(-1, 3) @ R.T + c
            uv = np.stack([p[..., a1].ravel(), p[..., a2].ravel()], 1) / 100
            i0 = M.verts(Pw, uv)
            nt = np.zeros(3); nt[ax] = sg; nt = R @ nt
            for i in range(n1):
                for j in range(n2):
                    a = i0 + i * (n2 + 1) + j; b = a + n2 + 1
                    M.tri(a, b, b + 1, slot, nt); M.tri(a, b + 1, a + 1, slot, nt)


def _frame(t):
    ref = np.array([0.0, 0.0, 1.0]) if abs(t[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    y = np.cross(ref, t); y /= np.linalg.norm(y); z = np.cross(t, y)
    return y, z


def add_cyl(M, p0, p1, r0, r1, slot, cap_slot=None, n=24, rings=2, caps=True, rough=0.0, seed=0):
    """valec / kuzel z p0 do p1 (polomery r0 -> r1), plast slot, cela cap_slot"""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); ax = p1 - p0; L = np.linalg.norm(ax); t = ax / L
    y, z = _frame(t); th = np.linspace(0, 2 * math.pi, n + 1); W1 = waves(seed + 5, 6, 3, 15)
    k = np.linspace(0, 1, rings + 1)
    P = []; UV = []
    for kk in k:
        r = r0 + (r1 - r0) * kk
        ring = p0 + ax * kk + r * (np.cos(th)[:, None] * y + np.sin(th)[:, None] * z)
        if rough: ring = ring + (rough * noise(ring, W1))[:, None] * (ring - (p0 + ax * kk)) / max(r, 1e-3)
        P.append(ring); UV.append(np.stack([th / (2 * math.pi) * max(1, round(2 * math.pi * max(r0, r1) / 100)), np.full(n + 1, kk * L / 100)], 1))
    i0 = M.verts(np.array(P), np.array(UV))
    for i in range(rings):
        for j in range(n):
            a = i0 + i * (n + 1) + j; b = a + n + 1
            cm = (np.array(P[i][j]) + P[i + 1][j + 1]) / 2; tgt = cm - (p0 + ax * (i + 0.5) / rings)
            M.tri(a, b, b + 1, slot, tgt); M.tri(a, b + 1, a + 1, slot, tgt)
    if caps:
        for i, cc, sg in ((0, p0, -1), (rings, p1, 1)):
            ci = M.verts(np.array([cc] + list(P[i][:-1])), np.vstack([[0, 0], np.stack([np.cos(th[:-1]), np.sin(th[:-1])], 1) * (r0 if i == 0 else r1) / 100]))
            for j in range(n):
                M.tri(ci, ci + 1 + j, ci + 1 + (j + 1) % n, cap_slot if cap_slot is not None else slot, sg * t)


def add_lathe(M, prof, origin, axis, slots, n=32, rough=0.0, seed=0, seam=0.0):
    """rotacni teleso: prof = [(h, r), ...] obrys v rovine (r, h); vnejsi normala useku = (dh, -dr) (radialne, osove).
    Pravidlo: obrys pevneho telesa jde zdola od osy ven, po plasti nahoru a nahore zpet k ose (napr. kotouc, sud, obruc).
    Opacne poradi = normaly dovnitr (kontrola: tools/checks/check_normals.py). slots = slot kazdeho useku (len(prof) - 1)"""
    o = np.asarray(origin, float); t = np.asarray(axis, float); t = t / np.linalg.norm(t); y, z = _frame(t)
    th = np.linspace(0, 2 * math.pi, n + 1) + seam; W1 = waves(seed + 7, 8, 4, 20)
    prof = np.asarray(prof, float)
    for k in range(len(prof) - 1):
        (h0, r0), (h1, r1) = prof[k], prof[k + 1]
        dr, dh = r1 - r0, h1 - h0; n2 = np.array([dh, -dr]); n2 = n2 / (np.linalg.norm(n2) + 1e-9)    # (radialne, osove) ven
        P = []; UV = []
        for hh, rr in ((h0, r0), (h1, r1)):
            radial = np.cos(th)[:, None] * y + np.sin(th)[:, None] * z
            ring = o + hh * t + rr * radial
            if rough: ring = ring + (rough * noise(ring, W1))[:, None] * radial
            P.append(ring); UV.append(np.stack([th / (2 * math.pi) * max(1, round(2 * math.pi * max(r0, r1, 1) / 100)), np.full(n + 1, (hh + rr) / 100)], 1))
        i0 = M.verts(np.array(P), np.array(UV))
        for j in range(n):
            a = i0 + j; b = a + n + 1
            ang = (th[j] + th[j + 1]) / 2; rad = math.cos(ang) * y + math.sin(ang) * z
            tgt = n2[0] * rad + n2[1] * t
            M.tri(a, b, b + 1, slots[k], tgt); M.tri(a, b + 1, a + 1, slots[k], tgt)


def add_prism(M, poly, slots, x0, x1, end_slot, R=None, c=(0, 0, 0)):
    """vytazeny konvexni profil poly [(y, z)] (proti smeru hodin) podel X od x0 do x1; slots = slot kazde hrany"""
    R = np.eye(3) if R is None else R; c = np.asarray(c, float); poly = np.asarray(poly, float); m = len(poly)
    for k in range(m):
        a2, b2 = poly[k], poly[(k + 1) % m]
        P = np.array([[x0, a2[0], a2[1]], [x1, a2[0], a2[1]], [x1, b2[0], b2[1]], [x0, b2[0], b2[1]]]) @ R.T + c
        e = b2 - a2; ln = np.linalg.norm(e)
        i0 = M.verts(P, [[0, 0], [(x1 - x0) / 100, 0], [(x1 - x0) / 100, ln / 100], [0, ln / 100]])
        tgt = R @ np.array([0.0, e[1], -e[0]])
        M.tri(i0, i0 + 1, i0 + 2, slots[k], tgt); M.tri(i0, i0 + 2, i0 + 3, slots[k], tgt)
    ctr = poly.mean(0)
    for x, sg in ((x0, -1), (x1, 1)):
        P = np.vstack([[x, ctr[0], ctr[1]], np.column_stack([np.full(m, x), poly])]) @ R.T + c
        i0 = M.verts(P, np.vstack([ctr, poly]) / 100)
        for k in range(m):
            M.tri(i0, i0 + 1 + k, i0 + 1 + (k + 1) % m, end_slot, R @ np.array([sg, 0.0, 0.0]))


LOGMAP = {0: WOOD, 1: END, 2: BARK}


def log_piece(M, p0, p1, R_, seed, bark, n_ar=24, step=4.0, knots=1, cut=3.0):
    """kus kulatiny z p0 do p1 (mesh_log.tube) vlozeny do propu"""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); L = np.linalg.norm(p1 - p0)
    T = mesh_log.tube(mesh_log.Mesh(), L, R_, seed, bark, n_ar=n_ar, step=step, path=lambda s: p0 + (p1 - p0) * s,
                      taper=0.97, knots=knots, bark_t=min(0.8, 0.12 * R_), start=dict(cut=cut), end=dict(cut=cut))
    M.merge(T, LOGMAP)


# ------------------------------------------------------------------ props
def stump(seed):
    """spalek O 50, vyska 45 (kura, cela nahore a dole)"""
    M = PM(); log_piece(M, (0, 0, 0), (0, 0, 45), 25.0, seed, True, n_ar=48, step=3.0, knots=2, cut=2.0)
    return M


def anvil(seed):
    """kovadlina: pata, pas, telo, roh (kuzel), zadni pata"""
    M = PM(); r = np.random.default_rng(seed)
    add_box(M, (0, 0, 3), (22, 18, 6), CLEAN, rough=0.3, seed=seed)
    add_box(M, (0, 0, 10), (14, 10, 8), CLEAN, rough=0.3, seed=seed + 1)
    add_box(M, (0, 0, 18), (32, 11, 8), CLEAN, rough=0.15, seed=seed + 2, round_=0.4)
    add_cyl(M, (16, 0, 19), (36, 0, 20.5), 5.2, 0.8, CLEAN, n=20, rings=4, seed=seed + 3)
    add_box(M, (-19, 0, 19), (8, 8, 5), CLEAN, rough=0.15, seed=seed + 4)
    return M


def bellows(seed):
    """mech: dve desky (kapka), horni s rukojeti z jednoho kusu, kuze v zahybech mezi nimi, zelezna vyfucna;
    ram (4 nohy, 2 lany) ve vysce 90 cm"""
    M = PM(); r = np.random.default_rng(seed)
    for (x, y) in ((-70, -32), (-70, 32), (50, -32), (50, 32)):                  # ram
        add_box(M, (x, y, 45), (7, 7, 90), WOOD, R=rot(r.uniform(-2, 2)), rough=0.3, seed=seed + int(x + y))
    for y in (-32, 32):
        add_box(M, (-10, y, 86), (140, 7, 8), WOOD, rough=0.3, seed=seed + 50 + y)
    for x in (-70, 50):                                                          # pricky mezi nohami (dole a pod podelniky)
        add_box(M, (x, 0, 18), (6, 64, 6), WOOD, rough=0.3, seed=seed + 60 + x)
        add_box(M, (x, 0, 78), (6, 64, 6), WOOD, rough=0.3, seed=seed + 65 + x)
    def outline(m=40):
        a = np.linspace(0, 2 * math.pi, m, endpoint=False)
        x = -45 + 40 * np.cos(a); y = 38 * np.sin(a)
        nose = np.cos(a) > 0
        x = np.where(nose, -45 + 40 * np.cos(a) + 70 * np.cos(a) ** 3, x)
        y = np.where(nose, 38 * np.sin(a) * (1 - 0.75 * np.cos(a) ** 2), y)
        return np.stack([x, y], 1)
    ol = outline(); m = len(ol)
    z0, open_deg = 92.0, 12.0
    hinge_x = ol[:, 0].max()
    def top_z(x): return z0 + 4 + (hinge_x - x) * math.tan(math.radians(open_deg))
    def with_handle(ol):
        """obrys horni desky s rukojeti z jednoho kusu: zadni konec pokracuje zuzujicim se jazykem se zaoblenym koncem"""
        xr = ol[:, 0].min(); cut = (ol[:, 0] < xr + 8) & (np.abs(ol[:, 1]) < 9)
        a = np.radians(np.linspace(90, 270, 9))
        tongue = [(xr + 3, 8.0), (xr - 6, 5.5), (xr - 26, 4.2)] + [(xr - 34 + 4.2 * math.cos(t), 4.2 * math.sin(t)) for t in a] + \
                 [(xr - 26, -4.2), (xr - 6, -5.5), (xr + 3, -8.0)]
        out = []; done = False
        for j in range(len(ol)):
            if cut[j]:
                if not done: out += tongue; done = True
                continue
            out.append(tuple(ol[j]))
        return np.array(out)
    olc = ol.mean(0)
    for zf, sg, OL in ((lambda x: np.full_like(x, z0), -1, ol), (top_z, 1, with_handle(ol))):    # desky (tl. 3 cm)
        mm = len(OL)
        for k, dz in ((0, 0.0), (1, 3.0 * sg)):
            Pp = np.column_stack([OL, zf(OL[:, 0]) + dz]); ctr = np.array([olc[0], olc[1], zf(np.array([olc[0]]))[0] + dz])
            i0 = M.verts(np.vstack([ctr, Pp]), np.vstack([ctr[:2], OL]) / 100)
            nz = np.array([0, 0, float(sg if k else -sg)])
            for j in range(mm): M.tri(i0, i0 + 1 + j, i0 + 1 + (j + 1) % mm, WOOD, nz)
        P0 = np.column_stack([OL, zf(OL[:, 0])]); P1 = P0.copy(); P1[:, 2] += 3.0 * sg
        per = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(OL, axis=0), axis=1))]) / 100
        i0 = M.verts(np.vstack([P0, P1]), np.vstack([np.column_stack([per, np.zeros(mm)]), np.column_stack([per, np.full(mm, 0.03)])]))
        for j in range(mm):
            j1 = (j + 1) % mm; e = OL[j1] - OL[j]; tgt = np.array([e[1], -e[0], 0.0])        # obrys proti smeru hodin -> ven vpravo
            M.tri(i0 + j, i0 + j1, i0 + mm + j1, WOOD, tgt); M.tri(i0 + j, i0 + mm + j1, i0 + mm + j, WOOD, tgt)
    # kuze: pas mezi deskami se zahyby (folds) a mirne vyboulena ven
    nl = 7
    P = []; UV = []
    ctr2 = ol.mean(0)
    for li in range(nl + 1):
        f = li / nl
        bulge = 4.0 * math.sin(math.pi * f) + 2.5 * math.sin(math.pi * f * 6) * math.sin(math.pi * f)
        dirs = ol - ctr2; dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
        xy = ol * 0.97 + dirs * bulge * (0.3 + 0.7 * np.clip((hinge_x - ol[:, [0]]) / 100, 0, 1))
        z = z0 + (top_z(ol[:, 0]) - z0) * f
        P.append(np.column_stack([xy, z])); UV.append(np.column_stack([np.linspace(0, 3, m), np.full(m, f * 0.3)]))
    i0 = M.verts(np.array(P), np.array(UV))
    for li in range(nl):
        for j in range(m):
            j1 = (j + 1) % m; a = i0 + li * m + j; b = i0 + (li + 1) * m + j
            tgt = np.array([ol[j, 0] - ctr2[0], ol[j, 1] - ctr2[1], 0])
            M.tri(a, i0 + li * m + j1, i0 + (li + 1) * m + j1, LEATHER, tgt); M.tri(a, i0 + (li + 1) * m + j1, b, LEATHER, tgt)
    add_cyl(M, (hinge_x - 4, 0, z0 + 2), (hinge_x + 22, 0, z0 - 1), 4.0, 1.6, IRON, n=16, rings=2, seed=seed + 9)   # vyfucna
    return M


def barrel(seed, nst=18):
    """kalici sud O 60, vyska 80 z nst duzin (tvarovana prkna se sparami, ruzna tloustka a vyska, vlakna svisle),
    dno (zapustene 4 cm), 3 zelezne obruce, voda kousek pod okrajem"""
    M = PM(); r = np.random.default_rng(seed); H = 80.0; Rm = 30.0; T = 2.0
    zs = np.linspace(0, H, 17)
    def rr(z): return Rm * (0.88 + 0.12 * np.sin(math.pi * np.asarray(z) / H))
    gap = 0.12 / Rm                                                               # spara ~2,4 mm
    for k in range(nst):
        a0 = 2 * math.pi * k / nst + gap; a1 = 2 * math.pi * (k + 1) / nst - gap
        dk = r.uniform(-0.2, 0.2); t = T * r.uniform(0.9, 1.1); bot = r.uniform(-0.3, 0.3); top = H + r.uniform(-0.8, 0.4)
        th = np.linspace(a0, a1, 5); z = bot + (top - bot) * zs / H
        R_o = rr(zs) + dk; R_i = R_o - t
        def surf(R, sgn):
            P = np.stack([R[:, None] * np.cos(th)[None, :], R[:, None] * np.sin(th)[None, :], np.repeat(z[:, None], len(th), 1)], -1)
            uv = np.stack([np.repeat(z[:, None], len(th), 1) / 100, (th[None, :] - a0) * Rm / 100 + k * 0.37 + 0 * z[:, None]], -1)
            i0 = M.verts(P, uv)
            for i in range(len(zs) - 1):
                for j in range(len(th) - 1):
                    a = i0 + i * len(th) + j; b = a + len(th); am = (th[j] + th[j + 1]) / 2
                    tg = sgn * np.array([math.cos(am), math.sin(am), 0.0])
                    M.tri(a, b, b + 1, WOOD, tg); M.tri(a, b + 1, a + 1, WOOD, tg)
        surf(R_o, 1); surf(R_i, -1)
        for a, sg in ((a0, -1), (a1, 1)):                                         # boky duziny (spara)
            P = np.array([[[ro * math.cos(a), ro * math.sin(a), zz], [ri * math.cos(a), ri * math.sin(a), zz]] for ro, ri, zz in zip(R_o, R_i, z)])
            i0 = M.verts(P, np.stack([np.repeat(z[:, None], 2, 1) / 100, np.tile([0, t / 100], (len(z), 1))], -1))
            tg = sg * np.array([-math.sin(a), math.cos(a), 0.0])
            for i in range(len(zs) - 1):
                aa = i0 + 2 * i; M.tri(aa, aa + 2, aa + 3, WOOD, tg); M.tri(aa, aa + 3, aa + 1, WOOD, tg)
        for i, sg in ((0, -1), (len(zs) - 1, 1)):                                 # cela duziny nahore a dole
            P = np.array([[[R_o[i] * math.cos(a), R_o[i] * math.sin(a), z[i]], [R_i[i] * math.cos(a), R_i[i] * math.sin(a), z[i]]] for a in th])
            i0 = M.verts(P, np.stack([np.cos(np.repeat(th[:, None], 2, 1)) * 0.3, np.tile([0, t / 100], (len(th), 1))], -1))
            for j in range(len(th) - 1):
                aa = i0 + 2 * j; M.tri(aa, aa + 2, aa + 3, END, (0, 0, sg)); M.tri(aa, aa + 3, aa + 1, END, (0, 0, sg))
    rb = float(rr(5.0)) - T - 0.05                                                  # dno
    add_lathe(M, [(4.0, 0.0), (4.0, rb), (6.5, rb), (6.5, 0.0)], (0, 0, 0), (0, 0, 1), [WOOD, END, WOOD], n=48, seed=seed + 3)
    for zh in (8.0, 40.0, 72.0):                                                 # obruce (uzavreny profil)
        k = float(rr(zh)) + 0.15
        add_lathe(M, [(zh - 2.5, k - 0.4), (zh - 2.5, k + 0.45), (zh + 2.5, k + 0.45), (zh + 2.5, k - 0.4), (zh - 2.5, k - 0.4)],
                  (0, 0, 0), (0, 0, 1), [IRON] * 4, n=48, rough=0.05, seed=seed + int(zh))
    zw = H - 9.0; rw = float(rr(zw)) - T                                          # hladina
    add_lathe(M, [(zw, 0.0), (zw, rw)][::-1], (0, 0, 0), (0, 0, 1), [WATER], n=48)
    return M


def grindstone(seed, treadle=False, AZ=70.0):
    """brus: piskovcovy kotouc O 70 na zelezne ose (osa Y ve vysce AZ) v loziskach na podelnicich ramu 120 x 60,
    spodek kotouce se namaci ~3 cm do vody v koryte pod nim. Ram ma pricky dole i nahore (samonosny).
    treadle=False: rucni klika; True: slapaci - klikova paka na ose, drevena ojnice dolu ke slapadlu (prkno na cepu
    u zadni nohy, vne ramu na strane osy +Y). Brusic sedi na stolicce (SM_RuinStool)."""
    M = PM(); r = np.random.default_rng(seed)
    for (x, y) in ((-50, -26), (-50, 26), (50, -26), (50, 26)):
        add_box(M, (x, y, 30), (7, 7, 60), WOOD, R=rot(r.uniform(-3, 3)), rough=0.3, seed=seed + x + y)
    for y in (-26, 26):
        add_box(M, (0, y, 63), (120, 7, 7), WOOD, rough=0.3, seed=seed + 40 + y)
    for x in (-50, 50):                                                          # pricky mezi nohami (dole a pod podelniky)
        add_box(M, (x, 0, 14), (6, 52, 6), WOOD, rough=0.3, seed=seed + 50 + x)
        add_box(M, (x, 0, 55), (6, 52, 6), WOOD, rough=0.3, seed=seed + 55 + x)
    add_box(M, (0, -26, 69), (10, 8, 6), WOOD, rough=0.2, seed=seed + 60); add_box(M, (0, 26, 69), (10, 8, 6), WOOD, rough=0.2, seed=seed + 61)   # loziska: osa prochazi spaliky
    prof = [(-6, 1.6), (-6, 34), (-4.5, 35), (4.5, 35), (6, 34), (6, 1.6), (-6, 1.6)]   # kotouc (h = osa Y), otvor = osa
    add_lathe(M, prof, (0, 0, AZ), (0, 1, 0), [SAND] * 6, n=56, rough=0.3, seed=seed + 2)
    add_cyl(M, (0, -36, AZ), (0, 36, AZ), 1.4, 1.4, IRON, n=12, seed=seed + 3)   # osa
    if not treadle:
        add_cyl(M, (0, 36, AZ), (0, 37, AZ - 18), 1.2, 1.2, IRON, n=10)          # klika
        add_cyl(M, (0, 37, AZ - 18), (0, 50, AZ - 18), 1.6, 1.6, WOOD, n=10)     # drzadlo kliky
    else:
        add_box(M, (0, 37, AZ - 6), (3.5, 2.0, 15), IRON, rough=0.05, round_=0.3, seed=seed + 90)   # klikova paka (polomer 12)
        add_cyl(M, (0, 36, AZ - 12), (0, 41, AZ - 12), 1.2, 1.2, IRON, n=10)                       # cep kliky
        add_cyl(M, (0, 41.5, AZ - 12), (2, 41.5, 17), 1.9, 2.1, WOOD, END, n=10, rings=3, rough=0.1)  # ojnice (tyc)
        add_cyl(M, (-50, 26, 7), (-50, 50, 7), 1.6, 1.6, WOOD, END, n=10)                          # cep slapadla (od zadni nohy ven)
        add_box(M, (-6, 41, 12), (92, 14, 3), WOOD, R=rot(0, -7.5), sub=5, rough=0.3, seed=seed + 91)   # slapadlo (prkno)
        add_box(M, (36, 41, 18.5), (10, 16, 1.5), WOOD, R=rot(0, -7.5), sub=2, rough=0.2, seed=seed + 92)  # oslapana podlozka nohy
    # koryto: dno + 4 steny, voda (hladina 3 cm nad spodkem kotouce, kotouc 3 cm nade dnem)
    wb = AZ - 35 - 3.0                                                           # horni plocha dna koryta
    add_box(M, (0, 0, wb - 1), (64, 20, 2), WOOD, seed=seed + 70)
    for (x, y, sx, sy) in ((0, -10, 64, 2), (0, 10, 64, 2), (-32, 0, 2, 20), (32, 0, 2, 20)):
        add_box(M, (x, y, wb - 2 + 5), (sx, sy, 10), WOOD, seed=seed + 71 + int(x + y))
    add_box(M, (0, 0, wb + 6), (60, 17, 0.4), WATER, sub=2, rough=0.0)
    for (x, y) in ((-26, -7), (-26, 7), (26, -7), (26, 7)):                   # 4 nohy koryta
        add_box(M, (x, y, (wb - 2) / 2), (5, 5, wb - 2), WOOD, rough=0.3, seed=seed + 80 + x + y)
    return M


def stool(seed):
    """jednoducha trinoha stolicka: kulate sedatko O 32 (tl. 4), vyska 45, tri loupane nohy O 4 rozkrocene do stran"""
    M = PM(); r = np.random.default_rng(seed)
    add_lathe(M, [(41.0, 0.0), (41.0, 15.5), (41.6, 16.0), (44.4, 16.0), (45.0, 15.5), (45.0, 0.0)], (0, 0, 0), (0, 0, 1),
              [WOOD, WOOD, END, WOOD, WOOD], n=36, rough=0.25, seed=seed)
    for k in range(3):
        a = 2 * math.pi * k / 3 + r.uniform(-0.15, 0.15)
        top = (8.5 * math.cos(a), 8.5 * math.sin(a), 43.0); bot = (17.0 * math.cos(a), 17.0 * math.sin(a), 0.0)
        log_piece(M, bot, top, 2.0, seed + 10 + k, False, n_ar=10, step=5.0, knots=1, cut=2.0)
    return M


def workbench(seed):
    """ponk 220 x 70, vyska 85: deska ze tri fosen, 4 nohy, prickle, predni sverak (drevena celist, zelezny sroub, pricna tyc)"""
    M = PM(); r = np.random.default_rng(seed)
    for k, y in enumerate((-23, 0, 23)):
        add_box(M, (r.uniform(-1, 1), y, 81), (220, 23, 8), WOOD, R=rot(r.uniform(-0.4, 0.4)), sub=5, rough=0.35, seed=seed + k)
    for (x, y) in ((-95, -28), (-95, 28), (95, -28), (95, 28)):
        add_box(M, (x, y, 38.5), (9, 9, 77), WOOD, R=rot(r.uniform(-2, 2)), rough=0.3, seed=seed + 10 + x + y)
    for x in (-95, 95):
        add_box(M, (x, 0, 20), (7, 56, 7), WOOD, rough=0.3, seed=seed + 20 + x)
    add_box(M, (0, 0, 20), (190, 7, 7), WOOD, rough=0.3, seed=seed + 30)                    # podelna pricka prostredkem
    add_box(M, (-80, -40, 74), (28, 7, 20), WOOD, rough=0.3, seed=seed + 40)                 # celist sveraku
    add_cyl(M, (-80, -50, 76), (-80, -20, 76), 1.8, 1.8, IRON, n=12, rings=3)               # sroub
    add_cyl(M, (-92, -50, 76), (-68, -50, 76), 1.2, 1.2, WOOD, n=10)                        # pricna tyc
    return M


def tongs(seed):
    """kovarske kleste 50 cm: dve ramena (ohnute), cep"""
    M = PM()
    for sg in (-1, 1):
        pts = [(-25, 1.2 * sg, 0), (-5, 1.0 * sg, 0), (2, 0.4 * sg, 0), (10, -1.2 * sg, 0), (22, -1.6 * sg, 0), (25, -0.8 * sg, 0)]
        for a, b in zip(pts[:-1], pts[1:]):
            add_cyl(M, a, b, 0.75, 0.75, CLEAN, n=8, caps=True)
    add_cyl(M, (2, 0, -1.4), (2, 0, 1.4), 1.2, 1.2, CLEAN, n=10)
    return M


def hammer(seed):
    """kovarske kladivo s priecnym penem: hlava 11 cm napric toporem (podel Z), toporo 36 cm (podel Y)
    - tloukova cast 3,8 x 3,8 cm s udernou plochou nahore, kolem oka mirne rozsirena
    - pena dole se zuzuje do zaobleneho ostri; ostri je kolmo na toporo (podel X)"""
    M = PM()
    add_box(M, (0, 0, 2.0), (3.8, 3.8, 7.0), CLEAN, rough=0.08, round_=0.35, seed=seed)        # tlouk, uderna plocha z = 5,5 (soumerne s penem)
    add_box(M, (0, 0, 0.0), (4.3, 4.1, 3.4), CLEAN, rough=0.06, round_=0.5, seed=seed + 1)     # rozsireni kolem oka
    peen = [(-1.9, -1.2), (-0.75, -4.9), (-0.3, -5.5), (0.3, -5.5), (0.75, -4.9), (1.9, -1.2)]   # profil (y, z), zuzuje se dolu
    add_prism(M, peen, [CLEAN] * len(peen), -1.9, 1.9, CLEAN)
    add_cyl(M, (0, -2.4, 0.0), (0, 34, 0.0), 1.45, 1.3, WOOD, END, n=12, rings=3, rough=0.1)  # toporo, konec kousek nad okem
    return M


def chisel(seed):
    """sekac 20 cm: osmihranna tyc, ostri klinem, roztepena hlava"""
    M = PM()
    add_cyl(M, (-10, 0, 0), (6, 0, 0), 1.1, 1.0, CLEAN, n=8, rings=2)
    add_cyl(M, (6, 0, 0), (10, 0, 0), 1.0, 0.15, CLEAN, n=8, rings=1)
    add_cyl(M, (-10.6, 0, 0), (-10, 0, 0), 1.4, 1.1, CLEAN, n=8, rings=1)
    return M


def nail_header(seed):
    """hrebovnice: plocha zelezna tyc 25 cm s rozsirenim a otvorem uprostred"""
    M = PM()
    add_box(M, (0, 0, 0), (25, 3.5, 1.4), CLEAN, rough=0.08, round_=0.2, seed=seed)
    add_cyl(M, (0, 0, -0.75), (0, 0, 0.75), 3.0, 3.0, CLEAN, n=16)
    return M


def add_slab(M, poly, tf, tb, slot, U=(0, 1, 0), V=(0, 0, 1), N=(1, 0, 0), c=(0, 0, 0)):
    """deska z konvexniho profilu poly [(a, b)] v rovine U-V; vrchol i ma lice v +N o tf[i] a rub v -N o tb[i]
    (zuzujici se cepel, jednostranne nebo oboustranne broušena). Poradi poly libovolne (srovna se na CCW)."""
    U, V, N, c = (np.asarray(v, float) for v in (U, V, N, c)); poly = np.asarray(poly, float)
    tf = np.broadcast_to(np.asarray(tf, float), len(poly)); tb = np.broadcast_to(np.asarray(tb, float), len(poly))
    area = 0.5 * np.sum(poly[:, 0] * np.roll(poly[:, 1], -1) - np.roll(poly[:, 0], -1) * poly[:, 1])
    if area < 0: poly, tf, tb = poly[::-1], tf[::-1], tb[::-1]
    m = len(poly); base = c + poly[:, :1] * U + poly[:, 1:] * V
    F_ = base + tf[:, None] * N; B_ = base - tb[:, None] * N
    for k in range(m):                                                   # boky (ostri = uzky bok)
        k2 = (k + 1) % m; e = poly[k2] - poly[k]; ln = np.linalg.norm(e)
        i0 = M.verts([B_[k], F_[k], F_[k2], B_[k2]], [[0, 0], [0.02, 0], [0.02, ln / 100], [0, ln / 100]])
        tgt = e[1] * U - e[0] * V
        M.tri(i0, i0 + 1, i0 + 2, slot, tgt); M.tri(i0, i0 + 2, i0 + 3, slot, tgt)
    for side, sg in ((F_, 1), (B_, -1)):                                 # lice a rub (vejir ze stredu)
        i0 = M.verts(np.vstack([side.mean(0), side]), np.vstack([poly.mean(0), poly]) / 100)
        for k in range(m):
            M.tri(i0, i0 + 1 + k, i0 + 1 + (k + 1) % m, slot, sg * N)


def _strip(cl, hw):
    """pas kolem stredni cary cl [(a, b)] s polovicni sirkou hw -> seznam konvexnich ctyruhelniku"""
    cl = np.asarray(cl, float); d = np.gradient(cl, axis=0); d /= np.linalg.norm(d, axis=1)[:, None]
    n = np.stack([-d[:, 1], d[:, 0]], 1); L = cl + n * np.asarray(hw)[:, None]; R_ = cl - n * np.asarray(hw)[:, None]
    return [np.array([R_[i], R_[i + 1], L[i + 1], L[i]]) for i in range(len(cl) - 1)]


def mallet(seed):
    """drevena palice do jedne ruky: valcova hlava O 9 x 14 cm (osa napric toporem, podel Z), na obou koncich zelezna
    obruc proti roztepeni (o kousek zapustena od cela), toporo 30 cm"""
    M = PM()
    add_cyl(M, (0, 0, -7), (0, 0, 7), 4.5, 4.5, WOOD, END, n=28, rings=4, rough=0.15, seed=seed)
    for h0 in (-6.9, 5.7):
        h1 = h0 + 1.2
        add_lathe(M, [(h0, 4.3), (h0, 4.75), (h1, 4.75), (h1, 4.3), (h0, 4.3)], (0, 0, 0), (0, 0, 1), [CLEAN] * 4, n=28, rough=0.04, seed=seed + int(h0))
    add_cyl(M, (0, -4.9, 0), (0, 30, 0), 1.6, 1.4, WOOD, END, n=12, rings=3, rough=0.1, seed=seed + 5)
    return M


def nail_hammer(seed):
    """tesarske kladivo na hrebiky: kulata uderna plocha nahore, dole rozpolceny drapak zahnuty k toporu, toporo 32 cm"""
    M = PM()
    add_box(M, (0, 0, 0), (3.0, 3.6, 3.4), CLEAN, rough=0.05, round_=0.4, seed=seed)              # oko (obemyka toporo)
    add_cyl(M, (0, 0, 1.4), (0, 0, 4.6), 1.15, 1.45, CLEAN, n=16, rings=2)                         # krk a uderna plocha
    cl = [(0, -1.2), (0.35, -3.0), (1.2, -4.4), (2.5, -5.3), (3.8, -5.7)]; hw = [1.15, 1.0, 0.8, 0.55, 0.2]
    for x0, x1 in ((-1.25, -0.2), (0.2, 1.25)):                                                    # dva hroty drapaku
        for q in _strip(cl, hw):
            add_slab(M, q, (x1 - x0) / 2, (x1 - x0) / 2, CLEAN, c=((x0 + x1) / 2, 0, 0))
    add_cyl(M, (0, -2.0, 0), (0, 6, 0), 1.15, 1.15, WOOD, END, n=12, rings=1, rough=0.05, seed=seed + 5)    # u hlavy tensi
    add_cyl(M, (0, 6, 0), (0, 32, 0), 1.15, 1.3, WOOD, END, n=12, rings=3, rough=0.08, seed=seed + 6)
    return M


def broadaxe(seed):
    """sekera sirocina (tesani tramu): siroka cepel s bradou k toporu, ostri ~27 cm podel topora, brousena jen z lice
    (rub rovny), toporo 70 cm vyhnute od rubu, aby ruce nedrely o tram"""
    M = PM()
    add_box(M, (0, 0, -0.3), (4.8, 7.4, 5.4), CLEAN, rough=0.05, round_=0.4, seed=seed)            # oko s tylem (obemyka toporo)
    add_slab(M, [(-3.6, 2.0), (3.6, 2.0), (8.5, 6.0), (-4.0, 6.0)], [2.3, 2.3, 0.82, 0.82], [2.3, 2.3, 0.32, 0.32], CLEAN)   # krk: nabeh z oka do cepele
    poly = [(-3.4, 2.0), (3.4, 2.0), (20, 15), (21, 19), (15, 21), (5, 22), (-5, 21.5), (-6, 19)]
    add_slab(M, poly, [1.0, 1.0, 0.35, 0.1, 0.1, 0.1, 0.1, 0.15], 0.3, CLEAN)
    add_cyl(M, (0, -4.0, 0), (0, 7.0, 0), 1.8, 1.75, WOOD, END, n=12, rings=1, rough=0.08, seed=seed + 5)
    add_cyl(M, (0, 7.0, 0), (3.0, 66.0, 0), 1.75, 1.5, WOOD, END, n=12, rings=4, rough=0.08, seed=seed + 6)
    return M


def axe(seed):
    """sekera na stipani: klinovita hlava (tluste oko, ostri ~11 cm), tyl na prirazeni klinu, rovne toporo 75 cm"""
    M = PM()
    add_box(M, (0, 0, -0.2), (4.6, 7.2, 5.6), CLEAN, rough=0.05, round_=0.4, seed=seed)            # oko (obemyka toporo)
    add_box(M, (0, 0, -3.9), (4.4, 6.6, 2.0), CLEAN, rough=0.05, round_=0.3, seed=seed + 1)        # tyl
    poly = [(-3.5, 1.4), (3.5, 1.4), (5.6, 11.0), (4.6, 13.2), (0, 13.8), (-4.6, 13.2), (-5.0, 11.0)]   # zacina uvnitr oka
    t = [2.2, 2.2, 0.6, 0.15, 0.12, 0.15, 0.6]
    add_slab(M, poly, t, t, CLEAN)
    add_cyl(M, (0, -4.0, 0), (0, 70.0, 0), 1.9, 1.6, WOOD, END, n=12, rings=4, rough=0.08, seed=seed + 5)
    add_cyl(M, (0, 70.0, 0), (0, 71.5, 0), 1.6, 2.0, WOOD, END, n=12, rings=1, rough=0.05, seed=seed + 6)   # zakonceni
    return M


def crosscut_saw(seed):
    """dvoumuzna pila 152 cm: list podel X (ke koncum uzsi, bricho dole se zuby), svisle drevene rukojeti 3 cm od konce listu"""
    M = PM(); L = 76.0; pitch = 2.5
    top = lambda x: 10.0 - 3.0 * (x / L) ** 2
    bot = lambda x: -3.0 + 2.0 * (x / L) ** 2
    xs = np.arange(-L, L + 1e-6, pitch)
    for a, b in zip(xs[:-1], xs[1:]):
        add_slab(M, [(a, bot(a)), (b, bot(b)), (b, top(b)), (a, top(a))], 0.08, 0.08, CLEAN, U=(1, 0, 0), V=(0, 0, 1), N=(0, 1, 0))
        if abs(a) < L - 6 and abs(b) < L - 6:                                                     # zuby (konce bez zubu)
            m_ = (a + b) / 2
            add_slab(M, [(a, bot(a)), (m_, bot(m_) - 1.3), (b, bot(b))], 0.1, 0.1, CLEAN, U=(1, 0, 0), V=(0, 0, 1), N=(0, 1, 0))
    for sg in (-1, 1):
        add_cyl(M, (sg * (L - 3.0), 0, -2.0), (sg * (L - 3.0), 0, 24.0), 1.9, 1.7, WOOD, END, n=12, rings=3, rough=0.08, seed=seed + sg)   # rukojet 3 cm od konce listu
    return M


def add_sheet(M, Pg, thick, slot, uv_scale=100.0):
    """plosna latka s tloustkou z mrizky bodu Pg [nu, nv, 3] (horni lice): spodni lice posunute o thick proti normale,
    okraje uzavrene -> uzavrene teleso (prikryvka, houne)"""
    Pg = np.asarray(Pg, float); nu, nv = Pg.shape[:2]
    du = np.gradient(Pg, axis=0); dv = np.gradient(Pg, axis=1); nn = np.cross(du, dv)
    nn /= np.linalg.norm(nn, axis=-1, keepdims=True) + 1e-9
    if nn[..., 2].mean() < 0: nn = -nn                                   # horni lice miri nahoru
    Bg = Pg - nn * thick
    su = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Pg[:, nv // 2], axis=0), axis=1))]) / uv_scale
    sv = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Pg[nu // 2], axis=0), axis=1))]) / uv_scale
    UVg = np.stack(np.meshgrid(su, sv, indexing="ij"), -1)
    for G_, sg in ((Pg, 1), (Bg, -1)):
        i0 = M.verts(G_, UVg)
        for i in range(nu - 1):
            for j in range(nv - 1):
                a = i0 + i * nv + j; b = a + nv
                t = sg * (nn[i, j] + nn[i + 1, j + 1])
                M.tri(a, b, b + 1, slot, t); M.tri(a, b + 1, a + 1, slot, t)
    ring = [(i, 0) for i in range(nu)] + [(nu - 1, j) for j in range(1, nv)] + [(i, nv - 1) for i in range(nu - 2, -1, -1)] + [(0, j) for j in range(nv - 2, 0, -1)]
    ctr = Pg.reshape(-1, 3).mean(0)
    for k in range(len(ring)):                                            # lem
        (i1, j1), (i2, j2) = ring[k], ring[(k + 1) % len(ring)]
        Q = np.array([Pg[i1, j1], Pg[i2, j2], Bg[i2, j2], Bg[i1, j1]])
        i0 = M.verts(Q, [[0, 0], [0.02, 0], [0.02, 0.02], [0, 0.02]])
        out = (Q[0] + Q[1]) / 2 - ctr; out[2] = 0 if abs(out[2]) < 1e9 else out[2]
        M.tri(i0, i0 + 1, i0 + 2, slot, out); M.tri(i0, i0 + 2, i0 + 3, slot, out)


def bed(seed, folded=False):
    """luzko 200 x 80: ctyri nohy (hlava vyssi s celem), bocnice, laty, slamnik (sypana slama) a vlnena houne
    (A rozprostrena pres slamu s previsem do stran, B slozena v nohach)"""
    M = PM(); r = np.random.default_rng(seed); L, W = 200.0, 80.0
    for x, hh in ((-L / 2 + 4, 62), (L / 2 - 4, 46)):
        for y in (-W / 2 + 4, W / 2 - 4):
            add_box(M, (x + r.uniform(-0.3, 0.3), y, hh / 2), (8, 8, hh), WOOD, sub=4, rough=0.3, seed=seed + int(x + y))
    for y in (-W / 2 + 3, W / 2 - 3):                                            # bocnice
        add_box(M, (0, y, 30), (L - 16, 5, 13), WOOD, R=rot(r.uniform(-0.3, 0.3)), sub=5, rough=0.3, seed=seed + 20 + int(y))
    for x in (-L / 2 + 4, L / 2 - 4):                                            # celo v hlave, prkno v nohach
        add_box(M, (x, 0, 30), (5, W - 16, 13), WOOD, sub=4, rough=0.3, seed=seed + 30 + int(x))
    add_box(M, (-L / 2 + 4, 0, 50), (4, W - 12, 18), WOOD, sub=4, rough=0.3, seed=seed + 35)
    for k in range(7):                                                            # laty
        x = -L / 2 + 20 + k * (L - 40) / 6
        add_box(M, (x + r.uniform(-1, 1), 0, 36.5 + 1), (9, W - 12, 2.5), WOOD, R=rot(r.uniform(-2, 2)), sub=3, rough=0.2, seed=seed + 40 + k)
    W1 = waves(seed + 3, 12, 5, 30)
    def top(x, y):                                                                # povrch slamy (zmackany pod hlavou)
        q = np.stack([x, y, np.zeros_like(x)], -1).reshape(-1, 3)
        e = np.clip(1 - np.maximum(np.abs(x) / (L / 2 - 6), np.abs(y) / (W / 2 - 6)), 0, 1)
        return 38 + 10 * np.minimum(1, e * 7) ** 0.6 + 1.5 * noise(q, W1).reshape(np.shape(x)) - 2.5 * np.exp(-((x + 75) / 22) ** 2)
    nx, ny = 30, 14; xs = np.linspace(-L / 2 + 7, L / 2 - 7, nx + 1); ys = np.linspace(-W / 2 + 6, W / 2 - 6, ny + 1)
    X, Y = np.meshgrid(xs, ys, indexing="ij"); Z = top(X, Y)
    i0 = M.verts(np.stack([X, Y, Z], -1), np.stack([X, Y], -1) / 50)
    for i in range(nx):
        for j in range(ny):
            a = i0 + i * (ny + 1) + j; b = a + ny + 1
            M.tri(a, b, b + 1, STRAW, (0, 0, 1)); M.tri(a, b + 1, a + 1, STRAW, (0, 0, 1))
    if folded:                                                                    # slozena houne v nohach
        add_box(M, (L / 2 - 38, 0, float(top(np.array(L / 2 - 38), np.array(0.0))) + 3.0), (44, W - 14, 7), WOOL, R=rot(r.uniform(-4, 4)), sub=4, rough=0.6, round_=2.5, seed=seed + 60)
        add_box(M, (L / 2 - 38 + r.uniform(-2, 2), r.uniform(-2, 2), float(top(np.array(L / 2 - 38), np.array(0.0))) + 8.5), (40, W - 20, 5), WOOL, R=rot(r.uniform(-6, 6)), sub=4, rough=0.6, round_=2.0, seed=seed + 61)
    else:                                                                         # houne pres slamu, previs do stran
        W2 = waves(seed + 5, 10, 4, 18)
        su = np.linspace(-L / 2 + 40, L / 2 - 8, 26); sv = np.linspace(-W / 2 - 18, W / 2 + 18, 22)
        U, V = np.meshgrid(su, sv, indexing="ij"); yc = np.clip(V, -W / 2 + 1, W / 2 - 1)
        over = np.maximum(np.abs(V) - (W / 2 - 1), 0)                             # cast visici dolu
        Zt = top(U, np.clip(yc, -W / 2 + 6, W / 2 - 6)) + 2.8                       # nad slamou (bez prosvitani)
        q = np.stack([U, V, np.zeros_like(U)], -1).reshape(-1, 3); wr = noise(q, W2).reshape(U.shape)
        hang = np.minimum(over, 3) / 3                                            # plynuly prechod pres hranu
        Pg = np.stack([U, yc + np.sign(V) * (4.0 * hang + 0.6 * wr * hang), Zt - over * 1.0 + 0.4 * wr], -1)
        add_sheet(M, Pg, 1.2, WOOL)
    return M


def table(seed):
    """stul 120 x 70 x 76: deska ze 3 prken, 4 nohy mirne rozkrocene, luby pod deskou, prickove spojeni dole (H)"""
    M = PM(); r = np.random.default_rng(seed); L, W, H = 120.0, 70.0, 76.0
    for k in range(3):
        add_box(M, (r.uniform(-0.5, 0.5), -W / 3 + k * W / 3, H - 2), (L, W / 3 - 0.5, 4), WOOD, R=rot(r.uniform(-0.3, 0.3)), sub=5, rough=0.3, seed=seed + k)
    for sx in (-1, 1):
        for sy in (-1, 1):
            add_box(M, (sx * (L / 2 - 14), sy * (W / 2 - 9), (H - 4) / 2), (6.5, 6.5, H - 4), WOOD,
                    R=rot(0, sx * 2.5, -sy * 2.5), sub=4, rough=0.3, seed=seed + 10 + sx + 2 * sy)
    for sy in (-1, 1):
        add_box(M, (0, sy * (W / 2 - 9), H - 10), (L - 34, 3, 10), WOOD, sub=4, rough=0.25, seed=seed + 20 + sy)
    for sx in (-1, 1):
        add_box(M, (sx * (L / 2 - 14), 0, H - 10), (3, W - 24, 10), WOOD, sub=4, rough=0.25, seed=seed + 25 + sx)
        add_box(M, (sx * (L / 2 - 14.6), 0, 14), (5, W - 16, 5), WOOD, sub=4, rough=0.25, seed=seed + 30 + sx)
    add_box(M, (0, 0, 14), (L - 32, 5, 5), WOOD, sub=4, rough=0.25, seed=seed + 35)
    return M


def chest(seed):
    """truhla 90 x 50 x 55: prkenne steny na nozkach, zavrene viko, zelezne pasy pres viko a celo, zaves s okem
    na zamek, postranni drzadla (kruhy)"""
    M = PM(); r = np.random.default_rng(seed); L, W, H = 90.0, 50.0, 46.0
    for y in (-W / 2 + 1.25, W / 2 - 1.25):
        for k in range(2):
            add_box(M, (0, y, 6 + 10 + k * 20.5), (L, 2.5, 20), WOOD, R=rot(r.uniform(-0.3, 0.3)), sub=5, rough=0.25, seed=seed + k + int(y))
    for x in (-L / 2 + 1.25, L / 2 - 1.25):
        add_box(M, (x, 0, 6 + H / 2 - 4.5), (2.5, W - 5, 41), WOOD, sub=4, rough=0.25, seed=seed + 10 + int(x))
    add_box(M, (0, 0, 7.5), (L - 5, W - 5, 2.5), WOOD, sub=4, rough=0.2, seed=seed + 15)            # dno
    for x in (-L / 2 + 6, L / 2 - 6):                                                          # nozky (prapory)
        add_box(M, (x, 0, 3.5), (8, W, 7), WOOD, sub=4, rough=0.3, seed=seed + 18 + int(x))
    add_box(M, (0, 0, 47 + 1.75), (L + 2, W + 2, 3.5), WOOD, sub=5, rough=0.3, seed=seed + 20)  # viko
    add_box(M, (0, -W / 2 - 0.4, 46.5), (L + 2, 1.5, 4), WOOD, sub=5, rough=0.2, seed=seed + 21)
    for x in (-L / 2 + 14, L / 2 - 14):                                                        # pasy pres viko a celo
        add_box(M, (x, 0, 50.7), (4, W + 2.4, 0.5), IRON, sub=3, rough=0.03, round_=0.15, seed=seed + 30 + int(x))
        add_box(M, (x, -W / 2 - 1.15, 30), (4, 0.5, 40), IRON, sub=3, rough=0.03, round_=0.15, seed=seed + 31 + int(x))
        add_box(M, (x, W / 2 + 1.15, 34), (4, 0.5, 32), IRON, sub=3, rough=0.03, round_=0.15, seed=seed + 32 + int(x))
    add_box(M, (0, -W / 2 - 1.3, 44), (5, 0.6, 12), IRON, sub=3, rough=0.03, round_=0.15, seed=seed + 40)    # zaves
    add_cyl(M, (0, -W / 2 - 1.5, 39), (0, -W / 2 - 3.2, 39), 1.0, 1.0, IRON, n=10)                 # oko na zamek
    for sx in (-1, 1):                                                                        # drzadla
        x = sx * (L / 2 + 0.4); add_box(M, (x, 0, 38), (0.6, 8, 4), IRON, sub=2, rough=0.02, round_=0.15, seed=seed + 50 + sx)
        pts = [(x + sx * 0.5, -4, 37), (x + sx * 1.5, -4.2, 33), (x + sx * 1.8, 0, 31.5), (x + sx * 1.5, 4.2, 33), (x + sx * 0.5, 4, 37)]
        for a, b in zip(pts[:-1], pts[1:]): add_cyl(M, a, b, 0.5, 0.5, IRON, n=8)
    return M


def shelf(seed):
    """police na osobni veci 100 x 28 x 90 (stoji na zemi u zdi): dve bocnice, tri desky, zadni lista (strana +Y ke zdi)"""
    M = PM(); r = np.random.default_rng(seed); L, D, H = 100.0, 28.0, 90.0
    for x in (-L / 2 + 1.25, L / 2 - 1.25):
        add_box(M, (x, 0, H / 2), (2.5, D, H), WOOD, sub=5, rough=0.25, seed=seed + int(x))
    for k, z in enumerate((14, 50, 88)):
        add_box(M, (r.uniform(-0.4, 0.4), 0.5, z), (L - 5, D - 1, 2.5), WOOD, R=rot(r.uniform(-0.3, 0.3)), sub=5, rough=0.25, seed=seed + 10 + k)
    add_box(M, (0, D / 2 - 1, 80), (L - 5, 2, 8), WOOD, sub=4, rough=0.2, seed=seed + 20)            # zadni lista
    return M


def door(seed, W=100.0, H=220.0):
    """dvere 100 x 220: 4 svisla prkna (lic -Y), zezadu 3 svlaky a 2 sikme vzpery (Z), na lici 2 pasove zavesy
    se zavesy na ose X = -W/2, kruhove drzadlo a zastrcka"""
    M = PM(); r = np.random.default_rng(seed); n = 4; pw = W / n
    for k in range(n):
        x = -W / 2 + pw * (k + 0.5)
        add_box(M, (x + r.uniform(-0.2, 0.2), 0, H / 2), (pw - 0.5, 3.0, H - r.uniform(0, 1.5)), WOOD, R=rot(0, r.uniform(-0.15, 0.15)), sub=5, rough=0.3, seed=seed + k)
    zs = (28.0, H / 2, H - 28)
    for k, z in enumerate(zs):                                                                  # svlaky
        add_box(M, (0, 3.0, z), (W - 8, 3.0, 13), WOOD, sub=5, rough=0.3, seed=seed + 10 + k)
    for z0, z1 in ((zs[0], zs[1]), (zs[1], zs[2])):                                              # sikme vzpery (od zavesu dolu ke klice)
        x0, x1 = -W / 2 + 10, W / 2 - 10; dz = z1 - z0 - 13; ln = math.hypot(x1 - x0, dz); ang = math.degrees(math.atan2(dz, x1 - x0))
        add_box(M, (0, 3.0, (z0 + z1) / 2), (ln, 2.8, 10), WOOD, R=rot(0, ang), sub=5, rough=0.3, seed=seed + 20 + int(z0))
    for z in (zs[0], zs[2]):                                                                    # pasove zavesy
        add_box(M, (-W / 2 + 33, -1.75, z), (64, 0.5, 5), IRON, sub=4, rough=0.03, round_=0.15, seed=seed + 30 + int(z))
        add_cyl(M, (-W / 2 - 1.0, -1.0, z - 6), (-W / 2 - 1.0, -1.0, z + 6), 1.3, 1.3, IRON, n=10)      # oko zavesu
    hz = 105.0; hx = W / 2 - 14
    add_cyl(M, (hx, -1.5, hz), (hx, -3.0, hz), 3.0, 2.5, IRON, n=12)                               # stitek
    pts = [(hx + 6 * math.cos(a), -3.4, hz - 6 + 6 * math.sin(a)) for a in np.linspace(math.pi / 2, math.pi / 2 + 2 * math.pi, 13)]
    pts = [(hx, -3.4, hz)] + [(p[0], p[1], p[2] - 0) for p in pts[1:-1]] + [(hx, -3.4, hz)]
    for a, b in zip(pts[:-1], pts[1:]): add_cyl(M, a, b, 0.55, 0.55, IRON, n=8)                     # kruh
    add_box(M, (hx - 10, 4.8, hz), (14, 1.2, 2.5), IRON, sub=2, rough=0.02, round_=0.2, seed=seed + 40)   # zastrcka zezadu
    return M


def shutter(seed):
    """okenice 60 x 60 (na 50 x 50 skalovat): 3 prkna, zezadu 2 svlaky, na lici 2 male pasove zavesy, drzatko"""
    M = PM(); r = np.random.default_rng(seed); W = H = 60.0; n = 3; pw = W / n
    for k in range(n):
        add_box(M, (-W / 2 + pw * (k + 0.5) + r.uniform(-0.15, 0.15), 0, H / 2), (pw - 0.4, 2.5, H - r.uniform(0, 0.8)), WOOD, sub=4, rough=0.25, seed=seed + k)
    for k, z in enumerate((11.0, H - 11)):
        add_box(M, (0, 2.5, z), (W - 6, 2.5, 8), WOOD, sub=4, rough=0.25, seed=seed + 10 + k)
    for z in (11.0, H - 11):
        add_box(M, (-W / 2 + 17, -1.5, z), (34, 0.45, 3.5), IRON, sub=3, rough=0.02, round_=0.12, seed=seed + 20 + int(z))
        add_cyl(M, (-W / 2 - 0.8, -0.9, z - 4), (-W / 2 - 0.8, -0.9, z + 4), 1.0, 1.0, IRON, n=10)
    add_cyl(M, (W / 2 - 8, -1.25, H / 2), (W / 2 - 8, -4.5, H / 2), 1.1, 1.4, WOOD, END, n=10)      # drzatko (kolik)
    return M


def coal_box(seed):
    """truhlik na drevene uhli 80 x 120 x 80: prkenne steny bez vika (viko je samostatny SM_RuinCoalBoxLid),
    uhli do 85 % vysky: tmavy podklad a ~420 kousku"""
    M = PM(); r = np.random.default_rng(seed)
    add_box(M, (0, 0, 2), (80, 120, 4), WOOD, sub=4, seed=seed)
    for (x, y, sx, sy) in ((0, -58, 80, 4), (0, 58, 80, 4), (-38, 0, 4, 112), (38, 0, 4, 112)):
        for k in range(3):                                                    # tri prkna nad sebou
            add_box(M, (x, y, 4 + 12.7 + k * 25.3), (sx, sy, 25), WOOD, R=rot(r.uniform(-0.5, 0.5)), sub=4, rough=0.3, seed=seed + k * 7 + int(x + y))
    W1 = waves(seed + 3, 10, 4, 14)
    def hgt(x, y): return 66 + 2.5 * noise(np.stack([x, y, np.zeros_like(x)], -1).reshape(-1, 3), W1).reshape(np.shape(x)) + 4 * np.exp(-((x / 30) ** 2 + (y / 40) ** 2))
    nx, ny = 16, 24; xs = np.linspace(-36, 36, nx + 1); ys = np.linspace(-56, 56, ny + 1)      # podklad (tmavy, mezi kousky)
    X, Y = np.meshgrid(xs, ys, indexing="ij"); Z = hgt(X, Y)
    i0 = M.verts(np.stack([X, Y, Z], -1), np.stack([X, Y], -1) / 100)
    for i in range(nx):
        for j in range(ny):
            a = i0 + i * (ny + 1) + j; b = a + ny + 1
            M.tri(a, b, b + 1, COAL, (0, 0, 1)); M.tri(a, b + 1, a + 1, COAL, (0, 0, 1))
    for k in range(420):                                                          # kousky uhli (nepravidelne hranoly)
        x = r.uniform(-34, 34); y = r.uniform(-54, 54); sz = r.uniform(2.5, 6.5)
        dims = (sz * r.uniform(0.8, 1.6), sz * r.uniform(0.6, 1.1), sz * r.uniform(0.4, 0.8))
        z = float(hgt(np.array(x), np.array(y))) + dims[2] * r.uniform(-0.1, 0.35)
        add_box(M, (x, y, z), dims, COAL, R=rot(r.uniform(0, 360), r.uniform(-35, 35), r.uniform(-35, 35)), sub=1, rough=0.35, round_=0.15, seed=seed + 200 + k)
    return M


def box_lid(seed):
    """volne viko truhliku 80 x 120: tri prkna podel Y, zespodu dve priecne lajsny (zapadnou mezi steny),
    nahore drevene drzadlo; bez pantu - polozi se bokem"""
    M = PM(); r = np.random.default_rng(seed)
    for k in range(3):                                                         # prkna 26,7 cm, mezi nimi drobna mezera
        x = -26.7 + k * 26.7
        add_box(M, (x + r.uniform(-0.2, 0.2), r.uniform(-0.5, 0.5), 3 + 1.75), (26.2, 120, 3.5), WOOD,
                R=rot(r.uniform(-0.4, 0.4)), sub=4, rough=0.3, seed=seed + k * 7)
    for y in (-40, 40):                                                        # priecne lajsny zespodu, uvnitr sten (vnitrni sirka 72)
        add_box(M, (0, y + r.uniform(-1, 1), 1.5), (68, 7, 3), WOOD, R=rot(r.uniform(-0.6, 0.6)), sub=4, rough=0.3, seed=seed + 40 + int(y))
    add_box(M, (0, 0, 6.5 + 2), (6, 26, 4), WOOD, R=rot(r.uniform(-1, 1)), sub=4, rough=0.3, round_=0.3, seed=seed + 60)   # drzadlo
    return M


def oven_door(seed):
    """poklop usti pece (dobove provizorium z kovarny): kovany plech 46 x 42 cm, tl. 1,2 cm, v rovine XZ; na strane -Y
    drevena rukojet ("chnapka", da se chytit i horka) podel X na dvou kovanych trnech"""
    M = PM(); r = np.random.default_rng(seed)
    add_box(M, (0, 0, 0), (46, 1.2, 42), IRON, sub=5, rough=0.12, round_=0.25, seed=seed)
    for x in (-7.0, 7.0):                                                      # trny rukojeti (roznytovane v plechu)
        add_cyl(M, (x, 0.3, 4.0), (x, -6.0, 4.0), 0.7, 0.6, IRON, n=10, rings=1)
    add_cyl(M, (-10.5, -6.0, 4.0 + r.uniform(-0.2, 0.2)), (10.5, -6.0, 4.0), 1.8, 1.7, WOOD, cap_slot=END, n=14, rings=2, rough=0.08, seed=seed + 3)
    return M


def woodpile(seed, W=190.0, H=140.0, D=60.0):
    """hranice stipanych polen: delka polen podel Y (hloubka 60), rady podel X do vysky H; ctvrtiny a pulky kmene
    (kura na oblouku, cela na koncich)"""
    M = PM(); r = np.random.default_rng(seed)
    z = 0.0
    while z < H - 8:
        x = -W / 2; hrow = 0.0
        while x < W / 2 - 6:
            R_ = r.uniform(7, 10); kind = r.integers(0, 3)          # 0 ctvrtina, 1 pulka, 2 cela kulatina
            if x + 2 * R_ > W / 2: break
            if kind == 2 and R_ > 8.5: kind = 0
            a0 = r.uniform(0, 2 * math.pi)
            if kind == 2:
                arc = np.linspace(0, 2 * math.pi, 14, endpoint=False); poly = np.stack([R_ * 0.75 * np.cos(arc), R_ * 0.75 * np.sin(arc)], 1)
                sl = [BARK] * len(poly)
            else:
                span = math.pi / 2 if kind == 0 else math.pi
                arc = np.linspace(a0, a0 + span, 9); poly = np.vstack([[0, 0], np.stack([R_ * np.cos(arc), R_ * np.sin(arc)], 1)])
                sl = [WOOD] + [BARK] * (len(arc) - 1) + [WOOD]
            poly = poly - poly.min(0)                                 # na zem / na radu
            Rz = rot(90 + r.uniform(-4, 4), 0, 0)
            ln = D * r.uniform(0.92, 1.0); w = poly[:, 0].max()
            add_prism(M, poly, sl, -ln / 2, ln / 2, END, R=Rz, c=(x + r.uniform(-1, 1), r.uniform(-3, 3), z))
            x += w + r.uniform(0.3, 1.5); hrow = max(hrow, poly[:, 1].max())
        z += hrow * 0.92
    return M


def iron_bars(seed):
    """svazek 8 zeleznych prutu 100 cm (ctvercovy prurez 1,5 cm), mirne krive"""
    M = PM(); r = np.random.default_rng(seed)
    for k in range(8):
        y = (k % 4) * 1.8 - 2.7; z = (k // 4) * 1.8 + 0.9
        add_box(M, (r.uniform(-3, 3), y, z), (100, 1.5, 1.5), IRON, R=rot(r.uniform(-1.5, 1.5), r.uniform(-0.5, 0.5)), sub=8, rough=0.05, round_=0.15, seed=seed + k)
    return M


def basket(seed):
    """proutny kos O 40, vyska 35 (vypletany: pruty po obvodu), silnejsi okraj"""
    M = PM()
    zs = np.linspace(0, 35, 15); rr = 15 + 6 * (zs / 35) ** 0.8
    outer = list(zip(zs, rr)); inner = [(z, r - 1.2) for z, r in zip(zs[::-1], rr[::-1])]
    prof = [(0.0, 0.0)] + outer + inner + [(1.2, 0.0)]
    add_lathe(M, prof, (0, 0, 0), (0, 0, 1), [WATTLE] * (len(prof) - 1), n=40, rough=0.35, seed=seed)
    add_lathe(M, [(33.5, rr[-1] - 1.6), (33.5, rr[-1] + 0.8), (36.5, rr[-1] + 0.8), (36.5, rr[-1] - 1.6), (33.5, rr[-1] - 1.6)], (0, 0, 0), (0, 0, 1), [WATTLE] * 4, n=40, rough=0.3, seed=seed + 1)
    return M


def ladder(seed, L=450.0, wd=45.0):
    """zebrik: dve tyce s kurou O 7 (delka podel X), pricle O 4 po 30 cm, konce pricli presahuji"""
    M = PM(); r = np.random.default_rng(seed)
    for k, y in enumerate((-wd / 2, wd / 2)):
        log_piece(M, (-L / 2, y + r.uniform(-1, 1), 0), (L / 2, y + r.uniform(-1, 1), 0), 3.5, seed + k * 11, True, n_ar=14, step=10.0, knots=3)
    x = -L / 2 + 25
    k = 0
    while x < L / 2 - 15:
        log_piece(M, (x, -wd / 2 - 4, 0), (x + r.uniform(-1, 1), wd / 2 + 4, 0), 2.0, seed + 100 + k, False, n_ar=10, step=6.0, knots=0)
        x += 30; k += 1
    return M


PROPS = [  # (jmeno, funkce, varianty, popis)
    ("SM_RuinStump", stump, "AB", "spalek"),
    ("SM_RuinAnvil", anvil, "A", "kovadlina"),
    ("SM_RuinBellows", bellows, "A", "mech na ramu"),
    ("SM_RuinBarrel", barrel, "A", "kalici sud s vodou"),
    ("SM_RuinGrindstone", grindstone, "A", "brus"),
    ("SM_RuinWorkbench", workbench, "A", "ponk se sverakem"),
    ("SM_RuinTongs", tongs, "A", "kovarske kleste"),
    ("SM_RuinHammer", hammer, "A", "kovarske kladivo"),
    ("SM_RuinChisel", chisel, "A", "sekac"),
    ("SM_RuinNailHeader", nail_header, "A", "hrebovnice"),
    ("SM_RuinCoalBox", coal_box, "A", "truhlik s drevenym uhlim"),
    ("SM_RuinWoodpile", woodpile, "A", "hranice stipanych polen"),
    ("SM_RuinIronBars", iron_bars, "A", "svazek zeleznych prutu"),
    ("SM_RuinBasket", basket, "A", "proutny kos"),
    ("SM_RuinLadder", ladder, "A", "zebrik z tyci s kurou"),
    ("SM_RuinGrindstoneTreadle", lambda s: grindstone(s, treadle=True), "A", "slapaci brus"),
    ("SM_RuinStool", stool, "A", "trinoha stolicka"),
    ("SM_RuinCoalBoxLid", box_lid, "A", "volne viko truhliku"),
    ("SM_RuinMallet", mallet, "A", "drevena palice s obrucemi"),
    ("SM_RuinNailHammer", nail_hammer, "A", "kladivo na hrebiky s drapakem"),
    ("SM_RuinBroadaxe", broadaxe, "A", "sekera sirocina"),
    ("SM_RuinAxe", axe, "A", "sekera na stipani"),
    ("SM_RuinCrosscutSaw", crosscut_saw, "A", "dvoumuzna pila"),
    ("SM_RuinBed", lambda s: bed(s, folded=False), "A", "luzko, houne pres slamu"),
    ("SM_RuinBedFolded", lambda s: bed(s, folded=True), "A", "luzko, houne slozena v nohach"),
    ("SM_RuinTable", table, "A", "stul"),
    ("SM_RuinChest", chest, "A", "truhla"),
    ("SM_RuinShelf", shelf, "A", "police"),
    ("SM_RuinDoor", door, "A", "dvere"),
    ("SM_RuinShutter", shutter, "A", "okenice"),
    ("SM_RuinOvenDoor", oven_door, "A", "poklop usti pece s drevenou rukojeti"),
]
NOMINAL = {     # jmenovity rozmer (cm) = bounding box; mesh se na nej normalizuje. Stejna cisla v LIB_MESHES (zrlib/config.py)
    "SM_RuinStump": (53.6, 49.7, 46.7),
    "SM_RuinAnvil": (59.1, 18.1, 24.3),
    "SM_RuinBellows": (210.4, 85.4, 139.0),
    "SM_RuinBarrel": (61.3, 61.2, 80.3),
    "SM_RuinGrindstone": (120.0, 86.0, 105.4),
    "SM_RuinWorkbench": (221.5, 85.9, 85.2),
    "SM_RuinTongs": (50.2, 4.7, 2.8),
    "SM_RuinHammer": (4.3, 36.4, 11.0),
    "SM_RuinChisel": (20.6, 2.8, 2.8),
    "SM_RuinNailHeader": (25.0, 6.0, 1.5),
    "SM_RuinCoalBox": (80.6, 120.5, 80.0),
    "SM_RuinWoodpile": (191.3, 65.0, 136.4),
    "SM_RuinIronBars": (103.2, 9.0, 3.8),
    "SM_RuinBasket": (43.5, 44.0, 36.5),
    "SM_RuinLadder": (450.4, 53.7, 7.8),
    "SM_RuinGrindstoneTreadle": (120.0, 86.0, 105.3),
    "SM_RuinStool": (34.9, 33.4, 45.4),
    "SM_RuinCoalBoxLid": (80.1, 120.3, 10.6),
    "SM_RuinMallet": (9.5, 34.9, 14.0),
    "SM_RuinNailHammer": (3.0, 34.0, 10.5),
    "SM_RuinBroadaxe": (6.9, 72.1, 25.0),
    "SM_RuinAxe": (4.6, 76.5, 18.7),
    "SM_RuinCrosscutSaw": (150.9, 3.9, 28.3),
    "SM_RuinBed": (200.2, 87.2, 61.9),
    "SM_RuinBedFolded": (200.3, 80.3, 62.5),
    "SM_RuinTable": (119.7, 69.5, 76.2),
    "SM_RuinChest": (95.4, 54.6, 51.2),
    "SM_RuinShelf": (100.2, 27.7, 89.6),
    "SM_RuinDoor": (101.8, 9.3, 219.3),
    "SM_RuinShutter": (61.4, 8.4, 59.2),
    "SM_RuinOvenDoor": (45.9, 8.6, 41.9),
}


def build(out):
    """props do slozky out -> seznam (jmeno, vrcholu, trojuhelniku)"""
    made = []
    for pref, fn, vs, desc in PROPS:
        for vi, v in enumerate(vs):
            P, UV, G, F, S = fn(23000 + 97 * PROPS.index((pref, fn, vs, desc)) + vi * 13).arrays()
            used = sorted(set(S.tolist())); names = tuple(SLOTS[i] for i in used); remap = {s: i for i, s in enumerate(used)}
            S2 = np.array([remap[s] for s in S])
            mn, mx = P.min(0), P.max(0)
            P = (P - (mn + mx) / 2) / (mx - mn) * np.array(NOMINAL[pref])
            name = "%s_%s" % (pref, v)
            write_obj_slots(os.path.join(out, name + ".obj"), P, UV, smooth_normals(P, F, G), F, S2, name, desc, names)
            made.append((name, len(P), len(F)))
    return made
