"""
build_ruin_blocks.py - zricenina z jednotlivych kamennych bloku (Unreal Editor 5.8)

Zed = vodorovne rady kamene. Kazda rada ma dva lice z lomovych kvadru (ruzne delky, prevazba)
a mezi nimi jadro z lomu a malty. Model rozpadu (stejny jako build_ruin.py) urci dochovanou vysku;
bloky nad ni zmizi, u paty se rozebira lic (odkryje se jadro), otvory se vyriznou, intaktni osteni
a oblouky se postavi z opracovanych kvadru.

Uprava zriceniny:
  - v levelu objemy (TriggerBox s tagem) -> pregenerovat:
        Ruin_Cut, Ruin_Opening:<okno|dvere|portal|brana|strilna|prulom> (+Ruin_Intact, Ruin_Protect),
        Ruin_Keep, Ruin_Explode (bloky jako samostatne actory k rucnimu posunu / mazani)
  - v datech (ruin_layout.json -> "edits"): cut / cut_box / set_height / restore  -> pregenerovat
  - rucne: v levelu smazat jednotlive bloky (instance), pak spustit capture_manual_edits()
           -> smazane bloky se zapisi do manual_edits.json a pri pregenerovani zustanou smazane

Pouziti v UE: Tools -> Execute Python Script -> build_ruin_blocks.py
  (ruin_layout.json a manual_edits.json vedle skriptu, nebo nastav LAYOUT_PATH)
Mimo UE: python build_ruin_blocks.py [ruin_layout.json]  -> statistika (pocet bloku)
"""
import json, math, os, random, sys, zlib

# ------------------------------------------------------------------ nastaveni
LAYOUT_PATH = None                       # None = ruin_layout.json vedle skriptu
AGE = None                               # None = podle JSON ("1650"); nebo "1540" / "1650"
OVERRIDE = {}                            # prepis parametru, napr. {"ROBBING": 6}
RUIN_TAG = "Zricenina_Ruin"
CUBE_MESH = "/Engine/BasicShapes/Cube.Cube"
# --- materialy: None = skript si sam vytvori M_RuinStone + MI_RuinFace/Core/Frame v MAT_DIR (textury ze StarterContent);
#     nebo cesta k vlastnimu materialu, napr. "/Game/Megascans/.../MI_Rock.MI_Rock"
MAT_FACE  = None                         # lic (lomove kameny)
MAT_CORE  = None                         # jadro (lom + malta)
MAT_FRAME = None                         # osteni, oblouky (opracovany kamen)
MAT_CROWN = None                         # koruna zdi: odkryte horni kameny (vic zvetrale, svetlejsi, s nadechem lisejniku)
CROWN_WEATHER = True                     # odkryte kameny koruny = zvetrale tvary (SM_RuinStone_W_*) + material MI_RuinCrown
MAT_DIR   = "/Game/Skvt/Lapikus/Ruin/Materials"
TEXTURES = {   # kandidati (BaseColor, Normal) - pouzije se prvni existujici
    "wood_tar": [("/Game/StarterContent/Textures/T_Wood_Pine_D", "/Game/StarterContent/Textures/T_Wood_Pine_N"),
                 ("/Game/StarterContent/Textures/T_Wood_Oak_D", "/Game/StarterContent/Textures/T_Wood_Oak_N")],
    "wood_oil": [("/Game/StarterContent/Textures/T_Wood_Oak_D", "/Game/StarterContent/Textures/T_Wood_Oak_N"),
                 ("/Game/StarterContent/Textures/T_Wood_Pine_D", "/Game/StarterContent/Textures/T_Wood_Pine_N")],
    "wood_blood": [("/Game/StarterContent/Textures/T_Wood_Oak_D", "/Game/StarterContent/Textures/T_Wood_Oak_N"),
                   ("/Game/StarterContent/Textures/T_Wood_Pine_D", "/Game/StarterContent/Textures/T_Wood_Pine_N")],
    "wood_old": [("/Game/StarterContent/Textures/T_Wood_Pine_D", "/Game/StarterContent/Textures/T_Wood_Pine_N"),
                 ("/Game/StarterContent/Textures/T_Wood_Oak_D", "/Game/StarterContent/Textures/T_Wood_Oak_N")],
    "wood":  [("/Game/StarterContent/Textures/T_Wood_Pine_D", "/Game/StarterContent/Textures/T_Wood_Pine_N"),
              ("/Game/StarterContent/Textures/T_Wood_Oak_D", "/Game/StarterContent/Textures/T_Wood_Oak_N"),
              ("/Game/StarterContent/Textures/T_Wood_Walnut_D", "/Game/StarterContent/Textures/T_Wood_Walnut_N")],
    "face":  [("/Game/StarterContent/Textures/T_Rock_Slate_D", "/Game/StarterContent/Textures/T_Rock_Slate_N"),
              ("/Game/StarterContent/Textures/T_Rock_Basalt_D", "/Game/StarterContent/Textures/T_Rock_Basalt_N")],
    "core":  [("/Game/StarterContent/Textures/T_Rock_Slate_D", "/Game/StarterContent/Textures/T_Rock_Slate_N"),
              ("/Game/StarterContent/Textures/T_Rock_Basalt_D", "/Game/StarterContent/Textures/T_Rock_Basalt_N")],
    "crown": [("/Game/StarterContent/Textures/T_Rock_Slate_D", "/Game/StarterContent/Textures/T_Rock_Slate_N"),
              ("/Game/StarterContent/Textures/T_Rock_Basalt_D", "/Game/StarterContent/Textures/T_Rock_Basalt_N")],
    "frame": [("/Game/StarterContent/Textures/T_Rock_Slate_D", "/Game/StarterContent/Textures/T_Rock_Slate_N"),     # stejny kamen jako lic,
              ("/Game/StarterContent/Textures/T_Rock_Sandstone_D", "/Game/StarterContent/Textures/T_Rock_Sandstone_N")],  # jen opracovany
}
# vzhled instanci materialu (lze pak menit primo v MI_* v editoru): tint A..B (nahodne na kamen), meritko textury, drsnost
MAT_LOOK = {
    "face":  dict(TintA=(0.62, 0.58, 0.52), TintB=(0.95, 0.90, 0.80), Tiling=0.9, Roughness=0.9),
    "core":  dict(TintA=(0.60, 0.58, 0.54), TintB=(0.82, 0.79, 0.73), Tiling=1.2, Roughness=0.97),   # kamen s maltou, sedejsi
    "frame": dict(TintA=(0.70, 0.67, 0.60), TintB=(0.86, 0.82, 0.74), Tiling=0.8, Roughness=0.9),    # o kousek svetlejsi nez lic, ne oranzovy
    "crown": dict(TintA=(0.64, 0.62, 0.55), TintB=(0.96, 0.93, 0.84), Tiling=1.0, Roughness=0.95),
    # zasle nelakovane drevo: sedohneda, matna; kazdy tram / prkno jinak (Per Instance Random)
    "wood":  dict(TintA=(0.40, 0.37, 0.33), TintB=(0.62, 0.58, 0.52), Tiling=1.0, Roughness=0.97),
    # dehtovane (venkovni a masivni drevo): tmave hnedocerne, matne (zvetraly dehet, ne cerstvy lesk)
    # (hodnoty jsou linearni: 0.05 ~ sRGB 0.25 -> po vynasobeni texturou skoro hnedocerne jako stare dehtovane tramy)
    "wood_tar": dict(TintA=(0.045, 0.032, 0.022), TintB=(0.085, 0.060, 0.040), Tiling=1.0, Roughness=0.88),
    # morene olejem (jemna prace, vnitrni stavebni drevo): teple tmavsi hnede, polomatne
    "wood_oil": dict(TintA=(0.34, 0.23, 0.14), TintB=(0.50, 0.35, 0.21), Tiling=1.0, Roughness=0.8),
    # morene krvi (volska / kravska krev s vapnem): stary nater, tmave cervenohnede, matne, textura castecne odbarvena
    "wood_blood": dict(TintA=(0.075, 0.028, 0.018), TintB=(0.14, 0.055, 0.032), Tiling=1.0, Roughness=0.9, Desaturate=0.5),
    # stare neosetrene drevo (slunce, dest): sede az stribrite, odbarvene, uplne matne, zaprasene a ochozene
    "wood_old": dict(TintA=(0.34, 0.33, 0.31), TintB=(0.55, 0.53, 0.50), Tiling=1.0, Roughness=1.0, Desaturate=0.8,
                     DustTint=(0.40, 0.37, 0.32), DustAmount=0.3),
}
# zvetrani shora (v materialu podle normaly): plochy mirici nahoru svetlejsi, nazelenale (lisejnik, prach), drsnejsi.
# TopStart = od jakeho sklonu (0 svisla stena .. 1 vodorovny vrsek), TopSharp = ostrost prechodu, TopAmount = sila
MAT_TOP = {
    "face":  dict(TopTint=(0.86, 0.90, 0.76), TopStart=0.55, TopSharp=3.0, TopAmount=0.55),
    "core":  dict(TopTint=(0.86, 0.90, 0.76), TopStart=0.55, TopSharp=3.0, TopAmount=0.45),
    "frame": dict(TopTint=(0.86, 0.90, 0.76), TopStart=0.55, TopSharp=3.0, TopAmount=0.5),
    "crown": dict(TopTint=(0.80, 0.88, 0.66), TopStart=0.35, TopSharp=2.5, TopAmount=1.00),
    "wood":  dict(TopTint=(0.86, 0.86, 0.82), TopStart=0.60, TopSharp=3.0, TopAmount=0.35),    # vrch vybledly sluncem
    "wood_tar": dict(TopTint=(1.3, 1.27, 1.2), TopStart=0.6, TopSharp=3.0, TopAmount=0.3),    # dehet na vrsku jen lehce vybledne (porad tmavy)
    "wood_oil": dict(TopTint=(1.15, 1.12, 1.05), TopStart=0.60, TopSharp=3.0, TopAmount=0.25),
    "wood_blood": dict(TopTint=(1.25, 1.15, 1.10), TopStart=0.6, TopSharp=3.0, TopAmount=0.3),   # nater na vrsku lehce vybledly
    "wood_old": dict(TopTint=(1.12, 1.12, 1.10), TopStart=0.6, TopSharp=3.0, TopAmount=0.4),     # slapane / slunecne plochy svetlejsi
}
MAT_VERSION = 7                          # vyssi nez v projektu -> skript prestavi graf M_RuinStone a doplni parametry MI_*
                                         # (tinty MI_RuinFace/Frame zustanou, jak je mas; MAT_RESET viz nize)
MAT_RESET = {"crown": 2, "core": 3, "frame": 4, "wood_tar": 6}      # MI starsi nez tato verze dostane znovu tint a texturu z MAT_LOOK / TEXTURES
# --- zaoblene zvetrale kameny lice (gen_stones.py -> stones/*.obj vedle skriptu; skript je sam naimportuje)
USE_STONE_MESHES = True                  # False = vsude kostky (Cube) jako drive
STONE_DIR   = "/Game/Skvt/Lapikus/Ruin/Stones"
STONE_RATIOS = [1.2, 1.8, 2.6, 3.4]      # pomer delka/vyska variant (SM_RuinStone_R12_A ...)
STONE_VARIANTS = "ABC"
STONE_NOMINAL = (30.0, 45.0, 30.0)        # vyska, hloubka (cm) jmenoviteho kamene; delka = vyska * pomer
STONE_OVERSIZE = 1.04                    # zaobleny kamen o kousek vetsi nez blok -> spary nejsou az moc hluboke
ASHLAR_MESH = "SM_RuinAshlar"
# fyzika volnych kamenu (odpadle pres detach_stones.py, sut ve 05_constructions): trvale, at s nimi hrac muze hnout.
# Hmotnost podle objemu kamene (hustota kamene ~2600 kg/m3) -> 30x40x60 cm kamen ~160 kg, hrac s nim jen malo pohne.
DETACHED_PHYSICS = True
STONE_PHYSICS = dict(density=2600.0,     # kg/m3 (vapenec, piskovec, zula 2500-2700)
                     fill=0.85,          # podil objemu kvadru (zaoblene hrany, otluceni)
                     lin_damp=0.3, ang_damp=0.8,          # tlumeni -> kamen se nekouli donekonecna
                     friction=0.9, restitution=0.05,      # drsny kamen, skoro neodskakuje (PM_RuinStone)
                     shrink=0.97)        # o kousek mensi nez blok -> prekryv se sousedy ho pri startu nevystreli
WOOD_MESHES = True                       # tramy, prkna, sloupy z meshu zasleho dreva (SM_RuinTimber/Plank/Post_*); False = kostky
WOOD_NOMINAL = {"SM_RuinTimber": (100.0, 25.0, 25.0), "SM_RuinPlank": (100.0, 25.0, 5.0), "SM_RuinPost": (25.0, 25.0, 100.0)}
DRESSED_FRAMES = True                     # osteni, nadprazi, strilny z opracovanych kamenu SM_RuinDressed_* (False = kvadr SM_RuinAshlar)
STONE_MESH_VERSION = {"SM_RuinStone_W_": 2, "SM_RuinTimber_": 2, "SM_RuinPlank_": 2, "SM_RuinPost_": 2}   # meshe s nizsi verzi v projektu se naimportuji znovu (prefix -> verze)
MAT_WOOD = ["/Game/StarterContent/Materials/M_Wood_Oak.M_Wood_Oak", "/Game/StarterContent/Materials/M_Wood_Pine.M_Wood_Pine"]   # zaloha, kdyz chybi textury dreva pro MI_RuinWood
MAT_WOOD_MI = None                       # vlastni material neosetreneho dreva (cesta); None = MI_RuinWood (vytvori skript)
# druhy dreva (Stone.cat): "wood" bez upravy (MI_RuinWood), "wood_tar" dehtovane, "wood_oil" morene olejem,
# "wood_blood" morene krvi, "wood_old" stare neosetrene (zasedle, zaprasene)
WOOD_FINISH = {"raw": "wood", "tar": "wood_tar", "oil": "wood_oil", "blood": "wood_blood", "old": "wood_old"}
WOOD_MI = {"wood": "MI_RuinWood", "wood_tar": "MI_RuinWood_Tar", "wood_oil": "MI_RuinWood_Oil",
           "wood_blood": "MI_RuinWood_Blood", "wood_old": "MI_RuinWood_Old"}
# vychozi uprava podle casti stavby (lze prepsat v datech: floors[...]["finish"]); prkna jednoho patra: "planks_<patro>"
WOOD_FINISH_DEFAULT = dict(beams="tar", girder="tar", posts="tar", heads="tar", planks="raw", stairs="raw",
                           porch_beams="blood", porch_braces="blood", porch_posts="blood", porch_planks="blood", planks_2="old")            # osteni a oblouky: lehce srazene hrany
BLOCK_BP  = "/Game/Skvt/Lapikus/Ruin/BP_RuinBlocks"   # zalozni Blueprint s InstancedStaticMesh (kdyz nejde pridat komponentu)
TERRAIN_FROM_LEVEL = True                # True = vysky terenu se pri buildu zmeri primo z landscapu v levelu (line trace)
                                         #   a ulozi do terrain_from_level.json (capture_manual_edits pouzije tento ulozeny stav)
                                         # False = vysky z ruin_layout.json (puvodni heightmapa)
ONLY_WALLS = None                        # napr. ["Brana_V", "Brana_J"] = postavit jen tyto zdi (rychle ladeni)

OPENING_TYPES = {
    "strilna":    dict(frame=0.20, lintel="kamen",  value=0.6),
    "okno":       dict(frame=0.25, lintel="kamen",  value=1.0),
    "okno_drevo": dict(frame=0.00, lintel="drevo",  value=0.0),
    "dvere":      dict(frame=0.30, lintel="kamen",  value=1.0),
    "portal":     dict(frame=0.35, lintel="oblouk", value=1.2),
    "brana":      dict(frame=0.45, lintel="oblouk", value=1.2),
    "prulom":     dict(frame=0.00, lintel="oblouk", value=0.0),   # pozdeji vybourany otvor: bez osteni, nepravidelny "oblouk"
    "kapsa":      dict(frame=0.00, lintel="kamen",  value=0.0),   # kapsa pro tram: jen ve vnitrnim lici (ne skrz zed)
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
    st = dict(kind=o.get("kind"), robbed=robbed, arch=arch, sill=sill, top=top, x0=x0, x1=x1, wl=wl, wr=wr, frame=fr,
              splay=o.get("splay"), ragged=o.get("ragged", 0.0), s=o["s"], outer=o.get("outer", False))
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
        kl = b.get("slope_l", b.get("slope", 1.0)); kr = b.get("slope_r", b.get("slope", 1.0))   # strmost boku (1 = 45 st.)
        pl = b.get("power_l", b.get("power", 1.0)); pr = b.get("power_r", b.get("power", 1.0))   # >1 = bok se ke koruně zvedá strměji (zaoblená linie)
        h = [min(hi, b["floor"] + max(0, (c - w) - x) ** pl * kl + max(0, x - (c + w)) ** pr * kr) for hi, x in zip(h, xs)]
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


# ------------------------------------------------------------------ parametry a stari
def params(layout):
    P = dict(layout["params"])
    age = AGE or layout.get("age", "1540")
    P.update(layout.get("presets", {}).get(age, {}))
    P.update(OVERRIDE)
    P["_AGE"] = age
    return P

# ------------------------------------------------------------------ bloky
def _hash01(*k):
    return (zlib.crc32(("%d|" * len(k) % k).encode()) & 0xFFFFFF) / float(0xFFFFFF)

def blob_noise(s, z, seed, cs=0.8, czz=0.6):
    """plynuly 2D sum 0..1 (mrizka cs x czz m, smoothstep) -> sousedni kameny se rozebiraji ve hloucich"""
    u = s / cs; v = z / czz; i = math.floor(u); j = math.floor(v); fu = u - i; fv = v - j
    fu = fu * fu * (3 - 2 * fu); fv = fv * fv * (3 - 2 * fv)
    a = _hash01(seed, i, j); b = _hash01(seed, i + 1, j); c = _hash01(seed, i, j + 1); d = _hash01(seed, i + 1, j + 1)
    return (a + (b - a) * fu) * (1 - fv) + (c + (d - c) * fu) * fv

_BQ = [(0.0, 0.0), (0.02, 0.073), (0.05, 0.118), (0.1, 0.176), (0.2, 0.25), (0.3, 0.319), (0.4, 0.4), (0.5, 0.499),
       (0.6, 0.597), (0.7, 0.679), (0.8, 0.75), (0.9, 0.823), (1.0, 1.0)]
def blob_q(p):
    """prah sumu blob_noise, pod kterym lezi podil p plochy (rozlozeni sumu neni rovnomerne)"""
    p = min(max(p, 0.0), 1.0)
    for (p0, q0), (p1, q1) in zip(_BQ[:-1], _BQ[1:]):
        if p <= p1: return q0 + (q1 - q0) * (p - p0) / max(p1 - p0, 1e-9)
    return 1.0

class Stone:
    __slots__ = ("id", "cat", "x", "y", "z", "yaw", "pitch", "roll", "sx", "sy", "sz", "seg", "span", "mesh", "rough")
    def __init__(self, sid, cat, x, y, z, yaw, sx, sy, sz, pitch=0.0, roll=0.0, seg=0):
        self.span = None; self.mesh = None
        self.rough = False   # odkryte jadro: lomovy kamen (mesh) misto kostky
        self.seg = seg   # usek zdi (index rovneho useku mezi zlomy)
        self.id = sid; self.cat = cat; self.x = x; self.y = y; self.z = z; self.yaw = yaw
        self.sx = sx; self.sy = sy; self.sz = sz; self.pitch = pitch; self.roll = roll

def courses(zmin, zmax, rng, P):
    """Vodorovne rady (cm) spolecne pro celou zed."""
    out = []; z = zmin
    while z < zmax:
        hgt = rng.uniform(P["COURSE_MIN"], P["COURSE_MAX"]) * 100
        out.append((z, z + hgt)); z += hgt
    return out

def edit_applies(e, wname):
    w = e.get("wall")
    return w is None or w == wname or (isinstance(w, list) and wname in w)

def apply_plinth(wd):
    """podstavba (m): zed stoji na nizsim terenu -> vyska, parapety otvoru, ochrana a sesuvy se zvednou"""
    pl = wd.get("plinth", 0.0)
    if not pl: return wd
    wd = dict(wd, H0=wd["H0"] + pl)
    wd["openings"] = [dict(o, sill=o["sill"] + pl) for o in wd.get("openings", [])]
    wd["protect"] = [dict(p, min=p["min"] + pl) if "min" in p else p for p in wd.get("protect", [])]   # "to" = absolutne, bez podstavby
    wd["breaches"] = [dict(b, floor=b["floor"] + pl) for b in wd.get("breaches", [])]
    return wd

def _pt_on(points, s):
    """bod na lomene care ve vzdalenosti s (m) od prvniho bodu"""
    c = 0.0
    for i in range(len(points) - 1):
        p, q = points[i], points[i + 1]; ln = math.hypot(q[0] - p[0], q[1] - p[1]) / 100
        if s <= c + ln or i == len(points) - 2:
            f = (s - c) / max(ln, 1e-6); return p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f
        c += ln

def apply_ref_z(wd, terr):
    """ref_z (absolutni cm, napr. podlaha veze): vysky otvoru (sill, splay floor/top) jsou zadane od ni,
    ne od paty zdi -> prevedou se na vysky od mistni paty."""
    ref = wd.get("ref_z")
    if ref is None: return wd
    ops = []
    for o in wd.get("openings", []):
        zb = terr.z(*_pt_on(wd["points"], o["s"]))
        o = dict(o, sill=(ref + o["sill"] * 100 - zb) / 100)
        if o.get("splay"):
            sp = o["splay"]; o["splay"] = dict(sp, floor=(ref + sp["floor"] * 100 - zb) / 100, top=(ref + sp["top"] * 100 - zb) / 100)
        ops.append(o)
    return dict(wd, openings=ops)

def opening_top_abs(wd, idx, terr):
    """absolutni vyska (cm) vrsku otvoru idx vcetne osteni / oblouku (s podstavbou a z_offset)"""
    w2 = apply_ref_z(apply_plinth(wd), terr); o = w2["openings"][idx]
    zb = terr.z(*_pt_on(wd["points"], o["s"]))
    return zb + (o["sill"] + o["h"] + OPENING_TYPES[o["kind"]]["frame"]) * 100 + wd.get("z_offset", 0.0) * 100

def resolve_protect_to(wd, terr, walls):
    """ochrana s "to": [{wall, opening, dz}, ...] = zed alespon do vysky vrsku otvoru jine zdi (napr. oblouku brany);
    dva cile = linearne od s0 k s1. Prevede se na kousky po 0.5 m s min (m) od paty teto zdi."""
    out = []
    byname = {w["name"]: w for w in walls}
    for p in wd.get("protect", []):
        if "to" not in p: out.append(p); continue
        zs = [opening_top_abs(byname[t["wall"]], t.get("opening", 0), terr) + t.get("dz", 0.0) * 100 for t in p["to"]]
        z0, z1 = zs[0], zs[-1]; n = max(1, int(math.ceil((p["s1"] - p["s0"]) / 0.5)))
        for i in range(n):
            a = p["s0"] + (p["s1"] - p["s0"]) * i / n; b = p["s0"] + (p["s1"] - p["s0"]) * (i + 1) / n
            sm = min(max((a + b) / 2, 0.0), _wall_len(wd["points"]))
            za = z0 + (z1 - z0) * ((a + b) / 2 - p["s0"]) / max(p["s1"] - p["s0"], 1e-6)
            zb = terr.z(*_pt_on(wd["points"], sm))
            out.append(dict(s0=a, s1=b, min=(za - zb - wd.get("z_offset", 0.0) * 100) / 100))
    return dict(wd, protect=out)

def _wall_len(pts):
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)) / 100

def build_wall_stones(wd, P, terr, layout, edits, removed, centroid):
    wd = resolve_protect_to(wd, terr, layout.get("walls", []))
    wd = apply_ref_z(apply_plinth(wd), terr)
    rng = random.Random(wd.get("seed", 1) * 4093 + P["SEED"])
    pts = [list(p) for p in wd["points"]]
    # roh: kazda zed se na zacatku prodlouzi o pul tloustky -> rohy budou plne (u uzavrenych obrysu)
    if wd.get("extend_start", True):
        dx, dy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]; dl = math.hypot(dx, dy) or 1
        e = wd["thickness"] * 50
        pts[0] = [pts[0][0] - dx / dl * e, pts[0][1] - dy / dl * e]
    shift = wd["thickness"] / 2 if wd.get("extend_start", True) else 0.0   # s v JSON plati od puvodniho bodu
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) / 100 for i in range(len(pts) - 1)]
    cum = [0.0]
    for s in seg: cum.append(cum[-1] + s)
    L = cum[-1]
    corners = list(wd.get("corners", [])) + cum[1:-1]
    sh = lambda lst, keys: [dict(d, **{k: d[k] + shift for k in keys if k in d}) for d in lst]
    xs, h, states = wall_profile(L, wd["H0"], wd["access"], [c + shift for c in corners[:len(wd.get("corners", []))]] + corners[len(wd.get("corners", [])):],
                                 sh(wd.get("openings", []), ["s"]), sh(wd.get("breaches", []), ["s0", "s1"]),
                                 sh(wd.get("protect", []), ["s0", "s1"]), [a + shift for a in wd.get("access_points", [])], wd.get("seed", 1), P,
                                 mid=wd.get("mid", 0.88))
    edits = [dict(e, **{k: e[k] + shift for k in ("s0", "s1") if k in e}) if e["op"] in ("cut", "set_height", "restore") else e for e in edits]
    # datove upravy vysky
    for e in edits:
        if e["op"] in ("set_height", "restore") and edit_applies(e, wd["name"]):
            for i, x in enumerate(xs):
                if e["s0"] <= x <= e["s1"]:
                    h[i] = e["h"] if e["op"] == "set_height" else max(h[i], e["h"])
    # zvyseni useku zdi (m) nad vysledek rozpadu, na krajich plynule (1 m)
    for r in wd.get("raise", []):
        r0, r1 = r["s0"] + shift, r["s1"] + shift
        for i, x in enumerate(xs):
            wgt = max(0.0, min(1.0, (x - r0) + 0.5, (r1 - x) + 0.5))
            if wgt > 0: h[i] = min(h[i] + r["dh"] * wgt, wd["H0"] + r["dh"])
    access_arr = [wd["access"]] * len(xs)
    for ap in wd.get("access_points", []):
        access_arr = [a + P["ACCESS_BOOST"] * math.exp(-((x - ap) / P["ACCESS_RADIUS"]) ** 2) for a, x in zip(access_arr, xs)]
    T = wd["thickness"] * 100
    face_d = min(P["FACE_DEPTH"] * 100, T * 0.4)
    core_w = max(T - 2 * face_d, 10)
    zref = layout["plateau_z_cm"]
    # pata a koruna v absolutnich cm podel zdi
    def at(s):
        k = 0
        while k < len(seg) - 1 and s > cum[k + 1]: k += 1
        p, q = pts[k], pts[k + 1]; f = (s - cum[k]) / max(seg[k], 1e-6)
        x = p[0] + (q[0] - p[0]) * f; y = p[1] + (q[1] - p[1]) * f
        yaw = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        nx, ny = -(q[1] - p[1]) / (seg[k] * 100), (q[0] - p[0]) / (seg[k] * 100)
        return x, y, yaw, nx, ny, k
    zlo = min(terr.z(*at(s)[:2]) for s in [i * 0.5 for i in range(int(L / 0.5) + 1)]) - 120
    zhi = zref + wd["H0"] * 100 + 200
    if wd.get("course_grid"):                     # pevne rady (vez): vsechny zdi maji spary ve stejne vysce jako patra
        g0, gh = wd["course_grid"][0], wd["course_grid"][1] * 100
        k0 = int(math.floor((zlo - g0) / gh)); k1 = int(math.ceil((zhi - g0) / gh))
        crs = [(g0 + k * gh, g0 + (k + 1) * gh) for k in range(k0, k1)]
    else:
        crs = courses(zlo, zhi, rng, P)
    # ktera strana je vnitrni (k tezisti hradu): +1 = levy lic (normala), -1 = pravy
    xm, ym, _, nxm, nym, _ = at(L / 2)
    inner = 1 if (xm + nxm * 100 - centroid[0]) ** 2 + (ym + nym * 100 - centroid[1]) ** 2 < (xm - centroid[0]) ** 2 + (ym - centroid[1]) ** 2 else -1
    if wd.get("inside_pt"):                        # vnitrek mistnosti (vez): strana pro kapsy a vyklenky strilen
        ip = wd["inside_pt"]
        inside = 1 if (ip[0] - xm) * nxm + (ip[1] - ym) * nym > 0 else -1
    else:
        inside = inner
    rside = wd.get("rubble", "both")
    robbed_sides = {"out": [inner], "in": [inner], "both": [1, -1]}.get(rside, [1, -1])  # vnejsi lic nad utesem se nerozebira
    stones = []
    # zlomy lomene zdi: znamenkovy uhel (+ = zatacka doleva), prodlouzeni / zkraceni kamenu u zlomu
    bend = []
    for i_ in range(1, len(pts) - 1):
        d1 = (pts[i_][0] - pts[i_ - 1][0], pts[i_][1] - pts[i_ - 1][1]); d2 = (pts[i_ + 1][0] - pts[i_][0], pts[i_ + 1][1] - pts[i_][1])
        bend.append((cum[i_], math.atan2(d1[0] * d2[1] - d1[1] * d2[0], d1[0] * d2[0] + d1[1] * d2[1])))
    def corner_ext(th, layer):
        t_ = math.tan(min(abs(th), math.radians(80)) / 2)
        if layer == 0: return core_w / 200 * t_
        convex = (th > 0 and layer == -1) or (th < 0 and layer == 1)
        return (T / 200 * t_) if convex else -(T / 200 * t_)
    # --- otvory zarovnat na rady kamene (parapet a nadprazi lezi na sparach) + rozmery osteni po radach
    bounds = [c0 for c0, c1 in crs] + [crs[-1][1]]
    def snap(zab): return min(bounds, key=lambda b: abs(b - zab))
    for st in states:
        sm_ = (st["x0"] + st["x1"]) / 2
        zb_o = terr.z(*at(sm_)[:2]); st["zb"] = zb_o
        h0 = st["top"] - st["sill"]
        if st["sill"] > 0.05: st["sill"] = (snap(zb_o + st["sill"] * 100) - zb_o) / 100
        top = (snap(zb_o + st["top"] * 100) - zb_o) / 100
        st["top"] = top if top - st["sill"] >= 0.6 * h0 else st["sill"] + h0
        st["inside"] = inside
        if st.get("splay"):
            sp = st["splay"]
            st["niche"] = (snap(zb_o + sp["floor"] * 100), snap(zb_o + sp["top"] * 100)); st["w_in"] = sp.get("w_in", 1.6)
        fr = st["frame"]
        st["framed"] = fr > 0 and not (st["robbed"] == "both" and not (st["arch"] and not st["lintel_lost"]))
        if st["arch"]:
            r = (st["x1"] - st["x0"]) / 2
            jb = st["sill"] + st.get("jamb_h", 0); jt = st["top"] - r
        else:
            jb, jt = st["sill"], st["top"]
        st["jamb_z"] = (zb_o + jb * 100, zb_o + jt * 100)
        st["lintel_z"] = st["sill_z"] = None
        if st["framed"] and not st["arch"] and st["kind"] in ("okno", "dvere", "strilna") and not st["lintel_lost"]:
            z0 = zb_o + st["top"] * 100; z1 = z0
            for c0, c1 in crs:                       # nadprazi = 1-2 rady nad otvorem (vyska >= 1.2 * osteni)
                if c0 >= z0 - 1 and z1 - z0 < fr * 120: z1 = c1
            st["lintel_z"] = (z0, z1)
            if st["sill"] > 0.05:
                cb = [c for c in crs if abs(c[1] - (zb_o + st["sill"] * 100)) < 1]
                if cb: st["sill_z"] = cb[0]
    def forbidden(cz0, cz1, layer=1):
        """useky s (m) v teto rade (cz0..cz1 absolutni cm), kam nesmi zadny blok zdi: svetlost otvoru
        + osteni/nadprazi/parapet/oblouk (ty postavi opracovane kvadry). Bloky se v techto mistech rozdeli
        -> otvor je vzdy pruhledny."""
        out = []
        e = 1.0                                       # cm
        for st in states:
            x0, x1, fr = st["x0"], st["x1"], st["frame"]
            z0r = (cz0 - st["zb"]) / 100; z1r = (cz1 - st["zb"]) / 100
            if st["kind"] == "kapsa":                  # kapsa: jen vnitrni lic (outer=True: jen vnejsi lic, napr. po podeste)
                if layer == (-st["inside"] if st.get("outer") else st["inside"]) and z1r > st["sill"] + 0.01 and z0r < st["top"] - 0.01:
                    out.append((x0, x1))
                continue
            if st.get("niche") and layer in (0, st["inside"]):
                # vyklenek strilny zevnitr: siroky prostor (do nej se postavi sikme boky) + preklad nad nim
                n0, n1 = st["niche"]; c = (x0 + x1) / 2; wi = st["w_in"] / 2
                if cz1 > n0 + e and cz0 < n1 - e: out.append((c - wi - 0.05, c + wi + 0.05))
                elif cz1 > n1 + e and cz0 < n1 + 36: out.append((c - wi - 0.25, c + wi + 0.25))
            if st.get("ragged") and layer != 0 and z1r > st["sill"] + 0.01 and z0r < st["top"] + 0.2:
                # rozbitejsi okraje pruchodu: lic kolem otvoru nahodne vylamany (jadro zustava)
                rr_ = random.Random(zlib.crc32(("%s|%d|%d" % (wd["name"], round(cz0), layer)).encode()))
                out.append((x0 - rr_.uniform(0, st["ragged"]), x0)); out.append((x1, x1 + rr_.uniform(0, st["ragged"])))
            framed = st["framed"]
            okL = st["arch"] or st["robbed"] != "one" or st.get("wl", 0) == 0
            okR = st["arch"] or st["robbed"] != "one" or st.get("wr", 0) == 0
            jz = st["jamb_z"]
            if framed and cz1 > jz[0] + e and cz0 < jz[1] - e:
                if okL: out.append((x0 - fr, x0))
                if okR: out.append((x1, x1 + fr))
            if st["arch"]:
                r = (x1 - x0) / 2; c = (x0 + x1) / 2; spring = st["top"] - r
                # vylomene opracovane kameny ostění: kdyz oblouk stoji, zustane za nimi jadro (nese oblouk)
                if st["jamb_h"] > 0 and z1r > st["sill"] + 0.01 and z0r < st["sill"] + st["jamb_h"] - 0.01 \
                   and (layer != 0 or st["lintel_lost"]):
                    if st["wl"] > 0: out.append((x0 - st["wl"], x0))
                    if st["wr"] > 0: out.append((x1, x1 + st["wr"]))
                rr = r + (fr if framed and not st["lintel_lost"] else 0.0)
                if z1r > st["sill"] + 0.01 and z0r < spring + rr - 0.01:
                    if z1r <= spring + 0.01:
                        out.append((x0, x1))               # pod patkou oblouku jen svetlost (paty nese zdivo / jadro)
                    else:
                        zl = max(z0r, spring)
                        hw = math.sqrt(max(rr * rr - (zl - spring) ** 2, 0.0))
                        out.append((c - hw, c + hw))
            else:
                if z1r > st["sill"] + 0.01 and z0r < st["top"] - 0.01:
                    if layer != 0 or st["lintel_lost"]:
                        out.append((x0 - st["wl"], x1 + st["wr"]))
                    else:                                  # nadprazi stoji -> jadro za vylomenym ostěním ho nese
                        out.append((x0, x1))
                for zz in (st["lintel_z"], st["sill_z"]):
                    if zz and cz1 > zz[0] + e and cz0 < zz[1] - e:
                        out.append((x0 - fr, x1 + fr))
        return out
    def subtract(s0, s1, bad):
        pieces = [(s0, s1)]
        for a, b in bad:
            nxt = []
            for p0, p1 in pieces:
                if b <= p0 or a >= p1: nxt.append((p0, p1)); continue
                if a > p0: nxt.append((p0, a))
                if b < p1: nxt.append((b, p1))
            pieces = nxt
        return [p for p in pieces if p[1] - p[0] >= 0.12]
    def cut_hit(x, y, z0, z1, s0, s1, z0r, z1r):
        for e in edits:
            if not edit_applies(e, wd["name"]): continue
            if e["op"] == "cut" and s1 > e["s0"] and s0 < e["s1"] and z1r > e["z0"] and z0r < e["z1"]: return True
            if e["op"] == "cut_box":
                b = e["box"]
                if b[0] <= x <= b[3] and b[1] <= y <= b[4] and z1 > b[2] and z0 < b[5]: return True
        return False
    prev = {1: None, 0: None, -1: None}           # obsazene useky predchozi rady (podpora)
    def bridged(s0, s1, below, row):
        """klenuti / malta: kamen nad mezerou do BRIDGE m drzi, kdyz lezi obema konci (levy konec muze drzet i soused v rade)"""
        BR = P.get("BRIDGE", 0.6); e_ = min(0.25, (s1 - s0) / 2)
        sup = sorted((max(s0, b0), min(s1, b1)) for b0, b1 in below if b1 > s0 and b0 < s1)
        left = any(b0 < s0 + e_ and b1 > s0 + 0.04 for b0, b1 in sup) or any(abs(r1 - s0) < 0.05 for _, r1 in row)
        right = any(b1 > s1 - e_ and b0 < s1 - 0.04 for b0, b1 in sup)
        if not (left and right): return False
        x_ = s0; gap = 0.0
        for b0, b1 in sup:
            gap = max(gap, b0 - x_); x_ = max(x_, b1)
        return max(gap, s1 - x_) <= BR
    def lintel_over(s0, s1, z0r):
        for st in states:
            if st["lintel_lost"] or st["frame"] <= 0: continue
            if st["robbed"] == "both" and not st["arch"]: continue
            if s1 > st["x0"] - st["frame"] and s0 < st["x1"] + st["frame"] and z0r >= st["top"] - 0.05: return True
        return False
    for ci, (cz0, cz1) in enumerate(crs):
        cur = {1: [], 0: [], -1: []}
        # tri vrstvy: levy lic (+1), jadro (0), pravy lic (-1)
        for layer in (1, 0, -1):
            off = (T / 2 - face_d / 2) * layer if layer else 0.0
            depth = face_d if layer else core_w
            lmin, lmax = (P["STONE_MIN"], P["STONE_MAX"]) if layer else (P["CORE_MIN"], P["CORE_MAX"])
            s = -rng.uniform(0, lmax) if ci % 2 else 0.0           # prevazba
            if wd.get("extend_start", True) and layer == 0: s = face_d / 100     # jadro az za nárožním kvádrem
            bi = 0
            while s < L:
                ln = rng.uniform(lmin, lmax); s0 = max(s, 0.0); s1 = min(s + ln, L); s = s + ln
                sid = "%s|%d|%d|%d" % (wd["name"], ci, layer, bi); bi += 1
                srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])   # nahoda vazana na blok -> upravy neposunou ostatni
                # blok pres zlom zdi se rozdeli na dva kusy (kazdy rovne podel sveho useku)
                bnds = [s0] + [kc for kc in cum[1:-1] if s0 + 0.01 < kc < s1 - 0.01] + [s1]
                pieces = []
                for a_, b_ in zip(bnds[:-1], bnds[1:]):
                    if b_ - a_ >= 0.12: pieces += subtract(a_, b_, forbidden(cz0, cz1, layer))
                if not pieces: continue
                sid0 = sid; os0, os1 = s0, s1
                for pi, (s0, s1) in enumerate(pieces):
                    # nerozdeleny blok si necha puvodni id (rucni upravy plati dal), kusy dostanou .a/.b
                    sid = sid0 if len(pieces) == 1 else "%s.%s" % (sid0, "abcdefgh"[pi])
                    if sid != sid0: srng = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
                    sc = (s0 + s1) / 2
                    x, y, yaw, nx, ny, k = at(sc)
                    zb = terr.z(x, y)
                    top_abs = zb + interp(sc, xs, h) * 100
                    if cz0 >= top_abs: continue
                    part = (top_abs - cz0) / (cz1 - cz0)
                    if part < 1 and srng.random() > part * 1.15: continue      # rozvolnena koruna
                    if cz1 < zb - 140: continue                              # hluboko pod terenem
                    z0r = (cz0 - zb) / 100; z1r = (cz1 - zb) / 100
                    # rozebrany lic (odkryje jadro): hlavne shora pod korunou (kameny se berou odshora), u paty jen
                    # mensi hloucky tam, kam se dosahne. Plynuly sum -> hloucky sousednich kamenu, ne jednotlive dirky
                    if layer in robbed_sides and layer != 0 and part >= 1:
                        a = interp(sc, xs, access_arr)
                        wseed = zlib.crc32(wd["name"].encode()) ^ P["SEED"]
                        zr_side = z0r
                        if wd.get("ref_z") and layer == inside: zr_side = (cz0 - wd["ref_z"]) / 100   # vnitrek veze: od podlahy
                        dc = (top_abs - cz1) / 100                                   # hloubka rady pod korunou (m)
                        p_top = P.get("TOP_ROB", 0.55) * (0.5 + 0.5 * a) * math.exp(-max(dc, 0) / P.get("TOP_ROB_D", 0.7))
                        if blob_noise(sc, dc, wseed * 3 + layer, 0.9, 0.5) < blob_q(p_top): continue
                        H_ = P["FACE_ROB_H"]
                        if 0 <= zr_side < H_:
                            p_base = min(0.5, a * P["FACE_ROB"] * P.get("FACE_ROB_BASE", 0.45) * (1 - zr_side / H_) ** 1.5)
                            if blob_noise(sc, zr_side, wseed * 5 + layer, 0.7, 0.45) < blob_q(p_base): continue
                    cx = x + nx * off; cy = y + ny * off
                    if cut_hit(cx, cy, cz0, cz1, s0, s1, z0r, z1r): continue
                    # podpora: blok musi lezet na necem (predchozi rada v teze nebo vedlejsi vrstve, nebo nadprazi)
                    if z0r > 0.2 and prev[layer] is not None:
                        # lic musi lezet na licovem kameni (ne jen na jadru) -> zadne kameny lice visici nad vybranou mezerou;
                        # jadro se opira o cokoli pod sebou
                        below = prev[layer] if layer else prev[0] + prev[1] + prev[-1]
                        ov = sum(max(0, min(s1, b1) - max(s0, b0)) for b0, b1 in below)
                        if ov < 0.3 * (s1 - s0) and not lintel_over(s0, s1, z0r) \
                           and not (layer and bridged(s0, s1, below, cur[layer])): continue
                    cur[layer].append((s0, s1))
                    # zchatrale: u koruny pootocene a vysunute bloky (u otvoru jen nepatrne, at nezasahuji do svetlosti)
                    loose = part < 1.6 and layer != 0
                    if abs(s0 - os0) > 1e-6 or abs(s1 - os1) > 1e-6: loose = False   # kus u otvoru: drzi lic
                    yaw2 = yaw + (srng.uniform(-6, 6) if loose else srng.uniform(-0.8, 0.8))
                    pitch = srng.uniform(-4, 4) if loose else 0.0
                    push = srng.uniform(0, 4) * layer if loose else 0.0
                    gapw = P["JOINT"] * 100
                    cxx = cx + nx * push; cyy = cy + ny * push
                    if layer == 0: gapw = 0.0                # jadro bez spar (je skryte) -> zed neni skrz pruhledna
                    # na zlomu zdi: vnejsi (vypukla) strana se prodlouzi az do spolecne hrany licu, vnitrni se zkrati
                    e0 = e1 = 0.0
                    for kc, th in bend:
                        if abs(s1 - kc) < 1e-6: e1 = corner_ext(th, layer)
                        if abs(s0 - kc) < 1e-6: e0 = corner_ext(th, layer)
                    lenc = (s1 - s0 + e0 + e1) * 100 - gapw
                    if lenc < 8: continue
                    if e0 or e1:
                        ya = math.radians(yaw); dsh = (e1 - e0) * 50
                        cxx += math.cos(ya) * dsh; cyy += math.sin(ya) * dsh
                    stones.append(Stone(sid, "core" if layer == 0 else "face", cxx, cyy, (cz0 + cz1) / 2, yaw2,
                                        lenc, depth - gapw, (cz1 - cz0) - gapw * 0.7, pitch, seg=k))
                    stones[-1].span = (s0 - e0, s1 + e1, z0r, z1r)  # pro kontrolu (test_openings.py)
        # narozni kvadr na zacatku zdi (zakryje prurez zdi v rohu)
        if wd.get("extend_start", True):
            sc = face_d / 200
            x, y, yaw, nx, ny, k = at(sc); zb = terr.z(x, y)
            top_abs = zb + interp(sc, xs, h) * 100
            z0r = (cz0 - zb) / 100; z1r = (cz1 - zb) / 100
            sid = "%s|%d|Q" % (wd["name"], ci)
            if cz1 <= top_abs and cz1 > zb - 140 and not cut_hit(x, y, cz0, cz1, 0, sc * 2, z0r, z1r) \
               and (z0r <= 0.2 or prev[1] is None or any(b0 < sc * 2 for b0, b1 in prev[1] + prev[-1])):
                # narozi z vice kamenu pres tloustku zdi: u vnejsiho rohu strida dlouhy a kratky kvadr (vazba narozi),
                # zbytek tloustky lomove kameny bezne delky
                qr = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
                first = qr.uniform(1.0, 1.35) if ci % 2 == 0 else qr.uniform(0.45, 0.7)
                lens = [first]
                while sum(lens) < T / 100 - 0.01:
                    rest = T / 100 - sum(lens)
                    l_ = qr.uniform(P["STONE_MIN"], P["STONE_MAX"])
                    if rest - l_ < P["STONE_MIN"]: l_ = rest
                    lens.append(min(l_, rest))
                out_s = -inner                                   # vnejsi strana zdi (od teziste hradu)
                t = out_s * T / 2                                 # zacit u vnejsiho rohu
                for qi, l_ in enumerate(lens):
                    tc = t - out_s * l_ * 50
                    qid = sid if qi == 0 else "%s.%d" % (sid, qi)
                    stones.append(Stone(qid, "face", x + nx * tc, y + ny * tc, (cz0 + cz1) / 2, yaw + 90.0 + qr.uniform(-0.6, 0.6),
                                        l_ * 100 - P["JOINT"] * 100, face_d - 1.5, (cz1 - cz0) - 1.0, seg=k))
                    t -= out_s * l_ * 100
                cur[1].append((0, sc * 2)); cur[-1].append((0, sc * 2))
        prev = cur
    # osteni a oblouky intaktnich otvoru (opracovane kvadry, cela tloustka zdi)
    SPLIT = P.get("FRAME_SPLIT", 1.1) * 100                # kvadr delsi nez toto (cm) se v hloubce rozdeli na vic kamenu
    def put_frame(sid, x, y, z, yaw, sx, sy, sz, pitch=0.0, seg=0, along="y"):
        """opracovany kamen; pres silnou zed (nebo dlouhy bok vyklenku) z vice kusu ruzne delky, spary strida"""
        L_ = sy if along == "y" else sx
        if L_ <= SPLIT:
            stones.append(Stone(sid, "frame", x, y, z, yaw, sx, sy, sz, pitch, seg=seg)); return
        r_ = random.Random(zlib.crc32(sid.encode()) ^ P["SEED"])
        lens = []; tot = L_ / 100
        first = r_.uniform(0.75, 1.0) if r_.random() < 0.5 else r_.uniform(0.4, 0.6)
        while sum(lens) < tot - 0.01:
            rest = tot - sum(lens); l_ = first if not lens else r_.uniform(0.5, 1.0)
            if rest - l_ < 0.35: l_ = rest
            lens.append(min(l_, rest))
        a = math.radians(yaw)
        ax_, ay_ = ((-math.sin(a), math.cos(a)) if along == "y" else (math.cos(a), math.sin(a)))
        t = -L_ / 2
        for i, l_ in enumerate(lens):
            tc = t + l_ * 50
            w_ = l_ * 100 - (1.0 if i < len(lens) - 1 else 0.0)
            stones.append(Stone(sid if i == 0 else "%s.%d" % (sid, i), "frame", x + ax_ * tc, y + ay_ * tc, z,
                                yaw + r_.uniform(-0.4, 0.4), w_ if along == "x" else sx, w_ if along == "y" else sy, sz, pitch, seg=seg))
            t += l_ * 100
    for oi, st in enumerate(states):
        if st["frame"] <= 0: continue
        if st["robbed"] == "both" and not (st["arch"] and not st["lintel_lost"]): continue
        fr = st["frame"]; sm_ = (st["x0"] + st["x1"]) / 2
        x, y, yaw, nx, ny, k = at(sm_); zb = terr.z(x, y)
        wall_top = min(interp(s_, xs, h) for s_ in (st["x0"] - fr, sm_, st["x1"] + fr))
        sp_out = -st["inside"] if st.get("niche") else 0      # strilna s vyklenkem: osteni jen ve vnejsim lici
        def add(sid, s0, s1, z0r, z1r, rot_extra=0.0, sxo=None):
            if z1r > min(interp(s0, xs, h), interp(s1, xs, h)) + 0.05: return
            xx, yy, yw, nnx, nny, kk = at((s0 + s1) / 2)
            dep = (face_d - 1) if sp_out else (T - 2)
            o_ = (T / 2 - face_d / 2) * sp_out
            # o 2 cm presah do sousednich bloku -> zadna pruhledna spara kolem osteni
            put_frame(sid, xx + nnx * o_, yy + nny * o_, zb + (z0r + z1r) / 2 * 100, yw, sxo or (s1 - s0) * 100 + 2,
                      dep, (z1r - z0r) * 100 - 0.5, rot_extra, seg=kk)
        if st.get("niche"):
            # vyklenek: sikme boky (kónické rozsireni zevnitr k uzkemu pruzoru), preklad nahore
            n0, n1 = st["niche"]; c = sm_; wi = st["w_in"] / 2; wo = (st["x1"] - st["x0"]) / 2 + fr
            dep_in = T - face_d                                   # hloubka od vnitrniho lice k vnejsimu lici
            for side in (-1, 1):
                a_s = c + side * wo; b_s = c + side * wi              # s na vnejsim lici / na vnitrnim lici
                a_n = (T / 2 - face_d) * (-st["inside"]); b_n = (T / 2) * st["inside"]
                ax_, ay_, _, nnx, nny, kk = at(a_s); bx_, by_, _, _, _, _ = at(b_s)
                A = (ax_ + nnx * a_n, ay_ + nny * a_n); Bp = (bx_ + nnx * b_n, by_ + nny * b_n)
                dx_, dy_ = Bp[0] - A[0], Bp[1] - A[1]; ln = math.hypot(dx_, dy_)
                px_, py_ = -dy_ / ln, dx_ / ln                       # kolmo na bok; ven z vyklenku
                tx_, ty_ = at(c)[0] - (A[0] + Bp[0]) / 2, at(c)[1] - (A[1] + Bp[1]) / 2
                if px_ * tx_ + py_ * ty_ > 0: px_, py_ = -px_, -py_
                mx_, my_ = (A[0] + Bp[0]) / 2 + px_ * 15, (A[1] + Bp[1]) / 2 + py_ * 15
                yw_ = math.degrees(math.atan2(dy_, dx_))
                j = 0
                for c0, c1 in crs:
                    if c0 < n0 - 1 or c1 > n1 + 1: continue
                    if (c1 - zb) / 100 > min(interp(a_s, xs, h), interp(b_s, xs, h)) + 0.05: break
                    put_frame("%s|F%d|N%s%d" % (wd["name"], oi, "L" if side < 0 else "R", j), mx_, my_, (c0 + c1) / 2,
                              yw_, ln + 8, 30, (c1 - c0) - 0.5, seg=kk, along="x")
                    j += 1
            lz0 = n1; lz1 = n1 + 35
            if (lz1 - zb) / 100 <= min(interp(c - wi, xs, h), interp(c + wi, xs, h)) + 0.05:
                xx, yy, yw, nnx, nny, kk = at(c); o_ = (face_d / 2) * st["inside"]
                put_frame("%s|F%d|NT" % (wd["name"], oi), xx + nnx * o_, yy + nny * o_, (lz0 + lz1) / 2, yw,
                          (2 * wi + 0.5) * 100, dep_in - 1, (lz1 - lz0) - 0.5, seg=kk)
        okL = st["arch"] or st["robbed"] != "one" or st.get("wl", 0) == 0
        okR = st["arch"] or st["robbed"] != "one" or st.get("wr", 0) == 0
        jz0, jz1 = st["jamb_z"]
        j = 0
        for c0, c1 in crs:                                   # ostění po radach zdi
            z0 = max(c0, jz0); z1 = min(c1, jz1)
            if z1 - z0 < 3: continue
            z0r = (z0 - zb) / 100; z1r = (z1 - zb) / 100
            if okL: add("%s|F%d|L%d" % (wd["name"], oi, j), st["x0"] - fr, st["x0"], z0r, z1r)
            if okR: add("%s|F%d|R%d" % (wd["name"], oi, j), st["x1"], st["x1"] + fr, z0r, z1r)
            j += 1
        if st["lintel_z"]:
            add("%s|F%d|T" % (wd["name"], oi), st["x0"] - fr, st["x1"] + fr, (st["lintel_z"][0] - zb) / 100, (st["lintel_z"][1] - zb) / 100)
        if st["sill_z"]:
            add("%s|F%d|B" % (wd["name"], oi), st["x0"] - fr, st["x1"] + fr, (st["sill_z"][0] - zb) / 100, (st["sill_z"][1] - zb) / 100)
        if st["arch"] and not st["lintel_lost"]:
            r = (st["x1"] - st["x0"]) / 2; spring = st["top"] - r
            n = max(5, int(math.pi * (r + fr / 2) / 0.32))
            for q in range(n):
                a0 = math.pi * q / n; a1 = math.pi * (q + 1) / n; am = (a0 + a1) / 2
                rm = r + fr / 2
                s_c = sm_ - rm * math.cos(am); z_c = spring + rm * math.sin(am)
                if z_c + fr / 2 > interp(s_c, xs, h) + 0.15: continue
                xx, yy, yw, _, _, kk = at(s_c)
                sid = "%s|F%d|A%d" % (wd["name"], oi, q)
                # klinovy kamen: delka po oblouku, natoceny kolem normaly zdi (roll)
                put_frame(sid, xx, yy, zb + z_c * 100, yw, rm * (a1 - a0) * 100 - 1.5, T - 2, fr * 100,
                          pitch=90.0 - math.degrees(am), seg=kk)
    # odkryte jadro: kde chybi lic, rozpadne se jadro na lomove kameny ruzne zapustene (ne hladka tmava stena s ostrou hranou)
    if P.get("CORE_ROUGH", True): stones = rough_core(stones, wd, P, face_d, core_w, T, removed)
    # koruna: odkryte horni kameny (nic na nich nelezi) -> zvetrale tvary a material koruny
    if CROWN_WEATHER:
        byz = {}
        for st_ in stones:
            if st_.span and st_.cat in ("face", "core"): byz.setdefault(round((st_.z - st_.sz / 2) / 3), []).append(st_)
        for st_ in stones:
            if not st_.span or st_.cat not in ("face", "core"): continue
            lay_ = int(st_.id.split("|")[2]) if st_.id.count("|") >= 3 else 0
            top_ = st_.z + st_.sz / 2
            above = [b for k_ in (round(top_ / 3) - 1, round(top_ / 3), round(top_ / 3) + 1) for b in byz.get(k_, [])
                     if abs((b.z - b.sz / 2) - top_) < 3 and int(b.id.split("|")[2]) == lay_]
            cov = sum(max(0.0, min(st_.span[1], b.span[1]) - max(st_.span[0], b.span[0])) for b in above)
            if cov < 0.5 * (st_.span[1] - st_.span[0]):
                st_.cat = "crown"
    # useky lomene cary seskupene do actoru (zaoblene zlomy: oblouk patri k sousednim rovnym usekum)
    sg = wd.get("seg_group")
    if sg:
        for st_ in stones: st_.seg = sg[min(st_.seg, len(sg) - 1)]
    # svisly posun cele zdi (m), napr. zapusteni do terenu; kameny pod terenem nejsou videt
    off = wd.get("z_offset", 0.0) * 100
    if off:
        for st_ in stones: st_.z += off
        for st_ in states: st_["zb"] += off
    return stones, states, L

def rough_core(stones, wd, P, face_d, core_w, T, removed=()):
    """Jadro, pred kterym chybi lic: blok se rozdeli na kameny 0.35-0.7 m, kazdy zapusteny o 5-20 cm od odkryte
    strany (nahodne, u okraje diry mene -> zubaty prechod), mirne pootoceny; mesh lomoveho kamene."""
    byc = {}
    for st in stones:
        if st.span and st.cat == "face" and st.id.count("|") >= 3 and st.id not in removed:   # rucne smazany lic = odkryto
            p_ = st.id.split("|")
            if p_[2] in ("1", "-1"): byc.setdefault((p_[1], int(p_[2])), []).append(st.span)
    out = []; J = P["JOINT"] * 100
    r0, r1 = P.get("CORE_RECESS", (0.05, 0.2))
    sup = {}                                   # obsazene useky kazde rady (vsechny vrstvy) -> kus jadra nesmi viset
    def ci_of(st): return int(st.id.split("|")[1]) if st.span and st.id.count("|") >= 3 and st.id.split("|")[1].isdigit() else None
    for st in stones:                          # lic a ostatni hned, jadro postupne podle rad (co spadlo, nedrzi)
        if st.cat != "core" and ci_of(st) is not None: sup.setdefault(ci_of(st), []).append(st.span)
    for st in stones:
        if not (st.span and st.cat == "core" and st.id.count("|") >= 3) or st.id in removed:   # smazane / oddelene jadro: id zustane
            out.append(st); continue
        ci = st.id.split("|")[1]
        s0, s1, z0r, z1r = st.span
        def cov(a, b, lay):
            return sum(max(0.0, min(b, f1) - max(a, f0)) for f0, f1, _, _ in byc.get((ci, lay), [])) / max(b - a, 1e-6)
        if z1r < 0.05 or (cov(s0, s1, 1) > 0.8 and cov(s0, s1, -1) > 0.8):
            out.append(st); sup.setdefault(int(ci), []).append(st.span); continue
        rng = random.Random(zlib.crc32((st.id + "|rough").encode()) ^ P["SEED"])
        ya = math.radians(st.yaw); dx, dy = math.cos(ya), math.sin(ya); nx, ny = -dy, dx
        L_ = s1 - s0; cuts = [s0]
        while cuts[-1] < s1 - 1e-6:
            l_ = rng.uniform(0.35, 0.7)
            if s1 - (cuts[-1] + l_) < 0.3: l_ = s1 - cuts[-1]
            cuts.append(min(cuts[-1] + l_, s1))
        if len(cuts) == 2 and cov(s0, s1, 1) > 0.5 and cov(s0, s1, -1) > 0.5:
            out.append(st); sup.setdefault(int(ci), []).append(st.span); continue
        cm = (s0 + s1) / 2
        for i, (a, b) in enumerate(zip(cuts[:-1], cuts[1:])):
            off_ = 0.0; dep = st.sy
            for lay in (1, -1):
                c = cov(a, b, lay)
                if c > 0.5: continue                                         # lic pred kusem stoji
                edge = cov(a - 0.4, b + 0.4, lay) > 0.15                         # u okraje diry -> mene zapusteny
                r = rng.uniform(0.0, 0.08) if edge else rng.uniform(r0, r1)
                if c == 0 and rng.random() < 0.25: r = -rng.uniform(0.0, 0.4) * face_d / 100   # zbytek zaklady lice vystupuje
                r *= 100; dep -= r; off_ -= lay * r / 2
            dep = max(dep, 15.0)
            if z0r > 0.2 and int(ci) - 1 in sup:
                ov = sum(max(0.0, min(b, q1) - max(a, q0)) for q0, q1, _, _ in sup[int(ci) - 1])
                if ov < 0.3 * (b - a): continue
            m = (a + b) / 2 - cm
            pc = Stone("%s.r%d" % (st.id, i), "core", st.x + dx * m * 100 + nx * off_, st.y + dy * m * 100 + ny * off_, st.z,
                       st.yaw + rng.uniform(-3, 3), (b - a) * 100 - J, dep, st.sz - J * 0.7, rng.uniform(-2, 2), seg=st.seg)
            pc.span = (a, b, z0r, z1r); pc.rough = True
            out.append(pc); sup.setdefault(int(ci), []).append(pc.span)
    return out

def _clip_segment_box(p, q, x0, y0, x1, y1):
    """Liang-Barsky: cast usecky p->q uvnitr obdelniku, vrati (t0, t1) nebo None."""
    dx, dy = q[0] - p[0], q[1] - p[1]; t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0: return None
        else:
            r = qq / pp
            if pp < 0: t0 = max(t0, r)
            else: t1 = min(t1, r)
    return (t0, t1) if t0 < t1 else None

def wall_box_hits(wd, box, terr):
    """Kde box (x0,y0,z0,x1,y1,z1 v cm) protina osu zdi: [(s0, s1, sill_m, top_m)], s od prvniho bodu zdi."""
    pts = wd["points"]; hits = []; cum = 0.0
    pad = wd["thickness"] * 50
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]; ln = math.hypot(q[0] - p[0], q[1] - p[1]) / 100
        r = _clip_segment_box(p, q, box[0] - pad * 0.2, box[1] - pad * 0.2, box[3] + pad * 0.2, box[4] + pad * 0.2)
        if r:
            t0, t1 = r; tm = (t0 + t1) / 2
            zb = terr.z(p[0] + (q[0] - p[0]) * tm, p[1] + (q[1] - p[1]) * tm)
            hits.append((cum + t0 * ln, cum + t1 * ln, (box[2] - zb) / 100, (box[5] - zb) / 100))
        cum += ln
    return hits

def apply_volumes(layout, volumes, terr):
    """Prevede objemy z levelu (TriggerBox s tagem) na upravy:
       Ruin_Cut            -> cut_box (vyrizne vse uvnitr)
       Ruin_Opening:<typ>  -> novy otvor ve zdi (okno, dvere, portal, brana, strilna, prulom) s plnou logikou rozpadu
                              + Ruin_Intact (osteni cele) / Ruin_Protect (oblouk se nezrouti)
       Ruin_Keep           -> restore: zdi v boxu alespon do vysky vrsku boxu
       Ruin_Explode        -> bloky uvnitr jako samostatne actory (rucni posun / mazani)"""
    walls = [dict(w, openings=list(w.get("openings", []))) for w in layout["walls"]]
    edits = list(layout.get("edits", [])); explode = []
    for v in volumes:
        tags = v["tags"]; box = v["box"]
        if "Ruin_Cut" in tags:
            edits.append({"op": "cut_box", "box": box})
        if "Ruin_Explode" in tags:
            explode.append(box)
        kinds = [t.split(":", 1)[1] for t in tags if t.startswith("Ruin_Opening:")]
        keep = "Ruin_Keep" in tags
        if not kinds and not keep: continue
        for w in walls:
            for s0, s1, sill, top in wall_box_hits(w, box, terr):
                if s1 - s0 < 0.1: continue
                if keep:
                    edits.append({"op": "restore", "wall": w["name"], "s0": s0, "s1": s1, "h": top})
                for kind in kinds:
                    o = dict(kind=kind if kind in OPENING_TYPES else "prulom", s=(s0 + s1) / 2, w=s1 - s0,
                             sill=max(0.0, sill), h=max(0.3, top - max(0.0, sill)))
                    if "Ruin_Intact" in tags: o["robbed"] = "none"
                    if "Ruin_Protect" in tags: o["protect"] = True
                    w["openings"].append(o)
    return dict(layout, walls=walls, edits=edits), explode

def in_box(s, box):
    return box[0] <= s.x <= box[3] and box[1] <= s.y <= box[4] and box[2] <= s.z <= box[5]

def stone_mesh_name(st):
    """Varianta zaobleneho kamene podle pomeru delka/vyska bloku (deterministicky podle id)."""
    if not USE_STONE_MESHES: return None
    if st.cat in WOOD_MI:
        if not WOOD_MESHES: return None
        v = "ABC"[zlib.crc32(st.id.encode()) % 3]
        if st.sz > 1.5 * max(st.sx, st.sy): return "SM_RuinPost_" + v          # sloup (delka nahoru)
        if st.sz < 0.45 * st.sy: return "SM_RuinPlank_" + v                     # prkno, fosna schodu
        return "SM_RuinTimber_" + v
    if st.cat == "floor" or (st.cat == "frame" and not DRESSED_FRAMES): return ASHLAR_MESH
    if st.cat == "frame":
        r = max(st.sx, 1) / max(st.sz, 1)
        best = min(STONE_RATIOS, key=lambda q: abs(math.log(r / q)))
        return "SM_RuinDressed_R%02d_%s" % (round(best * 10), "AB"[zlib.crc32(st.id.encode()) % 2])
    if st.cat not in ("face", "crown") and not (st.cat == "core" and st.rough): return None
    r = max(st.sx, 1) / max(st.sz, 1)
    best = min(STONE_RATIOS, key=lambda q: abs(math.log(r / q)))
    v = STONE_VARIANTS[zlib.crc32(st.id.encode()) % len(STONE_VARIANTS)]
    return "SM_RuinStone_%sR%02d_%s" % ("W_" if st.cat == "crown" else "", round(best * 10), v)

def assign_meshes(stones):
    for st in stones:
        st.mesh = stone_mesh_name(st)
        if st.mesh and st.cat in ("face", "crown", "core") and (zlib.crc32(st.id.encode()) >> 8) & 1:
            st.yaw += 180.0          # otoceni kamene o 180 st. = dalsi varianta vzhledu (rozmer sedi)

def build_floor_stones(fs, P, walls_out, terr=None):
    """Podlahy ve vezi (layout["floors"]): kamenna dlazba prizemi + tramy v kapsach a hrube prkna v patrech.
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

def compute_blocks(layout, removed=(), moved=None, volumes=None, rubble=False, detached=()):
    """detached = id kamenu oddelenych od zdi (detach_stones.py): vzdy samostatne actory, i mimo Ruin_Explode"""
    P = params(layout); terr = Terrain(layout["terrain"])
    vols = list(layout.get("volumes", [])) + list(volumes or [])
    layout, explode = apply_volumes(layout, vols, terr)
    removed = set(removed); moved = moved or {}; detached = set(detached or ())
    edits = list(layout.get("edits", []))
    allpts = [p for w in layout["walls"] for p in w["points"]]
    centroid = (sum(p[0] for p in allpts) / len(allpts), sum(p[1] for p in allpts) / len(allpts))
    out = {}
    for wd in layout["walls"]:
        if ONLY_WALLS and wd["name"] not in ONLY_WALLS: continue
        stones, states, L = build_wall_stones(wd, P, terr, layout, edits, removed | detached, centroid)   # oddeleny lic = odkryte jadro
        out[wd["name"]] = dict(folder=wd["folder"], stones=stones)
    for fs in layout.get("floors", []):
        if ONLY_WALLS and fs["name"] not in ONLY_WALLS and not any(w in ONLY_WALLS for w in fs.get("walls", [])): continue
        out[fs["name"]] = dict(folder=fs.get("folder", "Ruin"), stones=build_floor_stones(fs, P, out, terr))
    # sut na zemi: od 11/2026 ve 05_constructions (build_constructions.py); rubble=True ji prida i sem (stary zpusob)
    if rubble:
        for name, r in make_rubble(out, P, terr, removed).items():
            out[name]["rubble"] = r["stones"]
    for w in out.values():
        assign_meshes(w["stones"] + w.get("rubble", []))
    for name, w in out.items():
        w["stones"] = [st for st in w["stones"] if st.id not in removed and st.id.split(".r")[0] not in removed]
        # rucne posunute bloky a rozlozeni na samostatne kameny
        # samostatne kameny = jen ty v boxu Ruin_Explode (podle puvodni i posunute polohy);
        # posunute kameny mimo box se vrati do Instanced Static Mesh na nove misto ("slouceni")
        loose_ids = set()
        for st in w["stones"] + w.get("rubble", []):
            if any(in_box(st, b) for b in explode) or st.id in detached: loose_ids.add(st.id)
            m = moved.get(st.id)
            if m:
                st.x, st.y, st.z, st.roll, st.pitch, st.yaw = m
                if any(in_box(st, b) for b in explode): loose_ids.add(st.id)
        loose_ids.update(st.id for st in w.get("rubble", []))      # kameny na zemi vzdy samostatne
        w["loose"] = [st for st in w["stones"] + w.get("rubble", []) if st.id in loose_ids]
        lid = set(id(st) for st in w["loose"])
        w["stones"] = [st for st in w["stones"] if id(st) not in lid]
        w["rubble"] = [st for st in w.get("rubble", []) if id(st) not in lid]
    return out, P

# ------------------------------------------------------------------ Unreal
def _script_dir():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.path.dirname(LAYOUT_PATH) if LAYOUT_PATH else os.getcwd()

def load_layout():
    path = LAYOUT_PATH or os.path.join(_script_dir(), "ruin_layout.json")
    with open(path, encoding="utf-8") as f: return json.load(f)

def edits_path():
    return os.path.join(os.path.dirname(LAYOUT_PATH) if LAYOUT_PATH else _script_dir(), "manual_edits.json")

def load_manual():
    p = edits_path()
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f: d = json.load(f)
        return d.get("removed", []), d.get("moved", {})
    return [], {}

def load_detached():
    """id kamenu oddelenych od zdi (detach_stones.py) z manual_edits.json"""
    p = edits_path()
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f: return set(json.load(f).get("detached", []))
    return set()

def save_manual(removed, moved, detached):
    with open(edits_path(), "w", encoding="utf-8") as f:
        json.dump({"removed": sorted(removed), "moved": moved, "detached": sorted(detached)}, f, ensure_ascii=False, indent=1)

def load_removed():
    return load_manual()[0]

def gather_volumes(unreal, eas):
    """TriggerBoxy (nebo jine actory) s tagy Ruin_Cut / Ruin_Opening:<typ> / Ruin_Keep / Ruin_Explode."""
    vols = []
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        if not any(t.startswith(("Ruin_Cut", "Ruin_Opening", "Ruin_Keep", "Ruin_Explode")) for t in tags): continue
        origin, ext = a.get_actor_bounds(False)
        vols.append(dict(tags=tags, name=a.get_actor_label(),
                         box=[origin.x - ext.x, origin.y - ext.y, origin.z - ext.z, origin.x + ext.x, origin.y + ext.y, origin.z + ext.z]))
    return vols

def _asset_path(folder, name): return "%s/%s.%s" % (folder, name, name)

def ensure_materials(unreal):
    """Vrati {"face": mat, "core": mat, "frame": mat}. Chybejici M_RuinStone / MI_Ruin* vytvori (jen poprve,
    pak je muzes upravovat v editoru - skript je neprepise)."""
    eal = unreal.EditorAssetLibrary
    mats = {}
    user = {"face": MAT_FACE, "core": MAT_CORE, "frame": MAT_FRAME, "crown": MAT_CROWN}
    if all(user.values()):
        return {c: unreal.load_asset(p) for c, p in user.items()}
    def pick(cat):
        for d, n in TEXTURES[cat]:
            if eal.does_asset_exist(d): return unreal.load_asset(d), (unreal.load_asset(n) if n and eal.does_asset_exist(n) else None)
        return None, None
    at = unreal.AssetToolsHelpers.get_asset_tools(); mel = unreal.MaterialEditingLibrary
    mpath = _asset_path(MAT_DIR, "M_RuinStone")
    if eal.does_asset_exist(mpath):
        master = unreal.load_asset(mpath)
    else:
        d0, n0 = pick("face")
        if not d0:
            unreal.log_warning("Ruin: nenalezeny textury pro material (StarterContent?) - nastav MAT_FACE/MAT_CORE/MAT_FRAME.")
            return {c: (unreal.load_asset(p) if p else None) for c, p in user.items()}
        master = at.create_asset("M_RuinStone", MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
        _build_master(unreal, master, d0, n0)
        unreal.log("Ruin: vytvoren material %s" % mpath)
    if _ver(eal, master, "RuinMatVersion") < MAT_VERSION:
        # starsi graf (bez zvetrani shora) -> prestavet na miste; instance (MI_*) zustanou a jen se doplni parametry
        d0, n0 = pick("face")
        mel.delete_all_material_expressions(master)
        _build_master(unreal, master, d0, n0)
        unreal.log("Ruin: material %s prestaven na verzi %d (zvetrani shora)" % (mpath, MAT_VERSION))
    for cat, mi_name in (("face", "MI_RuinFace"), ("core", "MI_RuinCore"), ("frame", "MI_RuinFrame"), ("crown", "MI_RuinCrown")):
        if user[cat]:
            mats[cat] = unreal.load_asset(user[cat]); continue
        ip = _asset_path(MAT_DIR, mi_name)
        if eal.does_asset_exist(ip):
            mi = unreal.load_asset(ip)
            if _ver(eal, mi, "RuinMatVersion") < MAT_VERSION:       # doplnit nove parametry, rucni upravy jinak nechat
                reset = _ver(eal, mi, "RuinMatVersion") < MAT_RESET.get(cat, 0)
                if reset:
                    d, n = pick(cat)
                    if d: mel.set_material_instance_texture_parameter_value(mi, "BaseColor", d)
                    if n:
                        try: mel.set_material_instance_texture_parameter_value(mi, "Normal", n)
                        except Exception: pass
                _set_top(unreal, mel, mi, cat, look=reset)
                eal.set_metadata_tag(mi, "RuinMatVersion", str(MAT_VERSION)); eal.save_loaded_asset(mi)
            mats[cat] = mi; continue
        mi = at.create_asset(mi_name, MAT_DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
        mel.set_material_instance_parent(mi, master)
        d, n = pick(cat)
        if d: mel.set_material_instance_texture_parameter_value(mi, "BaseColor", d)
        if n:
            try: mel.set_material_instance_texture_parameter_value(mi, "Normal", n)
            except Exception: pass
        lk = MAT_LOOK[cat]
        for pn in ("TintA", "TintB"):
            c = lk[pn]; mel.set_material_instance_vector_parameter_value(mi, pn, unreal.LinearColor(c[0], c[1], c[2], 1))
        for pn in ("Tiling", "Roughness"):
            mel.set_material_instance_scalar_parameter_value(mi, pn, lk[pn])
        _set_top(unreal, mel, mi, cat)
        eal.set_metadata_tag(mi, "RuinMatVersion", str(MAT_VERSION))
        eal.save_loaded_asset(mi)
        mats[cat] = mi
    for wc, wn in WOOD_MI.items():
        mats[wc] = _wood_mi(unreal, master, pick, wc, wn)
    for wc in WOOD_MI:                                   # chybi-li textury, aspon stejne drevo vsude
        mats[wc] = mats[wc] or mats.get("wood")
    return mats

def _wood_mi(unreal, master, pick, cat="wood", name="MI_RuinWood"):
    """MI_RuinWood(_Tar/_Oil): drevo na M_RuinStone (textura dreva, tint podle upravy, matne). Bez textur dreva -> MAT_WOOD."""
    eal = unreal.EditorAssetLibrary; mel = unreal.MaterialEditingLibrary
    if MAT_WOOD_MI and cat == "wood": return unreal.load_asset(MAT_WOOD_MI)
    ip = _asset_path(MAT_DIR, name)
    if eal.does_asset_exist(ip):
        mi = unreal.load_asset(ip)
        if _ver(eal, mi, "RuinMatVersion") < MAT_RESET.get(cat, 0):        # novejsi vychozi vzhled -> prepsat tint a vybledani
            _set_top(unreal, mel, mi, cat, look=True)
            eal.set_metadata_tag(mi, "RuinMatVersion", str(MAT_VERSION)); eal.save_loaded_asset(mi)
        return mi
    d, n = pick(cat)
    if not d or master is None:
        return next((unreal.load_asset(p) for p in MAT_WOOD if eal.does_asset_exist(p.split(".")[0])), None)
    mi = unreal.AssetToolsHelpers.get_asset_tools().create_asset(name, MAT_DIR, unreal.MaterialInstanceConstant,
                                                                unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(mi, master)
    mel.set_material_instance_texture_parameter_value(mi, "BaseColor", d)
    if n:
        try: mel.set_material_instance_texture_parameter_value(mi, "Normal", n)
        except Exception: pass
    _set_top(unreal, mel, mi, cat, look=True)
    eal.set_metadata_tag(mi, "RuinMatVersion", str(MAT_VERSION)); eal.save_loaded_asset(mi)
    unreal.log("Ruin: vytvoren material dreva %s" % ip)
    return mi


def _ver(eal, asset, tag):
    try: return int(eal.get_metadata_tag(asset, tag) or 0)
    except Exception: return 0


def _set_top(unreal, mel, mi, cat, look=False):
    """parametry zvetrani shora (MAT_TOP); look=True prepise i tint / drsnost z MAT_LOOK"""
    lk = MAT_TOP[cat]
    c = lk["TopTint"]; mel.set_material_instance_vector_parameter_value(mi, "TopTint", unreal.LinearColor(c[0], c[1], c[2], 1))
    for pn in ("TopStart", "TopSharp", "TopAmount"):
        mel.set_material_instance_scalar_parameter_value(mi, pn, lk[pn])
    if look:
        lk = MAT_LOOK[cat]
        for pn in ("TintA", "TintB"):
            c = lk[pn]; mel.set_material_instance_vector_parameter_value(mi, pn, unreal.LinearColor(c[0], c[1], c[2], 1))
        for pn in ("Tiling", "Roughness", "Desaturate", "DustAmount"):
            if pn in lk: mel.set_material_instance_scalar_parameter_value(mi, pn, lk[pn])
        if "DustTint" in lk:
            c = lk["DustTint"]; mel.set_material_instance_vector_parameter_value(mi, "DustTint", unreal.LinearColor(c[0], c[1], c[2], 1))
    mel.update_material_instance(mi)


def _build_master(unreal, master, d0, n0):
    """graf M_RuinStone: textura s nahodnym posunem UV a tintem na kamen + zvetrani shora podle normaly
    (VertexNormalWS.z: plochy nahoru svetlejsi / nazelenale a drsnejsi, rozbite texturou)"""
    mel = unreal.MaterialEditingLibrary; eal = unreal.EditorAssetLibrary
    for prop in ("used_with_instanced_static_meshes", "used_with_nanite"):
        try: master.set_editor_property(prop, True)
        except Exception: pass
    E = lambda cls, x, y: mel.create_material_expression(master, cls, x, y)
    C = mel.connect_material_expressions
    def scal(name, val, x, y):
        e_ = E(unreal.MaterialExpressionScalarParameter, x, y)
        e_.set_editor_property("parameter_name", name); e_.set_editor_property("default_value", val); return e_
    def vec(name, c, x, y):
        e_ = E(unreal.MaterialExpressionVectorParameter, x, y)
        e_.set_editor_property("parameter_name", name); e_.set_editor_property("default_value", unreal.LinearColor(c[0], c[1], c[2], 1)); return e_
    tc = E(unreal.MaterialExpressionTextureCoordinate, -1400, 0)
    pir = E(unreal.MaterialExpressionPerInstanceRandom, -1400, 200)
    k = E(unreal.MaterialExpressionConstant, -1400, 300); k.set_editor_property("r", 7.31)
    mul = E(unreal.MaterialExpressionMultiply, -1200, 250)
    C(pir, "", mul, "A"); C(k, "", mul, "B")
    add = E(unreal.MaterialExpressionAdd, -1000, 100)          # nahodny posun UV na kamen -> kazdy kamen jinak
    C(tc, "", add, "A"); C(mul, "", add, "B")
    til = scal("Tiling", 1.0, -1000, 300)
    uv = E(unreal.MaterialExpressionMultiply, -800, 150)
    C(add, "", uv, "A"); C(til, "", uv, "B")
    tx = E(unreal.MaterialExpressionTextureSampleParameter2D, -550, -100)
    tx.set_editor_property("parameter_name", "BaseColor")
    if d0: tx.set_editor_property("texture", d0)
    C(uv, "", tx, "UVs")
    ta = vec("TintA", (0.62, 0.58, 0.52), -550, 200)
    tb = vec("TintB", (0.95, 0.90, 0.80), -550, 400)
    lp = E(unreal.MaterialExpressionLinearInterpolate, -300, 300)
    C(ta, "", lp, "A"); C(tb, "", lp, "B"); C(pir, "", lp, "Alpha")
    # odbarveni textury (Desaturate 0..1: stare / morene drevo) a zaprasení (DustTint, DustAmount) - vychozi 0 = beze zmeny
    ds = E(unreal.MaterialExpressionDesaturation, -350, -250)
    C(tx, "RGB", ds, ""); C(scal("Desaturate", 0.0, -550, -300), "", ds, "Fraction")
    bc0 = E(unreal.MaterialExpressionMultiply, -150, -100)
    C(ds, "", bc0, "A"); C(lp, "", bc0, "B")
    bc = E(unreal.MaterialExpressionLinearInterpolate, 0, 0)
    C(bc0, "", bc, "A"); C(vec("DustTint", (0.40, 0.37, 0.32), -300, -450), "", bc, "B")
    C(scal("DustAmount", 0.0, -300, -550), "", bc, "Alpha")
    # --- zvetrani shora: maska = saturate((N.z - TopStart) * TopSharp) * TopAmount, rozbita jasem textury
    vn = E(unreal.MaterialExpressionVertexNormalWS, -1400, 900)
    cm = E(unreal.MaterialExpressionComponentMask, -1200, 900)
    for ch, on in (("r", False), ("g", False), ("b", True), ("a", False)): cm.set_editor_property(ch, on)
    C(vn, "", cm, "")
    t_st = scal("TopStart", 0.55, -1200, 1050)
    sb = E(unreal.MaterialExpressionSubtract, -1000, 950); C(cm, "", sb, "A"); C(t_st, "", sb, "B")
    t_sh = scal("TopSharp", 3.0, -1000, 1100)
    m1 = E(unreal.MaterialExpressionMultiply, -800, 950); C(sb, "", m1, "A"); C(t_sh, "", m1, "B")
    sat = E(unreal.MaterialExpressionSaturate, -650, 950); C(m1, "", sat, "")
    brk = E(unreal.MaterialExpressionAdd, -650, 1100)          # 0.5 + jas textury -> skvrny, ne rovnomerny nater
    half = E(unreal.MaterialExpressionConstant, -800, 1150); half.set_editor_property("r", 0.5)
    C(tx, "G", brk, "A"); C(half, "", brk, "B")
    m2 = E(unreal.MaterialExpressionMultiply, -500, 1000); C(sat, "", m2, "A"); C(brk, "", m2, "B")
    t_am = scal("TopAmount", 0.5, -500, 1150)
    m3 = E(unreal.MaterialExpressionMultiply, -350, 1000); C(m2, "", m3, "A"); C(t_am, "", m3, "B")
    mask = E(unreal.MaterialExpressionSaturate, -200, 1000); C(m3, "", mask, "")
    t_ti = vec("TopTint", (0.86, 0.90, 0.76), -350, 700)
    tcol = E(unreal.MaterialExpressionMultiply, -100, 500); C(bc, "", tcol, "A"); C(t_ti, "", tcol, "B")
    fin = E(unreal.MaterialExpressionLinearInterpolate, 100, 200)
    C(bc, "", fin, "A"); C(tcol, "", fin, "B"); C(mask, "", fin, "Alpha")
    mel.connect_material_property(fin, "", unreal.MaterialProperty.MP_BASE_COLOR)
    ro = scal("Roughness", 0.9, -300, 600)
    one = E(unreal.MaterialExpressionConstant, -100, 750); one.set_editor_property("r", 1.0)
    rl = E(unreal.MaterialExpressionLinearInterpolate, 100, 650)
    C(ro, "", rl, "A"); C(one, "", rl, "B"); C(mask, "", rl, "Alpha")
    mel.connect_material_property(rl, "", unreal.MaterialProperty.MP_ROUGHNESS)
    if n0:
        nx = E(unreal.MaterialExpressionTextureSampleParameter2D, -550, 1400)
        nx.set_editor_property("parameter_name", "Normal"); nx.set_editor_property("texture", n0)
        nx.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
        C(uv, "", nx, "UVs")
        mel.connect_material_property(nx, "RGB", unreal.MaterialProperty.MP_NORMAL)
    mel.recompile_material(master)
    eal.set_metadata_tag(master, "RuinMatVersion", str(MAT_VERSION))
    eal.save_loaded_asset(master)

def _needed_meshes():
    names = ["SM_RuinStone_%sR%02d_%s" % (w, round(r * 10), v) for w in ("", "W_") for r in STONE_RATIOS for v in STONE_VARIANTS]
    if DRESSED_FRAMES: names += ["SM_RuinDressed_R%02d_%s" % (round(r * 10), v) for r in STONE_RATIOS for v in "AB"]
    if WOOD_MESHES: names += ["%s_%s" % (k, v) for k in WOOD_NOMINAL for v in "ABC"]
    return names + [ASHLAR_MESH]

def ensure_stone_meshes(unreal):
    """Nacte zaoblene kameny z STONE_DIR; chybejici naimportuje ze stones/*.obj vedle skriptu
    (box kolize + Nanite). Vrati {jmeno: StaticMesh}; co chybi, nahradi se kostkou."""
    if not USE_STONE_MESHES: return {}
    eal = unreal.EditorAssetLibrary
    def want(n): return max([v for pf, v in STONE_MESH_VERSION.items() if n.startswith(pf)] or [0])
    missing = []
    for n in _needed_meshes():
        pth = _asset_path(STONE_DIR, n)
        if not eal.does_asset_exist(pth): missing.append(n); continue
        if want(n) and _ver(eal, unreal.load_asset(pth), "RuinStoneVersion") < want(n): missing.append(n)   # novejsi OBJ -> znovu
    src = os.path.join(_script_dir(), "stones")
    tasks = []
    for n in missing:
        f = os.path.join(src, n + ".obj")
        if not os.path.exists(f): continue
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", f); t.set_editor_property("destination_path", STONE_DIR)
        t.set_editor_property("destination_name", n)
        t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True)
        t.set_editor_property("save", True)
        tasks.append(t)
    if tasks:
        unreal.log("Ruin: importuji %d kamenu z %s" % (len(tasks), src))
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    out = {}; n_fix = 0
    sms = None
    try: sms = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    except Exception: pass
    for n in _needed_meshes():
        pth = _asset_path(STONE_DIR, n)
        if not eal.does_asset_exist(pth):
            # Interchange obcas pojmenuje asset jinak (napr. podle objektu v OBJ) - zkus najit podle jmena
            hits = [a for a in eal.list_assets(STONE_DIR, recursive=True) if a.split(".")[-1].startswith(n)] \
                if eal.does_directory_exist(STONE_DIR) else []
            if not hits: continue
            pth = hits[0]
        sm = unreal.load_asset(pth)
        if not isinstance(sm, unreal.StaticMesh): continue
        if n in [t.get_editor_property("destination_name") for t in tasks] and sms:
            try:      # jednoducha kolize = kvadr (hrac nepropadne)
                sms.remove_collisions(sm); sms.add_simple_collisions(sm, unreal.ScriptCollisionShapeType.BOX)
            except Exception as ex: unreal.log_warning("Ruin: kolize %s: %s (pridej rucne Collision -> Add Box)" % (n, ex))
            try:
                ns = sm.get_editor_property("nanite_settings"); ns.set_editor_property("enabled", True)
                sms.set_nanite_settings(sm, ns, True)
            except Exception as ex: unreal.log_warning("Ruin: Nanite %s: %s (zapni rucne v meshi)" % (n, ex))
            if want(n): eal.set_metadata_tag(sm, "RuinStoneVersion", str(want(n)))
            eal.save_loaded_asset(sm)
        if _fix_collision(unreal, sm, sms): n_fix += 1
        out[n] = sm
    if n_fix: unreal.log("Ruin: kolize opravena u %d meshu kamenu (jednoducha kolize misto Complex as Simple -> jde fyzika)" % n_fix)
    lost = [n for n in _needed_meshes() if n not in out]
    if lost:
        unreal.log_warning("Ruin: chybi %d kamenu (%s...) -> pouziji se kostky. Zkopiruj slozku stones/ vedle skriptu." % (len(lost), lost[0]))
    return out

def _fix_collision(unreal, sm, sms):
    """volne kameny s fyzikou potrebuji jednoduchou kolizi: Complex as Simple (import OBJ / Interchange) fyziku nepusti.
    -> kolize "Default" + kvadr, kdyz zadna jednoducha kolize neni. Vrati True, kdyz se neco menilo."""
    changed = False
    try:
        if sms and sms.get_simple_collision_count(sm) == 0:
            sms.add_simple_collisions(sm, unreal.ScriptCollisionShapeType.BOX); changed = True
    except Exception as ex:
        unreal.log_warning("Ruin: kolize %s: %s (pridej rucne Collision -> Add Box)" % (sm.get_name(), ex))
    try:
        bs = sm.get_editor_property("body_setup")
        if bs and bs.get_editor_property("collision_trace_flag") == unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE:
            bs.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_DEFAULT); changed = True
    except Exception as ex:
        unreal.log_warning("Ruin: Collision Complexity %s: %s (v meshi nastav Collision Complexity = Project Default)" % (sm.get_name(), ex))
    if changed:
        try: sm.modify(); unreal.EditorAssetLibrary.save_loaded_asset(sm)
        except Exception: pass
    return changed

_FIX = {}
def _mesh_fix(unreal, mesh, nominal):
    """Lokalni transformace meshe: posun pivotu do stredu, prohozeni os (kdyz import otocil osy) a rozmer.
    Vrati (Transform rotace+posun pro jednotkove meritko, extent po osach meshe, role os)."""
    key = mesh.get_path_name()
    if key in _FIX: return _FIX[key]
    bb = mesh.get_bounding_box()
    mn, mx = bb.min, bb.max
    ext = [max(mx.x - mn.x, 0.01), max(mx.y - mn.y, 0.01), max(mx.z - mn.z, 0.01)]
    c = [(mx.x + mn.x) / 2, (mx.y + mn.y) / 2, (mx.z + mn.z) / 2]
    import itertools
    em = max(ext); nm = max(nominal)
    best = min(itertools.permutations(range(3)),
               key=lambda pr: sum(abs(ext[i] / em - nominal[pr[i]] / nm) for i in range(3)))
    # sloupce rotace: osa meshe i -> svetova role best[i]; liche permutace -> zrcadleni jedne osy (det = +1)
    cols = []
    for i in range(3):
        v = [0.0, 0.0, 0.0]; v[best[i]] = 1.0; cols.append(v)
    inv = sum(1 for i in range(3) for j in range(i + 1, 3) if best[i] > best[j])
    if inv % 2: cols[0] = [-q for q in cols[0]]
    V = lambda q: unreal.Vector(q[0], q[1], q[2])
    rot = unreal.MathLibrary.make_rotation_from_axes(V(cols[0]), V(cols[1]), V(cols[2]))
    _FIX[key] = (rot, ext, best, c)
    return _FIX[key]

def stone_transform(unreal, s, mesh, nominal):
    """Transformace instance: mesh naskalovany presne na rozmer bloku (s.sx, s.sy, s.sz)."""
    rot, ext, role, c = _mesh_fix(unreal, mesh, nominal)
    k = STONE_OVERSIZE if s.mesh and s.cat == "face" else 1.0
    dims = [max(s.sx, 2) * k, max(s.sy, 2) * k, max(s.sz, 2) * k]
    sc = [dims[role[i]] / ext[i] for i in range(3)]
    local = unreal.Transform(location=unreal.Vector(-c[0] * sc[0], -c[1] * sc[1], -c[2] * sc[2]),
                             rotation=unreal.Rotator(0, 0, 0), scale=unreal.Vector(sc[0], sc[1], sc[2]))
    fix = unreal.Transform(location=unreal.Vector(0, 0, 0), rotation=rot, scale=unreal.Vector(1, 1, 1))
    st = unreal.Transform(location=unreal.Vector(s.x, s.y, s.z), rotation=unreal.Rotator(roll=s.roll, pitch=s.pitch, yaw=s.yaw),
                          scale=unreal.Vector(1, 1, 1))
    cm = unreal.MathLibrary.compose_transforms
    return cm(cm(local, fix), st)

def _unit(unreal, t):
    loc, rot, _ = unreal.MathLibrary.break_transform(t)
    return unreal.Transform(location=loc, rotation=rot, scale=unreal.Vector(1, 1, 1))

def _fix_unit(unreal, s, mesh, nominal):
    """Korekce meshe bez meritka: actor = F * kamen (presne invertovatelne)."""
    rot, ext, role, c = _mesh_fix(unreal, mesh, nominal)
    full = stone_transform(unreal, s, mesh, nominal)
    st = unreal.Transform(location=unreal.Vector(s.x, s.y, s.z), rotation=unreal.Rotator(roll=s.roll, pitch=s.pitch, yaw=s.yaw),
                          scale=unreal.Vector(1, 1, 1))
    return unreal.MathLibrary.compose_transforms(_unit(unreal, full), unreal.MathLibrary.invert_transform(st))

def _resolve(unreal, s, cube, meshes):
    m = meshes.get(s.mesh) if s.mesh else None
    if m is None: return cube, (100.0, 100.0, 100.0)
    if s.mesh == ASHLAR_MESH: return m, (100.0, 100.0, 100.0)
    if s.mesh.rsplit("_", 1)[0] in WOOD_NOMINAL: return m, WOOD_NOMINAL[s.mesh.rsplit("_", 1)[0]]
    r = float(s.mesh.rsplit("_R", 1)[1][:2]) / 10
    h, d = STONE_NOMINAL[0], STONE_NOMINAL[1]
    return m, (h * r, d, h)

def _new_actor(unreal, eas):
    actor = eas.spawn_actor_from_class(unreal.Actor, unreal.Vector(0, 0, 0))
    sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    root = sds.k2_gather_subobject_data_for_instance(actor)[0]
    return actor, sds, root

def _add_ism(unreal, sds, root):
    prm = unreal.AddNewSubobjectParams(parent_handle=root, new_class=unreal.InstancedStaticMeshComponent, blueprint_context=None)
    handle, fail = sds.add_new_subobject(prm)
    comp = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle))
    if not isinstance(comp, unreal.InstancedStaticMeshComponent): raise RuntimeError("komponenta nevznikla")
    return comp

def _ism_actor(unreal, eas, name, folder, parts, material, tag):
    """Actor s InstancedStaticMeshComponent pro kazdy mesh v parts [(mesh, [Transform])].
    Komponenty pres SubobjectDataSubsystem, jinak Blueprint BLOCK_BP (pak jeden actor na mesh)."""
    actors = []
    try:
        actor, sds, root = _new_actor(unreal, eas)
        try:
            comps = [_add_ism(unreal, sds, root) for _ in parts]
        except Exception:
            eas.destroy_actor(actor); raise
        for comp, (mesh, trs) in zip(comps, parts):
            comp.set_static_mesh(mesh)
            if material: comp.set_material(0, material)
            comp.add_instances(trs, False, True)
        actors.append(actor)
    except Exception as ex:
        bp = unreal.load_asset(BLOCK_BP)
        if not bp:
            raise RuntimeError("Nejde pridat InstancedStaticMeshComponent (%s) a chybi Blueprint %s. "
                               "Vytvor ho podle README_bloky.md kap. 1." % (ex, BLOCK_BP))
        for mesh, trs in parts:
            actor = eas.spawn_actor_from_object(bp, unreal.Vector(0, 0, 0), unreal.Rotator())
            comp = actor.get_component_by_class(unreal.InstancedStaticMeshComponent)
            comp.set_static_mesh(mesh)
            if material: comp.set_material(0, material)
            comp.add_instances(trs, False, True)
            actors.append(actor)
    for i, actor in enumerate(actors):
        actor.tags = [tag, unreal.Name("RuinBlocks")]
        actor.set_folder_path(folder)
        actor.set_actor_label(name if i == 0 else "%s_%d" % (name, i + 1))
    return actors

def _terrain_cache_path():
    return os.path.join(os.path.dirname(os.path.abspath(LAYOUT_PATH)) if LAYOUT_PATH else _script_dir(), "terrain_from_level.json")

def sample_level_terrain(unreal, layout):
    """Zmeri vysky landscapu v mrizce layout["terrain"] (line trace shora, ignoruje vse krome landscapu).
    Vysledek ulozi do terrain_from_level.json a vrati upraveny layout."""
    t = layout["terrain"]
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    x0, y0, st, nx, ny = t["x0"], t["y0"], t["step"], t["nx"], t["ny"]
    x1, y1 = x0 + (nx - 1) * st, y0 + (ny - 1) * st
    ignore = []
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.LandscapeProxy): continue
        try:
            o, e = a.get_actor_bounds(False)
            if o.x + e.x < x0 or o.x - e.x > x1 or o.y + e.y < y0 or o.y - e.y > y1: continue
        except Exception:
            pass
        ignore.append(a)
    Z = [row[:] for row in t["z"]]; hits = 0
    with unreal.ScopedSlowTask(ny, "Merim teren z landscapu...") as task:
        task.make_dialog(True)
        for j in range(ny):
            task.enter_progress_frame(1)
            for i in range(nx):
                x, y = x0 + i * st, y0 + j * st
                res = unreal.SystemLibrary.line_trace_single(world, unreal.Vector(x, y, 200000), unreal.Vector(x, y, -200000),
                                                            unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ignore,
                                                            unreal.DrawDebugTrace.NONE, True)
                hit = res[-1] if isinstance(res, tuple) else res
                if hit is None: continue
                try: vals = list(unreal.GameplayStatics.break_hit_result(hit))
                except Exception: vals = list(hit.to_tuple())
                if not vals or not vals[0]: continue
                act = next((v for v in vals if isinstance(v, unreal.Actor)), None)
                loc = next((v for v in vals if isinstance(v, unreal.Vector)), None)
                if loc is None or (act is not None and not isinstance(act, unreal.LandscapeProxy)): continue
                Z[j][i] = round(loc.z); hits += 1
    layout = dict(layout, terrain=dict(t, z=Z))
    with open(_terrain_cache_path(), "w", encoding="utf-8") as f:
        json.dump(dict(t, z=Z, hits=hits), f)
    unreal.log("Ruin: teren z levelu - %d / %d bodu zasahlo landscape (ulozeno terrain_from_level.json)" % (hits, nx * ny))
    if hits < nx * ny * 0.5:
        unreal.log_warning("Ruin: landscape zasazen jen v %d bodech - zbytek z ruin_layout.json. Ma landscape kolizi?" % hits)
    return layout

def cached_level_terrain(layout):
    p = _terrain_cache_path()
    if TERRAIN_FROM_LEVEL and os.path.exists(p):
        t = json.load(open(p, encoding="utf-8")); t.pop("hits", None)
        if (t["x0"], t["y0"], t["nx"], t["ny"]) == (layout["terrain"]["x0"], layout["terrain"]["y0"], layout["terrain"]["nx"], layout["terrain"]["ny"]):
            return dict(layout, terrain=t)
    return layout

def build_in_unreal():
    import unreal
    layout = load_layout(); removed, moved = load_manual()
    if TERRAIN_FROM_LEVEL:
        try:
            layout = sample_level_terrain(unreal, layout)
        except Exception as ex:
            unreal.log_warning("Ruin: mereni terenu z levelu selhalo (%s) - pouziji vysky z ruin_layout.json" % ex)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    vols = gather_volumes(unreal, eas)
    detached = load_detached()
    data, P = compute_blocks(layout, removed, moved, vols, detached=detached)
    cube = unreal.load_asset(CUBE_MESH)
    mats = ensure_materials(unreal)
    mats["floor"] = mats.get("frame")
    if not mats.get("wood"):
        mats["wood"] = next((unreal.load_asset(p) for p in MAT_WOOD if unreal.EditorAssetLibrary.does_asset_exist(p.split(".")[0])), None)
    for wc in WOOD_MI: mats[wc] = mats.get(wc) or mats["wood"]
    meshes = ensure_stone_meshes(unreal)
    tag = unreal.Name(RUIN_TAG); n_total = 0
    with unreal.ScopedEditorTransaction("Build ruin (blocks)"):
        old = [a for a in eas.get_all_level_actors() if tag in a.tags
               and (not ONLY_WALLS or any(a.get_actor_label().startswith(w + "_") for w in ONLY_WALLS))]
        if old: eas.destroy_actors(old)
        with unreal.ScopedSlowTask(len(data), "Stavim zriceninu z bloku...") as task:
            task.make_dialog(True)
            for name, w in data.items():
                task.enter_progress_frame(1, name)
                groups = {}
                for s in w["stones"] + w.get("rubble", []):
                    groups.setdefault((s.seg, s.cat), []).append(s)
                nseg = len(set(k[0] for k in groups))
                for (seg, cat), sts in sorted(groups.items()):
                    bym = {}
                    for s in sts:
                        m, nom = _resolve(unreal, s, cube, meshes)
                        bym.setdefault(m.get_path_name(), [m, []])[1].append(stone_transform(unreal, s, m, nom))
                    cname = {"face": "Lic", "core": "Jadro", "frame": "Osteni", "wood": "Drevo", "wood_tar": "Drevo_Dehet", "wood_oil": "Drevo_Olej",
                             "wood_blood": "Drevo_Krev", "wood_old": "Drevo_Stare",
                             "floor": "Podlaha", "crown": "Koruna"}[cat]
                    label = ("%s_%02d_%s" % (name, seg + 1, cname)) if nseg > 1 else ("%s_%s" % (name, cname))
                    _ism_actor(unreal, eas, label, w["folder"] + ("/%s" % name if nseg > 1 else ""),
                               [tuple(v) for _, v in sorted(bym.items())], mats.get(cat), tag)
                    n_total += len(sts)
                # samostatne kameny (sut, Ruin_Explode / rucne posunute): kazdy vlastni actor, ID v tagu
                for s in w.get("loose", []):
                    m, nom = _resolve(unreal, s, cube, meshes)
                    act = eas.spawn_actor_from_object(m, unreal.Vector(s.x, s.y, s.z), unreal.Rotator(roll=s.roll, pitch=s.pitch, yaw=s.yaw))
                    if not act: continue
                    act.set_actor_transform(stone_transform(unreal, s, m, nom), False, False)
                    act.tags = [tag, unreal.Name("RuinStone"), unreal.Name("id:" + s.id)] + ([unreal.Name("Ruin_Detached")] if s.id in detached else [])
                    act.set_folder_path(w["folder"] + ("/Sut" if "|R" in s.id else "/Odpadle" if s.id in detached else "/Kameny"))
                    act.set_actor_label("Kamen_" + s.id.replace("|", "_"))
                    if mats.get(s.cat): act.static_mesh_component.set_material(0, mats[s.cat])
                    if DETACHED_PHYSICS and s.id in detached:
                        stone_physics(unreal, act, s, asleep=s.id in moved)
                    n_total += 1
    unreal.log("Zricenina z bloku (%s): %d bloku ve %d zdech, objemu %d, samostatnych kamenu %d, rucne smazanych %d, posunutych %d, zaoblenych meshu %d." % (
        P["_AGE"], n_total, len(data), len(vols), sum(len(w.get("loose", [])) for w in data.values()), len(removed), len(moved), len(meshes)))

def capture_manual_edits():
    """Ulozi rucni upravy do manual_edits.json:
       - smazane bloky (chybi v Instanced Static Mesh nebo chybi samostatny kamen)
       - posunute / pootocene samostatne kameny (Ruin_Explode)"""
    import unreal
    layout = cached_level_terrain(load_layout()); removed, moved = load_manual(); removed = set(removed)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    detached = load_detached()
    data, P = compute_blocks(layout, removed, moved, gather_volumes(unreal, eas), detached=detached)
    cube = unreal.load_asset(CUBE_MESH)
    meshes = ensure_stone_meshes(unreal)
    present = set(); loose_now = {}
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        if RUIN_TAG not in tags: continue
        ids = [t[3:] for t in tags if t.startswith("id:")]
        if ids:
            loose_now[ids[0]] = a
            continue
        for comp in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
            for i in range(comp.get_instance_count()):
                res = comp.get_instance_transform(i, True)
                tr = res[-1] if isinstance(res, tuple) else res
                t = tr.translation
                present.add((round(t.x), round(t.y), round(t.z)))
    n_rem = 0; n_mov = 0
    for name, w in data.items():
        for s in w["stones"] + w.get("rubble", []):
            m, nom = _resolve(unreal, s, cube, meshes)
            t = stone_transform(unreal, s, m, nom).translation
            if (round(t.x), round(t.y), round(t.z)) not in present:
                removed.add(s.id); n_rem += 1
        for s in w.get("loose", []):
            a = loose_now.get(s.id)
            if a is None:
                removed.add(s.id); moved.pop(s.id, None); detached.discard(s.id); n_rem += 1; continue
            # poloha "kamene" = transformace actoru bez lokalni korekce meshe (F = otoceni os + posun pivotu, meritko 1)
            m, nom = _resolve(unreal, s, cube, meshes)
            st_t = unreal.MathLibrary.compose_transforms(unreal.MathLibrary.invert_transform(_fix_unit(unreal, s, m, nom)),
                                                         _unit(unreal, a.get_actor_transform()))
            loc, rot, _ = unreal.MathLibrary.break_transform(st_t)
            cur = [loc.x, loc.y, loc.z, rot.roll, rot.pitch, rot.yaw]
            same = all(abs(p - q) < 1.0 for p, q in zip(cur[:3], [s.x, s.y, s.z])) and \
                   all(abs(((p - q) + 180) % 360 - 180) < 1.0 for p, q in zip(cur[3:], [s.roll, s.pitch, s.yaw]))
            if not same:
                moved[s.id] = [round(v, 2) for v in cur]; n_mov += 1
    save_manual(removed, moved, detached)
    unreal.log("manual_edits.json: oddeleno %d, smazano %d (nove %d), posunuto %d (nove %d)." % (len(detached), len(removed), n_rem, len(moved), n_mov))

_PM = {}
def ensure_phys_material(unreal):
    """PM_RuinStone (fyzikalni material kamene: trenie, odraz, hustota) - vytvori se jednou, pak ho lze ladit v editoru"""
    if "pm" in _PM: return _PM["pm"]
    path = _asset_path(MAT_DIR, "PM_RuinStone"); pm = None
    try:
        eal = unreal.EditorAssetLibrary
        if eal.does_asset_exist(path):
            pm = unreal.load_asset(path)
        else:
            pm = unreal.AssetToolsHelpers.get_asset_tools().create_asset("PM_RuinStone", MAT_DIR, unreal.PhysicalMaterial, unreal.PhysicalMaterialFactoryNew())
            for k, v in (("friction", STONE_PHYSICS["friction"]), ("static_friction", STONE_PHYSICS["friction"]),
                         ("restitution", STONE_PHYSICS["restitution"]), ("density", STONE_PHYSICS["density"] / 1000.0)):
                try: pm.set_editor_property(k, v)
                except Exception: pass
            eal.save_loaded_asset(pm)
    except Exception as ex:
        unreal.log_warning("Ruin: PM_RuinStone nejde vytvorit (%s) - kameny budou mit vychozi fyzikalni material" % ex)
    _PM["pm"] = pm
    return pm

def stone_mass_kg(s):
    return s.sx * s.sy * s.sz / 1e6 * STONE_PHYSICS["fill"] * STONE_PHYSICS["density"]

def stone_physics(unreal, act, s, on=True, asleep=False):
    """volny kamen s trvalou fyzikou: hmotnost podle objemu, tlumeni, drsny material.
    asleep = kamen uz je usazeny (ulozena poloha) -> spi, dokud do nej nekdo nestrci"""
    smc = act.static_mesh_component
    if not on:
        smc.set_simulate_physics(False)
        try: smc.set_collision_profile_name("BlockAll")
        except Exception: pass
        smc.set_mobility(unreal.ComponentMobility.STATIC)
        return
    smc.set_mobility(unreal.ComponentMobility.MOVABLE)
    k = STONE_PHYSICS["shrink"]
    if k != 1.0:
        sc = act.get_actor_scale3d(); act.set_actor_scale3d(unreal.Vector(sc.x * k, sc.y * k, sc.z * k))
    try: smc.set_collision_profile_name("PhysicsActor")
    except Exception: pass
    pm = ensure_phys_material(unreal)
    if pm:
        try: smc.set_phys_material_override(pm)
        except Exception: pass
    try: smc.set_mass_override_in_kg(unreal.Name("None"), max(stone_mass_kg(s), 5.0), True)
    except Exception as ex: unreal.log_warning("Ruin: hmotnost %s: %s" % (s.id, ex))
    try:
        smc.set_linear_damping(STONE_PHYSICS["lin_damp"]); smc.set_angular_damping(STONE_PHYSICS["ang_damp"])
    except Exception: pass
    if asleep:
        try:
            bi = smc.get_editor_property("body_instance"); bi.set_editor_property("start_awake", False)
            smc.set_editor_property("body_instance", bi)
        except Exception: pass
    smc.set_simulate_physics(True)

def _has_unreal():
    try:
        import unreal  # noqa
        return True
    except ImportError:
        return False

MODE = "build"        # "build" = postavit, "capture" = ulozit rucne smazane bloky

if (__name__ == "__main__" or "unreal" in sys.modules) and not getattr(sys, "_ruin_import_only", False):
    if _has_unreal():
        capture_manual_edits() if MODE == "capture" else build_in_unreal()
    else:
        if len(sys.argv) > 1: LAYOUT_PATH = sys.argv[1]
        lay = load_layout(); rm, mv = load_manual(); data, P = compute_blocks(lay, rm, mv, detached=load_detached())
        tot = 0
        for n, w in data.items():
            c = {"face": 0, "core": 0, "frame": 0, "wood": 0, "floor": 0, "crown": 0}
            for s in w["stones"] + w.get("loose", []): c["wood" if s.cat in WOOD_MI else s.cat] = c.get("wood" if s.cat in WOOD_MI else s.cat, 0) + 1
            tot += sum(c.values()) + len(w.get("rubble", []))
            print("  %-18s lic %5d  jadro %4d  osteni %3d  sut %3d" % (n, c["face"], c["core"], c["frame"], len(w.get("rubble", [])))
                  + ("  koruna %4d" % c["crown"]) + ("  drevo %4d  dlazba %3d" % (c["wood"], c["floor"]) if c["wood"] or c["floor"] else ""))
        print("stari:", P["_AGE"], " bloku celkem:", tot)
