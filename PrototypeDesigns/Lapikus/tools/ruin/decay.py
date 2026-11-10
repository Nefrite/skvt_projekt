"""Model rozpadu zdi - sdileny pro nakresy i pozdejsi build_ruin.py

Dve slozky:
  1) PRIRODNI ROZPAD (cas) - mirny: zubata koruna, nizsi pole mezi rohy, V-zarezy nad otvory
  2) AKTIVNI ROZEBIRANI (lide berou kamen) - podle DOSTUPNOSTI zdi:
       access 0 = nedostupna (vnejsi zed nad utesem, vnejsi lic veze)
       access 1 = nejdostupnejsi (vnitrni pricky v nadvori)
     + mistni zvyseni u pristupovych mist (brana, dvere) -> zdi se tam rozebiraji vic
     + podle VYSKY: co je v dosahu (do REACH), se rozebere rychle; vysoka zed jen pomalu
       -> nizke zdi (a nizka mista ve zdi: V-zarezy, prulomy) mizi nejvic, vysoke zdi zustavaji
     Rozebirani bere kamen shora po radach -> rovnejsi, stupnovita koruna.
  3) OTVORY (okna, strilny, dvere, portaly, brana): opracovane osteni je nejcennejsi kamen ->
     dostupna osteni se vylamou (otvor se rozsiri, zmizi nadprazi -> V-zarez); vysoko polozena
     a nedostupna (zed nad utesem, vez) zustanou cela. Oblouky drzi, vylamou se jen spodni osteni.
"""
import numpy as np
from scipy.ndimage import uniform_filter1d
sm = lambda v, k: uniform_filter1d(v, k, mode="nearest")

WEATHER = 0.9          # kolik vysky zbude po prirodnim rozpadu (1 = nic)
ROBBING = 4.75         # rychlost rozebirani (m za obdobi) pri access = 1 a zdi v dosahu
REACH = 8.0            # m, do jake vysky se kamen bere snadno (z terenu, suti, zebriku, lesení)
ACCESS_RADIUS = 6.0    # m, dosah zvyseni dostupnosti od pristupoveho mista
ACCESS_BOOST = 0.3
FRAME_REACH = 2.5      # m, do jake vysky se vylamou ostění oblouku (portal, brana)

# Typy otvoru. frame = sirka kamenneho osteni (m), lintel = cim je otvor zaklenut,
# value = jak moc stoji za to osteni vylamat (opracovany kamen je nejcennejsi)
OPENING_TYPES = {
    "strilna":    dict(frame=0.20, lintel="kamen",  value=0.6),   # uzka strbina, uvnitr sikmy vyklenek
    "okno":       dict(frame=0.25, lintel="kamen",  value=1.0),   # kamenne osteni + nadprazi, vyklenek se sedatky
    "okno_drevo": dict(frame=0.00, lintel="drevo",  value=0.0),   # jednoduche okno s drevenym prekladem
    "dvere":      dict(frame=0.30, lintel="kamen",  value=1.0),   # kamenny portal s nadprazim
    "portal":     dict(frame=0.35, lintel="oblouk", value=1.2),   # klenuty portal
    "brana":      dict(frame=0.45, lintel="oblouk", value=1.2),   # bransky oblouk, drazka pro mriz, kapsy pro zavoru
}

def opening_state(o, access_local, rng, reach=REACH):
    """Co se stalo s otvorem. Vraci dict:
       robbed: none / one / both (vylamane osteni), side (l/r pro 'one'),
       x0, x1, sill, top: novy (rozsireny) otvor, lintel_lost: zda nad otvorem vznikl V-zarez,
       jamb_h: do jake vysky jsou vylamana osteni u oblouku, frame: sirka osteni."""
    t = OPENING_TYPES[o.get("kind", "okno")]
    f_h = min(1.0, reach / (o["sill"] + 1.5))                     # vysoko polozene osteni se bere hur
    score = access_local * t["value"] * f_h + rng.normal(0, 0.06)
    robbed = "none" if score < 0.25 or t["frame"] == 0 else ("one" if score < 0.42 else "both")
    robbed = o.get("robbed", robbed)                              # rucni prepis (napr. dochovane jedno osteni)
    side = o.get("side", "l" if rng.random() < 0.5 else "r")
    fr = t["frame"]; rag = lambda: fr + rng.uniform(0.0, 0.15)
    wl = rag() if robbed == "both" or (robbed == "one" and side == "l") else 0.0
    wr = rag() if robbed == "both" or (robbed == "one" and side == "r") else 0.0
    st = dict(robbed=robbed, side=side, frame=fr, kind=o.get("kind", "okno"), orig=o)
    if t["lintel"] == "oblouk":
        st.update(x0=o["x0"], x1=o["x1"], sill=o["sill"], top=o["top"], wl=wl, wr=wr,
                  jamb_h=min(FRAME_REACH, o["top"] - (o["x1"] - o["x0"]) / 2) if robbed != "none" else 0.0,
                  lintel_lost=(robbed == "both" and not o.get("protect", False)))
    else:
        drop = 0.3 if robbed == "both" and o["sill"] > 0 else 0.0     # vylamany parapet
        st.update(x0=o["x0"] - wl, x1=o["x1"] + wr, sill=max(0.0, o["sill"] - drop), top=o["top"], wl=wl, wr=wr, jamb_h=0.0,
                  # kamenne nadprazi spadne jen kdyz chybi obe osteni; drevene shnije vzdy
                  lintel_lost=(t["lintel"] == "drevo") or robbed == "both" or o.get("lintel_lost", False))
    return st

def wall_profile(L, H0, keep=None, corners=(), openings=(), breaches=(), seed=1, step=0.25,
                 corner_strength=0.2, mid=0.88, jag=0.45, course=0.3, protect=(),
                 access=0.3, access_points=(), weather=WEATHER, robbing=ROBBING, reach=REACH, states_out=None):
    """Vrati x (m) a dochovanou vysku h(x).  'keep' se uz nepouziva (zachovano kvuli kompatibilite).
    states_out: seznam, do ktereho se pripisi stavy otvoru (opening_state)."""
    rng = np.random.default_rng(seed)
    x = np.arange(0, L + 1e-6, step)
    # dostupnost a(x) + mistni zvyseni u bran a dveri (pouziva se pro otvory i rozebirani)
    a = np.full_like(x, access, dtype=float)
    for ap in access_points:
        a += ACCESS_BOOST * np.exp(-((x - ap) / ACCESS_RADIUS) ** 2)
    a = sm(np.clip(a, 0, 1), 9)
    orng = np.random.default_rng(seed + 1000)
    states = [opening_state(o, float(np.interp(0.5 * (o["x0"] + o["x1"]), x, a)), orng, reach) for o in openings]
    if states_out is not None: states_out.extend(states)
    # --- 1) prirodni rozpad (mirny) ---
    cs = np.array(sorted(set([0.0, L, *corners])))
    dc = np.min(np.abs(x[:, None] - cs[None, :]), axis=1)
    span = np.max(np.diff(cs)) if len(cs) > 1 else L
    t = np.clip(dc / max(1.5, min(6.0, span / 3)), 0, 1)
    prof = 1.0 - (1.0 - mid) * (0.5 - 0.5 * np.cos(np.pi * t))
    h = H0 * weather * prof * (1 + corner_strength * (1 - t)) / (1 + corner_strength)
    n = sm(rng.standard_normal(len(x)), 7)
    h = h + jag * n * 1.6
    for o in states:
        if o["lintel_lost"]:
            c = 0.5 * (o["x0"] + o["x1"]); w = 0.5 * (o["x1"] - o["x0"])
            v = o["top"] - 0.3 + np.maximum(0, np.abs(x - c) - w) * np.tan(np.radians(57))
            h = np.minimum(h, np.maximum(v, o["top"] - 0.3))
    # pruloomy (zadane rucne) pred rozebiranim -> nizka mista se rozebiraji dal
    for b in breaches:
        c = 0.5 * (b["x0"] + b["x1"]); w = 0.5 * (b["x1"] - b["x0"])
        v = b["floor"] + np.maximum(0, np.abs(x - c) - w) * 1.0
        h = np.minimum(h, v)
    # --- 2) aktivni rozebirani podle dostupnosti A VYSKY ---
    # rychlost rozebirani dh/dt = -ROBBING * a * min(1, REACH / h):
    #   co je do dosahu (REACH, z terenu / suti / zebriku) se bere plnou rychlosti,
    #   vysoka zed se rozebira pomalu (nahore se spatne pracuje) - dokud nezeslabne pod dosah
    A = robbing * a; R = reach; h0 = np.maximum(h, 0.0)
    low = h0 <= R
    t1 = np.where(low, 0.0, (h0 ** 2 - R ** 2) / (2 * R * np.maximum(A, 1e-6)))
    h_hi = np.sqrt(np.maximum(h0 ** 2 - 2 * R * A, 0))
    h_rob = np.where(low, h0 - A, np.where(t1 >= 1, h_hi, R - A * (1 - t1)))
    work = sm(rng.standard_normal(len(x)), 15) * 0.5 * a      # rozebirani po delsich usecich
    h = np.where(h_rob < h, h_rob + work, h)
    for x0, x1, hm in protect:
        m = (x >= x0) & (x <= x1); h[m] = np.maximum(h[m], hm)
    h = np.clip(h, 0.3, H0)
    h = np.floor(h / course) * course
    return x, h
