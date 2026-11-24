---
# orchestrace
type: state
validity: valid
updated: 2026-11-24
# hra
domain: structures
depth: 4
entity: "[[Lapikus]]"
build_step: 03_ruin
---
# Zřícenina – stav 03_ruin (bloky, půdorys v3)

## Souhrn
Platný stav kroku `03_ruin` (zřícenina z bloků, půdorys v3, 11/2026) a přehled staveb na ní v `05_constructions`. Řádek „Hrad“ v `Zricenina_README_PROJEKT.md` je zastaralý, platí tento dokument.
- **Generování:** `build_ruin_blocks.py`, data `gen_layout.py` → `ruin_layout.json`, terén se měří z levelu; `manual_edits.json` se nepřepisuje (kap. *Pracovní postup*, *Jak se teď generuje*).
- **Zřícenina (03):** půdorys v3, úpravy zdí, materiály a dřevo, věž (kap. *Půdorys v3*, *Úpravy zdí*, *Věž*; škody z dobývání a přístřešek hlídky v [[stav_vez_pristresek]]). Dělení 03 (zdi, kámen) / 05 (dřevěné vestavby, suť) a spouštěče: kap. *Rozdělení 03 / 05*.
- **Stavby po částech:** západní část u ostrohu (krov, dostavba); palác – kovárna (všechny kroky hotové, v UE ověřeny jen zčásti); palác – dům posádky (kroky 1–3 hotové, staveniště ověřeno jen mimo UE); brána – strážní stanoviště (kroky 1–3 ve skriptech) a šíjový příkop s mostní lávkou a zátarasem (ověřeno v UE 24. 11. 2026, [[stav_brana]]).
- **Otevřené:** přístřešek z kůry nad bránou, krytina, strop a vybavení domu, ověření posledních úprav ostatních staveb v UE (kap. *Otevřené / další kroky* a stavy staveb). Optimalizace (34,5 mil. trojúhelníků, s Nanite bez problému) se zatím neřeší.
- **Přednost:** u domu a brány platí kap. 0 návrhů [[navrh_palac_obydli_stred]] a [[navrh_brana_straz]]. Koruny `Palac_J` jsou v návrhu domu o 0,31 m výš než skutečnost ([[stav_palac_kovarna]]).

Doplňuje `Zricenina_README_PROJEKT.md`. Řádek „Hrad“ v jeho kap. 1 je zastaralý, platí tento dokument.

## Pracovní postup

- Úpravy, které Jirka zadá, Claude rovnou ukládá do skriptů a dat v `skvt_projekt\PrototypeDesigns\Lapikus` a pošle náhled. Napřed se ptá, jen když se teprve řeší, jak něco udělat.
- `manual_edits.json` Claude nikdy nepřepisuje. Poslední terén z levelu je v `skvt_projekt\...\03_ruin\blocks\terrain_from_level.json`.

## Jak se teď generuje

- **Generátor z bloků:** `03_ruin/blocks/build_ruin_blocks.py`, stav ~1650. Lomové kameny líce jsou zaoblené zvětralé meshe `SM_RuinStone_*` (OBJ v `meshes/stone/`, automatický import, Nanite, box kolize). Jádro jsou kostky. Ostění tvoří `SM_RuinAshlar`. Materiál `M_RuinStone` + `MI_RuinFace/Core/Frame` vytvoří skript sám. Návod je v [[03_ruin]].
- **Data:** `tools/ruin/gen_layout.py` + `03_ruin/ruin_layout_draft.json` → `ruin_layout.json`. Mimo UE: `tools/checks/run_checks.py` (otvory, kameny bez podpory, ostroh), `tools/checks/preview3d.py` a `check_blocks.py` (náhledy).
- **Terén:** `TERRAIN_FROM_LEVEL = True`. Build změří landscape v levelu a uloží `terrain_from_level.json`. Capture používá stejný uložený stav.
- **Ruční úpravy v levelu:**
  - bourací objemy (Trigger Box s tagy `Ruin_*`),
  - `capture_manual_edits()` → `manual_edits.json`,
  - `tools/ruin/export_level_layout.py` → `layout_from_level.json` (posunuté zdi + body `RuinPt_<Zed>_<NN>`).
- **Kde leží soubory:** `skvt_projekt/PrototypeDesigns/Lapikus` (`03_ruin`, `tools/ruin`). Odtud se spouští v UE. `GameDesign/Claude outputs/Lapikus` je jen archiv starších kopií.

## Půdorys v3 (11/2026)

- **Strážní věž se dvěma branami** (asi 7 × 7 m, SV od hlavní věže):
  - `Brana_V`: 1. brána z východu, `plinth` 2 m (stojí na nižším terénu, most nebo rampa přes příkop),
  - `Brana_S`: severní stěna,
  - `Brana_J`: 2. brána na západ do uličky podél severní strany věže,
  - `Brana_Jih`: jižní stěna.
- **`Hradba_V`** vede od jižní stěny strážní věže obloukem k JV rohu hlavní věže, asi 5–7 m od věže.
- **`Hradba_Z_S`** končí pootočeným úsekem 08 a napojením na SZ roh strážní věže.
- **Vstup do hlavní věže:** průlom 1,6 × 2,45 m ve `Vez_S` (s = 8,0 m), pod původními dveřmi v 1. patře (s = 7,62 m). Mezi vrchem průlomu a kapsami ochozu (3,85 m) zůstává 1,4 m zdiva.
- **Příkop a přemostění (11/2026):** starý příkop pod strážní věží je v heightmapě zasypaný výškami z levelu; před `Brana_V` a `Hradba_V` je vygenerován šíjový příkop (`Z 2700 cm`) bez čelních valů (zrušeny 24. 11. 2026), přístupový úvoz, severní úniková rampa, v `03_ruin` mostní pilíř `Brana_Pilir` a opěra `Brana_Opera` a v `05_constructions` lávka `Brana_Most` se zátarasem `Brana_Zataras` ([[navrh_brana_prikop]], [[stav_brana]]).
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
- **Škody z dobývání a přístřešek hlídky (17. 11. 2026):** stav v [[stav_vez_pristresek]], návrh škod [[navrh_vez_skody]], návrh přístřešku [[navrh_vez_pristresek]].

- **Překlad výklenku střílen (11/2026):** je vysoký přesně jednu řadu kamene (dřív pevně 35 cm). Nad překladem tak nezůstává vynechaná řada („kapsa“).

- **Stavění po částech (11/2026):** `03_ruin/blocks/casti/Obvod.py` (věž, obvodové hradby, brány, dlažba věže), `Palac.py` a `Ostroh.py` (vnitřní zdi) postaví jen jednu část. Rozdělení je v `CASTI` v `build_ruin_blocks.py`, actory mají tag `cast:<Část>`. Úsek hradby u ostrohu (krov) patří do Obvodu.

- **Refaktoring (11/2026):** sdílená knihovna `zrlib/` v kořeni (nastavení vzhledu `config.py`, geometrie, Unreal), 03 rozdělené na `zr_ruin/` (rozpad, příprava, zeď po krocích, úpravy, dlažba, suť), 05 na typy staveb `zr_stavby/` s registrem `TYPES` (dřevo věže přesunuté z 03 do 05). Kontroly a otisk v `tools/checks/`. Výstup bit po bitu stejný jako před refaktoringem.

## Rozdělení 03 / 05 (11/2026)

- **03_ruin** (`build_ruin_blocks.py`, `ruin_layout.json`): zřícenina, tedy zdi, otvory, ostění, kapsy a kamenná dlažba (`Vez_Dlazba`). Tag `Zricenina_Ruin`.
- **05_constructions** (`build_constructions.py`, `constructions.json`, `constructions_edits.json`): druhé zabydlení, tedy dřevěné vestavby (`Vez_Patra`: trámy, prkna, průvlak, schody, podesta) a volná suť. Tag `Zricenina_Stavby`, složky `Stavby/...`. Staví se zvlášť, zříceninu nepřestavuje. Generátor zříceniny používá jako knihovnu.
- **Společné rozměry věže** jsou v `tools/ruin/tower_spec.py`. Když se změní, přegeneruje se `gen_layout.py` i `tools/constructions/gen_constructions.py`.
- **Náhled věže:** `tools/constructions/check_tower.py`.
- **Všechno najednou (15. 11. 2026):** `build_normal.py` v kořeni postaví hrad (03) i stavby (05) aditivně, `build_fullscope.py` je oprava (smaže generované actory a knihovní meshe a vše postaví znovu). Společná logika je v `zrlib/pipeline.py`.
- **Spouštění po stavbách:** `05_constructions/stavby/<Stavba>.py` (`Vez_Patra`, `Vez_Pristresek`, `Ostroh_Krov`, `Ostroh_Dostavba`, `Ostroh_Podlaha`, `Sut`) postaví jen jednu stavbu. `build_constructions.py` postaví všechny.

## Otevřené / další kroky

- Provizorní hlídková konstrukce nad branami: rozestavěno (chybí přístřešek z kůry), viz kapitola „Brána – strážní stanoviště“.
- Náhledy na skutečném terénu: po buildu poslat `terrain_from_level.json`.
- Nárožní kvádry na zlomech lomené hradby (prosvítá jádro).

## Západní část u ostrohu (11/2026)

- `Hradba_Z_S` je v západní části (s 10,3–34,0) cíleně snížená a zarovnaná. Zůstávají jen celé řady pod 3,3 m (`cap`).
- V koruně je 7 žlábků pro trámy (`notches`).
- 05 `Ostroh_Krov`: 2 sloupy asi 1 m od vnitřního líce `ZBudova_V` po stranách průchodu, příčka (hřeben) a 7 paprskovitých trámů ve žlábcích hradby (11–17°, přesahují ji jako okap). Od příčky vedou i paprskové trámy na jejích koncích a 2 trámy zpět na dostavbu `ZBudova_V` (11–14°), takže střecha klesá na všechny strany. Všechno je dehtované.
- Krytina je z dehtovaných prken po spádu na latích, s lištami přes spáry a krycím prknem přes každý trám. Lemování u příčky se vyřeší jinak. Koruna hradby pod střechou je směrem ven snížená ve sklonu střechy (`roof_clear`).
- Žlábky se od 11/2026 počítají přesně podle půdorysu trámu (`dir`, `bw`), takže sedí i v oblouku hradby (dřív tam trám B3 zasahoval asi 11 cm do kamene).
- **Uzavřená obytná část (05 `Ostroh_Dostavba`):** jednořadé kamenné dostavby z kamene rozvalin (0,45 m) na koruně `ZBudova_V` (s dveřmi v průchodu a jedním oknem 1,4 × 0,7 m severně od nich, k `ZBudova_S`), `ZBudova_S` a mezi trámy na hradbě, všude až pod střechu. Dostavba je pod trámy dokola příčky snížená, na bocích víc než uprostřed. Nadpraží dveří i okna je o půl řady výš než řada nad 2,2 m nad terénem (spodek asi 2,4 m), podložené a dorovnané polovičními kameny. Okno 1,25 m široké; v místě okna je původní zeď `ZBudova_V` vybouraná nad 1,4 m (03 `edits` → `cut` z `ostroh_spec.py`), okno sahá až na korunu zříceniny. Ve dveřích je dřevěný práh 1,5 cm nad podlahou, v dostavbě jako samostatný actor (výška se dá doladit ručně a uložit přes capture). Maltové jádro dostavby `V` pokračuje až do země ve zdi `ZBudova_V`: za lícovými kameny v rovině dostavby, kde líc chybí, v jádru zdi (zdí neprosvítá). Kámen dostavby je stejně velký jako ve zdech hradu. Suť uvnitř je uklizená. Prkenná podlaha na dehtovaných podvalech (05 `Ostroh_Podlaha`). **Zřícenina se kvůli dostavbě nemění**, všechno je v 05.
- Rozměry jsou v `tools/ruin/ostroh_spec.py`, dostavba a trámy dokola příčky v `tools/constructions/gen_constructions.py`. Žlab, okapnice, sud a lemování horního okraje krytiny přijdou později.

- **Oprava natočení v UE (11/2026):** UE má `roll` opačně než výpočty, kontroly a náhledy. Do UE se proto posílá `-roll` (`zrlib/ue_assets.ue_rotator`), capture ho vrací zpět. Dřív byly v UE kusy s `roll` nakloněné na opačnou stranu. Nejvíc to bylo vidět na prknech v bočních polích krovu, kde vznikaly průsvitné spáry. Týká se to i mírně nakloněných kamenů zříceniny a dřeva ve věži, proto je potřeba přestavět 03 i 05.

## Palác – kovárna ve východní místnosti (11/2026)

Návrh [[navrh_palac_kovarna]], stav stavby [[stav_palac_kovarna]].

## Palác – dům posádky v prostřední místnosti (11/2026)

Návrh [[navrh_palac_obydli_stred]], stav stavby [[stav_palac_obydli]], předání staviteli [[predani_palac_obydli_stavitel]].

## Brána – strážní stanoviště nad oblouky (11/2026)

Návrh [[navrh_brana_straz]], stav stavby [[stav_brana_straz]].

## Brána – šíjový příkop, mostní pilíř, lávka a zátaras (11/2026)

Návrh [[navrh_brana_prikop]], stav stavby [[stav_brana]] (v `03_ruin` vnější ozub prahu `Brana_V`, pilíř `Brana_Pilir` a opěra `Brana_Opera`, rozšířená mřížka `terrain` na `x1 = 4400`; v `05_constructions` vyrovnání `Brana_Most_Kamen`, lávka `Brana_Most` a zátaras `Brana_Zataras`).

## Optimalizace do budoucna (zatím není potřeba)

- **Stav 11/2026:** zřícenina má asi 23 500 kamenů a 34,5 mil. trojúhelníků. Z toho připadá 24,7 mil. na lomové kameny (`SM_RuinStone`), 6,2 mil. na korunu (`_W`) a 3,4 mil. na ostění (`SM_RuinDressed`). Dřevo ve věži má asi 0,5 mil. Unikátních meshí je jen 33, zbytek jsou instance. S Nanite to není problém.
- **Kdy na to sáhnout:** ray tracing (Lumen Hardware), platforma bez Nanite, Merge Actors, export.
- **Hint:** v `tools/meshes/mesh_stone.py` dát běžnému kameni (`SM_RuinStone_R*`) hrubší síť na plochách a jemnější jen v pásu zaoblení hran. Stejně se to už dělá u `_W` (funkce `grid` podle úhlu). Ušetří se 40–50 % trojúhelníků, celkem by vyšlo asi 18–20 mil. Pak zvýšit `STONE_MESH_VERSION` pro `SM_RuinStone_R` a skript meshe přeimportuje sám.
- Korunu a ostění nechat, jsou vidět zblízka. Skryté jádro je už teď jen kostka.
