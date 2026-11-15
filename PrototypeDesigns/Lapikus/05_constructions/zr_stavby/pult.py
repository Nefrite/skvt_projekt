"""pultova strecha na sloupech (typ pult_roof): sloupy na patnich kamenech, pozednice / vaznice, krokve, krytina, lemovani.
Krytina ma stejnou skladbu jako krov u ostrohu (late napric krokvemi, prkna po spadu, listy pres spary), ale vlastni kod:
krokve jsou rovnobezne, takze late jdou pres celou sirku strechy a prkna nejsou rozdelena do poli mezi tramy (krov._fan_roof_cover
pocita klinova pole mezi paprskovitymi tramy). Prostup komina: prkna se kladou od jeho okraju ven, nad a pod otvorem lat.

Data (constructions.json -> frames, generuje tools/constructions/gen_constructions.py z tools/ruin/palac_spec.py):
  origin (UE cm), u, v (jednotkove vektory ramu stavby), rozmery v m v tomto ramu
  axis      osa ramu, po ktere strecha pada: "u" nebo "v" (pozednice jsou na ni kolme)
  ref       bod (u, v), od jehoz terenu se pocitaji vysky
  supports  podpory krokvi: [dict(id, at (m na ose spadu), span (c0, c1 = rozsah napric), top (vrch, m nad terenem),
            sec (sirka, vyska m), posts [c ...] (polohy sloupu), post (strana sloupu m))]; sklon urcuje nejvyssi a nejnizsi
  rafters   krokve: dict(d (prumer kulatiny m) nebo sec (sirka, vyska m), bark, pos [c ...], a0, a1 (od - do na ose spadu),
            seat (osedlani = zapusteni do pozednic m))
  pads      patni kameny pod sloupy (samostatne actory): dict(l, w, h, sink) nebo nic (sloup 10 cm v zemi)
  plan      pudorys strechy: dict(a (a0, a1), c (c0, c1)) v ramu (a = osa u, c = osa v)
  openings  prostupy krytinou: [dict(kind="chimney", a, c (stred), w (strana))]
  roof      krytina (bez ni jen kostra): dict(lath (vyska, sirka m), board_t, board_w (min, max), gap (spara), batten (sirka,
            tloustka listy pres sparu), lath_step (nejvetsi rozestup lati m), eave_over (presah prken za konec krokvi),
            top_gap / side_gap (mezera prken od zdi u horniho / bocniho okraje), hole_gap (mezera od komina))
  flashing  lemovani: [dict(edge = "top" (horni okraj, u veze; gap od zdi) nebo "c0" / "c1" (bocni okraj, na hrane krajniho
            prkna), t, h (vyska nad krytinou))]
  finish    uprava dreva: posts, plates, rafters, roof_laths, roof_boards, roof_battens, roof_flashing"""
import math, random
from zrlib.config import WOOD_FINISH
from zrlib.geom import crc
from zrlib.stones import Stone


def pult_geom(fr, terr, cache=None):
    """spolecna geometrie: prevod ramu, vyska terenu, sklon, spodek a vrch krokvi (i pro krytinu a dalsi stavby pod strechou)"""
    if cache is not None and fr["name"] in cache: return cache[fr["name"]]
    O, U, V = fr["origin"], fr["u"], fr["v"]
    A, C = (U, V) if fr.get("axis", "u") == "u" else (V, U)          # A = po spadu, C = podel pozednic
    P = lambda a, c: (O[0] + (A[0] * a + C[0] * c) * 100, O[1] + (A[1] * a + C[1] * c) * 100)
    sup = sorted(fr["supports"], key=lambda s: -s["top"]); hi, lo = sup[0], sup[-1]
    ref = fr.get("ref") or [(hi["at"] + lo["at"]) / 2, sum(hi["span"]) / 2]
    z0 = terr.z(*P(*ref))
    run = abs(lo["at"] - hi["at"]); sg = 1.0 if lo["at"] > hi["at"] else -1.0   # smer spadu na ose A
    slope = (hi["top"] - lo["top"]) / run; ang = math.atan(slope)
    rf = fr["rafters"]; seat = rf.get("seat", 0.0)
    rw, rh = (rf["d"], rf["d"]) if "d" in rf else rf["sec"]
    vert = rh / math.cos(ang)                                        # svisla vyska krokve
    under = lambda a: z0 + (hi["top"] - seat - slope * (a - hi["at"]) * sg) * 100      # spodek krokve (cm) v miste a (m)
    a_hi, a_lo = (rf["a0"], rf["a1"]) if (rf["a1"] - rf["a0"]) * sg > 0 else (rf["a1"], rf["a0"])
    D = (A[0] * sg, A[1] * sg); Lh = abs(a_lo - a_hi) * 100           # smer dolu, vodorovna delka (cm)
    geo = []                                                         # krokve ve tvaru tramu krovu (krov.ostroh_geom -> geo)
    for i, c in enumerate(rf["pos"]):
        geo.append(dict(id="B%d" % i, c=c, S=P(a_hi, c), D=D, sl=slope, at=0.0, a1=Lh,
                        bottom=lambda a: under(a_hi + sg * a / 100), top=lambda a: under(a_hi + sg * a / 100) + vert * 100))
    G = dict(P=P, A=A, C=C, z0=z0, slope=slope, ang=ang, sg=sg, under=under, vert=vert * 100, rw=rw * 100, rh=rh * 100,
             a_hi=a_hi, a_lo=a_lo, hi=hi, lo=lo, geo=geo, bw=rw * 100, bh=rh * 100)
    if cache is not None: cache[fr["name"]] = G
    return G


def build_pult_roof(fr, P_, walls, terr, cache=None, cover=True):
    """sloupy (na patnich kamenech), pozednice a krokve pultove strechy; cover = i krytina a lemovani (fr["roof"])"""
    out = []; name = fr["name"]
    fin = fr.get("finish", {}); WC = lambda part: WOOD_FINISH.get(fin.get(part, "raw"), "wood")
    G = pult_geom(fr, terr, cache); P = G["P"]; A, C = G["A"], G["C"]; z0 = G["z0"]
    yaw_a = math.degrees(math.atan2(A[1], A[0])); yaw_c = math.degrees(math.atan2(C[1], C[0]))
    pad = fr.get("pads")
    for k, s in enumerate(fr["supports"]):
        sid = s.get("id", "V%d" % k); w, h = s["sec"][0] * 100, s["sec"][1] * 100
        c0, c1 = s["span"]; x, y = P(s["at"], (c0 + c1) / 2); top = z0 + s["top"] * 100
        out.append(Stone("%s|%s" % (name, sid), WC("plates"), x, y, top - h / 2, yaw_c, (c1 - c0) * 100, w, h))
        ps = s.get("post", 0.2) * 100
        for j, c in enumerate(s.get("posts", [])):
            px, py = P(s["at"], c); zg = terr.z(px, py)
            if pad:                                   # plochy kamen z rozvalin pod sloupem (samostatny actor, da se doladit rucne)
                ph = pad["h"] * 100; zb = zg - pad.get("sink", 0.0) * 100 + ph
                st = Stone("%s|%s|K%d" % (name, sid, j), "face", px, py, zb - ph / 2, yaw_a, pad["l"] * 100, pad["w"] * 100, ph)
                st.loose = True; out.append(st)
            else: zb = zg - 10
            out.append(Stone("%s|%s|P%d" % (name, sid, j), WC("posts"), px, py, (zb + top - h) / 2, yaw_a, ps, ps, top - h - zb))
    rf = fr["rafters"]; ang = G["ang"]; rnd = "d" in rf
    for g in G["geo"]:
        a1 = g["a1"]; mx, my = g["S"][0] + g["D"][0] * a1 / 2, g["S"][1] + g["D"][1] * a1 / 2
        zc = (g["bottom"](0) + g["bottom"](a1)) / 2 + G["vert"] / 2
        yaw = math.degrees(math.atan2(-g["D"][1], -g["D"][0]))        # osa X dilce od okapu (nize) nahoru -> pitch kladny
        out.append(Stone("%s|%s" % (name, g["id"]), WC("rafters"), mx, my, zc, yaw, a1 / math.cos(ang), G["rw"], G["rh"],
                         pitch=math.degrees(ang), shape="round" if rnd else None, bark=bool(rf.get("bark"))))
    if cover and fr.get("roof"): out += _pult_cover(fr, G, WC)
    return out


def roof_holes(fr):
    """prostupy krytinou vcetne mezery: [(a0, a1, c0, c1)] v m"""
    g = fr.get("roof", {}).get("hole_gap", 0.03); out = []
    for o in fr.get("openings", []):
        h = o["w"] / 2 + g
        out.append((o["a"] - h, o["a"] + h, o["c"] - h, o["c"] + h))
    return out


def roof_layers(fr, G):
    """vysky vrstev krytiny (cm, absolutni Z) v miste a (m): rafter = vrch krokve, lath = vrch lati (spodek prken),
    board = vrch prken; svisle = tloustka / cos(sklon)"""
    rf = fr["roof"]; k = 100.0 / math.cos(G["ang"])
    lh = rf.get("lath", (0.05, 0.06))[0]; bt = rf.get("board_t", 0.035)
    top = lambda a: G["under"](a) + G["vert"]
    return dict(rafter=top, lath=lambda a: top(a) + lh * k, board=lambda a: top(a) + (lh + bt) * k)


def _pult_cover(fr, G, WC):
    """krytina pultove strechy: late napric krokvemi (pres celou sirku), prkna po spadu od horniho okraje po okap s presahem,
    listy pres spary, prostup komina (prkna od jeho okraju ven, lat nad a pod nim), lemovani prknem na stojato"""
    out = []; name = fr["name"]; rf = fr["roof"]; P = G["P"]; A, C, sg = G["A"], G["C"], G["sg"]; ang = G["ang"]
    lh, lw = rf.get("lath", (0.05, 0.06)); bt = rf.get("board_t", 0.035); bwmin, bwmax = rf.get("board_w", (0.22, 0.30))
    gap = rf.get("gap", 0.015); btw, bth = rf.get("batten", (0.10, 0.035)); k = 1.0 / math.cos(ang)
    plan = fr.get("plan") or dict(a=sorted((G["a_hi"], G["a_lo"])), c=[min(G["hi"]["span"][0], G["lo"]["span"][0]), max(G["hi"]["span"][1], G["lo"]["span"][1])])
    L = roof_layers(fr, G); rng = random.Random(crc("%s|roof" % name))
    hi_end = max(plan["a"]) if sg < 0 else min(plan["a"])                  # horni okraj krytiny (u zdi / veze)
    a_top = hi_end + sg * rf.get("top_gap", 0.005)                        # konec prken nahore (sg = smer dolu na ose a)
    a_eave = G["a_lo"] + sg * rf.get("eave_over", 0.10)                   # konec prken na okapu (za koncem krokvi)
    c0, c1 = plan["c"][0] + rf.get("side_gap", 0.005), plan["c"][1]
    holes = roof_holes(fr)
    yaw_up = math.degrees(math.atan2(-A[1] * sg, -A[0] * sg))            # osa X prken nahoru po spadu -> pitch kladny
    yaw_c = math.degrees(math.atan2(C[1], C[0]))
    ysg = 1.0 if (-C[1] * -A[0] * sg + C[0] * -A[1] * sg) > 0 else -1.0  # lokalni Y dilce podel c miri nahoru (+1) / dolu
    pitch = math.degrees(ang)
    def piece(sid, cat, a0, a1, cc, w, t, zfun, lift):
        """dilec po spadu od a0 do a1 (m), stred napric cc, sirka w, tloustka t; spodek v zfun(a), lift = cm nad nim"""
        am = (a0 + a1) / 2; x, y = P(am, cc); ln = abs(a1 - a0) * 100 * k
        out.append(Stone("%s|R|%s" % (name, sid), cat, x, y, zfun(am) + lift + t * 50 * k, yaw_up, ln, w * 100, t * 100, pitch=pitch))
    def split(a0, a1, cc0, cc1):
        """useky po spadu (a0..a1) pasu cc0..cc1 bez prostupu"""
        segs = [(min(a0, a1), max(a0, a1))]
        for ha0, ha1, hc0, hc1 in holes:
            if cc1 <= hc0 + 1e-4 or cc0 >= hc1 - 1e-4: continue
            segs = [q for (s0, s1) in segs for q in ((s0, min(s1, ha0)), (max(s0, ha1), s1)) if q[1] - q[0] > 0.08]
        return segs
    # pasy prken: zony mezi okraji strechy a okraji prostupu, v kazde prkna nahodne sirky (posledni dorovnane)
    edges = sorted({c0, c1} | {q for h in holes for q in (h[2], h[3]) if c0 < q < c1})
    boards = []
    for z0_, z1_ in zip(edges[:-1], edges[1:]):
        W = z1_ - z0_; n = max(1, int(round(W / ((bwmin + bwmax) / 2 + gap))))
        ws = [rng.uniform(bwmin, bwmax) for _ in range(n)]; f = (W - gap * (n - 1)) / sum(ws); x = z0_
        for w in ws:
            boards.append((x, x + w * f)); x += w * f + gap
    for i, (b0, b1) in enumerate(boards):
        for j, (s0, s1) in enumerate(split(a_eave, a_top, b0, b1)):
            piece("K%d.%d" % (i, j), WC("roof_boards"), s0, s1, (b0 + b1) / 2, b1 - b0 - 0.004, bt, L["lath"], 0.0)
    # listy pres spary (konci pod lemovanim nahore)
    fl_top = next((f for f in fr.get("flashing", []) if f.get("edge") == "top"), None)
    a_bt = a_top + sg * ((fl_top["t"] + fl_top.get("gap", 0.005) + 0.01) if fl_top else 0.0)
    for i in range(len(boards) - 1):
        cm = (boards[i][1] + boards[i + 1][0]) / 2
        for j, (s0, s1) in enumerate(split(a_eave, a_bt, cm - btw / 2, cm + btw / 2)):
            piece("L%d.%d" % (i, j), WC("roof_battens"), s0, s1, cm, btw, bth, L["board"], 0.0)
    # late napric krokvemi: u horniho konce krokvi, u okapu, u prostupu (nad a pod otvorem), mezi nimi po nejvys lath_step
    a_hi, a_lo = G["a_hi"], G["a_lo"]; m = lw / 2 + 0.01
    rows = [a_hi + sg * m, a_lo - sg * m]
    for ha0, ha1, hc0, hc1 in holes:
        rows += [ha0 - lw / 2, ha1 + lw / 2]
    rows = sorted(r for r in rows if min(a_hi, a_lo) <= r <= max(a_hi, a_lo))
    full = []
    for r0, r1 in zip(rows[:-1], rows[1:]):
        if any(r0 < (h[0] + h[1]) / 2 < r1 for h in holes): full.append(r0); continue     # nad otvorem nic
        n = int(math.ceil((r1 - r0) / rf.get("lath_step", 0.9) - 1e-6))
        full += [r0 + (r1 - r0) * q / n for q in range(n)]
    full.append(rows[-1])
    for r_, a in enumerate(full):
        x, y = P(a, (c0 + c1) / 2)
        out.append(Stone("%s|R|T%d" % (name, r_), WC("roof_laths"), x, y, L["rafter"](a) + lh * 50 * k, yaw_c,
                         (c1 - c0 - 0.01) * 100, lw * 100, lh * 100, roll=ysg * pitch))
    # lemovani: prkno na stojato na krytine u zdi (horni okraj u veze, bocni okraj podel zdi)
    for f in fr.get("flashing", []):
        t, h, g = f["t"], f["h"], f.get("gap", 0.005)
        if f["edge"] == "top":
            a = hi_end + sg * (g + t / 2); x, y = P(a, (c0 + c1) / 2)
            zb = L["board"](a - sg * t / 2)                                 # spodek na krytine (vyssi hrana)
            out.append(Stone("%s|R|F%s" % (name, f["edge"]), WC("roof_flashing"), x, y, zb + h * 50, yaw_c,
                             (c1 - c0) * 100, t * 100, h * 100))
        else:
            cc = c0 + t / 2 if f["edge"] == "c0" else c1 - t / 2          # na krajnim prknu u jeho hrany (mezera od zdi = side_gap)
            a1 = a_top + sg * ((fl_top["t"] + fl_top.get("gap", 0.005)) if fl_top else 0.0)
            am = (a_eave + a1) / 2; x, y = P(am, cc)
            out.append(Stone("%s|R|F%s" % (name, f["edge"]), WC("roof_flashing"), x, y, L["board"](am) + h * 50 * k, yaw_up,
                             abs(a1 - a_eave) * 100 * k, t * 100, h * 100, pitch=pitch))
    return out
