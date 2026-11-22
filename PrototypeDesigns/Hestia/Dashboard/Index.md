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
- [[predani_knihovnik_rozdeleni]]
- [[predani_knihovnik_souhrny]]
- [[predani_palac_obydli_stavitel]] – [[Palac_Obydli]]

**Otevřené otázky:** do 14 dní 13 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-22 · agent pilotu · Handovers/predani_knihovnik_souhrny.md, Handovers/predani_knihovnik_rozdeleni.md · jednorázový úkol Knihovníka P17 (G14a souhrny, G14b/G14c návrhy rozdělení), `for_role: [Librarian]` · pokyn GameDesignera, P17
- 2026-11-22 · Librarian · Les_Lapikus · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Characters · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Lapikus · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Brana_Straz · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Nadvori_Stan · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Palac_Kovarna · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Palac_Kovarna_Vybaveni · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Palac_Obydli · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Vez_Pristresek · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md

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
