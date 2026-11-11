"""gen_stones.py - zaoblene, lehce zvetrale kameny pro build_ruin_blocks.py (OBJ, cm, Z nahoru).

python gen_stones.py <vystupni slozka>     (potrebuje numpy)

Lomovy kamen: kvadr se zaoblenymi hranami (radius ~3.5 cm), mirne vypoukle (polstarovite) plochy,
nizkofrekvencni nerovnosti a vylamane / zvetrale hrany. Rozmery: delka 30*r cm (r = pomer delka/vyska),
hloubka 45 cm, vyska 30 cm, pivot ve stredu. Skript ve hre kamen naskaluje na presny rozmer bloku.
UV v metrech (1 UV = 1 m) -> textura ma stejne meritko na vsech kamenech.
Zvetrale kameny koruny: SM_RuinStone_W_* - zvetrale hlavne shora (horni hrany zaobleni 8.5-10.5 cm, otluceni,
dulky na vrsku), spodek ostrejsi (3 cm), protoze lezi na kameni pod nim.
Opracovane kameny osteni, nadprazi a strilen: SM_RuinDressed_R12..R34_A/B (zaobleni 2.4-3.7 cm, mirne otlucene).
Kvadr (SM_RuinAshlar): 100x100x100 cm, jen lehce srazene hrany - dlazba.
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


def grid_sin(n):
    u = np.linspace(-1, 1, n + 1)
    return np.sin(u * math.pi / 2)                                  # hustsi u hran (zaobleni)


def grid(e_, b_lo, b_hi, R_face, step, n_band=7):
    """souradnice -e..e podel jedne osy plochy: rovna cast rovnomerne, pasy zaobleni (b_lo / b_hi) po stejnych uhlech
    (bod v pasu ve vzdalenosti t od vnitrniho kvadru ma po zaobleni uhel atan(t / R_face) od normaly plochy)"""
    a, b = -e_ + b_lo, e_ - b_hi
    nf = max(2, int(round((b - a) / step)))
    flat = np.linspace(a, b, nf + 1)
    def band(bw):
        tm = math.atan(bw / R_face); k = max(2, int(round(n_band * tm / (math.pi / 2))))
        return R_face * np.tan(np.linspace(0, tm, k + 1)[1:])
    return np.concatenate([a - band(b_lo)[::-1], flat, b + band(b_hi)])


def make_stone(L, Dp, Hh, radius, seed, amp=0.9, edge=1.6, bulge=0.6, step=4.0, r_top=None, r_bot=None, top_wear=0.0):
    """r_top / r_bot: jine zaobleni horni a spodni casti (zvetrani shora); top_wear: navic obrouseni a otluceni shora,
    spodek (lezi na kameni pod nim) zustava ostrejsi"""
    e = np.array([L / 2, Dp / 2, Hh / 2])
    two = r_top is not None or r_bot is not None        # zvetrale (jine zaobleni nahore / dole) -> sit podle uhlu, mirne otluceni
    r_top = radius if r_top is None else r_top; r_bot = radius if r_bot is None else r_bot
    inner_hi = e - np.array([radius, radius, r_top]); inner_lo = e - np.array([radius, radius, r_bot])
    W1 = waves(seed, 10, 9, 30); W2 = waves(seed + 99, 14, 3, 8); W3 = waves(seed + 7, 4, 25, 60)
    verts, uvs, faces = [], [], []
    for ax in range(3):
        for sg in (-1, 1):
            a1, a2 = [i for i in range(3) if i != ax]
            if sg < 0: a1, a2 = a2, a1                               # spravna orientace (normala ven)
            Rf = (r_top if sg > 0 else r_bot) if ax == 2 else radius          # polomer zaobleni smerem od teto plochy
            def gr(a_):
                lo, hi = (r_bot, r_top) if a_ == 2 else (radius, radius)
                return grid(e[a_], lo, hi, Rf, step)
            if two:
                g1, g2 = gr(a1), gr(a2)
            else:                                        # bezne kameny: puvodni sit (stejne meshe jako drive)
                g1 = grid_sin(max(4, int(round(2 * e[a1] / step)))) * e[a1]; g2 = grid_sin(max(4, int(round(2 * e[a2] / step)))) * e[a2]
            n1, n2 = len(g1) - 1, len(g2) - 1
            U, V = np.meshgrid(g1, g2, indexing="ij")
            p = np.zeros(U.shape + (3,)); p[..., ax] = sg * e[ax]; p[..., a1] = U; p[..., a2] = V
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
    q = np.clip(P, -inner_lo, inner_hi)
    d = P - q; dn = np.linalg.norm(d, axis=1, keepdims=True); dn[dn == 0] = 1
    nrm = d / dn
    # elipticke zaobleni: do stran polomer radius, nahoru r_top, dolu r_bot (plynule, bez schodu na hrane)
    Rv = np.stack([np.full(len(P), radius), np.full(len(P), radius), np.where(nrm[:, 2] >= 0, r_top, r_bot)], 1)
    P2 = q + nrm * Rv
    inner = (inner_hi + inner_lo) / 2
    # polstar: plocha mirne vypoukla do stredu
    rel = np.abs(q) / np.maximum(inner, 1e-6)
    pill = np.zeros(len(P))
    for ax in range(3):
        o = [i for i in range(3) if i != ax]
        on = np.abs(nrm[:, ax]) > 0.7
        pill = np.where(on, (1 - rel[:, o[0]] ** 2) * (1 - rel[:, o[1]] ** 2), pill)
    # hranovost: 1 na hranach a rozich (normala neni osova), 0 uprostred ploch. Kvadraticky nabeh (nulovy sklon na plose),
    # jinak otluceni hran vyrobi u velkeho horniho zaobleni schod / obrubu
    if two:
        edginess = np.clip((1 - np.max(np.abs(nrm), axis=1)) / 0.29, 0, 1) ** 2
    else:
        edginess = np.clip((1 - np.max(np.abs(nrm), axis=1)) * 3.0, 0, 1)
    nz = nrm[:, 2]
    topw = np.clip(nz, 0, 1); botw = np.clip(-nz, 0, 1)
    wear = 1 + top_wear * topw - 0.6 * (top_wear > 0) * botw          # shora vic, zespodu min
    disp = bulge * pill + amp * wear * (noise(P2, W1) + 0.35 * noise(P2, W2)) + 0.6 * amp * noise(P2, W3)
    chip = np.clip(noise(P2, W2) * 0.5 + 0.5, 0, 1) ** 1.5
    ero = (edge * edginess * (0.4 + chip) + 0.8 * edge * np.clip(noise(P2, W1), 0, 1) * edginess) * wear
    # hloubka otluceni max. ~30 % mistniho polomeru zaobleni (plynule), aby hrana nepropadla pod plochu
    Rloc = radius + (Rv[:, 2] - radius) * nz ** 2
    cap = 0.3 * Rloc
    disp -= ero * cap / (cap + ero + 1e-6) if two else ero
    disp -= top_wear * 0.8 * topw ** 4 * np.clip(noise(P2, W2) * 0.5 + 0.5, 0, 1) ** 2          # dulky a stopy po vode na vrsku
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
    # zvetrale kameny koruny zdi: vetsi zaobleni, hlubsi otluceni hran, nerovnejsi plochy
    for ri, r in enumerate(RATIOS):
        for vi, v in enumerate(VARIANTS):
            name = "SM_RuinStone_W_R%02d_%s" % (round(r * 10), v)
            P, UV, N, F = make_stone(H * r, D, H, radius=4.5 + vi * 0.5, seed=5000 + ri * 23 + vi * 197,
                                     amp=1.2, edge=2.4, bulge=0.25, step=3.5,
                                     r_top=8.5 + vi * 1.0, r_bot=3.0, top_wear=1.2)
            write_obj(os.path.join(out, name + ".obj"), P, UV, N, F, name)
            made.append((name, len(P), len(F)))
    # opracovane kameny osteni a strilen: rovnejsi plochy, mensi otluceni, ale ne ostre hrany (zvetrale)
    for ri, r in enumerate(RATIOS):
        for vi, v in enumerate("AB"):
            name = "SM_RuinDressed_R%02d_%s" % (round(r * 10), v)
            P, UV, N, F = make_stone(H * r, D, H, radius=2.4 + vi * 0.5, seed=7000 + ri * 29 + vi * 151,
                                     amp=0.35, edge=1.1, bulge=0.12, step=4.0, r_top=3.2 + vi * 0.5, r_bot=2.0, top_wear=0.4)
            write_obj(os.path.join(out, name + ".obj"), P, UV, N, F, name)
            made.append((name, len(P), len(F)))
    P, UV, N, F = make_stone(100, 100, 100, radius=2.0, seed=5, amp=0.25, edge=0.5, bulge=0.15, step=10)
    write_obj(os.path.join(out, "SM_RuinAshlar.obj"), P, UV, N, F, "SM_RuinAshlar"); made.append(("SM_RuinAshlar", len(P), len(F)))
    for m in made: print("%-24s vrcholu %5d  trojuhelniku %5d" % m)
    return made


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "stones")
