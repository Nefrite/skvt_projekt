# 03 Ruin – zřícenina z kamenných bloků (stav ~1650) – návod pro UE 5.8

Nová metoda generování: zřícenina se skládá **z jednotlivých kamenných bloků** (~18 500 kusů) místo svislých sloupců.

- Okna, průchody a výšky zdí upravíš **bouracími objemy přímo v levelu** (Trigger Box s tagem, kap. 5) nebo v datech (kap. 4) a přegeneruješ.
- Jednotlivé kameny můžeš rozložit na samostatné actory, ručně posunout a smazat. Změny se pamatují i po přegenerování.

![Náhled (spočítáno mimo UE)](Zricenina_bloky_nahled.png)

Původní sloupcový generátor (`03_ruin\build`) zůstává beze změny. Obě metody používají tag `Zricenina_Ruin`, takže generují do stejných složek a navzájem se přepisují.

---

## Jak je zeď složená

| Vrstva | Co to je | Materiál (výchozí) |
|---|---|---|
| **Líc** (obě strany zdi) | lomové kameny v řádcích 25–40 cm, délky 35–90 cm, převazba (spáry se střídají). **Zaoblené, lehce zvětralé meshe** `SM_RuinStone_*` | `MI_RuinFace` (Slate, náhodný odstín na kámen) |
| **Jádro** (mezi líci) | delší bloky z lomu a malty 1,0–1,8 m (kostky, většinou skryté) | `MI_RuinCore` (šedý kámen s maltou) |
| **Ostění a oblouky** | opracované kvádry kolem intaktních otvorů po řádcích zdi, nadpraží, parapet, klínové kameny oblouků. Meshe `SM_RuinDressed_*` (opracovaný kámen, zaoblené a lehce otlučené hrany, 4 poměry × 2 varianty; `DRESSED_FRAMES = False` = kvádr `SM_RuinAshlar`) | `MI_RuinFrame` (stejný kámen jako líc, o kousek světlejší) |
| **Nárožní kvádry** | zakrývají průřez zdi v rozích. U vnějšího rohu se střídá dlouhý a krátký kvádr, zbytek tloušťky tvoří lomové kameny | jako líc |
| **Zlomy lomené zdi** | kámen přes zlom se rozdělí na dva. Na vnější (vypouklé) straně se líc prodlouží do společné hrany, na vnitřní se zkrátí, takže zvenku nevznikají klínové díry. Jádro se prodlouží | – |
| **Podpora líce** | lícový kámen musí ležet na lícovém kameni (ne jen na jádru). Nad vybraným lícem tak nevisí žádné kameny a díra se nahoru stupňovitě uzavírá. **Klenutí:** kámen nad mezerou do 0,6 m (`BRIDGE`) zůstane, když leží oběma konci (levý konec může držet i soused v řadě, malta) | – |
| **Odkryté jádro** | kde chybí líc, jádro se rozpadne na lomové kameny 0,35–0,7 m (mesh `SM_RuinStone_*`), každý jinak zapuštěný o 5–20 cm (`CORE_RECESS`). U okraje díry méně, občas vystupuje zbytek líce, takže hrana není ostrá. Kus, který by visel, odpadne. Vypíná se `CORE_ROUGH: false` | `MI_RuinCore` (šedý kámen s maltou) |
| **Koruna** | odkryté horní kameny, na kterých už nic neleží (i na dně děr po vybraném líci), jsou zvětralé **hlavně shora** (počasí): tvary `SM_RuinStone_W_*` mají horní hrany obroušené do velkého zaoblení, nerovný vrch s důlky, spodek (leží na kameni pod sebou) zůstává ostrý. Materiál `MI_RuinCrown` zesvětlí a zazelená (lišejník, prach) jen plochy mířící nahoru. Vypíná se `CROWN_WEATHER = False` | `MI_RuinCrown` |

**Rozpad** jde v tomto pořadí:

1. **Výška zdi:** model rozpadu z `README_ruin.md` kap. 4 (čas, rozebírání podle dostupnosti a výšky, otvory) určí, jak vysoko zeď v daném místě sahá.
2. **Bloky nad touto výškou zmizí.** Na koruně zůstanou jednotlivé uvolněné a pootočené kameny.
3. **Podpora:** blok bez opory pod sebou nezůstane (výjimka: je nad intaktním nadpražím nebo obloukem).
4. **Rozebraný líc:** kameny se berou hlavně **shora**, v pásu pod korunou (`TOP_ROB`, `TOP_ROB_D`). Líc pod korunou ustupuje stupňovitě. U paty jen menší hloučky 2–4 kamenů, kam se dosáhne (`FACE_ROB_BASE`, víc u `access_points`). Ve věži se výška u paty měří zevnitř od podlahy. Kameny se vybírají v hloučcích (plynulý šum), ne po jednom. Vnější líc nad útesem zůstává.
5. **Otvory:** parapet a nadpraží se zarovnají na spáry řádků. Bloky, které do otvoru nebo ostění zasahují, se **rozdělí** (nevynechávají se celé), takže každý otvor je opravdu průhledný a kolem ostění nevznikají díry. Intaktní ostění (po řádcích), nadpraží, parapet a oblouky se postaví z opracovaných kvádrů. Když lidé vylámali opracované kameny ostění, ale oblouk nebo nadpraží stojí, zůstane za nimi zapuštěné jádro zdi a nese je, takže nic nevisí ve vzduchu. Kontrola mimo UE: `python test_openings.py` → `kolize: 0`.
6. **Suť:** jen málo bloků u paty, protože většinu kamene lidé odvezli.

---

## 1. Příprava (jednorázově)

1. Zkopíruj obsah složky `03_ruin\blocks` kamkoli. Soubory `build_ruin_blocks.py`, `ruin_layout.json` a `manual_edits.json` musí zůstat **vedle sebe**.
2. **Záložní Blueprint (doporučeno vytvořit hned).** Skript se nejdřív pokusí přidat komponentu Instanced Static Mesh sám. Kdyby to v UE 5.8 nešlo, použije tento Blueprint:
   1. Content Browser → `Skvt/Lapikus/Ruin` → pravé tlačítko → **Blueprint Class → Actor** → `BP_RuinBlocks`.
   2. Otevři ho a v panelu Components dej **Add → Instanced Static Mesh**. Komponentu nech, jak je, nic nenastavuj.
   3. **Compile** a **Save**.
3. **Zaoblené kameny:** složka `stones` (13 souborů `.obj`) musí ležet vedle skriptu. Při prvním spuštění je skript sám naimportuje do `/Game/Skvt/Lapikus/Ruin/Stones` (zapne Nanite a přidá krabicovou kolizi). Podrobnosti a ruční import v kap. 1.1.
4. **Materiály:** skript při prvním spuštění vytvoří `M_RuinStone` a instance `MI_RuinFace`, `MI_RuinCore`, `MI_RuinFrame` v `/Game/Skvt/Lapikus/Ruin/Materials` (textury ze StarterContent). Další spuštění je už nepřepisují (kromě přechodu na novou `MAT_VERSION`, viz kap. 1.2), takže je můžeš ladit v editoru.
5. **Ulož mapu a commitni.** Před generováním smaž sloupcovou zříceninu, pokud v mapě je. Nová ji sice smaže sama, ale sloučené meshe smazat musíš ručně.

### 1.1 Zaoblené kameny líce (`stones/*.obj`)

- `SM_RuinStone_R12/R18/R26/R34_A/B/C`: 4 poměry délka/výška (1,2 / 1,8 / 2,6 / 3,4) × 3 varianty tvaru. Zaoblené hrany (3,5–4,7 cm), mírně vypouklé plochy, nerovnosti a otlučené hrany. Každý má 1 000–2 300 trojúhelníků.
- `SM_RuinStone_W_R12…R34_A/B/C`: zvětralé kameny koruny. Nahoře zaoblení 8,5–10,5 cm, otlučení a důlky, do stran 4,5–5,5 cm, dole jen 3 cm. Verze meshe je v metadatech (`RuinStoneVersion`, `STONE_MESH_VERSION` ve skriptu). Když jsou v projektu starší, skript je sám naimportuje znovu.
- `SM_RuinDressed_R12…R34_A/B`: opracované kameny ostění, nadpraží, parapetů a výklenků střílen. Rovné plochy, zaoblení 2,4–3,7 cm, nahoře o něco víc.
- `SM_RuinAshlar`: kvádr s lehce sraženými hranami, jen dlažba.
- **Dřevo** (`WOOD_MESHES = True`): `SM_RuinTimber_A/B/C` (trám, průvlak, schodnice, vzpěry), `SM_RuinPlank_A/B/C` (prkna, fošny schodů), `SM_RuinPost_A/B/C` (sloupy). Dřevo je vysušené od slunce: podélné praskliny (i až do čela), ohlazené a otlučené hrany, měkká promáčknutí, lehký prohyb a zkrut. Prkna jsou mírně prohnutá do misky. Vlákna a letokruhy dělá normálová mapa materiálu, ne geometrie. Síť je hrubá, asi 2–3 tisíce trojúhelníků na kus. Skript kus vybere podle tvaru a naskaluje na přesný rozměr.
- Skript vybere ke každému bloku variantu podle poměru délka/výška a naškáluje ji **přesně na rozměr bloku** (`STONE_OVERSIZE = 1.04` = o 4 % větší, aby spáry nebyly moc hluboké). Polovina kamenů je otočená o 180°, takže se tvary méně opakují. Varianta je vázaná na ID bloku a po přegenerování se nemění.
- Osy po importu kontroluje skript sám podle bounding boxu, takže nezáleží na tom, jak je importér otočí.
- **Ruční import** (když automatický selže, v Output Logu je `Ruin: chybi … kamenu`):
  1. Přetáhni všechny `.obj` ze složky `stones` do Content Browseru, do `Skvt/Lapikus/Ruin/Stones`.
  2. V importu zapni **Nanite**. Materiál neřeš.
  3. Každý mesh otevři a dej **Collision → Add Box Simplified Collision** → Save. Bez toho postava projde zdí.
  4. Názvy assetů musí zůstat `SM_RuinStone_R12_A` atd.
- **Vlastní tvary:** `python gen_stones.py stones` (potřebuje numpy) přegeneruje OBJ. Tvar se ladí parametry `make_stone` (`radius`, `amp`, `edge`, `bulge`). Pak smaž staré meshe v `Ruin/Stones` a spusť build znovu.
- `USE_STONE_MESHES = False` vrátí všude kostky.

### 1.2 Materiály

- `M_RuinStone` je master materiál s parametry `BaseColor`, `Normal`, `TintA`, `TintB`, `Tiling` a `Roughness`. Každý kámen dostane náhodný odstín mezi TintA a TintB a náhodný posun textury (Per Instance Random), takže dva sousední kameny nikdy nevypadají stejně. Žádné „cihly v cihle“ jako u `M_Brick_Hewn_Stone`.
- **Zvětrání shora (všechny kameny):** podle normaly plochy (`VertexNormalWS.z`). Co míří nahoru, je světlejší, nazelenalé a drsnější. Skvrny rozbíjí textura. Parametry: `TopTint` (barva), `TopStart` (od jakého sklonu, 0 = svislá stěna, 1 = vodorovný vrch), `TopSharp` (ostrost přechodu), `TopAmount` (síla: líc 0,55, jádro 0,45, ostění 0,35, koruna 1,0). Výchozí hodnoty jsou v `MAT_TOP` ve skriptu.
- **Verze materiálu:** `MAT_VERSION` ve skriptu. Když je `M_RuinStone` v projektu starší, skript jeho graf přestaví na místě a do `MI_Ruin*` jen doplní nové parametry `Top*`. Tvoje tinty a textury v `MI_RuinFace/Core/Frame` zůstanou, `MI_RuinCrown` dostane nový tint z `MAT_LOOK`.
- Vzhled ladíš v `MI_RuinFace`, `MI_RuinCore` a `MI_RuinFrame` (dvojklik → Details). Hodí se tam i textura z Fabu (Megascans, např. „Rock“ nebo „Stone Wall“ surface): stačí přepsat `BaseColor` a `Normal`.
- Úplně vlastní materiál nastavíš nahoře ve skriptu: `MAT_FACE = "/Game/…/MI_X.MI_X"` (stejně `MAT_CORE`, `MAT_FRAME`). `None` znamená automatický materiál.
- Když chceš materiál vytvořit znovu od nuly, smaž `M_RuinStone` a `MI_Ruin*` a spusť build.
- **Chybí textury StarterContent:** Output Log hlásí `nenalezeny textury`. Přidej Starter Content (Content Browser → **Add → Add Feature or Content Pack → Starter Content**), nebo v `TEXTURES` nahoře ve skriptu nastav vlastní cesty.

---

## 2. Vygenerování

1. Otevři `LapikusPrototypeMap` a otevři **Output Log**.
2. Dej **Tools → Execute Python Script…** a vyber `build_ruin_blocks.py`.
3. Průběh je vidět v okně „Stavím zříceninu z bloků…“, po jednotlivých zdech.
4. Output Log pak vypíše:
   ```
   Zricenina z bloku (1650): 18... bloku ve 17 zdech, objemu 0, samostatnych kamenu 0, rucne smazanych 0, posunutych 0, zaoblenych meshu 13.
   ```
5. V Outlineru se objeví složky `Ruin/Hradba`, `Ruin/Palac`, `Ruin/Vez`, `Ruin/Brana` a `Ruin/ZapadniBudova`:
   - **Každý rovný úsek zdi (od zlomu ke zlomu) je samostatný actor.** Úseky se dělí dál na `…_Lic`, `…_Jadro` a `…_Osteni` (Instanced Static Mesh). Zdi s více zlomy (hradba) mají vlastní podsložku a úseky číslované, např. `Ruin/Hradba/Hradba_Z_S/Hradba_Z_S_03_Lic`.
   - Rozpad je přitom spočítaný **přes celou zeď najednou**, takže na zlomech nevznikají skoky ve výšce.
   - **Kameny na zemi (suť)** jsou vždy **samostatné actory** ve složce `…/Sut`. Můžeš je rovnou posouvat a mazat a uložit přes capture (kap. 5.2), bez boxu `Ruin_Explode`.

### 2.1 Stavění po částech (`casti\<Cast>.py`)

Hrad je rozdělený na tři části, které se dají stavět zvlášť. Při ladění vnitřních zdí se tak nepřestavuje celý hrad.

| Skript | Část | Zdi |
|---|---|---|
| `casti\Obvod.py` | věž a obvod | `Vez_*`, `Hradba_Z_S`, `Hradba_V`, brány `Brana_*`, dlažba věže `Vez_Dlazba` |
| `casti\Palac.py` | palác (vnitřní) | `Palac_J`, `Palac_S`, `Palac_Z`, `Palac_pricka_1`, `Palac_pricka_2` |
| `casti\Ostroh.py` | západní budova u ostrohu (vnitřní) | `ZBudova_V`, `ZBudova_S` |

- **Tools → Execute Python Script → `03_ruin\blocks\casti\Palac.py`** (nebo `Ostroh.py`, `Obvod.py`). Smaže a postaví jen actory této části, ostatní zůstanou, jak jsou.
- `build_ruin_blocks.py` spuštěný přímo dál staví **celý hrad**.
- Každý actor zříceniny má tag `cast:<Část>` a `zed:<jméno zdi>`, podle nich build části maže jen svoje actory. Actor zříceniny bez těchto tagů smaže jen build celého hradu.
- Počítá se vždy celý hrad (návaznosti mezi zdmi, např. výška `Brana_S` podle oblouku brány, terén z levelu). Staví se jen vybraná část, takže je to výrazně rychlejší.
- **Nová zeď:** do části se zařadí podle jména (`CASTI` nahoře v `build_ruin_blocks.py`, platí první shoda). Co nespadá pod `Palac_*` ani `ZBudova_*`, patří do `Obvod`.
- **Pozor:** úsek hradby u ostrohu (snížení a žlábky pro trámy krovu) je součástí `Hradba_Z_S`, tedy části **Obvod**. Když se změní krov (`ostroh_spec.py`), spusť `Obvod.py`. Po přestavbě části `Ostroh` postav znovu i dostavbu a podlahu v 05 (`Ostroh_Dostavba.py`, `Ostroh_Podlaha.py`), protože stojí na koruně `ZBudova_V` a `ZBudova_S`.
- `MODE = "capture"` ve skriptu části ukládá ruční úpravy (smazané, posunuté kameny) vždy za celý hrad.

**Rychlé ladění jedné zdi:** nahoře ve skriptu nastav `ONLY_WALLS = ["Brana_V", "Brana_J"]`. Přegeneruje se jen tato zeď, ostatní zůstanou.

**Když to selže:**

- **`Ruin: chybi … kamenu … pouziji se kostky`:** složka `stones` neleží vedle skriptu, nebo import selhal. Řeš podle kap. 1.1 (ruční import).
- **Postava prochází zdí:** meshe nemají kolizi. Postup v kap. 1.1, krok 3.

- **„Nejde pridat InstancedStaticMeshComponent… chybi Blueprint“:** vytvoř `BP_RuinBlocks` (krok 1.2).
- **Chybí soubor:** v `build_ruin_blocks.py` nastav `LAYOUT_PATH = r"…\ruin_layout.json"`.
- **Jiná chyba:** pošli text z Output Logu.

---

## 3. Stáří zříceniny

V `ruin_layout.json` je `"age": "1650"` a sekce `presets`. Přepnout jde i nahoře ve skriptu: `AGE = "1540"`.

| Stáří | Věž | Palác nad útesem | Hradba | Vnitřek (palác do nádvoří, příčky, západní budova) | Suť |
|---|---|---|---|---|---|
| `1540` (60–80 let po opuštění) | 17–21 m | 8–11 m | 5–7 m | 2–8 m | střední |
| **`1650`** (~170 let, výchozí) | **12–14 m** | **5–7 m** | **3–5 m** | **1–2 m**, portál a oblouk brány stojí | **malá**, odvezená |

Preset `1650` mění parametry takto:

| Parametr | 1650 | Význam |
|---|---|---|
| `WEATHER` | 0.6 | víc přirozeného rozpadu |
| `ROBBING` | 7 | víc rozebíráno |
| `REMAIN` | 1,2 m | spodní řady zasypané zeminou zůstávají |
| `JAG` | 1.8 | zubatější koruna |
| `FRAME_ROB` | 1.4 | víc vylámaných ostění |
| `FACE_ROB` | 1.4 | víc odkrytého jádra |
| `RUBBLE_*` | malé | suť většinou odvezená |

Vlastní stáří přidáš novým presetem v `presets` (např. `"1800": {...}`) a nastavíš `"age": "1800"`.

---

## 4. Úpravy v datech (nedestruktivní)

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
- **Typy otvorů a celé zdi** (výška `H0`, dostupnost `access`, otvory `openings`) se mění v `walls` (viz `03_ruin\build\README_build_ruin.md` kap. 3).
- **Zvýšení úseku (`raise` u zdi):** `{"s0": 15.85, "s1": 26.75, "dh": 0.5}` zvedne zeď nad výsledek rozpadu o `dh` m, na krajích plynule. `ZBudova_V` má +0,7 m (2 řady), `Hradba_Z_S` úseky 03–04 +0,5 m.
- **Zaoblené zlomy (`fillet` v `gen_layout.py`):** zlomy `Hradba_Z_S` mezi úseky 02–06 jsou oblouky. Výšky a otvory se zadávají podle původní nezaoblené čáry a `remap_wall` je převede. `seg_group` drží číslování actorů podle původních úseků (oblouk patří k sousedním úsekům).
- **Sesuv (`breaches` u zdi):** `{"s0": 0.6, "s1": 2.6, "floor": 0.5, "slope_l": 2.0, "slope_r": 6.0}` sníží zeď mezi `s0` a `s1` na `floor` m. Boky stoupají se strmostí `slope_l`/`slope_r` (1 = 45°, 6 = skoro svisle, výchozí 1). `power_l`/`power_r` > 1 bok zakřiví: dole pozvolna, ke koruně strměji (výchozí 1 = rovná linie). Ostrým bokem se sesuv udrží v jednom úseku a sousední úsek zůstane vysoký. Příklad: `Hradba_Z_S`, úsek 01 (stezka k vodě): `{"s0": -1.0, "s1": 1.3, "floor": 0.5, "slope_r": 2.4, "power_r": 1.5}` = šikmý sesuv, nízko u paláce.
- Datové úpravy **neposouvají ostatní bloky**. Každý blok má vlastní náhodu podle svého ID, takže zbytek zříceniny zůstane stejný.

### Půdorys v3 a terén z levelu (11/2026)

- **Strážní věž se dvěma branami.** `Brana_V` je 1. brána z východu, `Brana_S` severní stěna, `Brana_J` 2. brána na západ do uličky podél věže a `Brana_Jih` nová jižní stěna. `Hradba_V` vede od jižní stěny strážní věže obloukem k JV rohu věže. `Hradba_Z_S` končí na SZ rohu strážní věže. Vstup do hlavní věže je průlom (`prulom`) ve `Vez_S`.
- **Ochrana do výšky jiného otvoru (`protect` s `to`):** `{"s0": -1, "s1": 8, "to": [{"wall": "Brana_V", "opening": 0, "dz": 0.1}, {"wall": "Brana_J", "opening": 0, "dz": 0.1}]}` drží zeď alespoň do výšky vrchu oblouku (otvor + ostění) jiné zdi. Výška je v absolutních souřadnicích, takže sedí i při jiném terénu, podstavbě nebo `z_offset`. Se dvěma cíli vede výška lineárně od `s0` k `s1`. Použito u `Brana_S` (do výšky oblouků obou bran, sem přijde hlídková konstrukce) a u přilehlých konců `Brana_V` a `Brana_J`.
- **Snížená a zarovnaná zeď (`cap`):** `{"s0": 12.4, "s1": 31.9, "z": 3459}` = mezi `s0` a `s1` zůstanou jen celé řady kamenů pod absolutní výškou `z` (cm). Koruna je rovná, jako by zeď někdo cíleně rozebral. Bez volných kamenů a bez rozebírání líce.
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
- **Dřevěné vestavby a suť jsou od 11/2026 v `05_constructions`.** Patří sem trámy, prkna, průvlak, schody, podesta a volná suť na zemi (`build_constructions.py`, návod `README_constructions.md`). Build zříceniny je nestaví ani nemaže. `compute_blocks(..., rubble=True)` sem suť vrátí postaru.
- **Přenos ručních posunů zdí do dat:** `tools\ruin\export_level_layout.py` zapíše posunuté actory a body `RuinPt_<Zed>_<NN>` do `layout_from_level.json`. Podle něj se upraví `gen_layout.py`.

---

## 5. Úpravy přímo v levelu: bourací objemy (doporučeno)

Každá zeď je v levelu jeden Instanced Static Mesh. Kliknutím proto vybereš celou zeď, ne jednotlivý blok. Na úpravy jsou určené **objemy**: do levelu vložíš **Trigger Box**, dáš mu tag a přegeneruješ. Skript si objemy při každém spuštění načte sám. Posunem nebo zvětšením boxu a novým spuštěním úpravu upravíš, smazáním boxu ji vrátíš.

### 5.1 Vložení objemu

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

### 5.2 Ruční posun a mazání jednotlivých kamenů

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

### 5.3 Oddělení části zdi bez přegenerování (`detach_stones.py`)

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

**Fyzika volných kamenů (`STONE_PHYSICS` v `build_ruin_blocks.py`, platí i pro suť ve 05):**
- **Hmotnost podle objemu kamene:** hustota 2600 kg/m³ × objem bloku × 0,85 (zaoblení). Kámen 30 × 40 × 60 cm váží asi 160 kg, suť většinou 20–280 kg. Hráč takový kámen posune jen málo.
- **Tlumení** (`lin_damp` 0,3, `ang_damp` 0,8): kámen se nekoulí donekonečna.
- **Fyzikální materiál `PM_RuinStone`**, který skript vytvoří ve složce materiálů: tření 0,9, odraz 0,05.
- Kameny jsou o 3 % menší než blok (`shrink`), aby je při startu nevystřelil překryv se sousedy.
- Jak silně hráč tlačí, se nastavuje u postavy v **Character Movement**: zapnutý `Enable Physics Interaction`, `Push Force Factor` asi 100 000–300 000 a vypnutý `Push Force Scaled To Mass`. Pak se těžký kámen pohne málo a lehký víc. Kameny můžeš i ručně posouvat nebo mazat a uložit přes capture.

**Vrácení do zdi:** box `Ruin_Detach` přes oddělené kameny a `MODE = "undo"`. Kameny se vrátí do zdi při dalším buildu.

Oddělit jde líc, koruna, jádro i ostění (`CATS`). Za odpadlým lícem je hned po oddělení hladké jádro (kostky). Při dalším buildu se tam jádro samo rozpadne na lomové kameny jako u ostatních odkrytých míst.

## 6. Dál: sloučení a vzhled

- Až bude rozpad hotový, můžeš každou část sloučit přes **Tools → Merge Actors** (Instanced Static Mesh je podporovaný) do jednoho meshe pro Modeling Mode. Po sloučení už ale nejde jednoduše přegenerovat, takže si nejdřív zálohuj JSON a `manual_edits.json`.
- Materiály a kameny: kap. 1.1 a 1.2.
- **Výkon:** ~19 000 instancí. Se zaoblenými kameny je to ~25 mil. trojúhelníků, proto **nech na meshích Nanite**: s ním je to nenáročné, bez něj by to bylo těžké. Když potřebuješ rychlý blockout, nastav `USE_STONE_MESHES = False`. Pro jemnější bloky (`STONE_MIN/MAX`, `COURSE_MIN/MAX` v `params`) počítej se 2–4× víc.
- **ID bloků u otvorů:** bloky rozdělené otvorem mají ID s příponou `.a`/`.b`. Ruční smazání bloku, který se nově rozdělil, je proto potřeba po této verzi zopakovat (týká se jen bloků těsně u otvorů).

---

## Parametry bloků (`ruin_layout.json` → `params`)

| Parametr | Výchozí | Význam |
|---|---|---|
| `COURSE_MIN` / `COURSE_MAX` | 0.25 / 0.40 m | výška řádků |
| `STONE_MIN` / `STONE_MAX` | 0.35 / 0.90 m | délka lícových kvádrů |
| `CORE_MIN` / `CORE_MAX` | 1.0 / 1.8 m | délka bloků jádra |
| `FACE_DEPTH` | 0.40 m | hloubka lícových kvádrů |
| `JOINT` | 0.015 m | spára mezi bloky |
| `FRAME_SPLIT` | 1.1 m | opracovaný kámen (ostění, oblouk, boky výklenku) delší, než je tato hodnota, se v hloubce zdi rozdělí na více kusů s posunutými spárami |
| `FACE_ROB` / `FACE_ROB_H` | 1.0 / 2.2 m | síla a výška rozebírání líce u paty (odkryté jádro) |
| `FACE_ROB_BASE` | 0.45 | podíl rozebírání u paty (násobí `FACE_ROB` × dostupnost) |
| `TOP_ROB` / `TOP_ROB_D` | 0.55 / 0.7 m | rozebírání líce shora: síla u koruny a jak rychle slábne směrem dolů |
| `BRIDGE` | 0.6 m | nejširší mezera, kterou kámen líce překlene |
| `CORE_ROUGH` / `CORE_RECESS` | true / [0.05, 0.2] m | odkryté jádro z lomových kamenů, rozsah zapuštění |
| `RUBBLE_BLOCKS` | 0.02 | podíl bloků jako suť u paty |
| `SEED` | 1 | jiná varianta celé zříceniny |

---

## Soubory

| Soubor | Obsah |
|---|---|
| `build_ruin_blocks.py` | generátor z bloků (čistý Python), `MODE = "build"` / `"capture"`; spuštěný přímo staví celý hrad; mimo UE vypíše počty bloků po částech |
| `casti\Obvod.py`, `casti\Palac.py`, `casti\Ostroh.py` | postaví jen jednu část hradu (kap. 2.1) |
| `ruin_layout.json` | zdi, otvory, presety stáří, `edits`, `edits_examples`, `volumes_examples`, výšková mřížka terénu |
| `manual_edits.json` | ručně smazané (`removed`), posunuté (`moved`) a oddělené (`detached`) kameny |
| `detach_stones.py` | oddělení části zdi v boxu `Ruin_Detach` bez přegenerování, fyzika pro pád (kap. 5.3) |
| `stones\*.obj` | zaoblené kameny líce a kvádr ostění (import automaticky) |
| `gen_stones.py` | generátor zaoblených kamenů (numpy) |
| `test_openings.py` | kontrola: žádný blok v otvoru (`kolize: 0`) |
| `Zricenina_kameny_detail.png` | detail zdi paláce se střílnou (zaoblené kameny, ostění) |
| `Zricenina_bloky_nahled.png` | náhled (věž z nádvoří, brána detail, celek, brána a věž, palác) |
| `..\..\tools\ruin\check_blocks.py` | vykreslí náhled bez Unrealu |
| `..\..\tools\ruin\gen_layout.py` | vytvoří `ruin_layout.json` z `ruin_layout_draft.json` a heightmapy |
