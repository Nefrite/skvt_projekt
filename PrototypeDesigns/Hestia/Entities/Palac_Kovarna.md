---
# orchestrace
type: entity
updated: 2026-11-19
aliases: []
# hra
kind: structure
parent: "[[Palac]]"
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
depth_structures: 4
---
# Palac_Kovarna

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 4 | 4 | – | build | bez cíle |
| gameplay | – | – | – | design | bez cíle |

Agregace z potomků (04 kap. 3):

_Potomci nemají cíle._

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[navrh_palac_kovarna]] – design, depth 4, valid, in_progress
- [[stav_palac_kovarna]] – state, depth 4, valid

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[05_constructions]] | `Palac_Kovarna.py`, `Palac_Kovarna_Kul.py`, `Palac_Kovarna_Okap.py`, `Palac_Kovarna_Pristresek.py`, `Palac_Kovarna_Stena.py`, `Palac_Kovarna_Vyhen.py` | [[navrh_palac_kovarna]], [[stav_palac_kovarna]] |
| [[06_furnishing]] | `Palac_Kovarna.py`, `Palac_Kovarna_Capture.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Kul.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Okap.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Pristresek.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Stena.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Vyhen.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Palac_Kovarna.py` | entry | 06_furnishing | name |
| `/PrototypeDesigns/Lapikus/06_furnishing/vybaveni/Palac_Kovarna_Capture.py` | entry | 06_furnishing | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-21 · `Maintenance/reports/ue_Palac_Kovarna.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 15 vlastních, 37 za potomky (Palac_Kovarna_Vybaveni)
- Třídy: StaticMesh 7, Blueprint 0, BSP 0, ostatní 8
- Zástupné meshe (`/Engine/BasicShapes/`): 2; výchozí materiály: 0
- Fáze: –
- Rozsah: 762 × 1494 × 3807 cm
- Pro srovnání `depth_*`: structures 4; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)
- Pozor: `state` stav_palac_kovarna (2026-11-16) je starší než čtení z UE (2026-11-21); ověř § *V levelu*; report potvrzuje jen „v levelu je“, vzhled a funkci § *Vizuálně ověřeno*

<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0016 (G2, [[Palac_Kovarna]]): očekávaná doména gameplay (kind structure) bez target_gameplay ani u potomků; očekávaná doména structures (kind structure) bez target_structures ani u potomků
- Fronta T-0007 (–, [[navrh_palac_kovarna]]): kap. 0 duplicitní se [[stav_palac_kovarna]]: sjednotit (M22)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
