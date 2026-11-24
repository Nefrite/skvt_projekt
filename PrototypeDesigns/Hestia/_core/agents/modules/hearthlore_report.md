---
type: agent_module
module_id: hearthlore_report
trigger: dávka podnětů, před aktualizací, po ověření CR z nové verze
requires: []
modes: [vault]
validity: valid
updated: 2026-11-24
compile: listed
---
# Podněty a hlášení pro HearthLore (Steward)

## Kdy
Po každé dávce `feedback_log`, před každou aktualizací core a po ověření CR, které přinesla nová verze.

## Postup
1. Podněty z fronty: `feedback_log` (dry-run, pak `--apply`); podnět „k ruční opravě“ oprav podle důvodu ve výpisu.
2. `export_cr` (dry-run, pak `--apply`): záznamy `structure_log.md` bez `cr`, jeden záznam = jeden CR v `outbox/`; doplň *Dopad* a *Alternativy*. Co CR nebude, označ s člověkem `cr: none`.
3. Forma podle obsahu: žádost o změnu Hestie a sdílené know-how = CR; informace o stavu instance (ověřené CR, verze, slabá místa) = hlášení.
4. Hlášení `outbox/report_RRRR-MM-DD.md` podle `tpl_report_hearthlore`: *Přehled CR instance* ze `structure_log.md` (sloupec `cr`) a z `outbox/` (připravené, v `outbox/sent/` odeslané); stav v HearthLore neuvádíš.
5. Odesílá člověk; odeslané soubory přesouvá do `outbox/sent/` on.

## Výstup
CR a hlášení v `Maintenance/outbox/`, připravené k odeslání; `structure_log.md` s vyplněnou buňkou `cr`.

## Známé pasti
- Víc záznamů v jednom CR: každý se přijímá a zapracovává zvlášť.
- Stav informace (ověřené CR) poslat jako CR místo hlášení.
- Podněty nechat ležet ve `structure_log.md` až do měsíčního exportu.
