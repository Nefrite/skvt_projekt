# 05 Constructions – dodatečné stavby a suť („druhé zabydlení“) – návod pro UE 5.8

Do této složky patří všechno, co do zříceniny později přistavěli její obyvatelé, a volná suť na zemi. Staví se **zvlášť od zříceniny**: když ladíš schody, trámy nebo podestu, nemusíš přegenerovat celý hrad.

| Kde | Co |
|---|---|
| **03_ruin** (`03_ruin\blocks\build_ruin_blocks.py`) | zřícenina jako taková: zdi, otvory, ostění, kapsy pro trámy, kamenná dlažba přízemí věže |
| **05_constructions** (`build_constructions.py`) | dřevěné vestavby: trámy, prkna, průvlak se sloupy, provizorní schody, ochoz. Volná suť u zdí. |

Kapsy ve zdech patří ke zřícenině. Dřevo, které v nich leží, patří sem.

---

## 1. Soubory

| Soubor | Obsah |
|---|---|
| `build_constructions.py` | stavba v UE (`MODE = "build"`) a uložení ručních úprav (`MODE = "capture"`). Mimo UE vypíše počty kusů. |
| `constructions.json` | data staveb (`floors` → `Vez_Patra`) a nastavení suti (`rubble`) |
| `constructions_edits.json` | ručně smazané (`removed`) a posunuté (`moved`) kusy. Vzniká přes capture, nepřepisovat. |
| `Stavby_vez_nahled.png` | řez věží: patra, schody, ochoz |
| `..\tools\constructions\gen_constructions.py` | vytvoří `constructions.json` z `ruin_layout_draft.json` |
| `..\tools\constructions\check_tower.py` | náhled řezu věží bez Unrealu (zřícenina + stavby) |
| `..\tools\ruin\tower_spec.py` | **společné rozměry věže** pro 03 i 05 (podlaha, výška patra, polohy trámů, průvlaku, otvorů, dveří) |

Skript používá generátor zříceniny jako knihovnu. Složka `03_ruin\blocks` proto musí ležet vedle `05_constructions`, jinak v `build_constructions.py` nastav `RUIN_DIR`.

---

## 2. Postup v UE

1. **Nejdřív zřícenina:** `03_ruin\blocks\build_ruin_blocks.py`. Ta změří terén (`terrain_from_level.json`) a postaví zdi a kapsy.
2. **Pak stavby:** **Tools → Execute Python Script → `05_constructions\build_constructions.py`.**
   - Smaže jen svoje actory (tag `Zricenina_Stavby`) a postaví je znovu.
   - Zříceniny se nedotkne. Build zříceniny zase nesmaže stavby.
3. V Outlineru přibude:
   - `Stavby/Vez/Vez_Patra_Drevo`: trámy, prkna, průvlak, sloupy, schody a ochoz (Instanced Static Mesh),
   - `Stavby/Sut/<část hradu>/Kamen_…`: kameny suti jako samostatné actory.

**Rychlé ladění jen jedné části:** `ONLY = ["Vez_Patra"]` (jen dřevo) nebo `ONLY = ["Sut"]` (jen suť).

**Ruční úpravy:** smaž instanci nebo kámen, posuň kámen suti, pak nastav `MODE = "capture"` a spusť skript. Změny se zapíšou do `constructions_edits.json` a platí i po dalším buildu.

**Fyzika suti:** kameny suti mají trvalou fyziku (`RUBBLE_PHYSICS = True`, tag `Ruin_Physics`), takže s nimi hráč může pohnout. Hmotnost odpovídá objemu kamene, většinou 20–280 kg. Nastavení je v `STONE_PHYSICS` v `03_ruin\blocks\build_ruin_blocks.py` a je společné s odpadlými kusy zdi.

1. Usazení: spusť **Simulate** (Alt+S) a kameny se usadí na terénu a o sebe.
2. Vyber je (Outliner `Stavby/Sut` nebo tag `Ruin_Physics`), stiskni **K** (Keep Simulation Changes) a simulaci ukonči.
3. `MODE = "capture"` uloží jejich polohy.

Usazené kameny ve hře spí, dokud do nich někdo nestrčí. Staticky bez fyziky: `MODE = "freeze"` (do dalšího buildu) nebo `RUBBLE_PHYSICS = False`. Jak silně hráč tlačí, se nastavuje v Character Movement postavy (viz `README_bloky.md`, kap. 5.3).

---

## 3. Kdy co přegenerovat

| Změna | Co spustit |
|---|---|
| schody, prkna, ochoz, sloupy, suť (v `constructions.json` nebo `gen_constructions.py`) | jen `build_constructions.py` |
| **polohy trámů, průvlaku, otvorů nebo dveří** (`tower_spec.py`), **krov u ostrohu** (`ostroh_spec.py`) | `gen_layout.py` **i** `gen_constructions.py` (kapsy jsou ve zdech), pak oba buildy |
| zdi, rozpad, otvory zříceniny | `build_ruin_blocks.py`, pak `build_constructions.py` (trámy se kontrolují proti zdem) |

Trám nebo průvlak se nepostaví, když zeď u jeho kapsy spadla.

---

## 4. Co je v `constructions.json` (Vez_Patra)

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

- **Sloupy a příčka:** 2 sloupy stojí těsně u vnitřního líce `ZBudova_V`, po stranách průchodu, 10 cm od jeho hran (`POST_SPREAD`). Průchod 1,6 m (`PASS_W`) zůstává volný. Na sloupech leží příčka (vaznice), 3,8 m dlouhá, s přesahem 85 cm na každou stranu. Šikmé vzpěry vedou od sloupů ven a hlavou podpírají přesahy příčky.
- **Paprskovité trámy:** 7 trámů 22 × 24 cm vede z příčky na hradbu `Hradba_Z_S`.
- **Hradba:** je v tomto úseku cíleně snížená a zarovnaná, asi 3 m nad terénem.
- **Uložení:** trámy leží ve žlábcích koruny, u vnitřního líce zhruba do poloviny výšky trámu. Mírně se svažují ke zdi (6–10°, příčka 0,8 m nad dnem žlábků, `RISE`) a 0,6 m přesahují vnější líc (okap).
- **Dřevo:** všechno je dehtované (`finish`).
- **Rozměry:** jsou v `tools/ruin/ostroh_spec.py` a sdílí ho 03 (snížení a žlábky) i 05 (dřevo). Po změně přegeneruj `gen_layout.py` i `gen_constructions.py` a postav 03 i 05.

- **Krytina** (`roof`, všechno dehtované):
  - **Latě:** 5 řad napříč trámy.
  - **Prkna:** po spádu, 22–30 cm široká, se spárami 1,5 cm. V každém poli mezi trámy leží rovnoběžně. Krajní jsou kratší a vyplňují klín, jak se pole ke zdi rozšiřuje. Začínají už tam, kde se do pole dostane jejich vnitřní hrana, takže u trámů nezůstávají díry. Sousední pole se u trámu překrývají (každé druhé o tloušťku prkna výš).
  - **Lišty:** přes každou spáru. Přes každý trám leží krycí prkno 36 cm, které zakryje spoj dvou polí.
  - **Lemování u příčky:** zatím není, vyřeší se jinak.
- **Koruna pod střechou:** kameny hradby mezi trámy jsou směrem ven snížené ve sklonu střechy (`roof_clear` v 03), aby nezasahovaly do latí a prken.

Žlab, okapnice a sud přijdou později.

Souřadnice jsou v rámu věže: **u** vede od jihozápadního rohu podél jižní zdi (`Vez_J`), **v** od jihozápadního rohu k severu. Obojí v metrech, osy zdí jsou na 0 a 11 m.

**Dřevo:** tvary jsou meshe zašlého dřeva `SM_RuinTimber/Plank/Post_*` (praskliny, ohlazené hrany, prohyb; vlákna dělá normálová mapa materiálu, asi 2–3 tisíce trojúhelníků na kus). Generuje je `gen_stones.py`, importují se automaticky a vypínají se přes `WOOD_MESHES = False` v `build_ruin_blocks.py`. Úpravy dřeva (materiály vytvoří skript 03):

| Úprava | Materiál | Vzhled | Kde |
|---|---|---|---|
| dehet (`tar`) | `MI_RuinWood_Tar` | skoro hnědočerné, matné (staré zvětralé dehtování), vršky jen lehce vybledlé | masivní dřevo: trámy, průvlak, sloupy |
| krev (`blood`) | `MI_RuinWood_Blood` | starý nátěr volskou krví: tmavě červenohnědé, matné | venkovní ochoz u původního vstupu (trámy, vzpěry, prkna) |
| staré (`old`) | `MI_RuinWood_Old` | staré neošetřené: zašedlé až stříbřité, odbarvené, úplně matné, zaprášené a ochozené | prkna ve 2. patře (víc slunce a počasí) |
| bez úpravy (`raw`) | `MI_RuinWood` | šedohnědé, matné | vnitřní velké plochy: prkna v 1. patře a schody (ladí s podlahou) |
| olej (`oil`) | `MI_RuinWood_Oil` | teplá tmavší hnědá, polomatné | jemná práce a vnitřní stavební dřevo (zatím nepoužito) |

Master `M_RuinStone` má kvůli tomu parametry `Desaturate` (odbarvení textury, 0–1) a `DustAmount` / `DustTint` (zaprášení). U ostatních materiálů jsou na 0, takže se nic nemění. Rozdělení se mění v `constructions.json` → `finish` (výchozí hodnoty jsou v `WOOD_FINISH_DEFAULT` ve skriptu 03). Neošetřené dřevo je `MI_RuinWood`, který vytvoří skript 03. Je to zašlé nelakované dřevo, šedohnědé a matné. Každý trám a prkno má trochu jiný odstín a vršky jsou vybledlé od slunce. Ladí se v `MI_RuinWood` (`TintA`/`TintB`, `Roughness`) nebo v `MAT_LOOK["wood"]` ve skriptu 03. Vlastní materiál nastavíš v `MAT_WOOD_MI`.

---

## 5. Do budoucna

Sem patří další dostavby druhého zabydlení: střecha na krovu u ostrohu (latě, krytina), hlídková konstrukce na `Brana_S`, žebříky, lávky, dřevěné přístřešky, ohrady, provizorní střechy, zábrany v průlomech. Každá nová stavba je další položka v `constructions.json` a případně nový typ v `build_constructions.py`.
