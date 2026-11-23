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
# Dům posádky 1/7 – kontrola etapy 1 a hranic staveniště v UE

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Fronta předání domu posádky ze zkrácení [[predani_palac_obydli_stavitel]] (G14c, návrh Knihovníka 2026-11-23). -->

## Pro koho a co
- Jirka potvrdil kontrolu v UE a rozmístění hranic; capture uložený, po buildu beze změny polohy;
- `run_checks.py --only obydli` OK; [[stav_palac_obydli]] aktuální; `task_close`.
## Zadání
Builder s Jirkou: dokončit staveniště etapy 1 v UE ([[navrh_palac_obydli_stavenisko]]).

## Platná rozhodnutí
1. Jirka v UE: `05_constructions/stavby/Palac_Obydli.py`, pak `Etapa.py` s `ETAPA = 1` (kontrola staveniště), pak `ETAPA = 2` (staveniště zmizí, dům beze změny). Na co se dívat: vzpěry na líci sloupů 11,1 a 13,0, žebřík mezi krokvemi 18,273 a 19,282, hranice na nádvoří (na terénu, mimo průlom, portál a dveře s = 27), v etapě 1 bez uhlí pod plotnou.
2. Vzhled schválil Jirka 21. 11. 2026; zbývá ověřit rozdělení na objekty a rozmístění hranic podle game designu: Jirka hranice posune v UE, pak `stavby/Palac_Obydli_Stavenisko_Capture.py` (polohy do `constructions_edits.json`), nový build a `run_checks.py --only obydli` (kontroly berou polohy z levelu). Ověř, že hranice po buildu zůstane, kde byla (capture zatím neověřený).
3. Výsledek do [[stav_palac_obydli]] (§ *Ověřeno v UE*: *V levelu* a *Vizuálně ověřeno*).
## Výchozí stav
- Návrh domu: [[navrh_palac_obydli_stred]]; co platí a zamčená sada `base`: kap. 0.7 (hodnoty `base` neměň; když je to nutné, napiš Jirkovi a projdi kontroly etapy 1).
- Postavený stav a odchylky: [[stav_palac_obydli]]; dokument kroku: [[05_constructions]], data domu: [[05_constructions_dum]].
- Sdílené soubory s kovárnou (`pult.py`, `ohniste.py`, `build_constructions.py`, `gen_constructions.py`, `palac_spec.py`, `config.py`): data kovárny se nesmí změnit, ověř `run_checks.py --only palac`. `manual_edits.json` a `constructions_edits.json` nikdy nepřepisuj.
- Kontroly etapy 1: [[navrh_palac_obydli_stavenisko]] kap. 9.4; postavená verze staveniště: [[stav_palac_obydli]], *Co se liší od návrhu*.
## Kritéria hotovo
[[stav_palac_obydli]] (21. 11. 2026): kámen, krov bez krytiny, srub, pec a staveniště postavené; etapa 1 ověřená mimo UE.
## Otevřené otázky

## Zbývá
