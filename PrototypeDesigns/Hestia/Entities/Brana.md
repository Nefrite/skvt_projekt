---
# orchestrace
type: entity
updated: 2026-11-23
aliases: []
# hra
kind: structure
parent: "[[Hradby_a_Brana]]"
located_in: []
derived_from:
alternative_to: []
pattern:
status: built
# depth_<domain> / target_<domain>: očekávané domény podle kind (01, kap. 8), jiné jen když se řeší
# depth_* = realizace (Unreal, data, StateTree); hloubka návrhu se počítá z dokumentů (01, kap. 5)
# target_mode_<domain>: design | build, jen při odchylce od výchozího režimu domény
ue_path:
assets: []
depth_structures: 1
target_structures: 4
target_gameplay: 0
---
# Brana

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | – | 1 | 4 | build | −3 |
| gameplay | – | – | 0 | design | ✔ |

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

_Zatím žádné dokumenty._

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[03_ruin]] | `brana_spec.py` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/tools/ruin/brana_spec.py` | spec | 03_ruin | name |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE
<!-- hestia:generated:start -->

Poslední čtení: 2026-11-23 · `Maintenance/reports/ue_Brana.json` · etapa 1 (skript v editoru) · mapa `/Game/Skvt/LapikusPrototypeMap`

- Actory: 0 vlastních
- Třídy: StaticMesh 0, Blueprint 0, BSP 0, ostatní 0
- Zástupné meshe (`/Engine/BasicShapes/`): 0; výchozí materiály: 0
- Fáze: –
- Pro srovnání `depth_*`: structures 1; úroveň realizace posoudí agent nebo GameDesigner (12 kap. 3b.8)

<!-- hestia:generated:end -->

## Assety
<!-- hestia:generated:start -->

Souhrn: requested 0, in_progress 0, generated 0, imported 2, verified 0 · graybox 0 · outdated v UE — (signál vedle `depth_*`, hloubka se z něj nepočítá)

| Asset | Stav | Náhrada v levelu |
|---|---|---|
| [[SM_RuinLogBark_A]] | imported | none |
| [[SM_RuinStakeSmall_A]] | imported | none |

<!-- hestia:generated:end -->
## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
- [ ] Po změně na `depth_structures: 1` (2026-11-21): brána má dál `status: built` a skript `tools/ruin/brana_spec.py` (krok 03_ruin, přiřazený jménem k Brana; audit G10). Změnit `status` (např. `in_progress` / `planned`) a patří `brana_spec.py` spíš [[Strazni_Vez]] (zdi brány)? — agent pilotu, 2026-11-21
- [x] Jakou hodnotu `depth_structures` má brána mít: 1 (blockout – má polohu ve strážní věži) nebo 0 (vlastní realizace žádná)? Dnes 4 — agent pilotu, 2026-11-21 → GameDesigner 2026-11-21: 1; zapsáno `depth_structures: 1`
- [x] Unreal (report `ue_Brana.json`, 2026-11-21): bráně nepatří žádný actor, zdi `Ruin/Brana` jsou podle `ue_map` u [[Strazni_Vez]] (brány jsou otvory ve zdech, GameDesigner 2026-11-21). Odpovídá tomu `depth_structures: 4` u brány, nebo se realizace vede jen u strážní věže? — agent pilotu, 2026-11-21 → GameDesigner 2026-11-21: ne – zdi brány jsou realizací strážní věže; brána sama je dána polohou v ní, její podoba (zátaras, vrata apod.) je teprve na game designu. Nová hodnota `depth_structures` čeká na potvrzení GameDesignera (otázka níže)
<!-- hestia:generated:start -->

- Fronta F-0003 (G4, [[Brana]]): status built bez platného dokumentu state
- Fronta F-0029 (G3, [[Brana]]): bez dokumentu v doméně structures (target_structures 4)
- Fronta T-0036 (role:Builder, [[Brana]]): Španělský jezdec `Brana_Zataras` jako jeden actor: kmen s kůrou Ø 18 × 3,4 m ([[SM_RuinLogBark_A]]) a 4 páry kůlů Ø 7 × 1,6 m ([[SM_RuinStakeSmall_A]]); zátaras zbývá podle [[stav_brana_straz]] (doklad: [[CHECKLIST_assets_navrhy]] kap. 6.4, 11.3 „zatím ne“)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
