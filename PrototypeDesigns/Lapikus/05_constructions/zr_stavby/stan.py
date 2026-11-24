"""stan do A (typ tent): dve stojky a hreben z tyci s kurou (SM_RuinPoleBark), ovazani spoju (SM_RuinLashing),
plachta na miru (SM_RuinCanvasTent_A podle meshes/textile/<mesh>.json), obvodove koliky u lemu (SM_RuinStakeSmall)
a napinaci snury (retez SM_RuinRope_A) ke kotvicim kolikum.

Data (constructions.json -> addons, generuje tools/constructions/gen_constructions.py z tools/ruin/nadvori_spec.stan):
  origin, u, v   ram stanu (UE cm, jednotkove vektory; u = +X smer vchodu, v = +Y odhrnuta chlopen = u otocena o +90 st.)
  mesh           jmeno meshe plachty na miru (SM_RuinCanvasTent_A; polohy tyci a koliku z meshes/textile/<mesh>.json)
  pole_sink      zapusteni stojek pod teren (m, vychozi 0,08)
  peg            dict(len, d, sink, tilt): delka, prumer, zapusteni (m) a odklon od svisle ven (st.)
  rope           dict(d, link): prumer a delka clanku lana (m)
  guys           seznam dict(id, a=(x, y, z), p=(x, y)): kotvici snura z bodu a na plachte/hrebeni ke koliku p (m)
  finish, bark   uprava dreva (vychozi raw, bark True)
entities: [Nadvori_Stan]
docs: [navrh_nadvori_stan, 05_constructions]
build_step: 05_constructions
domains: structures"""
import json, math, os
from zrlib.config import LIB_MESHES, LIB_SHAPES, WOOD_FINISH
from zrlib.stones import Stone

MESH_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "meshes", "textile"))
LIB_SHAPE_OF = {"SM_RuinCanvasTent_A": "canvas_tent"}


def _tent_meta(mesh):
    p = os.path.join(MESH_DIR, mesh + ".json")
    if not os.path.exists(p):
        raise RuntimeError("Chybi %s - spust python tools/meshes/gen_meshes.py textile" % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def build_tent(ad, terr):
    out = []; name = ad["name"]; O, U, V = ad["origin"], ad["u"], ad["v"]
    if U[0] * V[1] - U[1] * V[0] < 0:
        raise ValueError("%s: ram musi mit v = u otocenou o +90 st. v UE (u x v > 0)" % name)
    Z0 = terr.z(O[0], O[1])
    W = lambda x, y, z: (O[0] + (U[0] * x + V[0] * y) * 100, O[1] + (U[1] * x + V[1] * y) * 100, Z0 + z * 100)
    yaw_u = math.degrees(math.atan2(U[1], U[0]))
    fin = ad.get("finish", "raw"); wc = WOOD_FINISH.get(fin, "wood"); bark = ad.get("bark", True)

    def seg(sid, p0, p1, d, shape="round", cat=None, bk=bark):
        """dilec podel osy p0 -> p1 (m v ramci stanu); X = osa"""
        (x0, y0, z0), (x1, y1, z1) = W(*p0), W(*p1)
        hl = math.hypot(x1 - x0, y1 - y0); L = math.hypot(hl, z1 - z0)
        s = Stone("%s|%s" % (name, sid), cat or wc, (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2,
                  math.degrees(math.atan2(y1 - y0, x1 - x0)) if hl > 0.1 else yaw_u, L, d * 100, d * 100,
                  pitch=math.degrees(math.atan2(z1 - z0, hl)), shape=shape, bark=bk)
        out.append(s); return s

    def lash(sid, p, axis_dir, d):
        """ovazani kolem tyce O d (m) v bode p, osa podel axis_dir"""
        dx, dy, dz = axis_dir; n = math.sqrt(dx * dx + dy * dy + dz * dz); dx, dy, dz = dx / n, dy / n, dz / n
        nx, ny, nz = LIB_MESHES[LIB_SHAPES["lashing"]][0]; k = d * 100 / 8.0
        a = (p[0] - dx * 0.01, p[1] - dy * 0.01, p[2] - dz * 0.01)
        b = (p[0] + dx * 0.01, p[1] + dy * 0.01, p[2] + dz * 0.01)
        s = seg(sid, a, b, 0.01, shape="lashing", cat="rope", bk=False); s.sx, s.sy, s.sz = nx * k, ny * k, nz * k
        return s

    def peg(sid, px, py, dx_out, dy_out, tilt_deg):
        """dreveny kolik (SM_RuinStakeSmall) v (px, py) nakloneny o tilt_deg ven ve smeru (dx_out, dy_out)"""
        pg = ad.get("peg", {}); L = pg.get("len", 0.30); d = pg.get("d", 0.035); sink = pg.get("sink", 0.15)
        n = math.hypot(dx_out, dy_out) or 1.0; ux, uy = dx_out / n, dy_out / n
        t = math.radians(tilt_deg); above = L - sink
        # spodek mirne dovnitr (pod zemi), vrch mirne ven (hlava koliku)
        p0 = (px - ux * sink * math.sin(t), py - uy * sink * math.sin(t), -sink * math.cos(t))
        p1 = (px + ux * above * math.sin(t), py + uy * above * math.sin(t), above * math.cos(t))
        seg(sid, p0, p1, d, shape="stake2", cat=wc, bk=False)
        # bod uvazu snury cca 2/3 nadzemni casti koliku
        return (px + ux * above * 0.65 * math.sin(t), py + uy * above * 0.65 * math.sin(t), above * 0.65 * math.cos(t))

    mesh = ad["mesh"]; meta = _tent_meta(mesh)
    rg = meta["ridge"]; r_d = rg["d"] / 100.0; r_axis = (rg["z_top"] - rg["d"] / 2.0) / 100.0
    rx0, rx1 = rg["x"][0] / 100.0, rg["x"][1] / 100.0
    p_d = meta["pole_d"] / 100.0; sink = ad.get("pole_sink", 0.08)

    # --- 1) stojky, hreben, ovazani
    for i, (px_cm, py_cm) in enumerate(meta["poles"]):
        px, py = px_cm / 100.0, py_cm / 100.0
        seg("P%d" % i, (px, py, -sink), (px, py, r_axis), p_d).pitch = 90.0
        lash("L%d" % i, (px, py, r_axis), (1.0, 0.0, 0.0), r_d)
    seg("R", (rx0, 0.0, r_axis), (rx1, 0.0, r_axis), r_d)

    # --- 2) plachta na miru (posazena podle center a size v .json)
    c, sz = meta["center"], meta["size"]
    cx, cy, cz = W(c[0] / 100.0, c[1] / 100.0, c[2] / 100.0)
    out.append(Stone("%s|C" % name, "canvas", cx, cy, cz, yaw_u, sz[0], sz[1], sz[2], shape=LIB_SHAPE_OF[mesh]))

    # --- 3) obvodove koliky u lemu (13 ks z .json)
    tilt = ad.get("peg", {}).get("tilt", 15.0)
    for i, (px_cm, py_cm, _) in enumerate(meta.get("pegs", [])):
        px, py = px_cm / 100.0, py_cm / 100.0
        # smer ven od pudorysu: u boku ven do +-Y, u stitu ven do +-X
        dx_o = px if abs(py) < 0.8 else 0.0
        dy_o = py if abs(py) >= 0.8 else 0.0
        peg("K%02d" % i, px, py, dx_o, dy_o, tilt)

    # --- 4) napinaci snury (retez SM_RuinRope_A) a kotvici koliky
    rp = ad.get("rope", {}); r_rope = rp.get("d", 0.014); link = rp.get("link", 0.25)
    for g in ad.get("guys", []):
        gid = g["id"]; ax, ay, az = g["a"]; px, py = g["p"]
        tie = peg("G%s" % gid, px, py, px - ax, py - ay, tilt + 5.0)
        L = math.dist(W(ax, ay, az), W(*tie)) / 100.0
        m = max(1, math.ceil(L / link))
        for q in range(m):
            p0 = (ax + (tie[0] - ax) * q / m, ay + (tie[1] - ay) * q / m, az + (tie[2] - az) * q / m)
            p1 = (ax + (tie[0] - ax) * (q + 1) / m, ay + (tie[1] - ay) * (q + 1) / m, az + (tie[2] - az) * (q + 1) / m)
            seg("N%s_%02d" % (gid, q), p0, p1, r_rope, shape="rope", cat="rope", bk=False)

    return out
