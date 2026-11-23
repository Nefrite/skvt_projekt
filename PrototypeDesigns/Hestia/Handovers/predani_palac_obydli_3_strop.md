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
# Dům posádky 3/7 – strop světnice se zavěšením dymníku (Palac_Obydli_Strop)

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Fronta předání domu posádky ze zkrácení [[predani_palac_obydli_stavitel]] (G14c, návrh Knihovníka 2026-11-23). -->

## Pro koho a co
- strop a zavěšení dymníku v datech (`final`), nic nevisí; kontroly OK, náhled;
- odchylky v [[stav_palac_obydli]]; `task_close`.
## Zadání
Builder: strop světnice, nový typ nebo rozšíření `tower_floor`, sada `final`.

## Platná rozhodnutí
- Světnice je teď s = 14,97–20,6 (ne 15,9–20,6 jako v návrhu kap. 4.5). Trámky 14 × 18 cm východ–západ, spodek 2,3 m, prkna 4 cm; uložení na srub příčky a východní stěny (vrch srubu 2,5 m).
- **Otvor pro dymník a komín:** dymník 1,6 × 1,1 m (s = 15,96–17,56; n = 1,15–2,25), spodní okraj 1,8 m, vrch 2,6 m; otvor asi 1,7 × 1,2 m, přerušené trámky do výměny.
- **Zavěšení dymníku** (teď visí ve vzduchu) na výměnu stropu, závěsné tyče jako u kovárny (`hangers`).
- Sloupy krovu s = 15,3 / 18,0 / 20,4 (n = 0,85) stojí ve světnici u jižní zdi: strop je obejde.
- Přístup na půdu: otvor ve štítu příčky, žebřík ze síně (kulisa).
## Výchozí stav
- Návrh domu: [[navrh_palac_obydli_stred]]; co platí a zamčená sada `base`: kap. 0.7 (hodnoty `base` neměň; když je to nutné, napiš Jirkovi a projdi kontroly etapy 1).
- Postavený stav a odchylky: [[stav_palac_obydli]]; dokument kroku: [[05_constructions]], data domu: [[05_constructions_dum]].
- Sdílené soubory s kovárnou (`pult.py`, `ohniste.py`, `build_constructions.py`, `gen_constructions.py`, `palac_spec.py`, `config.py`): data kovárny se nesmí změnit, ověř `run_checks.py --only palac`. `manual_edits.json` a `constructions_edits.json` nikdy nepřepisuj.
- Místnosti a pec: [[navrh_palac_obydli_stred]] kap. 4.5, 4.6.
## Kritéria hotovo
[[stav_palac_obydli]] (21. 11. 2026): kámen, krov bez krytiny, srub, pec a staveniště postavené; etapa 1 ověřená mimo UE.
## Otevřené otázky

## Zbývá
