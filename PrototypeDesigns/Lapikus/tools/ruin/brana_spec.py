"""brana_spec.py - spolecne rozmery strazniho stanoviste nad branami a premosteni sijoveho prikopu (03, 05, 06),
navrhy Docs/structures/navrh_brana_straz.md a Docs/structures/navrh_brana_prikop.md.
Ram brany: pocatek = SZ roh strazni veze (prusecik os Brana_S a Brana_J), u (m) podel Brana_S k vychodu, d (m) kolmo k jihu.
Vysky jsou ABSOLUTNE v UE cm (Z): teren v prujezdu je sikmy a zdi maji kazda jinou patu (Brana_V ma podstavbu a z_offset).
Stav dat 16.-23. 11. 2026 (polohy zdi prevzate z levelu): koruna Brana_V 3617-3654, vrch vychodniho oblouku 3529, koruna Brana_J
3455-3549, Brana_S 3459-3552, prah 1. brany Z 3040, dno sijoveho prikopu Z 2700.
03 (gen_layout.py -> prikop_walls, ruin_edits): kapsy pro tramy a vnejsi ozub prahu v Brana_V, pilir Brana_Pilir a opera Brana_Opera.
05 (gen_constructions.py -> brana): Brana_Straz_Kamen, Brana_Straz_Podesta, Brana_Straz_Kryty, Brana_Most_Kamen, Brana_Most, Brana_Zataras.
Kdyz se tu neco zmeni, pregeneruj gen_layout.py i gen_constructions.py a postav 03 (cast Obvod) i 05.
entities: [Brana, Brana_Straz, Strazni_Vez]
docs: [navrh_brana_straz, stav_brana_straz, navrh_brana_prikop, stav_brana]
build_step: 03_ruin
domains: structures"""
import math

WALL_S, WALL_J, WALL_V = "Brana_S", "Brana_J", "Brana_V"
WALL_PILIR, WALL_OPERA = "Brana_Pilir", "Brana_Opera"

B_BEAM_Z = 3552.0                # spodek tramu (UE cm) = spara rad Brana_V (rada 3552-3585 nad obloukem brany, vrch oblouku 3529);
                                 # kapsa se zarovnava na rady kamene -> pri zmene zdi zmer znovu (run_checks.py --only brana)
B_BEAM = dict(d=0.24, pos=(0.8, 2.2, 3.6, 5.0),                  # tramy: loupana kulatina, polohy d (m); rozpeti 5.4 m mezi lici;
                                                                 # 4 kusy v kapsach Brana_V po 1.4 m (Jirka 23. 11. 2026: zvyseno ze 4 na 5 kulatin celkem,
                                                                 # aby zapadni sloupky strisky d = 0.78 a 3.57 m staly nad 2. a 4. kulatinou), prkna 5 cm na 1.4 m
              wall=dict(d=-0.2, u=(0.1, 6.2)),                   # 1. (severni) tram lezi na vyrovnane korune Brana_S (podesta saha az nad zed)
              u=(0.1, 6.63))                                     # od - do: na zapade 0.8 m na korune Brana_J, na vychode 0.33 m v kapse
B_POCKET = dict(w=0.32, h=0.33)  # kapsa v Brana_V: sirka, vyska (= rada kamene), hloubka = licovy kamen (0.38 m)
B_LEVEL = dict(u=(0.2, 0.65), d=(0.65, 5.3), bottom=3440.0)      # vyrovnavaci rada z kamene rozvalin na korune Brana_J (vrch = spodek tramu);
                                 # bottom = nejnizsi spodek (cm): pod korunou (3455) je portal a dutiny ve zdi, ty se nezazdivaji
B_LEVEL_V = dict(depth=0.38, d=(1.1, 5.2), bottom=3480.0)       # podlozeni tramu ve vnitrnim lici Brana_V: nad obloukem brany a u Brana_S
                                 # chybi pod kapsami licovy kamen (mezera 26-39 cm) -> doplni se kamenem z rozvalin
B_LEVEL_S = dict(u=(0.2, 6.25), d=(-0.45, 0.05), bottom=3440.0)  # vyrovnani koruny Brana_S pod tramem na zdi
B_DECK = dict(u=(0.2, 6.27), d=(-0.55, 5.25), t=0.05, w=(0.22, 0.32), gap=0.006)   # prkna kolmo na tramy; na vychode k lici Brana_V,
                                 # na severu az nad Brana_S k severnimu krytu (Jirka 16. 11. 2026: za krytem se nema dat stoupnout)
B_RAIL = dict(h=1.0, post_d=0.10, post_step=1.5, rail_d=0.08, levels=(0.5, 0.95), inset=0.07)   # zabradli: sloupky a 2 tyce s kurou
B_RAIL_SOUTH_END = 4.3           # jizni zabradli konci na linii vychodniho lice Hradba_V (dal k vychodu jizni kryt z kulatiny)
B_RAILS = False                  # Jirka 16. 11. 2026: zabradli smerem do hradu se nestavi (bude tudy vylez na podestu)
# vychodni kryt z kulatiny (typ palisade, sada base): kuly s kurou na korune Brana_V, 0.3 m vychodne od osy zdi
B_COVER_E = dict(off=0.30, d=(-0.64, 5.35),                       # osa krytu od osy Brana_V (m), rozsah d
                 top=1.80, stake_d=(0.18, 0.22), gap=0.01, jit=0.04, sink=0.25, min_len=0.5,   # vrch nad podlahou (m); sink: kuly
                                                                 # "utopene" 25 cm ve vydlabane korune zdi (Jirka 16. 11. 2026)
                 slits=(1.5, 3.1, 4.6), slit_w=0.14, slit_bottom=1.35,                       # pruzory: polohy d, sirka, spodek nad podlahou;
                                                                 # kul v pruzoru je rovne seriznuty (bez spicky)
                 rail_d=0.10, rails=(0.55, 1.22), rail_d0=-0.5)  # rahna zevnitr: u spodu (nad korunou zdi) a tesne pod pruzory
# SV narozi: kameny koruny Brana_V nad urovni paty krytu posadka rozebrala (03, cap) - kryt jde pres narozi bez mezery
B_CUT_NE = dict(d1=0.75, z=3618.0)                               # Brana_V od severniho konce po d1: jen cele rady pod z (cm)
# severni kryt (sada final): na vnitrnim okraji koruny Brana_S po cele delce, prsni vysky (strili se pres vrch), bez pruzoru
B_COVER_N = dict(d=-0.75, u=(0.0, 7.6), top=1.25, sink=0.25,     # u vnejsi hrany Brana_S (vnejsi lic), za krytem neni kam stoupnout
                 slits=(1.8, 3.7, 5.6), slit_bottom=0.90,        # pruzory: polohy u, spodek nad podlahou
                 rails=(0.45, 0.78))                             # rahna: nad korunou Brana_V v narozi a tesne pod pruzory
# jizni kryt (sada final): na jiznim okraji podesty, od vychodniho krytu do dvou tretin sirky (po Hradba_V); zapadni tretina
# zustava otevrena (vylez na podestu). Kuly stoji na podlaze, na vychode na korune Brana_V.
B_COVER_S = dict(d=5.15, u=(2.6, 7.38), top=1.80, sink=0.25, slits=(4.6, 6.0), rails=(0.55, 1.22))                 # rahna zevnitr: vysky nad podlahou (nad korunou zdi, ta je 0.4-0.7 m)


def frame(walls):
    """ram brany z ruin_layout: origin (UE cm), u, d (jednotkove vektory), delka Brana_S (m), s kapsy na Brana_V pro dane d"""
    W = {w["name"]: w for w in walls}
    ne, nw = W[WALL_S]["points"][0], W[WALL_S]["points"][-1]
    ux, uy = ne[0] - nw[0], ne[1] - nw[1]; ln = math.hypot(ux, uy); ux, uy = ux / ln, uy / ln
    dx, dy = -uy, ux
    sw = W[WALL_J]["points"][-1]
    if (sw[0] - nw[0]) * dx + (sw[1] - nw[1]) * dy < 0: dx, dy = -dx, -dy
    to_d = lambda p: ((p[0] - nw[0]) * dx + (p[1] - nw[1]) * dy) / 100
    v0 = W[WALL_V]["points"][0]                                   # Brana_V zacina na jihu: s = d(zacatek) - d
    return dict(origin=[nw[0], nw[1]], u=[round(ux, 5), round(uy, 5)], d=[round(dx, 5), round(dy, 5)], len_s=round(ln / 100, 3),
                v_d0=round(to_d(v0), 3), face_j=round(W[WALL_J]["thickness"] / 2, 3),
                face_v=round(ln / 100 - W[WALL_V]["thickness"] / 2, 3), face_s=round(W[WALL_S]["thickness"] / 2, 3))


def straz(walls):
    """rozmery strazniho stanoviste v ramu brany (m, vysky cm absolutne)"""
    F = frame(walls); dk = B_DECK["t"]
    deck_z = B_BEAM_Z + B_BEAM["d"] * 100 + dk * 100
    r = B_RAIL; i = r["inset"]; (u0, u1), (d0, d1) = B_DECK["u"], B_DECK["d"]
    rails = [dict(id="Z", p0=[round(u0 + i, 3), round(d0 + i, 3)], p1=[round(u0 + i, 3), round(d1 - i, 3)]),            # zapadni strana
             dict(id="J", p0=[round(u0 + i, 3), round(d1 - i, 3)], p1=[B_RAIL_SOUTH_END, round(d1 - i, 3)])]            # jizni strana po Hradba_V
    return dict(frame=F, beam_z=B_BEAM_Z, deck_z=deck_z, beam=dict(B_BEAM), level=dict(B_LEVEL), deck=dict(B_DECK),
                level_s=dict(B_LEVEL_S),
                level_v=dict(u=(round(F["face_v"] + 0.005, 3), round(F["face_v"] + B_LEVEL_V["depth"], 3)), d=B_LEVEL_V["d"], bottom=B_LEVEL_V["bottom"]),
                rail=dict(B_RAIL), rails=rails if B_RAILS else [], covers=_covers(F, deck_z))


def _covers(F, deck_z):
    """kryty z kulatiny: linie kulu (m v ramu brany), vysky absolutne (cm). V = vychodni na korune Brana_V (base),
    S = severni na korune Brana_S (final), J = jizni na okraji podesty (final)"""
    C = B_COVER_E; u = round(F["len_s"] + C["off"], 3); d0, d1 = C["d"]; com = dict(d=list(C["stake_d"]), gap=C["gap"], jit=C["jit"], min_len=C["min_len"])
    slit = lambda at: dict(at=round(at, 3), w=C["slit_w"], bottom=deck_z + C["slit_bottom"] * 100, flat=True)
    rz = lambda zs: [deck_z + z * 100 for z in zs]
    east = dict(com, id="V", p0=[u, d0], p1=[u, d1], top=deck_z + C["top"] * 100, sink=C["sink"], on=[WALL_V, WALL_S],
                slits=[slit(s - d0) for s in C["slits"]],
                rails=dict(d=C["rail_d"], z=rz(C["rails"]), side=1.0, span=[round(C["rail_d0"] - d0, 3), round(d1 - d0 + 0.1, 3)]), stage="base")
    N = B_COVER_N; (n0, n1) = N["u"]
    north = dict(com, id="S", p0=[n0, N["d"]], p1=[n1, N["d"]], top=deck_z + N["top"] * 100, sink=N["sink"], on=[WALL_S, WALL_J, WALL_V],
                 slits=[dict(slit(s - n0), bottom=deck_z + N["slit_bottom"] * 100) for s in N["slits"]],
                 rails=dict(d=C["rail_d"], z=rz(N["rails"]), side=1.0, span=[-0.1, round(n1 - n0 + 0.02, 3)]), stage="final")
    S_ = B_COVER_S; (s0, s1) = S_["u"]
    south = dict(com, id="J", p0=[s0, S_["d"]], p1=[s1, S_["d"]], top=deck_z + S_["top"] * 100, sink=S_["sink"], on=[WALL_V], floor=deck_z,
                 slits=[slit(s - s0) for s in S_["slits"]],
                 rails=dict(d=C["rail_d"], z=rz(S_["rails"]), side=-1.0, span=[-0.1, round(s1 - s0 + 0.02, 3)]), stage="final")
    return [east, north, south]


def ruin_edits(walls):
    """upravy zriceniny (03) pro gen_layout.py: kapsy pro tramy podesty ve vnitrnim lici Brana_V, vnejsi ozub prahu mostu
    v Brana_V a zarovnani korun mostniho pilire Brana_Pilir a opery Brana_Opera na Z 3011 cm."""
    F = frame(walls)
    pockets = [dict(kind="kapsa", s=round(F["v_d0"] - d, 3), w=B_POCKET["w"], sill=0.0, h=B_POCKET["h"], z_abs=B_BEAM_Z,
                    _="tram strazni podesty (brana_spec.py)") for d in B_BEAM["pos"]]
    rb = B_BRIDGE_REBATE
    pockets.append(dict(kind="kapsa", s=round(F["v_d0"] - rb["d"], 3), w=rb["w"], sill=0.0, h=rb["h"], z_abs=rb["z_abs"],
                        outer=True, _="vnejsi ozub prahu mostu (brana_spec.py)"))
    cut = dict(s0=round(F["v_d0"] - B_CUT_NE["d1"], 3), s1=round(F["v_d0"] + 1.5, 3), z=B_CUT_NE["z"])    # SV narozi rozebrane po uroven paty krytu
    p0, p1, pm = B_PILIR["protect"]; pc0, pc1 = B_PILIR["cap"]
    o0, o1, om = B_OPERA["protect"]; oc0, oc1 = B_OPERA["cap"]
    return {
        WALL_V: dict(openings=pockets, cap=[cut]),
        WALL_PILIR: dict(protect=[dict(s0=p0, s1=p1, min=pm)], cap=[dict(s0=pc0, s1=pc1, z=B_BRIDGE_BEAM_Z)]),
        WALL_OPERA: dict(protect=[dict(s0=o0, s1=o1, min=om)], cap=[dict(s0=oc0, s1=oc1, z=B_BRIDGE_BEAM_Z)]),
    }


# ------------------------------------------------------------------ sijovy prikop, mostni pilir, lavka a zataras (navrh_brana_prikop.md)
B_MOAT_FLOOR_Z = 2700.0          # dno sijoveho prikopu pred branou (UE cm)
B_BRIDGE_BEAM_Z = 3011.0         # spodek mostnich tramu (UE cm): +24 cm tram + 5 cm prkno = vrch mostovky Z 3040 (= prah brany)
B_BRIDGE_REBATE = dict(d=3.10, w=2.50, z_abs=3003.0, h=0.37)   # vnejsi ozub (kapsa) v prahu Brana_V (rada 9, Z 3003-3040) pro ulozeni mostu
B_PILIR = dict(u=12.20, d=(4.60, 1.60), H0=3.5, t=1.4, access=0.45, seed=64, protect=(0.35, 2.65, 3.15), cap=(-0.10, 3.10))
B_OPERA = dict(u=16.30, d=(4.70, 1.50), H0=2.2, t=1.2, access=0.40, seed=65, z_offset=-1.2, protect=(0.15, 3.05, 1.45), cap=(-0.10, 3.30))
B_BRIDGE_BEAM = dict(
    d=0.24,
    pos=(1.98, 2.98, 3.98, 2.23, 3.23, 4.23),                  # 3 zapadni + 3 vychodni klady prelozene vedle sebe nad pilirem (vule 1 cm, stred d = 3.105)
    spans=[(7.84, 12.40)] * 3 + [(12.00, 16.55)] * 3,
    a=(7.84, 16.55),
    bark=False,
    stage="base",
)
B_BRIDGE_DECK = dict(
    a=(7.82, 16.50), c=(1.90, 4.30),                           # delka 8.68 m (od otesaneho jadra prahu Brana_V u=7.79 k opere u=16.50), sirka lavky 2.40 m
    t=0.05, w=(0.22, 0.32), gap=0.010, max_len=2.6, stage="base",
)
B_BRIDGE_FILL = [
    dict(id="pilir", a=(11.65, 12.75), c=(1.80, 4.40), bottom_abs=2940.0, top_abs=B_BRIDGE_BEAM_Z),
    dict(id="opera", a=(15.85, 16.75), c=(1.80, 4.40), bottom_abs=2960.0, top_abs=B_BRIDGE_BEAM_Z),
]
B_BRIDGE_CLEAR = dict(u=(16.20, 19.20), d=(1.40, 4.80))        # predmosti a hrdlo uvozu bez volne suti (pod zatarasem a cestou)
B_ZATARAS = dict(
    u=17.20, d=3.10, ref=(16.53, 3.10),                        # predmosti v hrdle uvozu valu (0.7 m pred lavkou, Z = 3040 cm)
    log_d=0.18, log_len=3.40, log_z=0.566,                     # kmen s kurou SM_RuinLogBark_A (osa v pruseciku kulu 1.60*sin(45)/2)
    stake_d=0.07, stake_len=1.60, stake_offs=(-1.25, -0.42, 0.42, 1.25), stake_pair_dc=0.04,
    stage="base",
)


def prikop_walls(nw, ne, sw):
    """zdi mostniho pilire a opery v 03_ruin (Ruin/Brana) ze souradnic rohu strazni veze"""
    ux, uy = ne[0] - nw[0], ne[1] - nw[1]; ln = math.hypot(ux, uy); ux, uy = ux / ln, uy / ln
    dx, dy = -uy, ux
    if (sw[0] - nw[0]) * dx + (sw[1] - nw[1]) * dy < 0: dx, dy = -dx, -dy
    P = lambda u, d: [round(nw[0] + (ux * u + dx * d) * 100), round(nw[1] + (uy * u + dy * d) * 100)]
    return [
        dict(name=WALL_PILIR, folder="Ruin/Brana", points=[P(B_PILIR["u"], B_PILIR["d"][0]), P(B_PILIR["u"], B_PILIR["d"][1])],
             H0=B_PILIR["H0"], thickness=B_PILIR["t"], access=B_PILIR["access"], seed=B_PILIR["seed"], rubble="both", extend_start=False),
        dict(name=WALL_OPERA, folder="Ruin/Brana", points=[P(B_OPERA["u"], B_OPERA["d"][0]), P(B_OPERA["u"], B_OPERA["d"][1])],
             H0=B_OPERA["H0"], thickness=B_OPERA["t"], access=B_OPERA["access"], seed=B_OPERA["seed"], z_offset=B_OPERA["z_offset"],
             rubble="out", extend_start=False),
    ]


def most(walls):
    """rozmery mostni lavky Brana_Most, vyrovnani Brana_Most_Kamen a zatarasu Brana_Zataras v ramu brany (05_constructions)"""
    F = frame(walls)
    deck_z = B_BRIDGE_BEAM_Z + B_BRIDGE_BEAM["d"] * 100 + B_BRIDGE_DECK["t"] * 100
    Z = B_ZATARAS; u0, d0 = Z["u"], Z["d"]; ref = list(Z["ref"]); r = lambda v: round(v, 3)
    hl = Z["stake_len"] * math.cos(math.radians(45.0)) / 2.0
    hz = Z["stake_len"] * math.sin(math.radians(45.0))
    zc = r(hz / 2.0)
    zitems = [
        dict(id="Kmen", shape="round", d=Z["log_d"], bark=True,
             p0=[u0, r(d0 - Z["log_len"] / 2.0), zc], p1=[u0, r(d0 + Z["log_len"] / 2.0), zc], ref=ref),
    ]
    dc = Z["stake_pair_dc"]
    for k, off in enumerate(Z["stake_offs"]):
        di = d0 + off
        zitems.append(dict(id="Kul%dA" % (k + 1), shape="stake2", d=Z["stake_d"], bark=False,
                           p0=[r(u0 - hl), r(di - dc), 0.0], p1=[r(u0 + hl), r(di - dc), r(hz)], ref=ref))
        zitems.append(dict(id="Kul%dB" % (k + 1), shape="stake2", d=Z["stake_d"], bark=False,
                           p0=[r(u0 + hl), r(di + dc), 0.0], p1=[r(u0 - hl), r(di + dc), r(hz)], ref=ref))
    return dict(frame=F, beam_z=B_BRIDGE_BEAM_Z, deck_z=deck_z, beam=dict(B_BRIDGE_BEAM), deck=dict(B_BRIDGE_DECK),
                fill=[dict(p) for p in B_BRIDGE_FILL], clear=dict(B_BRIDGE_CLEAR), zataras=zitems, zataras_spec=dict(B_ZATARAS))


# ------------------------------------------------------------------ vybaveni Brana_Straz (06_furnishing, typ props)
# Ram skupiny = ram brany (frame): a = u podel Brana_S k vychodu (m), c = d kolmo k jihu (m).
# Podlaha podesty (Brana_Straz_Podesta): a = 0,20 - 6,27 m, c = -0,55 - 5,25 m, vrch prken deck_z = Z 3581 cm.
# Striska z kury (Brana_Straz_Pristresek, kap. 11; polohy sloupku upravene Jirkou v levelu 23. 11. 2026):
# zapadni sloupky na podlaze v a = 3,40; c = 0,78 m a a = 3,465; c = 3,574 m (nad budoucim 2. a 4. tramem pri 5 kulatinach
# d = -0,20 / 0,80 / 2,20 / 3,60 / 5,00 m), vychodni na korune Brana_V (+0,366 m) v a = 7,15; c = 0,81 a 3,70 m;
# pudorys krytiny s presahem a = 3,15 - 8,00 m, c = 0,25 - 3,80 m.
# Graybox (23. 11. 2026, polohy z levelu Jirka): strazce sedi u SZ sloupku sikmo celem do hradu (-22 st.), pred sebou ma
# prevracenou bednu (zvysenou na 52,5 cm) se sadou nastroju na vyrobu sipu a vedle ni toulec na vyrobene sipy;
# pohotovostni toulec a luk stoji na kamenne korune Brana_V (+0,366 m) mezi vychodnimi pruzory d = 1,5 a 3,1 m.
B_FURN_REF = (4.5, 2.2)                                             # bod, od jehoz terenu se meri vysky (podlaha podesty je vodorovna)
B_FURN_CRATE = dict(a=4.111, c=1.558, x=(0.3685, 0.9296), size=(65.0, 45.0, 52.5))          # prevracena bedna dnem vzhuru jako pracovni stolek (SM_RuinCrate_A)
B_FURN_TOOLS = dict(a=4.111, c=1.558, dz=0.525, x=(0.3685, 0.9296), size=(45.0, 30.0, 12.0)) # sada nastroju na vyrobu sipu na vrchu bedny (SM_RuinArrowTools_A)
B_FURN_STOOL = dict(a=4.604, c=1.362, x=(-0.9296, 0.3685), size=(35.0, 34.0, 46.0))         # stolicka pro strazce za bednou, celem do hradu (SM_RuinStool_A, v 1. navrhu graybox)
B_FURN_QUIVER_WORK = dict(a=3.607, c=0.827, x=(0.3685, 0.9296), size=(22.0, 18.0, 75.0))    # toulec u bedny a SZ sloupku jako odloziste na prave vyrobene sipy (SM_RuinQuiver_A)
B_FURN_QUIVER_GUARD = dict(a=7.138, c=2.238, dz=0.366, x=(1.0, 0.0), size=(22.0, 18.0, 75.0)) # pohotovostni toulec na korune Brana_V mezi pruzory (SM_RuinQuiver_A)
B_FURN_BOW = dict(a=7.159, c=1.966, dz=0.366, x=(-0.0127, 0.9999), size=(25.0, 8.0, 145.0))   # luk na korune Brana_V vedle pohotovostniho toulce (SM_RuinBow_A)
# docasni zastupci sloupku strisky z kury (05_constructions, Brana_Straz_Pristresek): O 14 cm, do vysky strisky (3,20 m zapadni na podlaze,
# 1,74 - 1,82 m vychodni na korune Brana_V +0,366 m nad podlahou); po postaveni strisky stavitelem se odeberou
B_FURN_POSTS = [
    dict(id="Sloupek_SZ_Zastupce", a=3.400, c=0.777, dz=0.0, size=(14.0, 14.0, 320.0)),
    dict(id="Sloupek_JZ_Zastupce", a=3.465, c=3.574, dz=0.0, size=(14.0, 14.0, 320.0)),
    dict(id="Sloupek_SV_Zastupce", a=7.148, c=0.807, dz=0.366, size=(14.0, 14.0, 174.4)),
    dict(id="Sloupek_JV_Zastupce", a=7.150, c=3.700, dz=0.366, size=(14.0, 14.0, 181.6)),
]
B_FURN_MESH = {}                                                    # v 1. navrhu je vse v grayboxu (Jirka 23. 11. 2026)


def brana_straz_vybaveni(floor_z, graybox=True):
    """vybaveni strazniho stanoviste nad branami -> seznam kusu v ramu brany (m). floor_z = vrch prken podesty (deck_z)
    v m nad terenem v bode B_FURN_REF (pocita gen_furnishing.py). V 1. navrhu vse graybox (cat 'graybox' -> Cube, MAT_GRAYBOX)."""
    fz = round(floor_z, 3)
    def gb(id_, a, c, size, dz=0.0, x=(1, 0)):
        z = round(fz + dz, 3)
        if not graybox and id_ in B_FURN_MESH:
            shape, fin = B_FURN_MESH[id_]
            return dict(id=id_, shape=shape, finish=fin, a=round(a, 3), c=round(c, 3), z=z, ref=list(B_FURN_REF), x=list(x), size=list(size))
        return dict(id=id_, cat="graybox", a=round(a, 3), c=round(c, 3), z=z, ref=list(B_FURN_REF), x=list(x), size=list(size))
    out = [
        gb("Stolicka", B_FURN_STOOL["a"], B_FURN_STOOL["c"], B_FURN_STOOL["size"], x=B_FURN_STOOL["x"]),
        gb("Bedna_Sipy", B_FURN_CRATE["a"], B_FURN_CRATE["c"], B_FURN_CRATE["size"], x=B_FURN_CRATE["x"]),
        gb("Naradi_Sipy", B_FURN_TOOLS["a"], B_FURN_TOOLS["c"], B_FURN_TOOLS["size"], dz=B_FURN_TOOLS["dz"], x=B_FURN_TOOLS["x"]),
        gb("Toulec_Vyroba", B_FURN_QUIVER_WORK["a"], B_FURN_QUIVER_WORK["c"], B_FURN_QUIVER_WORK["size"], x=B_FURN_QUIVER_WORK["x"]),
        gb("Toulec_Straz", B_FURN_QUIVER_GUARD["a"], B_FURN_QUIVER_GUARD["c"], B_FURN_QUIVER_GUARD["size"], dz=B_FURN_QUIVER_GUARD["dz"], x=B_FURN_QUIVER_GUARD["x"]),
        gb("Luk", B_FURN_BOW["a"], B_FURN_BOW["c"], B_FURN_BOW["size"], dz=B_FURN_BOW["dz"], x=B_FURN_BOW["x"]),
    ]
    for p in B_FURN_POSTS:
        out.append(gb(p["id"], p["a"], p["c"], p["size"], dz=p["dz"]))
    return out
