---
# orchestrace
type: knowhow
knowhow_kind: technique
tech: [python]
scope: instance
verified: 2026-11-17
validity: valid
updated: 2026-11-19
aliases: []
# hra
domain: structures
---
# Změř skutečný stav, než navrhneš výšky

<!-- Z AGENT_Architekt_hrad.md kap. 5 body 8–9 (pilot Lapikus, B6). -->

8. **Změř skutečný stav, než navrhneš výšky** (poučení z 16. 11. 2026):
   - koruny zdí, vrchy oblouků a terén ber ze stavu **s terénem z levelu** (`terrain_from_level.json`); zkušební `ruin_layout.json` mimo `03_ruin\blocks` se počítá bez něj a výšky vyjdou až o 2 m jinak;
   - u návrhu uveď datum měření. Když se od té doby měnily polohy zdí nebo terén, čísla znovu ověř (návrh strážní podesty počítal s korunou `Brana_V` o 1,6–2 m níž);
   - u zdí s různou patou (brána) piš výšky absolutně v UE cm.
9. **Porovnej polohy prvků mezi sebou**, ne jen se zdmi: sloup proti podezdívce a příčce, komín proti krokvím (osa komína = střed mezi krokvemi), ráhna proti průzorům, sloupky proti střílnám a průzorům. Návrh domu měl sloup v ose příčky a komín v krokvi.
