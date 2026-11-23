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
aliases: ["SM_RuinCampBed"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Nadvori_Stan]]"]
envelope: [200, 77, 33]
stand_in: none
asset_source: tools/meshes/mesh_props.py:camp_bed (folded=False/True)
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinCampBed_A
variants: [SM_RuinCampBedFolded_A]
---
# SM_RuinCampBed_A

## Účel a použití
Lůžko ve stanu z klád a tyčí, výplň sláma a houně; `SM_RuinCampBed_A` houně přes slámu (`shape: camp_bed`), tvarová varianta `SM_RuinCampBedFolded_A` houně složená v nohách (`camp_bed_folded`); `finish: raw`. Ve stanu jedno lůžko na straně zavřené chlopně, hlavou k zadnímu štítu, vnější okraj asi 0,9 m od osy stanu (plachta tam 35 cm nad zemí).

Osy: X podél lůžka, **hlava −X**; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Stan_luzko_nahled.png)
![Náhled varianty](../../../Lapikus/05_constructions/Stan_luzko_slozena_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 198.8 × 76.2 × 28.8 cm; `envelope` 200 × 77 × 33 cm: vejde se
- Varianty: `SM_RuinCampBed_A`, `SM_RuinCampBedFolded_A`
- Sloty: ['wood', 'endgrain', 'bark', 'straw', 'wool']
- Výchozí materiál: `wood`
- Verze: 1 (prefix `SM_RuinCampBed`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinCampBed_A.SM_RuinCampBed_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:269`
- Data: bez výskytu

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinCampBed_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinCampBed_A.SM_RuinCampBed_A`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current
- `SM_RuinCampBedFolded_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinCampBedFolded_A.SM_RuinCampBedFolded_A`) · `RuinStoneVersion` 1 (kód 1) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Konstrukce: 2 příčné klády s kůrou Ø 15 × 75 cm (26 a 24 cm od konců), 10 tyčí s kůrou Ø 5 × 200 cm, sláma (pod hlavou o 3 cm víc), houně s převisem 10 cm; pomocná funkce `_pole`.
- Funkční: vrch slámy asi 25 cm nad zemí.
- Převedeno z [[Katalog_props]] a [[CHECKLIST_assets_navrhy]] kap. 6.5 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
