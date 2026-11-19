---
# orchestrace
type: design
validity: valid
updated: 2026-11-16
# hra
status: in_progress
domain: structures
depth: 3
entity: "[[Brana_Straz]]"
build_step: 05_constructions
---
# Návrh: Brana_Straz – strážní podesta nad oblouky východní brány

Specifikace od architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **rozestavěno, viz kap. 0** (podesta je ve skriptech, kryty a přístřešek ne). Náčrt: [[navrh_brana_straz.png]] (schéma, ne přesný model).

**Připravenost (15. 11. 2026)** – podrobně [[CHECKLIST_assets_navrhy]]:
- **Hotové dílce:** loupaná kulatina `SM_RuinLog` (trámy podesty Ø 22), kůly se špičkou `SM_RuinStake` (kryty), tyče s kůrou `SM_RuinPoleBark` (ráhna, zábradlí, krokvičky, přítlačné tyče), kulatina s kůrou `SM_RuinLogBark` (sloupky, vaznice, kmen jezdce), loupané kůly `SM_RuinStakeSmall` (ramena jezdce), pásy kůry `SM_RuinBarkStrip`, ovázání `SM_RuinLashing`, prkna `SM_RuinPlank`. Materiál kůry `MI_RuinBark` už existuje.
- **Chybí:** typy staveb `palisade` a `bark_roof`, trámy na koruně (rozšíření `tower_floor`), `tools/ruin/brana_spec.py`, složení španělského jezdce do jednoho actoru. Otevřený zůstává výstup na podestu a etapa (kap. 9).

## 0. Stav stavby (16. 11. 2026, platí přednostně před kap. 2–7)

Přesunuto do [[stav_brana_straz]] (stav stavby, odchylky od návrhu a rozhodnutí Jirky 16. 11. 2026).

## 1. Zadání

- **Odkud:** Jirka (14. 11. 2026). Navazuje na otevřený bod ve stavovém dokumentu: provizorní hlídková konstrukce na `Brana_S`.
- **Herní účel:** stanoviště stráže nad východní bránou, kryté od východu, severu a zčásti od jihu.
- **Požadavky:**
  - dřevěná podesta z kulatiny a prken nad oblouky obou bran;
  - kryty z kulatiny od východu, od severu a od jihu (jižní jen po linii hradby);
  - severní kryt bez průzorů, jen tak vysoký, aby se přes něj dalo střílet z luku;
  - přístřešek z kůry (při stavbě obydlí je jí dost);
  - před bránou zátaras, který vypadá přenosně.
- **Neřeší se:**
  - **výstup na podestu** (schody nebo žebřík). Jirka ho umístí sám, až bude podesta stát;
  - příkop a most před bránou. Zátaras se pak posune.

## 2. Výchozí stav (spočítáno z dat, 11/2026)

**Souřadnice brány:** počátek v SZ rohu strážní věže (bod C, UE 1930 / −3107). `u` v metrech podél `Brana_S` k východu, jednotkový vektor v UE (0,9760; −0,2180). `d` v metrech kolmo k jihu, jednotkový vektor (0,2180; 0,9760). Výšky jsou **absolutně v UE cm (Z)**, protože terén v průjezdu v datech neodpovídá levelu (je v něm ještě starý příkop).

| Zeď | Osa | Tloušťka | Koruna (Z) | Otvor |
|---|---|---|---|---|
| `Brana_J` (západní) | u = 0; d = 0–7,32 | 1,8 m | d < 0,5: 3348–3374; d 1–6: 3408–3474; d > 6,5: klesá k zemi | portál 2,8 × 3,8 m, d = 2,1–4,9 |
| `Brana_V` (východní) | u = 7,2; d = 0–6,6 | 1,8 m | d < 0,6: 3531–3571; d 1,1–5,1: 3423–3493 (nad obloukem 3423–3455); d > 5,6: 3322 a níž | brána 3,2 × 4,5 m, d = 1,5–4,7 |
| `Brana_S` (severní) | d = 0; u = 0–7,2 | 1,8 m | 3321–3386, vyrovnaná | žádný |
| `Brana_Jih` (jižní) | od (0; 7,32) do (7,2; 6,6) | 1,8 m | zřícená k zemi, stojí jen pahýl u JZ rohu (3280–3379) | |

- Vnitřek věže: u = 0,9–6,3 (5,4 m), d = 0,9 až asi 5,8.
- `Hradba_V` se napojuje na jižní zeď v u = 3,0 a vede k jihu. Její východní líc je v u = 4,3. Východně od něj je jižní strana brány otevřená ven.
- `Hradba_Z_S` končí v SZ rohu (bod C), přichází od západu.
- Práh východní brány je asi v Z 2920, práh západního portálu asi v Z 3020 (odhad z výšek oblouků). Plošina hradu je v Z 3129.

## 3. Úpravy 03 (zřícenina)

**Ne.** `Brana_S` je už vyrovnaná do výšky oblouků. Vyrovnání korun pod trámy je dostavba 05.

## 4. Cílová struktura

### 4.1 Podesta

| Prvek | Průřez | Počet / délka | Poloha | Na čem leží |
|---|---|---|---|---|
| Vyrovnávací řada | kámen z rozvalin, šířka 0,45 m | 2 pásy po 4,4 m | na vnitřní polovině korun `Brana_J` (u = 0,2–0,65) a `Brana_V` (u = 6,55–7,0), d = 0,9–5,3 | na koruně, kopíruje ji; vrch v Z 3495 (výška 0–0,7 m) |
| Trámy | kulatina Ø 22 cm | 6 ks, délka 7,6 m | rovnoběžně s `Brana_S`, d = 1,1 / 1,9 / 2,7 / 3,5 / 4,3 / 5,1; u = −0,2 až 7,4 | na obou vyrovnávacích řadách, spodek Z 3495, uložení 0,45 m na každé straně |
| Podlaha | prkna 5 cm, šířka 22–32 cm | kladená kolmo na trámy | u = 0,2–7,0; d = 0,9–5,3 | na trámech, vrch **Z 3522** |

- **Rozpětí trámů** je 5,4 m mezi vnitřními líci zdí, bez podpory uprostřed.
- **Výška:** vrch podesty je asi 6,0 m nad prahem východní brány a 3,9 m nad plošinou hradu. Světlá výška průjezdu pod trámy je asi 5,7 m, u západního portálu 4,7 m.
- **Plocha:** 6,8 × 4,4 m.
- **Jižní okraj je v d = 5,3.** Dál k jihu už koruna `Brana_V` klesá a trám by neměl kde ležet. Oba oblouky (do d = 4,9) jsou zakryté.
- **Otvor pro výstup v podlaze není.** Doplní se, až bude určený výstup.

### 4.2 Kryty z kulatiny

Kůly Ø 18–22 cm nastojato, těsně vedle sebe, nahoře zašpičatělé. Drží je dvě vodorovné ráhna (Ø 10 cm) přivázaná zevnitř.

| Kryt | Kde | Na čem stojí | Vrch | Délka kůlů | Průzory |
|---|---|---|---|---|---|
| Východní | u = 7,5; d = −0,6 až 5,35 | na koruně `Brana_V`, 0,3 m východně od osy | Z 3702 (1,8 m nad podestou) | 1,3–2,8 m podle koruny | 3 ks v d ≈ 1,5 / 3,1 / 4,6: mezera 12 × 45 cm, spodek 1,35 m nad podestou |
| Severní | d = 0,75; u = 0,2–7,5 | na vnitřním okraji koruny `Brana_S` | Z 3647 (1,25 m nad podestou) | 2,6–3,0 m | žádné |
| Jižní | d = 5,35; u = 4,3–7,5 | na okraji podesty (práh z kulatiny na koncích trámů) | Z 3702 (1,8 m nad podestou) | 1,8 m | 1 ks uprostřed |

- **Severní kryt** je prsní výšky: přes vrch se střílí z luku. Pod úrovní podesty zakrývá mezeru mezi podestou a korunou `Brana_S`.
- **Jižní kryt** končí na linii východního líce `Hradba_V`. Západně od ní je podesta krytá hradbou.
- Na severním konci `Brana_V` (d < 0,6) je koruna výš než podesta, kůly tam vyjdou nejkratší.

### 4.3 Zábradlí

- **Jižní strana:** d = 5,3; u = 0,2–4,3.
- **Západní strana:** u = 0,2; d = 0,9–5,3.
- Sloupky Ø 10 cm po 1,5 m, dvě vodorovné tyče Ø 8 cm, vrch 1,0 m nad podestou.

### 4.4 Přístřešek z kůry

**Nahrazeno kap. 11** (16. 11. 2026).

- **Kde:** severovýchodní kout, u = 4,2–7,9; d = 0,9–4,0 (3,3 × 3,1 m plus přesah 0,4 m za východní kryt).
- **Nosná kostra:** na západě 2 sloupky Ø 14 cm (u = 4,2; d = 1,0 a 3,9) s vaznicí Ø 12 cm, vrch 3,25 m nad podestou. Na východě leží krokvičky na horním ráhnu východního krytu, 1,9 m nad podestou.
- **Krokvičky:** 7 tyčí Ø 8 cm po 0,5 m, délka 4,1 m.
- **Sklon:** 22° k východu. Voda padá přes východní kryt ven před bránu.
- **Krytina:** pásy smrkové kůry asi 0,7 × 1,6 m ve 3 řadách s přesahem 0,2 m, hrubou stranou nahoru. Zatížené 3 přítlačnými tyčemi Ø 6 cm přivázanými ke krokvičkám.
- Na severu je mezi krytem (1,25 m) a střechou volný pruh pro střelbu.

### 4.5 Zátaras

- **Typ:** španělský jezdec. Kulatina Ø 18 cm, délka 3,4 m, v ní 4 páry zkřížených kůlů Ø 7 cm × 1,6 m, na koncích zašpičatělé.
- **Kde:** před vnějším lícem `Brana_V`, střed u = 9,1; d = 3,1, rovnoběžně se zdí. Zakrývá celou šířku brány.
- **Chování:** jen vypadá přenosně, nehýbe se. Je to samostatný actor (`loose`), Jirka ho posune ručně, až bude řešit příkop a most.

### 4.6 Úprava dřeva

- Kulatina, kůly, tyče a prkna: čerstvé dřevo. Trámy podesty a ramena jezdce loupané, kůly krytů, ráhna, zábradlí, kostra přístřešku a kmen jezdce s kůrou (přiřazení podle [[CHECKLIST_assets_navrhy]] kap. 2.1, čeká na potvrzení). Prkna `raw`.
- Kůra: materiál `MI_RuinBark` (tmavě hnědá, hrubá).

## 5. Dostavba 05

| Stavba | Typ | Obsah |
|---|---|---|
| `Brana_Straz_Kamen` | existující `stone_addon` | vyrovnávací řady na korunách `Brana_J` a `Brana_V` |
| `Brana_Straz_Podesta` | nový, nebo rozšíření `tower_floor` (trámy na koruně místo v kapsách) | trámy, prkna, zábradlí |
| `Brana_Straz_Kryty` | **nový** (pracovně `palisade`) | tři kryty, ráhna, průzory |
| `Brana_Straz_Pristresek` | **nový** (pracovně `bark_roof`) | sloupky, vaznice, krokvičky, kůra, přítlačné tyče |
| `Brana_Zataras` | samostatný actor | španělský jezdec |

- **Složka:** `Stavby/Brana`.
- **Sdílené rozměry:** nový `tools/ruin/brana_spec.py` (souřadnice brány, polohy trámů, výška podesty, výšky krytů, rozsah přístřešku).
- **Výšky se počítají při buildu** z postavené zříceniny: vyrovnávací řada a paty kůlů kopírují skutečnou korunu. Čísla Z v tomto dokumentu jsou z dat bez ručních úprav.
- **Ruční doladění (`loose`):** zátaras.

## 6. Vazby, kolize, pořadí

- Trámy nesmí zasahovat do kamenů oblouků. Spodek trámů (Z 3495) je nad nejvyšším kamenem koruny v místě uložení.
- Průjezd pod podestou zůstává volný v celé šířce obou bran.
- Východní kryt stojí na koruně, ne na podestě. Jeho paty musí být uvnitř půdorysu koruny `Brana_V`.
- Prvky zříceniny `kapsa_most` a `retezy` na `Brana_V` zůstávají beze změny.
- **Pořadí:** 03 `Obvod` (pokud se měnil) → `Brana_Straz_Kamen` → `Brana_Straz_Podesta` → `Brana_Straz_Kryty` → `Brana_Straz_Pristresek`. Zátaras kdykoli.

## 7. Ověření

- `tools/checks/run_checks.py`: žádné kameny bez podpory, žádný průnik trámů s oblouky a ostěním bran.
- Každý trám leží na obou vyrovnávacích řadách aspoň 0,4 m.
- Podesta je vodorovná, vrch v Z 3522 ± 2 cm.
- Každý kůl východního a severního krytu stojí na kameni koruny, žádný nevisí.
- Mezery mezi kůly jsou nejvýš 3 cm, mimo průzory.
- Severní kryt má vrch 1,25 m ± 5 cm nad podestou po celé délce.
- Jižní kryt končí v u = 4,3 ± 0,1 m a navazuje na něj zábradlí.
- Zábradlí je souvislé na celé západní straně a na jižní straně až ke krytu.
- Přístřešek má sklon 22° ± 2° a přesahuje východní kryt.
- Světlá výška pod přístřeškem je u východního krytu aspoň 1,85 m.
- Náhled: `tools/checks/preview3d.py` (od východu zpoza příkopu, z průjezdu vzhůru, z podesty k východu a k severu).

## 8. Varianty a zavržené možnosti

- **Trámy sever–jih z koruny `Brana_S`:** jižní zeď je zřícená, druhý konec by neměl oporu.
- **Podesta v úrovni koruny `Brana_S` (o 1,4 m níž):** trámy by procházely horní částí oblouků.
- **Severní kryt s průzory ve výšce 1,8 m:** Jirka zvolil prsní výšku pro střelbu přes vrch.
- **Přístřešek z plátna:** kůry je při stavbě obydlí dost a plátno je už na věži.
- **Schody 60° podél severní zdi v průjezdu:** zamítnuto, výstup bude jinde.

## 9. Předpoklady a otevřené otázky

- **Předpoklad (terén):** výšky od země jsou odhad, v datech je uvnitř brány starý příkop. Stavitel bere terén z levelu.
- **Předpoklad (rozpětí):** kulatina Ø 22 cm na 5,4 m bez podpory je na horní hranici pravidel (trám do 5–6 m). Při pochybnosti přidat sedmý trám nebo zvětšit průměr na 24 cm.
- **Otevřené (Jirka):** výstup na podestu. Až bude určený, doplní se otvor v podlaze nebo mezera v zábradlí.
- **Otevřené (Jirka):** příkop a most před bránou, poloha zátarasu.
- **Otázka pro game designera:** jižní strana brány je východně od `Hradba_V` zřícená k zemi. Dá se tudy bránu obejít?
- **Otázka (etapy hry):** stojí podesta už při prvním příchodu hráče, nebo se staví až později? Návrh popisuje hotový stav.
- **Životnost:** kůra vydrží dva až pět let, pro provizorium to stačí.

## 10. Náčrt slovy

- **Půdorys:** obdélník podesty 6,8 × 4,4 m vyplňuje severní dvě třetiny strážní věže. Šest trámů vede od západní zdi k východní, rovnoběžně se severní. Kryt tvoří písmeno U otevřené k západu: celá východní strana, celá severní strana a východní 3 m jižní strany. Zbytek jižní strany a celá západní mají zábradlí. Přístřešek je v severovýchodním koutě. Před východní bránou stojí zátaras.
- **Řez východ–západ:** trámy leží na korunách obou bran na vyrovnávací řadě kamene, nad nimi prkna. Na východní koruně stojí kůly do výšky 1,8 m nad podestou. Od nich stoupá střecha z kůry k západu na dva sloupky. V pozadí severní kryt: kůly stojí na nižší koruně severní zdi a končí 1,25 m nad podestou.
- **Pohled od východu:** nad obloukem brány řada zašpičatělých kůlů se třemi průzory, nad ní okraj kůrové střechy. Vpravo (na severu) nižší kryt, vlevo (na jihu) krátký kryt končící u hradby. Před bránou španělský jezdec.

## 11. Přístřešek z kůry – návrh 16. 11. 2026 (nahrazuje kap. 4.4)

Z předání [[predani_brana_straz_striska_stavitel]] (kap. 3 a 5); kap. 4.4 tím neplatí.

### 3. Návrh

Pultová stříška v severovýchodním koutě, spád 22° k východu. Voda stéká přes východní kryt ven před bránu. **Kostra je samostatná, o kryt se neopírá**: nahoře u krytu není ráhno (vedlo by přes průzory) a kůly mají špičky.

#### 3.1 Kostra

| Prvek | Průřez | Počet a délka | Poloha | Na čem stojí nebo leží |
|---|---|---|---|---|
| západní sloupky | kulatina s kůrou Ø 14 cm | 2 ks, 3,2 m | u = 4,0; d = 1,3 a 3,15 | na podlaze přesně nad trámy podesty |
| východní sloupky | kulatina s kůrou Ø 14 cm | 2 ks, asi 1,55 m | u = 7,15; d = 0,8 a 3,7 | na koruně `Brana_V` (pata kopíruje kámen), 0,35 m za kůly krytu |
| západní vaznice | tyč s kůrou Ø 12 cm | 1 ks, 3,4 m | u = 4,0; d = 0,3–3,7; vrch 3,32 m | na západních sloupcích |
| východní vaznice | tyč s kůrou Ø 12 cm | 1 ks, 3,6 m | u = 7,15; d = 0,3–3,9; vrch 2,05 m | na východních sloupcích |
| krokvičky | tyče s kůrou Ø 8 cm | 7 ks, 4,55 m | d = 0,5 až 3,5 po 0,5 m; u = 3,75–7,95 | na obou vaznicích, přivázané |
| příčné tyčky pod kůru | tyče s kůrou Ø 5 cm | 6 ks, 3,5 m | napříč krokvičkami po 0,8 m po spádu, d = 0,25–3,75 | na krokvičkách |
| vzpěrky | tyče s kůrou Ø 8 cm | 4 ks, 0,7 m | šikmo 45° od západních sloupků k vaznici (na obě strany podél d) | zavětrování |

- **Východní sloupky nesmí stát za průzory.** Průzory jsou v d = 1,5 a 3,1, sloupky v d = 0,8 a 3,7 (odstup 0,6 m).
- **Krokvičky jdou těsně nad špičkami kůlů:** spodek krokvičky je nad osou krytu (u = 7,5) v 1,91 m, nejvyšší špička v 1,84 m. Kdyby se v UE dotýkaly, zvedni obě vaznice o 5 cm.
- **Světlá výška** pod krokvičkami: u východního sloupku 2,05 m, u západní vaznice 3,2 m.
- **Přesahy:** na východě 0,45 m za osu krytu (okap), na západě 0,25 m za vaznici.
- **Spoje jsou vázané:** na každém styku krokvičky s vaznicí a vaznice se sloupkem ovázání `SM_RuinLashing`.

#### 3.2 Krytina

- **Pásy kůry** `SM_RuinBarkStrip` (jmenovitě 1,6 × 0,7 m), hrubou stranou nahoru, delší stranou po spádu.
- **3 řady po spádu** s přesahem 0,2 m: horní řada vždy překrývá spodní. Délku pásu dopočítej tak, aby tři řady pokryly celou délku krokviček (vychází asi 1,64 m).
- **V řadě 6 pásů** vedle sebe s bočním přesahem 0,1 m; sousední řady jsou posunuté o půl pásu.
- **Půdorys krytiny:** u = 3,7–8,0; d = 0,25–3,75 (4,3 × 3,5 m).
- **3 přítlačné tyče** Ø 6 cm s kůrou napříč (podél d), po jedné na každém přesahu řad a jedna u okapu, přivázané na koncích ke krajním krokvičkám.
- Pásy lehce náhodně natoč (do ± 3°) a posuň (do ± 3 cm), ať krytina nevypadá jako mřížka.

#### 3.3 Co zůstává volné

- Na severu je mezi vrchem severního krytu (1,25 m) a stříškou volný pruh na střelbu.
- Jižní část podesty (d > 3,9) a celá západní polovina zůstávají pod širým nebem; tam bude výlez.

### 5. Kontroly (doplň do `check_brana` v `tools/checks/run_checks.py`)

- sklon 22° ± 2°;
- západní sloupky stojí na podlaze nad trámem (d trámu ± 0,1 m), východní na kameni koruny;
- žádný sloupek blíž než 0,5 m (podél d) od průzoru východního krytu;
- každá krokvička leží na obou vaznicích;
- spodek krokviček je nad špičkami kůlů východního krytu aspoň o 1 cm;
- světlá výška u východního krytu aspoň 1,85 m;
- stříška se neprotíná s kůly a ráhny krytů (východního ani severního);
- kůra pokrývá půdorys krytiny aspoň z 99 %;
- všechny dílce mají sadu `final`;
- náhled: doplň do `brana_scene` v `preview3d.py` pohled pod stříšku od západu a pohled od východu zpoza brány.
