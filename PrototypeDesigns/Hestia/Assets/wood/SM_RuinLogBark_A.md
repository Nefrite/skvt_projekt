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
aliases: ["SM_RuinLogBark"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Vez_Pristresek]]", "[[Palac_Obydli]]", "[[Brana]]"]
envelope: [100, 20, 20]
stand_in: none
asset_source: tools/meshes/mesh_log.py:make_log
ue_path: /Game/Skvt/Lapikus/Ruin/Wood/SM_RuinLogBark_A
variants: [SM_RuinLogBark_B, SM_RuinLogBark_C]
---
# SM_RuinLogBark_A

## Účel a použití
Kulatina s kůrou, místy odloupnutá (kmen jezdce, hřeben a okapová tyč věže, hromada kulatiny).

Osy: délka podél X (nominál 100,0 cm, délka a průměr přes scale); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Kulatina_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/wood/`): 100,0 × 20,0 × 20,0 cm
- varianty v UE: `SM_RuinLogBark_A`, `SM_RuinLogBark_B`, `SM_RuinLogBark_C`
- sloty: `wood`, `endgrain`, `bark`
- verze: `STONE_MESH_VERSION["SM_RuinLog"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 3 variant v `Content/Skvt/Lapikus/Ruin/Wood/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 2.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
