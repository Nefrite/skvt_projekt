---
# orchestrace
type: asset
asset_status: imported
requested_by: Builder
requested: 2026-11-14
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: ["SM_RuinChimney"]
# hra
asset_kind: mesh
asset_category: wattle
used_by: ["[[Palac_Kovarna]]", "[[Palac_Obydli]]", "[[Guesthouse]]"]
envelope: [60, 60, 100]
stand_in: none
asset_source: tools/meshes/mesh_wattle.py:make_tube
ue_path: /Game/Skvt/Lapikus/Ruin/Wattle/SM_RuinChimney_A
variants: [SM_RuinChimney_B]
---
# SM_RuinChimney_A

## Účel a použití
Komín z proutí a hlíny 60 × 60 cm, výška 100 cm (škáluje se na výšku), stěna 6 cm, mírně se zužuje.

Osy: osa komína Z (nahoru); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Knihovna_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 60 × 60 × 100 cm; `envelope` 60 × 60 × 100 cm: vejde se
- Varianty: `SM_RuinChimney_A`, `SM_RuinChimney_B`
- Sloty: ['daub', 'wattle']
- Výchozí materiál: `daub`
- Verze: 1 (prefix `SM_RuinChimney`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Wattle/SM_RuinChimney_A.SM_RuinChimney_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:228`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinChimney_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Wattle/SM_RuinChimney_A.SM_RuinChimney_A`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current
- `SM_RuinChimney_B` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Wattle/SM_RuinChimney_B.SM_RuinChimney_B`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
