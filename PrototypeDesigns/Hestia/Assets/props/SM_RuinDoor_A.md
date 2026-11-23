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
aliases: ["SM_RuinDoor"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Obydli]]"]
envelope: [102, 10, 220]
stand_in: none
asset_source: tools/meshes/mesh_props.py:door
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinDoor_A
variants: []
---
# SM_RuinDoor_A

## Účel a použití
Dveře 1,0 × 2,2 m z prken se svlaky; zrcadlit podle strany závěsů.

Osy: dveře v rovině XZ, tloušťka Y; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/props/`): 101,8 × 9,3 × 219,3 cm
- varianty v UE: `SM_RuinDoor_A`
- sloty: `wood`, `iron`; výchozí materiál dílce `wood`
- verze: `STONE_MESH_VERSION["SM_RuinDoor"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
