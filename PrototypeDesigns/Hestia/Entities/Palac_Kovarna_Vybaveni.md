---
# orchestrace
type: entity
updated: 2026-11-23
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
depth_structures: 4
target_structures: 4
target_gameplay: 0
---
# Palac_Kovarna_Vybaveni

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 4 | 4 | 4 | build | ✔ |
| gameplay | – | – | 0 | design | ✔ |

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

Poslední čtení: 2026-11-23 · `Maintenance/reports/ue_Palac_Kovarna_Vybaveni.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 37 vlastních
- Třídy: StaticMesh 37, Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 0; výchozí materiály: 0
- Fáze: –
- Rozsah: 625 × 600 × 372 cm
- Pro srovnání `depth_*`: structures 4; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Assety
<!-- hestia:generated:start -->

Souhrn: requested 0, in_progress 1, generated 0, imported 21, verified 0 · graybox 0 · outdated v UE — (signál vedle `depth_*`, hloubka se z něj nepočítá)

| Asset | Stav | Náhrada v levelu |
|---|---|---|
| [[MI_RuinSandstone]] | in_progress | none |
| [[MI_RuinCharcoal]] | imported | none |
| [[MI_RuinIron]] | imported | none |
| [[MI_RuinIronClean]] | imported | none |
| [[MI_RuinLeather]] | imported | none |
| [[MI_RuinWater]] | imported | none |
| [[SM_RuinAnvil_A]] | imported | none |
| [[SM_RuinBarrel_A]] | imported | none |
| [[SM_RuinBasket_A]] | imported | none |
| [[SM_RuinBellows_A]] | imported | none |
| [[SM_RuinChisel_A]] | imported | none |
| [[SM_RuinCoalBoxLid_A]] | imported | none |
| [[SM_RuinCoalBox_A]] | imported | none |
| [[SM_RuinGrindstoneTreadle_A]] | imported | none |
| [[SM_RuinHammer_A]] | imported | none |
| [[SM_RuinIronBars_A]] | imported | none |
| [[SM_RuinNailHeader_A]] | imported | none |
| [[SM_RuinStool_A]] | imported | none |
| [[SM_RuinStump_A]] | imported | none |
| [[SM_RuinTongs_A]] | imported | none |
| [[SM_RuinWoodpile_A]] | imported | none |
| [[SM_RuinWorkbench_A]] | imported | none |

<!-- hestia:generated:end -->
## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
- [x] Unreal (report `ue_Palac_Kovarna_Vybaveni.json`, 2026-11-21): 37 actorů StaticMesh z dat (`furnishing.json`), žádný zástupný mesh ani výchozí materiál; podle vodítka (meshe a data → asset_data) by realizace odpovídala spíš 4 než `depth_structures: 3`. Ponechat 3, nebo zvýšit? (rozhoduje realizátor nebo GameDesigner) — agent pilotu, 2026-11-21 → GameDesigner 2026-11-21: zvýšit na 4; zapsáno `depth_structures: 4`
<!-- hestia:generated:start -->

- Fronta T-0007 (–, [[navrh_palac_kovarna]]): kap. 0 duplicitní se [[stav_palac_kovarna]]: sjednotit (M22)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
