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
aliases: ["SM_RuinShelf"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Palac_Obydli]]"]
envelope: [101, 28, 90]
stand_in: none
asset_source: tools/meshes/mesh_props.py:shelf
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinShelf_A
variants: []
---
# SM_RuinShelf_A

## Účel a použití
Police na osobní věci (1,0 × 0,28 × 0,9 m).

Osy: nejdelší rozměr podél X (podle rozměru meshe); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Props_kovarna_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 100.2 × 27.7 × 89.6 cm; `envelope` 101 × 28 × 90 cm: vejde se
- Varianty: `SM_RuinShelf_A`
- Sloty: ['wood']
- Výchozí materiál: `wood`
- Verze: 1 (prefix `SM_RuinShelf`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinShelf_A.SM_RuinShelf_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:265`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinShelf_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinShelf_A.SM_RuinShelf_A`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 6.2 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
