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
aliases: ["SM_RuinPost"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Palac_Kovarna]]", "[[Palac_Obydli]]", "[[Vez_Pristresek]]", "[[Brana_Straz]]", "[[Guesthouse]]"]
envelope: [25, 25, 100]
stand_in: none
asset_source: tools/meshes/mesh_wood.py:make_timber
ue_path: 
variants: [SM_RuinPost_B, SM_RuinPost_C]
---
# SM_RuinPost_A

## Účel a použití
Sloup (hraněný), délka nahoru: sloupy přístřešků a krovů.

Osy: délka podél Z (nominál 100 cm), průřez X × Y; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

## Požadavek

## Na míru

## Z kódu
Ručně (doplněk k bloku: zdroj bez rozměru, rozměr z OBJ k 2026-11-23):
- rozměr (bounding box OBJ `meshes/wood/`): 25,0 × 25,0 × 100,0 cm
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 25 × 25 × 100 cm; `envelope` 25 × 25 × 100 cm: vejde se
- Varianty: `SM_RuinPost_A`, `SM_RuinPost_B`, `SM_RuinPost_C`
- Verze: 2 (prefix `SM_RuinPost_`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Wood/SM_RuinPost_A.SM_RuinPost_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:188`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 3 variant v `Content/Skvt/Lapikus/Ruin/Wood/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
- Asset je vyrobený a `.uasset` existuje, karta ale nemá vlastní náhled (podmínka stavu `generated`, 07 kap. 20): zůstává `in_progress`, dokud Builder nedoplní náhled a nenastaví `imported`.
