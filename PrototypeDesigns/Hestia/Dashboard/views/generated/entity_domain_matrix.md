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
| [[Brana]] | structure |  | 4/4 |  |  | bez cíle |  |
| [[Brana_Straz]] | structure |  | 3/4 ⚠ |  |  | návrh 0/4 ⚠ |  |
| [[Characters]] | system |  |  |  |  | bez cíle |  |
| [[Characters_Animace_Sezeni]] | system |  |  |  |  | bez cíle |  |
| [[Guesthouse]] | structure |  | 4/4 |  |  | návrh 0/4 ⚠ |  |
| [[Hradby_a_Brana]] | group |  | podstrom 3/4 ⚠ (min 3); vlastní 4/4 |  |  | podstrom 0/2 ⚠ (min 0) |  |
| [[Lapikus]] | location |  | podstrom 10/12 ⚠ (min 3) | bez cíle | bez cíle | podstrom 0/4 ⚠ (min 0) | bez cíle |
| [[Lapikus_Region]] | place | podstrom 1/3 ⚠ (min 1); vlastní 4/4 | podstrom 10/12 ⚠ (min 3) | podstrom 0/2 ⚠ (min 0) |  | podstrom 0/4 ⚠ (min 0) | podstrom 0/1 ⚠ (min 0); vlastní návrh 0/1 ⚠ |
| [[Les_Lapikus]] | place | 1/4 ⚠ (návrh 4) |  | 0/4 ⚠ |  |  | bez cíle |
| [[Nadvori]] | place | bez cíle | podstrom 1/1 (min 4) | bez cíle |  |  | bez cíle |
| [[Nadvori_Stan]] | object |  | 4/4 |  |  | bez cíle |  |
| [[Ostroh]] | place | bez cíle |  | bez cíle |  |  | bez cíle |
| [[Palac]] | structure |  | podstrom 3/4 ⚠ (min 3); vlastní 4/4 |  |  | podstrom 0/1 ⚠ (min 0) |  |
| [[Palac_Kovarna]] | structure |  | podstrom 2/2 (min 4); vlastní 4/4 |  |  | bez cíle |  |
| [[Palac_Kovarna_Vybaveni]] | object |  | 4/4 |  |  | bez cíle |  |
| [[Palac_Obydli]] | structure |  | 3/4 ⚠ (návrh 4) |  |  | návrh 0/3 ⚠ |  |
| [[Palac_Treti]] | structure |  | bez cíle |  |  | bez cíle |  |
| [[Pristup_JV]] | place | bez cíle |  | bez cíle |  |  | bez cíle |
| [[Strazni_Vez]] | structure |  | 4/4 |  |  | návrh 0/4 ⚠ |  |
| [[Udoli_Reky]] | place | 2/4 ⚠ |  | 0/4 ⚠ |  |  | bez cíle |
| [[Vez]] | structure |  | podstrom 2/2 (min 4); vlastní 4/4 |  |  | bez cíle |  |
| [[Vez_Pristresek]] | structure |  | 4/4 |  |  | bez cíle |  |

<!-- hestia:generated:end -->
