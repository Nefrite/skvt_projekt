---
type: agent_module
module_id: core_update
trigger: aktualizace core, ruční úkoly z manifestu
requires: []
modes: [vault]
validity: valid
updated: 2026-11-24
compile: listed
---
# Aktualizace core (Steward)

## Kdy
GameDesigner chce novou verzi core, `health` nebo `doctor` hlásí novější značku, nebo čekají ruční úkoly `update_core:*` ve frontě.

## Postup
1. `doctor`: Python, PyYAML, `core_source`, necommitnuté změny (před `--apply` musí být vault commitnutý).
2. Před aktualizací odešli čekající podněty (modul `hearthlore_report`: `feedback_log`, `export_cr`).
3. Dry-run `update_core --latest` (na připojené složce `--work-copy`): rozdíl, poznámky z `CHANGELOG.md`, manifest (automatické kroky, ruční úkoly, CR k ověření, *Změny instrukcí*).
4. Hlášení GameDesignerovi: verze od → do, co se změní, ruční úkoly, migrace; počkej na schválení.
5. `update_core --latest --apply` (s `--work-copy`, je-li vault na připojené složce). Selže-li krok, `update_core --after-only --apply`.
6. Report `Maintenance/reports/update_core_RRRR-MM-DD.md`: zkontroluj kroky; ruční úkoly jsou ve frontě (`T-…`), projdi je s GameDesignerem a hotové uzavři (`state`, `closed`).
7. Kompiláty: do Claude Projectu nahraj jen `changed` z reportu `compose_role`; `unchanged` nech. Role se změněným základem: `role_diff <Role>`.
8. CR k ověření (`crs` v manifestu) uveď v hlášení pro HearthLore (modul `hearthlore_report`) s výsledkem ověření.

## Výstup
Nový `_core/`, report `update_core_…`, ruční úkoly ve frontě, hlášení GameDesignerovi a podklad pro hlášení HearthLore.

## Známé pasti
- `--apply` bez schválení nebo s necommitnutými změnami.
- Na připojené složce přechod bez `--work-copy` nestihne limit volání; pracovní adresář z výpisu zadej v dalším volání výslovně.
- Ruční úkol uzavřít dřív, než je práce hotová a ověřená.
