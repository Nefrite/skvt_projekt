"""
build_ruin.py - postavi blockout zriceniny v Unreal Editoru podle ruin_layout.json

Pouziti v UE 5.8:
  1) Python Editor Script Plugin zapnuty, otevrena mapa LapikusPrototypeMap
  2) Tools -> Execute Python Script -> tento soubor (ruin_layout.json musi lezet vedle nej,
     nebo uprav LAYOUT_PATH nize)
  3) Opakovane spusteni nejdriv smaze predchozi zriceninu (actory s tagem RUIN_TAG).
     Vse jde vratit pres Ctrl+Z.

Mimo Unreal (bez modulu unreal) skript jen spocita sloupce a vypise statistiku:
  python build_ruin.py [ruin_layout.json]

Model rozpadu (README_ruin.md kap. 4):
  1) mirny prirozeny rozpad (WEATHER, zubata koruna, V-zarezy nad otvory bez nadprazi)
  2) rozebirani podle dostupnosti a vysky (ROBBING, REACH, ACCESS_*)
  3) otvory: osteni se vylamou podle dostupnosti (OPENING_TYPES)
Vsechno v ciste Pythonu (UE nema numpy).
"""
import json, math, os, random, sys

# ------------------------------------------------------------------ nastaveni
LAYOUT_PATH = None             # None = ruin_layout.json vedle skriptu
RUIN_TAG = "Zricenina_Ruin"
CUBE_MESH = "/Engine/BasicShapes/Cube.Cube"                 # 100 cm, pivot uprostred
ROCK_MESH = "/Game/StarterContent/Props/SM_Rock.SM_Rock"   # sut (None = bez suti)
MATERIAL = "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray.MI_PrototypeGrid_Gray"  # None = vychozi
MAX_ROCKS = 450
OVERRIDE = {}                  # napr. {"ROBBING": 3.5, "SEED": 2} - prepise params z JSON

OPENING_TYPES = {
    "strilna":    dict(frame=0.20, lintel="kamen",  value=0.6),
    "okno":       dict(frame=0.25, lintel="kamen",  value=1.0),
    "okno_drevo": dict(frame=0.00, lintel="drevo",  value=0.0),
    "dvere":      dict(frame=0.30, lintel="kamen",  value=1.0),
    "portal":     dict(frame=0.35, lintel="oblouk", value=1.2),
    "brana":      dict(frame=0.45, lintel="oblouk", value=1.2),
    "prulom":     dict(frame=0.00, lintel="oblouk", value=0.0),
}

# ------------------------------------------------------------------ pomocne
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

# ------------------------------------------------------------------ rozpad
def opening_state(o, a_loc, rng, P):
    t = OPENING_TYPES[o.get("kind", "okno")]
    x0 = o["s"] - o["w"] / 2; x1 = o["s"] + o["w"] / 2; sill = o["sill"]; top = sill + o["h"]
    f_h = min(1.0, P["REACH"] / (sill + 1.5))
    score = a_loc * t["value"] * f_h * P.get("FRAME_ROB", 1.0) + rng.gauss(0, 0.06)
    robbed = "none" if (score < 0.25 or t["frame"] == 0) else ("one" if score < 0.42 else "both")
    robbed = o.get("robbed", robbed)
    side = o.get("side", "l" if rng.random() < 0.5 else "r")
    fr = t["frame"]
    wl = fr + rng.uniform(0, 0.15) if robbed == "both" or (robbed == "one" and side == "l") else 0.0
    wr = fr + rng.uniform(0, 0.15) if robbed == "both" or (robbed == "one" and side == "r") else 0.0
    arch = t["lintel"] == "oblouk"
    st = dict(kind=o.get("kind"), robbed=robbed, arch=arch, sill=sill, top=top, x0=x0, x1=x1, wl=wl, wr=wr, frame=fr)
    if arch:
        st["jamb_h"] = min(P["FRAME_REACH"], top - (x1 - x0) / 2) if robbed != "none" else 0.0
        st["lintel_lost"] = robbed == "both" and not o.get("protect", False)
    else:
        st["jamb_h"] = 0.0
        if robbed == "both" and sill > 0: st["sill"] = max(0.0, sill - 0.3)
        st["lintel_lost"] = t["lintel"] == "drevo" or robbed == "both" or o.get("lintel_lost", False)
    return st

def opening_gap(st, x):
    """Vrati (spodek, vrsek) otvoru v miste x (m), nebo None."""
    x0, x1 = st["x0"], st["x1"]
    if st["arch"]:
        if x0 - st["wl"] <= x < x0 or x1 < x <= x1 + st["wr"]:
            return (st["sill"], st["sill"] + st["jamb_h"]) if st["jamb_h"] > 0 else None
        if x0 <= x <= x1:
            r = (x1 - x0) / 2; c = (x0 + x1) / 2; spring = st["top"] - r
            return (st["sill"], spring + math.sqrt(max(r * r - (x - c) ** 2, 0)))
        return None
    if x0 - st["wl"] <= x <= x1 + st["wr"]:
        return (st["sill"], st["top"])
    return None

def wall_profile(L, H0, access, corners, openings, breaches, protect, access_points, seed, P, mid=0.88, jag=0.45):
    rng = random.Random(seed * 7919 + P["SEED"])
    step = 0.25; n = int(L / step) + 1; xs = [i * step for i in range(n)]
    # dostupnost
    a = [access] * n
    for ap in access_points:
        a = [ai + P["ACCESS_BOOST"] * math.exp(-((x - ap) / P["ACCESS_RADIUS"]) ** 2) for ai, x in zip(a, xs)]
    a = smooth([min(max(v, 0), 1) for v in a], 9)
    orng = random.Random(seed * 104729 + P["SEED"])
    states = [opening_state(o, interp(o["s"], xs, a), orng, P) for o in openings]
    # 1) prirodni rozpad
    cs = sorted(set([0.0, L] + list(corners)))
    span = max(cs[i + 1] - cs[i] for i in range(len(cs) - 1))
    sc = max(1.5, min(6.0, span / 3)); cst = P["CORNER_STRENGTH"]
    noise = smooth([rng.gauss(0, 1) for _ in range(n)], 7)
    h = []
    for x, nz in zip(xs, noise):
        t = min(min(abs(x - c) for c in cs) / sc, 1.0)
        prof = 1.0 - (1.0 - mid) * (0.5 - 0.5 * math.cos(math.pi * t))
        h.append(H0 * P["WEATHER"] * prof * (1 + cst * (1 - t)) / (1 + cst) + jag * P.get("JAG", 1.0) * nz * 1.6)
    for st in states:
        if st["lintel_lost"]:
            c = (st["x0"] + st["x1"]) / 2; w = (st["x1"] - st["x0"]) / 2; k = math.tan(math.radians(57))
            h = [min(hi, max(st["top"] - 0.3 + max(0, abs(x - c) - w) * k, st["top"] - 0.3)) for hi, x in zip(h, xs)]
    for b in breaches:
        c = (b["s0"] + b["s1"]) / 2; w = (b["s1"] - b["s0"]) / 2
        h = [min(hi, b["floor"] + max(0, abs(x - c) - w)) for hi, x in zip(h, xs)]
    # 2) rozebirani podle dostupnosti a vysky
    R = P["REACH"]; work = smooth([rng.gauss(0, 1) for _ in range(n)], 15)
    out = []
    for hi, ai, wk in zip(h, a, work):
        A = P["ROBBING"] * ai; h0 = max(hi, 0.0)
        if h0 <= R: hr = h0 - A
        else:
            t1 = (h0 * h0 - R * R) / (2 * R * max(A, 1e-6))
            hr = math.sqrt(max(h0 * h0 - 2 * R * A, 0)) if t1 >= 1 else R - A * (1 - t1)
        out.append(hr + wk * 0.5 * ai if hr < hi else hi)
    # zbytek u paty: spodni rady zasypane zeminou a suti se nevyplati rozebirat
    rem = smooth([rng.uniform(0, 1) for _ in range(n)], 11)
    h = [max(o, min(hi, P.get("REMAIN", 0.0) * (0.6 + 0.8 * r))) for o, hi, r in zip(out, h, rem)]
    for pr in protect:
        h = [max(hi, pr["min"]) if pr["s0"] <= x <= pr["s1"] else hi for hi, x in zip(h, xs)]
    c = P["COURSE"]
    h = [math.floor(min(max(hi, 0.3), H0) / c) * c for hi in h]
    return xs, h, states

# ------------------------------------------------------------------ vypocet sloupcu
def compute(layout):
    P = dict(layout["params"]); P.update(OVERRIDE)
    terr = Terrain(layout["terrain"]); cols = []; rubble = []; rrng = random.Random(P["SEED"] * 31 + 5)
    for wd in layout["walls"]:
        pts = wd["points"]
        seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) / 100 for i in range(len(pts) - 1)]
        cum = [0.0]
        for s in seg: cum.append(cum[-1] + s)
        L = cum[-1]
        corners = list(wd.get("corners", [])) + cum[1:-1]
        xs, h, states = wall_profile(L, wd["H0"], wd["access"], corners, wd.get("openings", []), wd.get("breaches", []),
                                     wd.get("protect", []), wd.get("access_points", []), wd.get("seed", 1), P,
                                     mid=wd.get("mid", 0.88))
        colw = P["COLUMN"]; t = wd["thickness"]; k = 0; s = colw / 2
        while s < L:
            while k < len(seg) - 1 and s > cum[k + 1]: k += 1
            p, q = pts[k], pts[k + 1]; f = (s - cum[k]) / max(seg[k], 1e-6)
            x = p[0] + (q[0] - p[0]) * f; y = p[1] + (q[1] - p[1]) * f
            yaw = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
            top = interp(s, xs, h); zt = terr.z(x, y)
            # pata: pod nejnizsi teren v sirce zdi
            nx, ny = -(q[1] - p[1]), (q[0] - p[0]); nl = math.hypot(nx, ny) or 1; nx, ny = nx / nl * t * 50, ny / nl * t * 50
            zb = min(zt, terr.z(x + nx, y + ny), terr.z(x - nx, y - ny)) - 100
            z0 = layout["plateau_z_cm"] if wd.get("base") == "plateau" else zt
            ztop = z0 + top * 100
            # svisle intervaly bez otvoru
            gaps = sorted([g for g in (opening_gap(st, s) for st in states) if g], key=lambda g: g[0])
            lo = zb; segs = []
            for g0, g1 in gaps:
                a0 = z0 + g0 * 100; a1 = z0 + g1 * 100
                if a0 > lo + 5: segs.append((lo, min(a0, ztop)))
                lo = max(lo, a1)
            if ztop > lo + 5: segs.append((lo, ztop))
            for za, zb2 in segs:
                if zb2 - za > 5:
                    cols.append(dict(wall=wd["name"], folder=wd["folder"], x=x, y=y, yaw=yaw, len=colw * 100 + 2,
                                     thick=t * 100, z0=za, z1=zb2))
            # sut
            miss = wd["H0"] - top
            side = wd.get("rubble", "both")
            if miss > 1.0 and rrng.random() < P["RUBBLE_FACTOR"] * min(1.0, miss / 6):
                sgn = {"out": 1, "in": -1}.get(side, rrng.choice([-1, 1]))
                # "out" = vlevo od smeru zdi je venek? urci se podle teziste hradu nize
                rubble.append(dict(folder=wd["folder"], x=x, y=y, nx=nx / max(t * 50, 1), ny=ny / max(t * 50, 1),
                                   side=side, sgn=sgn, miss=miss, t=t))
            s += colw
    # smer "ven": od teziste hradu
    cx = sum(c["x"] for c in cols) / max(len(cols), 1); cy = sum(c["y"] for c in cols) / max(len(cols), 1)
    rocks = []
    for r in rubble[:MAX_ROCKS]:
        out_dir = 1 if (r["x"] + r["nx"] - cx) ** 2 + (r["y"] + r["ny"] - cy) ** 2 > (r["x"] - cx) ** 2 + (r["y"] - cy) ** 2 else -1
        d = out_dir if r["side"] == "out" else (-out_dir if r["side"] == "in" else r["sgn"])
        off = (r["t"] * 50 + rrng.uniform(40, 220)) * d
        x = r["x"] + r["nx"] * off; y = r["y"] + r["ny"] * off
        rocks.append(dict(folder=r["folder"], x=x, y=y, z=terr.z(x, y) - 20, scale=rrng.uniform(0.35, 1.0 + min(r["miss"], 6) * 0.12),
                          yaw=rrng.uniform(0, 360), pitch=rrng.uniform(-15, 15)))
    ramps = []
    for rp in layout.get("ramps", []):
        (x0, y0), (x1, y1) = rp["start"], rp["end"]
        z0 = terr.z(x0, y0); z1 = layout["plateau_z_cm"] + rp["top"] * 100
        run = math.hypot(x1 - x0, y1 - y0); rise = z1 - z0; length = math.hypot(run, rise)
        ramps.append(dict(folder=rp["folder"], name=rp["name"], x=(x0 + x1) / 2, y=(y0 + y1) / 2, z=(z0 + z1) / 2 - 30,
                          yaw=math.degrees(math.atan2(y1 - y0, x1 - x0)), pitch=math.degrees(math.atan2(rise, run)),
                          len=length, width=rp["width"] * 100, slope=math.degrees(math.atan2(rise, run))))
    return cols, rocks, ramps

# ------------------------------------------------------------------ Unreal
def build_in_unreal(layout):
    import unreal
    cols, rocks, ramps = compute(layout)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    cube = unreal.load_asset(CUBE_MESH)
    rock = unreal.load_asset(ROCK_MESH) if ROCK_MESH else None
    mat = unreal.load_asset(MATERIAL) if MATERIAL else None
    if not cube:
        unreal.log_error("Nenalezen mesh %s" % CUBE_MESH); return
    tag = unreal.Name(RUIN_TAG)
    total = len(cols) + len(rocks) + len(ramps)
    with unreal.ScopedEditorTransaction("Build ruin"):
        old = [a for a in eas.get_all_level_actors() if tag in a.tags]
        if old: eas.destroy_actors(old)
        with unreal.ScopedSlowTask(total, "Stavim zriceninu...") as task:
            task.make_dialog(True)
            def spawn(mesh, loc, rot, scale, folder, label, material=None):
                act = eas.spawn_actor_from_object(mesh, loc, rot)
                if not act: return None
                act.set_actor_scale3d(scale)
                act.tags = [tag]
                act.set_folder_path(folder)
                act.set_actor_label(label)
                if material: act.static_mesh_component.set_material(0, material)
                return act
            for i, c in enumerate(cols):
                if task.should_cancel(): break
                task.enter_progress_frame(1)
                spawn(cube, unreal.Vector(c["x"], c["y"], (c["z0"] + c["z1"]) / 2), unreal.Rotator(roll=0, pitch=0, yaw=c["yaw"]),
                      unreal.Vector(c["len"] / 100, c["thick"] / 100, (c["z1"] - c["z0"]) / 100), c["folder"], "%s_%04d" % (c["wall"], i), mat)
            for i, r in enumerate(rocks):
                task.enter_progress_frame(1)
                if rock:
                    spawn(rock, unreal.Vector(r["x"], r["y"], r["z"]), unreal.Rotator(roll=0, pitch=r["pitch"], yaw=r["yaw"]),
                          unreal.Vector(r["scale"], r["scale"], r["scale"] * 0.7), r["folder"] + "/Sut", "Sut_%03d" % i)
            for r in ramps:
                task.enter_progress_frame(1)
                spawn(cube, unreal.Vector(r["x"], r["y"], r["z"]), unreal.Rotator(roll=0, pitch=r["pitch"], yaw=r["yaw"]),
                      unreal.Vector(r["len"] / 100, r["width"] / 100, 0.6), r["folder"], r["name"], mat)
    unreal.log("Zricenina: %d dilu zdi, %d kamenu, %d ramp (sklon %s st). Tag %s." % (
        len(cols), len(rocks), len(ramps), ", ".join("%.0f" % r["slope"] for r in ramps), RUIN_TAG))

def load_layout(path=None):
    if path is None:
        path = LAYOUT_PATH
    if path is None:
        try:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ruin_layout.json")
        except NameError:
            raise RuntimeError("Nastav LAYOUT_PATH na cestu k ruin_layout.json")
    with open(path, encoding="utf-8") as f: return json.load(f)

def main():
    if "unreal" in sys.modules or _has_unreal():
        build_in_unreal(load_layout())
    else:
        lay = load_layout(sys.argv[1] if len(sys.argv) > 1 else None)
        cols, rocks, ramps = compute(lay)
        print("dily zdi:", len(cols), "kameny:", len(rocks), "rampy:", [(r["name"], round(r["slope"])) for r in ramps])
        by = {}
        for c in cols:
            by.setdefault(c["wall"], []).append((c["z1"] - lay["plateau_z_cm"]) / 100)
        for k, v in by.items(): print("  %-18s dilu %4d  max vyska nad plosinou %.1f m" % (k, len(v), max(v)))

def _has_unreal():
    try:
        import unreal  # noqa
        return True
    except ImportError:
        return False

if __name__ == "__main__" or "unreal" in sys.modules:
    main()
