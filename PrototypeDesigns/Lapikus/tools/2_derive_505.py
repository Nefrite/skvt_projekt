"""
Zricenina - odvozene podklady pro orez 505 px z vystupu 1_gen_heightmap_1009.py

Pouziti:
  python 2_derive_505.py crop   <dir>                 -> Zricenina_heightmap_505_50cm.png, Zricenina_preview_orez.png
  python 2_derive_505.py river  <dir>                 -> Zricenina_505_body_reky.csv, river_points.txt (pro import_river_spline.py)
  python 2_derive_505.py mask   <dir>                 -> T_RiverMask_505.png (R = dno, G = bahno)
  python 2_derive_505.py zones  <dir> <nacrt.png>     -> Zricenina_les_plan.png, T_ForestZones_505.png,
                                                         Zricenina_les_zony.csv, zone_points.json, zones_masks.npz
  python 2_derive_505.py alders <dir>                 -> Zricenina_olse.csv, alder_points.txt, Zricenina_olse_plan.png
                                                         (po kroku zones; olse podel reky podle tvaru koryta)

<dir> = slozka s H.npy, S.npy, Zricenina_heightmap_1009.png (vystup kroku 1).
Pozadavky: numpy, scipy, pillow, scikit-image.

Souradnice:
  1009 px mapa (0,5 m/px, 504 m)  --orez od (326, 309), 505 px-->  landscape 252 x 252 m
  UE: X = (px - 252) * 50 cm, Y = (py - 252) * 50 cm, Z = vyska_m * 100 (pri Location Z 3200, Scale Z 12.5)
Nacrt pro "zones": screenshot Zricenina_les_plan.png 658x658 px, mapa v nem na (8, 5) o velikosti 650 px
  (cervena = hrad, oranzova = osa cesty, fialova = skalnate podlozi). Pri jinem screenshotu upravit SHOT_*.
"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import cKDTree
from scipy.ndimage import (gaussian_filter, label, distance_transform_edt, uniform_filter1d,
                           binary_closing, binary_fill_holes, binary_dilation)

N = 505; RES = 0.5
CROP0 = np.array([326, 309])          # roh orezu v 1009 px mape
SHOT_OFF = (8, 5); SHOT_SIZE = 650    # poloha mapy ve screenshotu s nacrtem
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def ss(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)

def load(d):
    full = np.array(Image.open(f"{d}/Zricenina_heightmap_1009.png"))
    c = full[CROP0[1]:CROP0[1] + N, CROP0[0]:CROP0[0] + N]
    H = c.astype(float) / 65535 * 64.0
    S = np.load(f"{d}/S.npy") / RES - CROP0          # osa reky v px orezu
    yy, xx = np.mgrid[0:N, 0:N]; P = np.c_[xx.ravel(), yy.ravel()]
    D = cKDTree(S).query(P)[0].reshape(N, N) * RES    # vzdalenost od osy reky (m)
    return c, H, S, P, D

def slope_rgb(H):
    gy, gx = np.gradient(H, RES)
    sl = np.degrees(np.arctan(np.hypot(gx, gy)))
    asp = np.arctan2(-gx, gy); s = np.arctan(np.hypot(gx, gy))
    hs = np.clip(np.sin(np.radians(45)) * np.cos(s) + np.cos(np.radians(45)) * np.sin(s) * np.cos(np.radians(315) - asp), 0, 1)
    cols = np.array([[205, 228, 180], [233, 205, 170], [225, 160, 160], [205, 110, 140], [180, 50, 110]], float)
    return cols[np.digitize(sl, [8, 18, 28, 38])] * (0.55 + 0.45 * hs[..., None])

def cmd_crop(d):
    c, H, S, P, D = load(d)
    Image.fromarray(c).save(f"{d}/Zricenina_heightmap_505_50cm.png")
    Image.fromarray(slope_rgb(H).astype(np.uint8)).save(f"{d}/Zricenina_preview_orez.png")

def cmd_river(d):
    c, H, S, P, D = load(d)
    yy, xx = np.mgrid[0:N, 0:N]
    arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(S, axis=0), axis=1))] * RES
    ins = np.where((S[:, 0] >= 0) & (S[:, 0] < N) & (S[:, 1] >= 0) & (S[:, 1] < N))[0]
    rows = []
    for t in np.r_[np.arange(arc[ins[0]], arc[ins[-1]], 20.0), arc[ins[-1]]]:
        i = min(np.searchsorted(arc, t), len(S) - 1); x, y = S[i]
        near = np.hypot(xx - x, yy - y) * RES < 12
        bed = H[near & (D < 1.5)].min()
        bank = np.percentile(H[near & (D > 4.5) & (D < 7.0)], 10)
        rows.append([x, y, bank - 0.25])               # hladina 25 cm pod hranou brehu
    rows = np.array(rows)[::-1]                         # smer toku jih -> SV
    w = np.convolve(np.r_[rows[0, 2], rows[:, 2], rows[-1, 2]], [0.25, 0.5, 0.25], "valid")
    for k in range(1, len(w)): w[k] = min(w[k], w[k - 1])   # hladina nesmi po proudu stoupat
    pts = [((x - 252) * 50, (y - 252) * 50, z * 100) for (x, y, _), z in zip(rows, w)]
    def ext(p, q, dist=1000):
        v = np.array(p[:2]) - np.array(q[:2]); v = v / np.linalg.norm(v) * dist
        return (p[0] + v[0], p[1] + v[1], p[2])
    pts = [ext(pts[0], pts[1])] + pts + [ext(pts[-1], pts[-2])]
    open(f"{d}/Zricenina_505_body_reky.csv", "w").write(
        "#;X_cm;Y_cm;Z_cm_hladina\n" + "\n".join("%d;%d;%d;%d" % (i + 1, *map(round, p)) for i, p in enumerate(pts)) + "\n")
    open(f"{d}/river_points.txt", "w").write("\n".join("    (%d, %d, %d)," % tuple(map(round, p)) for p in pts) + "\n")

def cmd_mask(d):
    c, H, S, P, D = load(d)
    yy, xx = np.mgrid[0:N, 0:N]
    r = np.random.default_rng(3)
    from scipy.ndimage import zoom
    n = sum(zoom(r.standard_normal((b, b)), N / b, order=3)[:N, :N] * a for b, a in ((12, 1.0), (40, 0.5)))
    tree = cKDTree(S); idx = tree.query(P)[1].reshape(N, N)
    Si = np.clip(np.rint(S).astype(int), 0, N - 1)
    rel = H - gaussian_filter(H, 3)[Si[:, 1], Si[:, 0]][idx]     # vyska nad dnem koryta
    bed = 1 - ss(3.0, 4.2, D + 0.6 * n)
    mud = np.maximum((1 - ss(5.5, 9.0, D + 1.5 * n)) * (1 - ss(1.6, 2.6, rel + 0.3 * n)) - bed, 0)
    img = np.zeros((N, N, 3), np.uint8); img[..., 0] = bed * 255; img[..., 1] = mud * 255
    Image.fromarray(img).save(f"{d}/T_RiverMask_505.png")

def cmd_zones(d, sketch):
    from skimage import measure
    c, H, S, P, D = load(d)
    a = np.array(Image.open(sketch).convert("RGB")).astype(int); R, G, B = a[..., 0], a[..., 1], a[..., 2]
    hh, ww = R.shape; yy, xx = np.mgrid[0:hh, 0:ww]; legend = (xx < 340) & (yy > 535)
    strokes = {"red": (R > 200) & (G < 70) & (B < 70), "ora": (R > 220) & (G > 130) & (G < 210) & (B < 70),
               "mag": (R > 140) & (G < 70) & (B > 70) & (B < 150) & (R - B > 40)}
    def to_crop(m):
        ys, xs = np.nonzero(m & ~legend); out = np.zeros((N, N), bool)
        out[np.clip(np.rint((ys - SHOT_OFF[1]) * N / SHOT_SIZE).astype(int), 0, N - 1),
            np.clip(np.rint((xs - SHOT_OFF[0]) * N / SHOT_SIZE).astype(int), 0, N - 1)] = True
        return binary_dilation(out, iterations=1)
    disk = lambda r: np.hypot(*np.mgrid[-r:r + 1, -r:r + 1]) <= r
    red, ora, mag = (to_crop(strokes[k]) for k in ("red", "ora", "mag"))
    castle = binary_fill_holes(binary_closing(red, disk(12))) | red
    rocky = binary_fill_holes(binary_closing(mag, disk(10))) | mag
    # osa cesty z oranzove cary
    cl = np.array([(x, np.nonzero(ora[:, x])[0].mean()) for x in range(N) if ora[:, x].any()], float)
    cl[:, 1] = uniform_filter1d(cl[:, 1], 9, mode="nearest")
    cl = np.vstack([[np.nonzero(castle[int(cl[0, 1])])[0].max() - 2, cl[0, 1]], cl])
    dd = np.r_[0, np.cumsum(np.hypot(np.diff(cl[:, 0]), np.diff(cl[:, 1])))]
    cp = np.c_[np.interp(np.linspace(0, dd[-1], 600), dd, cl[:, 0]), np.interp(np.linspace(0, dd[-1], 600), dd, cl[:, 1])]
    Dp = cKDTree(cp).query(P)[0].reshape(N, N) * RES
    path = (Dp < 3.0) & ~castle; trail = Dp < 1.25
    tg = np.r_[np.arange(0, dd[-1] * RES, 10), dd[-1] * RES] / RES
    pxs, pys = np.interp(tg, dd, cl[:, 0]), np.interp(tg, dd, cl[:, 1])
    hz = lambda x, y: H[int(min(max(round(y), 0), N - 1)), int(min(max(round(x), 0), N - 1))] * 100
    path_pts = [((x - 252) * 50, (y - 252) * 50, hz(x, y)) for x, y in zip(pxs, pys)]
    def poly(m):
        cc = max(measure.find_contours(m.astype(float), 0.5), key=len)
        cc = measure.approximate_polygon(cc, tolerance=2.0)[:-1]
        return [((x - 252) * 50, (y - 252) * 50, hz(x, y)) for y, x in cc]
    zp = {"castle": poly(castle), "rocky": poly(rocky), "path": path_pts}
    json.dump(zp, open(f"{d}/zone_points.json", "w"))
    rows = ["zona;#;X_cm;Y_cm;Z_cm"]
    for k, nme in (("castle", "PCG_NoForest"), ("rocky", "PCG_Rocky"), ("path", "PCG_Path")):
        rows += ["%s;%d;%d;%d;%d" % (nme, i + 1, *map(round, q)) for i, q in enumerate(zp[k])]
    open(f"{d}/Zricenina_les_zony.csv", "w").write("\n".join(rows) + "\n")
    # zony
    gy, gx = np.gradient(gaussian_filter(H, 1), RES); sl = np.degrees(np.arctan(np.hypot(gx, gy)))
    river = D < 12; rock = sl > 50; sparse = (sl > 38) & ~rock
    free = ~(river | castle | path)
    edge = free & (distance_transform_edt(~(river | castle)) * RES < 8) & ~rocky
    edgep = free & (Dp < 9) & ~rocky
    A = free & ~edge & ~edgep & ~sparse & ~rock & ~rocky
    # expozice svahu: svah obraceny k severu (stinny, vlhky) -> buk + javor; jinak dub + habr
    Hs = gaussian_filter(H, 12); sy, sx = np.gradient(Hs, RES)
    down_y = sy / (np.hypot(sx, sy) + 1e-9)          # obraz: +y = jih; po spadu k severu je gradient +y
    shady = (down_y > 0.35) & (np.degrees(np.arctan(np.hypot(sx, sy))) > 6)
    A_n = A & shady; A_s = A & ~shady
    g = slope_rgb(H).mean(-1, keepdims=True) * np.ones(3) * 0.55 + 80
    def paint(m, col, al):
        nonlocal g; g = g * (1 - al * m[..., None]) + np.array(col) * al * m[..., None]
    paint(A_s, (40, 110, 45), .75); paint(A_n, (25, 85, 75), .8); paint(free & (edge | edgep) & ~rock, (150, 170, 60), .75)
    paint(free & sparse & ~edge & ~edgep & ~rocky, (95, 140, 110), .8); paint(free & rocky, (170, 120, 160), .8)
    paint(river, (80, 140, 220), .55); paint(castle, (230, 190, 90), .8)
    paint(path, (205, 150, 95), .75); paint(trail, (140, 95, 55), .9); paint(free & rock & ~rocky, (120, 110, 110), .85)
    im = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).resize((1010, 1010), Image.NEAREST)
    dr = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, 17)
    leg = [((40, 110, 45), "A1 dubohabrina - dub, habr + liska, kapradi"), ((25, 85, 75), "A2 stinne svahy k S - buk, javor, habr"), ((150, 170, 60), "B  okraj lesa - osika, liska, jerab, bez, briza"),
           ((95, 140, 110), "D  sraz 38-50 st - ridky les"), ((120, 110, 110), "S  skala > 50 st - kameny"),
           ((170, 120, 160), "K  skalnate podlozi - borovice, briza, vres, boruvky"), ((80, 140, 220), "R  bez stromu - okoli reky (12 m)"),
           ((230, 190, 90), "C  bez stromu - hrad"), ((205, 150, 95), "P  stara cesta - trava, nizke kere, bez stromu"),
           ((140, 95, 55), "   vyslapana stezka (~2,5 m)")]
    y = 1010 - len(leg) * 26 - 14; dr.rectangle((10, y - 8, 540, 1004), fill=(255, 255, 255))
    for col, t in leg:
        dr.rectangle((20, y, 44, y + 19), fill=col); dr.text((54, y), t, fill=(0, 0, 0), font=f); y += 26
    im.save(f"{d}/Zricenina_les_plan.png")
    np.savez(f"{d}/zones_masks.npz", castle=castle, path=path, rocky=rocky, shady=shady)
    m = np.zeros((N, N, 3), np.uint8); m[..., 0] = ~free * 255; m[..., 1] = rocky * 255; m[..., 2] = trail * 255
    Image.fromarray(m).save(f"{d}/T_ForestZones_505.png")

def cmd_alders(d, seed=21):
    """Olse lepkava podel reky.
    Pravidla (jak olse roste ve skutecnosti):
      - pas tesne u vody: 0,5-5 m od hrany koryta (osa +3,5 az +8,5 m), max ~1,8 m nad dnem (vlhka pud)
      - vysepny (vnejsi) breh: souvisla linie primo na hrane, stromy se naklani nad vodu (5-10 st)
      - jesep (vnitrni breh, naplavy): ridsi, dal od vody, mladsi a mensi stromy
      - skupiny po 2-6 stromech, mezi nimi mezery 10-30 m (nahodne, ale ne pravidelne)
      - ne na srazu > 32 st, ne v plose hradu a na ceste, ne u okraje mapy
    """
    c, H, S, P, D = load(d)
    z = np.load(f"{d}/zones_masks.npz"); castle, path = z["castle"], z["path"]
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:N, 0:N]
    tree = cKDTree(S); dist, idx = tree.query(P); idx = idx.reshape(N, N)
    # smer toku a krivost osy
    T = np.gradient(S, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True)
    k = T[:, 0] * np.gradient(T[:, 1]) - T[:, 1] * np.gradient(T[:, 0])
    k = uniform_filter1d(k / (np.linalg.norm(np.diff(S, axis=0), axis=1).mean() * RES), 60, mode="nearest")
    side = np.sign(T[idx, 0] * (yy - S[idx, 1]) - T[idx, 1] * (xx - S[idx, 0]))
    outer = (-np.sign(k[idx]) * side) > 0                     # True = vysepny breh
    bend = np.clip(np.abs(k[idx]) * 35, 0, 1)
    Si = np.clip(np.rint(S).astype(int), 0, N - 1)
    rel = H - gaussian_filter(H, 3)[Si[:, 1], Si[:, 0]][idx]  # vyska nad dnem
    gy, gx = np.gradient(gaussian_filter(H, 1), RES); sl = np.degrees(np.arctan(np.hypot(gx, gy)))
    # preferovana vzdalenost od osy: vysepny breh tesne u vody, jesep dal
    d0 = np.where(outer, 4.2, 6.0 + 2.0 * bend); w = np.where(outer, 1.3, 2.2)
    p = np.exp(-((D - d0) / w) ** 2)
    p *= np.where(outer, 1.0, 0.55)                            # jesep ridsi
    p *= 1 - ss(1.4, 2.2, rel)                                 # jen vlhka pud nizko nad vodou
    p *= 1 - ss(28, 34, sl)
    p *= ~(castle | path)
    border = (xx > 6) & (xx < N - 7) & (yy > 6) & (yy < N - 7); p *= border
    # skupiny a mezery podel toku: 1D sum podel delky reky
    arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(S, axis=0), axis=1))] * RES
    L = arc[-1]; xs = np.arange(0, L + 8, 4.0)
    g1 = np.interp(arc, xs, uniform_filter1d(rng.standard_normal(len(xs)), 6, mode="wrap"))
    g2 = np.interp(arc, xs, uniform_filter1d(rng.standard_normal(len(xs)), 6, mode="wrap"))
    grp = np.where(side > 0, g1[idx], g2[idx])                # kazdy breh ma vlastni rytmus
    p *= ss(-0.05, 0.25, grp)
    # vzorkovani s minimalnim rozestupem (Poisson disk)
    cand = np.argwhere(rng.random((N, N)) < p * 0.02)
    rng.shuffle(cand)
    pts = []; tr = None; MIN = 4.0 / RES
    for (y, x) in cand:
        if pts:
            if tr is None or len(pts) % 20 == 0: tr = cKDTree(np.array(pts)[:, :2])
            if tr.query([x, y])[0] < MIN or any(np.hypot(q[0] - x, q[1] - y) < MIN for q in pts[-20:]): continue
        pts.append((x, y))
    out = []
    for x, y in pts:
        j = idx[y, x]; to = S[j] - np.array([x, y]); to /= np.linalg.norm(to) + 1e-9
        o = outer[y, x]
        lean = rng.uniform(5, 10) if o else rng.uniform(0, 4)
        scale = rng.uniform(0.85, 1.2) if o else rng.uniform(0.6, 0.95)
        out.append(dict(x=(x - 252) * 50, y=(y - 252) * 50, z=H[y, x] * 100 - 15, yaw=rng.uniform(0, 360),
                        lean=lean, dirx=float(to[0]), diry=float(to[1]), scale=scale, bank="vysep" if o else "jesep"))
    rows = ["#;X_cm;Y_cm;Z_cm;Yaw;Lean_deg;DirX;DirY;Scale;breh"]
    rows += ["%d;%d;%d;%d;%.0f;%.1f;%.3f;%.3f;%.2f;%s" % (i + 1, round(a["x"]), round(a["y"]), round(a["z"]), a["yaw"], a["lean"],
             a["dirx"], a["diry"], a["scale"], a["bank"]) for i, a in enumerate(out)]
    open(f"{d}/Zricenina_olse.csv", "w").write("\n".join(rows) + "\n")
    open(f"{d}/alder_points.txt", "w").write("\n".join("    (%d, %d, %d, %.0f, %.1f, %.3f, %.3f, %.2f, %d)," % (
        round(a["x"]), round(a["y"]), round(a["z"]), a["yaw"], a["lean"], a["dirx"], a["diry"], a["scale"], a["bank"] == "vysep") for a in out) + "\n")
    # nahled: jen teren, reka, hrad, cesta a olse (legenda zon je v Zricenina_les_plan.png)
    g = slope_rgb(H).mean(-1, keepdims=True) * np.ones(3) * 0.5 + 95
    def paint(m, col, al):
        nonlocal g; g = g * (1 - al * m[..., None]) + np.array(col) * al * m[..., None]
    paint(D < 2.6, (70, 130, 210), .85); paint((D >= 2.6) & (D < 12), (120, 165, 225), .25)
    paint(castle, (230, 190, 90), .6); paint(path, (205, 150, 95), .6)
    base = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).resize((1010, 1010), Image.NEAREST)
    dr = ImageDraw.Draw(base)
    for a in out:
        X, Y = (a["x"] / 50 + 252) * 2, (a["y"] / 50 + 252) * 2; r = 5 * a["scale"] + 3
        col = (20, 80, 30) if a["bank"] == "vysep" else (110, 170, 70)
        dr.ellipse((X - r, Y - r, X + r, Y + r), fill=col, outline=(255, 255, 255))
        dr.line((X, Y, X + a["dirx"] * a["lean"] * 2.2, Y + a["diry"] * a["lean"] * 2.2), fill=(255, 255, 255), width=2)
    f = ImageFont.truetype(FONT, 17)
    nv = sum(a["bank"] == "vysep" for a in out); nj = len(out) - nv
    leg = [((20, 80, 30), "olse - vysepny breh, nad vodou (%d)" % nv),
           ((110, 170, 70), "olse - jesep, mladsi, mensi (%d)" % nj),
           ((70, 130, 210), "reka (pas 12 m od osy svetleji)"),
           ((230, 190, 90), "hrad"), ((205, 150, 95), "stara cesta")]
    y0 = 600; y = y0 + 8; dr.rectangle((540, y0, 1004, y0 + 8 + len(leg) * 26 + 22), fill=(255, 255, 255))
    for col, t in leg:
        dr.ellipse((552, y + 1, 570, y + 19), fill=col, outline=(0, 0, 0)); dr.text((580, y), t, fill=(0, 0, 0), font=f); y += 26
    dr.text((552, y), "cara = smer a sila naklonu koruny", fill=(60, 60, 60), font=ImageFont.truetype(FONT, 14))
    base.save(f"{d}/Zricenina_olse_plan.png")
    print("olse:", len(out))

if __name__ == "__main__":
    cmd = sys.argv[1]
    {"crop": cmd_crop, "river": cmd_river, "mask": cmd_mask, "alders": cmd_alders}.get(cmd, lambda d: cmd_zones(d, sys.argv[3]))(sys.argv[2])
