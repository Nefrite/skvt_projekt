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
aliases: ["SM_RuinGrindstoneTreadle"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Kovarna_Vybaveni]]"]
envelope: [120, 86, 106]
stand_in: none
asset_source: tools/meshes/mesh_props.py:grindstone (treadle=True)
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinGrindstoneTreadle_A
variants: []
---
# SM_RuinGrindstoneTreadle_A

## Účel a použití
Šlapací brus: kotouč Ø 0,7 m na rámu 1,2 × 0,6 m, osa 0,75 m, kliková páka, ojnice, šlapadlo, korýtko (Jirka 14. 11. 2026).

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 120 × 86 × 105.3 cm; `envelope` 120 × 86 × 106 cm: vejde se
- Varianty: `SM_RuinGrindstoneTreadle_A`
- Sloty: ['wood', 'endgrain', 'iron', 'sandstone', 'water']
- Výchozí materiál: `wood`
- Verze: 2 (prefix `SM_RuinGrindstoneTreadle`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinGrindstoneTreadle_A.SM_RuinGrindstoneTreadle_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:253`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinGrindstoneTreadle_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinGrindstoneTreadle_A.SM_RuinGrindstoneTreadle_A`) · `RuinStoneVersion` 6 (kód 2) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.1 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
