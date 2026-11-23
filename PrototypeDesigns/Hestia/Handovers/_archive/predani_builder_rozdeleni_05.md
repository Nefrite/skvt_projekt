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
build_step: 05_constructions
---
# Rozdělení dokumentu kroku 05_constructions (G14b)

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Navazuje na tematické rozdělení dokumentů (G14b, návrh Knihovníka 2026-11-23, [[predani_knihovnik_rozdeleni]]). -->

## Pro koho a co
- audit bez G14b u [[05_constructions]]; odkazy a `lint --all` bez chyb; `task_close`.
## Zadání
Builder: rozdělit [[05_constructions]] (audit 48 717 znaků, limit 20 000) tematicky (01 kap. 9.2).

## Platná rozhodnutí
- Sekci *Vstupy a výstupy → 4. Co je v `constructions.json`* (asi 37 600 znaků) rozdělit po skupinách staveb do samostatných dokumentů kroku: Ostroh (`Ostroh_Krov`, `_Dostavba`, `_Podlaha`), Kovárna (`Palac_Kovarna_Pristresek`, `_Vyhen`, `_Stena`, `_Kul`, `_Okap`), Dům (`Palac_Obydli_*`), Věž (`Vez_Patra`, `Vez_Pristresek`).
- V hlavním dokumentu zůstane účel, spouštění, skripty a soubory a odkazy na části; doplň *Souhrn*.
- Souvisí s úkolem T-0005 (`Vez_Patra` do specifikace entity [[Vez]]).
- Přesuny a nové soubory po schválení Jirkou (návrh rozdělení předlož).
## Výchozí stav
- *Jeden dokument, jedno téma*: 01 kap. 9.2; dokument kroku: šablona `tpl_step`.
## Kritéria hotovo
[[05_constructions]] 2026-11-23: asi 56 000 znaků.
## Otevřené otázky

## Zbývá
- [x] návrh rozdělení schválen Jirkou 2026-11-23 (včetně sdílených meshí v `Steps/shared/`).
- [x] [[05_constructions_ostroh]], [[05_constructions_kovarna]], [[05_constructions_dum]], [[05_constructions_vez]] (tabulka klíčů `floors` a souřadnice věže, `Vez_Pristresek`).
- [x] [[Meshe]] (dřevo, kulatina, další knihovní meshe) a [[Meshe_props]] (props) v `Steps/shared/`.
- [x] [[05_constructions]]: *Souhrn*, kap. 4 jako rozcestník, etapy (sady actorů) a klíč `rubble` zůstávají v hlavním dokumentu.
- [x] T-0005 (`queue.md`) odkazuje na „[[05_constructions]] kap. 4 (Vez_Patra)“: obsah je teď v [[05_constructions_vez]]; řádek fronty jsem neměnil (fronta patří Curatorovi).
