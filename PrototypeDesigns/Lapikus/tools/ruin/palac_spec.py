"""palac_spec.py - spolecne rozmery staveb v palaci (03 i 05): souradny ram palace a kovarna ve vychodni mistnosti.
Ram palace (navrhy new_designs/navrh_palac_*.md): pocatek = prvni bod Palac_J, s (m) podel Palac_J k vezi,
n (m) kolmo k severu (k Palac_S). Vysky v m nad terenem v miste stavby.
05 (gen_constructions.py): Palac_Kovarna_* (pristresek s krytinou, vyhen, stena, okap; pozdeji vybaveni).
03 (gen_layout.py -> ruin_edits): cela Palac_J zanorena o jednu radu kamene do zeme (J_SINK), u veze rozebrana koruna
(J_BREACH, aby ji komin kovarny presahoval) a kapsa pro vychodni pozednici kovarny v Palac_J (misto rohoveho sloupu);
sem prijde i snizeni koruny Palac_J u komina domu (navrh_palac_obydli_stred.md).
Kdyz se tu neco zmeni, pregeneruj gen_layout.py i gen_constructions.py a postav 03 (cast Palac) i 05."""
import math

WALL_J, WALL_S, TOWER = "Palac_J", "Palac_S", "Vez_Z"      # jizni a severni zed palace, zed veze na vychodnim konci

# --- uprava zriceniny (03), Jirka 15. 11. 2026: cela jizni zed palace posunuta po ose Z o jednu radu kamene niz (zanorena
#     do zeme, pocet rad se nemeni) a u veze rozebrana tak, aby ji komin kovarny presahoval
J_SINK = 0.31                    # m: vyska prvni cele rady nad terenem (16-47 cm) -> spary u zeme vypadaji stejne jako pred posunem;
                                 # posouva se vsechno ve zdi vcetne strilen a vyklenku (z_offset zdi)
J_DROP_ROWS = 0                  # 03 drop_rows (horni kameny kazde vrstvy pryc): pro Palac_J se nepouziva, parametr zustava v kodu
J_BREACH = dict(s0=29.6, s1=33.0, floor=6.1, slope_l=0.8)   # rozebrani koruny u veze (starsi zriceni, ne rovne zarovnani):
                                 # s (m), floor = m od paty zdi pred rozebiranim lice; koruna vychazi 4.0-5.2 m nad terenem
                                 # (stupne po radach), komin 5.5 m ji presahuje
J_PROTECT = dict(s0=30.3, s1=30.9, min=4.95)   # nad kapsou pozednice zed neklesne pod tuto vysku (m od paty) -> rada nad kapsou

# --- kovarna ve vychodni mistnosti (navrh_palac_kovarna.md): pristresek s pultovou strechou, spad k zapadu
K_POST_E_GAP = 0.10              # sloupy u veze: mezera mezi sloupem a licem veze (m)
K_POST_E = dict(post=0.20, n=(4.4, 6.2))                   # sloupy u veze (ctverec m, poloha n): mezi mechy a brusem a severni
                                                           # (rozsireni 16. 11. 2026); v koute u Palac_J
                                                           # sloup neni (stoji tam vyhen), pozednice je zapustena do zdi
K_PLATE_E = dict(sec=(0.20, 0.20), top=4.24, n1=6.4)       # vychodni pozednice: prurez, vrch (m), severni konec (n); 4.24 = spodek
                                                           # na spare rad Palac_J (4.04 m): kapsa se zarovnava na rady kamene
K_POCKET = dict(bear=0.30, side=0.03, under=0.02, over=0.02)   # kapsa v Palac_J pro jizni konec vychodni pozednice (03):
                                                           # ulozeni (m do zdi), vule po stranach, pod a nad tramem
K_WEST = 25.85                   # zapadni linie (sloupy, pozednice, stena z prouti): s (m); vychodne od vyklenku
                                 # strilny s = 25 (24.35-25.65), aby stena dosedla na plny lic Palac_J
K_POST_W = dict(post=0.18, n=(0.9, 3.55, 6.2))             # sloupy na zapade (rovnomerne, rozsireni o radu krokvi 16. 11. 2026)
K_PLATE_W = dict(sec=(0.18, 0.18), top=2.5, span=(0.74, 6.4))    # zapadni pozednice: vrch 2.5 m -> sklon 20 st.
K_RAFTER = dict(d=0.16, bark=False,                        # krokve: loupana kulatina O 16 cm
                n=(0.9, 1.8, 2.7, 3.6, 4.5, 5.4, 6.3),     # polohy n (m); 6.3 = rozsireni k severu (Jirka 16. 11. 2026)
                gap_tower=0.10,                            # horni konec o tolik m pred licem veze
                over=0.90,                                 # presah za zapadni pozednici: okap + kryti hranice dreva
                                                           # vyskladane zvenku podel zapadni steny (Jirka 15. 11. 2026)
                seat=0.03)                                 # osedlani: krokev zapustena do pozednic (m)
K_ROOF_N = (0.7, 6.6)            # pudorys strechy (krytiny): rozsah n
K_PAD = dict(l=0.36, w=0.36, h=0.14, sink=0.04)            # patni kamen pod sloupem (plochy kamen z rozvalin), zapusteny do zeme;
                                 # jen 36 cm: sloupy stoji 10 cm od lice veze a 11 cm od lice Palac_J
K_CHIMNEY = dict(s=30.0, n=1.35, w=0.5, top=5.5)           # komin: stred, strana, vrch (m); mezi krokvemi n = 0.9 a 1.8, mimo pozednici
# vyhen v koute mistnosti mezi Palac_J a vezi (Jirka 15. 11. 2026): kamenny stul, bocni zidka k mechum, ohniste pod kominem,
# dymnik; vyklenek strilny s = 29 hned vedle stolu = manipulacni prostor
K_FORGE = dict(len_s=1.0, len_n=1.2, h=0.75, course=0.25,         # stul: delka od lice veze, od lice Palac_J (m), vyska, vyska rady kamene
               gap_tower=0.02, gap_wall=0.02,                   # mezera kamene od lice veze a od lice Palac_J
               pit=0.4, daub=0.04)                              # ohniste (strana m), hlineny maz na stole
K_FORGE_WALL = dict(t=0.3, h=1.2, course=0.225,                   # bocni zidka severne od stolu (chrani mechy pred zarem): tloustka, vyska; stoji na zemi
                    hole=dict(w=0.2, z=(0.75, 0.975)))          # otvor pro vyfucnu v ose ohniste
K_HOOD = dict(size=(1.4, 1.2), bottom=1.8, h=1.0)               # dymnik: podel s (az k vezi) x podel n, spodni okraj, vyska
K_TRIMMER = dict(d=0.10, gap=0.03)                              # vymeny mezi krokvemi u komina: prumer, mezera od komina
K_HANGER = dict(d=0.05)                                         # zavesne tyce dymniku
K_ANVIL = (28.0, 1.4)            # kovadlina na spalku (16. 11. 2026 o 0,5 m dal od vyhne: byla prilis blizko)
K_ANVIL_GAP = (1.4, 1.6)         # kontrola: mezera hrana stolu vyhne - okraj spalku (m)
K_QUENCH_MAX = 1.7               # kontrola: kalici sud nejvys tak daleko od kovadliny i od vyhne (m)
# krytina pristresku (krok 2): skladba jako u ostrohu (late, prkna po spadu, listy pres spary), bez dehtu (nad vyhni)
K_ROOF = dict(lath=(0.05, 0.06), board_t=0.035, board_w=(0.22, 0.30), gap=0.015, batten=(0.10, 0.035),
              lath_step=0.9,                                    # nejvetsi rozestup lati po spadu (m, vodorovne)
              eave_over=0.10,                                   # prkna presahuji konec krokvi na okapu (okapova hrana s = 24.85, nad zlabem)
              top_gap=0.005, side_gap=0.035,                    # mezera prken od lice veze a od lice Palac_J (kameny koruny
                                                                # Palac_J v s = 27-29 lezi v urovni strechy a vystupuji z lice o 1-3 cm)
              hole_gap=0.03)                                    # mezera krytiny od komina (prostup)
K_FLASH = dict(t=0.035, h=0.25, gap=0.005)                      # lemovani: prkno na stojato na krytine u veze (gap od lice)
                                                                # a podel Palac_J (na hrane krajniho prkna)
# zapadni stena z prouti a hliny (krok 3, typ wattle_wall): v linii zapadnich sloupu, dilce SM_RuinWattlePanel mezi sloupy,
# na spojich dilcu kuly (zakryji spary dilcu, nahore presahuji)
K_WALL = dict(n=(0.70, 6.30), h=2.1, t=0.08, sink=0.03, gap=0.005,       # rozsah n, vyska nad terenem, tloustka, zapusteni, mezera od zdi
              tile=(1.1, 1.05),                                          # nejvetsi dilec (sirka, vyska m); dilec 1 x 1 m se skaluje
              stake=dict(d=0.09, over=0.06, sink=0.3))                   # kuly na spojich: prumer, presah nad stenu, v zemi
# okap (krok 3, typ gutter): vydlabany loupany kmen pod okapovou hranou, spad k severu, na rozsochach; konci nad sudem
K_GUTTER = dict(s=24.8, n=(0.72, 6.8), d=0.20,                           # osa, rozsah n (od lice Palac_J po sud), prumer
                drop=0.12,                                               # vrch zlabu na jiznim konci pod spodkem prken na okapove hrane
                fall=0.025,                                              # spad k severu (m/m); 2,5 % = zretelny sklon k sudu
                forks=(1.7, 4.0, 6.3), post_d=0.12, sink=0.4)            # rozsochy: polohy n (rovnomerne), prumer kulu, v zemi; jizni 1 m od
                                                                         # Palac_J (pruchod k vyklenku strilny s = 25), zlab k zdi volne presahuje
K_BARREL = (24.8, 6.8)           # sud na destovou vodu pod severnim koncem zlabu (SM_RuinBarrel, samostatny actor)
# vybaveni (krok 4, typ props): polohy v ramu palace (m), vsechno samostatne actory (rucni doladeni pres capture)
K_QUENCH = (28.3, 2.6)           # kalici sud mezi kovadlinou a vyhni (16. 11. 2026 dal od vyhne)
K_GRIND = (27.6, 5.4)            # stred ramu slapaciho brusu (ram podel s); slapadlo a sedatko k severu (otevrena strana, svetlo);
                                 # o 0,2 m severneji nez v navrhu -> mezi brusem a kalicim sudem pruchod 1,2 m k ponku
K_BENCH = dict(s=(26.05, 26.75), n=(2.6, 4.8))       # ponk: deska (o 0,1 m vychodneji nez navrh, patni kameny zapadnich sloupu)
K_COAL = dict(s=(26.05, 26.85), n=(0.8, 2.0), lid_shift=0.4)   # truhlik na uhli; viko volne, posunute k severu (pootevreny)
K_RACK = dict(s=(26.2, 28.0), z=1.5, gap=0.035)      # lista na naradi na jizni zdi: rozsah s, vyska stredu, mezera od lice
K_BARS = (27.15, 75.0)           # zelezne pruty oprene o jizni zed: s, sklon (st.)
K_NAILER = (27.35, 1.75, 0.55)   # hrebovnice na mensim spalku u kovadliny: s, n, vyska spalku
K_BELLOWS = dict(s=30.0, tip=2.0)                   # mechy: osa s (= ohniste), spicka vyfucny v otvoru bocni zidky (n)
K_LEVER = dict(d=0.06, p0=(30.0, 3.95, 1.75), p1=(28.55, 2.2, 1.6), rafter_n=2.7)   # paka mechu: konce (s, n, z), zavesena
                                 # na lane z krokve n = 2.7, s mechy spojena lanem
K_BASKET = (26.45, 6.0)          # kos s hrebiky u ponku
# drevo (Jirka 16. 11. 2026, navic proti navrhu): pod presahem strechy zvenku u zapadni steny, od kulu 1,5 m od Palac_J
# k severnimu okraji strechy (pruchod podel Palac_J k vyklenku strilny s = 25 zustava volny)
K_WOOD = dict(s=25.33, stake_gap=1.5, stake_d=0.10, stake_h=1.5, n1=6.4, parts=3, h=(1.0, 0.92, 0.97))   # n1: konec u sudu pod zlabem (pod okrajem strechy)


# --- dum posadky v prostredni mistnosti (navrh_palac_obydli_stred.md); vse v ramu palace (m). Etapy: sada actoru u kazde casti
#     (base = stoji uz v etape 1, final = dostavba, site = staveniste; zrlib/config.py STAGES)
D_PART_W, D_PART_E = "Palac_pricka_1", "Palac_pricka_2"    # pricky, na kterych stoji bocni steny domu
D_N_NORTH = 6.2                  # osa severni (srubove) steny: n
D_S_PART = 15.75                 # osa srubove pricky mezi sini a svetnici: s
D_FILL_TOP = 1.4                 # srovnani korun pricek kamenem (vcetne zazdeni jejich dveri): vrch m nad terenem
D_SILL = dict(w=0.45, h=0.45)    # podezdivka severni steny a pricky: sirka, vyska
D_DOOR_N = (13.8, 14.8)          # vchod v severni stene: s
D_DOOR_P = (3.3, 4.3)            # dvere v pricce: n
D_GAP = 0.02                     # mezera noveho zdiva od lice Palac_J
D_HEARTH = dict(s=(16.2, 17.6), len_n=1.4, h=0.5, course=0.25, pit=0.5, daub=0.04)   # zaklad ohniste u jizni zdi ve svetnici
D_CHIMNEY = dict(s=16.9, n=1.6, w=0.6, top=5.3)            # komin (final): stred, strana, vrch


def frame(walls):
    """ram palace z ruin_layout: origin (UE cm), s, n (jednotkove vektory), s_tower = s lice veze (m), n_in = n vnitrniho
    lice Palac_J (m), n_north = n vnitrniho lice Palac_S (m)"""
    W = {w["name"]: w for w in walls}
    a, b = W[WALL_J]["points"][0], W[WALL_J]["points"][-1]
    ux, uy = b[0] - a[0], b[1] - a[1]; ul = math.hypot(ux, uy); ux, uy = ux / ul, uy / ul
    nx, ny = -uy, ux
    q = W[WALL_S]["points"][0]
    if (q[0] - a[0]) * nx + (q[1] - a[1]) * ny < 0: nx, ny = -nx, -ny
    to_s = lambda p: ((p[0] - a[0]) * ux + (p[1] - a[1]) * uy) / 100
    to_n = lambda p: ((p[0] - a[0]) * nx + (p[1] - a[1]) * ny) / 100
    s_tower = min(to_s(p) for p in W[TOWER]["points"]) - W[TOWER]["thickness"] / 2
    n_north = min(to_n(p) for p in W[WALL_S]["points"]) - W[WALL_S]["thickness"] / 2
    return dict(origin=[a[0], a[1]], s=[round(ux, 5), round(uy, 5)], n=[round(nx, 5), round(ny, 5)],
                s_tower=round(s_tower, 3), n_in=round(W[WALL_J]["thickness"] / 2, 3), n_north=round(n_north, 3))


def kovarna(walls):
    """rozmery kovarny v ramu palace (m): linie sloupu a pozednic, krokve, pudorys strechy, komin"""
    F = frame(walls)
    s_e = round(F["s_tower"] - K_POST_E_GAP - K_POST_E["post"] / 2, 3)        # osa sloupu a pozednice u veze
    s_hi = round(F["s_tower"] - K_RAFTER["gap_tower"], 3)                     # horni konec krokvi
    s_lo = round(K_WEST - K_RAFTER["over"], 3)                                # okap
    slope = (K_PLATE_E["top"] - K_PLATE_W["top"]) / (s_e - K_WEST)
    plate_e = dict(sec=K_PLATE_E["sec"], top=K_PLATE_E["top"], span=(round(F["n_in"] - K_POCKET["bear"], 3), K_PLATE_E["n1"]))
    fn0 = round(F["n_in"] + K_FORGE["gap_wall"], 3); fn1 = round(F["n_in"] + K_FORGE["len_n"], 3)
    return dict(frame=F, s_east=s_e, s_west=K_WEST, s_hi=s_hi, s_lo=s_lo, slope=round(slope, 4),
                slope_deg=round(math.degrees(math.atan(slope)), 2),
                post_e=dict(K_POST_E), plate_e=plate_e, post_w=dict(K_POST_W), plate_w=dict(K_PLATE_W),
                rafter=dict(K_RAFTER), roof=dict(s=(s_lo, F["s_tower"]), n=K_ROOF_N), pad=dict(K_PAD),
                chimney=dict(K_CHIMNEY), anvil=K_ANVIL,
                forge=dict(s=(round(F["s_tower"] - K_FORGE["len_s"], 3), round(F["s_tower"] - K_FORGE["gap_tower"], 3)), n=(fn0, fn1),
                           h=K_FORGE["h"], course=K_FORGE["course"], pit=K_FORGE["pit"], daub=K_FORGE["daub"]),
                forge_wall=dict(K_FORGE_WALL, n=(fn1, round(fn1 + K_FORGE_WALL["t"], 3))), hood=dict(K_HOOD),
                trimmer=dict(K_TRIMMER), hanger=dict(K_HANGER),
                roof_cover=dict(K_ROOF), flashing=dict(K_FLASH), wall=dict(K_WALL), gutter=dict(K_GUTTER), barrel=K_BARREL)


def obydli(walls):
    """rozmery domu v ramu palace (m): osy a lice bocnich sten (z pricek zriceniny), podezdivky, zaklad ohniste, uklizeny pudorys"""
    F = frame(walls); W = {w["name"]: w for w in walls}; a = F["origin"]
    to_s = lambda p: ((p[0] - a[0]) * F["s"][0] + (p[1] - a[1]) * F["s"][1]) / 100
    sw = round(sum(to_s(p) for p in W[D_PART_W]["points"]) / len(W[D_PART_W]["points"]), 3); tw = W[D_PART_W]["thickness"]
    se = round(sum(to_s(p) for p in W[D_PART_E]["points"]) / len(W[D_PART_E]["points"]), 3); te = W[D_PART_E]["thickness"]
    n0 = round(F["n_in"] + D_GAP, 3); hw = D_SILL["w"] / 2
    return dict(frame=F, s_west=sw, s_east=se, n0=n0, n_north=D_N_NORTH, s_part=D_S_PART,
                fill_w=dict(s=(round(sw - tw / 2, 3), round(sw + tw / 2, 3)), n=(n0, round(D_N_NORTH + hw, 3)), top=D_FILL_TOP),
                fill_e=dict(s=(round(se - te / 2, 3), round(se + te / 2, 3)), n=(n0, round(D_N_NORTH + hw, 3)), top=D_FILL_TOP),
                sill_n=dict(s=(round(sw + tw / 2, 3), round(se - te / 2, 3)), n=(round(D_N_NORTH - hw, 3), round(D_N_NORTH + hw, 3)),
                            top=D_SILL["h"], door=D_DOOR_N),
                sill_p=dict(s=(round(D_S_PART - hw, 3), round(D_S_PART + hw, 3)), n=(n0, round(D_N_NORTH - hw, 3)), top=D_SILL["h"], door=D_DOOR_P),
                hearth=dict(s=D_HEARTH["s"], n=(n0, round(F["n_in"] + D_HEARTH["len_n"], 3)), h=D_HEARTH["h"], course=D_HEARTH["course"],
                            pit=D_HEARTH["pit"], daub=D_HEARTH["daub"]),
                chimney=dict(D_CHIMNEY),
                plan=dict(s=(round(sw - tw / 2, 3), round(se + te / 2, 3)), n=(F["n_in"], F["n_north"])))    # dum + zaprazi


def ruin_edits(walls):
    """upravy zriceniny (03) pro gen_layout.py: {zed: dict(z_offset, breaches, protect, openings)} - doplni se k datum zdi.
    Palac_J: cela zed o J_SINK niz (z_offset), rozebrana koruna u veze, kapsa ve vnitrnim lici pro vychodni pozednici
    kovarny. Vyska kapsy je od terenu na ose zdi (v datech rovina; pozednice se meri od terenu uprostred pristresku);
    z_offset posouva i otvory, proto je parapet kapsy o J_SINK vys."""
    K = kovarna(walls); w, h = K["plate_e"]["sec"]
    pocket = dict(kind="kapsa", s=K["s_east"], w=round(w + 2 * K_POCKET["side"], 3),
                  sill=round(K["plate_e"]["top"] - h - K_POCKET["under"] + J_SINK, 3), h=round(h + K_POCKET["under"] + K_POCKET["over"], 3),
                  _="vychodni pozednice kovarny (palac_spec.py)")
    ed = dict(z_offset=-J_SINK, breaches=[dict(J_BREACH, _="rozebrana koruna u veze: komin kovarny ji presahuje (palac_spec.py)")],
              protect=[dict(J_PROTECT)], openings=[pocket])
    if J_DROP_ROWS: ed["drop_rows"] = J_DROP_ROWS
    return {WALL_J: ed}


if __name__ == "__main__":
    import json, os, sys
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "03_ruin", "blocks", "ruin_layout.json")
    print(json.dumps(kovarna(json.load(open(p))["walls"]), indent=1))


def kovarna_vybaveni(walls):
    """vybaveni kovarny (typ props, zr_stavby/vybaveni.py) -> seznam dilcu v ramu palace (m); rozmery meshu = jmenovite
    (LIB_MESHES), odsazeni stredu bounding boxu od funkcniho stredu propu zmereno na meshich (mesh_props.py)"""
    K = kovarna(walls); n_in = K["frame"]["n_in"]; it = []
    # kovadlina na spalku (vrch 0,75 m), kalici sud, hrebovnice na mensim spalku
    a, c = K_ANVIL; h_anv = 24.3; h_st = 75.0 - h_anv
    it += [dict(id="Spalek", shape="stump", a=a, c=c, z=0.0, scale=(1.0, 1.0, h_st / 46.7)),
           dict(id="Kovadlina", shape="anvil", a=a, c=round(c + 0.065, 3), z=round(h_st / 100, 3), x=(0, 1)),   # roh k severu, telo na spalku
           dict(id="KaliciSud", shape="barrel", a=K_QUENCH[0], c=K_QUENCH[1], z=0.0),
           dict(id="Spalek2", shape="stump", a=K_NAILER[0], c=K_NAILER[1], z=0.0, scale=(0.7, 0.7, K_NAILER[2] * 100 / 46.7)),
           dict(id="Hrebovnice", shape="nail_header", a=K_NAILER[0], c=K_NAILER[1], z=K_NAILER[2], x=(0.6, 0.8))]
    # mechy: vyfucna (+X) k jihu do otvoru bocni zidky, spicka 105 cm od stredu bounding boxu; paka a lana
    B = K_BELLOWS; L = K_LEVER
    it += [dict(id="Mechy", shape="bellows", a=B["s"], c=round(B["tip"] + 1.052, 3), z=0.0, x=(0, -1))]
    t = (L["p0"][1] - L["rafter_n"]) / (L["p0"][1] - L["p1"][1]); pv = [round(L["p0"][i] + (L["p1"][i] - L["p0"][i]) * t, 3) for i in range(3)]
    it += [dict(id="Paka", shape="round", d=L["d"], p0=L["p0"], p1=L["p1"]),
           dict(id="Paka_Lano", shape="rope", cat="rope", d=0.015, p0=tuple(pv), p1=(pv[0], L["rafter_n"], "rafter")),
           dict(id="Mechy_Lano", shape="rope", cat="rope", d=0.015, p0=(B["s"], 4.03, 1.37), p1=L["p0"])]
    # slapaci brus (ram podel s, slapadlo +Y = k severu), stolicka u slapadla
    ga, gc = K_GRIND
    it += [dict(id="Brus", shape="grindstone_treadle", a=ga, c=round(gc + 0.07, 3), z=0.0, x=(-1, 0)),
           dict(id="Stolicka", shape="stool", a=round(ga - 0.30, 3), c=round(gc + 0.80, 3), z=0.0)]
    # ponk (sverak -Y k vychodu do mistnosti), truhlik s volnym vikem, kos
    bs, bn = K_BENCH["s"], K_BENCH["n"]; cs, cn = K_COAL["s"], K_COAL["n"]
    it += [dict(id="Ponk", shape="workbench", a=round(sum(bs) / 2 + 0.084, 3), c=round(sum(bn) / 2, 3), z=0.0, x=(0, -1)),
           dict(id="Truhlik", shape="coal_box", a=round(sum(cs) / 2, 3), c=round(sum(cn) / 2, 3), z=0.0),
           dict(id="Truhlik_Viko", shape="coal_box_lid", a=round(sum(cs) / 2, 3), c=round(sum(cn) / 2 + K_COAL["lid_shift"], 3), z=0.80),
           dict(id="Kos", shape="basket", a=K_BASKET[0], c=K_BASKET[1], z=0.0)]
    # lista na naradi na jizni zdi (na dvou kolicich ve sparach), naradi zavesene na jejim lici, pruty oprene o zed
    R = K_RACK; rn = round(n_in + R["gap"] + 0.0125, 4); fn = rn + 0.0125; z = R["z"]
    it += [dict(id="Lista", cat="wood", a=round(sum(R["s"]) / 2, 3), c=rn, zc=z, size=(round((R["s"][1] - R["s"][0]) * 100, 1), 10.0, 2.5), roll=90.0)]
    it += [dict(id="Kolik%d" % k, shape="round", d=0.03, p0=(sa, round(fn + 0.01, 3), z), p1=(sa, round(n_in - 0.05, 3), z))
           for k, sa in enumerate((R["s"][0] + 0.25, R["s"][1] - 0.25))]
    for k, (sa, kind) in enumerate(((26.35, "tongs"), (26.55, "tongs"), (26.9, "hammer"), (27.2, "hammer"), (27.55, "chisel"), (27.75, "chisel"))):
        if kind == "hammer":                                   # toporo dolu (roll -90: +Y dolu), hlava nahore u listy, ostri napric
            it.append(dict(id="Naradi%d" % k, shape=kind, a=sa, c=round(fn + 0.0215 + 0.005, 3), zc=round(z - 0.158 - 0.02, 3), x=(0, -1), roll=-90.0))
        else:                                                  # kleste a sekac svisle (pitch 90), tloustka podel n
            L_ = 50.2 if kind == "tongs" else 20.6
            it.append(dict(id="Naradi%d" % k, shape=kind, a=sa, c=round(fn + 0.014 + 0.005, 3), zc=round(z - L_ / 200, 3), x=(0, 1), pitch=90.0))
    bs_, ang = K_BARS; hl = 0.516 * math.cos(math.radians(ang))
    it.append(dict(id="Pruty", shape="iron_bars", a=bs_, c=round(n_in + 0.045 + hl, 3), zc=round(0.516 * math.sin(math.radians(ang)) + 0.02, 3),
                   x=(0, -1), pitch=ang))
    # drevo pod presahem: kul a hranice az k okraji strechy
    W = K_WOOD; n0 = round(n_in + W["stake_gap"], 3); m0 = n0 + W["stake_d"] / 2 + 0.01; seg = (W["n1"] - m0) / W["parts"]
    it.append(dict(id="Kul", shape="stake", d=W["stake_d"], bark=True, p0=(W["s"], n0, W["stake_h"]), p1=(W["s"], n0, -0.4)))
    for k in range(W["parts"]):
        it.append(dict(id="Drevo%d" % k, shape="woodpile", a=W["s"], c=round(m0 + seg * (k + 0.5), 3), z=0.0, x=(0, 1),
                       scale=(round(seg * 100 / 191.3, 4), 1.0, W["h"][k])))
    return it
