---
# orchestrace
type: asset
asset_status: imported
requested_by: Furnisher
requested: 2026-11-14
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: ["SM_RuinStump"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]", "[[Nadvori_Stan]]"]
envelope: [54, 50, 47]
stand_in: none
asset_source: tools/meshes/mesh_props.py:stump
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinStump_A
variants: [SM_RuinStump_B]
---
# SM_RuinStump_A

## Účel a použití
Špalek z kulatiny s kůrou a horním čelem: pod kovadlinu, pod hřebovnici, k sezení ve stanu.

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 53.6 × 49.7 × 46.7 cm; `envelope` 54 × 50 × 47 cm: vejde se
- Varianty: `SM_RuinStump_A`, `SM_RuinStump_B`
- Sloty: ['wood', 'endgrain', 'bark']
- Výchozí materiál: `wood`
- Verze: 1 (prefix `SM_RuinStump`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinStump_A.SM_RuinStump_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:238`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinStump_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinStump_A.SM_RuinStump_A`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current
- `SM_RuinStump_B` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinStump_B.SM_RuinStump_B`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1, 6.6 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
