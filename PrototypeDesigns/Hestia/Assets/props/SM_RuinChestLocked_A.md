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
aliases: ["SM_RuinChestLocked"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Guesthouse]]"]
envelope: [95, 55, 51]
stand_in: none
asset_source: tools/meshes/mesh_props.py:chest_locked
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinChestLocked_A
variants: []
---
# SM_RuinChestLocked_A

## Účel a použití
Kovaná truhla na cennosti hosta se zámkem (graybox `GH_CHEST`), v nohách postele, zámkem k severu; `shape: chest_locked`, `finish: oil`.

Osy: **zámek a závěra −Y**, pásové závěsy +Y, držadla s kruhy ±X, delší strana X; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Guesthouse_truhla_nahled.png)

## Požadavek

## Na míru

## Z kódu
Ručně do etapy B (P20, `asset_sources.yaml`), stav kódu 2026-11-23:
- rozměr (bounding box OBJ `meshes/props/`): 94,2 × 54,2 × 50,7 cm
- varianty v UE: `SM_RuinChestLocked_A`
- sloty: `wood`, `endgrain`, `ironclean`; výchozí materiál dílce `wood`
- verze: `STONE_MESH_VERSION["SM_RuinChestLocked"]` = 1; `MESH_AXES` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Props/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Konstrukce: hoblovaná prkna na soklu, klenuté víko, černé kování bez rzi (`IronClean`): rohovníky, 2 svislé pásy přes korpus a víko, vodorovný pás, nýty, zámková deska s klíčovou dírkou.
- Převedeno z [[Katalog_props]] a [[CHECKLIST_assets_navrhy]] kap. 6.8 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
