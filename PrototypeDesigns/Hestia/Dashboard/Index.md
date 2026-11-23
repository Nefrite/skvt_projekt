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
- [[predani_lapikus_koren_actoru_stavitel]] – [[Lapikus]]
- [[predani_palac_obydli_1_etapa1_ue]] – [[Palac_Obydli]]
- [[predani_palac_obydli_2_krytina]] – [[Palac_Obydli]]
- [[predani_palac_obydli_3_strop]] – [[Palac_Obydli]]
- [[predani_palac_obydli_4_podlaha]] – [[Palac_Obydli]]
- [[predani_palac_obydli_5_okap]] – [[Palac_Obydli]]
- [[predani_palac_obydli_6_zarubne]] – [[Palac_Obydli]]
- [[predani_palac_obydli_7_vybaveni]] – [[Palac_Obydli]]

**Otevřené otázky:** do 14 dní 16 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-23 · agent pilotu (Steward) · Nadvori_Stan · karty assetů v used_by (blok ## Assety): plachta, lůžko, truhlička, vak, špalek a díly stanu · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Palac_Obydli · karty assetů v used_by (blok ## Assety), požadavky staveniště (loupák, hromada hlíny, třísky, udusaná hlína, saze) · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Palac_Kovarna_Vybaveni · karty props kovárny v used_by (blok ## Assety) · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Roles/Crafter.md · nový profil projektové role (asset_work, ue_lookup; role_base 0.23.0), kompilát Crafter_compiled · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Roles/Furnisher.md · asset_request, ue_lookup, požadavky jako karty místo checklistu, owner vždy; role_base 0.23.0 · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Roles/Builder.md · asset_request, asset_work (jednoduché díly), knihovní assety vyrábí Crafter, owner vždy; role_base 0.23.0 · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Roles/Architect.md, Roles/GameDesign.md · asset_request a pravidlo owner vždy; role_base 0.23.0 · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Maintenance/queue.md · úkoly rolí T-0035–T-0040 (Builder, Crafter, Curator), podněty P-0006–P-0008; done T-0003, T-0029, T-0030, T-0032–T-0034 · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Maintenance/ue/ue_query_all.py · čtecí skript core 0.23.0 (`ue_query --all --emit --apply`) pro ověření WI-44 bez restartu editoru · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · Architect · Lapikus · navrh konvence korene sloucenych ISM actoru staveb (03 a 05) a predani pro Builder · chat:koren_actoru_staveb

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
