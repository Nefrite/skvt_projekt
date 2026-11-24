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
| [[Lapikus_Region]] | 0 % (1) | 71 % (3) | 0 % (0) | bez cíle | 0 % (0) | bez cíle |

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

- 2026-11-24 · Builder · Brana_Straz · Brana: sijovy prikop, celni valy, uvoz a unikova rampa (gen_moat.py), Brana_Pilir a Brana_Opera (03), Brana_Most_Kamen, Brana_Most a Brana_Zataras (05), stav_brana zalozen; T-0036 uzavren · predani_brana_prikop_stavitel
- 2026-11-24 · Builder · Lapikus_Region · Brana: sijovy prikop, celni valy, uvoz a unikova rampa (gen_moat.py), Brana_Pilir a Brana_Opera (03), Brana_Most_Kamen, Brana_Most a Brana_Zataras (05), stav_brana zalozen; T-0036 uzavren · predani_brana_prikop_stavitel
- 2026-11-24 · Builder · Brana · Brana: zruseny celni terenni valy pred sijovym prikopem (rozhodnuti GameDesignera 2026-11-24, takticka vyhoda utocniku); pregenerovan vyskopis, terrain_from_level.json, ruin_layout.json, constructions.json a nahledy · chat:zruseni_valu_brana
- 2026-11-24 · Builder · Strazni_Vez · Brana: zruseny celni terenni valy pred sijovym prikopem (rozhodnuti GameDesignera 2026-11-24, takticka vyhoda utocniku); pregenerovan vyskopis, terrain_from_level.json, ruin_layout.json, constructions.json a nahledy · chat:zruseni_valu_brana
- 2026-11-24 · Builder · Hradby_a_Brana · Brana: zruseny celni terenni valy pred sijovym prikopem (rozhodnuti GameDesignera 2026-11-24, takticka vyhoda utocniku); pregenerovan vyskopis, terrain_from_level.json, ruin_layout.json, constructions.json a nahledy · chat:zruseni_valu_brana
- 2026-11-24 · Builder · Lapikus_Region · Brana: zruseny celni terenni valy pred sijovym prikopem (rozhodnuti GameDesignera 2026-11-24, takticka vyhoda utocniku); pregenerovan vyskopis, terrain_from_level.json, ruin_layout.json, constructions.json a nahledy · chat:zruseni_valu_brana
- 2026-11-24 · Builder · Lapikus · Brana: zruseny celni terenni valy pred sijovym prikopem (rozhodnuti GameDesignera 2026-11-24, takticka vyhoda utocniku); pregenerovan vyskopis, terrain_from_level.json, ruin_layout.json, constructions.json a nahledy · chat:zruseni_valu_brana
- 2026-11-24 · Builder · Brana · Brana: sijovy prikop bez valu, mostni pilir, opera, lavka Brana_Most a zataras Brana_Zataras overeny v UE (GameDesigner 2026-11-24); depth_structures 3 -> 4, predani archivovano · predani_brana_prikop_stavitel
- 2026-11-24 · Builder · Lapikus · Brana: sijovy prikop bez valu, mostni pilir, opera, lavka Brana_Most a zataras Brana_Zataras overeny v UE (GameDesigner 2026-11-24); depth_structures 3 -> 4, predani archivovano · predani_brana_prikop_stavitel
- 2026-11-24 · Builder · Handovers/predani_brana_prikop_stavitel.md · předání archivováno · predani_brana_prikop_stavitel

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
