---
type: agent_module
module_id: file_info
trigger: pokyn k zápisu
requires: [completeness, canon_check]
modes: [vault, chat]
compile: listed
validity: valid
updated: 2026-11-20
---
# Kam zápis patří

## Kdy
Dostaneš pokyn k zápisu („Zapiš: palisáda má tři střílny.“), v chatu i ve vaultu, nebo položku inboxu k zařazení. Formalizace běží **vždy**, i u krátkého pokynu.

## Postup
1. Urči druh tvrzení a cíl:
   - fakt o entitě → doménový dokument entity: záměr a parametry do `design` / `spec`, postavené a naměřené do `state`;
   - svět, doba, postavy, příběh → master lore (`Docs/narrative/Lore_<Prototyp>.md`), rozšíření jako samostatný dokument `narrative`;
   - nerozhodnutý nápad → tematický `Scratch/` (jen na pokyn GameDesignera);
   - rozhodnutí, které uzavírá cestu → `decision` (modul `decision`);
   - pojem a jeho význam → glosář;
   - rozpor s tím, co platí → modul `canon_check` (12 kap. 3b.3–3b.4).
2. Urči entitu a doménu podle hubu a indexu dokumentů (`lookup`). Když nejde jednoznačně říct, je-li to návrh, nebo realizace, nebo které entity se týká, **zeptej se**; nedomýšlej.
3. Rozliš formu (12 kap. 3b.2): **doslovná textace** GameDesignera se zapíše přímo, se zdrojem (chat, datum) a řádkem v `changes.md`, i do nového dokumentu; **přeformulování, sloučení, zkrácení** předlož ke schválení jako diff. Doslovná textace v rozporu s kánonem nikdy přímo.
4. Před zápisem spusť `completeness`, pak zapiš na určené místo; přepis platného textu jen s `nahradit:` nebo po schválení (12 kap. 6.1).

## Výstup
Cíl zápisu (dokument a sekce), forma (doslovně / přeformulováno ke schválení) a řádek `changes.md`; v chatu položka zápisu Hestia s polem `forma` (modul `chat_entry`).

## Známé pasti
- Zapsat návrh do `state` (nebo naopak) jen proto, že dokument už existuje.
- Uložit fakt o světě do doménového dokumentu místo master lore; svět se pak popisuje na dvou místech.
- Přeformulovat doslovnou textaci „pro čitelnost“ a zapsat ji bez schválení.
- Založit nový scratch bez pokynu GameDesignera.
