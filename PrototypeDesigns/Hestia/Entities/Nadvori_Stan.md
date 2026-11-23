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

## Assety
<!-- hestia:generated:start -->

Souhrn: requested 0, in_progress 1, generated 0, imported 19, verified 0 · graybox 0 · outdated v UE 0 (signál vedle `depth_*`, hloubka se z něj nepočítá)

| Asset | Stav | Náhrada v levelu |
|---|---|---|
| [[MI_RuinWood]] | in_progress | none |
| [[MI_RuinBark]] | imported | none |
| [[MI_RuinCanvas]] | imported | none |
| [[MI_RuinIron]] | imported | none |
| [[MI_RuinRope]] | imported | none |
| [[MI_RuinSackcloth]] | imported | none |
| [[MI_RuinStraw]] | imported | none |
| [[MI_RuinWool]] | imported | none |
| [[SM_RuinBarkStrip_A]] | imported | none |
| [[SM_RuinBundle_A]] | imported | none |
| [[SM_RuinCampBed_A]] | imported | none |
| [[SM_RuinCanvasTent_A]] | imported | none |
| [[SM_RuinChestSmall_A]] | imported | none |
| [[SM_RuinForkHead_A]] | imported | none |
| [[SM_RuinLashing_A]] | imported | none |
| [[SM_RuinPoleBark_A]] | imported | none |
| [[SM_RuinPole_A]] | imported | none |
| [[SM_RuinRope_A]] | imported | none |
| [[SM_RuinStakeSmall_A]] | imported | none |
| [[SM_RuinStump_A]] | imported | none |

<!-- hestia:generated:end -->
## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta T-0035 (role:Builder, [[Nadvori_Stan]]): Typ `tent` (stojky, hřeben, kolíky, šňůry jako řetěz [[SM_RuinRope_A]]) a stříška stanu typem `bark_roof` (typ zakládá [[predani_brana_straz_striska_stavitel]]); plachtu [[SM_RuinCanvasTent_A]] posadit podle `center` v `meshes/textile/SM_RuinCanvasTent_A.json` (doklad: [[CHECKLIST_assets_navrhy]] kap. 6.5, 7; [[navrh_nadvori_stan]]; entita `on_hold`)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
