"""kryt z kulatiny (typ palisade): kuly s kurou nastojato tesne vedle sebe, nahore zaspicatele (SM_RuinStake, spicka nahoru),
zevnitr privazana vodorovna rahna; pruzory = kratsi a tensi kul (mezera nahore mezi sousednimi kuly).
Kuly stoji na korune zdi: pata kazdeho kulu = vrch nejvyssiho kamene zriceniny pod nim (kopiruje skutecnou korunu).
Kde je koruna tak vysoko, ze by kul byl kratsi nez min_len, kul se vynecha (kryje zed sama). Vysky absolutne (UE cm).

Data (constructions.json -> addons, generuje tools/constructions/gen_constructions.py z tools/ruin/brana_spec.py):
  origin, u, v   ram stavby (UE cm, jednotkove vektory), rozmery v m: a = podel u, c = podel v
  lines          [dict(id, p0 (a, c), p1 (a, c), top (vrch kulu, UE cm), d (min, max prumer m), gap (mezera mezi kuly m),
                 jit (nahodne +- vrchu m), sink (zapusteni paty do koruny m), min_len, on [jmena zdi, na kterych stoji],
                 floor (UE cm: pata kulu, kde pod nim neni kamen nebo je niz - napr. vrch podlahy podesty; None = kul bez kamene
                 se vynecha), sink = zapusteni paty do koruny (m): kuly "utopene" ve vydlabane korune zdi lepe drzi,
                 slits [dict(at (m od p0), w (m), bottom (UE cm), flat = True: kul v pruzoru je rovne seriznuty (bez spicky))], rails dict(d, z [UE cm ...], side (+1 / -1 = strana
                 vlevo / vpravo ve smeru p0 -> p1), span (od, do v m od p0)), stage)]
  finish         uprava dreva: stakes, rails"""
import math, random
from zrlib.config import WOOD_FINISH
from zrlib.geom import crc
from zrlib.stones import Stone
from zr_stavby.zdivo import frame_box


def build_palisade(ad, walls, terr=None):
    out = []; name = ad["name"]
    O, U, V = ad["origin"], ad["u"], ad["v"]
    P = lambda a, c: (O[0] + (U[0] * a + V[0] * c) * 100, O[1] + (U[1] * a + V[1] * c) * 100)
    fin = ad.get("finish", {}); WC = lambda part: WOOD_FINISH.get(fin.get(part, "raw"), "wood")
    for ln in ad["lines"]:
        (a0, c0), (a1, c1) = ln["p0"], ln["p1"]; L = math.hypot(a1 - a0, c1 - c0); da, dc = (a1 - a0) / L, (c1 - c0) / L
        rng = random.Random(crc("%s|%s" % (name, ln["id"]))); dmin, dmax = ln.get("d", (0.18, 0.22)); gap = ln.get("gap", 0.01)
        names = ln.get("on") or list(walls)
        ruin = [(frame_box(s, O, U, V), s.z + s.sz / 2) for n in names for s in walls[n]["stones"] + walls[n].get("loose", [])]
        near = [(b, t) for (b, t) in ruin if b[1] > min(a0, a1) - 0.5 and b[0] < max(a0, a1) + 0.5 and b[3] > min(c0, c1) - 0.5 and b[2] < max(c0, c1) + 0.5]
        slits = sorted(ln.get("slits", []), key=lambda s: s["at"])
        # rozmisteni: kuly nahodneho prumeru od p0 k p1, pruzory na svych mistech (tensi kratky kul)
        items = []; x = 0.0; si = 0
        while x < L - 0.05:
            if si < len(slits) and x + dmax / 2 >= slits[si]["at"] - slits[si]["w"] / 2:
                s = slits[si]; si += 1
                items.append((x + s["w"] / 2, s["w"] - 0.01, s["bottom"], bool(s.get("flat")))); x += s["w"]; continue
            d = rng.uniform(dmin, dmax)
            if L - (x + d) < dmin * 0.5: d = L - x
            items.append((x + d / 2, d, None, False)); x += d + gap
        yaw = math.degrees(math.atan2(U[1] * da + V[1] * dc, U[0] * da + V[0] * dc))
        for i, (m, d, slit_top, flat) in enumerate(items):
            a, c = a0 + da * m, c0 + dc * m; r = d / 2
            tops = [t for (b, t) in near if b[0] - r * 0.6 <= a <= b[1] + r * 0.6 and b[2] - r * 0.6 <= c <= b[3] + r * 0.6]
            if ln.get("floor") is not None: tops.append(ln["floor"])
            if not tops: continue
            foot = max(tops)
            zt = slit_top if slit_top is not None else ln["top"] + rng.uniform(-1, 1) * ln.get("jit", 0.04) * 100
            zb = foot - (ln.get("sink", 0.03) if foot != ln.get("floor") else 0.0) * 100     # na podlaze kul stoji, do kamene je zapusteny
            if zt - zb < ln.get("min_len", 0.5) * 100: continue
            px, py = P(a, c)
            st = Stone("%s|%s|K%d" % (name, ln["id"], i), WC("stakes"), px, py, (zb + zt) / 2, yaw, zt - zb, d * 100, d * 100, pitch=90.0,
                       shape="round" if flat else "stake", bark=True)
            st.stage = ln.get("stage"); out.append(st)
        rl = ln.get("rails")
        if rl:                                                        # rahna privazana z jedne strany kulu
            side = rl.get("side", 1.0) * (dmax / 2 + rl["d"] / 2); m0, m1 = rl.get("span", (-0.15, L + 0.15))    # rozsah podel linie (m od p0)
            na, nc = -dc * side, da * side
            for k, z in enumerate(rl["z"]):
                (x0, y0), (x1, y1) = P(a0 + da * m0 + na, c0 + dc * m0 + nc), P(a0 + da * m1 + na, c0 + dc * m1 + nc)
                st = Stone("%s|%s|R%d" % (name, ln["id"], k), WC("rails"), (x0 + x1) / 2, (y0 + y1) / 2, z, yaw, (m1 - m0) * 100, rl["d"] * 100, rl["d"] * 100,
                           shape="round", bark=True)
                st.stage = ln.get("stage"); out.append(st)
    return out
