"""03 podlahy v layoutu (kamenna dlazba)"""
import math, random, zlib
from zrlib.stones import Stone


def build_floor_stones(fs, P, walls_out, terr=None):
    """Podlahy zriceniny (layout["floors"]): kamenna dlazba prizemi veze. (Drevene podlahy, schody a ochoz veze
    stavi 05_constructions - zr_stavby/vez.py.)
    Souradnice v ramu veze: u (m) podel fs["u"], v (m) podel fs["v"] od fs["origin"]."""
    rng = random.Random(zlib.crc32(fs["name"].encode()) ^ P["SEED"])
    ox, oy = fs["origin"]; ux, uy = fs["u"]; vx, vy = fs["v"]
    u0, u1, v0, v1 = fs["inner"]
    W = lambda u, v: (ox + (u * ux + v * vx) * 100, oy + (u * uy + v * vy) * 100)
    yaw_u = math.degrees(math.atan2(uy, ux)); yaw_v = math.degrees(math.atan2(vy, vx))
    ref = fs["ref_z"]; out = []
    # --- kamenna podlaha prizemi (horni plocha = ref_z)
    sf = fs.get("stone_floor")
    if sf:
        t = sf.get("thickness", 0.18) * 100; v = v0; r = 0
        while v < v1 - 0.05:
            dv = min(rng.uniform(0.45, 0.8), v1 - v); u = u0 - rng.uniform(0, 0.4) * (r % 2); c = 0
            while u < u1 - 0.05:
                du = rng.uniform(0.5, 1.0); a, b = max(u, u0), min(u + du, u1)
                sid = "%s|P|%d|%d" % (fs["name"], r, c); c += 1; u += du
                if b - a < 0.15: continue
                srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
                if srng.random() < sf.get("missing", 0.07): continue
                x, y = W((a + b) / 2, v + dv / 2)
                tilt = srng.random() < 0.12
                out.append(Stone(sid, "floor", x, y, ref - t / 2 + (srng.uniform(0, 3) if tilt else 0), yaw_u + srng.uniform(-1.5, 1.5),
                                 (b - a) * 100 - 1.5, dv * 100 - 1.5, t, pitch=srng.uniform(-3, 3) if tilt else 0.0,
                                 roll=srng.uniform(-3, 3) if tilt else 0.0))
            v += dv; r += 1
    return out
