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
aliases: ["SM_RuinMallet"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Obydli]]"]
envelope: [10, 35, 14]
stand_in: none
asset_source: tools/meshes/mesh_props.py:mallet
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinMallet_A
variants: []
---
# SM_RuinMallet_A

## Účel a použití
Dřevěná palice s obručemi (tesařské nářadí staveniště).

Osy: nejdelší rozměr podél Y (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 9.5 × 34.9 × 14 cm; `envelope` 10 × 35 × 14 cm: vejde se
- Varianty: `SM_RuinMallet_A`
- Sloty: ['wood', 'endgrain', 'ironclean']
- Výchozí materiál: `wood`
- Verze: 2 (prefix `SM_RuinMallet`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinMallet_A.SM_RuinMallet_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:256`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.3 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
