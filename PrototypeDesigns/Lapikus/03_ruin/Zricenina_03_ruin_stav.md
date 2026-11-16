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

- Provizorní hlídková konstrukce nad branami: rozestavěno, viz kapitola „Brána – strážní stanoviště“.
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

- **Návrh:** `new_designs/navrh_palac_kovarna.md`. V kap. 0 je přehled, co je hotové a co zbývá. Staví se po krocích: úprava 03 a přístřešek bez krytiny → výheň → krytina → stěna z proutí a okap → vybavení a úklid suti. Hotové jsou všechny kroky (16. 11. 2026).
- **Úprava zříceniny (03, část `Palac`, 15. 11. 2026):**
  - celá `Palac_J` je zanořená o jednu řadu kamene do země (`z_offset` −0,31 m): posunutá po ose Z jako celek i se střílnami a výklenky, počet řad se nemění;
  - u věže je koruna `Palac_J` rozebraná (`breaches` s = 29,6–33, `floor` 6,1): vychází 5,2 m v s = 28,5–29,3 a 4,0–4,8 m dál k věži, komín kovárny (5,5 m) ji přesahuje;
  - ve vnitřním líci `Palac_J` je kapsa pro východní pozednici kovárny (s = 30,55; řada 4,04–4,43 m nad terénem), `protect` nad ní drží jednu řadu kamene;
  - parametr zdi `drop_rows` (horní kameny každé vrstvy pryč, `zr_ruin/post.py`) je v kódu, žádná zeď ho nepoužívá;
  - obojí je v `tools/ruin/palac_spec.py` → `ruin_edits`, do `ruin_layout.json` to zapisuje `gen_layout.py`;
  - **koruny `Palac_J` v návrhu domu (`navrh_palac_obydli_stred.md`) jsou tím o 0,31 m výš než skutečnost.**
- **Přístřešek (15. 11. 2026):** 05 `Palac_Kovarna_Pristresek` (typ `pult_roof`, `05_constructions/zr_stavby/pult.py`) v koutě mezi `Palac_J` a věží:
  - východní pozednice 20 × 20 cm s vrchem ve 4,24 m (spodek na spáře řad zdi): jižní konec 0,3 m v kapse `Palac_J`, dál na sloupech u věže (s = 30,55; n = 4,4 a 6,2). V koutě sloup není,
  - 3 sloupy 18 × 18 cm na západě (s = 25,85; n = 0,9 / 3,55 / 6,2) s pozednicí ve 2,5 m,
  - 7 krokví z loupané kulatiny Ø 16 cm (n = 0,9–6,3, rozšíření o řadu krokví k severu (Jirka 16. 11. 2026)), sklon 20,3° k západu, přesah 0,9 m (pod ním bude zvenku u západní stěny hranice dřeva),
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
  - 05 `Palac_Kovarna_Stena` (typ `wattle_wall`, `zr_stavby/stena.py`): proutí s hlínou v s = 25,85; n = 0,7–6,3, výška 2,1 m, dílce mezi sloupy, kůly na spojích,
  - 05 `Palac_Kovarna_Okap` (typ `gutter`, `zr_stavby/okap.py`): loupaný žlab Ø 20 cm v s = 24,8; n = 0,72–6,8 se spádem 2,5 % k severu na třech rozsochách (n = 1,7 / 4,0 / 6,3; jižní 1 m od líce `Palac_J`, průchod ke střílně), sud na vodu pod jeho koncem (samostatný actor), svod se nedělá.
- **Rozměry:** `tools/ruin/palac_spec.py` (rám paláce `s` / `n`, konstanty `K_*`, `J_SINK`, `J_BREACH`), data generuje `gen_layout.py` (03) a `tools/constructions/gen_constructions.py` → `palac` (05).
- **Spuštění v UE:** celá kovárna `05_constructions/stavby/Palac_Kovarna.py` (s `RUIN = True` i část zříceniny `Palac`, se `SUT = True` i suť), jednotlivě `Palac_Kovarna_Pristresek.py`, `_Vyhen`, `_Stena`, `_Okap`, `_Kul` a `Sut.py`, vybavení `06_furnishing/vybaveni/Palac_Kovarna.py`. Úprava 03, kostra a výheň ověřené v UE (Jirka 15. 11. 2026); krytina, stěna, okap a vybavení jen mimo UE (`run_checks.py`, náhled `05_constructions/Stavby_palac_kovarna_nahled.png`).
- **Vybavení (16. 11. 2026, od večera v `06_furnishing`):** skupina `Palac_Kovarna_Vybaveni` (typ `props`), samostatné actory: kovadlina na špalku (1,5 m před výhní), kalicí sud, hřebovnice na špalku, měchy s výfučnou v otvoru zídky a pákou na laně z krokve, šlapací brus se stoličkou, ponk, truhlík s uhlím a volným víkem, koš, lišta s nářadím a železné pruty u jižní zdi, zvenku pod přesahem hranice dřeva od kůlu (kůl je pevný, 05 `Palac_Kovarna_Kul`) k okraji střechy. Suť v celé východní místnosti uklizená (`clear_poly` u přístřešku). Spuštění a ruční posuny: `06_furnishing/vybaveni/Palac_Kovarna.py` (`MODE` `build` / `capture` / `list` / `reset`).
- **Zbývá:** ověření kroků 2–4 v UE; odloženo žhavé uhlí, oheň a kouř, udusaná hlína.

## Palác – dům posádky v prostřední místnosti (11/2026)

- **Návrh a plán po etapách:** `new_designs/navrh_palac_obydli_stred.md`, kap. 0 (platí přednostně před staršími kapitolami). **Předání staviteli** (co zbývá, na co si dát pozor): `new_designs/predani_palac_obydli_stavitel.md`.
- **Etapy = tři sady actorů** s tagy `stage:base` (stojí už v etapě 1 a zůstává), `stage:final` (dostavba) a `stage:site` (staveniště). Etapa 1 = `base` + `site`, etapa 2 = `base` + `final`. Přepíná se v Blueprintu. Sady: `zrlib/config.py` → `STAGES`.
- **Úpravy zříceniny kolem domu (03, část `Palac`, 16. 11. 2026):**
  - vstupní oblouk (portál) je přesunutý do západní místnosti: `Palac_S` s = 4,5, zeď kolem něj do 4,2 m;
  - ve střední místnosti ho posádka rozebrala na stavbu: v `Palac_S` v s = 16 zůstal hrubý průchod 1,8 m až k zemi v nízké zdi;
  - `Palac_pricka_2` je severně od domu rozebraná: hrubý průchod n = 6,9–8,5 ze zápraží na dvorek kovárny, po stranách zbytky zdi (`D_PASS` v `palac_spec.py`).
  - Plánované snížení koruny `Palac_J` u komína odpadlo, po zanoření zdi je koruna u komína 4,4–4,8 m.
- **Krok 1 hotový (16. 11. 2026), sada `base`:**
  - 05 `Palac_Obydli_Kamen` (typ `stone_fill`, `05_constructions/zr_stavby/zdivo.py`): obě příčky srovnané kamenem na 1,4 m včetně zazděných dveří, podezdívky severní stěny (osa n = 6,2, vchod s = 13,4–14,4) a příčky (osa s = 14,85, dveře n = 3,3–4,3);
  - 05 `Palac_Obydli_Ohniste` (typ `hearth`): od 16. 11. 2026 **pec s nístějí** u jižní zdi ve světnici (osa s = 16,76): kamenný sokl 1,6 × 1,6 × 0,6 m, pec 1,4 × 1,0 m s hliněnou klenbou (mesh `SM_RuinOvenDome`) a ústím k severu, nístěj s železnou plotnou na zídkách (sada `base`); sopouch, dymník, komín 0,5 m do 5,3 m a železo (sada `final`); plotna a poklop ústí s dřevěnou rukojetí (mesh `SM_RuinOvenDoor`) jsou samostatné actory;
  - stará zeď je vyspravená maltou: maltové jádro 6 cm v ose příček a podezdívek od země až pod vrch (i přes zříceninu pod novým zdivem), zdí neprosvítá;
  - suť v domě a na zápraží uklizená.
- **Kroky 2 a 3 hotové (16. 11. 2026), krov bez krytiny a srub:**
  - 05 `Palac_Obydli_Krov` (typ `pult_roof`, spád 16° k severu): 5 sloupů u `Palac_J` (s = 11,1 / 13,0 / 15,3 / 18,0 / 20,4), horní pozednice (vrch 4,03 m) a střední vaznice (vrch 3,02 m, na špalcích na stěnách) ze dvou kusů, 12 hraněných krokví 18 × 22 cm, 2 řady latí nad světnicí;
  - 05 `Palac_Obydli_Srub` (typ `log_wall`, `05_constructions/zr_stavby/srub.py`): severní stěna (9 řad do 2,5 m), příčka, srub na obou srovnaných příčkách (1,4–2,5 m), prkenné štíty; vchod, dveře v příčce a dvě okénka zarovnané na řady;
  - sady etap: nad světnicí a kolem ní `base` (stěny v plné výšce, východní kusy pozednice a vaznice, 6 krokví, latě), v síni `base` jen sloupy a spodní 3 řady severní stěny (1,16 m); zbytek `final`;
  - boční stěny a příčka začínají a končí půltrámem, v nárožích se tak kulatiny střídají se severní stěnou.
- **Větší světnice (Jirka 16. 11. 2026):** příčka je v s = 14,85 (dřív 15,75), západně od středního sloupu krovu, který tak stojí ve světnici. Světnice má 5,63 m, síň 3,83 m. Vchod je v s = 13,4–14,4, okénko světnice v s = 17,5–18,1 (uprostřed stěny).
- **Přepnutí etapy v editoru:** `05_constructions/stavby/Etapa.py` (`ETAPA` 1 / 2 / 0), po buildu pustit znovu.
- **Okap domu:** spád k západu (od kovárny), sud pod západním koncem, svod se nedělá (Jirka 16. 11. 2026). Zatím nepostavený.
- **Spuštění v UE:** po změně zříceniny nejdřív `03_ruin/blocks/casti/Palac.py`, pak celý dům `05_constructions/stavby/Palac_Obydli.py` (se `SUT = True` i suť), jednotlivě `Palac_Obydli_Kamen.py`, `Palac_Obydli_Krov.py`, `Palac_Obydli_Ohniste.py`, `Palac_Obydli_Srub.py` a `Sut.py`. Navázání kamene potvrzené v UE (Jirka 16. 11. 2026), krov a srub jen mimo UE (`run_checks.py --only obydli`, náhledy `05_constructions/Stavby_palac_obydli_nahled.png` a `Stavby_palac_obydli_nahled_etapa1.png`).
- **Zbývá:** krytina a lemování (s prostupem komína), strop (se zavěšením dymníku), podlaha, okap, vybavení (dveře, okenice, zárubně), staveniště.

## Brána – strážní stanoviště nad oblouky (11/2026)

- **Návrh a stav:** `new_designs/navrh_brana_straz.md`, kap. 0 (platí přednostně). Rozměry `tools/ruin/brana_spec.py`, výšky absolutně v UE cm.
- **Úprava zříceniny (03, část `Obvod`, 16. 11. 2026):** 3 kapsy pro trámy podesty ve vnitřním líci `Brana_V` (spodek Z 3552, řada nad obloukem brány; otvor s klíčem `z_abs` = absolutní výška spodku, `zr_ruin/prep.py`) a rozebrané SV nároží `Brana_V` (`cap`: v d < 0,75 jen řady pod Z 3618), aby kryt z kulatiny šel přes nároží. Ostatní zdi se nezměnily.
- **Krok 1 hotový (16. 11. 2026):** 05 `Brana_Straz_Kamen` (vyrovnání koruny `Brana_J` na Z 3552, podložení trámů v líci `Brana_V`) a 05 `Brana_Straz_Podesta` (typ `platform`, `05_constructions/zr_stavby/podesta.py`): 3 trámy Ø 24 cm v kapsách a čtvrtý na vyrovnané koruně `Brana_S`, prkna od severního krytu (d = −0,55) po d = 5,25, vrch podlahy Z 3581. Zábradlí směrem do hradu se nestaví (bude tam výlez). Sada `base`.
- **Krok 2 hotový (16. 11. 2026):** 05 `Brana_Straz_Kryty` (typ `palisade`, `05_constructions/zr_stavby/kryty.py`): východní kryt z 30 kůlů s kůrou na koruně `Brana_V`, vrch 1,8 m nad podlahou, 3 průzory s rovně seříznutým kůlem, sada `base`; severní kryt po celé délce u vnější hrany `Brana_S` (vrch 1,25 m, 3 průzory) a jižní kryt na okraji podesty ve východních dvou třetinách (vrch 1,8 m, 2 průzory), oba sada `final`. Ráhna zevnitř u spodu a těsně pod průzory, kůly zapuštěné 25 cm do koruny.
- **Spuštění v UE:** `05_constructions/stavby/Brana_Straz.py` s `RUIN = True` (přestaví `Obvod` kvůli kapsám), jednotlivě `Brana_Straz_Kamen.py`, `Brana_Straz_Podesta.py`, `Brana_Straz_Kryty.py`. Ověřeno jen mimo UE (`run_checks.py --only brana`, náhledy `05_constructions/Stavby_brana_straz_nahled.png` a `Stavby_brana_straz_nahled_etapa1.png`). Podestu a východní kryt viděl Jirka v UE 16. 11. 2026, úpravy po jeho připomínkách ne.
- **Zbývá:** přístřešek z kůry, zátaras, staveniště, výstup na podestu.

## Optimalizace do budoucna (zatím není potřeba)

- **Stav 11/2026:** zřícenina má asi 23 500 kamenů a 34,5 mil. trojúhelníků. Z toho připadá 24,7 mil. na lomové kameny (`SM_RuinStone`), 6,2 mil. na korunu (`_W`) a 3,4 mil. na ostění (`SM_RuinDressed`). Dřevo ve věži má asi 0,5 mil. Unikátních meshí je jen 33, zbytek jsou instance. S Nanite to není problém.
- **Kdy na to sáhnout:** ray tracing (Lumen Hardware), platforma bez Nanite, Merge Actors, export.
- **Hint:** v `tools/meshes/mesh_stone.py` dát běžnému kameni (`SM_RuinStone_R*`) hrubší síť na plochách a jemnější jen v pásu zaoblení hran. Stejně se to už dělá u `_W` (funkce `grid` podle úhlu). Ušetří se 40–50 % trojúhelníků, celkem by vyšlo asi 18–20 mil. Pak zvýšit `STONE_MESH_VERSION` pro `SM_RuinStone_R` a skript meshe přeimportuje sám.
- Korunu a ostění nechat, jsou vidět zblízka. Skryté jádro je už teď jen kostka.
