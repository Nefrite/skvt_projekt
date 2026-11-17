"""mesh_textile - lano, ovazani, platno (OBJ, cm, Z nahoru). Kategorie textile (v UE Ruin/Textile).

SM_RuinRope_A..B: clanek konopneho lana 100 cm, prumer 1,5 cm, 3 prameny stocene. Prevesene lano mezi dvema body
    stavba slozi z nekolika clanku podel retezovky (delka podel X, scale na delku clanku a prumer).
SM_RuinLashing_A..B: ovazani na kriseni / spoji tyci: krizem natocene zavity lana kolem valce O 8 cm (osa X),
    sirka 6 cm. Skaluje se podle prumeru tyce.
SM_RuinCanvasSample_A: ukazka plachty z make_canvas (3 x 2,4 m, 5 krokvovych tyci, sklon 22 st.) - pro kontrolu
    vzhledu a materialu; stavby si generuji plachtu na miru funkci make_canvas (OBJ podle poloh tyci).
SM_RuinCanvasVez_A, SM_RuinCanvasVezGable_A: plachta a stit pristresku hlidky na vezi na miru (tower_spec.pristresek),
    OBJ vystredeny + <jmeno>.json se stredem a rozmerem v lokalnich osach stavby (write_fitted).
Sloty: Rope (lano, ovazani), Canvas (platno; material oboustranny, viz M_RuinCloth).
"""
import math, os
import numpy as np

from mesh_common import waves, noise, smooth_normals, write_obj_slots

NOMINAL = {
    "SM_RuinRope":         (100.0, 1.5, 1.5),
    "SM_RuinLashing":      (7.0, 10.5, 10.5),
    "SM_RuinCanvasSample": (300.0, 221.6, 93.8),       # = rozmer ukazky z make_canvas (sklon 22,6 st.)
}


def _sweep(path, R, n_ar, twist_pitch, lobes=3, lobe_amp=0.16, caps=True):
    """lano podel krivky path (k,3): kruhovy prurez s 3 stocenymi prameny (laloky), UV u = delka (m), v = obvod * 0,25"""
    T = np.gradient(path, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True)
    ref = np.array([0.0, 0.0, 1.0])
    arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))])
    th = np.linspace(0, 2 * math.pi, n_ar + 1)
    P = np.zeros((len(path), n_ar + 1, 3)); UV = np.zeros((len(path), n_ar + 1, 2))
    Y0 = None
    for i in range(len(path)):
        t = T[i]
        if Y0 is None:
            r0 = ref if abs(t @ ref) < 0.9 else np.array([0.0, 1.0, 0.0])
            Y0 = np.cross(r0, t); Y0 /= np.linalg.norm(Y0)
        Yi = Y0 - (Y0 @ t) * t; Yi /= np.linalg.norm(Yi); Zi = np.cross(t, Yi); Y0 = Yi    # paralelni transport
        r = R * (1 - lobe_amp + lobe_amp * np.abs(np.cos(lobes / 2 * (th - 2 * math.pi * arc[i] / twist_pitch))))
        P[i] = path[i] + r[:, None] * (np.cos(th)[:, None] * Yi + np.sin(th)[:, None] * Zi)
        UV[i, :, 0] = arc[i] / 100; UV[i, :, 1] = th / (2 * math.pi) * 0.25
    n = len(path)
    F = []
    for i in range(n - 1):
        for j in range(n_ar):
            a = i * (n_ar + 1) + j; b = a + n_ar + 1
            F += [(a, a + 1, b + 1), (a, b + 1, b)]
    P = P.reshape(-1, 3); UV = UV.reshape(-1, 2)
    if caps:
        for i, sg in ((0, -1), (n - 1, 1)):
            c = len(P); P = np.vstack([P, path[i]]); UV = np.vstack([UV, [0.0, 0.0]])
            for j in range(n_ar):
                a = i * (n_ar + 1) + j
                F.append((c, a + 1, a) if sg < 0 else (c, a, a + 1))
    F = np.array(F)
    return P, UV, F


def _fix_out(P, F, axis_pts):
    """normaly lana ven: plocha musi mirit od nejblizsiho bodu osy"""
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); c = P[F].mean(1)
    d = c[:, None, :] - axis_pts[None, :, :]
    k = np.argmin((d ** 2).sum(-1), axis=1); out = c - axis_pts[k]
    flip = (fn * out).sum(1) < 0
    F = F.copy(); F[flip] = F[flip][:, ::-1]
    return F


def make_rope(seed, L=100.0, R=0.75):
    rng = np.random.default_rng(seed)
    x = np.linspace(-L / 2, L / 2, 241)
    path = np.stack([x, 0.05 * np.sin(x * 0.11 + rng.uniform(0, 6)), 0.05 * np.cos(x * 0.07 + rng.uniform(0, 6))], 1)
    P, UV, F = _sweep(path, R, 12, 4.0)
    return P, UV, _fix_out(P, F, path)


def make_lashing(seed, Rp=4.0, R=0.6, turns=5, width=6.0):
    """dve krizem vinute sroubovice kolem tyce O 2*Rp (osa X)"""
    rng = np.random.default_rng(seed)
    Ps, UVs, Fs, ax = [], [], [], []
    off = 0
    for sgn in (1, -1):
        t = np.linspace(0, turns, turns * 40 + 1)
        rr = Rp + R * (1.0 + 0.15 * np.sin(t * 7 + rng.uniform(0, 6)))
        x = sgn * (-width / 2 + width * t / turns) + 0.3 * np.sin(t * 2 * math.pi)
        a = 2 * math.pi * t + (0 if sgn > 0 else math.pi / turns)
        path = np.stack([x, rr * np.cos(a), rr * np.sin(a)], 1)
        P, UV, F = _sweep(path, R, 10, 3.0)
        F = _fix_out(P, F, path)
        Ps.append(P); UVs.append(UV); Fs.append(F + off); off += len(P); ax.append(path)
    return np.concatenate(Ps), np.concatenate(UVs), np.concatenate(Fs)


def make_canvas(eave0, eave1, ridge0, ridge1, rafters=(), sag=4.0, slope_sag=0.4, seed=0, step=4.0, wrinkle=0.25):
    """plachta na miru (cm, souradnice stavby): ctyrhelnik okap (eave0 -> eave1) a hreben (ridge0 -> ridge1),
    rafters = polohy krokvovych tyci jako podil sirky 0..1 (tam plachta lezi); mezi nimi se prevesi o sag (cm),
    nejvic uprostred spadu (slope_sag = podil prevesu u okapu a hrebene). Za krajnimi tycemi visi volny okraj.
    Vrati (P, UV, F) - jednovrstva plocha, material oboustranny. UV v m (dlazdice platna 0,25 m)."""
    e0, e1, r0, r1 = (np.asarray(p, float) for p in (eave0, eave1, ridge0, ridge1))
    wd = max(np.linalg.norm(e1 - e0), np.linalg.norm(r1 - r0)); ln = max(np.linalg.norm(r0 - e0), np.linalg.norm(r1 - e1))
    nu = max(4, int(round(wd / step))); nv = max(4, int(round(ln / step)))
    u = np.linspace(0, 1, nu + 1); v = np.linspace(0, 1, nv + 1)
    U, V = np.meshgrid(u, v, indexing="ij")
    P = ((1 - U) * (1 - V))[..., None] * e0 + (U * (1 - V))[..., None] * e1 + ((1 - U) * V)[..., None] * r0 + (U * V)[..., None] * r1
    rf = sorted(rafters) or [0.0, 1.0]
    g = np.zeros_like(U)
    for k in range(len(rf) - 1):
        a, b = rf[k], rf[k + 1]; m = (U >= a) & (U <= b)
        g = np.where(m, np.sin(math.pi * (U - a) / max(b - a, 1e-6)), g)
    g = np.where(U < rf[0], 0.6 * (rf[0] - U) / max(rf[0], 1e-6), g)               # volny okraj pred prvni tyci
    g = np.where(U > rf[-1], 0.6 * (U - rf[-1]) / max(1 - rf[-1], 1e-6), g)
    along = slope_sag + (1 - slope_sag) * np.sin(math.pi * V)
    W = waves(seed + 1, 10, 15, 60)
    q = P.reshape(-1, 3)
    wr = (wrinkle * noise(q, W)).reshape(U.shape)
    P = P.copy(); P[..., 2] -= sag * g * along + wr * g
    UVa = np.stack([U * wd / 100, V * ln / 100], -1)
    F = []
    for a in range(nu):
        for b in range(nv):
            v00 = a * (nv + 1) + b; v10 = v00 + nv + 1
            F += [(v00, v10, v10 + 1), (v00, v10 + 1, v00 + 1)]
    F = np.array(F); P = P.reshape(-1, 3)
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    if fn[:, 2].sum() < 0: F = F[:, ::-1]                                        # lic nahoru
    return P, UVa.reshape(-1, 2), F


def write_canvas(path, name, P, UV, F):
    """OBJ plachty pro stavbu (souradnice beze zmeny, cm)"""
    write_obj_slots(path, P, UV, smooth_normals(P, F, np.zeros(len(P), int)), F, np.zeros(len(F), int), name, "plachta (platno)", ("Canvas",))


def _write(out, name, P, UV, F, slot_name, desc, made):
    nom = NOMINAL[name.rsplit("_", 1)[0]]
    if nom:
        mn, mx = P.min(0), P.max(0)
        P = (P - (mn + mx) / 2) / (mx - mn) * np.array(nom)
    write_obj_slots(os.path.join(out, name + ".obj"), P, UV, smooth_normals(P, F, np.zeros(len(P), int)), F, np.zeros(len(F), int),
                    name, desc, (slot_name,))
    made.append((name, len(P), len(F)))


def build(out):
    """lano, ovazani, ukazka plachty do slozky out -> seznam (jmeno, vrcholu, trojuhelniku)"""
    made = []
    for vi, v in enumerate("AB"):
        _write(out, "SM_RuinRope_" + v, *make_rope(20000 + vi * 31), "Rope", "clanek lana", made)
        _write(out, "SM_RuinLashing_" + v, *make_lashing(20500 + vi * 37), "Rope", "ovazani lanem", made)
    s = math.radians(22.6); Lr = 240.0
    P, UV, F = make_canvas((-150, 0, 0), (150, 0, 0), (-150, Lr * math.cos(s), Lr * math.sin(s)), (150, Lr * math.cos(s), Lr * math.sin(s)),
                           rafters=(0.05, 0.28, 0.5, 0.72, 0.95), sag=4.0, seed=21000)
    P = P - (P.min(0) + P.max(0)) / 2
    _write(out, "SM_RuinCanvasSample_A", P, UV, F, "Canvas", "ukazka plachty (make_canvas)", made)
    for name, (P, UV, F) in canvas_vez().items():                      # plachta a stit pristresku na vezi (na miru)
        write_fitted(out, name, P, UV, F, "plachta pristresku na vezi (tower_spec.pristresek)", made)
    return made


# --- tvary na miru pro stavby: OBJ vystredeny na bounding box + <jmeno>.json se stredem a rozmerem v lokalnich osach
#     stavby (UE cm); stavba podle nej mesh posadi (05 zr_stavby/pristresek.py). Lokalni osy pristresku na vezi:
#     X = u, Y = -v (ram veze je v UE levotocivy: v = osa X otocena o -90 st.), Z = h od VEZ_F
def write_fitted(out, name, P, UV, F, desc, made):
    import json
    mn, mx = P.min(0), P.max(0); c = (mn + mx) / 2
    write_obj_slots(os.path.join(out, name + ".obj"), P - c, UV, smooth_normals(P, F, np.zeros(len(P), int)), F, np.zeros(len(F), int),
                    name, desc, ("Canvas",))
    with open(os.path.join(out, name + ".json"), "w") as f:
        json.dump(dict(center=[round(float(q), 3) for q in c], size=[round(float(q), 3) for q in mx - mn]), f)
    made.append((name, len(P), len(F)))


def canvas_vez():
    """plachta a stit pristresku hlidky na vezi z tools/ruin/tower_spec.pristresek -> {jmeno: (P, UV, F)} v lokalnich osach
    stavby (X = u, Y = -v, Z = h; cm)"""
    import json, sys
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    sys.path.insert(0, os.path.join(root, "tools", "ruin"))
    from tower_spec import spec, pristresek
    with open(os.path.join(root, "03_ruin", "ruin_layout_draft.json"), encoding="utf-8") as f: D = json.load(f)
    p = pristresek(spec(D["tower"])); cv = p["canvas"]; L = lambda u, v, h: (u * 100, -v * 100, h * 100)
    (u0, u1), (v0, v1) = cv["u"], cv["v"]; ch = p["canvas_h"]
    raf = [(u - u0) / (u1 - u0) for u in p["rafters"]["u"]]
    out = {"SM_RuinCanvasVez_A": make_canvas(L(u0, v0, ch(v0)), L(u1, v0, ch(v0)), L(u0, v1, ch(v1)), L(u1, v1, ch(v1)),
                                            rafters=raf, sag=cv["sag"] * 100, seed=cv["seed"])}
    # stit: svisly trojuhelnik v rovine u = g["u"]; make_canvas v rovine (v, h), "prevesi" = vyduti podel u (dovnitr veze)
    g = p["gable"]; (gv0, gv1) = g["v"]; top = lambda v: p["rafter_axis"](v) - p["rafters"]["d"] / 2      # spodek krajni krokve
    P, UV, F = make_canvas((gv0 * 100, g["bottom"] * 100, 0), (gv1 * 100, g["bottom"] * 100, 0),
                           (gv0 * 100, max(top(gv0), g["bottom"] + 0.005) * 100, 0), (gv1 * 100, top(gv1) * 100, 0),
                           sag=g["bulge"] * 100, seed=g["seed"], wrinkle=0.15)
    P = np.stack([g["u"] * 100 - P[:, 2], -P[:, 0], P[:, 1]], 1)                       # (v, h, vyduti) -> (u, -v, h)
    out["SM_RuinCanvasVezGable_A"] = (P, UV, F)
    return out
