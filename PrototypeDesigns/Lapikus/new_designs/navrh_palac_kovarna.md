# Návrh: Palac_Kovarna – provizorní kovárna pod přístřeškem

Specifikace od architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **návrh, nepostaveno.** Náčrt: `navrh_palac_kovarna.png` (schéma, ne přesný model).

**Připravenost (15. 11. 2026)** – podrobně `..\CHECKLIST_assets_navrhy.md`, kap. 6.1:
- **Vybavení je hotové** jako vlastní procedurální props (`tools/meshes/mesh_props.py`), zatím nerozmístěné: špalek `SM_RuinStump`, kovadlina `SM_RuinAnvil`, měchy s rámem a výfučnou `SM_RuinBellows`, páka (loupaná tyč `SM_RuinPole`), kalicí sud `SM_RuinBarrel`, **šlapací brus** `SM_RuinGrindstoneTreadle` s třínohou stoličkou `SM_RuinStool`, ponk se svěrákem `SM_RuinWorkbench`, kleště, kladivo, sekáč (`SM_RuinTongs`, `SM_RuinHammer`, `SM_RuinChisel`), hřebovnice `SM_RuinNailHeader`, truhlík na uhlí `SM_RuinCoalBox` s volným víkem `SM_RuinCoalBoxLid`, hranice dřeva `SM_RuinWoodpile`, železné pruty `SM_RuinIronBars`, koš `SM_RuinBasket`.
- **Hotové dílce stavby:** loupaná kulatina `SM_RuinLog` (krokve), dílce proutěné stěny `SM_RuinWattlePanel`, dymník `SM_RuinSmokeHood`, komín `SM_RuinChimney`, žlab `SM_RuinGutter`.
- **Chybí:** typy staveb `pult_roof`, `hearth`, `wattle_wall`, `gutter`, rozmístění props, `tools/ruin/palac_spec.py`. Dále žhavé uhlí ve výhni, saze, udusaná hlína, oheň a kouř.

## 1. Zadání

- **Odkud:** Jirka (14. 11. 2026).
- **Herní účel:** provizorní kovárna posádky. Vyrábí základní spojovací materiál (hřebíky, skoby, kramle) a dělá základní opravy zbraní.
- **Požadavky:**
  - práce pod přístřeškem;
  - výheň, od které je teplo i v zimě;
  - brusný kotouč;
  - sud na chlazení a kalení;
  - zásoba dřeva.
- **Umístění:** východní místnost paláce u věže. Obydlí je kvůli tomu v prostřední místnosti (`navrh_palac_obydli_stred.md`).

## 2. Výchozí stav (spočítáno z dat, 11/2026)

**Souřadnice paláce:** `s` v metrech podél `Palac_J` od jejího prvního bodu (UE −2350 / −50), `n` v metrech kolmo k severu. Jednotkové vektory v UE: `s` = (0,9758; −0,2184), `n` = (−0,2189; −0,9757). Výšky v metrech nad terénem (v datech rovina Z 3129).

Východní místnost má uvnitř 9,35 × 8,1 m (s = 21,4–30,75; n = 0,7–8,8).

| Strana | Zeď | Koruna | Otvory |
|---|---|---|---|
| jih | `Palac_J` (1,4 m) | s 24–25,5: 4,7–5,1; s 26–28,5: 3,9–4,3; s 29–31: 5,5–6,7 | střílny s výklenkem v s = 25 a 29 |
| sever | `Palac_S` (1,4 m) | 0,7–1,3; u věže 2,0–2,7 | dveře s = 26,45–27,55, až k zemi |
| západ | `Palac_pricka_2` (osa s = 21,0) | podle návrhu domu srovnaná na 1,4 m, nad ní srub a štít domu | dveře zazděné |
| východ | věž `Vez_Z` (líc s = 30,75) | 9–13,5 | okno 1. patra věže: n = 5,05–5,95, výška 5,1–6,5 m |

- Terén v místnosti je v datech rovný.
- Východní štít domu je v s = 21,4. Jeho střecha je dehtovaná.

## 3. Úpravy 03 (zřícenina)

**Ne.**

## 4. Cílová struktura

Kovárna stojí v jihovýchodním koutě místnosti. Jižní stranu tvoří `Palac_J`, východní věž. Půdorys přístřešku: s = 25,1–30,75; n = 0,7–5,7 (asi 28 m²). Severní strana je otevřená, západní má lehkou stěnu.

### 4.1 Přístřešek (pultová střecha, spád k západu)

| Prvek | Průřez | Počet / délka | Poloha | Na čem leží |
|---|---|---|---|---|
| Sloupy u věže | 20 × 20 cm | 2 ks, výška 4,0 m | s = 30,55; n = 0,9 a 5,3 | na plochém kameni na terénu, těsně u líce věže |
| Východní pozednice | 20 × 20 cm | 4,8 m | s = 30,55; vrch 4,2 m | na sloupech, rozpětí 4,4 m |
| Sloupy na západě | 18 × 18 cm | 3 ks, výška 2,1 m | s = 25,5; n = 0,9 / 3,1 / 5,3 | na plochém kameni na terénu |
| Západní pozednice | 18 × 18 cm | 4,8 m | s = 25,5; vrch 2,3 m | na sloupech |
| Krokve | kulatina Ø 16 cm | 6 ks, délka 5,9 m | n = 0,9 / 1,8 / 2,7 / 3,6 / 4,5 / 5,4; od s = 30,65 po s = 25,1 | obě pozednice, přesah 0,4 m na západ |

- **Sklon:** 20° k západu. Vysoká strana je u věže, aby nad výhní bylo co nejvíc místa a komín vycházel v nejvyšším bodě.
- **Krytina:** latě a prkna po spádu s lištami, stejná skladba jako `Ostroh_Krov`, ale **bez dehtu** (`raw`). Dehet je nad výhní hořlavý.
- **Plocha střechy:** 5,0 × 6,0 m, asi 30 m².
- **Lemování:** prkno na stojato podél věže (horní okraj) a podél `Palac_J` (jižní okraj).
- **Výška pod střechou:** u věže 4,0 m, nad kovadlinou 3,3 m, u západní stěny 2,1 m.
- **Poměr k oknu věže:** vrch krytiny u věže je asi 4,5 m, tedy 0,6 m pod parapetem okna.

### 4.2 Stěny

| Strana | Řešení |
|---|---|
| Jižní | stojící `Palac_J`. Je všude vyšší než okraj střechy, bez dozdívky. |
| Východní | stojící věž. |
| Západní | stěna z proutí vypleteného mezi sloupy a kůly, omazaná hlínou. s = 25,5; n = 0,7–5,4; výška 1,9 m. Nad ní volný pruh pod střechou. |
| Severní | otevřená. Vstup a světlo. |

- **Západní stěna** chrání oheň před převládajícím větrem a dům před jiskrami.
- **Na zimu** se dá severní strana zčásti zavřít prkny. Není součástí návrhu.

### 4.3 Výheň, měchy a komín

| Prvek | Rozměr | Poloha |
|---|---|---|
| Výheň | kamenný stůl 1,2 × 1,0 m, výška 0,75 m, z kamene rozvalin, nahoře vymazaný hlínou; ohniště 0,4 × 0,4 m | u stěny věže: s = 29,75–30,75; n = 1,5–2,7 |
| Boční zídka | kámen, 0,3 × 1,0 m, výška 1,2 m | n = 2,7–3,0; chrání měchy před žárem, prochází jí výfučna |
| Měchy | kožený měch 1,7 × 0,8 m na dřevěném rámu ve výšce 0,9 m | podél věže: s = 29,9–30,7; n = 3,0–4,7 |
| Páka měchů | tyč 2,2 m zavěšená na krokvi | konec u kovadliny |
| Dymník | proutěný koš vymazaný hlínou, 1,4 × 1,2 m, spodní okraj 1,8 m | nad výhní |
| Komín | 0,5 × 0,5 m, proutí s hlínou | u stěny věže, střed s = 30,45; n = 2,1; prochází střechou mezi krokvemi n = 1,8 a 2,7; vrch 5,5 m |

- Komín je 3 m jižně od okna věže.
- Stěna věže za výhní je kamenná, bez úpravy.

### 4.4 Vybavení

| Prvek | Rozměr | Poloha (s; n) |
|---|---|---|
| Kovadlina na špalku | špalek Ø 0,5 m, vrch kovadliny 0,75 m | 28,5; 2,1 (1,0 m před výhní) |
| Kalicí sud | Ø 0,6 m, výška 0,8 m, s vodou | 28,9; 3,4 |
| Brus | pískovcový kotouč Ø 0,7 m na dřevěném rámu 1,2 × 0,6 m, osa 0,75 m, **šlapací** (kliková páka, ojnice, šlapadlo; rozhodl Jirka 14. 11. 2026), pod kotoučem korýtko s vodou; u něj třínohá stolička (sedátko Ø 32 cm, výška 45 cm) | 26,3–27,5; 4,0–4,6 (u otevřené strany kvůli světlu) |
| Ponk se svěrákem | 2,2 × 0,7 m, výška 0,85 m | u jižní zdi: 26,0–28,2; 0,75–1,45 |
| Nářadí | kleště, kladiva, sekáče na liště | na jižní zdi nad ponkem |
| Truhlík na dřevěné uhlí | 0,8 × 1,2 m, výška 0,8 m, s volným víkem (bez pantů, pokládá se bokem) | u západní stěny: 25,65–26,45; 2,0–3,2 |
| Zásoba dřeva | hranice 0,6 × 1,9 m, výška 1,4 m | u západní stěny: 25,65–26,25; 3,4–5,3 |
| Železo a hotové hřebíky | pruty, koš | ve výklenku střílny s = 29 |
| Hřebovnice | na menším špalku | u kovadliny |

- **Kovadlina, sud a výheň** jsou od sebe na krok, kovář se mezi nimi jen otáčí.
- **Výheň je v nejtmavším koutě.** Kovář potřebuje šero, aby poznal barvu rozžhaveného železa. Brus a ponk jsou naopak u světla.
- **Podlaha:** udusaná hlína.

### 4.5 Okap

- **Žlab:** vydlabaný kmen Ø 20 cm pod západním okapem, s = 24,95; n = 0,7–5,7, se spádem k severu.
- **Svod:** koryto od severního konce žlabu přes dvorek a přes nízké místo `Palac_S` (s = 24–25, koruna 0,7 m) na nádvoří.
- Vyústění je dočasné jako u domu, cisterna se neřeší.

### 4.6 Úprava dřeva

- Všechno dřevo `raw`. Žádný dehet.

## 5. Dostavba 05

| Stavba | Typ | Obsah |
|---|---|---|
| `Palac_Kovarna_Pristresek` | `pult_roof` (stejný nový typ jako `Palac_Obydli_Krov`) | sloupy, pozednice, krokve, krytina, lemování |
| `Palac_Kovarna_Stena` | **nový** (pracovně `wattle_wall`) | západní stěna z proutí a hlíny |
| `Palac_Kovarna_Vyhen` | stejný nový typ jako `Palac_Obydli_Ohniste`, rozšířený o boční zídku | výheň, zídka, dymník, komín |
| `Palac_Kovarna_Okap` | stejný jako `Palac_Obydli_Okap` | žlab, svod |
| `Palac_Kovarna_Vybaveni` | samostatné actory | měchy, kovadlina, sud, brus, ponk, truhlík, dřevo, nářadí |

- **Složka:** `Stavby/Palac`.
- **Sdílené rozměry:** `tools/ruin/palac_spec.py` (společně s domem).
- **Vybavení nejsou generované dílce.** Měchy, kovadlina, brus, sud a nářadí jsou hotové modely, které generátor jen rozmístí. Jsou to vlastní props ve stylu hradu (rozhodl Jirka 14. 11. 2026), všechny už existují.
- **Suť:** v celé východní místnosti uklizená (`clear_rubble`).
- **Ruční doladění (`loose`):** všechno vybavení.

## 6. Vazby, kolize, pořadí

- **Odstup od domu:** výheň je 8,3 m od východního štítu domu, západní okraj přístřešku 3,7 m. Podmínka z návrhu domu (výheň aspoň 6 m) je splněná.
- **Sloupy u věže** nesmí stát v místě výhně a měchů (n = 1,5–4,7), proto jsou jen dva a pozednice mezi nimi má rozpětí 4,4 m.
- **Sloup u jižní zdi** (s = 30,55; n = 0,9) je mimo výklenek střílny s = 29 (ten končí v s = 29,65).
- **Vstup:** původními dveřmi paláce (s = 27) na dvorek a odtud otevřenou severní stranou. Cesta musí zůstat volná v šířce aspoň 1,2 m.
- **Svod** vede po západním okraji dvorku, mimo cestu ode dveří.
- **Okno věže** je 0,6 m nad střechou. Platí stejná otázka jako u původního návrhu domu: může tudy postava z věže na střechu?
- **Pořadí:** `Palac_Kovarna_Pristresek` (bez krytiny) → `Palac_Kovarna_Vyhen` → krytina → `Palac_Kovarna_Stena`, `Palac_Kovarna_Okap`, vybavení.

## 7. Ověření

- `tools/checks/run_checks.py`: žádné průniky dřeva se zdivem mimo uložení.
- Každý sloup stojí na terénu nebo patním kameni, každá krokev leží na obou pozednicích.
- Krytina pokrývá aspoň 99 % půdorysu přístřešku mimo otvor komína.
- Sklon střechy je 20° ± 1°.
- Komín prochází střechou bez dotyku s krokvemi (vůle aspoň 10 cm) a končí aspoň 0,8 m nad krytinou.
- Mezi kovadlinou a výhní je 0,9–1,1 m, kalicí sud je do 1,5 m od obou.
- Kolem kovadliny, brusu a ponku zůstává průchod aspoň 1,2 m k otevřené severní straně.
- Světlá výška nad kovadlinou je aspoň 3,0 m.
- Žlab má spád k severu a svod končí za vnějším lícem `Palac_S`.
- Náhled: `tools/checks/preview3d.py` (ze dvorku od severu, zevnitř od ponku k výhni).

## 8. Varianty a zavržené možnosti

- **Spád střechy k severu (jako u domu):** styk s věží by byl po celé délce nad výhní a měchy, zatékalo by na ně.
- **Volně stojící přístřešek uprostřed místnosti:** výheň by neměla kamennou stěnu za zády a kouř by šel pod střechu.
- **Krytina z kůry:** kůry je dost, ale nad výhní je suchá kůra nejhořlavější možnost. Dá se použít jen na západní polovině střechy dál od komína.
- **Kovárna mimo palác (u hradby, na nádvoří):** dál od skladu ve věži a bez dvou hotových kamenných stěn.

## 9. Předpoklady a otevřené otázky

- **Předpoklad (umístění):** východní místnost paláce, jak jsme probírali u přesunu domu. Jirka to výslovně nepotvrdil.
- **Předpoklad (etapy):** kovárna stojí hotová už v etapě 1. Dům potřebuje hřebíky a kramle, takže kovárna musí být dřív.
- **Předpoklad (palivo):** výheň topí dřevěným uhlím. Zásoba dřeva v kovárně slouží na podpal a na pálení uhlí. Malý milíř nebo jáma na uhlí by byla někde mimo hrad, návrh ji neřeší.
- **Předpoklad (voda):** do sudu a korýtka brusu se nosí z potoka.
- **Otázka pro game designera:** okno věže nad střechou jako možná cesta postavy.
- **Riziko (kouř):** komín je pod stěnou věže vysokou 9–13,5 m. Tah bude slabý a kouř půjde po stěně k hlídce nahoře. Kove se ale ve dne a s přestávkami.
- **Riziko (zatékání):** po stěně věže stéká při dešti voda na horní okraj střechy. U otevřeného přístřešku to vadí méně než u domu, ale měchy jsou právě tam.
- **Riziko (rozpětí):** krokve Ø 16 cm na 5,1 m bez střední podpory. Pro lehkou krytinu to stačí, při pochybnosti přidat střední vaznici na dvou sloupech.
- **Neřeší se:** zimní zavření severní strany, milíř, cisterna.

## 10. Náčrt slovy

- **Půdorys:** obdélník 5,65 × 5,0 m v koutě mezi jižní zdí paláce a věží. Výheň je u věže blízko kouta, měchy za ní podél věže. Krok před výhní stojí kovadlina, vedle ní sud. U jižní zdi ponk. U západní stěny truhlík s uhlím a hranice dřeva. Brus je u otevřené severní strany. Před přístřeškem je dvorek, do kterého se vchází původními dveřmi paláce.
- **Řez východ–západ:** u věže vysoké sloupy s pozednicí ve 4,2 m, krokve klesají 20° k západu na pozednici ve 2,3 m. U věže stoupá komín nad střechu do 5,5 m. Pod ním dymník a kamenný stůl výhně. Na západě stěna z proutí a hlíny do 1,9 m, pod okapem žlab.
- **Pohled ze dvorku:** otevřená strana přístřešku, vpředu brus, vlevo za ním temný kout s výhní a měchy u stěny věže, vzadu ponk s nářadím na jižní zdi.
