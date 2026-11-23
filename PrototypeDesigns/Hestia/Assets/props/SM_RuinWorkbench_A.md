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
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/props/`): 221,5 × 85,9 × 85,2 cm
- varianty v UE: `SM_RuinWorkbench_A`
- sloty: `wood`, `iron`; výchozí materiál dílce `wood`
- verze: `STONE_MESH_VERSION["SM_RuinWorkbench"]` = 3; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1, 6.2, 6.6 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
