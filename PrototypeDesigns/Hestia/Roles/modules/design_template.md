---
type: agent_module
module_id: design_template
trigger: návrh dostavby nebo herního místa
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-21
---
<!-- Z AGENT_GameDesign_hrad.md kap. 7 (pilot Lapikus, B5). -->
# design_template

## Kdy
Game design píše nebo doplňuje návrh dostavby nebo herního místa v `Docs/<doména>/`.

## Postup
Obsah návrhu piš podle bodů níže a zapiš ho do sekcí doménového dokumentu (07 kap. 2):

| Body šablony | Sekce dokumentu |
|---|---|
| Herní účel, Příběh, Priorita a náročnost | *Zadání / záměr* |
| Kde | *Výchozí stav* |
| Konstrukce, Vyžaduje úpravu 03, Varianty, Etapa, Vybavení, Náčrt slovy | *Návrh* |
| Vazby | *Vazby a závislosti* |
| Otevřené otázky | *Otevřené otázky* |

Body:

```
### <Název návrhu>
- Kde: část hradu + zeď (jméno z dat) + poloha (s v m podél zdi od jejího prvního bodu, nebo UE cm X/Y), výška od terénu
- Herní účel: co hráč dělá, jak se tam dostane, co tím získá
- Příběh: kdo a proč to postavil / použil, co o něm vypovídá
- Konstrukce: z čeho, hlavní rozměry (m), jak je ukotvená v ruině, úprava dřeva
- Vyžaduje úpravu 03 (zříceniny)?: ne / ano - co přesně
- Vazby: na co navazuje, s čím se nesmí bít
- Varianty: A / B (krátce, co je lepší pro hru)
- Etapa: platí v etapě 1, 2, nebo v obou
- Vybavení: které hotové props, které by byly nové
- Priorita a náročnost: vysoká/střední/nízká; malá/střední/velká stavba
- Otevřené otázky pro Jirku
- Náčrt slovy: pohled, rozmístění, rozměry
```

## Výstup
Zapisuješ do `Docs/<doména>/` (existující dokumentaci entity doplníš, nový dokument jen když žádný není); navazující práci zadáš předáním v `Handovers/`.

## Známé pasti
