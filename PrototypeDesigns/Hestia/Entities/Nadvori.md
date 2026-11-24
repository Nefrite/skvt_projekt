---
# orchestrace
type: entity
updated: 2026-11-19
aliases: []
# hra
kind: place
parent: "[[Lapikus]]"
located_in: []
derived_from:
alternative_to: []
pattern:
status: built
# depth_<domain> / target_<domain>: očekávané domény podle kind (01, kap. 8), jiné jen když se řeší
# depth_* = realizace (Unreal, data, StateTree); hloubka návrhu se počítá z dokumentů (01, kap. 5)
# target_mode_<domain>: design | build, jen při odchylce od výchozího režimu domény
ue_path:
assets: []
scale: feature
---
# Nadvori

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| environment | – | – | – | build | bez cíle |
| paths | – | – | – | build | bez cíle |
| narrative | – | – | – | design | bez cíle |

Zralost podstromu (jednotky s vlastním cílem včetně této entity, 04 kap. 3):

| Doména | Zralost | Nejslabší článek |
|---|---|---|
| structures | 100 % (1 z 1) | 4 – [[Nadvori_Stan]] |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

_Zatím žádné dokumenty._

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[03_ruin]] | `nadvori_spec.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/tools/ruin/nadvori_spec.py` | spec | 03_ruin | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->
<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0011 (G2, [[Nadvori]]): očekávaná doména environment (kind place) bez target_environment ani u potomků; očekávaná doména narrative (kind place) bez target_narrative ani u potomků; očekávaná doména paths (kind place) bez target_paths ani u potomků
- Fronta F-0012 (G4, [[Nadvori]]): status built bez platného dokumentu state
- Fronta F-0050 (G11, [[Nadvori]]): změna /PrototypeDesigns/Lapikus/tools/ruin/nadvori_spec.py bez řádku v changes.md a novějšího updated

<!-- hestia:generated:end -->

## Historie a rozhodnutí
