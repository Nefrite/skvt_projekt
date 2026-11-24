---
# orchestrace
type: entity
updated: 2026-11-24
aliases: []
# hra
kind: structure
parent: "[[Lapikus]]"
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
depth_structures: 4
target_structures: 4
target_gameplay: 0
---
# Vez

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | 3 | 4 | 4 | build | ✔ |
| gameplay | – | – | 0 | design | ✔ |

Zralost podstromu (jednotky s vlastním cílem včetně této entity, 04 kap. 3):

| Doména | Zralost | Nejslabší článek |
|---|---|---|
| structures | 100 % (2 z 2) | 4 – [[Vez]] |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[navrh_vez_skody]] – design, depth 3, valid, in_progress

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[03_ruin]] | – | [[navrh_vez_skody]] |
| [[05_constructions]] | `Vez.py`, `Vez_Patra.py`, `vez.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez_Patra.py` | entry | 05_constructions | name |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/vez.py` | library | 05_constructions | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-23 · `Maintenance/reports/ue_Vez.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 21 vlastních, 16 za potomky (Vez_Pristresek)
- Třídy: StaticMesh 0, ISM 21 (8433 instancí), Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 0 (vynecháno podle `placeholder_ignore`: 4); výchozí materiály: 0
- Fáze: –
- Rozsah: 1618 × 1618 × 1575 cm
- Kořen daleko od geometrie (`pivot_far`, víc než 500 cm): 21 actorů; informace pro modelování v instanci, ne nález
- Pro srovnání `depth_*`: structures 4; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

_Žádné otevřené otázky z dokumentů, fronty ani scratch._

<!-- hestia:generated:end -->

## Historie a rozhodnutí
