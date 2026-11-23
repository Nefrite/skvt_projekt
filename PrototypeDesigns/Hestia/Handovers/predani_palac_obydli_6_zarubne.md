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
# Dům posádky 6/7 – zárubně otvorů srubu

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Fronta předání domu posádky ze zkrácení [[predani_palac_obydli_stavitel]] (G14c, návrh Knihovníka 2026-11-23). -->

## Pro koho a co
- zárubně v datech (`final`), etapa 1 beze změny; kontroly OK; `task_close`.
## Zadání
Builder: zárubně otvorů srubu, sada `final` (v etapě 1 jsou otvory bez nich, [[navrh_palac_obydli_stavenisko]] kap. 9.1).

## Platná rozhodnutí
- Konce kulatin v otvorech jsou volné: svislé fošny po stranách otvorů.
- Otvory: vchod 1,0 × 2,28 m, dveře v příčce 1,0 × 2,17 m, okénko světnice 0,6 × 0,66 m (parapet 1,4 m), okénko síně 0,5 × 0,44 m (zůstává v s = 11,8–12,3, návrh kap. 0.6).
- Dveře a okenice osadí Furnisher (předání 7/7) do hotových zárubní.
## Výchozí stav
- Návrh domu: [[navrh_palac_obydli_stred]]; co platí a zamčená sada `base`: kap. 0.7 (hodnoty `base` neměň; když je to nutné, napiš Jirkovi a projdi kontroly etapy 1).
- Postavený stav a odchylky: [[stav_palac_obydli]]; dokument kroku: [[05_constructions]], data domu: [[05_constructions_dum]].
- Sdílené soubory s kovárnou (`pult.py`, `ohniste.py`, `build_constructions.py`, `gen_constructions.py`, `palac_spec.py`, `config.py`): data kovárny se nesmí změnit, ověř `run_checks.py --only palac`. `manual_edits.json` a `constructions_edits.json` nikdy nepřepisuj.
- Otvory: [[navrh_palac_obydli_stred]] kap. 4.4.
## Kritéria hotovo
[[stav_palac_obydli]] (21. 11. 2026): kámen, krov bez krytiny, srub, pec a staveniště postavené; etapa 1 ověřená mimo UE.
## Otevřené otázky

## Zbývá
