"""mesh_bark - pasy kury na strechy (OBJ, cm, Z nahoru). Kategorie wood (vola mesh_wood.build).

SM_RuinBarkStrip_A..C: pas smrkove kury 160 x 70 cm, tloustka 1,5 cm, prohnuty do oblouku (vrch kmene nahoru),
roztrepene okraje. Delka podel X (= po spadu strechy), sirka Y. Sloty: Bark (vrch a okraje), EndGrain (spodek = lyko,
svetle; material cel). Klade se hrubou stranou nahoru s presahem 0,2 m.
"""
import math, os
import numpy as np

from mesh_common import waves, noise, smooth_normals, write_obj_slots

NOMINAL = {"SM_RuinBarkStrip": (160.0, 70.0, 9.0)}
SLOTS = ("Bark", "EndGrain")


def make_strip(seed, L=160.0, Wd=70.0, T=1.5, arch=6.0, nx=40, ny=18):
    rng = np.random.default_rng(seed)
    W1 = waves(seed + 1, 8, 20, 60); Wf = waves(seed + 2, 12, 2.0, 5.0); We = waves(seed + 3, 8, 3, 12)
    s = np.linspace(0, 1, nx + 1); t = np.linspace(-1, 1, ny + 1)
    S, Tt = np.meshgrid(s, t, indexing="ij")
    # obrys: roztrepene konce a okraje
    xa = -L / 2 + 4.0 * noise(np.stack([np.zeros_like(t), t * 40, np.zeros_like(t)], 1), We)
    xb = L / 2 + 4.0 * noise(np.stack([np.full_like(t, 50.0), t * 40, np.zeros_like(t)], 1), We)
    X = xa[None, :] * (1 - S) + xb[None, :] * S
    hw = Wd / 2 * (1 + 0.10 * noise(np.stack([s * L, np.zeros_like(s), np.zeros_like(s)], 1), W1)) \
        + 1.5 * noise(np.stack([s * L, np.full_like(s, 30.0), np.zeros_like(s)], 1), We)
    Y = Tt * hw[:, None]
    q = np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], 1)
    ridge = (1 - np.abs(noise(q * np.array([0.12, 1, 1]), Wf))) ** 4
    Z = arch * (1 - Tt ** 2) + (0.6 * noise(q, W1)).reshape(X.shape) - 0.35 * ridge.reshape(X.shape)
    Z += rng.uniform(-1, 1) * 2.0 * (S - 0.5) ** 2                  # mirne zkrouceni
    top = np.stack([X, Y, Z], -1)
    bot = top.copy(); bot[..., 2] -= T + 0.2 * (1 - np.abs(Tt))
    P = []; UV = []; G = []; F = []; SL = []
    def add(A, uv, g):
        P.append(A.reshape(-1, 3)); UV.append(uv.reshape(-1, 2)); G.append(np.full(A.shape[0] * A.shape[1], g))
        return sum(len(p) for p in P[:-1])
    i0 = add(top, np.stack([X / 100, Y / 100], -1), 0)
    i1 = add(bot, np.stack([X / 100, Y / 100], -1), 1)
    def grid(i, flip, sl):
        for a in range(nx):
            for b in range(ny):
                v00 = i + a * (ny + 1) + b; v10 = v00 + ny + 1; v01 = v00 + 1; v11 = v10 + 1
                f1, f2 = (v00, v10, v11), (v00, v11, v01)
                if flip: f1, f2 = f1[::-1], f2[::-1]
                F.extend([f1, f2]); SL.extend([sl, sl])
    grid(i0, False, 0); grid(i1, True, 1)
    # okraj: obvodova smycka gridu (top -> bot)
    loop = [(a, 0) for a in range(nx)] + [(nx, b) for b in range(ny)] + [(a, ny) for a in range(nx, 0, -1)] + [(0, b) for b in range(ny, 0, -1)]
    tp = np.array([top[a, b] for a, b in loop]); bp = np.array([bot[a, b] for a, b in loop])
    per = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(np.vstack([tp, tp[:1]]), axis=0), axis=1))])[:-1] / 100
    n = len(loop)
    i2 = add(tp[None], np.stack([per, np.zeros(n)], -1)[None], 2); i3 = add(bp[None], np.stack([per, np.full(n, 0.015)], -1)[None], 2)
    for k in range(n):
        k1 = (k + 1) % n
        F.extend([(i2 + k, i3 + k, i3 + k1), (i2 + k, i3 + k1, i2 + k1)]); SL.extend([0, 0])
    P = np.concatenate(P); UV = np.concatenate(UV); G = np.concatenate(G); F = np.array(F); SL = np.array(SL)
    # orientace: vrch nahoru, spodek dolu, okraj ven
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); c = P[F].mean(1)
    want = np.where(G[F[:, 0]] == 0, 1.0, np.where(G[F[:, 0]] == 1, -1.0, 0.0))
    flip = np.where(want != 0, fn[:, 2] * want < 0, (fn[:, :2] * c[:, :2]).sum(1) < 0)
    F[flip] = F[flip][:, ::-1]
    return P, UV, G, F, SL


def build(out):
    made = []
    for vi, v in enumerate("ABC"):
        P, UV, G, F, SL = make_strip(17000 + vi * 61)
        mn, mx = P.min(0), P.max(0)
        P = (P - (mn + mx) / 2) / (mx - mn) * np.array(NOMINAL["SM_RuinBarkStrip"])
        name = "SM_RuinBarkStrip_" + v
        write_obj_slots(os.path.join(out, name + ".obj"), P, UV, smooth_normals(P, F, G), F, SL, name, "pas kury", SLOTS)
        made.append((name, len(P), len(F)))
    return made
