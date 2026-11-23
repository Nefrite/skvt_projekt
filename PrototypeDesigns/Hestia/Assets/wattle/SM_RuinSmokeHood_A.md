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
aliases: ["SM_RuinSmokeHood"]
# hra
asset_kind: mesh
asset_category: wattle
used_by: ["[[Palac_Kovarna]]", "[[Palac_Obydli]]", "[[Guesthouse]]"]
envelope: [140, 120, 100]
stand_in: none
asset_source: tools/meshes/mesh_wattle.py:make_tube
ue_path: /Game/Skvt/Lapikus/Ruin/Wattle/SM_RuinSmokeHood_A
variants: [SM_RuinSmokeHood_B]
---
# SM_RuinSmokeHood_A

## Účel a použití
Dymník: zužující se koš z proutí s hlínou, dole 140 × 120, nahoře 50 × 50 cm, výška 100 cm (škáluje se) – ohniště domu, výheň kovárny, kamna Guesthouse.

Osy: osa koše Z (nahoru); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Knihovna_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/wattle/`): 140,0 × 120,0 × 100,0 cm
- varianty v UE: `SM_RuinSmokeHood_A`, `SM_RuinSmokeHood_B`
- sloty: `daub`, `wattle`; výchozí materiál dílce `daub`
- verze: `STONE_MESH_VERSION["SM_RuinSmokeHood"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 2 variant v `Content/Skvt/Lapikus/Ruin/Wattle/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
