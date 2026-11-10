"""Zricenina v meandru - heightmap v2
- prirozeny meandr (stridave oblouky, mirna sinuozita)
- asymetricke brehy: vymolovy (strmy) breh na vnejsi strane oblouku, jesep/niva na vnitrni
- hlubsi koryto u vnejsiho brehu, mirny spad toku
- castice-ova hydraulicka eroze (strze, napavy) + termalni eroze (sut pod svahy)
"""
import numpy as np, sys, json
from PIL import Image
from scipy.interpolate import splprep, splev
from scipy.ndimage import gaussian_filter, zoom, uniform_filter1d
import numba as nb

OUT = sys.argv[1]
N = 1009; RES = 0.5
PXM = 184 / 36.0; OFF = np.array([162.0, 181.0])
s2w = lambda p: np.asarray(p, float) / PXM + OFF
ys, xs = np.mgrid[0:N, 0:N] * RES
P = np.stack([xs, ys], -1)
rng = np.random.default_rng(7)

def ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t)

def fbm(octaves, base, seed):
    r = np.random.default_rng(seed); out = np.zeros((N, N)); amp = 1.0; tot = 0
    for o in range(octaves):
        n = base * 2 ** o
        out += amp * zoom(r.standard_normal((n, n)), N / n, order=3)[:N, :N]; tot += amp; amp *= 0.5
    return out / tot

def resample(C, step=0.25):
    L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))]
    s = np.arange(0, L[-1], step)
    return np.stack([np.interp(s, L, C[:, 0]), np.interp(s, L, C[:, 1])], -1), s

def spline(pts_w, smooth, n=6000):
    tck, _ = splprep(np.asarray(pts_w).T, s=smooth)
    return np.stack(splev(np.linspace(0, 1, n), tck), -1)

def nearest(C, step=4):
    """distance, side sign, nearest index of curve C for every grid cell"""
    sub = P[::step, ::step].reshape(-1, 2)
    best = np.full(len(sub), 1e9); side = np.zeros(len(sub)); idx = np.zeros(len(sub))
    seg = np.diff(C, axis=0); L2 = (seg ** 2).sum(1) + 1e-9
    for i in range(len(C) - 1):
        a = C[i]; dd = seg[i]
        t = np.clip(((sub - a) @ dd) / L2[i], 0, 1)
        dist = np.linalg.norm(sub - (a + t[:, None] * dd), axis=1)
        m = dist < best
        best[m] = dist[m]
        side[m] = np.sign(dd[0] * (sub[m, 1] - a[1]) - dd[1] * (sub[m, 0] - a[0]))
        idx[m] = i + t[m]
    sh = P[::step, ::step].shape[:2]
    f = lambda g: zoom(g.reshape(sh), N / sh[0], order=1)[:N, :N]
    return f(best), f(side), f(idx)

# ------------------------------------------------------------------ stream
# world-metre control points; the middle part follows the screenshot trace,
# up- and downstream continue as alternating meanders instead of straight lines
trace_px = [(917, 75), (780, 96), (650, 110), (520, 128), (400, 158), (300, 180), (215, 194),
            (150, 204), (108, 222), (86, 252), (88, 292), (110, 340), (150, 402), (205, 476),
            (262, 560), (310, 645), (345, 727)]
up = [(530, 90), (500, 118), (468, 150), (440, 168), (410, 172), (380, 178), (355, 190)]
down = [(238, 345), (250, 368), (272, 390), (305, 402), (338, 415), (360, 438), (366, 466),
        (356, 495), (338, 520), (330, 545)]
ctrl = np.array(up + [tuple(p) for p in s2w(trace_px)] + down)
S = spline(ctrl, smooth=len(ctrl) * 6.0)
S, arc = resample(S, 0.25)
# small-scale sinuosity (1-1.5 m wobble)
T = np.gradient(S, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True)
Nrm = np.stack([-T[:, 1], T[:, 0]], -1)
wob = 2.6 * np.sin(arc / 17.0 + 1.3) + 0.8 * np.sin(arc / 6.5 + 0.4)
S = S + Nrm * wob[:, None]
S, arc = resample(S, 0.5)
# signed curvature (smoothed over ~25 m)
T = np.gradient(S, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True)
dT = np.gradient(T, axis=0) / 0.5
kap = T[:, 0] * dT[:, 1] - T[:, 1] * dT[:, 0]
kap = uniform_filter1d(kap, 50, mode="nearest")

d, side, si = nearest(S)
ii = np.clip(np.rint(si).astype(int), 0, len(S) - 1)
along = gaussian_filter(arc[ii], 10)
n1 = fbm(5, 4, 1); n2 = fbm(3, 16, 2); n3 = fbm(4, 3, 3)
# per-point bank parameters, smoothed along the stream; looked up per cell, then blurred spatially
b_pt = uniform_filter1d(np.clip(np.abs(kap) * 35.0, 0, 1), 60, mode="nearest")   # 1 = tight bend
o_pt = uniform_filter1d(-np.sign(kap), 60, mode="nearest")   # +1: left side is the outer (cut) bank
def per_side(v_out, v_in, sgn):
    wo = np.clip(0.5 + 0.5 * o_pt * sgn, 0, 1); return wo * v_out + (1 - wo) * v_in
sd = ss(-0.5, 0.5, side)                         # 1 = left side of the stream
pick = lambda vL, vR: sd * vL[ii] + (1 - sd) * vR[ii]
blur = lambda g: gaussian_filter(g, 16)
bend = blur(b_pt[ii])
outer = blur(pick(per_side(1.0, 0.0, +1), per_side(1.0, 0.0, -1)))
# floodplain: wide on the inside of bends (point bars), narrow at cut banks
wf = blur(pick(per_side(4.5 - 2.5 * b_pt, 7 + 16 * b_pt, +1), per_side(4.5 - 2.5 * b_pt, 7 + 16 * b_pt, -1))) + 2.0 * n1
# valley side: steep cut bank outside, gentle slip-off slope inside
sw = blur(pick(per_side(34 - 18 * b_pt, 55 + 35 * b_pt, +1), per_side(34 - 18 * b_pt, 55 + 35 * b_pt, -1))) + 8 * n3
fall = 3.0 * (along / along.max())   # tok tece od jihu k SV (sipka na mape), spad ~3 m
flood = 2.2 + fall + 0.012 * d + 0.25 * n2
hill = 18 + 9 * n1 + 18 * ss(230, 470, xs) + 6 * ss(150, 20, ys)
H = flood + hill * ss(wf, wf + sw, d)

# ------------------------------------------------------------------ spur (ostroh)
cast_w = s2w((600, 445)); ci = (int(cast_w[1] / RES), int(cast_w[0] / RES))
axis_px = [(235, 522), (270, 515), (380, 497), (480, 478), (600, 448), (720, 428), (820, 395),
           (950, 355), (1150, 320), (1500, 300), (2300, 280)]
A = spline(s2w(axis_px), len(axis_px) * 2.0, 3000)
da, sa, ia = nearest(A)
LA = np.r_[0, np.cumsum(np.linalg.norm(np.diff(A, axis=0), axis=1))]
ta = np.interp(ia, np.arange(len(A)), LA)
across = da * sa + 5.0 * n3
pn = (int((cast_w[1] - 20) / RES), int(cast_w[0] / RES))
if across[pn] < 0: across = -across                 # + = north
t_rel = ta - ta[ci]
# zahloubeni pod jizni stenou ostrohu (aby stena vynikla jako na mape)
H -= 13.0 * ss(-12, -40, across) * (1 - ss(60, 140, -across)) * (1 - ss(30, 90, t_rel)) * ss(-110, -70, t_rel) * ss(wf, wf + sw, d) * ss(-0.3, 0.3, side * np.sign(side[ci]))
top = np.interp(t_rel, [-75, -66, -50, -32, -18, 30, 38, 60, 140, 400],
                       [  2,   4,  13,  23,  30, 30, 31, 33,  36, 38]) + fall[ci]
drop_n = ss(3, 72, across)
cliff = 1 - ss(5, 45, t_rel)
drop_s = cliff * (0.72 * ss(9, 19, -across) + 0.28 * ss(19, 48, -across)) + (1 - cliff) * ss(6, 55, -across)
spur = top * (1 - np.maximum(drop_n, drop_s))
spur += 0.8 * n2 * ss(5, 20, np.abs(across))
rock_mask = ss(8, 12, -across) * (1 - ss(22, 30, -across)) * ss(-70, -40, t_rel) * (1 - ss(30, 50, t_rel))
spur += 2.5 * gaussian_filter(rng.standard_normal((N, N)), 2) * rock_mask
spur *= ss(wf - 2, wf + 30, d)
k = 4.0
hh = np.clip(0.5 + 0.5 * (spur - H) / k, 0, 1)
H = H * (1 - hh) + spur * hh + k * hh * (1 - hh)

# ------------------------------------------------------------------ erosion
@nb.njit(cache=True)
def hydraulic(h, n_drops, seed, rad, inertia, cap, min_slope, erode, deposit, evap, grav, life):
    np.random.seed(seed)
    n = h.shape[0]
    offs = []
    for oy in range(-rad, rad + 1):
        for ox in range(-rad, rad + 1):
            dd = (ox * ox + oy * oy) ** 0.5
            if dd <= rad:
                offs.append((oy, ox, rad - dd))
    wsum = 0.0
    for o in offs: wsum += o[2]
    for _ in range(n_drops):
        x = np.random.random() * (n - 2); y = np.random.random() * (n - 2)
        dx = 0.0; dy = 0.0; sp = 1.0; water = 1.0; sed = 0.0
        for _s in range(life):
            ix = int(x); iy = int(y)
            if ix < 1 or iy < 1 or ix >= n - 2 or iy >= n - 2: break
            fx = x - ix; fy = y - iy
            h00 = h[iy, ix]; h10 = h[iy, ix + 1]; h01 = h[iy + 1, ix]; h11 = h[iy + 1, ix + 1]
            gx = (h10 - h00) * (1 - fy) + (h11 - h01) * fy
            gy = (h01 - h00) * (1 - fx) + (h11 - h10) * fx
            hc = h00 * (1 - fx) * (1 - fy) + h10 * fx * (1 - fy) + h01 * (1 - fx) * fy + h11 * fx * fy
            dx = dx * inertia - gx * (1 - inertia); dy = dy * inertia - gy * (1 - inertia)
            ln = (dx * dx + dy * dy) ** 0.5
            if ln < 1e-9: break
            dx /= ln; dy /= ln
            nx = x + dx; ny = y + dy
            jx = int(nx); jy = int(ny)
            if jx < 1 or jy < 1 or jx >= n - 2 or jy >= n - 2: break
            gfx = nx - jx; gfy = ny - jy
            hn = (h[jy, jx] * (1 - gfx) * (1 - gfy) + h[jy, jx + 1] * gfx * (1 - gfy)
                  + h[jy + 1, jx] * (1 - gfx) * gfy + h[jy + 1, jx + 1] * gfx * gfy)
            dh = hn - hc
            c = max(-dh, min_slope) * sp * water * cap
            if sed > c or dh > 0:
                amt = min(dh, sed) if dh > 0 else (sed - c) * deposit
                sed -= amt
                h[iy, ix] += amt * (1 - fx) * (1 - fy); h[iy, ix + 1] += amt * fx * (1 - fy)
                h[iy + 1, ix] += amt * (1 - fx) * fy; h[iy + 1, ix + 1] += amt * fx * fy
            else:
                amt = min((c - sed) * erode, -dh, 0.15)
                for o in offs:
                    yy = iy + o[0]; xx = ix + o[1]
                    if yy >= 0 and xx >= 0 and yy < n and xx < n:
                        e = amt * o[2] / wsum
                        h[yy, xx] -= e
                sed += amt
            sp = (max(sp * sp + dh * grav, 0.0)) ** 0.5
            water *= (1 - evap)
            x = nx; y = ny
    return h

def thermal(h, talus_tan, iters=40, rate=0.25):
    # move material downhill where slope exceeds the talus angle (cell units)
    for _ in range(iters):
        acc = np.zeros_like(h)
        hp = np.pad(h, 1, mode="edge"); n0, n1_ = h.shape
        for sy, sx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            diff = h - hp[1 + sy:1 + sy + n0, 1 + sx:1 + sx + n1_]
            ex = np.where(diff > talus_tan, (diff - talus_tan) * rate * 0.25, 0.0)
            acc -= ex
            ep = np.zeros_like(hp); ep[1 + sy:1 + sy + n0, 1 + sx:1 + sx + n1_] = ex
            acc += ep[1:-1, 1:-1]
        h = h + acc
    return h

Hc = H / RES                       # heights in cell units -> gradient = tan(slope)
before = Hc.copy()
Hc = hydraulic(Hc, 220000, 11, 3, 0.05, 4.0, 0.002, 0.2, 0.25, 0.015, 4.0, 80)
talus = np.where(rock_mask > 0.3, 2.5, 0.95)  # rock cliff may stay ~68 deg, soil ~44 deg
Hc = thermal(Hc, talus)
H = Hc * RES
er = (before - Hc) * RES

# ------------------------------------------------------------------ man-made features (after erosion)
cx, cy = cast_w
el = ((xs - (cx - 6)) / 34) ** 2 + ((ys - cy) / 13) ** 2
pl = 1 - ss(0.75, 1.25, el)
plat = 30.0 + fall[ci]
H = H * (1 - pl) + plat * pl
ditch = np.exp(-((t_rel - 37.0) / 3.5) ** 2) * (1 - ss(9, 15, np.abs(across)))
H -= 6.0 * ditch

# ------------------------------------------------------------------ channel (after erosion)
u = d * np.where(outer > 0.5, 1, -1)              # + toward outer bank
c_off = 0.9 * bend                                 # thalweg shifted outward in bends
half = 2.6 + 0.6 * bend
prof = 1 - ss(half * 0.55, half, np.abs(u - c_off))
depth = 1.1 + 0.9 * bend * ss(-half, half, u)      # deeper pool at the cut bank
bed_h = flood - depth - 0.012 * d
H = H * (1 - prof) + np.minimum(H, bed_h) * prof
H = gaussian_filter(H, 0.7)
H = np.maximum(H, 0)

ZMAX = 64.0
Image.fromarray(np.clip(H / ZMAX * 65535, 0, 65535).astype(np.uint16)).save(f"{OUT}/Zricenina_heightmap_1009.png")
np.save(f"{OUT}/H.npy", H); np.save(f"{OUT}/S.npy", S)
json.dump({"min": float(H.min()), "max": float(H.max()), "plateau": float(H[ci]),
           "erosion_max_cut": float(er.max()), "erosion_max_fill": float(-er.min()),
           "water_level_upstream": float(2.2 + 3.0 - 0.6), "water_level_downstream": float(2.2 - 0.6)}, sys.stdout)
