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
# Dům posádky 4/7 – podlaha světnice (Palac_Obydli_Podlaha)

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Fronta předání domu posádky ze zkrácení [[predani_palac_obydli_stavitel]] (G14c, návrh Knihovníka 2026-11-23). -->

## Pro koho a co
- podlaha v datech (`final`); kontroly OK; odchylky v [[stav_palac_obydli]]; `task_close`.
## Zadání
Builder: prkenná podlaha světnice (`plank_floor`), sada `final`.

## Platná rozhodnutí
- Obrys = vnitřek světnice mimo sokl pece (s = 15,96–17,56; n = 0,72–2,32) a patní kameny sloupů (`avoid`). Síň má udusanou hlínu (nestaví se).
- Práh dveří v příčce: podezdívka je ve dveřích přerušená, podlaha končí u příčky.
## Výchozí stav
- Návrh domu: [[navrh_palac_obydli_stred]]; co platí a zamčená sada `base`: kap. 0.7 (hodnoty `base` neměň; když je to nutné, napiš Jirkovi a projdi kontroly etapy 1).
- Postavený stav a odchylky: [[stav_palac_obydli]]; dokument kroku: [[05_constructions]], data domu: [[05_constructions_dum]].
- Sdílené soubory s kovárnou (`pult.py`, `ohniste.py`, `build_constructions.py`, `gen_constructions.py`, `palac_spec.py`, `config.py`): data kovárny se nesmí změnit, ověř `run_checks.py --only palac`. `manual_edits.json` a `constructions_edits.json` nikdy nepřepisuj.
- Místnosti: [[navrh_palac_obydli_stred]] kap. 4.5.
## Kritéria hotovo
[[stav_palac_obydli]] (21. 11. 2026): kámen, krov bez krytiny, srub, pec a staveniště postavené; etapa 1 ověřená mimo UE.
## Otevřené otázky

## Zbývá
