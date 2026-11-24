---
# orchestrace
type: asset
asset_status: in_progress
requested_by: legacy
requested:
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-24
aliases: ["SM_RuinOvenDome"]
# hra
asset_kind: mesh
asset_category: wattle
used_by: ["[[Palac_Obydli]]", "[[Guesthouse]]"]
envelope: [140, 100, 40]
stand_in: none
asset_source: tools/meshes/mesh_wattle.py:make_dome
ue_path: 
variants: [SM_RuinOvenDome_B]
---
# SM_RuinOvenDome_A

## Účel a použití
Hliněná klenba pece (plné těleso, valená klenba): pec s nístějí domu, kamna Guesthouse (škálovat).

Osy: X šířka (rozpětí), Y hloubka, Z výška; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 140 × 100 × 40 cm; `envelope` 140 × 100 × 40 cm: vejde se
- Varianty: `SM_RuinOvenDome_A`, `SM_RuinOvenDome_B`
- Sloty: ['daub', 'wattle']
- Výchozí materiál: `daub`
- Verze: 1 (prefix `SM_RuinOvenDome`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Wattle/SM_RuinOvenDome_A.SM_RuinOvenDome_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:229`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 2 variant v `Content/Skvt/Lapikus/Ruin/Wattle/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
- Asset je vyrobený a `.uasset` existuje, karta ale nemá vlastní náhled (podmínka stavu `generated`, 07 kap. 20): zůstává `in_progress`, dokud Crafter nedoplní náhled a nenastaví `imported`.
