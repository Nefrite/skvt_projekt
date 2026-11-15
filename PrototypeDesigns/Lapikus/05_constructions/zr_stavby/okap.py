"""okap (typ gutter): vydlabany zlab pod okapovou hranou strechy na rozsochach (kul v zemi + hlava rozsochy), se spadem
k jednomu konci; pod nim sud na destovou vodu (samostatny actor, da se doladit rucne). Svod se nedela.

Data (constructions.json -> addons, generuje tools/constructions/gen_constructions.py z tools/ruin/palac_spec.py):
  origin, u, v     ram stavby (UE cm, jednotkove vektory), rozmery v m: a = podel u, c = podel v
  roof             jmeno strechy (typ pult_roof): vyska zlabu od spodku prken na jeji okapove hrane
  a, c (c0, c1)    osa zlabu (pod okapem) a rozsah; voda tece od c0 k c1
  d, bark          prumer zlabu, s kurou / loupany
  drop             vrch zlabu na zacatku (c0) pod spodkem prken na okapove hrane (m)
  fall             spad k c1 (m/m)
  forks            rozsochy pod zlabem: polohy c; post_d = prumer kulu, sink = kul v zemi (m)
  barrel           sud pod koncem zlabu: dict(a, c) nebo nic
  finish           uprava dreva: gutter, forks, barrel"""
import math, random
from zrlib.config import LIB_MESHES, ROUND_MESHES, WOOD_FINISH
from zrlib.geom import crc
from zrlib.stones import Stone, round_mesh_name
from zr_stavby.pult import pult_geom, roof_layers

# hlava rozsochy SM_RuinForkHead (45 x 30 x 12 cm, kmen na -X, vidlice na +X): kde v ni lezi zlab O 20 cm
# = vyska osy zlabu nad stredem hlavy podel X (cm), zmereno na OBJ (kruh R 10 v rovine ramen, zadny vrchol uvnitr)
FORK_SEAT = {"A": 28.0, "B": 26.0}
FORK_OVERLAP = 8.0               # kul konci 8 cm uvnitr kmene hlavy rozsochy


def gutter_line(ad, terr, frames, cache=None):
    """-> (P, z_top(c) cm = vrch zlabu, sz (vyska meshe zlabu cm)); vrch zlabu od spodku prken na okapove hrane strechy"""
    O, U, V = ad["origin"], ad["u"], ad["v"]
    P = lambda a, c: (O[0] + (U[0] * a + V[0] * c) * 100, O[1] + (U[1] * a + V[1] * c) * 100)
    fr = next(f for f in frames if f["name"] == ad["roof"])
    G = pult_geom(fr, terr, cache); L = roof_layers(fr, G)
    a_e = G["a_lo"] + G["sg"] * fr["roof"].get("eave_over", 0.10)      # okapova hrana krytiny
    z0 = L["lath"](a_e) - ad.get("drop", 0.12) * 100                    # spodek prken na okapove hrane - drop
    c0 = ad["c"][0]; fall = ad.get("fall", 0.015)
    nom = 11.0 / 20.0                                                   # vyska / sirka meshe zlabu (SM_RuinGutter 100 x 20 x 11)
    return P, (lambda c: z0 - fall * (c - c0) * 100), nom * ad["d"] * 100


def build_gutter(ad, terr, frames, cache=None):
    out = []; name = ad["name"]; U, V = ad["u"], ad["v"]
    fin = ad.get("finish", {}); WC = lambda part: WOOD_FINISH.get(fin.get(part, "raw"), "wood")
    P, ztop, sz = gutter_line(ad, terr, frames, cache)
    a = ad["a"]; c0, c1 = ad["c"]; d = ad["d"] * 100; fall = ad.get("fall", 0.015)
    yaw_c = math.degrees(math.atan2(V[1], V[0])); ang = math.atan(fall)
    # zlab: osa X podel +c, spad k c1 -> pitch zaporny
    cm = (c0 + c1) / 2; x, y = P(a, cm)
    out.append(Stone("%s|G" % name, WC("gutter"), x, y, ztop(cm) - sz / 2, yaw_c, (c1 - c0) * 100 / math.cos(ang), d, sz,
                     pitch=-math.degrees(ang), shape="gutter", bark=bool(ad.get("bark"))))
    # rozsochy: hlava (osa X nahoru, ramena napric zlabem = podel u) na kulu v zemi
    yaw_f = math.degrees(math.atan2(-U[0], U[1]))                       # lokalni Y hlavy = u
    fl, fw, fh = ROUND_MESHES["SM_RuinForkHead"][0]                    # hlava rozsochy v jmenovitem rozmeru (45 x 30 x 12)
    for k, c in enumerate(ad.get("forks", [])):
        x, y = P(a, c); zg = terr.z(x, y)
        axis = ztop(c) - sz + d / 2                                     # osa zlabu (spodek zlabu + polomer)
        f = Stone("%s|F%d" % (name, k), WC("forks"), x, y, 0.0, yaw_f, fl, fw, fh, pitch=90.0, shape="fork", bark=True)
        f.z = axis - FORK_SEAT[round_mesh_name(f)[-1]]
        out.append(f)
        z0 = zg - ad.get("sink", 0.4) * 100; z1 = f.z - fl / 2 + FORK_OVERLAP; pd = ad.get("post_d", 0.12) * 100
        out.append(Stone("%s|P%d" % (name, k), WC("forks"), x, y, (z0 + z1) / 2, yaw_f, z1 - z0, pd, pd, pitch=90.0, shape="round", bark=True))
    br = ad.get("barrel")
    if br:                                                             # sud na destovou vodu (samostatny actor)
        x, y = P(br["a"], br["c"]); zg = terr.z(x, y); bx, by, bz = LIB_MESHES["SM_RuinBarrel"][0]
        b = Stone("%s|S" % name, WC("barrel"), x, y, zg + bz / 2, random.Random(crc(name)).uniform(0, 360), bx, by, bz, shape="barrel")
        b.loose = True; out.append(b)
    return out
