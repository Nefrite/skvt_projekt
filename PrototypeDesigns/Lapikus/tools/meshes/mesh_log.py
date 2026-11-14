"""mesh_log - kulatina (OBJ, cm, Z nahoru): loupana a s kurou, tyce, kuly, hlava rozsochy, zlab. Kategorie wood.

Kazdy mesh ma materialove sloty (usemtl, poradi SLOT_ORDER v mesh_common):
  Wood     = plast loupane kulatiny, holy povrch pod kurou, zaseknute spicky, vydlabany zlab -> material podle upravy dreva
  EndGrain = cela (letokruhy; UV polarni: u = uhel, v = vzdalenost od stredu v m)
  Bark     = kura (jen *Bark, kul, rozsocha)
Delka podel X, prurez Y x Z, pivot ve stredu, bounding box = jmenovity rozmer (NOMINAL, stejne v zrlib/config.py ROUND_MESHES).
UV plaste: u = delka v m, v = obvod jako cely pocet m (bez svu textury).
"""
import math, os
import numpy as np

from mesh_common import waves, noise, smooth_normals, write_obj_slots

WOOD, END, BARK = 0, 1, 2

# jmenovite rozmery (cm): delka, sirka, vyska; musi odpovidat ROUND_MESHES v zrlib/config.py
NOMINAL = {
    "SM_RuinLog":        (100.0, 20.0, 20.0),
    "SM_RuinLogBark":    (100.0, 20.0, 20.0),
    "SM_RuinPole":       (100.0, 8.0, 8.0),
    "SM_RuinPoleBark":   (100.0, 8.0, 8.0),
    "SM_RuinStake":      (200.0, 20.0, 20.0),
    "SM_RuinStakeSmall": (160.0, 7.0, 7.0),
    "SM_RuinForkHead":   (45.0, 30.0, 12.0),
    "SM_RuinGutter":     (100.0, 20.0, 11.0),
    "SM_RuinGutterBark": (100.0, 20.0, 11.0),
}
VARIANTS = {"SM_RuinStakeSmall": "AB", "SM_RuinForkHead": "AB", "SM_RuinGutter": "AB", "SM_RuinGutterBark": "AB"}      # ostatni ABC


def _frame(T):
    ref = np.array([0.0, 0.0, 1.0]) if abs(T[2]) < 0.9 else np.array([0.0, 1.0, 0.0])
    Z = ref - (ref @ T) * T; Z /= np.linalg.norm(Z)
    return np.cross(Z, T), Z


def _angdiff(a, b):
    return (a - b + math.pi) % (2 * math.pi) - math.pi


class Mesh:
    """skladani dilu: vrcholy, UV, plochy, slot plochy, skupina hladkych normal vrcholu"""
    def __init__(self):
        self.P, self.UV, self.G, self.F, self.S = [], [], [], [], []
        self.n = 0; self.g = 0
    def verts(self, P, UV):
        i0 = self.n; P = np.asarray(P).reshape(-1, 3); UV = np.asarray(UV).reshape(-1, 2)
        self.P.append(P); self.UV.append(UV); self.G.append(np.full(len(P), self.g)); self.n += len(P)
        return i0
    def new_group(self):
        self.g += 1
    def tri(self, a, b, c, slot):
        self.F.append((a, b, c)); self.S.append(slot)
    def arrays(self):
        P = np.concatenate(self.P); UV = np.concatenate(self.UV); G = np.concatenate(self.G)
        F = np.array(self.F, dtype=int); S = np.array(self.S, dtype=int)
        a = np.linalg.norm(np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]), axis=1)
        keep = a > 1e-4                                   # bez degenerovanych trojuhelniku
        return P, UV, G, F[keep], S[keep]


def tube(M, L, R, seed, bark, n_ar=48, step=4.0, path=None, taper=0.95, bark_t=0.9, strip=0.22, oval=0.035,
         start=None, end=None, knots=3, peel=True, bow=0.5):
    """kulatina podel stredove cary path(s) (s 0..1 -> bod), polomer dreva R (cm), kura bark_t navic.
    start / end: dict(cut=uhel seknuti ve st.) nebo dict(tip=delka spicky, facets=pocet) - konce, vzdy s celem."""
    rng = np.random.default_rng(seed)
    start = start or dict(cut=rng.uniform(1, 5)); end = end or dict(cut=rng.uniform(1, 5))
    if path is None:
        bd = rng.normal(size=2); bd = bd / (np.linalg.norm(bd) + 1e-9) * bow
        path = lambda s: np.array([(s - 0.5) * L, bd[0] * 4 * s * (1 - s), bd[1] * 4 * s * (1 - s)])
    # rady vrcholu: rovnomerne, na spickach husteji
    t0 = start.get("tip", 0.0) / L; t1 = end.get("tip", 0.0) / L
    ss = [np.linspace(0, t0, 9)[:-1]] if t0 else []
    nb = max(2, int(round((1 - t0 - t1) * L / step)))
    ss.append(np.linspace(t0, 1 - t1, nb + 1))
    if t1: ss.append(np.linspace(1 - t1, 1, 9)[1:])
    S = np.concatenate(ss); n_r = len(S)
    C = np.array([path(s) for s in S])
    dC = np.gradient(C, axis=0); T = dC / np.linalg.norm(dC, axis=1, keepdims=True)
    arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))])
    th = np.linspace(0, 2 * math.pi, n_ar + 1)
    W1 = waves(seed + 1, 8, 12, 40); Wf = waves(seed + 2, 12, 2.0, 5.0); Wm = waves(seed + 3, 6, 15, 45)
    po = rng.uniform(0, 2 * math.pi); kn = [(rng.uniform(0.1, 0.9), rng.uniform(0, 2 * math.pi), rng.uniform(0.25, 0.5), rng.uniform(1.5, 3.0))
                                           for _ in range(knots)]
    nf = int(rng.integers(9, 15)); pph = rng.uniform(0, 2 * math.pi)
    P = np.zeros((n_r, n_ar + 1, 3)); RW = np.zeros((n_r, n_ar + 1)); RF = np.zeros_like(RW); BK = np.zeros(RW.shape, bool)
    ct, st = np.cos(th), np.sin(th)
    # oloupana mista kury: prah podle rozlozeni sumu -> podil holeho povrchu = strip
    mnz = np.array([noise(np.stack([np.full(n_ar + 1, arc[i]), R * ct, R * st], 1) * np.array([0.5, 1.0, 1.0]), Wm) for i in range(n_r)])
    mth = np.quantile(mnz, strip) if bark else 0.0
    for i in range(n_r):
        x = arc[i]; base = R * (1 + (taper - 1) * S[i])
        q = np.stack([np.full(n_ar + 1, x), base * ct, base * st], 1)
        rw = base * (1 + oval * np.cos(2 * (th - po))) + 0.03 * R * noise(q, W1)
        for ks, kt, ka, kz in kn:                      # suky
            dx = x - ks * L; da = _angdiff(th, kt) * base
            rw = rw + ka * np.exp(-(dx * dx + da * da) / (kz * kz))
        if not bark and peel:                          # stopy po loupaku: mele ploske pasy podel delky
            rw = rw - 0.012 * R * (0.5 + 0.5 * np.cos(nf * th + pph + 0.8 * noise(q * [0.02, 1, 1], W1)))
        rt = rw.copy(); pres = np.zeros(n_ar + 1, bool)
        if bark:
            qa = q * np.array([0.12, 1.0, 1.0])
            pres = mnz[i] > mth
            fur = (1 - np.abs(noise(qa, Wf))) ** 4
            rt = rw + bark_t * pres * (1 - 0.55 * fur)
        rf = rt.copy()
        for e, sgn, sx in ((start, -1, x), (end, 1, arc[-1] - x)):
            if "tip" in e:                             # zaseknuta spicka: rovne plochy (facets) ke stredu
                h = sx / e["tip"] * R * 1.05
                if h < base * 1.6:
                    fk = e.get("facets", 5); ph = rng.uniform(0, 2 * math.pi) if i == 0 else e.setdefault("_ph", rng.uniform(0, 2 * math.pi))
                    lim = np.full(n_ar + 1, np.inf)
                    for k in range(fk):
                        c = np.cos(th - (ph + 2 * math.pi * k / fk))
                        lim = np.minimum(lim, np.where(c > 0.15, h / np.maximum(c, 0.15), np.inf))
                    rf = np.minimum(rf, np.maximum(lim, 0.25))
        cut = rf < rt - 0.05
        Y, Z = _frame(T[i])
        d = ct[:, None] * Y + st[:, None] * Z
        P[i] = C[i] + rf[:, None] * d
        RW[i] = np.minimum(rw, rf); RF[i] = rf; BK[i] = pres & ~cut
    # seknute / rezane konce: celo sikmo (cut = uhel)
    for i, e, sgn in ((0, start, -1), (n_r - 1, end, 1)):
        if "cut" in e:
            al = rng.uniform(0, 2 * math.pi); tl = math.tan(math.radians(e["cut"]))
            P[i] += (sgn * tl * RF[i] * np.cos(th - al))[:, None] * T[i]
    kv = max(1, round(2 * math.pi * R / 100.0))
    UVm = np.stack([np.repeat(arc / 100.0, n_ar + 1), np.tile(th / (2 * math.pi) * kv, n_r)], 1)
    M.new_group(); i0 = M.verts(P, UVm)
    idx = lambda i, j: i0 + i * (n_ar + 1) + j
    for i in range(n_r - 1):
        for j in range(n_ar):
            sl = BARK if (BK[i, j] and BK[i + 1, j] and BK[i, j + 1] and BK[i + 1, j + 1]) else WOOD
            M.tri(idx(i, j), idx(i, j + 1), idx(i + 1, j + 1), sl); M.tri(idx(i, j), idx(i + 1, j + 1), idx(i + 1, j), sl)
    # cela
    for i, sgn in ((0, -1), (n_r - 1, 1)):
        Pr = P[i]; ce = Pr[:-1].mean(0); nrm = sgn * T[i]
        kw = (RW[i] / np.maximum(RF[i], 1e-6))[:, None]
        rings = [(Pr, RF[i]), (ce + kw * (Pr - ce), RW[i])]
        for rho in (0.68, 0.36):
            rings.append((ce + rho * kw * (Pr - ce), rho * RW[i]))
        M.new_group(); base_i = []
        rng2 = np.random.default_rng(seed + 50 + i)
        for k, (pp, rr) in enumerate(rings):
            pp = pp.copy()
            if k > 1:                                    # mirne propadle, nerovne celo (seknuti, vysychani)
                pp -= (0.04 * R * (1 - (rr / max(R, 1e-6)) ** 2))[:, None] * nrm[None, :]
                pp += nrm[None, :] * rng2.normal(0, 0.03 * R / 10, (n_ar + 1, 1))
            uv = np.stack([th / math.pi, rr / 100.0], 1)
            base_i.append(M.verts(pp, uv))
        cen = M.verts(np.repeat(ce[None, :] - nrm * 0.04 * R, n_ar, 0), np.stack([(th[:-1] + th[1:]) / (2 * math.pi), np.zeros(n_ar)], 1))
        faces = []
        for k in range(len(rings) - 1):
            a0, b0 = base_i[k], base_i[k + 1]
            for j in range(n_ar):
                sl = END
                if k == 0:
                    if not (BK[i, j] and BK[i, j + 1]): continue
                    sl = BARK
                faces.append((a0 + j, a0 + j + 1, b0 + j + 1, sl)); faces.append((a0 + j, b0 + j + 1, b0 + j, sl))
        last = base_i[-1]
        for j in range(n_ar):
            faces.append((last + j, last + j + 1, cen + j, END))
        allP = np.concatenate(M.P)
        for a, b, c, sl in faces:
            fn = np.cross(allP[b] - allP[a], allP[c] - allP[a])
            if fn @ nrm < 0: a, b = b, a
            M.tri(a, b, c, sl)
    return M


def finish(M, nominal):
    P, UV, G, F, S = M.arrays()
    mn, mx = P.min(0), P.max(0)
    P = (P - (mn + mx) / 2) / (mx - mn) * np.array(nominal)
    return P, UV, smooth_normals(P, F, G), F, S


def make_log(seed, bark, R=10.0, L=100.0):
    return tube(Mesh(), L, R, seed, bark)


def make_pole(seed, bark):
    return tube(Mesh(), 100.0, 4.0, seed, bark, n_ar=24, step=5.0, bark_t=0.35, strip=0.12, knots=4, oval=0.05, bow=0.9, taper=0.93)


def make_stake(seed):
    rng = np.random.default_rng(seed)
    return tube(Mesh(), 200.0, 10.0, seed, True, step=5.0, end=dict(tip=rng.uniform(24, 32), facets=int(rng.integers(4, 7))), bow=1.0)


def make_stake_small(seed):
    rng = np.random.default_rng(seed)
    return tube(Mesh(), 160.0, 3.5, seed, False, n_ar=20, step=6.0, start=dict(tip=rng.uniform(10, 14), facets=4),
                end=dict(tip=rng.uniform(10, 14), facets=4), knots=2, bow=0.8, taper=0.97)


def make_fork(seed):
    """hlava rozsochy: kousek kmene a dve ramena vidlice (kura), ramena seknuta; prekryvy dilu nevadi"""
    rng = np.random.default_rng(seed)
    M = Mesh()
    tube(M, 20.0, 6.0, seed, True, n_ar=32, step=3.0, path=lambda s: np.array([s * 20.0, 0, 0]), taper=0.98, knots=1)
    for k, sg in enumerate((-1, 1)):
        sp = rng.uniform(11, 14); ln = rng.uniform(40, 45)
        p0 = np.array([12.0, 0, 0]); p1 = np.array([24.0, sg * 2.5, rng.uniform(-1, 1)]); p2 = np.array([ln, sg * sp, rng.uniform(-1.5, 1.5)])
        path = lambda s, p0=p0, p1=p1, p2=p2: (1 - s) ** 2 * p0 + 2 * s * (1 - s) * p1 + s * s * p2
        tube(M, ln - 10, 4.3, seed + 10 + k, True, n_ar=28, step=3.0, path=path, taper=0.8, knots=1,
             start=dict(cut=0.0), end=dict(cut=rng.uniform(15, 30)))
    return M


def make_gutter(seed, bark=True, L=100.0, R=10.0, bark_t=0.9):
    """zlab: pulka kmene (s kurou zvenku, nebo loupana se stopami po loupaku), nahore rovina stipu, vydlabany zlab, cela"""
    rng = np.random.default_rng(seed)
    M = Mesh()
    c = 0.12 * R; ri = 0.62 * R; depth = 0.75 * ri
    a0 = math.asin(c / R); nf = int(rng.integers(9, 15)); pph = rng.uniform(0, 2 * math.pi)
    nO, nI, n_l = 40, 28, int(L / 4)
    xs = np.linspace(-L / 2, L / 2, n_l + 1)
    W1 = waves(seed + 1, 8, 12, 40); Wf = waves(seed + 2, 12, 2.0, 5.0); Wm = waves(seed + 3, 6, 15, 45)
    tho = np.linspace(math.pi - a0, 2 * math.pi + a0, nO + 1)            # vnejsi oblouk zleva dolu doprava
    thi = np.linspace(math.pi, 2 * math.pi, nI + 1)                       # zlab
    def outer(x):
        q = np.stack([np.full(nO + 1, x), R * np.cos(tho), R * np.sin(tho)], 1)
        rw = R * (1 + 0.03 * noise(q, W1)); pres = (noise(q * [0.5, 1, 1], Wm) > mth) & bark
        fur = (1 - np.abs(noise(q * [0.12, 1, 1], Wf))) ** 4
        r = rw + bark_t * pres * (1 - 0.55 * fur)
        if not bark:                                       # stopy po loupaku (ploske pasy podel delky)
            r = r - 0.012 * R * (0.5 + 0.5 * np.cos(nf * tho + pph + 0.8 * noise(q * [0.02, 1, 1], W1)))
        y = r * np.cos(tho); z = np.maximum(r * np.sin(tho), -9e9); z[0] = z[-1] = c
        return np.stack([np.full(nO + 1, x), y, z], 1), pres
    mth = np.quantile(np.concatenate([noise(np.stack([np.full(nO + 1, x), R * np.cos(tho), R * np.sin(tho)], 1) * [0.5, 1, 1], Wm)
                                      for x in xs]), 0.2)
    def inner(x):
        y = ri * np.cos(thi); z = c + depth * np.sin(thi) * (1 + 0.04 * np.sin(x * 0.1 + seed))
        return np.stack([np.full(nI + 1, x), y, z], 1)
    O = np.array([outer(x)[0] for x in xs]); PR = np.array([outer(x)[1] for x in xs]); I = np.array([inner(x) for x in xs])
    O[:, 0, 2] = c; O[:, -1, 2] = c
    def strip(A, uv_v, slot_fn, flip=False):
        M.new_group(); n1 = A.shape[1]
        i0 = M.verts(A.reshape(-1, 3), np.stack([np.repeat(xs / 100.0, n1), np.tile(uv_v, len(xs))], 1))
        for i in range(len(xs) - 1):
            for j in range(n1 - 1):
                a, b, cc, d = i0 + i * n1 + j, i0 + i * n1 + j + 1, i0 + (i + 1) * n1 + j + 1, i0 + (i + 1) * n1 + j
                sl = slot_fn(i, j)
                if flip: M.tri(a, cc, b, sl); M.tri(a, d, cc, sl)
                else: M.tri(a, b, cc, sl); M.tri(a, cc, d, sl)
    arcO = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(O[0], axis=0), axis=1))]) / 100.0
    strip(O, arcO, lambda i, j: BARK if PR[i, j] and PR[i + 1, j] and PR[i, j + 1] and PR[i + 1, j + 1] else WOOD)
    arcI = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(I[0], axis=0), axis=1))]) / 100.0
    strip(I, arcI, lambda i, j: WOOD, flip=True)
    for side in (0, -1):                                   # rovina stipu (okraje zlabu)
        A = np.stack([O[:, side], I[:, side]], 1)
        strip(A, np.array([0.0, abs(O[0, side, 1] - I[0, side, 1]) / 100.0]), lambda i, j: WOOD, flip=(side == 0))
    for i, sgn in ((0, -1), (len(xs) - 1, 1)):             # cela: pas mezi vnejsim obloukem a zlabem
        M.new_group()
        k = np.linspace(0, 1, nO + 1); Iu = np.array([np.interp(k, np.linspace(0, 1, nI + 1), I[i][:, a]) for a in range(3)]).T
        oo = M.verts(O[i], np.stack([O[i][:, 1] / 100.0, O[i][:, 2] / 100.0], 1))
        ii = M.verts(Iu, np.stack([Iu[:, 1] / 100.0, Iu[:, 2] / 100.0], 1))
        allP = np.concatenate(M.P); nrm = np.array([sgn, 0.0, 0.0])
        for j in range(nO):
            for a, b, cc in ((oo + j, oo + j + 1, ii + j + 1), (oo + j, ii + j + 1, ii + j)):
                if np.cross(allP[b] - allP[a], allP[cc] - allP[a]) @ nrm < 0: a, b = b, a
                M.tri(a, b, cc, END)
    return M


def _write(out, name, M, desc, made):
    P, UV, N, F, S = finish(M, NOMINAL[name.rsplit("_", 1)[0]])
    write_obj_slots(os.path.join(out, name + ".obj"), P, UV, N, F, S, name, desc)
    made.append((name, len(P), len(F)))


def build(out):
    """kulatina do slozky out -> seznam (jmeno, vrcholu, trojuhelniku)"""
    made = []
    for vi, v in enumerate("ABC"):
        _write(out, "SM_RuinLog_" + v, make_log(12000 + vi * 71, False), "loupana kulatina", made)
        _write(out, "SM_RuinLogBark_" + v, make_log(12500 + vi * 73, True), "kulatina s kurou", made)
        _write(out, "SM_RuinPole_" + v, make_pole(13000 + vi * 79, False), "loupana tyc", made)
        _write(out, "SM_RuinPoleBark_" + v, make_pole(13500 + vi * 83, True), "tyc s kurou", made)
        _write(out, "SM_RuinStake_" + v, make_stake(14000 + vi * 89), "kul s kurou, zaseknuta spicka", made)
    for vi, v in enumerate("AB"):
        _write(out, "SM_RuinStakeSmall_" + v, make_stake_small(14500 + vi * 97), "loupany kul, spicky na obou koncich", made)
        _write(out, "SM_RuinForkHead_" + v, make_fork(15000 + vi * 101), "hlava rozsochy (vidlice)", made)
        _write(out, "SM_RuinGutter_" + v, make_gutter(15600 + vi * 107, bark=False), "vydlabany zlab loupany", made)
        _write(out, "SM_RuinGutterBark_" + v, make_gutter(15500 + vi * 103), "vydlabany zlab s kurou", made)
    return made
