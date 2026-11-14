# Návrh: Palac_Obydli – obytná stavba posádky v prostřední místnosti paláce

Specifikace od architekta pro stavitele (šablona `Lapikus\AGENT_Architekt_hrad.md`, kap. 8). Stav: **návrh finální stavby, nepostaveno.** Je to kopie návrhu `navrh_palac_obydli.md` (dům ve východní místnosti u věže) přenesená do **prostřední místnosti**. Původní dokument zůstává beze změny pro srovnání. Náčrty: `navrh_palac_obydli_stred.png` (hotová stavba) a `navrh_palac_obydli_stred_etapa1.png` (rozestavěný stav). Jsou to schémata, ne přesné modely.

**Proč prostřední místnost (Jirka, 14. 11. 2026):** součástí osídlení bude provizorní kovárna a u věže má komín špatný tah. Prostřední místnost je 11 m od věže, jižní zeď je tu rovnoměrnější a vstupem je zachovaný portál.

## 1. Zadání

- **Odkud:** Jirka.
- **Herní účel:** finální obydlí pro dva až tři členy posádky, s možností zimního vytápění.
- **Očekávání:**
  - ubytování dvou až tří postav,
  - uložení osobních věcí (hlavní sklad je v přízemí věže),
  - malý stůl pro drobnou práci za špatného počasí,
  - hrubé práce, společné jídlo a vaření v době stavby jsou venku pod jinými přístřešky.
- **Prostředky:** kámen z hradu, dřevo z okolního lesa, hrubé opracování (rychle, levně, prakticky).
- **Boční stěny:** stávající příčky zarovnané kamennou dozdívkou, nad nimi srub kvůli teplu.
- **Komín:** jižní zeď smí být v místě komína níž (starší zřícení), aby ji komín přesahoval.
- **Dvě etapy hry:** v první se stavba teprve staví, ve druhé je hotová. Kapitoly 3–8 popisují hotovou stavbu (etapa 2), rozestavěný stav (etapa 1) je v kap. 9.
- **Cisterna se neřeší.** Okapy budou, vyústění je dočasné.

## 2. Výchozí stav (spočítáno z dat, 11/2026)

**Souřadnice paláce:** `s` v metrech podél `Palac_J` od jejího prvního bodu (UE −2350 / −50), `n` v metrech kolmo od osy `Palac_J` k severu. Jednotkové vektory v UE: `s` = (0,9758; −0,2184), `n` = (−0,2189; −0,9757). Výšky jsou v metrech nad terénem (v datech rovina Z 3129, v levelu se může lišit).

Prostřední místnost má uvnitř 9,7 × 8,1 m (s = 10,9–20,6, n = 0,7–8,8).

| Strana | Zeď | Tloušťka | Koruna | Otvory |
|---|---|---|---|---|
| jih | `Palac_J` | 1,4 m | s 10–11,5: 5,8–6,0; s 12–14: 5,1–5,8; s 14,5–15: 4,3–5,1; s 15,5: vnitřní líc 3,9, jinak 4,7–5,1; s 16–20: 5,1 (vnitřní líc v s = 17 jen 4,3); s 20,5–21,5: 5,5–6,4 | střílny s výklenkem v s = 14 a 19 (výklenek 0,55–2,7 m, uvnitř 1,3 m široký) |
| sever | `Palac_S` | 1,4 m | s 11–13: 1,1–1,6; s 14–18: 3,9–4,3; s 19–21: 1,1–1,3 | portál s = 15,2–16,8, výška 3,0 m, s obloukem |
| západ | `Palac_pricka_1` (osa s = 10,5) | 0,8 m | 1,0–1,4 | dveře n = 4,25–5,25 (až k zemi) |
| východ | `Palac_pricka_2` (osa s = 21,0) | 0,8 m | 0,8–1,4 | dveře n = 4,25–5,25 (až k zemi) |

- Terén v místnosti je v datech rovný.
- **Sklep** je zatím jen v návrhu dat (`ruin_layout_draft.json`): s = 3–15, n = 1–8,5, klenba částečně propadlá. Zasahoval by pod západní polovinu domu (síň).
- Věž je od východního štítu domu 9,4 m.

## 3. Úprava 03: zřícení koruny jižní zdi u komína

**Vyžaduje úpravu 03.** Koruna `Palac_J` je u komína dnes 5,1 m, stejně jako vrch komína bez úpravy. Zeď se proto v tomto místě sníží jako starší zřícení (součást zříceniny, stav 1650), žádné cílené bourání posádkou.

- **Zápis v datech** (`tools/ruin/gen_layout.py`, zeď `Palac_J`): k dnešnímu `breaches` `{"s0": 16.5, "s1": 20.5, "floor": 6.0}` přidat `{"s0": 15.5, "s1": 18.3, "floor": 5.5, "slope_l": 1.2, "slope_r": 0.6}`.
- **Jednotky:** `floor` je v metrech od paty zdi. Koruna vychází asi o 0,8–1,2 m níž než zadaná hodnota.
- **Ověřeno výpočtem** mimo UE na dočasné kopii `ruin_layout.json` (žádný soubor projektu se neměnil). Výsledek závisí na `seed`.

Koruna `Palac_J` (m nad terénem):

| s (m) | Dnes | Nově |
|---|---|---|
| 10–15 | 4,7–6,0 | beze změny |
| 15,5 | vnitřní líc 3,9; jádro 4,7; vnější líc 5,1 | vnitřní líc 3,9; jádro a vnější líc 4,3 |
| 16–16,5 | 5,1 | vnitřní líc a jádro 4,3; vnější líc 4,7 |
| 17–18 | 5,1 (vnitřní líc v s = 17 jen 4,3) | 4,3–4,7 |
| 18,5 | 5,1 | 4,7 |
| 19–21,5 | 5,1–6,4 | beze změny |

- **Ubude** asi 21 kamenů, 2,3 m³.
- **Tvar:** mělké sedlo dlouhé asi 3 m, na západě ostřejší hrana, k východu pozvolna stoupá do dnešní koruny.
- **Podmínka pro dům:** koruna nesmí v s = 15,5–18,5 klesnout pod 4,3 m (horní okraj krytiny). Kde je vnitřní líc níž, dozdí se pod střechu (kap. 4.3).
- **Přestavět:** část `Palac`.

## 4. Cílová struktura

Dům zabírá jižní část místnosti v celé délce: s = 10,1–21,4 (obě boční stěny stojí na příčkách), n = 0,7–6,3. Uvnitř 52 m². Mezi domem a severní zdí paláce zůstává zápraží 2,3 m, na které se vchází portálem.

### 4.1 Krov (pultová střecha, spád k severu)

| Prvek | Průřez | Počet / délka | Poloha | Na čem leží |
|---|---|---|---|---|
| Sloupy u jižní zdi | 20 × 20 cm | 5 ks, výška 3,83 m | n = 0,85; s = 11,1 / 13,0 / 15,6 / 18,0 / 20,4 | na plochém kameni na terénu, těsně u líce `Palac_J`, mimo výklenky střílen |
| Horní pozednice | 20 × 20 cm | 9,7 m (2 kusy, spoj nad sloupem s = 15,6) | n = 0,85, vrch 4,03 m | na sloupech |
| Střední vaznice | 20 × 24 cm | 11,3 m (2 kusy, spoj nad příčkou) | n = 4,4, vrch 3,02 m | západní stěna (s = 10,5), srubová příčka (s = 15,75), východní stěna (s = 21,0); rozpětí 2 × 5,25 m, bez sloupů v místnostech |
| Dolní pozednice | poslední trám srubu | viz 4.2 | n = 6,2, vrch 2,50 m | severní srubová stěna |
| Krokve | 18 × 22 cm | 12 ks, délka 6,3 m | s = 10,2 až 21,3 po 1,01 m; od n = 0,75 po n = 6,8 | horní pozednice, střední vaznice, dolní pozednice; přesah 0,5 m za severní stěnu |

- **Sklon:** 16°. Střední vaznice je ve dvou třetinách délky krokve od jižní zdi.
- **Krytina:** stejná skladba jako `Ostroh_Krov`: latě napříč, prkna po spádu 22–30 cm, lišty přes spáry, krycí prkna přes krokve. Prkna jsou ve dvou délkách (3,4 + 3,2 m), horní řada přesahuje dolní o 0,25 m nad latí. Všechno dehtované (`tar`).
- **Plocha střechy:** s = 9,8–21,7 × 6,3 m, asi 75 m². Na obou štítech přesah 0,3 m za příčku.
- **Lemování:** jen podél `Palac_J` (horní okraj): prkno 20 cm na stojato, přitlačené ke zdi a zamazané jílem. Styk s věží odpadá.
- **Vrch krytiny u jižní zdi** je asi 4,3 m.

### 4.2 Stěny

| Stěna | Konstrukce | Poloha | Výška |
|---|---|---|---|
| Severní | srub z kulatiny Ø 22 cm, 9 řad, na podezdívce | osa n = 6,2; s = 10,1–21,4 (3 délky, spoje v nárožích a u příčky) | podezdívka 0–0,45 m, srub 0,45–2,50 m |
| Příčka | srub z kulatiny Ø 22 cm na podezdívce | osa s = 15,75; n = 0,7–6,2 | do 2,50 m, nad tím prkenný štít pod střechu |
| Západní | kámen + srub na `Palac_pricka_1` | osa s = 10,5; n = 0,7–6,2 | příčka srovnaná kamenem na 1,4 m, srub 1,4–2,50 m (5 řad), nad tím prkenný štít |
| Východní | kámen + srub na `Palac_pricka_2` | osa s = 21,0; n = 0,7–6,2 | příčka srovnaná kamenem na 1,4 m, srub 1,4–2,50 m (5 řad), nad tím prkenný štít |
| Jižní | stojící `Palac_J` | | dozdívka jen v místě sníženého vnitřního líce (4.3) |

- **Srub na obou bočních stěnách.** Východní stěna patří k vytápěné světnici, tam je srub kvůli teplu. Západní je u nevytápěné síně, ale je návětrná, nese konec střední vaznice a severní stěna na ní potřebuje nároží. Úspora při vynechání by byla jen 5 kulatin po 5,6 m.
- **Spáry srubu:** vymazané mechem a hlínou (vizuálně tmavší výplň mezi kulatinami).
- **Prkenné štíty:** svislá prkna s lištami. Východní štít je nad stropem světnice (u půdy), západní nad síní.
- **Úprava dřeva:** srub, sloupy a štíty `raw`, podlaha `raw`, krov a krytina `tar`.

### 4.3 Kamenné části (kámen z rozvalin, jako `Ostroh_Dostavba`)

| Část | Kde | Rozměr |
|---|---|---|
| Srovnání koruny `Palac_pricka_1` | n = 0,7–6,2, včetně zazdění dveří příčky | na 1,4 m, v celé tloušťce 0,8 m (dnes 1,0–1,4 m) |
| Srovnání koruny `Palac_pricka_2` | n = 0,7–6,2, včetně zazdění dveří příčky | na 1,4 m, v celé tloušťce 0,8 m (dnes 0,8–1,4 m) |
| Podezdívka severní stěny | osa n = 6,2; s = 10,9–20,6, přerušená ve dveřích | 0,45 × 0,45 m |
| Podezdívka příčky | osa s = 15,75; n = 0,7–6,0, přerušená ve dveřích | 0,45 × 0,45 m |
| Dozdívka koruny `Palac_J` | s = 15,25–18,25, kde je vnitřní líc pod 4,35 m | 0,45 m na vnitřní polovině koruny, až pod střechu (0–0,45 m) |

- Dozdívka příček je v celé tloušťce 0,8 m, tedy širší než jednořadá zeď 0,45 m u ostrohu. Je to parametr tloušťky, ne nový typ.

### 4.4 Otvory

| Otvor | Kde | Rozměr | Poznámka |
|---|---|---|---|
| Vchod | severní stěna, s = 13,8–14,8 | 1,0 × 2,2 m | do síně; od portálu 1,5 m šikmo vlevo |
| Dveře do světnice | příčka, n = 3,3–4,3 | 1,0 × 2,2 m | |
| Okénko světnice | severní stěna, s = 18,5–19,1 | 0,6 × 0,6 m, parapet 1,3 m | okenice, bez skla; proti nízké části `Palac_S` |
| Okénko síně | severní stěna, s = 11,8–12,3 | 0,5 × 0,5 m, parapet 1,3 m | okenice |
| Střílny `Palac_J` | s = 14 (síň), s = 19 (světnice) | stávající | světlo a výhled na jih, výklenek jako police |

### 4.5 Místnosti

| Místnost | Rozměr uvnitř | Podlaha | Strop |
|---|---|---|---|
| Světnice (východní) | s = 15,9–20,6; n = 0,7–6,05 (4,7 × 5,35 m) | prkna na podvalech (`plank_floor`) | trámkový, spodek 2,3 m |
| Síň a komora (západní) | s = 10,9–15,6; n = 0,7–6,05 (4,7 × 5,35 m) | udusaná hlína | bez stropu, otevřeno do krovu |
| Půda nad světnicí | nad stropem | prkna stropu | výška 0–1,6 m, přístup žebříkem ze síně otvorem ve štítu příčky |

- **Strop světnice:** 6 trámků 14 × 18 cm ve směru východ–západ po 0,9 m (n = 1,1 až 5,6), prkna 4 cm. Leží v zářezech srubové příčky a srubu východní stěny, žádné další sloupy. U jižní zdi je otvor 1,6 × 1,6 m pro dymník a komín: trámky n = 1,1 a 2,0 jsou tam přerušené a uložené do výměny.

### 4.6 Ohniště a komín

- **Kde:** u jižní zdi ve světnici, s = 16,2–17,6; n = 0,7–2,1. Zády k `Palac_J`, mezi příčkou a výklenkem střílny.
- **Základ:** kamenný blok 1,4 × 1,4 m, výška 0,5 m, z kamene rozvalin.
- **Dymník:** proutěný koš vymazaný hlínou, spodní okraj 1,7 m, zužuje se ke stropu.
- **Komín:** 0,6 × 0,6 m, proutí s hlínou, střed s = 16,9; n = 1,6. Prochází stropem a střechou mezi krokvemi a končí v **5,3 m** nad terénem (1,2 m nad krytinou).
- **Poměr ke zdi:** po úpravě 03 je koruna `Palac_J` v s = 15,5–18,5 ve výšce 4,3–4,7 m. Komín ji přesahuje o 0,6–1,0 m. Mimo snížený úsek je zeď vyšší (5,1–6,4 m).
- Horní pozednice (n = 0,75–0,95) vede 0,35 m jižně od komína, komín se jí nedotýká.

### 4.7 Okap

- **Žlab:** vydlabaný kmen Ø 20 cm pod severním okapem, n = 6,85; s = 9,9–21,6. Spád 1 % k východu (vrch 2,25 → 2,13 m). Nesou ho vidlice zaražené u stěny.
- **Svod:** koryto od žlabu v s = 20,0 přes zápraží a přes nízkou část `Palac_S` (koruna 1,1 m) na nádvoří, konec u n = 10,7.
- **Vyústění je dočasné.** Až bude určená cisterna, svod se přesměruje. Poloha svodu má být parametr.

### 4.8 Vybavení (orientačně, pro game designera)

- **Světnice:** tři lůžka 2,0 × 0,8 m (dvě u východní stěny, jedno u severní), stůl 1,2 × 0,7 m u okénka, dvě truhly.
- **Síň:** hranice dřeva u západní stěny, ponk u střílny s = 14, police na osobní věci.
- Tři osoby se vejdou pohodlně, čtvrtá v nouzi.

## 5. Dostavba 05

| Stavba | Typ | Obsah |
|---|---|---|
| `Palac_Obydli_Krov` | **nový** (pracovně `pult_roof`), krytina sdílená s `fan_roof` | sloupy, pozednice, vaznice, krokve, krytina, lemování |
| `Palac_Obydli_Srub` | **nový** (pracovně `log_wall`) | severní stěna, příčka, srub na obou bočních stěnách, prkenné štíty, otvory |
| `Palac_Obydli_Kamen` | existující `stone_addon` (s parametrem tloušťky) | srovnání obou příček, podezdívky, dozdívka koruny `Palac_J` |
| `Palac_Obydli_Strop` | nový, nebo rozšíření `tower_floor` | trámky, výměna u komína, prkna |
| `Palac_Obydli_Podlaha` | existující `plank_floor` | podlaha světnice |
| `Palac_Obydli_Ohniste` | **nový** | základ, dymník, komín |
| `Palac_Obydli_Okap` | **nový** (malý) | žlab, vidlice, svod |

- **Složka:** `Stavby/Palac`.
- **Sdílené rozměry:** nový `tools/ruin/palac_spec.py` (osy stěn, výšky pozednic a vaznice, sklon, polohy sloupů, otvorů a komína, rozsah snížení `Palac_J`). Čte ho 03 (`gen_layout.py`, průlom) i 05.
- **Suť:** uvnitř domu a na zápraží uklizená (`clear_rubble`).
- **Ruční doladění (`loose`):** práh vchodu, patní kameny sloupů, vidlice žlabu.

## 6. Vazby, kolize, pořadí

- Sloupy u jižní zdi nesmí stát ve výklencích střílen (s = 13,35–14,65 a 18,35–19,65).
- Ohniště nesmí zasahovat do výklenku střílny s = 19 (mezera 0,75 m).
- Svod kříží zápraží na východním konci (s = 20,0), mimo cestu od portálu (s = 16) ke vchodu (s = 14,3).
- **Kovárna ve východní místnosti:** výheň má být až u věže, aspoň 6 m od východního štítu domu (dehtovaná střecha). Dveře v `Palac_pricka_2` jsou zazděné, mezi domem a kovárnou není průchod.
- **Pořadí:** 03 `Palac` → `Palac_Obydli_Kamen` → `Palac_Obydli_Krov` (bez krytiny) → `Palac_Obydli_Srub` → krytina → `Palac_Obydli_Strop`, `Palac_Obydli_Podlaha`, `Palac_Obydli_Ohniste`, `Palac_Obydli_Okap`. Dozdívka koruny `Palac_J` bere výšku z krovu, stejně jako u ostrohu.

## 7. Ověření

- `tools/checks/run_checks.py`: žádné kameny bez podpory, průniky dřeva se zdivem jen v zářezech a uloženích.
- Koruna `Palac_J` v s = 15,5–18,5 je 4,3–4,7 m a nikde v s = 10,9–20,6 není pod 4,3 m (po dozdívce).
- Vrch komína je aspoň 0,5 m nad korunou `Palac_J` v okruhu 1,5 m od komína.
- Každý sloup stojí na terénu nebo patním kameni, každá krokev leží na třech podporách.
- Krytina pokrývá aspoň 99,5 % půdorysu domu (s = 10,1–21,4; n = 0,7–6,3).
- Mezi krytinou a `Palac_J` není mezera větší než 5 cm (po dozdívce a lemování).
- Zdí neprosvítá: srub, srovnané příčky, podezdívky a dozdívka koruny jsou souvislé.
- Sklon střechy je 16° ± 1°.
- Vchod i dveře do světnice mají volný průchod 1,0 × 2,2 m, práh nejvýš 45 cm.
- Světlá výška ve světnici je aspoň 2,3 m, v síni pod střední vaznicí aspoň 2,7 m.
- Zápraží má volnou šířku aspoň 2,0 m, portál zůstává průchozí.
- Žlab má spád k východu a svod končí za vnějším lícem `Palac_S`.
- Náhled: `tools/checks/preview3d.py` (zvenku od nádvoří portálem, zevnitř ze světnice a ze síně).

## 8. Rozdíly proti návrhu ve východní místnosti

| | Východní (`navrh_palac_obydli.md`) | Prostřední (tento dokument) |
|---|---|---|
| Plocha uvnitř | 49 m² | 52 m² |
| Východní stěna | věž | kámen + srub na `Palac_pricka_2` |
| Ohniště | u stěny věže | u jižní zdi |
| Komín proti okolním zdem | pod věží (9–13,5 m) i jižní zdí (až 6,7 m) | 0,6–1,0 m nad sníženou jižní zdí |
| Úprava 03 | žádná | snížení koruny `Palac_J` u komína (21 kamenů) |
| Dozdívka koruny `Palac_J` | s = 25,5–29, až 0,4 m | jen vnitřní líc u komína, do 0,45 m |
| Lemování střechy | jižní zeď a věž | jen jižní zeď |
| Sloupy uvnitř místností | jeden v síni | žádný |
| Vstup | původní dveře | portál |
| Střecha | 66 m², 11 krokví | 75 m², 12 krokví |
| Okno věže nad střechou | ano (možná cesta postavy) | netýká se |

## 9. Etapa 1: rozestavěná stavba (hráč přichází poprvé)

Začátek léta, posádka dům teprve staví. Stav je navržený jako **postup od západu k východu**: síň je u základů, světnice už má stěny a první krokve. Hráč tak na jednom místě přečte celý postup stavby.

Zřícenina (03) je v obou etapách stejná, včetně snížené koruny `Palac_J` u komína. Mezi etapami se přestavuje jen 05.

### 9.1 Co stojí

| Stavba | Etapa 1 | Chybí do etapy 2 |
|---|---|---|
| `Palac_Obydli_Kamen` | obě příčky srovnané na 1,4 m včetně zazděných dveří; podezdívky severní stěny a příčky hotové | dozdívka koruny `Palac_J` pod střechu |
| `Palac_Obydli_Srub`, východní polovina (světnice) | severní stěna s = 15,75–21,4 v plné výšce 2,50 m s otvorem pro okénko; příčka v plné výšce s otvorem pro dveře; srub na východní stěně hotový (5 řad) | prkenné štíty, dveře, okenice, výplň spár |
| `Palac_Obydli_Srub`, západní polovina (síň) | severní stěna s = 10,1–15,75 jen 3 řady (vrch 1,13 m), s mezerou pro vchod | zbylých 6 řad severní stěny, celý srub na západní stěně (5 řad), štít |
| `Palac_Obydli_Krov`, sloupy | všech 5 sloupů u jižní zdi stojí | |
| `Palac_Obydli_Krov`, pozednice | východní kus (s = 15,6–20,6) leží na sloupech | západní kus (leží na zemi v síni) |
| `Palac_Obydli_Krov`, vaznice | východní kus (příčka → východní stěna) je osazený | západní kus (leží na staveništi) |
| `Palac_Obydli_Krov`, krokve | 6 krokví nad světnicí (s = 16,26 až 21,31) je osazených, na nich 2 řady latí jako zavětrování | 6 krokví nad síní, ostatní latě, krytina, lemování |
| `Palac_Obydli_Ohniste` | vyskládaná první řada kamenů základu (0,25 m) | zbytek základu, dymník, komín |
| `Palac_Obydli_Strop`, `Palac_Obydli_Podlaha`, `Palac_Obydli_Okap` | nic | všechno |

- Všechno dřevo v etapě 1 je čerstvé (`raw`), i krov. Dehtuje se až po dokončení, v etapě 2 je krov a krytina `tar`.
- Otvory jsou prázdné: vchod, dveře v příčce a okénko nemají výplň.
- Nad světnicí je mezi krokvemi vidět nebe, nad síní není nic.

### 9.2 Staveniště (jen v etapě 1)

Nová stavba `Palac_Obydli_Stavenisko`, v etapě 2 se nestaví.

| Prvek | Rozměr | Kde |
|---|---|---|
| Dočasné vzpěry sloupů | kulatina Ø 10 cm, asi 3 m, 2 ks na sloup | u západních sloupů (s = 11,1 a 13,0), které ještě nedrží pozednice; šikmo do země k severu a do strany |
| Žebřík | 4,5 m | opřený o horní pozednici ve světnici |
| Tesařské kozy s rozpracovanou kulatinou | 2 kozy, kulatina 5,7 m | na zápraží západně od vchodu (s = 10,9–13,5) |
| Západní kus pozednice | 20 × 20 cm, 4,9 m | na zemi v síni podél západní stěny |
| Hromada kamene | asi 1 m³ | ve světnici u základu ohniště |
| Hlína a mech na spáry | hromada a koš | v síni |
| Třísky a kůra | plošně | na zápraží a kolem koz |
| Kulatina na srub | 11 ks Ø 22 cm × 5,7 m, ve dvou vrstvách | na nádvoří před severní zdí paláce, západně od portálu |
| Krokve a západní kus vaznice | 6 ks 6,3 m + 1 ks 5,7 m | na nádvoří před severní zdí paláce, východně od portálu |
| Prkna na krytinu | první hromada, asi 20 ks | na nádvoří u krokví |

- Polohy hromad jsou doporučené, přesné rozmístění určí game designer. Podmínka: cesta portál → vchod → dveře do světnice zůstává volná v šířce aspoň 1,2 m.
- Hromady a nářadí mají být samostatné actory (`loose`), aby se daly doladit ručně.

### 9.3 Pohyb hráče

- **Trasa:** nádvoří → portál → zápraží → mezera pro vchod → síň → otvor v příčce → světnice. Všude po terénu, bez prahů.
- **Nízký srub síně (1,13 m) se nedá přejít,** dovnitř se jde jen mezerou pro vchod.
- **Srovnané příčky (1,4 m) jsou bez průchodu.** Do západní a východní místnosti se z domu nedá projít.
- **Dočasné vzpěry** u západních sloupů zužují síň u jižní zdi. Střed síně musí zůstat volný.

### 9.4 Pro stavitele

- **Přepínání etap:** jeden parametr `ETAPA` (1 / 2) v `palac_spec.py`. Každý dílec nebo skupina dílců má údaj, od které etapy existuje, a staveniště údaj, do které.
- **Počty řad srubu a krokví** v etapě 1 mají být parametry, ne pevné hodnoty. Stav se bude ladit podle toho, jak vypadá ve hře.
- **Úprava dřeva podle etapy:** krov `raw` v etapě 1, `tar` v etapě 2.
- **Ověření etapy 1:**
  - každá osazená krokev leží na třech podporách (pozednice, vaznice, severní stěna),
  - žádný dílec nevisí ve vzduchu, ležící trámy leží na terénu,
  - sloupy bez pozednice mají obě vzpěry,
  - trasa z kap. 9.3 je průchozí v šířce 1,2 m.

### 9.5 Otázky k etapě 1

- **Žebřík:** má být pro postavu použitelný (výstup na pozednici a krokve), nebo jen kulisa?
- **Kde v etapě 1 spí ti, kdo nejsou na hlídce?** Dům ještě nemá střechu. Návrh to neřeší.
- **Jak se etapy ve hře přepnou** (dvě verze levelu, skrytí a zobrazení sad actorů), je věc game designu.

## 10. Předpoklady a otevřené otázky

- **Předpoklad („podložené ve dvou třetinách"):** čteno jako střední vaznice pod krokvemi ve 2/3 délky.
- **Předpoklad (vítr):** převládá západní až severozápadní. V podkladech to není.
- **Předpoklad:** dveře v obou příčkách se zazdí. Kdyby západní místnost měla sloužit jako dřevník nebo chlév, dají se dveře v `Palac_pricka_1` nechat jako zadní vchod ze síně.
- **Sklep:** je jen v návrhu dat a ležel by pod síní. Až se bude stavět, je potřeba vyřešit dvě věci: severní srubová stěna síně (s = 10,9–15) by stála nad klenbou a propadlé místo klenby nesmí být pod podezdívkou. Výhoda: vstup do sklepa přímo ze síně.
- **Rozšíření o podsíň:** pokud se počítá s pozdějším zastřešením zápraží, je lepší postavit severní stěnu rovnou 3,0 m vysokou. Krov by byl o 0,5 m výš, a tím i komín a potřebné snížení jižní zdi.
- **Riziko (kouř):** mimo snížený úsek je jižní zeď vyšší než komín (5,1–6,4 m) a v 1. patře má okenní otvory. Za jižního větru může kouř srážet dolů.
- **Riziko (déšť od jihu):** ve sníženém úseku je koruna zdi skoro v úrovni střechy. Hnaný déšť od útesu jde přes zeď rovnou na lemování.
- **Neřeší se:** cisterna, kovárna, přístřešky pro hrubé práce a společný stůl, venkovní ohniště.

## 11. Náčrt slovy

- **Půdorys:** obdélník 11,3 × 5,6 m u jižní zdi prostřední místnosti. Jižní stranu tvoří `Palac_J`, obě boční stěny stojí na příčkách, severní je nový srub. Srubová příčka v s = 15,75 dělí dům na světnici (východ) a síň (západ). Ohniště je ve světnici u jižní zdi hned za příčkou. Vchod je v severní stěně do síně, šikmo proti portálu. Před domem zápraží 2,3 m.
- **Řez jih–sever:** u jižní zdi sloup s pozednicí (vrch 4,03 m), krokve klesají 16° přes střední vaznici (vrch 3,02 m ve n = 4,4) na srubovou stěnu (vrch 2,50 m ve n = 6,2) a přesahují ji o 0,5 m. U jižní zdi stoupá komín do 5,3 m, zeď je vedle něj snížená na 4,3–4,7 m. Ve světnici strop se spodkem trámků 2,3 m, nad ním půda.
- **Boční stěna:** dole stará příčka srovnaná kamenem na 1,4 m, nad ní pět řad kulatiny do 2,5 m, nad tím trojúhelník svislých prken pod střechu.
- **Pohled od nádvoří:** portálem je vidět srubová stěna s dveřmi, nad nízkými částmi zdi paláce vykukuje tmavá prkenná střecha stoupající k jižní zdi a nad ní komín.
