---
# orchestrace
type: step
validity: valid
aliases: [README_constructions]
step_kind: build
updated: 2026-11-24
# hra
build_step: 05_constructions
domains: [structures]
---
# 05 Constructions – dodatečné stavby a suť („druhé zabydlení“) – návod pro UE 5.8

## Souhrn
Dodatečné stavby „druhého zabydlení“ a suť, stavěné zvlášť od zříceniny (`build_constructions.py`, data `constructions.json` z `gen_constructions.py`). Tady je postup v UE, co kdy přegenerovat, skripty a soubory; data jednotlivých skupin staveb jsou v částech:
- [[05_constructions_ostroh]]: krov, dostavba a podlaha u ostrohu;
- [[05_constructions_kovarna]]: přístřešek, výheň, stěna, kůl a okap kovárny;
- [[05_constructions_dum]]: dům posádky (`Palac_Obydli_*`);
- [[05_constructions_vez]]: patra ve věži a přístřešek hlídky;
- sdílené meshe: [[Meshe]] (dřevo, kulatina, knihovní meshe), [[Meshe_props]] (props).

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

Usazené kameny ve hře spí, dokud do nich někdo nestrčí. Staticky bez fyziky: `MODE = "freeze"` (do dalšího buildu) nebo `RUBBLE_PHYSICS = False`. Jak silně hráč tlačí, se nastavuje v Character Movement postavy (viz [[03_ruin_upravy]], kap. 5.3).

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
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_postel_nahled.png` | data | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_stojan_brneni_nahled.png` | data | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_truhla_nahled.png` | data | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Knihovna_meshe_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Knihovna_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Kulatina_meshe_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Kulatina_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Props_kovarna_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Props_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_luzko_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_luzko_slozena_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_plachta_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_truhlicka_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_vak_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_prikop_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_straz_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_straz_nahled_etapa1.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_drevo_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_nadvori_stan_nahled.png` | data | [[Lapikus]] | – |
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
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana.py` | entry | [[Brana]] | [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Capture.py` | entry | [[Brana]] | [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Most.py` | entry | [[Brana]] | [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Most_Kamen.py` | entry | [[Brana]] | [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz.py` | entry | [[Brana_Straz]] | [[navrh_brana_straz]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kamen.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kryty.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Podesta.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Zataras.py` | entry | [[Brana]] | [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Etapa.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Nadvori_Stan.py` | entry | [[Nadvori_Stan]] | [[navrh_nadvori_stan]], [[05_constructions]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Nadvori_Stan_Capture.py` | entry | [[Nadvori_Stan]] | [[navrh_nadvori_stan]], [[05_constructions]] |
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
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Stavenisko.py` | entry | [[Palac_Obydli]] | [[navrh_palac_obydli_stred]], [[stav_palac_obydli]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Stavenisko_Capture.py` | entry | [[Palac_Obydli]] | [[navrh_palac_obydli_stred]], [[stav_palac_obydli]] |
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
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/stan.py` | library | [[Nadvori_Stan]] | [[navrh_nadvori_stan]], [[05_constructions]] |
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
| `stavby\<Stavba>.py` | **spuštění jedné stavby**: `Vez_Patra.py` (dřevo ve věži), `Ostroh_Krov.py` (krov u ostrohu), `Ostroh_Dostavba.py` (kamenná dostavba u ostrohu), `Ostroh_Podlaha.py` (prkenná podlaha u ostrohu), `Palac_Kovarna.py` (**celá kovárna najednou**: přístřešek, výheň, stěna, okap, vybavení; přepínače `KRYTINA`, `RUIN` = i část zříceniny `Palac`, `SUT`), `Palac_Kovarna_Pristresek.py` (přístřešek kovárny v paláci), `Palac_Kovarna_Vyhen.py` (výheň kovárny), `Palac_Kovarna_Stena.py` (stěna z proutí), `Palac_Kovarna_Okap.py` (žlab a sud), `Palac_Kovarna_Kul.py` (kůl u dřeva), **`Palac_Obydli.py` (celý dům posádky najednou: seznam staveb, `SUT`)**, `Palac_Obydli_Kamen.py` a `Palac_Obydli_Ohniste.py` (jeho kamenné části a základ ohniště), `Palac_Obydli_Krov.py` (krov bez krytiny), `Palac_Obydli_Srub.py` (srub a štíty), `Palac_Obydli_Stavenisko.py` (celé staveniště etapy 1: vzpěry, žebřík a tři hranice) a `Palac_Obydli_Stavenisko_Capture.py` (uložení ručních úprav staveniště), **`Brana_Straz.py` (celé strážní stanoviště nad branami: seznam staveb, `RUIN` = i část zříceniny `Obvod`, `SUT`)**, `Brana_Straz_Kamen.py`, `Brana_Straz_Podesta.py` a `Brana_Straz_Kryty.py`, **`Brana.py` (celé přemostění šíjového příkopu a zátaras: `Brana_Most_Kamen`, `Brana_Most`, `Brana_Zataras`, přepínače `RUIN`, `SUT`)**, `Brana_Capture.py` (uložení posunu/natočení zátarasu v UE), `Brana_Most_Kamen.py`, `Brana_Most.py` a `Brana_Zataras.py`, `Etapa.py` (přepnutí etapy v editoru), `Sut.py` (suť). Nahoře `MODE` (`build` / `capture`, u suti i `freeze`). V `Ostroh_Krov.py` navíc `KRYTINA`: `False` postaví jen sloupy, příčku a trámy (ladění trámoví a dostavby), `True` i latě, prkna, lišty a hřeben. Dostavba je na krytině nezávislá (výšky bere z trámů). Stejný přepínač `KRYTINA` má `Palac_Kovarna_Pristresek.py` (výchozí `True`). |
| `build_constructions.py` | nastavení, registr typů staveb (`TYPES`, povinné klíče `REQUIRED`), build / capture / freeze v UE. Spuštěný přímo postaví všechny stavby najednou. Mimo UE vypíše počty kusů. |
| `zr_stavby\*.py` | typy staveb: `vez.py` (dřevo ve věži, `tower_floor`), `krov.py` (krov u ostrohu `fan_roof` + společná geometrie), `dostavba.py` (`stone_addon`), `podlaha.py` (`plank_floor`), `pult.py` (pultová střecha na sloupech, `pult_roof`), `ohniste.py` (ohniště / výheň s dymníkem a komínem, `hearth`), `zdivo.py` (zdivo z kamene rozvalin: srovnání korun, podezdívky, `stone_fill`), `stena.py` (stěna z proutí, `wattle_wall`), `okap.py` (žlab na rozsochách se sudem, `gutter`), `vybaveni.py` (rozmístění props, `props`), `srub.py` (srubové stěny a prkenné štíty, `log_wall`), `podesta.py` (trámy, prkna a zábradlí ve výšce zadané absolutně, `platform`), `kryty.py` (kryt z kůlů se špičkou na koruně zdi, paty kopírují korunu, průzory, ráhna, `palisade`) |
| `..\zrlib\*.py` | sdílená knihovna s 03 (`config.py` = materiály, dřevo, fyzika; geometrie, Unreal; `pipeline.py` = spouštění: stavby, části, `build_normal.py`, `build_fullscope.py`) |
| `constructions.json` | data staveb (`floors` → `Vez_Patra`, `frames` → `Ostroh_Krov`, `Palac_Kovarna_Pristresek`, `addons` → `Ostroh_Dostavba`, `Ostroh_Podlaha`, `Palac_Kovarna_Vyhen`, `Palac_Kovarna_Stena`, `Palac_Kovarna_Okap`) a nastavení suti (`rubble`) |
| `Stavby_palac_kovarna_nahled.png` | náhled kovárny ve východní místnosti paláce (přístřešek s krytinou, výheň, stěna z proutí, okap se sudem; 8 pohledů, dílce jsou v náhledu jen kvádry) |
| `Stavby_ostroh_dostavba_nahled.png` | náhled uzavřené obytné části u ostrohu zvenku a zevnitř |
| `Stavby_ostroh_podlaha_nahled.png` | náhled podlahy u ostrohu |
| `Stavby_palac_obydli_nahled.png` | náhled domu posádky v prostřední místnosti paláce, etapa 2 (nový kámen je v náhledu okrový); `Stavby_palac_obydli_nahled_etapa1.png` = etapa 1 se staveništěm (pohledy na vzpěry v síni a hranice na nádvoří) |
| `constructions_edits.json` | ručně smazané (`removed`) a posunuté (`moved`) kusy. Vzniká přes capture, nepřepisovat. |
| `Stavby_vez_nahled.png` | řez věží: patra, schody, ochoz |
| `..\tools\constructions\gen_constructions.py` | vytvoří `constructions.json` z `ruin_layout_draft.json` |
| `..\tools\constructions\check_tower.py` | náhled řezu věží bez Unrealu (zřícenina + stavby) |
| `..\tools\ruin\tower_spec.py` | **společné rozměry věže** pro 03 i 05 (podlaha, výška patra, polohy trámů, průvlaku, otvorů, dveří) |
| `..\tools\ruin\palac_spec.py` | **společné rozměry staveb v paláci**: souřadný rám paláce (`s` podél `Palac_J`, `n` k severu) a kovárna (linie sloupů, pozednice, krokve, komín) |

Skript používá generátor zříceniny jako knihovnu. Složka `03_ruin\blocks` proto musí ležet vedle `05_constructions` (jinak v `build_constructions.py` nastav `RUIN_DIR`) a v kořeni musí být `zrlib`.

---

### 4. Co je v `constructions.json`
Data staveb po skupinách: [[05_constructions_ostroh]], [[05_constructions_kovarna]], [[05_constructions_dum]], [[05_constructions_vez]] (klíče `floors` věže). Meshe dílců: [[Meshe]] a [[Meshe_props]]. Klíč `rubble`: suť (`enabled`, složka v Outlineru).

**Etapy stavby (sady actorů).** Stavba s klíčem `stage` v datech se staví po sadách: `base` (stojí už v etapě 1 a zůstává), `final` (dostavba, přibude v etapě 2), `site` (staveniště, jen v etapě 1). Každý actor sady má tag `stage:<sada>` a v názvu příponu (`…_Kamen_Base`). Přepnutí etapy ve hře = zobrazit a skrýt actory podle tagu: etapa 1 = `base` + `site`, etapa 2 = `base` + `final`. Dílec může mít vlastní sadu (`Stone.stage`), jinak patří do sady stavby; u ohniště dává `stage_top` sadu dymníku a komína. Sady jsou v `zrlib\config.py` (`STAGES`, `STAGE_TAG`). Stavby bez `stage` (věž, ostroh, kovárna) se nemění.

## Dopad na dokumentaci
Doplní se při rozpadu.

## Známé pasti
Doplní se při rozpadu.

## Další rozvoj
### 5. Do budoucna

Sem patří další dostavby druhého zabydlení: žlab a okapnice u ostrohu, lemování horního okraje krytiny, hlídková konstrukce na `Brana_S`, žebříky, lávky, dřevěné přístřešky, ohrady, provizorní střechy, zábrany v průlomech. Každá nová stavba je další položka v `constructions.json` a případně nový typ v `build_constructions.py`.
