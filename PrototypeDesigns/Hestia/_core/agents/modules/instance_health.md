---
type: agent_module
module_id: instance_health
trigger: týdenní běh, pokyn ke kontrole zdraví
requires: []
modes: [vault]
validity: valid
updated: 2026-11-24
compile: listed
---
# Zdraví instance (Steward)

## Kdy
Týdenní běh (`weekly`, naplánovaná úloha nebo pokyn), nebo GameDesigner chce vědět, v jakém stavu je instance.

## Postup
1. `weekly --apply` (vault na připojené složce s `--work-copy`), nebo přečti výsledek naplánované úlohy `Maintenance/reports/weekly_RRRR-MM-DD.md`. Samotná kontrola: `health` (s `--apply` report `health_…`).
2. U každé sekce `pozor` (prostředí, verze core, kompiláty, ruční úkoly, podněty, outbox, Unreal) vylož, co nález znamená, a navrhni krok z reportu.
3. Nálezy auditu: počty proti minulému týdnu; chyby G6, G7 a upozornění předej rolím, které je vlastní (úkol ve frontě `code: role:<Role>`), obsah sám neopravuj.
4. Hlášení GameDesignerovi: co je v pořádku, co čeká, doporučené kroky; zásah až po schválení.

## Výstup
Reporty `weekly_…` a `health_…`, hlášení GameDesignerovi, případně úkoly pro role ve frontě.

## Známé pasti
- Opravit obsah kvůli nálezu: kontrola jen hlásí a navrhuje.
- Spustit `update_core --apply` z kontroly zdraví bez schválení (modul `core_update`).
- Brát starý report Unrealu jako chybu: čtecí dotaz má smysl, jen když běží editor.
