---
# orchestrace
type: step
validity: valid
updated: 2026-11-26
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
Promo průlet (`LS_Promo_Prulet`), jen v editoru UE 5.8:
1. Level `/Content/Skvt/LapikusPrototypeMap`, scéna postavená (zřícenina, stavby, les).
2. `05_constructions/stavby/Etapa.py` s `ETAPA = 2` (*Tools → Execute Python Script*); po každém buildu staveb znovu.
3. `Lapikus/cinematics/build_sequence.py` (*Execute Python Script*): smaže předchozí `LS_Promo_Prulet` a actory s tagem `Promo_Prulet` a postaví vše znovu. V Output Logu: „Promo zaber N (rig): hotovo“, případně „selhal“ s tracebackem.
4. Kontrola a render podle `stav_promo_prulet` (kap. *Postup v UE*).
Ruční ladění v UE se přepisuje do `promo_prulet.json` a do stavu (*Ruční ladění*); skript je jinak při dalším běhu přepíše.
## Skripty
<!-- hestia:generated:start -->

_Žádné skripty._

<!-- hestia:generated:end -->
## Vstupy a výstupy
Vstup: `Lapikus/cinematics/promo_prulet.json` (jediný zdroj hodnot záběrů), postavený level se stavem etapy 2. Výstup: `/Content/Skvt/Cinematics/LS_Promo_Prulet`, actory `Promo_Cam_*`, `Promo_Rail_*`, `Promo_Crane_*`, `Promo_Pivot_Vez`, `Promo_Fokus_*` (tag `Promo_Prulet`); render do `Saved/MovieRenders/` (mimo git).
## Dopad na dokumentaci
Změna `promo_prulet.json` nebo `build_sequence.py` = nový běh skriptu a aktualizace `[[stav_promo_prulet]]`; změna polohy nebo výšky staveb, na které kamera míří (věž, brána, dům, kovárna), může vyžadovat úpravu dat záběrů.
## Známé pasti
Sequencer v Pythonu (rozdíly API v UE 5.8): [[Pasti_sequencer_python]].
<!-- ## Historie: volitelná, archivovaní předchůdci kroku (10 kap. 5a) -->
