"""drevo ve vezi (typ tower_floor, constructions.json -> floors): tramy v kapsach, prkna, pruvlak, podesta, schody."""
import math, random, zlib
from zrlib.config import WOOD_FINISH, WOOD_FINISH_DEFAULT
from zrlib.stones import Stone


def build_tower_floor(fs, P, walls_out, terr=None):
    """Drevo ve vezi (constructions.json -> floors): tramy v kapsach a hrube prkna v patrech, pruvlak se sloupem,
    podesta pred dvermi, provizorni schody. (Puvodne cast build_floor_stones ve 03.)
    Souradnice v ramu veze: u (m) podel fs["u"], v (m) podel fs["v"] od fs["origin"]."""
    rng = random.Random(zlib.crc32(fs["name"].encode()) ^ P["SEED"])
    ox, oy = fs["origin"]; ux, uy = fs["u"]; vx, vy = fs["v"]
    u0, u1, v0, v1 = fs["inner"]
    W = lambda u, v: (ox + (u * ux + v * vx) * 100, oy + (u * uy + v * vy) * 100)
    yaw_u = math.degrees(math.atan2(uy, ux)); yaw_v = math.degrees(math.atan2(vy, vx))
    ref = fs["ref_z"]; out = []
    # --- patra: tramy v kapsach, prkna na tramech (horni plocha prken = ref_z + n * storey)
    fin = dict(WOOD_FINISH_DEFAULT, **fs.get("finish", {}))
    WC = lambda part: WOOD_FINISH.get(fin.get(part, "raw"), "wood")       # kategorie (material) dreva podle casti
    bm = fs.get("beams", {}); pk = fs.get("planks", {})
    def wall_stands(x, y, zmin):
        for wn in fs.get("walls", []):
            for s_ in walls_out.get(wn, {}).get("stones", []):
                if abs(s_.x - x) < 130 and abs(s_.y - y) < 130 and s_.z > zmin: return True
        return False
    for lvl in fs.get("levels", []):
        zt = ref + lvl * fs["storey"] * 100
        hatch = fs.get("hatches", {}).get(str(lvl), fs.get("hatch"))     # otvor pro schody / zebrik v tomto patre
        bh = bm.get("h", 0.28) * 100; bw = bm.get("w", 0.26) * 100; brg = bm.get("bearing", 0.33)
        ok_v = []
        for i, vb in enumerate(bm["v"]):
            ea = W(u0 - brg / 2, vb); eb = W(u1 + brg / 2, vb)
            if not (wall_stands(ea[0], ea[1], zt + 30) and wall_stands(eb[0], eb[1], zt + 30)): continue   # zed u kapsy spadla -> tram chybi
            sid = "%s|B%d|%d" % (fs["name"], lvl, i); srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
            x, y = W((u0 + u1) / 2, vb + srng.uniform(-0.02, 0.02))
            out.append(Stone(sid, WC("beams"), x, y, zt - 6 - bh / 2, yaw_u + srng.uniform(-0.4, 0.4), (u1 - u0 + 2 * brg) * 100 - 4, bw, bh,
                             pitch=srng.uniform(-0.3, 0.3)))
            ok_v.append(vb)
        if len(ok_v) < 2: continue
        t = pk.get("t", 0.05) * 100; u = u0; r = 0
        while u < u1 - 0.05:
            w_ = min(rng.uniform(pk.get("wmin", 0.2), pk.get("wmax", 0.34)), u1 - u)
            uc = u + w_ / 2; u += w_ + rng.uniform(0.005, 0.02); r += 1
            if w_ < 0.08: continue
            # prkno z kusu, spoje vzdy nad tramem (2-3 pole na kus), prvni a posledni kus az ke zdi
            joints = [ok_v[0] - 0.75 if ok_v[0] - 0.75 > v0 else v0]
            k = rng.randint(1, 2)
            while k < len(ok_v) - 1:
                joints.append(ok_v[k]); k += rng.randint(2, 3)
            joints.append(v1)
            for j in range(len(joints) - 1):
                a, b = joints[j], joints[j + 1]
                if j == 0: a = v0
                pieces = [(a, b)]
                if hatch and hatch[0] < uc < hatch[1]:
                    pieces = [(p0, min(p1, hatch[2])) for p0, p1 in pieces if p0 < hatch[2]] + \
                             [(max(p0, hatch[3]), p1) for p0, p1 in pieces if p1 > hatch[3]]
                for q, (pa, pb) in enumerate(pieces):
                    if pb - pa < 0.3: continue
                    sid = "%s|K%d|%d|%d%s" % (fs["name"], lvl, r, j, "abc"[q])
                    srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
                    if srng.random() < pk.get("missing", 0.04): continue
                    x, y = W(uc + srng.uniform(-0.01, 0.01), (pa + pb) / 2)
                    out.append(Stone(sid, WC("planks_%d" % lvl) if "planks_%d" % lvl in fin else WC("planks"), x, y, zt - 1 - t / 2 + srng.uniform(-0.4, 0.4), yaw_v + srng.uniform(-1.0, 1.0),
                                     (pb - pa) * 100 - 1, w_ * 100 - 0.5, t, roll=srng.uniform(-0.6, 0.6)))
    # --- pruvlak (sever-jih pod tramy, konce v kapsach) a sloup s hlavici pod nim
    gd = fs.get("girder")
    if gd:
        gw = gd.get("w", 0.30) * 100; ch = fs.get("course", 0.35) * 100
        for lvl in gd.get("levels", []):
            zt = ref + lvl * fs["storey"] * 100; zg1 = zt - ch; zg0 = zg1 - ch      # pod tramy, jedna rada (kapsy v J a S zdi)
            ea = W(gd["u"], v0 - 0.2); eb = W(gd["u"], v1 + 0.2)
            if not (wall_stands(ea[0], ea[1], zg1 + 30) and wall_stands(eb[0], eb[1], zg1 + 30)): continue
            sid = "%s|G%d" % (fs["name"], lvl)
            x, y = W(gd["u"], (v0 + v1) / 2)
            out.append(Stone(sid, WC("girder"), x, y, (zg0 + zg1) / 2 - 0.5, yaw_v, (v1 - v0 + 0.66) * 100 - 4, gw, ch - 1))
            zf = ref + (lvl - 1) * fs["storey"] * 100 - (0 if lvl == 1 else 1)     # podlaha pod sloupem (dlazba / prkna)
            ps = gd.get("post", 0.25) * 100
            for j, pv in enumerate(gd.get("post_v", [])):
                x, y = W(gd["u"], pv)
                head = 15
                out.append(Stone("%s|G%d|P%d" % (fs["name"], lvl, j), WC("posts"), x, y, (zf + zg0 - head) / 2, yaw_v, ps, ps, zg0 - head - zf))
                out.append(Stone("%s|G%d|H%d" % (fs["name"], lvl, j), WC("heads"), x, y, zg0 - head / 2, yaw_v, 70, gw, head - 0.5))   # hlavice (sedlo)
    # --- podesta pred dvermi (vne veze): tramy z kapes ven, prkna podel zdi, sloupky na terenu
    pc = fs.get("porch")
    if pc:
        zt = ref + pc.get("level", 1) * fs["storey"] * 100
        vw = pc["v_wall"]; dp = pc.get("depth", 1.3); wd_ = pc.get("width", 2.6) / 2
        bw, bh = pc.get("beam", (0.24, 0.28))
        for j, du in enumerate((-pc.get("beam_du", 1.1), pc.get("beam_du", 1.1))):
            x, y = W(pc["u"] + du, vw + (dp - 0.35) / 2)
            out.append(Stone("%s|D|B%d" % (fs["name"], j), WC("porch_beams"), x, y, zt - 6 - bh * 50, yaw_v, (dp + 0.35) * 100, bw * 100, bh * 100))
            if pc.get("posts") and terr is not None:
                x, y = W(pc["u"] + du, vw + dp - 0.12)
                zg = terr.z(x, y) - 10
                ztop = zt - 6 - bh * 100
                out.append(Stone("%s|D|P%d" % (fs["name"], j), WC("porch_posts"), x, y, (zg + ztop) / 2, yaw_v, 20, 20, ztop - zg))
            br = pc.get("braces")
            if br:     # sikma vzpera: pata oprena o lic zdi, hlava pod tramem (tram je zapusteny v kapse)
                dv_, dz_, bw_ = br.get("dv", 0.75), br.get("dz", 0.75), br.get("w", 0.14)
                ztop = zt - 6 - bh * 100
                ang = math.atan2(dz_, dv_); Lb = math.hypot(dv_, dz_) * 100
                x, y = W(pc["u"] + du, vw + dv_ / 2 + 0.02)
                out.append(Stone("%s|D|V%d" % (fs["name"], j), WC("porch_braces"), x, y, ztop - dz_ * 50 - bw_ * 30, yaw_v, Lb + bw_ * 60, bw_ * 100, bw_ * 100,
                                 pitch=math.degrees(ang)))
        t = 5.0; v = vw + 0.02; r = 0
        while v < vw + dp - 0.05:
            w_ = min(rng.uniform(0.22, 0.32), vw + dp - v)
            sid = "%s|D|K%d" % (fs["name"], r); srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
            x, y = W(pc["u"] + srng.uniform(-0.03, 0.03), v + w_ / 2)
            out.append(Stone(sid, WC("porch_planks"), x, y, zt - 1 - t / 2, yaw_u + srng.uniform(-1.2, 1.2), 2 * wd_ * 100, w_ * 100 - 1, t))
            v += w_ + 0.01; r += 1
    # --- provizorni schody: dve schodnice (tramy) a do nich zasazene hrube fosny, vedou otvorem do patra
    for k, sd in enumerate(fs.get("stairs", [])):
        za = ref + sd["from"] * fs["storey"] * 100; zb_ = ref + sd["to"] * fs["storey"] * 100
        A = math.radians(sd.get("angle", 60)); rise = (zb_ - za) / 100
        run = rise / math.tan(A); hw = sd.get("width", 0.8) / 2
        # axis "u": schody podel tramu (mezi dvema tramy, otvor muze byt dlouhy); "v": napric tramy
        along_u = sd.get("axis", "v") == "u"
        t1 = sd["u_top"] if along_u else sd["v_top"]; dirn = sd.get("dir", 1)
        t0 = t1 - dirn * run; cc = sd["v"] if along_u else sd["u"]
        P2 = (lambda a, c: W(a, c)) if along_u else (lambda a, c: W(c, a))
        yaw_run = (yaw_u if along_u else yaw_v) + (0 if dirn > 0 else 180); yaw_tr = yaw_v if along_u else yaw_u
        sw, sh = sd.get("stringer", (0.12, 0.22))
        L = math.hypot(run, rise)
        for side in (-1, 1):
            sid = "%s|S%d|T%d" % (fs["name"], k, 0 if side < 0 else 1)
            x, y = P2((t0 + t1) / 2, cc + side * (hw + sw / 2))
            out.append(Stone(sid, WC("stairs"), x, y, (za + zb_) / 2 + 4, yaw_run, L * 100 + 15, sw * 100, sh * 100, pitch=math.degrees(A)))
        n = max(2, int(round(rise / sd.get("step", 0.25))))
        for i in range(1, n):
            sid = "%s|S%d|F%d" % (fs["name"], k, i)
            srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
            zr = rise * i / n; a_ = t0 + dirn * zr / math.tan(A)
            x, y = P2(a_, cc + srng.uniform(-0.01, 0.01))
            out.append(Stone(sid, WC("stairs"), x, y, za + zr * 100 + srng.uniform(-0.8, 0.8), yaw_tr + srng.uniform(-2, 2),
                             (2 * hw + 0.06) * 100, srng.uniform(22, 27), 5.5, roll=srng.uniform(-1.2, 1.2)))
    return out
