---
# orchestrace
type: entity
updated: 2026-11-19
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
---
# Ostroh

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| environment | – | – | – | build | bez cíle |
| paths | – | – | – | build | bez cíle |
| narrative | – | – | – | design | bez cíle |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

_Zatím žádné dokumenty._

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[03_ruin]] | `Ostroh.py`, `ostroh_spec.py` | – |
| [[05_constructions]] | `Ostroh_Dostavba.py`, `Ostroh_Krov.py`, `Ostroh_Podlaha.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/tools/ruin/ostroh_spec.py` | spec | 03_ruin | name |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/casti/Ostroh.py` | entry | 03_ruin | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Dostavba.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Krov.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Podlaha.py` | entry | 05_constructions | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

_Žádné otevřené otázky z dokumentů, fronty ani scratch._

<!-- hestia:generated:end -->

## Historie a rozhodnutí
