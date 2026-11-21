---
type: agent_module
module_id: inbox_import
trigger: pokyn k importu z externího zdroje
requires: [file_safety]
modes: [vault]
compile: listed
validity: valid
updated: 2026-11-21
---
# Import do inboxu

## Kdy
GameDesigner dá pokyn importovat položky z externího zdroje (např. databáze v Notion) do `Inbox/`. Jednorázový import, jen scratch; bez synchronizace a bez příloh (13 kap. 10.12). Třídění importovaných položek je až potom (`inbox_triage`, Knihovník).

## Postup
1. **Zadání:** ověř zdroj, filtr (např. projekt, stav) a cílový stav ve zdroji po importu (např. „In Hestia“). Nejasnost řeš modulem `question`.
2. **Čtení zdroje přes konektor:** dotaz s filtrem ze zadání; počet a seznam položek porovnej se zadáním (rozdíl = otázka, ne import). Ověř, že cílový stav ve zdroji existuje; když ne, nezakládej ho a zeptej se.
3. **Soubor výměny** `Maintenance/import/<zdroj>_RRRR-MM-DD.json`: `source`, `source_query` (dotaz a filtr), `exported`, `items` s `ref` (adresa nebo ID ve zdroji), `title`, `created`, `type`, `tags`, `content` a `content_format` (`markdown`, `notion-md` = výstup Notion fetch). Obsah ber doslovně, nic neupravuj ani neopravuj.
4. **Dry-run:** `python _core/scripts/hestia.py inbox_import --from Maintenance/import/<soubor>.json`. Předlož GameDesignerovi jména souborů, kategorie, přeskočené duplicity, nenamapované hodnoty (`tag_map`) a položky, které vyžadují ruční kontrolu.
5. Po schválení `inbox_import --from … --apply` (zapíše scratch, `lint`, `doc_index`, `changes.md`). Nenamapovanou hodnotu doplní do `taxonomy_local/tag_map.yaml` Curator po schválení, kategorie se nevymýšlí.
6. **Stav ve zdroji** měň jen u položek, které výstup příkazu uvádí jako zapsané (`written`), a až po úspěšném `--apply` (návratový kód 0). Pak závěrečný dotaz do zdroje (nic ze zadání nezbylo, zapsané mají cílový stav) a řádek v `Maintenance/sources.md` (zdroj, dotaz, datum, počet).
7. Položky s ruční kontrolou (`needs_review`) projdi s GameDesignerem; nepřevedený blok zůstává v souboru v ohrazení `notion-md`.

## Výstup
Hlášení GameDesignerovi: zdroj a dotaz, počet zapsaných, přeskočených a s ruční kontrolou, nenamapované hodnoty, změna stavu ve zdroji, soubor výměny.

## Známé pasti
- Změnit stav ve zdroji před zápisem do vaultu nebo u položky, která se nezapsala; položka pak ze zdroje „zmizí“ a ve vaultu není.
- Měnit ve zdroji jiné vlastnosti než dohodnutý stav, měnit schéma zdroje nebo ve zdroji mazat.
- Upravit text položky při přípravě souboru výměny (překlepy, formát); import je doslovný.
- Třídit při importu (`raw` → `prepared`, přesun do `Scratch/`); to je `inbox_triage`.
- Spustit import podruhé s novým souborem výměny bez dry-runu; duplicity podle `source_ref` se přeskočí, ale nový `ref` téže položky ne.
