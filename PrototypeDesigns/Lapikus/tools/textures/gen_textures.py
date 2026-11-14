"""gen_textures.py - procedurni textury zriceniny a dostaveb (PNG 1024, bezesve dlazdice). Potrebuje numpy a Pillow.

    python tools/textures/gen_textures.py [vystupni slozka]

Bez slozky zapisuje do textures/ v koreni (odtud je build sam naimportuje do UE, TEX_DIR v zrlib/config.py).
Textury jsou v odstinech sedi (barvu dava tint v materialu, MAT_LOOK v zrlib/config.py) + normalova mapa (DirectX, jako UE).
  T_RuinBark_*      kura (smrk): supiny protazene podel osy U (= delka kmene), brazdy, dlazdice 0,5 m
  T_RuinEndGrain_*  celo: letokruhy jako vodorovne pruhy (UV cela je polarni: V = vzdalenost od stredu), radialni trhliny
                    svisle (U = uhel), dlazdice 0,5 m
  T_RuinRope_*      konopne lano: 3 prameny stocene sikmo (U = delka), dlazdice 0,25 m x obvod
  T_RuinWattle_*    vyplet z prouti: vodorovne pruty stridave pred a za koly, dlazdice 0,5 m
  T_RuinDaub_*      mazanina (hlina se slamou, praskliny), i vypln spar srubu, dlazdice 0,5 m
  T_RuinCanvas_*    lnene platno: platnova vazba a nite (bez skvrn), dlazdice 0,25 m
  T_RuinCanvasMacro_D  velke skvrny a zasednuti plachty, dlazdice 4 m (M_RuinCloth: MacroTiling, MacroAmount)
  T_RuinIron_*      kovane zelezo s patinou rzi: okuje, dulky po kladivu, hnede skvrny rzi (barva v texture), dlazdice 0,5 m
  T_RuinIronClean_* kovane zelezo bez rzi (naradi, kovadlina): okuje a dulky, o neco svetlejsi
  T_RuinLeather_*   kuze: vrasky, pory, odrena mista (barva v texture)
  T_RuinCharcoal_*  drevene uhli: kousky s lomy, cerne spary
  T_RuinWater_*     hladina: tmava, vlnky v normale
Jen vybrane: python tools/textures/gen_textures.py [slozka] T_RuinRope T_RuinDaub
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


def rope():
    """konopne lano: 3 prameny stocene sikmo (U = delka lana, V = obvod), vlakna podel pramene. Dlazdice 0,25 m delky
    x cely obvod (UV lana: v = obvod * 0,25, Tiling 4)."""
    uu = _u[None, :]; vv = _u[:, None]
    ph = 3 * vv + 6 * uu                                       # 3 prameny, 6 zavitu na dlazdici (~4 cm)
    f = ph - np.floor(ph)
    strand = np.sin(math.pi * f) ** 0.6                         # profil pramene
    fib = pnoise(301, 70, (30, 120), (10, 60), 0.3)             # vlakna (jemne, podel pramene)
    fib2 = np.sin(2 * math.pi * (40 * vv - 30 * uu) + 3 * pnoise(302, 20, (4, 12), (4, 12)))
    h = strand + 0.10 * fib + 0.05 * fib2
    d = 0.55 + 0.30 * strand + 0.08 * fib + 0.04 * fib2 - 0.25 * (1 - strand) ** 3
    col = np.stack([d, d * 0.93, d * 0.80], -1)
    return np.clip(col, 0, 1), normal_map(h, 5.0)


def wattle():
    """vyplet z prouti: vodorovne pruty (U) stridave pred a za svislymi koly (2 kuly na dlazdici 0,5 m), kazdy prut jinak
    tmavy, kura na prutech"""
    rows = 20                                                   # pruty na dlazdici (~2,5 cm)
    uu = _u[None, :]; vv = _u[:, None]
    r = np.floor(vv * rows); fr = vv * rows - r
    wobble = 0.15 * pnoise(401, 20, (2, 8), (1, 4))
    fr2 = np.clip(fr + wobble, 0, 1)
    rod = np.sin(math.pi * fr2) ** 0.5
    weave = np.cos(2 * math.pi * 2 * uu + math.pi * (r % 2))    # pred / za kulem
    rng = np.random.default_rng(402); lum = rng.uniform(0.75, 1.15, rows)[r.astype(int) % rows]
    stake = np.exp(-(((uu * 2) % 1.0 - 0.5) / 0.035) ** 2)      # svisle kuly (vidi se v mezerach)
    fine = pnoise(403, 60, (20, 80), (20, 80), 0.5)
    h = rod * (0.6 + 0.4 * weave) + 0.06 * fine
    gap = (1 - rod) ** 4
    d = (0.35 + 0.35 * rod * lum + 0.06 * fine) * (1 - 0.6 * gap) + 0.15 * stake * gap
    col = np.stack([d, d * 0.92, d * 0.80], -1)
    return np.clip(col, 0, 1), normal_map(h, 7.0)


def daub():
    """mazanina: hlina se slamou, praskliny po vysychani (Voronoi hrany), otisky dlani, dlazdice 0,5 m"""
    F1, F2, ID = voronoi(501, 70, 1.0)
    crack = np.exp(-((F2 - F1) / 0.004) ** 2) * (pnoise(502, 20, (2, 8), (2, 8)) > -0.2)
    big = pnoise(503, 40, (1, 6), (1, 6)); mid = pnoise(504, 60, (6, 24), (6, 24), 0.6); fine = pnoise(505, 90, (30, 100), (30, 100), 0.4)
    r = np.random.default_rng(506); straw = np.zeros((N, N))
    for _ in range(420):                                         # stebla slamy (kratke svetle carky)
        cu, cv = r.uniform(0, 1, 2); a = r.uniform(0, math.pi); ln = r.uniform(0.004, 0.013); w = r.uniform(0.0006, 0.0011)
        du = (_u[None, :] - cu + 0.5) % 1.0 - 0.5; dv = (_u[:, None] - cv + 0.5) % 1.0 - 0.5
        t = du * math.cos(a) + dv * math.sin(a); n = -du * math.sin(a) + dv * math.cos(a)
        straw = np.maximum(straw, np.exp(-(n / w) ** 2) * (np.abs(t) < ln))
    h = 0.5 * big + 0.3 * mid + 0.08 * fine - 0.8 * crack + 0.05 * straw
    d = 0.58 + 0.10 * big + 0.08 * mid + 0.05 * fine - 0.40 * crack + 0.10 * straw
    col = np.stack([d, d * 0.90, d * 0.76], -1)
    return np.clip(col, 0, 1), normal_map(h, 6.0)


def canvas():
    """lnene platno: platnova vazba (osnova U, utek V, ~1 mm), nestejne silne nite, dlazdice 0,25 m. Bez skvrn: male
    dlazdice by je opakovaly (vzor po 25 cm); skvrny jsou ve velke texture T_RuinCanvasMacro (dlazdice 4 m)."""
    uu = _u[None, :]; vv = _u[:, None]
    k = 256                                                      # nite na dlazdici
    wu = np.sin(2 * math.pi * k * uu); wv = np.sin(2 * math.pi * k * vv)
    weave = 0.5 + 0.25 * np.sign(wu * wv) * np.minimum(np.abs(wu), np.abs(wv)) ** 0.5
    slub_u = pnoise(601, 40, (1, 3), (40, 200), 0.2); slub_v = pnoise(602, 40, (40, 200), (1, 3), 0.2)
    h = weave + 0.15 * slub_u + 0.15 * slub_v
    d = 0.72 + 0.06 * (weave - 0.5) + 0.03 * slub_u + 0.03 * slub_v
    col = np.stack([d, d * 0.97, d * 0.90], -1)
    return np.clip(col, 0, 1), normal_map(h, 2.5)


def canvas_macro():
    """velke skvrny a zasednuti plachty (dlazdice 4 m, v M_RuinCloth pres MacroTiling 0,25 / m): stredni sed 0,5 = beze zmeny,
    tmavsi skvrny od vody a sazi, svetlejsi vybledla mista; mekke prechody. Jen barva (normala rovna)."""
    big = pnoise(701, 30, (1, 4), (1, 4)); mid = pnoise(702, 50, (3, 12), (3, 12), 0.7)
    stain = np.clip((pnoise(703, 40, (2, 8), (2, 8)) - 0.35) * 2.5, 0, 1)            # ojedinele tmave skvrny
    d = 0.5 + 0.10 * big + 0.05 * mid - 0.12 * stain
    flat = np.zeros((N, N, 3)); flat[..., 2] = 1.0
    return np.clip(np.stack([d, d, d], -1), 0, 1), flat * 0.5 + 0.5


def iron(rusty=True):
    """kovane zelezo: tmave sede s okujemi, mele dulky po kladivu (bunky); rusty = skvrny rzi (tlumene hnede, ne cervene).
    Barva je v texture (tint v materialu ~ bila), dlazdice 0,5 m"""
    F1, F2, ID = voronoi(801, 160, 1.0)
    r = np.random.default_rng(802); lum = r.uniform(0.85, 1.1, ID.max() + 1)[ID]
    dent = (F1 / (F1 + F2 + 1e-6))                             # 0 ve stredu dulku, 0,5 na hrane
    scale = pnoise(803, 40, (2, 10), (2, 10)); fine = pnoise(804, 80, (30, 120), (30, 120), 0.4)
    rust = np.clip((pnoise(805, 40, (1, 6), (1, 6)) + 0.3 * pnoise(806, 60, (8, 30), (8, 30)) - 0.38) * 2.5, 0, 1) * 0.9
    if not rusty: rust = np.zeros_like(rust)
    g = ((0.22 if rusty else 0.26) + 0.06 * scale + 0.04 * fine) * lum * (0.92 + 0.16 * dent)
    col = np.stack([g, g * 1.01, g * 1.04], -1)
    rc = np.stack([0.30 + 0.05 * fine, 0.21 + 0.035 * fine, 0.14 + 0.02 * fine], -1)          # tlumena hneda rez
    col = col * (1 - rust[..., None]) + rc * rust[..., None]
    h = 0.6 * dent + 0.05 * fine + 0.25 * rust * (0.5 + 0.5 * fine)
    return np.clip(col, 0, 1), normal_map(h, 9.0)


def leather():
    """kuze (mech): hnede, vrasky (protazene podel U), pory, odrena svetlejsi mista"""
    wr = pnoise(901, 60, (2, 10), (10, 40), 0.6); wr2 = pnoise(902, 40, (8, 30), (1, 6), 0.6)
    pores = pnoise(903, 120, (60, 200), (60, 200), 0.2); big = pnoise(904, 30, (1, 5), (1, 5))
    wr3 = pnoise(905, 80, (10, 40), (10, 40), 0.5)
    crease = 0.6 * np.exp(-(wr / 0.025) ** 2) * (wr3 > -0.2) + 0.3 * np.exp(-(wr2 / 0.02) ** 2) * (wr3 > 0.1)
    worn = np.clip((big - 0.3) * 2.0, 0, 1)
    h = -0.5 * crease + 0.08 * pores + 0.15 * big + 0.1 * wr3
    g = 0.30 + 0.05 * pores - 0.07 * crease + 0.10 * worn + 0.02 * wr3
    col = np.stack([g * 1.15, g * 0.75, g * 0.48], -1)
    return np.clip(col, 0, 1), normal_map(h, 5.0)


def charcoal():
    """drevene uhli: kousky (bunky) s ostrymi hranami a lesklymi lomy, cerne spary mezi nimi, dlazdice 0,5 m"""
    F1, F2, ID = voronoi(1001, 220, 1.0)
    r = np.random.default_rng(1002); lum = r.uniform(0.6, 1.4, ID.max() + 1)[ID]; tilt = r.uniform(-1, 1, ID.max() + 1)[ID]
    gap = np.exp(-((F2 - F1) / 0.006) ** 2)
    grain = np.abs(np.sin(2 * math.pi * (_u[None, :] * 40 + 6 * pnoise(1003, 30, (2, 10), (2, 10)))))       # letokruhy na lomech
    h = (1 - gap) * (0.6 + 0.2 * tilt * (F1 * 20)) + 0.03 * grain
    g = (0.55 + 0.08 * grain) * lum * (1 - 0.8 * gap)        # svetla detailni textura; cernou barvu dava tint (MAT_LOOK charcoal)
    col = np.stack([g, g, g * 1.05], -1)
    return np.clip(col, 0, 1), normal_map(h, 8.0)


def water():
    """hladina ve sudu a korytu: skoro jednolita tmava, jemne vlnky jen v normale"""
    rip = pnoise(1101, 40, (2, 12), (2, 12), 0.8)
    d = 0.5 + 0.03 * pnoise(1102, 20, (1, 4), (1, 4))
    return np.clip(np.stack([d, d, d], -1), 0, 1), normal_map(0.4 * rip, 1.5)


TEXTURES = {"T_RuinBark": bark, "T_RuinEndGrain": endgrain, "T_RuinRope": rope, "T_RuinWattle": wattle,
            "T_RuinDaub": daub, "T_RuinCanvas": canvas, "T_RuinCanvasMacro": canvas_macro,
            "T_RuinIron": iron, "T_RuinIronClean": lambda: iron(False), "T_RuinLeather": leather, "T_RuinCharcoal": charcoal, "T_RuinWater": water}
NO_NORMAL = {"T_RuinCanvasMacro"}           # jen barva


def main(out=None, names=None):
    out = out or DEFAULT_OUT
    os.makedirs(out, exist_ok=True)
    for name, fn in TEXTURES.items():
        if names and name not in names: continue
        d, n = fn()
        save(d, os.path.join(out, name + "_D.png"))
        if name not in NO_NORMAL: save(n, os.path.join(out, name + "_N.png"))
        print("%-18s %s" % (name, out))


if __name__ == "__main__":
    a = sys.argv[1:]
    out = a.pop(0) if a and not a[0].startswith("T_Ruin") else None
    main(out, a)
