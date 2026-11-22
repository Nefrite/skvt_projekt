---
type: agent_module
module_id: hestia_feedback
trigger: problém nebo možnost zlepšení Hestie jako nástroje
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-22
---
# Podnět ke změně Hestie

## Kdy
Narazíš na problém nebo možnost zlepšení Hestie jako nástroje: kontrakt, moduly, šablony, taxonomie, skripty, kontroly, proces. Nápad k obsahu hry je nápad (`idea_capture`), ne podnět.

## Postup
1. Change request nezakládáš a do `structure_log.md` ani `outbox/` nepíšeš: CR mimo kanál Curatora (`export_cr`) by nikdo nezpracoval.
2. **Režim vault:** připiš na konec `Maintenance/queue.md` položku `kind: proposal`, `code: hestia`, `target` = čeho se týká (entita, dokument nebo část Hestie, např. `tpl_state`, `audit G10`), `proposal` = `<role>: co se stalo (doklad: odkaz na dokument, report nebo řádek) → navrhovaná změna`, `priority: medium` (`high` jen když podnět blokuje práci), `state: open`. Schválení GameDesignera k zápisu není potřeba.
3. **Režim chat:** podnět dej do zápisu Hestia, sekce *Podněty pro Hestii* (modul `chat_entry`); do fronty ho zapíše ten, kdo zápis zapracuje.
4. Podnět uveď v hlášení na konci tasku (`task_close`, krok 11).

## Výstup
Položka fronty `P-…` s kódem `hestia` (nebo sekce v zápisu Hestia). Curator ji převede do `structure_log.md` a uzavře; o CR rozhoduje člověk při `export_cr`.

## Známé pasti
- Založit CR přímo v `outbox/` nebo v repozitáři projektu: zůstane mimo kanál a nikdo ho nezpracuje.
- Podnět bez dokladu: Curator ho nemůže posoudit.
- Zaměnit podnět s otázkou (`question`) nebo s nálezem údržby (zapisuje Auditor).
