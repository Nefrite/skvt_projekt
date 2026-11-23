---
# orchestrace
type: state
validity: valid
updated: 2026-11-23
aliases: []
# hra
domain: structures
entity: "[[Palac_Obydli]]"
depth: 3
build_step: 05_constructions
assets: []
---
# Palac_Obydli – stav stavby

## Souhrn
Stav stavby domu posádky k 21. 11. 2026 proti návrhu [[navrh_palac_obydli_stred]] a [[navrh_palac_obydli_stavenisko]]. Kámen, krov bez krytiny, srub a pec jsou postavené a Jirka je 21. 11. 2026 v UE vizuálně zkontroloval; staveniště etapy 1 a uhlí pod plotnou jsou ověřené jen mimo UE.
- **Co je hotové:** tabulka staveb a sad, podrobnosti kroků 1–3.
- **Specifikace:** rozměry v `tools/ruin/palac_spec.py`, data, spouštěče, kontroly a náhled (sekce *Souhrn specifikace*, *Spuštění v UE*).
- **Odchylky:** od kap. 4 návrhu a od návrhu staveniště (sekce *Co se liší od návrhu*).
- **Zbývá:** vizuální kontrola staveniště v UE, pak krytina, strop, podlaha, okap, zárubně a vybavení (fronta předání [[predani_palac_obydli_1_etapa1_ue]] až [[predani_palac_obydli_7_vybaveni]]).

## Co je hotové
| Stavba | Typ, modul | Obsah | Sady |
|---|---|---|---|
| 03 část `Palac` | `gen_layout.py`, `palac_spec.ruin_edits` | portál přesunutý do západní místnosti (`Palac_S` s = 4,5), hrubý průchod v `Palac_S` s = 16, průchod v `Palac_pricka_2` n = 6,9–8,5 ke kovárně | – |
| `Palac_Obydli_Kamen` | `stone_fill`, `zr_stavby/zdivo.py` | obě příčky srovnané na 1,4 m, podezdívky severní stěny a příčky, maltové jádro v ose | `base` |
| `Palac_Obydli_Krov` | `pult_roof`, `zr_stavby/pult.py` | 5 sloupů na patních kamenech, horní pozednice a střední vaznice ze dvou kusů, 3 špalky pod vaznicí, 12 krokví, 2 řady latí nad světnicí. **Bez krytiny.** | `base` / `final` |
| `Palac_Obydli_Ohniste` | `hearth`, `zr_stavby/ohniste.py` | pec s nístějí: sokl, zdi pece, klenba (`SM_RuinOvenDome`), zídky plotny; sopouch, dymník, komín, pás nad ústím, plotna a poklop | kámen, klenba a tmavý vnitřek pece `base`; ostatní včetně uhlí pod plotnou (box `U`) `final` |
| `Palac_Obydli_Srub` | `log_wall`, `zr_stavby/srub.py` | severní stěna, příčka, srub na obou bočních stěnách, prkenné štíty, otvory zarovnané na řady | `base` / `final` |
| `Palac_Obydli_Stavenisko`, `_Kulatina`, `_Tramy`, `_Prkna`, `_Kozy` | `props`, `zr_stavby/vybaveni.py` | staveniště etapy 1: vzpěry V1–V4 sloupů 11,1 a 13,0, žebřík ve světnici, na nádvoří před `Palac_S` hranice srubové kulatiny (S3), tesaného dřeva krovu (S4) a jedna hranice prken na krytinu (S5, 75 prken, vrch 1,375 m; poloha z levelu, Jirka 21. 11. 2026); kozy s rozpracovanou kulatinou (S6, mesh `SM_RuinLogPeeling`) a pruhy kůry. Rozměry `palac_spec.py` → `D_SITE`, `obydli_stavenisko()` | `site` |

- **Samostatné actory** (ruční doladění, `MODE = "capture"` ve spouštěči stavby): patní kameny sloupů, plotna (`Palac_Obydli_Ohniste|I2`), poklop ústí (`Palac_Obydli_Ohniste|Poklop`, mesh `SM_RuinOvenDoor`: plech s dřevěnou rukojetí, opřený o čelo pece západně od ústí).
- **Nové meshe** (naimportují se při buildu samy): `meshes/wattle/SM_RuinOvenDome_A/B.obj`, `meshes/props/SM_RuinOvenDoor_A.obj`, `meshes/wood/SM_RuinLogPeeling_A/B.obj` (rozpracovaná kulatina, 21. 11. 2026).
- **Staveniště:** vzpěry a žebřík jsou samostatné actory. Každá hranice je samostatná stavba a v UE jeden actor (pivot dole uprostřed, tag `pile:<stavba>`) ve složce `Stavby/Palac/Obydli/Stavenisko`. Po posunu nebo natočení v UE uložit přes `Palac_Obydli_Stavenisko_Capture.py`. Suť pod původní polohou hranic na nádvoří je uklizená (`clear_poly`).
- **Přepnutí etapy v editoru:** `05_constructions/stavby/Etapa.py` (`ETAPA` 1 / 2 / 0). Po každém buildu pustit znovu.
- **Náhledy:** `05_constructions/Stavby_palac_obydli_nahled.png` (etapa 2), `Stavby_palac_obydli_nahled_etapa1.png` (etapa 1 se staveništěm, 21. 11. 2026).

### Krok 1 (z návrhu kap. 0.5)

- **Srovnání příček** (`W`, `E`): s = 10,1–10,9 a 20,6–21,4; n = 0,72–6,43; vrch 1,4 m. Kámen z rozvalin ve dvou řadách přes tloušťku 0,8 m, spodek kopíruje korunu zříceniny, v místě dveří příček stojí zdivo od země.
- **Podezdívka severní stěny** (`N`): osa n = 6,2; s = 10,9–20,6; 0,45 × 0,45 m; vchod s = 13,8–14,8 volný.
- **Podezdívka příčky** (`P`): osa s = 15,75; n = 0,72–5,98; dveře n = 3,3–4,3 volné.
- **Základ ohniště**: s = 16,2–17,6; n = 0,72–2,1; výška 0,5 m ve 2 řadách, maz 4 cm, uprostřed studené ohniště 0,5 × 0,5 m.
- **Suť** v domě a na zápraží je uklizená (`clear_poly`).
- **Vyspravení staré zdi maltou** (Jirka 16. 11. 2026, jako u `Ostroh_Dostavba`): v ose obou příček i podezdívek je maltové jádro 6 cm (`mortar`, materiál `MI_RuinCore`) od země až 2 cm pod vrch. Prochází novým zdivem i starou příčkou pod ním; kde staré zdi chybí jádro, vyplní dutinu mezi líci. Zdí tak neprosvítá. Ve dveřích a ve větší díře skrz zeď malta není.
- Rozměry: `tools/ruin/palac_spec.py` (`D_*`, `obydli`). Kontrola: `run_checks.py --only obydli`. Náhled: `preview3d.py obydli <out.png> [--stage 1|2]`, `05_constructions/Stavby_palac_obydli_nahled.png`.
- V UE: celý dům `05_constructions/stavby/Palac_Obydli.py` (seznam hotových částí v pořadí, se `SUT = True` i suť); jednotlivě `Palac_Obydli_Kamen.py`, `Palac_Obydli_Krov.py`, `Palac_Obydli_Ohniste.py`, `Palac_Obydli_Srub.py`, pak `Sut.py`. Navázání kamene potvrzené v UE (Jirka 16. 11. 2026), ostatní neověřeno.

### Kroky 2 a 3: krov bez krytiny a srub (z návrhu kap. 0.6)

Všechno je ve skriptech a prošlo kontrolami mimo Unreal, v UE zatím nic z toho neběželo. Náhledy: `05_constructions/Stavby_palac_obydli_nahled.png` (etapa 2) a `Stavby_palac_obydli_nahled_etapa1.png` (etapa 1).

**Krov `Palac_Obydli_Krov`** (typ `pult_roof`, spád 16,0° k severu, všechno dřevo `raw`):

| Dílec | Rozměr a poloha | Sada |
|---|---|---|
| 5 sloupů 20 × 20 cm na patních kamenech | n = 0,85; s = 11,1 / 13,0 / 15,3 / 18,0 / 20,4; výška 3,73 m | `base` |
| horní pozednice 20 × 20 cm, vrch 4,03 m | západní kus s = 10,1–15,3, východní 15,3–21,4 (spoj nad středním sloupem) | západní `final`, východní `base` |
| střední vaznice 20 × 24 cm, vrch 3,02 m, n = 4,4 | západní kus s = 10,1–14,85, východní 14,85–21,4 (spoj nad příčkou) | západní `final`, východní `base` |
| 3 špalky 20 × 20 × 28 cm pod vaznicí | na vrchní řadě srubu západní stěny, příčky a východní stěny | západní `final`, ostatní `base` |
| 12 krokví 18 × 22 cm, délka 6,2 m | s = 10,2 až 21,3 po 1,01 m; n = 0,8–6,8 (přesah 0,6 m za severní stěnu), osedlání 3 cm | 6 nad světnicí `base`, 6 nad síní `final` |
| 2 řady latí (zavětrování) | n = 2,6 a 5,3; s = 16,17–21,4 | `base` |

**Srub `Palac_Obydli_Srub`** (typ `log_wall`, loupaná kulatina, `raw`):

| Stěna | Řady | Sada |
|---|---|---|
| severní, světnice (s = 14,85–21,45) | 9 řad od podezdívky do 2,5 m (4 řady po 24 cm do 1,4 m, 5 řad po 22 cm) | `base` |
| severní, síň (s = 10,05–14,85) | spodní 3 řady (vrch 1,16 m) s mezerou pro vchod | `base` |
| severní, síň | zbylých 6 řad | `final` |
| příčka (s = 14,85; n = 0,74–6,5) | 9 řad, první a poslední je půltrám | `base` |
| východní (na srovnané příčce, 1,4–2,5 m) | 4 řady kulatiny mezi dvěma půltrámy | `base` |
| západní | stejně | `final` |
| prkenné štíty (západní, východní, nad příčkou) | svislá prkna 20–28 cm od vrchu srubu pod vrch krokví, výřezy pro pozednici a vaznici | `final` |

- **Nároží jako u skutečného srubu:** boční stěny a příčka začínají a končí půltrámem (hraněný, 11 cm), jejich řady jsou proto o půl řady posunuté proti severní stěně. V nárožích se kulatiny střídají a zhlaví přesahují 0,3 m (náhodně ± 5 cm).
- **Zdí neprosvítá:** kulatina je o 1,2 cm tlustší než řada (překryv jako v drážce). Výplň spár mechem a hlínou se proto nestaví.
- **Otvory jsou zarovnané na řady:** vchod 1,0 × 2,28 m, dveře v příčce 1,0 × 2,17 m, okénko světnice 0,6 × 0,66 m (parapet 1,4 m), okénko síně 0,5 × 0,44 m (parapet 1,4 m) v s = 11,8–12,3. Okénko síně zůstává, kde je postavené, i když není přesně uprostřed stěny vlevo od vchodu (střed 12,15) (Jirka 21. 11. 2026). Zárubně, dveře a okenice přijdou s vybavením.

**Odchylky od kap. 4 (důvod):**

- střední sloup v s = 15,3 místo 15,6, spoj pozednice je nad ním; příčka je od 16. 11. 2026 západně od něj (kap. 0.5a);
- pozednice je dlouhá jako vaznice (s = 10,1–21,4 místo 10,9–20,6), aby na ní ležely i štítové krokve;
- vaznice leží na špalcích 28 cm (srub končí ve 2,5 m, spodek vaznice je ve 2,78 m);
- krokve začínají v n = 0,8 místo 0,75 (kameny líce `Palac_J` vystupují až o 5 cm);
- komín je v s = 16,76 (v 16,9 by zasáhl do krokve s = 17,26); stojí s pecí (kap. 0.5b), prostup krytinou přijde s krytinou;
- dveře v příčce mají světlou výšku 2,17 m místo 2,2 m (zarovnání na řady);
- štíty končí rovně pod vrchem krokví, u příčky zůstává pod krytinou stupňovitá mezera do 7 cm.

**Okap (rozhodnutí Jirky 16. 11. 2026, staví se v kroku 4):** žlab má spád k západu, od kovárny. Sud stojí pod jeho západním koncem, svod přes zápraží se nedělá. Cesta ze zápraží ke kovárně tak zůstává volná. Kap. 4.7 a poznámka o svodu v kap. 6 tím neplatí.

## Souhrn specifikace
| Co | Kde |
|---|---|
| rozměry domu (jediné místo, kde se mění čísla) | `tools/ruin/palac_spec.py`: `D_*`, `obydli()`, `_obydli_pec()`, `_obydli_drevo()` |
| data staveb | `tools/constructions/gen_constructions.py` → `palac()` → `05_constructions/constructions.json` (jen generátorem) |
| registr typů | `05_constructions/build_constructions.py` → `TYPES`, `REQUIRED`, `CNAME` |
| spouštěče | `05_constructions/stavby/Palac_Obydli.py` (seznam `STAVBY`), `Palac_Obydli_<Část>.py` |
| kontroly | `tools/checks/run_checks.py --only obydli` → `check_obydli` |
| náhled | `tools/checks/preview3d.py obydli <out.png> [--stage 1\|2]` → `obydli_scene` |

Rám paláce: `s` podél `Palac_J` k věži, `n` k severu, výšky v metrech nad terénem v `ref` (střed domu). Vnitřní líc `Palac_J` je n = 0,7, nové zdivo začíná v n = 0,72.

Postup po změně čísel: `gen_constructions.py` (argumenty: `03_ruin/ruin_layout_draft.json`, výstup, `03_ruin/blocks/ruin_layout.json`) → `run_checks.py` → náhled. Před přepsáním `constructions.json` vygeneruj do dočasného souboru a porovnej, že se změnily jen očekávané stavby (sdílené soubory může měnit i jiná session).

## Co se liší od návrhu (a proč)
Přesné rozměry a odchylky od původního návrhu: *Co je hotové* (krok 1, kroky 2 a 3), návrh kap. 4.5 (větší světnice) a 4.6 (pec), níže *Staveniště* ( pultramy S3 jako třetí vrstva, výšky hranic 0,72 / 0,58 / 1,375 m, jedna vyšší hranice prken, každá hranice jeden objekt posouvaný v UE, uklizená suť pod hranicemi).

### Staveniště: postavená verze a odchylky od návrhu 9.2 (21. 11. 2026, z návrhu kap. 9.2a)

Postaveno ve skriptech, kontroly kap. 9.4 procházejí (`run_checks.py --only obydli`), v UE zatím neověřeno.

- **Uhlí pod plotnou:** box `U` v `_obydli_pec` má příznak `top`, takže patří do sady `stage_top` (`final`). Typ `hearth` se neměnil, data kovárny jsou beze změny.
- **Data:** `palac_spec.py` → `D_SITE` a funkce `obydli_stavenisko()`. Délky, průměry a počty kusů S3 a S4 se počítají z dat sady `final`: krokve 6 × 6,24 m (0,18 × 0,22), pozednice 5,2 m, vaznice 4,75 m, srub síně 4 × 5,76 m a 5 × 4,80 m (Ø 0,23), 1 × 3,92 m (Ø 0,25) a 2 pultramy 5,76 × 0,22 × 0,11 m. Počet prken S5 se počítá vzorcem z kap. 9.2: 2 × 44.
- **Výšky** se měří od terénu v jednom bodě (nový klíč `ref` u položek typu `props`). Vzpěry a žebřík mají stejný ref jako krov a srub (střed domu), každá hranice svůj střed.
- **Hranice jako samostatné objekty (Jirka 21. 11. 2026, mění 9.2 Ruční doladění):** staveniště jsou čtyři stavby ve složce `Stavby/Palac/Obydli/Stavenisko`: `Palac_Obydli_Stavenisko` (vzpěry V1–V4 a žebřík jako samostatné actory, úklid suti) a hranice `_Kulatina` (S3, 14 kusů), `_Tramy` (S4, 14 kusů) a `_Prkna` (S5, 134 kusů). Každá hranice je jeden actor (Instanced Static Mesh) s pivotem dole uprostřed. V UE se posune nebo natočí kolem svislé osy jako celek. `Palac_Obydli_Stavenisko_Capture.py` uloží polohu do `constructions_edits.json` (klíč `pile:<stavba>`) a ta má přednost před `D_SITE`. Náklon hranice se neukládá.
- **Hranoly a prkna** umí typ `props` bez nového tvaru: dílec dřeva bez `shape` s rozměrem `size` dostane mesh `SM_RuinTimber` nebo `SM_RuinPlank` podle poměru stran.
- **S3:** pultramy neleží v horní vrstvě, ale naplocho jako třetí vrstva nad žlábky horní vrstvy (do horní vrstvy se 4 kusy kulatiny a 2 pultramy nevešly). Výška hranice je 0,72 m.
- **S4:** výška je 0,58 m, ne asi 0,7 m (4 krokve naplocho, proklady 5 cm, nahoře 2 krokve, pozednice a vaznice naplocho).
- **S5 (Jirka 21. 11. 2026):** jedna hranice prken 3,4 m v s = 18,0–21,4; n = 12,0–13,45, o 0,5 m vyšší než původní: 15 vrstev po 5 prknech (75 kusů), proklady 4 v každé mezeře mezi vrstvami, 3 podkladky. Vrch je ve výšce 1,375 m. Šířky prken jsou náhodné v rozmezí 0,22–0,30 a v každé vrstvě srovnané na šířku hranice 1,45 m. Původní varianta: dvě hranice po 44 prknech (3,4 m a 3,2 m), výška 0,87 m, `D_SITE` → `boards.variant = "two"`.
- **Žebřík:** pata v n = 3,13, vrchol n = 0,97 a z = 3,95, sklon 61,3°.
- **S6 kozy s rozpracovanou kulatinou (Jirka 21. 11. 2026):** stavba `Palac_Obydli_Stavenisko_Kozy`, jeden objekt jako ostatní hranice. Je to doplněk navíc, kulatina na kozách se nepočítá do kusů S3.
  - Kulatina 5,76 m Ø 0,23 m s kůrou, nahoře asi ve 2/3 délky oloupaná s nerovným okrajem kůry. Nový mesh `SM_RuinLogPeeling` (`mesh_log.py`, varianty A, B; oloupaná strana je +Z, nahoru).
  - Dvě kozy do X z tyčí s kůrou Ø 11 cm v s = 19,3 a 23,1: paty 0,40 m od osy, křížení ve výšce 0,63 m, vrchy tyčí 1,17 m. Kulatina leží ve vidlicích, osa ve výšce 0,95 m.
  - Pod kulatinou leží 5 pruhů kůry 55 × 16 cm (`SM_RuinBarkStrip`).
  - Výchozí poloha je na původním místě hranice prken (s = 18,3–24,1; n ≈ 12,85), protože prkna Jirka přemístil na s ≈ 12, n ≈ 18 (natočení 10°). Rozměry: `D_SITE` → `horses`.
- **Suť:** do obrysu S4 zasahoval kámen suti `Palac_S|R1` (s = 21,38; n = 10,63). Suť pod hranicemi je proto uklizená pomocí `clear_poly` (s = 8,4–25,1; n = 10,45–13,55). Suť nemá sady, chybí tedy v obou etapách.
- **Terén** pod hranicemi je v datech levelu rovný (Z 3129 cm, rozdíl 0 cm).

## Ověřeno v UE (ano/ne, kdy, kým)
Všechno je ve skriptech a prošlo `tools/checks/run_checks.py` (`SOUHRN: ... obydli OK`). **Kámen, krov, srub, pec, posun příčky a nové meshe jsou v UE postavené a Jirka je 21. 11. 2026 vizuálně zkontroloval: v pořádku, nic nechybí.** Čtení stavu v UE z téhož dne: 18 actorů, 12 `base`, 6 `final`.

**Staveniště a uhlí pod plotnou v sadě `final` (21. 11. 2026):** jen mimo UE. `run_checks.py --only obydli` OK včetně kontrol etapy 1 (kap. 9.4 návrhu), náhled etapy 1 hotový. Vizuální kontrola v UE zatím neproběhla.

**Kontroly etapy 1 mimo UE (z předání staviteli kap. 4, 21. 11. 2026):**

- ✅ Uhlí pod plotnou (box `U`) je v sadě `final` (příznak `top`, typ `hearth` beze změny, data kovárny beze změny).
- ✅ `Palac_Obydli_Stavenisko` (typ `props`, sada `site`): vzpěry V1–V4, žebřík; hranice S3, S4 a S5 jako samostatné stavby `_Kulatina`, `_Tramy`, `_Prkna`, každá jako jeden actor (Jirka 21. 11. 2026: rozmístí je podle game designu, uložení polohy a natočení `Palac_Obydli_Stavenisko_Capture.py`, `pile` v `build_constructions.py`; uložení polohy v UE zatím neověřené). Prkna jsou v jedné hranici o 0,5 m vyšší (75 kusů), původní dvě hranice zůstávají jako varianta v `D_SITE`. Jirka prkna přemístil a uložil (capture, 21. 11. 2026). Přibyly kozy s rozpracovanou kulatinou `_Kozy` (S6, nový mesh `SM_RuinLogPeeling`), návrh kap. 9.2a. Data: `palac_spec.py` → `D_SITE`, `obydli_stavenisko()`, generátor `palac()`, spouštěč `stavby/Palac_Obydli_Stavenisko.py`, v `STAVBY` za `Palac_Obydli_Srub`, tedy až po pecí.
- ✅ Počty z dat sady `final`: krokve 6, pozednice 1, vaznice 1, srub síně 10 + 2 pultramy; prkna 75 (aspoň 44 = jedna řada krytiny).
- ✅ Ověřeno: `props` umí hranoly a prkna. Terén pod hranicemi je rovný (rozdíl 0 cm).
- ✅ Kontroly kap. 9.4 v `check_obydli`: nic nevisí, 2 vzpěry na líci sloupů 11,1 a 13,0, trasy a volné pásy, kolize se zříceninou, `base`, kovárnou, vybavením i mezi sebou, terén, počty a délky, v etapě 2 nic ze `site`. Zkoušeno i na záměrně pokažených datech: kontroly chybu chytí.
- ✅ `run_checks.py --only obydli` OK. `--only palac` hlásí 4 chyby vybavení kovárny (06, polohy z levelu), které tam byly už před tímto krokem. Výstup je beze změny.
- ✅ Náhled `05_constructions/Stavby_palac_obydli_nahled_etapa1.png` (přidané pohledy na vzpěry a hranice).

## Spuštění v UE
- **Spuštění v UE:** po změně zříceniny nejdřív `03_ruin/blocks/casti/Palac.py`, pak celý dům `05_constructions/stavby/Palac_Obydli.py` (se `SUT = True` i suť), jednotlivě `Palac_Obydli_Kamen.py`, `Palac_Obydli_Krov.py`, `Palac_Obydli_Ohniste.py`, `Palac_Obydli_Srub.py`, `Palac_Obydli_Stavenisko.py` (celé staveniště; uložení ručních úprav `Palac_Obydli_Stavenisko_Capture.py`) a `Sut.py`. Navázání kamene potvrzené v UE (Jirka 16. 11. 2026), krov a srub jen mimo UE (`run_checks.py --only obydli`, náhledy `05_constructions/Stavby_palac_obydli_nahled.png` a `Stavby_palac_obydli_nahled_etapa1.png`).

## Co zbývá
Fronta předání v tomto pořadí: [[predani_palac_obydli_1_etapa1_ue]] (kontrola etapy 1 v UE), [[predani_palac_obydli_2_krytina]], [[predani_palac_obydli_3_strop]], [[predani_palac_obydli_4_podlaha]], [[predani_palac_obydli_5_okap]], [[predani_palac_obydli_6_zarubne]], [[predani_palac_obydli_7_vybaveni]]. Návrh staveniště: [[navrh_palac_obydli_stavenisko]].

## Odkazy na návrh a předání
- návrh: [[navrh_palac_obydli_stred]] (rozměry), plán po etapách [[navrh_palac_obydli_etapy]], pec [[navrh_palac_obydli_pec]], staveniště [[navrh_palac_obydli_stavenisko]]
- předání: fronta [[predani_palac_obydli_1_etapa1_ue]] až [[predani_palac_obydli_7_vybaveni]] (aktivní); dřívější [[predani_palac_obydli_stavitel]] (archivováno 2026-11-23)
