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
aliases: ["SM_RuinShutter"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Obydli]]"]
envelope: [62, 9, 60]
stand_in: none
asset_source: tools/meshes/mesh_props.py:shutter
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinShutter_A
variants: []
---
# SM_RuinShutter_A

## Účel a použití
Okenice 60 × 60 cm; menší 50 × 50 škálou 0,83.

Osy: okenice v rovině XZ, tloušťka Y; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 61.4 × 8.4 × 59.2 cm; `envelope` 62 × 9 × 60 cm: vejde se
- Varianty: `SM_RuinShutter_A`
- Sloty: ['wood', 'endgrain', 'iron']
- Výchozí materiál: `wood`
- Verze: 1 (prefix `SM_RuinShutter`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinShutter_A.SM_RuinShutter_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:267`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
