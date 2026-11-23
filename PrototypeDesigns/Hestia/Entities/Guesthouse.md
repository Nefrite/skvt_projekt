---
# orchestrace
type: entity
updated: 2026-11-23
aliases: [Ostroh_Krov, Ostroh_Dostavba, Ostroh_Podlaha]
# hra
kind: structure
parent: "[[Lapikus]]"
located_in: ["[[Ostroh]]"]
derived_from:
alternative_to: []
pattern:
status: in_progress
# depth_<domain> / target_<domain>: očekávané domény podle kind (01, kap. 8), jiné jen když se řeší
# depth_* = realizace (Unreal, data, StateTree); hloubka návrhu se počítá z dokumentů (01, kap. 5)
# target_mode_<domain>: design | build, jen při odchylce od výchozího režimu domény
ue_path:
assets: []
depth_structures: 4
target_structures: 4
target_gameplay: 4
---
# Guesthouse

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 4 | 4 | 4 | build | ✔ |
| gameplay | – | – | 4 | design | −4 |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[navrh_guesthouse_vybaveni]] – design, depth 4, valid
- [[stav_guesthouse]] – state, depth 2, valid
- [[rozhodnuti_guesthouse_meshe_dlazba]] – decision, valid

**Aktivní předání**
- [[predani_guesthouse_kamna_stavitel]]

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[05_constructions]] | `Guesthouse_postel_nahled.png`, `Guesthouse_stojan_brneni_nahled.png`, `Guesthouse_truhla_nahled.png`, `Ostroh_Dostavba.py`, `Ostroh_Krov.py`, `Ostroh_Podlaha.py` | – |
| [[06_furnishing]] | `Guesthouse.py`, `Guesthouse_Capture.py` | [[navrh_guesthouse_vybaveni]], [[stav_guesthouse]] |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Dostavba.py` | entry | 05_constructions | alias |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Krov.py` | entry | 05_constructions | alias |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Podlaha.py` | entry | 05_constructions | alias |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Guesthouse.py` | entry | 06_furnishing | name |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Guesthouse_Capture.py` | entry | 06_furnishing | name |
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_postel_nahled.png` | data | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_stojan_brneni_nahled.png` | data | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_truhla_nahled.png` | data | 05_constructions | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-23 · `Maintenance/reports/ue_Guesthouse.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 13 vlastních
- Třídy: StaticMesh 1, ISM 12 (1860 instancí), Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 0 (vynecháno podle `placeholder_ignore`: 3); výchozí materiály: 0
- Fáze: –
- Rozsah: 1273 × 1550 × 579 cm
- Kořen daleko od geometrie (`pivot_far`, víc než 500 cm): 12 actorů; informace pro modelování v instanci, ne nález
- Pro srovnání `depth_*`: structures 4; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)
- Pozor: `state` stav_guesthouse (2026-11-22) je starší než čtení z UE (2026-11-23); ověř § *V levelu*; report potvrzuje jen „v levelu je“, vzhled a funkci § *Vizuálně ověřeno*

<!-- hestia:generated:end -->

## Assety
<!-- hestia:generated:start -->

Souhrn: requested 4, in_progress 4, generated 0, imported 13, verified 0 · graybox 4 · outdated v UE — (signál vedle `depth_*`, hloubka se z něj nepočítá)

| Asset | Stav | Náhrada v levelu |
|---|---|---|
| [[SM_RuinDesk_A]] | requested | graybox |
| [[SM_RuinShelfTall_A]] | requested | graybox |
| [[SM_RuinWeaponRack_A]] | requested | graybox |
| [[SM_RuinWoodpileSmall_A]] | requested | graybox |
| [[MI_RuinWood]] | in_progress | none |
| [[SM_RuinOvenDome_A]] | in_progress | none |
| [[SM_RuinOvenDoor_A]] | in_progress | none |
| [[SM_RuinPost_A]] | in_progress | none |
| [[MI_RuinCanvas]] | imported | none |
| [[MI_RuinDaub]] | imported | none |
| [[MI_RuinIronClean]] | imported | none |
| [[MI_RuinWood_EndGrain]] | imported | none |
| [[MI_RuinWool]] | imported | none |
| [[SM_RuinArmorStand_A]] | imported | none |
| [[SM_RuinBedLarge_A]] | imported | none |
| [[SM_RuinChestLocked_A]] | imported | none |
| [[SM_RuinChimney_A]] | imported | none |
| [[SM_RuinPlank_A]] | imported | none |
| [[SM_RuinSmokeHood_A]] | imported | none |
| [[SM_RuinStool_A]] | imported | none |
| [[SM_RuinTimber_A]] | imported | none |

<!-- hestia:generated:end -->
## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- [[navrh_guesthouse_vybaveni]]: Výstroj na stojanu na brnění a zbraně na stojanu na zbraně (které, sdílet se zbrojí posádky?) — Furnisher, 2026-11-21
- Fronta F-0031 (G3, [[Guesthouse]]): bez dokumentu v doméně gameplay (target_gameplay 4)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
