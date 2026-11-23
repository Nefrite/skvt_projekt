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
aliases: ["SM_RuinGrindstone"]
# hra
asset_kind: mesh
asset_category: props
used_by: []
envelope: [120, 86, 106]
stand_in: none
asset_source: tools/meshes/mesh_props.py:grindstone
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinGrindstone_A
variants: []
---
# SM_RuinGrindstone_A

## Účel a použití
Brus na ruční kliku; v kovárně je šlapací varianta (`SM_RuinGrindstoneTreadle`), tento zůstává v knihovně (Jirka 14. 11. 2026).

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 120 × 86 × 105.4 cm; `envelope` 120 × 86 × 106 cm: vejde se
- Varianty: `SM_RuinGrindstone_A`
- Sloty: ['wood', 'iron', 'sandstone', 'water']
- Výchozí materiál: `wood`
- Verze: 6 (prefix `SM_RuinGrindstone`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinGrindstone_A.SM_RuinGrindstone_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:242`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
