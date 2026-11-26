---
type: agent_module
module_id: core_update
trigger: aktualizace core, ruční úkoly z manifestu
requires: []
modes: [vault]
validity: valid
updated: 2026-11-26
compile: listed
---
# Aktualizace core (Steward)

## Kdy
GameDesigner chce novou verzi core, `health` nebo `doctor` hlásí novější značku, nebo čekají ruční úkoly `update_core:*` ve frontě.

## Postup
1. `doctor`: Python, PyYAML, `core_source`, necommitnuté změny (před `--apply` musí být vault commitnutý).
2. Před aktualizací odešli čekající podněty (modul `hearthlore_report`: `feedback_log`, `export_cr`).
3. Dry-run `update_core --latest` (na připojené složce `--work-copy`, po fázích `--work-phase copy|run|back`): rozdíl, poznámky z `CHANGELOG.md`, manifest (automatické kroky, ruční úkoly, CR k ověření, *Změny instrukcí*).
4. **Lokální odchylky** (oddíl dry-runu; registr `Maintenance/local_overrides.md`): každou vypsanou náhradu modulu core roztřiď podle rozdílu modulu core: platí dál (stav beze změny) / nová verze ji řeší (stav `zrušená`, lokální modul do `_to_delete/` po schválení) / konflikt (stav `konflikt`, otázka GameDesignerovi). `--apply` se zastaví, jen když nahrazovaný modul v nové verzi chybí: rozhodne GameDesigner (nový modul v `overrides`, nebo zrušení náhrady: záznam `zrušená` a lokální modul do `_to_delete/`), pak registr a modul oprav a spusť znovu; přepínač, který zastavení přeskočí, není.
5. Hlášení GameDesignerovi: verze od → do, co se změní, ruční úkoly, migrace, roztříděné odchylky; počkej na schválení.
6. `update_core --latest --apply` (s `--work-copy`, je-li vault na připojené složce). Selže-li krok, `update_core --after-only --apply`.
7. Report `Maintenance/reports/update_core_RRRR-MM-DD.md`: zkontroluj kroky (u opakované fáze jsou výsledky všech běhů s číslem běhu a časem); ruční úkoly jsou ve frontě (`T-…`), projdi je s GameDesignerem a hotové uzavři (`state`, `closed`).
8. Kompiláty: do Claude Projectu nahraj kompiláty z řádku *Kompiláty changed ve všech bězích* (sečtené přes opakované běhy); `unchanged` nech. Role se změněným základem: `role_diff <Role>`.
9. CR k ověření (`crs` v manifestu) uveď v hlášení pro HearthLore (modul `hearthlore_report`) s výsledkem ověření.

## Výstup
Nový `_core/`, report `update_core_…`, ruční úkoly ve frontě, hlášení GameDesignerovi a podklad pro hlášení HearthLore.

## Známé pasti
- `--apply` bez schválení nebo s necommitnutými změnami.
- Na připojené složce přechod bez `--work-copy` nestihne limit volání; pracovní adresář z výpisu zadej v dalším volání výslovně.
- Ruční úkol uzavřít dřív, než je práce hotová a ověřená.
- Odchylku označit `zrušená` jen proto, že se modul core změnil: nová verze ji řeší, jen když dělá totéž, co lokální modul.
