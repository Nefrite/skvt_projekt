---
# orchestrace
type: asset
asset_status: imported
requested_by: legacy
requested:
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-24
aliases: ["SM_RuinCanvasSample"]
# hra
asset_kind: mesh
asset_category: textile
used_by: []
envelope: [300, 222, 94]
stand_in: none
asset_source: tools/meshes/mesh_textile.py:make_canvas
ue_path: /Game/Skvt/Lapikus/Ruin/Textile/SM_RuinCanvasSample_A
variants: []
---
# SM_RuinCanvasSample_A

## Účel a použití
Ukázka plachty z `make_canvas` (3 × 2,4 m, 5 krokvových tyčí, sklon 22°) pro kontrolu generátoru; ve stavbě se nepoužívá.

Osy: plachta v rovině XY se sklonem; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Knihovna_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 300 × 221.6 × 93.8 cm; `envelope` 300 × 222 × 94 cm: vejde se
- Varianty: `SM_RuinCanvasSample_A`
- Sloty: ['canvas']
- Výchozí materiál: `canvas`
- Verze: 1 (prefix `SM_RuinCanvasSample`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Textile/SM_RuinCanvasSample_A.SM_RuinCanvasSample_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:233`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinCanvasSample_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Textile/SM_RuinCanvasSample_A.SM_RuinCanvasSample_A`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
