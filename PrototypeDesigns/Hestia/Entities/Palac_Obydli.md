---
# orchestrace
type: entity
updated: 2026-11-23
aliases: []
# hra
kind: structure
parent: "[[Palac]]"
located_in: []
derived_from:
alternative_to: []
pattern:
status: in_progress
# depth_<domain> / target_<domain>: očekávané domény podle kind (01, kap. 8), jiné jen když se řeší
# depth_* = realizace (Unreal, data, StateTree); hloubka návrhu se počítá z dokumentů (01, kap. 5)
# target_mode_<domain>: design | build, jen při odchylce od výchozího režimu domény
ue_path:
assets: []
depth_structures: 3
target_structures: 4
target_gameplay: 3
---
# Palac_Obydli

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 4 | 3 | 4 | build | −1 |
| gameplay | – | – | 3 | design | −3 |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[navrh_palac_obydli_etapy]] – design, depth 4, valid, in_progress
- [[navrh_palac_obydli_pec]] – design, depth 4, valid, in_progress
- [[navrh_palac_obydli_stavenisko]] – design, depth 4, valid, in_progress
- [[navrh_palac_obydli_stred]] – design, depth 4, valid, in_progress
- [[stav_palac_obydli]] – state, depth 3, valid
- nahrazené nebo archivované: 1

**Aktivní předání**
- [[predani_palac_obydli_1_etapa1_ue]]
- [[predani_palac_obydli_2_krytina]]
- [[predani_palac_obydli_3_strop]]
- [[predani_palac_obydli_4_podlaha]]
- [[predani_palac_obydli_5_okap]]
- [[predani_palac_obydli_6_zarubne]]
- [[predani_palac_obydli_7_vybaveni]]

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[05_constructions]] | `Palac_Obydli.py`, `Palac_Obydli_Kamen.py`, `Palac_Obydli_Krov.py`, `Palac_Obydli_Ohniste.py`, `Palac_Obydli_Srub.py`, `Palac_Obydli_Stavenisko.py`, `Palac_Obydli_Stavenisko_Capture.py` | [[navrh_palac_obydli_etapy]], [[navrh_palac_obydli_pec]], [[navrh_palac_obydli_stavenisko]], [[navrh_palac_obydli_stred]], [[stav_palac_obydli]] |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Kamen.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Krov.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Ohniste.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Srub.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Stavenisko.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Stavenisko_Capture.py` | entry | 05_constructions | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-23 · `Maintenance/reports/ue_Palac_Obydli.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 29 vlastních
- Třídy: StaticMesh 12, ISM 17 (598 instancí), Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 0 (vynecháno podle `placeholder_ignore`: 6); výchozí materiály: 0
- Fáze: base 12, final 7, site 10
- Rozsah: 1554 × 1832 × 541 cm
- Kořen daleko od geometrie (`pivot_far`, víc než 500 cm): 12 actorů; informace pro modelování v instanci, ne nález
- Pro srovnání `depth_*`: structures 3; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Assety
<!-- hestia:generated:start -->

Souhrn: requested 5, in_progress 5, generated 0, imported 36, verified 0 · graybox 0 · outdated v UE 0 (signál vedle `depth_*`, hloubka se z něj nepočítá)

| Asset | Stav | Náhrada v levelu |
|---|---|---|
| [[MI_RuinRammedEarth]] | requested | none |
| [[MI_RuinSoot]] | requested | none |
| [[MI_RuinWoodChips]] | requested | none |
| [[SM_RuinDrawknife_A]] | requested | none |
| [[SM_RuinEarthPile_A]] | requested | none |
| [[MI_RuinWood]] | in_progress | none |
| [[SM_RuinLogPeeling_A]] | in_progress | none |
| [[SM_RuinOvenDome_A]] | in_progress | none |
| [[SM_RuinOvenDoor_A]] | in_progress | none |
| [[SM_RuinPost_A]] | in_progress | none |
| [[MI_RuinBark]] | imported | none |
| [[MI_RuinChinking]] | imported | none |
| [[MI_RuinDaub]] | imported | none |
| [[MI_RuinIron]] | imported | none |
| [[MI_RuinIronClean]] | imported | none |
| [[MI_RuinStraw]] | imported | none |
| [[MI_RuinWattle]] | imported | none |
| [[MI_RuinWood_EndGrain]] | imported | none |
| [[MI_RuinWool]] | imported | none |
| [[SM_RuinAxe_A]] | imported | none |
| [[SM_RuinBarkStrip_A]] | imported | none |
| [[SM_RuinBarrel_A]] | imported | none |
| [[SM_RuinBasket_A]] | imported | none |
| [[SM_RuinBed_A]] | imported | none |
| [[SM_RuinBroadaxe_A]] | imported | none |
| [[SM_RuinChest_A]] | imported | none |
| [[SM_RuinChimney_A]] | imported | none |
| [[SM_RuinCrosscutSaw_A]] | imported | none |
| [[SM_RuinDoor_A]] | imported | none |
| [[SM_RuinForkHead_A]] | imported | none |
| [[SM_RuinGutterBark_A]] | imported | none |
| [[SM_RuinGutter_A]] | imported | none |
| [[SM_RuinLadder_A]] | imported | none |
| [[SM_RuinLogBark_A]] | imported | none |
| [[SM_RuinLog_A]] | imported | none |
| [[SM_RuinMallet_A]] | imported | none |
| [[SM_RuinNailHammer_A]] | imported | none |
| [[SM_RuinPlank_A]] | imported | none |
| [[SM_RuinPoleBark_A]] | imported | none |
| [[SM_RuinShelf_A]] | imported | none |
| [[SM_RuinShutter_A]] | imported | none |
| [[SM_RuinSmokeHood_A]] | imported | none |
| [[SM_RuinTable_A]] | imported | none |
| [[SM_RuinTimber_A]] | imported | none |
| [[SM_RuinWoodpile_A]] | imported | none |
| [[SM_RuinWorkbench_A]] | imported | none |

<!-- hestia:generated:end -->
## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta T-0008 (–, [[navrh_palac_obydli_stred]]): kap. 0.5–0.6 (postavené) se překrývá se [[stav_palac_obydli]]: sjednotit (B4)
- Fronta F-0033 (G3, [[Palac_Obydli]]): bez dokumentu v doméně gameplay (target_gameplay 3)
- Fronta T-0037 (role:Builder, [[Palac_Obydli]]): Hromada kamene (asi 1 m³ z kamenů zříceniny, [[SM_RuinStone_R12_A]]) na staveništi etapy 1; hromada hlíny a třísky jsou karty požadavků [[SM_RuinEarthPile_A]], [[MI_RuinWoodChips]] (doklad: [[CHECKLIST_assets_navrhy]] kap. 6.3, 11.3 „zatím ne“; [[navrh_palac_obydli_stavenisko]])

<!-- hestia:generated:end -->

## Historie a rozhodnutí
