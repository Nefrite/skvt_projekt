---
# orchestrace
type: asset
asset_status: in_progress
requested_by: Builder
requested: 2026-11-14
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: ["SM_RuinCanvasVez"]
# hra
asset_kind: mesh
asset_category: textile
used_by: ["[[Vez_Pristresek]]"]
envelope: [600, 430, 181]
stand_in: none
asset_source: tools/meshes/mesh_textile.py:canvas_vez
ue_path: 
variants: []
---
# SM_RuinCanvasVez_A

## Účel a použití
Plachta přístřešku hlídky na věži na míru (`tower_spec.pristresek`, 6,0 × 4,3 m), prověšená mezi krokvovými tyčemi, oboustranná.

Osy: v osách stavby podle `.json`; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

## Požadavek

## Na míru
Tvar na míru: `meshes/textile/SM_RuinCanvasVez_A.json` (střed a rozměr v osách stavby); stavba bere rozměr z `.json`.

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/textile/`): 600,0 × 430,0 × 180,5 cm
- varianty v UE: `SM_RuinCanvasVez_A`
- sloty: `canvas`; výchozí materiál dílce `canvas`
- verze: `STONE_MESH_VERSION["SM_RuinCanvasVez"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Textile/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
- Asset je vyrobený a `.uasset` existuje, karta ale nemá vlastní náhled (podmínka stavu `generated`, 07 kap. 20): zůstává `in_progress`, dokud Crafter nedoplní náhled a nenastaví `imported`.
