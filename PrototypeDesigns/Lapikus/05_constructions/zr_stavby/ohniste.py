"""ohniste / vyhen (typ hearth): kamenny stul z kamene rozvalin vymazany hlinou s ohnistem, bocni zidky, dymnik a komin
z prouti a hliny. Dymnik visi na zavesnych tycich z vymen mezi krokvemi, komin prochazi mezi vymenami nad strechu.

Data (constructions.json -> addons, generuje tools/constructions/gen_constructions.py z tools/ruin/palac_spec.py):
  origin, u, v     ram stavby (UE cm, jednotkove vektory), rozmery v m v tomto ramu: a = podel u, c = podel v
  roof             jmeno strechy (typ pult_roof): od jejiho terenu se pocitaji vysky, mezi jeji krokve jdou vymeny
  table            kamenny stul: dict(a (a0, a1), c (c0, c1), h, course (vyska rady))
  daub             tloustka hlineneho mazu na stole (m); pit = ohniste: dict(a, c, w, d (zapusteni pod maz))
  walls            bocni zidky: [dict(id, a (a0, a1), c (c0, c1), h, course, hole = dict(a, w, z (z0, z1)) otvor pro vyfucnu,
                   base = spodek m nad terenem (bez nej stoji na zemi; zdi pece a zidky pod plotnou stoji na stole))]
  dome             hlinena klenba pece (mesh SM_RuinOvenDome): dict(a (a0, a1), c (c0, c1), z (spodek, vrch m))
  boxes            jednoduche kvadry: [dict(id, cat (iron / charcoal / daub ...), a (a0, a1), c (c0, c1), z (z0, z1), top = True:
                   patri do sady stage_top)] - zelezny pas nad ustim, poklop, plotna, tmavy vnitrek pece, uhli pod plotnou
  props            hotove meshe jako samostatne actory (rucni doladeni pres capture): [dict(id, shape (LIB_SHAPES), cat,
                   a, c (stred bounding boxu), zc (stred m nad terenem), size (cm), top)] - poklop usti pece;
                   kvadr v boxes s loose = True je taky samostatny actor (plotna)
  flue             sopouch (hlineny kourovod z klenby do dymniku, mesh komina): dict(a, c, w, z (spodek, vrch m))
  hood             dymnik: dict(a, c (stred), size (podel a, podel c), bottom (spodni okraj), h)
  chimney          komin: dict(a, c (stred), w, top (vrch))
  trimmers         vymeny mezi krokvemi po obou stranach komina: dict(d (prumer), gap (od komina))
  hangers          zavesne tyce dymniku: dict(d (prumer))
  stone            kamen: dict(len (min, max), joint)
  finish           uprava dreva: trimmers, hangers
  stage, stage_top sada etapy cele stavby a sada dymniku, komina, vymen a zavesnych tyci (napr. zaklad base, komin final)"""
import math, random
from zrlib.config import WOOD_FINISH
from zrlib.geom import crc
from zrlib.stones import Stone
from zr_stavby.pult import pult_geom


def _block(name, tag, P, yaw_a, z_lo, a, c, h, course, stone, rng, hole=None):
    """kvadr z kamenu v radach (cm): rady vysoke course, v kazde rade pasy kamenu stridave podel a / podel c (uzka zidka
    vzdy podel sebe), spary joint;
    hole = dict(a, w, z): v radach, ktere zasahuji do z0-z1, se vynecha otvor sirky w kolem a (pro vyfucnu)"""
    out = []; j = stone.get("joint", 0.015); lmin, lmax = stone.get("len", (0.35, 0.6))
    n_rows = max(1, int(round(h / course))); ch = h / n_rows
    for r in range(n_rows):
        z0 = r * ch; along_a = (r % 2 == 0)
        if min(a[1] - a[0], c[1] - c[0]) < 0.5: along_a = (a[1] - a[0]) >= (c[1] - c[0])    # uzka zidka: kameny vzdy podel ni
        (p0, p1), (q0, q1) = (a, c) if along_a else (c, a)          # p = smer delky kamenu, q = napric
        nq = max(1, int(round((q1 - q0) / 0.45))); qw = (q1 - q0) / nq
        for k in range(nq):
            cuts = []                                                # useky podel p (pripadne preruseni otvorem)
            if hole and along_a and hole["z"][0] < z0 + ch - 0.02 and hole["z"][1] > z0 + 0.02:
                cuts = [(p0, hole["a"] - hole["w"] / 2), (hole["a"] + hole["w"] / 2, p1)]
            else: cuts = [(p0, p1)]
            for ci, (s0, s1) in enumerate(cuts):
                x = s0; i = 0
                while x < s1 - 1e-6:
                    ln = rng.uniform(lmin, lmax)
                    if s1 - (x + ln) < lmin * 0.6: ln = s1 - x          # posledni kamen do konce (ne kratky zbytek)
                    pm = x + ln / 2; qm = q0 + qw * (k + 0.5)
                    aa, cc = (pm, qm) if along_a else (qm, pm)
                    px, py = P(aa, cc)
                    out.append(Stone("%s|%s|%d.%d.%d.%d" % (name, tag, r, k, ci, i), "face", px, py, z_lo + (z0 + ch / 2) * 100,
                                     yaw_a + (0.0 if along_a else 90.0), (ln - j) * 100, (qw - j) * 100, (ch - j) * 100))
                    x += ln; i += 1
    return out


def build_hearth(ad, terr, frames, cache=None):
    out = []; name = ad["name"]
    fr = next((f for f in frames if f["name"] == ad.get("roof")), None)
    G = pult_geom(fr, terr, cache) if fr else None
    O, U, V = ad["origin"], ad["u"], ad["v"]
    P = lambda a, c: (O[0] + (U[0] * a + V[0] * c) * 100, O[1] + (U[1] * a + V[1] * c) * 100)
    yaw_a = math.degrees(math.atan2(U[1], U[0])); yaw_c = math.degrees(math.atan2(V[1], V[0]))
    tb = ad["table"]; ta, tc = tb["a"], tb["c"]
    zg = terr.z(*P((ta[0] + ta[1]) / 2, (tc[0] + tc[1]) / 2))       # teren pod stolem
    z0 = G["z0"] if G else zg                                         # vysky dymniku a komina od terenu strechy
    rng = random.Random(crc(name)); st = ad.get("stone", {})
    fin = ad.get("finish", {}); WC = lambda part: WOOD_FINISH.get(fin.get(part, "raw"), "wood")
    # kamenny stul a bocni zidky
    out += _block(name, "T", P, yaw_a, zg, ta, tc, tb["h"], tb.get("course", 0.25), st, rng)
    for w in ad.get("walls", []):
        out += _block(name, w.get("id", "Z"), P, yaw_a, zg + w.get("base", 0.0) * 100, w["a"], w["c"], w["h"], w.get("course", 0.3), st, rng, w.get("hole"))
    top_ids = set()
    dm = ad.get("dome")
    if dm:                                                         # hlinena klenba pece na jejich zdech
        (a0, a1), (c0, c1), (zb, zt) = dm["a"], dm["c"], dm["z"]; x, y = P((a0 + a1) / 2, (c0 + c1) / 2)
        out.append(Stone("%s|K" % name, "daub", x, y, zg + (zb + zt) * 50, yaw_a, (a1 - a0) * 100, (c1 - c0) * 100, (zt - zb) * 100, shape="oven_dome"))
    for b in ad.get("boxes", []):
        (a0, a1), (c0, c1), (zb, zt) = b["a"], b["c"], b["z"]; x, y = P((a0 + a1) / 2, (c0 + c1) / 2)
        out.append(Stone("%s|%s" % (name, b["id"]), b.get("cat", "iron"), x, y, zg + (zb + zt) * 50, yaw_a, (a1 - a0) * 100, (c1 - c0) * 100, (zt - zb) * 100))
        if b.get("loose"): out[-1].loose = True
        if b.get("top"): top_ids.add(out[-1].id)
    for q in ad.get("props", []):
        x, y = P(q["a"], q["c"]); sx, sy, sz = q["size"]
        s_ = Stone("%s|%s" % (name, q["id"]), q.get("cat", "wood"), x, y, zg + q["zc"] * 100, yaw_a + q.get("yaw", 0.0), sx, sy, sz, shape=q["shape"])
        s_.loose = True; out.append(s_)
        if q.get("top"): top_ids.add(s_.id)
    fl = ad.get("flue")
    if fl:                                                         # sopouch: tah z pece primo do dymniku / komina
        x, y = P(fl["a"], fl["c"]); zb, zt = fl["z"]
        out.append(Stone("%s|S" % name, "daub", x, y, zg + (zb + zt) * 50, yaw_a, fl["w"] * 100, fl["w"] * 100, (zt - zb) * 100, shape="chimney"))
    # hlineny maz na stole kolem ohniste, v ohnisti drevene uhli
    dt = ad.get("daub", 0.04) * 100; pit = ad.get("pit"); top = zg + tb["h"] * 100
    def slab(tag, cat, a0, a1, c0, c1, zc, t):
        if a1 - a0 < 0.01 or c1 - c0 < 0.01: return
        x, y = P((a0 + a1) / 2, (c0 + c1) / 2)
        out.append(Stone("%s|%s" % (name, tag), cat, x, y, zc, yaw_a, (a1 - a0) * 100, (c1 - c0) * 100, t))
    if pit:
        h = pit["w"] / 2; pa0, pa1, pc0, pc1 = pit["a"] - h, pit["a"] + h, pit["c"] - h, pit["c"] + h
        slab("M0", "daub", ta[0], ta[1], tc[0], pc0, top + dt / 2, dt); slab("M1", "daub", ta[0], ta[1], pc1, tc[1], top + dt / 2, dt)
        slab("M2", "daub", ta[0], pa0, pc0, pc1, top + dt / 2, dt); slab("M3", "daub", pa1, ta[1], pc0, pc1, top + dt / 2, dt)
        ct = max(dt - pit.get("d", 0.02) * 100, 0.5)
        slab("U", "charcoal", pa0, pa1, pc0, pc1, top + ct / 2, ct)
    else: slab("M0", "daub", ta[0], ta[1], tc[0], tc[1], top + dt / 2, dt)
    # dymnik a komin (knihovni meshe z prouti a hliny, skaluji se na rozmer)
    hd = ad.get("hood"); ch = ad.get("chimney")
    if hd:
        x, y = P(hd["a"], hd["c"])
        out.append(Stone("%s|D" % name, "daub", x, y, z0 + (hd["bottom"] + hd["h"] / 2) * 100, yaw_a,
                         hd["size"][0] * 100, hd["size"][1] * 100, hd["h"] * 100, shape="smoke_hood"))
    if ch:
        zb = (hd["bottom"] + hd["h"]) if hd else tb["h"]
        x, y = P(ch["a"], ch["c"])
        out.append(Stone("%s|C" % name, "daub", x, y, z0 + (zb + ch["top"]) / 2 * 100, yaw_a,
                         ch["w"] * 100, ch["w"] * 100, (ch["top"] - zb) * 100, shape="chimney"))
    # vymeny mezi krokvemi po obou stranach komina (kratke kulatiny v urovni krokvi) a zavesne tyce dymniku
    tr = ad.get("trimmers")
    if tr and ch and G:
        cs = sorted(g["c"] for g in G["geo"])
        lo = max((c for c in cs if c < ch["c"]), default=None); hi = min((c for c in cs if c > ch["c"]), default=None)
        if lo is not None and hi is not None:
            d = tr["d"] * 100; hgr = ad.get("hangers")
            for k, sg in enumerate((-1, 1)):
                a = ch["a"] + sg * (ch["w"] / 2 + tr.get("gap", 0.03) + tr["d"] / 2)
                zc = G["under"](a) + G["vert"] / 2                    # osa krokve v miste vymeny
                x, y = P(a, (lo + hi) / 2)
                out.append(Stone("%s|X%d" % (name, k), WC("trimmers"), x, y, zc, yaw_c, (hi - lo) * 100 - G["rw"] + 4, d, d,
                                 shape="round", bark=False))
                if hgr and hd:                                       # z koncu vymeny k rohum spodniho okraje dymniku
                    for m, cg in enumerate((-1, 1)):
                        top_pt = (a, (lo + hi) / 2 + cg * ((hi - lo) / 2 - G["rw"] / 200 - 0.08), zc - d / 2)
                        bot_pt = (hd["a"] + sg * (hd["size"][0] / 2 - 0.03), hd["c"] + cg * (hd["size"][1] / 2 - 0.03),
                                  z0 + (hd["bottom"] + 0.06) * 100)
                        (x1, y1), (x0, y0) = P(top_pt[0], top_pt[1]), P(bot_pt[0], bot_pt[1])
                        hl = math.hypot(x1 - x0, y1 - y0); dz = top_pt[2] - bot_pt[2]; hd_ = hgr["d"] * 100
                        out.append(Stone("%s|H%d%d" % (name, k, m), WC("hangers"), (x0 + x1) / 2, (y0 + y1) / 2, (top_pt[2] + bot_pt[2]) / 2,
                                         math.degrees(math.atan2(y1 - y0, x1 - x0)), math.hypot(hl, dz), hd_, hd_,
                                         pitch=math.degrees(math.atan2(dz, hl)), shape="round", bark=False))
    top_stage = ad.get("stage_top")                                 # dymnik, komin a jejich zaveseni v jine sade etapy nez kamenny zaklad
    if top_stage:
        for s in out:
            if s.shape in ("smoke_hood", "chimney") or s.id.split("|")[-1][0] in "XH" or s.id in top_ids: s.stage = top_stage
    return out
