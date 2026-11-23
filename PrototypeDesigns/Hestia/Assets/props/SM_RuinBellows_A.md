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
aliases: ["SM_RuinBellows"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]"]
envelope: [211, 86, 139]
stand_in: none
asset_source: tools/meshes/mesh_props.py:bellows
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinBellows_A
variants: []
---
# SM_RuinBellows_A

## Účel a použití
Měch na dřevěném rámu včetně výfučny (1,7 × 0,8 m, rám ve výšce 0,9 m); funkční střed (výfučna, rám) změřit na `mesh_props.py`.

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 210.4 × 85.4 × 139 cm; `envelope` 211 × 86 × 139 cm: vejde se
- Varianty: `SM_RuinBellows_A`
- Sloty: ['wood', 'iron', 'leather']
- Výchozí materiál: `wood`
- Verze: 5 (prefix `SM_RuinBellows`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinBellows_A.SM_RuinBellows_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:240`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
