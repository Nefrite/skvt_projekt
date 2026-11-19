---
# orchestrace
type: reference
validity: valid
updated: 2026-11-19
aliases: []
---
# Lapikus – rozcestník

Hlavní rozcestník vaultu Hestia. Pohledy jsou v `Dashboard/views/`: do rozhodnutí Q1 varianta Bases (`bases/`, core plugin), Dataview (`dataview/`, funguje po instalaci pluginu Dataview) a u matice a mapy skript (`generated/`, přepisuje `hubs`). Vlastní pohledy instance patří do `local/`.

## Prototyp

- Kořenová entita: [[Lapikus_Region]]
- Master lore: [[Lore_Lapikus]]
- Pojmy: [[Glossary]]

## Přehled
<!-- hestia:generated:start -->

**Kořenové entity** (zralost po doménách, v závorce nejslabší článek; 04 kap. 3)

| Entita | environment | structures | paths | npc | gameplay | narrative |
|---|---|---|---|---|---|---|
| [[Characters]] | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle |
| [[Lapikus_Region]] | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle |

**Aktivní předání**

- [[predani_brana_straz_striska_stavitel]] – [[Brana_Straz]]
- [[predani_palac_obydli_stavitel]] – [[Palac_Obydli]]

**Otevřené otázky:** do 14 dní 11 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-19 · migrace · Attachments/Zricenina_pudorys_navrh_v3.png · přesun z PrototypeDesigns/Lapikus/03_ruin/Zricenina_pudorys_navrh_v3.png · migrace
- 2026-11-19 · migrace · Attachments/Zricenina_pudorys_v3_nahled.png · přesun z PrototypeDesigns/Lapikus/03_ruin/Zricenina_pudorys_v3_nahled.png · migrace
- 2026-11-19 · migrace · Attachments/Zricenina_rozpad_hmota.png · přesun z PrototypeDesigns/Lapikus/03_ruin/Zricenina_rozpad_hmota.png · migrace
- 2026-11-19 · migrace · Attachments/Zricenina_rozpad_pohledy.png · přesun z PrototypeDesigns/Lapikus/03_ruin/Zricenina_rozpad_pohledy.png · migrace
- 2026-11-19 · migrace · Attachments/navrh_hradba_strilny.png · přesun z PrototypeDesigns/Lapikus/03_ruin/navrh_hradba_strilny.png · migrace
- 2026-11-19 · migrace · Attachments/navrh_koruna_zvetrala.png · přesun z PrototypeDesigns/Lapikus/03_ruin/navrh_koruna_zvetrala.png · migrace
- 2026-11-19 · migrace · Attachments/ZBudova_V_podpora.png · přesun z PrototypeDesigns/Lapikus/03_ruin/ZBudova_V_podpora.png · migrace
- 2026-11-19 · migrace · Attachments/Hradba_Z_S_zaobleni.png · přesun z PrototypeDesigns/Lapikus/03_ruin/Hradba_Z_S_zaobleni.png · migrace
- 2026-11-19 · migrace · Attachments/Hradba_V_zlomy_pred_po.png · přesun z PrototypeDesigns/Lapikus/03_ruin/Hradba_V_zlomy_pred_po.png · migrace
- 2026-11-19 · migrace · Attachments/navrh_ostroh_tramy.png · přesun z PrototypeDesigns/Lapikus/05_constructions/navrh_ostroh_tramy.png · migrace

<!-- hestia:generated:end -->

## Zóny

| Složka | Obsah |
|---|---|
| `Inbox/` | rychlé zápisy a import (`scratch`, `intake: raw`) |
| `Scratch/` | předzpracované a ručně psané nápady |
| `Entities/` | huby entit |
| `Docs/<domain>/`, `Docs/crosscut/` | celková dokumentace podle domén a přesahy |
| `Steps/`, `Steps/shared/` | dokumentace kroků prototypování a sdíleného kódu |
| `Handovers/` | aktivní předání; splněná v `Handovers/_archive/` |
| `KnowHow/` | ověřené know-how |
| `Roles/` | profily projektových rolí |
| `Maintenance/` | údržba: konfigurace, fronta, logy, reporty |
| `_core/` | modul Hestia (needitovat) |
