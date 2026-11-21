---
# orchestrace
type: design
validity: valid
alternative_to: ["[[navrh_palac_obydli]]"]
updated: 2026-11-21
# hra
status: in_progress
domain: structures
depth: 4
entity: "[[Palac_Obydli]]"
build_step: 05_constructions
---
# Návrh: Palac_Obydli – obytná stavba posádky v prostřední místnosti paláce

Specifikace od architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **staví se po krocích** (16. 11. 2026): plán po etapách a stav je v kap. 0, která platí přednostně; kamenné části jsou ve skriptech. Je to kopie návrhu [[navrh_palac_obydli]] (dům ve východní místnosti u věže) přenesená do **prostřední místnosti**. Původní dokument zůstává beze změny pro srovnání. Náčrty: [[navrh_palac_obydli_stred.png]] (hotová stavba) a [[navrh_palac_obydli_stred_etapa1.png]] (rozestavěný stav). Jsou to schémata, ne přesné modely.

**Připravenost (15. 11. 2026)** – podrobně [[CHECKLIST_assets_navrhy]]. **Tohle je platný návrh domu**, varianta ve východní místnosti je zavržená.
- **Hotové dílce stavby:** loupaná kulatina `SM_RuinLog` (srub), trámy, sloupy a prkna (`SM_RuinTimber`, `SM_RuinPost`, `SM_RuinPlank`), žlab `SM_RuinGutter` / `SM_RuinGutterBark` s vidlicí `SM_RuinForkHead`, dymník `SM_RuinSmokeHood`, komín `SM_RuinChimney`. Materiály: loupané dřevo (`peeled`), výplň spár srubu `MI_RuinChinking`, mazanina, proutí.
- **Hotové vybavení (kap. 4.8):** lůžko `SM_RuinBed` / `SM_RuinBedFolded`, stůl `SM_RuinTable`, truhla `SM_RuinChest`, police `SM_RuinShelf`, ponk `SM_RuinWorkbench` (menší škálováním), hranice dřeva `SM_RuinWoodpile`, dveře `SM_RuinDoor`, okenice `SM_RuinShutter` (0,5 × 0,5 m škálováním), žebřík `SM_RuinLadder`.
- **Hotové pro staveniště (kap. 9.2):** žebřík, koš `SM_RuinBasket`, tesařské nářadí (sekera, širočina, dvoumužná pila, kladivo, palice).
- **Chybí:** typy staveb `pult_roof`, `log_wall`, `hearth`, `gutter`, rozšíření `stone_addon` o tloušťku, strop s výměnou, rozmístění props, přepínač `ETAPA`, `tools/ruin/palac_spec.py`, úprava 03 (kap. 3). Ze staveniště tesařské kozy, rozpracovaná kulatina, hromady materiálu, loupák, třísky na zemi. Dále zářez srubu v nárožích, saze, udusaná hlína, oheň a kouř.

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

- **Srovnání příček** (`W`, `E`): s = 10,1–10,9 a 20,6–21,4; n = 0,72–6,43; vrch 1,4 m. Kámen z rozvalin ve dvou řadách přes tloušťku 0,8 m, spodek kopíruje korunu zříceniny, v místě dveří příček stojí zdivo od země.
- **Podezdívka severní stěny** (`N`): osa n = 6,2; s = 10,9–20,6; 0,45 × 0,45 m; vchod s = 13,8–14,8 volný.
- **Podezdívka příčky** (`P`): osa s = 15,75; n = 0,72–5,98; dveře n = 3,3–4,3 volné.
- **Základ ohniště**: s = 16,2–17,6; n = 0,72–2,1; výška 0,5 m ve 2 řadách, maz 4 cm, uprostřed studené ohniště 0,5 × 0,5 m.
- **Suť** v domě a na zápraží je uklizená (`clear_poly`).
- **Vyspravení staré zdi maltou** (Jirka 16. 11. 2026, jako u `Ostroh_Dostavba`): v ose obou příček i podezdívek je maltové jádro 6 cm (`mortar`, materiál `MI_RuinCore`) od země až 2 cm pod vrch. Prochází novým zdivem i starou příčkou pod ním; kde staré zdi chybí jádro, vyplní dutinu mezi líci. Zdí tak neprosvítá. Ve dveřích a ve větší díře skrz zeď malta není.
- Rozměry: `tools/ruin/palac_spec.py` (`D_*`, `obydli`). Kontrola: `run_checks.py --only obydli`. Náhled: `preview3d.py obydli <out.png> [--stage 1|2]`, `05_constructions/Stavby_palac_obydli_nahled.png`.
- V UE: celý dům `05_constructions/stavby/Palac_Obydli.py` (seznam hotových částí v pořadí, se `SUT = True` i suť); jednotlivě `Palac_Obydli_Kamen.py`, `Palac_Obydli_Krov.py`, `Palac_Obydli_Ohniste.py`, `Palac_Obydli_Srub.py`, pak `Sut.py`. Navázání kamene potvrzené v UE (Jirka 16. 11. 2026), ostatní neověřeno.

### 0.5a Větší světnice (Jirka 16. 11. 2026, platí přednostně před čísly níž i v kap. 4)

- **Příčka je posunutá na s = 14,85** (dřív 15,75), tedy na západní stranu středního sloupu krovu (s = 15,3). Sloup teď stojí ve světnici 23 cm od příčky.
- **Světnice** má uvnitř s = 14,97–20,6 (5,63 m, dřív 4,7 m), **síň** s = 10,9–14,73 (3,83 m).
- **Vchod** je posunutý na s = 13,4–14,4 (dřív 13,8–14,8), od podezdívky příčky 0,22 m. Od průchodu v `Palac_S` je teď asi 2 m šikmo vlevo.
- **Okénko světnice** je v s = 17,5–18,1 (dřív 18,5–19,1): uprostřed stěny světnice a mezi krokvemi 17,26 a 18,27.
- S příčkou se posunula její podezdívka, spoj a špalek střední vaznice a prkenný štít nad ní. Spoj horní pozednice zůstává nad sloupem (s = 15,3). Ohniště, komín a krokve se nemění.
- Podezdívka příčky končí u `Palac_J` těsně u výklenku střílny síně (s = 13,35–14,65), kulatina je od něj 8 cm.
- Sady etap se dělí dál podle krokví (s ≥ 16 je `base`); doladí se se staveništěm.

### 0.5b Pec s nístějí místo otevřeného ohniště (Jirka 16. 11. 2026, nahrazuje kap. 4.6 a základ ohniště z kap. 0.5)

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

### 0.6 Co je postavené (kroky 2 a 3: krov bez krytiny a srub, 16. 11. 2026)

Všechno je ve skriptech a prošlo kontrolami mimo Unreal, v UE zatím nic z toho neběželo. Náhledy: `05_constructions/Stavby_palac_obydli_nahled.png` (etapa 2) a `Stavby_palac_obydli_nahled_etapa1.png` (etapa 1).

**Krov `Palac_Obydli_Krov`** (typ `pult_roof`, spád 16,0° k severu, všechno dřevo `raw`):

| Dílec | Rozměr a poloha | Sada |
|---|---|---|
| 5 sloupů 20 × 20 cm na patních kamenech | n = 0,85; s = 11,1 / 13,0 / 15,3 / 18,0 / 20,4; výška 3,73 m | `base` |
| horní pozednice 20 × 20 cm, vrch 4,03 m | západní kus s = 10,1–15,3, východní 15,3–21,4 (spoj nad středním sloupem) | západní `final`, východní `base` |
| střední vaznice 20 × 24 cm, vrch 3,02 m, n = 4,4 | západní kus s = 10,1–14,85, východní 14,85–21,4 (spoj nad příčkou) | západní `final`, východní `base` |
| 3 špalky 20 × 20 × 28 cm pod vaznicí | na vrchní řadě srubu západní stěny, příčky a východní stěny | západní `final`, ostatní `base` |
| 12 krokví 18 × 22 cm, délka 6,2 m | s = 10,2 až 21,3 po 1,01 m; n = 0,8–6,8 (přesah 0,6 m za severní stěnu), osedlání 3 cm | 6 nad světnicí `base`, 6 nad síní `final` |
| 2 řady latí (zavětrování) | n = 2,6 a 5,3; s = 16,17–21,4 | `base` |

**Srub `Palac_Obydli_Srub`** (typ `log_wall`, loupaná kulatina, `raw`):

| Stěna | Řady | Sada |
|---|---|---|
| severní, světnice (s = 14,85–21,45) | 9 řad od podezdívky do 2,5 m (4 řady po 24 cm do 1,4 m, 5 řad po 22 cm) | `base` |
| severní, síň (s = 10,05–14,85) | spodní 3 řady (vrch 1,16 m) s mezerou pro vchod | `base` |
| severní, síň | zbylých 6 řad | `final` |
| příčka (s = 14,85; n = 0,74–6,5) | 9 řad, první a poslední je půltrám | `base` |
| východní (na srovnané příčce, 1,4–2,5 m) | 4 řady kulatiny mezi dvěma půltrámy | `base` |
| západní | stejně | `final` |
| prkenné štíty (západní, východní, nad příčkou) | svislá prkna 20–28 cm od vrchu srubu pod vrch krokví, výřezy pro pozednici a vaznici | `final` |

- **Nároží jako u skutečného srubu:** boční stěny a příčka začínají a končí půltrámem (hraněný, 11 cm), jejich řady jsou proto o půl řady posunuté proti severní stěně. V nárožích se kulatiny střídají a zhlaví přesahují 0,3 m (náhodně ± 5 cm).
- **Zdí neprosvítá:** kulatina je o 1,2 cm tlustší než řada (překryv jako v drážce). Výplň spár mechem a hlínou se proto nestaví.
- **Otvory jsou zarovnané na řady:** vchod 1,0 × 2,28 m, dveře v příčce 1,0 × 2,17 m, okénko světnice 0,6 × 0,66 m (parapet 1,4 m), okénko síně 0,5 × 0,44 m (parapet 1,4 m) v s = 11,8–12,3. Okénko síně zůstává, kde je postavené, i když není přesně uprostřed stěny vlevo od vchodu (střed 12,15) (Jirka 21. 11. 2026). Zárubně, dveře a okenice přijdou s vybavením.

**Odchylky od kap. 4 (důvod):**

- střední sloup v s = 15,3 místo 15,6, spoj pozednice je nad ním; příčka je od 16. 11. 2026 západně od něj (kap. 0.5a);
- pozednice je dlouhá jako vaznice (s = 10,1–21,4 místo 10,9–20,6), aby na ní ležely i štítové krokve;
- vaznice leží na špalcích 28 cm (srub končí ve 2,5 m, spodek vaznice je ve 2,78 m);
- krokve začínají v n = 0,8 místo 0,75 (kameny líce `Palac_J` vystupují až o 5 cm);
- komín je v s = 16,76 (v 16,9 by zasáhl do krokve s = 17,26); stojí s pecí (kap. 0.5b), prostup krytinou přijde s krytinou;
- dveře v příčce mají světlou výšku 2,17 m místo 2,2 m (zarovnání na řady);
- štíty končí rovně pod vrchem krokví, u příčky zůstává pod krytinou stupňovitá mezera do 7 cm.

**Okap (rozhodnutí Jirky 16. 11. 2026, staví se v kroku 4):** žlab má spád k západu, od kovárny. Sud stojí pod jeho západním koncem, svod přes zápraží se nedělá. Cesta ze zápraží ke kovárně tak zůstává volná. Kap. 4.7 a poznámka o svodu v kap. 6 tím neplatí.

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

Dům zabírá jižní část místnosti v celé délce: s = 10,1–21,4 (obě boční stěny stojí na příčkách), n = 0,7–6,3. Uvnitř 52 m². Mezi domem a severní zdí paláce zůstává zápraží 2,3 m, na které se vchází průchodem v `Palac_S` (s = 16). Ze zápraží vede na východ průchod v `Palac_pricka_2` (n = 6,9–8,5) na dvorek kovárny.

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
| Vchod | severní stěna, s = 13,8–14,8 | 1,0 × 2,2 m | do síně; od průchodu v `Palac_S` 1,5 m šikmo vlevo |
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

Začátek léta, posádka dům teprve staví. Postup jde **od západu k východu**. Světnice má stěny, kostru krovu a pec, síň je u základů. Zřícenina (03) je v obou etapách stejná. Etapa 1 = sady `base` + `site`, etapa 2 = `base` + `final` (kap. 0.1). Čísla jsou změřená z dat 21. 11. 2026.

### 9.1 Co v etapě 1 stojí (sada `base`)

| Stavba | Etapa 1 (`base`) | Chybí do etapy 2 (`final`) |
|---|---|---|
| `Palac_Obydli_Kamen` | obě příčky srovnané na 1,4 m se zazděnými dveřmi; podezdívky severní stěny a příčky | – |
| `Palac_Obydli_Srub`, světnice | severní stěna s = 14,85–21,445 v plné výšce 2,5 m s otvorem okénka (s = 17,5–18,1); příčka s = 14,85 v plné výšce s otvorem dveří (n = 3,3–4,3); východní stěna (6 řad včetně pultramů) | prkenné štíty |
| `Palac_Obydli_Srub`, síň | severní stěna s = 10,93–14,85, řady 0–2 (vrch 1,16 m), mezera vchodu s = 13,4–14,4 | řada 3 a řady 4–8 severní stěny, celá západní stěna (6 řad), štít |
| `Palac_Obydli_Krov` | 5 sloupů na patních kamenech (s = 11,1 / 13,0 / 15,3 / 18,0 / 20,4); východní kus pozednice (od spoje na sloupu 15,3); východní kus vaznice (od příčky 14,85) se špalky na příčce a východní stěně; 6 krokví s = 16,255–21,3; 2 řady latí s = 16,17–21,4 | západní kusy pozednice a vaznice, špalek na západní stěně, 6 krokví s = 10,2–15,245, ostatní latě, krytina, lemování |
| `Palac_Obydli_Ohniste` | sokl, zdi pece, hliněná klenba, zídky plotny, tmavý vnitřek pece (box `V`) | sopouch, dymník, komín, plotna, pás nad ústím, poklop, vrstva uhlí pod plotnou (box `U`) |
| `Palac_Obydli_Strop`, `_Podlaha`, `_Okap`, `_Vybaveni` | nic | všechno |

- Dřevo je v obou etapách surové (`raw`), dehtuje se až případně ve třetím stavu.
- Otvory srubu jsou v etapě 1 bez zárubní, s volnými konci kulatin. Ve srubu se otvory obvykle dořezávají až po vyzdvižení stěn (předpoklad).
- Nad světnicí je mezi krokvemi vidět nebe, nad síní stojí jen dva sloupy se vzpěrami.

### 9.2 Staveniště `Palac_Obydli_Stavenisko`

```
### Palac_Obydli_Stavenisko
- Zadání: Jirka 21. 11. 2026, priorita před dokončením domu. Herní účel: hráč při prvním příchodu pozná, že dům se
  teprve staví a z čeho bude (materiál připravený na zbývající části).
- Kde: palác, střední místnost (síň a světnice) a nádvoří před Palac_S (s = 8,5–25,0; n = 10,6–13,5).
  Výšky od terénu v místě dílce.
- Výchozí stav (data 21. 11. 2026):
  - Palac_S: osa n = 9,5, tloušťka 1,4 m (vnitřní líc n = 8,8, vnější n = 10,2), nízká koruna 1,1–1,4 m;
    průlom s = 15,1–16,9, portál do západní místnosti s = 3,7–5,3, dveře do východní místnosti s = 26,45–27,55.
  - Síň: s = 10,93–14,85 (vnitřní líc Palac_pricka_1 je 10,9); n = 0,72–5,98 (severní srub do n ≈ 6,3).
  - Zápraží: n = 6,43–8,8; průchod v Palac_pricka_2 ke kovárně n = 6,9–8,5.
  - Sloupy krovu 0,20 × 0,20 m v n = 0,85, vrch 3,83 m (pozednice 4,03 m); patní kameny 0,26 × 0,36 m.
  - Terén nádvoří není změřený (předpoklad: rovný). Ověř z levelu.
- Cílová struktura (všechno sada site):
  - S1 Vzpěry sloupů bez pozednice (statika etapy 1), 4 ks, tyče s kůrou Ø 0,10 m (shape "round", d <= 11 cm
    → SM_RuinPole*). Horní konec na líci sloupu ve výšce 2,6 m, pata na terénu:
      | id | sloup | p0 (s, n, z) | p1 (s, n, z) | délka |
      | V1 | 11,1 | (11,10; 0,95; 2,6) | (11,10; 2,45; 0) | 3,00 m |
      | V2 | 11,1 | (11,20; 0,85; 2,6) | (12,70; 0,85; 0) | 3,00 m |
      | V3 | 13,0 | (13,00; 0,95; 2,6) | (13,00; 2,45; 0) | 3,00 m |
      | V4 | 13,0 | (13,10; 0,85; 2,6) | (14,40; 0,85; 0) | 2,91 m |
    Obě boční vzpěry míří k východu. Na západ od sloupu 11,1 zbývá ke stěně jen 0,1 m. Vzpěra sloupu 13,0
    k západu by se křížila s V2. Pata V4 zůstává 0,2 m před podezdívkou příčky (s = 14,625).
  - S2 Žebřík (kulisa), SM_RuinLadder 4,5 m ve světnici mezi krokvemi 18,273 a 19,282. Osa s = 18,78.
    Vrchol se opírá o severní líc pozednice (n ≈ 0,97; z ≈ 3,95), pata je na n ≈ 3,13; sklon asi 61°.
  - S3 Hranice kulatiny na srub síně, nádvoří západně od průlomu: obrys s = 8,5–14,3; n = 10,6–12,2;
    výška asi 0,65 m. Obsah = chybějící kulatina sady final ve srubu síně:
      - 4× kulatina 5,76 m Ø 0,23 (západní stěna, řady 1–4),
      - 2× hraněný pultram 5,76 × 0,22 × 0,12 m (západní stěna, řady 0 a 5),
      - 5× kulatina 4,80 m Ø 0,23 (severní stěna síně, řady 4–8),
      - 1× kulatina 3,92 m Ø 0,25 (severní stěna síně, řada 3).
    Uložení: 2 podkladky (kulatina s kůrou Ø 0,15 × 1,8 m, napříč v s = 9,3 a 13,5). Spodní vrstva:
    4× 5,76 m + 2× 4,80 m. Horní vrstva v žlábcích: 3× 4,80 + 1× 3,92 + 2 pultramy. Kulatina je loupaná (srub).
  - S4 Hranice tesaného dřeva krovu, nádvoří východně od průlomu: obrys s = 17,9–24,15; n = 10,6–11,65;
    výška asi 0,7 m. Obsah = chybějící dřevo krovu sady final:
      - 6× krokev 0,18 × 0,22 × 6,24 m (vodorovně 6,0 m, sklon 0,286),
      - 1× západní kus pozednice 0,20 × 0,20 × 5,2 m (s = 10,1–15,3),
      - 1× západní kus vaznice 0,20 × 0,24 × 4,75 m (s = 10,1–14,85).
    Uložení: 3 podkladky (Ø 0,15 × 1,2 m, s = 18,4 / 21,0 / 23,6). Spodní vrstva 4 krokve naplocho, proklady
    z latí 0,05 × 0,06. Horní vrstva 2 krokve, pozednice a vaznice.
  - S5 Hranice prken na krytinu, nádvoří za S4: dvě hranice podle délek krytiny (předání, kap. 5.1)
    (prkna 3,4 m a 3,2 m, šířka náhodně 0,22–0,30, tloušťka 0,035; K_ROOF):
      - S5a 3,4 m: s = 18,0–21,4; n = 12,0–13,45,
      - S5b 3,2 m: s = 21,8–25,0; n = 12,0–13,45.
    Počet v každé = počet prken krytiny v jedné řadě po spádu: ceil((21,7 − 9,8) / (0,26 + 0,015)) = 44.
    Až bude krytina postavená, srovnej počet s daty. Skladba na sušení: 5 prken ve vrstvě s mezerou 0,03,
    9 vrstev, mezi vrstvami proklady z latí příčně po asi 1,1 m (4 na vrstvu), 3 podkladky Ø 0,15 × 1,6 m.
    Výška asi 0,7 m. Lišty přes spáry a latě zatím ne (doplněk).
  - Úprava dřeva: všechno raw; vzpěry a podkladky s kůrou, srubová kulatina loupaná, krokve, pozednice,
    vaznice a prkna tesané.
- Úpravy 03 (zřícenina): ne.
- Dostavba 05: nová stavba Palac_Obydli_Stavenisko, typ props (zr_stavby/vybaveni.py), "stage": "site"
  na úrovni stavby (build_constructions dá sadu všem dílcům). Origin, u, v jsou rám paláce jako u ostatních
  staveb domu. Data jen přes gen_constructions.py → palac(); stavba patří do STAVBY v Palac_Obydli.py
  (za Ohniste).
- Dílce a props:
  - hotové: SM_RuinPole* / SM_RuinLog* / SM_RuinLogBark* (shape "round"), SM_RuinLadder (shape "ladder"),
  - hranoly a prkna: SM_RuinTimber / SM_RuinPlank. Předpoklad: props je umí položit jako dílec dřeva
    bez shape s rozměrem size. Ověř ve vybaveni.build_props a ue_actors; když ne, je potřeba doplnit shape
    "timber" / "plank".
  - nové tvary: žádné.
- Etapa: celá stavba je site. V etapě 2 se skryje celá (Etapa.py). Z base ani final se nic nemění.
- Sdílené rozměry: nový slovník D_SITE v palac_spec.py (vzpěry, žebřík, obrysy hranic S3–S5, podkladky,
  proklady). Délky a počty kusů S3 a S4 se počítají z dat sady final (krokve, pozednice, vaznice, segmenty
  srubu), ne ručně. Při změně final se změní i staveniště.
- Ruční doladění: loose jsou vzpěry V1–V4, žebřík a každá hranice jako celek (poloha hranice jedním
  parametrem v D_SITE). Jednotlivé kusy v hranicích nejsou loose, aby nevzniklo asi 150 actorů.
  Předpoklad: props umí položit kusy hranice jako jeden celek, jinak kusy loose: false a doladění jen přes D_SITE.
- Vazby a kolize:
  - V1–V4 se nesmí bít s patními kameny, podezdívkou příčky a výklenkem střílny s = 14 (13,35–14,65; vzpěra
    V4 jde před výklenkem v n = 0,85, líc zdi je 0,7);
  - žebřík se nesmí bít s krokvemi 18,273 a 19,282, latěmi n = 2,6 a pecí (s = 15,96–17,56);
  - hranice S3–S5 nesmí zasahovat do Palac_S (vnější líc n = 10,2) ani do sebe;
  - volné pásy na nádvoří (aspoň 1,2 m, doporučeno do n = 12,5): před průlomem s = 14,5–17,5, před
    portálem s = 3,2–5,8, před dveřmi do východní místnosti s = 25,9–28,1;
  - pořadí: 03 Palac → Kamen, Krov, Srub, Ohniste → Stavenisko → Etapa.py.
- Ověření: kap. 9.4.
- Varianty:
  - S5 A (doporučuji): celá zásoba prken (2× 44). Materiál pro střechu je zjevně připravený.
  - S5 B: jen první hromada asi 20 prken 3,4 m. Méně dílců, slabší čitelnost.
  - Kozy s rozpracovanou kulatinou a západní kus pozednice v síni (dřívější návrh) odpadají:
    · kulatina 5,7 m se na zápraží západně od vchodu (2,5 × 2,4 m) nevejde,
    · pozednice 5,2 m se v síni vejde jen podélně (n = 0,72–5,98), těsně a přes vzpěry sloupu 11,1,
    · obojí je proto na nádvoří (S3, S4); kozy jsou doplněk, až bude asset.
- Předpoklady a otevřené otázky: kap. 9.5.
- Náčrt slovy: kap. 9.6.
```

### 9.2a Postavená verze a odchylky od 9.2 (21. 11. 2026)

Postaveno ve skriptech, kontroly kap. 9.4 procházejí (`run_checks.py --only obydli`), v UE zatím neověřeno.

- **Uhlí pod plotnou:** box `U` v `_obydli_pec` má příznak `top`, takže patří do sady `stage_top` (`final`). Typ `hearth` se neměnil, data kovárny jsou beze změny.
- **Data:** `palac_spec.py` → `D_SITE` a funkce `obydli_stavenisko()`. Délky, průměry a počty kusů S3 a S4 se počítají z dat sady `final`: krokve 6 × 6,24 m (0,18 × 0,22), pozednice 5,2 m, vaznice 4,75 m, srub síně 4 × 5,76 m a 5 × 4,80 m (Ø 0,23), 1 × 3,92 m (Ø 0,25) a 2 pultramy 5,76 × 0,22 × 0,11 m. Počet prken S5 se počítá vzorcem z kap. 9.2: 2 × 44.
- **Výšky** se měří od terénu v jednom bodě (nový klíč `ref` u položek typu `props`). Vzpěry a žebřík mají stejný ref jako krov a srub (střed domu), každá hranice svůj střed.
- **Hranice jako samostatné objekty (Jirka 21. 11. 2026, mění 9.2 Ruční doladění):** staveniště jsou čtyři stavby ve složce `Stavby/Palac/Obydli/Stavenisko`: `Palac_Obydli_Stavenisko` (vzpěry V1–V4 a žebřík jako samostatné actory, úklid suti) a hranice `_Kulatina` (S3, 14 kusů), `_Tramy` (S4, 14 kusů) a `_Prkna` (S5, 134 kusů). Každá hranice je jeden actor (Instanced Static Mesh) s pivotem dole uprostřed. V UE se posune nebo natočí kolem svislé osy jako celek. `Palac_Obydli_Stavenisko_Capture.py` uloží polohu do `constructions_edits.json` (klíč `pile:<stavba>`) a ta má přednost před `D_SITE`. Náklon hranice se neukládá.
- **Hranoly a prkna** umí typ `props` bez nového tvaru: dílec dřeva bez `shape` s rozměrem `size` dostane mesh `SM_RuinTimber` nebo `SM_RuinPlank` podle poměru stran.
- **S3:** pultramy neleží v horní vrstvě, ale naplocho jako třetí vrstva nad žlábky horní vrstvy (do horní vrstvy se 4 kusy kulatiny a 2 pultramy nevešly). Výška hranice je 0,72 m.
- **S4:** výška je 0,58 m, ne asi 0,7 m (4 krokve naplocho, proklady 5 cm, nahoře 2 krokve, pozednice a vaznice naplocho).
- **S5 (Jirka 21. 11. 2026):** jedna hranice prken 3,4 m v s = 18,0–21,4; n = 12,0–13,45, o 0,5 m vyšší než původní: 15 vrstev po 5 prknech (75 kusů), proklady 4 v každé mezeře mezi vrstvami, 3 podkladky. Vrch je ve výšce 1,375 m. Šířky prken jsou náhodné v rozmezí 0,22–0,30 a v každé vrstvě srovnané na šířku hranice 1,45 m. Původní varianta: dvě hranice po 44 prknech (3,4 m a 3,2 m), výška 0,87 m, `D_SITE` → `boards.variant = "two"`.
- **Žebřík:** pata v n = 3,13, vrchol n = 0,97 a z = 3,95, sklon 61,3°.
- **S6 kozy s rozpracovanou kulatinou (Jirka 21. 11. 2026):** stavba `Palac_Obydli_Stavenisko_Kozy`, jeden objekt jako ostatní hranice. Je to doplněk navíc, kulatina na kozách se nepočítá do kusů S3.
  - Kulatina 5,76 m Ø 0,23 m s kůrou, nahoře asi ve 2/3 délky oloupaná s nerovným okrajem kůry. Nový mesh `SM_RuinLogPeeling` (`mesh_log.py`, varianty A, B; oloupaná strana je +Z, nahoru).
  - Dvě kozy do X z tyčí s kůrou Ø 11 cm v s = 19,3 a 23,1: paty 0,40 m od osy, křížení ve výšce 0,63 m, vrchy tyčí 1,17 m. Kulatina leží ve vidlicích, osa ve výšce 0,95 m.
  - Pod kulatinou leží 5 pruhů kůry 55 × 16 cm (`SM_RuinBarkStrip`).
  - Výchozí poloha je na původním místě hranice prken (s = 18,3–24,1; n ≈ 12,85), protože prkna Jirka přemístil na s ≈ 12, n ≈ 18 (natočení 10°). Rozměry: `D_SITE` → `horses`.
- **Suť:** do obrysu S4 zasahoval kámen suti `Palac_S|R1` (s = 21,38; n = 10,63). Suť pod hranicemi je proto uklizená pomocí `clear_poly` (s = 8,4–25,1; n = 10,45–13,55). Suť nemá sady, chybí tedy v obou etapách.
- **Terén** pod hranicemi je v datech levelu rovný (Z 3129 cm, rozdíl 0 cm).

### 9.3 Pohyb hráče

- **Trasa:** nádvoří → průlom v `Palac_S` (s = 15,1–16,9) → zápraží → mezera vchodu (s = 13,4–14,4) → síň → dveře v příčce (n = 3,3–4,3) → světnice. Druhá trasa vede ze zápraží průchodem v `Palac_pricka_2` (n = 6,9–8,5) do dvorku kovárny. Všude po terénu, bez prahů.
- Zápraží zůstává v etapě 1 bez materiálu.
- Nízký srub síně (1,16 m) ani srovnané příčky (1,4 m) se nedají přejít.
- Vzpěry zabírají pás u jižní zdi síně do n = 2,45. Trasa ze vchodu ke dveřím v příčce vede po n ≥ 3,2 a zůstává volná.
- Hranice na nádvoří jsou přes nízkou `Palac_S` vidět z nádvoří i ze zápraží.

### 9.4 Kontroly etapy 1 (`run_checks.py --only obydli`, `check_obydli`)

Kontroluje se sestava `base` + `site`. Kontroly sady `final` zůstávají, jak jsou.

1. Každá krokev `base` leží na třech podporách `base` (pozednice, vaznice, vrchní trám severní stěny). Tahle kontrola už existuje.
2. Nic z `base` ani `site` nevisí ve vzduchu:
   - spodek dílce je na terénu (±3 cm), nebo leží na jiném dílci téže sady (vrstvy hranic, podkladky, proklady),
   - horní konec vzpěry se dotýká líce sloupu (≤ 2 cm).
3. Sloupy bez `base` pozednice (11,1 a 13,0) mají každý dvě vzpěry.
4. Trasy z kap. 9.3 a volné pásy na nádvoří (9.2, Vazby) jsou průchozí v šířce aspoň 1,2 m.
5. Dílce `site` se neprotínají s `base`, se zříceninou ani mezi sebou (kromě styku vrstev v hranici).
6. Počty v hranicích odpovídají chybějícím dílcům `final`: krokve 6, pozednice 1, vaznice 1, srub síně 10 + 2 pultramy.
7. V etapě 2 (`base` + `final`) není vidět žádný dílec `site`.

Vizuální kontrola v UE (Jirka): `Palac_Obydli.py`, pak `Etapa.py` s `ETAPA = 1` a pohled z nádvoří přes průlom a ze síně. Pak `ETAPA = 2` a kontrola, že staveniště zmizelo.

### 9.5 Předpoklady a otevřené otázky

- Ověřeno (21. 11. 2026): nádvoří před `Palac_S` je pod hranicemi rovné (rozdíl 0 cm) a volné, jen jeden kámen suti byl uklizen (9.2a).
- Ověřeno (21. 11. 2026): props umí hranoly a prkna (`SM_RuinTimber`, `SM_RuinPlank`). Hranici jako jeden celek posunout neumí, posouvá se v `D_SITE` (9.2a).
- Kde v etapě 1 spí posádka, návrh staveniště neřeší. Bude to samostatný task (Jirka 21. 11. 2026).
- Doplňky na později (zatím bez assetů): hlína a mech na spáry, třísky, latě a lišty, kámen nebo proutí na komín. Kozy s rozpracovanou kulatinou a pruhy kůry jsou hotové (9.2a, S6). Nářadí má hotové meshe (`axe`, `broadaxe`, `crosscut_saw`, `mallet`), jde přidat kdykoli.
- Zodpovězeno: žebřík je jen kulisa. Etapy se přepínají sadami actorů (kap. 0.1).

### 9.6 Náčrt slovy

**Půdorys (rám paláce):**
- Na jihu je `Palac_J` a pod ním řada pěti sloupů v n = 0,85.
- Západní dva sloupy (11,1 a 13,0) stojí v síni volně. Každý má vzpěru k severu (pata n = 2,45) a k východu (paty s = 12,7 a 14,4).
- Ve světnici je u jižní zdi pec (s = 15,96–17,56) a východně od ní žebřík opřený o pozednici v s = 18,78, pata asi 2,2 m od zdi.
- Severně je srubová stěna n = 6,2, za ní zápraží (bez materiálu) a `Palac_S` s průlomem s = 15,1–16,9.
- Za `Palac_S` na nádvoří:
  - západně od průlomu hranice srubové kulatiny (s = 8,5–14,3; n = 10,6–12,2),
  - východně od průlomu hranice krokví a trámů (s = 17,9–24,15; n = 10,6–11,65),
  - za ní dvě hranice prken (s = 18,0–21,4 a 21,8–25,0; n = 12,0–13,45),
  - před průlomem, portálem a dveřmi do východní místnosti zůstávají volné pásy.

**Řez napříč (po n, pohled k západu):**
- Sloup 3,83 m s pozednicí na vrchu (4,03 m) jen od s = 15,3 na východ.
- Nad síní stojí sloupy bez pozednice, vzpěra jde z 2,6 m šikmo k severu na terén 1,5 m od sloupu.
- Ve světnici krokve se sklonem 0,286 z pozednice přes vaznici (n = 4,4; 3,0 m) na srub (2,5 m), přesah do n = 6,8.
- Žebřík od pozednice dolů k severu pod sklonem 61°.
- Na nádvoří hranice vysoké 0,65–0,7 m, za nízkou `Palac_S` (1,1–1,4 m) jsou z nádvoří vidět celé, ze zápraží jejich horní část.

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
