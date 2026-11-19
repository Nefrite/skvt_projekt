---
# orchestrace
type: design
validity: valid
updated: 2026-11-16
# hra
status: on_hold
domain: structures
depth: 2
entity: "[[Nadvori_Stan]]"
---
# Návrh: Nadvori_Stan – zabydlený vojenský stan pro dva na nádvoří

Specifikace od architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **podmíněný návrh, nepostaveno.** Jirka zatím nerozhodl, jestli stan ve hře bude (14. 11. 2026). Náčrt není, jen popis slovy v kap. 10.

**Připravenost (15. 11. 2026)** – podrobně [[CHECKLIST_assets_navrhy]] (položky ⛺):
- **Rozhodnutí pořád chybí.** Stan se drží v seznamu s nízkou prioritou.
- **Hotové dílce:** tyče s kůrou `SM_RuinPoleBark` (stojky, hřeben, krokvičky), kolíky `SM_RuinStakeSmall`, vidlice `SM_RuinForkHead`, pásy kůry `SM_RuinBarkStrip`, lano `SM_RuinRope`, špalek `SM_RuinStump`, materiál plátna `MI_RuinCanvas`.
- **Chybí:** plachta stanu do A, lůžka z klád a tyčí, výplň lůžek, ranec a truhlička, typy staveb `tent` a `bark_roof`, přepínač `ETAPA`.

**Proč je to otevřené:** posádka má k dispozici věž. Letní bouřku jde přečkat i v jejím chladnějším spodním patře, takže stan nemusí být potřeba. Tento dokument je připravený pro případ, že se stan použije.

## 1. Zadání

- **Odkud:** Jirka.
- **Herní účel:** dočasné spaní pro dva členy posádky v etapě 1, dokud obytná stavba v paláci nemá střechu.
- **Souvislosti:**
  - začátek léta: teplo, sucho, občas bouřka;
  - posádka má vojenské stany, jeden už padl na plachtu na věži (`Vez_Pristresek`);
  - všechny ruce jsou na stavbě domu, na dočasné spaní se nedává práce navíc;
  - kůry je ze stavby dost.
- **Trvání:** jen etapa 1. V etapě 2 (dům hotový) stan nestojí.

## 2. Výchozí stav (spočítáno z dat, 11/2026)

**Souřadnice paláce** (stejné jako v [[navrh_palac_obydli_stred]]): `s` v metrech podél `Palac_J` od jejího prvního bodu (UE −2350 / −50), `n` v metrech kolmo k severu. Jednotkové vektory v UE: `s` = (0,9758; −0,2184), `n` = (−0,2189; −0,9757). Výšky v metrech nad terénem (v datech rovina Z 3129).

Nádvoří je pruh mezi severní zdí paláce (vnější líc n = 10,2) a severní hradbou.

| Úsek `Hradba_Z_S` (podle s paláce) | Vnitřní líc (n) | Koruna |
|---|---|---|
| s = 14–20 | 19,0–17,7 | 1,8–2,8 m |
| **s = 21–23** | **17,5–17,1** | **4,0–4,4 m** |
| s = 24–28 | 17,0–17,3 | 3,5–4,1 m |
| s = 29–33 | 17,4–17,6 | 2,8–3,2 m |

- Vnitřní líc hradby je obrácený k jihu.
- Nádvoří je v místě stanu široké asi 6,9 m.
- Vstup do věže (průlom ve `Vez_S`) je v s = 35, n = 11, tedy 11 m východně.
- Vstup do prostřední místnosti paláce je hrubý průchod v s = 15,1–16,9 (portál je od 16. 11. 2026 v západní místnosti, s = 3,7–5,3).
- V okolí leží v datech jeden kámen suti (s = 23,2; n = 17,9).
- Cisterna je jen v návrhu dat (střed s = 25,2; n = 11,8; průměr 3 m) a její poloha je otevřená.

## 3. Úpravy 03 (zřícenina)

**Ne.**

## 4. Cílová struktura

Stan stojí u paty severní hradby v nejvyšším úseku (s = 21,5–23,9), hřebenem rovnoběžně s hradbou. Vchod má na východ, k věži a bráně. Západní štít je zavřený proti převládajícímu větru.

### 4.1 Stan

| Prvek | Rozměr | Poloha |
|---|---|---|
| Půdorys | 2,4 m (podél hřebene) × 2,2 m | s = 21,5–23,9; n = 14,6–16,8 |
| Stojky | 2 ks, tyč Ø 7 cm, výška 1,9 m | ve štítech, n = 15,7; s = 21,5 a 23,9 |
| Hřebenová tyč | Ø 6 cm, délka 2,6 m | na stojkách, vrch 1,9 m |
| Plátno | lněné, jeden díl přes hřeben až k zemi, dva štítové díly | boky se sklonem asi 60° |
| Kolíky | 12 ks, dřevěné, 30 cm | po obvodu, po 0,6 m |
| Šňůry | 4 rohové a 2 štítové | ke kolíkům 0,5 m od plátna |

- **Vchod:** východní štít (s = 23,9), rozdělený uprostřed. Jedna chlopeň je odhrnutá a přivázaná.
- **Mezera k hradbě:** 0,3–0,5 m. Vede jí stružka.
- **Plátno:** stejný materiál jako plachta `Vez_Pristresek`, zašedlé, místy záplaty.

### 4.2 Úpravy pro delší pobyt

| Prvek | Rozměr | Poloha |
|---|---|---|
| Stružka | šířka 0,2 m, hloubka 0,15 m | kolem stanu 0,2 m od plátna, odtok po spádu terénu (určí se podle levelu) |
| Lůžka | 2 ks, každé 2,0 × 0,7 m, výška 0,25 m | podél boků stanu, mezi nimi ulička 0,6 m |
| Konstrukce lůžka | 2 příčné klády Ø 15 cm × 0,75 m, na nich 10 tyčí Ø 5 cm × 2,0 m | |
| Výplň lůžka | kapradí nebo sláma, přes ni houně | |

### 4.3 Stříška z kůry před vchodem

- **Kde:** s = 23,9–25,9; n = 14,7–16,7 (2,0 × 2,0 m), východně od vchodu.
- **Kostra:** 4 tyče s vidlicí Ø 8 cm zaražené do země. Jižní dvojice má vrch 2,1 m, severní 1,4 m. Na nich 2 vodorovné tyče a 5 krokviček Ø 6 cm.
- **Sklon:** asi 19° k severu, voda stéká do pruhu u hradby a do stružky.
- **Krytina:** pásy smrkové kůry ve 2 řadách s přesahem 0,2 m, zatížené 2 přítlačnými tyčemi. Stejná skladba jako `Brana_Straz_Pristresek`.
- **Otevřená** je na jih a na východ. Vchází se z jihu pod vyšší okraj.
- **Pod stříškou** (orientačně, pro game designera): špalek k sezení, zavěšené boty a zbraně, ranec nebo truhlička.

### 4.4 Úprava dřeva

- Tyče a klády `raw`, kůra jako u brány.

## 5. Dostavba 05

| Stavba | Typ | Obsah |
|---|---|---|
| `Nadvori_Stan` | **nový** (pracovně `tent`); plátno sdílí materiál s `Vez_Pristresek` | stojky, hřeben, plátno, kolíky, šňůry, lůžka |
| `Nadvori_Stan_Striska` | `bark_roof` (stejný jako u brány) | vidlice, tyče, kůra |

- **Složka:** `Stavby/Nadvori`.
- **Etapa:** jen etapa 1. Použít stejné přepínání etap jako u `Palac_Obydli` (parametr `ETAPA`).
- **Stružka** je úprava terénu, ne dílec. Buď se vymodeluje v levelu ručně, nebo se vynechá.
- **Suť:** kámen v s = 23,2; n = 17,9 je za stanem u hradby, nevadí.
- **Ruční doladění (`loose`):** celý stan má jít posunout jako jedna skupina, vybavení pod stříškou jsou samostatné actory.

## 6. Vazby, kolize, pořadí

- **Staveniště domu:** hromada krokví a prken leží podle [[navrh_palac_obydli_stred]] před severní zdí paláce (n = 10,5–12,3). Mezi ní a stanem zůstává průchod 2,3 m.
- **Cesta brána → vstup do paláce (průchod v s = 16)** vede tímto průchodem. Musí zůstat volná v šířce aspoň 1,2 m.
- **Cisterna:** stan je mimo její obrys z návrhu dat. Až bude poloha určená, zkontrolovat.
- **Šňůry a kolíky** nesmí zasahovat do průchodu. Na jižní straně končí nejdál v n = 14,1.
- **Pořadí:** nezávisí na jiných stavbách.

## 7. Ověření

- Stan ani stříška se nedotýkají hradby (mezera aspoň 0,3 m).
- Stojky a vidlice stojí na terénu, plátno dosedá k zemi po celém obvodu mimo vchod.
- Vchodem projde postava: volný otvor aspoň 0,7 × 1,7 m.
- Průchod jižně od stanu má aspoň 2,0 m.
- V etapě 2 není v místě žádný dílec stanu ani stříšky.

## 8. Varianty

| Varianta | Práce | Kdy dává smysl |
|---|---|---|
| Holý stan bez úprav | čtvrt hodiny | posádka právě dorazila |
| **Zabydlený stan (tento návrh)** | stan a půl dne úprav | jsou tu pár týdnů a zůstanou do dokončení domu |
| Přístěnek z tyčí a kůry opřený o hradbu | den pro dva lidi | stany došly nebo se šetří plátno |
| **Bez stanu, spaní ve věži** | žádná | Jirka to zvažuje: spodní patro věže je chladnější, ale suché |

## 9. Předpoklady a otevřené otázky

- **Otevřené (Jirka):** bude stan ve hře vůbec? Pokud ne, tento dokument se nepoužije.
- **Předpoklad (stan):** rozměry jsou podle obecné znalosti dobových vojenských stanů do A, ne z podkladů projektu.
- **Předpoklad (vítr):** převládá západní až severozápadní, proto je vchod na východ.
- **Předpoklad (terén):** v datech je nádvoří rovné. Odtok stružky se určí podle levelu.
- **Pokud by se spalo ve věži:** přízemí je hlavní sklad a 2. patro má hlídka pod plachtou. Pro dva lidi zbývá 1. patro (prkenná podlaha, kryté stropem 2. patra jen částečně, protože prkna 2. patra nejsou těsná).
- **Poloha cisterny** může místo stanu změnit.

## 10. Náčrt slovy

- **Půdorys:** stan 2,4 × 2,2 m leží u paty severní hradby, delší stranou podél ní, 0,4 m od líce. Na východ na něj navazuje stříška z kůry 2 × 2 m. Kolem stanu stružka. Jižně od stanu průchod nádvořím, za ním hromady dřeva u zdi paláce.
- **Řez sever–jih:** hradba 4,0–4,4 m, před ní trojúhelník stanu vysoký 1,9 m se šňůrami ke kolíkům. Uvnitř dvě nízká lůžka na kládách.
- **Pohled od východu (od věže):** v popředí stříška z kůry na čtyřech vidlicích, nižší u hradby, vyšší k nádvoří. Za ní otevřený štít stanu s odhrnutou chlopní, za stanem stěna hradby.
