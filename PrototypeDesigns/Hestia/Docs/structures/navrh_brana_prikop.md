---
# orchestrace
type: design
validity: valid
derived_from:
alternative_to: []
updated: 2026-11-23
aliases: []
# hra
status: in_progress
domain: structures
category: []
entity: "[[Brana]]"
depth: 4
build_step: 05_constructions
assets: []
---
# Návrh: Šíjový příkop, terénní valy, přemostění a zátaras před vstupní branou

## Souhrn
Architektonický návrh hlavního ve skále vylámaného šíjového příkopu, vnějších terénních valů na šíji ostrožny, únikové rampy ze dna příkopu, zbytků kamenného mostního pilíře a opěry ([[03_ruin]]), provizorní dřevěné mostní lávky a umístění přenosného zátarasu `Brana_Zataras` ([[05_constructions]]) před východní vstupní branou ([[Brana]], [[Strazni_Vez]], [[Hradby_a_Brana]]).
- **Terén ([[01_terrain]]):** V `tools/1_gen_heightmap_1009.py` (a/nebo pomocným skriptem nad `Zricenina_heightmap_505_50cm.png` a `terrain_from_level.json`) se zruší starý příkop (`t_rel = 37 m`, který po posunu strážní věže v Půdorysu v3 ležel přímo pod věží) a pod zdmi hradu (`u <= 8,1 m` u `Brana_*`, `u <= 5,8 m` u `Hradba_V`) se zachovají výšky z `terrain_from_level.json`. Těsně před `Brana_V` a `Hradba_V` se vyláme nový **šíjový příkop** (horní šířka `8,2 m` mezi `u = 8,1 m` a `u = 16,3 m`, šířka plochého dna `3,8 m` mezi `u = 10,3 m` a `u = 14,1 m`, kóta dna `Z = 2700 cm`, sklon skalních stěn `54°–56° > 42°` pro skalní texturu v [[M_Landscape_Forest_Auto]] i `> 44°` limit chůze postavy). Na severním konci příkopu (`d = -1,0 .. -5,5 m`) vede ze dna šikmá **úniková rampa** (`sklon 25,8° < 44°`, šířka `2,0 m`) ven na severní svah šíje před valy, aby hráč po pádu do příkopu neuvízl.
- **Terénní valy na šíji (`u = 16,3 .. 23,5 m`):** Před vnější hranou příkopu stojí čelní **terénní val** (hřeben v `u = 19,0 m`), rozdělený v ose 1. brány (`d = 3,1 m`) přístupovým úvozem šířky `3,2 m` na **jižní hlavní křídlo** (`d = 5,5 .. 19,5 m`, koruna `Z = 3380–3440 cm`, převýšení `+1,2 až +1,4 m` nad hřbetem šíje) a **severní křídlo** (`d = -3,5 .. 0,8 m`, koruna `Z = 3180–3250 cm`, převýšení `+1,0 m`).
- **Zřícenina ([[03_ruin]], část `Obvod`):** Kamenná podstavba `Brana_V` (`plinth: 2,0 m`, `z_offset: -2,1 m`, kameny do `Z = 2692 cm`) se na skarpě příkopu odkryje v celé výšce `3,4 m` pod prahem brány (`Z = 3040 cm`). Uprostřed příkopu (`u = 12,20 m`, `d = 1,60 .. 4,60 m`) stojí rozpadlý kamenný **mostní pilíř `Brana_Pilir`** (`3,0 × 1,4 m`, koruna `Z ≈ 2990–3010 cm`) a na vnější hraně kontraskarpy (`u = 16,30 m`, `d = 1,50 .. 4,70 m`) kamenná **mostní opěra `Brana_Opera`** (`3,2 × 1,2 m`). Mřížka `terrain` v `gen_layout.py` se na východě rozšíří z `x1 = 3600` na `x1 = 4400`.
- **Dostavba druhého zabydlení ([[05_constructions]], sada `base`):** Posádka vyrovnala korunu pilíře a opěry kamenem z rozvalin (`Brana_Most_Kamen`, typ `stone_fill`, vrch `Z = 3011 cm`) a přes dvě pole po `~3,3 m` světlého rozpětí položila provizorní dřevěnou lávku **`Brana_Most`** (typ `platform`: 3 podélné klády [[SM_RuinLog_A]] Ø `24 cm` v `d = 2,1 / 3,1 / 4,1 m`, `u = 7,75 .. 16,65 m`, a příčná prkna [[SM_RuinPlank_A]] tl. `5 cm` v šířce `2,40 m`, vrch mostovky **`Z = 3040 cm`** v rovině prahu brány i předmostí). Přenosný španělský jezdec **`Brana_Zataras`** ([[SM_RuinLogBark_A]] + [[SM_RuinStakeSmall_A]]) stojí v hrdle přístupového úvozu na východním předmostí lávky (`u = 17,20 m, d = 3,10 m, Z = 3040 cm`).

## Zadání / záměr
- **Odkud:** GameDesigner (2026-11-23), historický záznam o předloze ([[Lore_Lapikus]]): *„Přístupovou stranu (šíji ostrožny) chránily terénní valy a hluboký, ve skále vylámaný šíjový příkop.“*
- **Potvrzená rozhodnutí GameDesignera (2026-11-23):**
  1. **Rozsah (Varianta 1):** Kompletní řešení hlavního šíjového příkopu těsně před `Brana_V` a `Hradba_V` včetně vnějších terénních valů, zbytků mostního pilíře a opěry (03), provizorní mostní lávky (05), polohy zátarasu `Brana_Zataras` a napojení na podstavby zdí. (Vzdálenější 1. příkop a předhradí se podle [[Zricenina_03_ruin_stav]] zatím nedělají.)
  2. **Způsob realizace v terénu (Varianta B se zálohou A):** Primárně upravit generování heightmapy (`Zricenina_heightmap_505_50cm.png` + `terrain_from_level.json`) se zasypáním původního příkopu (`t_rel = 37 m`) pod strážní věží; pro případ, že by reimport PNG do UE kolidoval s úpravami landscapu v levelu, dodat i pomocný Python skript pro aplikaci výškového rozdílu příkopu a valů přímo v UE Editoru.
  3. **Hratelnost a suť:** Hráč po případném pádu do příkopu **nesmí uvíznout** – ze dna příkopu musí vést schůdná cesta ven (`< 44°`). Suťové kužely na dně příkopu se doladí až po vizuální kontrole vykopaného tvaru v levelu.

## Výchozí stav

### 1. Souřadný rámec brány a poloha východních zdí (změřeno z dat k 2026-11-23)
Všechny souřadnice návrhu jsou vztažené k **rámu brány** z `Lapikus/tools/ruin/brana_spec.py` (`frame(walls)`):
- **Počátek rámu `origin`:** SZ roh strážní věže `GT_NW = [1930, -3107]` (UE cm).
- **Osa `u` (m, k VSV podél `Brana_S`):** jednotkový vektor `(0,97596; -0,21796)`, azimut `-12,59°`.
- **Osa `d` (m, kolmo k JJV podél `Brana_J`):** jednotkový vektor `(0,21796; 0,97596)`, azimut `+77,41°`.
- **Převod `(u, d)` [m] → světové `(X, Y)` [UE cm]:**
  `X = 1930 + 97,596 * u + 21,796 * d`, `Y = -3107 - 21,796 * u + 97,596 * d`.
- **Výšky `Z`:** absolutně v UE cm (kde `Z = výška_m * 100` při `Location Z = 3200`, `Scale Z = 12,5`).

| Prvek zříceniny (03) | Poloha v rámu brány `(u, d)` [m] | Světové `(X, Y)` [UE cm] | Tloušťka | Spodek kamenů `z_min` [cm] | Koruna / otvor `Z` [cm] | Poznámka |
|---|---|---|---|---|---|---|
| `Brana_V` (1. brána, východní) | osa `u = 7,20`; `d = 0,00 .. 6,60`<br>vnější líc **`u = 8,10`** | `(2633, -3264)` až `(2777, -2620)`<br>líc u brány `(2788, -2981)` | `1,8 m` | **`2692`** (`d = 0..6`), `2728` (`d = 6..7`) | koruna `3617–3655`<br>vrch oblouku `3529`<br>**práh brány `3040`** | `plinth: 2,0 m`, `z_offset: -2,1 m`; otvor `brana` š. `3,2 m` (`d = 1,50 .. 4,70`, střed `d = 3,10`) |
| `Brana_S` (severní stěna) | osa `d = 0,00`; `u = 0,00 .. 7,20` | `(1930, -3107)` až `(2633, -3264)` | `1,8 m` | `2863` | koruna `3459–3553` | nese 4. trám podesty `Brana_Straz` a severní kryt |
| `Brana_J` (2. brána, západní) | osa `u = 0,00`; `d = 0,00 .. 7,32` | `(1930, -3107)` až `(2090, -2393)` | `1,8 m` | `2842` | koruna `3455–3549`<br>práh portálu `~3035` | portál `2,8 × 3,8 m` (`d = 2,10 .. 4,90`) |
| `Brana_Jih` (jižní stěna) | od `(0,00; 7,32)` do `(7,20; 6,60)` | `(2090, -2393)` až `(2777, -2620)` | `1,8 m` | `2947` | pahýl `3280–3377` | východně od `Hradba_V` (`u > 4,3 m`) silně rozpadlá |
| `Hradba_V` (východní hradba) | úsek 01–02: osa `u = 3,00 → 4,46`, `d = 7,03 → 16,01` (vnější líc **`u = 4,25 → 5,71`**); dále oblouk k `Vez_V` | `(2376, -2487)` → `(2585, -1610)` → `(1846, -989)` | `2,5 m` | **`2948`** (úsek 01, 05–07), `2985–3018` (úsek 02–04) | koruna `3385–3545` | ustoupená o `~2,4–3,8 m` západně za vnější líc `Brana_V`; bez `plinth` |
| Cesta `PCG_Path` ([[04_forest]]) | bod 1: `u = 14,50, d = 6,00`<br>bod 2: `u = 24,10, d = 7,70` | `(3250, -2231)` → `(4248, -2280)` → `(12600, -3761)` | šířka `6 m` (stezka `2,5 m`) | terén `3262 → 3370` | – | přichází od východu po hřbetu šíje |

### 2. Stav terénu (`terrain_from_level.json` vs. `Zricenina_heightmap_505_50cm.png`)
- Porovnání všech `89 × 43` buněk `Lapikus/03_ruin/blocks/terrain_from_level.json` (`X = -5200 .. 3600`, `Y = -3800 .. 400`, krok `100 cm`) s `Lapikus/01_terrain/Zricenina_heightmap_505_50cm.png` ukázalo, že **západně od `X = 1800` je terén v levelu totožný s PNG heightmapou** (odchylky `<= 20 cm` dané interpolací mřížky).
- Jediný rozdíl v levelu je v pásu `X = 1800 .. 3600` (`u = 0 .. 12 m`), kde byl v `1_gen_heightmap_1009.py` (ř. 214: `t_rel = 37,0 m`, `σ = 3,5 m`, hloubka `6,0 m`) vygenerován původní příkop (`Z ≈ 2572–2750 cm`), který po posunu strážní věže v Půdorysu v3 vyšel přímo pod `Brana_S/J/V` (`u = 0 .. 8,1 m`) a v UE levelu byl proto ručně zasypán na `Z ≈ 3015–3190 cm`.
- Východně od `Brana_V` (`u = 8,1 .. 25,0 m`) terén v `terrain_from_level.json` plynule stoupá z `Z = 3057 cm` (`u = 8 m, d = 3,1 m`) na `Z = 3225–3330 cm` směrem k hřbetu šíje – **před `Brana_V` a `Hradba_V` dnes žádný příkop ani valy nejsou**.

## Návrh

### 1. Šíjový příkop, terénní valy a úniková rampa ([[01_terrain]])

#### 1.1 Trasa a podélné vedení příkopu přes šíji ostrožny
Příkop protíná celou šíji ostrožny od severního svahu (`d = -5,5 m`) k jižnímu skalnímu srázu (`d = +20,5 m`, celková délka `~26 m`). Protože strážní věž `Brana_V` (`vnější líc u = 8,10 m`) předstupuje o `~2,5–3,8 m` před východní hradbu `Hradba_V` (`vnější líc u = 4,25 .. 5,71 m`), sleduje vnitřní horní hrana příkopu (`u_in(d)`) čelo hradu v plynulé křivce:

$$\text{u\_in}(d) = 8{,}10 - 1{,}10 \cdot \text{smoothstep}(6{,}5,\; 11{,}5,\; d) \quad [\text{m}]$$

- **Před strážní věží `Brana_V` (`d <= 6,5 m`):** `u_in = 8,10 m` – horní hrana vnitřní skalní stěny (*skarpy*) lícuje přímo s vnějším lícem `Brana_V` (`u = 8,10 m`). Tím zůstává terén v průjezdu brány (`u <= 8,10 m`, `Z = 3035–3055 cm`) **beze změny**, zatímco na vnějším líci `Brana_V` příkop obnaží kamennou podstavbu (`plinth: 2,0 m`, `z_offset: -2,1 m`, kameny do `Z = 2692 cm`) v čisté výšce **`3,40 m`** (od prahu `Z = 3040 cm` na dno příkopu `Z = 2700 cm`).
- **Před východní hradbou `Hradba_V` (`d = 11,5 .. 20,5 m`):** `u_in = 7,00 m`. Protože vnější líc `Hradba_V` leží v `u = 4,25 .. 5,71 m` a spodek jejích kamenů sahá na `Z = 2948 cm`, zůstává mezi patou `Hradba_V` a horní hranou skarpy (`u_in = 7,00 m`) skalní lavice (berma) šířky **`1,3–2,7 m`** na původní výšce terénu (`Z = 3120–3200 cm`). **Žádný kámen `Hradba_V` ani `Brana_Jih` tak nevisí ve vzduchu a výšky pat žádné zdi v `03_ruin` se neposunou.**

#### 1.2 Příčný profil příkopu (skarpa, dno, kontraskarpa)
V každém řezu `d` (pro `d \in [-5,0;\; 20,5]\text{ m}`) se příčný profil příkopu počítá od vnitřní hrany `u_in(d)`:

| Část profilu | Rozsah `u` před bránou (`d = 3,1 m`) | Obecný rozsah `u(d)` | Šířka | Výška `Z` [UE cm] | Sklon stěny | Materiál v [[M_Landscape_Forest_Auto]] |
|---|---|---|---|---|---|---|
| **Horní hrana skarpy** | `u = 8,10 m` | `u_in(d)` | – | `3030–3055` (u brány)<br>`3140–3200` (u `Hradba_V`) | – | přechod podstavba zdi / skála |
| **Vnitřní stěna (skarpa)** | `u = 8,10 .. 10,30 m` | `u_in .. u_in + 2,20 m` | `2,20 m` | klesá z `3040–3190` na `2700` | **`56°–65°`** (`> 44°` limit chůze) | **čistá skála** (`T_Rock_Slate`, `> 42°`) |
| **Ploché dno příkopu** | `u = 10,30 .. 14,10 m` | `u_in + 2,20 .. u_in + 6,00 m` | **`3,80 m`** | **`2700 cm`** (`d = -1..15 m`), ke koncům klesá na `2660 cm` | `0°–4°` (odvodnění k S a J srázu) | tráva se štěrkem (`< 25°`) |
| **Vnější stěna (kontraskarpa)** | `u = 14,10 .. 16,30 m` | `u_in + 6,00 .. u_in + 8,20 m` | `2,20 m` | stoupá z `2700` na `3040` (v úvozu cesty) resp. `3380–3440` (pod valem) | **`57°`** v úvozu, **`63°`** pod valem (`> 44°`) | **čistá skála** (`T_Rock_Slate`, `> 42°`) |
| **Celková horní šířka příkopu** | **`u = 8,10 .. 16,30 m`** | `u_in .. u_in + 8,20 m` | **`8,20 m`** | hloubka **`3,40 m`** pod prahem brány, **`6,8–7,4 m`** pod korunou valu | – | ve skále vylámaný šíjový příkop |

#### 1.3 Vnější terénní valy a přístupový úvoz na šíji (`u = 16,3 .. 24,0 m`)
Hned za horní hranou kontraskarpy (`u_out(d) = u_in(d) + 8,20 m`) navazuje **čelní šíjový val** navršený z vylámané horniny, přerušený v ose 1. brány (`d = 3,10 m`) přístupovým úvozem pro vozovou cestu a předmostí:

| Část valu / úvozu | Rozsah `u` [m] | Rozsah `d` [m] | Světové `(X, Y)` středu [cm] | Výška koruny / dna `Z` [UE cm] | Převýšení nad rostlým terénem | Tvar a herní účel |
|---|---|---|---|---|---|---|
| **Jižní (hlavní) křídlo valu** | základna `15,5 .. 23,5`<br>hřeben **`u = 19,0`** (šířka koruny `1,6 m`) | `d = 5,2 .. 19,5` (délka `14,3 m`) | `(4002, -2545)` (u `d = 10`) | **`3380–3440 cm`** | **`+1,20 až +1,45 m`** | Chrání celou jižní polovinu šíje před `Hradba_V`; vnitřní svah přechází plynule do skalní kontraskarpy (`63°`), vnější svah k východu klesá pod úhlem `~22°–26°` (štěrk/tráva). Koruna valu je o `1,4–2,0 m` níž než podesta `Brana_Straz` (`Z 3581`), takže necloní výhledu a střelbě stráže. |
| **Severní křídlo valu** | základna `15,8 .. 22,5`<br>hřeben **`u = 18,5`** (šířka koruny `1,4 m`) | `d = -3,8 .. 1,0` (délka `4,8 m`) | `(3703, -3657)` (u `d = -1,5`) | **`3180–3250 cm`** | **`+0,95 až +1,15 m`** | Uzavírá severní bok předmostí mezi přístupovým úvozem a severním svahem ostrožny. |
| **Přístupový úvoz (průrva ve valu)** | `u = 16,3 .. 24,5` (délka `8,2 m`) | dno `d = 1,50 .. 4,70` (šířka **`3,20 m`**, osa `d = 3,10`) | předmostí `(3588, -3160)` → napojení na cestu `(4389, -3339)` | předmostí (`u = 16,3`): **`3040 cm`**<br>ústí (`u = 24,5`): **`3250 cm`** | zářez `-1,4 až -1,8 m` oproti korunám valů | Dno úvozu začíná na předmostí (`u = 16,3 m`) přesně na kótě prahu 1. brány **`Z = 3040 cm`** a stoupá k východu pod mírným úhlem **`14,4°`** (`2,10 m` na `8,2 m`) na úroveň cesty `PCG_Path`. Boční svahy úvozu do obou křídel valu mají sklon `35°–42°` (štěrk/skála). |

#### 1.4 Cesta ven ze dna příkopu (ochrana proti uvíznutí hráče)
Aby hráč po pádu z mostní lávky na dno příkopu (`Z = 2700 cm`) v příkopu nikdy neuvízl, ale zároveň nemohl příkopem obejít bránu do hradu:
- **Severní úniková rampa (`d = -1,0 .. -5,5 m`, `u = 11,5 .. 16,8 m`):**
  - Ze severního konce plochého dna příkopu (`u = 12,2 m, d = -1,0 m, Z = 2700 cm`) vede šikmo ven přes severní výběžek kontraskarpy vylámaná rampa do bodu `(u = 16,5 m, d = -5,5 m, Z = 2990 cm)` (světově `(3122, -3471)` → `(3420, -4003)`).
  - **Parametry rampy:** délka `6,2 m`, šířka **`2,0 m`** (`>= 1,2 m` minimum pro pohyb postavy), převýšení `+2,90 m`, podélný sklon **`25,1°`** (`<< 44°` limit `Character Movement`, v materiálu terénu vykreslená jako štěrková stezka `20°–28°`).
  - Z horního konce rampy (`u = 16,5 m, d = -5,5 m, Z = 2990 cm`) přechází hráč po přirozeném severním úbočí šíje (`sklon 18°–24°`) vně severního křídla valu zpět na přístupovou cestu východně od úvozu (`u ≈ 23 m, d ≈ 2 m`).
  - Vnitřní stěna příkopu (skarpa pod `Brana_V` a `Hradba_V`) i jižní vyústění příkopu nad skalním srázem (`d > 19 m`) zůstávají po celé délce strmé (`> 53°`), takže ze dna příkopu nelze nikde vylézt přímo do hradu.

---

### 2. Úpravy zříceniny ([[03_ruin]], část `Obvod`)

#### 2.1 Odhalená podstavba `Brana_V` a berma `Hradba_V`
- **`Brana_V`:** beze změny parametrů v `gen_layout.py` (`plinth: 2,0 m`, `z_offset: -2,1 m`). Vykopáním skarpy od `u_in = 8,10 m` se automaticky odkryje stávající kamenná podstavba `Brana_V` od prahu brány (`Z = 3040 cm`) až na dno příkopu (`Z = 2700 cm`; nejnižší řada kamenů `Brana_V` leží na `Z = 2692 cm`, tj. `8 cm` pod dnem příkopu). Kapsy kladek a čepů padacího mostu (`features=["kapsa_most", "retezy"]`) na vnějším líci `Brana_V` zůstanou přímo nad mostovkou.
- **`Hradba_V` a `Brana_Jih`:** beze změny parametrů – díky skalní bermě (`u_in = 7,00 m` před `Hradba_V`) zůstává terén pod všemi kameny `Hradba_V` (`u <= 5,45 m`) i `Brana_Jih` (`u <= 7,15 m`) na původních výškách z `terrain_from_level.json`.
- **Rozšíření terénní mřížky v `Lapikus/tools/ruin/gen_layout.py` a `Lapikus/03_ruin/blocks/build_ruin_blocks.py`:**
  - V `gen_layout.py` (ř. 202) a v `zrlib/level.py` (`sample_terrain`, pokud přebírá rozsah z `layout["terrain"]`) rozšířit východní hranici mřížky `x1` z `3600` na **`4400`** (`nx` ze `89` na `97`), aby `terrain_from_level.json` pokryl celý příkop, mostní pilíř, vnější opěru i čelní valy.

#### 2.2 Středový mostní pilíř `Brana_Pilir` a vnější opěra `Brana_Opera` (`03_ruin`)
Světlá šířka příkopu `8,20 m` (`u = 8,10 .. 16,30 m`) je rozdělena středovým kamenným pilířem na dvě pole po `~3,3 m` světlého rozpětí (odpovídá [[Lore_Lapikus]]: *„most přes příkop zřícený (zbyly pilíře a trámy)“*):

| Zeď v `gen_layout.py` | Složka / část | Osa `points` v rámu `(u, d)` [m] → světové `[X, Y]` [cm] | Délka × tloušťka | `H0` / `access` / `seed` | Výškové osazení (`ref_z` / `cap` / `z_offset`) | Výsledný tvar v `03_ruin` |
|---|---|---|---|---|---|---|
| **`Brana_Pilir`** | `Ruin/Brana` (`Obvod`) | `(u = 12,20, d = 4,60)` → `(u = 12,20, d = 1,60)`<br>`[[3221, -2924], [3155, -3217]]` | **`3,00 × 1,40 m`** (`u = 11,50 .. 12,90`) | `H0 = 3,5 m`, `access = 0,45`, `seed = 64`, `rubble = "both"`, `extend_start = False` | pata na dně příkopu `Z = 2700 cm`; v `brana_spec.ruin_edits()` `cap` uprostřed (`s = 0,3 .. 2,7 m`) na **`z = 3011 cm`** | Masivní kamenný pilíř uprostřed příkopu vysoký `~3,1 m` nad dnem (`Z 2690–3011 cm`), s rozpadlými čely na S a J konci a rovně ubouranou korunou pod trámy lávky. |
| **`Brana_Opera`** | `Ruin/Brana` (`Obvod`) | `(u = 16,30, d = 4,70)` → `(u = 16,30, d = 1,50)`<br>`[[3623, -3004], [3554, -3316]]` | **`3,20 × 1,20 m`** (`u = 15,70 .. 16,90`) | `H0 = 2,2 m`, `access = 0,40`, `seed = 65`, `rubble = "out"`, `extend_start = False` | `z_offset = -1,2 m`, v `brana_spec.ruin_edits()` `cap` v šířce lávky (`s = 0,4 .. 2,8 m`) na **`z = 3011 cm`** | Kamenná opěrná zeď předmostí zapuštěná do horní hrany kontraskarpy v úvozu valu; nese východní konce mostních trámů a na krajích (`d = 1,5..1,9` a `4,3..4,7`) vyčnívá o 1 řadu kamene (`Z ~3045 cm`) jako boční zídky předmostí. |

---

### 3. Dostavba druhého zabydlení: lávka přes příkop a zátaras ([[05_constructions]])

Všechny prvky přemostění se definují ve sdílené specifikaci `Lapikus/tools/ruin/brana_spec.py` (nová funkce `most(walls)` a rozšíření `ruin_edits(walls)`) a generují přes `Lapikus/tools/constructions/gen_constructions.py` pomocí **stávajících typů staveb** `stone_fill` (`zr_stavby/zdivo.py`), `platform` (`zr_stavby/podesta.py`) a `props` (`zr_stavby/vybaveni.py`) a **stávajících assetů** (0 nových požadavků na assety).

#### 3.1 Přehled staveb přemostění v `05_constructions`

| Název stavby (`addon`) | Typ v `zr_stavby` | Sada (`stage`) | Assety a materiál | Rozměry v rámu brány `(u, d)` [m] a absolutní `Z` [cm] | Popis konstrukce |
|---|---|---|---|---|---|
| **`Brana_Most_Kamen`** | `stone_fill` | `base` | lomový kámen `SM_RuinStone_*` (`MI_RuinFace`) + jádro (`MI_RuinCore`, `mortar: 0,45 m`) | 1. díl `pilir`: `u = (11,65; 12,75)`, `d = (1,85; 4,35)`, `bottom_abs = 2940`, **`top_abs = 3011`**<br>2. díl `opera`: `u = (15,85; 16,75)`, `d = (1,85; 4,35)`, `bottom_abs = 2960`, **`top_abs = 3011`** | Vyrovnání vybouraných kapes a nerovností v koruně pilíře `Brana_Pilir` a opěry `Brana_Opera` kamenem z rozvalin do vodorovné roviny spodku mostních trámů `Z = 3011 cm`. |
| **`Brana_Most`** | `platform` | `base` | trámy: [[SM_RuinLog_A]] (loupaná kulatina, `finish: "old"` → `wood_old`)<br>mostovka: [[SM_RuinPlank_A]] (štípaná/řezaná prkna, `finish: "old"`) | **Trámy (`beams`):** 3 ks Ø **`0,24 m`**, `pos = [2,10; 3,10; 4,10]`, `a = (7,75; 16,65)` (délka `8,90 m`, styk nad pilířem v `u = 12,20 m`), spodek **`z = 3011 cm`**, vrch `3035 cm`.<br>**Mostovka (`planks`):** příčná prkna tl. **`0,05 m`**, š. `0,22–0,32 m`, mezera `0,010 m`, `a = (7,90; 16,50)` (délka `8,60 m`), `c = (1,90; 4,30)` (**šířka lávky `2,40 m`**), **`deck_top = 3040 cm`**.<br>**Zábradlí:** žádné (`rails = []`). | Provizorní dřevěná lávka přes obě pole příkopu (světlá rozpětí `3,40 m` a `2,80 m` – kulatina Ø 24 cm s velkou rezervou splňuje limit 5–6 m). Na západě leží `0,35 m` na kamenném prahu v průjezdu `Brana_V` (`u = 7,75..8,10`), uprostřed `1,40 m` na `Brana_Pilir` (`u = 11,50..12,90`) a na východě `0,95 m` na `Brana_Opera` (`u = 15,70..16,65`). Vrch mostovky `Z = 3040 cm` plynule navazuje na práh brány (`Z 3040`) i terén předmostí (`Z 3040`). |
| **`Brana_Zataras`** | `props` (`loose: True`) | `base` | hlavní kmen: [[SM_RuinLogBark_A]] (kulatina s kůrou Ø `0,18 m`, délka `3,40 m`)<br>4 páry kůlů: [[SM_RuinStakeSmall_A]] (loupané zašpičatělé kůly Ø `0,07 m`, délka `1,60 m`) | Střed na předmostí v hrdle úvozu valu: **`u = 17,20 m, d = 3,10 m`**, terén **`Z = 3040 cm`** (`ref = (16,50; 3,10)`).<br>Osa kmene rovnoběžně s `Brana_V` (`d = 1,40 .. 4,80 m`), střed kmene ve výšce `z = +0,56 m` (`Z = 3096 cm`); 4 páry zkřížených kůlů pod úhlem `±45°` v `d = 1,85 / 2,68 / 3,52 / 4,35 m`, opřené špičkami o zem v `u = 17,20 ± 0,56 m` a vršky čnící do `Z = 3153 cm` (`1,13 m` nad zemí). | Přenosný španělský jezdec (1+8 dílců se společným `ref`, nebo složený actor podle úkolu `T-0036`). Uzavírá celou šířku `3,20 m` přístupového úvozu ve valu `0,70 m` před vstupem na dřevěnou lávku (`u = 16,50 m`), přesně v palebném poli tří průzorů východního krytu [[Brana_Straz]] (`u = 7,50 m, Z = 3716 cm`). |

> **Poznámka k dělení klád lávky (`Brana_Most`):** V `zr_stavby/podesta.py` se každý trám v `beams["pos"]` klade v rozsahu `a = (a0, a1)`. Aby lávka konstrukčně odpovídala dvěma polím z kratších klád (`~4,5 m`, které 2–3 lidé unesou a položí ručně) se stykem nad středovým pilířem `Brana_Pilir` (`u = 11,50 .. 12,90 m`), zadá se v `beams`:
> - `pos = [2.10, 3.10, 4.10, 2.34, 3.34, 4.34]` (nebo 3 západní klády `spans = [(7.75, 12.40)] * 3` v `d = 2.10, 3.10, 4.10` a 3 východní klády `spans = [(12.00, 16.65)] * 3` přeložené vedle nich o `0,22 m` v `d = 2.32, 3.32, 4.32` nad pilířem `u = 12.00 .. 12.40 m`). Přeložení dvou ~4,6m klád vedle sebe nad středovým pilířem vypadá v levelu přirozeně a nevyžaduje žádnou úpravu kódu `podesta.py` (`podesta.py` už parametr `spans` na ř. 34 přímo podporuje!).

---

## Souhrn specifikace

### 1. Parametry terénu příkopu, valů a únikové rampy (pro `tools/1_gen_heightmap_1009.py` / `tools/terrain/gen_moat.py`)
Funkce `apply_gate_moat(H_505, terr_level)` nad výřezem `505 × 505 px` (`0,5 m/px`, `X = (px - 252) * 50`, `Y = (py - 252) * 50`, `Z_m = H_505`):
1. **Zasypání starého příkopu (`u <= 8,1 m`):**
   - V oblasti hradu a strážní věže (`X \in [-5200, 3600]`, `Y \in [-3800, 400]`) se před vyhloubením nového příkopu pro `u <= 10,0 m` převezme vyhlazená výška z `terrain_from_level.json` (s plynulým prolnutím `smoothstep(9,0, 13,0, u)` do původní `Zricenina_heightmap_505_50cm.png`), čímž zmizí starý příkop (`t_rel = 37 m`) pod strážní věží a **všechny stávající zdi hradu si zachovají na milimetr stejnou výšku paty `zb`**.
2. **Nový šíjový příkop (`u_in(d) = 8,10 - 1,10 * ss(6,5, 11,5, d)`):**
   - Podélná maska šíje: `m_d = ss(-6,5, -3,5, d) * (1 - ss(18,5, 21,5, d))`.
   - Příčný profil příkopu:
     `w_cut(u, d) = ss(u_in(d), u_in(d) + 2,20, u) * (1 - ss(u_in(d) + 6,00, u_in(d) + 8,20, u))`.
   - Cílová výška dna příkopu (m):
     `z_floor(d) = 27,00 - 0,30 * ss(0,0, -5,0, d) - 0,40 * ss(14,0, 20,0, d)`.
   - Aplikace výkopu: `H = H * (1 - m_d * w_cut) + np.minimum(H, z_floor) * (m_d * w_cut)`.
3. **Severní úniková rampa (`d \in [-6,0, -0,5]`, `u \in [11,5, 17,0]`):**
   - Osa rampy od `P0 = (u = 12,2, d = -1,0, Z = 27,00 m)` do `P1 = (u = 16,5, d = -5,5, Z = 29,90 m)`.
   - Pro body ve vzdálenosti `dist_ramp <= 1,8 m` od úsečky `P0–P1` (`w_ramp = 1 - ss(0,9, 1,8, dist_ramp)`): lineární rampa `z_ramp(t) = 27,00 + 2,90 * t` (`sklon 25,1°`), prolnutá do `H`: `H = H * (1 - w_ramp) + z_ramp * w_ramp`.
4. **Čelní terénní valy a přístupový úvoz (`u_out(d) = u_in(d) + 8,20`):**
   - Příčný profil valu (`u_val = u_out(d) + 2,60`, základna od `u_out(d)` do `u_out(d) + 7,20`):
     `w_val_u = ss(u_out(d), u_out(d) + 1,80, u) * (1 - ss(u_out(d) + 3,40, u_out(d) + 7,20, u))`.
   - Podélná maska křídel valu (přerušená úvozem v `d = 1,50 .. 4,70 m`):
     - Jižní křídlo: `m_val_J = ss(4,70, 6,00, d) * (1 - ss(17,5, 20,0, d))`, převýšení `+1,35 m`.
     - Severní křídlo: `m_val_S = ss(-4,2, -2,8, d) * (1 - ss(0,4, 1,50, d))`, převýšení `+1,05 m`.
     - `H += w_val_u * (1,35 * m_val_J + 1,05 * m_val_S)`.
   - Přístupový úvoz (`d \in [1,0, 5,2]`, `u \in [16,3, 24,5]`):
     - Maska úvozu `w_cut_path = (1 - ss(1,40, 2,40, abs(d - 3,10))) * ss(15,8, 16,3, u) * (1 - ss(22,5, 25,0, u))`.
     - Cílová niveleta cesty v úvozu: `z_path(u) = 30,40 + 2,10 * np.clip((u - 16,3) / 8,2, 0, 1)`.
     - `H = H * (1 - w_cut_path) + z_path * w_cut_path`.

### 2. Specifikace do `Lapikus/tools/ruin/brana_spec.py`
```python
WALL_PILIR, WALL_OPERA = "Brana_Pilir", "Brana_Opera"

B_MOAT_FLOOR_Z = 2700.0          # dno sijoveho prikopu pred branou (UE cm)
B_BRIDGE_BEAM_Z = 3011.0         # spodek mostnich tramu (UE cm): +24 cm tram + 5 cm prkno = vrch mostovky Z 3040 (= prah brany)
B_BRIDGE_BEAM = dict(
    d=0.24,
    pos=(2.10, 3.10, 4.10, 2.32, 3.32, 4.32),                  # 3 zapadni + 3 vychodni klady prelozene nad stredovym pilirem
    spans=[(7.75, 12.40)] * 3 + [(12.00, 16.65)] * 3,
    a=(7.75, 16.65),
    bark=False,
    stage="base",
)
B_BRIDGE_DECK = dict(
    a=(7.90, 16.50), c=(1.90, 4.30),                           # delka 8.6 m, sirka lavky 2.4 m (stred d = 3.10)
    t=0.05, w=(0.22, 0.32), gap=0.010, max_len=2.6, stage="base",
)
B_BRIDGE_FILL = [
    dict(id="pilir", a=(11.65, 12.75), c=(1.85, 4.35), bottom_abs=2940.0, top_abs=B_BRIDGE_BEAM_Z),
    dict(id="opera", a=(15.85, 16.75), c=(1.85, 4.35), bottom_abs=2960.0, top_abs=B_BRIDGE_BEAM_Z),
]
B_ZATARAS = dict(
    u=17.20, d=3.10, ref=(16.50, 3.10),                        # predmosti v hrdle uvozu valu (0.7 m pred lavkou, Z = 3040 cm)
    log_d=0.18, log_len=3.40, log_z=0.56,                      # kmen s kurou SM_RuinLogBark_A
    stake_d=0.07, stake_len=1.60, stake_offs=(-1.25, -0.42, 0.42, 1.25),
    stage="base",
)
```

### 3. Náčrt slovy
- **Půdorys (od západu k východu v ose 1. brány `d = 3,1 m`):**
  - Východní zeď strážní věže `Brana_V` (`u = 6,3 .. 8,1 m`) s průjezdem šířky `3,2 m` (`d = 1,5 .. 4,7 m`).
  - Hned za vnějším lícem `Brana_V` (`u = 8,1 m`) padá do hloubky `3,4 m` ve skále vylámaný šíjový příkop široký nahoře `8,2 m` (`u = 8,1 .. 16,3 m`) a dole `3,8 m` (`u = 10,3 .. 14,1 m`), který běží napříč celou šíjí od severního svahu (`d = -5,5 m`) k jižnímu útesu (`d = 20,5 m`).
  - Uprostřed dna příkopu (`u = 12,2 m`) stojí kamenný pilíř `Brana_Pilir` (`3,0 × 1,4 m`) a na vnější hraně příkopu (`u = 16,3 m`) kamenná opěra `Brana_Opera` (`3,2 × 1,2 m`).
  - Přes obě pole příkopu vede dřevěná lávka `Brana_Most` široká `2,4 m` z příčných prken na třech dvojicích podélných klád přeložených nad středovým pilířem.
  - Za vnější hranou příkopu (`u = 16,3 .. 23,5 m`) se zvedá mohutný terénní val s hřebenem v `u = 19,0 m`, rozdělený v ose mostu (`d = 1,5 .. 4,7 m`) zářezem přístupového úvozu. V úzkém hrdle úvozu těsně před lávkou (`u = 17,2 m`) stojí napříč španělský jezdec `Brana_Zataras`.
  - Na severním konci příkopu (`d = -1,0 .. -5,5 m`) vede ze dna šikmo ven štěrková úniková rampa (`25,1°`), po které lze z příkopu vyjít kolem severního křídla valu zpět na cestu.
- **Podélný řez východ–západ (`d = 3,1 m`):**
  - Vlevo průjezd strážní věže (`Z = 3040–3048 cm`) s gotickým obloukem `Brana_V` (`vrch Z 3529 cm`) a strážní podestou + východním krytem z kůlů nahoře (`Z 3581–3761 cm`).
  - Pod prahem brány (`Z 3040 cm`) klesá kamenná podstavba `Brana_V` po skalní skarpě (`56°`) až na dno příkopu (`Z 2700 cm`).
  - Ze dna příkopu (`Z 2700 cm`) vystupuje uprostřed (`u = 12,2 m`) kamenný pilíř `Brana_Pilir` do výšky `Z 3011 cm`. Na něm a na opěře `Brana_Opera` (`u = 16,3 m`) leží klády Ø 24 cm (`Z 3011–3035 cm`) a prkna mostovky (`vrch Z 3040 cm`) v jedné vodorovné rovině s prahem brány.
  - Vpravo za opěrou (`u = 16,3 m, Z 3040 cm`) stojí na předmostí španělský jezdec (`u = 17,2 m`), po obou stranách úvozu se tyčí křídla čelního valu (`Z 3250` na severu, `Z 3420` na jihu) a dno úvozu stoupá mírným sklonem (`14,4°`) na hřbet šíje k cestě `PCG_Path` (`u = 24,5 m, Z 3250 cm`).

## Vazby a závislosti
- **Vazba na [[Brana_Straz]] ([[navrh_brana_straz]], [[stav_brana_straz]]):**
  - Tento návrh uzavírá otevřené body z [[navrh_brana_straz]] kap. 1, 4.5 a 9 (*„příkop a most před bránou, poloha zátarasu“*).
  - Výška žádných stávajících zdí strážní věže (`Brana_V`, `Brana_S`, `Brana_J`, `Brana_Jih`) ani `Hradba_V` se nemění, takže kapsy v `Brana_V` (`B_BEAM_Z = 3552 cm`), podesta (`Z 3581 cm`), kryty i navržená stříška z kůry ([[predani_brana_straz_striska_stavitel]]) zůstávají beze změny.
- **Vazba na úkol `T-0036` (`Brana_Zataras`):**
  - Úkol `T-0036` ve frontě `Maintenance/queue.md` zadává staviteli složení španělského jezdce `Brana_Zataras` z [[SM_RuinLogBark_A]] a 4 párů [[SM_RuinStakeSmall_A]]. Tento návrh určuje jeho cílovou souřadnici na východním předmostí v hrdle valu (`u = 17,20 m, d = 3,10 m, Z = 3040 cm`).
- **Vazba na [[01_terrain]] a [[04_forest]]:**
  - Při úpravě `Zricenina_heightmap_505_50cm.png` (Varianta B) se v `Lapikus/01_terrain/` přegeneruje i náhled sklonu `Zricenina_preview_orez.png`. První bod splinu `PCG_Path` (`(3250, -2231)`, tj. `u = 14,5 m, d = 6,0 m`) ležel před posunem brány jižně od osy brány; s novým příkopem začíná vozová cesta před úvozem valu v `(4389, -3339, Z 3250)`.
  - Pokud by reimport PNG do UE Landscape přepsal jiné ruční úpravy v levelu, použije [[Builder]] záložní **Variantu A**: Python skript v UE Editoru, který upraví výšky landscapu (nebo přímo `terrain_from_level.json` + Landscape heightmap data přes `LandscapeEditorUtils`) pouze v masce nového příkopu a valů (`u >= 8,1 m`).

## Ověření
1. **Kontrola terénu a materiálů ([[01_terrain]]):**
   - V `Zricenina_preview_orez.png` i v UE Editoru (při zapnutém `Debug_Slope` v `MI_Landscape_Forest_Auto`) jsou skarpa (`u = 8,1 .. 10,3 m`) i kontraskarpa (`u = 14,1 .. 16,3 m`) červené (`> 42°`, textura skály `T_Rock_Slate`), zatímco dno příkopu (`Z = 2700 cm`), koruny valů a severní úniková rampa (`25,1°`) jsou zelené/žluté (tráva/štěrk).
   - Pod zdmi `Brana_S`, `Brana_J`, `Brana_Jih` a `Hradba_V` se výška terénu oproti dosavadnímu `terrain_from_level.json` nezměnila (`ΔZ = 0 cm`).
2. **Kontroly zříceniny a dostaveb mimo UE (`run_checks.py`, `preview3d.py`):**
   - `python Lapikus/tools/checks/run_checks.py` projde bez chyby (`openings`, `floating`, `brana` – žádné plovoucí kameny na `Brana_V`, `Brana_Pilir`, `Brana_Opera` ani `Hradba_V`).
   - 3D náhled `python Lapikus/tools/checks/preview3d.py brana <out.png>` zobrazí pilíř `Brana_Pilir`, opěru `Brana_Opera`, vyrovnávací zdivo `Brana_Most_Kamen`, dřevěnou lávku `Brana_Most` a španělského jezdce `Brana_Zataras`.
3. **Herní test v UE Editoru (`Play`):**
   - Postava plynule přejde z přístupového úvozu ve valu (`u = 24,5 → 16,5 m`) kolem/po odsunutí `Brana_Zataras` po dřevěné lávce `Brana_Most` (`šířka 2,4 m, Z = 3040 cm`) přímo do průjezdu `Brana_V` (`Z = 3040 cm`) bez zadrhnutí o schod.
   - Po seskočení z lávky na dno příkopu (`Z = 2700 cm`) postava nevyběhne po skalní skarpě do hradu (`56° > 44°`), ale po severní únikové rampě (`d = -1,0 → -5,5 m`, `25,1° < 44°`) plynule vyjde z příkopu ven na severní svah šíje a vrátí se na cestu před valy.

## Otevřené otázky
- [x] Rozsah návrhu (Varianta 1: příkop + valy + přemostění + zátaras vs. Varianta 2: jen terén), způsob realizace v terénu (Varianta B: úprava heightmapy PNG se zasypáním starého příkopu + záloha A skriptem) a průchodnost příkopu (úniková cesta ven proti uvíznutí hráče, suť později) — Architect, 2026-11-23 → **Rozhodnuto (GameDesigner, 2026-11-23):** Schválena Varianta 1 (kompletní návrh hlavního příkopu u brány), pro terén Varianta B se zasypáním starého příkopu v PNG (při problému Varianta A pomocným skriptem) a povinná cesta ven z příkopu proti uvíznutí hráče (suť se dořeší po vizuální kontrole tvaru).
