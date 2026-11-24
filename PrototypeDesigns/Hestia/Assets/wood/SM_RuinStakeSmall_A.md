---
# orchestrace
type: asset
asset_status: imported
requested_by: legacy
requested:
owner: Builder
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-24
aliases: ["SM_RuinStakeSmall"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Nadvori_Stan]]", "[[Brana]]"]
envelope: [160, 7, 7]
stand_in: none
asset_source: tools/meshes/mesh_log.py:make_stake_small
ue_path: /Game/Skvt/Lapikus/Ruin/Wood/SM_RuinStakeSmall_A
variants: [SM_RuinStakeSmall_B]
---
# SM_RuinStakeSmall_A

## Účel a použití
Loupaný kůl zašpičatělý na obou koncích (ramena jezdce, kolíky stanu).

Osy: délka podél X (nominál 160,0 cm, délka a průměr přes scale); špičky na obou koncích X; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Kulatina_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 160 × 7 × 7 cm; `envelope` 160 × 7 × 7 cm: vejde se
- Varianty: `SM_RuinStakeSmall_A`, `SM_RuinStakeSmall_B`
- Sloty: ['wood', 'endgrain']
- Verze: 1 (prefix `SM_RuinStake`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Wood/SM_RuinStakeSmall_A.SM_RuinStakeSmall_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:200`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 2 variant v `Content/Skvt/Lapikus/Ruin/Wood/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 2.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
