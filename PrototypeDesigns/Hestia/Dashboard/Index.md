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
- [[predani_palac_obydli_stavitel]] – [[Palac_Obydli]]

**Otevřené otázky:** do 14 dní 12 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-21 · Builder · Palac · sdílený kód paláce (palac_spec: D_SITE, obydli_stavenisko; vybaveni.py: klíč ref); data kovárny beze změny · predani_palac_obydli_stavitel kap. 4
- 2026-11-21 · Builder · Palac · palac_spec: D_SITE boards.variant (one / two), obydli_stavenisko vrací skupiny; data kovárny beze změny · chat: Jirka 21. 11. 2026 (staveniště jako samostatné objekty, jedna vyšší hranice prken)
- 2026-11-21 · Builder · Lapikus · stav 03_ruin, krok 05, checklist a know-how: staveniště jako samostatné objekty, jedna hranice prken · chat: Jirka 21. 11. 2026 (staveniště jako samostatné objekty, jedna vyšší hranice prken)
- 2026-11-21 · Builder · Palac_Obydli · staveniště: hranice na nádvoří jako samostatné stavby (_Kulatina, _Tramy, _Prkna), všechny kusy samostatné actory, spouštěč Palac_Obydli_Stavenisko_Capture.py; jedna hranice prken o 0,5 m vyšší (75 ks), varianta dvou hranic zachovaná v D_SITE · chat: Jirka 21. 11. 2026 (staveniště jako samostatné objekty, jedna vyšší hranice prken)
- 2026-11-21 · Builder · Lapikus · krok 05: hranice materiálu jako jeden posouvatelný objekt (pile, capture polohy), stav 03_ruin a know-how opraveny · chat: Jirka 21. 11. 2026 (oprava: hranice jako jednotlivé objekty, ne po kusech)
- 2026-11-21 · Builder · Palac · sdílený build: build_constructions._pile, ue_actors.place_ism s pivotem; ostatní stavby beze změny · chat: Jirka 21. 11. 2026 (oprava: hranice jako jednotlivé objekty, ne po kusech)
- 2026-11-21 · Builder · Palac_Obydli · staveniště: každá hranice na nádvoří jeden actor s pivotem (data pile), posun a natočení ukládá Palac_Obydli_Stavenisko_Capture.py; ověřeno jen mimo UE · chat: Jirka 21. 11. 2026 (oprava: hranice jako jednotlivé objekty, ne po kusech)
- 2026-11-21 · Builder · Lapikus · nový mesh SM_RuinLogPeeling (mesh_log.py, tvar peeling), krok 05 a checklist assetů; ostatní meshe beze změny · chat: Jirka 21. 11. 2026 (kozy s rozpracovanou kulatinou)
- 2026-11-21 · Builder · Palac · palac_spec: D_SITE horses; kontrola visení: kus ve vidlici šikmých tyčí · chat: Jirka 21. 11. 2026 (kozy s rozpracovanou kulatinou)
- 2026-11-21 · Builder · Palac_Obydli · staveniště: kozy s rozpracovanou kulatinou Palac_Obydli_Stavenisko_Kozy (S6, jeden objekt), pruhy kůry; prkna přemístěná Jirkou (capture); ověřeno jen mimo UE · chat: Jirka 21. 11. 2026 (kozy s rozpracovanou kulatinou)

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
