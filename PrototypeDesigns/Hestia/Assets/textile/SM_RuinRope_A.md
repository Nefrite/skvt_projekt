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
aliases: ["SM_RuinRope"]
# hra
asset_kind: mesh
asset_category: textile
used_by: ["[[Vez_Pristresek]]", "[[Nadvori_Stan]]"]
envelope: [100, 2, 2]
stand_in: none
asset_source: tools/meshes/mesh_textile.py:make_rope
ue_path: /Game/Skvt/Lapikus/Ruin/Textile/SM_RuinRope_A
variants: [SM_RuinRope_B]
---
# SM_RuinRope_A

## Účel a použití
Článek konopného lana 100 cm, Ø 1,5 cm, 3 prameny; prověšené lano = řetěz článků podél řetězovky (počítá stavba): bouřková lana věže, vazby hřebene, šňůry stanu.

Osy: délka X; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Knihovna_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 100 × 1.5 × 1.5 cm; `envelope` 100 × 2 × 2 cm: vejde se
- Varianty: `SM_RuinRope_A`, `SM_RuinRope_B`
- Sloty: ['rope']
- Výchozí materiál: `rope`
- Verze: 1 (prefix `SM_RuinRope`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Textile/SM_RuinRope_A.SM_RuinRope_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:230`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 2 variant v `Content/Skvt/Lapikus/Ruin/Textile/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
