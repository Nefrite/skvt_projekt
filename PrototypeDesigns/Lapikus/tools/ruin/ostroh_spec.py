"""ostroh_spec.py - spolecne rozmery dreveneho zastreseni v zapadni casti hradu u ostrohu (03 i 05).
03 (gen_layout.py): hradba se v teto casti cilene snizi a zarovna (cap) a do koruny se vysekaji zlabky pro tramy (notches).
05 (gen_constructions.py): dva sloupy u dveri ZBudova_V, pricka (vaznice) mezi nimi, z ni paprskovite tramy na hradbu.
Kdyz se tu neco zmeni, pregeneruj gen_layout.py i gen_constructions.py a postav 03 i 05."""
import math, os, sys
_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if _ROOT not in sys.path: sys.path.insert(0, _ROOT)
from zrlib.geom import polyline_len as _len, point_at as _pt     # noqa: E402  (sdilena geometrie)

WALL = "Hradba_Z_S"              # hradba, na kterou tramy dosedaji
ENTRY = ("ZBudova_V", 6.0)       # zed a s (m) dveri, u kterych stoji sloupy
INSIDE_REF = "ZBudova_S"         # zed, ktera vede do zastresene casti (urcuje stranu "dovnitr")
PLATEAU = 3129                   # teren uvnitr (abs. cm) - pro vysku snizene hradby
CAP_H = 3.3                      # snizena a zarovnana hradba: vrch nejvys CAP_H m nad terenem (posledni cela rada pod touto vyskou)
POST = 0.28                      # sloup (m, ctverec)
POST_GAP = 0.02                  # sloup tesne u vnitrniho lice ZBudova_V
PASS_W = 1.6                     # skutecna sirka pruchodu ve zdi (dvere 1 m + vylamane osteni, zmereno v 03): sloupy stoji
                                 # po stranach pruchodu, souběžne s jeho hranami (pruchod zustava volny)
POST_SPREAD = 0.10               # sloupy jeste o tolik m dal od hrany pruchodu (kazdy)
CROSS_OVER = 0.85                # pricka presahuje sloupy na kazde strane (m) - az za hlavy sikmych vzper (0.6 m)
N_BEAMS = 7                      # paprskovite tramy
FAN = 66.0                       # vejir tramu +-FAN stupnu od smeru dovnitr (kolmo na ZBudova_V)
BEAM = (0.22, 0.24)              # prurez tramu (sirka, vyska) m
NOTCH_D = 0.5                    # zlabek do poloviny vysky tramu
RISE = 0.8                       # pricka (spodek tramu) o tolik m vys nez dno zlabku u vnitrniho lice -> strecha se mirne zvazuje ke zdi
OVERHANG = 0.6                   # tram presahuje vnejsi lic hradby (okap)
LATH = 0.05                      # late krytiny na tramech (05) - kvuli zarovnani koruny pod strechou


def spec(walls):
    """walls = seznam zdi z ruin_layout (name, points, thickness). Vrati rozmery (UE cm, s v m)."""
    W = {w["name"]: w for w in walls}
    ev = W[ENTRY[0]]["points"]; hz = W[WALL]["points"]
    D = _pt(ev, ENTRY[1])
    ux, uy = ev[1][0] - ev[0][0], ev[1][1] - ev[0][1]; ul = math.hypot(ux, uy); ux, uy = ux / ul, uy / ul
    nx, ny = uy, -ux
    # dovnitr = do zapadni casti (tam, kam vede ZBudova_S od rohu u ZBudova_V)
    L = _len(hz); far = W[INSIDE_REF]["points"][-1]
    if (far[0] - D[0]) * nx + (far[1] - D[1]) * ny < 0: nx, ny = -nx, -ny
    post_in = W[ENTRY[0]]["thickness"] / 2 + POST / 2 + POST_GAP          # od osy zdi ke stredu sloupu
    post_half = PASS_W / 2 + POST / 2 + POST_SPREAD
    M = (D[0] + nx * post_in * 100, D[1] + ny * post_in * 100)
    posts = [(M[0] + ux * post_half * 100, M[1] + uy * post_half * 100), (M[0] - ux * post_half * 100, M[1] - uy * post_half * 100)]
    # konce tramu: paprsky ze stredu mezi sloupy do vejire +-FAN st. od smeru dovnitr, prusecik s osou hradby
    def hit(px, py, dx, dy, pts):
        best = None; c = 0.0
        for i in range(len(pts) - 1):
            ax_, ay_ = pts[i]; bx_, by_ = pts[i + 1]; ex, ey = bx_ - ax_, by_ - ay_; ln = math.hypot(ex, ey) / 100
            den = dx * ey - dy * ex
            if abs(den) > 1e-9:
                t = ((ax_ - px) * ey - (ay_ - py) * ex) / den; f = ((ax_ - px) * dy - (ay_ - py) * dx) / den
                if t > 50 and 0 <= f <= 1 and (best is None or t < best[0]): best = (t, c + f * ln)
            c += ln
        return best
    ends = []
    for i in range(N_BEAMS):
        th = math.radians(-FAN + 2 * FAN * i / (N_BEAMS - 1))
        dx = nx * math.cos(th) - ny * math.sin(th); dy = nx * math.sin(th) + ny * math.cos(th)
        h = hit(M[0], M[1], dx, dy, hz)
        if h: ends.append(h[1])
    if len(ends) < 2: raise RuntimeError("ostroh_spec: paprsky nezasahly %s" % WALL)
    s0, s1 = min(ends), max(ends)
    T = W[WALL]["thickness"]
    beams = []
    # tramy rozlozene po cele pricce vcetne presahu (pricka je kratka, sloupy jsou u pruchodu)
    sh_ = (post_half + CROSS_OVER - BEAM[0] / 2 - 0.05) * 100
    starts = [(M[0] + ux * sh_ * (2 * i / (N_BEAMS - 1) - 1), M[1] + uy * sh_ * (2 * i / (N_BEAMS - 1) - 1)) for i in range(N_BEAMS)]
    # poradi: kazdy tram k nejblizsimu konci (bez krizeni) - seradit oboji podle uhlu kolem dveri
    ang = lambda q: math.atan2(q[1] - D[1], q[0] - D[0])
    ref = ang((M[0] + nx * 100, M[1] + ny * 100))
    rel = lambda q: (ang(q) - ref + math.pi) % (2 * math.pi) - math.pi
    starts.sort(key=rel); ends.sort(key=lambda s: rel(_pt(hz, s)))
    for st, se in zip(starts, ends):
        p = _pt(hz, se); q = _pt(hz, min(se + 0.1, L))
        wx, wy = (q[0] - p[0]), (q[1] - p[1]); wl = math.hypot(wx, wy) or 1
        bx, by = p[0] - st[0], p[1] - st[1]; bl = math.hypot(bx, by)
        sin_a = abs((wx * by - wy * bx) / (wl * bl))           # uhel tramu ke zdi
        d_in = bl / 100 - (T / 2) / max(sin_a, 0.35)            # vodorovne od pricky k vnitrnimu lici hradby (m)
        # normala hradby dovnitr (k pricce)
        mx, my = -wy / wl, wx / wl
        if mx * (st[0] - p[0]) + my * (st[1] - p[1]) < 0: mx, my = -mx, -my
        # tram jde ke zdi sikmo: v miste posunutem o off (cm) od osy zdi dovnitr lezi zlabek na s + off * k / 100
        bux, buy = bx / bl, by / bl
        k = (bux * wx / wl + buy * wy / wl) / (bux * mx + buy * my)
        beams.append(dict(start=[round(st[0], 1), round(st[1], 1)], wall_s=round(se, 3), wall_pt=[round(p[0], 1), round(p[1], 1)], k=round(k, 4),
                          notch_w=round(BEAM[0] / max(sin_a, 0.35) + 0.08, 3), length=round(bl / 100, 2),
                          slope=round(RISE / d_in, 4), d_in=round(d_in, 3), wall_in=[round(mx, 5), round(my, 5)], sin=round(sin_a, 4),
                          dir=[round(bux, 5), round(buy, 5)]))
    return dict(post=POST, crossbeam_over=CROSS_OVER, pass_w=PASS_W, posts=[[round(x, 1), round(y, 1)] for x, y in posts], door=[round(D[0], 1), round(D[1], 1)],
                u=[round(ux, 5), round(uy, 5)], n=[round(nx, 5), round(ny, 5)], beams=beams,
                cap=dict(s0=round(s0 - 1.6, 2), s1=round(s1 + 1.6, 2), z=PLATEAU + CAP_H * 100),
                # zlabek: u vnitrniho lice hloubka d, ven hloubsi podle sklonu tramu (tram lezi v celem zlabku)
                notches=[dict(s=b_["wall_s"], w=b_["notch_w"], d=round(BEAM[1] * NOTCH_D, 3), slope=round(b_["slope"] / max(b_["sin"], 0.35), 4),
                              pt=b_["wall_pt"], nin=b_["wall_in"], t=T, k=b_["k"], dir=b_["dir"], bw=BEAM[0]) for b_ in beams],
                # koruna pod strechou: kameny nesmi prekazet latim a prknum mezi tramy -> vrch zdi ven ve sklonu strechy
                roof_clear=dict(clear=round(BEAM[1] * (1 - NOTCH_D), 3), margin=0.02),      # pod vrch tramu (late lezi na tramech)
                beam=list(BEAM), rise=RISE, overhang=OVERHANG, wall=WALL, wall_t=T)
