---
# orchestrace
type: handover
validity: valid
superseded_by:
for_role: [Librarian]
updated: 2026-11-22
# hra
domain: structures
entity: ""
build_step:
---
# Souhrny dlouhých dokumentů (G14a): předání Knihovníkovi

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Jednorázový úkol přechodu P17 (zadání 0.21, podklad kap. 7 bod 2). -->

## Pro koho a co
Knihovník, režim vault. Doplnit sekci `## Souhrn` hned za titul doménových dokumentů a `state` nad `doc_summary_chars` (6 000 znaků), které ji nemají (audit G14a, 2026-11-22).

## Zadání
1. `hestia.py doctor`, pak `hestia.py audit` (dry-run): aktuální seznam G14a je zdroj, níže je stav k 2026-11-22.
2. Po jednom dokumentu: osnova `section --list`, přečti jen sekce potřebné pro souhrn (co platí, hlavní rozhodnutí, odkazy na sekce; asi do 1 500 znaků, 07 kap. 2).
3. Souhrn je **přeformulování** → předlož diff ke schválení GameDesignerovi (12 kap. 3b.2), zapiš až po schválení. Text dokumentu jinak neměň.
4. Narazíš-li na rozpor nebo vrstvené kapitoly „platí přednostně“, nerozhoduj: otázka do dokumentu (`question`), rozdělení patří do předání [[predani_knihovnik_rozdeleni]].
5. Uzavření: `task_close --role Librarian` (dry-run, pak `--apply`).

Dokumenty (G14a, 2026-11-22), doporučené pořadí podle čtení rolemi:
- `Docs/structures/`: [[Zricenina_03_ruin_stav]], [[navrh_palac_obydli_stred]], [[navrh_palac_kovarna]], [[navrh_vez_pristresek]], [[navrh_brana_straz]], [[navrh_palac_obydli]], [[README_ruin]] (`outdated`, jen pokud ho GameDesigner chce), [[navrh_nadvori_stan]], [[Rozhodnuti_zricenina]], [[stav_palac_kovarna]], [[stav_brana_straz]], [[Katalog_props]]
- `Docs/environment/`: [[README_forest]]; `Docs/gameplay/`: [[README_animations]]
- [[CHECKLIST_assets_navrhy]] **ne**: převede se až po etapě A (GameDesigner 2026-11-22).

## Platná rozhodnutí
- Čtení výběrem a Souhrn nad prahem: `_core/agents/modules/start.md` (*Čtení*), 07 kap. 2, 01 kap. 9.2.
- Zápis Knihovníka: `_core/agents/write_rules.md`, oddíl Knihovník.

## Výchozí stav
Audit 2026-11-22 (core 0.21.1): G14a u 16 dokumentů, z toho 14 výše k řešení.

## Kritéria hotovo
- audit bez G14a u dokumentů ze seznamu (kromě odložených), `lint --all` 0 chyb;
- `doc_index` má u nich `chars` a `sections`; `find` na „brána“, „palisáda“, „cisterna“ vrací očekávané dokumenty (výsledek do hlášení);
- řádky `changes.md` zapsal `task_close`.

## Otevřené otázky

## Zbývá
