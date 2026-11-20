---
# orchestrace
type: entity
updated: 2026-11-19
aliases: []
# hra
kind: object
parent: "[[Palac_Kovarna]]"
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
depth_structures: 3
---
# Palac_Kovarna_Vybaveni

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 4 | 3 | – | build | bez cíle |
| gameplay | – | – | – | design | bez cíle |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[navrh_palac_kovarna]] – design, depth 4, valid, in_progress

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[05_constructions]] | – | [[navrh_palac_kovarna]] |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

_Žádné soubory._

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->
<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0017 (G2, [[Palac_Kovarna_Vybaveni]]): očekávaná doména gameplay (kind object) bez target_gameplay; očekávaná doména structures (kind object) bez target_structures
- Fronta T-0007 (–, [[navrh_palac_kovarna]]): kap. 0 duplicitní se [[stav_palac_kovarna]]: sjednotit (M22)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
