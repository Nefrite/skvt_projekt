"""nadvori_spec.py - spolecne rozmery a polohy staveb a vybaveni na nadvori (Nadvori_Stan).
Stan stoji v etape 1 (sada site) u severni hradby Hradba_Z_S mezi Guesthouse (ZBudova_V, s = -8,41) a hranici prken
staveniste (Palac_Obydli_Stavenisko_Prkna, s = 10,53..13,59), vchodem na jih do nadvori.
Ramec stanu (origin, u, v): u = smer vchodu (+X meshe SM_RuinCanvasTent_A = jih, -n palace),
v = u otocena v UE o +90 st. (+Y meshe = odhrnuta chlopen = zapad, -s palace).
entities: [Nadvori_Stan]
docs: [navrh_nadvori_stan, 05_constructions, 06_furnishing]
build_step: 03_ruin
domains: structures"""
from palac_spec import frame as palac_frame

# Poloha stredu pudorysu stanu v ramci palace (s, n v m):
# - Guesthouse (Ostroh_Krov) konci na s = -8,41; prkna staveniste zacinaji na s = 10,53
# - Hradba_Z_S v s = 0..3 ma vnitrni lic n = 20,91..21,29 a vysku 4,6..5,2 m; teren je rovny (Z = 3129 cm)
# - Zadni stit stanu (x = -1,20) je na n = 20,00, zadni kotvici kolik (x = -1,70) na n = 20,50 (mezera k hradbe >= 0,41 m)
STAN_CENTER = (1.5, 18.8)
STAN_MESH = "SM_RuinCanvasTent_A"
STAN_POLE_SINK = 0.08            # zapusteni stojek do zeme (m)
STAN_PEG = dict(len=0.30, d=0.035, sink=0.15, tilt=15.0)    # obvodove koliky (SM_RuinStakeSmall)
STAN_ROPE = dict(d=0.015, link=1.0)                         # napinaci snury jako retez SM_RuinRope_A (stejne jako Vez_Pristresek)
# 6 napinacich snur (2 stitove z koncu hrebene + 4 rohove z boku ve vysce 0,35 m) ke kolikum 0,5 m od platna
STAN_GUYS = [
    dict(id="GZ", a=(-1.26,  0.00, 1.87), p=(-1.70,  0.00)),   # zadni stit (sever, u hradby)
    dict(id="GP", a=( 1.26,  0.00, 1.87), p=( 1.70,  0.00)),   # predni stit (jih, u vchodu)
    dict(id="G1", a=(-1.18, -0.90, 0.35), p=(-1.35, -1.60)),   # severovychodni roh
    dict(id="G2", a=( 1.18, -0.90, 0.35), p=( 1.35, -1.60)),   # jihovychodni roh
    dict(id="G3", a=(-1.18,  0.90, 0.35), p=(-1.35,  1.60)),   # severozapadni roh
    dict(id="G4", a=( 1.18,  0.90, 0.35), p=( 1.35,  1.60)),   # jihozapadni roh
]
STAN_CLEAR = ((-1.90, -1.80), (1.90, -1.80), (1.90, 1.80), (-1.90, 1.80))   # uklid suti pod stanem a snurami (m v ramci stanu)


def stan_frame(walls):
    """ram stanu v UE cm: pocatek pod stredem hrebene, u = jih (+X vchod), v = zapad (+Y odhrnuta chlopen)"""
    F = palac_frame(walls)
    O, S, N = F["origin"], F["s"], F["n"]
    sc, nc = STAN_CENTER
    origin = [round(O[0] + (S[0] * sc + N[0] * nc) * 100, 2),
              round(O[1] + (S[1] * sc + N[1] * nc) * 100, 2)]
    u = [round(-N[0], 6), round(-N[1], 6)]         # +X = jih (-n palace)
    v = [round(-S[0], 6), round(-S[1], 6)]         # +Y = zapad (-s palace; v UE je u otocena o +90 st.)
    return dict(origin=origin, u=u, v=v)


def stan(walls):
    """parametry stavby Nadvori_Stan (05_constructions, typ tent)"""
    F = stan_frame(walls)
    O, U, V = F["origin"], F["u"], F["v"]
    W = lambda x, y: [round(O[0] + (U[0] * x + V[0] * y) * 100, 1),
                      round(O[1] + (U[1] * x + V[1] * y) * 100, 1)]
    return dict(frame=F, mesh=STAN_MESH, pole_sink=STAN_POLE_SINK,
                peg=dict(STAN_PEG), rope=dict(STAN_ROPE),
                guys=[dict(g, a=list(g["a"]), p=list(g["p"])) for g in STAN_GUYS],
                clear_poly=[W(x, y) for x, y in STAN_CLEAR])


def stan_vybaveni():
    """vybaveni stanu (06_furnishing, Nadvori_Stan_Vybaveni, sada site) v ramci stanu (a = +X jih, c = +Y zapad):
    jedno luzko podel vychodni (zavrene) strany uvnitr stanu, truhlicka a vak uvnitr na zapadni strane,
    spalek k sezeni pred vchodem."""
    return [
        dict(id="Luzko",     shape="camp_bed",    a=-0.10, c=-0.49, z=0.0, x=[1.0,  0.0], scale=[1.0, 0.90, 1.0], finish="raw"),
        dict(id="Truhlicka", shape="chest_small", a=-0.65, c= 0.45, z=0.0, x=[1.0,  0.0], finish="raw"),
        dict(id="Vak",       shape="bundle",      a= 0.15, c= 0.50, z=0.0, x=[0.95, 0.31], cat="sackcloth"),
        dict(id="Spalek",    shape="stump",       a= 2.00, c=-0.55, z=0.0, x=[1.0,  0.0], finish="raw"),
    ]
