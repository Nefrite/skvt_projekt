---
# orchestrace
type: asset
asset_status: in_progress
requested_by: Builder
requested: 2026-11-14
owner: Builder
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: []
# hra
asset_kind: mesh
asset_category: stone
used_by: ["[[Lapikus]]"]
envelope: [100, 100, 100]
stand_in: none
asset_source: tools/meshes/mesh_stone.py:build
ue_path: 
variants: []
---
# SM_RuinAshlar

## Účel a použití
Kvádr 100 × 100 × 100 cm s lehce sraženými hranami: dlažba a záložní ostění (`ASHLAR_MESH`, když `DRESSED_FRAMES = False`).

Osy: krychle, natahuje se ve všech osách; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/stone/`): 100,0 × 100,0 × 100,0 cm
- varianty v UE: `SM_RuinAshlar`
- verze: bez záznamu v `STONE_MESH_VERSION` (výchozí); `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Stones/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
- Asset je vyrobený a `.uasset` existuje, karta ale nemá vlastní náhled (podmínka stavu `generated`, 07 kap. 20): zůstává `in_progress`, dokud Builder nedoplní náhled a nenastaví `imported`.
