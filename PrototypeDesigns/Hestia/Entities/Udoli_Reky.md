---
# orchestrace
type: entity
updated: 2026-11-23
aliases: []
# hra
kind: place
parent: "[[Lapikus_Region]]"
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
scale: sector
depth_environment: 2
target_environment: 4
target_paths: 4
depth_paths: 0
target_narrative: 0
---
# Udoli_Reky

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| environment | – | 2 | 4 | build | −2 |
| paths | – | 0 | 4 | build | −4 |
| narrative | – | – | 0 | design | ✔ |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

_Zatím žádné dokumenty._

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[02_river]] | `T_RiverMask_505.png`, `T_RiverMask_preview.png`, `Zricenina_505_body_reky.csv`, `Zricenina_505_body_reky.png`, `import_river_spline.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/02_river/import_river_spline.py` | entry | 02_river | folder |
| `/PrototypeDesigns/Lapikus/02_river/T_RiverMask_505.png` | data | 02_river | folder |
| `/PrototypeDesigns/Lapikus/02_river/T_RiverMask_preview.png` | data | 02_river | folder |
| `/PrototypeDesigns/Lapikus/02_river/Zricenina_505_body_reky.csv` | data | 02_river | folder |
| `/PrototypeDesigns/Lapikus/02_river/Zricenina_505_body_reky.png` | data | 02_river | folder |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->
<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0035 (G3, [[Udoli_Reky]]): bez dokumentu v doméně environment (target_environment 4); bez dokumentu v doméně paths (target_paths 4)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
