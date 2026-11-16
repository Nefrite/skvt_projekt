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
# vybaveni (krok 4, 06_furnishing, typ props): polohy v ramu palace (m), samostatne actory (rucni doladeni pres capture)
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
D_S_PART = 14.85                 # osa srubove pricky mezi sini a svetnici: s; zapadne od stredniho sloupu krovu (s = 15.3),
                                 # ktery tak stoji ve svetnici 23 cm od pricky (Jirka 16. 11. 2026: vetsi svetnice; driv 15.75)
D_FILL_TOP = 1.4                 # srovnani korun pricek kamenem (vcetne zazdeni jejich dveri): vrch m nad terenem
D_SILL = dict(w=0.45, h=0.45)    # podezdivka severni steny a pricky: sirka, vyska
D_DOOR_N = (13.4, 14.4)          # vchod v severni stene: s (posunuty s prickou, od jeji podezdivky 0.22 m; driv 13.8-14.8)
D_DOOR_P = (3.3, 4.3)            # dvere v pricce: n
D_GAP = 0.02                     # mezera noveho zdiva od lice Palac_J
# pec s nistejí u jizni zdi ve svetnici (Jirka 16. 11. 2026, misto otevreneho ohniste): kamenny sokl, na nem vzadu pec
# (kamenne zdi, hlinena klenba, usti k severu), vpredu nistej s zeleznou plotnou na zidkach; kour z pece sopouchem do dymniku.
# Osa s = uprostred mezi krokvemi 16.26 a 17.26 (komin 16 cm od obou); stred mezi sloupy 15.3 a 18.0 je 16.65.
D_OVEN = dict(s=16.76, w=1.6, len_n=1.6, h=0.6, course=0.3, daub=0.04,          # sokl: osa, sirka, hloubka od Palac_J, vyska
              body=dict(w=1.4, len_n=1.0, wall_t=0.22, wall_h=0.36, course=0.18, dome_h=0.34),   # pec: zdi na soklu, klenba
              mouth=dict(w=0.4),                                                # usti (vysoke jako zdi pece), pas a poklop ze zeleza
              plate=dict(s=(17.0, 17.56), n=(1.84, 2.26), h=0.22, cheek=0.10, t=0.012),   # plotna na vychodni strane nisteje
              flue=dict(n=1.56, w=0.28),                                        # sopouch z klenby za celem pece
              hood=dict(n=1.70, size=(1.6, 1.1), bottom=1.8, h=0.8))            # dymnik nad ustim a nistejí; komin v jeho ose
D_CHIMNEY = dict(s=16.76, n=1.70, w=0.5, top=5.3)          # komin (final): stred, strana, vrch; s = uprostred mezi krokvemi
                                                           # 16.26 a 17.26 (navrh 16.9 by zasahl do krokve)
# pruchod ze zaprazi domu na dvorek kovarny (03): posadka rozebrala Palac_pricka_2 severne od domu na kamen pro podezdivky;
# hruby pruchod az k zemi, po stranach zbytky zdi (je videt, ze tu zed byla)
D_PASS = dict(n=(6.9, 8.5), h=2.2, ragged=0.35)            # rozsah n (od rohu domu 0.45 m, od Palac_S 0.3 m), vylamane okraje


# krov domu (typ pult_roof, osa spadu n: od Palac_J k severu). Tri podpory krokvi: horni pozednice na sloupech u Palac_J,
# stredni vaznice na spalcich na bocnich stenach a pricce, vrchni trám severni srubove steny (ten patri ke srubu).
D_ROOF_S = (10.1, 21.4)          # delka pozednice a vaznice (s): pres obe bocni steny, at na nich lezi i stitove krokve
                                 # (navrh mel pozednici jen 10.9-20.6, stitove krokve by nahore visely)
D_PLATE = dict(n=0.85, top=4.03, sec=(0.20, 0.20), post=0.20,
               posts=(11.1, 13.0, 15.3, 18.0, 20.4),       # sloupy (s): mimo vyklenky strilen (13.35-14.65, 18.35-19.65) a ohniste;
                                                           # stredni v s = 15.3 (navrh 15.6 by stal v podezdivce a srubu pricky)
               joint=15.3)                                 # spoj dvou kusu nad strednim sloupem; vychodni kus = sada base
D_PURLIN = dict(n=4.4, sec=(0.20, 0.24), joint=D_S_PART, stub=0.20)   # stredni vaznice: spoj nad prickou, spalky (strana m) na stenach
D_RAFTER = dict(sec=(0.18, 0.22), count=12, s=(10.2, 21.3), n=(0.80, 6.8), seat=0.03)   # hranene krokve, presah 0.6 m za severni stenu;
                                 # horni konec 10 cm od lice Palac_J (kameny lice vystupuji az o 5 cm)
D_STAGE_S = 16.0                 # krokve s s >= teto hodnote (nad svetnici) stoji uz v etape 1 (base), ostatni final
D_PAD = dict(l=0.26, w=0.36, h=0.14, sink=0.04)            # patni kamen sloupu: l napric (k Palac_J zbyva 2 cm), w podel zdi
D_BRACE_LATHS = dict(n=(2.6, 5.3), s=(16.17, 21.4), lath=(0.05, 0.06))   # 2 rady lati na krokvich nad svetnici (zavetrovani, base)
# srub (typ log_wall): loupana kulatina v radach; rady severni steny do 1.4 m (vrch srovnanych pricek) a nad nim stejne
# jako na bocnich stenach. Bocni steny a pricka zacinaji a konci pultramem (prvni a posledni rada polovicni, hranena):
# jejich rady jsou tak o pul rady posunute proti severni stene a v narozich se stridaji jako u skutecneho srubu.
D_LOG = dict(top=2.5, rows_low=4, rows_up=5,               # vrch srubu; rady severni steny pod 1.4 m a nad nim
             lap=0.012, half_w=0.22,                       # kulatina je o tolik tlustsi nez rada (prekryv = zdi neprosvita); sirka pultramu
             over=0.30, jit=0.05,                          # presah zhlavi za osu krizici steny, nahodne +-
             west_base_rows=3)                             # sin: tolik rad severni steny stoji uz v etape 1 (vrch 1.16 m)
D_WINDOWS = (dict(s=(17.5, 18.1), z=(1.3, 2.0)),           # okenko svetnice (na rady: 1.40-2.06 m); uprostred steny svetnice
                                                           # (s = 14.97-20.6) a mezi krokvemi 17.26 a 18.27
             dict(s=(11.8, 12.3), z=(1.3, 1.9)))           # okenko sine (1.40-1.84 m)
D_DOOR_H = 2.2                   # vyska dveri (rada se vynecha, kdyz ma stred pod touto vyskou): vchod 2.28 m, dvere v pricce 2.17 m
D_GABLE = dict(t=0.035, board_w=(0.20, 0.28), lap=0.10, gap=0.02)   # prkenne stity: tloustka, sirka prken, prekryti vrchni rady
                                                           # srubu, mezera od lice srubu


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
                hearth=_obydli_pec(n0),
                chimney=dict(D_CHIMNEY), **_obydli_drevo(sw, se, n0),
                plan=dict(s=(round(sw - tw / 2, 3), round(se + te / 2, 3)), n=(F["n_in"], F["n_north"])))    # dum + zaprazi


def _obydli_pec(n0):
    """pec s nistejí (typ hearth) v ramu palace: sokl, zdi pece, klenba, kvadry (zelezo, uhli), sopouch, dymnik, komin"""
    O = D_OVEN; B = O["body"]; r = lambda v: round(v, 3)
    s0, s1 = r(O["s"] - O["w"] / 2), r(O["s"] + O["w"] / 2); n1 = r(n0 + O["len_n"])
    b0, b1 = r(O["s"] - B["w"] / 2), r(O["s"] + B["w"] / 2); bn1 = r(n0 + B["len_n"]); t = B["wall_t"]
    zb = r(O["h"] + O["daub"]); zw = r(zb + B["wall_h"]); zd = r(zw + B["dome_h"]); mw = O["mouth"]["w"] / 2
    walls = [dict(id="OW", a=[b0, r(b0 + t)], c=[n0, r(bn1 - t)], h=B["wall_h"], course=B["course"], base=zb),
             dict(id="OE", a=[r(b1 - t), b1], c=[n0, r(bn1 - t)], h=B["wall_h"], course=B["course"], base=zb),
             dict(id="OF", a=[b0, b1], c=[r(bn1 - t), bn1], h=B["wall_h"], course=B["course"], base=zb,
                  hole=dict(a=O["s"], w=O["mouth"]["w"], z=[0.0, B["wall_h"]]))]          # celo pece s ustim
    PL = O["plate"]; (p0, p1), (q0, q1) = PL["s"], PL["n"]; ck = PL["cheek"]
    walls += [dict(id="PW", a=[p0, r(p0 + ck)], c=[q0, q1], h=PL["h"], course=PL["h"], base=zb),      # zidky pod plotnou
              dict(id="PE", a=[r(p1 - ck), p1], c=[q0, q1], h=PL["h"], course=PL["h"], base=zb)]
    zp = r(zb + PL["h"])
    boxes = [dict(id="V", cat="charcoal", a=[r(b0 + t), r(b1 - t)], c=[r(n0 + 0.02), r(bn1 - t)], z=[zb, r(zw - 0.02)]),   # tmavy vnitrek pece
             dict(id="U", cat="charcoal", a=[r(p0 + ck), r(p1 - ck)], c=[r(q0 + 0.03), r(q1 - 0.03)], z=[zb, r(zb + 0.03)]),   # uhli pod plotnou
             dict(id="I0", cat="iron", top=True, a=[r(O["s"] - mw - 0.15), r(O["s"] + mw + 0.15)], c=[r(bn1 - t), r(bn1 + 0.01)], z=[r(zw - 0.015), zw]),   # pas nad ustim
             dict(id="I2", cat="iron", top=True, loose=True, a=[r(p0 - 0.01), r(p1 + 0.01)], c=[r(q0 - 0.01), r(q1 + 0.01)], z=[zp, r(zp + PL["t"])])]                    # plotna
    # poklop usti: samostatny actor (mesh SM_RuinOvenDoor 45,9 x 8,6 x 41,9 cm: plech + drevena rukojet), opreny o celo pece
    # zapadne od usti, rukojeti do mistnosti; stred plechu je 3,56 cm za stredem bounding boxu (lokalni Y = -n)
    props = [dict(id="Poklop", shape="oven_door", cat="wood", top=True, a=r((b0 + O["s"] - mw) / 2 - 0.01), c=r(bn1 + 0.012 + 0.0356),
                  zc=r(zb + 0.2095), size=[45.9, 8.6, 41.9])]
    H = O["hood"]; C = D_CHIMNEY
    return dict(s=(s0, s1), n=(n0, n1), h=O["h"], course=O["course"], daub=O["daub"], walls=walls,
                dome=dict(a=[b0, b1], c=[n0, bn1], z=[zw, zd]), boxes=boxes, props=props,
                flue=dict(a=O["s"], c=O["flue"]["n"], w=O["flue"]["w"], z=[r(zd - 0.08), r(H["bottom"] + H["h"] * 0.6)]),
                hood=dict(a=O["s"], c=H["n"], size=list(H["size"]), bottom=H["bottom"], h=H["h"]),
                chimney=dict(a=C["s"], c=C["n"], w=C["w"], top=C["top"]))


def _obydli_drevo(sw, se, n0):
    """krov a srub domu (m v ramu palace): podpory krokvi, krokve, rady a useky srubovych sten se sadami etap, stity"""
    slope = (D_PLATE["top"] - D_LOG["top"]) / (D_N_NORTH - D_PLATE["n"])
    r0, r1 = D_RAFTER["s"]; nr = D_RAFTER["count"]
    pos = [round(r0 + (r1 - r0) * i / (nr - 1), 3) for i in range(nr)]
    purlin_top = round(D_PLATE["top"] - slope * (D_PURLIN["n"] - D_PLATE["n"]), 3)
    # rady: severni stena od podezdivky po 1.4 m a dal po vrch; bocni steny od 1.4 m, pricka od podezdivky (pultramy na krajich)
    lo = [round(D_SILL["h"] + (D_FILL_TOP - D_SILL["h"]) * i / D_LOG["rows_low"], 4) for i in range(D_LOG["rows_low"])]
    up = [round(D_FILL_TOP + (D_LOG["top"] - D_FILL_TOP) * i / D_LOG["rows_up"], 4) for i in range(D_LOG["rows_up"] + 1)]
    z_n = lo + up; h_up = up[1] - up[0]; h_lo = lo[1] - lo[0]
    z_side = [up[0]] + [round(z + h_up / 2, 4) for z in up[:-1]] + [up[-1]]
    z_part = [lo[0]] + [round(z + h_lo / 2, 4) for z in lo] + z_side[1:]
    ov = D_LOG["over"]; nl = D_LOG["rows_low"]; top_n = len(z_n) - 2; wb = D_LOG["west_base_rows"]
    fw1, fe0 = round(sw + 0.4, 3), round(se - 0.4, 3)          # lice srovnanych pricek uvnitr domu (tloustka 0.8 m)
    door = lambda span: dict(span=list(span), z=[0.0, D_DOOR_H])
    walls_ = [
        dict(id="N", dir="a", at=D_N_NORTH, z=z_n, openings=[door(D_DOOR_N)] + [dict(span=list(w["s"]), z=list(w["z"])) for w in D_WINDOWS],
             segs=[dict(rows=[0, wb - 1], span=[round(fw1 + 0.03, 3), D_S_PART], stage="base"),              # sin: prvni rady uz v etape 1
                   dict(rows=[wb, nl - 1], span=[round(fw1 + 0.03, 3), D_S_PART], stage="final"),
                   dict(rows=[nl, top_n], span=[round(sw - ov - 0.15, 3), D_S_PART], free=[1, 0], stage="final"),   # nad priccou az za narozi
                   dict(rows=[0, nl - 1], span=[D_S_PART, round(fe0 - 0.03, 3)], stage="base"),              # svetnice: cela vyska v etape 1
                   dict(rows=[nl, top_n], span=[D_S_PART, round(se + ov + 0.15, 3)], free=[0, 1], stage="base")]),
        dict(id="P", dir="c", at=D_S_PART, z=z_part, half=[0, len(z_part) - 2], openings=[door(D_DOOR_P)],
             segs=[dict(rows=[0, len(z_part) - 2], span=[round(n0 + 0.02, 3), round(D_N_NORTH + ov, 3)], free=[0, 1], stage="base")]),
        dict(id="W", dir="c", at=sw, z=z_side, half=[0, len(z_side) - 2],
             segs=[dict(rows=[0, len(z_side) - 2], span=[round(n0 + 0.02, 3), round(D_N_NORTH + ov, 3)], free=[0, 1], stage="final")]),
        dict(id="E", dir="c", at=se, z=z_side, half=[0, len(z_side) - 2],
             segs=[dict(rows=[0, len(z_side) - 2], span=[round(n0 + 0.02, 3), round(D_N_NORTH + ov, 3)], free=[0, 1], stage="base")])]
    # prkenne stity nad srubem pod strechu (final): na vnejsim lici bocnich sten, u pricky na strane sine; vyrezy pro pozednici a vaznici
    g = D_GABLE; off = 0.12 + g["gap"] + g["t"] / 2
    cut = lambda n, sec, top: dict(c=[round(n - sec[0] / 2 - 0.01, 3), round(n + sec[0] / 2 + 0.01, 3)], z=[round(top - sec[1] - 0.01, 3), round(top + 0.01, 3)])
    cuts = [cut(D_PLATE["n"], D_PLATE["sec"], D_PLATE["top"]), cut(D_PURLIN["n"], D_PURLIN["sec"], purlin_top)]
    gables = [dict(id="GW", at=round(sw - off, 3), c=[n0, round(D_N_NORTH + 0.25, 3)]),
              dict(id="GE", at=round(se + off, 3), c=[n0, round(D_N_NORTH + 0.25, 3)]),
              dict(id="GP", at=round(D_S_PART - off, 3), c=[n0, round(D_N_NORTH - 0.13, 3)])]
    for q in gables: q.update(base=round(D_LOG["top"] - g["lap"], 3), t=g["t"], board_w=list(g["board_w"]), cuts=cuts, stage="final")
    return dict(
        roof=dict(slope=round(slope, 4), slope_deg=round(math.degrees(math.atan(slope)), 2), span=D_ROOF_S,
                  plate=dict(D_PLATE), purlin=dict(D_PURLIN, top=purlin_top,
                                                   stubs=[dict(c=sw, stage="final"), dict(c=D_S_PART, stage="base"), dict(c=se, stage="base")]),
                  north=dict(n=D_N_NORTH, top=D_LOG["top"], span=(round(sw - ov - 0.1, 3), round(se + ov + 0.1, 3))),
                  rafter=dict(D_RAFTER, pos=pos, stages=["base" if p >= D_STAGE_S else "final" for p in pos]),
                  pad=dict(D_PAD), brace_laths=dict(D_BRACE_LATHS)),
        log=dict(lap=D_LOG["lap"], half_w=D_LOG["half_w"], jit=D_LOG["jit"], walls=walls_, gables=gables),
        doors=dict(n=D_DOOR_N, p=D_DOOR_P, h=D_DOOR_H), windows=[dict(w) for w in D_WINDOWS])


def ruin_edits(walls):
    """upravy zriceniny (03) pro gen_layout.py: {zed: dict(z_offset, breaches, protect, openings)} - doplni se k datum zdi.
    Palac_pricka_2: hruby pruchod ze zaprazi domu na dvorek kovarny (D_PASS).
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
    # pruchod v Palac_pricka_2 (s zdi = n ramu palace: zed zacina na ose Palac_J)
    n0, n1 = D_PASS["n"]
    passage = dict(kind="prulom", s=round((n0 + n1) / 2, 3), w=round(n1 - n0, 3), sill=0, h=D_PASS["h"], ragged=D_PASS["ragged"],
                   _="pruchod ze zaprazi domu ke kovarne (palac_spec.py)")
    return {WALL_J: ed, D_PART_E: dict(openings=[passage])}


if __name__ == "__main__":
    import json, os, sys
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "03_ruin", "blocks", "ruin_layout.json")
    print(json.dumps(kovarna(json.load(open(p))["walls"]), indent=1))


def kovarna_kul(walls):
    """pevny kul zatluceny do zeme na zacatku hranice dreva (05, typ props) -> [dilec]; hranice sama je vybaveni (06)"""
    W = K_WOOD; n0 = round(kovarna(walls)["frame"]["n_in"] + W["stake_gap"], 3)
    return [dict(id="Kul", shape="stake", d=W["stake_d"], bark=True, p0=(W["s"], n0, W["stake_h"]), p1=(W["s"], n0, -0.4))]


def kovarna_vybaveni(walls):
    """prenosne vybaveni kovarny (06_furnishing, typ props, zr_stavby/vybaveni.py) -> seznam kusu v ramu palace (m); rozmery meshu = jmenovite
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
    for k in range(W["parts"]):
        it.append(dict(id="Drevo%d" % k, shape="woodpile", a=W["s"], c=round(m0 + seg * (k + 0.5), 3), z=0.0, x=(0, 1),
                       scale=(round(seg * 100 / 191.3, 4), 1.0, W["h"][k])))
    return it
