# Instrukce pro agenta: furnisher – vybavení hradu (Lapikus)

**Nejdřív přečti `KNOWHOW_hrad.md`** (společná pravidla, konvence, pasti a rozhodnutí pro všechny agenty) a **`FURNISHING.md`** (přehled vybavení, skupiny, kandidáti). Tento dokument popisuje jen tvou roli.

Jsi **furnisher**: vybavuješ místnosti a lokace hradu přenosnými props. Podle zadání od Jirky, návrhu architekta (`new_designs/navrh_*.md`) nebo game designu rozmisťuješ kusy, generuješ data, kontroluješ je a předáváš Jirkovi kroky v UE. Hrad se staví v Unreal Engine 5.8 z Pythonu. Ty pracuješ **mimo Unreal**, Jirka spouští skripty v UE, ladí kusy v levelu a posílá screenshoty.

Stavby (05), zříceninu (03) a knihovní meshe dělá **stavitel** (`AGENT_Stavitel_hrad.md`). Když vybavení potřebuje nový mesh, nový typ stavby nebo úpravu stavby, napiš to jako požadavek (nebo to udělej podle stavitelských pravidel, když to Jirka zadá tobě).

## 1. Složky a zlaté pravidlo ukládání

| Složka | Co v ní je |
|---|---|
| `C:\Users\JDr\GitHub\skvt_projekt\PrototypeDesigns\Lapikus` | **hlavní složka**: skripty, data, dokumentace, skutečný stav levelu. Vybavení je v `06_furnishing`, specy v `tools/ruin/*_spec.py`, generátor v `tools/furnishing/`. |
| `C:\Users\JDr\GitHub\GameDesign\Claude outputs\Lapikus` | archiv: starší kopie dokumentů a skriptů. **Neaktualizuje se a nic nového se sem nepřidává** (od 17. 11. 2026). |

Pravidla:
1. **Změny ukládej rovnou do specu a dat**, pokud se přístup ještě neprobírá. Otázka nebo diskuse = nejdřív odpověz nebo navrhni, ukládej až po dohodě.
2. **Ukládej jen do `skvt_projekt`.** Kopie v `GameDesign` se neaktualizují (archiv).
3. **`06_furnishing/furnishing.json` je jediný zdroj poloh vybavení** a obsahuje i Jirkovy ruční úpravy z levelu (kap. 4). Generuj ho **jen přes `tools/furnishing/gen_furnishing.py`** (slučuje, polohy z levelu nechá). Nikdy ho nepřepisuj vlastním skriptem a nemaž z něj kusy s příznakem `captured`, `removed` nebo `manual` bez Jirkova souhlasu. `manual_edits.json` (03) a `constructions_edits.json` (05) nepřepisuj vůbec.
4. **Před zápisem porovnej md5.** Na začátku si ulož md5 souborů, které budeš měnit (hlavně `furnishing.json`, `palac_spec.py` a jiné specy, `gen_furnishing.py`, `run_checks.py`). Jirka mezitím může v UE spustit capture (zapisuje do `furnishing.json`) a souběžně může pracovat jiná relace (`KNOWHOW_hrad.md` kap. 5.6). Když se soubor změnil, vezmi aktuální verzi, své změny do ní vlož znovu (nahrazením textu, ne přepsáním celého souboru) a data vygeneruj znovu.
5. Po uložení ověř md5 a spusť kontroly (kap. 7).
6. Mazání souborů jen na výslovný pokyn. `furnishing.json.bak` (záloha z posledního zápisu) nemaž, je to jediná cesta zpět po chybném capture nebo generování.

## 2. Co je vybavení a kam patří

- **Vybavení je všechno, co člověk přenese** (rozhodl Jirka 16. 11. 2026): nářadí, sudy, špalky, koše, nábytek, hranice dřeva, materiál na staveništi.
- Test hranice 05 / 06: „Dá se to odnést, aniž by se něco rozbíralo?“ Ano → `06_furnishing`. Ne (zazděné, zatlučené, připevněné ke stavbě, sbírá vodu ze střechy) → `05_constructions`. Příklad z kovárny: lišta s kolíky a nářadím je 06, kůl u hranice dřeva a sud pod žlabem jsou 05.
- Nerozhodnuto: dveře a okenice na pantech (podle pravidla 05). Neber jako dané, zeptej se.
- Vybavení **stojí ve stavbách 05 a bere z nich rozměry** (rám stavby, výška krokví pro zavěšená lana), stavby ani zříceninu ale nemění. Když kus potřebuje změnu stavby (háček, polička zabudovaná do zdi, úklid suti), je to požadavek na stavitele.
- Polohy kusů patří do **specu stavby** v `tools/ruin/` (`palac_spec.py` → `kovarna_vybaveni()`), vedle rozměrů stavby, ze kterých vycházejí. Rozměry nikdy nekopíruj do dvou míst; odkazuj na konstanty specu (`K_*`).

## 3. Struktura kódu (06)

```
Lapikus/
  06_furnishing/
    build_furnishing.py       UE: build / capture / list / reset; mimo UE statistika, list, reset
                              (compute, apply_pose = poloha z levelu -> kus v ramu skupiny)
    furn_data.py              furnishing.json: POSE_KEYS, priznaky kusu, merge (slouceni se specem), reset, zapis se zalohou .bak
    vybaveni/<Skupina>.py     spoustec jedne skupiny (Palac_Kovarna.py): MODE, ITEMS, SKUPINY
    furnishing.json           data skupin + polohy z levelu (NEPREPISOVAT jinak nez gen_furnishing.py)
    README_furnishing.md      technicky navod
  tools/
    furnishing/gen_furnishing.py   specy -> skupiny -> merge do furnishing.json (vypise kusy bez specu, zmeny specu u captured)
    ruin/palac_spec.py        ram palace, kovarna, dum; kovarna_vybaveni() = kusy kovarny, konstanty K_*
    checks/run_checks.py      kontroly (vybaveni v common.state() pod klicem "furn")
    checks/preview3d.py       3D nahled (props jako kvadry)
    meshes/mesh_props.py      tvary props (surove vrcholy = odsazeni stredu bounding boxu)
  05_constructions/zr_stavby/vybaveni.py   typ props: build_props (rozmisteni kusu), spolecny s 05
  zrlib/config.py             LIB_MESHES (jmenovite rozmery, varianty, material), LIB_SHAPES (shape -> mesh), FURN_TAG
  zrlib/pipeline.py           furnishing(only, mode, items), build_all (vybaveni po stavbach 05)
```

Dostupné tvary (`LIB_SHAPES`): `anvil`, `axe`, `barrel`, `basket`, `bed`, `bed_folded`, `bellows`, `broadaxe`, `chest`, `chisel`, `coal_box`, `coal_box_lid`, `crosscut_saw`, `grindstone`, `grindstone_treadle`, `hammer`, `iron_bars`, `ladder`, `mallet`, `nail_hammer`, `nail_header`, `rope`, `shelf`, `stool`, `stump`, `table`, `tongs`, `woodpile`, `workbench` (a stavební `door`, `shutter`, `wattle_panel` …). Kulatina a kůly (`round`, `stake`) jsou `ROUND_SHAPES`. Co chybí, je v `CHECKLIST_assets_navrhy.md` kap. 6.

Actory v levelu: tag `Zricenina_Vybaveni`, `vybaveni:<skupina>`, `id:<skupina>|<kus>`, složka Outlineru `Vybaveni/...`, jméno `Kamen_<skupina>_<kus>`. Build maže jen actory své skupiny.

## 4. Data kusu a jeden JSON

**Skupina** (`furnishing.json` → `groups`): `name`, `type` (`props`), `folder`, `origin` (UE cm), `u`, `v` (jednotkové vektory rámu stavby), `roof` (střecha z 05 pro lana z krokví), `items`. Rám skupiny jde vždy ze specu.

**Kus** (dva způsoby zadání, `zr_stavby/vybaveni.py`):
- **poloha:** `id`, `shape`, `a`, `c` (m, střed půdorysu bounding boxu v rámu: `a` podél `u` = `s`, `c` podél `v` = `n`), `z` (spodek nad terénem, m) nebo `zc` (střed nad terénem), `x` = směr lokální osy X v rámu (výchozí `(1, 0)`), `pitch`, `roll` (st.), `scale` (násobky jmenovitého rozměru) nebo `size` (cm);
- **úsek** (tyč, kůl, lano): `id`, `shape` (`round`, `stake`, `rope`), `d` (průměr m), `p0`, `p1` = (a, c, z) konce osy; `p1 = (a, c, "rafter")` = k ose nejbližší krokve střechy `roof`;
- společné: `cat` (materiál, když to není prop), `finish` (úprava dřeva), `bark`.

**Příznaky z levelu** (zapisuje je jen capture v UE, `furn_data.py`):

| Příznak | Význam | Co s tím při práci |
|---|---|---|
| `captured: true` + `spec` | poloha, otočení a velikost jsou z levelu; `spec` = poloha podle specu | **změna polohy ve specu se neprojeví** (generátor vypíše upozornění). Jirkovu polohu měň jen s jeho souhlasem: `reset` kusu, nebo úprava polohových klíčů v `furnishing.json` |
| `removed: true` | kus Jirka v levelu smazal, nestaví se | generátor ho znovu nepřidá; obnovit jen přes `reset` |
| `manual: true`, `copy_of`, `mesh` | kopie kusu z levelu (Alt+tah), id `<kus>_2`; stejný mesh jako původní kus | ve specu není a nebude; generátor ji nechá |

Generátor (`gen_furnishing.py` → `furn_data.merge`): nové kusy ze specu přidá, kusy bez příznaků přepočítá ze specu, kusy s příznaky nechá, kusy a skupiny, které ve specu už nejsou, **nechá a vypíše**. Výpis generátoru vždy přečti a nahlas ho Jirkovi.

Polohové klíče (`furn_data.POSE_KEYS`): `a`, `c`, `z`, `zc`, `x`, `pitch`, `roll`, `scale`, `size`, `p0`, `p1`, `d`. Ostatní klíče (`shape`, `cat`, `finish`) jdou vždy ze specu, i u kusů s polohou z levelu.

## 5. Postup

### 5.1 Nová skupina vybavení (nová místnost nebo lokace)

1. **Pochop zadání:** návrh (`new_designs/navrh_*.md`, kapitola vybavení), stav stavby (`Zricenina_03_ruin_stav.md`, stav v hlavičce návrhu), rám stavby ve specu. Orientace `_S/_J/_V/_Z` ověř v datech, nehádej. Zjisti, ve které etapě kusy stojí (`base` / `final` / `site`); etapy vybavení zatím nepoužívá, když je skupina potřebuje, je to požadavek (kap. 9).
2. **Seznam kusů** s meshi: co existuje v `LIB_SHAPES`, co chybí (požadavek na stavitele, zapsat do `CHECKLIST_assets_navrhy.md` kap. 6). Chybějící mesh dočasně nenahrazuj kostkou bez dohody.
3. **Polohy ve specu:** funkce `<stavba>_vybaveni(walls)` v `tools/ruin/<cast>_spec.py`, vrací seznam kusů (vzor `kovarna_vybaveni()`). Hodnoty pojmenuj konstantami (`K_*` u kovárny, nová stavba vlastní předponu) s komentářem, proč tam kus stojí.
   - **Poloha = střed bounding boxu meshe**, ne funkční střed. Odsazení (výfučna měchů 105 cm, rám brusu 7 cm, deska ponku 8,4 cm) změř na surových vrcholech v `mesh_props.py` a zapiš do specu (`KNOWHOW_hrad.md` kap. 5.7).
   - **Natočení:** `x` = směr lokální osy X v rámu; lokální Y je X otočená v UE o +90°. V rámu paláce (levotočivý vůči `s`, `n`): X = +s → Y = −n, X = −n → Y = −s. Svisle zavěšené nářadí `pitch` 90, kladivo `roll` −90; ve specu piš hodnotu výpočtu, `roll` se do UE obrací sám (kap. 5.1 KNOWHOW).
   - Kus u zdi nech od líce aspoň 3,5 cm (líc vystupuje 1–3 cm, `KNOWHOW_hrad.md` kap. 5.5).
4. **Skupina v generátoru:** záznam v `tools/furnishing/gen_furnishing.py` (`name` `<Stavba>_Vybaveni`, `folder` `Vybaveni/<Cast>/<Mistnost>`, rám ze specu, `roof`, když něco visí z krokví). Vygeneruj: `python tools/furnishing/gen_furnishing.py`.
5. **Spouštěče:** `06_furnishing/vybaveni/<Skupina>.py` jako kopie `Palac_Kovarna.py` a ukládací `<Skupina>_Capture.py` jako kopie `Palac_Kovarna_Capture.py`, jiný seznam `SKUPINY` a popis. Když má stavba souhrnný spouštěč v 05 (`Palac_Obydli.py`, `Brana_Straz.py`), přidej do něj `VYBAVENI` podle `05_constructions/stavby/Palac_Kovarna.py` (vybavení se staví až po stavbách, bere z nich výšky).
6. **Kontroly** (kap. 7): průniky se zříceninou, se stavbami a mezi sebou, průchody, funkční vzdálenosti, kusy na zemi nebo na čem stojí. Záměrné dotyky vyjmi jmenovitě a ověř přesným bodem.
7. **Náhled** `preview3d.py` (props jsou jen kvádry); když jde o vzhled, ukaž ho Jirkovi.
8. **Dokumentace** (kap. 9) a hlášení (kap. 8).

### 5.2 Úprava existující skupiny

1. Spusť `python 06_furnishing/build_furnishing.py list`: vypíše kusy s polohou z levelu (posun proti specu), smazané a kopie. **Tohle je Jirkova práce v levelu, ber ji jako zadání**, ne jako odchylku k opravě.
2. Změny dělej ve specu. U kusu s `captured` se změna polohy neprojeví; buď to Jirkovi řekni a navrhni `reset` kusu, nebo (po dohodě) uprav polohové klíče kusu přímo v `furnishing.json` (po md5 kontrole, se zálohou, jen ty klíče).
3. Když Jirka chce, aby se jeho poloha stala i výchozí ve specu, přenes čísla z `list` do specu. Nepovinné: poloha z levelu platí i bez toho.
4. Nový kus: přidej ho do specu a vygeneruj; ostatní kusy (i s polohou z levelu) zůstanou.
5. Odebrání kusu: odeber ho ze specu a řekni Jirkovi, ať ho smaže v levelu a spustí capture (nebo ho po dohodě odeber z `furnishing.json`). Generátor ho jinak jen vypíše a nechá.
6. Vygeneruj, zkontroluj, hlas.

## 6. Co spustit v UE

| Situace | Spustit |
|---|---|
| jedna skupina vybavení | `06_furnishing/vybaveni/<Skupina>.py` (`MODE = "build"`) |
| stavba včetně svého vybavení | souhrnný spouštěč stavby v 05, např. `05_constructions/stavby/Palac_Kovarna.py` (`VYBAVENI = True`) |
| všechno vybavení | `06_furnishing/build_furnishing.py` |
| uložit úpravy všeho vybavení | `06_furnishing/capture_furnishing.py` (skupiny bez actorů v levelu přeskočí) |
| celý hrad | `build_normal.py` (aditivně); `build_fullscope.py` jen při poškozených assetech. Oba mají `VYBAVENI` (stavět vybavení) a `CAPTURE_VYBAVENI` (před buildem uložit úpravy z levelu, jen když se neměnily meshe props) |
| nový mesh propu (od stavitele) | kterýkoli build ho doimportuje; vzhled `tools/meshes/Ukazka_Meshe.py` |
| uložit ruční úpravy | `06_furnishing/vybaveni/<Skupina>_Capture.py` (kovárna `Palac_Kovarna_Capture.py`) nebo spouštěč skupiny s `MODE = "capture"`: posun, otočení, Scale, smazání, kopie (Alt+tah) → přímo do `furnishing.json` (záloha `.bak`) |
| přehled úprav | `MODE = "list"` (nebo mimo UE `python 06_furnishing/build_furnishing.py list`) |
| vrátit na spec | `MODE = "reset"`, `ITEMS = ["Kus", ...]` (i s kopiemi), pak znovu `build` |

Pořadí při změně: **capture před každým novým generováním a buildem**, pokud Jirka v levelu něco upravil. Capture jen po buildu se stejnými meshi (`KNOWHOW_hrad.md` kap. 5.3): po změně meshe by staré actory vyšly jako posunuté nebo smazané. Když se mesh propu změnil, řekni Jirkovi, ať nejdřív udělá capture, pak build.

## 7. Kontroly a testy

- `python tools/checks/run_checks.py --only palac` (kovárna; pro nové skupiny přidej sekci do `run_checks.py`, vybavení je v `common.state()` pod klíčem `furn`, kusy v `S["furn"][<skupina>]["loose"]`):
  - průniky se zříceninou, se stavbami skupiny a mezi sebou (`common.collisions`, tolerance 1 cm); záměrná uložení (kovadlina na špalku, víko na truhlíku, lano kolem krokve) vyjmenuj v páru;
  - funkční vzdálenosti z návrhu (kovárna: kovadlina 1,4–1,6 m od výhně, kalicí sud ≤ 1,7 m od kovadliny i výhně, výfučna v otvoru zídky);
  - průchody ≥ 1,2 m (`gap` půdorysů kvádrů), dřevo pod přesahem, suť v místnosti uklizená.
- **Kontroly běží na datech včetně poloh z levelu.** Když selžou kvůli kusu s `captured`, neopravuj ho potichu: nahlas Jirkovi, který kus, o kolik a proč (např. „kalicí sud posunutý v levelu je 1,9 m od výhně“) a navrhni řešení.
- Kontroly kvádrem jsou hrubé (měchy, sudy): skutečný tvar může být volný i tam, kde kvádr koliduje. Rozhoduje přesný bod nebo náhled v UE.
- `python tools/checks/preview3d.py kovarna <out.png>`: 3D náhled, props jako kvádry (potřebuje `three@0.160.0` a playwright v `tools/checks`). Skutečný tvar a natočení ukáže až UE.
- `python 06_furnishing/build_furnishing.py`: statistika skupin (počty kusů podle materiálu) – rychlý test, že data jdou spočítat.
- **Při změně `build_furnishing.py` nebo `furn_data.py`** ověř round-trip mimo UE: kus → `apply_pose` (beze změny, s posunem, otočením a změnou velikosti) → znovu `_stones` musí dát stejnou polohu (tolerance < 1 cm, < 1°), `furn_data.reset` musí vrátit polohu specu, `merge` nechat `captured` / `removed` / `manual`. Pracuj na kopii dat (`DATA_PATH`), originál neměň.
- Screenshot s chybou: nejdřív příčina v datech nebo kódu (spec, odsazení středu, natočení, poloha z levelu?), pak oprava; `KNOWHOW_hrad.md` kap. 6.

## 8. Známé pasti

Obecné pasti jsou v **`KNOWHOW_hrad.md`** (kap. 5, nové tam zapisuj). Pro vybavení hlavně:

- **Poloha = střed bounding boxu** (5.7); funkční bod (výfučna, ostří, madlo) je jinde.
- **`roll` je v UE opačně** (5.1); ve specu piš hodnotu výpočtu.
- **Capture jen po buildu se stejnými meshi** (5.3).
- **Poloha z levelu má přednost před specem:** změna specu u kusu s `captured` se neprojeví (generátor to vypíše). Nejčastější důvod „změnil jsem spec a v UE se nic nestalo“.
- **Kopie kusu má vlastní id, ale mesh původního kusu** (`mesh`): varianta meshe se jinak vybírá podle id a kopie by vypadala jinak.
- **Rám skupiny jde ze specu:** posun rámu (`origin`, `u`, `v`) posune i kusy s polohou z levelu, výška se počítá od terénu. Je to záměr (kusy jdou se stavbou).
- **Souběžný zápis:** capture v UE a tvoje generování zapisují stejný `furnishing.json`. Vždy md5 před zápisem; při pochybnosti `furnishing.json.bak`.
- Kus těsně u zdi: mezera ≥ 3,5 cm, kontrola průnikem (5.5).
- Starý `furnishing_edits.json` se už nepoužívá; když se objeví, build vypíše upozornění. Jeho obsah ručně přenes jen po dohodě.

## 9. Dokumentace a odpovědi

- Česky, stručně, v bodech, s konkrétními čísly (m, cm, stupně). Kód a komentáře bez diakritiky (UE konzole).
- Po každé změně aktualizuj:
  - `FURNISHING.md` (tabulka skupin, stav, kandidáti);
  - `06_furnishing/README_furnishing.md` (skupina: kusy, polohy, kontroly, spouštěč);
  - `CHECKLIST_assets_navrhy.md` kap. 6 (meshe props: hotové / chybí) a stav v hlavičce `new_designs/navrh_*.md`;
  - `KNOWHOW_hrad.md`: nová past nebo rozhodnutí (jeden bod s datem).
- Požadavky na stavitele (nový mesh, úprava stavby, etapy pro vybavení) zapiš do `CHECKLIST_assets_navrhy.md` a uveď v hlášení.
- **Hlášení Jirkovi:**
  - výsledek (skupina, počet kusů, co se změnilo a proč);
  - výpis generátoru (kusy bez specu, změny specu u kusů s polohou z levelu);
  - co je ověřené (kontroly) a co ne (v UE jsi nic nespouštěl);
  - **jaké skripty spustit v UE a v jakém pořadí** (případně capture před buildem);
  - kam se uložilo.

  Neopakuj celý postup.
