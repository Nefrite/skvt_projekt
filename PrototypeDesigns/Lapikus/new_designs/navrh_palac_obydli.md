# Návrh: Palac_Obydli – obytná stavba posádky ve východní části paláce

Specifikace od architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **návrh finální stavby, nepostaveno. Vybraná varianta C** (pultová střecha opřená o jižní zeď a věž, rozhodl Jirka 14. 11. 2026). Náčrt: `navrh_palac_obydli.png` (schéma, ne přesný model). Nahrazuje východní místnost ze staršího `navrh_palac_posadka.md`.

**ZAVRŽENÁ VARIANTA (stav 15. 11. 2026).** Dům u věže se stavět nebude: ve východní místnosti má být kovárna a komín u věže má špatný tah. Platí `navrh_palac_obydli_stred.md` (dům v prostřední místnosti). Tento dokument zůstává jen pro srovnání (rozdíly jsou v kap. 8 platného návrhu) a neaktualizuje se.

## 1. Zadání

- **Odkud:** Jirka.
- **Herní účel:** finální obydlí pro dva až tři členy posádky, s možností zimního vytápění.
- **Očekávání:**
  - ubytování dvou až tří postav,
  - uložení osobních věcí (hlavní sklad je v přízemí věže),
  - malý stůl pro drobnou práci za špatného počasí,
  - hrubé práce, společné jídlo a vaření v době stavby jsou venku pod jinými přístřešky.
- **Prostředky:** kámen z hradu na podezdívky, dřevo z okolního lesa, hrubé opracování (rychle, levně, prakticky).
- **Dvě etapy hry:** v první se stavba teprve staví (stojí trámy a podezdívky), ve druhé je hotová. Tento dokument popisuje hotovou stavbu. Stav první etapy se určí později (kap. 9).
- **Cisterna se neřeší.** Okapy budou, ale její poloha je zatím otevřená.

## 2. Výchozí stav (spočítáno z dat, 11/2026)

**Souřadnice paláce:** `s` v metrech podél `Palac_J` od jejího prvního bodu (UE −2350 / −50), `n` v metrech kolmo od osy `Palac_J` k severu. Jednotkové vektory v UE: `s` = (0,9758; −0,2184), `n` = (−0,2189; −0,9757). Výšky jsou v metrech nad terénem (v datech rovina Z 3129, v levelu se může lišit).

Východní místnost má uvnitř 9,35 × 8,1 m (s = 21,4–30,75, n = 0,7–8,8).

| Strana | Zeď | Tloušťka | Koruna | Otvory |
|---|---|---|---|---|
| jih | `Palac_J` | 1,4 m | s 21,5–23,5: 5,5–6,4; s 24–25,5: 4,7–5,1; s 26–28,5: 3,9–4,3; s 29–31: 5,5–6,7 | střílny s výklenkem v s = 25 a 29 (výklenek 0,55–2,7 m, uvnitř 1,3 m široký) |
| sever | `Palac_S` | 1,4 m | 0,7–1,3; u věže 2,0–2,7 | dveře s = 27 (mezera 26,45–27,55 až k zemi) |
| západ | `Palac_pricka_2` (osa s = 21,0) | 0,8 m | 0,8–1,1 | dveře n = 4,25–5,25 (až k zemi) |
| východ | věž `Vez_Z` (líc s = 30,75) | 2,5 m | 9–13,5 | okno 1. patra věže: n = 5,05–5,95, výška 5,1–6,5 m |

- Terén v místnosti je v datech rovný.
- Suť uvnitř: asi 9 kamenů u zdí.

## 3. Úpravy 03 (zřícenina)

**Ne.** Zřícenina se nemění. Dozdívky stojí na korunách jako dostavba 05, stejně jako u ostrohu.

## 4. Cílová struktura

Dům zabírá jižní část místnosti v celé délce: s = 20,6–30,75 (západní stěna stojí na příčce), n = 0,7–6,3. Uvnitř 49 m². Mezi domem a nízkou severní zdí paláce zůstává zápraží 2,3 m.

### 4.1 Krov (pultová střecha, spád k severu)

| Prvek | Průřez | Počet / délka | Poloha | Na čem leží |
|---|---|---|---|---|
| Sloupy u jižní zdi | 20 × 20 cm | 5 ks, výška 3,83 m | n = 0,85; s = 21,6 / 23,9 / 26,1 / 27,9 / 30,5 | na plochém kameni na terénu, těsně u líce `Palac_J`, mimo výklenky střílen |
| Horní pozednice | 20 × 20 cm | 9,3 m (2 kusy, spoj nad sloupem s = 26,1) | n = 0,85, vrch 4,03 m | na sloupech |
| Střední vaznice | 20 × 24 cm | 10,0 m (2 kusy, spoj nad příčkou) | n = 4,4, vrch 3,02 m | sloup u věže (s = 30,55), srubová příčka (s = 26,0), volný sloup v síni (s = 23,7), západní stěna (s = 21,0) |
| Dolní pozednice | poslední trám srubu | viz 4.2 | n = 6,2, vrch 2,50 m | severní srubová stěna |
| Krokve | 18 × 22 cm | 11 ks, délka 6,3 m | s = 20,7 až 30,6 po 0,99 m; od n = 0,75 po n = 6,8 | horní pozednice, střední vaznice, dolní pozednice; přesah 0,5 m za severní stěnu |

- **Sklon:** 16°. Střední vaznice je ve dvou třetinách délky krokve od jižní zdi.
- **Krytina:** stejná skladba jako `Ostroh_Krov`: latě napříč, prkna po spádu 22–30 cm, lišty přes spáry, krycí prkna přes krokve. Prkna jsou ve dvou délkách (3,4 + 3,2 m), horní řada přesahuje dolní o 0,25 m nad latí. Všechno dehtované (`tar`).
- **Plocha střechy:** s = 20,3–30,75 × 6,3 m, asi 66 m². Na západě přesah 0,3 m za příčku.
- **Lemování:** podél `Palac_J` (horní okraj) a podél věže (východní okraj) prkno 20 cm na stojato, přitlačené ke zdi a zamazané jílem.
- **Vrch krytiny u jižní zdi** je asi 4,3 m.

### 4.2 Stěny

| Stěna | Konstrukce | Poloha | Výška |
|---|---|---|---|
| Severní | srub z kulatiny Ø 22 cm, 9 řad, na podezdívce | osa n = 6,2; s = 20,6–30,75 (2 délky, spoj v nároží s příčkou) | podezdívka 0–0,45 m, srub 0,45–2,50 m |
| Příčka | srub z kulatiny Ø 22 cm na podezdívce | osa s = 26,0; n = 0,7–6,2 | do 2,50 m, nad tím prkenný štít pod střechu |
| Západní | srub na koruně `Palac_pricka_2` | osa s = 21,0; n = 0,7–6,2 | koruna příčky srovnaná na 1,1 m, srub 1,1–2,50 m, nad tím prkenný štít pod střechu |
| Jižní | stojící `Palac_J` | | nízká koruna dozděná pod střechu (4.3) |
| Východní | stojící věž `Vez_Z` | | beze změny |

- **Spáry srubu:** vymazané mechem a hlínou (vizuálně tmavší výplň mezi kulatinami).
- **Prkenné štíty:** svislá prkna s lištami, bez úpravy (`raw`).
- **Úprava dřeva:** srub a sloupy `raw`, podlaha `raw`, krov a krytina `tar`.

### 4.3 Kamenné části (kámen z rozvalin, jako `Ostroh_Dostavba`)

| Část | Kde | Rozměr |
|---|---|---|
| Podezdívka severní stěny | osa n = 6,2; s = 21,4–30,75, přerušená ve dveřích | 0,45 × 0,45 m |
| Podezdívka příčky | osa s = 26,0; n = 0,7–6,0, přerušená ve dveřích | 0,45 × 0,45 m |
| Srovnání koruny `Palac_pricka_2` | n = 0,7–6,2, včetně zazdění dveří příčky | na 1,1 m, v celé tloušťce 0,8 m |
| Dozdívka koruny `Palac_J` | s = 25,5–29,0, kde je koruna pod 4,3 m | 0,45 m na vnitřní polovině koruny, až pod střechu (0–0,4 m) |

### 4.4 Otvory

| Otvor | Kde | Rozměr | Poznámka |
|---|---|---|---|
| Vchod | severní stěna, s = 24,6–25,6 | 1,0 × 2,2 m | do síně; práh v úrovni podlahy, nadpraží je řada srubu |
| Dveře do světnice | příčka, n = 4,5–5,5 | 1,0 × 2,2 m | sloupek střední vaznice tvoří zárubeň |
| Okénko světnice | severní stěna, s = 27,5–28,1 | 0,6 × 0,6 m, parapet 1,3 m | okenice, bez skla |
| Okénko síně | severní stěna, s = 22,6–23,1 | 0,5 × 0,5 m, parapet 1,3 m | okenice |
| Střílny `Palac_J` | s = 25 (síň), s = 29 (světnice) | stávající | světlo a výhled na jih, výklenek jako police |

### 4.5 Místnosti

| Místnost | Rozměr uvnitř | Podlaha | Strop |
|---|---|---|---|
| Světnice (u věže) | s = 26,1–30,75; n = 0,7–6,05 (4,65 × 5,35 m) | prkna na podvalech (`plank_floor`) | trámkový, spodek 2,3 m |
| Síň a komora (u příčky) | s = 21,4–25,9; n = 0,7–6,05 (4,45 × 5,35 m) | udusaná hlína | bez stropu, otevřeno do krovu |
| Půda nad světnicí | nad stropem | prkna stropu | výška 0–1,6 m, přístup žebříkem ze síně otvorem ve štítu příčky |

- **Strop světnice:** 6 trámků 14 × 18 cm ve směru východ–západ po 0,9 m (n = 1,1 až 5,6), prkna 4 cm. Na západě leží v zářezech srubové příčky, na východě na průvlaku 16 × 20 cm u stěny věže (na třech sloupech: jižní sloup s = 30,5, sloup vaznice s = 30,55 a nový sloupek u severní stěny). V rohu nad ohništěm je otvor pro dymník.

### 4.6 Ohniště

- **Kde:** u stěny věže, s = 29,75–30,75; n = 1,5–2,9.
- **Základ:** kamenný blok 1,0 × 1,4 m, výška 0,5 m, z kamene rozvalin.
- **Dymník:** proutěný koš vymazaný hlínou, spodní okraj 1,7 m, zužuje se ke stropu.
- **Komín:** 0,6 × 0,6 m, proutí s hlínou, prochází stropem a střechou u s = 30,4; n = 2,2 a končí 1,0 m nad krytinou (asi 5,0 m nad terénem).
- Stěna věže za ohništěm je kamenná, bez úpravy.

### 4.7 Okap

- **Žlab:** vydlabaný kmen Ø 20 cm pod severním okapem, n = 6,85; s = 20,4–30,7. Spád 1 % k východu (vrch 2,25 → 2,15 m). Nesou ho vidlice zaražené u stěny.
- **Svod:** koryto od východního konce žlabu přes zápraží a přes nízké místo `Palac_S` (s = 29,3, koruna 0,7 m) na nádvoří, konec u n = 10,7.
- **Vyústění je dočasné.** Až bude určená cisterna, svod se přesměruje. Poloha svodu má být parametr.

### 4.8 Vybavení (orientačně, pro game designera)

- **Světnice:** tři lůžka 2,0 × 0,8 m (u jižní zdi, u příčky, u severní stěny), stůl 1,2 × 0,7 m u okénka, dvě truhly.
- **Síň:** hranice dřeva u západní stěny, ponk u střílny s = 25, police na osobní věci.
- Tři osoby se vejdou pohodlně, čtvrtá v nouzi.

## 5. Dostavba 05

| Stavba | Typ | Obsah |
|---|---|---|
| `Palac_Obydli_Krov` | **nový** (pracovně `pult_roof`), krytina sdílená s `fan_roof` | sloupy, pozednice, vaznice, krokve, krytina, lemování |
| `Palac_Obydli_Srub` | **nový** (pracovně `log_wall`) | severní stěna, příčka, západní stěna, prkenné štíty, otvory |
| `Palac_Obydli_Kamen` | existující `stone_addon` | podezdívky, srovnání příčky, dozdívka koruny `Palac_J` |
| `Palac_Obydli_Strop` | nový, nebo rozšíření `tower_floor` | průvlak, trámky, prkna, otvor pro dymník |
| `Palac_Obydli_Podlaha` | existující `plank_floor` | podlaha světnice |
| `Palac_Obydli_Ohniste` | **nový** | základ, dymník, komín |
| `Palac_Obydli_Okap` | **nový** (malý) | žlab, vidlice, svod |

- **Složka:** `Stavby/Palac`.
- **Sdílené rozměry:** nový `tools/ruin/palac_spec.py` (osy stěn, výšky pozednic a vaznice, sklon, polohy sloupů a otvorů). 03 z něj zatím nic nečte, ale dozdívka koruny a čištění suti z něj berou obrys.
- **Suť:** uvnitř domu a na zápraží uklizená (`clear_rubble`).
- **Ruční doladění (`loose`):** práh vchodu, patní kameny sloupů, vidlice žlabu.

## 6. Vazby, kolize, pořadí

- Sloupy u jižní zdi nesmí stát ve výklencích střílen (s = 24,35–25,65 a 28,35–29,65).
- Volný sloup v síni (s = 23,7; n = 4,4) nechává průchody aspoň 1,2 m na všechny strany.
- Svod kříží zápraží na východním konci (s = 29,3), mimo cestu od původních dveří (s = 27) ke vchodu (s = 25).
- Krytina je pod parapetem okna věže (v n = 5,5 asi 3,0 m, parapet 5,1 m). Okno se nezakrývá.
- Komín je 3 m jižně od okna věže.
- **Pořadí:** `Palac_Obydli_Kamen` → `Palac_Obydli_Krov` (bez krytiny) → `Palac_Obydli_Srub` → krytina → `Palac_Obydli_Strop`, `Palac_Obydli_Podlaha`, `Palac_Obydli_Ohniste`, `Palac_Obydli_Okap`. Dozdívka koruny `Palac_J` bere výšku z krovu, stejně jako u ostrohu.

## 7. Ověření

- `tools/checks/run_checks.py`: žádné kameny bez podpory, průniky dřeva se zdivem jen v zářezech a uloženích.
- Každý sloup stojí na terénu nebo patním kameni, každá krokev leží na třech podporách.
- Krytina pokrývá aspoň 99,5 % půdorysu domu (s = 20,6–30,75; n = 0,7–6,3).
- Mezi krytinou a `Palac_J` ani věží není mezera větší než 5 cm (po dozdívce a lemování).
- Zdí neprosvítá: srub, podezdívky a dozdívka koruny jsou souvislé.
- Sklon střechy je 16° ± 1°.
- Vchod i dveře do světnice mají volný průchod 1,0 × 2,2 m, práh nejvýš 45 cm.
- Světlá výška ve světnici je aspoň 2,3 m, v síni pod střední vaznicí aspoň 2,7 m.
- Zápraží má volnou šířku aspoň 2,0 m.
- Žlab má spád k východu a svod končí za vnějším lícem `Palac_S`.
- Náhled: `tools/checks/preview3d.py` (zvenku od nádvoří, zevnitř ze světnice a ze síně).

## 8. Zvažované varianty

| Varianta | Popis | Proč ne |
|---|---|---|
| A | volně stojící áčko 5 × 6 m, hřeben sever–jih | jen 24 m², zimní vytápění obtížné |
| B | áčko na severní zdi, hřeben východ–západ | zastaví původní dveře, jižní okap nemá kam odtékat |
| **C** | **pult o jižní zeď a věž, hloubka 5,35 m** | **vybraná** |
| D | jeden pult přes celý původní půdorys (8,1 m) | krokve 10 m, střecha 97 m², spád 15° s nastavovanými prkny, velký nevytápěný objem |
| E | C a krytá podsíň místo zápraží | možné rozšíření později; C tomu nebrání, jen by severní stěna musela být 3,0 m vysoká |

## 9. Předpoklady a otevřené otázky

- **Předpoklad (stěny):** srub z kulatiny. Jirka to zatím nepotvrdil. Druhá možnost je kamenná dostavba 0,45 m jako u ostrohu: méně dřeva, ale studenější.
- **Předpoklad („podložené ve dvou třetinách"):** čteno jako střední vaznice pod krokvemi ve 2/3 délky.
- **Předpoklad:** dveře v `Palac_pricka_2` se zazdí (teplo). Kdyby prostřední místnost paláce měla později sloužit jako dílna, dají se nechat jako zadní vchod.
- **Otázka pro game designera:** okno 1. patra věže je asi 2,1 m nad střechou. Má to být cesta pro postavu (seskok z věže na střechu), nebo se má zamezit?
- **Otázka (rozšíření E):** pokud se počítá s pozdější podsíní, je lepší postavit severní stěnu rovnou 3,0 m vysokou. Krov by pak byl o 0,5 m výš a dozdívka koruny `Palac_J` větší.
- **K určení později:** stav první etapy (stavba v běhu). Přirozené mezistavy podle pořadí stavění: (1) podezdívky a srovnaná příčka, (2) sloupy, pozednice a vaznice, (3) krokve bez krytiny, (4) srub do poloviny výšky.
- **Riziko (kouř):** jižní zeď i věž jsou vyšší než komín, za některých větrů bude ohniště kouřit.
- **Riziko (zatékání):** po stěně věže steče při dešti hodně vody na východní okraj střechy. Lemování tam je nejslabší místo stavby.
- **Neřeší se:** cisterna, přístřešky pro hrubé práce a společný stůl, venkovní ohniště.

## 10. Náčrt slovy

- **Půdorys:** obdélník 10,15 × 5,6 m v jihovýchodním koutě paláce. Jižní stranu tvoří `Palac_J`, východní věž, západní stojí na `Palac_pricka_2`, severní je nový srub. Srubová příčka v s = 26,0 dělí dům na světnici u věže a síň u příčky. Vchod je v severní stěně do síně, 2 m západně od původních dveří paláce. Před domem zápraží 2,3 m a nízká severní zeď paláce.
- **Řez jih–sever:** u jižní zdi sloup s pozednicí (vrch 4,03 m), krokve klesají 16° přes střední vaznici (vrch 3,02 m ve n = 4,4) na srubovou stěnu (vrch 2,50 m ve n = 6,2) a přesahují ji o 0,5 m. Pod okapem žlab. Ve světnici strop se spodkem trámků 2,3 m, nad ním půda.
- **Pohled od nádvoří:** za nízkou zdí paláce srubová stěna 2,5 m s dveřmi a dvěma okénky, nad ní tmavá prkenná střecha stoupající k jižní zdi. Vpravo se střecha opírá o stěnu věže, u ní komín. Nad střechou okno věže.
