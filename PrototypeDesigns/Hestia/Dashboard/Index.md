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
| [[Lapikus_Region]] | 0 % (1) | 57 % (1) | 0 % (0) | bez cíle | 0 % (0) | bez cíle |

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

- 2026-11-23 · Curator · Brana · doplněno target_structures 4, target_gameplay 0 · chat:L5_target
- 2026-11-23 · Curator · Brana_Straz · doplněno target_structures 4, target_gameplay 4 · chat:L5_target
- 2026-11-23 · Curator · Guesthouse · doplněno target_structures 4, target_gameplay 4 · chat:L5_target
- 2026-11-23 · Curator · Les_Lapikus · doplněno target_environment 4, target_paths 4, target_narrative 0 · chat:L5_target
- 2026-11-23 · Curator · Nadvori_Stan · doplněno target_structures 4, target_gameplay 0 · chat:L5_target
- 2026-11-23 · Curator · Palac_Kovarna_Vybaveni · doplněno target_structures 4, target_gameplay 0 · chat:L5_target
- 2026-11-23 · Curator · Palac_Obydli · doplněno target_structures 4, target_gameplay 3 · chat:L5_target
- 2026-11-23 · Curator · Strazni_Vez · doplněno target_structures 4, target_gameplay 4 · chat:L5_target
- 2026-11-23 · Curator · Udoli_Reky · doplněno target_environment 4, target_paths 4, target_narrative 0 · chat:L5_target
- 2026-11-23 · Curator · Vez_Pristresek · doplněno target_structures 4, target_gameplay 0 · chat:L5_target

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
