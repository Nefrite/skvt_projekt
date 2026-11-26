---
type: role
validity: valid
updated: {{date:YYYY-MM-DD}}
modules: [start, metadata, file_safety, knowhow_lookup, knowhow_write, question, task_close]
context: []             # dokumenty, které role načítá vždy (např. "[[Lore_<Prototyp>]]")
knowhow_tags: []
combines: []            # role, se kterými se profil skládá
role_base: ""   # verze core z _core/VERSION, se kterou je profil srovnaný se základem rolí; doplní, kdo profil zakládá (12 kap. 2.1)
---
<!-- Jen účel a hranice, vstupy a výstupy, postup role, styl hlášení (12, kap. 2.1).
     Žádné lore, stav, podklady, popis kódu, pasti, konvence ani pravidla návrhu.
     Profil kontrakt zpřísňuje, neruší: výsledek své práce role zapisuje do vaultu (princip 12, task_close);
     zákazy zápisu jen pro kód, data a assety. Zápis do Docs/ je dokumentace domény podle 07 kap. 2, ne výstup role; existující dokumentaci entity
     doplň, nový dokument jen když žádný není. Předání (Handovers/) píšeš z role. -->
# {{title}}

## Co děláš a co ne
## Na čem pracuješ (oblast, entity, cesty v projektu)
## Postup specifický pro projekt
- Před realizací (zadání v chatu, předání) ověř, že návrh (`type: design`), podle kterého realizuješ, má `validity: valid`; když ne, vyžádej si schválení GameDesignera dřív, než realizuješ (12 kap. 3, modul `start`).
## Vstupy a výstupy
## Uzavření tasku
Podle modulu `task_close`; specifika role (např. co patří do `state`):
## Styl hlášení
## Kdy se zeptat GameDesignera
