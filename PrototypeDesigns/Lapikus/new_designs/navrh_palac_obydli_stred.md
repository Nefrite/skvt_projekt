# Návrh: Palac_Obydli – obytná stavba posádky v prostřední místnosti paláce

Specifikace od architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **staví se po krocích** (16. 11. 2026): plán po etapách a stav je v kap. 0, která platí přednostně; kamenné části jsou ve skriptech. Je to kopie návrhu `navrh_palac_obydli.md` (dům ve východní místnosti u věže) přenesená do **prostřední místnosti**. Původní dokument zůstává beze změny pro srovnání. Náčrty: `navrh_palac_obydli_stred.png` (hotová stavba) a `navrh_palac_obydli_stred_etapa1.png` (rozestavěný stav). Jsou to schémata, ne přesné modely.

**Připravenost (15. 11. 2026)** – podrobně `..\CHECKLIST_assets_navrhy.md`. **Tohle je platný návrh domu**, varianta ve východní místnosti je zavržená.
- **Hotové dílce stavby:** loupaná kulatina `SM_RuinLog` (srub), trámy, sloupy a prkna (`SM_RuinTimber`, `SM_RuinPost`, `SM_RuinPlank`), žlab `SM_RuinGutter` / `SM_RuinGutterBark` s vidlicí `SM_RuinForkHead`, dymník `SM_RuinSmokeHood`, komín `SM_RuinChimney`. Materiály: loupané dřevo (`peeled`), výplň spár srubu `MI_RuinChinking`, mazanina, proutí.
- **Hotové vybavení (kap. 4.8):** lůžko `SM_RuinBed` / `SM_RuinBedFolded`, stůl `SM_RuinTable`, truhla `SM_RuinChest`, police `SM_RuinShelf`, ponk `SM_RuinWorkbench` (menší škálováním), hranice dřeva `SM_RuinWoodpile`, dveře `SM_RuinDoor`, okenice `SM_RuinShutter` (0,5 × 0,5 m škálováním), žebřík `SM_RuinLadder`.
- **Hotové pro staveniště (kap. 9.2):** žebřík, koš `SM_RuinBasket`, tesařské nářadí (sekera, širočina, dvoumužná pila, kladivo, palice).
- **Chybí:** typy staveb `pult_roof`, `log_wall`, `hearth`, `gutter`, rozšíření `stone_addon` o tloušťku, strop s výměnou, rozmístění props, přepínač `ETAPA`, `tools/ruin/palac_spec.py`, úprava 03 (kap. 3). Ze staveniště tesařské kozy, rozpracovaná kulatina, hromady materiálu, loupák, třísky na zemi. Dále zářez srubu v nárožích, saze, udusaná hlína, oheň a kouř.

**Proč prostřední místnost (Jirka, 14. 11. 2026):** součástí osídlení bude provizorní kovárna a u věže má komín špatný tah. Prostřední místnost je 11 m od věže, jižní zeď je tu rovnoměrnější. Vstupem byl původně portál; od 16. 11. 2026 je portál v západní místnosti a sem se vchází hrubým průchodem po něm (kap. 0.2a).

## 0. Plán stavby po etapách (16. 11. 2026, platí přednostně před kap. 3–9)

Dohodnuto s Jirkou 15.–16. 11. 2026. Kde se tato kapitola liší od starších kapitol níž, platí tato. Co zbývá dodělat a na co si dát pozor, je v předávacím dokumentu `new_designs/predani_palac_obydli_stavitel.md`.

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
- **Ladí se nejdřív hotový stav** (základ + dostavba), staveniště a kontrola etapy 1 až nakonec.
- **Dřevo je surové (`raw`) v obou etapách**, krov i krytina. Dehtování může přijít jako pozdější třetí stav. Srub je loupaná kulatina se stejným materiálem v obou etapách.
- **Dveře a okenice** jsou v etapě 2 otevřené (kulisa, než se rozhýbou). **Žebříky** nejsou pro postavu použitelné (chybí animace); půda bude mít vlastní žebřík, staveništní zmizí.
- **Sklep** se neřeší. Jestli přijde, podřídí se stavbě.

### 0.2 Výchozí stav po úpravě `Palac_J` (změřeno z dat 16. 11. 2026)

Celá `Palac_J` je zanořená o 0,31 m (`navrh_palac_kovarna.md` kap. 3). V prostřední místnosti z toho plyne:

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
| `Palac_Obydli_Stavenisko` | rozmístění props, vše `site` | – | – | ⬜ až nakonec |

- **Staveniště (`site`)**: dočasné vzpěry západních sloupů, žebřík, kozy s rozpracovanou kulatinou, západní kus pozednice na zemi, hromady kamene, hlíny, kulatiny, krokví a prken, nářadí, třísky. Zásoba materiálu se „spotřebuje“, proto mizí celá.
- **Stavební logika etapy 1** (od západu k východu, východ je dál): krokve nad světnicí leží na třech podporách, které už stojí (pozednice na 3 sloupech, vaznice na příčce a východní stěně, severní stěna). Západní sloupy stojí bez pozednice, proto mají vzpěry. Základ ohniště je hotový dřív než podlaha. Nic se nestaví dřív, než má na čem ležet.

### 0.4 Pořadí stavění (ladí se hotový stav)

1. ✅ Sady etap v build skriptu, `palac_spec.py` → `obydli`, `Palac_Obydli_Kamen`, základ `Palac_Obydli_Ohniste`.
2. ✅ `Palac_Obydli_Krov` bez krytiny (rozšíření `pult_roof`: dělené pozednice, vaznice uložená na stěnách).
3. ✅ `Palac_Obydli_Srub` se štíty a otvory (`log_wall`).
4. Krytina a lemování s prostupem komína, strop se zavěšením dymníku, podlaha, okap. (Pec s dymníkem a komínem už stojí, kap. 0.5b.)
5. Vybavení (dveře, okenice, nábytek).
6. Staveniště a kontrola etapy 1 (trasa hráče, vzpěry, nic nevisí ve vzduchu).

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
- **Otvory jsou zarovnané na řady:** vchod 1,0 × 2,28 m, dveře v příčce 1,0 × 2,17 m, okénko světnice 0,6 × 0,66 m (parapet 1,4 m), okénko síně 0,5 × 0,44 m (parapet 1,4 m). Zárubně, dveře a okenice přijdou s vybavením.

**Odchylky od kap. 4 (důvod):**

- střední sloup v s = 15,3 místo 15,6, spoj pozednice je nad ním; příčka je od 16. 11. 2026 západně od něj (kap. 0.5a);
- pozednice je dlouhá jako vaznice (s = 10,1–21,4 místo 10,9–20,6), aby na ní ležely i štítové krokve;
- vaznice leží na špalcích 28 cm (srub končí ve 2,5 m, spodek vaznice je ve 2,78 m);
- krokve začínají v n = 0,8 místo 0,75 (kameny líce `Palac_J` vystupují až o 5 cm);
- komín je v s = 16,76 (v 16,9 by zasáhl do krokve s = 17,26); stojí s pecí (kap. 0.5b), prostup krytinou přijde s krytinou;
- dveře v příčce mají světlou výšku 2,17 m místo 2,2 m (zarovnání na řady);
- štíty končí rovně pod vrchem krokví, u příčky zůstává pod krytinou stupňovitá mezera do 7 cm.

**Okap (rozhodnutí Jirky 16. 11. 2026, staví se v kroku 4):** žlab má spád k západu, od kovárny. Sud stojí pod jeho západním koncem, svod přes zápraží se nedělá. Cesta ze zápraží ke kovárně tak zůstává volná. Kap. 4.7 a poznámka o svodu v kap. 6 tím neplatí.

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
| Vstup | původní dveře | původně portál, od 16. 11. 2026 hrubý průchod po rozebraném portálu |
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
| Kulatina na srub | 11 ks Ø 22 cm × 5,7 m, ve dvou vrstvách | na nádvoří před severní zdí paláce, západně od průchodu (s = 16) |
| Krokve a západní kus vaznice | 6 ks 6,3 m + 1 ks 5,7 m | na nádvoří před severní zdí paláce, východně od průchodu (s = 16) |
| Prkna na krytinu | první hromada, asi 20 ks | na nádvoří u krokví |

- Polohy hromad jsou doporučené, přesné rozmístění určí game designer. Podmínka: cesta průchod v `Palac_S` → vchod → dveře do světnice a cesta po zápraží ke kovárně zůstávají volné v šířce aspoň 1,2 m.
- Hromady a nářadí mají být samostatné actory (`loose`), aby se daly doladit ručně.

### 9.3 Pohyb hráče

- **Trasa:** nádvoří → průchod v `Palac_S` → zápraží → mezera pro vchod → síň → otvor v příčce → světnice. Všude po terénu, bez prahů. Druhá trasa: zápraží → průchod v `Palac_pricka_2` → dvorek kovárny.
- **Nízký srub síně (1,13 m) se nedá přejít,** dovnitř se jde jen mezerou pro vchod.
- **Srovnané příčky (1,4 m) jsou bez průchodu.** Do západní a východní místnosti se z domu nedá projít; ke kovárně se jde ze zápraží průchodem v `Palac_pricka_2`.
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

- **Půdorys:** obdélník 11,3 × 5,6 m u jižní zdi prostřední místnosti. Jižní stranu tvoří `Palac_J`, obě boční stěny stojí na příčkách, severní je nový srub. Srubová příčka v s = 15,75 dělí dům na světnici (východ) a síň (západ). Ohniště je ve světnici u jižní zdi hned za příčkou. Vchod je v severní stěně do síně, šikmo proti průchodu v `Palac_S`. Před domem zápraží 2,3 m, z něj na východ průchod ke kovárně.
- **Řez jih–sever:** u jižní zdi sloup s pozednicí (vrch 4,03 m), krokve klesají 16° přes střední vaznici (vrch 3,02 m ve n = 4,4) na srubovou stěnu (vrch 2,50 m ve n = 6,2) a přesahují ji o 0,5 m. U jižní zdi stoupá komín do 5,3 m, zeď je vedle něj snížená na 4,3–4,7 m. Ve světnici strop se spodkem trámků 2,3 m, nad ním půda.
- **Boční stěna:** dole stará příčka srovnaná kamenem na 1,4 m, nad ní pět řad kulatiny do 2,5 m, nad tím trojúhelník svislých prken pod střechu.
- **Pohled od nádvoří:** přes nízkou zeď a průchodem je vidět srubová stěna s dveřmi, nad zdí paláce vykukuje tmavá prkenná střecha stoupající k jižní zdi a nad ní komín.
