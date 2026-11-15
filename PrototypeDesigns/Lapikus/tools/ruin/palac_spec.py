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
K_POST_E = dict(post=0.20, n=(5.3,))                       # sloup u veze (ctverec m, poloha n): jen severni; v koute u Palac_J
                                                           # sloup neni (stoji tam vyhen), pozednice je zapustena do zdi
K_PLATE_E = dict(sec=(0.20, 0.20), top=4.24, n1=5.5)       # vychodni pozednice: prurez, vrch (m), severni konec (n); 4.24 = spodek
                                                           # na spare rad Palac_J (4.04 m): kapsa se zarovnava na rady kamene
K_POCKET = dict(bear=0.30, side=0.03, under=0.02, over=0.02)   # kapsa v Palac_J pro jizni konec vychodni pozednice (03):
                                                           # ulozeni (m do zdi), vule po stranach, pod a nad tramem
K_WEST = 25.85                   # zapadni linie (sloupy, pozednice, stena z prouti): s (m); vychodne od vyklenku
                                 # strilny s = 25 (24.35-25.65), aby stena dosedla na plny lic Palac_J
K_POST_W = dict(post=0.18, n=(0.9, 3.1, 5.3))              # sloupy na zapade
K_PLATE_W = dict(sec=(0.18, 0.18), top=2.5, span=(0.74, 5.5))    # zapadni pozednice: vrch 2.5 m -> sklon 20 st.
K_RAFTER = dict(d=0.16, bark=False,                        # krokve: loupana kulatina O 16 cm
                n=(0.9, 1.8, 2.7, 3.6, 4.5, 5.4),          # polohy n (m)
                gap_tower=0.10,                            # horni konec o tolik m pred licem veze
                over=0.90,                                 # presah za zapadni pozednici: okap + kryti hranice dreva
                                                           # vyskladane zvenku podel zapadni steny (Jirka 15. 11. 2026)
                seat=0.03)                                 # osedlani: krokev zapustena do pozednic (m)
K_ROOF_N = (0.7, 5.7)            # pudorys strechy (krytiny): rozsah n
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
K_ANVIL = (28.5, 1.4)            # kovadlina (pro kontrolu svetle vysky a vzdalenosti od vyhne)
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
K_WALL = dict(n=(0.70, 5.40), h=2.1, t=0.08, sink=0.03, gap=0.005,       # rozsah n, vyska nad terenem, tloustka, zapusteni, mezera od zdi
              tile=(1.1, 1.05),                                          # nejvetsi dilec (sirka, vyska m); dilec 1 x 1 m se skaluje
              stake=dict(d=0.09, over=0.06, sink=0.3))                   # kuly na spojich: prumer, presah nad stenu, v zemi
# okap (krok 3, typ gutter): vydlabany loupany kmen pod okapovou hranou, spad k severu, na rozsochach; konci nad sudem
K_GUTTER = dict(s=24.8, n=(0.72, 5.9), d=0.20,                           # osa, rozsah n (od lice Palac_J po sud), prumer
                drop=0.12,                                               # vrch zlabu na jiznim konci pod spodkem prken na okapove hrane
                fall=0.015,                                              # spad k severu (m/m)
                forks=(0.9, 3.1, 5.3), post_d=0.12, sink=0.4)            # rozsochy: polohy n (jako sloupy), prumer kulu, v zemi
K_BARREL = (24.8, 5.9)           # sud na destovou vodu pod severnim koncem zlabu (SM_RuinBarrel, samostatny actor)


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
