---
# orchestrace
type: handover
validity: archived
superseded_by:
for_role: [Builder]
updated: 2026-11-23
# hra
domain: structures
entity: ""
build_step: 03_ruin
---
# Rozdělení dokumentu kroku 03_ruin (G14b)

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Navazuje na tematické rozdělení dokumentů (G14b, návrh Knihovníka 2026-11-23, [[predani_knihovnik_rozdeleni]]). -->

## Pro koho a co
- audit bez G14b u [[03_ruin]]; odkazy a `lint --all` bez chyb; `task_close`.
## Zadání
Builder: rozdělit [[03_ruin]] (audit 39 913 znaků, limit 20 000) tematicky (01 kap. 9.2).

## Platná rozhodnutí
- Sekci *Spouštění* (asi 28 200 znaků) rozdělit: jednorázová příprava (kap. 1) zůstane, úpravy (kap. 4 *Úpravy v datech*, kap. 5 *Bourací objemy*) do samostatného dokumentu kroku.
- V hlavním dokumentu doplň *Souhrn* a odkazy na část.
- Přesuny a nové soubory po schválení Jirkou (návrh rozdělení předlož).
## Výchozí stav
- *Jeden dokument, jedno téma*: 01 kap. 9.2; dokument kroku: šablona `tpl_step`.
## Kritéria hotovo
[[03_ruin]] 2026-11-23: asi 44 000 znaků.
## Otevřené otázky

## Zbývá
- [x] návrh rozdělení schválen Jirkou 2026-11-23 (včetně `03_ruin_generator` a přesunu kap. 1.1–1.2 do sdílených meshí).
- [x] [[03_ruin_upravy]]: kap. 4 Úpravy v datech, kap. 5 Bourací objemy (čísla kapitol zachována).
- [x] [[03_ruin_generator]]: skladba zdi a kap. 7 Struktura kódu.
- [x] [[Meshe]] (`Steps/shared/`): kap. 1.1 Meshe kamenů a dřeva, kap. 1.2 Materiály.
- [x] [[03_ruin]]: *Souhrn*, odkazy na části; odkazy „kap. 1.1/1.2/4/5/7“ převedené na nové dokumenty; odkaz v [[05_constructions]] na kap. 5.3 → [[03_ruin_upravy]].
