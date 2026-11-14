"""mesh_wood - drevo (OBJ, cm, Z nahoru). Kulatina je v mesh_log.py (stejna kategorie wood).

Hranene drevo: SM_RuinTimber_A..C (tram 100x25x25), SM_RuinPost_A..C (sloup, delka nahoru), SM_RuinPlank_A..C
(prkno 100x25x5): vysusene, podelne praskliny, ohlazene hrany, lehky prohyb; prkna miskovite prohnuta.
Vlakna dela normalova mapa materialu. Skript ve hre kus naskaluje na presny rozmer (WOOD_NOMINAL v zrlib/config.py).
"""
import math, os
import numpy as np

from mesh_common import write_obj
import mesh_log


def _rrect(w, h, r, n):
    """obvod obdelniku w x h se zaoblenymi rohy r: n bodu rovnomerne po obvodu -> (body (n,2), normaly (n,2), t 0..1, vzdalenost k rohu)"""
    segs = []
    hw, hh = w / 2 - r, h / 2 - r
    # useky: rovne strany a ctvrtkruhy, proti smeru hodin od (+w/2, -hh)
    L_side = [2 * hh, 2 * hw, 2 * hh, 2 * hw]; L_arc = math.pi / 2 * r
    total = sum(L_side) + 4 * L_arc
    s = np.linspace(0, total, n, endpoint=False)
    P = np.zeros((n, 2)); N = np.zeros((n, 2)); dc = np.zeros(n)
    centers = [(hw, hh), (-hw, hh), (-hw, -hh), (hw, -hh)]
    for i, si in enumerate(s):
        acc = 0.0
        for k in range(4):
            ls = L_side[k]
            if si < acc + ls:
                f = si - acc
                if k == 0: p = (w / 2, -hh + f); nn = (1, 0)
                elif k == 1: p = (hw - f, h / 2); nn = (0, 1)
                elif k == 2: p = (-w / 2, hh - f); nn = (-1, 0)
                else: p = (-hw + f, -h / 2); nn = (0, -1)
                P[i] = p; N[i] = nn; dc[i] = min(f, ls - f) + 0.0
                break
            acc += ls
            if si < acc + L_arc:
                a = (si - acc) / r + k * math.pi / 2
                c = centers[k]; nn = (math.cos(a), math.sin(a))
                P[i] = (c[0] + r * nn[0], c[1] + r * nn[1]); N[i] = nn; dc[i] = 0.0
                break
            acc += L_arc
    return P, N, s / total, dc


def make_timber(L, W, Hh, seed, n_ring=80, n_len=16, r=1.6, cracks=(3, 5), crack_d=(1.2, 3.0), grain=0.0,
                wane=2.2, bow=0.5, plank=False, crack_w=(0.9, 1.6)):
    """zasly tram / prkno: vysusene od slunce, podelne praskliny, otluceni / ohlazene hrany, mekka promacknuti,
    lehky prohyb a zkrut. Delka podel X, prurez W (Y) x Hh (Z), cm.
    Letokruhy / vlakna nejsou v geometrii (grain=0) - dela je normalova mapa materialu; sit je hruba (~2-3 tis. trojuhelniku)."""
    rng = np.random.default_rng(seed)
    P0, N0, T, dc = _rrect(W, Hh, r, n_ring)
    xs = np.linspace(-L / 2, L / 2, n_len + 1)
    # leto: rady vlaken napric (vlnky), jejich poloha se podel delky pomalu meni
    nr = 22 if not plank else 18
    ph = rng.uniform(0, 2 * math.pi, 3); fr = rng.uniform(0.8, 1.6, 3)
    per = W * 2 + Hh * 2
    def grain_f(t, x):
        u = t * per
        g = 0.0
        for k in range(3):
            g = g + np.sin(u * (2 * math.pi / (1.1 + 0.8 * k)) * fr[k] + ph[k] + 0.04 * x * (k + 1))
        g = g / 3
        return np.sign(g) * np.abs(g) ** 0.6          # ostrejsi hrebinky (mekke drevo vymlete, leto vystupuje)
    # praskliny (podelne, V profil, na koncich se ztraci)
    cr = []
    for _ in range(rng.integers(cracks[0], cracks[1] + 1)):
        t_c = rng.uniform(0, 1)
        x0 = rng.uniform(-L / 2, L / 4); x1 = min(L / 2, x0 + rng.uniform(0.25, 0.8) * L)
        if rng.random() < 0.35: x0 = -L / 2 - 1     # prasklina az na konec (ctela vysychaji nejvic)
        if rng.random() < 0.35: x1 = L / 2 + 1
        cr.append((t_c, rng.uniform(*crack_w) / per, rng.uniform(*crack_d) * (0.5 if plank else 1.0), x0, x1, rng.uniform(0, 6)))
    bw_ = rng.normal(size=2) * bow; tw = rng.uniform(-0.03, 0.03)
    wn = [rng.uniform(0, 2 * math.pi, 4), rng.uniform(0.5, 1.0, 4)]
    verts, uvs = [], []
    for x in xs:
        fx = x / (L / 2)
        disp = -grain * (0.6 + 0.4 * grain_f(T, x)) if grain else np.zeros(n_ring)
        # mekke promacknuti a vymleti povrchu (nizka frekvence)
        disp = disp - 0.35 * (0.5 + 0.5 * np.sin(T * per * 0.21 + wn[0][1] + x * 0.031) * np.sin(x * 0.053 + wn[0][2]))
        for t_c, w_c, d_c, x0, x1, wob in cr:
            taper = np.clip(min(x - x0, x1 - x) / (0.08 * L + 1e-6), 0, 1)
            if taper <= 0: continue
            tc = t_c + 0.004 * math.sin(x * 0.05 + wob)                     # prasklina se lehce vlni
            dt = np.abs(((T - tc) + 0.5) % 1.0 - 0.5)
            disp = disp - d_c * taper * np.clip(1 - dt / w_c, 0, 1) ** 1.4
        # ohlazene / otlucene hrany (nepravidelne podel delky)
        wv = 0.5 + 0.5 * np.sin(x * 0.07 * wn[1][0] + wn[0][0] + T * 9) * np.sin(x * 0.19 * wn[1][1] + wn[0][3])
        disp = disp - wane * np.exp(-(dc / 1.8) ** 2) * (0.3 + 0.7 * wv)
        if plank:      # prkno: miskovite prohnuti napric (vysychani)
            disp = disp - 0.35 * (1 - (2 * np.abs(P0[:, 0]) / W) ** 2) * (N0[:, 1] > 0.7)
        ring = P0 + N0 * disp[:, None]
        # prohyb a zkrut podel delky
        a = tw * fx
        ca, sa = math.cos(a), math.sin(a)
        yy = ring[:, 0] * ca - ring[:, 1] * sa + bw_[0] * (1 - fx * fx)
        zz = ring[:, 0] * sa + ring[:, 1] * ca + bw_[1] * (1 - fx * fx)
        verts.append(np.stack([np.full(n_ring, x), yy, zz], 1))
        uvs.append(np.stack([np.full(n_ring, x / 100.0), T * per / 100.0], 1))
    V = np.concatenate(verts); UV = np.concatenate(uvs)
    F = []
    for i in range(n_len):
        a0 = i * n_ring; b0 = (i + 1) * n_ring
        for j in range(n_ring):
            j1 = (j + 1) % n_ring
            F.append((a0 + j, b0 + j, b0 + j1)); F.append((a0 + j, b0 + j1, a0 + j1))
    # ctela: vejir se stredem, mirne propadly (vysychani)
    for end, base in ((0, 0), (1, n_len * n_ring)):
        c = V[base:base + n_ring].mean(0); c[0] += (0.4 if end == 0 else -0.4)
        ci = len(V); V = np.vstack([V, c]); UV = np.vstack([UV, [[c[0] / 100, 0]]])
        for j in range(n_ring):
            j1 = (j + 1) % n_ring
            F.append((ci, base + j1, base + j) if end == 0 else (ci, base + j, base + j1))
    F = np.array(F)
    fn0 = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    flip = (fn0 * (V[F].mean(1) * [0.0, 1, 1] + [[0.0, 0, 0]])).sum(1) < 0
    endf = np.abs(V[F].mean(1)[:, 0]) > L / 2 - 1.0
    flip_end = (fn0[:, 0] * np.sign(V[F].mean(1)[:, 0])) < 0
    flip = np.where(endf, flip_end, flip)
    F[flip] = F[flip][:, ::-1]
    mn, mx = V.min(0), V.max(0)
    V = (V - (mn + mx) / 2) / (mx - mn) * np.array([L, W, Hh])
    fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    N = np.zeros_like(V)
    for c in range(3): np.add.at(N, F[:, c], fn)
    N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
    return V, UV, N, F


WOOD_VARIANTS = "ABC"
TIMBER = (100.0, 25.0, 25.0)      # jmenovite rozmery (cm): delka, sirka, vyska; skript naskaluje na presny kus
PLANK = (100.0, 25.0, 5.0)


def build(out):
    """vsechno drevo do slozky out -> seznam (jmeno, vrcholu, trojuhelniku)"""
    made = []
    for vi, v in enumerate(WOOD_VARIANTS):
        P, UV, N, F = make_timber(*TIMBER, seed=9000 + vi * 37, r=1.4 + vi * 0.4)
        name = "SM_RuinTimber_%s" % v; write_obj(os.path.join(out, name + ".obj"), P, UV, N, F, name); made.append((name, len(P), len(F)))
        # sloup: stejny tram postaveny na vysku (delka podel Z)
        Pp = P[:, [1, 2, 0]]; Np = N[:, [1, 2, 0]]
        name = "SM_RuinPost_%s" % v; write_obj(os.path.join(out, name + ".obj"), Pp, UV, Np, F, name); made.append((name, len(P), len(F)))
        P, UV, N, F = make_timber(*PLANK, seed=9500 + vi * 41, r=0.7, n_ring=64, cracks=(2, 3), crack_d=(1.0, 1.8),
                                  wane=0.9, bow=0.25, plank=True, crack_w=(0.8, 1.3))
        name = "SM_RuinPlank_%s" % v; write_obj(os.path.join(out, name + ".obj"), P, UV, N, F, name); made.append((name, len(P), len(F)))
    return made + mesh_log.build(out)          # kulatina (mesh_log.py)
