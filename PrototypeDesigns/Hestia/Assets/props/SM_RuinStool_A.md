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
aliases: ["SM_RuinStool"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]", "[[Guesthouse]]", "[[Brana_Straz]]"]
envelope: [35, 34, 46]
stand_in: none
asset_source: tools/meshes/mesh_props.py:stool
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinStool_A
variants: []
---
# SM_RuinStool_A

## Účel a použití
Třínohá stolička (sedátko Ø 32, výška 45 cm): k brusu v kovárně; v Guesthouse ke stolu ve škále 1,035.

Osy: nejdelší rozměr podél Z (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 34.9 × 33.4 × 45.4 cm; `envelope` 35 × 34 × 46 cm: vejde se
- Varianty: `SM_RuinStool_A`
- Sloty: ['wood', 'endgrain']
- Výchozí materiál: `wood`
- Verze: 1 (prefix `SM_RuinStool`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinStool_A.SM_RuinStool_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:254`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1, 6.8 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
