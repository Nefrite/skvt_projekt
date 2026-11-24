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
aliases: ["SM_RuinPoleBark"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Vez_Pristresek]]", "[[Brana_Straz]]", "[[Palac_Obydli]]", "[[Nadvori_Stan]]"]
envelope: [100, 8, 8]
stand_in: none
asset_source: tools/meshes/mesh_log.py:make_pole
ue_path: /Game/Skvt/Lapikus/Ruin/Wood/SM_RuinPoleBark_A
variants: [SM_RuinPoleBark_B, SM_RuinPoleBark_C]
---
# SM_RuinPoleBark_A

## Účel a použití
Tenká tyč s kůrou (krokvové tyče, vzpěry, ráhna, krokvičky, přítlačné tyče, stojky stanu, kozy a vzpěry staveniště).

Osy: délka podél X (nominál 100,0 cm, délka a průměr přes scale); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Kulatina_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 100 × 8 × 8 cm; `envelope` 100 × 8 × 8 cm: vejde se
- Varianty: `SM_RuinPoleBark_A`, `SM_RuinPoleBark_B`, `SM_RuinPoleBark_C`
- Sloty: ['wood', 'endgrain', 'bark']
- Verze: 1 (prefix `SM_RuinPole`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Wood/SM_RuinPoleBark_A.SM_RuinPoleBark_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:198`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 3 variant v `Content/Skvt/Lapikus/Ruin/Wood/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 2.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
