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
# Know-how z předání domu posádky (pasti v kódu)

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Fronta předání domu posádky ze zkrácení [[predani_palac_obydli_stavitel]] (G14c, návrh Knihovníka 2026-11-23). -->

## Pro koho a co
- poznámky v `KnowHow/` (nové nebo doplněné), `lint` bez chyb; `task_close`.
## Zadání
Builder: zapsat ověřené pasti z původního předání domu do `KnowHow/` (modul `knowhow_write`; existující poznámku doplň, nezakládej duplicitu).

## Platná rozhodnutí
- `pult._pult_cover` čte `plan["a"]` jako osu spádu; u domu je spád po ose `v` (u kovárny `u`).
- Výměny v `ohniste.py` předpokládají spád po ose `u`, pro dům nic nepostaví.
- Typ `gutter` počítá spád k `+c`; spád k západu (−s) je třeba ověřit.
- Zásady: sdílené soubory s kovárnou (data kovárny se nesmí změnit, `run_checks.py --only palac`); nepřepisovat `manual_edits.json` ani `constructions_edits.json`; před stavbou dřeva porovnat polohy sloupů, krokví, komína a podezdívek (návrh měl sloup v ose příčky a komín v krokvi); „o řadu níž“ a podobná zadání upřesnit předem.
- Jako past zapisuj jen ověřené; neověřené (`gutter`, osy u domu) ověř při předáních 2/7 a 5/7, nebo je nech jako otázku.
## Výchozí stav
- Know-how: `_core/agents/modules/knowhow_write.md`; tematické poznámky `Pasti_*` v `KnowHow/`.
## Kritéria hotovo
Pasti jsou zatím jen v archivovaném [[predani_palac_obydli_stavitel]] (kap. 5.1, 5.4, 6).
## Otevřené otázky

## Zbývá
