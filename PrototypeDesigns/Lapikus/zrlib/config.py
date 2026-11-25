"""zrlib.config - spolecna nastaveni vzhledu a meshi pro 03 (zricenina) i 05 (stavby):
tagy, materialy, zaoblene kameny, drevo, fyzika volnych kamenu. Uprav tady (driv nahore v build_ruin_blocks.py)."""

RUIN_TAG = "Zricenina_Ruin"                      # tag actoru zriceniny 03_ruin
CONSTR_TAG = "Zricenina_Stavby"                  # tag actoru staveb 05_constructions
FURN_TAG = "Zricenina_Vybaveni"                  # tag actoru vybaveni 06_furnishing (prenosne props)
# etapy stavby (05): kazdy dilec stavby s etapami patri do jedne sady; actor sady ma tag STAGE_TAG + jmeno sady.
# Prepnuti ve hre = zobrazit / skryt (i kolizi) actory podle tagu: etapa 1 = base + site, etapa 2 = base + final.
STAGE_TAG = "stage:"
STAGES = ("base",    # postaveno uz v etape 1 a zustava (v etape 2 se nic z toho neskryva)
          "final",   # dostavba: pribude v etape 2
          "site")    # staveniste: naradi, zebriky, kozy, vzpery, hromady materialu - jen v etape 1
CUBE_MESH = "/Engine/BasicShapes/Cube.Cube"
# --- materialy: None = skript si sam vytvori M_RuinStone + MI_RuinFace/Core/Frame v MAT_DIR (textury ze StarterContent);
#     nebo cesta k vlastnimu materialu, napr. "/Game/Megascans/.../MI_Rock.MI_Rock"
MAT_FACE  = None                         # lic (lomove kameny)
MAT_CORE  = None                         # jadro (lom + malta)
MAT_FRAME = None                         # osteni, oblouky (opracovany kamen)
MAT_CROWN = None                         # koruna zdi: odkryte horni kameny (vic zvetrale, svetlejsi, s nadechem lisejniku)
CROWN_WEATHER = True                     # odkryte kameny koruny = zvetrale tvary (SM_RuinStone_W_*) + material MI_RuinCrown
MAT_DIR   = "/Game/Skvt/Lapikus/Ruin/Materials"
MAT_GRAYBOX = "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray.MI_PrototypeGrid_Gray"   # graybox (cat "graybox": Cube, overeni meritka)
# --- vlastni procedurni textury (tools/textures/gen_textures.py -> textures/*.png v koreni; skript je sam naimportuje)
TEX_SRC = "textures"
TEX_DIR = "/Game/Skvt/Lapikus/Ruin/Textures"
TEX_VERSION = 4                          # vyssi nez v projektu -> textury se naimportuji znovu (po zmene gen_textures.py)
TEX_FILES = {"T_Ruin%s_%s" % (t, k): ("color" if k == "D" else "normal")
             for t in ("Bark", "EndGrain", "Rope", "Wattle", "Daub", "Canvas", "Iron", "IronClean", "Leather", "Charcoal", "Water", "Straw", "Wool") for k in "DN"}
TEX_FILES["T_RuinCanvasMacro_D"] = "color"         # velke skvrny plachty (M_RuinCloth)
CLOTH_MACRO = TEX_DIR + "/T_RuinCanvasMacro_D"
TEXTURES = {   # kandidati (BaseColor, Normal) - pouzije se prvni existujici
    "bark":     [(TEX_DIR + "/T_RuinBark_D", TEX_DIR + "/T_RuinBark_N")],
    "endgrain": [(TEX_DIR + "/T_RuinEndGrain_D", TEX_DIR + "/T_RuinEndGrain_N")],
    "rope":     [(TEX_DIR + "/T_RuinRope_D", TEX_DIR + "/T_RuinRope_N")],
    "wattle":   [(TEX_DIR + "/T_RuinWattle_D", TEX_DIR + "/T_RuinWattle_N")],
    "daub":     [(TEX_DIR + "/T_RuinDaub_D", TEX_DIR + "/T_RuinDaub_N")],
    "chinking": [(TEX_DIR + "/T_RuinDaub_D", TEX_DIR + "/T_RuinDaub_N")],       # vypln spar srubu = mazanina, jiny tint
    "canvas":   [(TEX_DIR + "/T_RuinCanvas_D", TEX_DIR + "/T_RuinCanvas_N")],
    "sackcloth": [(TEX_DIR + "/T_RuinCanvas_D", TEX_DIR + "/T_RuinCanvas_N")],   # vak: stejne platno, jiny tint a vic skvrn
    "iron":     [(TEX_DIR + "/T_RuinIron_D", TEX_DIR + "/T_RuinIron_N")],              # s patinou rzi
    "ironclean": [(TEX_DIR + "/T_RuinIronClean_D", TEX_DIR + "/T_RuinIronClean_N")],   # bez rzi (naradi, kovadlina)
    "leather":  [(TEX_DIR + "/T_RuinLeather_D", TEX_DIR + "/T_RuinLeather_N")],
    "charcoal": [(TEX_DIR + "/T_RuinCharcoal_D", TEX_DIR + "/T_RuinCharcoal_N")],
    "water":    [(TEX_DIR + "/T_RuinWater_D", TEX_DIR + "/T_RuinWater_N")],
    "straw":    [(TEX_DIR + "/T_RuinStraw_D", TEX_DIR + "/T_RuinStraw_N")],
    "wool":     [(TEX_DIR + "/T_RuinWool_D", TEX_DIR + "/T_RuinWool_N")],
    "sandstone": [("/Game/StarterContent/Textures/T_Rock_Sandstone_D", "/Game/StarterContent/Textures/T_Rock_Sandstone_N")],
    "wood_peeled": [("/Game/StarterContent/Textures/T_Wood_Pine_D", "/Game/StarterContent/Textures/T_Wood_Pine_N"),
                    ("/Game/StarterContent/Textures/T_Wood_Oak_D", "/Game/StarterContent/Textures/T_Wood_Oak_N")],
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
    # cerstve loupana kulatina (etapa 1): svetle nazloutle drevo, polomatne
    "wood_peeled": dict(TintA=(0.80, 0.64, 0.42), TintB=(0.98, 0.82, 0.58), Tiling=1.0, Roughness=0.85),
    # smrkova kura (slot Bark kulatiny): sedohneda az cervenohneda, matna; dlazdice textury 0,5 m -> Tiling 2
    "bark":     dict(TintA=(0.20, 0.14, 0.10), TintB=(0.32, 0.25, 0.19), Tiling=2.0, Roughness=0.95),
    # cela (slot EndGrain): svetle okrove, letokruhy z textury; UV polarni (v = vzdalenost od stredu v m), dlazdice 0,5 m
    "endgrain": dict(TintA=(0.62, 0.48, 0.30), TintB=(0.82, 0.66, 0.44), Tiling=2.0, Roughness=0.9),
    # konopne lano: svetle bezove; dlazdice 0,25 m (UV lana v = obvod * 0,25) -> Tiling 4
    "rope":     dict(TintA=(0.55, 0.45, 0.30), TintB=(0.72, 0.60, 0.42), Tiling=4.0, Roughness=0.95),
    # prouti (vyplet, kde opadala hlina): sedohnede pruty s kurou
    "wattle":   dict(TintA=(0.28, 0.22, 0.15), TintB=(0.42, 0.34, 0.24), Tiling=2.0, Roughness=0.95),
    # mazanina: svetla okrova hlina se slamou
    "daub":     dict(TintA=(0.55, 0.45, 0.32), TintB=(0.70, 0.58, 0.43), Tiling=2.0, Roughness=0.97),
    # vypln spar srubu: tmavsi hlina s mechem
    "chinking": dict(TintA=(0.24, 0.24, 0.15), TintB=(0.36, 0.34, 0.22), Tiling=4.0, Roughness=1.0),
    # lnene platno (M_RuinCloth, oboustranne): zasedle, skvrny; WindAmount = pohyb ve vetru v cm (0 = staticke)
    "canvas":   dict(TintA=(0.60, 0.56, 0.48), TintB=(0.74, 0.70, 0.61), Tiling=4.0, Roughness=0.9,
                     WindAmount=0.0, WindSpeed=0.6, WindScale=0.01, MacroAmount=0.6, MacroTiling=0.25),
    # pouzivany vak (M_RuinCloth): zazloutle hrube platno, husti skvrny (makro dlazdice 0,4 m), zaprasene
    "sackcloth": dict(TintA=(0.60, 0.51, 0.34), TintB=(0.75, 0.65, 0.45), Tiling=4.0, Roughness=0.95,
                      WindAmount=0.0, WindSpeed=0.6, WindScale=0.01, MacroAmount=1.0, MacroTiling=2.5),
    # props (barva zeleza a kuze je v texture -> tint skoro bily); Metallic = kovovy lesk (parametr M_RuinStone, jinak 0)
    "iron":     dict(TintA=(0.85, 0.85, 0.85), TintB=(1.0, 1.0, 1.0), Tiling=2.0, Roughness=0.7, Metallic=0.5),    # s patinou rzi (kovani, obruce, pruty)
    "ironclean": dict(TintA=(0.85, 0.85, 0.85), TintB=(1.0, 1.0, 1.0), Tiling=2.0, Roughness=0.5, Metallic=0.8),   # bez rzi (naradi, kovadlina)
    "leather":  dict(TintA=(0.80, 0.80, 0.80), TintB=(1.0, 1.0, 1.0), Tiling=2.0, Roughness=0.75),
    "sandstone": dict(TintA=(0.75, 0.68, 0.55), TintB=(0.90, 0.82, 0.68), Tiling=1.0, Roughness=0.95),     # brusny kotouc
    "water":    dict(TintA=(0.05, 0.07, 0.08), TintB=(0.06, 0.08, 0.09), Tiling=1.0, Roughness=0.05),
    "charcoal": dict(TintA=(0.035, 0.035, 0.038), TintB=(0.07, 0.07, 0.075), Tiling=2.0, Roughness=0.8),   # tmavost z tintu, textura je jen detail
    "straw":    dict(TintA=(0.85, 0.85, 0.85), TintB=(1.0, 1.0, 1.0), Tiling=2.0, Roughness=0.9),      # slama v luzku (barva v texture)
    "wool":     dict(TintA=(0.85, 0.85, 0.85), TintB=(1.0, 1.0, 1.0), Tiling=2.0, Roughness=1.0),      # houne, nebarvena vlna
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
    "wood_peeled": dict(TopTint=(1.05, 1.03, 0.98), TopStart=0.6, TopSharp=3.0, TopAmount=0.2),
    "bark":     dict(TopTint=(1.15, 1.20, 1.05), TopStart=0.55, TopSharp=3.0, TopAmount=0.3),    # vrch kury: prach, lisejnik
    "endgrain": dict(TopTint=(1.10, 1.08, 1.02), TopStart=0.6, TopSharp=3.0, TopAmount=0.2),
    "rope":     dict(TopTint=(1.05, 1.05, 1.00), TopStart=0.6, TopSharp=3.0, TopAmount=0.2),
    "wattle":   dict(TopTint=(1.10, 1.12, 1.02), TopStart=0.6, TopSharp=3.0, TopAmount=0.25),
    "daub":     dict(TopTint=(1.08, 1.06, 1.00), TopStart=0.55, TopSharp=3.0, TopAmount=0.3),     # vrch vymyty destem
    "chinking": dict(TopTint=(0.90, 1.05, 0.80), TopStart=0.5, TopSharp=3.0, TopAmount=0.4),      # mech nahore
    "canvas":   dict(TopTint=(1.05, 1.05, 1.00), TopStart=0.6, TopSharp=3.0, TopAmount=0.25),
    "sackcloth": dict(TopTint=(1.08, 1.05, 0.96), TopStart=0.5, TopSharp=2.5, TopAmount=0.4),       # vrch zapraseny
    "iron":     dict(TopTint=(1.10, 1.05, 1.00), TopStart=0.6, TopSharp=3.0, TopAmount=0.15),
    "ironclean": dict(TopTint=(1.05, 1.05, 1.05), TopStart=0.6, TopSharp=3.0, TopAmount=0.1),
    "leather":  dict(TopTint=(1.10, 1.08, 1.05), TopStart=0.6, TopSharp=3.0, TopAmount=0.2),
    "sandstone": dict(TopTint=(1.05, 1.05, 1.00), TopStart=0.6, TopSharp=3.0, TopAmount=0.2),
    "water":    dict(TopTint=(1.0, 1.0, 1.0), TopStart=0.9, TopSharp=3.0, TopAmount=0.0),
    "charcoal": dict(TopTint=(1.0, 1.0, 1.0), TopStart=0.9, TopSharp=3.0, TopAmount=0.0),
    "straw":    dict(TopTint=(1.0, 1.0, 1.0), TopStart=0.9, TopSharp=3.0, TopAmount=0.0),
    "wool":     dict(TopTint=(1.0, 1.0, 1.0), TopStart=0.9, TopSharp=3.0, TopAmount=0.0),
}
MAT_VERSION = 10                         # vyssi nez v projektu -> skript prestavi graf M_RuinStone a doplni parametry MI_*
                                         # (tinty MI_RuinFace/Frame zustanou, jak je mas; MAT_RESET viz nize)
MAT_RESET = {"crown": 2, "core": 3, "frame": 4, "wood_tar": 6, "charcoal": 9, "iron": 10}      # MI starsi nez tato verze dostane znovu tint a texturu z MAT_LOOK / TEXTURES
# --- knihovni meshe (tools/meshes/gen_meshes.py -> meshes/<kategorie>/*.obj v koreni vedle zrlib; skript je sam naimportuje)
USE_STONE_MESHES = True                  # False = vsude kostky (Cube) jako drive
# OBJ se zapisuje rovnou v osach UE (mesh_common.obj_v), asset stoji spravne i v Content Browseru.
MESH_AXES = 10                           # verze importu meshi: mesh importovany se starsi se naimportuje znovu, at je
                                         # v STONE_MESH_VERSION cokoliv. 1 = OBJ Y-up (v UE naležato, pri stavbe se otacel),
                                         # 2 = osy UE, ale lice naruby, 3 = hromadny import (nektere meshe s poskozenymi
                                         # vykreslovacimi daty), 4 = import po jednom (poskozena data ale UE vzal z cache
                                         # DDC, protoze OBJ byly stejne), 5 = OBJ s presnosti 0,1 mm (nova data, cista cache),
                                         # 6 = po importu plne prestaveni meshe (Interchange "fast build" nechava v UE
                                         # neinicializovane bounds vykreslovacich dat -> nahodne NaN), 7 = prestaveni
                                         # s kontrolou bounds (kontrola NaN nepozna, build byl porad fast), 8 = po importu
                                         # build z mesh description s fast_build=False (cache vratila poskozena data),
                                         # 9 = import do docasneho assetu, cil se stavi jen radne (ue_assets._import_one),
                                         # 10 = cil s priznakem bDoFastBuild se smaze a vytvori znovu + novy klic cache
                                         # (BUILD_CFG); pricina NaN = priznak v assetech kamenu a poskozena cache
MESH_SRC  = "meshes"                     # slozka s OBJ v koreni, podslozky podle kategorie (stone, wood, ...)
MESH_ROOT = "/Game/Skvt/Lapikus/Ruin"
MESH_DIRS = {"stone": "Stones",          # kategorie (= podslozka meshes/<kategorie>, CATEGORIES v gen_meshes.py)
             "wood":  "Wood",            #   -> slozka v UE MESH_ROOT/<slozka>
             "wattle": "Wattle",
             "textile": "Textile",
             "props": "Props"}
STONE_DIR = MESH_ROOT + "/" + MESH_DIRS["stone"]
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
# kulatina (tools/meshes/mesh_log.py): prefix -> (jmenovity rozmer delka, sirka, vyska v cm = NOMINAL v mesh_log.py, varianty,
# sloty v poradi v OBJ). Delka podel sx dilce (svisly kul / sloup = pitch 90).
# Sloty: wood = material podle upravy dilce (cat), ostatni = SLOT_MI.
ROUND_MESHES = {
    "SM_RuinLog":        ((100.0, 20.0, 20.0), "ABC", ("wood", "endgrain")),   # loupana kulatina
    "SM_RuinLogBark":    ((100.0, 20.0, 20.0), "ABC", ("wood", "endgrain", "bark")),   # kulatina s kurou
    "SM_RuinLogPeeling": ((100.0, 20.0, 20.0), "AB", ("wood", "endgrain", "bark")),    # rozpracovana: nahore (+Z) castecne oloupana
    "SM_RuinPole":       ((100.0, 8.0, 8.0), "ABC", ("wood", "endgrain")),     # loupana tyc
    "SM_RuinPoleBark":   ((100.0, 8.0, 8.0), "ABC", ("wood", "endgrain", "bark")),     # tyc s kurou
    "SM_RuinStake":      ((200.0, 20.0, 20.0), "ABC", ("wood", "endgrain", "bark")),   # kul s kurou, zaseknuta spicka na +X
    "SM_RuinStakeSmall": ((160.0, 7.0, 7.0), "AB", ("wood", "endgrain")),      # loupany kul, spicky na obou koncich
    "SM_RuinForkHead":   ((45.0, 30.0, 12.0), "AB", ("wood", "endgrain", "bark")),     # hlava rozsochy: kmen na -X, vidlice na +X, ramena v rovine XY
    "SM_RuinGutter":     ((100.0, 20.0, 11.0), "AB", ("wood", "endgrain")),    # loupany zlab: rez nahore (+Z), vydlabany
    "SM_RuinGutterBark": ((100.0, 20.0, 11.0), "AB", ("wood", "endgrain", "bark")),    # zlab s kurou zvenku
}
ROUND_SHAPES = {   # Stone.shape -> (prefix loupany, prefix s kurou); None = tvar existuje jen v druhe variante
    "round":  ("SM_RuinLog", "SM_RuinLogBark"),          # Pole / PoleBark, kdyz prumer <= POLE_MAX_D
    "stake":  ("SM_RuinStake", "SM_RuinStake"),
    "peeling": ("SM_RuinLogPeeling", "SM_RuinLogPeeling"),   # rozpracovana kulatina na kozach (oloupana strana nahoru: roll 0)
    "stake2": ("SM_RuinStakeSmall", "SM_RuinStakeSmall"),
    "fork":   ("SM_RuinForkHead", "SM_RuinForkHead"),
    "gutter": ("SM_RuinGutter", "SM_RuinGutterBark"),
}
POLE_MAX_D = 11.0                        # cm: tenci kulatina = tyc (SM_RuinPole*), jinak SM_RuinLog*
# materialy slotu (jmeno slotu v OBJ malymi pismeny -> MI na M_RuinStone); slot "wood" / neznamy = material dilce (cat).
# Klice jsou zaroven kategorie dilcu (Stone.cat = "rope", "daub" ... -> material slotu).
SLOT_MI = {"bark": "MI_RuinBark", "endgrain": "MI_RuinWood_EndGrain", "rope": "MI_RuinRope", "wattle": "MI_RuinWattle",
           "daub": "MI_RuinDaub", "chinking": "MI_RuinChinking", "iron": "MI_RuinIron", "ironclean": "MI_RuinIronClean", "leather": "MI_RuinLeather",
           "sandstone": "MI_RuinSandstone", "water": "MI_RuinWater", "charcoal": "MI_RuinCharcoal",
           "straw": "MI_RuinStraw", "wool": "MI_RuinWool",
           "face": "MI_RuinFace"}                # kamen lice zriceniny jako slot propu (kameny ohniste)
CLOTH_MI = {"canvas": "MI_RuinCanvas", "sackcloth": "MI_RuinSackcloth"}   # na M_RuinCloth: oboustranny, posun ve vetru (WindAmount, vychozi 0 = staticke)
CLOTH_VERSION = 2                        # vyssi nez v projektu -> skript prestavi graf M_RuinCloth
# dalsi knihovni meshe: prefix -> (jmenovity rozmer cm, varianty, kategorie (MESH_DIRS), sloty v poradi v OBJ, zakladni cat).
# Dilec: Stone.shape z LIB_SHAPES, Stone.cat = material slotu wood / jednoho slotu (napr. "rope", "canvas").
LIB_MESHES = {
    "SM_RuinBarkStrip":    ((160.0, 70.0, 9.0), "ABC", "wood", ("bark", "endgrain"), "bark"),       # pas kury (spodek = lyko)
    "SM_RuinWattlePanel":  ((100.0, 8.0, 100.0), "ABC", "wattle", ("daub", "wattle"), "daub"),      # dilec proutene steny XZ
    "SM_RuinSmokeHood":    ((140.0, 120.0, 100.0), "AB", "wattle", ("daub", "wattle"), "daub"),     # dymnik
    "SM_RuinChimney":      ((60.0, 60.0, 100.0), "AB", "wattle", ("daub", "wattle"), "daub"),       # komin
    "SM_RuinOvenDome":     ((140.0, 100.0, 40.0), "AB", "wattle", ("daub", "wattle"), "daub"),      # hlinena klenba pece
    "SM_RuinRope":         ((100.0, 1.5, 1.5), "AB", "textile", ("rope",), "rope"),                 # clanek lana
    "SM_RuinLashing":      ((7.0, 10.5, 10.5), "AB", "textile", ("rope",), "rope"),                 # ovazani tyce O 8 cm
    "SM_RuinCanvasSample": ((300.0, 221.6, 93.8), "A", "textile", ("canvas",), "canvas"),           # ukazka plachty
    # tvary na miru (mesh_textile.write_fitted: OBJ vystredeny, <mesh>.json = stred a rozmer v osach stavby; stavba bere rozmer z .json)
    "SM_RuinCanvasVez":      ((600.0, 430.0, 180.5), "A", "textile", ("canvas",), "canvas"),        # plachta pristresku na vezi
    "SM_RuinCanvasVezGable": ((2.0, 269.0, 111.8), "A", "textile", ("canvas",), "canvas"),          # stit plachty (svisly, X = tloustka)
    "SM_RuinCanvasTent":     ((246.0, 227.7, 189.6), "A", "textile", ("canvas",), "canvas"),        # plachta stanu do A na nadvori (X = hreben, +X vchod, +Y odhrnuta chlopen)
    # props (tools/meshes/mesh_props.py, kategorie props, v UE Ruin/Props); slot wood = material dilce (uprava dreva)
    "SM_RuinStump": ((53.6, 49.7, 46.7), "AB", "props", ('wood', 'endgrain', 'bark'), "wood"),
    "SM_RuinAnvil": ((59.1, 18.1, 24.3), "A", "props", ('ironclean',), "ironclean"),
    "SM_RuinBellows": ((210.4, 85.4, 139.0), "A", "props", ('wood', 'iron', 'leather'), "wood"),
    "SM_RuinBarrel": ((61.3, 61.2, 80.3), "A", "props", ('wood', 'endgrain', 'iron', 'water'), "wood"),
    "SM_RuinGrindstone": ((120.0, 86.0, 105.4), "A", "props", ('wood', 'iron', 'sandstone', 'water'), "wood"),
    "SM_RuinWorkbench": ((221.5, 85.9, 85.2), "A", "props", ('wood', 'iron'), "wood"),
    "SM_RuinTongs": ((50.2, 4.7, 2.8), "A", "props", ('ironclean',), "ironclean"),
    "SM_RuinHammer": ((4.3, 36.4, 11.0), "A", "props", ('wood', 'endgrain', 'ironclean'), "wood"),
    "SM_RuinChisel": ((20.6, 2.8, 2.8), "A", "props", ('ironclean',), "ironclean"),
    "SM_RuinNailHeader": ((25.0, 6.0, 1.5), "A", "props", ('ironclean',), "ironclean"),
    "SM_RuinCoalBox": ((80.6, 120.5, 80.0), "A", "props", ('wood', 'charcoal'), "wood"),                # bez vika
    "SM_RuinWoodpile": ((191.3, 65.0, 136.4), "A", "props", ('wood', 'endgrain', 'bark'), "wood"),
    "SM_RuinIronBars": ((103.2, 9.0, 3.8), "A", "props", ('iron',), "iron"),
    "SM_RuinBasket": ((43.5, 44.0, 36.5), "A", "props", ('wattle',), "wattle"),
    "SM_RuinLadder": ((450.4, 53.7, 7.8), "A", "props", ('wood', 'endgrain', 'bark'), "wood"),
    "SM_RuinGrindstoneTreadle": ((120.0, 86.0, 105.3), "A", "props", ('wood', 'endgrain', 'iron', 'sandstone', 'water'), "wood"),   # slapaci brus
    "SM_RuinStool": ((34.9, 33.4, 45.4), "A", "props", ('wood', 'endgrain'), "wood"),   # trinoha stolicka
    "SM_RuinCoalBoxLid": ((80.1, 120.3, 10.6), "A", "props", ('wood',), "wood"),         # volne viko truhliku (bez pantu)
    "SM_RuinMallet": ((9.5, 34.9, 14.0), "A", "props", ('wood', 'endgrain', 'ironclean'), "wood"),   # palice
    "SM_RuinNailHammer": ((3.0, 34.0, 10.5), "A", "props", ('wood', 'endgrain', 'ironclean'), "wood"),   # kladivo na hrebiky
    "SM_RuinBroadaxe": ((6.9, 72.1, 25.0), "A", "props", ('wood', 'endgrain', 'ironclean'), "wood"),   # sekera sirocina
    "SM_RuinAxe": ((4.6, 76.5, 18.7), "A", "props", ('wood', 'endgrain', 'ironclean'), "wood"),   # sekera na stipani
    "SM_RuinCrosscutSaw": ((150.9, 3.9, 28.3), "A", "props", ('wood', 'endgrain', 'ironclean'), "wood"),   # dvoumuzna pila
    "SM_RuinBed": ((200.2, 87.2, 61.9), "A", "props", ('wood', 'straw', 'wool'), "wood"),   # luzko, houne pres slamu
    "SM_RuinBedFolded": ((200.3, 80.3, 62.5), "A", "props", ('wood', 'straw', 'wool'), "wood"),   # luzko, houne slozena
    "SM_RuinTable": ((119.7, 69.5, 76.2), "A", "props", ('wood',), "wood"),   # stul
    "SM_RuinChest": ((95.4, 54.6, 51.2), "A", "props", ('wood', 'iron'), "wood"),   # truhla
    "SM_RuinShelf": ((100.2, 27.7, 89.6), "A", "props", ('wood',), "wood"),   # police
    "SM_RuinDoor": ((101.8, 9.3, 219.3), "A", "props", ('wood', 'iron'), "wood"),   # dvere 1,0 x 2,2
    "SM_RuinShutter": ((61.4, 8.4, 59.2), "A", "props", ('wood', 'endgrain', 'iron'), "wood"),   # okenice 60 x 60 (50 x 50 = skala 0,83)
    "SM_RuinOvenDoor": ((45.9, 8.6, 41.9), "A", "props", ('wood', 'endgrain', 'iron'), "wood"),   # poklop usti pece: plech v XZ, drevena rukojet na -Y (stred plechu +3.56 cm v Y od stredu)
    "SM_RuinCampBed": ((198.8, 76.2, 28.8), "A", "props", ('wood', 'endgrain', 'bark', 'straw', 'wool'), "wood"),   # luzko ve stanu (klady, tyce s kurou, slama, houne pres slamu), hlava na -X
    "SM_RuinCampBedFolded": ((200.0, 76.5, 32.1), "A", "props", ('wood', 'endgrain', 'bark', 'straw', 'wool'), "wood"),   # luzko ve stanu, houne slozena v nohach
    "SM_RuinChestSmall": ((59.3, 38.0, 31.7), "A", "props", ('wood', 'iron'), "wood"),   # truhlicka 55 x 35 x 32 (s drzadly 59,3), oko na zamek na -Y
    "SM_RuinBundle": ((76.0, 43.4, 22.5), "A", "props", ('rope', 'sackcloth'), "sackcloth"),   # vak z platna lezici na boku: dno -X, hrdlo stazene lanem +X, popruh na +Y
    "SM_RuinChestLocked": ((94.2, 54.2, 50.7), "A", "props", ('wood', 'endgrain', 'ironclean'), "wood"),   # kovana truhla na cennosti (Guesthouse): zamek na -Y, zavesy na +Y, klenute viko
    "SM_RuinBedLarge": ((250.2, 109.1, 95.0), "A", "props", ('wood', 'wool', 'canvas'), "wood"),   # postel hosta (Guesthouse): hlava na -X (celo 95 cm), slamnik a polstar v lnenem potahu, houne
    "SM_RuinCampfire": ((98.1, 98.8, 40.7), "A", "props", ('wood', 'endgrain', 'bark', 'charcoal', 'face'), "wood"),   # ohniste: kruh kamenu, uhli, polena se zuhelnatelymi stredy
    "SM_RuinArmorStand": ((60.1, 60.3, 175.0), "A", "props", ('wood', 'endgrain'), "wood"),   # stojan na brneni (Guesthouse): celo -Y, body pro brneni mesh_props.ARMOR_STAND_POINTS
}
LIB_SHAPES = {"bark_strip": "SM_RuinBarkStrip", "wattle_panel": "SM_RuinWattlePanel", "smoke_hood": "SM_RuinSmokeHood",
              "chimney": "SM_RuinChimney", "oven_dome": "SM_RuinOvenDome", "rope": "SM_RuinRope", "lashing": "SM_RuinLashing",
              "canvas_vez": "SM_RuinCanvasVez", "canvas_vez_gable": "SM_RuinCanvasVezGable",
              "canvas_tent": "SM_RuinCanvasTent",
              # props
              "stump": "SM_RuinStump",
              "anvil": "SM_RuinAnvil",
              "bellows": "SM_RuinBellows",
              "barrel": "SM_RuinBarrel",
              "grindstone": "SM_RuinGrindstone",
              "workbench": "SM_RuinWorkbench",
              "tongs": "SM_RuinTongs",
              "hammer": "SM_RuinHammer",
              "chisel": "SM_RuinChisel",
              "nail_header": "SM_RuinNailHeader",
              "coal_box": "SM_RuinCoalBox",
              "woodpile": "SM_RuinWoodpile",
              "iron_bars": "SM_RuinIronBars",
              "basket": "SM_RuinBasket",
              "ladder": "SM_RuinLadder",
              "grindstone_treadle": "SM_RuinGrindstoneTreadle",
              "stool": "SM_RuinStool",
              "coal_box_lid": "SM_RuinCoalBoxLid",
              "mallet": "SM_RuinMallet",
              "nail_hammer": "SM_RuinNailHammer",
              "broadaxe": "SM_RuinBroadaxe",
              "axe": "SM_RuinAxe",
              "crosscut_saw": "SM_RuinCrosscutSaw",
              "bed": "SM_RuinBed",
              "bed_folded": "SM_RuinBedFolded",
              "table": "SM_RuinTable",
              "chest": "SM_RuinChest",
              "shelf": "SM_RuinShelf",
              "door": "SM_RuinDoor",
              "shutter": "SM_RuinShutter",
              "oven_door": "SM_RuinOvenDoor",
              "camp_bed": "SM_RuinCampBed",
              "camp_bed_folded": "SM_RuinCampBedFolded",
              "chest_small": "SM_RuinChestSmall",
              "bundle": "SM_RuinBundle",
              "chest_locked": "SM_RuinChestLocked",
              "bed_large": "SM_RuinBedLarge",
              "armor_stand": "SM_RuinArmorStand",
              "campfire": "SM_RuinCampfire"}
STONE_MESH_VERSION = {"SM_RuinStone_W_": 2, "SM_RuinTimber_": 2, "SM_RuinPlank_": 2, "SM_RuinPost_": 2,
                      "SM_RuinLog": 1, "SM_RuinLogPeeling": 1, "SM_RuinPole": 1, "SM_RuinStake": 1, "SM_RuinForkHead": 1, "SM_RuinGutter": 2,       # Gutter 2: SM_RuinGutter je loupany, s kurou SM_RuinGutterBark
                      "SM_RuinBarkStrip": 1, "SM_RuinWattlePanel": 1, "SM_RuinSmokeHood": 1, "SM_RuinChimney": 1, "SM_RuinOvenDome": 1,
                      "SM_RuinRope": 1, "SM_RuinLashing": 1, "SM_RuinCanvasSample": 1, "SM_RuinCanvasVez": 1, "SM_RuinCanvasTent": 1,
                      "SM_RuinStump": 1, "SM_RuinAnvil": 3, "SM_RuinBellows": 5, "SM_RuinBarrel": 3, "SM_RuinGrindstone": 6, "SM_RuinWorkbench": 3, "SM_RuinTongs": 2, "SM_RuinHammer": 5, "SM_RuinChisel": 2, "SM_RuinNailHeader": 3, "SM_RuinCoalBox": 4, "SM_RuinWoodpile": 1, "SM_RuinIronBars": 2, "SM_RuinBasket": 3, "SM_RuinLadder": 1, "SM_RuinGrindstoneTreadle": 2, "SM_RuinStool": 1, "SM_RuinCoalBoxLid": 2, "SM_RuinMallet": 2, "SM_RuinNailHammer": 3, "SM_RuinBroadaxe": 3, "SM_RuinAxe": 3, "SM_RuinCrosscutSaw": 2, "SM_RuinBed": 1, "SM_RuinBedFolded": 1, "SM_RuinTable": 1, "SM_RuinChest": 1, "SM_RuinShelf": 1, "SM_RuinDoor": 1, "SM_RuinShutter": 1, "SM_RuinOvenDoor": 1, "SM_RuinCampBed": 1, "SM_RuinCampBedFolded": 1, "SM_RuinChestSmall": 1, "SM_RuinBundle": 2, "SM_RuinChestLocked": 1, "SM_RuinBedLarge": 2, "SM_RuinArmorStand": 3, "SM_RuinCampfire": 1}   # meshe s nizsi verzi v projektu se naimportuji znovu (prefix -> verze)
MAT_WOOD = ["/Game/StarterContent/Materials/M_Wood_Oak.M_Wood_Oak", "/Game/StarterContent/Materials/M_Wood_Pine.M_Wood_Pine"]   # zaloha, kdyz chybi textury dreva pro MI_RuinWood
MAT_WOOD_MI = None                       # vlastni material neosetreneho dreva (cesta); None = MI_RuinWood (vytvori skript)
# druhy dreva (Stone.cat): "wood" bez upravy (MI_RuinWood), "wood_tar" dehtovane, "wood_oil" morene olejem,
# "wood_blood" morene krvi, "wood_old" stare neosetrene (zasedle, zaprasene), "wood_peeled" cerstve loupana kulatina
WOOD_FINISH = {"raw": "wood", "tar": "wood_tar", "oil": "wood_oil", "blood": "wood_blood", "old": "wood_old", "peeled": "wood_peeled"}
WOOD_MI = {"wood": "MI_RuinWood", "wood_tar": "MI_RuinWood_Tar", "wood_oil": "MI_RuinWood_Oil",
           "wood_blood": "MI_RuinWood_Blood", "wood_old": "MI_RuinWood_Old", "wood_peeled": "MI_RuinWood_Peeled"}
# vychozi uprava podle casti stavby (lze prepsat v datech: floors[...]["finish"]); prkna jednoho patra: "planks_<patro>"
WOOD_FINISH_DEFAULT = dict(beams="tar", girder="tar", posts="tar", heads="tar", planks="raw", stairs="raw",
                           porch_beams="blood", porch_braces="blood", porch_posts="blood", porch_planks="blood", planks_2="old")            # osteni a oblouky: lehce srazene hrany
BLOCK_BP  = "/Game/Skvt/Lapikus/Ruin/BP_RuinBlocks"   # zalozni Blueprint s InstancedStaticMesh (kdyz nejde pridat komponentu)
