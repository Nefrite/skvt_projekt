---
# orchestrace
type: reference
validity: valid
updated: 2026-11-19
aliases: []
---
# Entity × domain matrix (skript)

Zkušební pohled 2 pro rozhodnutí Q1 (zadání 04 kap. 2.1 a 5.1), varianta skript: tabulku přepisuje `hubs` při každém běhu (`python _core/scripts/hestia.py hubs --apply`). Buňka podle režimu cíle (zadání 0.13): režim `build` `realizace/cíl` (`depth_*`), u vyšší hloubky návrhu navíc „(návrh N)“; režim `design` „návrh N/cíl“ (hloubka návrhu z platných dokumentů `design` a `spec`); ⚠ = mezera; „bez cíle“ = doména očekávaná podle `kind` bez cíle; prázdné = neočekávaná doména bez cíle. Domény a očekávané domény bere z taxonomie instance (včetně `taxonomy_local`). Varianty Bases a Dataview (`bases/entity_domain_matrix.base`, `dataview/dv_entity_domain_matrix.md`) ukazují jen realizaci, hloubku návrhu spočítat neumí.

## Pohled
<!-- hestia:generated:start -->

| Entita | kind | environment | structures | paths | npc | gameplay | narrative |
|---|---|---|---|---|---|---|---|
| [[Brana]] | structure |  | 1/4 ⚠ |  |  | bez cíle |  |
| [[Brana_Straz]] | structure |  | 3/4 ⚠ |  |  | návrh 0/4 ⚠ |  |
| [[Characters]] | system |  |  |  |  | bez cíle |  |
| [[Characters_Animace_Sezeni]] | system |  |  |  |  | bez cíle |  |
| [[Guesthouse]] | structure |  | 4/4 |  |  | návrh 0/4 ⚠ |  |
| [[Hradby_a_Brana]] | group |  |  |  |  |  |  |
| [[Lapikus]] | location |  | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle |
| [[Lapikus_Region]] | place | bez cíle |  | bez cíle |  |  | návrh 0/1 ⚠ |
| [[Les_Lapikus]] | place | 1/4 ⚠ (návrh 4) |  | 0/4 ⚠ |  |  | bez cíle |
| [[Nadvori]] | place | bez cíle |  | bez cíle |  |  | bez cíle |
| [[Nadvori_Stan]] | object |  | 0/4 ⚠ (návrh 2) |  |  | bez cíle |  |
| [[Ostroh]] | place | bez cíle |  | bez cíle |  |  | bez cíle |
| [[Palac]] | structure |  | bez cíle |  |  | bez cíle |  |
| [[Palac_Kovarna]] | structure |  | bez cíle |  |  | bez cíle |  |
| [[Palac_Kovarna_Vybaveni]] | object |  | 4/4 |  |  | bez cíle |  |
| [[Palac_Obydli]] | structure |  | 3/4 ⚠ (návrh 4) |  |  | návrh 0/3 ⚠ |  |
| [[Palac_Treti]] | structure |  | bez cíle |  |  | bez cíle |  |
| [[Pristup_JV]] | place | bez cíle |  | bez cíle |  |  | bez cíle |
| [[Strazni_Vez]] | structure |  | 4/4 |  |  | návrh 0/4 ⚠ |  |
| [[Udoli_Reky]] | place | 2/4 ⚠ |  | 0/4 ⚠ |  |  | bez cíle |
| [[Vez]] | structure |  | bez cíle |  |  | bez cíle |  |
| [[Vez_Pristresek]] | structure |  | 4/4 |  |  | bez cíle |  |

<!-- hestia:generated:end -->
