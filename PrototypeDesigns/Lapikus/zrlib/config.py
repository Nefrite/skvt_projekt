"""zrlib.config - spolecna nastaveni vzhledu a meshi pro 03 (zricenina) i 05 (stavby):
tagy, materialy, zaoblene kameny, drevo, fyzika volnych kamenu. Uprav tady (driv nahore v build_ruin_blocks.py)."""

RUIN_TAG = "Zricenina_Ruin"                      # tag actoru zriceniny 03_ruin
CONSTR_TAG = "Zricenina_Stavby"                  # tag actoru staveb 05_constructions
CUBE_MESH = "/Engine/BasicShapes/Cube.Cube"
# --- materialy: None = skript si sam vytvori M_RuinStone + MI_RuinFace/Core/Frame v MAT_DIR (textury ze StarterContent);
#     nebo cesta k vlastnimu materialu, napr. "/Game/Megascans/.../MI_Rock.MI_Rock"
MAT_FACE  = None                         # lic (lomove kameny)
MAT_CORE  = None                         # jadro (lom + malta)
MAT_FRAME = None                         # osteni, oblouky (opracovany kamen)
MAT_CROWN = None                         # koruna zdi: odkryte horni kameny (vic zvetrale, svetlejsi, s nadechem lisejniku)
CROWN_WEATHER = True                     # odkryte kameny koruny = zvetrale tvary (SM_RuinStone_W_*) + material MI_RuinCrown
MAT_DIR   = "/Game/Skvt/Lapikus/Ruin/Materials"
# --- vlastni procedurni textury (tools/textures/gen_textures.py -> textures/*.png v koreni; skript je sam naimportuje)
TEX_SRC = "textures"
TEX_DIR = "/Game/Skvt/Lapikus/Ruin/Textures"
TEX_VERSION = 1                          # vyssi nez v projektu -> textury se naimportuji znovu (po zmene gen_textures.py)
TEX_FILES = {"T_RuinBark_D": "color", "T_RuinBark_N": "normal", "T_RuinEndGrain_D": "color", "T_RuinEndGrain_N": "normal"}
TEXTURES = {   # kandidati (BaseColor, Normal) - pouzije se prvni existujici
    "bark":     [(TEX_DIR + "/T_RuinBark_D", TEX_DIR + "/T_RuinBark_N")],
    "endgrain": [(TEX_DIR + "/T_RuinEndGrain_D", TEX_DIR + "/T_RuinEndGrain_N")],
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
}
MAT_VERSION = 7                          # vyssi nez v projektu -> skript prestavi graf M_RuinStone a doplni parametry MI_*
                                         # (tinty MI_RuinFace/Frame zustanou, jak je mas; MAT_RESET viz nize)
MAT_RESET = {"crown": 2, "core": 3, "frame": 4, "wood_tar": 6}      # MI starsi nez tato verze dostane znovu tint a texturu z MAT_LOOK / TEXTURES
# --- knihovni meshe (tools/meshes/gen_meshes.py -> meshes/<kategorie>/*.obj v koreni vedle zrlib; skript je sam naimportuje)
USE_STONE_MESHES = True                  # False = vsude kostky (Cube) jako drive
MESH_SRC  = "meshes"                     # slozka s OBJ v koreni, podslozky podle kategorie (stone, wood, ...)
MESH_ROOT = "/Game/Skvt/Lapikus/Ruin"
MESH_DIRS = {"stone": "Stones",          # kategorie (= podslozka meshes/<kategorie>, CATEGORIES v gen_meshes.py)
             "wood":  "Wood"}            #   -> slozka v UE MESH_ROOT/<slozka>
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
# kulatina (tools/meshes/mesh_log.py): prefix -> (jmenovity rozmer delka, sirka, vyska v cm = NOMINAL v mesh_log.py, varianty).
# Delka podel sx dilce (svisly kul / sloup = pitch 90). Sloty: Wood (material podle upravy dilce), EndGrain, Bark (SLOT_MI).
ROUND_MESHES = {
    "SM_RuinLog":        ((100.0, 20.0, 20.0), "ABC"),   # loupana kulatina
    "SM_RuinLogBark":    ((100.0, 20.0, 20.0), "ABC"),   # kulatina s kurou
    "SM_RuinPole":       ((100.0, 8.0, 8.0), "ABC"),     # loupana tyc
    "SM_RuinPoleBark":   ((100.0, 8.0, 8.0), "ABC"),     # tyc s kurou
    "SM_RuinStake":      ((200.0, 20.0, 20.0), "ABC"),   # kul s kurou, zaseknuta spicka na +X
    "SM_RuinStakeSmall": ((160.0, 7.0, 7.0), "AB"),      # loupany kul, spicky na obou koncich
    "SM_RuinForkHead":   ((45.0, 30.0, 12.0), "AB"),     # hlava rozsochy: kmen na -X, vidlice na +X, ramena v rovine XY
    "SM_RuinGutter":     ((100.0, 20.0, 11.0), "AB"),    # loupany zlab: rez nahore (+Z), vydlabany
    "SM_RuinGutterBark": ((100.0, 20.0, 11.0), "AB"),    # zlab s kurou zvenku
}
ROUND_SHAPES = {   # Stone.shape -> (prefix loupany, prefix s kurou); None = tvar existuje jen v druhe variante
    "round":  ("SM_RuinLog", "SM_RuinLogBark"),          # Pole / PoleBark, kdyz prumer <= POLE_MAX_D
    "stake":  ("SM_RuinStake", "SM_RuinStake"),
    "stake2": ("SM_RuinStakeSmall", "SM_RuinStakeSmall"),
    "fork":   ("SM_RuinForkHead", "SM_RuinForkHead"),
    "gutter": ("SM_RuinGutter", "SM_RuinGutterBark"),
}
POLE_MAX_D = 11.0                        # cm: tenci kulatina = tyc (SM_RuinPole*), jinak SM_RuinLog*
SLOT_MI = {"bark": "MI_RuinBark", "endgrain": "MI_RuinWood_EndGrain"}   # materialy slotu Bark a EndGrain kulatiny
STONE_MESH_VERSION = {"SM_RuinStone_W_": 2, "SM_RuinTimber_": 2, "SM_RuinPlank_": 2, "SM_RuinPost_": 2,
                      "SM_RuinLog": 1, "SM_RuinPole": 1, "SM_RuinStake": 1, "SM_RuinForkHead": 1, "SM_RuinGutter": 2}   # Gutter 2: SM_RuinGutter je loupany, s kurou SM_RuinGutterBark   # meshe s nizsi verzi v projektu se naimportuji znovu (prefix -> verze)
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
