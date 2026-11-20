---
# orchestrace
type: step
validity: valid
aliases: [README_constructions]
step_kind: build
updated: 2026-11-17
# hra
build_step: 05_constructions
domains: [structures]
---
# 05 Constructions – dodatečné stavby a suť („druhé zabydlení“) – návod pro UE 5.8

## Účel kroku
Do této složky patří všechno, co do zříceniny později přistavěli její obyvatelé, a volná suť na zemi. Staví se **zvlášť od zříceniny**: když ladíš schody, trámy nebo podestu, nemusíš přegenerovat celý hrad.

| Kde | Co |
|---|---|
| **03_ruin** (`03_ruin\blocks\build_ruin_blocks.py`) | zřícenina jako taková: zdi, otvory, ostění, kapsy pro trámy, kamenná dlažba přízemí věže |
| **05_constructions** (`build_constructions.py`) | dřevěné vestavby: trámy, prkna, průvlak se sloupy, provizorní schody, ochoz, krov u ostrohu. Kamenné dostavby z kamene rozvalin (stojí na zřícenině, ale nemění ji). Volná suť u zdí. |

Kapsy ve zdech patří ke zřícenině. Dřevo, které v nich leží, patří sem.

---

## Spouštění
### 2. Postup v UE

1. **Nejdřív zřícenina:** `03_ruin\blocks\build_ruin_blocks.py`. Ta změří terén (`terrain_from_level.json`) a postaví zdi a kapsy.
2. **Pak stavby:** **Tools → Execute Python Script →**
   - **jedna stavba:** `05_constructions\stavby\Ostroh_Krov.py` (nebo `Ostroh_Dostavba.py`, `Ostroh_Podlaha.py`, `Vez_Patra.py`, `Palac_Kovarna_Pristresek.py`, `Palac_Kovarna_Vyhen.py`, `Palac_Kovarna_Stena.py`, `Palac_Kovarna_Okap.py`, `Sut.py`). Smaže a postaví jen tuto stavbu, ostatní zůstanou, jak jsou.
   - **všechno:** `05_constructions\build_constructions.py`.
   - **zřícenina i stavby jedním spuštěním:** `build_normal.py` v kořeni prototypu (aditivně), nebo `build_fullscope.py` (oprava: smaže generované actory a meshe a vše postaví znovu; popis v [[03_ruin]] kap. 2.1).
   - Každý actor má tag `Zricenina_Stavby` a `stavba:<jméno>`. Zříceniny se build staveb nedotkne a build zříceniny nesmaže stavby.
3. V Outlineru přibude:
   - `Stavby/Vez/Vez_Patra_Drevo`: trámy, prkna, průvlak, sloupy, schody a ochoz (Instanced Static Mesh),
   - `Stavby/Ostroh/Ostroh_Krov_Drevo_Dehet`: krov a krytina u ostrohu,
   - `Stavby/Ostroh/Ostroh_Dostavba_Kamen` a `..._Drevo_Stare`: kamenná dostavba a dřevěná nadpraží,
   - `Stavby/Ostroh/Ostroh_Podlaha_Drevo` a `..._Drevo_Dehet`: prkna a podvaly podlahy,
   - `Stavby/Palac/Palac_Kovarna_Pristresek_Drevo`: sloupy, pozednice, krokve a krytina přístřešku kovárny (latě, prkna, lišty, lemování); patní kameny sloupů jsou samostatné actory ve stejné složce,
   - `Stavby/Palac/Palac_Kovarna_Vyhen_Kamen`, `..._Mazanina` (maz stolu, dymník, komín), `..._Uhli`, `..._Drevo` (výměny, závěsné tyče),
   - `Stavby/Palac/Palac_Kovarna_Stena_Mazanina` (dílce stěny z proutí) a `..._Drevo` (kůly),
   - `Stavby/Palac/Palac_Kovarna_Okap_Drevo` (žlab, rozsochy); sud na vodu je samostatný actor ve stejné složce,
   - `Stavby/Sut/<část hradu>/Kamen_…`: kameny suti jako samostatné actory.

**Ruční úpravy:** smaž instanci nebo kámen, posuň kámen suti. Pak ve skriptu dané stavby (`stavby\<Stavba>.py`) nastav `MODE = "capture"` a spusť ho. Změny se zapíšou do `constructions_edits.json`, úpravy ostatních staveb v něm zůstanou, a platí i po dalším buildu.

**Nová stavba:**
1. **Typ:** když žádný existující nesedí, nový modul v `zr_stavby\` s funkcí, která z dat vrátí seznam dílců (`Stone` ze `zrlib.stones`). Geometrie je v `zrlib.geom`, dřevo podle `finish` přes `zrlib.config.WOOD_FINISH`.
2. **Registr:** záznam v `TYPES` a povinné klíče v `REQUIRED` v `build_constructions.py`.
3. **Data:** položka v `constructions.json` (přes `gen_constructions.py`) s `name`, `type` a `folder`.
4. **Launcher:** kopie jednoho ze skriptů ve `stavby\` s novým jménem v `STAVBA`.

Mazání v UE jde podle tagu `stavba:<jméno>`. Actor bez něj (ze starších buildů) smaže jen build všech staveb najednou (`build_constructions.py` spuštěný přímo).

**Fyzika suti:** kameny suti mají trvalou fyziku (`RUBBLE_PHYSICS = True`, tag `Ruin_Physics`), takže s nimi hráč může pohnout. Hmotnost odpovídá objemu kamene, většinou 20–280 kg. Nastavení je v `STONE_PHYSICS` v `03_ruin\blocks\build_ruin_blocks.py` a je společné s odpadlými kusy zdi.

1. Usazení: spusť **Simulate** (Alt+S) a kameny se usadí na terénu a o sebe.
2. Vyber je (Outliner `Stavby/Sut` nebo tag `Ruin_Physics`), stiskni **K** (Keep Simulation Changes) a simulaci ukonči.
3. `MODE = "capture"` uloží jejich polohy.

Usazené kameny ve hře spí, dokud do nich někdo nestrčí. Staticky bez fyziky: `MODE = "freeze"` (do dalšího buildu) nebo `RUBBLE_PHYSICS = False`. Jak silně hráč tlačí, se nastavuje v Character Movement postavy (viz [[03_ruin]], kap. 5.3).

---

### 3. Kdy co přegenerovat

| Změna | Co spustit |
|---|---|
| schody, prkna, ochoz, sloupy, suť (v `constructions.json` nebo `gen_constructions.py`) | jen `build_constructions.py` |
| podlaha u ostrohu (`gen_constructions.py` → `floor`) | `gen_constructions.py`, pak `Ostroh_Podlaha.py` a `Sut.py` |
| dostavba u ostrohu (okno, dveře, tloušťka, kámen, trámy dokola příčky v `gen_constructions.py`) | `gen_constructions.py`, pak `Ostroh_Krov.py` **i** `Ostroh_Dostavba.py` (dostavba sahá pod střechu, výšky bere z krovu) a `Sut.py` (úklid uvnitř) |
| **polohy trámů, průvlaku, otvorů nebo dveří** (`tower_spec.py`), **krov u ostrohu** (`ostroh_spec.py`) | `gen_layout.py` **i** `gen_constructions.py` (kapsy jsou ve zdech), pak oba buildy |
| zdi, rozpad, otvory zříceniny | `build_ruin_blocks.py`, pak `build_constructions.py` (trámy se kontrolují proti zdem) |
| kovárna v paláci (`palac_spec.py`, `gen_constructions.py` → `palac`) | `gen_constructions.py`, pak **`Palac_Kovarna.py`** (celá kovárna ve správném pořadí, suť a vybavení z 06), nebo jednotlivě `Palac_Kovarna_Pristresek.py`, `Palac_Kovarna_Vyhen.py` (výměny u komína berou výšku z krokví), `Palac_Kovarna_Stena.py` `Palac_Kovarna_Okap.py` (žlab bere výšku z okapové hrany krytiny) , nakonec `Sut.py`; vybavení `06_furnishing/vybaveni/Palac_Kovarna.py`. Zřícenina se mění při změně kapsy pro východní pozednici, zanoření `Palac_J` (`J_SINK`) nebo rozebrání koruny u věže (`J_BREACH`); pak `gen_layout.py` a část `Palac` (nebo `Palac_Kovarna.py` s `RUIN = True`). |

Trám nebo průvlak se nepostaví, když zeď u jeho kapsy spadla.

---

## Skripty
<!-- hestia:generated:start -->

| Skript | Role | Entity | Dokumenty |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/Knihovna_meshe_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Knihovna_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Kulatina_meshe_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Kulatina_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Props_kovarna_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Props_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_straz_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_straz_nahled_etapa1.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_drevo_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_dostavba_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_podlaha_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_tramovi_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_kovarna_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_obydli_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_obydli_nahled_etapa1.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_vez_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_vez_pristresek_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/build_constructions.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/constructions.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/constructions_edits.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz.py` | entry | [[Brana_Straz]] | [[navrh_brana_straz]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kamen.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kryty.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Podesta.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Etapa.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Dostavba.py` | entry | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Krov.py` | entry | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Podlaha.py` | entry | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Kul.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Okap.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Pristresek.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Stena.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Vyhen.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli.py` | entry | [[Palac_Obydli]] | [[navrh_palac_obydli_stred]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Kamen.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Krov.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Ohniste.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Srub.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Sut.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez.py` | entry | [[Vez]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez_Patra.py` | entry | [[Vez]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez_Pristresek.py` | entry | [[Vez_Pristresek]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/__init__.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/dostavba.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/krov.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/kryty.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/ohniste.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/okap.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/podesta.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/podlaha.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/pristresek.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/pult.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/srub.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/stena.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/vez.py` | library | [[Vez]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/vybaveni.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/zdivo.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/tools/constructions/check_tower.py` | generator | – | – |
| `/PrototypeDesigns/Lapikus/tools/constructions/gen_constructions.py` | generator | – | – |

<!-- hestia:generated:end -->

## Vstupy a výstupy
### 1. Soubory

| Soubor | Obsah |
|---|---|
| `stavby\<Stavba>.py` | **spuštění jedné stavby**: `Vez_Patra.py` (dřevo ve věži), `Ostroh_Krov.py` (krov u ostrohu), `Ostroh_Dostavba.py` (kamenná dostavba u ostrohu), `Ostroh_Podlaha.py` (prkenná podlaha u ostrohu), `Palac_Kovarna.py` (**celá kovárna najednou**: přístřešek, výheň, stěna, okap, vybavení; přepínače `KRYTINA`, `RUIN` = i část zříceniny `Palac`, `SUT`), `Palac_Kovarna_Pristresek.py` (přístřešek kovárny v paláci), `Palac_Kovarna_Vyhen.py` (výheň kovárny), `Palac_Kovarna_Stena.py` (stěna z proutí), `Palac_Kovarna_Okap.py` (žlab a sud), `Palac_Kovarna_Kul.py` (kůl u dřeva), **`Palac_Obydli.py` (celý dům posádky najednou: seznam staveb, `SUT`)**, `Palac_Obydli_Kamen.py` a `Palac_Obydli_Ohniste.py` (jeho kamenné části a základ ohniště), `Palac_Obydli_Krov.py` (krov bez krytiny), `Palac_Obydli_Srub.py` (srub a štíty), **`Brana_Straz.py` (celé strážní stanoviště nad branami: seznam staveb, `RUIN` = i část zříceniny `Obvod`, `SUT`)**, `Brana_Straz_Kamen.py`, `Brana_Straz_Podesta.py` a `Brana_Straz_Kryty.py`, `Etapa.py` (přepnutí etapy v editoru), `Sut.py` (suť). Nahoře `MODE` (`build` / `capture`, u suti i `freeze`). V `Ostroh_Krov.py` navíc `KRYTINA`: `False` postaví jen sloupy, příčku a trámy (ladění trámoví a dostavby), `True` i latě, prkna, lišty a hřeben. Dostavba je na krytině nezávislá (výšky bere z trámů). Stejný přepínač `KRYTINA` má `Palac_Kovarna_Pristresek.py` (výchozí `True`). |
| `build_constructions.py` | nastavení, registr typů staveb (`TYPES`, povinné klíče `REQUIRED`), build / capture / freeze v UE. Spuštěný přímo postaví všechny stavby najednou. Mimo UE vypíše počty kusů. |
| `zr_stavby\*.py` | typy staveb: `vez.py` (dřevo ve věži, `tower_floor`), `krov.py` (krov u ostrohu `fan_roof` + společná geometrie), `dostavba.py` (`stone_addon`), `podlaha.py` (`plank_floor`), `pult.py` (pultová střecha na sloupech, `pult_roof`), `ohniste.py` (ohniště / výheň s dymníkem a komínem, `hearth`), `zdivo.py` (zdivo z kamene rozvalin: srovnání korun, podezdívky, `stone_fill`), `stena.py` (stěna z proutí, `wattle_wall`), `okap.py` (žlab na rozsochách se sudem, `gutter`), `vybaveni.py` (rozmístění props, `props`), `srub.py` (srubové stěny a prkenné štíty, `log_wall`), `podesta.py` (trámy, prkna a zábradlí ve výšce zadané absolutně, `platform`), `kryty.py` (kryt z kůlů se špičkou na koruně zdi, paty kopírují korunu, průzory, ráhna, `palisade`) |
| `..\zrlib\*.py` | sdílená knihovna s 03 (`config.py` = materiály, dřevo, fyzika; geometrie, Unreal; `pipeline.py` = spouštění: stavby, části, `build_normal.py`, `build_fullscope.py`) |
| `constructions.json` | data staveb (`floors` → `Vez_Patra`, `frames` → `Ostroh_Krov`, `Palac_Kovarna_Pristresek`, `addons` → `Ostroh_Dostavba`, `Ostroh_Podlaha`, `Palac_Kovarna_Vyhen`, `Palac_Kovarna_Stena`, `Palac_Kovarna_Okap`) a nastavení suti (`rubble`) |
| `Stavby_palac_kovarna_nahled.png` | náhled kovárny ve východní místnosti paláce (přístřešek s krytinou, výheň, stěna z proutí, okap se sudem; 8 pohledů, dílce jsou v náhledu jen kvádry) |
| `Stavby_ostroh_dostavba_nahled.png` | náhled uzavřené obytné části u ostrohu zvenku a zevnitř |
| `Stavby_ostroh_podlaha_nahled.png` | náhled podlahy u ostrohu |
| `Stavby_palac_obydli_nahled.png` | náhled domu posádky v prostřední místnosti paláce (zatím kamenné části; nový kámen je v náhledu okrový) |
| `constructions_edits.json` | ručně smazané (`removed`) a posunuté (`moved`) kusy. Vzniká přes capture, nepřepisovat. |
| `Stavby_vez_nahled.png` | řez věží: patra, schody, ochoz |
| `..\tools\constructions\gen_constructions.py` | vytvoří `constructions.json` z `ruin_layout_draft.json` |
| `..\tools\constructions\check_tower.py` | náhled řezu věží bez Unrealu (zřícenina + stavby) |
| `..\tools\ruin\tower_spec.py` | **společné rozměry věže** pro 03 i 05 (podlaha, výška patra, polohy trámů, průvlaku, otvorů, dveří) |
| `..\tools\ruin\palac_spec.py` | **společné rozměry staveb v paláci**: souřadný rám paláce (`s` podél `Palac_J`, `n` k severu) a kovárna (linie sloupů, pozednice, krokve, komín) |

Skript používá generátor zříceniny jako knihovnu. Složka `03_ruin\blocks` proto musí ležet vedle `05_constructions` (jinak v `build_constructions.py` nastav `RUIN_DIR`) a v kořeni musí být `zrlib`.

---

### 4. Co je v `constructions.json` (Vez_Patra)

| Klíč | Význam |
|---|---|
| `levels` | patra s trámy a prkny (1, 2) |
| `beams` | trámy: polohy `v` (m od jižní zdi), průřez, zapuštění do kapsy `bearing` |
| `planks` | prkna: tloušťka, šířky, podíl chybějících |
| `girder` | průvlak sever–jih pod trámy, sloup s hlavicí (`post_v`) |
| `hatches` | otvory pro schody v každém patře (u0, u1, v0, v1) |
| `stairs` | schody: `from` / `to` patro, `axis` `"u"` (podél trámů), `dir` (+1 stoupá k východu, −1 k západu), `u_top` (horní konec), `v`, `angle`, `width`. Cik-cak: do 1. patra k východu, do 2. patra k západu |
| `porch` | ochoz před původním vstupem: šířka, hloubka, trámy zapuštěné v kapsách, šikmé vzpěry pod trámy opřené o zeď (`braces`: `dv`, `dz`, `w`). Sloupky na zem (`posts`) jsou vypnuté |
| `finish` | úprava dřeva podle části: `tar` dehtované, `raw` bez úpravy, `oil` mořené olejem, `blood` mořené krví, `old` staré neošetřené. Části: `beams`, `girder`, `posts`, `heads`, `planks` (a `planks_1`, `planks_2` pro jedno patro), `stairs`, `porch_beams`, `porch_braces`, `porch_posts`, `porch_planks` |
| `rubble` | suť: `enabled`, složka v Outlineru |

**`frames` → `Ostroh_Krov`** (typ `fan_roof`): krov v západní části u ostrohu.

- **Sloupy a příčka:** 2 sloupy stojí asi 1 m od vnitřního líce `ZBudova_V` v prostoru (`POST_SHIFT`), po stranách průchodu, 10 cm od jeho hran (`POST_SPREAD`). Průchod 1,6 m (`PASS_W`) zůstává volný. Na sloupech leží příčka (vaznice), 3,8 m dlouhá, s přesahem 85 cm na každou stranu. Šikmé vzpěry vedou od sloupů ven a hlavou podpírají přesahy příčky. **Příčka je hřeben střechy:** střecha od ní klesá na všechny strany.
- **Paprskovité trámy:** 7 trámů 22 × 24 cm vede z příčky na hradbu `Hradba_Z_S`.
- **Hradba:** je v tomto úseku cíleně snížená a zarovnaná, asi 3 m nad terénem, i 4 m za krajní trámy vějíře (`CAP_EXT`, pod krytinou paprskových trámů).
- **Uložení:** trámy leží ve žlábcích koruny, u vnitřního líce zhruba do poloviny výšky trámu. Svažují se ke zdi (11–17°, příčka 1,2 m nad dnem žlábků, `RISE`) a 0,6 m přesahují vnější líc (okap).
- **Dřevo:** všechno je dehtované (`finish`).
- **Rozměry:** jsou v `tools/ruin/ostroh_spec.py` a sdílí ho 03 (snížení a žlábky) i 05 (dřevo). Po změně přegeneruj `gen_layout.py` i `gen_constructions.py` a postav 03 i 05.

- **Krytina** (`roof`, všechno dehtované):
  - **Latě:** 5 řad napříč trámy.
  - **Prkna:** po spádu, 22–30 cm široká, se spárami 1,5 cm. V každém poli mezi trámy leží rovnoběžně. Krajní jsou kratší a vyplňují klín, jak se pole ke zdi rozšiřuje. Začínají už tam, kde se do pole dostane jejich vnitřní hrana, takže u trámů nezůstávají díry. Sousední pole se u trámu překrývají (každé druhé o tloušťku prkna výš).
  - **Lišty:** 10 cm široké přes každou spáru (1,5 cm), každá přesahuje spáru asi 4 cm na obě strany. Přes každý trám leží krycí prkno 36 cm, které zakryje spoj dvou polí.
  - **Lemování u příčky:** zatím není, vyřeší se jinak.
- **Koruna pod střechou:** kameny hradby mezi trámy jsou směrem ven snížené ve sklonu střechy (`roof_clear` v 03), aby nezasahovaly do latí a prken.

- **Trámy dokola příčky** (`ring`, pořadí navazuje na vějíř, `ring_closed` = pole krytiny i mezi posledním a prvním trámem):
  - `PB0–2` a `PA0–2`: paprskové trámy na koncích příčky, rovnoměrně mezi krajním trámem vějíře (B6 / B0) a směrem zpět ke `ZBudova_V` (`N_RAD`);
  - `E0–1`: 2 trámy z příčky zpět na dostavbu `ZBudova_V` nad dveřmi, mezi začátky trámů vějíře (`E_AT`, jen krajní);
  - každý končí na nejbližší zdi: na dostavbě (`ZBudova_V`, `ZBudova_S`) má sklon 14° (`SLOPE_DOST`), dlouhé trámy klesnou nejvýš 0,8 m (`DROP_MAX`, ne pod 10°). Na koruně zříceniny leží na nejvyšším kameni pod sebou (zřícenina se pro ně nesnižuje);
  - přesah 0,4 m za vnější líc (`OH_RING`). Dostavba se pod nimi sníží: uprostřed (krátké trámy `E`) nejméně, na bocích víc.
- **Sklon:** vějíř 11–17°, trámy dokola 11–14°.
- **Hřebenová prkna** (`ridge`): dvě prkna 26 cm přes příčku, na každou stranu jedno, překrývají začátky polí.
- Latě se mezi trámy s různým sklonem kladou šikmo, aby ležely na obou trámech.

Žlab, okapnice a sud přijdou později.

**`addons` → `Ostroh_Dostavba`** (typ `stone_addon`): uzavření obytné části u ostrohu. Provizorní dostavba z kamene rozvalin, jedna řada kamenů přes celou tloušťku (líc z obou stran). Zřícenina se nemění, dostavba jen stojí na koruně zdí.

| Zeď | Kde |
|---|---|
| `V` | na vnitřní polovině `ZBudova_V` (vnitřní líc v rovině líce zdi), po celé délce a přes mezeru u jižního konce až k hradbě. **Dveře** v průchodu (1,6 m, vrch 2,2 m nad terénem, nadpraží ve stejné výšce jako nadpraží okna, `align`), **okno** 3,4 m severně od dveří (k `ZBudova_S`), 1,25 m široké, parapet 1,4 m (rozměry v `ostroh_spec.py` → `WINDOW`). V místě okna je původní zeď `ZBudova_V` v 03 vybouraná nad 1,4 m (`edits` → `cut`), takže okno sahá až na korunu zříceniny (asi 1,35 m) a není zastavěné zříceninou |
| `S` | na jižní (vnitřní) polovině `ZBudova_S`, od rohu se `ZBudova_V` k hradbě |
| `H` | na vnitřní polovině hradby mezi rohy (vyrovnání koruny pod okapem mezi trámy) |

- **Kámen** (`stone`): použitý kámen z hradu, stejně velký jako ve zdech (délka a výška řad z `STONE_MIN/MAX` a `COURSE_MIN/MAX` v `ruin_layout.json`: 35–90 cm, řady 25–40 cm), tloušťka 0,45 m, spáry 1,5 cm. U koruny a u trámů jsou kusy kratší, aby dosáhly pod střechu.
- **Spodek** kopíruje korunu zříceniny pod sebou (nejvyšší kámen v místě kusu), kde zeď chybí, stojí dostavba na terénu.
- **Vrch** dosahuje pod vrch trámů (latě a prkna leží na trámech) a v místě trámu pod jeho spodek, trámy procházejí zdivem. Pod šikmým trámem se kámen koruny rozdělí přes tloušťku na tři, aby každý kus dosáhl co nejvýš (mezera pod střechou je většinou do 5 cm; poslední řada se dorovná až pod střechu, když by nad ní zbylo méně než 12 cm).
- **Malta** (`mortar`): uprostřed tloušťky zdi je 10 cm silné jádro (kostky s materiálem jádra zříceniny `MI_RuinCore`) přes všechny spáry, takže zdí neprosvítá. Ve spárách vypadá jako malta. V Outlineru `Ostroh_Dostavba_Malta`.
  - **Malta až do země** (`mortar_down` = seznam zdí, teď jen `V`): jádro pokračuje pod dostavbou ve zdi zříceniny od terénu ke koruně. Kde v jeho rovině stojí lícový kámen zříceniny, je malta v téže rovině (vidět jen ve spárách). Druhá rovina malty (6 cm) je v prostřední vrstvě zdi mezi kameny jádra (`mid_off` = odsazení osy zdi zříceniny v m), takže zdí neprosvítá ani tam, kde chybí oba líce. Malta leží jen uvnitř kamenů zříceniny a ve spárách mezi nimi (v líci do 2,5 cm podél zdi a 4 cm mezi řadami, v jádru do 4 / 6 cm, protože lomové kusy jsou různě zapuštěné), nikdy v díře ani nad kamenem. Odkrytá koruna v okně se počítá jen do půlky výšky, mírně nakloněné kusy (do 6°) jen v části, kterou zabírají celou výškou. Spára mezi korunou zříceniny a dostavbou (do 5 cm) je vyplněná taky. Malta se počítá po 5 cm sloupcích podél zdi a sousední sloupce se stejně vysokým úsekem (do 1,5 cm) se slučují do jednoho souvislého kusu, bez mezer mezi kusy. Ve dveřích není, pod oknem končí pod parapetem.
  - Malta v kusech dostavby přechází spáry k sousedním kamenům. U otvoru, na konci zdi, pod střechou a pod parapetem končí 1,5–2 cm uvnitř kamene, takže nevylézá.
- **Otvory:** vrch dveří a okna i parapet jsou zarovnané na řady kamene. Kámen pod oknem tenčí než 15 cm se nepostaví, okno pak sahá až na korunu zříceniny. Nad otvorem leží dřevěné nadpraží přes jednu řadu, 25 cm na každé straně uložené ve zdi (`lintel`), staré neošetřené dřevo (`finish` → `lintels`).
- **Nadpraží o půl řady výš** (`lintel` → `half`): spodek nadpraží je v polovině řady, vrch v polovině další řady. Pod konci nadpraží jsou poloviční kameny až k jeho spodku, nad nadpražím poloviční kameny do další řady.
- **Práh** (`threshold`): dřevěný trám ve dveřích, v linii dostavby přes celou její tloušťku a šířku průchodu. Je 5 cm v zemi (`sink`) a 1,5 cm nad podlahou (`over`, výšku bere z podlahy `floor`). Je to **samostatný actor** (`Ostroh_Dostavba|Prah`), ne instance: můžeš s ním ručně pohnout a uložit to přes `Ostroh_Dostavba.py` s `MODE = "capture"` do `constructions_edits.json`. Další build polohu zachová. Staré neošetřené dřevo (`finish` → `threshold`).
- **Suť** uvnitř obytné části je uklizená (`clear_rubble`): `Sut.py` ji tam nepostaví.
- Polohy (osy dostaveb, trámy dokola příčky, otvory) počítá `gen_constructions.py` ze zdí v `ruin_layout.json` a z `ostroh_spec.py`. Výšky (koruna, střecha) se počítají až při buildu z postavené zříceniny a krovu.

**`addons` → `Ostroh_Podlaha`** (typ `plank_floor`): prkenná podlaha v obytné části u ostrohu.

- **Obrys** (`outline`): vnitřní líce zdí zříceniny (`ZBudova_V`, `ZBudova_S`, hradba), 2 cm od nich (`inset`). Počítá ho `gen_constructions.py`.
- **Podvaly** (`sleepers`): 14 × 10 cm, napříč prkny po 0,8 m, v kusech po 1,2 m. Leží na zemi (zapuštěné 3 cm) a kopírují terén, dehtované.
- **Prkna** (`planks`): 4,5 cm silná, 22–32 cm široká, 2,4–4,5 m dlouhá, podél `ZBudova_V`, spáry 6 mm. Spoje jsou přesazené a leží vždy na podvalu. Bez úpravy, jako ve věži.
- **Výška:** spodek prken je 10 cm nad nejvyšším terénem v obrysu. V nižších místech jsou podvaly vyšší.
- Prkna i podvaly se vyříznou kolem sloupů krovu (`avoid`) a kolem kamenů zříceniny, které u paty zdí zasahují do podlahy. U oblouku hradby proto okraj podlahy nesleduje líc přesně (zuby po šířce prkna).
- **Suť:** na podlaze se nepostaví (`Sut.py`).



**`frames` → `Palac_Kovarna_Pristresek`** (typ `pult_roof`, `zr_stavby\pult.py`): přístřešek kovárny ve východní místnosti paláce, v koutě mezi `Palac_J` a věží (`Vez_Z`). Návrh: [[navrh_palac_kovarna]]. Kostra, krytina s prostupem komína a lemování.

- **Rám stavby:** `origin`, `u`, `v` = rám paláce z `palac_spec.py` (`s` podél `Palac_J` k věži, `n` k severu), rozměry v metrech. `axis` = osa, po které střecha padá (`"u"`: spád k západu). Výšky se počítají od terénu v bodě `ref` (střed přístřešku).
- **Podpory** (`supports`): pozednice kolmé na spád, každá s polohou `at`, rozsahem `span`, vrchem `top`, průřezem `sec` a sloupy (`posts`, `post`).
  - `VE` u věže: 20 × 20 cm, vrch 4,24 m (spodek na spáře řad `Palac_J`, kapsa se zarovnává na řady). Jižní konec je 0,3 m v kapse `Palac_J` (03, `kapsa` z `palac_spec.py`), dál na sloupech n = 4,4 (mezi měchy a brusem) a 6,2, 10 cm od líce věže. V koutě sloup není, stojí tam výheň. Pozednice sahá do n = 6,4.
  - `VW` na západě: 18 × 18 cm, vrch 2,5 m, 3 sloupy (n = 0,9 / 3,55 / 6,2, rovnoměrně) v s = 25,85, těsně východně od výklenku střílny s = 25.
- **Patní kameny** (`pads`): plochý kámen z rozvalin 36 × 36 × 14 cm pod každým sloupem, 4 cm v zemi. Jsou to **samostatné actory** (`Palac_Kovarna_Pristresek|VE|K0` …), dají se ručně doladit a uložit přes `MODE = "capture"`.
- **Krokve** (`rafters`): 7 ks loupané kulatiny Ø 16 cm (`SM_RuinLog`), n = 0,9 až 6,3 po 0,9 m (rozšíření o řadu krokví k severu (Jirka 16. 11. 2026); krytina do n = 6,6), od s = 30,65 (10 cm před lícem věže) po s = 24,95 (přesah 0,9 m za západní pozednici; pod ním bude zvenku u stěny hranice dřeva). Sklon 20,3°, osedlání 3 cm (`seat`). Typ umí i hraněné krokve (`sec` místo `d`) a víc než dvě podpory (dům posádky).
- **Dřevo:** všechno `raw` (nad výhní žádný dehet).
- **Prostup komína** (`openings`): střed s = 30,0; n = 1,35 (mezi krokvemi n = 0,9 a 1,8), strana 0,5 m; vůle 12 cm od krokví, 20 cm od pozednice. Krytina kolem něj má mezeru 3 cm (`hole_gap`).
- **Krytina** (`roof`, 15. 11. 2026): stejná skladba jako u ostrohu, ale vlastní kód (`pult._pult_cover`): krokve jsou rovnoběžné, takže latě jdou přes celou šířku a prkna nejsou rozdělená do polí mezi trámy.
  - **latě** 6 × 5 cm napříč krokvemi (9 řad): u horního konce krokví, u okapu, těsně nad a pod prostupem komína, mezi nimi nejvýš po 0,9 m (`lath_step`);
  - **prkna** 3,5 cm, šířka 22–30 cm, spára 1,5 cm, po spádu od líce věže (mezera 0,5 cm) po okapovou hranu s = 24,85 (10 cm za konci krokví, `eave_over`, nad osou žlabu). Pásy se kladou od okrajů prostupu ven, prkna nad prostupem jsou rozdělená;
  - **lišty** 10 × 3,5 cm přes každou spáru, nahoře končí pod lemováním;
  - **od líce `Palac_J` mezera 3,5 cm** (`side_gap`): kameny koruny v s = 27–29 leží v úrovni střechy a vystupují z líce o 1–3 cm;
  - vrch krytiny: okap 2,36 m, u komína 4,27 m, u věže 4,54 m nad terénem. Pokrytí půdorysu mimo prostup 99,2 % (zbytek jsou mezery u zdí).
- **Lemování** (`flashing`): prkno 3,5 × 25 cm na stojato na krytině podél věže (horní okraj, 0,5 cm od líce) a podél `Palac_J` (na hraně krajního prkna).
- **Rozměry** jsou v `tools\ruin\palac_spec.py` (konstanty `K_*`, krytina `K_ROOF`, lemování `K_FLASH`). Po změně přegeneruj `gen_constructions.py`; když se mění východní pozednice (kapsa), i `gen_layout.py` a postav část `Palac`.
- **Kontrola a náhled:** `tools\checks\run_checks.py --only palac`, `tools\checks\preview3d.py kovarna <out.png>`.

**`addons` → `Palac_Kovarna_Vyhen`** (typ `hearth`, `zr_stavby\ohniste.py`): výheň v koutě mezi `Palac_J` a věží pod přístřeškem kovárny. Rám a výšky jako u přístřešku (`roof` = jméno střechy).

- **Stůl** (`table`): kámen z rozvalin, s = 29,75–30,73; n = 0,72–1,9 (2 cm od líce věže i `Palac_J`); výška 0,75 m ve 3 řadách, kameny střídavě podél a napříč. Nahoře hliněný maz 4 cm (`daub`, kostky s materiálem `MI_RuinDaub`).
- **Ohniště** (`pit`): 0,4 × 0,4 m pod komínem (střed s = 30,0; n = 1,35), dřevěné uhlí 2 cm pod úrovní mazu (`MI_RuinCharcoal`). Žhavé uhlí a oheň zatím nejsou.
- **Boční zídka** (`walls`): severně od stolu, n = 1,9–2,2, výška 1,2 m v 5 řadách, stojí na zemi. Ve 4. řadě (0,72–0,96 m) je otvor 0,2 m pro výfučnu měchů (`hole`).
- **Dymník** (`hood`): `SM_RuinSmokeHood` 1,4 × 1,2 × 1,0 m, spodní okraj 1,9 m (17. 11. 2026), střed v ose komína, východní okraj u věže.
- **Komín** (`chimney`): `SM_RuinChimney` 0,5 × 0,5 m od vrchu dymníku (2,8 m) do 5,5 m, 1,2 m nad krytinou.
- **Výměny** (`trimmers`): 2 loupané kulatiny Ø 10 cm mezi krokvemi n = 0,9 a 1,8, v úrovni krokví, 3 cm od komína na východ a na západ. Mezi nimi bude otvor v krytině.
- **Závěsné tyče** (`hangers`): 4 loupané tyče Ø 5 cm z konců výměn k rohům spodního okraje dymníku. Dymník tak nevisí ve vzduchu.
- **Rozměry** jsou v `tools\ruin\palac_spec.py` (`K_FORGE`, `K_FORGE_WALL`, `K_HOOD`, `K_CHIMNEY`, `K_TRIMMER`, `K_HANGER`).
- Typ je obecný: bez `walls`, `trimmers` a `hangers` postaví ohniště domu (základ, dymník, komín).

**`addons` → `Palac_Kovarna_Stena`** (typ `wattle_wall`, `zr_stavby\stena.py`, 15. 11. 2026): západní stěna kovárny z proutí omazaného hlínou v linii západních sloupů přístřešku.

- **Poloha:** s = 25,85; n = 0,7–6,3 (od líce `Palac_J` po severní sloup), výška 2,1 m nad terénem, tloušťka 8 cm, 3 cm v zemi. Pod západní pozednicí zůstává volný pruh 0,22 m.
- **Dílce** `SM_RuinWattlePanel` (1 × 1 m, rovné okraje) se skalují na pole mezi sloupy, nejvýš 1,1 × 1,05 m (`tile`). Spodní pás (do vrchu patních kamenů, 0,1 m) končí u patních kamenů, výš dílce končí u sloupů (mezera 0,5 cm).
- **Kůly** (`stake`): loupané Ø 9 cm na svislých spojích dílců (zakryjí spáry), 0,3 m v zemi, 6 cm nad stěnou.
- Rozměry: `palac_spec.py` → `K_WALL`. Sloupy a patní kameny bere z přístřešku (`posts`).

**`addons` → `Palac_Kovarna_Kul`** (typ `props`, `zr_stavby\vybaveni.py`): pevný kůl s kůrou Ø 10 cm zatlučený do země zvenku pod přesahem, 1,5 m od `Palac_J` (1,5 m nad zemí, 0,4 m v zemi). Od něj vede hranice dřeva, ta je vybavení.

**Vybavení kovárny** (kovadlina, měchy s pákou, brus, ponk, truhlík, nářadí s lištou, pruty, koš, hranice dřeva) je od 16. 11. 2026 v **`06_furnishing`** (skupina `Palac_Kovarna_Vybaveni`, [[06_furnishing]]). Typ `props` (`zr_stavby/vybaveni.py`) je společný: v 05 pro pevné kusy, v 06 pro přenosné. Úklid suti v celé východní místnosti dělá `clear_poly` u `Palac_Kovarna_Pristresek` (s = 21,35–30,8; n = 0,65–8,85).

**`addons` → `Palac_Kovarna_Okap`** (typ `gutter`, `zr_stavby\okap.py`, 15. 11. 2026): žlab pod západním okapem přístřešku a sud na dešťovou vodu.

- **Žlab:** loupaný vydlabaný kmen Ø 20 cm (`SM_RuinGutter`), osa s = 24,8 (pod okapovou hranou krytiny s = 24,85); n = 0,72–6,8 (0,2 m za okraj střechy); spád k severu 2,5 % (15 cm). Vrch 12 cm pod spodkem prken na jižním konci, 27 cm na severním (2,20 → 2,05 m nad terénem). Výška se počítá z krytiny střechy `roof` (`pult.roof_layers`).
- **Rozsochy:** 3 hlavy `SM_RuinForkHead` (ramena napříč žlabem) na kůlech s kůrou Ø 12 cm (0,4 m v zemi) v n = 1,7 / 4,0 / 6,3 (rovnoměrně). Jižní rozsocha je 1 m od líce `Palac_J` (průchod postavy k výklenku střílny s = 25, Jirka 16. 11. 2026), žlab k hradbě volně přesahuje o 1 m. Žlab leží ve vidlici: osa žlabu je 28 cm (varianta A) / 26 cm (B) nad středem hlavy (`FORK_SEAT`, změřeno na OBJ pro žlab Ø 20).
- **Sud** `SM_RuinBarrel` pod severním koncem žlabu (s = 24,8; n = 6,8), **samostatný actor** (dá se doladit a uložit přes capture). Svod se nedělá, voda padá ze žlabu asi 1,3 m.
- Rozměry: `palac_spec.py` → `K_GUTTER`, `K_BARREL`. Typ je obecný (pro `Palac_Obydli_Okap`), počítá se střechou typu `pult_roof`.

**Etapy stavby (sady actorů).** Stavba s klíčem `stage` v datech se staví po sadách: `base` (stojí už v etapě 1 a zůstává), `final` (dostavba, přibude v etapě 2), `site` (staveniště, jen v etapě 1). Každý actor sady má tag `stage:<sada>` a v názvu příponu (`…_Kamen_Base`). Přepnutí etapy ve hře = zobrazit a skrýt actory podle tagu: etapa 1 = `base` + `site`, etapa 2 = `base` + `final`. Dílec může mít vlastní sadu (`Stone.stage`), jinak patří do sady stavby; u ohniště dává `stage_top` sadu dymníku a komína. Sady jsou v `zrlib\config.py` (`STAGES`, `STAGE_TAG`). Stavby bez `stage` (věž, ostroh, kovárna) se nemění.

**`addons` → `Palac_Obydli_Kamen`** (typ `stone_fill`, `zr_stavby\zdivo.py`, sada `base`): kamenné části domu posádky v prostřední místnosti paláce. Návrh a plán po etapách: [[navrh_palac_obydli_stred]], kap. 0.

- **Části** (`parts`): obdélník v rámu paláce (`a` = s, `c` = n), vrch `top` v m nad terénem v bodě `ref`, mezery `gaps` (dveře).
  - `W`, `E`: srovnání korun `Palac_pricka_1` a `_2` na 1,4 m v celé tloušťce 0,8 m, včetně zazdění jejich dveří.
  - `N`: podezdívka severní srubové stěny (osa n = 6,2; 0,45 × 0,45 m), vchod s = 13,8–14,8 volný.
  - `P`: podezdívka srubové příčky (osa s = 15,75), dveře n = 3,3–4,3 volné.
- **Kámen** (`stone`): jako ve zdech hradu, řady 25–40 cm, kusy 35–60 cm, přes tloušťku po 0,42 m (`row`), spáry 1,5 cm, 10 cm v zemi (`sink`). Spodek každého kamene kopíruje zříceninu pod ním (po 5 cm podél zdi, kameny se v místě skoku dělí); kde zeď chybí, stojí zdivo na terénu.
- **Maltové jádro** (`mortar`, 6 cm, kostky s materiálem `MI_RuinCore`, v Outlineru `Palac_Obydli_Kamen_Malta_Base`): vyspravení staré zdi. Jde v ose zdi od země až 2 cm pod vrch přes nové zdivo i přes zříceninu pod ním (líc i jádro; kde jádro chybí, vyplní dutinu mezi líci), spáry a mezery do 12 cm překlene, ve dveřích a ve větší díře není. Počítá se po 5 cm podél zdi a sousední kroky se slučují do velkých kusů. Zdí neprosvítá.
- **Suť** v domě a na zápraží je uklizená (`clear_poly`, platí pro `Sut.py`).
- **`Palac_Obydli_Ohniste`** (typ `hearth`, sada `base`, `stage_top` = `final`): od 16. 11. 2026 pec s nístějí u jižní zdi ve světnici (návrh kap. 0.5b). Nové klíče `hearth`: `walls[].base` (zídka stojí na stole, ne na zemi), `dome` (hliněná klenba, mesh `SM_RuinOvenDome`, `tools\meshes\mesh_wattle.py`), `boxes` (kvádry: železo `iron`, uhlí `charcoal`; s `top` patří do sady `stage_top`, s `loose` je kvádr samostatný actor: plotna), `props` (hotový mesh jako samostatný actor: poklop ústí `SM_RuinOvenDoor`, `tools\meshes\mesh_props.py`), `flue` (sopouch, mesh komína). Kovárna je nepoužívá. Rozměry: `palac_spec.py` → `D_OVEN`.
- **Rozměry:** `tools\ruin\palac_spec.py` (`D_*`, funkce `obydli`). **Kontrola a náhled:** `run_checks.py --only obydli`, `preview3d.py obydli <out.png> [--stage 1|2]`.
- **`Palac_Obydli_Krov`** (typ `pult_roof`, 16. 11. 2026, zatím bez krytiny): spád k severu (`axis = "v"`), tři podpory. Nové klíče `pult_roof`: `pieces` (trám z více kusů, každý se svou sadou etapy), `stubs` (špalek pod trámem na zdi nebo srubu), `virtual` (podpora patří jiné stavbě, tady jen určuje sklon: vrchní trám srubu), `rafters.stages` (sada pro každou krokev), `pre_laths` (latě na krokvích už v kostře). Kovárna je nepoužívá, její data se nezměnila.
- **`Palac_Obydli_Srub`** (typ `log_wall`, `zr_stavby\srub.py`, 16. 11. 2026): stěna = seznam hranic řad `z`, úseky `segs` (rozsah řad, rozsah délky, volné zhlaví, sada etapy), otvory zarovnané na řady, řady v `half` jsou půltrámy (posun o půl řady proti křížící stěně → střídání v nároží). Kulatina je o `lap` tlustší než řada, zdí neprosvítá. Prkenné štíty (`gables`) sahají pod vrch krokví střechy `roof`, s výřezy pro pozednici a vaznici. Rozměry: `palac_spec.py` → `D_PLATE`, `D_PURLIN`, `D_RAFTER`, `D_LOG`, `D_WINDOWS`, `D_GABLE`, `D_STAGE_S`.
- **Přepnutí etapy v editoru:** `stavby\Etapa.py` (`ETAPA` 1 / 2 / 0, `JEN` = jen stavby s daným začátkem jména) zobrazí a skryje actory podle tagu `stage:<sada>` (editor, hra i kolize). Build staví vždy všechny sady viditelné, po buildu se pouští znovu.
- **Spuštění v UE:** celý dům `stavby\Palac_Obydli.py` (všechny hotové části v pořadí, se `SUT = True` i suť). Nová část domu se přidá do jeho seznamu `STAVBY`.

Souřadnice jsou v rámu věže: **u** vede od jihozápadního rohu podél jižní zdi (`Vez_J`), **v** od jihozápadního rohu k severu. Obojí v metrech, osy zdí jsou na 0 a 11 m.

**Dřevo:** tvary jsou meshe zašlého dřeva `SM_RuinTimber/Plank/Post_*` (praskliny, ohlazené hrany, prohyb; vlákna dělá normálová mapa materiálu, asi 2–3 tisíce trojúhelníků na kus). Generuje je `tools\meshes\gen_meshes.py` (modul `mesh_wood.py`, OBJ v `meshes\wood`), importují se automaticky do `/Game/Skvt/Lapikus/Ruin/Wood` a vypínají se přes `WOOD_MESHES = False` v `zrlib\config.py`. Úpravy dřeva (materiály vytvoří skript 03):

| Úprava | Materiál | Vzhled | Kde |
|---|---|---|---|
| dehet (`tar`) | `MI_RuinWood_Tar` | skoro hnědočerné, matné (staré zvětralé dehtování), vršky jen lehce vybledlé | masivní dřevo: trámy, průvlak, sloupy |
| krev (`blood`) | `MI_RuinWood_Blood` | starý nátěr volskou krví: tmavě červenohnědé, matné | venkovní ochoz u původního vstupu (trámy, vzpěry, prkna) |
| staré (`old`) | `MI_RuinWood_Old` | staré neošetřené: zašedlé až stříbřité, odbarvené, úplně matné, zaprášené a ochozené | prkna ve 2. patře (víc slunce a počasí) |
| bez úpravy (`raw`) | `MI_RuinWood` | šedohnědé, matné | vnitřní velké plochy: prkna v 1. patře a schody (ladí s podlahou) |
| olej (`oil`) | `MI_RuinWood_Oil` | teplá tmavší hnědá, polomatné | jemná práce a vnitřní stavební dřevo (zatím nepoužito) |

**Kulatina** (meshe z `tools\meshes\mesh_log.py`, OBJ v `meshes\wood`, v UE `/Game/Skvt/Lapikus/Ruin/Wood`): dílec je kulatina, když má `Stone.shape` (jinak hraněné dřevo podle rozměrů). Délka je vždy podél `sx` (svislý kůl = `pitch` 90°).

| `shape` | Mesh (`bark` = False / True) | Poznámka |
|---|---|---|
| `round` | `SM_RuinLog` / `SM_RuinLogBark`, při průměru do 11 cm (`POLE_MAX_D`) `SM_RuinPole` / `SM_RuinPoleBark` | kmen, tyč; sbíhavost, suky, prohnutí; u loupané stopy po loupáku, u kůry odloupnutá místa (asi 20 %) |
| `stake` | `SM_RuinStake` | kůl s kůrou, na +X zaseknutá špička (4–6 ploch) |
| `stake2` | `SM_RuinStakeSmall` | loupaný kůl, špičky na obou koncích |
| `fork` | `SM_RuinForkHead` | hlava rozsochy: kmen na −X, vidlice na +X. Na kůl se nasadí jako zvláštní dílec, aby se vidlice nenatahovala s délkou kůlu. |
| `gutter` | `SM_RuinGutter` / `SM_RuinGutterBark` | žlab: řez nahoře (+Z), vydlabaný vnitřek; zvenku loupaný (stopy po loupáku), nebo s kůrou |

- **Materiálové sloty:** `Wood` = materiál podle úpravy dílce (`cat`: `raw`, `tar`, `old`… a nově `peeled` = `MI_RuinWood_Peeled`, čerstvě loupané světlé dřevo), `EndGrain` = čela `MI_RuinWood_EndGrain` (letokruhy, trhliny), `Bark` = kůra `MI_RuinBark`. Materiály slotů vytvoří skript 03 (`SLOT_MI` v `zrlib\config.py`), vzhled v `MAT_LOOK["bark"]`, `["endgrain"]`, `["wood_peeled"]`.
- **Textury** kůry a čel jsou vlastní, procedurální (`tools\textures\gen_textures.py`). Čela mají polární UV (u = úhel, v = vzdálenost od středu), takže letokruhy jsou soustředné a s náhodným posunem materiálu každé čelo jiné.
- **Rozměry a varianty:** `ROUND_MESHES` v `zrlib\config.py` (musí odpovídat `NOMINAL` v `mesh_log.py`).
- **Ukázka v UE:** `tools\meshes\Ukazka_Meshe.py` postaví kulatinu ve třech řadách (`peeled`, `raw`, `tar`) a za ní řadu ostatních knihovních meshí, na `ORIGIN`. Má tag `Ukazka_Meshe` a `MODE = "clear"` ji smaže (i starší ukázku `Ukazka_Kulatina`). Import a materiály dělá mimo transakci, Undo vrátí jen actory. Level zříceniny ani stavby nemění.

**Další knihovní meshe** (`LIB_MESHES` v `zrlib\config.py`, dílec = `Stone` se `shape` z `LIB_SHAPES`, `cat` = materiál):

| `shape` | Mesh | Kategorie (UE) | Sloty | `cat` | Poznámka |
|---|---|---|---|---|---|
| `bark_strip` | `SM_RuinBarkStrip` 160 × 70 cm | `wood` (`Ruin/Wood`) | `Bark`, `EndGrain` (spodek = lýko) | `bark` | pás kůry, délka podél X = po spádu, hrubá strana nahoru (+Z) |
| `wattle_panel` | `SM_RuinWattlePanel` 100 × 8 × 100 cm | `wattle` (`Ruin/Wattle`) | `Daub`, `Wattle` | `daub` | dílec stěny v rovině XZ, rovné okraje → skládá se vedle sebe a nad sebe |
| `smoke_hood` | `SM_RuinSmokeHood` 140 × 120 × 100 cm | `wattle` | `Daub`, `Wattle` | `daub` | dymník, škáluje se na rozměr |
| `chimney` | `SM_RuinChimney` 60 × 60 × 100 cm | `wattle` | `Daub`, `Wattle` | `daub` | komín, výška přes `sz` |
| `rope` | `SM_RuinRope` 100 × 1,5 cm | `textile` (`Ruin/Textile`) | `Rope` | `rope` | článek lana; prověšené lano = řetěz článků podél řetězovky |
| `lashing` | `SM_RuinLashing` 7 × 10,5 cm | `textile` | `Rope` | `rope` | ovázání tyče Ø 8 cm (osa X), škáluje se s tyčí |

**Props** (`tools\meshes\mesh_props.py`, kategorie `props`, OBJ v `meshes\props`, v UE `/Game/Skvt/Lapikus/Ruin/Props`): vlastní procedurální modely, dílec = `Stone` se `shape` z `LIB_SHAPES`, rozměry v `LIB_MESHES`. Slot `Wood` = materiál dílce (`cat`, úprava dřeva), ostatní sloty pevné.

| `shape` | Mesh | Rozměr (cm) | Sloty |
|---|---|---|---|
| `stump` | `SM_RuinStump_A–B` | Ø 50 × 47 | Wood, EndGrain, Bark |
| `anvil` | `SM_RuinAnvil` | 59 × 18 × 24 | IronClean |
| `bellows` | `SM_RuinBellows` (měch na rámu s příčkami, výfučna, horní deska s rukojetí z jednoho kusu) | 210 × 85 × 139 | Wood, Iron, Leather |
| `barrel` | `SM_RuinBarrel` (kalicí sud z 18 dužin se spárami, dno, obruče, voda) | Ø 61 × 80 | Wood, EndGrain, Iron, Water |
| `grindstone` | `SM_RuinGrindstone` (kotouč na ose v ložiskách, spodek 3 cm ve vodě, rám s příčkami, ruční klika, koryto na 4 nohách) | 120 × 86 × 105 | Wood, Iron, Sandstone, Water |
| `grindstone_treadle` | `SM_RuinGrindstoneTreadle` (šlapací: kliková páka, ojnice, šlapadlo na čepu u zadní nohy, strana +Y) – **použít v kovárně** | 120 × 86 × 105 | Wood, EndGrain, Iron, Sandstone, Water |
| `stool` | `SM_RuinStool` (třínohá stolička k brusu) | 35 × 33 × 45 | Wood, EndGrain |
| `workbench` | `SM_RuinWorkbench` (ponk se svěrákem, podélná příčka prostředkem) | 222 × 86 × 85 | Wood, Iron |
| `tongs`, `hammer`, `chisel` | `SM_RuinTongs`, `SM_RuinHammer` (kladivo s příčným penem: hlava 11 cm, tlouk a pena souměrně kolem oka, toporo prochází okem), `SM_RuinChisel` | 50, 36, 21 délka | IronClean (kladivo + Wood, EndGrain) |
| `mallet` | `SM_RuinMallet` (dřevěná palice do jedné ruky: hlava Ø 9 × 14 cm, na koncích železné obruče proti roztřepení) | 10 × 35 × 14 | Wood, EndGrain, IronClean |
| `nail_hammer` | `SM_RuinNailHammer` (tesařské kladivo na hřebíky: kulatá úderná plocha, rozpolcený drápák zahnutý k toporu, toporo u hlavy tenčí, prochází okem) | 3 × 34 × 11 | Wood, EndGrain, IronClean |
| `broadaxe` | `SM_RuinBroadaxe` (širočina: ostří ~27 cm s bradou k toporu, broušená jen z líce, plynulý náběh z oka do čepele, toporo 70 cm vyhnuté od rubu, prochází okem) | 7 × 72 × 25 | Wood, EndGrain, IronClean |
| `axe` | `SM_RuinAxe` (sekera na štípání: klínovitá hlava s týlem, ostří ~11 cm, čepel vychází z oka, toporo 75 cm prochází okem) | 5 × 77 × 19 | Wood, EndGrain, IronClean |
| `crosscut_saw` | `SM_RuinCrosscutSaw` (dvoumužná pila: list 152 cm s břichem a zuby, ke koncům užší, svislé rukojeti 3 cm od konců listu) | 151 × 4 × 28 | Wood, EndGrain, IronClean |
| `bed`, `bed_folded` | `SM_RuinBed` (lůžko: nohy, čelo v hlavě, bočnice, laťky, sypaná sláma, houně přes slámu s převisem do stran), `SM_RuinBedFolded` (houně složená v nohách) | 200 × 87 × 62 | Wood, Straw, Wool |
| `table` | `SM_RuinTable` (stůl: deska ze 3 prken, rozkročené nohy, luby, příčky dole) | 120 × 70 × 76 | Wood |
| `chest` | `SM_RuinChest` (truhla: prkna, nožky, zavřené víko, železné pásy, závěs s okem na zámek, držadla) | 95 × 55 × 51 | Wood, Iron |
| `shelf` | `SM_RuinShelf` (police na osobní věci, stojí u zdi stranou +Y: 2 bočnice, 3 desky, zadní lišta) | 100 × 28 × 90 | Wood |
| `door` | `SM_RuinDoor` (dveře 1,0 × 2,2 m: 4 prkna, zezadu 3 svlaky a vzpěry Z, na líci (−Y) pásové závěsy na ose X = −50, kruh, zástrčka) | 102 × 9 × 219 | Wood, Iron |
| `shutter` | `SM_RuinShutter` (okenice 60 × 60: 3 prkna, 2 svlaky, závěsy na ose X = −30, kolík; pro okénko 50 × 50 škálovat 0,83) | 61 × 8 × 59 | Wood, EndGrain, Iron |
| `nail_header` | `SM_RuinNailHeader` | 25 × 6 × 1,5 | IronClean |
| `coal_box` | `SM_RuinCoalBox` (truhlík s uhlím: ~420 kousků na tmavém podkladu, bez víka) | 81 × 121 × 80 | Wood, Charcoal |
| `coal_box_lid` | `SM_RuinCoalBoxLid` (volné víko truhlíku bez pantů: 3 prkna, 2 lajsny zespodu, držadlo; položit bokem nebo na truhlík) | 80 × 120 × 11 | Wood |
| `woodpile` | `SM_RuinWoodpile` (štípaná polena, délka podél Y) | 191 × 65 × 136 | Wood, EndGrain, Bark |
| `iron_bars` | `SM_RuinIronBars` (svazek prutů) | 103 × 9 × 4 | Iron |
| `basket` | `SM_RuinBasket` | Ø 44 × 37 | Wattle |
| `ladder` | `SM_RuinLadder` (tyče s kůrou, příčle po 30 cm) | 450 × 54 × 8 | Wood, EndGrain, Bark |

- Materiály lůžka: `MI_RuinStraw` (sláma, textura `T_RuinStraw`), `MI_RuinWool` (houně z nebarvené vlny, `T_RuinWool`); sloty Straw, Wool.
- Materiály props: dvě železa – `MI_RuinIron` (slot Iron, s patinou tlumeně hnědé rzi, `Metallic` 0,5: kování, obruče, osy, pruty) a `MI_RuinIronClean` (slot IronClean, bez rzi, `Metallic` 0,8: nářadí a kovadlina); barva v textuře `T_RuinIron` / `T_RuinIronClean` (`TEX_VERSION` 4, `MAT_VERSION` 10, `MAT_RESET` iron 10), `MI_RuinLeather`, `MI_RuinSandstone` (StarterContent), `MI_RuinWater`, `MI_RuinCharcoal` (černou barvu dává tint, textura je jen světlý detail). Parametr `Metallic` je nově v `M_RuinStone` (výchozí 0, kámen a dřevo beze změny; `MAT_VERSION` 8 → master se při buildu přestaví).
- Náhled: `05_constructions\Props_kovarna_nahled.png`, textury `Props_textury_nahled.png`.

- **Materiály:** `MI_RuinRope`, `MI_RuinWattle`, `MI_RuinDaub`, `MI_RuinChinking` (výplň spár srubu, textura mazaniny) na `M_RuinStone`; plátno `MI_RuinCanvas` na novém `M_RuinCloth` (oboustranný). Vzhled v `MAT_LOOK` (`zrlib\config.py`).
- **Skvrny plachty:** textura plátna (dlaždice 25 cm) je bez skvrn, jinak by se opakovaly. Skvrny a zašednutí dává velká textura `T_RuinCanvasMacro` (dlaždice 4 m), kterou `M_RuinCloth` přimíchá: `MacroAmount` (síla, výchozí 0,6), `MacroTiling` (0,25 = dlaždice 4 m).
- **Plátno na míru:** `mesh_textile.make_canvas(okap0, okap1, hřeben0, hřeben1, rafters=…, sag=…)` vrátí plachtu prověšenou mezi tyčemi (cm, souřadnice stavby), `write_canvas` ji zapíše jako OBJ. Ukázka `SM_RuinCanvasSample_A` (3 × 2,4 m, 5 tyčí, sklon 22,6°). Stavba ji používá přes `canvas_vez` + `write_fitted` (OBJ vystředěný na bounding box + `<mesh>.json` se středem a rozměrem v osách stavby; typ `canvas_shelter` mesh podle něj posadí).
- **Vítr:** `M_RuinCloth` posouvá vrcholy podél normály: `WindAmount` (cm, výchozí 0 = staticky), `WindSpeed`, `WindScale`. Zapnout v `MI_RuinCanvas` nebo v `MAT_LOOK["canvas"]`. Úchyty na tyčích se zatím hýbou stejně jako zbytek plachty, proto jen malé hodnoty (1–3 cm).

Master `M_RuinStone` má kvůli tomu parametry `Desaturate` (odbarvení textury, 0–1) a `DustAmount` / `DustTint` (zaprášení). U ostatních materiálů jsou na 0, takže se nic nemění. Rozdělení se mění v `constructions.json` → `finish` (výchozí hodnoty jsou v `WOOD_FINISH_DEFAULT` v `zrlib\config.py`). Neošetřené dřevo je `MI_RuinWood`, který vytvoří skript 03. Je to zašlé nelakované dřevo, šedohnědé a matné. Každý trám a prkno má trochu jiný odstín a vršky jsou vybledlé od slunce. Ladí se v `MI_RuinWood` (`TintA`/`TintB`, `Roughness`) nebo v `MAT_LOOK["wood"]` v `zrlib\config.py`. Vlastní materiál nastavíš v `MAT_WOOD_MI` (tamtéž).

---

#### Přístřešek hlídky na věži (`Vez_Pristresek`, typ `canvas_shelter`)

- **Kód:** `zr_stavby/pristresek.py`, data `gen_constructions.py` → `vez_pristresek` z `tools/ruin/tower_spec.py` (`PR`, `pristresek()`); ram věže `u`, `v` (m), výšky `h` v m od `VEZ_F`.
- **Dílce:** kůly s hlavou rozsochy (hlava zvětšená `fork_k` na průměr kůlu, osa hřebene nad středem hlavy `seat` změřená na OBJ), hřeben z kusů, okapová tyč na podkladních kamenech (výška z postavené koruny, kámen koruny musí pod podkladem zasahovat aspoň 3 cm), krokvové tyče, vzpěry, ovázání (`SM_RuinLashing` zvětšené na průměr tyče), plachta a štít na míru, tyčka v lemu štítu, lana z článků `SM_RuinRope` přes plachtu ke kotevním kamenům, zátěžové kameny.
- **Plachta na míru:** `python tools/meshes/gen_meshes.py textile` → `meshes/textile/SM_RuinCanvasVez_A.obj` + `.json`, `SM_RuinCanvasVezGable_A.obj` + `.json`. Lokální osy meshe X = u, Y = −v, Z = h (ram věže je v UE levotočivý). Po změně `PR` (polohy, sklon) vždy přegenerovat meshe i `constructions.json` a zvýšit verzi `SM_RuinCanvasVez` v `STONE_MESH_VERSION`.
- **Ruční doladění:** podkladní, zátěžové a kotevní kameny jsou samostatné actory (`Vez_Pristresek.py`, `MODE = "capture"`).
- **Kontroly:** `run_checks.py --only vez`, náhled `preview3d.py vez` (plachta jako tenké kvádry).

## Dopad na dokumentaci
Doplní se při rozpadu.

## Známé pasti
Doplní se při rozpadu.

## Další rozvoj
### 5. Do budoucna

Sem patří další dostavby druhého zabydlení: žlab a okapnice u ostrohu, lemování horního okraje krytiny, hlídková konstrukce na `Brana_S`, žebříky, lávky, dřevěné přístřešky, ohrady, provizorní střechy, zábrany v průlomech. Každá nová stavba je další položka v `constructions.json` a případně nový typ v `build_constructions.py`.
