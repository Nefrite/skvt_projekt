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

**Otevřené otázky:** do 14 dní 16 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-24 · Builder · Lapikus · Brana: sijovy prikop bez valu, mostni pilir, opera, lavka Brana_Most a zataras Brana_Zataras overeny v UE (GameDesigner 2026-11-24); depth_structures 3 -> 4, predani archivovano · predani_brana_prikop_stavitel
- 2026-11-24 · Builder · Handovers/predani_brana_prikop_stavitel.md · předání archivováno · predani_brana_prikop_stavitel
- 2026-11-24 · Builder · Lapikus · Nový typ tent (zr_stavby/stan.py), stavba Nadvori_Stan (stage=site, pile=True) u Hradba_Z_S mezi Guesthouse a prkny s vchodem na jih a vybavení Nadvori_Stan_Vybaveni (06_furnishing, stage=site: 1 lůžko, truhlička a vak uvnitř, špalek venku); entita Nadvori_Stan převedena na built a založen stav_nadvori_stan · chat:T-0035
- 2026-11-24 · Builder · Nadvori_Stan · Nový typ tent (zr_stavby/stan.py), stavba Nadvori_Stan (stage=site, pile=True) u Hradba_Z_S mezi Guesthouse a prkny s vchodem na jih a vybavení Nadvori_Stan_Vybaveni (06_furnishing, stage=site: 1 lůžko, truhlička a vak uvnitř, špalek venku); entita Nadvori_Stan převedena na built a založen stav_nadvori_stan · chat:T-0035
- 2026-11-24 · Builder · Lapikus · Oprava ue_assets.mesh_slots() pro jednoslotové LIB_MESHES (SM_RuinCanvasTent, SM_RuinRope, SM_RuinLashing): pile actor Nadvori_Stan nyní správně přiřadí MI_RuinCanvas a MI_RuinRope místo MI_RuinWood · chat:T-0035-fix-canvas-mat
- 2026-11-24 · Builder · Nadvori_Stan · Oprava ue_assets.mesh_slots() pro jednoslotové LIB_MESHES (SM_RuinCanvasTent, SM_RuinRope, SM_RuinLashing): pile actor Nadvori_Stan nyní správně přiřadí MI_RuinCanvas a MI_RuinRope místo MI_RuinWood · chat:T-0035-fix-canvas-mat
- 2026-11-24 · Builder · Lapikus · Sjednocení článků lan STAN_ROPE na d=0,015 m a link=1,0 m (stejně jako Vez_Pristresek): 8 článků 80–92 cm místo 32 stlačených 20–23 cm, celkem 33 dílců · chat:T-0035-ropes
- 2026-11-24 · Builder · Nadvori_Stan · Sjednocení článků lan STAN_ROPE na d=0,015 m a link=1,0 m (stejně jako Vez_Pristresek): 8 článků 80–92 cm místo 32 stlačených 20–23 cm, celkem 33 dílců · chat:T-0035-ropes
- 2026-11-24 · Builder · Lapikus · Nadvori_Stan a Nadvori_Stan_Vybaveni vizuálně ověřeny v UE (GameDesigner 2026-11-24); depth_structures 3 -> 4 · chat:T-0035-ue-ok
- 2026-11-24 · Builder · Nadvori_Stan · Nadvori_Stan a Nadvori_Stan_Vybaveni vizuálně ověřeny v UE (GameDesigner 2026-11-24); depth_structures 3 -> 4 · chat:T-0035-ue-ok

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
