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
aliases: ["SM_RuinForkHead"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Vez_Pristresek]]", "[[Palac_Kovarna]]", "[[Palac_Obydli]]", "[[Nadvori_Stan]]"]
envelope: [45, 30, 12]
stand_in: none
asset_source: tools/meshes/mesh_log.py:make_fork
ue_path: /Game/Skvt/Lapikus/Ruin/Wood/SM_RuinForkHead_A
variants: [SM_RuinForkHead_B]
---
# SM_RuinForkHead_A

## Účel a použití
Hlava rozsochy s kůrou (vidlice), nasadí se na kůl `SM_RuinLogBark` nebo `SM_RuinPoleBark` (kůly přístřešku věže, vidlice žlabů, stříška stanu).

Osy: délka podél X (nominál 45,0 cm, délka a průměr přes scale); kmen na −X, vidlice na +X, ramena v rovině XY; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Kulatina_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně: klíč není v `LIB_MESHES` a manifest `asset_sources.yaml` ho nepokrývá (`ROUND_MESHES`, `WOOD_NOMINAL`, kameny v `mesh_stone.py`); stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/wood/`): 45,0 × 30,0 × 12,0 cm
- varianty v UE: `SM_RuinForkHead_A`, `SM_RuinForkHead_B`
- sloty: `wood`, `endgrain`, `bark`
- verze: `STONE_MESH_VERSION["SM_RuinForkHead"]` = 1; `MESH_AXES` = 10
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
