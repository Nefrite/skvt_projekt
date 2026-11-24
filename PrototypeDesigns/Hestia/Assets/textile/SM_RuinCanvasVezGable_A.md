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
aliases: ["SM_RuinCanvasVezGable"]
# hra
asset_kind: mesh
asset_category: textile
used_by: ["[[Vez_Pristresek]]"]
envelope: [3, 269, 112]
stand_in: none
asset_source: tools/meshes/mesh_textile.py:canvas_vez
ue_path: 
variants: []
---
# SM_RuinCanvasVezGable_A

## Účel a použití
Štít plachty přístřešku věže: trojúhelník zavěšený na krajní tyči nad `Vez_Z`, spodní lem vodorovně s tyčkou Ø 5 cm.

Osy: svislý štít, X = tloušťka; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

## Požadavek

## Na míru
Tvar na míru: `meshes/textile/SM_RuinCanvasVezGable_A.json` (střed a rozměr v osách stavby); stavba bere rozměr z `.json`.

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 2 × 269 × 111.8 cm; `envelope` 3 × 269 × 112 cm: vejde se
- Varianty: `SM_RuinCanvasVezGable_A`
- Sloty: ['canvas']
- Výchozí materiál: `canvas`
- Verze: 1 (prefix `SM_RuinCanvasVez`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Textile/SM_RuinCanvasVezGable_A.SM_RuinCanvasVezGable_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:235`
- Data: `PrototypeDesigns/Lapikus/05_constructions/constructions.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Textile/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
- Asset je vyrobený a `.uasset` existuje, karta ale nemá vlastní náhled (podmínka stavu `generated`, 07 kap. 20): zůstává `in_progress`, dokud Crafter nedoplní náhled a nenastaví `imported`.
