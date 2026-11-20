---
# orchestrace
type: reference
validity: valid
updated: {{date:YYYY-MM-DD}}
aliases: []
---
# Glossary

Pojmy projektu. Základní pojmy Hestia jsou předvyplněné; pojmy projektu doplňuje Knihovník (12 kap. 3b.6), kolize terminologie i do `structure_log` (kategorie `collision`). Změna významu pojmu je změna kánonu.

## Pojmy Hestia

| Pojem | Klíč | Význam |
|---|---|---|
| entita | `entity`, `kind` | věc, o které dokumentace je; má hub v `Entities/` |
| hub | `type: entity` | poznámka entity, kde se sbíhají odkazy na dokumenty |
| doména | `domain`, `domains` | část designu: `environment`, `structures`, `paths`, `npc`, `gameplay`, `narrative` |
| kategorie | `category` | jemnější druh obsahu (např. `building`, `lore`) |
| hloubka | `depth`, `depth_*`, `target_*` | rozpracovanost 0–6 (blockout … production) |
| krok | `build_step` | krok prototypovací cesty (složka v kódu) |
| milník | `milestone` | čas ve hře (chronologie nebo quest update) |
| platnost | `validity` | stav dokumentu: `valid`, `draft`, `outdated`, `superseded`, `archived` |
| stav | `status` | stav entity: `idea` … `verified`, `on_hold`, `rejected` |
| scratch | `type: scratch` | nezpracovaný nápad; `intake: raw` → `prepared` |
| crosscut | `type: crosscut` | přesah s dopadem na víc domén |
| master lore | `master: lore` | zdroj pravdy o světě prototypu |

## Kategorie `place` vs. druh `location`

- Kategorie `place` označuje **obsah o místě** a záměrně se jmenuje stejně jako druh entity `kind: place` (**entita místa**: pojmenované místo nebo území na mapě).
- `kind: location` je **složená lokace** z entit (hrad, osídlí), ne kategorie.
- Externí tag `location` (např. z Notion) se v `taxonomy_local/tag_map` mapuje na kategorii `place`.

## Pojmy projektu

<!-- canon_check čte tuto tabulku: pevné záhlaví, jeden pojem = jeden řádek (07 kap. 19); aliasy entit zůstávají v hubech -->
| Pojem | Význam | Hlavní dokument nebo hub | Aliasy | Zakázané varianty |
|---|---|---|---|---|
