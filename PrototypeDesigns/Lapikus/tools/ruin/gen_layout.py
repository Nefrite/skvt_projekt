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

# --- hradba: dve casti (mezi nimi stoji brana), jizni usek tvori palac a vez ---
cwA = cw[1:9] + [[661, -2249]]
cwB = [[1497, -2391]] + cw[10:14]
wall("Hradba_Z_S", "Ruin/Hradba", cwA, 9.0, 1.8, 0.18, seed=10,
     access_points=[79.5],
     openings=[op("dvere", 24.5 - 3.2, 1.0, 0, 2.2, robbed="one", side="r")]          # branka na spicku ostrohu
              + [op("strilna", s, 0.2, 1.3, 1.0) for s in (43, 62, 70, 76)]
              + [op("strilna", s, 0.2, 5.0, 0.9) for s in (39, 49, 66)],
     breaches=[dict(s0=54, s1=57.5, floor=1.5)],
     protect=[dict(s0=37, s1=46, min=5.2)],                                          # ochoz u rampy
     rubble="out")
wall("Hradba_V", "Ruin/Hradba", cwB, 9.0, 1.8, 0.2, seed=11, access_points=[0], rubble="out")
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
# --- vez ---
wall("Vez_J", "Ruin/Vez", [T[0], T[1]], 24.0, 2.5, 0.05, seed=50, mid=0.94,
     openings=[op("strilna", 5.5, 0.25, h, 1.2) for h in (3, 8, 12.5, 17)], rubble="out")
wall("Vez_V", "Ruin/Vez", [T[1], T[2]], 24.0, 2.5, 0.03, seed=51, mid=0.96,
     openings=[op("strilna", 5.5, 0.25, h, 1.25) for h in (4, 9, 14, 18.5)], rubble="out")
wall("Vez_S", "Ruin/Vez", [T[2], T[3]], 24.0, 2.5, 0.3, seed=52, mid=0.95,
     openings=[op("dvere", 5.5, 1.0, 6.5, 2.2), op("strilna", 5.5, 0.25, 11, 1.3)],
     breaches=[dict(s0=3.5, s1=7.5, floor=12)], rubble="in")
wall("Vez_Z", "Ruin/Vez", [T[3], T[0]], 24.0, 2.5, 0.25, seed=53, mid=0.94, rubble="in")
# --- brana (zalomeny vjezd: z vychodu dovnitr budovy, pak na jih do nadvori) ---
wall("Brana_V", "Ruin/Brana", [G[1], G[2]], 10.0, 1.8, 0.4, seed=60, mid=0.92,
     openings=[op("brana", 3.5, 3.2, 0, 4.5, protect=True), op("strilna", 0.9, 0.2, 4.6, 1.0)],
     protect=[dict(s0=1.4, s1=5.6, min=5.8)], features=["kapsa_most", "retezy"], rubble="out")
wall("Brana_J", "Ruin/Brana", [G[0], G[1]], 10.0, 1.8, 0.45, seed=61, mid=0.92,
     openings=[op("portal", 3.5, 2.8, 0, 3.8, protect=True)], protect=[dict(s0=1.8, s1=5.2, min=4.8)], rubble="in")
wall("Brana_S", "Ruin/Brana", [G[2], G[3]], 10.0, 1.8, 0.25, seed=62, rubble="out")
wall("Brana_Z", "Ruin/Brana", [G[3], G[0]], 10.0, 1.8, 0.35, seed=63, rubble="both")
# --- zapadni budova (vnejsi zdi tvori hradba) ---
wall("ZBudova_V", "Ruin/ZapadniBudova", [WB[1], WB[2]], 7.0, 1.2, 0.35, seed=70, access_points=[6],
     openings=[op("dvere", 6, 1.0, 0, 2.2)], rubble="both")
wall("ZBudova_S", "Ruin/ZapadniBudova", [WB[2], WB[3]], 7.0, 1.2, 0.35, seed=71, rubble="both")

ramps = [dict(name="Rampa_SZ", folder="Ruin/Rampa", start=[-2950, -1250], end=[-2950, -2120], top=5.2, width=3.0)]

# --- terenni mrizka (cm) pro paty zdi ---
x0, y0, x1, y1, st = -5200, -3300, 3000, 400, 100
xs = np.arange(x0, x1 + 1, st); ys = np.arange(y0, y1 + 1, st)
Z = [[round(float(H[int(np.clip(y / 50 + 252, 0, 504)), int(np.clip(x / 50 + 252, 0, 504))]) * 100) for x in xs] for y in ys]
out = dict(version=1, units="UE cm (pozice), m (s, vysky)", plateau_z_cm=D["plateau_z_cm"],
           params=dict(WEATHER=0.9, ROBBING=4.75, REACH=8.0, ACCESS_BOOST=0.3, ACCESS_RADIUS=6.0,
                       FRAME_REACH=2.5, CORNER_STRENGTH=0.2, COLUMN=0.5, COURSE=0.3, RUBBLE_FACTOR=0.25, SEED=1),
           walls=walls, ramps=ramps,
           terrain=dict(x0=x0, y0=y0, step=st, nx=len(xs), ny=len(ys), z=Z))
json.dump(out, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
print("zdi:", len(walls))
