---
type: agent_module
module_id: knowhow_lookup
trigger: chyba, neznámý postup, nová technologie; start tasku podle knowhow_tags
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-17
---
# Hledání know-how

## Kdy
Na startu tasku (podle `knowhow_tags` profilu a domény tasku) a vždy, když narazíš na chybu, neznámý postup nebo technologii, se kterou jsi v projektu ještě nepracoval. Hledej **dřív**, než začneš zkoušet.

## Postup
1. Hledej v `KnowHow/` podle `tech`, příznaku (text chyby, chování) a domény (`domain`, `entity`).
2. U nalezené poznámky zkontroluj `scope` a `engine_version`: know-how `scope: engine` pro starší verzi enginu nemusí platit.
3. Postupuj podle sekcí *Řešení* a *V projektu*; *Jak poznat včas* ti řekne, co hlídat.
4. Když nic nenajdeš, řeš problém a po ověření zapiš výsledek modulem `knowhow_write`.

V režimu `chat` hledáš jen v kontextu, který máš; když know-how chybí, požádej o ně GameDesignera nebo orchestračního agenta.

## Výstup
Použitý postup; v hlášení odkaz na poznámku know-how, podle které jsi postupoval.

## Známé pasti
- Zkoušet naslepo a znovu objevit past, která už je zapsaná.
- Použít know-how pro jinou verzi enginu bez ověření.
