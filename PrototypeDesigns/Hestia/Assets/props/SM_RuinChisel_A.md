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
aliases: ["SM_RuinChisel"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]"]
envelope: [21, 3, 3]
stand_in: none
asset_source: tools/meshes/mesh_props.py:chisel
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinChisel_A
variants: []
---
# SM_RuinChisel_A

## Účel a použití
Sekáč (nářadí na liště).

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 20.6 × 2.8 × 2.8 cm; `envelope` 21 × 3 × 3 cm: vejde se
- Varianty: `SM_RuinChisel_A`
- Sloty: ['ironclean']
- Výchozí materiál: `ironclean`
- Verze: 2 (prefix `SM_RuinChisel`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinChisel_A.SM_RuinChisel_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:246`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
