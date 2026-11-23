---
# orchestrace
type: design
validity: valid
derived_from:
alternative_to: []
updated: 2026-11-23
aliases: []
# hra
domain: structures
category: []
entity: "[[Guesthouse]]"
depth: 4
build_step: 06_furnishing
assets: []
---
# Guesthouse – vybavení pokoje hosta

## Zadání / záměr
Zadání Jirky 21. 11. 2026: vybavit obytnou část u ostrohu (Guesthouse) pro hosta. Host je inkvizitor řádu, klíč od svých věcí nosí na krku ([[Guest_on_hunt]]). Pokoj má být pro něj pohodlný.

Seznam vybavení ze zadání: pracovní stůl pro jednoho se stoličkou pod oknem, postel u jižní části zdi se vchodem, stojan na brnění a stojan na zbraně (dva odlišné objekty), truhla s železným kováním a zámkem, výhřev po vzoru obydlí bez plotny (menší a úspornější). Při ladění v levelu přibyly regál na další věci a hromádka dřeva u kamen.

## Výchozí stav
Obytná část u ostrohu: krov [[05_constructions]] `Ostroh_Krov`, kamenná dostavba `Ostroh_Dostavba` (dveře 1,6 m, okno 1,25 m s parapetem 1,4 m) a prkenná podlaha `Ostroh_Podlaha`. Půdorys tvoří rovná východní zeď `ZBudova_V` (vnitřní líc 12,36 m), krátká severní zeď `ZBudova_S` (2,85 m) a oblouk hradby `Hradba_Z_S` na západě a jihu; místnost je hluboká až 7,5 m. Vrch podlahy je 14,5 cm nad terénem, spodek krovu 2,9–4 m nad podlahou.

Rám vybavení = rám podlahy: `s` podél vnitřního líce `ZBudova_V` od jižního rohu k severu (0–12,36 m), `n` do místnosti k západu. Dveře s = 6,16–7,76; okno s = 9,74–10,99; sloupy krovu s = 5,92 a 8,0, n = 1,16.

## Návrh
Rozmístění je ověřené s postavou v levelu (Manny 180 cm) a polohy z větší části určil Jirka v levelu (21. 11. 2026). Postel, truhla, stojan na brnění a stolička jsou meshe z [[Katalog_props]] (úprava dřeva `oil`), ostatní kusy zatím graybox (kvádry s materiálem `MI_PrototypeGrid_Gray`); stav meshí vede [[CHECKLIST_assets_navrhy]] kap. 6.8. Půdorys: `Attachments/navrh_guesthouse_vybaveni_pudorys.png`.

| Kus | Rozměr (m) | Poloha s; n (m) | Rozhodnutí |
|---|---|---|---|
| postel `SM_RuinBedLarge` | 2,50 × 1,09 × 0,95 (čelo) | 1,85–4,35; 0,39–1,48 | pohodlná, větší než `SM_RuinBed` (Jirka); hlava k jihu |
| pracovní stůl | 1,25 × 0,75 × 0,78 | 9,76–11,01; 0,07–0,82 | pod oknem; nový mesh, ne `SM_RuinTable`; výška 78 cm (Jirka) |
| stolička `SM_RuinStool` | 0,36 × 0,35 × 0,47 | 10,21–10,57; 1,10–1,44 | úměrně ke stolu, postavě po kolena (Jirka) |
| truhla `SM_RuinChestLocked` | 0,94 × 0,54 × 0,51 | 4,46–5,00; 0,45–1,40 | v nohách postele, zámek k severu; nový mesh truhly se zámkem (Jirka) |
| stojan na brnění `SM_RuinArmorStand` | 0,6 × 0,6 × 1,75 | 9,70–10,55; 5,25–6,10 | u hradby na severozápadě, zády k hradbě, zatím prázdný (Jirka) |
| stojan na zbraně | 1,0 × 0,4 × 1,6 | 6,68–7,73; 6,47–7,04 | u hradby naproti dveřím, zatím prázdný (Jirka) |
| regál | 1,56 × 0,4 × 2,0 | 11,90–12,30; 0,94–2,50 | u severní zdi na místě původně navrženého stojanu na zbraně (Jirka) |
| kamna s dymníkem | asi 1,0 × 0,9 × 1,2 (těleso) | střed 3,12; 4,10, zády k hradbě | pevná stavba **05, staví stavitel** (Jirka); v 06 jen dočasný kvádr `Pec_Zastupce` |
| hromádka dřeva | 0,8 × 0,4 × 0,6 | 3,37–4,20; 4,48–5,34 | vedle kamen podél hradby, nový mesh (Jirka) |

- Průchod od dveří (s = 5,8–8,1; n = 0–2 m) zůstává volný.
- Kamna: menší než pec v obydlí ([[navrh_palac_obydli_pec]]), bez nístěje a plotny, s dymníkem nad ústím a komínem skrz krytinu. Pod kamny je kamenná dlažba (Jirka). Zadání pro stavitele: [[predani_guesthouse_kamna_stavitel]].

## Souhrn specifikace
- Polohy a rozměry: `tools/ruin/ostroh_spec.py` → `GH_BED`, `GH_DESK`, `GH_STOOL`, `GH_CHEST`, `GH_ARMOR`, `GH_WEAPONS`, `GH_SHELF`, `GH_WOOD`, `GH_OVEN`, `GH_REF`, funkce `guesthouse_vybaveni()`.
- Skupina `Guesthouse_Vybaveni` v `06_furnishing/furnishing.json` (generátor `tools/furnishing/gen_furnishing.py` → `guesthouse()`; výšky od vrchu prken podlahy, po změně terénu nebo podlahy přegenerovat).
- Meshe: `GH_MESH` (id kusu → `shape`, `finish`); graybox: kusy s `cat = "graybox"` = Cube s materiálem `zrlib/config.py` → `MAT_GRAYBOX`.

## Vazby a závislosti
- Stavby u ostrohu (05): `Ostroh_Krov`, `Ostroh_Dostavba`, `Ostroh_Podlaha`; vybavení je nemění.
- Kamna (05) a komín musí projít krytinou krovu mezi trámy vějíře, viz předání stavitele.
- Meshe: [[CHECKLIST_assets_navrhy]] kap. 6.8.

## Ověření
- `tools/checks/run_checks.py --only ostroh`: průniky vybavení se zříceninou, dostavbou, krovem a mezi sebou, kusy na podlaze, volný průchod u dveří (21. 11. 2026 OK).
- V UE: graybox postele, stolu a stoličky postavený a srovnaný Jirkou (21. 11. 2026); ostatní kusy rozmístěné v levelu Jirkou, poslední build po opravě regálu zatím nespuštěný.

## Otevřené otázky
- [ ] Výstroj na stojanu na brnění a zbraně na stojanu na zbraně (které, sdílet se zbrojí posádky?) — Furnisher, 2026-11-21
