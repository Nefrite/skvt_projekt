---
# orchestrace
type: step
validity: valid
aliases: []
step_kind: build
updated: 2026-11-23
# hra
build_step: 03_ruin
domains: [structures]
entity: "[[Lapikus]]"
---
# 03 Ruin – úpravy zříceniny: data a bourací objemy v levelu

<!-- Část dokumentu kroku [[03_ruin]], rozděleno tematicky 2026-11-23 (G14b, předání Builderovi). -->

## Účel kroku
Úpravy vygenerované zříceniny bez zásahu do kódu: nedestruktivní operace v `ruin_layout.json` (kap. 4) a bourací objemy, ruční posun a mazání kamenů a oddělení části zdi přímo v levelu (kap. 5). Příprava a generování: [[03_ruin]].

## Spouštění
Spouštění, nastavení a pořadí skriptů: [[03_ruin]] (*Spouštění*).

## Skripty
<!-- hestia:generated:start -->

| Skript | Role | Entity | Dokumenty |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_Brana_S_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_bloky_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_kameny_detail.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_kameny_koruny.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_koruna_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_lic_pred_po.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_strilna_preklad_pred_po.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_strilny_osteni_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/build_ruin_blocks.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/casti/Obvod.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/casti/Ostroh.py` | entry | [[Ostroh]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/casti/Palac.py` | entry | [[Palac]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/detach_stones.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/gen_stones.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/manual_edits.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/ruin_layout.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/terrain_from_level.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/__init__.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/compute.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/decay.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/floor.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/post.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/prep.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/rubble.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/wall.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/build/Zricenina_blockout_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/build/build_ruin.py` | entry | [[Lapikus]] | [[README_ruin]] |
| `/PrototypeDesigns/Lapikus/03_ruin/build/ruin_layout.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_okna_podesta.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_patra_strilny.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_schody.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_vyklenky_kvadry.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/ruin_layout_draft.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/brana_spec.py` | spec | [[Brana]], [[Brana_Straz]], [[Strazni_Vez]] | [[navrh_brana_straz]], [[stav_brana_straz]], [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/tools/ruin/build_ruin.py` | entry | [[Lapikus]] | [[README_ruin]] |
| `/PrototypeDesigns/Lapikus/tools/ruin/check3d.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/check_blocks.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/decay.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/elev.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/export_level_layout.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/gen_layout.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/layout_from_level.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/massing.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/nadvori_spec.py` | spec | [[Nadvori_Stan]], [[Nadvori]] | [[navrh_nadvori_stan]], [[05_constructions]], [[06_furnishing]] |
| `/PrototypeDesigns/Lapikus/tools/ruin/ostroh_spec.py` | spec | [[Ostroh]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/palac_spec.py` | spec | [[Palac]] | [[navrh_palac_obydli_stred]] |
| `/PrototypeDesigns/Lapikus/tools/ruin/tower_spec.py` | spec | [[Lapikus]] | [[navrh_vez_pristresek]] |

<!-- hestia:generated:end -->

## Vstupy a výstupy
Číslování kapitol zůstává z původního [[03_ruin]] (kap. 4 a 5), aby platily starší odkazy.

### 4. Úpravy v datech (nedestruktivní)

Do `ruin_layout.json` → `"edits": [ ... ]` přidej operace a spusť skript znovu. Ukázky jsou v `"edits_examples"`. Zkopíruj je do `"edits"` a uprav.

| Operace | Zápis | Co udělá |
|---|---|---|
| **vybourat otvor ve zdi** (pohodlněji objemem, kap. 5) | `{"op": "cut", "wall": "Palac_J", "s0": 21.0, "s1": 22.2, "z0": 5.6, "z1": 7.8}` | odstraní bloky v obdélníku: `s` = metry podél zdi od jejího prvního bodu, `z` = metry od paty |
| **průchod přes více zdí** | `{"op": "cut_box", "box": [x0, y0, z0, x1, y1, z1]}` | odstraní bloky ve světovém kvádru (UE cm); `wall` lze vynechat = všechny zdi |
| **nastavit výšku** | `{"op": "set_height", "wall": "Hradba_Z_S", "s0": 37, "s1": 46, "h": 5.2}` | úsek zdi bude přesně `h` m |
| **zachránit / zvýšit** | `{"op": "restore", "wall": "Vez_S", "s0": 0, "s1": 11, "h": 14.0}` | úsek bude alespoň `h` m (rozpad ho nesníží) |

Tipy:

- **Kde je `s`:** v sekci `walls` má každá zeď `points` (UE cm). `s` se měří od prvního bodu v metrech. Délku úseku zjistíš v UE měřením (prostřední tlačítko myši + tah v Top/Side view).
- **Hledání `box`:** vlož do levelu kostku, umísti ji na místo průchodu a z Details opiš Location ± polovinu Scale × 50.
- **Typy otvorů a celé zdi** (výška `H0`, dostupnost `access`, otvory `openings`) se mění v `walls` (viz [[README_build_ruin]] kap. 3).
- **Zvýšení úseku (`raise` u zdi):** `{"s0": 15.85, "s1": 26.75, "dh": 0.5}` zvedne zeď nad výsledek rozpadu o `dh` m, na krajích plynule. `ZBudova_V` má +0,7 m (2 řady), `Hradba_Z_S` úseky 03–04 +0,5 m.
- **Zaoblené zlomy (`fillet` v `gen_layout.py`):** zlomy `Hradba_Z_S` mezi úseky 02–06 jsou oblouky. Výšky a otvory se zadávají podle původní nezaoblené čáry a `remap_wall` je převede. `seg_group` drží číslování actorů podle původních úseků (oblouk patří k sousedním úsekům).
- **Sesuv (`breaches` u zdi):** `{"s0": 0.6, "s1": 2.6, "floor": 0.5, "slope_l": 2.0, "slope_r": 6.0}` sníží zeď mezi `s0` a `s1` na `floor` m. Boky stoupají se strmostí `slope_l`/`slope_r` (1 = 45°, 6 = skoro svisle, výchozí 1). `power_l`/`power_r` > 1 bok zakřiví: dole pozvolna, ke koruně strměji (výchozí 1 = rovná linie). Ostrým bokem se sesuv udrží v jednom úseku a sousední úsek zůstane vysoký. Příklad: `Hradba_Z_S`, úsek 01 (stezka k vodě): `{"s0": -1.0, "s1": 1.3, "floor": 0.5, "slope_r": 2.4, "power_r": 1.5}` = šikmý sesuv, nízko u paláce.
- Datové úpravy **neposouvají ostatní bloky**. Každý blok má vlastní náhodu podle svého ID, takže zbytek zříceniny zůstane stejný.

#### Půdorys v3 a terén z levelu (11/2026)

- **Strážní věž se dvěma branami.** `Brana_V` je 1. brána z východu, `Brana_S` severní stěna, `Brana_J` 2. brána na západ do uličky podél věže a `Brana_Jih` nová jižní stěna. `Hradba_V` vede od jižní stěny strážní věže obloukem k JV rohu věže. `Hradba_Z_S` končí na SZ rohu strážní věže. Vstup do hlavní věže je průlom (`prulom`) ve `Vez_S`.
- **Ochrana do výšky jiného otvoru (`protect` s `to`):** `{"s0": -1, "s1": 8, "to": [{"wall": "Brana_V", "opening": 0, "dz": 0.1}, {"wall": "Brana_J", "opening": 0, "dz": 0.1}]}` drží zeď alespoň do výšky vrchu oblouku (otvor + ostění) jiné zdi. Výška je v absolutních souřadnicích, takže sedí i při jiném terénu, podstavbě nebo `z_offset`. Se dvěma cíli vede výška lineárně od `s0` k `s1`. Použito u `Brana_S` (do výšky oblouků obou bran, sem přijde hlídková konstrukce) a u přilehlých konců `Brana_V` a `Brana_J`.
- **Snížená a zarovnaná zeď (`cap`):** `{"s0": 10.26, "s1": 34.01, "z": 3459}` = mezi `s0` a `s1` zůstanou jen celé řady kamenů pod absolutní výškou `z` (cm). Koruna je rovná, jako by zeď někdo cíleně rozebral. Bez volných kamenů a bez rozebírání líce.
- **Vybourané okno u ostrohu:** `gen_layout.py` přidá do `edits` `cut` ve zdi `ZBudova_V` v místě okna dostavby (05) nad 1,4 m. Hodnoty počítá `tools/ruin/ostroh_spec.py` (`WINDOW`, `WINDOW_CUT`). Zeď patří do části **Ostroh**.
- **Žlábky v koruně (`notches`):** `{"s", "w", "d", "slope", "pt", "nin", "t", "k", "dir", "bw"}`. V horní řadě se kámen v šířce `w` kolem `s` sníží o `d`, tak aby v něm ležel trám. Trám jde přes zeď šikmo a ve sklonu, proto se žlábek u každé vrstvy (vnitřní líc, jádro, vnější líc) posune (`k`) a ven prohlubuje (`slope`). S `dir` (směr trámu) a `bw` (šířka trámu) se žlábek v každém kameni počítá přesně podle půdorysu trámu, i v oblouku nebo na zlomu zdi. Použito u `Hradba_Z_S` v západní části u ostrohu. Hodnoty počítá `tools/ruin/ostroh_spec.py`.
- **Koruna pod střechou (`roof_clear`):** v úseku `s0`–`s1` se kameny koruny směrem ven od vnitřního líce sníží ve sklonu střechy, který se bere ze žlábků (`slope`). Pak nezasahují do latí a prken krovu (05). `clear` je výška vrchu trámu nad korunou u vnitřního líce.
- **`plinth` (podstavba, m)** u zdi zvedne výšku, parapety otvorů, ochranu i sesuvy. Patří k zdi na nižším terénu. `Brana_V` má `plinth: 2.0`. **`z_offset` (m)** posune celou zeď svisle, třeba zapuštění do terénu. `Brana_V` má `z_offset: -2.1` podle posunu v levelu. `Hradba_V` je silná 2,5 m (vnější líc v rovině jižní zdi věže) a oblouk k věži má 6 úseků s plynulým napojením.
- **`TERRAIN_FROM_LEVEL = True`** (nahoře ve skriptu): build změří výšky landscapu v levelu (line trace, ostatní actory ignoruje) a uloží je do `terrain_from_level.json`. Capture (`capture_manual_edits`) používá tento uložený stav. Po úpravě terénu stačí znovu spustit build.
- **Věž: kapsy, střílny s výklenkem, dlažba.** Zdi věže mají `ref_z` (podlaha přízemí, Z 3150), `course_grid` (pevné řady 0,35 m) a `inside_pt` (vnitřek věže). Všechny výšky otvorů se zadávají od podlahy.
  - Typ otvoru `kapsa` prorazí jen vnitřní líc. S `outer: true` prorazí vnější líc, takhle jsou kapsy pro trámy podesty.
  - Střílna nebo okno se `splay` (`floor`, `top`, `w_in`) má zevnitř kónický výklenek s šikmými boky a překladem. Překlad je vysoký přesně jednu řadu kamene (vrch na spáře), takže nad ním nezůstává mezera.
  - Střílny v hradbě `Hradba_Z_S` mají výklenek stejně jako ve věži (`strilna_h` v `gen_layout.py`, šířka zevnitř 1,4 m). Dolní střílny mají výklenek od terénu, horní (parapet 5 m) od úrovně ochozu asi 4 m.
  - `ragged` (m) náhodně vylámá líc kolem průchodu.
  - Kamenná dlažba přízemí je v `floors` → `Vez_Dlazba`.
  - Rozměry věže (podlaha, patro, polohy trámů, průvlaku, dveří) jsou společné se stavbami v `tools\ruin\tower_spec.py`.
- **Dřevěné vestavby a suť jsou od 11/2026 v `05_constructions`.** Patří sem trámy, prkna, průvlak, schody, podesta a volná suť na zemi (`build_constructions.py`, návod [[05_constructions]]). Build zříceniny je nestaví ani nemaže. `compute_blocks(..., rubble=True)` sem suť vrátí postaru.
- **Přenos ručních posunů zdí do dat:** `tools\ruin\export_level_layout.py` zapíše posunuté actory a body `RuinPt_<Zed>_<NN>` do `layout_from_level.json`. Podle něj se upraví `gen_layout.py`.

---

### 5. Úpravy přímo v levelu: bourací objemy (doporučeno)

Každá zeď je v levelu jeden Instanced Static Mesh. Kliknutím proto vybereš celou zeď, ne jednotlivý blok. Na úpravy jsou určené **objemy**: do levelu vložíš **Trigger Box**, dáš mu tag a přegeneruješ. Skript si objemy při každém spuštění načte sám. Posunem nebo zvětšením boxu a novým spuštěním úpravu upravíš, smazáním boxu ji vrátíš.

#### 5.1 Vložení objemu

1. **Window → Place Actors**, vyhledej **Trigger Box** a přetáhni ho k místu na zdi.
2. Box **musí protínat osu zdi**. Nastav ho přes gizmo nebo v Details → Transform. Rozměr Trigger Boxu je 2 × Box Extent × Scale. Pro vstup do věže stačí třeba šířka 1,4 m, výška 2,6 m a hloubka 4 m, aby box prošel celou zdí.
3. V Details → **Actor → Tags** přidej tag nebo více tagů:

| Tag | Co udělá |
|---|---|
| `Ruin_Opening:dvere` | **dveře** v místě boxu (kamenné ostění + nadpraží; podle dostupnosti se může vylámat) |
| `Ruin_Opening:portal` | **klenutý portál** (oblouk z klínových kamenů) |
| `Ruin_Opening:okno` / `Ruin_Opening:strilna` | **okno / střílna** (spodek boxu = parapet) |
| `Ruin_Opening:brana` | **brána** (velký oblouk) |
| `Ruin_Opening:prulom` | **vybouraný průchod** bez ostění, nepravidelný horní okraj |
| `Ruin_Intact` (spolu s Opening) | ostění se nevylámá, otvor zůstane jako nový |
| `Ruin_Protect` (spolu s Opening) | oblouk se nezřítí |
| `Ruin_Cut` | **vyřízne vše** uvnitř boxu (hrubá díra, i přes víc zdí) |
| `Ruin_Keep` | zdi v boxu se **nerozpadnou pod vršek boxu** (zvýšení / záchrana úseku) |
| `Ruin_Explode` | bloky uvnitř boxu se vytvoří jako **samostatné kameny** pro ruční posun a mazání (kap. 5.2) |

4. Spusť `build_ruin_blocks.py`. Output Log vypíše mimo jiné počet načtených objemů.

**Rozdíl mezi `Ruin_Opening` a `Ruin_Cut`:**

- **`Ruin_Opening`** vytvoří skutečný otvor se vším, co k tomu patří: ostění, nadpraží, oblouk a rozpad podle dostupnosti. Například dveře v dostupné zdi mohou mít vylámané ostění a V-zářez.
- **`Ruin_Cut`** jen vyřízne bloky. Hodí se na hrubé díry a průlomy.

**Vstup do věže** je teď v datech rovnou: **vybouraný průchod (`prulom`) v přízemí severní strany věže z nádvoří**, 1,4 × 2,6 m. Další vstup z paláce do věže přidáš boxem s tagy `Ruin_Opening:portal` a `Ruin_Protect` přes západní zeď věže. Ukázka je v `ruin_layout.json` → `volumes_examples`.

Doporučení:

- Objemy si dej do vlastní složky v Outlineru, např. `Ruin_Objemy`.
- Pojmenuj je podle účelu, např. `Vstup_vez_z_palace`.
- Trigger Box se ve hře nezobrazuje a postavě nebrání. Může v levelu zůstat napořád.

#### 5.2 Ruční posun a mazání jednotlivých kamenů

1. Přes místo, které chceš ručně doladit, polož Trigger Box s tagem **`Ruin_Explode`** a přegeneruj.
2. Bloky v boxu jsou teď **samostatné actory** ve složce `Ruin/<Část>/Kameny` (suť je samostatná vždy, ve složce `…/Sut`) s názvem `Kamen_<ID>`. Jde je vybírat, posouvat, otáčet i mazat jako běžné objekty. Box drž malý, každý kámen je jeden actor.
3. Po úpravách nastav nahoře v `build_ruin_blocks.py` `MODE = "capture"` a spusť ho. Do `manual_edits.json` se zapíšou:
   - **smazané** kameny (`removed`)
   - **posunuté a pootočené** kameny (`moved`)
4. Vrať `MODE = "build"`. Při dalším generování zůstanou smazané kameny smazané a posunuté na novém místě. Platí to i po změně stáří nebo dalších úprav.
5. **Sloučení zpět do zdi:** smaž (nebo přejmenuj tag) box `Ruin_Explode` a přegeneruj. Posunuté kameny se vrátí do Instanced Static Mesh **na svých nových místech** a samostatné actory zmizí. Smazané kameny zůstanou smazané.
6. **Další ladění:** stačí box `Ruin_Explode` vrátit. Kameny se znovu rozloží, i ty dříve posunuté, a to podle původní i nové polohy.
7. **Vrácení:** smaž záznam z `manual_edits.json`, nebo soubor přepiš na `{"removed": [], "moved": {}, "detached": []}`.

Pozor: capture spouštěj vždy **před** dalším generováním, i před sloučením (krok 5). Generování ruční změny bez capture přepíše.

Tip: box `Ruin_Explode` nemusíš mazat. Stačí mu dočasně přepsat tag na `x_Ruin_Explode`, skript ho pak ignoruje.

#### 5.3 Oddělení části zdi bez přegenerování (`detach_stones.py`)

Když chceš, aby kus zdi odpadl nebo se sesypal, a nechceš kvůli tomu stavět celou zříceninu znovu:

1. Přes část zdi, která má odpadnout, polož Trigger Box s tagem **`Ruin_Detach`**. Když nějaké takové boxy vybereš, použijí se jen vybrané.
2. **Tools → Execute Python Script → `detach_stones.py`** (`MODE = "detach"`).
   - Kameny v boxu se vyjmou z Instanced Static Meshe zdi a vzniknou jako samostatné actory na stejném místě, se stejným meshem a materiálem. Najdeš je ve složce `…/Odpadle` s tagem `Ruin_Detached`.
   - Zbytek zdi se nemění.
   - Oddělení se hned zapíše do `manual_edits.json` (`detached`).
3. Kameny mají **trvalou fyziku** (`SIMULATE = True`), takže s nimi hráč může pohnout. Spusť **Simulate** (Alt+S) a nech je spadnout.
4. Až se usadí, vyber je (Outliner, složka `Odpadle`) a stiskni **K** (Keep Simulation Changes). Simulaci ukonči.
5. `build_ruin_blocks.py` s `MODE = "capture"` uloží jejich nové polohy.

Box `Ruin_Detach` pak můžeš smazat. Další build zříceniny postaví oddělené kameny jako samostatné actory na uložených místech, zase s fyzikou (`DETACHED_PHYSICS`). Usazené kameny s uloženou polohou ve hře spí, dokud do nich někdo nestrčí. Bez fyziky (staticky): `MODE = "freeze"` (do dalšího buildu) nebo `DETACHED_PHYSICS = False`.

**Fyzika volných kamenů (`STONE_PHYSICS` v `zrlib\config.py`, platí i pro suť ve 05):**
- **Hmotnost podle objemu kamene:** hustota 2600 kg/m³ × objem bloku × 0,85 (zaoblení). Kámen 30 × 40 × 60 cm váží asi 160 kg, suť většinou 20–280 kg. Hráč takový kámen posune jen málo.
- **Tlumení** (`lin_damp` 0,3, `ang_damp` 0,8): kámen se nekoulí donekonečna.
- **Fyzikální materiál `PM_RuinStone`**, který skript vytvoří ve složce materiálů: tření 0,9, odraz 0,05.
- Kameny jsou o 3 % menší než blok (`shrink`), aby je při startu nevystřelil překryv se sousedy.
- Jak silně hráč tlačí, se nastavuje u postavy v **Character Movement**: zapnutý `Enable Physics Interaction`, `Push Force Factor` asi 100 000–300 000 a vypnutý `Push Force Scaled To Mass`. Pak se těžký kámen pohne málo a lehký víc. Kameny můžeš i ručně posouvat nebo mazat a uložit přes capture.

**Vrácení do zdi:** box `Ruin_Detach` přes oddělené kameny a `MODE = "undo"`. Kameny se vrátí do zdi při dalším buildu.

Oddělit jde líc, koruna, jádro i ostění (`CATS`). Za odpadlým lícem je hned po oddělení hladké jádro (kostky). Při dalším buildu se tam jádro samo rozpadne na lomové kameny jako u ostatních odkrytých míst.

## Dopad na dokumentaci
Změna dat nebo typu stavby: aktualizuj tento dokument a stavový dokument entity (`stav_*`).

## Známé pasti
Viz `KnowHow/Pasti_*` (tematické seznamy pastí).
