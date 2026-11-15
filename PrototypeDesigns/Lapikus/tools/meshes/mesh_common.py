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


def obj_v(p):
    """bod / normala UE (x, y, z) -> OBJ. Import OBJ do UE (Interchange, overeno tools/checks/UE_Osy_OBJ.py 15. 11. 2026)
    bere osy tak, jak jsou, jen otoci znamenko Y: UE = (X, -Y, Z) z OBJ, a protoze tim mesh zrcadli, otoci i poradi
    vrcholu trojuhelniku. Zapis proto Y otoci predem (obj_v) a trojuhelniky zapise obracene (obj_f): v OBJ je pak
    lice proti smeru hodin jako v norme OBJ a v UE vyjde presne mesh generatoru (osy i lice)."""
    return (p[0], -p[1], p[2])


def obj_f(a, b, c):
    """trojuhelnik (indexy od 1) do OBJ: obracene poradi k zrcadleni v obj_v (viz tam)"""
    return "f %d/%d/%d %d/%d/%d %d/%d/%d\n" % (a, a, a, c, c, c, b, b, b)


def _write_vtn(f, P, UV, N):
    for p in P: f.write("v %.4f %.4f %.4f\n" % obj_v(p))       # 0,1 mm (od MESH_AXES 5; jina data = novy klic DDC v UE)
    for t in UV: f.write("vt %.4f %.4f\n" % (t[0], t[1]))
    for n in N: f.write("vn %.4f %.4f %.4f\n" % obj_v(n))


def write_obj(path, P, UV, N, F, name, desc="zaobleny zvetraly kamen"):
    """zapis OBJ v osach UE (cm, Z nahoru). desc = popis v hlavicce. Prevod os viz obj_v."""
    with open(path, "w") as f:
        f.write("# %s - %s (cm, Z nahoru)\no %s\n" % (name, desc, name))
        _write_vtn(f, P, UV, N)
        for a, b, c in F + 1: f.write(obj_f(a, b, c))


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
        _write_vtn(f, P, UV, N)
        for si, sn in enumerate(names):
            sel = F[slot == si]
            if not len(sel): continue
            f.write("usemtl %s\n" % sn)
            for a, b, c in sel + 1: f.write(obj_f(a, b, c))
