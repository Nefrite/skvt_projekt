"""tower_spec.py - spolecne rozmery veze pro zriceninu (03, kapsy a otvory) i drevene vestavby (05, tramy, schody).
Kdyz se zmeni polohy tramu / pruvlaku / dveri, je potreba pregenerovat obe casti (gen_layout.py i gen_constructions.py)."""
import math

VEZ_F = 3150          # horni plocha kamenne podlahy prizemi (abs. cm)
VEZ_ST = 4.2          # vyska patra (m)
VEZ_C = 0.35          # vyska rady kamene ve vezi (m) - spary = urovne pater


def spec(T):
    """T = 4 rohy veze (osy zdi, UE cm): J-Z, J-V, S-V, S-Z. Vrati slovnik rozmeru v ramu veze
    (u od J-Z rohu podel jizni zdi, v od J-Z rohu na sever, metry)."""
    LT = math.hypot(T[1][0] - T[0][0], T[1][1] - T[0][1]) / 100            # strana veze (osy zdi), m
    UV = [(T[1][0] - T[0][0]) / LT / 100, (T[1][1] - T[0][1]) / LT / 100]
    VV = [(T[3][0] - T[0][0]) / LT / 100, (T[3][1] - T[0][1]) / LT / 100]
    # tramy rovnomerne po ~1.64 m (s pruvlakem uprostred staci), krajni tesne u zdi; kazde pole je dost siroke pro schody
    BEAM_V = [round(1.4 + i * (LT - 2.8) / 5, 3) for i in range(6)]
    bay = lambda i: [round(BEAM_V[i] + 0.13, 3), round(BEAM_V[i + 1] - 0.13, 3)]
    GIRD_U = round(LT / 2, 3)                                               # pruvlak uprostred veze (sever-jih pod tramy)
    U_TOP = round(GIRD_U + 0.17, 3)                                         # horni konec schodu se opira o pruvlak
    DOOR_U = round((1.25 + GIRD_U) / 2, 3)                                  # puvodni vstup: zevnitr mezi Z zdi a sloupem
    return dict(LT=LT, UV=UV, VV=VV, origin=T[0], BEAM_V=BEAM_V, GIRD_U=GIRD_U, GIRD_POST_V=round(LT / 2, 3),
                U_TOP=U_TOP, HATCH1=[U_TOP, round(U_TOP + 2.2, 3)] + bay(4),  # do 1. patra: pole u severni zdi
                HATCH2=[U_TOP, round(U_TOP + 2.2, 3)] + bay(3),               # do 2. patra: sousedni pole
                DOOR_U=DOOR_U, DOOR_S=round(LT - DOOR_U, 3), PORCH_BEAM_DS=1.1,
                inner=[1.25, LT - 1.25, 1.25, LT - 1.25])


# --- skody z dobyvani (03): hrad dobyvan od vychodu a jihovychodu (navrh_vez_pristresek.md kap. 3, Jirka 14. a 17. 11. 2026)
# floor / min v m od paty zdi (ref_z = VEZ_F), s podel zdi od jejiho prvniho bodu:
# Vez_J s = u (od JZ rohu), Vez_V s = v (od JV rohu), Vez_S s = LT - u (od SV rohu), Vez_Z s = LT - v (od SZ rohu)
S_RAMP = dict(floor=11.86, k=0.318, power=0.7, step=1.5, gap=0.65, s1=11.3)   # Vez_S: rampa breach B(s) = floor + k * s^power


def ruin_edits():
    """upravy zriceniny pro gen_layout.py (pridavaji se za stavajici breaches / protect; tvar U ve Vez_S je zruseny v gen_layout.py)"""
    R = S_RAMP
    B = lambda s: R["floor"] + R["k"] * s ** R["power"]
    s_prot = [dict(s0=-1.6, s1=0.0, min=11.56, _="SV roh navazuje na Vez_V")]
    s = 0.0
    while s < R["s1"] - 1e-6:
        s1 = round(min(s + R["step"], R["s1"]), 3) if s + 2 * R["step"] <= R["s1"] + 1e-6 else R["s1"]
        s_prot.append(dict(s0=round(s, 3), s1=s1, min=round(B(s) - R["gap"], 2)))
        s = s1
    return {
        "Vez_V": dict(breaches=[dict(s0=2.5, s1=6.5, floor=10.3, slope_l=0.7, slope_r=0.35, _="hlavni prulom"),
                                dict(s0=3.2, s1=4.8, floor=9.95, slope=0.6, _="nejhlubsi misto jizne od stredu")]),
        "Vez_J": dict(breaches=[dict(s0=1.25, s1=7.4, floor=11.15, slope_l=3.0, slope_r=0.5, _="prulom nad pristreskem"),
                                dict(s0=2.9, s1=4.1, floor=10.9, slope=0.6, _="hlubsi misto zapadne od strilny")],
                      protect=[dict(s0=4.6, s1=6.4, min=11.15, _="nadprazi strilny 2. patra")]),
        "Vez_Z": dict(protect=[dict(s0=7.0, s1=8.2, min=12.1, _="jen vedlejsi skody, stred vyssi"),
                               dict(s0=8.2, s1=9.5, min=11.8)]),
        "Vez_S": dict(breaches=[dict(s0=-3.0, s1=0.0, floor=R["floor"], slope_r=R["k"], power_r=R["power"],
                                     _="plynuly pokles od SZ k SV rohu")],
                      protect=s_prot),
    }


# --- platenny pristresek hlidky ve 2. patre (05 Vez_Pristresek, typ canvas_shelter; navrh_vez_pristresek.md kap. 4 a 5)
# ram veze (u, v v m), vysky h v m od VEZ_F. Pultova strecha nad JZ casti patra: hreben vychod-zapad nad stropnim tramem
# BEAM_V[2], okap na korune Vez_J, spad k jihu 22,6 st. (nesnizovat pod 22). Vsechna kulatina s kurou, cela a rezy raw.
PR = dict(
    floor_top=8.39,                                   # vrch prken 2. patra (Vez_Patra), paty kulu a vzper
    posts=dict(u=(1.40, 5.50, 7.15), d=0.16),         # kuly rozsochy nad tramem BEAM_V[2] (prostredni i nad pruvlakem)
    fork_k=0.16 / 0.12,                               # hlava rozsochy SM_RuinForkHead (kmen O 12 cm) skalovana na prumer kulu
    ridge=dict(pieces=((1.30, 5.70), (5.30, 7.40)), top=12.70, d=0.14),   # hreben ze dvou kusu, preplatovany nad prostrednim kulem
    eave=dict(u=(1.30, 7.40), v=1.00, bottom=11.05, d=0.12),              # okapova tyc na podkladnich kamenech na korune Vez_J
    pads=dict(u=(1.50, 2.20, 4.70, 6.30, 7.20), band_v=(0.85, 1.15), size=(0.40, 0.30), two_over=0.35, max_h=0.60),
    weights=dict(u=(1.9, 3.6, 5.1, 6.8), v=0.98, size=(0.35, 0.25, 0.16)),   # zatezove kameny na okapove tyci (pres lem platna)
    rafters=dict(u=(1.45, 2.90, 4.35, 5.80, 7.20), d=0.10, v=(0.50, 4.80)),  # krokvove tyce po spadu
    braces=dict(u=(2.60, 4.90), d=0.10, head_dv=0.12, head_h=12.55),        # vzpery: hlava pod hrebenem ze severu, pata nad BEAM_V[3]
    canvas=dict(u=(1.30, 7.30), v=(0.50, 4.80), lift=0.02, sag=0.04, seed=21500),    # platno 2 cm nad krokvemi (pres ovazani, to
                                                      # vycniva 1,6 cm; navrh 0,5 cm), prevesene mezi krokvemi
    gable=dict(u=1.37, v=(1.91, 4.60), bottom=11.55, bulge=0.02, seed=21600,          # stit pod krajni krokvi (rovina u = 1,37)
               hem=dict(v=(2.0, 4.60), h=11.58, d=0.05)),                            # tycka v lemu stitu
    ropes=(dict(ridge_u=3.40, edge_u=1.80, anchor=(1.80, -0.30)),                     # bourkova lana pres platno ke kamenum na korune
           dict(ridge_u=5.20, edge_u=6.90, anchor=(7.90, -0.30))),
    rope=dict(d=0.015, lift=0.02, link=1.0), anchor_size=(0.40, 0.30, 0.22),
)
FORK_SEAT_K = {"A": 17.5, "B": 17.25}   # osa hrebene O 14 cm nad stredem hlavy rozsochy pred skalovanim fork_k (cm), zmereno na OBJ:
                                        # kruh R 7 / fork_k mezi rameny bez vrcholu uvnitr (pro O 20: 27,75 / 25,75 = FORK_SEAT v okap.py)


def pristresek(TS):
    """rozmery pristresku v ramu veze (u, v m; h m od VEZ_F). TS = spec(T). Vrati PR doplneny o polohy z ramu veze
    a odvozene vysky: rafter_axis(v) = osa krokvove tyce, canvas_h(v) = vrch platna (bez prevesu)."""
    p = {k: v for k, v in PR.items()}
    rv = TS["BEAM_V"][2]; bv = TS["BEAM_V"][3]
    p.update(ridge_v=rv, brace_v=bv)
    r_raf = PR["rafters"]["d"] / 2
    e_top = PR["eave"]["bottom"] + PR["eave"]["d"]                        # vrch okapove tyce
    k = (PR["ridge"]["top"] - e_top) / (rv - PR["eave"]["v"])             # sklon krokvi (tg)
    p["slope"] = k
    p["rafter_axis"] = lambda v: e_top + r_raf + k * (v - PR["eave"]["v"])
    p["canvas_h"] = lambda v: e_top + 2 * r_raf + PR["canvas"]["lift"] + k * (v - PR["eave"]["v"])
    p["ridge_axis"] = PR["ridge"]["top"] - PR["ridge"]["d"] / 2
    return p
