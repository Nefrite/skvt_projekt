---
# orchestrace
type: entity
updated: 2026-11-19
aliases: []
# hra
kind: structure
parent: "[[Hradby_a_Brana]]"
located_in: []
derived_from: "[[Strazni_Vez]]"
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
# Brana_Straz

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 3 | 3 | – | build | bez cíle |
| gameplay | – | – | – | design | bez cíle |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[navrh_brana_straz]] – design, depth 3, valid, in_progress
- [[stav_brana_straz]] – state, depth 3, valid

**Aktivní předání**
- [[predani_brana_straz_striska_stavitel]]

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[05_constructions]] | `Brana_Straz.py`, `Brana_Straz_Kamen.py`, `Brana_Straz_Kryty.py`, `Brana_Straz_Podesta.py` | [[navrh_brana_straz]], [[stav_brana_straz]] |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kamen.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kryty.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Podesta.py` | entry | 05_constructions | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-21 · `Maintenance/reports/ue_Brana_Straz.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 4 vlastních
- Třídy: StaticMesh 0, Blueprint 0, BSP 0, ostatní 4
- Zástupné meshe (`/Engine/BasicShapes/`): 0; výchozí materiály: 0
- Fáze: base 3, final 1
- Rozsah: 2915 × 3488 × 3893 cm
- Pro srovnání `depth_*`: structures 3; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0004 (G2, [[Brana_Straz]]): očekávaná doména gameplay (kind structure) bez target_gameplay; očekávaná doména structures (kind structure) bez target_structures

<!-- hestia:generated:end -->

## Historie a rozhodnutí
