"""zakladni geometrie a pomocne funkce (cisty Python, bez numpy - kvuli Pythonu v Unrealu)"""
import math, zlib


def smooth(v, k):
    n = len(v); h = k // 2; out = []
    for i in range(n):
        s = 0.0
        for j in range(i - h, i - h + k):
            s += v[min(max(j, 0), n - 1)]
        out.append(s / k)
    return out

def interp(xq, xs, ys):
    if xq <= xs[0]: return ys[0]
    if xq >= xs[-1]: return ys[-1]
    lo, hi = 0, len(xs) - 1
    while hi - lo > 1:
        m = (lo + hi) // 2
        if xs[m] <= xq: lo = m
        else: hi = m
    t = (xq - xs[lo]) / (xs[hi] - xs[lo]); return ys[lo] + (ys[hi] - ys[lo]) * t

class Terrain:
    def __init__(self, t): self.t = t
    def z(self, x, y):     # cm
        t = self.t; fx = (x - t["x0"]) / t["step"]; fy = (y - t["y0"]) / t["step"]
        ix = min(max(int(math.floor(fx)), 0), t["nx"] - 2); iy = min(max(int(math.floor(fy)), 0), t["ny"] - 2)
        ax = min(max(fx - ix, 0), 1); ay = min(max(fy - iy, 0), 1); Z = t["z"]
        return (Z[iy][ix] * (1 - ax) + Z[iy][ix + 1] * ax) * (1 - ay) + (Z[iy + 1][ix] * (1 - ax) + Z[iy + 1][ix + 1] * ax) * ay

def _hash01(*k):
    return (zlib.crc32(("%d|" * len(k) % k).encode()) & 0xFFFFFF) / float(0xFFFFFF)

def _pt_on(points, s):
    """bod na lomene care ve vzdalenosti s (m) od prvniho bodu"""
    c = 0.0
    for i in range(len(points) - 1):
        p, q = points[i], points[i + 1]; ln = math.hypot(q[0] - p[0], q[1] - p[1]) / 100
        if s <= c + ln or i == len(points) - 2:
            f = (s - c) / max(ln, 1e-6); return p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f
        c += ln

def _wall_len(pts):
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)) / 100

def _clip_segment_box(p, q, x0, y0, x1, y1):
    """Liang-Barsky: cast usecky p->q uvnitr obdelniku, vrati (t0, t1) nebo None."""
    dx, dy = q[0] - p[0], q[1] - p[1]; t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0: return None
        else:
            r = qq / pp
            if pp < 0: t0 = max(t0, r)
            else: t1 = min(t1, r)
    return (t0, t1) if t0 < t1 else None


# ------------------------------------------------------------------ hash, rovina, polygon (05)
def crc(s):
    """deterministicky seed z textu (id kamene, jmeno stavby)"""
    import zlib
    return zlib.crc32(s.encode())


def inside_poly(poly, x, y):
    """bod uvnitr polygonu (seznam bodu)"""
    c = False
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        if (ay > y) != (by > y) and x < ax + (bx - ax) * (y - ay) / (by - ay): c = not c
    return c


def plane_fit(P):
    """nejmensi ctverce z = c0 + cx*x + cy*y pres body [((x, y), z)] - ciste v Pythonu (normalni rovnice, Cramer)"""
    mx = sum(q[0] for q, _ in P) / len(P); my = sum(q[1] for q, _ in P) / len(P); mz = sum(z for _, z in P) / len(P)
    sxx = sum((q[0] - mx) ** 2 for q, _ in P); syy = sum((q[1] - my) ** 2 for q, _ in P)
    sxy = sum((q[0] - mx) * (q[1] - my) for q, _ in P)
    sxz = sum((q[0] - mx) * (z - mz) for q, z in P); syz = sum((q[1] - my) * (z - mz) for q, z in P)
    det = sxx * syy - sxy * sxy
    if abs(det) < 1e-9: return mz, 0.0, 0.0
    cx = (sxz * syy - syz * sxy) / det; cy = (syz * sxx - sxz * sxy) / det
    return mz - cx * mx - cy * my, cx, cy


# ------------------------------------------------------------------ polylinie v pudorysu (cm), s v m (gen_constructions, ostroh)
def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy); return dx / l, dy / l


def offset_polyline(pts, off, ref):
    """polylinie posunuta o off (cm) na stranu bodu ref (pro kazdy usek zvlast, spojeni v prusecicich)"""
    segs = []
    for a, b in zip(pts[:-1], pts[1:]):
        ux, uy = unit(a, b); nx, ny = -uy, ux
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if (ref[0] - m[0]) * nx + (ref[1] - m[1]) * ny < 0: nx, ny = -nx, -ny
        segs.append(((a[0] + nx * off, a[1] + ny * off), (b[0] + nx * off, b[1] + ny * off)))
    out = [segs[0][0]]
    for (a1, b1), (a2, b2) in zip(segs[:-1], segs[1:]):
        p = isect_lines(a1, b1, a2, b2); out.append(p or b1)
    out.append(segs[-1][1]); return out


def isect_lines(a1, b1, a2, b2):
    d1 = (b1[0] - a1[0], b1[1] - a1[1]); d2 = (b2[0] - a2[0], b2[1] - a2[1]); den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-9: return None
    t = ((a2[0] - a1[0]) * d2[1] - (a2[1] - a1[1]) * d2[0]) / den
    return (a1[0] + d1[0] * t, a1[1] + d1[1] * t)


def extend_polyline(pts, e=400.0):
    ext = [list(p) for p in pts]
    ux, uy = unit(ext[1], ext[0]); ext[0] = [ext[0][0] + ux * e, ext[0][1] + uy * e]
    ux, uy = unit(ext[-2], ext[-1]); ext[-1] = [ext[-1][0] + ux * e, ext[-1][1] + uy * e]
    return ext


def polyline_hits(pts, other, ext_other=True):
    """pruseciky polylinie pts (konce prodlouzene o 4 m) s polylinii other (taky prodlouzenou)
    -> (prodlouzena pts, seznam (s v cm podel prodlouzene pts, bod))"""
    ext = extend_polyline(pts)
    if ext_other and len(other) > 1 and other[0] != other[1]: other = extend_polyline(other)
    res = []; c = 0.0
    for a, b in zip(ext[:-1], ext[1:]):
        for q, r in zip(other[:-1], other[1:]):
            d1 = (b[0] - a[0], b[1] - a[1]); d2 = (r[0] - q[0], r[1] - q[1]); den = d1[0] * d2[1] - d1[1] * d2[0]
            if abs(den) < 1e-9: continue
            t = ((q[0] - a[0]) * d2[1] - (q[1] - a[1]) * d2[0]) / den; u = ((q[0] - a[0]) * d1[1] - (q[1] - a[1]) * d1[0]) / den
            if 0 <= t <= 1 and -1e-6 <= u <= 1 + 1e-6: res.append((c + t * math.hypot(*d1), (a[0] + d1[0] * t, a[1] + d1[1] * t)))
        c += math.hypot(b[0] - a[0], b[1] - a[1])
    return ext, sorted(res)


def cut_polyline(pts, start_line=None, end_line=None):
    """vyrez polylinie mezi prvnim prusecikem se start_line a poslednim s end_line (konce se pripadne prodlouzi)"""
    ext = extend_polyline(pts)
    s0 = 400.0; L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(ext[:-1], ext[1:])); s1 = L - 400.0
    if start_line: s0 = polyline_hits(pts, start_line)[1][0][0]
    if end_line: s1 = polyline_hits(pts, end_line)[1][-1][0]
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


def project_s(pts, p):
    """s (m) nejblizsiho bodu polylinie k p"""
    best = None; c = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        ln = math.hypot(b[0] - a[0], b[1] - a[1]); ux, uy = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
        t = min(max((p[0] - a[0]) * ux + (p[1] - a[1]) * uy, 0), ln)
        q = (a[0] + ux * t, a[1] + uy * t); dd = math.hypot(p[0] - q[0], p[1] - q[1])
        if best is None or dd < best[0]: best = (dd, (c + t) / 100)
        c += ln
    return best[1]


def point_at(pts, s):
    c = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        ln = math.hypot(b[0] - a[0], b[1] - a[1]) / 100
        if s <= c + ln or b is pts[-1]:
            f = (s - c) / ln; return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        c += ln


def polyline_len(pts):
    """delka polylinie (m)"""
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)) / 100
