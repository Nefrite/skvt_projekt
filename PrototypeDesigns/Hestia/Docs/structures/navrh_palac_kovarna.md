---
# orchestrace
type: design
validity: valid
updated: 2026-11-22
# hra
status: in_progress
domain: structures
depth: 4
entity: ["[[Palac_Kovarna]]", "[[Palac_Kovarna_Vybaveni]]"]
build_step: 05_constructions
---
# Návrh: Palac_Kovarna – provizorní kovárna pod přístřeškem

## Souhrn
Platný návrh provizorní kovárny posádky pod pultovým přístřeškem ve východní místnosti paláce u věže (kap. 1). Text je platný, náčrt [[navrh_palac_kovarna.png]] je starší schéma a v rozměrech se liší. Stav: všechny kroky 1–4 hotové ve skriptech a ověřené mimo UE; v UE ověřená jen úprava 03, kostra přístřešku a výheň ([[stav_palac_kovarna]]).
- **Stavba:** pultová střecha spádem k západu, krytina z prken, stěna z proutí na západě, žlab a sud, výheň v koutě s dymníkem a komínem, vybavení jako samostatné actory (kap. 4).
- **Úpravy zříceniny (03):** `Palac_J` zanořená o řadu kamene, koruna u věže rozebraná, kapsa pro východní pozednici (kap. 3).
- **Odchylky od původního návrhu ze 14. 11. 2026 a odloženo** (žhavé uhlí, saze, oheň a kouř, podlaha z udusané hlíny): [[stav_palac_kovarna]].
- **Zavržené varianty:** kap. 8. **Rizika a předpoklady:** kap. 9 (kouř, zatékání po stěně věže, rozpětí krokví).

Specifikace od architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **vybraný návrh, staví se po krocích** (16. 11. 2026; hotové kroky 1–4, v UE ověřená kostra a výheň). Co je hotové a co zbývá, je v [[stav_palac_kovarna]]. Náčrt: [[navrh_palac_kovarna.png]] je starší schéma, které se v hlavním (výheň v koutě) shoduje, v rozměrech ne; **platí tento text**.

## 0. Stav stavby proti návrhu (16. 11. 2026)

Přesunuto do [[stav_palac_kovarna]] (co je hotové, odchylky a jejich důvody, připravenost assetů).

## 1. Zadání

- **Odkud:** Jirka (14. 11. 2026).
- **Herní účel:** provizorní kovárna posádky. Vyrábí základní spojovací materiál (hřebíky, skoby, kramle) a dělá základní opravy zbraní.
- **Požadavky:**
  - práce pod přístřeškem;
  - výheň, od které je teplo i v zimě;
  - brusný kotouč;
  - sud na chlazení a kalení;
  - zásoba dřeva.
- **Umístění:** východní místnost paláce u věže (potvrdil Jirka 15. 11. 2026). Obydlí je kvůli tomu v prostřední místnosti ([[navrh_palac_obydli_stred]]).

## 2. Výchozí stav (spočítáno z dat, 11/2026)

**Souřadnice paláce:** `s` v metrech podél `Palac_J` od jejího prvního bodu (UE −2350 / −50), `n` v metrech kolmo k severu. Jednotkové vektory v UE: `s` = (0,9758; −0,2184), `n` = (−0,2189; −0,9757). Výšky v metrech nad terénem (v datech rovina Z 3129).

Východní místnost má uvnitř 9,35 × 8,1 m (s = 21,4–30,75; n = 0,7–8,8).

| Strana | Zeď | Koruna | Otvory |
|---|---|---|---|
| jih | `Palac_J` (1,4 m) | po úpravě 03 (kap. 3): s 24–25,5: 4,4–4,8; s 26–28: 3,6–4,4; s 28,5–29,3: 5,2; s 29,5–31: 4,0–4,8 (původně 4,7–5,1 / 3,9–4,7 / 5,5–6,0 / 6,0–6,7) | střílny s výklenkem v s = 25 a 29 (výklenek 1,3 m široký, po zanoření 0,24–2,39 m nad zemí) |
| sever | `Palac_S` (1,4 m) | 0,7–1,3; u věže 2,0–2,7 | dveře s = 26,45–27,55, až k zemi |
| západ | `Palac_pricka_2` (osa s = 21,0) | podle návrhu domu srovnaná na 1,4 m, nad ní srub a štít domu | dveře zazděné |
| východ | věž `Vez_Z` (líc s = 30,75) | 9–13,5 | okno 1. patra věže: n = 5,05–5,95, výška 5,1–6,5 m |

- Terén v místnosti je v datech rovný.
- Východní štít domu je v s = 21,4. Jeho střecha je dehtovaná.

## 3. Úpravy 03 (zřícenina)

**Ano, vyžaduje úpravu 03** (rozhodl Jirka 15. 11. 2026). Přestavět část `Palac`. Rozměry jsou v `tools/ruin/palac_spec.py` → `ruin_edits`, do dat je zapisuje `tools/ruin/gen_layout.py`.

1. **Celá `Palac_J` je zanořená o jednu řadu kamene do země** (`z_offset: −0,31` v datech zdi, `J_SINK`).
   - Zeď se posouvá po ose Z jako celek, počet řad i tvar koruny zůstávají. 0,31 m je výška první celé řady nad terénem, takže spáry u země vypadají stejně jako před posunem.
   - Posouvá se všechno ve zdi: střílny, jejich výklenky (dno výklenku je teď 0,24 m nad zemí místo 0,55 m, vrch 2,39 m) i okna.
   - Týká se celé délky zdi, tedy i prostřední místnosti. **Koruny `Palac_J` v [[navrh_palac_obydli_stred]] (kap. 2 a 3) jsou proto o 0,31 m výš, než je skutečnost.**
2. **Rozebraná koruna u věže**, aby ji komín přesahoval: `breaches` `{s0: 29,6; s1: 33; floor: 6,1; slope_l: 0,8}` (`J_BREACH`). Je to rozpad, ne rovné zarovnání: koruna vychází ve stupních po řadách 5,2 m (s = 28,5–29,3), 4,8 m (od s = 29,5) a vnitřní líc u komína místy 4,0 m. Komín (5,5 m) ji v okruhu 1,5 m přesahuje o 0,3–1,5 m.
   - `protect` `{s0: 30,3; s1: 30,9; min: 4,95}` drží řadu kamene nad kapsou pozednice.
3. **Kapsa pro východní pozednici** ve vnitřním líci `Palac_J`: otvor `kapsa` v s = 30,55, šířka 0,26 m, hloubka = vnitřní líc (0,4 m). Kapsa se zarovnává na řady kamene: zabírá řadu 4,04–4,43 m nad terénem, pozednice v ní leží spodkem na spáře (proto má vrch 4,24 m, ne 4,2 m). Ostatní kameny zdi se kapsou nemění.
4. **`drop_rows`** (horní kameny každé vrstvy pryč, `zr_ruin/post.py` → `drop_top_rows`) vznikl při prvním pokusu o „řadu níž“. Pro `Palac_J` se nepoužívá (`J_DROP_ROWS = 0`), parametr zůstává v kódu pro jiné zdi.

## 4. Cílová struktura (podle postaveného stavu 16. 11. 2026)

Kovárna stojí v jihovýchodním koutě místnosti. Jižní stranu tvoří `Palac_J`, východní věž. Půdorys střechy: s = 24,95–30,75; n = 0,7–6,6 (asi 34 m², z toho 0,9 m je přesah za západní stěnu). Severní strana je otevřená, západní má lehkou stěnu. Výheň je přímo v koutě. Rozměry jsou v `tools/ruin/palac_spec.py` (konstanty `K_*`); čísla tady jsou z dat.

### 4.1 Přístřešek (pultová střecha, spád k západu)

| Prvek | Průřez | Počet / délka | Poloha | Na čem leží |
|---|---|---|---|---|
| Sloupy u věže | 20 × 20 cm | 2 ks, výška 3,9 m | s = 30,55; n = 4,4 (mezi měchy a brusem) / 6,2 | na plochém kameni 36 × 36 × 14 cm (vrch 10 cm nad terénem), 10 cm od líce věže. V koutě u `Palac_J` sloup není (stojí tam výheň). |
| Východní pozednice | 20 × 20 cm | 6,0 m (n = 0,4–6,4) | s = 30,55; vrch 4,24 m (spodek na spáře řad `Palac_J`) | jižní konec 0,3 m v kapse `Palac_J` (kap. 3), dál na sloupech; rozpětí 4,0 m a 1,8 m |
| Sloupy na západě | 18 × 18 cm | 3 ks, výška 2,2 m | s = 25,85; n = 0,9 / 3,55 / 6,2 (rovnoměrně) | na plochém kameni (jako u věže) |
| Západní pozednice | 18 × 18 cm | 5,66 m (n = 0,74–6,4) | s = 25,85; vrch 2,5 m | na sloupech |
| Krokve | loupaná kulatina Ø 16 cm | 7 ks, délka 6,1 m | n = 0,9 až 6,3 po 0,9 m; od s = 30,65 po s = 24,95 | obě pozednice (osedlání 3 cm), přesah 0,9 m na západ (kryje hranici dřeva u stěny) |
| Latě | 6 × 5 cm | 9 řad přes celou šířku | u horního konce krokví, u okapu, těsně nad a pod prostupem komína, mezi nimi nejvýš po 0,9 m | na krokvích |
| Prkna | 3,5 cm, šířka 22–30 cm, spára 1,5 cm | po spádu | od líce věže (mezera 0,5 cm) po okapovou hranu s = 24,85 (10 cm za konci krokví, nad osou žlabu); n = 0,735–6,6 | na latích; kolem prostupu komína se kladou od jeho okrajů ven |
| Lišty | 10 × 3,5 cm | přes každou spáru | po spádu, nahoře končí pod lemováním | na prknech |
| Lemování | prkno 3,5 × 25 cm na stojato | 2 ks | podél věže (horní okraj) a podél `Palac_J` (na hraně krajního prkna) | na krytině |

- **Sklon:** 20,3° k západu. Vysoká strana je u věže, aby nad výhní bylo co nejvíc místa a komín vycházel v nejvyšším bodě.
- **Krytina je bez dehtu** (`raw`), dehet je nad výhní hořlavý. Od líce `Palac_J` je 3,5 cm: kameny koruny v s = 27–29 leží v úrovni střechy a vystupují z líce o 1–3 cm.
- **Prostup komína:** otvor v krytině s mezerou 3 cm kolem komína, mezi krokvemi n = 0,9 a 1,8.
- **Výška pod krokvemi:** u věže 4,2 m, nad kovadlinou 3,3 m, u západní pozednice 2,5 m (spodek pozednice 2,3 m), na okapu 2,1 m. Vrch krytiny u věže 4,5 m.
- **Okno věže** (n = 5,05–5,95, parapet 5,1 m) je 0,6 m nad střechou. Je neprůchozí, slouží jen jako světlík do věže (Jirka 16. 11. 2026).

### 4.2 Stěny

| Strana | Řešení |
|---|---|
| Jižní | stojící `Palac_J`. Je všude vyšší než okraj střechy, bez dozdívky. |
| Východní | stojící věž. |
| Západní | stěna z proutí omazaná hlínou v linii západních sloupů: s = 25,85; n = 0,7–6,3; výška 2,1 m, tloušťka 8 cm. Dílce mezi sloupy, spodní pás 0,1 m mezi patními kameny, na spojích dílců kůly Ø 9 cm (6 cm nad stěnou). Nad ní volný pruh 0,22 m pod pozednicí. Na jihu dosedá na plný líc `Palac_J` těsně za výklenkem střílny s = 25. |
| Severní | otevřená. Vstup a světlo. |

- **Západní stěna** chrání oheň před převládajícím větrem a dům před jiskrami.
- **Na zimu** se dá severní strana zčásti zavřít prkny. Není součástí návrhu.

### 4.3 Výheň, měchy a komín

| Prvek | Rozměr | Poloha |
|---|---|---|
| Výheň | kamenný stůl 1,2 × 1,0 m, výška 0,75 m (3 řady po 25 cm), z kamene rozvalin, nahoře vymazaný hlínou (4 cm); ohniště 0,4 × 0,4 m pod komínem (střed s = 30,0; n = 1,35) s dřevěným uhlím | **v koutě** mezi `Palac_J` a věží: s = 29,75–30,73; n = 0,72–1,9 (2 cm od obou líců); západně hned vedle je výklenek střílny s = 29 |
| Boční zídka | kámen, 0,3 × 1,0 m, výška 1,2 m (5 řad), stojí na zemi | severně od stolu, n = 1,9–2,2; chrání měchy před žárem; otvor pro výfučnu 0,2 m v ose ohniště, ve výšce 0,72–0,96 m |
| Měchy | `SM_RuinBellows` 2,1 × 0,85 m na rámu ve výšce 0,9 m | podél věže severně od zídky: s = 29,57–30,43; n = 2,0–4,05; výfučna (0,91 m) v otvoru zídky |
| Páka měchů | loupaná tyč Ø 6 cm, 2,3 m | od madla měchů (s = 30,0; n = 3,95; 1,75 m) ke kovadlině (28,55; 2,2; 1,6 m); visí na laně z krokve n = 2,7, s madlem měchů spojená lanem |
| Dymník | proutěný koš vymazaný hlínou, 1,4 (podél s) × 1,2 m, spodní okraj 1,9 m (17. 11. 2026 zvednuto z 1,8 m, postava se zasekávala), výška 1,0 m | nad výhní, střed v ose komína, východní okraj u stěny věže; visí na 4 závěsných tyčích Ø 5 cm |
| Výměny | loupaná kulatina Ø 10 cm, 2 ks | mezi krokvemi n = 0,9 a 1,8, 3 cm východně a západně od komína; nesou závěsné tyče dymníku a drží komín |
| Komín | 0,5 × 0,5 m, proutí s hlínou | nad ohništěm, střed s = 30,0; n = 1,35; prochází střechou mezi krokvemi n = 0,9 a 1,8 (vůle 12 cm) a 20 cm od východní pozednice; vrch 5,5 m (1,1 m nad krytinou na horní hraně prostupu) |

- Komín je 0,4 m od líce `Palac_J`. Její koruna je u něj rozebraná na 4,0–4,8 m (kap. 3), komín ji v okruhu 1,5 m přesahuje aspoň o 0,3 m; dál na západ (s = 28,5–29,3) je 5,2 m.
- Stěna věže a `Palac_J` za výhní jsou kamenné, bez úpravy. Dymník (n = 0,75–1,95) je 5 cm od líce `Palac_J`.

### 4.4 Vybavení (`06_furnishing`, skupina `Palac_Kovarna_Vybaveni`, samostatné actory)

| Prvek | Rozměr | Poloha (s; n) |
|---|---|---|
| Kovadlina na špalku | špalek Ø 0,5 m, vrch kovadliny 0,75 m, roh k severu | 28,0; 1,4 (1,5 m před výhní, Jirka 16. 11. 2026) |
| Kalicí sud | Ø 0,6 m, výška 0,8 m, s vodou | 28,3; 2,6 (1,2 m od kovadliny, 1,6 m od výhně) |
| Hřebovnice | na menším špalku (Ø 0,35 m, výška 0,55 m) | 27,35; 1,75 |
| Brus | šlapací (rozhodl Jirka 14. 11. 2026): pískovcový kotouč Ø 0,7 m na rámu 1,2 × 0,6 m, korýtko s vodou, šlapadlo k severu; třínohá stolička | rám 27,0–28,2; 5,1–5,7; stolička 27,3; 6,2 (u otevřené strany kvůli světlu) |
| Ponk se svěrákem | 2,2 × 0,7 m, výška 0,85 m, svěrák do místnosti | u západní stěny: 26,05–26,75; 2,6–4,8 |
| Nářadí | 2× kleště, 2× kladivo, 2× sekáč, zavěšené na liště 1,8 × 0,1 m | lišta na jižní zdi s = 26,2–28,0, střed 1,5 m, na dvou kolících ve spárách |
| Železné pruty | svazek 1 m, opřený o zeď (75°) | 27,15; u jižní zdi |
| Truhlík na dřevěné uhlí | 0,8 × 1,2 m, výška 0,8 m, volné víko posunuté k severu (pootevřený) | 26,05–26,85; 0,8–2,0 |
| Koš na hřebíky | Ø 0,44 m | 26,45; 6,0 |
| Zásoba dřeva | kůl s kůrou Ø 10 cm (1,5 m nad zemí) a tři hranice 0,65 × 1,4 m, výška 1,25–1,36 m | **zvenku** pod přesahem střechy: kůl v n = 2,2 (1,5 m od `Palac_J`, průchod ke střílně s = 25), hranice s = 25,0–25,65; n = 2,26–6,4 (Jirka 16. 11. 2026) |

- **Kovadlina, sud a výheň** jsou na pár kroků od sebe, kovadlina dost daleko od výhně na práci kolem ní.
- **Výklenek střílny s = 29 zůstává volný** (manipulační prostor u výhně).
- **Výheň je v nejtmavším koutě.** Kovář potřebuje šero, aby poznal barvu rozžhaveného železa. Brus a ponk jsou naopak u světla.
- **Průchody:** od severu mezi brusem a měchy 1,7 m, k ponku mezi kalicím sudem a brusem 2,1 m.
- **Podlaha:** udusaná hlína (odloženo, chybí materiál).
- **Suť** je v celé východní místnosti uklizená.

### 4.5 Okap (`Palac_Kovarna_Okap`)

- **Žlab:** loupaný vydlabaný kmen Ø 20 cm pod okapovou hranou krytiny, s = 24,8; n = 0,72–6,8; spád 2,5 % k severu (15 cm). Vrch 12 cm pod krytinou na jižním konci, 27 cm na severním.
- **Rozsochy:** 3 kůly s kůrou Ø 12 cm s hlavou vidlice, rovnoměrně v n = 1,7 / 4,0 / 6,3. Jižní je 1 m od líce `Palac_J` (průchod ke střílně s = 25), žlab k hradbě volně přesahuje (Jirka 16. 11. 2026).
- **Sud:** na dešťovou vodu pod severním koncem žlabu (s = 24,8; n = 6,8), samostatný actor. Voda se hodí pro kalicí sud a korýtko brusu.
- **Svod se nedělá** (rozhodl Jirka 15. 11. 2026). Cisterna se neřeší.

### 4.6 Úprava dřeva

- Všechno dřevo `raw`. Žádný dehet. Krokve, výměny, páka a kůly stěny jsou loupaná kulatina, rozsochy a kůl u dřeva s kůrou.

## 5. Dostavba 05

| Stavba | Typ (`05_constructions/zr_stavby/`) | Obsah |
|---|---|---|
| `Palac_Kovarna_Pristresek` | `pult_roof` (`pult.py`, i pro `Palac_Obydli_Krov`) | sloupy na patních kamenech, pozednice, krokve, krytina, lemování |
| `Palac_Kovarna_Vyhen` | `hearth` (`ohniste.py`, i pro `Palac_Obydli_Ohniste`) | výheň, zídka, dymník, komín, výměny a závěsné tyče |
| `Palac_Kovarna_Stena` | `wattle_wall` (`stena.py`) | západní stěna z proutí a hlíny, kůly |
| `Palac_Kovarna_Okap` | `gutter` (`okap.py`, i pro `Palac_Obydli_Okap`) | žlab, rozsochy, sud (samostatný actor) |
| `Palac_Kovarna_Kul` | `props` (`vybaveni.py`) | pevný kůl u hranice dřeva |

**Vybavení** (`06_furnishing`, skupina `Palac_Kovarna_Vybaveni`, typ `props`): všechno přenosné (kap. 4.4) jako samostatné actory. Úklid suti v celé místnosti: `clear_poly` u `Palac_Kovarna_Pristresek`.

- **Spouštění v UE:** celá kovárna `05_constructions/stavby/Palac_Kovarna.py` (přepínače `KRYTINA`, `RUIN` = i část zříceniny `Palac`, `SUT`), jednotlivé stavby `Palac_Kovarna_<Část>.py`.
- **Složka:** `Stavby/Palac`, vybavení `Stavby/Palac/Kovarna_Vybaveni`.
- **Sdílené rozměry:** `tools/ruin/palac_spec.py` (společně s domem); čte ho 03 (`gen_layout.py`: zanoření `Palac_J`, kapsa, rozebraná koruna) i 05 (`gen_constructions.py` → `palac`). Polohy vybavení: `palac_spec.kovarna_vybaveni()`.
- **Vybavení nejsou generované dílce.** Jsou to vlastní props ve stylu hradu (rozhodl Jirka 14. 11. 2026), generátor je jen rozmístí. Jsou v `06_furnishing` (od 16. 11. 2026, vše přenosné odděleně od staveb). Ruční doladění se ukládá skriptem `06_furnishing/vybaveni/Palac_Kovarna.py` (`capture`, výpis `list`, zahození `reset`).

## 6. Vazby, kolize, pořadí

- **Odstup od domu:** výheň je 8,3 m od východního štítu domu, západní okraj přístřešku (okap) 3,55 m. Podmínka z návrhu domu (výheň aspoň 6 m) je splněná.
- **Dvorek před kovárnou** je mezi střechou (n = 6,6) a `Palac_S` (n = 8,8) široký 2,2 m. **Vstup:** původními dveřmi paláce (s = 26,45–27,55) na dvorek a odtud otevřenou severní stranou. Od 16. 11. 2026 i ze zápraží domu hrubým průchodem v `Palac_pricka_2` (n = 6,9–8,5; [[navrh_palac_obydli_stred]] kap. 0.2a), který ústí na západní konec dvorku (s = 21,4).
- **Výheň** (s od 29,75) nezasahuje do výklenku střílny s = 29 (ten končí v s = 29,65).
- **Západní linie** (s = 25,85) je 0,2 m východně od výklenku střílny s = 25; výklenek je přístupný ze dvorku podél `Palac_J` (volno 1 m k rozsoše, 1,45 m ke dřevu).
- **Sud pod žlabem** stojí u severozápadního rohu přístřešku, mimo cestu ode dveří.
- **Pořadí stavby:** 03 část `Palac` (zanoření `Palac_J`, kapsa) → `Palac_Kovarna_Pristresek` → `Palac_Kovarna_Vyhen` (výměny berou výšku z krokví) → `Palac_Kovarna_Stena`, `Palac_Kovarna_Okap` (žlab bere výšku z krytiny), `Palac_Kovarna_Kul` → `Sut` → vybavení 06 (lano páky bere výšku z krokve). Totéž dělá `Palac_Kovarna.py`.

## 7. Ověření

`tools/checks/run_checks.py --only palac` hlídá (16. 11. 2026):

- průniky dřeva, krytiny, stěny, okapu a vybavení se zříceninou a mezi sebou (mimo záměrná uložení: kapsa, kolíky lišty, výfučna v otvoru zídky, lano kolem krokve);
- každý sloup na patním kameni, každá krokev na obou pozednicích, východní pozednice aspoň 20 cm v kapse `Palac_J`;
- sklon 20° ± 1°; světlá výška nad kovadlinou aspoň 3,0 m, spodek krokví u okapu aspoň 2,0 m;
- krytina pokrývá aspoň 99 % půdorysu mimo prostup komína; lemování leží na krytině;
- komín: vůle aspoň 10 cm od krokví a pozednic, aspoň 0,8 m nad krytinou, přesah koruny `Palac_J` aspoň 0,3 m; dymník kryje ohniště; výměny v krokvích;
- stěna: výška, zaplnění linie mezi sloupy;
- okap: okapová hrana nad žlabem, spád k severu, konec nad sudem, sud na zemi;
- vybavení: výfučna v otvoru zídky, kovadlina 1,4–1,6 m před výhní, kalicí sud nejvýš 1,7 m od kovadliny i výhně, průchody aspoň 1,2 m, dřevo pod přesahem a aspoň 1,4 m od `Palac_J`, žádná suť v místnosti.

Náhled: `tools/checks/preview3d.py kovarna <out.png>` (8 pohledů), uložený v `05_constructions/Stavby_palac_kovarna_nahled.png`.

## 8. Varianty a zavržené možnosti

- **Spád střechy k severu (jako u domu):** styk s věží by byl po celé délce nad výhní a měchy, zatékalo by na ně.
- **Volně stojící přístřešek uprostřed místnosti:** výheň by neměla kamennou stěnu za zády a kouř by šel pod střechu.
- **Krytina z kůry:** kůry je dost, ale nad výhní je suchá kůra nejhořlavější možnost. Dá se použít jen na západní polovině střechy dál od komína.
- **Kovárna mimo palác (u hradby, na nádvoří):** dál od skladu ve věži a bez dvou hotových kamenných stěn.

## 9. Předpoklady a otevřené otázky

- **Umístění:** východní místnost paláce, potvrzeno 15. 11. 2026.
- **Předpoklad (etapy):** kovárna stojí hotová už v etapě 1. Dům potřebuje hřebíky a kramle, takže kovárna musí být dřív.
- **Předpoklad (palivo):** výheň topí dřevěným uhlím. Zásoba dřeva v kovárně slouží na podpal a na pálení uhlí. Malý milíř nebo jáma na uhlí by byla někde mimo hrad, návrh ji neřeší.
- **Předpoklad (voda):** do sudu a korýtka brusu se nosí z potoka.
- **Okno věže nad střechou:** neprůchozí světlík do věže, cesta postavy na střechu to není (Jirka 16. 11. 2026).
- **Riziko (kouř):** komín je v koutě pod stěnou věže vysokou 9–13,5 m. Jižní zeď přesahuje (kap. 3), věž ne. Tah bude slabší a kouř půjde po stěně věže k hlídce nahoře. Kove se ale ve dne a s přestávkami.
- **Riziko (střílna u výhně):** po zanoření zdi je průzor střílny s = 29 ve výšce 1,29–2,39 m a dno výklenku 0,24 m nad zemí. Jako odkladiště u výhně to vyhovuje, pro střelbu je průzor nízko.
- **Riziko (zatékání):** po stěně věže stéká při dešti voda na horní okraj střechy. U otevřeného přístřešku to vadí méně než u domu, ale měchy jsou právě tam.
- **Riziko (rozpětí):** krokve Ø 16 cm na 4,7 m bez střední podpory a s přesahem 0,9 m. Pro lehkou krytinu to stačí, při pochybnosti přidat střední vaznici na dvou sloupech.
- **Neřeší se:** zimní zavření severní strany, milíř, cisterna.

## 10. Náčrt slovy

- **Půdorys:** obdélník 4,9 × 5,9 m v koutě mezi jižní zdí paláce a věží, střecha přesahuje 0,9 m za západní stěnu. Výheň je přímo v koutě, severně od ní zídka a měchy podél věže. Půldruhého metru před výhní stojí kovadlina (před výklenkem střílny), mezi nimi kalicí sud. U západní stěny truhlík s uhlím a ponk, zvenku pod přesahem hranice dřeva od kůlu k sudu pod žlabem. Brus je u otevřené severní strany. Před přístřeškem je dvorek, do kterého se vchází původními dveřmi paláce.
- **Řez východ–západ:** u věže pozednice ve 4,24 m (jižním koncem v kapse `Palac_J`, dál na dvou sloupech), krokve klesají 20° k západu na pozednici ve 2,5 m a přesahují ji o 0,9 m. V koutě stoupá komín nad střechu do 5,5 m a přesahuje rozebranou korunu jižní zdi. Pod ním dymník na závěsných tyčích a kamenný stůl výhně. Na západě stěna z proutí a hlíny do 2,1 m, pod okapem žlab a u jeho severního konce sud.
- **Pohled ze dvorku:** otevřená strana přístřešku, vpředu brus, vlevo podél věže měchy a za nimi temný kout s výhní, vzadu jižní zeď s nářadím a výklenkem střílny, vpravo ponk u proutěné stěny.
