---
# orchestrace
type: reference
validity: superseded
superseded_by: "[[Konvence_assetu]]"
updated: 2026-11-23
aliases: [katalog props, katalog meshí]
# hra
domain: structures
entity: "[[Lapikus]]"
build_step: 06_furnishing
assets: ["/PrototypeDesigns/Lapikus/tools/meshes/mesh_props.py", "/PrototypeDesigns/Lapikus/tools/meshes/mesh_textile.py", "/PrototypeDesigns/Lapikus/tools/meshes/ukazka.py"]
---
# Katalog props a meshí na míru (stan, guesthouse)

> **Nahrazeno (P19, 2026-11-23):** karty assetů v `Assets/` (stan a Guesthouse: [[SM_RuinCanvasTent_A]], [[SM_RuinCampBed_A]], [[SM_RuinChestSmall_A]], [[SM_RuinBundle_A]], [[SM_RuinBedLarge_A]], [[SM_RuinChestLocked_A]], [[SM_RuinArmorStand_A]]; chybějící kusy jako požadavky [[SM_RuinDesk_A]], [[SM_RuinShelfTall_A]], [[SM_RuinWoodpileSmall_A]], [[SM_RuinWeaponRack_A]]) a společná pravidla v [[Konvence_assetu]]. Dokument se dál neudržuje.

## Souhrn
Karty knihovních meshí z 21.–22. 11. 2026 (AssetGenerator) pro stan na nádvoří a Guesthouse: jak je použít ve stavbě a vybavení a jak je upravovat. Starší props (kovárna, obydlí, nářadí) jsou v [[05_constructions]] (tabulka *Props*).
- **Společné konvence:** kód v `mesh_props.py` a `mesh_textile.py`, pivot ve středu bounding boxu, osy v UE (cm, Z nahoru), jmenovitý rozměr = bounding box, sloty materiálů, směr let dřeva, postup změny tvaru.
- **Stan ([[Nadvori_Stan]]):** plachta stanu, lůžko (i se složenou houní), truhlička, vak.
- **Guesthouse ([[navrh_guesthouse_vybaveni]]):** postel, kovaná truhla, stojan na brnění; stůl, regál, hromádka dřeva a stojan na zbraně zatím bez meshe.
- **Stav:** všechny meshe jsou importované do UE (22. 11. 2026), vzhled neověřen; postel (verze 2) a stojan na brnění (verze 3) čekají na nový import.

Karty knihovních meshí z 21.–22. 11. 2026 (AssetGenerator), jak je použít ve stavbě a vybavení a jak je dál upravovat. Starší props (kovárna, obydlí, nářadí) jsou v přehledu v [[05_constructions]] (tabulka *Props*). Stav požadavků vede [[CHECKLIST_assets_navrhy]] (kap. 6.5, 6.8).

## Společné konvence

- **Kód:** props v `tools/meshes/mesh_props.py` (kategorie `props`, v UE `/Game/Skvt/Lapikus/Ruin/Props`), plachty a textil v `tools/meshes/mesh_textile.py` (kategorie `textile`, v UE `Ruin/Textile`). Záznam v `zrlib/config.py`: `LIB_MESHES` (jmenovitý rozměr, varianty, sloty, základní materiál), `LIB_SHAPES` (klíč `shape` pro data), `STONE_MESH_VERSION`.
- **Pivot:** střed bounding boxu (výchozí pro všechny props, Jirka 21. 11. 2026). Typ `props` v datech bere `z` jako **spodek** kusu nad terénem nebo podlahou a střed dopočítá sám (`zc = z + sz / 2`); `zc` = střed.
- **Osy:** UE, cm, Z nahoru. Každá karta uvádí, kam míří čelo, hlava nebo zámek. Natočení v datech: `x = (da, dc)` = směr lokální osy X v rámu stavby; lokální +Y je X otočená o +90° v UE.
- **Rozměr:** jmenovitý rozměr = bounding box meshe (`NOMINAL` v modulu = `LIB_MESHES`). `size` nebo `scale` v datech mesh natáhne; props se mají klást v jmenovitém rozměru (scale 1).
- **Materiál:** slot `Wood` = úprava dřeva z dat (`finish`: `raw`, `oil`, `tar`, `old` …), ostatní sloty jsou pevné (`SLOT_MI`, `CLOTH_MI`). Nábytek hosta: doporučená úprava `oil` (kvalitnější), stan: `raw`.
- **Ukázka v UE:** `tools/meshes/ukazka/Ukazka_Stan.py`, `Ukazka_Guesthouse.py` (jen meshe tématu; seznam v `UKAZKY` v `tools/meshes/ukazka.py`).
- **Změna tvaru:** upravit funkci → přegenerovat jen ten mesh `python tools/meshes/gen_meshes.py --only <prefix>` → nový bounding box zapsat do `NOMINAL` a `LIB_MESHES` → zvednout `STONE_MESH_VERSION[<prefix>]` (jinak UE starý mesh nepřenačte) → kompletní `gen_meshes.py` do dočasné složky a md5 ostatních OBJ beze změny → náhled → ukázka v UE. Seed propu se odvozuje z pořadí v `PROPS`: nový prop vždy **na konec** seznamu.
- **Směr let dřeva:** dřevo se řeže tak, aby léta vedla podél **nejdelšího rozměru dílu**, případně podél směru, kde díl potřebuje pevnost (sloupek, noha, příčka, kolík, topůrko, prkno, soustružená hlavice podél osy). Textury dřeva mají léta podél U, takže UV dílu musí mít U podél jeho délky. V `mesh_props.py` to zajišťuje `grain="long"` u `add_box`, `add_cyl`, `add_lathe`, `add_prism` (Jirka 22. 11. 2026). Výchozí `GRAIN_DEFAULT = None` drží staré props beze změny; přepnutím na `"long"` se pravidlo uplatní na všechny props (změní UV 31 props, pak zvednout jejich `STONE_MESH_VERSION`; úkol T-0024 v `Maintenance/queue.md`).
- **Vytažený profil (`add_prism`):** body obrysu proti směru hodinových ručiček; po zrcadlení souřadnice obrátit pořadí (jinak normály dovnitř, v UE chybí plochy; 22. 11. 2026 jařmo stojanu na brnění).

## Stan na nádvoří ([[Nadvori_Stan]])

Rozmístění (Jirka 22. 11. 2026): jedno lůžko na straně spuštěné chlopně, hlavou k zadnímu štítu, vnější okraj asi 0,9 m od osy stanu; truhlička vedle lůžka u hlavy; vak pohozený o kus vedle. Stojky, hřeben, kolíky, šňůry a stříška skládá Builder z hotových meshí (typy `tent`, `bark_roof`).

### Plachta stanu `SM_RuinCanvasTent_A`

| | |
|---|---|
| Data | `shape: canvas_tent`, `cat: canvas` (`MI_RuinCanvas`, oboustranný `M_RuinCloth`) |
| Rozměr | 246,0 × 227,7 × 189,6 cm; půdorys 2,4 × 2,2 m, hřeben 1,9 m, boky asi 60° |
| Osy | X podél hřebene, **+X = štít se vchodem**, +Y = strana odhrnuté chlopně, −Y zavřená chlopeň; zadní štít (−X) zavřený |
| Na míru | `meshes/textile/SM_RuinCanvasTent_A.json`: `center` (střed bounding boxu v osách stanu, počátek na zemi pod středem hřebene), `size`, `ridge` (vrch 190 cm, Ø 6, x −130…130), `poles` (stojky Ø 7 v x = ±120), `pegs` (13 kolíků, lem k zemi), `door`. Stavba posadí mesh podle `center` (vzor `zr_stavby/pristresek.py`, `LIB_SHAPE_OF`). |
| Zdroj | `mesh_textile.canvas_tent(TENT)`; parametry `TENT`: `L`, `W`, `H`, `sag` (prohnutí boků), `bulge` (vydutí štítů), `hem` (zvednutí lemu mezi kolíky), `pegs_x`, `pegs_back`, `pegs_door`, `flap` (úhel odhrnuté chlopně u švu a u volného rohu) |
| Poznámka | Vchod jen shrbeně (polovina štítu, při 0,7 m šířky asi 0,7 m výšky), schválil Jirka 22. 11. 2026. Pro chlopeň na druhé straně stačí mesh zrcadlit (scale Y −1). |
| Náhled | `05_constructions/Stan_plachta_nahled.png` |

### Lůžko `SM_RuinCampBed_A`, `SM_RuinCampBedFolded_A`

| | |
|---|---|
| Data | `shape: camp_bed` (houně přes slámu), `camp_bed_folded` (houně složená v nohách); `finish: raw` |
| Rozměr | 198,8 × 76,2 × 28,8 cm (A), 200,0 × 76,5 × 32,1 cm (Folded) |
| Osy | X podél lůžka, **hlava −X** |
| Konstrukce | 2 příčné klády s kůrou Ø 15 × 75 cm (26 a 24 cm od konců), 10 tyčí s kůrou Ø 5 × 200 cm, sláma (pod hlavou o 3 cm víc), houně s převisem 10 cm |
| Sloty | `Wood`, `EndGrain`, `Bark`, `Straw`, `Wool` |
| Funkční | vrch slámy asi 25 cm nad zemí; plachta je ve vzdálenosti 0,9 m od osy stanu 35 cm nad zemí |
| Zdroj | `mesh_props.camp_bed(seed, folded)`, pomocná `_pole` (prohnutá tyč s kůrou) |
| Náhled | `05_constructions/Stan_luzko_nahled.png`, `Stan_luzko_slozena_nahled.png` |

### Truhlička `SM_RuinChestSmall_A`

| | |
|---|---|
| Data | `shape: chest_small`; `finish: raw` |
| Rozměr | 59,3 × 38,0 × 31,7 cm (korpus 55 × 35 × 32, s držadly) |
| Osy | **zámek (oko na zámek) −Y**, držadla ±X; k lůžku se klade zámkem do uličky |
| Sloty | `Wood`, `Iron` (s patinou rzi) |
| Zdroj | `mesh_props.chest_small` |
| Náhled | `05_constructions/Stan_truhlicka_nahled.png` |

### Vak (ranec) `SM_RuinBundle_A`

| | |
|---|---|
| Data | `shape: bundle`; materiál pevný |
| Rozměr | 76,0 × 43,4 × 22,5 cm; vak asi 62 × Ø 30 cm, leží na boku |
| Osy | **dno −X, hrdlo +X** (stažené dvěma závity lana, roztřepený okraj), popruh přes rameno leží volně na zemi na straně +Y |
| Sloty | `Sackcloth` (`MI_RuinSackcloth`: zažloutlé plátno, hustší skvrny, zaprášený vršek), `Rope` |
| Zdroj | `mesh_props.bundle`, pomocná `_rope` (lano podél křivky, prameny jako `SM_RuinRope`) |
| Náhled | `05_constructions/Stan_vak_nahled.png` |

## Guesthouse ([[navrh_guesthouse_vybaveni]], polohy `tools/ruin/ostroh_spec.py` → `GH_*`)

Nábytek hosta je kvalitnější než v domě, ale pořád ručně a hrubě opracovaný (Jirka 22. 11. 2026). Graybox se mění za mesh v `ostroh_spec.py` (`GH_MESH`: id kusu → `shape`, `finish`; `size` z `LIB_MESHES`). **22. 11. 2026 rozmístěné:** postel, truhla, stojan na brnění a stolička (skupina `Guesthouse_Vybaveni`, [[stav_guesthouse]]).

### Postel `SM_RuinBedLarge_A` (graybox `GH_BED`)

| | |
|---|---|
| Data | `shape: bed_large`; `finish: oil` |
| Rozměr | 250,2 × 109,1 × 95,0 cm (graybox 2,50 × 1,09 × 0,62 m; vyšší je jen čelo v hlavě ❓) |
| Osy | X podél postele, **hlava −X** (v pokoji u jižního rohu, s = 1,85), nohy +X (truhla) |
| Konstrukce | sloupky 9 × 9 se zkosenými hranami a hlavicí; čelo v hlavě 95 cm (rám, vložená deska, římsa), čelo v nohách 62 cm; bočnice 16 cm, lišty, 9 laťek; slamník 20 cm a polštář v lněném potahu, houně přes bočnice |
| Sloty | `Wood`, `Wool`, `Canvas` (potah, `MI_RuinCanvas`) |
| Funkční | ložná plocha 55 cm nad podlahou, bočnice nahoře 46 cm |
| Zdroj | `mesh_props.bed_large(seed, head_h=95)`; nižší čelo = parametr `head_h`; sloupky a hlavice s léty svisle (`grain="long"`, verze 2), ostatní díly zatím původní UV (úkol T-0024) |
| Náhled | `05_constructions/Guesthouse_postel_nahled.png` |

### Kovaná truhla na cennosti `SM_RuinChestLocked_A` (graybox `GH_CHEST`)

| | |
|---|---|
| Data | `shape: chest_locked`; `finish: oil` |
| Rozměr | 94,2 × 54,2 × 50,7 cm |
| Osy | **zámek a závěra −Y**, pásové závěsy +Y, držadla s kruhy ±X; delší strana X |
| Konstrukce | prkna na soklu, klenuté víko, černé kování bez rzi: rohovníky, 2 svislé pásy přes korpus a víko, vodorovný pás, nýty, zámková deska s klíčovou dírkou |
| Sloty | `Wood`, `EndGrain` (čela víka), `IronClean` |
| Zdroj | `mesh_props.chest_locked` |
| Náhled | `05_constructions/Guesthouse_truhla_nahled.png` |

### Stojan na brnění `SM_RuinArmorStand_A` (graybox `GH_ARMOR`)

| | |
|---|---|
| Data | `shape: armor_stand`; `finish: oil` |
| Rozměr | 60,1 × 60,3 × 175,0 cm |
| Osy | **čelo −Y** (zády ke zdi), kolík na rukavice +X |
| Konstrukce | varianta A (Jirka 22. 11. 2026): kříž noh 60 × 60 z přeplátovaných trámků se vzpěrami a patkou, sloupek 9 × 9, klenuté ramenní jařmo 46 cm se dvěma vzpěrami (unese plátovou zbroj), pásová příčka 34 cm, krček a ručně točená hlavice; ruční hrubé opracování; zatím prázdný |
| Body pro brnění | `mesh_props.ARMOR_STAND_POINTS` v cm od podlahy, osa sloupku x = y = 0: hlava 167, ramena 150, pás 105, kolík (10; 0; 126). V lokálních osách meshe (pivot ve středu) je od výšek odečíst 87,3 cm. Brnění = samostatný mesh posazený na tyto body. |
| Sloty | `Wood`, `EndGrain`; léta podél délky všech dílů (`grain="long"`) |
| Zdroj | `mesh_props.armor_stand` |
| Náhled | `05_constructions/Guesthouse_stojan_brneni_nahled.png` |

### Dál ve fázi Guesthouse (zatím bez meshe)

Pracovní stůl `SM_RuinDesk` (1,25 × 0,75 × 0,78), regál `SM_RuinShelfTall` (1,56 × 0,4 × 2,0), hromádka dřeva `SM_RuinWoodpileSmall` (0,8 × 0,4 × 0,6), stojan na zbraně (1,0 × 0,4 × 1,6; jméno ❓); ♻ stolička `SM_RuinStool` (škála 1,035), ♻ poklop `SM_RuinOvenDoor`.

## Stav

| Mesh | Import do UE | Vzhled ověřen |
|---|---|---|
| `SM_RuinCanvasTent_A` | ano (22. 11. 2026) | ne |
| `SM_RuinCampBed_A`, `SM_RuinCampBedFolded_A`, `SM_RuinChestSmall_A`, `SM_RuinBundle_A`, `MI_RuinSackcloth` | ano (22. 11. 2026) | ne |
| `SM_RuinChestLocked_A` | ano (22. 11. 2026) | ne |
| `SM_RuinBedLarge_A` | ano; verze 2 (léta sloupků) čeká na import | ne |
| `SM_RuinArmorStand_A` | ano; verze 3 (léta podél délky dílů) čeká na import | jařmo opravené (verze 2, screenshot 22. 11. 2026); léta sloupku napříč (verze 2) opravena ve verzi 3 |
