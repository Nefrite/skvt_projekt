---
# orchestrace
type: asset
asset_status: in_progress
requested_by: Furnisher
requested: 2026-11-14
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: ["SM_RuinOvenDoor"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Obydli]]", "[[Guesthouse]]"]
envelope: [46, 9, 42]
stand_in: none
asset_source: tools/meshes/mesh_props.py:oven_door
ue_path: 
variants: []
---
# SM_RuinOvenDoor_A

## Účel a použití
Poklop ústí pece: plech v rovině XZ, dřevěná rukojeť na −Y; střed plechu +3,56 cm v Y od středu meshe.

Osy: plech v rovině XZ, rukojeť −Y; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/props/`): 45,9 × 8,6 × 41,9 cm
- varianty v UE: `SM_RuinOvenDoor_A`
- sloty: `wood`, `endgrain`, `iron`; výchozí materiál dílce `wood`
- verze: `STONE_MESH_VERSION["SM_RuinOvenDoor"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.2, 6.8 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
- Asset je vyrobený a `.uasset` existuje, karta ale nemá vlastní náhled (podmínka stavu `generated`, 07 kap. 20): zůstává `in_progress`, dokud Crafter nedoplní náhled a nenastaví `imported`.
