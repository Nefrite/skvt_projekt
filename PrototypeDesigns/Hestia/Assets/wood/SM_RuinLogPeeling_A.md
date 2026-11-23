---
# orchestrace
type: asset
asset_status: in_progress
requested_by: Builder
requested: 2026-11-14
owner: Builder
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: ["SM_RuinLogPeeling"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Palac_Obydli]]"]
envelope: [100, 20, 20]
stand_in: none
asset_source: tools/meshes/mesh_log.py:make_log_peeling
ue_path: 
variants: [SM_RuinLogPeeling_B]
---
# SM_RuinLogPeeling_A

## Účel a použití
Rozpracovaná kulatina na kozách: nahoře (+Z) z části oloupaná (staveniště domu, etapa 1).

Osy: délka podél X (nominál 100,0 cm, délka a průměr přes scale); oloupaná strana nahoře (+Z, roll 0); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/wood/`): 100,0 × 20,0 × 20,0 cm
- varianty v UE: `SM_RuinLogPeeling_A`, `SM_RuinLogPeeling_B`
- sloty: `wood`, `endgrain`, `bark`
- verze: `STONE_MESH_VERSION["SM_RuinLogPeeling"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 2 variant v `Content/Skvt/Lapikus/Ruin/Wood/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 2.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Builder. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
- Asset je vyrobený a `.uasset` existuje, karta ale nemá vlastní náhled (podmínka stavu `generated`, 07 kap. 20): zůstává `in_progress`, dokud Builder nedoplní náhled a nenastaví `imported`.
