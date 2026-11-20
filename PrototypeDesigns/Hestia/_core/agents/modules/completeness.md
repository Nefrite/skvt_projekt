---
type: agent_module
module_id: completeness
trigger: pokyn k zápisu
requires: [question]
modes: [vault, chat]
compile: listed
validity: valid
updated: 2026-11-20
---
# Náležitosti zápisu

## Kdy
Před každým zápisem z pokynu (modul `file_info`), před založením nové entity nebo dokumentu a před předáním zápisu Hestia.

## Postup
1. Náležitosti ber z taxonomie, ne z úsudku: povinná pole typu (`types.yaml`, `fields.yaml`), povinné sekce hubu a kroku (`hub_sections.yaml`), očekávané domény podle `kind`, šablona typu (`_core/templates/`).
2. U entity zkontroluj `parent`, `kind`, doménu a režim cíle (návrh, nebo realizace; `target_mode_<domain>`); u dokumentu `domain`, `entity`, `depth` (hloubku popisu) a `validity`.
3. **Ve vaultu** zkontroluj koncept dřív, než ho zapíšeš:
   `python _core/scripts/hestia.py lint --draft <koncept.md> --as <cílová cesta>`
   (text na stdin: `--draft - --as <cesta>`). Nic se nezapisuje; výstup je seznam chybějících náležitostí.
4. **V chatu** projdi stejné náležitosti podle šablony z balíčku kontextu.
5. Každý chybějící údaj převeď na **otázku** GameDesignerovi (modul `question`), ne na domněnku. Otázky dávej najednou, krátce, s návrhem odpovědi, kde ho máš.

## Výstup
Seznam chybějících náležitostí převedený na otázky; po doplnění zápis bez nálezů lintu.

## Známé pasti
- Vyplnit chybějící pole odhadem („asi structures“, „hloubka 2“), aby lint prošel.
- Zkontrolovat jen frontmatter a zapomenout povinné sekce hubu.
- Spustit lint až po zápisu; nález pak zůstane ve vaultu a opravuje se dvakrát.
