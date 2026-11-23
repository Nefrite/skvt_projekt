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
aliases: ["SM_RuinWoodpile"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]", "[[Palac_Obydli]]"]
envelope: [192, 65, 137]
stand_in: none
asset_source: tools/meshes/mesh_props.py:woodpile
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinWoodpile_A
variants: []
---
# SM_RuinWoodpile_A

## Účel a použití
Hranice štípaných polen (0,6 × 1,9 × 1,4 m): kovárna, síň domu.

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 191.3 × 65 × 136.4 cm; `envelope` 192 × 65 × 137 cm: vejde se
- Varianty: `SM_RuinWoodpile_A`
- Sloty: ['wood', 'endgrain', 'bark']
- Výchozí materiál: `wood`
- Verze: 1 (prefix `SM_RuinWoodpile`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinWoodpile_A.SM_RuinWoodpile_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:249`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1, 6.2, 6.6 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
