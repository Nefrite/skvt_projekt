---
# orchestrace
type: handover
validity: valid
superseded_by:
for_role: [Builder]
updated: 2026-11-23
# hra
domain: structures
entity: "[[Palac_Obydli]]"
build_step: 05_constructions
---
# Dům posádky 5/7 – okap (Palac_Obydli_Okap)

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Fronta předání domu posádky ze zkrácení [[predani_palac_obydli_stavitel]] (G14c, návrh Knihovníka 2026-11-23). -->

## Pro koho a co
- okap a sud v datech (`final`); trasy průchozí (`run_checks.py --only obydli`); odchylky v [[stav_palac_obydli]]; `task_close`.
## Zadání
Builder: okap domu (`gutter`), sada `final`. **Až po krytině** (2/7), výšku bere z krytiny.

## Platná rozhodnutí
- Žlab pod severní okapovou hranou (n ≈ 6,85), **spád k západu**, rozsochy u stěny, **sud pod západním koncem** (samostatný actor); svod se nedělá.
- Typ `gutter` počítá spád k `+c`: pro spád k západu (−s) ověř směr na datech domu.
- Rozsochy nesmí stát ve vchodu (s = 13,4–14,4); zápraží zůstane průchozí (aspoň 2,0 m, k průchodu ke kovárně 1,2 m).
## Výchozí stav
- Návrh domu: [[navrh_palac_obydli_stred]]; co platí a zamčená sada `base`: kap. 0.7 (hodnoty `base` neměň; když je to nutné, napiš Jirkovi a projdi kontroly etapy 1).
- Postavený stav a odchylky: [[stav_palac_obydli]]; dokument kroku: [[05_constructions]].
- Sdílené soubory s kovárnou (`pult.py`, `ohniste.py`, `build_constructions.py`, `gen_constructions.py`, `palac_spec.py`, `config.py`): data kovárny se nesmí změnit, ověř `run_checks.py --only palac`. `manual_edits.json` a `constructions_edits.json` nikdy nepřepisuj.
- Okap: [[navrh_palac_obydli_stred]] kap. 4.7.
## Kritéria hotovo
[[stav_palac_obydli]] (21. 11. 2026): kámen, krov bez krytiny, srub, pec a staveniště postavené; etapa 1 ověřená mimo UE.
## Otevřené otázky

## Zbývá
