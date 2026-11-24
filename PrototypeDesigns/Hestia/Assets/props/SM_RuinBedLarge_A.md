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
aliases: ["SM_RuinBedLarge"]
# hra
asset_kind: mesh
asset_category: props
used_by: ["[[Guesthouse]]"]
envelope: [251, 110, 95]
stand_in: none
asset_source: tools/meshes/mesh_props.py:bed_large
ue_path: /Game/Skvt/Lapikus/Ruin/Props/SM_RuinBedLarge_A
variants: []
---
# SM_RuinBedLarge_A

## Účel a použití
Pohodlná postel hosta v Guesthouse (graybox `GH_BED` 2,50 × 1,09 m, ověřený s postavou 180 cm); `shape: bed_large`, `finish: oil`. Kvalitnější nábytek než v domě, ručně a hrubě opracovaný (Jirka 22. 11. 2026). Rozmístěna 22. 11. 2026 místo grayboxu, hlava u jižního rohu (s = 1,85), nohy k truhle.

Osy: X podél postele, **hlava −X** (čelo 95 cm), nohy +X; pivot ve středu bounding boxu. Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/05_constructions/Guesthouse_postel_nahled.png)

## Požadavek

## Na míru

## Z kódu
<!-- hestia:generated:start -->

<!-- hestia:asset_code -->
- Rozměr (skutečný): 250.2 × 109.1 × 95 cm; `envelope` 251 × 110 × 95 cm: vejde se
- Varianty: `SM_RuinBedLarge_A`
- Sloty: ['wood', 'wool', 'canvas']
- Výchozí materiál: `wood`
- Verze: 2 (prefix `SM_RuinBedLarge`, `RuinStoneVersion`)
- Globální verze: `MESH_AXES` 10
- `ue_path` (odvozená): `/Game/Skvt/Lapikus/Ruin/Props/SM_RuinBedLarge_A.SM_RuinBedLarge_A`
- `.uasset` na disku: ano
- Zdroj: `PrototypeDesigns/Lapikus/zrlib/config.py:274`
- Data: `PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` ([[Lapikus]])

<!-- hestia:generated:end -->

## Stav v UE
<!-- hestia:generated:start -->

<!-- hestia:asset_ue -->
Čtení z UE: `Maintenance/reports/ue_assets.json` · etapa 1 (skript v editoru) (datum čtení u každého assetu)

- `SM_RuinBedLarge_A` (čteno 2026-11-23): v UE ano (`/Game/Skvt/Lapikus/Ruin/Props/SM_RuinBedLarge_A.SM_RuinBedLarge_A`) · `RuinStoneVersion` 2 (kód 2) · `RuinMeshAxes` 10 (`MESH_AXES` 10) · current

<!-- hestia:generated:end -->

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Konstrukce: sloupky 9 × 9 se zkosenými hranami a hlavicí; čelo v hlavě 95 cm (rám, vložená deska, římsa), čelo v nohách 62 cm; bočnice 16 cm, lišty, 9 laťek; slamník 20 cm a polštář v lněném potahu (`Canvas`), houně přes bočnice. Nižší čelo = parametr `head_h`.
- Funkční: ložná plocha 55 cm nad podlahou, bočnice nahoře 46 cm.
- Verze 2: sloupky a hlavice s léty svisle (`grain="long"`), ostatní díly zatím původní UV (T-0024, *Změny konvence* v [[Konvence_assetu]]).
- Graybox `GH_BED` měl výšku 0,62 m; mesh je vyšší jen čelem v hlavě (95 cm) ❓ (z katalogu).
- Převedeno z [[Katalog_props]] a [[CHECKLIST_assets_navrhy]] kap. 6.8 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
