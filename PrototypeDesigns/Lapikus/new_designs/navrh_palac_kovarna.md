# Návrh: Palac_Kovarna – provizorní kovárna pod přístřeškem

Specifikace od architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **vybraný návrh, staví se po krocích** (15. 11. 2026; hotové kroky 1–3, zbývá vybavení a úklid suti). Co je hotové a co zbývá, je v kap. 0. Náčrt: `navrh_palac_kovarna.png` je starší schéma, které se v hlavním (výheň v koutě) shoduje, v rozměrech ne; **platí tento text**.

## 0. Stav stavby proti návrhu (15. 11. 2026)

Všechno „hotovo“ znamená: je ve skriptech a datech a prošlo kontrolami mimo Unreal (`tools/checks/run_checks.py`). **V UE je ověřená úprava 03, kostra přístřešku a výheň** (Jirka 15. 11. 2026); krytina, stěna a okap zatím ne.

| Část návrhu | Stavba / místo | Stav | Poznámka |
|---|---|---|---|
| Úprava 03: `Palac_J` zanořená o řadu do země (kap. 3) | `03_ruin`, část `Palac` | ✅ hotovo | `z_offset` −0,31 m |
| Úprava 03: rozebraná koruna `Palac_J` u věže (kap. 3) | `03_ruin`, část `Palac` | ✅ hotovo | `breaches`; komín ji přesahuje o 0,3–1,5 m |
| Úprava 03: kapsa pro východní pozednici (kap. 3) | `03_ruin`, část `Palac` | ✅ hotovo | `kapsa` ve vnitřním líci `Palac_J` |
| Sloupy, pozednice, krokve (kap. 4.1) | `Palac_Kovarna_Pristresek` | ✅ hotovo | 4 sloupy na patních kamenech, 2 pozednice, 6 krokví |
| Krytina, latě, lišty (kap. 4.1) | `Palac_Kovarna_Pristresek` | ✅ hotovo | skladba jako `Ostroh_Krov`, vlastní kód (`pult._pult_cover`); prostup komína s mezerou 3 cm |
| Lemování u věže a u `Palac_J` (kap. 4.1) | `Palac_Kovarna_Pristresek` | ✅ hotovo | prkno 25 cm na stojato |
| Výheň: stůl, maz, ohniště (kap. 4.3) | `Palac_Kovarna_Vyhen` | ✅ hotovo | v koutě místnosti |
| Boční zídka s otvorem pro výfučnu (kap. 4.3) | `Palac_Kovarna_Vyhen` | ✅ hotovo | |
| Dymník, komín, výměny, závěsné tyče (kap. 4.3) | `Palac_Kovarna_Vyhen` | ✅ hotovo | |
| Žhavé uhlí, saze, oheň a kouř | – | ⏸ odloženo | rozhodnuto 15. 11. 2026 |
| Západní stěna z proutí (kap. 4.2) | `Palac_Kovarna_Stena` | ✅ hotovo | typ `wattle_wall` (`zr_stavby/stena.py`), dílce mezi sloupy, kůly na spojích |
| Žlab, vidlice, sud na vodu (kap. 4.5) | `Palac_Kovarna_Okap` | ✅ hotovo | typ `gutter` (`zr_stavby/okap.py`), 3 rozsochy, sud = samostatný actor |
| Měchy, páka (kap. 4.3) | `Palac_Kovarna_Vybaveni` | ⬜ zbývá rozmístit | prop `SM_RuinBellows` hotový |
| Kovadlina, sud, brus, ponk, nářadí, truhlík, železo (kap. 4.4) | `Palac_Kovarna_Vybaveni` | ⬜ zbývá rozmístit | všechny props hotové; chybí kód pro rozmístění (`loose`) |
| Hranice dřeva pod přesahem (kap. 4.4) | `Palac_Kovarna_Vybaveni` | ⬜ zbývá rozmístit | prop `SM_RuinWoodpile` hotový |
| Úklid suti ve východní místnosti (kap. 5) | `Sut` | ⬜ zbývá | `clear_rubble` zatím umí jen kamenné dostavby |
| Podlaha z udusané hlíny (kap. 4.4) | – | ⏸ odloženo | chybí materiál |
| Sdílené rozměry (kap. 5) | `tools/ruin/palac_spec.py` | ✅ hotovo | rám paláce, kovárna, úpravy 03 |
| Kontroly a náhled (kap. 7) | `run_checks.py --only palac`, `preview3d.py kovarna` | ✅ hotovo pro postavené části | pokrytí krytinou, lemování, stěna, žlab a sud; průchody kolem vybavení přibudou v kroku 4 |
| Ověření v Unrealu | – | ◐ částečně | úprava 03, kostra přístřešku a výheň ověřené (Jirka 15. 11. 2026, v pořádku); krytina, lemování, stěna a okap zatím ne |

**Odchylky postaveného od původního návrhu ze 14. 11. 2026:** výheň v koutě místo u věže dál od zdi; `Palac_J` zanořená o řadu, rozebraná u věže a s kapsou (původně žádná úprava 03); východní pozednice ve 4,24 m místo 4,2 m; u věže jeden sloup místo dvou; západní linie v s = 25,85 místo 25,5; západní pozednice ve 2,5 m místo 2,3 m; krokve 6,1 m s přesahem 0,9 m místo 0,4 m; komín v s = 30,0; n = 1,35 místo s = 30,45; n = 2,1; dymník na závěsných tyčích (návrh uložení neřešil); dřevo venku pod přesahem místo uvnitř; žlab do sudu bez svodu; krytina 3,5 cm od líce `Palac_J` (kameny koruny v s = 27–29 vystupují z líce v úrovni střechy); okapová hrana s = 24,85, žlab n = 0,72–5,9.

**Změny 15. 11. 2026** (dohodnuto s Jirkou při zahájení stavby):
- **Umístění potvrzeno:** východní místnost paláce.
- **Západní linie posunutá z s = 25,5 na s = 25,85** (sloupy, pozednice, stěna z proutí). Na původním místě končila stěna ve výklenku střílny s = 25 (výklenek je s = 24,35–25,65) a neměla o co dosednout. Vrch západní pozednice je kvůli zachování sklonu 20° ve 2,5 m (dřív 2,3 m), stěna z proutí 2,1 m (dřív 1,9 m).
- **Výheň v koutě místnosti** (Jirka 15. 11. 2026, večer; ruší dřívější polohu u věže v n = 1,5–2,7): stůl leží v koutě mezi `Palac_J` a věží (n = 0,72–1,9). Výklenek střílny s = 29 je hned vedle stolu a dává kolem výhně manipulační prostor, proto zůstává volný.
- **Celá `Palac_J` je posunutá po ose Z o jednu řadu kamene níž** (zanořená do země, počet řad se nemění) a **u věže je koruna rozebraná** tak, aby ji komín přesahoval (úprava 03, kap. 3). První pokus (ubrání horní řady, `drop_rows`) byl nedorozumění a pro tuto zeď je zrušený.
- **Rohový sloup u věže odpadl** (stála by v něm výheň). Východní pozednice je jižním koncem zapuštěná 0,3 m do `Palac_J` (kapsa, úprava 03), na severu leží na sloupu.
- **Komín je o jedno pole krokví jižněji:** střed s = 30,0; n = 1,35, mezi krokvemi n = 0,9 a 1,8 (vůle 12 cm), 20 cm od východní pozednice. Původní poloha (s = 30,45; n = 2,1) procházela pozednicí.
- **Svod zrušen, žlab ústí do sudu** u svého severního konce. Svod přes dvorek by postavě odřízl západní kout dvorku.
- **Krokve protažené o 0,5 m** (přesah 0,9 m za západní pozednici, okap v s = 24,95). Pod přesahem se zvenku podél západní stěny vyskládá dřevo, aby bylo kryté (Jirka 15. 11. 2026). Hranice dřeva proto není uvnitř kovárny.
- **Vybavení u západní stěny** se posouvá s ní (kap. 4.4).
- **Dymník visí na krokvích:** mezi krokvemi n = 0,9 a 1,8 jsou po obou stranách komína výměny (loupaná kulatina Ø 10 cm), z jejich konců vedou čtyři závěsné tyče Ø 5 cm k rohům spodního okraje dymníku. Původní návrh uložení dymníku neřešil.
- **Ohniště** je pod komínem (střed s = 30,0; n = 1,35), tedy u západní hrany stolu, na dosah od kovadliny.
- **Okno věže nad střechou:** neřeší se, nechává se, jak vyjde.
- **Postup stavby:** 1. `palac_spec.py` a přístřešek bez krytiny, 2. výheň a krytina, 3. stěna a okap, 4. vybavení a úklid suti. Kroky 1 a výheň ověřené v UE (15. 11. 2026), kroky 2 a 3 hotové mimo UE (15. 11. 2026, večer).
- **Krytina (krok 2):** latě 9 řad (nad a pod prostupem komína, jinak nejvýš po 0,9 m), prkna 22–30 cm po spádu od líce věže po okapovou hranu s = 24,85 (10 cm za konci krokví, nad osou žlabu), lišty přes spáry, prostup komína s mezerou 3 cm (prkna se kladou od jeho okrajů ven). Od líce `Palac_J` mezera 3,5 cm, protože kameny koruny v s = 27–29 leží v úrovni střechy a vystupují z líce. Lemování: prkno 25 cm na stojato u věže a podél `Palac_J`.
- **Stěna a okap (krok 3):** stěna z dílců proutí mezi sloupy, spodní pás 0,1 m mezi patními kameny, kůly Ø 9 cm na spojích dílců. Žlab Ø 20 cm (loupaný) na třech rozsochách v n = 0,9 / 3,1 / 5,3, vrch 12–20 cm pod krytinou, spád 1,5 % k severu; sud pod jeho koncem (s = 24,8; n = 5,9) je samostatný actor.

**Připravenost (15. 11. 2026)** – podrobně `..\CHECKLIST_assets_navrhy.md`, kap. 6.1:
- **Vybavení je hotové** jako vlastní procedurální props (`tools/meshes/mesh_props.py`), zatím nerozmístěné: špalek `SM_RuinStump`, kovadlina `SM_RuinAnvil`, měchy s rámem a výfučnou `SM_RuinBellows`, páka (loupaná tyč `SM_RuinPole`), kalicí sud `SM_RuinBarrel`, **šlapací brus** `SM_RuinGrindstoneTreadle` s třínohou stoličkou `SM_RuinStool`, ponk se svěrákem `SM_RuinWorkbench`, kleště, kladivo, sekáč (`SM_RuinTongs`, `SM_RuinHammer`, `SM_RuinChisel`), hřebovnice `SM_RuinNailHeader`, truhlík na uhlí `SM_RuinCoalBox` s volným víkem `SM_RuinCoalBoxLid`, hranice dřeva `SM_RuinWoodpile`, železné pruty `SM_RuinIronBars`, koš `SM_RuinBasket`.
- **Hotové dílce stavby:** loupaná kulatina `SM_RuinLog` (krokve), dílce proutěné stěny `SM_RuinWattlePanel`, dymník `SM_RuinSmokeHood`, komín `SM_RuinChimney`, žlab `SM_RuinGutter`.
- **Hotové (15. 11. 2026):** typy `pult_roof` bez krytiny (`05_constructions/zr_stavby/pult.py`) a `hearth` (`zr_stavby/ohniste.py`), sdílené rozměry `tools/ruin/palac_spec.py`, úpravy 03 (`z_offset`, `breaches`, `kapsa`), kontrola `run_checks.py --only palac`, náhled `preview3d.py kovarna`.
- **Hotové (15. 11. 2026, večer):** krytina a lemování v `pult_roof`, typy `wattle_wall` (`zr_stavby/stena.py`) a `gutter` (`zr_stavby/okap.py`), kontroly krytiny, stěny a okapu v `run_checks.py --only palac`.
- **Chybí:** rozmístění props, úklid suti. Žhavé uhlí ve výhni, saze, udusaná hlína, oheň a kouř se zatím nedělají (rozhodnuto 15. 11. 2026).

## 1. Zadání

- **Odkud:** Jirka (14. 11. 2026).
- **Herní účel:** provizorní kovárna posádky. Vyrábí základní spojovací materiál (hřebíky, skoby, kramle) a dělá základní opravy zbraní.
- **Požadavky:**
  - práce pod přístřeškem;
  - výheň, od které je teplo i v zimě;
  - brusný kotouč;
  - sud na chlazení a kalení;
  - zásoba dřeva.
- **Umístění:** východní místnost paláce u věže (potvrdil Jirka 15. 11. 2026). Obydlí je kvůli tomu v prostřední místnosti (`navrh_palac_obydli_stred.md`).

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
   - Týká se celé délky zdi, tedy i prostřední místnosti. **Koruny `Palac_J` v `navrh_palac_obydli_stred.md` (kap. 2 a 3) jsou proto o 0,31 m výš, než je skutečnost.**
2. **Rozebraná koruna u věže**, aby ji komín přesahoval: `breaches` `{s0: 29,6; s1: 33; floor: 6,1; slope_l: 0,8}` (`J_BREACH`). Je to rozpad, ne rovné zarovnání: koruna vychází ve stupních po řadách 5,2 m (s = 28,5–29,3), 4,8 m (od s = 29,5) a vnitřní líc u komína místy 4,0 m. Komín (5,5 m) ji v okruhu 1,5 m přesahuje o 0,3–1,5 m.
   - `protect` `{s0: 30,3; s1: 30,9; min: 4,95}` drží řadu kamene nad kapsou pozednice.
3. **Kapsa pro východní pozednici** ve vnitřním líci `Palac_J`: otvor `kapsa` v s = 30,55, šířka 0,26 m, hloubka = vnitřní líc (0,4 m). Kapsa se zarovnává na řady kamene: zabírá řadu 4,04–4,43 m nad terénem, pozednice v ní leží spodkem na spáře (proto má vrch 4,24 m, ne 4,2 m). Ostatní kameny zdi se kapsou nemění.
4. **`drop_rows`** (horní kameny každé vrstvy pryč, `zr_ruin/post.py` → `drop_top_rows`) vznikl při prvním pokusu o „řadu níž“. Pro `Palac_J` se nepoužívá (`J_DROP_ROWS = 0`), parametr zůstává v kódu pro jiné zdi.

## 4. Cílová struktura

Kovárna stojí v jihovýchodním koutě místnosti. Jižní stranu tvoří `Palac_J`, východní věž. Půdorys přístřešku: s = 24,95–30,75; n = 0,7–5,7 (asi 29 m², z toho 0,9 m je přesah za západní stěnu). Severní strana je otevřená, západní má lehkou stěnu. Výheň je přímo v koutě.

### 4.1 Přístřešek (pultová střecha, spád k západu)

| Prvek | Průřez | Počet / délka | Poloha | Na čem leží |
|---|---|---|---|---|
| Sloup u věže | 20 × 20 cm | 1 ks, výška 3,9 m | s = 30,55; n = 5,3 | na plochém kameni (36 × 36 × 14 cm, vrch 10 cm nad terénem), 10 cm od líce věže. V koutě u `Palac_J` sloup není. |
| Východní pozednice | 20 × 20 cm | 5,1 m (n = 0,4–5,5) | s = 30,55; vrch 4,24 m (spodek na spáře řad `Palac_J`) | jižní konec 0,3 m v kapse `Palac_J` (kap. 3), severní na sloupu; rozpětí 4,6 m |
| Sloupy na západě | 18 × 18 cm | 3 ks, výška 2,2 m | s = 25,85; n = 0,9 / 3,1 / 5,3 | na plochém kameni (jako u věže) |
| Západní pozednice | 18 × 18 cm | 4,76 m (n = 0,74–5,5) | s = 25,85; vrch 2,5 m | na sloupech |
| Krokve | loupaná kulatina Ø 16 cm | 6 ks, délka 6,1 m | n = 0,9 / 1,8 / 2,7 / 3,6 / 4,5 / 5,4; od s = 30,65 po s = 24,95 | obě pozednice (osedlání 3 cm), přesah 0,9 m na západ (kryje hranici dřeva u stěny) |

- **Sklon:** 20° k západu (po zvednutí východní pozednice na 4,24 m přesně 20,3°). Vysoká strana je u věže, aby nad výhní bylo co nejvíc místa a komín vycházel v nejvyšším bodě.
- **Krytina:** latě a prkna po spádu s lištami, stejná skladba jako `Ostroh_Krov`, ale **bez dehtu** (`raw`). Dehet je nad výhní hořlavý.
- **Plocha střechy:** 5,0 × 6,1 m, asi 30 m².
- **Lemování:** prkno na stojato podél věže (horní okraj) a podél `Palac_J` (jižní okraj).
- **Výška pod krokvemi:** u věže 4,0 m, nad kovadlinou 3,4 m, u západní pozednice 2,3 m (spodek pozednice), na okapu 2,1 m.
- **Poměr k oknu věže:** vrch krytiny u věže je asi 4,5 m, tedy 0,6 m pod parapetem okna.

### 4.2 Stěny

| Strana | Řešení |
|---|---|
| Jižní | stojící `Palac_J`. Je všude vyšší než okraj střechy, bez dozdívky. |
| Východní | stojící věž. |
| Západní | stěna z proutí vypleteného mezi sloupy a kůly, omazaná hlínou. s = 25,85; n = 0,7–5,4; výška 2,1 m. Nad ní volný pruh 0,2 m pod pozednicí. Na jihu dosedá na plný líc `Palac_J` těsně za výklenkem střílny s = 25. |
| Severní | otevřená. Vstup a světlo. |

- **Západní stěna** chrání oheň před převládajícím větrem a dům před jiskrami.
- **Na zimu** se dá severní strana zčásti zavřít prkny. Není součástí návrhu.

### 4.3 Výheň, měchy a komín

| Prvek | Rozměr | Poloha |
|---|---|---|
| Výheň | kamenný stůl 1,2 × 1,0 m, výška 0,75 m (3 řady po 25 cm), z kamene rozvalin, nahoře vymazaný hlínou (4 cm); ohniště 0,4 × 0,4 m pod komínem (střed s = 30,0; n = 1,35) | **v koutě** mezi `Palac_J` a věží: s = 29,75–30,73; n = 0,72–1,9 (2 cm od obou líců); západně hned vedle je výklenek střílny s = 29 |
| Boční zídka | kámen, 0,3 × 1,0 m, výška 1,2 m (5 řad), stojí na zemi | severně od stolu, n = 1,9–2,2; chrání měchy před žárem; otvor pro výfučnu 0,2 m v ose ohniště, ve výšce 0,72–0,96 m |
| Měchy | kožený měch 1,7 × 0,8 m na dřevěném rámu ve výšce 0,9 m | podél věže severně od zídky: s = 29,9–30,7; n = 2,2–3,9 |
| Páka měchů | tyč 2,2 m zavěšená na krokvi | konec u kovadliny |
| Dymník | proutěný koš vymazaný hlínou, 1,4 (podél s) × 1,2 m, spodní okraj 1,8 m, výška 1,0 m | nad výhní, střed v ose komína, východní okraj u stěny věže; visí na 4 závěsných tyčích Ø 5 cm |
| Výměny | loupaná kulatina Ø 10 cm, 2 ks | mezi krokvemi n = 0,9 a 1,8, 3 cm východně a západně od komína; nesou závěsné tyče dymníku a drží komín |
| Komín | 0,5 × 0,5 m, proutí s hlínou | nad ohništěm, střed s = 30,0; n = 1,35; prochází střechou mezi krokvemi n = 0,9 a 1,8 (vůle 12 cm) a 20 cm od východní pozednice; vrch 5,5 m (1,2 m nad krytinou) |

- Komín je asi 3,4 m jižně od okna věže a 0,4 m od líce `Palac_J`. Její koruna je u něj rozebraná na 4,0–4,8 m (kap. 3), komín ji přesahuje o 0,7–1,5 m; dál na západ (s = 28,5–29,3) je 5,2 m.
- Stěna věže a `Palac_J` za výhní jsou kamenné, bez úpravy. Dymník (n = 0,75–1,95) je 5 cm od líce `Palac_J`.

### 4.4 Vybavení

| Prvek | Rozměr | Poloha (s; n) |
|---|---|---|
| Kovadlina na špalku | špalek Ø 0,5 m, vrch kovadliny 0,75 m | 28,5; 1,4 (1,0 m před výhní, před výklenkem střílny) |
| Kalicí sud | Ø 0,6 m, výška 0,8 m, s vodou | 28,9; 2,6 |
| Brus | pískovcový kotouč Ø 0,7 m na dřevěném rámu 1,2 × 0,6 m, osa 0,75 m, **šlapací** (kliková páka, ojnice, šlapadlo; rozhodl Jirka 14. 11. 2026), pod kotoučem korýtko s vodou; u něj třínohá stolička (sedátko Ø 32 cm, výška 45 cm) | 27,0–28,2; 4,0–4,6 (u otevřené strany kvůli světlu) |
| Ponk se svěrákem | 2,2 × 0,7 m, výška 0,85 m | u západní stěny: 25,95–26,65; 2,6–4,8 (u jižní zdi by stál v kovadlině) |
| Nářadí | kleště, kladiva, sekáče na liště | na jižní zdi, s = 26,2–28,0, výška 1,5 m |
| Truhlík na dřevěné uhlí | 0,8 × 1,2 m, výška 0,8 m, s volným víkem (bez pantů, pokládá se bokem) | u západní stěny v jihozápadním rohu: 25,95–26,75; 0,8–2,0 |
| Zásoba dřeva | hranice 0,6 × 1,9 m, výška 1,4 m (podle místa i dvě za sebou) | **zvenku** u západní stěny pod přesahem střechy: s = 25,15–25,8; n = 1,5–5,4 |
| Železo a hotové hřebíky | pruty, koš | pruty opřené o jižní zeď (s ≈ 27), koš u ponku; **výklenek střílny s = 29 zůstává volný** (manipulační prostor u výhně) |
| Hřebovnice | na menším špalku | u kovadliny |

- **Kovadlina, sud a výheň** jsou od sebe na krok, kovář se mezi nimi jen otáčí.
- **Výheň je v nejtmavším koutě.** Kovář potřebuje šero, aby poznal barvu rozžhaveného železa. Brus a ponk jsou naopak u světla.
- **Podlaha:** udusaná hlína.

### 4.5 Okap

- **Žlab:** vydlabaný kmen Ø 20 cm pod západním okapem, s = 24,8; n = 0,7–5,7, se spádem k severu. Nesou ho vidlice.
- **Sud:** na dešťovou vodu pod severním koncem žlabu (s ≈ 24,8; n ≈ 5,9). Voda se hodí pro kalicí sud a korýtko brusu.
- **Svod se nedělá** (rozhodl Jirka 15. 11. 2026). Cisterna se neřeší.

### 4.6 Úprava dřeva

- Všechno dřevo `raw`. Žádný dehet.

## 5. Dostavba 05

| Stavba | Typ | Obsah |
|---|---|---|
| `Palac_Kovarna_Pristresek` | `pult_roof` (stejný nový typ jako `Palac_Obydli_Krov`) | sloupy, pozednice, krokve, krytina, lemování |
| `Palac_Kovarna_Stena` | **nový** (pracovně `wattle_wall`) | západní stěna z proutí a hlíny |
| `Palac_Kovarna_Vyhen` | `hearth` (`zr_stavby/ohniste.py`, hotový 15. 11. 2026; stejný typ pro `Palac_Obydli_Ohniste`) | výheň, zídka, dymník, komín, výměny a závěsné tyče |
| `Palac_Kovarna_Okap` | stejný jako `Palac_Obydli_Okap` | žlab, vidlice, sud |
| `Palac_Kovarna_Vybaveni` | samostatné actory | měchy, kovadlina, sud, brus, ponk, truhlík, dřevo, nářadí |

- **Složka:** `Stavby/Palac`.
- **Sdílené rozměry:** `tools/ruin/palac_spec.py` (společně s domem); čte ho 03 (`gen_layout.py`: snížení `Palac_J`, kapsa) i 05.
- **Vybavení nejsou generované dílce.** Měchy, kovadlina, brus, sud a nářadí jsou hotové modely, které generátor jen rozmístí. Jsou to vlastní props ve stylu hradu (rozhodl Jirka 14. 11. 2026), všechny už existují.
- **Suť:** v celé východní místnosti uklizená (`clear_rubble`).
- **Ruční doladění (`loose`):** všechno vybavení.

## 6. Vazby, kolize, pořadí

- **Odstup od domu:** výheň je 8,3 m od východního štítu domu, západní okraj přístřešku (okap) 3,55 m. Podmínka z návrhu domu (výheň aspoň 6 m) je splněná.
- **Sloup u věže** je jen jeden (n = 5,3), severně od měchů. Východní pozednice má od kapsy v `Palac_J` ke sloupu rozpětí 4,6 m.
- **Výheň** (s od 29,75) nezasahuje do výklenku střílny s = 29 (ten končí v s = 29,65).
- **Vstup:** původními dveřmi paláce (s = 27) na dvorek a odtud otevřenou severní stranou. Cesta musí zůstat volná v šířce aspoň 1,2 m.
- **Sud pod žlabem** stojí u severozápadního rohu přístřešku, mimo cestu ode dveří. Západní kout dvorku zůstává průchozí.
- **Západní linie** (s = 25,85) je 0,2 m východně od výklenku střílny s = 25; výklenek zůstává volný ze dvorku.
- **Okno věže** je 0,6 m nad střechou. Platí stejná otázka jako u původního návrhu domu: může tudy postava z věže na střechu?
- **Pořadí:** 03 část `Palac` (snížení `Palac_J`, kapsa) → `Palac_Kovarna_Pristresek` (bez krytiny) → `Palac_Kovarna_Vyhen` → krytina → `Palac_Kovarna_Stena`, `Palac_Kovarna_Okap`, vybavení, `Sut`.

## 7. Ověření

- `tools/checks/run_checks.py`: žádné průniky dřeva se zdivem mimo uložení.
- Každý sloup stojí na terénu nebo patním kameni, každá krokev leží na obou pozednicích, východní pozednice je aspoň 20 cm v kapse `Palac_J` bez průniku se zdivem.
- Krytina pokrývá aspoň 99 % půdorysu přístřešku mimo otvor komína.
- Sklon střechy je 20° ± 1°.
- Komín prochází střechou bez dotyku s krokvemi (vůle aspoň 10 cm) a končí aspoň 0,8 m nad krytinou.
- Mezi kovadlinou a výhní je 0,9–1,1 m, kalicí sud je do 1,5 m od obou.
- Kolem kovadliny, brusu a ponku zůstává průchod aspoň 1,2 m k otevřené severní straně.
- Světlá výška nad kovadlinou je aspoň 3,0 m.
- Žlab má spád k severu a ústí nad sud.
- Stavitel (15. 11. 2026): kritéria hlídá `tools/checks/run_checks.py --only palac` (průniky se zříceninou, sloupy na patních kamenech, krokve na pozednicích, sklon, vůle komína, světlá výška, pokrytí krytinou, lemování, stěna, okapová hrana nad žlabem, spád žlabu, konec žlabu nad sudem). Průchody kolem vybavení přibudou s krokem 4.
- Náhled: `tools/checks/preview3d.py` (ze dvorku od severu, zevnitř od ponku k výhni).

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
- **Okno věže nad střechou** jako možná cesta postavy: neřeší se, nechává se, jak vyjde (Jirka 15. 11. 2026).
- **Riziko (kouř):** komín je v koutě pod stěnou věže vysokou 9–13,5 m. Jižní zeď přesahuje (kap. 3), věž ne. Tah bude slabší a kouř půjde po stěně věže k hlídce nahoře. Kove se ale ve dne a s přestávkami.
- **Riziko (střílna u výhně):** po zanoření zdi je průzor střílny s = 29 ve výšce 1,29–2,39 m a dno výklenku 0,24 m nad zemí. Jako odkladiště u výhně to vyhovuje, pro střelbu je průzor nízko.
- **Riziko (zatékání):** po stěně věže stéká při dešti voda na horní okraj střechy. U otevřeného přístřešku to vadí méně než u domu, ale měchy jsou právě tam.
- **Riziko (rozpětí):** krokve Ø 16 cm na 4,7 m bez střední podpory a s přesahem 0,9 m. Pro lehkou krytinu to stačí, při pochybnosti přidat střední vaznici na dvou sloupech.
- **Neřeší se:** zimní zavření severní strany, milíř, cisterna.

## 10. Náčrt slovy

- **Půdorys:** obdélník 5,3 × 5,0 m v koutě mezi jižní zdí paláce a věží, střecha přesahuje 0,9 m za západní stěnu. Výheň je přímo v koutě, severně od ní zídka a měchy podél věže. Krok před výhní stojí kovadlina (před výklenkem střílny), vedle ní sud. U západní stěny truhlík s uhlím a ponk, zvenku pod přesahem hranice dřeva. Brus je u otevřené severní strany. Před přístřeškem je dvorek, do kterého se vchází původními dveřmi paláce.
- **Řez východ–západ:** u věže pozednice ve 4,24 m (jižním koncem v kapse `Palac_J`, severním na sloupu), krokve klesají 20° k západu na pozednici ve 2,5 m a přesahují ji o 0,9 m. V koutě stoupá komín nad střechu do 5,5 m a přesahuje rozebranou korunu jižní zdi. Pod ním dymník na závěsných tyčích a kamenný stůl výhně. Na západě stěna z proutí a hlíny do 2,1 m, pod okapem žlab a u jeho severního konce sud.
- **Pohled ze dvorku:** otevřená strana přístřešku, vpředu brus, vlevo podél věže měchy a za nimi temný kout s výhní, vzadu jižní zeď s nářadím a výklenkem střílny, vpravo ponk u proutěné stěny.
