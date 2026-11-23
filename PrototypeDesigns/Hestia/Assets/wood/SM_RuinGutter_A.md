---
# orchestrace
type: asset
asset_status: imported
requested_by: Builder
requested: 2026-11-14
owner: Builder
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: ["SM_RuinGutter"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Palac_Kovarna]]", "[[Palac_Obydli]]"]
envelope: [100, 20, 11]
stand_in: none
asset_source: tools/meshes/mesh_log.py:make_gutter
ue_path: /Game/Skvt/Lapikus/Ruin/Wood/SM_RuinGutter_A
variants: [SM_RuinGutter_B]
---
# SM_RuinGutter_A

## Účel a použití
Vydlabaný půlkmen, loupaný: žlaby a svody.

Osy: délka podél X (nominál 100,0 cm, délka a průměr přes scale); řez nahoře (+Z), vydlabaný; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Kulatina_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně: klíč není v `LIB_MESHES` a manifest `asset_sources.yaml` ho nepokrývá (`ROUND_MESHES`, `WOOD_NOMINAL`, kameny v `mesh_stone.py`); stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/wood/`): 100,0 × 20,0 × 11,0 cm
- varianty v UE: `SM_RuinGutter_A`, `SM_RuinGutter_B`
- sloty: `wood`, `endgrain`
- verze: `STONE_MESH_VERSION["SM_RuinGutter"]` = 2; `MESH_AXES` = 10
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
_v kódu nenalezeno (`asset_sources.yaml`); technické údaje doplní kód, ne karta._

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 2 variant v `Content/Skvt/Lapikus/Ruin/Wood/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 2.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
