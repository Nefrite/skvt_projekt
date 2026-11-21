---
type: agent_module
module_id: inbox_triage
trigger: položky intake raw
requires: [file_info, lookup]
modes: [vault, chat]
compile: listed
validity: valid
updated: 2026-11-21
---
# Třídění inboxu

## Kdy
Na pokyn GameDesignera, typicky v chatu s ním: v `Inbox/` jsou položky `intake: raw` (12 kap. 3b.7, 05 kap. 6).

## Postup
1. Ve vaultu (i chat s připojenou složkou projektu) vezmi položky `intake: raw` přímo z `Inbox/`. V chatu bez vaultu je dostaneš v balíčku kontextu; **bez balíčku** netřiď a řekni přesně, co potřebuješ: `hestia.py compose_context --topic inbox --apply` (položky a k nim kandidátní dokumenty), nebo přístup k vaultu.
2. Po položkách předlož návrh: kategorie, entita, doména nebo crosscut, cíl (`file_info`); duplicity a souvislosti s dokumenty a otevřenými otázkami (`lookup`); rozpor s kánonem (`canon_check`).
3. GameDesigner rozhodne: zařadit (cíl), ponechat jako nápad, sloučit s existujícím, zahodit (`_to_delete/`), nebo odložit. Rozhodnutí je zároveň schválení přesunu.
4. Podle rozhodnutí:
   - přesuň položku do `Scratch/`, nastav `intake: prepared` a vyplň *Předzpracování*; text položky neměň;
   - jasný doslovný fakt s potvrzeným cílem rovnou zapiš (12 kap. 3b.2) a ve scratch nech odkaz na cíl;
   - přeformulování nebo sloučení předlož ke schválení.
5. **Bez GameDesignera** (velká dávka po importu) jen vyplň návrhy do *Předzpracování*, `intake: raw` nech a nic nepřesouvej ani nezapisuj.
6. V chatu bez vaultu vydej výsledek jako zápis Hestia (modul `chat_entry`). Ve vaultu bez možnosti spustit skript core (`lint --draft`, `doc_index`) zkontroluj náležitosti podle taxonomie ručně a v souhrnu výslovně uveď, že skript neběžel.

## Výstup
Na konci relace souhrn: zařazeno, čeká, duplicity, rozpory, změny kánonu.

## Známé pasti
- Přesunout nebo zahodit položku bez rozhodnutí GameDesignera.
- Upravit text položky při vyplňování *Předzpracování*.
- Přehlédnout, že položka opakuje existující otevřenou otázku; patří k ní, ne do nového scratch.
