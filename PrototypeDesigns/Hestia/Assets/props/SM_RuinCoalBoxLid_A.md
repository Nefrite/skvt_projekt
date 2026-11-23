---
# orchestrace
type: asset
asset_status: imported
requested_by: Furnisher
requested: 2026-11-14
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: ["SM_RuinCoalBoxLid"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]"]
envelope: [81, 121, 11]
stand_in: none
asset_source: tools/meshes/mesh_props.py:box_lid
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinCoalBoxLid_A
variants: []
---
# SM_RuinCoalBoxLid_A

## Účel a použití
Volné víko truhlíku (bez pantů, pokládá se bokem).

Osy: nejdelší rozměr podél Y (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 80.1 × 120.3 × 10.6 cm; `envelope` 81 × 121 × 11 cm: vejde se
- Varianty: `SM_RuinCoalBoxLid_A`
- Sloty: ['wood']
- Výchozí materiál: `wood`
- Verze: 2 (prefix `SM_RuinCoalBoxLid`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinCoalBoxLid_A.SM_RuinCoalBoxLid_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:255`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinCoalBoxLid_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinCoalBoxLid_A.SM_RuinCoalBoxLid_A`) · `RuinStoneVersion` 4 (kód 2) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
