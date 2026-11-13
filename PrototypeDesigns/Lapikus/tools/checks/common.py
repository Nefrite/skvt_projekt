"""spolecne nacteni pro kontroly a nahledy mimo Unreal: zricenina (03) a stavby (05) ve stejnem stavu jako v UE
(ruin_layout.json + terrain_from_level.json + manual_edits.json, constructions.json + constructions_edits.json)."""
import importlib.util, json, math, os, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
RUIN_DIR = os.path.join(ROOT, "03_ruin", "blocks")
CONSTR_DIR = os.path.join(ROOT, "05_constructions")


def _load(path, name, flag):
    setattr(sys, flag, True)
    try:
        sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    finally:
        setattr(sys, flag, False)
    return m


def ruin(layout_path=None):
    """modul build_ruin_blocks (03) jako knihovna; layout_path = jiny ruin_layout.json (napr. testovaci)"""
    R = _load(os.path.join(RUIN_DIR, "build_ruin_blocks.py"), "build_ruin_blocks", "_ruin_import_only")
    if layout_path: R.LAYOUT_PATH = os.path.abspath(layout_path)
    return R


def constructions():
    """modul build_constructions (05) jako knihovna"""
    return _load(os.path.join(CONSTR_DIR, "build_constructions.py"), "build_constructions", "_constr_import_only")


def state(layout_path=None, with_constructions=True):
    """-> dict(R, layout, terr, walls (kameny zriceniny), P, BC, data, groups (stavby 05))"""
    R = ruin(layout_path)
    lay = R.cached_level_terrain(R.load_layout()); rm, mv = R.load_manual()
    walls, P = R.compute_blocks(lay, rm, mv, None, detached=R.load_detached())
    out = dict(R=R, layout=lay, terr=R.Terrain(lay["terrain"]), walls=walls, P=P)
    if with_constructions:
        BC = constructions()
        R5 = BC.load_ruin()
        if layout_path: R5.LAYOUT_PATH = os.path.abspath(layout_path)
        data = BC.load_data()
        groups, _ = BC.compute(R5, data, *BC.load_edits())
        out.update(BC=BC, data=data, groups=groups)
    return out


# ------------------------------------------------------------------ kvadry (OBB): prunik, pudorys
def obb(s):
    """(stred, sloupce rotace 3x3, polovicni rozmery) kamene / dilce (cm)"""
    r_, p_, y_ = map(math.radians, (s.roll, s.pitch, s.yaw))
    cr, sr, cp, sp, cy, sy = math.cos(r_), math.sin(r_), math.cos(p_), math.sin(p_), math.cos(y_), math.sin(y_)
    Rz = [[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]]; Ry = [[cp, 0, -sp], [0, 1, 0], [sp, 0, cp]]; Rx = [[1, 0, 0], [0, cr, -sr], [0, sr, cr]]
    mul = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    M = mul(mul(Rz, Ry), Rx)
    return (s.x, s.y, s.z), [[M[r][c] for r in range(3)] for c in range(3)], (s.sx / 2, s.sy / 2, s.sz / 2)


def penetration(A, B):
    """hloubka pruniku dvou OBB (cm, test oddelujicich os); 0 = nedotykaji se"""
    (ca, Ra, ea), (cb, Rb, eb) = A, B
    d = [cb[i] - ca[i] for i in range(3)]
    dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
    cross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    axes = list(Ra) + list(Rb)
    for a in Ra:
        for b in Rb:
            c = cross(a, b); n = math.sqrt(dot(c, c))
            if n > 1e-6: axes.append((c[0] / n, c[1] / n, c[2] / n))
    best = 1e9
    for ax in axes:
        ra = sum(ea[k] * abs(dot(Ra[k], ax)) for k in range(3)); rb = sum(eb[k] * abs(dot(Rb[k], ax)) for k in range(3))
        o = ra + rb - abs(dot(d, ax))
        if o <= 0: return 0.0
        best = min(best, o)
    return best


def collisions(As, Bs, tol=2.0, skip=None):
    """pary (hloubka, id A, id B) s prunikem vetsim nez tol (cm), serazene od nejvetsiho"""
    grid = {}
    for b in Bs:
        r = math.sqrt(b.sx ** 2 + b.sy ** 2 + b.sz ** 2) / 2
        for gx in range(int((b.x - r) // 200), int((b.x + r) // 200) + 1):
            for gy in range(int((b.y - r) // 200), int((b.y + r) // 200) + 1):
                grid.setdefault((gx, gy), []).append(b)
    out = []
    for a in As:
        oa = obb(a); ra = math.sqrt(a.sx ** 2 + a.sy ** 2 + a.sz ** 2) / 2; seen = set()
        for gx in range(int((a.x - ra) // 200), int((a.x + ra) // 200) + 1):
            for gy in range(int((a.y - ra) // 200), int((a.y + ra) // 200) + 1):
                for b in grid.get((gx, gy), ()):
                    if id(b) in seen or b is a: continue
                    seen.add(id(b))
                    rb = math.sqrt(b.sx ** 2 + b.sy ** 2 + b.sz ** 2) / 2
                    if math.dist((a.x, a.y, a.z), (b.x, b.y, b.z)) > ra + rb or (skip and skip(a, b)): continue
                    p = penetration(oa, obb(b))
                    if p > tol: out.append((round(p, 1), a.id, b.id))
    return sorted(out, reverse=True)


def footprint(s):
    """pudorys kvadru (4 body, cm) - promitnuta delka u naklonenych dilcu"""
    y = math.radians(s.yaw); a = (math.cos(y), math.sin(y)); b = (-a[1], a[0])
    sx = s.sx * math.cos(math.radians(s.pitch)); sy = s.sy * math.cos(math.radians(s.roll))
    return [(s.x + i * a[0] * sx / 2 + j * b[0] * sy / 2, s.y + i * a[1] * sx / 2 + j * b[1] * sy / 2) for i, j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
