import numpy as np, json, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.colors as mc
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image
from decay import wall_profile
L = json.load(open('/mnt/user-data/outputs/03_ruin/ruin_layout_draft.json'))
Hm = np.array(Image.open('../testrun/Zricenina_heightmap_505_50cm.png')).astype(float) / 65535 * 64
Z0 = L["plateau_z_cm"] / 100
ter = lambda xm, ym: Hm[int(np.clip(ym * 2 + 252, 0, 504)), int(np.clip(xm * 2 + 252, 0, 504))] - Z0
polys, cols = [], []
Ld = np.array([-0.5, -0.4, 0.75]); Ld /= np.linalg.norm(Ld)

def col(x0, y0, x1, y1, t, h, base, c):
    dx, dy = x1 - x0, y1 - y0; n = np.array([-dy, dx]) / np.hypot(dx, dy) * t / 2
    P = [np.array([x0, y0]) + n, np.array([x1, y1]) + n, np.array([x1, y1]) - n, np.array([x0, y0]) - n]
    rgb = np.array(mc.to_rgb(c)); base = max(base, -3)
    polys.append([(p[0], p[1], h) for p in P]); cols.append(tuple(np.clip(rgb * 1.12, 0, 1)))
    for i in range(4):
        p, q = P[i], P[(i + 1) % 4]; e = q - p; nn = np.array([e[1], -e[0], 0.0]); nn /= np.linalg.norm(nn) + 1e-9
        polys.append([(p[0], p[1], base), (q[0], q[1], base), (q[0], q[1], h), (p[0], p[1], h)])
        cols.append(tuple(rgb * (0.55 + 0.45 * max(0, nn @ Ld))))

def wall(pts, t, H0, access, seed, breaches=(), c="#b9a687", mid=0.88, ap=()):
    pts = np.array(pts, float) / 100
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]; Ls = np.hypot(*(q - p))
        if Ls < 0.5: continue
        br = [dict(x0=b[1], x1=b[2], floor=b[3]) for b in breaches if b[0] == i]
        x, h = wall_profile(Ls, H0, None, breaches=br, seed=seed + i, step=0.5, mid=mid, access=access, access_points=[a - 0 for a in ap])
        for j in range(len(x) - 1):
            A = p + (q - p) * x[j] / Ls; B = p + (q - p) * x[j + 1] / Ls
            col(A[0], A[1], B[0], B[1], t, h[j], min(ter(*A), ter(*B)) - 1.0, c)

wall(L["curtain_wall"], 1.8, 9, 0.18, 10, breaches=[(7, 14, 17.5, 1.5)])
pal = L["palace"]; P = np.array(pal, float)
wall([pal[0], pal[1]], 1.4, 13, 0.12, 30, breaches=[(0, 16.5, 20.5, 6.0)])
wall([pal[2], pal[3]], 1.4, 13, 0.6, 31, ap=(5, 16, 27))
wall([pal[3], pal[0]], 1.4, 13, 0.5, 32)
for f in (10.5 / 32, 21 / 32):
    wall([P[0] + (P[1] - P[0]) * f, P[3] + (P[2] - P[3]) * f], 0.8, 13, 0.92, 40 + int(f * 10), c="#a89676")
tw = L["tower"]
wall([tw[0], tw[1]], 2.5, 24, 0.05, 50, mid=0.94); wall([tw[1], tw[2]], 2.5, 24, 0.03, 51, mid=0.95)
wall([tw[2], tw[3]], 2.5, 24, 0.3, 52, breaches=[(0, 3.5, 7.5, 12)], mid=0.95); wall([tw[3], tw[0]], 2.5, 24, 0.25, 53, mid=0.94)
g = L["gate"]; wall(g + [g[0]], 1.8, 10, 0.4, 60, mid=0.92)
wb = L["west_building"]; wall(wb + [wb[0]], 1.2, 7, 0.35, 70)

fig = plt.figure(figsize=(22, 9))
for k, (az, el, tt) in enumerate([(-125, 26, "pohled od JZ – jižní strana nad útesem"), (55, 30, "pohled od SV – brána, věž, nádvoří")]):
    ax = fig.add_subplot(1, 2, k + 1, projection='3d')
    gp = np.array(L["curtain_wall"], float) / 100
    ax.add_collection3d(Poly3DCollection([[(x, y, -0.05) for x, y in gp]], facecolors="#d7e2c4", edgecolors="none"))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors="none"))
    ax.set_xlim(-48, 22); ax.set_ylim(-30, 3); ax.set_zlim(-3, 22)
    ax.set_box_aspect((70, 33, 25), zoom=1.12)
    for nm,key,zz in (("věž","tower",23),("brána","gate",11),("palác","palace",11),("Z budova","west_building",8)):
        c=np.mean(np.array(L[key],float),0)/100; ax.text(c[0],c[1],zz,nm,fontsize=12,fontweight="bold",color="#5a1a1a",ha="center")
    ax.text(-20,-30,0,"sever →",fontsize=11,color="#334",zdir=None); ax.text(-20,3,0,"jih (útes)",fontsize=11,color="#334")
    ax.invert_yaxis(); ax.view_init(elev=el, azim=az); ax.set_axis_off(); ax.set_title(tt, fontsize=13)
fig.suptitle("Zřícenina – hmotový náčrt ~1540: vysoké vnější zdi zůstaly, nízké a dostupné rozebrané; paty zdí sahají k terénu, terén nezobrazen", fontsize=15, fontweight="bold")
plt.subplots_adjust(left=0, right=1, top=0.92, bottom=0, wspace=0)
plt.savefig(sys.argv[1], dpi=80)
