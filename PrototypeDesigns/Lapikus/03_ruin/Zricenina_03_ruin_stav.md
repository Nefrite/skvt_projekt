# Zřícenina – stav 03_ruin (bloky, půdorys v3)

Doplňuje `Zricenina_README_PROJEKT.md`. Řádek „Hrad“ v jeho kap. 1 je zastaralý, platí tento dokument.

## Pracovní postup

- Úpravy, které Jirka zadá, Claude rovnou ukládá do skriptů a dat v obou složkách (`GameDesign\Claude outputs\Zriceni_orez_505` a `skvt_projekt\PrototypeDesigns\Lapikus`) a pošle náhled. Napřed se ptá, jen když se teprve řeší, jak něco udělat.
- `manual_edits.json` Claude nikdy nepřepisuje. Poslední terén z levelu je v `skvt_projekt\...\03_ruin\blocks\terrain_from_level.json`.

## Jak se teď generuje

- **Generátor z bloků:** `03_ruin/blocks/build_ruin_blocks.py`, stav ~1650. Lomové kameny líce jsou zaoblené zvětralé meshe `SM_RuinStone_*` (OBJ ve `stones/`, automatický import, Nanite, box kolize). Jádro jsou kostky. Ostění tvoří `SM_RuinAshlar`. Materiál `M_RuinStone` + `MI_RuinFace/Core/Frame` vytvoří skript sám. Návod je v `README_bloky.md`.
- **Data:** `tools/ruin/gen_layout.py` + `03_ruin/ruin_layout_draft.json` → `ruin_layout.json`. Mimo UE: `test_openings.py` (žádný kámen ve světlosti otvorů) a `check_blocks.py` (náhled).
- **Terén:** `TERRAIN_FROM_LEVEL = True`. Build změří landscape v levelu a uloží `terrain_from_level.json`. Capture používá stejný uložený stav.
- **Ruční úpravy v levelu:**
  - bourací objemy (Trigger Box s tagy `Ruin_*`),
  - `capture_manual_edits()` → `manual_edits.json`,
  - `tools/ruin/export_level_layout.py` → `layout_from_level.json` (posunuté zdi + body `RuinPt_<Zed>_<NN>`).
- **Kde leží soubory:** `GameDesign/Claude outputs/Zriceni_orez_505` a kopie v `skvt_projekt/PrototypeDesigns/Lapikus` (`03_ruin`, `tools/ruin`). Odtud se spouští v UE.

## Půdorys v3 (11/2026)

- **Strážní věž se dvěma branami** (asi 7 × 7 m, SV od hlavní věže):
  - `Brana_V`: 1. brána z východu, `plinth` 2 m (stojí na nižším terénu, most nebo rampa přes příkop),
  - `Brana_S`: severní stěna,
  - `Brana_J`: 2. brána na západ do uličky podél severní strany věže,
  - `Brana_Jih`: jižní stěna.
- **`Hradba_V`** vede od jižní stěny strážní věže obloukem k JV rohu hlavní věže, asi 5–7 m od věže.
- **`Hradba_Z_S`** končí pootočeným úsekem 08 a napojením na SZ roh strážní věže.
- **Vstup do hlavní věže:** průlom 1,2 × 2,3 m ve `Vez_S` (s = 8 m), mimo osu původních dveří v 1. patře (6,5 m).
- **Příkop:** starý šíjový příkop je zasypaný (terén v UE). Nový se vykope ručně před linií strážní věže a hradby.
- **Předhradí** se zatím nedělá.

## Úpravy zdí (hotové)

- `Hradba_Z_S` úsek 01: šikmý sesuv, stezka k vodě u paláce s prahem asi 0,5 m (`breach` se `slope_r` / `power_r`).
- `Hradba_Z_S` úsek 03: branka zrušena, místo ní střílna. Úsek 04: střílna.
- Vylámané ostění pod stojícím obloukem nebo nadpražím: zůstává zapuštěné jádro a nese oblouk.
- Otvory jsou zarovnané na řady, kameny se kolem otvorů dělí (ID s příponou `.a` / `.b`).
- **Rozebírání líce (11/2026):** hlavně shora pod korunou, u paty jen malé hloučky. Kameny nad malou mezerou drží (klenutí). Odkryté jádro je z lomových kamenů různě zapuštěných a materiál `MI_RuinCore` je šedý (malta), ne tmavý.
- **Brana_S** je zvednutá do výšky oblouků obou bran (`protect` s `to`), přilehlé konce `Brana_V` a `Brana_J` taky. Na ni přijde provizorní hlídková konstrukce (05_constructions).
- **Palac_J:** střílny s výklenkem zevnitř jako ve věži a v hradbě.
- **Ostění a střílny** jsou z opracovaných kamenů `SM_RuinDressed_*` (zaoblené hrany). `MI_RuinFrame` je stejný kámen jako líc, jen o kousek světlejší.
- **Koruna zvětralá shora:** odkryté horní kameny mají meshe `SM_RuinStone_W_*` (nahoře zaoblení 8,5–10,5 cm a důlky, dole ostré 3 cm). `M_RuinStone` má zvětrání podle normaly: co míří nahoru, je světlejší a nazelenalé (`Top*` parametry, `MAT_TOP`). Graf materiálu i W meshe skript sám aktualizuje podle verze (`MAT_VERSION`, `STONE_MESH_VERSION`).

## Věž (hotovo 11/2026)

- Podlaha přízemí je v Z 3150 (`VEZ_F`), patra jsou po 4,2 m (`VEZ_ST`) a řady kamenů pevně po 0,35 m. Všechny výšky ve věži se počítají od podlahy.
- **Přízemí:** kamenná dlažba. Do věže se vchází vybouraným průchodem z uličky (`Vez_S`, 1,6 × 2,45 m, rozbité okraje).
- **1. a 2. patro:** trámy v kapsách (`Vez_V` a `Vez_Z`) a hrubá prkna, otvor pro žebřík v SV rohu. Ve 3. a 4. patře jsou jen prázdné kapsy.
- **Původní dveře** jsou v 1. patře (4,2 m), ve `Vez_S` zevnitř mezi západní zdí a sloupem. Zvenku je obnovená dřevěná podesta (trámy v kapsách + 2 sloupky).
- **Střílny:** zvenku úzký průzor, zevnitř kónický výklenek od podlahy do 2,1 m, parapet 1,05 m.
  - `Vez_J`: všechna podlaží včetně přízemí.
  - `Vez_V`: od 1. patra.
  - `Vez_S`: 2. patro.
- **Okna a podesta:** hradní okna ve `Vez_Z` (1. a 2. patro), zvenku na `Vez_S` kapsy po podestě pod původním vstupem.
- **Schody:** provizorní, 60°, oboje stoupají k západu a horním koncem se opírají o průvlak uprostřed věže: do 1. patra v poli u severní zdi, do 2. patra v sousedním poli. Trámy jsou po 1,64 m. Zábradlí se nedělá (provizorní oprava).
- **Náhled řezu věží:** `tools/constructions/check_tower.py`.

## Rozdělení 03 / 05 (11/2026)

- **03_ruin** (`build_ruin_blocks.py`, `ruin_layout.json`): zřícenina, tedy zdi, otvory, ostění, kapsy a kamenná dlažba (`Vez_Dlazba`). Tag `Zricenina_Ruin`.
- **05_constructions** (`build_constructions.py`, `constructions.json`, `constructions_edits.json`): druhé zabydlení, tedy dřevěné vestavby (`Vez_Patra`: trámy, prkna, průvlak, schody, podesta) a volná suť. Tag `Zricenina_Stavby`, složky `Stavby/...`. Staví se zvlášť, zříceninu nepřestavuje. Generátor zříceniny používá jako knihovnu.
- **Společné rozměry věže** jsou v `tools/ruin/tower_spec.py`. Když se změní, přegeneruje se `gen_layout.py` i `tools/constructions/gen_constructions.py`.
- **Náhled věže:** `tools/constructions/check_tower.py`.

## Otevřené / další kroky

- Provizorní hlídková konstrukce na `Brana_S` (05_constructions).
- Most nebo rampa k 1. bráně, zbytky mostního pilíře v příkopu.
- Náhledy na skutečném terénu: po buildu poslat `terrain_from_level.json`.
- Nárožní kvádry na zlomech lomené hradby (prosvítá jádro).
