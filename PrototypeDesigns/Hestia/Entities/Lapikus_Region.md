---
# orchestrace
type: entity
updated: 2026-11-24
aliases: []
# hra
kind: place          # place|location|district|plot|structure|room|character|object|route|system|group
parent:              # "[[Parent]]" ; u kořene prázdné
located_in: []       # prázdné = zdědí od parent
derived_from:
alternative_to: []
pattern:
status: in_progress
# depth_<domain> / target_<domain>: očekávané domény podle kind (01, kap. 8), jiné jen když se řeší
# depth_* = realizace (Unreal, data, StateTree); hloubka návrhu se počítá z dokumentů (01, kap. 5)
# target_mode_<domain>: design | build, jen při odchylce od výchozího režimu domény
ue_path:
assets: []
scale: cutout
depth_narrative: 0
target_narrative: 1
depth_environment: 4
target_environment: 4
---
# Lapikus_Region

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| environment | 3 | 4 | 4 | build | ✔ |
| paths | – | – | – | build | bez cíle |
| narrative | – | 0 | 1 | design | −1 |

Zralost podstromu (jednotky s vlastním cílem včetně této entity, 04 kap. 3):

| Doména | Zralost | Nejslabší článek |
|---|---|---|
| environment | 33 % (1 z 3) | 1 – [[Les_Lapikus]] |
| structures | 83 % (10 z 12) | 3 – [[Brana_Straz]] |
| paths | 0 % (0 z 2) | 0 – [[Les_Lapikus]] |
| gameplay | 0 % (0 z 4) | 0 – [[Brana_Straz]] |
| narrative | 0 % (0 z 1) | 0 – [[Lapikus_Region]] |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**environment**
- [[M_Landscape_Forest_Auto]] – spec, depth 3, valid

**narrative**
- [[Lore_Lapikus]] – concept, depth 1, draft

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[01_terrain]] | `UE_Prikop_Landscape.py`, `Zricenina_heightmap_505_50cm.png`, `Zricenina_preview_orez.png`, `gen_moat.py` | [[M_Landscape_Forest_Auto]] |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/01_terrain/UE_Prikop_Landscape.py` | entry | 01_terrain | folder |
| `/PrototypeDesigns/Lapikus/tools/terrain/gen_moat.py` | entry | 01_terrain | header |
| `/PrototypeDesigns/Lapikus/01_terrain/Zricenina_heightmap_505_50cm.png` | data | 01_terrain | folder |
| `/PrototypeDesigns/Lapikus/01_terrain/Zricenina_preview_orez.png` | data | 01_terrain | folder |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->
<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- Fronta T-0010 (–, [[README_PROJEKT]]): zařadit ze Scratch podle navrženého zařazení (M01, B10 pilotu)
- Scratch: [[README_PROJEKT]] (prepared)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
