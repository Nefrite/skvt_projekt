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
aliases: ["SM_RuinBed"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Obydli]]"]
envelope: [201, 88, 63]
stand_in: none
asset_source: tools/meshes/mesh_props.py:bed (folded=False/True)
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinBed_A
variants: [SM_RuinBedFolded_A]
---
# SM_RuinBed_A

## Účel a použití
Lůžko domu posádky (2,0 × 0,8 m), houně přes slámu; tvarová varianta `SM_RuinBedFolded_A` s houní složenou v nohách.

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 200.2 × 87.2 × 61.9 cm; `envelope` 201 × 88 × 63 cm: vejde se
- Varianty: `SM_RuinBed_A`, `SM_RuinBedFolded_A`
- Sloty: ['wood', 'straw', 'wool']
- Výchozí materiál: `wood`
- Verze: 1 (prefix `SM_RuinBed`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinBed_A.SM_RuinBed_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:261`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 2 variant v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
