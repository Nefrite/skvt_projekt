---
# orchestrace
type: handover
validity: valid
superseded_by:
for_role: [Librarian]
updated: 2026-11-22
# hra
domain: structures
entity: ""
build_step:
---
# Tematické rozdělení dokumentů (G14b, G14c): předání Knihovníkovi

<!-- Předání obsahuje jen zadání a odkazy (12, kap. 1). Jednorázový úkol přechodu P17 (zadání 0.21, podklad kap. 7 bod 2). Navazuje na [[predani_knihovnik_souhrny]]. -->

## Pro koho a co
Knihovník, režim vault. **Jen návrh**: tematické rozdělení dokumentů podle pravidla *Jeden dokument, jedno téma* (01 kap. 9.2). Přesuny a zápisy po schválení GameDesignera; u návrhů staveb s Architectem.

## Zadání
1. Pro každý dokument navrhni rozdělení: realizace z návrhu do `state`, samostatné části entit do vlastních dokumentů, vrstvené kapitoly „platí přednostně“ přepsat (`nahradit:`). Výstup: tabulka *dokument → cíl → sekce → forma*.
2. G14b (nad `doc_split_chars` 20 000) slouží jako kontrola, že nic nezůstalo:
   - `Docs/structures/`: [[navrh_palac_obydli_stred]] (53 103), [[navrh_vez_pristresek]] (29 872), [[navrh_palac_kovarna]] (28 773), [[Zricenina_03_ruin_stav]] (25 792);
   - mimo oblast Knihovníka (jen návrh pro vlastníka): `Steps/05_constructions` (48 717), `Steps/03_ruin` (39 913) → Builder; `Scratch/Kod_spousteni_kontroly_z_roli` (33 153) → GameDesigner;
   - [[CHECKLIST_assets_navrhy]] **ne** (po etapě A, GameDesigner 2026-11-22).
3. G14c: [[predani_palac_obydli_stavitel]] (10 891 znaků, limit 4 000) – navrhni frontu předání (jedno předání = jeden task, `for_role`), co z něj přenést do [[navrh_palac_obydli_stred]] a [[stav_palac_obydli]]. Předání zakládá a archivuje orchestrační agent, Knihovník jen navrhuje.
4. Rozpory a nejasné hranice témat jako otázky (`question`), ne rozhodnutí.

## Platná rozhodnutí
- Pravidlo *Jeden dokument, jedno téma*: 01 kap. 9.2; předání = jeden task: 12 kap. 1, `_core/agents/modules/handover_out.md`.
- Pokyn GameDesignera k rozdělení `navrh_palac_obydli_stred`: kanban pilotu (Architect připraven).

## Výchozí stav
Audit 2026-11-22 (core 0.21.1): G14b 8×, G14c 1×.

## Kritéria hotovo
- schválené návrhy rozdělení zapsané do hlášení (dokument, cíl, sekce), neschválené jako otázky;
- seznam změn pro Architecta, Buildera a orchestračního agenta (předání).

## Otevřené otázky

## Zbývá
