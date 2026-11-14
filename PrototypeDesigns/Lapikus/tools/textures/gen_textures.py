"""gen_textures.py - procedurni textury zriceniny a dostaveb (PNG 1024, bezesve dlazdice). Potrebuje numpy a Pillow.

    python tools/textures/gen_textures.py [vystupni slozka]

Bez slozky zapisuje do textures/ v koreni (odtud je build sam naimportuje do UE, TEX_DIR v zrlib/config.py).
Textury jsou v odstinech sedi (barvu dava tint v materialu, MAT_LOOK v zrlib/config.py) + normalova mapa (DirectX, jako UE).
  T_RuinBark_*      kura (smrk): supiny protazene podel osy U (= delka kmene), brazdy, dlazdice 0,5 m
  T_RuinEndGrain_*  celo: letokruhy jako vodorovne pruhy (UV cela je polarni: V = vzdalenost od stredu), radialni trhliny
                    svisle (U = uhel), dlazdice 0,5 m
Deterministicke (pevne seedy). Po zmene zvys TEX_VERSION v zrlib/config.py, jinak UE textury neprenacte.
"""
import math, os, sys
import numpy as np
from PIL import Image

N = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.normpath(os.path.join(HERE, "..", "..", "textures"))      # = TEX_SRC v zrlib/config.py
_u = np.arange(N) / N


def pnoise(seed, n, fu, fv, amp_pow=1.0):
    """periodicky sum: soucet n vln s celociselnymi frekvencemi (fu, fv = rozsahy) -> bezesva dlazdice, ~ -1..1"""
    r = np.random.default_rng(seed)
    out = np.zeros((N, N))
    for _ in range(n):
        a = int(r.integers(fu[0], fu[1] + 1)) * r.choice([-1, 1]); b = int(r.integers(fv[0], fv[1] + 1))
        ph = r.uniform(0, 2 * math.pi); w = 1.0 / max(1.0, math.hypot(a, b)) ** amp_pow
        out += w * np.cos(2 * math.pi * (b * _u[:, None] + a * _u[None, :]) + ph)      # [radek v, sloupec u]
    return out / (np.abs(out).max() + 1e-9)


def normal_map(h, strength):
    """vyska -> normalova mapa (DirectX: zelena = -dh/dv), periodicke diference"""
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5 * strength
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5 * strength
    n = np.stack([-dx, dy, np.ones_like(h)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return (n * 0.5 + 0.5)


def save(img, path, srgb=True):
    a = np.clip(img, 0, 1)
    if a.ndim == 2: a = np.stack([a] * 3, -1)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8), "RGB").save(path)


def voronoi(seed, n_pts, stretch_u):
    """periodicke Voronoi bunky: F1, F2 (vzdalenost k nejblizsimu a druhemu bodu) a index bunky.
    stretch_u > 1 = bunky protazene podel U"""
    r = np.random.default_rng(seed)
    pts = r.uniform(0, 1, (n_pts, 2))                         # (u, v)
    F1 = np.full((N, N), 9.0); F2 = np.full((N, N), 9.0); ID = np.zeros((N, N), int)
    vv = _u[:, None]; uu = _u[None, :]
    for k, (pu, pv) in enumerate(pts):
        du = ((uu - pu + 0.5) % 1.0 - 0.5) / stretch_u; dv = (vv - pv + 0.5) % 1.0 - 0.5
        d = np.sqrt(du * du + dv * dv)
        closer = d < F1
        F2 = np.where(closer, F1, np.minimum(F2, d)); ID = np.where(closer, k, ID); F1 = np.where(closer, d, F1)
    return F1, F2, ID


def bark():
    """smrkova kura: supiny (Voronoi bunky protazene podel U = delka kmene), mezi nimi brazdy; supina se zveda k jednomu
    okraji (odlupuje se), kazda jinak svetla; jemna struktura a zvetrale skvrny"""
    F1, F2, ID = voronoi(101, 340, 1.7)
    edge = F2 - F1                                            # 0 na hranici bunek
    r = np.random.default_rng(102)
    lum = r.uniform(0.75, 1.15, ID.max() + 1)[ID]             # jas supiny
    lift = r.uniform(0.0, 1.0, ID.max() + 1)[ID]
    fine = pnoise(103, 90, (20, 70), (20, 70), 0.5)
    warp = pnoise(104, 30, (2, 8), (4, 14))
    groove = np.exp(-(edge / (0.010 + 0.004 * warp)) ** 2)   # brazda mezi supinami
    bevel = np.clip(edge / 0.03, 0, 1) ** 0.6                 # zaobleni okraje supiny
    big = pnoise(105, 30, (1, 4), (3, 10))                    # hlubsi podelne brazdy (starsi kura)
    deep = np.exp(-(big / 0.07) ** 2)
    h = 0.55 * bevel + 0.25 * lift * F1 / (F1 + F2 + 1e-6) * 2 + 0.08 * fine - 0.5 * deep
    h = (h - h.min()) / (h.max() - h.min())
    d = (0.30 + 0.42 * bevel * lum + 0.05 * fine) * (1 - 0.6 * groove) * (1 - 0.45 * deep)
    lich = np.clip((pnoise(106, 30, (2, 8), (2, 8)) - 0.5) * 3, 0, 1) * bevel * 0.18   # svetlejsi zvetrale skvrny
    d = np.clip(d + lich, 0, 1)
    col = np.stack([d, d * 0.96, d * 0.92], -1)
    return col, normal_map(h, 10.0)


def endgrain():
    """celo: letokruhy (jarni svetle / letni tmave drevo) jako vodorovne pruhy, zvlnene; radialni trhliny svisle"""
    rings = 160                                               # pruhu na dlazdici (0,5 m -> ~3 mm na letokruh)
    warp = pnoise(201, 20, (1, 4), (1, 6))
    r1 = np.random.default_rng(205); wid = np.zeros(N)          # promenliva sirka letokruhu (suche / vlhke roky)
    for k in range(1, 25): wid += r1.normal(0, 1) / k * np.sin(2 * math.pi * (k * _u + r1.uniform()))
    gw = np.abs(np.gradient(wid) * N).max()
    wid *= 0.55 * rings / gw                                    # sirka letokruhu 45-155 % prumeru, pruhy se nekrizi
    ph = _u[:, None] * rings + wid[:, None] + 1.6 * warp + 0.2 * pnoise(202, 30, (2, 10), (4, 16))
    f = ph - np.floor(ph)
    late = np.clip((f - 0.70) / 0.12, 0, 1) * np.clip((1.0 - f) / 0.05, 0, 1)        # tmavsi letni drevo na konci pruhu
    fine = pnoise(203, 80, (20, 80), (20, 80), 0.5)
    crack = np.zeros((N, N))
    r = np.random.default_rng(204)
    for _ in range(3):                                        # radialni trhliny (svisle cary, jen cast vysky)
        u0 = r.uniform(0, 1); v0 = r.uniform(0, 1); ln = r.uniform(0.2, 0.5); w = r.uniform(0.0015, 0.003)
        du = ((_u[None, :] - u0 - 0.004 * np.sin(_u[:, None] * 40 + u0 * 9) + 0.5) % 1.0) - 0.5
        dv = ((_u[:, None] - v0 + 0.5) % 1.0) - 0.5
        crack = np.maximum(crack, np.exp(-(du / w) ** 2) * np.clip(1 - np.abs(dv) / (ln / 2), 0, 1) ** 0.5)
    saw = 0.5 + 0.5 * np.sin(2 * math.pi * (_u[None, :] * 9 + _u[:, None] * 31))      # stopy pily / sekery
    h = -0.35 * late + 0.08 * fine - 1.0 * crack + 0.06 * saw
    d = 0.70 + 0.08 * fine - 0.28 * late - 0.55 * crack + 0.03 * saw
    col = np.stack([d, d * 0.94, d * 0.86], -1)
    return np.clip(col, 0, 1), normal_map(h, 6.0)


TEXTURES = {"T_RuinBark": bark, "T_RuinEndGrain": endgrain}


def main(out=None):
    out = out or DEFAULT_OUT
    os.makedirs(out, exist_ok=True)
    for name, fn in TEXTURES.items():
        d, n = fn()
        save(d, os.path.join(out, name + "_D.png")); save(n, os.path.join(out, name + "_N.png"))
        print("%-18s %s" % (name, out))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
