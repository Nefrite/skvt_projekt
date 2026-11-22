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

- 2026-11-22 · Librarian · Palac_Kovarna · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Palac_Kovarna_Vybaveni · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Palac_Obydli · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Vez_Pristresek · doplněna sekce Souhrn (G14a) · Handovers/predani_knihovnik_souhrny.md
- 2026-11-22 · Librarian · Palac_Kovarna · kap. 0 návrhu přesunuta do stav_palac_kovarna (G14b) · Handovers/predani_knihovnik_rozdeleni.md
- 2026-11-22 · Librarian · Palac_Kovarna_Vybaveni · kap. 0 návrhu kovárny přesunuta do stav_palac_kovarna (G14b) · Handovers/predani_knihovnik_rozdeleni.md
- 2026-11-22 · Librarian · Vez_Pristresek · nový stav_vez_pristresek; kap. 3 návrhu přesunuta do navrh_vez_skody (G14b) · Handovers/predani_knihovnik_rozdeleni.md
- 2026-11-22 · Librarian · Vez · nový navrh_vez_skody (škody z dobývání, z navrh_vez_pristresek kap. 3) · Handovers/predani_knihovnik_rozdeleni.md
- 2026-11-22 · Librarian · Lapikus · Zricenina_03_ruin_stav: kapitoly kovárna, dům, brána a věž nahrazeny odkazy na stavy (G14b) · Handovers/predani_knihovnik_rozdeleni.md
- 2026-11-22 · Librarian · Palac_Obydli · navrh_palac_obydli_stred rozdělen: postavené do stav_palac_obydli, kap. 9 do navrh_palac_obydli_stavenisko, 0.5a/0.5b do kap. 4, kap. 3 odpadla, připravenost odkazem na CHECKLIST; stav doplněn z předání staviteli (G14b, G14c) · Handovers/predani_knihovnik_rozdeleni.md

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
