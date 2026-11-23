---
# orchestrace
type: asset
asset_status: imported
requested_by: Furnisher
requested: 2026-11-21
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: ["SM_RuinBundle"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Nadvori_Stan]]"]
envelope: [76, 44, 23]
stand_in: none
asset_source: tools/meshes/mesh_props.py:bundle
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinBundle_A
variants: []
---
# SM_RuinBundle_A

## Účel a použití
Vak (ranec) z plátna ležící na boku, pohozený o kus vedle lůžka; vak asi 62 × Ø 30 cm, popruh přes rameno; `shape: bundle`, materiál pevný (`MI_RuinSackcloth`: zažloutlé plátno, hustší skvrny, zaprášený vršek; Jirka 22. 11. 2026).

Osy: **dno −X, hrdlo +X** (stažené dvěma závity lana, roztřepený okraj), popruh leží volně na zemi na straně +Y; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Stan_vak_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/props/`): 76,0 × 43,4 × 22,5 cm
- varianty v UE: `SM_RuinBundle_A`
- sloty: `rope`, `sackcloth`; výchozí materiál dílce `sackcloth`
- verze: `STONE_MESH_VERSION["SM_RuinBundle"]` = 2; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Pomocná funkce `_rope` (lano podél křivky, prameny jako `SM_RuinRope`).
- Převedeno z [[Katalog_props]] a [[CHECKLIST_assets_navrhy]] kap. 6.5 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
