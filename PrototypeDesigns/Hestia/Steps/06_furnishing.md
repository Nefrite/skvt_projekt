---
# orchestrace
type: step
validity: valid
aliases: [README_furnishing]
step_kind: build
updated: 2026-11-23
# hra
build_step: 06_furnishing
domains: [structures]
---
# 06_furnishing – vybavení

## Účel kroku
Stav: 16. 11. 2026. Vybavení se od 16. 11. 2026 staví odděleně od dostaveb (05): **vybavení je všechno, co člověk přenese** (rozhodl Jirka). Pevné části staveb (výheň, sloupy, stěny, žlab, sud pod okapem, kůl zatlučený do země) zůstávají v `05_constructions`.

### 2. Jak to funguje

- Každý kus je **samostatný actor** s tagy `Zricenina_Vybaveni`, `vybaveni:<skupina>` a `id:<skupina>|<kus>`. Ve World Outlineru je ve složce `Vybaveni/...` (kovárna `Vybaveni/Palac/Kovarna`).
- Build smaže jen actory své skupiny a postaví je znovu podle `furnishing.json` a uložených ručních úprav. Navíc smaže staré actory stejné skupiny z doby, kdy vybavení bylo v 05 (tag `Zricenina_Stavby`, `stavba:Palac_Kovarna_Vybaveni`).
- Vybavení stojí ve stavbách 05 a bere z nich výšky (lano páky měchů visí z krokve střechy `Palac_Kovarna_Pristresek`, rámy čte z `05_constructions/constructions.json`). Stavby samo nemění.
- **Ruční doladění (od 16. 11. 2026, jeden JSON):** kusy v levelu posuň, otoč, změň jim velikost (Scale), smaž nebo zkopíruj (Alt+tah, Ctrl+D) a spusť skupinu s `MODE = "capture"`. Capture zapíše stav levelu **přímo do `furnishing.json`** (záloha `.bak`), další build postaví kusy přesně tam. Capture jen po buildu se stejnými meshi (`KNOWHOW_hrad.md` kap. 5.3).
  - **Poloha se ukládá v rámu skupiny**, stejně jako ve specu: `a`, `c` (s, n v m), `z` nad terénem (m; u kusů se `zc` střed), `x` = směr lokální osy X v rámu, `pitch`, `roll`; u úseků (páka, lana) koncové body `p0`, `p1` a průměr `d`. Kus se tak posune s rámem stavby a sedne na terén i po jeho změně.
  - **Velikost:** změna Scale actoru se zapíše jako násobek do `scale` (u kusů se `size` přímo do rozměrů); u úseků délka do `p0`/`p1` a tloušťka do `d`. Změny pod 0,5 % se ignorují.
  - **Příznaky kusu:** `captured` (poloha z levelu, `spec` = poloha podle specu), `removed` (v levelu smazaný, nestaví se), `manual` (kopie z levelu: id `<kus>_2`, `copy_of`, `mesh` = stejný mesh jako původní kus). Zkopírovanému actoru capture rovnou přepíše tag `id:` a jméno.
  - **Přegenerování dat** (`gen_furnishing.py`) JSON nepřepisuje, ale slučuje (`furn_data.merge`): rám skupiny a tvar kusů jdou ze specu, kusy s `captured` / `removed` si nechají polohu, kopie zůstanou, nové kusy ze specu přibudou. Kusy a skupiny, které ve specu už nejsou, zůstanou a vypíšou se; změna polohy ve specu u kusu s polohou z levelu se taky vypíše.
  - `MODE = "list"` vypíše kusy s polohou z levelu a jejich posun proti specu (s, n v m, z v cm, otočení, velikost), smazané a kopie.
  - `MODE = "reset"` vrátí kusy na spec (`ITEMS` = jen některé kusy, i s jejich kopiemi): zruší `captured` a `removed`, kopie smaže; záloha `.bak`. Pak znovu build.
  - Starý soubor `furnishing_edits.json` se už nepoužívá; když existuje, build i capture vypíšou upozornění.
- **Celý hrad:** `build_normal.py` a `build_fullscope.py` staví vybavení po stavbách 05 (`zrlib/pipeline.py` → `build_all`, `furnishing`). Fullscope maže i actory s tagem `Zricenina_Vybaveni`.

## Spouštění
### 4. Spuštění v UE

| Situace | Skript |
|---|---|
| jen vybavení kovárny | `06_furnishing/vybaveni/Palac_Kovarna.py` |
| celá kovárna včetně vybavení | `05_constructions/stavby/Palac_Kovarna.py` (`VYBAVENI = True`) |
| jen vybavení Guesthouse (graybox) | `06_furnishing/vybaveni/Guesthouse.py` |
| uložit ruční úpravy Guesthouse | `06_furnishing/vybaveni/Guesthouse_Capture.py` |
| jen vybavení strážního stanoviště nad bránou (graybox) | `06_furnishing/vybaveni/Brana_Straz.py` |
| uložit ruční úpravy vybavení brány | `06_furnishing/vybaveni/Brana_Straz_Capture.py` |
| celá strážnice nad bránou včetně vybavení | `05_constructions/stavby/Brana_Straz.py` (`VYBAVENI = True`) |
| uložit ruční úpravy | **`06_furnishing/vybaveni/Palac_Kovarna_Capture.py`**; jinak `Palac_Kovarna.py` s `MODE = "capture"`, nebo `Palac_Kovarna.py` v 05 s `MODE = "capture"` (uloží stavby do `constructions_edits.json` a vybavení do `furnishing.json`) |
| všechno vybavení | `06_furnishing/build_furnishing.py` |
| uložit úpravy všeho vybavení | `06_furnishing/capture_furnishing.py` (skupiny bez actorů v levelu přeskočí) |
| celý hrad | `build_normal.py` (`VYBAVENI = True` staví i vybavení; `CAPTURE_VYBAVENI = True` před buildem uloží úpravy z levelu), stejně `build_fullscope.py` |

### 5. Nová skupina vybavení

1. Kusy a polohy do specu stavby (funkce vracející seznam položek typu `props`, viz `kovarna_vybaveni()`; poloha = střed bounding boxu meshe, `KNOWHOW_hrad.md` kap. 5.7).
2. Skupinu do `tools/furnishing/gen_furnishing.py`, vygenerovat `furnishing.json` (existující data se sloučí, uložené polohy jiných skupin zůstanou).
3. Spouštěč `vybaveni/<Skupina>.py` (kopie `Palac_Kovarna.py`, jiný seznam `SKUPINY`); případně přidat do souhrnného spouštěče stavby v 05.
4. Kontroly do `run_checks.py` (vybavení je v `common.state()` pod klíčem `furn`).

## Skripty
<!-- hestia:generated:start -->

| Skript | Role | Entity | Dokumenty |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/06_furnishing/build_furnishing.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/06_furnishing/capture_furnishing.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/06_furnishing/furn_data.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Brana_Straz.py` | entry | [[Brana_Straz]] | [[navrh_brana_straz]], [[stav_brana_straz]], [[06_furnishing]] |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Brana_Straz_Capture.py` | entry | [[Brana_Straz]] | [[navrh_brana_straz]], [[stav_brana_straz]], [[06_furnishing]] |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Guesthouse.py` | entry | [[Guesthouse]] | [[navrh_guesthouse_vybaveni]], [[stav_guesthouse]], [[06_furnishing]], [[Katalog_props]] |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Guesthouse_Capture.py` | entry | [[Guesthouse]] | [[navrh_guesthouse_vybaveni]], [[stav_guesthouse]], [[06_furnishing]] |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Palac_Kovarna.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Palac_Kovarna_Capture.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/tools/furnishing/gen_furnishing.py` | generator | – | – |

<!-- hestia:generated:end -->

## Vstupy a výstupy
### 1. Soubory

| Soubor | Co dělá |
|---|---|
| `build_furnishing.py` | build, capture, výpis a vrácení na spec v UE; mimo UE statistika (`python build_furnishing.py`), `list`, `reset [kusy]` |
| `furn_data.py` | práce s `furnishing.json`: příznaky kusů, sloučení se specem (`merge`), vrácení na spec (`reset`), zápis se zálohou |
| `vybaveni\<Skupina>.py` | spuštění jedné skupiny vybavení: `Palac_Kovarna.py` (kovárna), `Guesthouse.py` (pokoj hosta u ostrohu), `Brana_Straz.py` (strážní stanoviště nad bránou). Nahoře `MODE` (`build` / `capture` / `list` / `reset`) a `ITEMS` (kusy pro `reset`) |
| `vybaveni\<Skupina>_Capture.py` | uložení ručních úprav skupiny z levelu (capture) bez přepínání `MODE`: `Palac_Kovarna_Capture.py`, `Guesthouse_Capture.py`, `Brana_Straz_Capture.py` |
| `furnishing.json` | **jediný zdroj poloh vybavení.** Sestaví ho `tools/furnishing/gen_furnishing.py` ze speců, capture do něj zapisuje polohy z levelu. Předchozí verze vždy v `furnishing.json.bak`. Ručně ho upravovat jde, ale běžná cesta je level + capture. |
| `..\tools\furnishing\gen_furnishing.py` | sestaví skupiny ze speců staveb (`tools/ruin/palac_spec.py` → `kovarna_vybaveni()`, `tools/ruin/ostroh_spec.py` → `guesthouse_vybaveni()`, `tools/ruin/brana_spec.py` → `brana_straz_vybaveni()`) |
| `..\05_constructions\zr_stavby\vybaveni.py` | typ `props` (rozmístění hotových meshí), společný s 05 (tam pro pevné kusy, např. kůl u dřeva) |

### 3. Skupiny

**`Palac_Kovarna_Vybaveni`** – vybavení kovárny ve východní místnosti paláce ([[navrh_palac_kovarna]] kap. 4.4). Polohy v rámu paláce (`s`, `n`), konstanty `K_*` a funkce `kovarna_vybaveni()` v `tools/ruin/palac_spec.py`:

- kovadlina na špalku (vrch 0,75 m) v s = 28,0; n = 1,4; kalicí sud (28,3; 2,6); hřebovnice na menším špalku (27,35; 1,75);
- měchy podél věže, výfučna v otvoru boční zídky výhně (0,91 m); páka Ø 6 cm na laně z krokve n = 2,7, s madlem měchů spojená lanem;
- šlapací brus (rám s = 27,0–28,2; n = 5,1–5,7) se stoličkou; ponk se svěrákem (s = 26,05–26,75; n = 2,6–4,8); truhlík s uhlím a volným víkem; koš (26,45; 6,0);
- lišta na jižní zdi (střed 1,5 m, na dvou kolících ve spárách) se dvěma kleštěmi, kladivy a sekáči; železné pruty opřené o zeď (s = 27,15);
- zvenku pod přesahem střechy tři hranice dřeva od kůlu (kůl je pevný, v 05 `Palac_Kovarna_Kul`) po sud pod žlabem (n = 2,26–6,4).

Kontrola: `tools/checks/run_checks.py --only palac` (průniky se zříceninou, se stavbami kovárny i mezi sebou, výfučna v otvoru, vzdálenosti kovadlina – výheň – sud, průchody, dřevo pod přesahem). Náhled: `tools/checks/preview3d.py kovarna`.

**`Guesthouse_Vybaveni`** – pokoj hosta v obytné části u ostrohu ([[navrh_guesthouse_vybaveni]], stav [[stav_guesthouse]]). Rám = rám podlahy `Ostroh_Podlaha` (`s` podél vnitřního líce `ZBudova_V` od jižního rohu, `n` do místnosti), výšky od vrchu prken podlahy (generátor ji spočítá z terénu; po změně terénu nebo podlahy přegenerovat). Konstanty `GH_*` a funkce `guesthouse_vybaveni()` v `tools/ruin/ostroh_spec.py`.

- Od 22. 11. 2026 jsou postel, truhla, stojan na brnění a stolička **meshe** (`GH_MESH` v `ostroh_spec.py`, úprava `oil`, [[Katalog_props]]); zbytek je **graybox** (21. 11. 2026): kvádry (`cat = "graybox"` → Cube s materiálem `zrlib/config.py` → `MAT_GRAYBOX` = `MI_PrototypeGrid_Gray`): postel, stůl, stolička, truhla, stojan na brnění, stojan na zbraně, regál, hromádka dřeva a dočasný `Pec_Zastupce` (kamna jsou 05, staví stavitel).
- Polohy postele, stolu, stoličky a stojanů jsou z levelu (capture, Jirka).

Kontrola: `tools/checks/run_checks.py --only ostroh` (průniky se zříceninou, dostavbou, krovem a mezi sebou, kusy na podlaze, volný průchod u dveří s = 5,8–8,1; n = 0–2 m).

**`Brana_Straz_Vybaveni`** – strážní stanoviště nad východní bránou ([[navrh_brana_straz]] kap. 12, stav [[stav_brana_straz]]). Rám = rám brány (`u` podél `Brana_S` k východu, `d` kolmo k jihu), výšky od vrchu prken podesty `Brana_Straz_Podesta` (`deck_z = 3581 cm`, generátor ji spočítá z terénu v bodě `B_FURN_REF`). Konstanty `B_FURN_*` a funkce `brana_straz_vybaveni()` v `tools/ruin/brana_spec.py`.

- V 1. návrhu (23. 11. 2026) je všech 10 kusů **graybox**: stolička (`Stolicka`), převrácená bedna (`Bedna_Sipy`), sada nástrojů na výrobu šípů položená na vrchu bedny (`Naradi_Sipy`), toulec u bedny na vyrobené šípy (`Toulec_Vyroba`), pohotovostní toulec (`Toulec_Straz`) a luk (`Luk`) u SZ sloupku stříšky + 4 dočasní zástupci sloupků stříšky z kůry (`Sloupek_SZ_Zastupce`, `Sloupek_JZ_Zastupce`, `Sloupek_SV_Zastupce`, `Sloupek_JV_Zastupce`, 05).

Kontrola: `tools/checks/run_checks.py --only brana` (průniky vybavení se zříceninou, podestou, vyrovnáním, kryty a mezi sebou, uložení na podlaze / bedně / koruně `Brana_V`, umístění pod půdorysem stříšky).

## Dopad na dokumentaci
Doplní se při rozpadu.

## Známé pasti
Doplní se při rozpadu.
