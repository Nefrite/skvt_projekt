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
# Vez

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
| [[05_constructions]] | `Vez.py`, `Vez_Patra.py`, `vez.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez_Patra.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/vez.py` | library | 05_constructions | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

_Žádné otevřené otázky z dokumentů, fronty ani scratch._

<!-- hestia:generated:end -->

## Historie a rozhodnutí
