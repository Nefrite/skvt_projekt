---
# orchestrace
type: asset
asset_status: imported
requested_by: Builder
requested: 2026-11-14
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: ["SM_RuinBarkStrip"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Brana_Straz]]", "[[Nadvori_Stan]]", "[[Palac_Obydli]]"]
envelope: [160, 70, 9]
stand_in: none
asset_source: tools/meshes/mesh_bark.py:make_strip
ue_path: /Game/Skvt/Lapikus/Ruin/Wood/SM_RuinBarkStrip_A
variants: [SM_RuinBarkStrip_B, SM_RuinBarkStrip_C]
---
# SM_RuinBarkStrip_A

## Účel a použití
Prohnutý pás smrkové kůry 160 × 70 cm, hrubá strana nahoru, roztřepené okraje, spodek světlé lýko (přístřešek brány, stříška stanu, pruhy kůry na staveništi).

Osy: délka X, šířka Y, prohnutí nahoru (+Z); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Knihovna_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/wood/`): 160,0 × 70,0 × 9,0 cm
- varianty v UE: `SM_RuinBarkStrip_A`, `SM_RuinBarkStrip_B`, `SM_RuinBarkStrip_C`
- sloty: `bark`, `endgrain`; výchozí materiál dílce `bark`
- verze: `STONE_MESH_VERSION["SM_RuinBarkStrip"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 3 variant v `Content/Skvt/Lapikus/Ruin/Wood/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
