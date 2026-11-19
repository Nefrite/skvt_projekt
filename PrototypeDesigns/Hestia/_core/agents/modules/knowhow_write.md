---
type: agent_module
module_id: knowhow_write
trigger: ověřená past, postup, diagnóza
requires: [knowhow_lookup]
modes: [vault, chat]
validity: valid
updated: 2026-11-17
---
# Zápis know-how

## Kdy
Ověřil jsi v praxi past, postup, diagnózu, konvenci nebo nastavení nástroje, které bude platit i příště. Nejpozději při uzavření tasku.

## Postup
1. Nejdřív `knowhow_lookup`: existující poznámku doplň, nezakládej duplicitu.
2. **Jedna poznámka = jedna past nebo postup.** Nová poznámka v `KnowHow/` ze šablony `tpl_knowhow`:
   - `knowhow_kind`: `pitfall`, `technique`, `diagnosis`, `convention`, `tool`;
   - `tech`: technologie (hodnoty z `taxonomy_local/tech`; novou hodnotu navrhni Curatorovi);
   - `scope`: `instance`, `engine` (pak povinně `engine_version`), `general`;
   - `verified`: datum ověření.
3. Tělo `pitfall`: *Příznak*, *Příčina*, *Řešení* (obecně, bez vazby na kód projektu), *V projektu* (jak je to vyřešené tady: odkazy na kód, konstanty, skripty), *Jak poznat včas*, *Ověřeno (kdy, kde, kým)*.
4. Při novém výskytu známé pasti doplň *Ověřeno* a `verified`.

## Výstup
Nová nebo doplněná poznámka v `KnowHow/`; v režimu `chat` položka v sekci *Know-how* zápisu Hestia.

## Známé pasti
- Zapsat neověřenou domněnku. Ta patří do `## Otevřené otázky` dokumentu, ne do know-how.
- Míchat obecné řešení s projektovým; obecná část se sdílí do dalších projektů, *V projektu* zůstává v instanci.
- Psát know-how do profilu role místo do `KnowHow/`.
