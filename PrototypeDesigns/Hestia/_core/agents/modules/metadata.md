---
type: agent_module
module_id: metadata
trigger: zápis frontmatteru
requires: []
modes: [vault]
validity: valid
updated: 2026-11-24
---
# Metadata

## Kdy
Zakládáš dokument nebo měníš jeho frontmatter, případně frontmatter hubu po své práci.

## Postup
1. Nový dokument zakládej ze šablony v `_core/templates/` (`tpl_<typ>`).
2. Projektová role vyplní minimální povinnou sadu:
   - `type`, `validity`, `updated`;
   - `domain` (u přesahu `domains`) a `entity`;
   - u hubu po své práci `depth_<doména>` a `status`, jen když jsi realizoval (Unreal, data, skripty, StateTree, animace); návrh `depth_*` nemění, hloubka návrhu se počítá z dokumentů.
   Zbytek (kategorie, aliasy, vazby) doplní Curator.
3. Hodnoty ber z taxonomie (`_core/taxonomy/` a `Maintenance/taxonomy_local/`); novou hodnotu nevymýšlej, navrhni ji Curatorovi.
4. Frontmatter upravuj po řádcích: neměň pořadí klíčů, komentáře `# orchestrace` / `# hra` ani uvozovky.
   **Zralost (04 kap. 3):** jednotky = entita a všichni potomci podle `parent`, kteří mají v doméně vlastní `target_d` > 0 (bez `status` `rejected`, `on_hold`); cíl a `depth_d` rodiče patří jen jeho vlastní části, rodič bez cíle je obálka.
   - dosaženo: `depth_d` v režimu `build`, hloubka návrhu (nejvyšší `depth` platných `concept`, `design`, `spec`) v režimu `design`;
   - zralost = splněné jednotky / jednotky; hloubka = nejslabší jednotka.
5. `kind`, `parent`, `located_in`, `derived_from`, `alternative_to` hubu měníš jen po schváleném návrhu; `target_*` jen určená role nebo člověk, se zápisem do `changes.md`.
6. Změnu metadat ve více než 10 souborech nech předem schválit (seznam změn z dry-run).

## Výstup
Platný frontmatter (projde `lint`); změna zapsaná v `changes.md` při uzavření tasku.

## Známé pasti
- Nastavit `depth_*` podle odhadu místo skutečně hotové práce.
- Přepsat frontmatter celý (`yaml.dump`) a ztratit komentáře a pořadí.
- Wikilink ve frontmatteru bez uvozovek (`entity: [[X]]` je v YAML seznam, ne odkaz).
