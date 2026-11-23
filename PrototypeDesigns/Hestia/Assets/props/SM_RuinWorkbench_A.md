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
aliases: ["SM_RuinWorkbench"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]", "[[Palac_Obydli]]"]
envelope: [222, 86, 86]
stand_in: none
asset_source: tools/meshes/mesh_props.py:workbench
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinWorkbench_A
variants: []
---
# SM_RuinWorkbench_A

## Účel a použití
Ponk se svěrákem (2,2 × 0,7 × 0,85 m); v síni domu menší (škálovat).

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 221.5 × 85.9 × 85.2 cm; `envelope` 222 × 86 × 86 cm: vejde se
- Varianty: `SM_RuinWorkbench_A`
- Sloty: ['wood', 'iron']
- Výchozí materiál: `wood`
- Verze: 3 (prefix `SM_RuinWorkbench`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinWorkbench_A.SM_RuinWorkbench_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:243`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinWorkbench_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinWorkbench_A.SM_RuinWorkbench_A`) · `RuinStoneVersion` 3 (kód 3) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1, 6.2, 6.6 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
