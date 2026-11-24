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
aliases: ["SM_RuinPole"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Palac_Kovarna]]", "[[Brana_Straz]]", "[[Nadvori_Stan]]"]
envelope: [100, 8, 8]
stand_in: none
asset_source: tools/meshes/mesh_log.py:make_pole
ue_path: /Game/Skvt/Lapikus/Ruin/Wood/SM_RuinPole_A
variants: [SM_RuinPole_B, SM_RuinPole_C]
---
# SM_RuinPole_A

## Účel a použití
Loupaná tenká tyč s výraznějším prohnutím (zábradlí, páka měchů, kolíky).

Osy: délka podél X (nominál 100,0 cm, délka a průměr přes scale); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Kulatina_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 100 × 8 × 8 cm; `envelope` 100 × 8 × 8 cm: vejde se
- Varianty: `SM_RuinPole_A`, `SM_RuinPole_B`, `SM_RuinPole_C`
- Sloty: ['wood', 'endgrain']
- Verze: 1 (prefix `SM_RuinPole`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Wood/SM_RuinPole_A.SM_RuinPole_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:197`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 3 variant v `Content/Skvt/Lapikus/Ruin/Wood/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 2.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
