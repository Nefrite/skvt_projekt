---
# orchestrace
type: entity
updated: 2026-11-19
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
---
# Palac_Obydli

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 4 | 3 | – | build | bez cíle |
| gameplay | – | – | – | design | bez cíle |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[navrh_palac_obydli]] – design, depth 2, valid, rejected
- [[navrh_palac_obydli_stavenisko]] – design, depth 4, valid, in_progress
- [[navrh_palac_obydli_stred]] – design, depth 4, valid, in_progress
- [[stav_palac_obydli]] – state, depth 3, valid

**Aktivní předání**
- [[predani_palac_obydli_stavitel]]

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[05_constructions]] | `Palac_Obydli.py`, `Palac_Obydli_Kamen.py`, `Palac_Obydli_Krov.py`, `Palac_Obydli_Ohniste.py`, `Palac_Obydli_Srub.py`, `Palac_Obydli_Stavenisko.py`, `Palac_Obydli_Stavenisko_Capture.py` | [[navrh_palac_obydli_stavenisko]], [[navrh_palac_obydli_stred]], [[stav_palac_obydli]] |

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

Poslední čtení: 2026-11-21 · `Maintenance/reports/ue_Palac_Obydli.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 18 vlastních
- Třídy: StaticMesh 7, Blueprint 0, BSP 0, ostatní 11
- Zástupné meshe (`/Engine/BasicShapes/`): 5; výchozí materiály: 0
- Fáze: base 12, final 6
- Rozsah: 1641 × 1312 × 3787 cm
- Pro srovnání `depth_*`: structures 3; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta F-0018 (G2, [[Palac_Obydli]]): očekávaná doména gameplay (kind structure) bez target_gameplay; očekávaná doména structures (kind structure) bez target_structures
- Fronta T-0008 (–, [[navrh_palac_obydli_stred]]): kap. 0.5–0.6 (postavené) se překrývá se [[stav_palac_obydli]]: sjednotit (B4)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
