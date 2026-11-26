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
aliases: ["SM_RuinNailHammer"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Obydli]]"]
envelope: [3, 34, 11]
stand_in: none
asset_source: tools/meshes/mesh_props.py:nail_hammer
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinNailHammer_A
variants: []
---
# SM_RuinNailHammer_A

## Účel a použití
Kladivo na hřebíky s drápákem (staveniště).

Osy: nejdelší rozměr podél Y (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 3 × 34 × 10.5 cm; `envelope` 3 × 34 × 11 cm: vejde se
- Varianty: `SM_RuinNailHammer_A`
- Sloty: ['wood', 'endgrain', 'ironclean']
- Výchozí materiál: `wood`
- Verze: 3 (prefix `SM_RuinNailHammer`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinNailHammer_A.SM_RuinNailHammer_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:258`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinNailHammer_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinNailHammer_A.SM_RuinNailHammer_A`) · `RuinStoneVersion` 3 (kód 3) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.3 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
