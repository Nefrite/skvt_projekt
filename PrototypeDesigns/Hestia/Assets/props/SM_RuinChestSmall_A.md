---
# orchestrace
type: asset
asset_status: imported
requested_by: legacy
requested:
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-24
aliases: ["SM_RuinChestSmall"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Nadvori_Stan]]"]
envelope: [60, 38, 32]
stand_in: none
asset_source: tools/meshes/mesh_props.py:chest_small
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinChestSmall_A
variants: []
---
# SM_RuinChestSmall_A

## Účel a použití
Truhlička ve stanu (korpus 55 × 35 × 32 cm, s držadly 59,3 cm), 2 železné pásy; `shape: chest_small`, `finish: raw`. Leží vedle lůžka u hlavy, zámkem do uličky.

Osy: **zámek (oko na zámek) −Y**, držadla ±X; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Stan_truhlicka_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 59.3 × 38 × 31.7 cm; `envelope` 60 × 38 × 32 cm: vejde se
- Varianty: `SM_RuinChestSmall_A`
- Sloty: ['wood', 'iron']
- Výchozí materiál: `wood`
- Verze: 1 (prefix `SM_RuinChestSmall`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinChestSmall_A.SM_RuinChestSmall_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:272`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinChestSmall_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinChestSmall_A.SM_RuinChestSmall_A`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Železo s patinou rzi (`Iron`).
- Převedeno z [[Katalog_props]] a [[CHECKLIST_assets_navrhy]] kap. 6.5 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
