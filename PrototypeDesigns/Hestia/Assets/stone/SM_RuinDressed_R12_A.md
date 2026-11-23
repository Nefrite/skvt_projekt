---
# orchestrace
type: asset
asset_status: imported
requested_by: Builder
requested: 2026-11-14
owner: Builder
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
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
Ručně: klíč není v `LIB_MESHES` a manifest `asset_sources.yaml` ho nepokrývá (`ROUND_MESHES`, `WOOD_NOMINAL`, kameny v `mesh_stone.py`); stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/stone/`): 36,0 × 45,0 × 30,0 cm (SM_RuinDressed_R12_A, SM_RuinDressed_R12_B); 54,0 × 45,0 × 30,0 cm (SM_RuinDressed_R18_A, SM_RuinDressed_R18_B); 78,0 × 45,0 × 30,0 cm (SM_RuinDressed_R26_A, SM_RuinDressed_R26_B); 102,0 × 45,0 × 30,0 cm (SM_RuinDressed_R34_A, SM_RuinDressed_R34_B)
- varianty v UE: `SM_RuinDressed_R12_A`, `SM_RuinDressed_R12_B`, `SM_RuinDressed_R18_A`, `SM_RuinDressed_R18_B`, `SM_RuinDressed_R26_A`, `SM_RuinDressed_R26_B`, `SM_RuinDressed_R34_A`, `SM_RuinDressed_R34_B`
- verze: bez záznamu v `STONE_MESH_VERSION` (výchozí); `MESH_AXES` = 10
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
_v kódu nenalezeno (`asset_sources.yaml`); technické údaje doplní kód, ne karta._

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 8 variant v `Content/Skvt/Lapikus/Ruin/Stones/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
