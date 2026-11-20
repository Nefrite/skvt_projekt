---
# orchestrace
type: entity
updated: 2026-11-19
aliases: []
# hra
kind: system
parent:
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
depth_npc: 3
depth_gameplay: 5
---
# Characters

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| gameplay | – | 5 | – | design | bez cíle |

Agregace z potomků (04 kap. 3):

_Potomci nemají cíle._

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**gameplay**
- [[README_animations]] – state, depth 5, valid

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[01_sitting]] | `seat_place_selected.py`, `seat_report.py`, `seat_test_station.py` | – |
| [[NPC]] | `npc_make_patrol_route.py`, `npc_nav_bounds.py`, `npc_report.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Characters/01_sitting/seat_place_selected.py` | entry | 01_sitting | folder |
| `/PrototypeDesigns/Characters/01_sitting/seat_report.py` | entry | 01_sitting | folder |
| `/PrototypeDesigns/Characters/01_sitting/seat_test_station.py` | entry | 01_sitting | folder |
| `/PrototypeDesigns/Characters/NPC/npc_make_patrol_route.py` | entry | NPC | folder |
| `/PrototypeDesigns/Characters/NPC/npc_nav_bounds.py` | entry | NPC | folder |
| `/PrototypeDesigns/Characters/NPC/npc_report.py` | entry | NPC | folder |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->
<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0005 (G2, [[Characters]]): očekávaná doména gameplay (kind system) bez target_gameplay ani u potomků
- Fronta T-0009 (–, [[01_sitting]]): záměr do `Docs/gameplay`, u [[NPC]] do `Docs/npc` (M30, M31)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
