"""check_normals.py - kontrola orientace normal v OBJ (bez Unrealu): z nahodnych ploch se vysle paprsek po normale
a spocita se, kolikrat protne povrch. Lichy pocet = normala miri dovnitr telesa (v UE pak je videt vnitrni strana).

    python tools/checks/check_normals.py <slozka s OBJ nebo meshes/> [prefix ...] [--limit 0.1] [--samples 300]

Vypise podil "dovnitr" na mesh a po materialovem slotu. U otevrenych ploch (platno, lem) je kontrola jen orientacni.
Navratovy kod 1, kdyz nejaky mesh presahne limit.
"""
import os, sys
import numpy as np


def load(path):
    V, F, S = [], [], []; cur = None
    for ln in open(path):
        if ln.startswith("v "): x, y, z = map(float, ln.split()[1:4]); V.append((x, -y, z))      # OBJ -> osy UE (mesh_common.obj_v)
        elif ln.startswith("usemtl"): cur = ln.split()[1]
        elif ln.startswith("f "): F.append([int(t.split("/")[0]) - 1 for t in ln.split()[1:4]][::-1]); S.append(cur)   # trojuhelnik obracene (mesh_common.obj_f)
    return np.array(V), np.array(F), np.array(S, dtype=object)


def ray_hits(o, d, A, B, C, eps=1e-6):
    """pocet pruseciku paprsku o + t d (t > 0) s trojuhelniky (Moller-Trumbore, vektorove)"""
    e1 = B - A; e2 = C - A; p = np.cross(d, e2); det = e1 @ d if False else (e1 * p).sum(1)
    ok = np.abs(det) > eps; inv = np.where(ok, 1.0 / np.where(ok, det, 1), 0)
    s = o - A; u = (s * p).sum(1) * inv; q = np.cross(s, e1); v = (q @ d) * inv; t = (e2 * q).sum(1) * inv
    return int((ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-4)).sum())


def check(path, samples=300, seed=0):
    V, F, S = load(path)
    A, B, C = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    n = np.cross(B - A, C - A); ln = np.linalg.norm(n, axis=1); good = ln > 1e-8
    rng = np.random.default_rng(seed); idx = np.flatnonzero(good)
    idx = rng.choice(idx, min(samples, len(idx)), replace=False)
    bad = {}; tot = {}
    for k in idx:
        c = (A[k] + B[k] + C[k]) / 3; d = n[k] / ln[k]
        d = d + rng.normal(0, 1e-3, 3); d /= np.linalg.norm(d)            # mimo hrany
        h = ray_hits(c + d * 1e-3, d, A, B, C)
        tot[S[k]] = tot.get(S[k], 0) + 1
        if h % 2: bad[S[k]] = bad.get(S[k], 0) + 1
    return sum(bad.values()) / max(len(idx), 1), {s: (bad.get(s, 0), t) for s, t in tot.items()}


def main(argv):
    lim = 0.1; samples = 300; args = []
    it = iter(argv)
    for a in it:
        if a == "--limit": lim = float(next(it))
        elif a == "--samples": samples = int(next(it))
        else: args.append(a)
    src, prefixes = args[0], args[1:]
    files = []
    for root, _, fs in os.walk(src):
        files += [os.path.join(root, f) for f in fs if f.endswith(".obj") and (not prefixes or any(f.startswith(p) for p in prefixes))]
    worst = 0.0
    for f in sorted(files, key=os.path.basename):
        frac, per = check(f, samples)
        worst = max(worst, frac)
        flag = "  <-- NORMALY DOVNITR" if frac > lim else ""
        detail = ", ".join("%s %d/%d" % (s, b, t) for s, (b, t) in sorted(per.items(), key=lambda x: str(x[0])) if b)
        print("%-28s dovnitr %5.1f %%%s%s" % (os.path.basename(f)[:-4], 100 * frac, flag, ("  (" + detail + ")") if detail else ""))
    return 1 if worst > lim else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
