---
# orchestrace
type: asset
asset_status: imported
requested_by: Builder
requested: 2026-11-14
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
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
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/textile/`): 300,0 × 221,6 × 93,8 cm
- varianty v UE: `SM_RuinCanvasSample_A`
- sloty: `canvas`; výchozí materiál dílce `canvas`
- verze: `STONE_MESH_VERSION["SM_RuinCanvasSample"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Textile/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
