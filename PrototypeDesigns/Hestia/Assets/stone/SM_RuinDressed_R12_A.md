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
aliases: ["SM_RuinDressed_R12"]
# hra
asset_kind: mesh
asset_category: stone
used_by: ["[[Lapikus]]"]
envelope: [102, 45, 30]
stand_in: none
asset_source: tools/meshes/mesh_stone.py:make_stone
ue_path: /Game/Skvt/Lapikus/Ruin/Stones/SM_RuinDressed_R12_A
variants: [SM_RuinDressed_R12_B, SM_RuinDressed_R18_A, SM_RuinDressed_R18_B, SM_RuinDressed_R26_A, SM_RuinDressed_R26_B, SM_RuinDressed_R34_A, SM_RuinDressed_R34_B]
---
# SM_RuinDressed_R12_A

## Účel a použití
Opracovaný kámen ostění, nadpraží a střílen (`DRESSED_FRAMES`), mírně otlučený. Varianty podle poměru délka/výška (R12 = 1,2 až R34 = 3,4, `STONE_RATIOS`) a tvaru (A/B); jmenovitý kámen výška 30 × hloubka 45 cm (`STONE_NOMINAL`), délka = výška × poměr, ve zdi se natahuje na blok.

Osy: délka podél X, hloubka zdi Y, výška Z; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/03_ruin/blocks/Zricenina_strilny_osteni_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně (doplněk k bloku: zdroj bez rozměru, rozměr z OBJ k 2026-11-23):
- rozměr (bounding box OBJ `meshes/stone/`): 36,0 × 45,0 × 30,0 cm (SM_RuinDressed_R12_A, SM_RuinDressed_R12_B); 54,0 × 45,0 × 30,0 cm (SM_RuinDressed_R18_A, SM_RuinDressed_R18_B); 78,0 × 45,0 × 30,0 cm (SM_RuinDressed_R26_A, SM_RuinDressed_R26_B); 102,0 × 45,0 × 30,0 cm (SM_RuinDressed_R34_A, SM_RuinDressed_R34_B)
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr: rozměr neznámý; `envelope` 102 × 45 × 30 cm se proti rozměru nekontroluje
- Varianty: `SM_RuinDressed_R12_A`, `SM_RuinDressed_R12_B`, `SM_RuinDressed_R18_A`, `SM_RuinDressed_R18_B`, `SM_RuinDressed_R26_A`, `SM_RuinDressed_R26_B`, `SM_RuinDressed_R34_A`, `SM_RuinDressed_R34_B`
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Stones/SM_RuinDressed_R12_A.SM_RuinDressed_R12_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/meshes/stone/SM_RuinDressed_R12_A.obj`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 8 variant v `Content/Skvt/Lapikus/Ruin/Stones/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
