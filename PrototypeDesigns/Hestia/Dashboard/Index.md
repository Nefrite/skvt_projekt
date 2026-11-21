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

**Otevřené otázky:** do 14 dní 11 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-21 · agent pilotu · Scratch/Scratch_Unreal_napojeni.md · část 2 (napojení entit) označena jako zpracovaná odkazem na `ue_map.yaml` · předání pilotu P9
- 2026-11-21 · agent pilotu · Maintenance/reports/ue_*.json (15 entit) · první čtení Unrealu (etapa 1, UE 5.8.3, `LapikusPrototypeMap`), `ue_query --import --all`; bloky `## Stav v UE` obnovil `hubs` · předání pilotu P6
- 2026-11-21 · agent pilotu · Brana · otevřená otázka: `depth_structures: 4` bez actorů (zdi u Strazni_Vez) · předání pilotu P6
- 2026-11-21 · agent pilotu · Les_Lapikus · otevřená otázka: v levelu žádné olše podle pravidla · předání pilotu P6
- 2026-11-21 · agent pilotu · Lapikus · otevřená otázka: rampa `Ruin/Rampa` v levelu nenalezena · předání pilotu P6
- 2026-11-21 · agent pilotu · Palac_Kovarna_Vybaveni · otevřená otázka: signály realizace (37 meshů z dat) vs. `depth_structures: 3` · předání pilotu P6
- 2026-11-21 · agent pilotu · Palac_Kovarna_Vybaveni · `depth_structures` 3 → 4 (rozhodnutí GameDesignera po prvním čtení Unrealu) · chat GameDesigner, P6
- 2026-11-21 · agent pilotu · Brana, Les_Lapikus, Lapikus, Palac_Kovarna_Vybaveni · otázky z P6 zodpovězeny a uzavřeny; u Brana nová otázka na hodnotu `depth_structures` · chat GameDesigner, P6
- 2026-11-21 · agent pilotu · Maintenance/queue.md · úkol T-0020: ověřit rozsah a třídu actorů ISM v reportech Unrealu · P6
- 2026-11-21 · agent pilotu · Brana · `depth_structures` 4 → 1 (poloha ve strážní věži; zdi jsou realizací Strazni_Vez, rozhodnutí GameDesignera) · chat GameDesigner, P6

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
