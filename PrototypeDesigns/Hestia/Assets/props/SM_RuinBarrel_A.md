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
aliases: ["SM_RuinBarrel"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]", "[[Palac_Obydli]]"]
envelope: [62, 62, 81]
stand_in: none
asset_source: tools/meshes/mesh_props.py:barrel
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinBarrel_A
variants: []
---
# SM_RuinBarrel_A

## Účel a použití
Kalicí sud s vodou (Ø 0,6 m, výška 0,8 m), dužiny a obruče; i sud pod okapem domu a kovárny.

Osy: nejdelší rozměr podél Z (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 61.3 × 61.2 × 80.3 cm; `envelope` 62 × 62 × 81 cm: vejde se
- Varianty: `SM_RuinBarrel_A`
- Sloty: ['wood', 'endgrain', 'iron', 'water']
- Výchozí materiál: `wood`
- Verze: 3 (prefix `SM_RuinBarrel`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinBarrel_A.SM_RuinBarrel_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:242`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinBarrel_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinBarrel_A.SM_RuinBarrel_A`) · `RuinStoneVersion` 3 (kód 3) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
