"""gen_stones.py - zaoblene, lehce zvetrale kameny pro build_ruin_blocks.py (OBJ, cm, Z nahoru).

python gen_stones.py <vystupni slozka>     (potrebuje numpy)

Lomovy kamen: kvadr se zaoblenymi hranami (radius ~3.5 cm), mirne vypoukle (polstarovite) plochy,
nizkofrekvencni nerovnosti a vylamane / zvetrale hrany. Rozmery: delka 30*r cm (r = pomer delka/vyska),
hloubka 45 cm, vyska 30 cm, pivot ve stredu. Skript ve hre kamen naskaluje na presny rozmer bloku.
UV v metrech (1 UV = 1 m) -> textura ma stejne meritko na vsech kamenech.
Kvadr osteni (SM_RuinAshlar): 100x100x100 cm, jen lehce srazene hrany (opracovany kamen).
"""
import math, os, sys
import numpy as np

RATIOS = [1.2, 1.8, 2.6, 3.4]     # musi odpovidat STONE_RATIOS v build_ruin_blocks.py
VARIANTS = "ABC"
H, D = 30.0, 45.0


def waves(seed, n, lmin, lmax):
    r = np.random.default_rng(seed)
    k = r.normal(size=(n, 3)); k /= np.linalg.norm(k, axis=1, keepdims=True)
    lam = r.uniform(lmin, lmax, n)
    return k * (2 * math.pi / lam)[:, None], r.uniform(0, 2 * math.pi, n), r.uniform(0.5, 1.0, n)


def noise(p, w):
    k, ph, a = w
    return (np.sin(p @ k.T + ph) * a).sum(1) / a.sum() * 1.6      # ~ -1..1


def grid(n):
    u = np.linspace(-1, 1, n + 1)
    return np.sin(u * math.pi / 2)                                  # hustsi u hran (zaobleni)


def make_stone(L, Dp, Hh, radius, seed, amp=0.9, edge=1.6, bulge=0.6, step=4.0):
    e = np.array([L / 2, Dp / 2, Hh / 2])
    inner = e - radius
    W1 = waves(seed, 10, 9, 30); W2 = waves(seed + 99, 14, 3, 8); W3 = waves(seed + 7, 4, 25, 60)
    verts, uvs, faces = [], [], []
    for ax in range(3):
        for sg in (-1, 1):
            a1, a2 = [i for i in range(3) if i != ax]
            if sg < 0: a1, a2 = a2, a1                               # spravna orientace (normala ven)
            n1 = max(4, int(round(2 * e[a1] / step))); n2 = max(4, int(round(2 * e[a2] / step)))
            g1, g2 = grid(n1), grid(n2)
            U, V = np.meshgrid(g1, g2, indexing="ij")
            p = np.zeros(U.shape + (3,)); p[..., ax] = sg * e[ax]; p[..., a1] = U * e[a1]; p[..., a2] = V * e[a2]
            verts.append(p.reshape(-1, 3))
            uv = np.stack([p[..., a1], p[..., a2]], -1).reshape(-1, 2) / 100.0
            uvs.append(uv)
            idx = np.arange((n1 + 1) * (n2 + 1)).reshape(n1 + 1, n2 + 1)
            q00 = idx[:-1, :-1].ravel(); q10 = idx[1:, :-1].ravel(); q11 = idx[1:, 1:].ravel(); q01 = idx[:-1, 1:].ravel()
            faces.append(np.stack([np.stack([q00, q10, q11], 1), np.stack([q00, q11, q01], 1)], 1).reshape(-1, 3))
    # sloucit indexy
    off = 0; F = []
    for v, f in zip(verts, faces):
        F.append(f + off); off += len(v)
    P = np.concatenate(verts); UV = np.concatenate(uvs); F = np.concatenate(F)
    # orientace trojuhelniku ven (konvexni zaklad -> normala musi mirit od stredu)
    fn0 = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    flip = (fn0 * P[F].mean(1)).sum(1) < 0
    F[flip] = F[flip][:, ::-1]
    # zaobleni: bod na kvadru -> nejblizsi bod vnitrniho kvadru + radius * smer
    q = np.clip(P, -inner, inner)
    d = P - q; dn = np.linalg.norm(d, axis=1, keepdims=True); dn[dn == 0] = 1
    nrm = d / dn
    P2 = q + nrm * radius
    # polstar: plocha mirne vypoukla do stredu
    rel = np.abs(q) / np.maximum(inner, 1e-6)
    pill = np.zeros(len(P))
    for ax in range(3):
        o = [i for i in range(3) if i != ax]
        on = np.abs(nrm[:, ax]) > 0.7
        pill = np.where(on, (1 - rel[:, o[0]] ** 2) * (1 - rel[:, o[1]] ** 2), pill)
    # hranovost: 1 na hranach a rozich (normala neni osova), 0 uprostred ploch
    edginess = 1 - np.max(np.abs(nrm), axis=1)
    edginess = np.clip(edginess * 3.0, 0, 1)
    disp = bulge * pill + amp * noise(P2, W1) + 0.35 * amp * noise(P2, W2) + 0.6 * amp * noise(P2, W3)
    chip = np.clip(noise(P2, W2) * 0.5 + 0.5, 0, 1) ** 1.5
    disp -= edge * edginess * (0.4 + chip) + 0.8 * edge * np.clip(noise(P2, W1), 0, 1) * edginess
    P3 = P2 + nrm * disp[:, None]
    # zpet na presne rozmery (bounding box = jmenovity rozmer)
    mn, mx = P3.min(0), P3.max(0)
    P3 = (P3 - (mn + mx) / 2) / (mx - mn) * (2 * e)
    # normaly (svarene podle polohy -> hladke pres svy ploch)
    key = np.round(P3, 3)
    _, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel()
    fn = np.cross(P3[F[:, 1]] - P3[F[:, 0]], P3[F[:, 2]] - P3[F[:, 0]])
    acc = np.zeros((inv.max() + 1, 3))
    for c in range(3): np.add.at(acc, inv[F[:, c]], fn)
    N = acc[inv]; N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
    return P3, UV, N, F


def write_obj(path, P, UV, N, F, name):
    with open(path, "w") as f:
        f.write("# %s - zaobleny zvetraly kamen (cm, Z nahoru)\no %s\n" % (name, name))
        # OBJ je Y-up: UE (x, y, z) -> OBJ (x, z, -y); skript stejne kontroluje osy podle bounding boxu
        for p in P: f.write("v %.3f %.3f %.3f\n" % (p[0], p[2], -p[1]))
        for t in UV: f.write("vt %.4f %.4f\n" % (t[0], t[1]))
        for n in N: f.write("vn %.4f %.4f %.4f\n" % (n[0], n[2], -n[1]))
        for a, b, c in F + 1: f.write("f %d/%d/%d %d/%d/%d %d/%d/%d\n" % (a, a, a, b, b, b, c, c, c))


def main(out):
    os.makedirs(out, exist_ok=True)
    made = []
    for ri, r in enumerate(RATIOS):
        for vi, v in enumerate(VARIANTS):
            name = "SM_RuinStone_R%02d_%s" % (round(r * 10), v)
            P, UV, N, F = make_stone(H * r, D, H, radius=3.5 + vi * 0.6, seed=1000 + ri * 17 + vi * 131)
            write_obj(os.path.join(out, name + ".obj"), P, UV, N, F, name)
            made.append((name, len(P), len(F)))
    P, UV, N, F = make_stone(100, 100, 100, radius=2.0, seed=5, amp=0.25, edge=0.5, bulge=0.15, step=10)
    write_obj(os.path.join(out, "SM_RuinAshlar.obj"), P, UV, N, F, "SM_RuinAshlar"); made.append(("SM_RuinAshlar", len(P), len(F)))
    for m in made: print("%-24s vrcholu %5d  trojuhelniku %5d" % m)
    return made


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "stones")
