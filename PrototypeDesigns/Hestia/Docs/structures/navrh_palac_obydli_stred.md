---
# orchestrace
type: design
validity: valid
alternative_to: ["[[navrh_palac_obydli]]"]
updated: 2026-11-23
# hra
status: in_progress
domain: structures
depth: 4
entity: "[[Palac_Obydli]]"
build_step: 05_constructions
---
# Návrh: Palac_Obydli – obytná stavba posádky v prostřední místnosti paláce

## Souhrn
Platný návrh domu posádky v prostřední místnosti paláce (varianta ve východní místnosti, [[navrh_palac_obydli]], je zavržená). Kap. 4–7 popisují hotovou stavbu (etapa 2) s čísly podle dat (`tools/ruin/palac_spec.py`); co je postavené a ověřené, je v [[stav_palac_obydli]].
- **Etapy:** plán po etapách, rozdělení po stavbách, pořadí a zamčená sada `base` jsou v [[navrh_palac_obydli_etapy]]; etapa 1 a staveniště v [[navrh_palac_obydli_stavenisko]].
- **Konstrukce:** pultový krov se spádem 16° k severu na třech podporách, srubové stěny a příčka v s = 14,85, kamenné podezdívky, okap se spádem k západu přes příčku do sudu, bez svodu (kap. 4). Pec s nístějí a komín: [[navrh_palac_obydli_pec]].
- **Dřevo a otvory:** všechno dřevo surové (`raw`); dveře a okenice v etapě 2 otevřené jako kulisa, žebříky jen kulisa.
- **Zbývá postavit:** krytina s lemováním, strop, podlaha, okap, zárubně, vybavení (předání [[predani_palac_obydli_2_krytina]] až [[predani_palac_obydli_7_vybaveni]]).
- **Otevřené otázky a rizika:** kap. 10 a [[navrh_palac_obydli_stavenisko]] kap. 9.5.

Náčrty: [[navrh_palac_obydli_stred.png]] (hotová stavba) a [[navrh_palac_obydli_stred_etapa1.png]] (rozestavěný stav); jsou to schémata, ne přesné modely. Připravenost assetů: [[CHECKLIST_assets_navrhy]].

**Proč prostřední místnost (Jirka, 14. 11. 2026):** součástí osídlení bude provizorní kovárna a u věže má komín špatný tah. Prostřední místnost je 11 m od věže, jižní zeď je tu rovnoměrnější. Vchází se sem hrubým průchodem v `Palac_S` po rozebraném portálu (kap. 3).

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
- **Dvě etapy hry:** v první se stavba teprve staví, ve druhé je hotová. Kap. 4–7 popisují hotovou stavbu (etapa 2), rozestavěný stav (etapa 1) je v [[navrh_palac_obydli_stavenisko]].
- **Cisterna se neřeší.** Okapy budou, voda zatím teče do sudu (kap. 4.7).

## 2. Výchozí stav (změřeno z dat 16. 11. 2026, po úpravách 03 z kap. 3)

**Souřadnice paláce:** `s` v metrech podél `Palac_J` od jejího prvního bodu (UE −2350 / −50), `n` v metrech kolmo od osy `Palac_J` k severu. Jednotkové vektory v UE: `s` = (0,9758; −0,2184), `n` = (−0,2189; −0,9757). Výšky jsou v metrech nad terénem (v datech rovina Z 3129, v levelu se může lišit).

Prostřední místnost má uvnitř 9,7 × 8,1 m (s = 10,9–20,6, n = 0,7–8,8).

| Strana | Zeď | Tloušťka | Koruna | Otvory |
|---|---|---|---|---|
| jih | `Palac_J` | 1,4 m | vnitřní líc po zanoření celé zdi o 0,31 m: s 10–11,5: 5,5–5,7; s 12–12,5: 4,8; s 13–14: 5,2–5,5; s 14,5–15,5: 4,4–4,8; s 16–20: 4,8 (v s = 17 jen 4,4); s 20,5–21,5: 5,5–6,0 | střílny s výklenkem v s = 14 a 19 (výklenek 0,24–2,39 m nad zemí, uvnitř 1,3 m široký) |
| sever | `Palac_S` | 1,4 m | s 11–14: 1,1–1,6; s 17–21: 1,1–1,4 | hrubý průchod s = 15,1–16,9 až k zemi, vylámané okraje (kap. 3) |
| západ | `Palac_pricka_1` (osa s = 10,5) | 0,8 m | 1,05–1,39 | dveře n = 4,25–5,25 (až k zemi) |
| východ | `Palac_pricka_2` (osa s = 21,0) | 0,8 m | 1,09 | dveře n = 4,25–5,25 (až k zemi); severně od domu průchod ke kovárně n = 6,9–8,5 (kap. 3) |

- Terén v místnosti je v datech rovný. Sklep je jen v návrhu dat (kap. 10).
- Vnitřní líc `Palac_J` je v celé délce domu nejníž 4,43 m, krytina u zdi končí ve 4,3 m: dozdívka koruny není potřeba, zůstává jen lemování.
- Věž je od východního štítu domu 9,4 m.

## 3. Úpravy 03 kolem domu (Jirka 16. 11. 2026)

Zapsáno v `tools/ruin/gen_layout.py` (zeď `Palac_S`) a `tools/ruin/palac_spec.py` (`D_PASS` → `ruin_edits`).

- **Vstupní oblouk (portál) je přesunutý do západní, prázdné místnosti:** `Palac_S` má portál 1,6 × 3,0 m v s = 4,5 (místo dveří), zeď kolem něj drží do 4,2 m (`protect` s = 2,5–6,5).
- **Ve střední místnosti posádka oblouk rozebrala na stavbu.** V `Palac_S` zůstal hrubý průchod až k zemi (`prulom` s = 16, šířka 1,8 m, vylámané okraje) v nízké zdi 1,1–1,4 m. Průchod je v s = 15,1–16,9.
- **Průchod ke kovárně:** `Palac_pricka_2` je severně od domu rozebraná na kámen pro podezdívky. Hrubý průchod až k zemi v n = 6,9–8,5 (šířka 1,6 m, vylámané okraje); u rohu domu a u `Palac_S` zůstaly zbytky zdi, takže je vidět, že tu zeď byla. Ze zápraží se jím jde na dvorek kovárny.
- Ostatní kameny obou zdí se nezměnily, jen u dveří do východní místnosti (`Palac_S`, s = 27) je vylámané ostění o kousek širší.
- **Zřícení koruny `Palac_J` u komína se nedělá:** po zanoření zdi je koruna u komína (s = 15,5–18,5) 4,4–4,8 m a komín 5,3 m ji přesahuje o 0,5–0,9 m ([[Rozhodnuti_zricenina]]).

## 4. Cílová struktura

Dům zabírá jižní část místnosti v celé délce: s = 10,1–21,4 (obě boční stěny stojí na příčkách), n = 0,7–6,3. Uvnitř 52 m². Mezi domem a severní zdí paláce zůstává zápraží 2,3 m, na které se vchází průchodem v `Palac_S` (s = 15,1–16,9). Ze zápraží vede na východ průchod v `Palac_pricka_2` (n = 6,9–8,5) na dvorek kovárny. Čísla jsou z `tools/ruin/palac_spec.py` (`D_*`); kde se liší od tohoto textu, platí data a text se opraví.

### 4.1 Krov (pultová střecha, spád k severu, typ `pult_roof`)

| Prvek | Průřez | Počet / délka | Poloha | Na čem leží | Sada |
|---|---|---|---|---|---|
| Sloupy u jižní zdi | 20 × 20 cm | 5 ks, výška 3,73 m | n = 0,85; s = 11,1 / 13,0 / 15,3 / 18,0 / 20,4 | na patním kameni 26 × 36 × 14 cm (zapuštěný 4 cm) těsně u líce `Palac_J`, mimo výklenky střílen a pec | `base` |
| Horní pozednice | 20 × 20 cm | 11,3 m, 2 kusy: s = 10,1–15,3 a 15,3–21,4 | n = 0,85, vrch 4,03 m | na sloupech, spoj nad sloupem 15,3 | západní `final`, východní `base` |
| Střední vaznice | 20 × 24 cm | 11,3 m, 2 kusy: s = 10,1–14,85 a 14,85–21,4 | n = 4,4, vrch 3,02 m | na 3 špalcích 20 × 20 × 28 cm na vrchní řadě srubu západní stěny (s = 10,5), příčky (14,85) a východní stěny (21,0); spoj nad příčkou, v místnostech bez sloupů | západní kus a jeho špalek `final`, ostatní `base` |
| Dolní pozednice | vrchní řada srubu | viz 4.2 | n = 6,2, vrch 2,50 m | severní srubová stěna | podle srubu |
| Krokve | 18 × 22 cm, hraněné | 12 ks, délka 6,2 m | s = 10,2 až 21,3 po 1,01 m; n = 0,80–6,8 | na všech třech podporách, osedlání 3 cm; horní konec 10 cm od líce `Palac_J`, přesah 0,6 m za severní stěnu | 6 nad světnicí (s ≥ 16,0) `base`, 6 nad síní `final` |
| Latě zavětrování | 5 × 6 cm | 2 řady | n = 2,6 a 5,3; s = 16,17–21,4 | na krokvích nad světnicí | `base` |

- **Sklon:** 16°. Vaznice je ve dvou třetinách délky krokve od jižní zdi.
- **Pozednice a vaznice jsou dlouhé přes obě boční stěny** (s = 10,1–21,4), aby na nich ležely i štítové krokve.
- **Krytina** (`final`): skladba jako `Ostroh_Krov`: latě napříč, prkna po spádu 22–30 cm, lišty přes spáry, krycí prkna přes krokve. Prkna ve dvou délkách (3,4 + 3,2 m), horní řada přesahuje dolní o 0,25 m nad latí. V řadách latí zavětrování se kladou jen západní části latí ([[navrh_palac_obydli_etapy]] kap. 0.7).
- **Plocha střechy:** s = 9,8–21,7 × 6,3 m, asi 75 m²; na obou štítech přesah 0,3 m za konec pozednice.
- **Lemování** (`final`): jen podél `Palac_J`, prkno 20 cm na stojato, přitlačené ke zdi a zamazané jílem. Dozdívka koruny `Palac_J` se nedělá (kap. 2).
- **Prostup komína** (`final`): komín 0,5 × 0,5 m (s = 16,76; n = 1,7) prochází krytinou mezi krokvemi 16,26 a 17,26 (16 cm od obou), bez výměny v krovu. Kolem komína je lemování jako u zdi (prkna na stojato, zamazaná jílem).
- **Úprava dřeva:** `raw`, krov i krytina.

### 4.2 Stěny (typ `log_wall`, loupaná kulatina, `raw`)

| Stěna | Konstrukce | Poloha | Výška | Sada |
|---|---|---|---|---|
| Severní, světnice | 9 řad kulatiny na podezdívce: 4 řady po 24 cm do 1,4 m, 5 řad po 22 cm | osa n = 6,2; s = 14,85–21,45 | podezdívka 0–0,45 m, srub 0,45–2,50 m | `base` |
| Severní, síň | stejně, mezera pro vchod | osa n = 6,2; s = 10,05–14,85 | stejně | spodní 3 řady (vrch 1,16 m) `base`, zbylých 6 `final` |
| Příčka | 9 řad, první a poslední půltrám, na podezdívce | osa s = 14,85; n = 0,74–6,5 | do 2,50 m, nad tím prkenný štít | `base` |
| Východní | kámen + srub na `Palac_pricka_2`: 4 řady kulatiny mezi dvěma půltrámy | osa s = 21,0; n = 0,7–6,2 | kámen do 1,4 m, srub 1,4–2,50 m, nad tím štít | `base` |
| Západní | stejně na `Palac_pricka_1` | osa s = 10,5; n = 0,7–6,2 | stejně | `final` |
| Jižní | stojící `Palac_J` | | bez dozdívky | – |
| Prkenné štíty | svislá prkna 20–28 cm, tl. 3,5 cm, přes vrchní řadu srubu 10 cm, výřezy pro pozednici a vaznici | západní, východní, nad příčkou | od vrchu srubu rovně pod vrch krokví | `final` |

- **Nároží jako u skutečného srubu:** boční stěny a příčka začínají a končí půltrámem (hraněný, 11 cm), jejich řady jsou proto o půl řady posunuté proti severní stěně. V nárožích se kulatiny střídají a zhlaví přesahují 0,3 m (náhodně ± 5 cm).
- **Zdí neprosvítá:** kulatina je o 1,2 cm tlustší než řada (překryv jako v drážce). Výplň spár mechem a hlínou se nestaví.
- **Srub na obou bočních stěnách.** Východní stěna patří k vytápěné světnici. Západní je u nevytápěné síně, ale je návětrná, nese konec vaznice a severní stěna na ní potřebuje nároží.
- **Štíty:** východní je nad stropem světnice (u půdy), západní nad síní. U příčky zůstává pod krytinou stupňovitá mezera do 7 cm.

### 4.3 Kamenné části (typ `stone_fill`, kámen z rozvalin jako `Ostroh_Dostavba`, vše `base`)

| Část | Kde | Rozměr |
|---|---|---|
| Srovnání `Palac_pricka_1` | s = 10,1–10,9; n = 0,72–6,43, včetně zazdění dveří příčky | vrch 1,4 m; dvě řady přes tloušťku 0,8 m, spodek kopíruje korunu zříceniny |
| Srovnání `Palac_pricka_2` | s = 20,6–21,4; n = 0,72–6,43, včetně zazdění dveří příčky | stejně |
| Podezdívka severní stěny | osa n = 6,2; s = 10,9–20,6, přerušená ve vchodu (s = 13,4–14,4) | 0,45 × 0,45 m |
| Podezdívka příčky | osa s = 14,85; n = 0,72–5,98, přerušená ve dveřích (n = 3,3–4,3) | 0,45 × 0,45 m |

- **Maltové jádro:** v ose obou příček i podezdívek je jádro 6 cm (`mortar`, materiál `MI_RuinCore`) od země až 2 cm pod vrch. Prochází novým zdivem i starou příčkou pod ním; kde staré zdi jádro chybí, vyplní dutinu mezi líci. Ve dveřích a ve větší díře skrz zeď není.
- **Nové zdivo** začíná v n = 0,72 (2 cm od líce `Palac_J`).
- Podezdívka příčky končí u `Palac_J` těsně u výklenku střílny síně (s = 13,35–14,65), kulatina je od něj 8 cm.

### 4.4 Otvory (zarovnané na řady srubu)

| Otvor | Kde | Světlý rozměr | Poznámka |
|---|---|---|---|
| Vchod | severní stěna, s = 13,4–14,4 | 1,0 × 2,28 m | do síně, 0,22 m od podezdívky příčky; od průchodu v `Palac_S` asi 2 m šikmo vlevo |
| Dveře do světnice | příčka, n = 3,3–4,3 | 1,0 × 2,17 m | |
| Okénko světnice | severní stěna, s = 17,5–18,1 | 0,6 × 0,66 m, parapet 1,4 m | uprostřed stěny světnice, mezi krokvemi 17,26 a 18,27; okenice, bez skla |
| Okénko síně | severní stěna, s = 11,8–12,3 | 0,5 × 0,44 m, parapet 1,4 m | okenice; zůstává takto, i když střed stěny vlevo od vchodu je 12,15 (Jirka 21. 11. 2026) |
| Střílny `Palac_J` | s = 14 (síň), s = 19 (světnice) | stávající, výklenek 0,24–2,39 m nad zemí | světlo a výhled na jih, výklenek jako police |

- Řada srubu se v otvoru vynechá, když má střed pod 2,2 m (`D_DOOR_H`); proto vchod 2,28 m a dveře 2,17 m.
- Zárubně, dveře a okenice jsou `final` a patří k vybavení; dveře a okenice jsou v etapě 2 otevřené ([[navrh_palac_obydli_etapy]] kap. 0.1).

### 4.5 Místnosti

| Místnost | Rozměr uvnitř | Podlaha | Strop |
|---|---|---|---|
| Světnice (východní) | s = 14,97–20,6; n = 0,7–6,05 (5,63 × 5,35 m) | prkna na podvalech (`plank_floor`) | trámkový, spodek 2,3 m |
| Síň a komora (západní) | s = 10,9–14,73; n = 0,7–6,05 (3,83 × 5,35 m) | udusaná hlína | bez stropu, otevřeno do krovu |
| Půda nad světnicí | nad stropem | prkna stropu | výška 0–1,6 m, přístup žebříkem ze síně otvorem ve štítu příčky |

- **Příčka je západně od středního sloupu krovu**, aby byla světnice větší (Jirka 16. 11. 2026); sloup s = 15,3 stojí ve světnici 23 cm od příčky.
- **Strop světnice** (`Palac_Obydli_Strop`): 6 trámků 14 × 18 cm ve směru východ–západ po 0,9 m (n = 1,1 až 5,6), prkna 4 cm. Leží v zářezech srubové příčky a srubu východní stěny, žádné další sloupy. U jižní zdi je otvor asi 1,7 × 1,2 m pro dymník a komín: trámky n = 1,1 a 2,0 jsou tam přerušené a uložené do výměny, na které visí dymník ([[navrh_palac_obydli_pec]]).
- **Podlaha světnice** (`Palac_Obydli_Podlaha`): prkna na podvalech. Předpoklad: končí u soklu pece (s = 15,96–17,56; n = 0,72–2,32) a u podezdívky příčky.

### 4.6 Pec s nístějí a komín

Stavba `Palac_Obydli_Ohniste` (typ `hearth`): [[navrh_palac_obydli_pec]]. Komín prochází krytinou (4.1), dymník visí na výměně stropu (4.5).

### 4.7 Okap (`Palac_Obydli_Okap`, typ `gutter`, `final`)

- **Žlab:** vydlabaný kmen Ø 20 cm pod severním okapem, n = 6,85; s = 9,6–21,6. Západním koncem přesahuje přes korunu `Palac_pricka_1` (1,0–1,4 m) do západní místnosti. Spád 1 % k západu, od kovárny (vrch 2,25 m u východního konce → 2,13 m u západního). Nesou ho rozsochy zaražené u stěny. Výšku žlabu upřesní postavená krytina.
- **Sud** (Ø asi 0,6 m) stojí v západní místnosti za `Palac_pricka_1` pod koncem žlabu: střed s ≈ 9,7; n ≈ 6,85, 0,1 m od líce příčky (Jirka 23. 11. 2026). Patří ke stavbě `Palac_Obydli_Okap` a je samostatný actor, polohu lze doladit podle vizuálu. Svod se nedělá (Jirka 16. 11. 2026), zápraží i cesta ke kovárně zůstávají volné.
- **Vyústění je dočasné.** Až bude určená cisterna, voda se přesměruje.

### 4.8 Vybavení (orientačně, pro game designera)

- **Otvory:** zárubně, dveře a okenice (otevřené, kap. 4.4), žebřík na půdu ze síně.
- **Světnice:** tři lůžka 2,0 × 0,8 m (dvě u východní stěny, jedno u severní), stůl 1,2 × 0,7 m u okénka, dvě truhly.
- **Síň:** hranice dřeva u západní stěny, ponk u střílny s = 14, police na osobní věci.
- Tři osoby se vejdou pohodlně, čtvrtá v nouzi.

## 5. Dostavba 05

Stavby, typy a sady jsou v [[navrh_palac_obydli_etapy]] kap. 0.3 (pec v [[navrh_palac_obydli_pec]]).

- **Složka:** `Stavby/Palac` (staveniště `Stavby/Palac/Obydli/Stavenisko`).
- **Sdílené rozměry:** `tools/ruin/palac_spec.py` (`D_*`, `obydli()`); čte ho 03 i 05. Postup po změně čísel: [[stav_palac_obydli]] (*Souhrn specifikace*).
- **Suť:** uvnitř domu a na zápraží uklizená (`clear_poly`).
- **Ruční doladění (samostatné actory, capture):** patní kameny sloupů, plotna, poklop ústí, práh vchodu, rozsochy žlabu, sud.

## 6. Vazby, kolize, pořadí

- Sloupy u jižní zdi nesmí stát ve výklencích střílen (s = 13,35–14,65 a 18,35–19,65).
- Sokl pece (s = 15,96–17,56) nesmí zasahovat do výklenku střílny s = 19 (mezera 0,79 m).
- Komín se nesmí dotknout krokví 16,26 a 17,26; strop a krytina kolem něj nechávají otvor (4.1, 4.5).
- Sud okapu stojí v západní místnosti za `Palac_pricka_1`, mimo zápraží; žlab nad příčkou se nesmí dotknout její koruny.
- **Kovárna ve východní místnosti:** výheň aspoň 6 m od východního štítu domu (dřevěná střecha); z domu se ke kovárně neprojde, ze zápraží vede průchod v `Palac_pricka_2` (kap. 3).
- **Sdílené soubory s kovárnou:** `constructions.json` jen generátorem, `manual_edits.json` a `constructions_edits.json` se nepřepisují.
- **Pořadí:** [[navrh_palac_obydli_etapy]] kap. 0.4.

## 7. Ověření

- `tools/checks/run_checks.py --only obydli`: žádné kameny bez podpory, průniky dřeva se zdivem jen v zářezech a uloženích.
- **Zamčená `base`:** hodnoty z [[navrh_palac_obydli_etapy]] kap. 0.7 v `palac_spec.py` se nezměnily a kontroly etapy 1 ([[navrh_palac_obydli_stavenisko]] kap. 9.4) procházejí.
- Koruna `Palac_J` je v s = 10,1–21,4 všude nad vrchem krytiny; mezi krytinou a `Palac_J` není po lemování mezera větší než 5 cm.
- Vrch komína je aspoň 0,5 m nad korunou `Palac_J` v okruhu 1,5 m od komína; komín se nedotýká krokví.
- Každý sloup stojí na patním kameni, každá krokev leží na třech podporách.
- Krytina pokrývá aspoň 99,5 % půdorysu domu (s = 10,1–21,4; n = 0,7–6,3); latě zavětrování jsou beze změny.
- Sklon střechy je 16° ± 1°.
- Zdí neprosvítá: srub, srovnané příčky, podezdívky a štíty jsou souvislé (mezera u příčky do 7 cm je pod krytinou).
- Vchod má volný průchod 1,0 × 2,28 m, dveře do světnice 1,0 × 2,17 m, práh nejvýš 45 cm.
- Světlá výška ve světnici je aspoň 2,3 m, v síni pod vaznicí aspoň 2,7 m.
- Zápraží má v s = 13,4–21,4 volnou šířku aspoň 2,0 m; průchod v `Palac_S` i průchod ke kovárně zůstávají volné v šířce aspoň 1,2 m.
- Žlab má spád k západu, konec nad sudem v západní místnosti a nedotýká se koruny `Palac_pricka_1`. Pozor: typ `gutter` počítá spád k `+c`, směr ověřit v datech.
- Náhled: `tools/checks/preview3d.py obydli <out.png> [--stage 1|2]` (zvenku od nádvoří průchodem, ze zápraží k průchodu ke kovárně, půdorys).

## 8. Rozdíly proti návrhu ve východní místnosti

Zavržená varianta u věže: [[navrh_palac_obydli]].

## 9. Etapa 1: rozestavěná stavba (hráč přichází poprvé)

Přesunuto do [[navrh_palac_obydli_stavenisko]] (kap. 9.1–9.6 tam mají stejná čísla); postavená verze a odchylky (dřív 9.2a) jsou v [[stav_palac_obydli]].

## 10. Předpoklady a otevřené otázky

- **Předpoklad („podložené ve dvou třetinách"):** čteno jako střední vaznice pod krokvemi ve 2/3 délky.
- **Předpoklad (vítr):** převládá západní až severozápadní. V podkladech to není.
- **Předpoklad (podlaha):** podlaha světnice končí u soklu pece.
- **Sklep:** je jen v návrhu dat a ležel by pod síní. Až se bude stavět, je potřeba vyřešit dvě věci: severní srubová stěna síně (s = 10,9–15) by stála nad klenbou a propadlé místo klenby nesmí být pod podezdívkou. Výhoda: vstup do sklepa přímo ze síně. Nad sklepem by stál i sud okapu v západní místnosti (s ≈ 9,7).
- **Rozšíření o podsíň:** pokud se počítá s pozdějším zastřešením zápraží, je lepší postavit severní stěnu rovnou 3,0 m vysokou. Krov by byl o 0,5 m výš, a tím i komín. Srub už stojí (2,5 m), takže by to znamenalo změnu sady `base`.
- **Riziko (kouř):** na koncích domu (s = 10–11,5 a 20,5–21,5) je jižní zeď vyšší než komín (5,5–6,0 m) a v 1. patře má okenní otvory. Za jižního větru může kouř srážet dolů.
- **Riziko (déšť od jihu):** u komína je koruna `Palac_J` jen 0,1–0,5 m nad krytinou. Hnaný déšť od útesu jde přes zeď rovnou na lemování.
- **Neřeší se:** cisterna, přístřešky pro hrubé práce a společný stůl, venkovní ohniště.

## 11. Náčrt slovy

- **Půdorys:** obdélník 11,3 × 5,6 m u jižní zdi prostřední místnosti. Jižní stranu tvoří `Palac_J`, obě boční stěny stojí na příčkách, severní je nový srub. Srubová příčka v s = 14,85 dělí dům na světnici (východ, větší) a síň (západ). Pec s nístějí je ve světnici u jižní zdi, střední sloup krovu stojí hned za příčkou. Vchod je v severní stěně do síně, šikmo proti průchodu v `Palac_S`. Před domem zápraží 2,3 m, z něj na východ průchod ke kovárně. Žlab vede přes západní příčku do sudu v západní místnosti.
- **Řez jih–sever:** u jižní zdi sloup s pozednicí (vrch 4,03 m), krokve klesají 16° přes vaznici (vrch 3,02 m v n = 4,4) na srubovou stěnu (vrch 2,50 m v n = 6,2) a přesahují ji o 0,6 m. U jižní zdi stoupá komín do 5,3 m, koruna zdi je vedle něj 4,4–4,8 m. Ve světnici strop se spodkem trámků 2,3 m, nad ním půda.
- **Boční stěna:** dole stará příčka srovnaná kamenem na 1,4 m, nad ní kulatina do 2,5 m, nad tím trojúhelník svislých prken pod střechu.
- **Pohled od nádvoří:** přes nízkou zeď a průchodem je vidět srubová stěna s dveřmi, nad zdí paláce vykukuje prkenná střecha ze surového dřeva stoupající k jižní zdi a nad ní komín.
