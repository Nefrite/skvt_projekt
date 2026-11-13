"""sut u paty zdi (stavi 05_constructions)"""
import math, random, zlib
from zrlib.stones import Stone, assign_meshes


def make_rubble(out, P, terr, removed=()):
    """trocha suti z lomovych kamenu u paty zdi (vetsinu lide odvezli) -> {zed: [Stone]}.
    Pouziva 05_constructions (sut se stavi zvlast, ne se zriceninou)."""
    res = {}
    for name, w in out.items():
        rng = random.Random(zlib.crc32(name.encode()) ^ (P["SEED"] * 977))
        faces = [s for s in w["stones"] if s.cat == "face"]
        if not faces: continue
        rub = []
        for i in range(int(len(faces) * P["RUBBLE_BLOCKS"])):
            s = rng.choice(faces); d = rng.choice((-1, 1)) * rng.uniform(80, 300)
            yaw = math.radians(s.yaw); nx, ny = -math.sin(yaw), math.cos(yaw)
            x = s.x + nx * d + rng.uniform(-60, 60); y = s.y + ny * d + rng.uniform(-60, 60)
            z = terr.z(x, y) + 8
            sid = "%s|R%d" % (name, i)
            if sid in removed: continue
            rub.append(Stone(sid, "face", x, y, z, rng.uniform(0, 360), s.sx, s.sy, s.sz, rng.uniform(-25, 25), rng.uniform(-25, 25)))
        assign_meshes(rub)
        res[name] = dict(folder=w["folder"], stones=rub)
    return res
