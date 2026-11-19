---
type: agent_module
module_id: chat_entry
trigger: práce v režimu chat (bez přístupu k vaultu)
requires: []
modes: [chat]
validity: valid
updated: 2026-11-17
---
# Zápis Hestia (režim chat)

## Kdy
Pracuješ v chatu bez přístupu k vaultu a končíš task (místo kroků 1–10 modulu `task_close`).

## Postup
Na konci tasku vydej strukturovaný blok. Prázdné sekce vynech.

```markdown
## Zápis Hestia
- task: <krátký název> | role: <role> | datum: RRRR-MM-DD
### Finální dokumentace
- [[cílový dokument]] § <sekce>: <text k zapsání nebo nahrazení>
### Předání
- [[predani_…]] → archivovat | zbývá: …
### Rozhodnutí (uzavírá cestu)
- <rozhodnutí> | uzavírá: [[…]]
### Metadata
- [[Hub]]: depth_structures 3→4, status in_progress
### Know-how
- nové | doplnit [[…]]: <knowhow_kind>, <tech>, příznak / příčina / řešení
### Otevřené otázky
- [[dokument]]: <otázka>
### Nápady (schválené)
- <téma>: <nápad>
### changes.md
- | RRRR-MM-DD | role | entita | co | zdroj |
```

- Položka, která **nahrazuje** existující text, uvádí cíl (dokument a sekce) a výslovně `nahradit:`; bez toho se text jen doplňuje.
- Když cílový text nevidíš, popiš ho **významem** (`nahradit: tvrzení o výstupu na podestu`); orchestrační agent text najde a přepis nechá schválit.
- Kopie dokumentů v chatu jsou jen zrcadla ke čtení; platí verze ve vaultu.

## Výstup
Blok *Zápis Hestia* v poslední odpovědi tasku. Zapracuje ho orchestrační agent nebo GameDesigner (zdroj v `changes.md` je `chat:<task>`).

## Známé pasti
- Napsat nový text bez `nahradit:`, když má starý nahradit; ve vaultu pak zůstanou obě tvrzení.
- Zapsat do bloku neschválený nápad nebo neověřenou domněnku jako know-how.
- Považovat kopii dokumentu v Claude Projectu za aktuální.
