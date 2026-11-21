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

- 2026-11-21 · agent pilotu · Palac_Kovarna_Vybaveni · `depth_structures` 3 → 4 (rozhodnutí GameDesignera po prvním čtení Unrealu) · chat GameDesigner, P6
- 2026-11-21 · agent pilotu · Brana, Les_Lapikus, Lapikus, Palac_Kovarna_Vybaveni · otázky z P6 zodpovězeny a uzavřeny; u Brana nová otázka na hodnotu `depth_structures` · chat GameDesigner, P6
- 2026-11-21 · agent pilotu · Maintenance/queue.md · úkol T-0020: ověřit rozsah a třídu actorů ISM v reportech Unrealu · P6
- 2026-11-21 · agent pilotu · Brana · `depth_structures` 4 → 1 (poloha ve strážní věži; zdi jsou realizací Strazni_Vez, rozhodnutí GameDesignera) · chat GameDesigner, P6
- 2026-11-21 · agent pilotu · Brana · otevřená otázka: `status: built` a `brana_spec.py` po změně `depth_structures` na 1 · P6
- 2026-11-21 · agent pilotu · CLAUDE.md · vstupní soubor podle `tpl_entrypoint` (profily rolí core v `Hestia/_core/agents/`), úkol T-0021 · update_core 0.14.4 (ruční úkol), P11
- 2026-11-21 · agent pilotu · Inbox/Guest_on_hunt.md, Inbox/Ranar.md, Inbox/Rad.md, Inbox/Palisada_nad_branou.md · `source_ref` z řádku Zdroj: (adresa stránky v Notion), úkol T-0022 · update_core 0.15.0 (ruční úkol), P11
- 2026-11-21 · agent pilotu · Maintenance/import/notion_2026-11-21.json · export čtyř poznámek Lapikus z Notion (jen čtení zdroje) pro ověření `inbox_import`; dry-run: 4 přeskočeno jako duplicity · P11
- 2026-11-21 · Architect · Palac_Obydli · staveniště a etapa 1 před dokončením domu; hranice sad podle dat, klenba pece base, uhlí pod plotnou final, zamčená base; specifikace Palac_Obydli_Stavenisko (návrh kap. 9); UE vizuálně ověřeno; předání přeřazeno (kap. 4 staveniště, kap. 5 finální stav) · chat:minimum staveniště Palac_Obydli
- 2026-11-21 · Architect · Palac_Obydli · okénko síně zůstává v s = 11,8–12,3 (rozhodnutí Jirky); otázka v předání uzavřena · chat:minimum staveniště Palac_Obydli

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
