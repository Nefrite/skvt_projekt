---
type: agent_module
module_id: canon_check
trigger: pokyn k zápisu, lookup s více zdroji
requires: [lookup]
modes: [vault, chat]
compile: listed
validity: valid
updated: 2026-11-21
---
# Soulad s kánonem

## Kdy
Před každým zápisem (modul `file_info`) a u odpovědi `lookup`, kterou skládáš z více zdrojů.

## Postup
1. Najdi, co o tvrzení dokumentace říká (`lookup`), a urči oblast tvrzení. Přednost od nejvyšší (12 kap. 3b.3):
   - **realizovaný stav:** report Unrealu → `state` → skript a dokumentace kroku → `design`;
   - **záměr a návrh:** `decision` → platný `design` / `spec` (ne `rejected`) → předání → scratch;
   - **svět, doba, postavy:** master lore → dokumenty `narrative` → ostatní;
   - **pojmy a jména:** glosář → `aliases` v hubech.
   Zastaralé a nahrazené dokumenty jsou jen historie; při shodě úrovně platí novější `updated`.
2. Glosář: čti tabulku *Pojmy projektu* v `Dashboard/Glossary.md`. Zakázaná varianta jména v zápisu = oprav na pojem, nebo se zeptej; kolize pojmů zapiš i do `structure_log` (kategorie `collision`). Starší záhlaví tabulky (tři sloupce) se nečte jako pojmy, `lint` k němu vypíše varování.
3. **Rozpor** se zápisem nerozhoduješ. Ukaž ho GameDesignerovi (co platí, kde, odkud) a zeptej se: „Měníš kánon?“
4. **Vědomá změna kánonu** (12 kap. 3b.4), jen po potvrzení „ano, měním“:
   - nové tvrzení na místo podle `file_info` (doslovně přímo, přeformulované po schválení);
   - u podstatné změny (svět, varianta, uzavření cesty) `decision` s důvodem;
   - staré tvrzení nemaž: `validity: outdated` s odkazem, nebo `nahradit:` (stará verze zůstane v historii);
   - řádek `changes.md`, jehož sloupec *co se změnilo* začíná `změna kánonu:` a obsahuje odkaz na rozhodnutí:
     `| RRRR-MM-DD | Librarian | <entita> | změna kánonu: <co> ([[<rozhodnutí>]]) | <zdroj> |`;
   - vypiš dokumenty, které staré tvrzení opakují (index dokumentů, glosář), a navrhni jejich úpravu ke schválení; sám nic nepřepisuj, neupravené nech jako otázky.
5. Bez potvrzení zůstává rozpor otázkou k dotčenému dokumentu (modul `question`), u rozporu mezi dokumenty i položka fronty.

## Výstup
„Bez rozporu“, nebo rozpor se zdroji a otázkou; po potvrzené změně kánonu zápis, případně `decision`, řádek `changes.md` s předponou `změna kánonu:` a seznam dotčených dokumentů k úpravě.

## Známé pasti
- Rozhodnout rozpor sám podle toho, co zní rozumněji. Poslední slovo má GameDesigner.
- Zapsat změnu kánonu bez předpony `změna kánonu:`; audit ji pak nezapočítá.
- Přepsat staré tvrzení a nechat v jiných dokumentech jeho kopie bez otázky.
