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
aliases: ["SM_RuinBarkStrip"]
# hra
asset_kind: mesh
asset_category: wood
used_by: ["[[Brana_Straz]]", "[[Nadvori_Stan]]", "[[Palac_Obydli]]"]
envelope: [160, 70, 9]
stand_in: none
asset_source: tools/meshes/mesh_bark.py:make_strip
ue_path: /Game/Skvt/Lapikus/Ruin/Wood/SM_RuinBarkStrip_A
variants: [SM_RuinBarkStrip_B, SM_RuinBarkStrip_C]
---
# SM_RuinBarkStrip_A

## Účel a použití
Prohnutý pás smrkové kůry 160 × 70 cm, hrubá strana nahoru, roztřepené okraje, spodek světlé lýko (přístřešek brány, stříška stanu, pruhy kůry na staveništi).

Osy: délka X, šířka Y, prohnutí nahoru (+Z); pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Knihovna_meshe_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 160 × 70 × 9 cm; `envelope` 160 × 70 × 9 cm: vejde se
- Varianty: `SM_RuinBarkStrip_A`, `SM_RuinBarkStrip_B`, `SM_RuinBarkStrip_C`
- Sloty: ['bark', 'endgrain']
- Výchozí materiál: `bark`
- Verze: 1 (prefix `SM_RuinBarkStrip`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Wood/SM_RuinBarkStrip_A.SM_RuinBarkStrip_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:226`
- Data: `PrototypeDesigns/Lapikus/05_constructions/constructions.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinBarkStrip_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Wood/SM_RuinBarkStrip_A.SM_RuinBarkStrip_A`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current
- `SM_RuinBarkStrip_B` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Wood/SM_RuinBarkStrip_B.SM_RuinBarkStrip_B`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current
- `SM_RuinBarkStrip_C` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Wood/SM_RuinBarkStrip_C.SM_RuinBarkStrip_C`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 4 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
