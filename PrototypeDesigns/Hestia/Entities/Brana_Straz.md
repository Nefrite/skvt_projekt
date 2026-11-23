---
# orchestrace
type: entity
updated: 2026-11-23
aliases: []
# hra
kind: structure
parent: "[[Hradby_a_Brana]]"
located_in: []
derived_from: "[[Strazni_Vez]]"
alternative_to: []
pattern:
status: in_progress
# depth_<domain> / target_<domain>: očekávané domény podle kind (01, kap. 8), jiné jen když se řeší
# depth_* = realizace (Unreal, data, StateTree); hloubka návrhu se počítá z dokumentů (01, kap. 5)
# target_mode_<domain>: design | build, jen při odchylce od výchozího režimu domény
ue_path:
assets: []
depth_structures: 3
target_structures: 4
target_gameplay: 4
---
# Brana_Straz

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 3 | 3 | 4 | build | −1 |
| gameplay | – | – | 4 | design | −4 |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[navrh_brana_straz]] – design, depth 3, valid, in_progress
- [[stav_brana_straz]] – state, depth 3, valid

**Aktivní předání**
- [[predani_brana_straz_striska_stavitel]]

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[05_constructions]] | `Brana_Straz.py`, `Brana_Straz_Kamen.py`, `Brana_Straz_Kryty.py`, `Brana_Straz_Podesta.py` | [[navrh_brana_straz]], [[stav_brana_straz]] |
| [[06_furnishing]] | `Brana_Straz.py`, `Brana_Straz_Capture.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kamen.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kryty.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Podesta.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Brana_Straz.py` | entry | 06_furnishing | name |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Brana_Straz_Capture.py` | entry | 06_furnishing | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-23 · `Maintenance/reports/ue_Brana_Straz.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 4 vlastních
- Třídy: StaticMesh 0, ISM 4 (203 instancí), Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 0; výchozí materiály: 0
- Fáze: base 3, final 1
- Rozsah: 880 × 764 × 331 cm
- Kořen daleko od geometrie (`pivot_far`, víc než 500 cm): 4 actorů; informace pro modelování v instanci, ne nález
- Pro srovnání `depth_*`: structures 3; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Assety
<!-- hestia:generated:start -->

Souhrn: requested 4, in_progress 2, generated 0, imported 10, verified 0 · graybox 4 · outdated v UE — (signál vedle `depth_*`, hloubka se z něj nepočítá)

| Asset | Stav | Náhrada v levelu |
|---|---|---|
| [[SM_RuinArrowTools_A]] | requested | graybox |
| [[SM_RuinBow_A]] | requested | graybox |
| [[SM_RuinCrate_A]] | requested | graybox |
| [[SM_RuinQuiver_A]] | requested | graybox |
| [[MI_RuinWood]] | in_progress | none |
| [[SM_RuinPost_A]] | in_progress | none |
| [[MI_RuinBark]] | imported | none |
| [[SM_RuinBarkStrip_A]] | imported | none |
| [[SM_RuinLashing_A]] | imported | none |
| [[SM_RuinLog_A]] | imported | none |
| [[SM_RuinPlank_A]] | imported | none |
| [[SM_RuinPoleBark_A]] | imported | none |
| [[SM_RuinPole_A]] | imported | none |
| [[SM_RuinStake_A]] | imported | none |
| [[SM_RuinStool_A]] | imported | none |
| [[SM_RuinTimber_A]] | imported | none |

<!-- hestia:generated:end -->
## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0030 (G3, [[Brana_Straz]]): bez dokumentu v doméně gameplay (target_gameplay 4)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
