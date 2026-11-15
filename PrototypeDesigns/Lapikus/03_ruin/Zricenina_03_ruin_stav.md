# Zřícenina – stav 03_ruin (bloky, půdorys v3)

Doplňuje `Zricenina_README_PROJEKT.md`. Řádek „Hrad“ v jeho kap. 1 je zastaralý, platí tento dokument.

## Pracovní postup

- Úpravy, které Jirka zadá, Claude rovnou ukládá do skriptů a dat v obou složkách (`GameDesign\Claude outputs\Lapikus` a `skvt_projekt\PrototypeDesigns\Lapikus`) a pošle náhled. Napřed se ptá, jen když se teprve řeší, jak něco udělat.
- `manual_edits.json` Claude nikdy nepřepisuje. Poslední terén z levelu je v `skvt_projekt\...\03_ruin\blocks\terrain_from_level.json`.

## Jak se teď generuje

- **Generátor z bloků:** `03_ruin/blocks/build_ruin_blocks.py`, stav ~1650. Lomové kameny líce jsou zaoblené zvětralé meshe `SM_RuinStone_*` (OBJ v `meshes/stone/`, automatický import, Nanite, box kolize). Jádro jsou kostky. Ostění tvoří `SM_RuinAshlar`. Materiál `M_RuinStone` + `MI_RuinFace/Core/Frame` vytvoří skript sám. Návod je v `README_bloky.md`.
- **Data:** `tools/ruin/gen_layout.py` + `03_ruin/ruin_layout_draft.json` → `ruin_layout.json`. Mimo UE: `tools/checks/run_checks.py` (otvory, kameny bez podpory, ostroh), `tools/checks/preview3d.py` a `check_blocks.py` (náhledy).
- **Terén:** `TERRAIN_FROM_LEVEL = True`. Build změří landscape v levelu a uloží `terrain_from_level.json`. Capture používá stejný uložený stav.
- **Ruční úpravy v levelu:**
  - bourací objemy (Trigger Box s tagy `Ruin_*`),
  - `capture_manual_edits()` → `manual_edits.json`,
  - `tools/ruin/export_level_layout.py` → `layout_from_level.json` (posunuté zdi + body `RuinPt_<Zed>_<NN>`).
- **Kde leží soubory:** `GameDesign/Claude outputs/Lapikus` a kopie v `skvt_projekt/PrototypeDesigns/Lapikus` (`03_ruin`, `tools/ruin`). Odtud se spouští v UE.

## Půdorys v3 (11/2026)

- **Strážní věž se dvěma branami** (asi 7 × 7 m, SV od hlavní věže):
  - `Brana_V`: 1. brána z východu, `plinth` 2 m (stojí na nižším terénu, most nebo rampa přes příkop),
  - `Brana_S`: severní stěna,
  - `Brana_J`: 2. brána na západ do uličky podél severní strany věže,
  - `Brana_Jih`: jižní stěna.
- **`Hradba_V`** vede od jižní stěny strážní věže obloukem k JV rohu hlavní věže, asi 5–7 m od věže.
- **`Hradba_Z_S`** končí pootočeným úsekem 08 a napojením na SZ roh strážní věže.
- **Vstup do hlavní věže:** průlom 1,6 × 2,45 m ve `Vez_S` (s = 8,0 m), pod původními dveřmi v 1. patře (s = 7,62 m). Mezi vrchem průlomu a kapsami ochozu (3,85 m) zůstává 1,4 m zdiva.
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
- **Všechno najednou (15. 11. 2026):** `build_normal.py` v kořeni postaví hrad (03) i stavby (05) aditivně, `build_fullscope.py` je oprava (smaže generované actory a knihovní meshe a vše postaví znovu). Společná logika je v `zrlib/pipeline.py`.
- **Spouštění po stavbách:** `05_constructions/stavby/<Stavba>.py` (`Vez_Patra`, `Ostroh_Krov`, `Ostroh_Dostavba`, `Ostroh_Podlaha`, `Sut`) postaví jen jednu stavbu. `build_constructions.py` postaví všechny.

## Otevřené / další kroky

- Provizorní hlídková konstrukce na `Brana_S` (05_constructions).
- Most nebo rampa k 1. bráně, zbytky mostního pilíře v příkopu.
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

- **Návrh:** `new_designs/navrh_palac_kovarna.md`. V kap. 0 je přehled, co je hotové a co zbývá. Staví se po krocích: úprava 03 a přístřešek bez krytiny → výheň → krytina → stěna z proutí a okap → vybavení a úklid suti. Hotové jsou první čtyři kroky, zbývá vybavení a úklid suti.
- **Úprava zříceniny (03, část `Palac`, 15. 11. 2026):**
  - celá `Palac_J` je zanořená o jednu řadu kamene do země (`z_offset` −0,31 m): posunutá po ose Z jako celek i se střílnami a výklenky, počet řad se nemění;
  - u věže je koruna `Palac_J` rozebraná (`breaches` s = 29,6–33, `floor` 6,1): vychází 5,2 m v s = 28,5–29,3 a 4,0–4,8 m dál k věži, komín kovárny (5,5 m) ji přesahuje;
  - ve vnitřním líci `Palac_J` je kapsa pro východní pozednici kovárny (s = 30,55; řada 4,04–4,43 m nad terénem), `protect` nad ní drží jednu řadu kamene;
  - parametr zdi `drop_rows` (horní kameny každé vrstvy pryč, `zr_ruin/post.py`) je v kódu, žádná zeď ho nepoužívá;
  - obojí je v `tools/ruin/palac_spec.py` → `ruin_edits`, do `ruin_layout.json` to zapisuje `gen_layout.py`;
  - **koruny `Palac_J` v návrhu domu (`navrh_palac_obydli_stred.md`) jsou tím o 0,31 m výš než skutečnost.**
- **Přístřešek (15. 11. 2026):** 05 `Palac_Kovarna_Pristresek` (typ `pult_roof`, `05_constructions/zr_stavby/pult.py`) v koutě mezi `Palac_J` a věží:
  - východní pozednice 20 × 20 cm s vrchem ve 4,24 m (spodek na spáře řad zdi): jižní konec 0,3 m v kapse `Palac_J`, severní na sloupu (s = 30,55; n = 5,3). V koutě sloup není,
  - 3 sloupy 18 × 18 cm na západě (s = 25,85; n = 0,9 / 3,1 / 5,3) s pozednicí ve 2,5 m,
  - 6 krokví z loupané kulatiny Ø 16 cm, sklon 20,3° k západu, přesah 0,9 m (pod ním bude zvenku u západní stěny hranice dřeva),
  - pod každým sloupem patní kámen jako samostatný actor (dá se doladit a uložit přes capture),
  - krytina (večer 15. 11. 2026): latě, prkna po spádu s lištami přes spáry, prostup komína s mezerou 3 cm, okapová hrana s = 24,85; od líce `Palac_J` 3,5 cm (kameny koruny v s = 27–29 leží v úrovni střechy a vystupují z líce), lemování prknem na stojato u věže a podél `Palac_J`,
  - všechno dřevo bez úpravy (`raw`).
- **Výheň (15. 11. 2026):** 05 `Palac_Kovarna_Vyhen` (typ `hearth`, `05_constructions/zr_stavby/ohniste.py`) **v koutě místnosti**:
  - kamenný stůl s = 29,75–30,73; n = 0,72–1,9; výška 0,75 m, hliněný maz, ohniště 0,4 × 0,4 m pod komínem,
  - výklenek střílny s = 29 hned vedle stolu zůstává volný (manipulační prostor),
  - boční zídka n = 1,9–2,2, výška 1,2 m, s otvorem pro výfučnu,
  - dymník 1,4 × 1,2 m se spodním okrajem 1,8 m, visí na 4 závěsných tyčích z výměn mezi krokvemi n = 0,9 a 1,8,
  - komín 0,5 × 0,5 m, střed s = 30,0; n = 1,35, vrch 5,5 m. Rozebranou korunu `Palac_J` přesahuje o 0,3–1,5 m.
- **Stěna a okap (15. 11. 2026, večer):**
  - 05 `Palac_Kovarna_Stena` (typ `wattle_wall`, `zr_stavby/stena.py`): proutí s hlínou v s = 25,85; n = 0,7–5,4, výška 2,1 m, dílce mezi sloupy, kůly na spojích,
  - 05 `Palac_Kovarna_Okap` (typ `gutter`, `zr_stavby/okap.py`): loupaný žlab Ø 20 cm v s = 24,8; n = 0,72–5,9 se spádem 1,5 % k severu na třech rozsochách, sud na vodu pod jeho koncem (samostatný actor), svod se nedělá.
- **Rozměry:** `tools/ruin/palac_spec.py` (rám paláce `s` / `n`, konstanty `K_*`, `J_SINK`, `J_BREACH`), data generuje `gen_layout.py` (03) a `tools/constructions/gen_constructions.py` → `palac` (05).
- **Spuštění v UE:** `03_ruin/blocks/casti/Palac.py`, pak `05_constructions/stavby/Palac_Kovarna_Pristresek.py`, `Palac_Kovarna_Vyhen.py`, `Palac_Kovarna_Stena.py`, `Palac_Kovarna_Okap.py` a `Sut.py`. Úprava 03, kostra a výheň ověřené v UE (Jirka 15. 11. 2026); krytina, stěna a okap jen mimo UE (`run_checks.py`, náhled `05_constructions/Stavby_palac_kovarna_nahled.png`).
- **Zbývá:** rozmístění vybavení, úklid suti (suť teď leží i pod výhní).

## Palác – dům posádky v prostřední místnosti (11/2026)

- **Návrh a plán po etapách:** `new_designs/navrh_palac_obydli_stred.md`, kap. 0 (platí přednostně před staršími kapitolami).
- **Etapy = tři sady actorů** s tagy `stage:base` (stojí už v etapě 1 a zůstává), `stage:final` (dostavba) a `stage:site` (staveniště). Etapa 1 = `base` + `site`, etapa 2 = `base` + `final`. Přepíná se v Blueprintu. Sady: `zrlib/config.py` → `STAGES`.
- **Zřícenina se kvůli domu nemění.** Plánované snížení koruny `Palac_J` u komína odpadlo, po zanoření zdi je koruna u komína 4,4–4,8 m.
- **Krok 1 hotový (16. 11. 2026), sada `base`:**
  - 05 `Palac_Obydli_Kamen` (typ `stone_fill`, `05_constructions/zr_stavby/zdivo.py`): obě příčky srovnané kamenem na 1,4 m včetně zazděných dveří, podezdívky severní stěny (osa n = 6,2, vchod s = 13,8–14,8) a příčky (osa s = 15,75, dveře n = 3,3–4,3);
  - 05 `Palac_Obydli_Ohniste` (typ `hearth`): kamenný základ 1,4 × 1,4 × 0,5 m u jižní zdi ve světnici (s = 16,2–17,6), studené ohniště; dymník a komín přijdou s krovem do sady `final`;
  - suť v domě a na zápraží uklizená.
- **Spuštění v UE:** `05_constructions/stavby/Palac_Obydli_Kamen.py`, `Palac_Obydli_Ohniste.py`, pak `Sut.py`. Ověřeno jen mimo UE (`run_checks.py --only obydli`, náhled `05_constructions/Stavby_palac_obydli_nahled.png`).
- **Zbývá:** krov, srub se štíty, krytina, dymník a komín, strop, podlaha, okap, vybavení, staveniště.

## Optimalizace do budoucna (zatím není potřeba)

- **Stav 11/2026:** zřícenina má asi 23 500 kamenů a 34,5 mil. trojúhelníků. Z toho připadá 24,7 mil. na lomové kameny (`SM_RuinStone`), 6,2 mil. na korunu (`_W`) a 3,4 mil. na ostění (`SM_RuinDressed`). Dřevo ve věži má asi 0,5 mil. Unikátních meshí je jen 33, zbytek jsou instance. S Nanite to není problém.
- **Kdy na to sáhnout:** ray tracing (Lumen Hardware), platforma bez Nanite, Merge Actors, export.
- **Hint:** v `tools/meshes/mesh_stone.py` dát běžnému kameni (`SM_RuinStone_R*`) hrubší síť na plochách a jemnější jen v pásu zaoblení hran. Stejně se to už dělá u `_W` (funkce `grid` podle úhlu). Ušetří se 40–50 % trojúhelníků, celkem by vyšlo asi 18–20 mil. Pak zvýšit `STONE_MESH_VERSION` pro `SM_RuinStone_R` a skript meshe přeimportuje sám.
- Korunu a ostění nechat, jsou vidět zblízka. Skryté jádro je už teď jen kostka.
