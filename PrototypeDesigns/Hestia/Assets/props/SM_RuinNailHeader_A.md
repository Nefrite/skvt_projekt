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
aliases: ["SM_RuinNailHeader"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]"]
envelope: [25, 6, 2]
stand_in: none
asset_source: tools/meshes/mesh_props.py:nail_header
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinNailHeader_A
variants: []
---
# SM_RuinNailHeader_A

## Účel a použití
Hřebovnice (na špalku `SM_RuinStump`).

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 25 × 6 × 1.5 cm; `envelope` 25 × 6 × 2 cm: vejde se
- Varianty: `SM_RuinNailHeader_A`
- Sloty: ['ironclean']
- Výchozí materiál: `ironclean`
- Verze: 3 (prefix `SM_RuinNailHeader`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinNailHeader_A.SM_RuinNailHeader_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:247`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
