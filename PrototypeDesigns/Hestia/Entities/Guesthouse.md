---
# orchestrace
type: entity
updated: 2026-11-19
aliases: [Ostroh_Krov, Ostroh_Dostavba, Ostroh_Podlaha]
# hra
kind: structure
parent: "[[Lapikus]]"
located_in: ["[[Ostroh]]"]
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
# Guesthouse

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | – | 4 | – | build | bez cíle |
| gameplay | – | – | – | design | bez cíle |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

_Zatím žádné dokumenty._

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[05_constructions]] | `Ostroh_Dostavba.py`, `Ostroh_Krov.py`, `Ostroh_Podlaha.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Dostavba.py` | entry | 05_constructions | alias |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Krov.py` | entry | 05_constructions | alias |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Podlaha.py` | entry | 05_constructions | alias |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-21 · `Maintenance/reports/ue_Guesthouse.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 13 vlastních
- Třídy: StaticMesh 1, Blueprint 0, BSP 0, ostatní 12
- Zástupné meshe (`/Engine/BasicShapes/`): 3; výchozí materiály: 0
- Fáze: –
- Rozsah: 4727 × 2019 × 3716 cm
- Pro srovnání `depth_*`: structures 4; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0007 (G2, [[Guesthouse]]): očekávaná doména gameplay (kind structure) bez target_gameplay; očekávaná doména structures (kind structure) bez target_structures

<!-- hestia:generated:end -->

## Historie a rozhodnutí
