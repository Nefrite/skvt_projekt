"""gen_constructions.py - vytvori constructions.json pro build_constructions.py (05_constructions)
Dodatecne stavby "druheho zabydleni" zriceniny:
  - tower_floors: drevene vestavby ve vezi (tramy, prkna, pruvlak, schody, podesta); rozmery veze sdili se zriceninou
    pres tools/ruin/tower_spec.py
  - ostroh: krov u ostrohu (ostroh_spec.py, sdileny s 03), kamenna dostavba obytne casti a prkenna podlaha
  - nastaveni volne suti

python gen_constructions.py <ruin_layout_draft.json> <vystup constructions.json> [<03_ruin/blocks/ruin_layout.json>]
Ostroh bere polohy zdi z ruin_layout.json (vychozi ../../03_ruin/blocks/ruin_layout.json).
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ruin"))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))          # zrlib
from tower_spec import VEZ_F, VEZ_ST, spec as tower_spec
from ostroh_spec import spec as ostroh_spec
from zrlib.geom import unit, offset_polyline, cut_polyline, polyline_hits, project_s, point_at

# --- uzavreni obytne casti u ostrohu (05, zricenina se nemeni): jednoradove kamenne dostavby na korunach zdi az pod strechu
#     (ZBudova_V s dvermi v pruchodu a jednim oknem severne od nich (k ZBudova_S), ZBudova_S, vyrovnani koruny hradby mezi tramy),
#     strecha od pricky (hrebenu) na vsechny strany: vejir na hradbu, paprsky na koncich pricky, tramy zpet na ZBudova_V
ADD_T = 0.45                      # tloustka dostavby (m): jedna rada kamenu, vnitrni lic v rovine vnitrniho lice zdi pod ni
# krov: pricka je hreben strechy. Od ni vejir na hradbu (ostroh_spec), paprskove tramy na koncich pricky
# a tramy zpet na dostavbu ZBudova_V; strecha tak klesa od pricky na vsechny strany
E_AT = (1.5, 4.5)                 # tramy z pricky zpet na dostavbu ZBudova_V: poloha na pricce v roztecich tramu vejire
                                  # od konce B (mezi zacatky tramu vejire); jen 2 krajni, nad dvermi dalsi netreba
N_RAD = 3                         # paprskove tramy na kazdem konci pricky (mezi krajnim tramem vejire a smerem ke ZBudova_V)
SLOPE_DOST = 0.25                 # sklon tramu na dostavbu (14 st.); dostavba pod nimi se snizi az pod strechu
DROP_MAX, SLOPE_MIN = 0.8, 0.18   # dlouhe tramy na dostavbu: pokles nejvys DROP_MAX m (ne mene nez SLOPE_MIN = 10 st.), jinak by krytina u rohu klesla pod korunu hradby
SLOPE_RUIN0 = 0.6                 # horni mez sklonu tramu na korunu zriceniny (05 ho polozi na nejvyssi kamen pod nim)
OH_RING = 0.4                     # presah tramu na dostavbu a na korunu za vnejsi lic zdi (m)
DOOR_TOP, LINTEL_BEAR = 2.2, 0.25 # dvere v pruchodu: vrch (m nad terenem; nadprazi se zarovna s oknem), ulozeni nadprazi na kazde strane
# okno severne od dveri (k ZBudova_S): posun od dveri (m podel zdi), sirka = vyklenek strilen hradby v teto casti (w_in 1.4 m,
# nadprazi pak stejne dlouhe jako vnitrni preklad strilny), parapet, vyska
# okno: rozmery sdili ostroh_spec.py (WINDOW; v 03 se v miste okna vybourá puvodni zed)


def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy); return dx / l, dy / l


def _offset(pts, off, ref):
    """polylinie posunuta o off (cm) na stranu bodu ref (pro kazdy usek zvlast, spojeni v prusecicich)"""
    segs = []
    for a, b in zip(pts[:-1], pts[1:]):
        ux, uy = _unit(a, b); nx, ny = -uy, ux
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if (ref[0] - m[0]) * nx + (ref[1] - m[1]) * ny < 0: nx, ny = -nx, -ny
        segs.append(((a[0] + nx * off, a[1] + ny * off), (b[0] + nx * off, b[1] + ny * off)))
    out = [segs[0][0]]
    for (a1, b1), (a2, b2) in zip(segs[:-1], segs[1:]):
        p = _isect_lines(a1, b1, a2, b2); out.append(p or b1)
    out.append(segs[-1][1]); return out


def _isect_lines(a1, b1, a2, b2):
    d1 = (b1[0] - a1[0], b1[1] - a1[1]); d2 = (b2[0] - a2[0], b2[1] - a2[1]); den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-9: return None
    t = ((a2[0] - a1[0]) * d2[1] - (a2[1] - a1[1]) * d2[0]) / den
    return (a1[0] + d1[0] * t, a1[1] + d1[1] * t)


def _ext(pts, e=400.0):
    ext = [list(p) for p in pts]
    ux, uy = _unit(ext[1], ext[0]); ext[0] = [ext[0][0] + ux * e, ext[0][1] + uy * e]
    ux, uy = _unit(ext[-2], ext[-1]); ext[-1] = [ext[-1][0] + ux * e, ext[-1][1] + uy * e]
    return ext


def _hits(pts, other, ext_other=True):
    """pruseciky polylinie pts (konce prodlouzene o 4 m) s polylinii other (taky prodlouzenou)
    -> (prodlouzena pts, seznam (s v cm podel prodlouzene pts, bod))"""
    ext = _ext(pts)
    if ext_other and len(other) > 1 and other[0] != other[1]: other = _ext(other)
    res = []; c = 0.0
    for a, b in zip(ext[:-1], ext[1:]):
        for q, r in zip(other[:-1], other[1:]):
            d1 = (b[0] - a[0], b[1] - a[1]); d2 = (r[0] - q[0], r[1] - q[1]); den = d1[0] * d2[1] - d1[1] * d2[0]
            if abs(den) < 1e-9: continue
            t = ((q[0] - a[0]) * d2[1] - (q[1] - a[1]) * d2[0]) / den; u = ((q[0] - a[0]) * d1[1] - (q[1] - a[1]) * d1[0]) / den
            if 0 <= t <= 1 and -1e-6 <= u <= 1 + 1e-6: res.append((c + t * math.hypot(*d1), (a[0] + d1[0] * t, a[1] + d1[1] * t)))
        c += math.hypot(b[0] - a[0], b[1] - a[1])
    return ext, sorted(res)


def _cut(pts, start_line=None, end_line=None):
    """vyrez polylinie mezi prvnim prusecikem se start_line a poslednim s end_line (konce se pripadne prodlouzi)"""
    ext = _ext(pts)
    s0 = 400.0; L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(ext[:-1], ext[1:])); s1 = L - 400.0
    if start_line: s0 = _hits(pts, start_line)[1][0][0]
    if end_line: s1 = _hits(pts, end_line)[1][-1][0]
    out = []; c = 0.0
    for a, b in zip(ext[:-1], ext[1:]):
        ln = math.hypot(b[0] - a[0], b[1] - a[1])
        if c + ln >= s0 and c <= s1:
            f0 = max(0.0, (s0 - c) / ln); f1 = min(1.0, (s1 - c) / ln)
            p0 = (a[0] + (b[0] - a[0]) * f0, a[1] + (b[1] - a[1]) * f0); p1 = (a[0] + (b[0] - a[0]) * f1, a[1] + (b[1] - a[1]) * f1)
            if not out: out.append(p0)
            out.append(p1)
        c += ln
    return [[round(x, 1), round(y, 1)] for x, y in out]


def _proj_s(pts, p):
    """s (m) nejblizsiho bodu polylinie k p"""
    best = None; c = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        ln = math.hypot(b[0] - a[0], b[1] - a[1]); ux, uy = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
        t = min(max((p[0] - a[0]) * ux + (p[1] - a[1]) * uy, 0), ln)
        q = (a[0] + ux * t, a[1] + uy * t); dd = math.hypot(p[0] - q[0], p[1] - q[1])
        if best is None or dd < best[0]: best = (dd, (c + t) / 100)
        c += ln
    return best[1]


def _pt_s(pts, s):
    c = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        ln = math.hypot(b[0] - a[0], b[1] - a[1]) / 100
        if s <= c + ln or b is pts[-1]:
            f = (s - c) / ln; return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        c += ln


def tower_floors(D):
    """drevo ve vezi (constructions.json -> floors)"""
    TS = tower_spec(D["tower"])
    LT = TS["LT"]; H1, H2 = TS["HATCH1"], TS["HATCH2"]
    floors = [dict(
        name="Vez_Patra", folder="Stavby/Vez", origin=TS["origin"], u=TS["UV"], v=TS["VV"], inner=TS["inner"],
        ref_z=VEZ_F, storey=VEZ_ST, levels=[1, 2], walls=["Vez_V", "Vez_Z", "Vez_J", "Vez_S"],   # tram jen kde zed u kapsy stoji
        beams=dict(v=TS["BEAM_V"], w=0.26, h=0.28, bearing=0.33),
        planks=dict(t=0.05, wmin=0.2, wmax=0.34, missing=0.04),
        girder=dict(u=TS["GIRD_U"], w=0.30, levels=[1, 2], post_v=[TS["GIRD_POST_V"]], post=0.25),
        hatches={"1": H1, "2": H2},
        # provizorni schody 60 st. podel tramu, cik-cak: do 1. patra stoupaji k vychodu (horni konec u vychodniho kraje otvoru),
        # do 2. patra k zapadu (horni konec se opira o pruvlak); z vystupu se prejde do sousedniho pole k dalsim schodum
        stairs=[dict(**{"from": 0, "to": 1}, axis="u", dir=1, u_top=H1[1], v=(H1[2] + H1[3]) / 2, angle=60, width=0.8),
                dict(**{"from": 1, "to": 2}, axis="u", dir=-1, u_top=H2[0], v=(H2[2] + H2[3]) / 2, angle=60, width=0.8)],
        # obnoveny ochoz pred puvodnim vstupem (zvenku Vez_S): 2 tramy zapustene v kapsach, prkna,
        # bez sloupku do zeme - jen kratke sikme vzpery pod tramy oprene o zed
        porch=dict(u=TS["DOOR_U"], level=1, v_wall=LT + 1.25, depth=1.3, width=2.6, beam_du=TS["PORCH_BEAM_DS"],
                   beam=(0.24, 0.28), posts=False, braces=dict(dv=0.75, dz=0.75, w=0.14)),
        # uprava dreva: tar = dehtovane (masivni), raw = bez upravy (vnitrni velke plochy, schody), oil = morene olejem (jemna prace),
        # blood = morene krvi (venkovni ochoz), old = stare neosetrene, zasedle a zaprasene (prkna horniho patra - vic slunce a pocasi)
        finish=dict(beams="tar", girder="tar", posts="tar", heads="tar", planks="raw", planks_2="old", stairs="raw",
                    porch_beams="blood", porch_braces="blood", porch_posts="blood", porch_planks="blood"))]
    return floors


def _ring_beam(p, d, axes):
    """tram z bodu p na pricce ve smeru d: konci na nejblizsi zdi (osa zdi zriceniny); na dostavbe (ZBudova_V, ZBudova_S)
    ma sklon SLOPE_DOST a dostavba se pod nim snizi, na korune zriceniny ho 05 polozi na nejvyssi kamen (SLOPE_RUIN0 = horni mez)"""
    best = None
    for name, (pts, T, rest) in axes.items():
        _, hs = polyline_hits([p, (p[0] + d[0] * 2000, p[1] + d[1] * 2000)], pts, ext_other=False)
        hs = [h for h in hs if h[0] > 400 + 20]                   # pred startem (prodlouzeni o 4 m dozadu) ne
        if hs and (best is None or hs[0][0] < best[0]): best = (hs[0][0], hs[0][1], name, pts, T, rest)
    if best is None: return None
    t, q, name, pts, T, rest = best; t -= 400
    seg = min(zip(pts[:-1], pts[1:]), key=lambda ab: abs((q[0] - ab[0][0]) * (ab[1][1] - ab[0][1]) - (q[1] - ab[0][1]) * (ab[1][0] - ab[0][0])) /
              max(math.hypot(ab[1][0] - ab[0][0], ab[1][1] - ab[0][1]), 1e-6))
    wx, wy = unit(*seg); sin_a = abs(wx * d[1] - wy * d[0])
    return dict(start=[round(p[0], 1), round(p[1], 1)], wall_pt=[round(q[0], 1), round(q[1], 1)],
                slope=max(min(SLOPE_DOST, DROP_MAX / max(t / 100, 0.1)), SLOPE_MIN) if rest == "addon" else SLOPE_RUIN0, sin=round(sin_a, 4), wall_t=T, rest=rest, wall=name, oh=OH_RING)


def _rot(n, deg):
    a = math.radians(deg); return (n[0] * math.cos(a) - n[1] * math.sin(a), n[0] * math.sin(a) + n[1] * math.cos(a))


def _ang(n, d):
    return math.degrees(math.atan2(n[0] * d[1] - n[1] * d[0], n[0] * d[0] + n[1] * d[1]))


def ostroh(LAY):
    """zapadni cast u ostrohu: 2 sloupy u dveri ZBudova_V, pricka (vaznice), z ni 7 paprskovitych tramu na snizenou hradbu
    (tramy lezi ve zlabcich koruny, presahuji vnejsi lic), tramy dokola pricky, krytina; kamenna dostavba; prkenna podlaha
    -> (frames, addons)"""
    OS = ostroh_spec(LAY["walls"])
    WALLS = {w["name"]: w for w in LAY["walls"]}
    EV, ES, HZ = WALLS["ZBudova_V"], WALLS["ZBudova_S"], WALLS[OS["wall"]]
    ROOM = (OS["door"][0] + OS["n"][0] * 300, OS["door"][1] + OS["n"][1] * 300)        # bod uvnitr obytne casti
    def off(w, d): return offset_polyline(w["points"], d * 100, ROOM)
    o_v = EV["thickness"] / 2; o_s = ES["thickness"] / 2; o_h = HZ["thickness"] / 2
    # osy dostaveb (vnitrni lic = vnitrni lic zdi pod nimi) a jejich konce
    line_v = cut_polyline(off(EV, o_v - ADD_T / 2), start_line=off(HZ, o_h), end_line=off(ES, o_s))
    line_s = cut_polyline(off(ES, o_s - ADD_T / 2), start_line=off(EV, o_v - ADD_T), end_line=off(HZ, o_h))
    line_h = cut_polyline(off(HZ, o_h - ADD_T / 2), start_line=off(EV, o_v - ADD_T), end_line=off(ES, o_s - ADD_T))
    # tramy kolem pricky (krome vejire): za poslednim tramem vejire (konec B) paprsky k ZBudova_V, tramy zpet na ZBudova_V
    # od konce B ke konci A, paprsky na konci A az k prvnimu tramu vejire -> poradi dokola (pole krytiny mezi sousedy)
    axes = {"ZBudova_V": (EV["points"], EV["thickness"], "addon"), "ZBudova_S": (ES["points"], ES["thickness"], "addon"),
            OS["wall"]: (HZ["points"], HZ["thickness"], "ruin")}
    n = OS["n"]; back = (-n[0], -n[1]); A, B = OS["fan_ends"]
    dirs = [unit(b["start"], b["wall_pt"]) for b in OS["beams"]]
    def radials(p, d_fan):
        th = _ang(n, d_fan); sg = 1 if th > 0 else -1
        return [_ring_beam(p, _rot(n, th + sg * (180 - abs(th)) * k / (N_RAD + 1)), axes) for k in range(1, N_RAD + 1)]
    nf = len(OS["beams"]) - 1                                     # zacatky tramu vejire jsou po 1/nf pricky
    east = [_ring_beam((B[0] + (A[0] - B[0]) * e / nf, B[1] + (A[1] - B[1]) * e / nf), back, axes) for e in E_AT]
    ring = [dict(id="PB", beams=[b for b in radials(B, dirs[-1]) if b]), dict(id="E", beams=[b for b in east if b]),
            dict(id="PA", beams=[b for b in radials(A, dirs[0]) if b][::-1])]
    s_door = project_s(line_v, OS["door"]); WINDOW = OS["window"]
    # bocni odsazeni osy zdi zriceniny ZBudova_V od osy dostavby V (m, kladne = vlevo po smeru line_v): malta pod dostavbou
    # tam, kde v jeji rovine chybi licovy kamen, jde do prostredni vrstvy (jadra) zdi
    pa, pb = point_at(line_v, s_door), point_at(line_v, s_door + 0.1); du = unit(pa, pb)
    q = point_at(EV["points"], project_s(EV["points"], pa))
    mid_off = ((q[0] - pa[0]) * -du[1] + (q[1] - pa[1]) * du[0]) / 100
    addon = dict(name="Ostroh_Dostavba", type="stone_addon", roof="Ostroh_Krov", folder="Stavby/Ostroh",
                 # kamen z rozvalin hradu: stejne velky jako ve zdech (STONE_MIN/MAX, COURSE_MIN/MAX), jedna rada pres celou tloustku
                 stone=dict(t=ADD_T, len=(LAY["params"]["STONE_MIN"], LAY["params"]["STONE_MAX"]),
                            course=(LAY["params"]["COURSE_MIN"], LAY["params"]["COURSE_MAX"]), joint=LAY["params"]["JOINT"]),
                 mortar=0.10,                                       # maltove jadro 10 cm uprostred zdi: zastavi svetlo ve sparach
                 mortar_down=["V"],                                 # ... a v dostavbe V pokracuje az do zeme ve zdi zriceniny pod ni
                 clear_rubble=True,                                 # sut uvnitr obytne casti uklizena
                 walls=[dict(name="V", pts=line_v, mid_off=round(mid_off, 3), openings=[
                            dict(kind="door", s=round(s_door, 3), w=OS["pass_w"], top=DOOR_TOP, align=1),   # nadprazi dveri ve vysce nadprazi okna
                            dict(kind="window", s=round(s_door + WINDOW["ds"], 3), w=WINDOW["w"], sill=WINDOW["sill"], top=WINDOW["sill"] + WINDOW["h"],
                                 sill_crown=True)]),                  # okno az na korunu zriceniny (v 03 vybourana nad parapetem)
                        dict(name="S", pts=line_s, openings=[]),
                        dict(name="H", pts=line_h, openings=[])],
                 lintel=dict(bear=LINTEL_BEAR, half=True),   # nadprazi o pul rady vys, podlozene a dorovnane pulenymi kameny
                 finish=dict(lintels="old", threshold="old"))
    # prah dveri: samostatny actor (soucast dostavby, rucne posunuty se ulozi pres capture), v linii dostavby pres jeji tloustku, 1.5 cm nad podlahou
    pd = point_at(line_v, s_door); pd2 = point_at(line_v, s_door + 0.1)
    addon["threshold"] = dict(pos=[round(pd[0], 1), round(pd[1], 1)], yaw=round(math.degrees(math.atan2(pd2[1] - pd[1], pd2[0] - pd[0])), 2),
                     len=round(OS["pass_w"] - 0.01, 3), depth=round(ADD_T - 0.01, 3),
                     floor="Ostroh_Podlaha", over=0.015, sink=0.05)

    # --- prkenna podlaha v obytne casti u ostrohu: podvaly na zemi, prkna podel ZBudova_V; obrys = vnitrni lice zdi zriceniny
    f_v = cut_polyline(off(EV, o_v), start_line=off(HZ, o_h), end_line=off(ES, o_s))
    f_s = cut_polyline(off(ES, o_s), start_line=off(EV, o_v), end_line=off(HZ, o_h))
    f_h = cut_polyline(off(HZ, o_h), start_line=off(EV, o_v), end_line=off(ES, o_s))
    floor = dict(name="Ostroh_Podlaha", type="plank_floor", folder="Stavby/Ostroh",
                 outline=f_v + f_s + f_h[::-1], inset=0.02, u=OS["u"], n=OS["n"],
                 avoid=[OS["posts"]],                              # sloupy krovu: prkna kolem nich vyriznuta
                 post=OS["post"],
                 sleepers=dict(w=0.14, h=0.10, step=0.8, seg=1.2), # podvaly napric prkny (po 0.8 m), lezi na zemi, kusy po 1.2 m
                 planks=dict(t=0.045, w=(0.22, 0.32), gap=0.006, len=(2.4, 4.5)),
                 finish=dict(sleepers="tar", planks="raw"))          # podvaly dehtovane (zeme), prkna bez upravy (jako ve vezi)

    frames = [dict(name="Ostroh_Krov", type="fan_roof", folder="Stavby/Ostroh", **OS,
                   crossbeam=(0.30, 0.32), start_over=0.15,         # tramy 15 cm za pricku (hreben)
                   knee=dict(l=0.6, w=0.14, out=True),               # kratke sikme vzpery sloup - pricka, ven (pruchod mezi sloupy volny)
                   ring=ring, ring_closed=True,                      # tramy dokola pricky (poradi navazuje na vejir B0..B6)
                   ridge=dict(w=0.26, t=0.035),                      # hrebenova prkna pres pricku (obe strany)
                   # krytina: dehtovana prkna po spadu na latich, listy pres spary, kryci prkno pres kazdy tram
                   roof=dict(lath=(0.05, 0.06), board_t=0.035, board_w=(0.22, 0.30), gap=0.015, batten=(0.10, 0.035), top_over=0.2,   # listy 10 cm pres spary 1.5 cm
                             lath_rows=(0.04, 0.35, 0.65, 0.9, 1.0), cover_w=0.36, flashing=None),   # lemovani u pricky: vyresi se jinak
                   finish=dict(posts="tar", crossbeam="tar", beams="tar", knee="tar",
                               roof_boards="tar", roof_battens="tar", roof_laths="tar", roof_flashing="tar"))]
    return frames, [addon, floor]


if __name__ == "__main__":
    D = json.load(open(sys.argv[1]))
    LAY = json.load(open(sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "..", "..", "03_ruin", "blocks", "ruin_layout.json")))
    floors = tower_floors(D)
    frames, addons = ostroh(LAY)
    out = dict(version=1, units="UE cm (pozice), m (rozmery v ramu veze)",
               note="Drevene vestavby a sut. Zricenina (zdi, kapsy, dlazba) je v 03_ruin/blocks/ruin_layout.json.",
               rubble=dict(enabled=True, folder="Stavby/Sut"),
               floors=floors, frames=frames, addons=addons)
    json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
    print("stavby:", ", ".join(f["name"] for f in floors + frames + addons), "| sut:", out["rubble"]["enabled"])
