"""mesh_common - spolecne funkce generatoru meshi (tools/meshes): sum, rozlozeni site, zapis OBJ.

Jednotky cm, Z nahoru, UV v metrech (1 UV = 1 m). Presunuto z 03_ruin/blocks/gen_stones.py beze zmeny vypoctu
(vystupni OBJ musi zustat bit po bitu stejne, kontrola md5).
"""
import math
import numpy as np


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


def write_obj(path, P, UV, N, F, name, desc="zaobleny zvetraly kamen"):
    """zapis OBJ (UE souradnice cm, Z nahoru -> OBJ Y-up). desc = popis v hlavicce; kameny a hranene drevo
    pouzivaji puvodni text, aby se stavajici OBJ nezmenily (STONE_MESH_VERSION by je jinak nemusel prenacist)."""
    with open(path, "w") as f:
        f.write("# %s - %s (cm, Z nahoru)\no %s\n" % (name, desc, name))
        # OBJ je Y-up: UE (x, y, z) -> OBJ (x, z, -y); skript stejne kontroluje osy podle bounding boxu
        for p in P: f.write("v %.3f %.3f %.3f\n" % (p[0], p[2], -p[1]))
        for t in UV: f.write("vt %.4f %.4f\n" % (t[0], t[1]))
        for n in N: f.write("vn %.4f %.4f %.4f\n" % (n[0], n[2], -n[1]))
        for a, b, c in F + 1: f.write("f %d/%d/%d %d/%d/%d %d/%d/%d\n" % (a, a, a, b, b, b, c, c, c))


# ------------------------------------------------------------------ vice materialovych slotu (kulatina: drevo, cela, kura)
SLOT_ORDER = ("Wood", "EndGrain", "Bark")      # poradi slotu v OBJ (usemtl); UE je pak mapuje podle jmena, jinak podle poradi


def smooth_normals(P, F, group):
    """normaly vrcholu: prumer normal ploch, svarene podle polohy jen uvnitr skupiny (group[v]) -> ostra hrana mezi skupinami"""
    key = np.concatenate([np.round(P, 3), group[:, None].astype(float)], 1)
    _, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel()
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    acc = np.zeros((inv.max() + 1, 3))
    for c in range(3): np.add.at(acc, inv[F[:, c]], fn)
    N = acc[inv]
    return N / (np.linalg.norm(N, axis=1, keepdims=True) + 1e-12)


def write_obj_slots(path, P, UV, N, F, slot, name, desc, names=SLOT_ORDER):
    """OBJ s materialovymi sloty: slot[f] = index do names (vychozi SLOT_ORDER kulatiny); plochy serazene podle slotu,
    kazda skupina 'usemtl <jmeno>'. Jmena slotu mapuje UE na materialy (SLOT_MI v zrlib/config.py)."""
    with open(path, "w") as f:
        f.write("# %s - %s (cm, Z nahoru)\no %s\n" % (name, desc, name))
        for p in P: f.write("v %.3f %.3f %.3f\n" % (p[0], p[2], -p[1]))
        for t in UV: f.write("vt %.4f %.4f\n" % (t[0], t[1]))
        for n in N: f.write("vn %.4f %.4f %.4f\n" % (n[0], n[2], -n[1]))
        for si, sn in enumerate(names):
            sel = F[slot == si]
            if not len(sel): continue
            f.write("usemtl %s\n" % sn)
            for a, b, c in sel + 1: f.write("f %d/%d/%d %d/%d/%d %d/%d/%d\n" % (a, a, a, b, b, b, c, c, c))
