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

- [[predani_brana_prikop_stavitel]] – [[Brana]]
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

- 2026-11-23 · agent pilotu (Steward) · Maintenance/ue/ue_query_assets.py · čtecí skript assetů pro etapu C (54 karet od generated) · predani_pilot_lapikus_knihovnik_unreal P20
- 2026-11-23 · Architect · Brana · navrh sijoveho prikopu, terennich valu, mostniho pilire, lavky a zatarasu pred vychodni branou a predani pro Builder · chat:prikop_pred_branou
- 2026-11-23 · Furnisher · Brana_Straz · Brana_Straz_Vybaveni: 1. navrh vybaveni strazniho stanoviste nad branou v grayboxu (stolicka, prevracena bedna, sada nastroju na sipy, 2 toulce, luk + 4 zastupci sloupku strisky) a karty pozadavku na assety · chat:task
- 2026-11-23 · Furnisher · Lapikus · Brana_Straz_Vybaveni: 1. navrh vybaveni strazniho stanoviste nad branou v grayboxu (stolicka, prevracena bedna, sada nastroju na sipy, 2 toulce, luk + 4 zastupci sloupku strisky) a karty pozadavku na assety · chat:task
- 2026-11-23 · Furnisher · Brana · Brana_Straz_Vybaveni: 1. navrh vybaveni strazniho stanoviste nad branou v grayboxu (stolicka, prevracena bedna, sada nastroju na sipy, 2 toulce, luk + 4 zastupci sloupku strisky) a karty pozadavku na assety · chat:task
- 2026-11-23 · agent pilotu (Steward) · Maintenance/reports/ue_assets.json · čtení assetů z UE (etapa C): current 54, outdated 0, missing 0 · predani_pilot_lapikus_knihovnik_unreal P20
- 2026-11-23 · agent pilotu (Steward) · Assets/ · blok *Stav v UE* (generovaný) ve 43 kartách imported, ruční text nahrazen · predani_pilot_lapikus_knihovnik_unreal P20
- 2026-11-23 · Builder · Brana · Brana_Straz_Podesta: zvýšen počet trámů podesty ze 4 na 5 kulatin (d = -0,20 na Brana_S + 4 v kapsách Brana_V v d = 0,80 / 2,20 / 3,60 / 5,00 m), B_LEVEL na Brana_J d = 0,65-5,30 m, přegenerovány ruin_layout.json a constructions.json; instrukce ke sloupkům stříšky zaneseny do predani_brana_straz_striska_stavitel.md, T-0041 uzavřen · T-0041
- 2026-11-23 · Builder · Lapikus · Brana_Straz_Podesta: zvýšen počet trámů podesty ze 4 na 5 kulatin (d = -0,20 na Brana_S + 4 v kapsách Brana_V v d = 0,80 / 2,20 / 3,60 / 5,00 m), B_LEVEL na Brana_J d = 0,65-5,30 m, přegenerovány ruin_layout.json a constructions.json; instrukce ke sloupkům stříšky zaneseny do predani_brana_straz_striska_stavitel.md, T-0041 uzavřen · T-0041
- 2026-11-23 · Builder · Brana_Straz · Brana_Straz_Podesta: zvýšen počet trámů podesty ze 4 na 5 kulatin (d = -0,20 na Brana_S + 4 v kapsách Brana_V v d = 0,80 / 2,20 / 3,60 / 5,00 m), B_LEVEL na Brana_J d = 0,65-5,30 m, přegenerovány ruin_layout.json a constructions.json; instrukce ke sloupkům stříšky zaneseny do predani_brana_straz_striska_stavitel.md, T-0041 uzavřen · T-0041

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
