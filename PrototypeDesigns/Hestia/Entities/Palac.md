---
# orchestrace
type: entity
updated: 2026-11-19
aliases: []
# hra
kind: structure
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
---
# Palac

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | – | 4 | – | build | bez cíle |
| gameplay | – | – | – | design | bez cíle |

Agregace z potomků (04 kap. 3):

_Potomci nemají cíle._

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

_Zatím žádné dokumenty._

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[03_ruin]] | `Palac.py`, `palac_spec.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/tools/ruin/palac_spec.py` | spec | 03_ruin | name |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/casti/Palac.py` | entry | 03_ruin | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-21 · `Maintenance/reports/ue_Palac.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 17 vlastních, 70 za potomky (Palac_Kovarna, Palac_Kovarna_Vybaveni, Palac_Obydli, Palac_Treti)
- Třídy: StaticMesh 0, Blueprint 0, BSP 0, ostatní 17
- Zástupné meshe (`/Engine/BasicShapes/`): 5; výchozí materiály: 0
- Fáze: –
- Rozsah: 3434 × 1873 × 3926 cm
- Pro srovnání `depth_*`: structures 4; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0015 (G2, [[Palac]]): očekávaná doména gameplay (kind structure) bez target_gameplay ani u potomků; očekávaná doména structures (kind structure) bez target_structures ani u potomků

<!-- hestia:generated:end -->

## Historie a rozhodnutí
