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
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/props/`): 53,6 × 49,7 × 46,7 cm
- varianty v UE: `SM_RuinStump_A`, `SM_RuinStump_B`
- sloty: `wood`, `endgrain`, `bark`; výchozí materiál dílce `wood`
- verze: `STONE_MESH_VERSION["SM_RuinStump"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 2 variant v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1, 6.6 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
