---
# orchestrace
type: step
validity: valid
updated: 2026-11-25
# hra
step_kind: build
build_step: cinematics
entity: "[[Cinematics_Lapikus]]"
domains: [narrative]
---
# cinematics – cutscény a promo sekvence

## Účel kroku
Cutscény a promo sekvence (Sequencer, CineCamera, Movie Render Queue) mimo sekvenci stavby světa. Hodnoty záběrů drží jen data `PrototypeDesigns/Lapikus/cinematics/<sekvence>.json`, skript `build_sequence.py` z nich v editoru postaví `LS_<Sekvence>` v `/Content/Skvt/Cinematics/`; ruční ladění se přepisuje zpět do dat. Krok vede role ScreenWriter; ostatní sekce doplní při první realizaci (promo průlet).
## Spouštění
## Skripty
<!-- hestia:generated:start -->
<!-- hestia:generated:end -->
## Vstupy a výstupy
## Dopad na dokumentaci
## Známé pasti
<!-- ## Historie: volitelná, archivovaní předchůdci kroku (10 kap. 5a) -->
