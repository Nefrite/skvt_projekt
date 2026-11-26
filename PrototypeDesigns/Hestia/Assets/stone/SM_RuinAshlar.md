---
# orchestrace
type: asset
asset_status: in_progress
requested_by: legacy
requested:
owner: Builder
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-24
aliases: []
# hra
asset_kind: mesh
asset_category: stone
used_by: ["[[Lapikus]]"]
envelope: [100, 100, 100]
stand_in: none
asset_source: tools/meshes/mesh_stone.py:build
ue_path: 
variants: []
---
# SM_RuinAshlar

## Účel a použití
Kvádr 100 × 100 × 100 cm s lehce sraženými hranami: dlažba a záložní ostění (`ASHLAR_MESH`, když `DRESSED_FRAMES = False`).

Osy: krychle, natahuje se ve všech osách; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

## Požadavek

## Na míru

## Z kódu
Ručně (doplněk k bloku: zdroj bez rozměru, rozměr z OBJ k 2026-11-23):
- rozměr (bounding box OBJ `meshes/stone/`): 100,0 × 100,0 × 100,0 cm
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr: rozměr neznámý; `envelope` 100 × 100 × 100 cm se proti rozměru nekontroluje
- Varianty: `SM_RuinAshlar`
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Stones/SM_RuinAshlar.SM_RuinAshlar`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/meshes/stone/SM_RuinAshlar.obj`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Stones/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
- Asset je vyrobený a `.uasset` existuje, karta ale nemá vlastní náhled (podmínka stavu `generated`, 07 kap. 20): zůstává `in_progress`, dokud Builder nedoplní náhled a nenastaví `imported`.
