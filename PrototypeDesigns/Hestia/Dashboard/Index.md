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
- [[predani_curator_fronta_t0006]]
- [[predani_curator_scratch_kod]]
- [[predani_guesthouse_kamna_stavitel]] – [[Guesthouse]]
- [[predani_knihovnik_rozdeleni]]
- [[predani_knihovnik_souhrny]]
- [[predani_palac_obydli_1_etapa1_ue]] – [[Palac_Obydli]]
- [[predani_palac_obydli_2_krytina]] – [[Palac_Obydli]]
- [[predani_palac_obydli_3_strop]] – [[Palac_Obydli]]
- [[predani_palac_obydli_4_podlaha]] – [[Palac_Obydli]]
- [[predani_palac_obydli_5_okap]] – [[Palac_Obydli]]
- [[predani_palac_obydli_6_zarubne]] – [[Palac_Obydli]]
- [[predani_palac_obydli_7_vybaveni]] – [[Palac_Obydli]]

**Otevřené otázky:** do 14 dní 13 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-23 · Builder · Palac_Obydli · KnowHow: pasti pult_roof (osa a = osa spadu) a vymeny dymniku pod strechou axis v (ohniste.py); sdilene soubory dum/kovarna · predani_builder_knowhow_dum
- 2026-11-23 · Builder · predani_builder_knowhow_dum · předání archivováno · predani_builder_knowhow_dum
- 2026-11-23 · Builder · Lapikus · Steps/03_ruin rozdelen tematicky (G14b): 03_ruin_upravy (kap. 4, 5), 03_ruin_generator (skladba zdi, kap. 7), shared/Meshe (kap. 1.1, 1.2); Souhrn · predani_builder_rozdeleni_03
- 2026-11-23 · Builder · predani_builder_rozdeleni_03 · předání archivováno · predani_builder_rozdeleni_03
- 2026-11-23 · Builder · Ostroh · data staveb u ostrohu v Steps/05_constructions_ostroh · predani_builder_rozdeleni_05
- 2026-11-23 · Builder · Palac_Kovarna · data kovarny v Steps/05_constructions_kovarna · predani_builder_rozdeleni_05
- 2026-11-23 · Builder · Palac_Obydli · data domu v Steps/05_constructions_dum; predani 1-6/7 odkazuji na novy dokument · predani_builder_rozdeleni_05
- 2026-11-23 · Builder · Vez · data Vez_Patra a Vez_Pristresek v Steps/05_constructions_vez · predani_builder_rozdeleni_05
- 2026-11-23 · Builder · Lapikus · Steps/05_constructions rozdelen tematicky (G14b): casti _ostroh, _kovarna, _dum, _vez; shared/Meshe a Meshe_props; Souhrn · predani_builder_rozdeleni_05
- 2026-11-23 · Builder · predani_builder_rozdeleni_05 · předání archivováno · predani_builder_rozdeleni_05

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
