---
# orchestrace
type: state
validity: valid
updated: 2026-11-21
aliases: []
# hra
domain: structures
entity: "[[Guesthouse]]"
depth: 2
build_step: 06_furnishing
assets: []
---
# Guesthouse – stav vybavení proti návrhu

Návrh: [[navrh_guesthouse_vybaveni]]. Stavby u ostrohu (krov, dostavba, podlaha) popisuje [[05_constructions]].

## Co je hotové
- Graybox všech kusů vybavení ve skupině `Guesthouse_Vybaveni` (9 kvádrů, materiál `MI_PrototypeGrid_Gray`): postel, stůl, stolička, truhla, stojan na brnění, stojan na zbraně, regál, hromádka dřeva a dočasný zástupce kamen `Pec_Zastupce`.
- Spouštěče `06_furnishing/vybaveni/Guesthouse.py` a `Guesthouse_Capture.py`, kontroly v `run_checks.py --only ostroh` (OK, 21. 11. 2026).
- Polohy z levelu (capture): postel, stůl, stolička, oba stojany; regál vrácený na spec s opravou (6 cm od kamenů `ZBudova_S`, se souhlasem Jirky).

## Souhrn specifikace
`tools/ruin/ostroh_spec.py` → `GH_*`, `guesthouse_vybaveni()`; data `06_furnishing/furnishing.json` → `Guesthouse_Vybaveni`.

## Co se liší od návrhu (a proč)
- Postel 2,5 × 1,09 m místo 2,0 × 0,87 m: má být pohodlná pro postavu 180 cm (Jirka).
- Stůl 1,25 × 0,75 × 0,78 m místo 1,0 × 0,6 × 0,76 m, stolička 47 cm místo 45 cm (Jirka v levelu).
- Stojany přesunuté z východní zdi k hradbě, na severní zdi místo stojanu na zbraně regál (Jirka v levelu).
- Kamna: v 06 jen zástupný kvádr; skutečná kamna s dymníkem postaví stavitel v 05.

## Ověřeno v UE (ano/ne, kdy, kým)
- Ano, částečně: graybox a polohy v levelu, Jirka 21. 11. 2026. Build po opravě regálu zatím neověřený.

## Co zbývá
- Kamna s dymníkem, komínem a kamennou dlažbou pod nimi (05): [[predani_guesthouse_kamna_stavitel]]; po postavení odebrat `Pec_Zastupce` z `guesthouse_vybaveni()` a z dat.
- Meshe místo grayboxu ([[CHECKLIST_assets_navrhy]] kap. 6.8): `SM_RuinBedLarge`, `SM_RuinDesk`, stojan na brnění, stojan na zbraně, `SM_RuinShelfTall`, `SM_RuinChestLocked`, `SM_RuinWoodpileSmall`; pak kusy přepnout z `cat = "graybox"` na tvary meshí (jiný mesh = nový build před capture).
- Výstroj a zbraně na stojany (zatím prázdné).

## Odkazy na návrh a předání
[[navrh_guesthouse_vybaveni]], [[predani_guesthouse_kamna_stavitel]], [[CHECKLIST_assets_navrhy]] kap. 6.8.
