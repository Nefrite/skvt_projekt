---
# orchestrace
type: entity
updated: 2026-11-23
aliases: []
# hra
kind: structure
parent: "[[Vez]]"
located_in: []
derived_from:
alternative_to: []
pattern:
status: built
# depth_<domain> / target_<domain>: očekávané domény podle kind (01, kap. 8), jiné jen když se řeší
# depth_* = realizace (Unreal, data, StateTree); hloubka návrhu se počítá z dokumentů (01, kap. 5)
# target_mode_<domain>: design | build, jen při odchylce od výchozího režimu domény
ue_path:
assets: []
depth_structures: 4
target_structures: 4
target_gameplay: 0
---
# Vez_Pristresek

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 3 | 4 | 4 | build | ✔ |
| gameplay | – | – | 0 | design | ✔ |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[navrh_vez_pristresek]] – design, depth 3, valid, in_progress
- [[stav_vez_pristresek]] – state, depth 3, valid

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[05_constructions]] | `Vez_Pristresek.py` | [[navrh_vez_pristresek]], [[stav_vez_pristresek]] |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez_Pristresek.py` | entry | 05_constructions | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-23 · `Maintenance/reports/ue_Vez_Pristresek.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 16 vlastních
- Třídy: StaticMesh 13, ISM 3 (50 instancí), Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 0; výchozí materiály: 0
- Fáze: base 16
- Rozsah: 779 × 739 × 451 cm
- Kořen daleko od geometrie (`pivot_far`, víc než 500 cm): 3 actorů; informace pro modelování v instanci, ne nález
- Pro srovnání `depth_*`: structures 4; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)
- Pozor: `state` stav_vez_pristresek (2026-11-22) je starší než čtení z UE (2026-11-23); ověř § *V levelu*; report potvrzuje jen „v levelu je“, vzhled a funkci § *Vizuálně ověřeno*

<!-- hestia:generated:end -->

## Assety
<!-- hestia:generated:start -->

Souhrn: requested 0, in_progress 4, generated 0, imported 10, verified 0 · graybox 0 · outdated v UE 0 (signál vedle `depth_*`, hloubka se z něj nepočítá)

| Asset | Stav | Náhrada v levelu |
|---|---|---|
| [[MI_RuinWood]] | in_progress | none |
| [[SM_RuinCanvasVezGable_A]] | in_progress | none |
| [[SM_RuinCanvasVez_A]] | in_progress | none |
| [[SM_RuinPost_A]] | in_progress | none |
| [[MI_RuinBark]] | imported | none |
| [[MI_RuinCanvas]] | imported | none |
| [[MI_RuinRope]] | imported | none |
| [[SM_RuinForkHead_A]] | imported | none |
| [[SM_RuinLashing_A]] | imported | none |
| [[SM_RuinLogBark_A]] | imported | none |
| [[SM_RuinPlank_A]] | imported | none |
| [[SM_RuinPoleBark_A]] | imported | none |
| [[SM_RuinRope_A]] | imported | none |
| [[SM_RuinTimber_A]] | imported | none |

<!-- hestia:generated:end -->
## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

_Žádné otevřené otázky z dokumentů, fronty ani scratch._

<!-- hestia:generated:end -->

## Historie a rozhodnutí
