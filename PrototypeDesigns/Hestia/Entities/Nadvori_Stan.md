---
# orchestrace
type: entity
updated: 2026-11-23
aliases: []
# hra
kind: object
parent: "[[Nadvori]]"
located_in: []
derived_from:
alternative_to: []
pattern:
status: on_hold
# depth_<domain> / target_<domain>: očekávané domény podle kind (01, kap. 8), jiné jen když se řeší
# depth_* = realizace (Unreal, data, StateTree); hloubka návrhu se počítá z dokumentů (01, kap. 5)
# target_mode_<domain>: design | build, jen při odchylce od výchozího režimu domény
ue_path:
assets: []
depth_structures: 0
target_structures: 4
target_gameplay: 0
---
# Nadvori_Stan

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 2 | 0 | 4 | build | −4 |
| gameplay | – | – | 0 | design | ✔ |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[navrh_nadvori_stan]] – design, depth 2, valid, on_hold

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

_Zatím žádné kroky._

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

_Žádné soubory._

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-23 · `Maintenance/reports/ue_Nadvori_Stan.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 0 vlastních
- Třídy: StaticMesh 0, Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 0; výchozí materiály: 0
- Fáze: –
- Pro srovnání `depth_*`: structures 0; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0013 (G2, [[Nadvori_Stan]]): očekávaná doména gameplay (kind object) bez target_gameplay; očekávaná doména structures (kind object) bez target_structures

<!-- hestia:generated:end -->

## Historie a rozhodnutí
