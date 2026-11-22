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
CAP_EXT = 4.0                    # snizeni hradby jeste o tolik m za krajni tramy vejire (pod krytinu paprskovych tramu na koncich pricky)
CAP_H = 3.3                      # snizena a zarovnana hradba: vrch nejvys CAP_H m nad terenem (posledni cela rada pod touto vyskou)
POST = 0.28                      # sloup (m, ctverec)
POST_GAP = 0.02                  # mezera sloupu od vnitrniho lice ZBudova_V ...
POST_SHIFT = 1.0                 # ... a sloupy jeste o tolik m dal do prostoru (pricka = hreben strechy; od ni tramy i zpet na ZBudova_V)
PASS_W = 1.6                     # skutecna sirka pruchodu ve zdi (dvere 1 m + vylamane osteni, zmereno v 03): sloupy stoji
                                 # po stranach pruchodu, souběžne s jeho hranami (pruchod zustava volny)
POST_SPREAD = 0.10               # sloupy jeste o tolik m dal od hrany pruchodu (kazdy)
CROSS_OVER = 0.85                # pricka presahuje sloupy na kazde strane (m) - az za hlavy sikmych vzper (0.6 m)
N_BEAMS = 7                      # paprskovite tramy
FAN = 66.0                       # vejir tramu +-FAN stupnu od smeru dovnitr (kolmo na ZBudova_V)
BEAM = (0.22, 0.24)              # prurez tramu (sirka, vyska) m
NOTCH_D = 0.5                    # zlabek do poloviny vysky tramu
RISE = 1.2                       # pricka (spodek tramu) o tolik m vys nez dno zlabku u vnitrniho lice -> sklon vejire 11-17 st.
OVERHANG = 0.6                   # tram presahuje vnejsi lic hradby (okap)
# okno v dostavbe ZBudova_V (05): ds = m od dveri k ZBudova_S, sirka, parapet a vyska (m nad terenem). V 03 se v miste okna
# vybourá puvodni zed nad WINDOW_CUT (edits -> cut), aby okno nebylo zastavene zriceninou ("odladene" pri dostavbe)
WINDOW = dict(ds=3.4, w=1.25, sill=1.4, h=0.8)
WINDOW_CUT = dict(z0=1.4, inset=0.1)      # od z0 m nad patou zdi nahoru, o inset m uzsi nez okno (kameny presahujici do otvoru zmizi cele)
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
    post_in = W[ENTRY[0]]["thickness"] / 2 + POST / 2 + POST_GAP + POST_SHIFT   # od osy zdi ke stredu sloupu
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
    # konce pricky: A u prvniho tramu vejire (B0), B u posledniho; tramy vejire zacinaji sh_ od stredu
    ends = [(M[0] - ux * sh_ * sgn, M[1] - uy * sh_ * sgn) for sgn in (1, -1)]
    if math.hypot(ends[0][0] - beams[0]["start"][0], ends[0][1] - beams[0]["start"][1]) > math.hypot(ends[1][0] - beams[0]["start"][0], ends[1][1] - beams[0]["start"][1]):
        ends = ends[::-1]
    return dict(post=POST, crossbeam_over=CROSS_OVER, fan_ends=[[round(x, 1), round(y, 1)] for x, y in ends], center=[round(M[0], 1), round(M[1], 1)], pass_w=PASS_W, posts=[[round(x, 1), round(y, 1)] for x, y in posts], door=[round(D[0], 1), round(D[1], 1)],
                u=[round(ux, 5), round(uy, 5)], n=[round(nx, 5), round(ny, 5)], beams=beams,
                cap=dict(s0=round(s0 - CAP_EXT, 2), s1=round(s1 + CAP_EXT, 2), z=PLATEAU + CAP_H * 100),
                # zlabek: u vnitrniho lice hloubka d, ven hloubsi podle sklonu tramu (tram lezi v celem zlabku)
                notches=[dict(s=b_["wall_s"], w=b_["notch_w"], d=round(BEAM[1] * NOTCH_D, 3), slope=round(b_["slope"] / max(b_["sin"], 0.35), 4),
                              pt=b_["wall_pt"], nin=b_["wall_in"], t=T, k=b_["k"], dir=b_["dir"], bw=BEAM[0]) for b_ in beams],
                # koruna pod strechou: kameny nesmi prekazet latim a prknum mezi tramy -> vrch zdi ven ve sklonu strechy
                roof_clear=dict(clear=round(BEAM[1] * (1 - NOTCH_D), 3), margin=0.02),      # pod vrch tramu (late lezi na tramech)
                beam=list(BEAM), rise=RISE, overhang=OVERHANG, wall=WALL, wall_t=T, window=dict(WINDOW),
                window_cut=dict(op="cut", wall=ENTRY[0], s0=round(ENTRY[1] + WINDOW["ds"] - WINDOW["w"] / 2 + WINDOW_CUT["inset"], 3),
                                s1=round(ENTRY[1] + WINDOW["ds"] + WINDOW["w"] / 2 - WINDOW_CUT["inset"], 3), z0=WINDOW_CUT["z0"], z1=20.0,
                                _="okno dostavby u ostrohu (ostroh_spec.py)"))


# ------------------------------------------------------------------ vybaveni Guesthouse (06_furnishing, typ props)
# Ram skupiny = ram podlahy Ostroh_Podlaha (constructions.json): a = s podel vnitrniho lice ZBudova_V od jizniho rohu
# k severu (0 - 12,36 m), c = n do mistnosti k zapadu. Dvere s = 6,16 - 7,76, okno s = 9,74 - 10,99 (parapet 1,4 m).
# Graybox (21. 11. 2026, overeni meritka s postavou): kvadry (Cube, MI_PrototypeGrid_Gray z LevelPrototyping), rozmery jako budouci meshe.
GH_BED = dict(s=(1.847, 4.348), n0=0.39, size=(250.2, 109.1, 95.0))  # postel podel vychodni zdi, 39 cm od ni (pohodlna: Jirka 21. 11. 2026 podle postavy 180 cm)
GH_DESK = dict(s=10.382, n0=0.07, size=(125.0, 75.0, 78.0))        # pracovni stul pro jednoho pod oknem (novy mesh SM_RuinDesk), vyska 78 cm
GH_STOOL = dict(c=1.272, size=(36.1, 34.6, 47.0))                  # stolicka u stolu, sedatko 47 cm (SM_RuinStool skala 1,035)
GH_CHEST = dict(a=4.73, c=0.93, x=(0, -1), size=(94.2, 54.2, 50.7))   # truhla v nohach postele, delsi strana kolmo ke zdi, zamek (-Y) k severu
GH_ARMOR = dict(a=10.125, c=5.677, x=(-0.766, 0.6428), size=(60.1, 60.3, 175.0))   # stojan na brneni u hradby na severozapade (prazdny; poloha Jirka 21. 11. 2026)
GH_WEAPONS = dict(a=7.205, c=6.757, x=(-0.9848, -0.1736), size=(100.0, 40.0, 160.0))   # stojan na zbrane u hradby naproti dverim (prazdny; Jirka 21. 11. 2026)
GH_SHELF = dict(a=12.10, c=1.719, size=(156.2, 40.0, 200.0))        # regal na dalsi veci u severni zdi ZBudova_S (misto stojanu na zbrane; rozmer a poloha Jirka 21. 11. 2026, 6 cm od kamenu zdi)
GH_WOOD = dict(off=1.05, back=0.05, size=(80.0, 40.0, 60.0))       # hromadka dreva vedle pece podel hradby: posun od stredu pece po ose x (m),
                                                                   # k hradbe (m; pec 0,9 m hluboka, hromadka 0,4 m), rozmery cm
GH_OVEN = dict(a=3.12, c=4.10, x=(0.67, 0.74), size=(100.0, 90.0, 120.0))   # ZASTUPCE pece (05, stavitel): zady k hradbe
                                                                   # v jihozapadnim klinu, komin mezi tramy vejire B0 a B1
# hotove meshe (Katalog_props, 22. 11. 2026): id kusu -> (shape, finish); ostatni kusy zustavaji graybox. Natoceni podle os meshe:
# postel hlava -X (x = (1, 0) -> hlava k jihu), truhla zamek -Y, stojan celo -Y (zady k hradbe). Nabytek hosta: olej.
GH_MESH = {"Postel": ("bed_large", "oil"), "Stolicka": ("stool", "oil"), "Truhla": ("chest_locked", "oil"),
           "Stojan_Brneni": ("armor_stand", "oil")}
GH_REF = (6.96, 2.0)                                               # bod, od jehoz terenu se meri vysky (podlaha je vodorovna)


def _wood_at():
    """stred hromadky dreva vedle pece: po ose x pece (podel hradby, od postele), zady k hradbe"""
    ox, oc = GH_OVEN["x"]; ln = (ox * ox + oc * oc) ** 0.5; ox, oc = ox / ln, oc / ln
    nx, nc = oc, -ox                                                # do mistnosti (od hradby)
    if nx < 0: nx, nc = -nx, -nc
    a = GH_OVEN["a"] + ox * GH_WOOD["off"] - nx * GH_WOOD["back"]; c = GH_OVEN["c"] + oc * GH_WOOD["off"] - nc * GH_WOOD["back"]
    return a, c


def guesthouse_vybaveni(floor_z, graybox=True):
    """vybaveni Guesthouse -> seznam kusu v ramu podlahy (m). floor_z = vrch prken podlahy v m nad terenem v bode GH_REF
    (pocita gen_furnishing.py z Ostroh_Podlaha). graybox = kvadry bez meshe (cat "graybox" -> Cube, MAT_GRAYBOX)."""
    fz = round(floor_z, 3)
    def gb(id_, a, c, size):
        if id_ in GH_MESH:                                          # hotovy mesh (size = jmenovity rozmer, u stolicky skala 1,035)
            shape, fin = GH_MESH[id_]
            return dict(id=id_, shape=shape, finish=fin, a=round(a, 3), c=round(c, 3), z=fz, ref=list(GH_REF), size=list(size))
        return dict(id=id_, cat="graybox", a=round(a, 3), c=round(c, 3), z=fz, ref=list(GH_REF), size=list(size))
    b = GH_BED; d = GH_DESK; s = GH_STOOL
    return [gb("Postel", sum(b["s"]) / 2, b["n0"] + b["size"][1] / 200, b["size"]),
            gb("Stul", d["s"], d["n0"] + d["size"][1] / 200, d["size"]),
            gb("Stolicka", d["s"], s["c"], s["size"]),
            dict(gb("Truhla", GH_CHEST["a"], GH_CHEST["c"], GH_CHEST["size"]), x=list(GH_CHEST["x"])),
            dict(gb("Stojan_Brneni", GH_ARMOR["a"], GH_ARMOR["c"], GH_ARMOR["size"]), x=list(GH_ARMOR["x"])),
            dict(gb("Stojan_Zbrane", GH_WEAPONS["a"], GH_WEAPONS["c"], GH_WEAPONS["size"]), x=list(GH_WEAPONS["x"])),
            dict(gb("Regal", GH_SHELF["a"], GH_SHELF["c"], GH_SHELF["size"]), x=[0, 1]),
            dict(gb("Drevo_Pec", *_wood_at(), GH_WOOD["size"]), x=list(GH_OVEN["x"])),
            # pec je pevna stavba (05): zde jen docasny kvadr pro rozvrzeni, po postaveni pece stavitelem se odebere
            dict(gb("Pec_Zastupce", GH_OVEN["a"], GH_OVEN["c"], GH_OVEN["size"]), x=list(GH_OVEN["x"]))]
