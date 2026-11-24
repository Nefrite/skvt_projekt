---
# orchestrace
type: entity
updated: 2026-11-24
aliases: []
# hra
kind: group
parent: "[[Lapikus]]"
located_in: []
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
---
# Hradby_a_Brana

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | – | 4 | 4 | build | ✔ |

Zralost podstromu (jednotky s vlastním cílem včetně této entity, 04 kap. 3):

| Doména | Zralost | Nejslabší článek |
|---|---|---|
| structures | 75 % (3 z 4) | 3 – [[Brana_Straz]] |
| gameplay | 0 % (0 z 2) | 0 – [[Brana_Straz]] |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

_Zatím žádné dokumenty._

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[01_terrain]] | `gen_moat.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/tools/terrain/gen_moat.py` | entry | 01_terrain | header |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-23 · `Maintenance/reports/ue_Hradby_a_Brana.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 53 vlastních, 18 za potomky (Brana, Brana_Straz, Strazni_Vez)
- Třídy: StaticMesh 0, ISM 53 (7071 instancí), Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 0 (vynecháno podle `placeholder_ignore`: 16); výchozí materiály: 0
- Fáze: –
- Rozsah: 7264 × 3297 × 791 cm
- Kořen daleko od geometrie (`pivot_far`, víc než 500 cm): 53 actorů; informace pro modelování v instanci, ne nález
- Pro srovnání `depth_*`: structures 4; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

_Žádné otevřené otázky z dokumentů, fronty ani scratch._

<!-- hestia:generated:end -->

## Historie a rozhodnutí
