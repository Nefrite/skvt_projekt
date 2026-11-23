---
# orchestrace
type: entity
updated: 2026-11-19
aliases: []
# hra
kind: structure
parent: "[[Hradby_a_Brana]]"
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
# Strazni_Vez

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

_Zatím žádné kroky._

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

_Žádné soubory._

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-23 · `Maintenance/reports/ue_Strazni_Vez.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 14 vlastních
- Třídy: StaticMesh 0, ISM 14 (2323 instancí), Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 4; výchozí materiály: 0
- Fáze: –
- Rozsah: 1068 × 1097 × 963 cm
- Kořen daleko od geometrie (`pivot_far`, víc než 500 cm): 14 actorů; informace pro modelování v instanci, ne nález
- Pro srovnání `depth_*`: structures 4; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0021 (G2, [[Strazni_Vez]]): očekávaná doména gameplay (kind structure) bez target_gameplay; očekávaná doména structures (kind structure) bez target_structures
- Fronta F-0022 (G4, [[Strazni_Vez]]): status built bez platného dokumentu state

<!-- hestia:generated:end -->

## Historie a rozhodnutí
