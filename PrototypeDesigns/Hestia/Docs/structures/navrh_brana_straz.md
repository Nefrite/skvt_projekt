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

**Návrh neseděl na dnešní data.** Od 14. 11. se polohy zdí brány převzaly z levelu. Změřeno 16. 11. 2026 (terén z levelu):

| | Návrh (kap. 2) | Skutečnost |
|---|---|---|
| koruna `Brana_V` nad obloukem | Z 3423–3493 | Z 3617–3654 |
| vrch východního oblouku | pod Z 3423 | Z 3529 |
| koruna `Brana_J` | Z 3408–3474 | Z 3455–3549 |
| koruna `Brana_S` | Z 3321–3386 | Z 3459–3552 |
| navržený vrch podesty | Z 3522 | pod vrchem východního oblouku |

**Rozhodnutí Jirky (16. 11. 2026):**

- **Trámy jdou na východě do kapes v `Brana_V`** (úprava 03, kap. 3 tím neplatí), na západě leží na vyrovnané koruně `Brana_J`. Východní zeď vyčnívá 0,4–0,7 m nad podestu jako kamenné předprsí; kůly východního krytu na ní budou kratší.
- **Etapy:** stanoviště je v etapě 1 rozestavěné. Sady: podesta (kámen, trámy, prkna) a východní kryt `base` (potvrzeno 16. 11. 2026); severní a jižní kryt `final` (návrh architekta, Jirka nepotvrdil), přístřešek návrh `final`.
- **Zábradlí směrem do hradu se nestaví** (16. 11. 2026, kap. 4.3 neplatí): na západní nebo jižní straně bude výlez na podestu. Kód zábradlí v typu `platform` zůstává, v datech žádné není (`B_RAILS = False`).

**Kroky 1 až 3 hotové (podesta a všechny tři kryty; ve skriptech). V UE Jirka viděl podestu a východní kryt (16. 11. 2026) a zadal úpravy, které jsou tu už zapracované; nový stav v UE neověřen.**

| Část | Provedení | Sada |
|---|---|---|
| 03: kapsy v `Brana_V` | 3 kapsy 32 × 33 cm ve vnitřním líci, spodek Z 3552 (řada 3552–3585 nad obloukem) | – |
| 03: SV nároží `Brana_V` | kameny koruny nad Z 3618 v d < 0,75 posádka rozebrala (`cap`), kryt jde přes nároží bez mezery | – |
| `Brana_Straz_Kamen` (`stone_fill`) | vyrovnání koruny `Brana_J` na Z 3552 (pás u = 0,2–0,65; d = 0,9–5,3; výška 0–1,0 m), vyrovnání koruny `Brana_S` pod trámem na zdi (pás d = −0,45 až 0,05) a podložení trámů v líci `Brana_V` | `base` |
| `Brana_Straz_Podesta` (typ `platform`) | **3 trámy** z loupané kulatiny Ø 24 cm, d = 1,3 / 3,15 / 5,0; u = 0,1–6,63 (na východě 0,33 m v kapse); spodek Z 3552; **čtvrtý trám leží na koruně `Brana_S`** (d = −0,2; u = 0,1–6,2) | `base` |
| | podlaha z prken 5 cm, u = 0,2–6,27, **d = −0,55 až 5,25** (na severu až nad `Brana_S` k severnímu krytu; prkna ze dvou kusů se spárou nad trámem); **vrch Z 3581** (4,5 m nad plošinou hradu, 5,4 m nad zemí v průjezdu) | `base` |
| `Brana_Straz_Kryty` (typ `palisade`), východní | 30 kůlů s kůrou Ø 18–22 cm se špičkou nahoru na koruně `Brana_V` (u = 7,5; d = −0,6 až 5,35); vrch 1,8 m nad podlahou; 3 průzory 14 × 45 cm (d = 1,5 / 3,1 / 4,6; spodek 1,35 m), kůl v průzoru je rovně seříznutý | `base` |
| severní | 37 kůlů **u vnější hrany `Brana_S`** (d = −0,75; u = 0–7,6; za krytem se nedá stoupnout), vrch 1,25 m nad podlahou (střílí se přes vrch), 3 průzory 14 × 35 cm (u = 1,8 / 3,7 / 5,6; spodek 0,9 m) | `final` |
| jižní | 23 kůlů na jižním okraji podesty (d = 5,15; u = 2,6–7,38, tedy východní dvě třetiny, po `Hradba_V`); stojí na podlaze, na východě na koruně `Brana_V`; vrch 1,8 m, 2 průzory (u = 4,6 a 6,0) | `final` |

- **Ráhna** Ø 10 cm jsou zevnitř: jedno u spodu (východní a jižní kryt 0,55 m, severní 0,45 m nad podlahou) a druhé těsně pod průzory (1,22 m; u severního krytu 0,78 m). Přes průzory žádné nevede.
- **Kůly jsou „utopené“ 25 cm v koruně zdi** (posádka korunu vydlabala, aby lépe držely). Ve skriptech kůl do kamene jen zasahuje, kameny koruny se kvůli tomu v 03 nemění.
- **Trámy:** 3 místo 6 (Jirka 16. 11. 2026), prkna 5 cm nesou na 1,85 m.
- Další odchylky od kap. 4: trámy Ø 24 místo 22; podesta končí na východě u líce zdi (ne na její koruně), plocha 6,1 × 5,8 m; jižní kryt stojí na podlaze v d = 5,15 (návrh: práh z kulatiny v d = 5,35) a je delší (návrh u = 4,3–7,5); `Hradba_V` má korunu v Z 3237, podestu tedy nekryje.
- Východní kryt stojí 1,2 m za okrajem podlahy na koruně zdi, která je 0,3–0,7 m nad podlahou: stráž k němu vystoupí na korunu.
- Rozměry: `tools/ruin/brana_spec.py` (výšky absolutně v UE cm). Kontrola: `run_checks.py --only brana`. Náhled: `preview3d.py brana <out.png> [--stage 1|2]`, `05_constructions/Stavby_brana_straz_nahled.png` a `Stavby_brana_straz_nahled_etapa1.png`.
- V UE: `05_constructions/stavby/Brana_Straz.py` s `RUIN = True` (přestaví část `Obvod` kvůli kapsám a nároží, dlouhé), příště stačí `RUIN = False`.

**Zbývá:** přístřešek z kůry (`bark_roof`; nový návrh a instrukce pro stavitele: [[predani_brana_straz_striska_stavitel]], nahrazuje kap. 4.4), zátaras, staveniště pro etapu 1, výstup na podestu (určí Jirka; západní třetina jižní strany a západní strana jsou volné).

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
