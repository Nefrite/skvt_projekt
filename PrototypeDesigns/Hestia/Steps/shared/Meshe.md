---
# orchestrace
type: step
validity: valid
aliases: []
step_kind: shared
updated: 2026-11-23
# hra
domains: [structures]
---
# Meshe kamenů a dřeva, materiály a knihovní meshe

<!-- Sdílená knihovna meshí; vzniklo tematickým rozdělením [[03_ruin]] a [[05_constructions]] 2026-11-23 (G14b). -->

## Co poskytuje
Knihovna procedurálních meshí pro zříceninu (03), stavby (05) a vybavení (06): kameny a dřevo (`tools\meshes\gen_meshes.py`, OBJ v `meshes\stone` a `meshes\wood`), kulatina, další knihovní meshe (`LIB_MESHES`, `ROUND_MESHES` v `zrlib\config.py`) a materiály. Props jsou v [[Meshe_props]]. Kapitoly 1.1 a 1.2 mají čísla z původního [[03_ruin]].

### 1.1 Meshe kamenů a dřeva (`meshes/<kategorie>/*.obj`)

- `SM_RuinStone_R12/R18/R26/R34_A/B/C`: 4 poměry délka/výška (1,2 / 1,8 / 2,6 / 3,4) × 3 varianty tvaru. Zaoblené hrany (3,5–4,7 cm), mírně vypouklé plochy, nerovnosti a otlučené hrany. Každý má 1 000–2 300 trojúhelníků.
- `SM_RuinStone_W_R12…R34_A/B/C`: zvětralé kameny koruny. Nahoře zaoblení 8,5–10,5 cm, otlučení a důlky, do stran 4,5–5,5 cm, dole jen 3 cm. Verze meshe je v metadatech (`RuinStoneVersion`, `STONE_MESH_VERSION` ve skriptu). Když jsou v projektu starší, skript je sám naimportuje znovu.
- `SM_RuinDressed_R12…R34_A/B`: opracované kameny ostění, nadpraží, parapetů a výklenků střílen. Rovné plochy, zaoblení 2,4–3,7 cm, nahoře o něco víc.
- `SM_RuinAshlar`: kvádr s lehce sraženými hranami, jen dlažba.
- **Dřevo** (`WOOD_MESHES = True`): `SM_RuinTimber_A/B/C` (trám, průvlak, schodnice, vzpěry), `SM_RuinPlank_A/B/C` (prkna, fošny schodů), `SM_RuinPost_A/B/C` (sloupy). Dřevo je vysušené od slunce: podélné praskliny (i až do čela), ohlazené a otlučené hrany, měkká promáčknutí, lehký prohyb a zkrut. Prkna jsou mírně prohnutá do misky. Vlákna a letokruhy dělá normálová mapa materiálu, ne geometrie. Síť je hrubá, asi 2–3 tisíce trojúhelníků na kus. Skript kus vybere podle tvaru a naskaluje na přesný rozměr.
- **Kulatina** (`tools/meshes/mesh_log.py`, také v `meshes/wood`, v UE `Ruin/Wood`): `SM_RuinLog`, `SM_RuinLogBark`, `SM_RuinPole`, `SM_RuinPoleBark`, `SM_RuinStake`, `SM_RuinStakeSmall`, `SM_RuinForkHead`, `SM_RuinGutter`, `SM_RuinGutterBark`. Má víc materiálových slotů (`Wood`, `EndGrain`, `Bark`), popis níž v *Dřevo, kulatina a další knihovní meshe*. Náhled: `05_constructions/Kulatina_meshe_nahled.png`.
- **Další knihovní meshe** (popis níž v *Dřevo, kulatina a další knihovní meshe*): pás kůry `SM_RuinBarkStrip` (`mesh_bark.py`, kategorie `wood`), proutí a mazanina `SM_RuinWattlePanel`, `SM_RuinSmokeHood`, `SM_RuinChimney` (`mesh_wattle.py`, `meshes/wattle`, v UE `Ruin/Wattle`), lano `SM_RuinRope`, ovázání `SM_RuinLashing` a ukázka plachty `SM_RuinCanvasSample` (`mesh_textile.py`, `meshes/textile`, v UE `Ruin/Textile`). Náhled: `05_constructions/Knihovna_meshe_nahled.png`. Props (kovárna, špalek, ponk, hranice, koš, žebřík): `mesh_props.py`, `meshes/props`, v UE `Ruin/Props`, náhled `05_constructions/Props_kovarna_nahled.png`.
- **Textury** (`tools/textures/gen_textures.py` → `textures/*.png`, nejsou v gitu): kůra, čela, lano, proutí, mazanina, plátno, železo, kůže, dřevěné uhlí, voda. Jen vybrané: `python tools/textures/gen_textures.py T_RuinRope T_RuinDaub`. Build je sám naimportuje do `/Game/Skvt/Lapikus/Ruin/Textures` (normálové mapy nastaví jako Normalmap). Po změně textur zvyš `TEX_VERSION` v `zrlib/config.py`.
- Skript vybere ke každému bloku variantu podle poměru délka/výška a naškáluje ji **přesně na rozměr bloku** (`STONE_OVERSIZE = 1.04` = o 4 % větší, aby spáry nebyly moc hluboké). Polovina kamenů je otočená o 180°, takže se tvary méně opakují. Varianta je vázaná na ID bloku a po přegenerování se nemění.
- **Osy meshů:** OBJ se zapisuje rovnou v osách UE (`tools/meshes/mesh_common.obj_v`, `obj_f`; import OBJ v UE otáčí znaménko Y a s ním pořadí vrcholů trojúhelníků, ověřeno skriptem `tools/checks/UE_Osy_OBJ.py`, proto se zapisuje zrcadlené Y i obrácené trojúhelníky). Asset tedy stojí správně i v Content Browseru a po ručním přetažení do scény. Skript při stavbě jen naškáluje mesh na rozměr bloku (osy prohodí, jen když nesedí rozměry, např. u cizího meshe). Meshe importované se starým zápisem (do 15. 11. 2026: OBJ Y-up, v UE naležato, při stavbě se otáčely o 180°) se díky `MESH_AXES` v `zrlib/config.py` naimportují znovu samy.
- **Kontrola normál bez UE:** `python tools/checks/check_normals.py meshes/props` (paprsky po normále; lichý počet průsečíků = normála dovnitř). Hlásí i falešné poplachy u otevřených ploch (hladina, otevřený náboj), ty ověř náhledem.
- **Ruční import** (když automatický selže, v Output Logu je `Ruin: chybi … kamenu`):
  1. Přetáhni `.obj` ze složky `meshes\stone` do Content Browseru do `Skvt/Lapikus/Ruin/Stones` a z `meshes\wood` do `Skvt/Lapikus/Ruin/Wood`.
  2. V importu zapni **Nanite**. Materiál neřeš.
  3. Každý mesh otevři a dej **Collision → Add Box Simplified Collision** → Save. Bez toho postava projde zdí.
  4. Názvy assetů musí zůstat `SM_RuinStone_R12_A` atd.
- **Vlastní tvary:** `python tools/meshes/gen_meshes.py` (z kořene, potřebuje numpy) přegeneruje OBJ do `meshes/<kategorie>/`. Jen část: `python tools/meshes/gen_meshes.py stone` (kategorie `stone`, `wood`). Tvar kamenů se ladí parametry `make_stone` v `tools/meshes/mesh_stone.py` (`radius`, `amp`, `edge`, `bulge`). Pak zvyš verzi v `STONE_MESH_VERSION` (`zrlib/config.py`), nebo smaž staré meshe v `Ruin/Stones` (`Ruin/Wood`), a spusť build znovu. Starý `gen_stones.py` dál funguje, volá nový generátor.
- **Složky podle kategorie:** kategorie = modul `tools/meshes/mesh_<kategorie>.py` = podsložka `meshes/<kategorie>` = složka v UE podle `MESH_DIRS` (`zrlib/config.py`). Nová kategorie: postup v hlavičce `gen_meshes.py`. Kategorie `wood` má tři moduly: `mesh_wood.py` (hraněné dřevo) volá `mesh_log.py` (kulatina) a `mesh_bark.py` (pásy kůry). Další kategorie: `wattle` (`mesh_wattle.py`), `textile` (`mesh_textile.py`), `props` (`mesh_props.py`).
- **Náhled bez Unrealu:** `python tools/checks/preview_meshes.py meshes/wood <out.png> [prefix ...]` vykreslí meshe ze dvou pohledů, barvy podle slotů. Odvrácené plochy se nekreslí, takže otočené normály jsou vidět jako díry.
- `USE_STONE_MESHES = False` vrátí všude kostky.

### 1.2 Materiály

- `M_RuinStone` je master materiál s parametry `BaseColor`, `Normal`, `TintA`, `TintB`, `Tiling` a `Roughness`. Každý kámen dostane náhodný odstín mezi TintA a TintB a náhodný posun textury (Per Instance Random), takže dva sousední kameny nikdy nevypadají stejně. Žádné „cihly v cihle“ jako u `M_Brick_Hewn_Stone`.
- **Zvětrání shora (všechny kameny):** podle normaly plochy (`VertexNormalWS.z`). Co míří nahoru, je světlejší, nazelenalé a drsnější. Skvrny rozbíjí textura. Parametry: `TopTint` (barva), `TopStart` (od jakého sklonu, 0 = svislá stěna, 1 = vodorovný vrch), `TopSharp` (ostrost přechodu), `TopAmount` (síla: líc 0,55, jádro 0,45, ostění 0,35, koruna 1,0). Výchozí hodnoty jsou v `MAT_TOP` ve skriptu.
- **Verze materiálu:** `MAT_VERSION` v `zrlib\config.py`. Když je `M_RuinStone` v projektu starší, skript jeho graf přestaví na místě a do `MI_Ruin*` jen doplní nové parametry `Top*`. Tvoje tinty a textury v `MI_RuinFace/Core/Frame` zůstanou, `MI_RuinCrown` dostane nový tint z `MAT_LOOK`.
- Vzhled ladíš v `MI_RuinFace`, `MI_RuinCore` a `MI_RuinFrame` (dvojklik → Details). Hodí se tam i textura z Fabu (Megascans, např. „Rock“ nebo „Stone Wall“ surface): stačí přepsat `BaseColor` a `Normal`.
- Úplně vlastní materiál nastavíš v `zrlib\config.py`: `MAT_FACE = "/Game/…/MI_X.MI_X"` (stejně `MAT_CORE`, `MAT_FRAME`). `None` znamená automatický materiál.
- Když chceš materiál vytvořit znovu od nuly, smaž `M_RuinStone` a `MI_Ruin*` a spusť build.
- **Chybí textury StarterContent:** Output Log hlásí `nenalezeny textury`. Přidej Starter Content (Content Browser → **Add → Add Feature or Content Pack → Starter Content**), nebo v `TEXTURES` nahoře ve skriptu nastav vlastní cesty.

---

### Dřevo, kulatina a další knihovní meshe

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
| `peeling` | `SM_RuinLogPeeling` | rozpracovaná kulatina s kůrou, nahoře (+Z) z 2/3 oloupaná (kozy na staveništi domu) |

- **Materiálové sloty:** `Wood` = materiál podle úpravy dílce (`cat`: `raw`, `tar`, `old`… a nově `peeled` = `MI_RuinWood_Peeled`, čerstvě loupané světlé dřevo), `EndGrain` = čela `MI_RuinWood_EndGrain` (letokruhy, trhliny), `Bark` = kůra `MI_RuinBark`. Materiály slotů vytvoří skript 03 (`SLOT_MI` v `zrlib\config.py`), vzhled v `MAT_LOOK["bark"]`, `["endgrain"]`, `["wood_peeled"]`.
- **Textury** kůry a čel jsou vlastní, procedurální (`tools\textures\gen_textures.py`). Čela mají polární UV (u = úhel, v = vzdálenost od středu), takže letokruhy jsou soustředné a s náhodným posunem materiálu každé čelo jiné.
- **Rozpracovaná kulatina** (tvar `peeling`, `SM_RuinLogPeeling_A/B`, 21. 11. 2026): kulatina s kůrou, nahoře (+Z) asi ve 2/3 délky oloupaná, okraj kůry v pruzích po loupáku, v oloupaném pásu stopy po loupáku. Klade se s `roll` 0, aby oloupaná strana byla nahoře. Parametr `bare` v `mesh_log.tube` (kde je kůra už oloupaná) ostatní meshe nemění, ty zůstaly bajtově stejné.
- **Rozměry a varianty:** `ROUND_MESHES` v `zrlib\config.py` (musí odpovídat `NOMINAL` v `mesh_log.py`).
- **Ukázka v UE:** `tools\meshes\Ukazka_Meshe.py` postaví všechna témata. Jednotlivá témata postaví `tools\meshes\ukazka\Ukazka_<Tema>.py` (kulatina, dřevo, kůra a proutí, textil, kovárna, nářadí, obydlí, stan, guesthouse; seznam meshí `UKAZKY` v `tools\meshes\ukazka.py`): téma importuje jen svoje meshe (`ensure_stone_meshes(only=…)`), stojí ve vlastním pásu v Y od `ORIGIN`, má tag `Ukazka_Meshe_<tema>` a `MODE = "clear"` smaže jen svoje téma. Nový mesh přidej do tématu v `UKAZKY`. Import a materiály dělá mimo transakci, Undo vrátí jen actory. Level zříceniny ani stavby nemění.
- **Jen vybrané OBJ:** `gen_meshes.py --only PREFIX,…` zapíše jen meshe s daným prefixem; kompletní podklady bez `--only` (22. 11. 2026).

**Další knihovní meshe** (`LIB_MESHES` v `zrlib\config.py`, dílec = `Stone` se `shape` z `LIB_SHAPES`, `cat` = materiál):

| `shape` | Mesh | Kategorie (UE) | Sloty | `cat` | Poznámka |
|---|---|---|---|---|---|
| `bark_strip` | `SM_RuinBarkStrip` 160 × 70 cm | `wood` (`Ruin/Wood`) | `Bark`, `EndGrain` (spodek = lýko) | `bark` | pás kůry, délka podél X = po spádu, hrubá strana nahoru (+Z) |
| `wattle_panel` | `SM_RuinWattlePanel` 100 × 8 × 100 cm | `wattle` (`Ruin/Wattle`) | `Daub`, `Wattle` | `daub` | dílec stěny v rovině XZ, rovné okraje → skládá se vedle sebe a nad sebe |
| `smoke_hood` | `SM_RuinSmokeHood` 140 × 120 × 100 cm | `wattle` | `Daub`, `Wattle` | `daub` | dymník, škáluje se na rozměr |
| `chimney` | `SM_RuinChimney` 60 × 60 × 100 cm | `wattle` | `Daub`, `Wattle` | `daub` | komín, výška přes `sz` |
| `rope` | `SM_RuinRope` 100 × 1,5 cm | `textile` (`Ruin/Textile`) | `Rope` | `rope` | článek lana; prověšené lano = řetěz článků podél řetězovky |
| `lashing` | `SM_RuinLashing` 7 × 10,5 cm | `textile` | `Rope` | `rope` | ovázání tyče Ø 8 cm (osa X), škáluje se s tyčí |
| `canvas_tent` | `SM_RuinCanvasTent_A` 246 × 228 × 190 cm (na míru, `.json` se stojkami a kolíky) | `textile` | `Canvas` | `canvas` | plachta stanu do A, +X vchod, +Y odhrnutá chlopeň; karta v [[Katalog_props]] |

## Kdo používá
- [[03_ruin]]: kameny zdí, ostění, kapsy; [[03_ruin_generator]].
- [[05_constructions]] a části ([[05_constructions_ostroh]], [[05_constructions_kovarna]], [[05_constructions_dum]], [[05_constructions_vez]]): dřevo, kulatina, knihovní meshe.
- [[06_furnishing]]: vybavení skládané z knihovních meshí.

## Dopad změny
- Nový nebo změněný mesh: funkce v `tools\meshes\mesh_*.py`, záznam v `LIB_MESHES` / `ROUND_MESHES` (`zrlib\config.py`), vygenerovat `python tools/meshes/gen_meshes.py`; build si chybějící meshe doimportuje sám.
- Změna rozměru v `LIB_MESHES` mění polohy dílců ve všech stavbách, které ho používají: přegeneruj dotčené kroky a spusť `run_checks.py`.
- Stav assetů pro návrhy: [[CHECKLIST_assets_navrhy]].

## Známé pasti
Viz [[Pasti_generator_meshi]] a [[Pasti_import_meshi_a_assety]].
