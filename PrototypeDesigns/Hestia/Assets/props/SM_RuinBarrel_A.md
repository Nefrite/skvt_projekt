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
aliases: ["SM_RuinBarrel"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]", "[[Palac_Obydli]]"]
envelope: [62, 62, 81]
stand_in: none
asset_source: tools/meshes/mesh_props.py:barrel
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinBarrel_A
variants: []
---
# SM_RuinBarrel_A

## Účel a použití
Kalicí sud s vodou (Ø 0,6 m, výška 0,8 m), dužiny a obruče; i sud pod okapem domu a kovárny.

Osy: nejdelší rozměr podél Z (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/props/`): 61,3 × 61,2 × 80,3 cm
- varianty v UE: `SM_RuinBarrel_A`
- sloty: `wood`, `endgrain`, `iron`, `water`; výchozí materiál dílce `wood`
- verze: `STONE_MESH_VERSION["SM_RuinBarrel"]` = 3; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
