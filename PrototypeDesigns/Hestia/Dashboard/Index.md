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
- [[predani_guesthouse_kamna_stavitel]] – [[Guesthouse]]
- [[predani_palac_obydli_stavitel]] – [[Palac_Obydli]]

**Otevřené otázky:** do 14 dní 13 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-21 · Builder · Palac · sdílený build: build_constructions._pile, ue_actors.place_ism s pivotem; ostatní stavby beze změny · chat: Jirka 21. 11. 2026 (oprava: hranice jako jednotlivé objekty, ne po kusech)
- 2026-11-21 · Builder · Palac_Obydli · staveniště: každá hranice na nádvoří jeden actor s pivotem (data pile), posun a natočení ukládá Palac_Obydli_Stavenisko_Capture.py; ověřeno jen mimo UE · chat: Jirka 21. 11. 2026 (oprava: hranice jako jednotlivé objekty, ne po kusech)
- 2026-11-21 · Builder · Lapikus · nový mesh SM_RuinLogPeeling (mesh_log.py, tvar peeling), krok 05 a checklist assetů; ostatní meshe beze změny · chat: Jirka 21. 11. 2026 (kozy s rozpracovanou kulatinou)
- 2026-11-21 · Builder · Palac · palac_spec: D_SITE horses; kontrola visení: kus ve vidlici šikmých tyčí · chat: Jirka 21. 11. 2026 (kozy s rozpracovanou kulatinou)
- 2026-11-21 · Builder · Palac_Obydli · staveniště: kozy s rozpracovanou kulatinou Palac_Obydli_Stavenisko_Kozy (S6, jeden objekt), pruhy kůry; prkna přemístěná Jirkou (capture); ověřeno jen mimo UE · chat: Jirka 21. 11. 2026 (kozy s rozpracovanou kulatinou)
- 2026-11-21 · Furnisher · Ostroh · ostroh_spec.py: GH_* a guesthouse_vybaveni() pro vybaveni Guesthouse (03 a 05 beze zmeny) · chat: Jirka 21. 11. 2026 (vybaveni Guesthouse)
- 2026-11-21 · Furnisher · Lapikus · 06_furnishing: skupina Guesthouse_Vybaveni, spoustece vybaveni/Guesthouse(_Capture).py, graybox material zrlib/config.py MAT_GRAYBOX, kontrola vybaveni v run_checks ostroh; CHECKLIST 6.8, know-how props · chat: Jirka 21. 11. 2026 (vybaveni Guesthouse)
- 2026-11-21 · Furnisher · Guesthouse · vybaveni 06 graybox (9 kusu, MI_PrototypeGrid_Gray): postel, stul, stolicka, truhla, prazdne stojany na brneni a zbrane, regal, drevo, zastupce kamen; polohy z levelu (Jirka); navrh, stav, predani kamen staviteli; overeno mimo UE a v levelu Jirkou · chat: Jirka 21. 11. 2026 (vybaveni Guesthouse)
- 2026-11-21 · Furnisher · Guesthouse · rozhodnuti Jirky: nove meshe truhly se zamkem a hromadky dreva, kamenna dlazba pod kamny (predani staviteli); uzavrene 3 otazky · chat: Jirka 21. 11. 2026 (vybaveni Guesthouse, rozhodnuti)
- 2026-11-21 · Furnisher · Lapikus · CHECKLIST 6.8: SM_RuinChestLocked, SM_RuinWoodpileSmall, dlazba pod kamny · chat: Jirka 21. 11. 2026 (vybaveni Guesthouse, rozhodnuti)

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
