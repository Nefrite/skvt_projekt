"""mesh_wattle - prouti a mazanina (OBJ, cm, Z nahoru). Kategorie wattle (v UE Ruin/Wattle).

SM_RuinWattlePanel_A..C: dilec proutene steny omazane hlinou 100 x 100 cm (X sirka, Z vyska), tloustka 8 cm (Y).
    Okraje dilce jsou rovne (bez nerovnosti), takze se dilce skladaji vedle sebe a nad sebe do libovolne steny.
SM_RuinSmokeHood_A..B: dymnik: zuzujici se kos z prouti vymazany hlinou, dole 140 x 120, nahore 50 x 50, vyska 100 cm,
    otevreny dole i nahore, stena 5 cm. Skaluje se na rozmer dymniku.
SM_RuinChimney_A..B: komin z prouti a hliny 60 x 60 cm, vyska 100 cm (skaluje se na vysku), stena 6 cm, mirne se zuzuje.
SM_RuinOvenDome_A..B: hlinena klenba pece (plne teleso, nize sklenuta valena klenba): X sirka 140 (rozpeti), Y hloubka 100,
    Z vyska 40 cm; dole otevrena (lezi na zdech pece), cela vymazana hlinou. Skaluje se na rozmer pece.
Sloty: Daub (mazanina, vetsina povrchu), Wattle (mista, kde hlina opadala a je videt vyplet; zapustena o 1,5-2 cm).
UV v metrech (textury: dlazdice 0,5 m, pruty vyspletu vodorovne podel U).
"""
import math, os
import numpy as np

from mesh_common import waves, noise, smooth_normals, write_obj_slots

NOMINAL = {
    "SM_RuinWattlePanel": (100.0, 8.0, 100.0),
    "SM_RuinSmokeHood":   (140.0, 120.0, 100.0),
    "SM_RuinChimney":     (60.0, 60.0, 100.0),
    "SM_RuinOvenDome":    (140.0, 100.0, 40.0),
}
SLOTS = ("Daub", "Wattle")
DAUB, WATTLE = 0, 1


class _M:
    def __init__(self): self.P, self.UV, self.G, self.F, self.S = [], [], [], [], []; self.n = 0
    def verts(self, P, UV, g):
        P = np.asarray(P).reshape(-1, 3); i = self.n; self.P.append(P); self.UV.append(np.asarray(UV).reshape(-1, 2))
        self.G.append(np.full(len(P), g)); self.n += len(P); return i
    def quad_grid(self, i0, n1, n2, slot_fn, flip=False):
        for a in range(n1):
            for b in range(n2):
                v00 = i0 + a * (n2 + 1) + b; v10 = v00 + n2 + 1; v01 = v00 + 1; v11 = v10 + 1
                f1, f2 = (v00, v10, v11), (v00, v11, v01)
                if flip: f1, f2 = f1[::-1], f2[::-1]
                sl = slot_fn(a, b); self.F += [f1, f2]; self.S += [sl, sl]
    def arrays(self):
        return np.concatenate(self.P), np.concatenate(self.UV), np.concatenate(self.G), np.array(self.F), np.array(self.S)


def _daub_disp(q, W1, W2, Wh, hole_th, amp=0.8, recess=1.8):
    """posun povrchu mazaniny (+ ven) a maska odhalenych mist (vyplet)"""
    d = amp * (noise(q, W1) + 0.35 * noise(q, W2))
    hole = noise(q * 0.8, Wh) > hole_th
    return np.where(hole, -recess + 0.3 * noise(q, W2), d), hole


def make_panel(seed, Wd=100.0, H=100.0, T=8.0, n=40, holes=0.10):
    W1 = waves(seed + 1, 10, 10, 40); W2 = waves(seed + 2, 12, 2, 6); Wh = waves(seed + 3, 8, 15, 40)
    xs = np.linspace(-Wd / 2, Wd / 2, n + 1); zs = np.linspace(-H / 2, H / 2, n + 1)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    fade = np.clip(np.minimum(Wd / 2 - np.abs(X), H / 2 - np.abs(Z)) / 4.0, 0, 1)       # rovne okraje -> dilce navazuji
    M = _M()
    allq = np.stack([X.ravel(), np.zeros(X.size), Z.ravel()], 1)
    th = np.quantile(noise(allq * 0.8, Wh), 1 - holes)
    for side, g in ((1, 0), (-1, 1)):
        q = np.stack([X.ravel(), np.full(X.size, side * 50.0), Z.ravel()], 1)
        d, hole = _daub_disp(q, W1, W2, Wh, th)
        d = d.reshape(X.shape) * fade; hole = hole.reshape(X.shape) & (fade > 0.5)
        Y = side * (T / 2 + d)
        i0 = M.verts(np.stack([X, Y, Z], -1), np.stack([X / 100, Z / 100], -1), g)
        M.quad_grid(i0, n, n, lambda a, b, h=hole: WATTLE if (h[a, b] and h[a + 1, b] and h[a, b + 1] and h[a + 1, b + 1]) else DAUB,
                    flip=(side < 0))
    # okraje (rovne, mazanina)
    for (x0, z0, x1, z1) in ((-Wd / 2, -H / 2, Wd / 2, -H / 2), (Wd / 2, -H / 2, Wd / 2, H / 2), (Wd / 2, H / 2, -Wd / 2, H / 2), (-Wd / 2, H / 2, -Wd / 2, -H / 2)):
        k = np.linspace(0, 1, n + 1)
        px = x0 + (x1 - x0) * k; pz = z0 + (z1 - z0) * k
        A = np.stack([np.stack([px, np.full(n + 1, -T / 2), pz], -1), np.stack([px, np.full(n + 1, T / 2), pz], -1)], 1)
        L = np.hypot(x1 - x0, z1 - z0) / 100
        i0 = M.verts(A, np.stack(np.meshgrid(k * L, [0, T / 100], indexing="ij"), -1), 2)
        M.quad_grid(i0, n, 1, lambda a, b: DAUB)
    return M


def make_tube(seed, bw, bd, tw, td, H, T, n_per=64, n_h=24, holes=0.10, round_r=6.0):
    """dutý jehlan / komin: obdelnik bw x bd dole -> tw x td nahore, vyska H, stena T; zaoblene rohy"""
    W1 = waves(seed + 1, 10, 10, 40); W2 = waves(seed + 2, 12, 2, 6); Wh = waves(seed + 3, 8, 15, 40)
    def rrect(w, d, r, m):
        """body po obvodu zaobleneho obdelniku (m bodu, rovnomerne po delce) + normaly ven"""
        hw, hd = w / 2 - r, d / 2 - r
        P = []; N = []
        per = 2 * (2 * hw) + 2 * (2 * hd) + 2 * math.pi * r
        for s in np.linspace(0, per, m, endpoint=False):
            for (cx, cy, a0, ln_) in ((hw, -hd, -math.pi / 2, 2 * hd), (hw, hd, 0, 2 * hw), (-hw, hd, math.pi / 2, 2 * hd), (-hw, -hd, math.pi, 2 * hw)):
                # rovny usek po ose a pak ctvrtkruh
                if s < ln_:
                    dirs = {-math.pi / 2: (0, 1), 0: (-1, 0), math.pi / 2: (0, -1), math.pi: (1, 0)}[a0]
                    nrm = (math.cos(a0 + math.pi / 2), math.sin(a0 + math.pi / 2))
                    P.append((cx + nrm[0] * r + dirs[0] * s, cy + nrm[1] * r + dirs[1] * s)); N.append(nrm); break
                s -= ln_
                arc = math.pi / 2 * r
                if s < arc:
                    a = a0 + math.pi / 2 + s / r
                    ccx, ccy = {(-math.pi / 2): (hw, hd), 0: (-hw, hd), (math.pi / 2): (-hw, -hd), math.pi: (hw, -hd)}[a0]
                    P.append((ccx + r * math.cos(a), ccy + r * math.sin(a))); N.append((math.cos(a), math.sin(a))); break
                s -= arc
        return np.array(P), np.array(N), per
    pb, nb, perb = rrect(bw, bd, round_r, n_per); pt, nt, pert = rrect(tw, td, round_r * tw / bw, n_per)
    h = np.linspace(0, 1, n_h + 1)
    qa = np.concatenate([np.stack([(pb * (1 - hh) + pt * hh)[:, 0], (pb * (1 - hh) + pt * hh)[:, 1], np.full(n_per, hh * H)], 1) for hh in h])
    th = np.quantile(noise(qa * 0.8, Wh), 1 - holes)                   # podil odhaleneho vypletu = holes
    M = _M()
    for side, g in ((1, 0), (-1, 1)):                                   # vnejsi a vnitrni plocha
        A = np.zeros((n_per + 1, n_h + 1, 3)); UV = np.zeros((n_per + 1, n_h + 1, 2)); HL = np.zeros((n_per + 1, n_h + 1), bool)
        for j, hh in enumerate(h):
            p = pb * (1 - hh) + pt * hh; nn = nb * (1 - hh) + nt * hh; nn /= np.linalg.norm(nn, axis=1, keepdims=True)
            z = np.full(n_per, hh * H)
            q = np.stack([p[:, 0], p[:, 1], z], 1)
            d, hole = _daub_disp(q, W1, W2, Wh, th)
            if side > 0: off = d
            else: off = -T + 0.3 * noise(q, W2); hole = np.zeros(n_per, bool)
            fade = np.clip(min(hh, 1 - hh) * H / 4.0, 0, 1)
            pp = p + nn * (off * (fade if side > 0 else 1))[:, None]
            A[:n_per, j] = np.stack([pp[:, 0], pp[:, 1], z], 1); A[n_per, j] = A[0, j]
            per = perb * (1 - hh) + pert * hh
            UV[:, j, 0] = np.linspace(0, per / 100, n_per + 1); UV[:, j, 1] = hh * H / 100
            HL[:n_per, j] = hole & (fade > 0.5); HL[n_per, j] = HL[0, j]
        i0 = M.verts(A, UV, g)
        M.quad_grid(i0, n_per, n_h, (lambda a, b, h_=HL: WATTLE if (h_[a, b] and h_[a + 1, b] and h_[a, b + 1] and h_[a + 1, b + 1]) else DAUB),
                    flip=(side < 0))
        if side > 0: outer = A
        else: inner = A
    for j, g in ((0, 2), (n_h, 3)):                                     # okraj dole a nahore
        R = np.stack([outer[:, j], inner[:, j]], 1)
        uv = np.stack(np.meshgrid(np.linspace(0, 1, n_per + 1), [0, T / 100], indexing="ij"), -1)
        i0 = M.verts(R, uv, g)
        M.quad_grid(i0, n_per, 1, lambda a, b: DAUB, flip=(j == n_h))
    return M


def make_dome(seed, Wd=140.0, D=100.0, H=40.0, n_u=36, n_v=20, holes=0.03):
    """klenba pece: profil napric X = stlaceny oblouk se svislymi boky (superelipsa), tazeny podel Y; cela (predni a zadni)
    jsou rovna. Povrch nerovny jako rukou nanesena hlina, misty odhaleny vyplet kostry."""
    W1 = waves(seed + 1, 10, 12, 45); W2 = waves(seed + 2, 12, 2, 6); Wh = waves(seed + 3, 8, 15, 40)
    t = np.linspace(0, math.pi, n_u + 1); e = 0.62
    px = -Wd / 2 * np.sign(np.cos(t)) * np.abs(np.cos(t)) ** e; pz = H * np.abs(np.sin(t)) ** e
    nx = np.gradient(pz); nz = -np.gradient(px); nl = np.hypot(nx, nz); nx, nz = -nx / nl, -nz / nl
    if nz[n_u // 2] < 0: nx, nz = -nx, -nz
    ys = np.linspace(-D / 2, D / 2, n_v + 1)
    X, Y = np.meshgrid(px, ys, indexing="ij"); Z = np.meshgrid(pz, ys, indexing="ij")[0]
    q = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    th = np.quantile(noise(q * 0.8, Wh), 1 - holes)
    d, hole = _daub_disp(q, W1, W2, Wh, th, amp=1.0, recess=1.5)
    fade = np.clip(np.minimum(np.minimum(Y - ys[0], ys[-1] - Y), Z) / 5.0, 0, 1)        # okraje rovne (dosedaji na zdi a cela)
    d = d.reshape(X.shape) * fade; hole = hole.reshape(X.shape) & (fade > 0.6)
    NX = np.repeat(nx[:, None], n_v + 1, 1); NZ = np.repeat(nz[:, None], n_v + 1, 1)
    A = np.stack([X + NX * d, Y, Z + NZ * d], -1)
    arc = np.concatenate([[0], np.cumsum(np.hypot(np.diff(px), np.diff(pz)))]) / 100
    M = _M()
    i0 = M.verts(A, np.stack(np.meshgrid(arc, (ys - ys[0]) / 100, indexing="ij"), -1), 0)
    M.quad_grid(i0, n_u, n_v, lambda a, b: WATTLE if (hole[a, b] and hole[a + 1, b] and hole[a, b + 1] and hole[a + 1, b + 1]) else DAUB)
    for j, g in ((0, 2), (n_v, 3)):                                     # cela: od oblouku dolu na zakladnu
        top = A[:, j]; base = np.stack([px, np.full(n_u + 1, ys[j]), np.zeros(n_u + 1)], 1)
        R = np.stack([top, base], 1)
        uv = np.stack([np.stack([px / 100 + 1, top[:, 2] / 100], 1), np.stack([px / 100 + 1, np.zeros(n_u + 1)], 1)], 1)
        i0 = M.verts(R, uv, g)
        M.quad_grid(i0, n_u, 1, lambda a, b: DAUB)
    return M


def _orient_convex(P, F):
    """vypukle teleso: normaly ploch ven od stredu"""
    c0 = (P.min(0) + P.max(0)) / 2; c0[2] = P[:, 2].min()
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); c = P[F].mean(1) - c0
    F = F.copy(); flip = (fn * c).sum(1) < 0; F[flip] = F[flip][:, ::-1]
    return F


def _orient(P, F, G, outward_groups):
    """otoci plochy tak, aby normaly vnejsi plochy smerovaly od osy Z, vnitrni k ose (okraje nechava)"""
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); c = P[F].mean(1)
    g = G[F[:, 0]]
    radial = (fn[:, :2] * c[:, :2]).sum(1)
    flip = np.zeros(len(F), bool)
    flip |= (g == 0) & (radial < 0); flip |= (g == 1) & (radial > 0)
    F = F.copy(); F[flip] = F[flip][:, ::-1]
    return F


def _orient_panel(P, F, G):
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); c = P[F].mean(1); g = G[F[:, 0]]
    flip = ((g == 0) & (fn[:, 1] < 0)) | ((g == 1) & (fn[:, 1] > 0)) | ((g == 2) & ((fn[:, [0, 2]] * c[:, [0, 2]]).sum(1) < 0))
    F = F.copy(); F[flip] = F[flip][:, ::-1]
    return F


def _orient_tube(P, F, G, H):
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); g = G[F[:, 0]]
    F = _orient(P, F, G, (0,))
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    flip = ((g == 2) & (fn[:, 2] > 0)) | ((g == 3) & (fn[:, 2] < 0))
    F[flip] = F[flip][:, ::-1]
    return F


def _write(out, name, P, UV, G, F, S, desc, made):
    nom = NOMINAL[name.rsplit("_", 1)[0]]
    mn, mx = P.min(0), P.max(0)
    P = (P - (mn + mx) / 2) / (mx - mn) * np.array(nom)
    write_obj_slots(os.path.join(out, name + ".obj"), P, UV, smooth_normals(P, F, G), F, S, name, desc, SLOTS)
    made.append((name, len(P), len(F)))


def build(out):
    """prouti a mazanina do slozky out -> seznam (jmeno, vrcholu, trojuhelniku)"""
    made = []
    for vi, v in enumerate("ABC"):
        P, UV, G, F, S = make_panel(18000 + vi * 67).arrays()
        _write(out, "SM_RuinWattlePanel_" + v, P, UV, G, _orient_panel(P, F, G), S, "dilec proutene steny s mazaninou", made)
    for vi, v in enumerate("AB"):
        P, UV, G, F, S = make_tube(18500 + vi * 71, 140, 120, 50, 50, 100, 5.0).arrays()
        _write(out, "SM_RuinSmokeHood_" + v, P, UV, G, _orient_tube(P, F, G, 100), S, "dymnik z prouti a hliny", made)
        P, UV, G, F, S = make_tube(19000 + vi * 73, 60, 60, 54, 54, 100, 6.0, n_per=40, n_h=20, round_r=5.0).arrays()
        _write(out, "SM_RuinChimney_" + v, P, UV, G, _orient_tube(P, F, G, 100), S, "komin z prouti a hliny", made)
        P, UV, G, F, S = make_dome(19500 + vi * 79).arrays()
        _write(out, "SM_RuinOvenDome_" + v, P, UV, G, _orient_convex(P, F), S, "hlinena klenba pece", made)
    return made
