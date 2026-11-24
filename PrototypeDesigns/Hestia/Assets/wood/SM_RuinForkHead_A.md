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
aliases: ["SM_RuinForkHead"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Vez_Pristresek]]", "[[Palac_Kovarna]]", "[[Palac_Obydli]]", "[[Nadvori_Stan]]"]
envelope: [45, 30, 12]
stand_in: none
asset_source: tools/meshes/mesh_log.py:make_fork
ue_path: /Game/Skvt/Lapikus/Ruin/Wood/SM_RuinForkHead_A
variants: [SM_RuinForkHead_B]
---
# SM_RuinForkHead_A

## Účel a použití
Hlava rozsochy s kůrou (vidlice), nasadí se na kůl `SM_RuinLogBark` nebo `SM_RuinPoleBark` (kůly přístřešku věže, vidlice žlabů, stříška stanu).

Osy: délka podél X (nominál 45,0 cm, délka a průměr přes scale); kmen na −X, vidlice na +X, ramena v rovině XY; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Kulatina_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 45 × 30 × 12 cm; `envelope` 45 × 30 × 12 cm: vejde se
- Varianty: `SM_RuinForkHead_A`, `SM_RuinForkHead_B`
- Sloty: ['wood', 'endgrain', 'bark']
- Verze: 1 (prefix `SM_RuinForkHead`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Wood/SM_RuinForkHead_A.SM_RuinForkHead_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:201`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 2 variant v `Content/Skvt/Lapikus/Ruin/Wood/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 2.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
