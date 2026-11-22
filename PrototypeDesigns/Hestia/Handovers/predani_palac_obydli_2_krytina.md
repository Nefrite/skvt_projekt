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
# Dům posádky 2/7 – krytina a lemování (Palac_Obydli_Krov)

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Fronta předání domu posádky ze zkrácení [[predani_palac_obydli_stavitel]] (G14c, návrh Knihovníka 2026-11-23). -->

## Pro koho a co
- krytina a lemování v datech, sada `final`; `run_checks.py --only obydli` a `--only palac` OK, náhled;
- odchylky v [[stav_palac_obydli]]; pasti s osami zapsané do `KnowHow/` (předání [[predani_builder_knowhow_dum]]); `task_close`.
## Zadání
Builder: krytina a lemování krovu domu, sada `final`. Po předání 1/7.

## Platná rozhodnutí
- Skladba jako u kovárny (`pult._pult_cover`): latě, prkna po spádu, lišty přes spáry; podle návrhu kap. 4.1 prkna ve dvou délkách (3,4 + 3,2 m), přesah 0,25 m nad latí, plocha s = 9,8–21,7, přesah 0,3 m za štíty.
- **Osy:** `_pult_cover` čte `plan["a"]` jako osu spádu; u kovárny je to `u`, u domu je spád po ose `v` (`axis = "v"`). Ověř na datech domu, případně sjednoť význam `plan`.
- **Latě v kostře** (`pre_laths`, 2 řady nad světnicí, `base`): nezdvojit ani neměnit, v těchto řadách jen západní část latí (`final`).
- **Počet prken po spádu** porovnej s hranicí prken na staveništi ([[stav_palac_obydli]]); když se liší, uprav ji.
- **Prostup komína:** `openings` = komín s = 16,76; n = 1,7; strana 0,5 m. Výměny v `ohniste.py` předpokládají spád po ose `u` a pro dům nic nepostaví: zobecni je, nebo postav výměny v krovu.
- **Lemování** jen podél `Palac_J` (horní okraj), prkno na stojato; koruna `Palac_J` je nad krytinou všude (nejníž 4,43 m, krytina u zdi asi 4,3 m).
- Po krytině zkontroluj stupňovitou mezeru štítu nad příčkou (do 7 cm), případně ji zakryj lištou.
## Výchozí stav
- Návrh domu: [[navrh_palac_obydli_stred]]; co platí a zamčená sada `base`: kap. 0.7 (hodnoty `base` neměň; když je to nutné, napiš Jirkovi a projdi kontroly etapy 1).
- Postavený stav a odchylky: [[stav_palac_obydli]]; dokument kroku: [[05_constructions]].
- Sdílené soubory s kovárnou (`pult.py`, `ohniste.py`, `build_constructions.py`, `gen_constructions.py`, `palac_spec.py`, `config.py`): data kovárny se nesmí změnit, ověř `run_checks.py --only palac`. `manual_edits.json` a `constructions_edits.json` nikdy nepřepisuj.
- Krov: [[navrh_palac_obydli_stred]] kap. 4.1.
## Kritéria hotovo
[[stav_palac_obydli]] (21. 11. 2026): kámen, krov bez krytiny, srub, pec a staveniště postavené; etapa 1 ověřená mimo UE.
## Otevřené otázky

## Zbývá
