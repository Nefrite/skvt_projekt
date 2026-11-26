---
# orchestrace
type: entity
updated: 2026-11-25
aliases: []
# hra
kind: sequence
parent:
located_in: ["[[Lapikus]]"]
derived_from:
alternative_to: []
pattern:
status: in_progress
# depth_<domain> / target_<domain>: očekávané domény podle kind (01, kap. 8), jiné jen když se řeší
# depth_* = realizace (Unreal, data, StateTree); hloubka návrhu se počítá z dokumentů (01, kap. 5)
# target_mode_<domain>: design | build, jen při odchylce od výchozího režimu domény
ue_path:
assets: []
---
# Cinematics_Lapikus

## Záměr
Cutscény a promo sekvence zříceniny Lapikus: scénář, kamera, střih a render v Sequenceru. Vede je role ScreenWriter, krok [[cinematics]]; první je promo průlet kamery kolem hradu (GameDesigner 2026-11-25).

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| narrative | 3 | – | – | design | bez cíle |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**narrative**
- [[navrh_promo_prulet_kamery]] – design, depth 3, valid
- [[stav_promo_prulet]] – state, depth 4, valid

**Know-how**
- [[Pasti_sequencer_python]]

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[cinematics]] | – | [[stav_promo_prulet]] |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

_Žádné soubory._

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- ručně: co je ověřeno v enginu, kým, kdy; níže blok z posledního čtení Unrealu (ue_map.yaml) -->
<!-- hestia:generated:start -->
<!-- hestia:generated:end -->

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- [[navrh_promo_prulet_kamery]]: Výška terénu v údolí pod útesem a v příkopu před branou: záběry 1, 2 a 4 mají Z odhadnuté; upravit podle levelu. — Architect, 2026-11-25
- [[navrh_promo_prulet_kamery]]: Výška koruny věže v datech (předpoklad 19 m) pro záběr 3. — Architect, 2026-11-25
- [[navrh_promo_prulet_kamery]]: Jsou v levelu kouř z komína a světlo výhně, nebo je dodá Furnisher / Crafter? — Architect, 2026-11-25
- [[navrh_promo_prulet_kamery]]: Délka a hudba: drží 80 s, nebo kratší verze (30 s: záběry 1, 3, 4, 7)? — Architect, 2026-11-25

<!-- hestia:generated:end -->

## Historie a rozhodnutí
