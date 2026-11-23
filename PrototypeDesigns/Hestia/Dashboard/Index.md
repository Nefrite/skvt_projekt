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

- 2026-11-23 · Builder · predani_builder_rozdeleni_05 · předání archivováno · predani_builder_rozdeleni_05
- 2026-11-23 · Steward · structure_log · T-0028: 9 záznamů cr: – → cr: none (8×) a cr: CR-015_ue_query_cesty_ve_skriptu (1×), nic k exportu (schválil GameDesigner) · T-0028
- 2026-11-23 · Steward · ue_map · placeholder_ignore: /Engine/BasicShapes/Cube.Cube (CR-024, schválil GameDesigner); ue_query_all.py znovu vygenerován · P18
- 2026-11-23 · Architect · Palac_Obydli · navrh_palac_obydli_stred: kap. 4 sjednocená s postaveným stavem a rozhodnutími z kap. 0.7 (vrstva „platí přednostně“ zrušena, kap. 0.5–0.6 zrušeny, 0.7 jen zamčená base a hranice sad, okap k západu do sudu, dřevo raw); navrh_palac_obydli: validity superseded; navrh_palac_obydli_stavenisko: rozhodnutí o hranicích, S5 a S6 z kap. 0.7 · chat:sjednoceni_navrhu_domu
- 2026-11-23 · Architect · Palac_Obydli · navrh_palac_obydli_stred: žlab přes Palac_pricka_1 do sudu v západní místnosti (s ≈ 9,7), lemování kolem komína potvrzeno; podnět P-0001 (G14 a status rejected) · chat:sjednoceni_navrhu_domu
- 2026-11-23 · Architect · Lapikus · CHECKLIST_assets_navrhy: odkaz na návrh domu přečíslován po rozdělení navrh_palac_obydli_stred (kap. 2, 3, etapy 0.1) · chat:rozdeleni_navrhu_domu
- 2026-11-23 · Architect · Guesthouse · navrh_guesthouse_vybaveni: odkaz na návrh domu přečíslován po rozdělení navrh_palac_obydli_stred (pec → navrh_palac_obydli_pec) · chat:rozdeleni_navrhu_domu
- 2026-11-23 · Architect · Palac_Kovarna · navrh_palac_kovarna: odkaz na návrh domu přečíslován po rozdělení navrh_palac_obydli_stred (kap. 0.2a → kap. 3) · chat:rozdeleni_navrhu_domu
- 2026-11-23 · Architect · Palac_Kovarna_Vybaveni · navrh_palac_kovarna: odkaz na návrh domu přečíslován po rozdělení navrh_palac_obydli_stred (kap. 0.2a → kap. 3) · chat:rozdeleni_navrhu_domu
- 2026-11-23 · Architect · Palac_Obydli · navrh_palac_obydli_stred rozdělen (G14c, varianta A): plán po etapách → navrh_palac_obydli_etapy (čísla 0.1, 0.3, 0.4, 0.7 zachována), pec → navrh_palac_obydli_pec (kap. 4.6); výchozí stav 0.2/0.2a sloučen do kap. 2 a 3, kap. 5, 6 a 8 bez duplicit; odkazy ve stavenisko a stav_palac_obydli · chat:rozdeleni_navrhu_domu

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
