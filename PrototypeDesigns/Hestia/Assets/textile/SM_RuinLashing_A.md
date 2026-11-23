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
aliases: ["SM_RuinLashing"]
# hra
asset_kind: mesh
asset_category: textile
used_by: ["[[Vez_Pristresek]]", "[[Brana_Straz]]", "[[Nadvori_Stan]]"]
envelope: [7, 11, 11]
stand_in: none
asset_source: tools/meshes/mesh_textile.py:make_lashing
ue_path: /Game/Skvt/Lapikus/Ruin/Textile/SM_RuinLashing_A
variants: [SM_RuinLashing_B]
---
# SM_RuinLashing_A

## Účel a použití
Ovázání na křížení tyčí: závity lana kolem tyče Ø 8 cm, škáluje se s tyčí (krokve, ráhna, vidlice).

Osy: osa tyče X; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Knihovna_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/textile/`): 7,0 × 10,5 × 10,5 cm
- varianty v UE: `SM_RuinLashing_A`, `SM_RuinLashing_B`
- sloty: `rope`; výchozí materiál dílce `rope`
- verze: `STONE_MESH_VERSION["SM_RuinLashing"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 2 variant v `Content/Skvt/Lapikus/Ruin/Textile/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
