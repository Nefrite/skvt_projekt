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
aliases: ["SM_RuinArmorStand"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Guesthouse]]"]
envelope: [61, 61, 175]
stand_in: none
asset_source: tools/meshes/mesh_props.py:armor_stand
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinArmorStand_A
variants: []
---
# SM_RuinArmorStand_A

## Účel a použití
Stojan na brnění v Guesthouse (graybox `GH_ARMOR`, u hradby na severozápadě), zatím prázdný; varianta A (Jirka 22. 11. 2026); `shape: armor_stand`, `finish: oil`. Brnění = samostatný mesh posazený na body stojanu.

Osy: **čelo −Y** (zády ke zdi), kolík na rukavice +X; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Guesthouse_stojan_brneni_nahled.png)

## Požadavek

## Na míru
Body pro brnění `mesh_props.ARMOR_STAND_POINTS` v cm od podlahy, osa sloupku x = y = 0: hlava 167, ramena 150, pás 105, kolík (10; 0; 126). V lokálních osách meshe (pivot ve středu) je od výšek odečíst 87,3 cm.

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 60.1 × 60.3 × 175 cm; `envelope` 61 × 61 × 175 cm: vejde se
- Varianty: `SM_RuinArmorStand_A`
- Sloty: ['wood', 'endgrain']
- Výchozí materiál: `wood`
- Verze: 3 (prefix `SM_RuinArmorStand`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinArmorStand_A.SM_RuinArmorStand_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:277`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinArmorStand_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinArmorStand_A.SM_RuinArmorStand_A`) · `RuinStoneVersion` 3 (kód 3) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Konstrukce: kříž noh 60 × 60 z přeplátovaných trámků se vzpěrami a patkou, sloupek 9 × 9, klenuté ramenní jařmo 46 cm se dvěma vzpěrami (unese plátovou zbroj), pásová příčka 34 cm, krček a ručně točená hlavice; léta podél délky všech dílů (`grain="long"`).
- Jařmo opravené ve verzi 2 (screenshot 22. 11. 2026); léta sloupku napříč (verze 2) opravena ve verzi 3.
- Převedeno z [[Katalog_props]] a [[CHECKLIST_assets_navrhy]] kap. 6.8 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
