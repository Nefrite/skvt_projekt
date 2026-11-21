"""mesh_textile - lano, ovazani, platno (OBJ, cm, Z nahoru). Kategorie textile (v UE Ruin/Textile).

SM_RuinRope_A..B: clanek konopneho lana 100 cm, prumer 1,5 cm, 3 prameny stocene. Prevesene lano mezi dvema body
    stavba slozi z nekolika clanku podel retezovky (delka podel X, scale na delku clanku a prumer).
SM_RuinLashing_A..B: ovazani na kriseni / spoji tyci: krizem natocene zavity lana kolem valce O 8 cm (osa X),
    sirka 6 cm. Skaluje se podle prumeru tyce.
SM_RuinCanvasSample_A: ukazka plachty z make_canvas (3 x 2,4 m, 5 krokvovych tyci, sklon 22 st.) - pro kontrolu
    vzhledu a materialu; stavby si generuji plachtu na miru funkci make_canvas (OBJ podle poloh tyci).
SM_RuinCanvasVez_A, SM_RuinCanvasVezGable_A: plachta a stit pristresku hlidky na vezi na miru (tower_spec.pristresek),
    OBJ vystredeny + <jmeno>.json se stredem a rozmerem v lokalnich osach stavby (write_fitted).
SM_RuinCanvasTent_A: plachta stanu do A na nadvori (navrh_nadvori_stan kap. 4.1, canvas_tent): dil pres hreben, zavreny
    zadni stit, vchod rozdeleny se zavrenou a odhrnutou chlopni; .json navic s polohou tyci a kolicku (lokalni osy stanu).
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
    tent, info = canvas_tent()                                         # plachta stanu na nadvori (na miru)
    for name, (P, UV, F) in tent.items():
        write_fitted(out, name, P, UV, F, "plachta stanu do A na nadvori (navrh_nadvori_stan)", made, extra=info)
    return made


# --- tvary na miru pro stavby: OBJ vystredeny na bounding box + <jmeno>.json se stredem a rozmerem v lokalnich osach
#     stavby (UE cm); stavba podle nej mesh posadi (05 zr_stavby/pristresek.py). Lokalni osy pristresku na vezi:
#     X = u, Y = -v (ram veze je v UE levotocivy: v = osa X otocena o -90 st.), Z = h od VEZ_F
def write_fitted(out, name, P, UV, F, desc, made, extra=None):
    """extra = dalsi klice do .json (napr. poloha tyci a kolicku, v lokalnich osach stavby pred vystredenim)"""
    import json
    mn, mx = P.min(0), P.max(0); c = (mn + mx) / 2
    write_obj_slots(os.path.join(out, name + ".obj"), P - c, UV, smooth_normals(P, F, np.zeros(len(P), int)), F, np.zeros(len(F), int),
                    name, desc, ("Canvas",))
    with open(os.path.join(out, name + ".json"), "w") as f:
        json.dump(dict(center=[round(float(q), 3) for q in c], size=[round(float(q), 3) for q in mx - mn], **(extra or {})), f)
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


# --- plachta stanu do A na nadvori (navrh_nadvori_stan kap. 4.1). Lokalni osy stanu: X podel hrebene (+X = stit
#     se vchodem), Y napric (+Y = strana odhrnute chlopne), Z nahoru od terenu; pocatek na zemi pod stredem hrebene.
#     Plachta lezi na hrebenove tyci (vrch = H) a k zemi ji drzi kolicky na spodnim lemu (lem se mezi nimi zvedne).
TENT = dict(L=240.0, W=220.0, H=190.0,           # pudorys podel hrebene x napric, vrch hrebene (= vrch tyce)
            over=3.0,                            # presah bocnich dilu pres stity
            ridge_r=2.0,                         # zaobleni plachty pres hrebenovou tyc
            sag=4.0, bulge=2.0,                  # prohnuti boku dovnitr, vyduti stitu
            hem=4.0, hem_z=1.0,                  # zvednuti lemu mezi kolicky (na 60 cm), vyska lemu u kolicku nad terenem
            pegs_x=(-120.0, -60.0, 0.0, 60.0, 120.0),     # kolicky na obou bocich
            pegs_back=(-55.0, 55.0),             # kolicky zadniho stitu (-X), krom rohu
            pegs_door=(-55.0,),                  # kolicek zavrene chlopne vchodu
            flap=(205.0, 255.0),                 # uhel odhrnute chlopne kolem jejiho svu (u svu -> u volneho rohu), st.
            step=4.0, seed=21500)


def _lift(q, pegs, hem):
    """zvednuti lemu mezi kolicky: 0 u kolicku, uprostred useku hem * (delka useku / 60 cm)"""
    pg = np.asarray(sorted(pegs), float); q = np.asarray(q, float)
    k = np.clip(np.searchsorted(pg, q) - 1, 0, len(pg) - 2)
    a, b = pg[k], pg[k + 1]; t = np.clip((q - a) / (b - a), 0, 1)
    out = hem * (b - a) / 60.0 * np.sin(math.pi * t)
    return np.where((q < pg[0]) | (q > pg[-1]), hem * 0.15, out)


def _grid_faces(nu, nv, off=0):
    F = []
    for a in range(nu):
        for b in range(nv):
            v00 = off + a * (nv + 1) + b; v10 = v00 + nv + 1
            F += [(v00, v10, v10 + 1), (v00, v10 + 1, v00 + 1)]
    return F


def _rodrigues(p, a, h, ang):
    """otoci body p (n,3) kolem osy bodem a se smerem h (jednotkovy) o ang (n,) radianu"""
    d = p - a; c = np.cos(ang)[:, None]; s = np.sin(ang)[:, None]
    return a + d * c + np.cross(h, d) * s + h * (d @ h)[:, None] * (1 - c)


def canvas_tent(t=TENT):
    """plachta stanu do A -> ({jmeno: (P, UV, F)}, info). Dily: plachta pres hreben (oba boky az k zemi), zadni stit (-X,
    zavreny), vchod (+X) rozdeleny uprostred: chlopen -Y zavrena, chlopen +Y odhrnuta ven (otocena kolem svu k boku).
    info = poloha tyci a kolicku v lokalnich osach stanu (pro stavbu), pred vystredenim (write_fitted)."""
    L, W, H, st = t["L"], t["W"], t["H"], t["step"]; hw = W / 2; x0, x1 = -L / 2, L / 2
    Wn = waves(t["seed"], 10, 12, 50); n_out = lambda sg: np.array([0.0, sg * H, hw]) / math.hypot(H, hw)

    def profile(x, sv):
        """bod boku: x podel hrebene, sv -1..1 napric (0 = hreben, +-1 = lem); -> (n,3)"""
        x = np.asarray(x, float); sv = np.asarray(sv, float); s = np.abs(sv); sg = np.where(sv < 0, -1.0, 1.0)
        y = sv * hw
        e = t["ridge_r"]; z = H * (1 - (np.sqrt(y * y + e * e) - e) / (math.sqrt(hw * hw + e * e) - e))   # zaobleni pres tyc (vrch = H)
        z = z + t["hem_z"] * s                                                   # lem nad terenem
        b = np.clip((s - 0.82) / 0.18, 0, 1) ** 2                                # zvednuti lemu jen u spodniho okraje
        z = z + b * _lift(x, t["pegs_x"], t["hem"])
        mid = 0.35 + 0.65 * np.sin(math.pi * np.clip((x - x0) / L, 0, 1))      # u stitu napnute, uprostred nejvic
        sag = t["sag"] * np.sin(math.pi * s) * mid
        P = np.stack([x, y, z], -1)
        N = np.stack([np.zeros_like(s), sg * H, np.full_like(s, hw)], -1) / math.hypot(H, hw)
        wr = 0.3 * noise(P.reshape(-1, 3), Wn).reshape(s.shape) * np.sin(math.pi * s)
        return P - N * (sag + wr)[..., None]

    parts = {}
    # 1) plachta pres hreben: u podel X (s presahem), v napric (husteji u hrebene)
    nu = int(round((L + 2 * t["over"]) / st)); nv = 2 * int(round(math.hypot(H, hw) / st))
    xs = np.linspace(x0 - t["over"], x1 + t["over"], nu + 1)
    vs = np.linspace(-1, 1, nv + 1); vs = np.sign(vs) * np.abs(vs) ** 1.25
    X, V = np.meshgrid(xs, vs, indexing="ij")
    P = profile(X, V).reshape(-1, 3)
    slen = math.hypot(H, hw)
    UV = np.stack([X / 100, (V + 1) * slen / 100], -1).reshape(-1, 2)
    parts["roof"] = (P, UV, np.array(_grid_faces(nu, nv)))

    # stit: body mezi levym a pravym bokem v rovine x (sv = -s .. +s), s od hrebene (0) k lemu (1)
    def gable(x, w0, w1, sgn_bulge, pegs, seed):
        ns = int(round(slen / st)); nw = max(4, int(round(W * (w1 - w0) / 2 / st)))
        s = np.linspace(0, 1, ns + 1) ** 1.1; w = np.linspace(w0, w1, nw + 1)
        S, Wg = np.meshgrid(s, w, indexing="ij")
        Lp = profile(np.full(S.size, x), -S.ravel()); Rp = profile(np.full(S.size, x), S.ravel())
        f = ((Wg.ravel() + 1) / 2)[:, None]
        Pg = Lp * (1 - f) + Rp * f
        Pg[:, 0] = x                                                           # rovina stitu (bok je u stitu napnuty)
        yb = Pg[:, 1]; bot = np.clip((S.ravel() - 0.85) / 0.15, 0, 1) ** 2      # lem stitu mezi kolicky
        Pg[:, 2] += bot * _lift(yb, pegs, t["hem"]) * (1 - np.abs(Wg.ravel()) ** 8)
        inner = (1 - Wg.ravel() ** 2) * np.sin(math.pi * np.clip(S.ravel(), 0, 1))
        Wg2 = waves(seed, 8, 15, 45)
        Pg[:, 0] += sgn_bulge * t["bulge"] * inner + 0.25 * noise(Pg, Wg2) * inner
        UVg = np.stack([Pg[:, 1] / 100, Pg[:, 2] / 100], -1)
        return Pg, UVg, np.array(_grid_faces(ns, nw)), S.ravel(), Wg.ravel()

    # 2) zadni stit (-X), zavreny, vyduty dovnitr (vitr od zapadu)
    Pg, UVg, Fg, _, _ = gable(x0, -1.0, 1.0, +1.0, (-hw,) + tuple(t["pegs_back"]) + (hw,), t["seed"] + 7)
    parts["back"] = (Pg, UVg, Fg)
    # 3) zavrena chlopen vchodu (-Y), stredovy okraj presahuje 3 cm pres osu
    Pg, UVg, Fg, _, _ = gable(x1, -1.0, 0.03, -1.0, (-hw,) + tuple(t["pegs_door"]) + (2.0,), t["seed"] + 11)
    parts["door_closed"] = (Pg, UVg, Fg)
    # 4) odhrnuta chlopen (+Y): rovinna polovina stitu otocena kolem svu s pravym bokem (hreben -> lem)
    Pg, UVg, Fg, S, Wg = gable(x1, 0.0, 1.0, 0.0, (0.0, hw), t["seed"] + 13)
    A = profile(np.array([x1]), np.array([0.0]))[0]; E = profile(np.array([x1]), np.array([1.0]))[0]
    h = (E - A) / np.linalg.norm(E - A)
    d = Pg - A; r = np.linalg.norm(d - (d @ h)[:, None] * h, axis=1); rmax = r.max()
    a0, a1 = (math.radians(q) for q in t["flap"])
    ang = a0 + (a1 - a0) * (r / rmax) ** 0.8
    test = _rodrigues(Pg[[np.argmax(r)]], A, h, np.array([math.pi / 2]))
    if test[0, 0] < x1: h = -h                                                 # smer otaceni: pres +X ven
    Pf = _rodrigues(Pg, A, h, ang)
    Wf = waves(t["seed"] + 17, 8, 10, 35)
    Pf = Pf + 0.8 * noise(Pf, Wf)[:, None] * (r / rmax)[:, None] * np.array([1.0, 1.0, 0.3])
    Pf = Pf + 1.2 * n_out(1.0)                                                 # odstup od boku (bez pruniku u svu)
    parts["door_open"] = (Pf, UVg, Fg)

    P = np.concatenate([p[0] for p in parts.values()]); UV = np.concatenate([p[1] for p in parts.values()])
    F, off = [], 0
    for p in parts.values():
        F.append(p[2] + off); off += len(p[0])
    F = np.concatenate(F)
    pegs = [[x, sg * hw, 0.0] for sg in (-1, 1) for x in t["pegs_x"]] + [[x0, y, 0.0] for y in t["pegs_back"]] + \
           [[x1, y, 0.0] for y in t["pegs_door"]]
    info = dict(frame="X podel hrebene (+X = vchod), Y napric (+Y = odhrnuta chlopen), Z od terenu; pocatek pod stredem hrebene",
                ridge=dict(z_top=H, d=6.0, x=[x0 - 10.0, x1 + 10.0]), poles=[[x0, 0.0], [x1, 0.0]], pole_d=7.0,
                pegs=pegs, door=dict(x=x1, open_side="+Y"))
    return {"SM_RuinCanvasTent_A": (P, UV, F)}, info
