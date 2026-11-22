---
# orchestrace
type: reference
validity: valid
updated: 2026-11-22
aliases: []
# hra
domain: structures
entity: "[[Lapikus]]"
---
# Rozhodnutí: zřícenina Lapikus

## Souhrn
Tabulka rozhodnutí k zřícenině Lapikus z 11/2026 (z `KNOWHOW_hrad.md`, kap. 7), aby se neotevírala znovu. Tematicky pokrývá:
- **Architektura projektu:** 03 a 05 oddělené, sdílená knihovna `zrlib`, hlavní složka `PrototypeDesigns/Lapikus`, vlastní procedurální props, generátor meshí, buildy `build_normal.py` a `build_fullscope.py`, 06_furnishing a jeden JSON pro vybavení.
- **Palác:** dům posádky v prostřední místnosti (varianta u věže zavržená), kovárna ve východní místnosti (výheň v koutě, zanořená `Palac_J`), etapy domu, portál v západní místnosti.
- **Věž a brána:** průlomy z dobývání z východu, přístřešek varianty B, výšky staveb na zdech s různou patou absolutně v UE cm.
- **Technické zásady:** maltové jádro nového zdiva, srub s půltrámy v nárožích, kontrola kolizí před stavbou dřeva.
- **Otevřené otázky** (konec dokumentu): stan na nádvoří, kůra nebo loupané dřevo u jednotlivých staveb, výstup na podestu brány, poloha cisterny.

<!-- Z KNOWHOW_hrad.md kap. 7 (pilot Lapikus, B6). Rozhodnutí, aby se neotevírala znovu. -->

| Datum | Rozhodnutí | Proč |
|---|---|---|
| 11/2026 | 03 a 05 oddělené, sdílená knihovna `zrlib` | dostavby jdou ladit bez přegenerování hradu |
| 14. 11. 2026 | hlavní složka je `skvt_projekt\PrototypeDesigns\Lapikus` | odtud se spouští v UE, je v gitu |
| 14. 11. 2026 | **props vlastní**, procedurálně v Pythonu (`tools/meshes/mesh_props.py`) | styl hradu, vizuální prototyp |
| 14. 11. 2026 | kulatina **s kůrou i bez**, podle stavby | pod kůrou dřevo hnije, nosné se loupe |
| 14. 11. 2026 | jeden generátor meshí `tools/meshes/gen_meshes.py` + moduly podle materiálu, OBJ v `meshes/<kategorie>/` | meshe používá 03 i 05 |
| 14. 11. 2026 | tvary na míru (plátno) jako OBJ, lano a výplet z knihovních dílců | bez Geometry Scriptu v UE |
| 14. 11. 2026 | **dům posádky v prostřední místnosti paláce**; varianta u věže zavržená | ve východní místnosti má být kovárna, komín u věže má špatný tah |
| 14. 11. 2026 | brus v kovárně **šlapací**, s třínohou stoličkou | – |
| 14. 11. 2026 | věž: průlomy z dobývání ve `Vez_V` a `Vez_J` místo rovného snížení; přístřešek varianta B | hrad se dobýval od východu a jihovýchodu; posádka by zeď kvůli plachtě nebourala |
| 15. 11. 2026 | meshe se importují přes dočasný asset, cíl s `bDoFastBuild` se maže, vlastní klíč cache (`BUILD_CFG`) | [[Pasti_import_meshi_a_assety]] |
| 15. 11. 2026 | dva celkové buildy: `build_normal.py` (aditivní) a `build_fullscope.py` (oprava); fullscope materiály ve výchozím stavu nemaže | ruční ladění materiálů se nemá ztratit |
| 15. 11. 2026 | level je celý generovaný skriptem, skripty můžou počítat s prázdným projektem | Jirka může cokoli generovaného ručně smazat |
| 15. 11. 2026 | **kovárna ve východní místnosti paláce potvrzena**; staví se ve 4 krocích (přístřešek bez krytiny → výheň a krytina → stěna a okap → vybavení) | po každém kroku náhled a kontrola v UE |
| 15. 11. 2026 | kovárna: západní linie s = 25,85 (ne 25,5), komín s = 30,0; n = 1,35 (mezi krokvemi n = 0,9 a 1,8), žlab do sudu bez svodu | stěna končila ve výklenku střílny, komín procházel pozednicí, svod by přehradil dvorek (`navrh_palac_kovarna.md`) |
| 15. 11. 2026 | **výheň kovárny je v koutě** mezi `Palac_J` a věží (ne u věže dál od zdi); celá `Palac_J` zanořená o řadu kamene do země (03 `z_offset` −0,31 m, počet řad se nemění) a u věže rozebraná (`breaches`), aby ji komín přesahoval; rohový sloup odpadl, východní pozednice je v kapse `Palac_J`; komín mezi krokvemi n = 0,9 a 1,8 | rozhodl Jirka; výklenek střílny s = 29 vedle výhně zůstává volný jako manipulační prostor |
| 15. 11. 2026 | kovárna: krokve přesahují západní stěnu o 0,9 m, hranice dřeva je zvenku pod přesahem; dymník visí na závěsných tyčích z výměn mezi krokvemi | dřevo má být kryté a nezabírat místo v kovárně; nic nevisí ve vzduchu |
| 15. 11. 2026 | krytina `pult_roof` má vlastní kód (stejná skladba jako u ostrohu): latě přes celou šířku, prkna od okrajů prostupu komína ven; okapová hrana 10 cm za konci krokví nad osou žlabu; výšku žlabu bere `gutter` z krytiny střechy | krokve jsou rovnoběžné, dělení na klínová pole krovu u ostrohu tu nemá smysl; žlab se posune se střechou |
| 16. 11. 2026 | **dům posádky se staví po etapách** podle `navrh_palac_obydli_stred.md` kap. 0: tři sady actorů s anglickými jmény, přepnutí v Blueprintu podle tagu; dřevo surové v obou etapách (dehtování možná později); ohniště má v etapě 1 celý kamenný základ, studené; dveře a okenice otevřené; žebříky jen kulisa; sklep se neřeší; ladí se nejdřív hotový stav | hráč domem jen prochází, etapy dávají dojem času |
| 16. 11. 2026 | nové zdivo na staré zdi (`stone_fill`) má maltové jádro v ose od země až pod vrch, i přes zříceninu pod ním | posádka by starou zeď vyspravila; zdí neprosvítá (stejně jako u `Ostroh_Dostavba`) |
| 16. 11. 2026 | srub (`log_wall`): křížící stěny mají řady posunuté o půl řady (začínají a končí půltrámem), kulatina je o 1,2 cm tlustší než řada | nároží vypadá jako skutečný srub a zdí neprosvítá bez výplně spár |
| 16. 11. 2026 | zkušební `ruin_layout.json` mimo `03_ruin/blocks` se počítá bez terénu z levelu (`terrain_from_level.json` leží vedle skutečného souboru): výšky zdí vyjdou až o 2 m jinak. Před stavbou na koruně zdi změř skutečné výšky ze stavu s terénem z levelu a návrh s nimi porovnej | návrh strážní podesty počítal s korunou `Brana_V` o 1,6–2 m níž, než je |
| 16. 11. 2026 | stavby na zdech s různou patou (brána) mají výšky absolutně v UE cm: otvor 03 s `z_abs`, `stone_fill` s `top_abs` / `bottom_abs`, typ `platform` | terén v průjezdu je šikmý a `Brana_V` má podstavbu a `z_offset` |
| 16. 11. 2026 | návrh domu měl sloup v ose příčky a komín v krokvi; před stavbou dřeva vždy porovnat polohy sloupů, krokví a komína s podezdívkami a mezi sebou | kolize se v textu návrhu nepozná, ukáže ji až výpočet |
| 16. 11. 2026 | portál paláce je v západní (prázdné) místnosti, ve střední ho posádka rozebrala (hrubý průchod v `Palac_S` s = 16); `Palac_pricka_2` má severně od domu hrubý průchod ke kovárně | kámen šel na podezdívky domu; ze zápraží se dá projít ke kovárně |
| 16. 11. 2026 | úprava 03 u komína domu a dozdívka koruny `Palac_J` odpadají | po zanoření zdi o 0,31 m je koruna u komína 4,4–4,8 m a všude nad krytinou |
| 16. 11. 2026 | **vybavení = 06_furnishing**: vše, co člověk přenese (props), samostatně od staveb 05 (vlastní data `furnishing.json` včetně poloh z levelu, viz další řádek; tag `Zricenina_Vybaveni`); pevné kusy (výheň, sud pod okapem, kůl v zemi) zůstávají v 05 | vybavení se ladí a přesouvá nezávisle na stavbách; rozhodl Jirka |
| 16. 11. 2026 | **vybavení: jeden JSON** – capture zapisuje polohy, otočení a velikost (`scale`) přímo do `furnishing.json` v rámu stavby, smazané (`removed`) a kopie z levelu (`manual`) taky; `gen_furnishing.py` slučuje a uložené polohy nechá; `furnishing_edits.json` zrušen | jedno místo s pravdou o poloze, nové generování postaví kusy rovnou na správné místo; rám stavby, aby kusy přežily posun rámu i změnu terénu; rozhodl Jirka |
| 17. 11. 2026 | věž dobývaná z východu: `Vez_Z` jen vedlejší škody, střed vyšší (`protect`), mezera pod přístřeškem se tím z velké části zavře, zbytek je větrání; `Vez_S` bez průlomu do tvaru U, koruna plynule klesá od západu k SV rohu a navazuje na průlom `Vez_V`; západní kůl přístřešku smí zakrýt okraj výklenku okna, když se do výklenku dá vejít; data v `tower_spec.ruin_edits()` | rozhodl Jirka |
| 16. 11. 2026 | typ `props` (samostatné actory, polohy ve specu) slouží 06 i pevným kusům 05; suť se uklízí `clear_poly` stavby; celá kovárna má souhrnný spouštěč `Palac_Kovarna.py` | ruční doladění přes capture, žádný duplicitní kód |
| 16. 11. 2026 | kovárna rozšířená o řadu krokví k severu (střecha do n = 6,6), sloup u věže i v n = 4,4; kovadlina 1,5 m před výhní; okno věže nad střechou je jen světlík (neprůchozí) | málo místa na vybavení; kovadlina a kalicí sud byly příliš blízko výhni |
| 15. 11. 2026 | typy `pult_roof`, `hearth`, `gutter` se píšou obecně (i pro dům); `ETAPA`, saze, udusaná hlína, žhavé uhlí a VFX ohně se s kovárnou nedělají | kovárna stojí v obou etapách; okno věže nad střechou se neřeší |

## Otevřené otázky

- [ ] jestli bude stan na nádvoří — z KNOWHOW_hrad, 2026-11-17
- [ ] přiřazení kůra / loupané u jednotlivých staveb — z KNOWHOW_hrad, 2026-11-17
- [ ] výstup na podestu brány — z KNOWHOW_hrad, 2026-11-17
- [ ] poloha cisterny — z KNOWHOW_hrad, 2026-11-17
