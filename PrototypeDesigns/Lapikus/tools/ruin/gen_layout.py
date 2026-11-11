"""Vytvori ruin_layout.json pro build_ruin.py z navrhu pudorysu + heightmapy.
python gen_layout.py <ruin_layout_draft.json> <Zricenina_heightmap_505_50cm.png> <vystup ruin_layout.json>
Souradnice UE cm. s = vzdalenost v m od zacatku zdi (prvni bod), vyska v m.
"""
import json, sys
import numpy as np
from PIL import Image

D = json.load(open(sys.argv[1]))
H = np.array(Image.open(sys.argv[2])).astype(float) / 65535 * 64.0     # m
P, T, G, WB = D["palace"], D["tower"], D["gate"], D["west_building"]
cw = D["curtain_wall"]
lerp = lambda a, b, f: [round(a[0] + (b[0] - a[0]) * f), round(a[1] + (b[1] - a[1]) * f)]

def op(kind, s, w, sill, h, **kw): return dict(kind=kind, s=s, w=w, sill=sill, h=h, **kw)

walls = []
def wall(name, folder, pts, H0, t, access, **kw):
    walls.append(dict(name=name, folder=folder, points=pts, H0=H0, thickness=t, access=access, **kw))

# --- pudorys v3 (11/2026): strazni vez se dvema branami dal od veze, hradba obloukem k JV rohu veze ---
# polohy prevzaty z levelu (export_level_layout.py -> layout_from_level.json): posunute zdi Brana_V/J/S, Hradba_V_03, Hradba_Z_S_08
def isect(a, b, c, d):
    """prusecik primek a-b a c-d"""
    x1, y1 = a; x2, y2 = b; x3, y3 = c; x4, y4 = d
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return [round(x1 + t * (x2 - x1)), round(y1 + t * (y2 - y1))]
GT_V = [[2777, -2620], [2624, -3303]]        # Brana_V (vnejsi stena, 1. brana) - J -> S
GT_J = [[1937, -3076], [2090, -2393]]        # Brana_J (vnitrni stena, 2. brana) - S -> J
GT_S = [[2584, -3253], [1901, -3100]]        # Brana_S (severni stena) - V -> Z
GT_NE = isect(*GT_V, *GT_S); GT_NW = isect(*GT_S, *GT_J)
GT_SE = GT_V[0]; GT_SW = GT_J[1]             # jizni stena (nova) spojuje jizni konce
HV3 = [[2385, -2460], [2585, -1610]]         # Hradba_V_03 (posunuta) - urcuje odstup hradby od veze
def on_line(a, b, p):
    """bod na primce a-b nejblize p"""
    ax, ay = a; dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)
    return [round(ax + t * dx), round(ay + t * dy)]
def bezier(p0, c, p1, n):
    return [[round((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0]),
             round((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])] for t in [i / n for i in range(1, n + 1)]]
# --- hradba: severni linie (Hradba_Z_S) konci na SZ rohu strazni veze; vychodni (Hradba_V) od strazni veze obloukem k JV rohu veze
cwA = cw[1:9] + [[582, -2619], GT_NW]        # usek 08 pootoceny (z levelu), pak nove napojeni na strazni vez
HV_C = isect(HV3[0], HV3[1], T[0], T[1])   # ridici bod oblouku: pokracovani Hradba_V_03 x prodlouzeni jizni zdi veze -> plynule navazani
cwB = [on_line(GT_SW, GT_SE, HV3[0]), HV3[1]] + bezier(HV3[1], HV_C, T[1], 6)
import math
LA = sum(math.hypot(cwA[i + 1][0] - cwA[i][0], cwA[i + 1][1] - cwA[i][1]) for i in range(len(cwA) - 1)) / 100
wall("Hradba_Z_S", "Ruin/Hradba", cwA, 9.0, 1.8, 0.18, seed=10,
     access_points=[LA - 1.5],                                                    # u 2. brany
     openings=[op("strilna", s, 0.2, 1.3, 1.0) for s in (43, 62, 70, 76)]
              + [op("strilna", s, 0.2, 5.0, 0.9) for s in (39, 49, 66)]
              + [op("strilna", 19.0, 0.2, 1.2, 0.9), op("strilna", 24.5, 0.2, 1.0, 1.05)],   # usek 03 a 04 (branka zrusena)
     breaches=[dict(s0=54, s1=57.5, floor=1.5),
               dict(s0=-1.0, s1=1.3, floor=0.5, slope_r=2.4, power_r=1.5)],       # usek 01: sikmy sesuv, nizko u palace (stezka k vode ~0.5 m), k useku 02 strmeji
     protect=[dict(s0=37, s1=46, min=5.2)],                                          # ochoz u rampy
     rubble="out")
wall("Hradba_V", "Ruin/Hradba", cwB, 9.0, 2.5, 0.2, seed=11, access_points=[0], rubble="out", extend_start=False)   # 2.5 m = vnejsi lic v rovine jizni zdi veze   # zacina v jizni stene strazni veze
# --- palac ---
wall("Palac_J", "Ruin/Palac", [P[0], P[1]], 13.0, 1.4, 0.12, seed=30, corners=[10.5, 21],
     openings=[op("strilna", s, 0.25, 1.6, 1.1) for s in (3, 8, 14, 19, 25, 29)]
              + [op("okno", s, 1.2, 5.6, 2.2) for s in (5.5, 12.5, 17, 26.5)]
              + [op("okno", s, 1.1, 10, 2.0) for s in (5.5, 12.5, 26.5)],
     breaches=[dict(s0=16.5, s1=20.5, floor=6.0)], rubble="out")
wall("Palac_S", "Ruin/Palac", [P[3], P[2]], 13.0, 1.4, 0.6, seed=31, corners=[10.5, 21],
     access_points=[4.5, 16, 27],
     openings=[op("dvere", 4.5, 1.1, 0, 2.4), op("portal", 16, 1.6, 0, 3.0, protect=True), op("dvere", 27, 1.1, 0, 2.4)]
              + [op("okno", s, 1.2, 5.6, 2.2) for s in (8.5, 23.5)],
     protect=[dict(s0=14, s1=18, min=4.2)], rubble="in")
wall("Palac_Z", "Ruin/Palac", [P[3], P[0]], 13.0, 1.4, 0.5, seed=32, rubble="in")
for i, f in enumerate((10.5 / 32, 21 / 32)):
    wall(f"Palac_pricka_{i+1}", "Ruin/Palac", [lerp(P[0], P[1], f), lerp(P[3], P[2], f)], 13.0, 0.8, 0.92, seed=40 + i,
         openings=[op("dvere", 4.75, 1.0, 0, 2.2)], rubble="both")
# --- vez: vse od podlahy prizemi (VEZ_F, abs. cm), patra po VEZ_ST m, rady kamene pevne po 0.35 m (spary = urovne pater)
VEZ_F = 3150; VEZ_ST = 4.2; VEZ_C = 0.35
TC = [sum(p[0] for p in T) / 4, sum(p[1] for p in T) / 4]
vez_kw = dict(ref_z=VEZ_F, course_grid=[VEZ_F, VEZ_C], inside_pt=TC)
LT = math.hypot(T[1][0] - T[0][0], T[1][1] - T[0][1]) / 100      # strana veze (osy zdi), m
BEAM_V = [2.0 + i for i in range(8)]                              # polohy tramu (v od jizni zdi), m
def strilna(s, n, w_in=1.6):
    """strilna v podlazi n: uzky pruzor zvenku, zevnitr kónicky vyklenek od podlahy do 2.1 m, parapet 1.05 m"""
    f = n * VEZ_ST
    return op("strilna", s, 0.2, f + 3 * VEZ_C, 3 * VEZ_C, robbed="none", splay=dict(floor=f, top=f + 6 * VEZ_C, w_in=w_in))
def kapsy(s_of_v, levels=(1, 2, 3, 4)):
    return [op("kapsa", s_of_v(v), 0.32, n * VEZ_ST - VEZ_C, VEZ_C) for n in levels for v in BEAM_V]
wall("Vez_J", "Ruin/Vez", [T[0], T[1]], 24.0, 2.5, 0.05, seed=50, mid=0.94, **vez_kw,
     openings=[strilna(5.5, n) for n in (0, 1, 2, 3)], rubble="out")                      # na vyvysenine: strilna i v prizemi
wall("Vez_V", "Ruin/Vez", [T[1], T[2]], 24.0, 2.5, 0.03, seed=51, mid=0.96, **vez_kw,
     openings=[strilna(5.5, n) for n in (1, 2, 3)] + kapsy(lambda v: v), rubble="out")   # prizemi bez strilny (za hradbou)
wall("Vez_S", "Ruin/Vez", [T[2], T[3]], 24.0, 2.5, 0.3, seed=52, mid=0.95, **vez_kw,
     openings=[op("dvere", 5.5, 1.0, VEZ_ST, 6 * VEZ_C, robbed="none"), strilna(5.5, 2),
               op("prulom", 8.0, 1.6, 0, 7 * VEZ_C, ragged=0.35)],     # puvodni vstup v 1. patre; pozdeji vybourany pruchod z ulicky
     breaches=[dict(s0=3.5, s1=7.5, floor=12)], rubble="in")
wall("Vez_Z", "Ruin/Vez", [T[3], T[0]], 24.0, 2.5, 0.25, seed=53, mid=0.94, **vez_kw,
     openings=kapsy(lambda v: LT - v), rubble="in")
UV = [(T[1][0] - T[0][0]) / LT / 100, (T[1][1] - T[0][1]) / LT / 100]
VV = [(T[3][0] - T[0][0]) / LT / 100, (T[3][1] - T[0][1]) / LT / 100]
floors = [dict(name="Vez_Patra", folder="Ruin/Vez", origin=T[0], u=UV, v=VV, inner=[1.25, LT - 1.25, 1.25, LT - 1.25],
               ref_z=VEZ_F, storey=VEZ_ST, levels=[1, 2], walls=["Vez_V", "Vez_Z"],
               stone_floor=dict(thickness=0.18, missing=0.07),
               beams=dict(v=BEAM_V, w=0.26, h=0.28, bearing=0.33),
               planks=dict(t=0.05, wmin=0.2, wmax=0.34, missing=0.04),
               hatch=[LT - 3.0, LT - 1.8, LT - 3.0, LT - 1.4])]                     # otvor pro zebrik u SV rohu
# --- strazni vez se dvema branami: 1. brana (Brana_V) z vychodu, 2. brana (Brana_J) na zapad do ulicky podel veze ---
# plinth = podstavba (m): zed zacina na nizsim terenu, vysky, otvory a ochrana se zvednou o tuto hodnotu
wall("Brana_V", "Ruin/Brana", [GT_SE, GT_NE], 10.0, 1.8, 0.4, seed=60, mid=0.92, plinth=2.0, z_offset=-2.1,   # z levelu: cela zed o 2.1 m niz (zapustena do terenu)
     openings=[op("brana", 3.5, 3.2, 0, 4.5, protect=True), op("strilna", 0.9, 0.2, 4.6, 1.0)],
     protect=[dict(s0=0.9, s1=6.1, min=5.8)], features=["kapsa_most", "retezy"], rubble="out")
wall("Brana_S", "Ruin/Brana", [GT_NE, GT_NW], 10.0, 1.8, 0.25, seed=62, rubble="out")
wall("Brana_J", "Ruin/Brana", [GT_NW, GT_SW], 10.0, 1.8, 0.45, seed=61, mid=0.92,
     openings=[op("portal", 3.5, 2.8, 0, 3.8, protect=True)], protect=[dict(s0=1.2, s1=5.8, min=4.8)], rubble="in")
wall("Brana_Jih", "Ruin/Brana", [GT_SW, GT_SE], 10.0, 1.8, 0.35, seed=63, rubble="both")
# --- zapadni budova (vnejsi zdi tvori hradba) ---
wall("ZBudova_V", "Ruin/ZapadniBudova", [WB[1], WB[2]], 7.0, 1.2, 0.35, seed=70, access_points=[6],
     openings=[op("dvere", 6, 1.0, 0, 2.2)], rubble="both")
wall("ZBudova_S", "Ruin/ZapadniBudova", [WB[2], WB[3]], 7.0, 1.2, 0.35, seed=71, rubble="both")

ramps = [dict(name="Rampa_SZ", folder="Ruin/Rampa", start=[-2950, -1250], end=[-2950, -2120], top=5.2, width=3.0)]

# --- terenni mrizka (cm) pro paty zdi ---
x0, y0, x1, y1, st = -5200, -3800, 3600, 400, 100      # mrizka pokryva i strazni vez
xs = np.arange(x0, x1 + 1, st); ys = np.arange(y0, y1 + 1, st)
Z = [[round(float(H[int(np.clip(y / 50 + 252, 0, 504)), int(np.clip(x / 50 + 252, 0, 504))]) * 100) for x in xs] for y in ys]
out = dict(version=1, units="UE cm (pozice), m (s, vysky)", plateau_z_cm=D["plateau_z_cm"],
           params=dict(WEATHER=0.9, ROBBING=4.75, REACH=8.0, ACCESS_BOOST=0.3, ACCESS_RADIUS=6.0,
                       FRAME_REACH=2.5, CORNER_STRENGTH=0.2, COLUMN=0.5, COURSE=0.3, RUBBLE_FACTOR=0.25, SEED=1,
                       COURSE_MIN=0.25, COURSE_MAX=0.4, FACE_DEPTH=0.4, STONE_MIN=0.35, STONE_MAX=0.9, CORE_MIN=1.0, CORE_MAX=1.8,
                       JOINT=0.015, FACE_ROB=1.0, FACE_ROB_H=2.2, RUBBLE_BLOCKS=0.02, REMAIN=0.0, JAG=1.0, FRAME_ROB=1.0),
           presets={"1540": {}, "1650": dict(WEATHER=0.6, ROBBING=7.0, REMAIN=1.2, JAG=1.8, FRAME_ROB=1.4, FACE_ROB=1.4,
                                             RUBBLE_FACTOR=0.08, RUBBLE_BLOCKS=0.015)},
           age="1650", edits=[], volumes_examples=[{'tags': ['Ruin_Opening:portal', 'Ruin_Protect'], 'box': [350, -1400, 3080, 750, -1200, 3420], '_': 'portal z palace do veze (testovaci, v levelu jako TriggerBox s tagy)'}, {'tags': ['Ruin_Cut'], 'box': [-3000, -2500, 3050, -2700, -2000, 3300], '_': 'vyrizne vse v boxu'}, {'tags': ['Ruin_Keep'], 'box': [-3600, -2400, 3100, -2500, -1900, 3700], '_': 'zdi v boxu alespon do vysky vrsku boxu'}, {'tags': ['Ruin_Explode'], 'box': [600, -2200, 3100, 1100, -1800, 3500], '_': 'bloky uvnitr jako samostatne actory'}], edits_examples=[{'op': 'cut', 'wall': 'Palac_J', 's0': 21.0, 's1': 22.2, 'z0': 5.6, 'z1': 7.8, '_': 'vybourat okno ve zdi (s = m od zacatku zdi, z = m od paty)'}, {'op': 'cut_box', 'box': [-1900, -1300, 3100, -1700, -1000, 3350], '_': 'vyriznout pruchod pres vsechny zdi v boxu (svetove cm: x0,y0,z0,x1,y1,z1)'}, {'op': 'set_height', 'wall': 'Hradba_Z_S', 's0': 37, 's1': 46, 'h': 5.2, '_': 'nastavit vysku useku (m) - presne'}, {'op': 'restore', 'wall': 'Vez_S', 's0': 0, 's1': 11, 'h': 14.0, '_': 'zvysit usek alespon na h (m) - zachrani rozpad'}],
           walls=walls, ramps=ramps, floors=floors,
           terrain=dict(x0=x0, y0=y0, step=st, nx=len(xs), ny=len(ys), z=Z))
json.dump(out, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
print("zdi:", len(walls))
