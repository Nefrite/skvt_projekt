# Zřícenina – stav 03_ruin (bloky, půdorys v3)

Doplňuje `Zricenina_README_PROJEKT.md`. Řádek „Hrad“ v jeho kap. 1 je zastaralý, platí tento dokument.

## Pracovní postup

- Úpravy, které Jirka zadá, Claude rovnou ukládá do skriptů a dat v obou složkách (`GameDesign\Claude outputs\Zriceni_orez_505` a `skvt_projekt\PrototypeDesigns\Lapikus`) a pošle náhled. Napřed se ptá, jen když se teprve řeší, jak něco udělat.
- `manual_edits.json` Claude nikdy nepřepisuje. Poslední terén z levelu je v `skvt_projekt\...\03_ruin\blocks\terrain_from_level.json`.

## Jak se teď generuje

- **Generátor z bloků:** `03_ruin/blocks/build_ruin_blocks.py`, stav ~1650. Lomové kameny líce jsou zaoblené zvětralé meshe `SM_RuinStone_*` (OBJ ve `stones/`, automatický import, Nanite, box kolize). Jádro jsou kostky. Ostění tvoří `SM_RuinAshlar`. Materiál `M_RuinStone` + `MI_RuinFace/Core/Frame` vytvoří skript sám. Návod je v `README_bloky.md`.
- **Data:** `tools/ruin/gen_layout.py` + `03_ruin/ruin_layout_draft.json` → `ruin_layout.json`. Mimo UE: `tools/checks/run_checks.py` (otvory, kameny bez podpory, ostroh), `tools/checks/preview3d.py` a `check_blocks.py` (náhledy).
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
- **Dřevo**, pět úprav (`constructions.json` → `finish`):
  - dehet `MI_RuinWood_Tar` (skoro hnědočerný, matný): trámy, průvlak, sloupy,
  - krev `MI_RuinWood_Blood` (tmavě červenohnědá): venkovní ochoz,
  - staré neošetřené `MI_RuinWood_Old` (zašedlé, zaprášené): prkna ve 2. patře,
  - bez úpravy `MI_RuinWood`: prkna v 1. patře a schody,
  - olej `MI_RuinWood_Oil`: připravený, zatím nepoužitý. Rozdělení je v `constructions.json` → `finish`.
- **Koruna zvětralá shora:** odkryté horní kameny mají meshe `SM_RuinStone_W_*` (nahoře zaoblení 8,5–10,5 cm a důlky, dole ostré 3 cm). `M_RuinStone` má zvětrání podle normaly: co míří nahoru, je světlejší a nazelenalé (`Top*` parametry, `MAT_TOP`). Graf materiálu i W meshe skript sám aktualizuje podle verze (`MAT_VERSION`, `STONE_MESH_VERSION`).

## Věž (hotovo 11/2026)

- Podlaha přízemí je v Z 3150 (`VEZ_F`), patra jsou po 4,2 m (`VEZ_ST`) a řady kamenů pevně po 0,35 m. Všechny výšky ve věži se počítají od podlahy.
- **Přízemí:** kamenná dlažba. Do věže se vchází vybouraným průchodem z uličky (`Vez_S`, 1,6 × 2,45 m, rozbité okraje).
- **1. a 2. patro:** trámy v kapsách (`Vez_V` a `Vez_Z`) a hrubá prkna, otvor pro žebřík v SV rohu. Ve 3. a 4. patře jsou jen prázdné kapsy.
- **Původní dveře** jsou v 1. patře (4,2 m), ve `Vez_S` zevnitř mezi západní zdí a sloupem. Zvenku je obnovený dřevěný ochoz (trámy zapuštěné v kapsách, krátké šikmé vzpěry o zeď, bez sloupků do země).
- **Střílny:** zvenku úzký průzor, zevnitř kónický výklenek od podlahy do 2,1 m, parapet 1,05 m.
  - `Vez_J`: všechna podlaží včetně přízemí.
  - `Vez_V`: od 1. patra.
  - `Vez_S`: 2. patro.
- **Okna a podesta:** hradní okna ve `Vez_Z` (1. a 2. patro), zvenku na `Vez_S` kapsy po podestě pod původním vstupem.
- **Schody:** provizorní, 60°, cik-cak. Do 1. patra stoupají k východu (pole u severní zdi), do 2. patra k západu a opírají se o průvlak (sousední pole). Trámy jsou po 1,64 m. Zábradlí se nedělá (provizorní oprava).
- **Náhled řezu věží:** `tools/constructions/check_tower.py`.

- **Překlad výklenku střílen (11/2026):** je vysoký přesně jednu řadu kamene (dřív pevně 35 cm). Nad překladem tak nezůstává vynechaná řada („kapsa“).

- **Stavění po částech (11/2026):** `03_ruin/blocks/casti/Obvod.py` (věž, obvodové hradby, brány, dlažba věže), `Palac.py` a `Ostroh.py` (vnitřní zdi) postaví jen jednu část. Rozdělení je v `CASTI` v `build_ruin_blocks.py`, actory mají tag `cast:<Část>`. Úsek hradby u ostrohu (krov) patří do Obvodu.

- **Refaktoring (11/2026):** sdílená knihovna `zrlib/` v kořeni (nastavení vzhledu `config.py`, geometrie, Unreal), 03 rozdělené na `zr_ruin/` (rozpad, příprava, zeď po krocích, úpravy, dlažba, suť), 05 na typy staveb `zr_stavby/` s registrem `TYPES` (dřevo věže přesunuté z 03 do 05). Kontroly a otisk v `tools/checks/`. Výstup bit po bitu stejný jako před refaktoringem.

## Rozdělení 03 / 05 (11/2026)

- **03_ruin** (`build_ruin_blocks.py`, `ruin_layout.json`): zřícenina, tedy zdi, otvory, ostění, kapsy a kamenná dlažba (`Vez_Dlazba`). Tag `Zricenina_Ruin`.
- **05_constructions** (`build_constructions.py`, `constructions.json`, `constructions_edits.json`): druhé zabydlení, tedy dřevěné vestavby (`Vez_Patra`: trámy, prkna, průvlak, schody, podesta) a volná suť. Tag `Zricenina_Stavby`, složky `Stavby/...`. Staví se zvlášť, zříceninu nepřestavuje. Generátor zříceniny používá jako knihovnu.
- **Společné rozměry věže** jsou v `tools/ruin/tower_spec.py`. Když se změní, přegeneruje se `gen_layout.py` i `tools/constructions/gen_constructions.py`.
- **Náhled věže:** `tools/constructions/check_tower.py`.
- **Spouštění po stavbách:** `05_constructions/stavby/<Stavba>.py` (`Vez_Patra`, `Ostroh_Krov`, `Ostroh_Dostavba`, `Ostroh_Podlaha`, `Sut`) postaví jen jednu stavbu. `build_constructions.py` postaví všechny.

## Otevřené / další kroky

- Provizorní hlídková konstrukce na `Brana_S` (05_constructions).
- Most nebo rampa k 1. bráně, zbytky mostního pilíře v příkopu.
- Náhledy na skutečném terénu: po buildu poslat `terrain_from_level.json`.
- Nárožní kvádry na zlomech lomené hradby (prosvítá jádro).

## Západní část u ostrohu (11/2026)

- `Hradba_Z_S` je v západní části (s 12,4–31,9) cíleně snížená a zarovnaná. Zůstávají jen celé řady pod 3,3 m (`cap`).
- V koruně je 7 žlábků pro trámy (`notches`).
- 05 `Ostroh_Krov`: 2 sloupy těsně u vnitřního líce `ZBudova_V` po stranách průchodu, příčka a 7 paprskovitých trámů ve žlábcích. Trámy se mírně svažují ke zdi a přesahují ji (okap). Všechno je dehtované.
- Krytina je z dehtovaných prken po spádu na latích, s lištami přes spáry a krycím prknem přes každý trám. Lemování u příčky se vyřeší jinak. Koruna hradby pod střechou je směrem ven snížená ve sklonu střechy (`roof_clear`).
- Žlábky se od 11/2026 počítají přesně podle půdorysu trámu (`dir`, `bw`), takže sedí i v oblouku hradby (dřív tam trám B3 zasahoval asi 11 cm do kamene).
- **Uzavřená obytná část (05 `Ostroh_Dostavba`):** jednořadé kamenné dostavby z kamene rozvalin (0,45 m) na koruně `ZBudova_V` (s dveřmi v průchodu a jedním oknem 1,4 × 0,9 m severně od nich, k `ZBudova_S`), `ZBudova_S` a mezi trámy na hradbě, všude až pod střechu. Střecha je prodloužená nad boční klíny (5 bočních trámů na jihu, 3 na severu). Kámen dostavby je stejně velký jako ve zdech hradu. Suť uvnitř je uklizená. Prkenná podlaha na dehtovaných podvalech (05 `Ostroh_Podlaha`). **Zřícenina se kvůli dostavbě nemění**, všechno je v 05.
- Rozměry jsou v `tools/ruin/ostroh_spec.py`, dostavba a boční trámy v `tools/constructions/gen_constructions.py`. Žlab, okapnice, sud a lemování horního okraje krytiny přijdou později.

## Optimalizace do budoucna (zatím není potřeba)

- **Stav 11/2026:** zřícenina má asi 23 500 kamenů a 34,5 mil. trojúhelníků. Z toho připadá 24,7 mil. na lomové kameny (`SM_RuinStone`), 6,2 mil. na korunu (`_W`) a 3,4 mil. na ostění (`SM_RuinDressed`). Dřevo ve věži má asi 0,5 mil. Unikátních meshí je jen 33, zbytek jsou instance. S Nanite to není problém.
- **Kdy na to sáhnout:** ray tracing (Lumen Hardware), platforma bez Nanite, Merge Actors, export.
- **Hint:** v `gen_stones.py` dát běžnému kameni (`SM_RuinStone_R*`) hrubší síť na plochách a jemnější jen v pásu zaoblení hran. Stejně se to už dělá u `_W` (funkce `grid` podle úhlu). Ušetří se 40–50 % trojúhelníků, celkem by vyšlo asi 18–20 mil. Pak zvýšit `STONE_MESH_VERSION` pro `SM_RuinStone_R` a skript meshe přeimportuje sám.
- Korunu a ostění nechat, jsou vidět zblízka. Skryté jádro je už teď jen kostka.
