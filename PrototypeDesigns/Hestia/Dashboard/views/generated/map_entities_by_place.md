---
# orchestrace
type: reference
validity: valid
updated: 2026-11-19
aliases: []
---
# Map: entities by place (skript)

Zkušební pohled 3 pro rozhodnutí Q1 (zadání 04 kap. 2.1 a 5.1), varianta skript: tabulku přepisuje `hubs` při každém běhu. Umístění = `located_in`; prázdné se dědí od `parent` do libovolné hloubky (zadání 03 kap. 1), sloupec *Umístění* říká, od koho. Prázdné *Místo* = entita bez umístění (nahoře: v hierarchii stojí nejvýš, nebo chybí umístění). Varianty Bases a Dataview: `bases/map_entities_by_place.base`, `dataview/dv_map_entities_by_place.md`.

## Pohled
<!-- hestia:generated:start -->

| Místo | Entita | kind | Umístění |
|---|---|---|---|
|  | [[Characters]] | system |  |
|  | [[Characters_Animace_Sezeni]] | system |  |
|  | [[Lapikus_Region]] | place |  |
|  | [[Les_Lapikus]] | place |  |
|  | [[Ostroh]] | place |  |
|  | [[Pristup_JV]] | place |  |
|  | [[Udoli_Reky]] | place |  |
| [[Lapikus]] | [[Cinematics_Lapikus]] | sequence | vlastní |
| [[Ostroh]] | [[Brana]] | structure | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Brana_Straz]] | structure | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Guesthouse]] | structure | vlastní |
| [[Ostroh]] | [[Hradby_a_Brana]] | group | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Lapikus]] | location | vlastní |
| [[Ostroh]] | [[Nadvori]] | place | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Nadvori_Stan]] | object | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Palac]] | structure | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Palac_Kovarna]] | structure | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Palac_Kovarna_Vybaveni]] | object | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Palac_Obydli]] | structure | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Palac_Treti]] | structure | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Strazni_Vez]] | structure | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Vez]] | structure | zděděno od [[Lapikus]] |
| [[Ostroh]] | [[Vez_Pristresek]] | structure | zděděno od [[Lapikus]] |

<!-- hestia:generated:end -->
