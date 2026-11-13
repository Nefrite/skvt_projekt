# 05 Constructions – dodatečné stavby a suť („druhé zabydlení“) – návod pro UE 5.8

Do této složky patří všechno, co do zříceniny později přistavěli její obyvatelé, a volná suť na zemi. Staví se **zvlášť od zříceniny**: když ladíš schody, trámy nebo podestu, nemusíš přegenerovat celý hrad.

| Kde | Co |
|---|---|
| **03_ruin** (`03_ruin\blocks\build_ruin_blocks.py`) | zřícenina jako taková: zdi, otvory, ostění, kapsy pro trámy, kamenná dlažba přízemí věže |
| **05_constructions** (`build_constructions.py`) | dřevěné vestavby: trámy, prkna, průvlak se sloupy, provizorní schody, ochoz, krov u ostrohu. Kamenné dostavby z kamene rozvalin (stojí na zřícenině, ale nemění ji). Volná suť u zdí. |

Kapsy ve zdech patří ke zřícenině. Dřevo, které v nich leží, patří sem.

---

## 1. Soubory

| Soubor | Obsah |
|---|---|
| `stavby\<Stavba>.py` | **spuštění jedné stavby**: `Vez_Patra.py` (dřevo ve věži), `Ostroh_Krov.py` (krov u ostrohu), `Ostroh_Dostavba.py` (kamenná dostavba u ostrohu), `Ostroh_Podlaha.py` (prkenná podlaha u ostrohu), `Sut.py` (suť). Nahoře `MODE` (`build` / `capture`, u suti i `freeze`). |
| `build_constructions.py` | nastavení, registr typů staveb (`TYPES`, povinné klíče `REQUIRED`), build / capture / freeze v UE. Spuštěný přímo postaví všechny stavby najednou. Mimo UE vypíše počty kusů. |
| `zr_stavby\*.py` | typy staveb: `vez.py` (dřevo ve věži, `tower_floor`), `krov.py` (krov u ostrohu `fan_roof` + společná geometrie), `dostavba.py` (`stone_addon`), `podlaha.py` (`plank_floor`) |
| `..\zrlib\*.py` | sdílená knihovna s 03 (`config.py` = materiály, dřevo, fyzika; geometrie, Unreal) |
| `constructions.json` | data staveb (`floors` → `Vez_Patra`, `frames` → `Ostroh_Krov`, `addons` → `Ostroh_Dostavba`, `Ostroh_Podlaha`) a nastavení suti (`rubble`) |
| `Stavby_ostroh_dostavba_nahled.png` | náhled uzavřené obytné části u ostrohu zvenku a zevnitř |
| `Stavby_ostroh_podlaha_nahled.png` | náhled podlahy u ostrohu |
| `constructions_edits.json` | ručně smazané (`removed`) a posunuté (`moved`) kusy. Vzniká přes capture, nepřepisovat. |
| `Stavby_vez_nahled.png` | řez věží: patra, schody, ochoz |
| `..\tools\constructions\gen_constructions.py` | vytvoří `constructions.json` z `ruin_layout_draft.json` |
| `..\tools\constructions\check_tower.py` | náhled řezu věží bez Unrealu (zřícenina + stavby) |
| `..\tools\ruin\tower_spec.py` | **společné rozměry věže** pro 03 i 05 (podlaha, výška patra, polohy trámů, průvlaku, otvorů, dveří) |

Skript používá generátor zříceniny jako knihovnu. Složka `03_ruin\blocks` proto musí ležet vedle `05_constructions` (jinak v `build_constructions.py` nastav `RUIN_DIR`) a v kořeni musí být `zrlib`.

---

## 2. Postup v UE

1. **Nejdřív zřícenina:** `03_ruin\blocks\build_ruin_blocks.py`. Ta změří terén (`terrain_from_level.json`) a postaví zdi a kapsy.
2. **Pak stavby:** **Tools → Execute Python Script →**
   - **jedna stavba:** `05_constructions\stavby\Ostroh_Krov.py` (nebo `Ostroh_Dostavba.py`, `Ostroh_Podlaha.py`, `Vez_Patra.py`, `Sut.py`). Smaže a postaví jen tuto stavbu, ostatní zůstanou, jak jsou.
   - **všechno:** `05_constructions\build_constructions.py`.
   - Každý actor má tag `Zricenina_Stavby` a `stavba:<jméno>`. Zříceniny se build staveb nedotkne a build zříceniny nesmaže stavby.
3. V Outlineru přibude:
   - `Stavby/Vez/Vez_Patra_Drevo`: trámy, prkna, průvlak, sloupy, schody a ochoz (Instanced Static Mesh),
   - `Stavby/Ostroh/Ostroh_Krov_Drevo_Dehet`: krov a krytina u ostrohu,
   - `Stavby/Ostroh/Ostroh_Dostavba_Kamen` a `..._Drevo_Stare`: kamenná dostavba a dřevěná nadpraží,
   - `Stavby/Ostroh/Ostroh_Podlaha_Drevo` a `..._Drevo_Dehet`: prkna a podvaly podlahy,
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

Usazené kameny ve hře spí, dokud do nich někdo nestrčí. Staticky bez fyziky: `MODE = "freeze"` (do dalšího buildu) nebo `RUBBLE_PHYSICS = False`. Jak silně hráč tlačí, se nastavuje v Character Movement postavy (viz `README_bloky.md`, kap. 5.3).

---

## 3. Kdy co přegenerovat

| Změna | Co spustit |
|---|---|
| schody, prkna, ochoz, sloupy, suť (v `constructions.json` nebo `gen_constructions.py`) | jen `build_constructions.py` |
| podlaha u ostrohu (`gen_constructions.py` → `floor`) | `gen_constructions.py`, pak `Ostroh_Podlaha.py` a `Sut.py` |
| dostavba u ostrohu (okno, dveře, tloušťka, kámen, boční trámy v `gen_constructions.py`) | `gen_constructions.py`, pak `Ostroh_Krov.py` **i** `Ostroh_Dostavba.py` (dostavba sahá pod střechu, výšky bere z krovu) a `Sut.py` (úklid uvnitř) |
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

- **Boční trámy** (`sides`, 5 na jihu `BJ*`, 3 na severu `BS*`): střecha je prodloužená i nad klíny mezi krajními trámy vějíře a zdí `ZBudova_V`. Boční trámy jsou rovnoběžné s krajním trámem (B0 / B6), po 1,3 m, a vedou z dostavby `ZBudova_V` (spodek ve výšce příčky) na hradbu (jih) a na `ZBudova_S` (sever). Zřícenina se pro ně nesnižuje: trám leží na nejvyšším kameni koruny pod sebou, sklon se mu podle toho zmírní (nejméně 6 %). Kdyby musel být vodorovný, skončí před tím kamenem (na severu před hradbou těsně za `ZBudova_S`).
- **Horní okraj krytiny** (`top_line`) vede rovnoběžně se `ZBudova_V` nad dostavbou, 12 cm přes její vnější líc. Všechny trámy sahají až k němu.

Žlab, okapnice a sud přijdou později.

**`addons` → `Ostroh_Dostavba`** (typ `stone_addon`): uzavření obytné části u ostrohu. Provizorní dostavba z kamene rozvalin, jedna řada kamenů přes celou tloušťku (líc z obou stran). Zřícenina se nemění, dostavba jen stojí na koruně zdí.

| Zeď | Kde |
|---|---|
| `V` | na vnitřní polovině `ZBudova_V` (vnitřní líc v rovině líce zdi), po celé délce a přes mezeru u jižního konce až k hradbě. **Dveře** v průchodu (1,6 m, vrch 2,7 m nad terénem, nadpraží ve stejné výšce jako nadpraží okna, `align`), **okno** 3,4 m severně od dveří (k `ZBudova_S`), 1,4 × 0,9 m, parapet 1,8 m. Šířka okna je jako výklenek střílen hradby v této části, takže nadpraží je stejně dlouhé jako vnitřní překlad střílny (1,9 m) |
| `S` | na jižní (vnitřní) polovině `ZBudova_S`, od rohu se `ZBudova_V` k hradbě |
| `H` | na vnitřní polovině hradby mezi rohy (vyrovnání koruny pod okapem mezi trámy) |

- **Kámen** (`stone`): použitý kámen z hradu, stejně velký jako ve zdech (délka a výška řad z `STONE_MIN/MAX` a `COURSE_MIN/MAX` v `ruin_layout.json`: 35–90 cm, řady 25–40 cm), tloušťka 0,45 m, spáry 1,5 cm. U koruny a u trámů jsou kusy kratší, aby dosáhly pod střechu.
- **Spodek** kopíruje korunu zříceniny pod sebou (nejvyšší kámen v místě kusu), kde zeď chybí, stojí dostavba na terénu.
- **Vrch** dosahuje pod vrch trámů (latě a prkna leží na trámech) a v místě trámu pod jeho spodek, trámy procházejí zdivem. Pod šikmým trámem se kámen koruny rozdělí přes tloušťku na tři, aby každý kus dosáhl co nejvýš (mezera pod střechou je většinou do 5 cm; poslední řada se dorovná až pod střechu, když by nad ní zbylo méně než 12 cm).
- **Malta** (`mortar`): uprostřed tloušťky zdi je 10 cm silné jádro (kostky s materiálem jádra zříceniny `MI_RuinCore`) přes všechny spáry, takže zdí neprosvítá. Ve spárách vypadá jako malta. V Outlineru `Ostroh_Dostavba_Malta`.
- **Otvory:** vrch dveří a okna i parapet jsou zarovnané na řady kamene. Kámen pod oknem tenčí než 15 cm se nepostaví, okno pak sahá až na korunu zříceniny. Nad otvorem leží dřevěné nadpraží přes jednu řadu, 25 cm na každé straně uložené ve zdi (`lintel`), staré neošetřené dřevo (`finish` → `lintels`).
- **Suť** uvnitř obytné části je uklizená (`clear_rubble`): `Sut.py` ji tam nepostaví.
- Polohy (osy dostaveb, boční trámy, otvory) počítá `gen_constructions.py` ze zdí v `ruin_layout.json` a z `ostroh_spec.py`. Výšky (koruna, střecha) se počítají až při buildu z postavené zříceniny a krovu.

**`addons` → `Ostroh_Podlaha`** (typ `plank_floor`): prkenná podlaha v obytné části u ostrohu.

- **Obrys** (`outline`): vnitřní líce zdí zříceniny (`ZBudova_V`, `ZBudova_S`, hradba), 2 cm od nich (`inset`). Počítá ho `gen_constructions.py`.
- **Podvaly** (`sleepers`): 14 × 10 cm, napříč prkny po 0,8 m, v kusech po 1,2 m. Leží na zemi (zapuštěné 3 cm) a kopírují terén, dehtované.
- **Prkna** (`planks`): 4,5 cm silná, 22–32 cm široká, 2,4–4,5 m dlouhá, podél `ZBudova_V`, spáry 6 mm. Spoje jsou přesazené a leží vždy na podvalu. Bez úpravy, jako ve věži.
- **Výška:** spodek prken je 10 cm nad nejvyšším terénem v obrysu. V nižších místech jsou podvaly vyšší.
- Prkna i podvaly se vyříznou kolem sloupů krovu (`avoid`) a kolem kamenů zříceniny, které u paty zdí zasahují do podlahy. U oblouku hradby proto okraj podlahy nesleduje líc přesně (zuby po šířce prkna).
- **Suť:** na podlaze se nepostaví (`Sut.py`).



Souřadnice jsou v rámu věže: **u** vede od jihozápadního rohu podél jižní zdi (`Vez_J`), **v** od jihozápadního rohu k severu. Obojí v metrech, osy zdí jsou na 0 a 11 m.

**Dřevo:** tvary jsou meshe zašlého dřeva `SM_RuinTimber/Plank/Post_*` (praskliny, ohlazené hrany, prohyb; vlákna dělá normálová mapa materiálu, asi 2–3 tisíce trojúhelníků na kus). Generuje je `gen_stones.py`, importují se automaticky a vypínají se přes `WOOD_MESHES = False` v `zrlib\config.py`. Úpravy dřeva (materiály vytvoří skript 03):

| Úprava | Materiál | Vzhled | Kde |
|---|---|---|---|
| dehet (`tar`) | `MI_RuinWood_Tar` | skoro hnědočerné, matné (staré zvětralé dehtování), vršky jen lehce vybledlé | masivní dřevo: trámy, průvlak, sloupy |
| krev (`blood`) | `MI_RuinWood_Blood` | starý nátěr volskou krví: tmavě červenohnědé, matné | venkovní ochoz u původního vstupu (trámy, vzpěry, prkna) |
| staré (`old`) | `MI_RuinWood_Old` | staré neošetřené: zašedlé až stříbřité, odbarvené, úplně matné, zaprášené a ochozené | prkna ve 2. patře (víc slunce a počasí) |
| bez úpravy (`raw`) | `MI_RuinWood` | šedohnědé, matné | vnitřní velké plochy: prkna v 1. patře a schody (ladí s podlahou) |
| olej (`oil`) | `MI_RuinWood_Oil` | teplá tmavší hnědá, polomatné | jemná práce a vnitřní stavební dřevo (zatím nepoužito) |

Master `M_RuinStone` má kvůli tomu parametry `Desaturate` (odbarvení textury, 0–1) a `DustAmount` / `DustTint` (zaprášení). U ostatních materiálů jsou na 0, takže se nic nemění. Rozdělení se mění v `constructions.json` → `finish` (výchozí hodnoty jsou v `WOOD_FINISH_DEFAULT` v `zrlib\config.py`). Neošetřené dřevo je `MI_RuinWood`, který vytvoří skript 03. Je to zašlé nelakované dřevo, šedohnědé a matné. Každý trám a prkno má trochu jiný odstín a vršky jsou vybledlé od slunce. Ladí se v `MI_RuinWood` (`TintA`/`TintB`, `Roughness`) nebo v `MAT_LOOK["wood"]` v `zrlib\config.py`. Vlastní materiál nastavíš v `MAT_WOOD_MI` (tamtéž).

---

## 5. Do budoucna

Sem patří další dostavby druhého zabydlení: žlab a okapnice u ostrohu, lemování horního okraje krytiny, hlídková konstrukce na `Brana_S`, žebříky, lávky, dřevěné přístřešky, ohrady, provizorní střechy, zábrany v průlomech. Každá nová stavba je další položka v `constructions.json` a případně nový typ v `build_constructions.py`.
