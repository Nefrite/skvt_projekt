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

- 2026-11-23 · agent pilotu (Steward) · Palac_Kovarna_Vybaveni · karty props kovárny v used_by (blok ## Assety) · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Roles/Crafter.md · nový profil projektové role (asset_work, ue_lookup; role_base 0.23.0), kompilát Crafter_compiled · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Roles/Furnisher.md · asset_request, ue_lookup, požadavky jako karty místo checklistu, owner vždy; role_base 0.23.0 · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Roles/Builder.md · asset_request, asset_work (jednoduché díly), knihovní assety vyrábí Crafter, owner vždy; role_base 0.23.0 · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Roles/Architect.md, Roles/GameDesign.md · asset_request a pravidlo owner vždy; role_base 0.23.0 · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Maintenance/queue.md · úkoly rolí T-0035–T-0040 (Builder, Crafter, Curator), podněty P-0006–P-0008; done T-0003, T-0029, T-0030, T-0032–T-0034 · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Maintenance/ue/ue_query_all.py · čtecí skript core 0.23.0 (`ue_query --all --emit --apply`) pro ověření WI-44 bez restartu editoru · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · Architect · Lapikus · navrh konvence korene sloucenych ISM actoru staveb (03 a 05) a predani pro Builder · chat:koren_actoru_staveb
- 2026-11-23 · agent pilotu (Steward) · Maintenance/reports/ue_*.json · reporty čtení z UE (15 entit) z výsledku 2026-11-23 20:30, format_version 3 (`ue_query --import --all --apply`; WI-44) · predani_pilot_lapikus_knihovnik_unreal P19
- 2026-11-23 · agent pilotu (Steward) · Lapikus · navrh_lapikus_koren_actoru: validity draft → valid, status draft → selected (Varianta C schválena GameDesignerem, předáno Builderovi) · pokyn GameDesignera 2026-11-23
- 2026-11-23 · agent pilotu (Steward) · Maintenance/taxonomy_local/asset_sources.yaml · nový manifest knihovních assetů (LIB_MESHES, STONE_MESH_VERSION, MESH_AXES, LIB_SHAPES, data Lapikus/**/*.json, Content/Skvt/Lapikus/Ruin); T-0031 · predani_pilot_lapikus_knihovnik_unreal P20
- 2026-11-23 · agent pilotu (Steward) · Maintenance/asset_index.json, asset_index.md · sekce library: 59 assetů z kódu (49 klíčů × varianty), 0 klíčů bez karty · predani_pilot_lapikus_knihovnik_unreal P20
- 2026-11-23 · agent pilotu (Steward) · Assets/ · blok *Z kódu* (generovaný) v 64 kartách meshí; ruční opis odstraněn u 47 karet, u 17 mimo LIB_MESHES ponechán s vysvětlením · predani_pilot_lapikus_knihovnik_unreal P20
- 2026-11-23 · agent pilotu (Steward) · Maintenance/queue.md · podněty P-0009 (manifest bez ROUND_MESHES, WOOD_NOMINAL, kamenů), P-0010 (výskyty v datech celé entitě Lapikus); T-0031 done · predani_pilot_lapikus_knihovnik_unreal P20
- 2026-11-23 · agent pilotu (Steward) · Maintenance/ue/ue_query_assets.py · čtecí skript assetů pro etapu C (54 karet od generated) · predani_pilot_lapikus_knihovnik_unreal P20
- 2026-11-23 · Architect · Brana · navrh sijoveho prikopu, terennich valu, mostniho pilire, lavky a zatarasu pred vychodni branou a predani pro Builder · chat:prikop_pred_branou

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
