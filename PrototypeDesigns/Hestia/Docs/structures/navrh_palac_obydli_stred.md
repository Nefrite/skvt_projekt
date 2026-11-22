---
# orchestrace
type: design
validity: valid
alternative_to: ["[[navrh_palac_obydli]]"]
updated: 2026-11-22
# hra
status: in_progress
domain: structures
depth: 4
entity: "[[Palac_Obydli]]"
build_step: 05_constructions
---
# Návrh: Palac_Obydli – obytná stavba posádky v prostřední místnosti paláce

## Souhrn
Platný návrh domu posádky v prostřední místnosti paláce (varianta ve východní místnosti, [[navrh_palac_obydli]], je zavržená). Stav: kroky 1–3 postavené (kámen, krov bez krytiny, srub), staveniště pro etapu 1 postavené ve skriptech a ověřené mimo UE (kap. 0.4, [[stav_palac_obydli]]).
- **Přednost:** kap. 0 platí přednostně před kap. 4–8; větší světnice a pec s nístějí jsou zapracované v kap. 4.5 a 4.6.
- **Etapy:** tři sady actorů `stage:base` / `stage:final` / `stage:site`; etapa 1 = `base` + `site`, etapa 2 = `base` + `final`. Sada `base` je zamčená (kap. 0.1, 0.7).
- **Konstrukce:** pultový krov se spádem 16° k severu, srubové stěny a příčka, kamenné podezdívky, pec s nístějí a komín, okap k západu bez svodu (kap. 0.7, 4).
- **Dřevo a otvory:** dřevo surové v obou etapách; dveře a okenice v etapě 2 otevřené jako kulisa, žebříky jen kulisa (kap. 0.1).
- **Zbývá:** krytina s lemováním, strop, podlaha, okap, vybavení (kap. 0.4). Předání staviteli: [[predani_palac_obydli_stavitel]].
- **Etapa 1 a staveniště:** [[navrh_palac_obydli_stavenisko]].
- **Otevřené otázky a rizika:** kap. 10 a [[navrh_palac_obydli_stavenisko]] kap. 9.5 (kouř při jižním větru, déšť přes sníženou zeď, kde spí posádka v etapě 1).
- **Kap. 3** (zřícení koruny u komína) odpadla (kap. 0.2a).

Specifikace od architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **staví se po krocích** (16. 11. 2026): plán po etapách a stav je v kap. 0, která platí přednostně; kamenné části jsou ve skriptech. Je to kopie návrhu [[navrh_palac_obydli]] (dům ve východní místnosti u věže) přenesená do **prostřední místnosti**. Původní dokument zůstává beze změny pro srovnání. Náčrty: [[navrh_palac_obydli_stred.png]] (hotová stavba) a [[navrh_palac_obydli_stred_etapa1.png]] (rozestavěný stav). Jsou to schémata, ne přesné modely.

**Připravenost assetů:** [[CHECKLIST_assets_navrhy]]. **Tohle je platný návrh domu**, varianta ve východní místnosti je zavržená.

**Proč prostřední místnost (Jirka, 14. 11. 2026):** součástí osídlení bude provizorní kovárna a u věže má komín špatný tah. Prostřední místnost je 11 m od věže, jižní zeď je tu rovnoměrnější. Vstupem byl původně portál; od 16. 11. 2026 je portál v západní místnosti a sem se vchází hrubým průchodem po něm (kap. 0.2a).

## 0. Plán stavby po etapách (16. 11. 2026, platí přednostně před kap. 3–9)

Dohodnuto s Jirkou 15.–16. 11. 2026. Kde se tato kapitola liší od starších kapitol níž, platí tato. Co zbývá dodělat a na co si dát pozor, je v předávacím dokumentu [[predani_palac_obydli_stavitel]].

### 0.1 Zásady

- **Jedna stavba, tři sady actorů.** Dům se počítá jednou jako hotový. Každý dílec patří do jedné sady a actory sady mají tag:

| Sada | Tag actoru | Etapa 1 | Etapa 2 | Obsah |
|---|---|---|---|---|
| základ | `stage:base` | vidět | vidět | co stojí už v etapě 1 a zůstává |
| dostavba | `stage:final` | skrytá | vidět | co se dodělá |
| staveniště | `stage:site` | vidět | skryté | nářadí, žebřík, kozy, vzpěry, hromady materiálu, ležící trámy |

- **Co je v etapě 1 postavené, v etapě 2 se neskrývá** a je to tentýž dílec na tomtéž místě. Skrývá se jen staveniště.
- **Přepnutí ve hře** = zobrazit a skrýt actory podle tagu (i kolizi). Dělá si ho Jirka v Blueprintu. Sady a tag jsou v `zrlib/config.py` (`STAGES`, `STAGE_TAG`), v datech stavby klíč `stage`.
- **Hráč domem jen prochází**, úkol se stavbou nesouvisí. Etapy mají dát dojem času.
- **Staveniště a etapa 1 jdou před dokončením domu** (Jirka 21. 11. 2026, zvýšená priorita). Funguje to proto, že etapa 1 ukazuje jen `base` + `site` a dokončení domu je celé v sadě `final`. Podmínkou je zamčená sada `base` (kap. 0.7).
- **Dřevo je surové (`raw`) v obou etapách**, krov i krytina. Dehtování může přijít jako pozdější třetí stav. Srub je loupaná kulatina se stejným materiálem v obou etapách.
- **Dveře a okenice** jsou v etapě 2 otevřené (kulisa, než se rozhýbou). **Žebříky** nejsou pro postavu použitelné (chybí animace); půda bude mít vlastní žebřík, staveništní zmizí.
- **Sklep** se neřeší. Jestli přijde, podřídí se stavbě.

### 0.2 Výchozí stav po úpravě `Palac_J` (změřeno z dat 16. 11. 2026)

Celá `Palac_J` je zanořená o 0,31 m ([[navrh_palac_kovarna]] kap. 3). V prostřední místnosti z toho plyne:

| s (m) | Koruna `Palac_J`, vnitřní líc (m nad terénem) |
|---|---|
| 10–11,5 | 5,5–5,7 |
| 12–12,5 | 4,8 |
| 13–14 | 5,2–5,5 |
| 14,5–15,5 | 4,4–4,8 |
| 16–20 | 4,8 (v s = 17 jen 4,4) |
| 20,5–21,5 | 5,5–6,0 |

- **Úprava 03 u komína (kap. 3) odpadá.** Koruna je u komína (s = 15,5–18,5) 4,4–4,8 m, tedy tam, kam ji mělo dostat plánované snížení. Komín 5,3 m ji přesahuje o 0,5–0,9 m.
- **Dozdívka koruny `Palac_J` pod střechu (kap. 4.3) odpadá.** Vnitřní líc je v celé délce domu nejníž 4,43 m, krytina u zdi končí ve 4,3 m. Zůstává jen lemování.
- **Výklenky střílen** s = 14 a 19 mají dno 0,24 m a vrch 2,39 m nad zemí (dřív 0,55–2,7 m). Jako police stačí.
- Příčky: `Palac_pricka_1` má korunu 1,05–1,39 m, `Palac_pricka_2` 1,09 m, dveře obou až k zemi (n = 4,25–5,25).

### 0.2a Úpravy zříceniny kolem domu (03, Jirka 16. 11. 2026)

Přestavět část `Palac`. Zapsáno v `tools/ruin/gen_layout.py` (zeď `Palac_S`) a `tools/ruin/palac_spec.py` (`D_PASS` → `ruin_edits`).

- **Vstupní oblouk (portál) je přesunutý do západní, prázdné místnosti:** `Palac_S` má portál 1,6 × 3,0 m v s = 4,5 (místo dveří), zeď kolem něj drží do 4,2 m (`protect` s = 2,5–6,5).
- **Ve střední místnosti posádka oblouk rozebrala na stavbu.** V `Palac_S` zůstal hrubý průchod až k zemi (`prulom` s = 16, šířka 1,8 m, vylámané okraje) v nízké zdi 1,1–1,4 m. Starší kapitoly jsou na to přepsané (průchod s = 15,1–16,9). Dům je teď z nádvoří vidět přes nízkou zeď.
- **Průchod ke kovárně:** `Palac_pricka_2` je severně od domu rozebraná na kámen pro podezdívky. Hrubý průchod až k zemi v n = 6,9–8,5 (šířka 1,6 m, vylámané okraje); u rohu domu a u `Palac_S` zůstaly zbytky zdi, takže je vidět, že tu zeď byla. Ze zápraží se jím jde na dvorek kovárny.
- Ostatní kameny obou zdí se nezměnily, jen u dveří do východní místnosti (`Palac_S`, s = 27) je vylámané ostění o kousek širší.

### 0.3 Rozdělení po stavbách

| Stavba | Typ | Základ (`base`) | Dostavba (`final`) | Stav |
|---|---|---|---|---|
| `Palac_Obydli_Kamen` | `stone_fill` (nový) | srovnání obou příček na 1,4 m včetně zazdění jejich dveří; podezdívky severní stěny a příčky 0,45 × 0,45 m | nic | ✅ ve skriptech (16. 11. 2026) |
| `Palac_Obydli_Ohniste` | `hearth` | pec s nístějí (kap. 0.5b): sokl, zdi pece, klenba, zídky plotny | sopouch, dymník, komín, železo (plotna, pás, poklop) | ✅ ve skriptech (16. 11. 2026); zavěšení dymníku se stropem |
| `Palac_Obydli_Krov` | `pult_roof` (3 podpory, hraněné krokve) | 5 sloupů; východní kus horní pozednice (s = 15,3–21,4) a střední vaznice (příčka → východní stěna); 6 krokví nad světnicí (s = 16,26–21,3); 2 řady latí nad světnicí | západní kusy pozednice a vaznice; 6 krokví nad síní; ostatní latě, krytina, lemování u `Palac_J` | ◐ kostra ve skriptech (16. 11. 2026), krytina chybí |
| `Palac_Obydli_Srub` | `log_wall` (nový) | světnice: severní stěna s = 15,75–21,4 a příčka v plné výšce 2,5 m s prázdnými otvory, srub na východní stěně (5 řad); síň: 3 řady severní stěny s mezerou pro vchod | zbylých 6 řad severní stěny síně, srub na západní stěně, prkenné štíty | ✅ ve skriptech (16. 11. 2026) |
| `Palac_Obydli_Strop` | nový nebo rozšíření `tower_floor` | nic | trámky, výměna u komína, prkna | ⬜ |
| `Palac_Obydli_Podlaha` | `plank_floor` | nic | podlaha světnice | ⬜ |
| `Palac_Obydli_Okap` | `gutter` | nic | žlab se spádem k západu (od kovárny), rozsochy, sud pod západním koncem; svod se nedělá (Jirka 16. 11. 2026) | ⬜ |
| `Palac_Obydli_Vybaveni` | rozmístění props | nic | dveře a okenice (otevřené), lůžka, stůl, truhly, police, ponk, dřevo, žebřík na půdu | ⬜ |
| `Palac_Obydli_Stavenisko` | `props`, celá stavba sada `site` | – | – | ⬜ další na řadě (kap. 9) |

- **Staveniště (`site`)**: obsah, polohy a kontroly jsou v kap. 9.2–9.4. Zásoba materiálu se „spotřebuje“, proto mizí celá.
- **Stavební logika etapy 1** (od západu k východu, východ je dál): krokve nad světnicí leží na třech podporách, které už stojí (pozednice na 3 sloupech, vaznice na příčce a východní stěně, severní stěna). Západní sloupy stojí bez pozednice, proto mají vzpěry. Základ ohniště je hotový dřív než podlaha. Nic se nestaví dřív, než má na čem ležet.

### 0.4 Pořadí stavění (ladí se hotový stav)

1. ✅ Sady etap v build skriptu, `palac_spec.py` → `obydli`, `Palac_Obydli_Kamen`, základ `Palac_Obydli_Ohniste`.
2. ✅ `Palac_Obydli_Krov` bez krytiny (rozšíření `pult_roof`: dělené pozednice, vaznice uložená na stěnách).
3. ✅ `Palac_Obydli_Srub` se štíty a otvory (`log_wall`).
4. ◐ **Staveniště a kontrola etapy 1** (kap. 9). Podmínkou je zamčená `base` (kap. 0.7). Postaveno ve skriptech a ověřeno kontrolami mimo UE (21. 11. 2026, kap. 9.2a), čeká na vizuální kontrolu v UE.
5. Krytina a lemování s prostupem komína, strop se zavěšením dymníku, podlaha, okap. (Pec s dymníkem a komínem už stojí, kap. 0.5b.)
6. Vybavení (dveře, okenice, nábytek, zárubně).

### 0.5 Co je postavené (krok 1)

Přesunuto do [[stav_palac_obydli]] (*Co je hotové*).

### 0.5a Větší světnice (Jirka 16. 11. 2026, platí přednostně před čísly níž i v kap. 4)

Zapracováno do kap. 4 (čísla příčky, místností a otvorů; podrobnosti v kap. 4.5).

### 0.5b Pec s nístějí místo otevřeného ohniště (Jirka 16. 11. 2026, nahrazuje kap. 4.6 a základ ohniště z kap. 0.5)

Přesunuto do kap. 4.6.

### 0.6 Co je postavené (kroky 2 a 3: krov bez krytiny a srub, 16. 11. 2026)

Přesunuto do [[stav_palac_obydli]] (*Co je hotové*, včetně odchylek od kap. 4).

### 0.7 Co platí (rozhodnutí Jirky, z předání 16. 11. 2026)

- **Etapy jsou tři sady actorů** s tagy `stage:base` / `stage:final` / `stage:site`. Dům se počítá jednou jako hotový, etapa 1 je jen filtr (`base` + `site`), etapa 2 = `base` + `final`. Co stojí v etapě 1, se v etapě 2 neskrývá.
- **Staveniště a etapa 1 jdou před dokončením domu** (Jirka 21. 11. 2026).
- **Dřevo je surové (`raw`) v obou etapách**, i krov a krytina. Dehtování je případný pozdější třetí stav.
- **Zabydlení je dlouhodobé a má být pohodlné.** Styl: dobové provizorium, železo z vlastní kovárny na míru.
- **Větší světnice:** příčka je v s = 14,85, západně od středního sloupu krovu (s = 15,3). Vchod s = 13,4–14,4, okénko světnice s = 17,5–18,1.
- **Pec s nístějí** místo otevřeného ohniště, osa s = 16,76 (uprostřed mezi krokvemi), kouř sopouchem do dymníku.
- **Okap:** spád k západu (od kovárny), sud pod západním koncem, svod se nedělá.
- **Dveře a okenice** jsou v etapě 2 otevřené (kulisa). **Žebříky** nejsou pro postavu použitelné. **Sklep** se neřeší.
- Hráč domem jen prochází, etapy mají dát dojem času.
- **Hranice sad `base` / `final` zůstává podle dat** (Jirka 21. 11. 2026): krokve od s ≥ 16,0 jsou `base` (`D_STAGE_S`), spoj pozednice je na sloupu 15,3, spoj vaznice na příčce 14,85, latě zavětrování jsou v s = 16,17–21,4, srub síně má v etapě 1 spodní 3 řady. Důvod: krokev s = 15,245 leží na spoji pozednice a nese ji hlavně západní kus, proto je `final`.
- **Pec v etapě 1:** sokl, kamenné zdi pece, hliněná klenba a tmavý vnitřek pece jsou `base`. Sopouch, dymník, komín, železo a vrstva uhlí pod plotnou jsou `final`, protože v etapě 1 se pec ještě nepoužívá (Jirka 21. 11. 2026).
- **Zamčená `base`:** dokončení domu nesmí změnit tyto hodnoty v `palac_spec.py`: `D_PLATE`, `D_PURLIN`, `D_RAFTER`, `D_STAGE_S`, `D_BRACE_LATHS`, `D_LOG` (včetně `west_base_rows`), `D_SILL`, `D_FILL_TOP`, `D_DOOR_N`, `D_DOOR_P`, okénko světnice v `D_WINDOWS`, `D_OVEN` a úpravy 03 v části `Palac`. Při změně kterékoli z nich znovu proběhnou kontroly etapy 1 (kap. 9.4) a polohy staveniště. Jediná schválená změna `base` před staveništěm: vrstva uhlí pod plotnou (box `U` v `Palac_Obydli_Ohniste`) přejde do `final`.
- **Krytina nemění latě zavětrování** (`pre_laths`, `base`): v jejich řadách položí jen západní část latí.
- **Každá hranice materiálu na nádvoří je samostatný objekt** (Jirka 21. 11. 2026): jeden actor na hranici. Jirka hranice v UE posune nebo natočí podle game designu a uloží přes capture. Jednotlivé kusy uvnitř hranice se nepřeskládávají.
- **Prkna na krytinu jsou v jedné hranici** o 0,5 m vyšší (Jirka 21. 11. 2026). Počet prken nemusí vycházet na kusy krytiny. Varianta se dvěma hranicemi (S5a, S5b) zůstává v datech pro pozdější použití (`D_SITE` → `boards.variant = "two"`).
- **Kozy s rozpracovanou kulatinou** patří na staveniště (Jirka 21. 11. 2026): kulatina na srub na dvou kozách, na jedné straně částečně oloupaná.


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
| sever | `Palac_S` | 1,4 m | po úpravě 16. 11. 2026: s 11–14: 1,1–1,6; s 17–21: 1,1–1,4 (dřív s 14–18: 3,9–4,3 kolem portálu) | hrubý průchod s = 15,1–16,9 až k zemi, vylámané okraje (dřív portál s obloukem; ten je teď v západní místnosti, s = 4,5) |
| západ | `Palac_pricka_1` (osa s = 10,5) | 0,8 m | 1,0–1,4 | dveře n = 4,25–5,25 (až k zemi) |
| východ | `Palac_pricka_2` (osa s = 21,0) | 0,8 m | 0,8–1,4 | dveře n = 4,25–5,25 (až k zemi) |

- Terén v místnosti je v datech rovný.
- **Sklep** je zatím jen v návrhu dat (`ruin_layout_draft.json`): s = 3–15, n = 1–8,5, klenba částečně propadlá. Zasahoval by pod západní polovinu domu (síň).
- Věž je od východního štítu domu 9,4 m.

## 3. Úprava 03: zřícení koruny jižní zdi u komína

**Odpadlo (16. 11. 2026).** Po zanoření `Palac_J` o 0,31 m je koruna u komína 4,4–4,8 m a všude nad krytinou; úprava 03 u komína ani dozdívka koruny se nedělají (kap. 0.2a, [[Rozhodnuti_zricenina]]).

## 4. Cílová struktura

Kde se postavený krov a srub liší od čísel v této kapitole, platí [[stav_palac_obydli]] (*Co je hotové*).

Dům zabírá jižní část místnosti v celé délce: s = 10,1–21,4 (obě boční stěny stojí na příčkách), n = 0,7–6,3. Uvnitř 52 m². Mezi domem a severní zdí paláce zůstává zápraží 2,3 m, na které se vchází průchodem v `Palac_S` (s = 16). Ze zápraží vede na východ průchod v `Palac_pricka_2` (n = 6,9–8,5) na dvorek kovárny.

### 4.1 Krov (pultová střecha, spád k severu)

| Prvek | Průřez | Počet / délka | Poloha | Na čem leží |
|---|---|---|---|---|
| Sloupy u jižní zdi | 20 × 20 cm | 5 ks, výška 3,83 m | n = 0,85; s = 11,1 / 13,0 / 15,6 / 18,0 / 20,4 | na plochém kameni na terénu, těsně u líce `Palac_J`, mimo výklenky střílen |
| Horní pozednice | 20 × 20 cm | 9,7 m (2 kusy, spoj nad sloupem s = 15,6) | n = 0,85, vrch 4,03 m | na sloupech |
| Střední vaznice | 20 × 24 cm | 11,3 m (2 kusy, spoj nad příčkou) | n = 4,4, vrch 3,02 m | západní stěna (s = 10,5), srubová příčka (s = 14,85), východní stěna (s = 21,0); rozpětí 2 × 5,25 m, bez sloupů v místnostech |
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
| Příčka | srub z kulatiny Ø 22 cm na podezdívce | osa s = 14,85; n = 0,7–6,2 | do 2,50 m, nad tím prkenný štít pod střechu |
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
| Podezdívka příčky | osa s = 14,85; n = 0,7–6,0, přerušená ve dveřích | 0,45 × 0,45 m |
| Dozdívka koruny `Palac_J` | s = 15,25–18,25, kde je vnitřní líc pod 4,35 m | 0,45 m na vnitřní polovině koruny, až pod střechu (0–0,45 m) |

- Dozdívka příček je v celé tloušťce 0,8 m, tedy širší než jednořadá zeď 0,45 m u ostrohu. Je to parametr tloušťky, ne nový typ.

### 4.4 Otvory

| Otvor | Kde | Rozměr | Poznámka |
|---|---|---|---|
| Vchod | severní stěna, s = 13,4–14,4 | 1,0 × 2,2 m | do síně; od průchodu v `Palac_S` 1,5 m šikmo vlevo |
| Dveře do světnice | příčka, n = 3,3–4,3 | 1,0 × 2,2 m | |
| Okénko světnice | severní stěna, s = 17,5–18,1 | 0,6 × 0,6 m, parapet 1,3 m | okenice, bez skla; proti nízké části `Palac_S` |
| Okénko síně | severní stěna, s = 11,8–12,3 | 0,5 × 0,5 m, parapet 1,3 m | okenice |
| Střílny `Palac_J` | s = 14 (síň), s = 19 (světnice) | stávající | světlo a výhled na jih, výklenek jako police |

### 4.5 Místnosti

| Místnost | Rozměr uvnitř | Podlaha | Strop |
|---|---|---|---|
| Světnice (východní) | s = 14,97–20,6; n = 0,7–6,05 (5,63 × 5,35 m) | prkna na podvalech (`plank_floor`) | trámkový, spodek 2,3 m |
| Síň a komora (západní) | s = 10,9–14,73; n = 0,7–6,05 (3,83 × 5,35 m) | udusaná hlína | bez stropu, otevřeno do krovu |
| Půda nad světnicí | nad stropem | prkna stropu | výška 0–1,6 m, přístup žebříkem ze síně otvorem ve štítu příčky |

- **Strop světnice:** 6 trámků 14 × 18 cm ve směru východ–západ po 0,9 m (n = 1,1 až 5,6), prkna 4 cm. Leží v zářezech srubové příčky a srubu východní stěny, žádné další sloupy. U jižní zdi je otvor asi 1,7 × 1,2 m pro dymník a komín (kap. 4.6): trámky n = 1,1 a 2,0 jsou tam přerušené a uložené do výměny.

**Větší světnice (Jirka 16. 11. 2026):**

- **Příčka je posunutá na s = 14,85** (dřív 15,75), tedy na západní stranu středního sloupu krovu (s = 15,3). Sloup teď stojí ve světnici 23 cm od příčky.
- **Světnice** má uvnitř s = 14,97–20,6 (5,63 m, dřív 4,7 m), **síň** s = 10,9–14,73 (3,83 m).
- **Vchod** je posunutý na s = 13,4–14,4 (dřív 13,8–14,8), od podezdívky příčky 0,22 m. Od průchodu v `Palac_S` je teď asi 2 m šikmo vlevo.
- **Okénko světnice** je v s = 17,5–18,1 (dřív 18,5–19,1): uprostřed stěny světnice a mezi krokvemi 17,26 a 18,27.
- S příčkou se posunula její podezdívka, spoj a špalek střední vaznice a prkenný štít nad ní. Spoj horní pozednice zůstává nad sloupem (s = 15,3). Ohniště, komín a krokve se nemění.
- Podezdívka příčky končí u `Palac_J` těsně u výklenku střílny síně (s = 13,35–14,65), kulatina je od něj 8 cm.
- Sady etap se dělí dál podle krokví (s ≥ 16 je `base`); doladí se se staveništěm.

### 4.6 Pec s nístějí a komín (Jirka 16. 11. 2026)

Zabydlení je dlouhodobé a má být pro posádku pohodlné. Styl: dobové provizorium, železo z vlastní kovárny na míru. Stavba `Palac_Obydli_Ohniste` (typ `hearth`), rozměry `palac_spec.py` → `D_OVEN`, `D_CHIMNEY`.

| Část | Rozměr a poloha | Sada |
|---|---|---|
| kamenný sokl | 1,6 × 1,6 × 0,6 m; s = 15,96–17,56; n = 0,72–2,32; nahoře hliněný maz 4 cm | `base` |
| pec (vzadu u `Palac_J`) | 1,4 × 1,0 m; kamenné zdi 22 cm do 1,0 m, čelo s ústím 0,4 × 0,36 m k severu | `base` |
| hliněná klenba | nízká valená klenba 1,4 × 1,0 m, vrch 1,34 m (nový mesh `SM_RuinOvenDome`) | `base` |
| nístěj (vpředu) | 1,6 × 0,6 m ve výšce 0,64 m | `base` |
| plotna | železná 0,58 × 0,44 m na dvou kamenných zídkách 22 cm, na východní straně nístěje (vrch 0,87 m), pod ní uhlí; **samostatný actor** | zídky `base`, plotna `final` |
| kovaný pás nad ústím | 0,7 m, v čele pece | `final` |
| poklop ústí | plech 46 × 42 cm s dřevěnou rukojetí na dvou trnech (mesh `SM_RuinOvenDoor`), opřený o čelo pece západně od ústí; **samostatný actor**, dá se ručně doladit a uložit přes capture | `final` |
| sopouch | hliněný kouřovod 0,28 m z klenby za čelem pece (n = 1,56) do dymníku | `final` |
| dymník | 1,6 × 1,1 m, spodní okraj 1,8 m, výška 0,8 m; nad ústím a nístějí (střed n = 1,7) | `final` |
| komín | 0,5 × 0,5 m, střed s = 16,76; n = 1,7; vrch 5,3 m | `final` |

- **Tah:** pec táhne sopouchem přímo do dymníku a komína, dymník sbírá kouř z plotny a z ústí při přikládání. Poklop se nasazuje po vyhoření.
- **Osa pece je s = 16,76**, uprostřed mezi krokvemi 16,26 a 17,26 (komín 16 cm od obou). Střed mezi sloupy 15,3 a 18,0 je 16,65; od patních kamenů zbývá 0,48 m na západě a 0,26 m na východě.
- **Zatím chybí:** zavěšení dymníku (přijde se stropem: výměna v trámcích stropu, otvor asi 1,7 × 1,2 m), prostup komína krytinou (s krytinou), žhavé uhlí a oheň.

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
- Svod kříží zápraží na východním konci (s = 20,0), mimo cestu od průchodu v `Palac_S` (s = 16) ke vchodu (s = 14,3). Pozor: kříží cestu ze zápraží ke kovárně (průchod v `Palac_pricka_2`, n = 6,9–8,5); svod je potřeba vést nad hlavou nebo jinudy.
- **Kovárna ve východní místnosti:** výheň má být až u věže, aspoň 6 m od východního štítu domu (dehtovaná střecha). Dveře v `Palac_pricka_2` jsou zazděné, z domu samotného se ke kovárně neprojde. Ze zápraží ale vede hrubý průchod v `Palac_pricka_2` (n = 6,9–8,5) na dvorek kovárny (kap. 0.2a).
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
- Zápraží má volnou šířku aspoň 2,0 m, průchod v `Palac_S` i průchod ke kovárně zůstávají volné v šířce aspoň 1,2 m.
- Žlab má spád k východu a svod končí za vnějším lícem `Palac_S`.
- Náhled: `tools/checks/preview3d.py` (zvenku od nádvoří průchodem, ze zápraží k průchodu ke kovárně, půdorys; `preview3d.py obydli`).

## 8. Rozdíly proti návrhu ve východní místnosti

| | Východní ([[navrh_palac_obydli]]) | Prostřední (tento dokument) |
|---|---|---|
| Plocha uvnitř | 49 m² | 52 m² |
| Východní stěna | věž | kámen + srub na `Palac_pricka_2` |
| Ohniště | u stěny věže | u jižní zdi |
| Komín proti okolním zdem | pod věží (9–13,5 m) i jižní zdí (až 6,7 m) | 0,6–1,0 m nad sníženou jižní zdí |
| Úprava 03 | žádná | snížení koruny `Palac_J` u komína (21 kamenů) |
| Dozdívka koruny `Palac_J` | s = 25,5–29, až 0,4 m | jen vnitřní líc u komína, do 0,45 m |
| Lemování střechy | jižní zeď a věž | jen jižní zeď |
| Sloupy uvnitř místností | jeden v síni | žádný |
| Vstup | původní dveře | původně portál, od 16. 11. 2026 hrubý průchod po rozebraném portálu |
| Střecha | 66 m², 11 krokví | 75 m², 12 krokví |
| Okno věže nad střechou | ano (možná cesta postavy) | netýká se |

## 9. Etapa 1: rozestavěná stavba (hráč přichází poprvé)

Přesunuto do [[navrh_palac_obydli_stavenisko]] (kap. 9.1–9.6 tam mají stejná čísla); postavená verze a odchylky (dřív 9.2a) jsou v [[stav_palac_obydli]].

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

- **Půdorys:** obdélník 11,3 × 5,6 m u jižní zdi prostřední místnosti. Jižní stranu tvoří `Palac_J`, obě boční stěny stojí na příčkách, severní je nový srub. Srubová příčka v s = 15,75 dělí dům na světnici (východ) a síň (západ). Ohniště je ve světnici u jižní zdi hned za příčkou. Vchod je v severní stěně do síně, šikmo proti průchodu v `Palac_S`. Před domem zápraží 2,3 m, z něj na východ průchod ke kovárně.
- **Řez jih–sever:** u jižní zdi sloup s pozednicí (vrch 4,03 m), krokve klesají 16° přes střední vaznici (vrch 3,02 m ve n = 4,4) na srubovou stěnu (vrch 2,50 m ve n = 6,2) a přesahují ji o 0,5 m. U jižní zdi stoupá komín do 5,3 m, zeď je vedle něj snížená na 4,3–4,7 m. Ve světnici strop se spodkem trámků 2,3 m, nad ním půda.
- **Boční stěna:** dole stará příčka srovnaná kamenem na 1,4 m, nad ní pět řad kulatiny do 2,5 m, nad tím trojúhelník svislých prken pod střechu.
- **Pohled od nádvoří:** přes nízkou zeď a průchodem je vidět srubová stěna s dveřmi, nad zdí paláce vykukuje tmavá prkenná střecha stoupající k jižní zdi a nad ní komín.
