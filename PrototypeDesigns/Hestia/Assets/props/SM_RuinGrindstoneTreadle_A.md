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
aliases: ["SM_RuinGrindstoneTreadle"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]"]
envelope: [120, 86, 106]
stand_in: none
asset_source: tools/meshes/mesh_props.py:grindstone (treadle=True)
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinGrindstoneTreadle_A
variants: []
---
# SM_RuinGrindstoneTreadle_A

## Účel a použití
Šlapací brus: kotouč Ø 0,7 m na rámu 1,2 × 0,6 m, osa 0,75 m, kliková páka, ojnice, šlapadlo, korýtko (Jirka 14. 11. 2026).

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/props/`): 120,0 × 86,0 × 105,3 cm
- varianty v UE: `SM_RuinGrindstoneTreadle_A`
- sloty: `wood`, `endgrain`, `iron`, `sandstone`, `water`; výchozí materiál dílce `wood`
- verze: `STONE_MESH_VERSION["SM_RuinGrindstoneTreadle"]` = 2; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
