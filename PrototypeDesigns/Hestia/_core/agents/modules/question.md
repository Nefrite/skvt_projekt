---
type: agent_module
module_id: question
trigger: nejasnost, kterou dokumentace neřeší; nejednoznačné zadání
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-17
---
# Otevřená otázka

## Kdy
Narazíš na nejasnost, kterou nevyřešíš z dokumentace ani z know-how, nebo je zadání nejednoznačné.

## Postup
1. Nejednoznačné zadání (např. „o řadu níž“) si nech upřesnit **dřív**, než ho rozpracuješ.
2. U rozhodnutí, které mění návrh, nabídni 2–3 varianty s doporučením.
3. Otázku vznes na GameDesignera v chatu nebo v předání.
4. Když GameDesigner neodpoví nebo odpověď odloží, zaeviduj otázku do sekce `## Otevřené otázky` dokumentu, kterého se týká:
   ```
   - [ ] <otázka> — <role>, RRRR-MM-DD
   ```
   Netýká-li se konkrétního dokumentu, zapiš ji do hubu entity; není-li ani entita, do scratch.
5. Po zodpovězení zapiš odpověď jako fakt do textu (modul `decision`) a položku uzavři: `- [x] <otázka> → zapracováno do kap. X`. Když odpověď uzavírá cestu, vznikne `decision`.

## Výstup
Otázka v chatu; nezodpovězená otázka zaevidovaná v dokumentu; zodpovězená zapracovaná do textu.

## Známé pasti
- Domýšlet odpověď a pokračovat bez upřesnění.
- Zapsat otázku do `queue.md`. Otázka není nález údržby.
- Nechat zodpovězenou otázku otevřenou nebo odpověď zapsat jen k otázce, ne do textu.
