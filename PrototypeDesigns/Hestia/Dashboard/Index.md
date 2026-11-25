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
| [[Lapikus_Region]] | 33 % (1) | 83 % (3) | 0 % (0) | bez cíle | 0 % (0) | 0 % (0) |

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

**Otevřené otázky:** do 14 dní 21 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-24 · agent pilotu (Steward) · Lapikus_Region · vlastní část terén: target_environment 4 (CR-035, schválil GameDesigner 2026-11-24) · predani_pilot_lapikus_knihovnik_unreal P21, P22
- 2026-11-24 · agent pilotu (Steward) · Maintenance/structure_log.md · buňka cr u P-0001–P-0016: CR-033 až CR-040 podle zaevidování v HearthLore · predani_pilot_lapikus_knihovnik_unreal P21, P22
- 2026-11-24 · agent pilotu (Steward) · Maintenance/reports/weekly_2026-11-24.md · první týdenní běh (doc_index, asset_index, hubs, audit, health) nad lokální kopií vaultu, zpět 26 souborů bez kolizí · predani_pilot_lapikus_knihovnik_unreal P21, P22
- 2026-11-24 · agent pilotu (Steward) · Maintenance/taxonomy_local/asset_sources.yaml · ROUND_MESHES a WOOD_NOMINAL s pevnou category, kameny zdrojem files (CR-037); knihovna 126 assetů, 0 klíčů bez karty · predani_pilot_lapikus_knihovnik_unreal P21, P22
- 2026-11-24 · agent pilotu (Steward) · Assets/ · requested_by: legacy u 82 karet vyrobených před zavedením karet (CR-036); blok *Z kódu* i u kulatiny, hraněného dřeva a kamenů · predani_pilot_lapikus_knihovnik_unreal P21, P22
- 2026-11-24 · agent pilotu (Steward) · Maintenance/queue.md · done T-0042 (own_targets), T-0043 (steward_active) · predani_pilot_lapikus_knihovnik_unreal P21, P22
- 2026-11-24 · Librarian · Lapikus · založen dokument Lore_Lapikus_pudorys (půdorys v romantizované podobě původního hradu pro potřeby hry, podklad k lore) a obrázek Lore_Lapikus_pudorys.svg · chat 2026-11-24 (GameDesigner)
- 2026-11-25 · AssetGenerator · Lapikus · nový prop SM_RuinCampfire (ohniště: kruh kamenů, uhlí, polena se zuhelnatělými středy), slot Face = MI_RuinFace (SLOT_MI, _KINDS), ukázka Ukazka_Ohniste.py, karta v Katalog_props; ostatní meshe beze změny; neověřeno v UE · chat: Jirka 25. 11. 2026 (ohniště)
- 2026-11-25 · Architect · Lapikus · nový návrh navrh_promo_prulet_kamery (narrative): průlet kamery pro promo video, 7 záběrů s UE souřadnicemi, zoomy, postup natočení přes Sequencer a Movie Render Queue, etapa 2 · chat:promo_prulet_kamery
- 2026-11-25 · AssetGenerator · SM_RuinCampfire_A · karta assetu Assets/props/SM_RuinCampfire_A.md (imported, envelope 99 × 99 × 41); sekce Ohniště vrácena z Katalog_props; slot Face do Konvence_assetu kap. Materiály · chat: Jirka 25. 11. 2026 (karta ohniště)

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
