---
type: reference
validity: valid
updated: 2026-11-24
---
# Plán kontrol (výchozí, core)

Kdy a kdo spouští kontroly. Výchozí plán podle zadání 05, kap. 6. Čísla (prahy) se berou z `Maintenance/config.yaml` (klíč `thresholds`, výchozí hodnoty v `_core/taxonomy/defaults.yaml`); tento dokument je lidský popis. Instance si odchylky v plánu zapíše do `Maintenance/review_plan_local.md`.

## Kdy a co

| Kdy | Co | Kdo |
|---|---|---|
| Po každém tasku | `task_close`: `lint` dotčených souborů (G6, G7), G11 dotčených entit | projektová role, orchestrační agent |
| Při změně core nebo profilu role | `compose_role` (kompiláty pro chat) | Curator |
| Při novém obsahu v `Inbox/` | metadata importu | Curator |
| Na pokyn GameDesignera (typicky v chatu) | třídění inboxu `raw` → `prepared` (12 kap. 3b.7) | Knihovník + člověk |
| Týdně | `weekly` (13 kap. 10.20): `audit` G1–G15, zralost, `asset_index`, `hubs`, `doc_index`, `health`; otevřené otázky podle stáří, metriky Knihovníka (12 kap. 3b.9); čtecí dotaz do Unrealu, běží-li editor (12 kap. 3b.8). Naplánovaná úloha instance (README core), bez zásahu do obsahu | Steward (bez Stewarda Auditor a Curator, `weekly` spouští člověk) |
| Po každé dávce `feedback_log` a před každou aktualizací core | `export_cr` a hlášení pro HearthLore (`outbox/report_…`) | Steward |
| Při uzavření fáze prototypu | revize `target_*`, dokumentační dluh, master lore (G12) | Auditor + člověk |
| Při nové doméně, kategorii, kroku nebo `kind` | zápis do `taxonomy_local` a `structure_log` | Curator |
| Měsíčně | `structure_log` → change requesty (`export_cr`), jen bez aktivního Stewarda (`steward_active: false`) | Curator + člověk |

## Prahy

| Klíč v `thresholds` | Co hlídá | Kde se projeví |
|---|---|---|
| `scratch_raw_days` | scratch `intake: raw` starší než práh | G5 |
| `stale_doc_days` | dokument bez změny `updated` déle než práh, přestože se jeho entita změnila | G5 |
| `open_question_days` | otevřená otázka starší než práh | report (stáří otázek) |
| `knowhow_unverified_days` | know-how bez `verified` déle než práh | report, G5 |
| `g11_step_entities` | skript kroku, který zasahuje víc entit než práh, se hlásí na úrovni kroku (`Steps/`), entity se jen vypíšou | G11 |
| `bulk_metadata_files` | od kolika souborů potřebuje změna metadat schválení | schvalování (`write_rules`) |

## Povinné dokumenty

Klíč `required_docs` v `Maintenance/config.yaml` (výchozí `lore_master`: master lore každého prototypu). Chybějící dokument nebo prázdná povinná sekce je G12.

Týdenní běh se po odzkoušení může stát naplánovanou úlohou.
