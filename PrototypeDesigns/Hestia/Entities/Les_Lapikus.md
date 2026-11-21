---
# orchestrace
type: entity
updated: 2026-11-21
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
depth_environment: 1
---
# Les_Lapikus

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| environment | 4 | 1 | – | build | bez cíle |
| paths | – | – | – | build | bez cíle |
| narrative | – | – | – | design | bez cíle |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**environment**
- [[README_forest]] – design, depth 4, valid

**Know-how**
- [[README_assets_stromy]]

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[04_forest]] | `T_ForestZones_505.png`, `Zricenina_les_plan.png`, `Zricenina_les_zony.csv`, `Zricenina_olse.csv`, `Zricenina_olse_plan.png`, `import_zone_splines.py`, `nacrt_zony.png`, `place_alders.py` | [[README_forest]] |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/04_forest/import_zone_splines.py` | entry | 04_forest | folder |
| `/PrototypeDesigns/Lapikus/04_forest/place_alders.py` | entry | 04_forest | folder |
| `/PrototypeDesigns/Lapikus/04_forest/T_ForestZones_505.png` | data | 04_forest | folder |
| `/PrototypeDesigns/Lapikus/04_forest/Zricenina_les_plan.png` | data | 04_forest | folder |
| `/PrototypeDesigns/Lapikus/04_forest/Zricenina_les_zony.csv` | data | 04_forest | folder |
| `/PrototypeDesigns/Lapikus/04_forest/Zricenina_olse.csv` | data | 04_forest | folder |
| `/PrototypeDesigns/Lapikus/04_forest/Zricenina_olse_plan.png` | data | 04_forest | folder |
| `/PrototypeDesigns/Lapikus/04_forest/nacrt_zony.png` | data | 04_forest | folder |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-21 · `Maintenance/reports/ue_Les_Lapikus.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 0 vlastních
- Třídy: StaticMesh 0, Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 0; výchozí materiály: 0
- Fáze: –
- Pro srovnání `depth_*`: environment 1; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
- [x] Unreal (report `ue_Les_Lapikus.json`, 2026-11-21): v levelu není žádný actor s tagem `Zricenina_Alder` ve složce `Forest/Alders` (`04_forest/place_alders.py`). Olše nejsou rozmístěné, nebo jsou jinde (jiná složka, PCG)? Podle toho upravit pravidlo v `ue_map.yaml`; `depth_environment: 1` beze změny — agent pilotu, 2026-11-21 → GameDesigner 2026-11-21: les v levelu ještě neexistuje, je jen návrh game designu; pravidlo v `ue_map.yaml` zůstává pro budoucí realizaci
<!-- hestia:generated:start -->

- Fronta F-0010 (G2, [[Les_Lapikus]]): očekávaná doména environment (kind place) bez target_environment; očekávaná doména narrative (kind place) bez target_narrative; očekávaná doména paths (kind place) bez target_paths
- Fronta T-0004 (–, [[README_forest]]): rozpad PCG a spouštění do [[04_forest]] (M14)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
