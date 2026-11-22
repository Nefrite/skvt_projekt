---
type: reference
validity: valid
updated: 2026-11-22
---
# Pravidla zápisu (výchozí, core)

Kdo smí co zapisovat ve vaultu. Výchozí pravidla core podle zadání 05, kap. 4–5 a 12, kap. 8. Instance je doplňuje v `Maintenance/write_rules_local.md` (např. které role smějí měnit `target_*`, chráněné soubory); lokální doplněk pravidla zpřísňuje nebo upřesňuje, core pravidla neruší.

## Zásady zápisu

- Platný text přepisuješ jen jako důsledek rozhodnutí GameDesignera nebo výsledku tasku ve své oblasti (12 kap. 6.1, `nahradit:`).
- Profil kontrakt zpřísňuje, neruší: výsledek své práce zapíšeš do vaultu vždy; zákazy zápisu v profilu platí pro kód, data a assety (12 kap. 2.1).
- Zápis do `Docs/` je dokumentace domény podle šablony (sekce, `depth`), ne výstup role: neříká, kdo psal a pro koho. Před zápisem najdi existující dokumentaci entity a doplň ji; nový dokument jen když žádný není. Předání (`Handovers/`) píšeš z role (12 kap. 8).
- Přesun a přejmenování jen se schválením; mazání jen přesunem do `_to_delete/` na pokyn (05 kap. 5).
- Problém s Hestií jako nástrojem neřešíš CR ani zápisem do `structure_log.md`: modul `hestia_feedback` (12 kap. 4.5).

## Matice pravomocí

| Oblast | Člověk (GameDesigner) | Curator | Auditor | Projektové role |
|---|---|---|---|---|
| `_core/` | jen `update_core` | ✘ | ✘ | ✘ |
| Tělo dokumentů v `Docs/` | ✔ | ✘ | ✘ | ✔ (své role, přenos z předání) |
| `Handovers/`: založení | ✔ | ✘ | ✘ | ✔ (`handover_out`, orchestrační agent) |
| `Handovers/`: archivace po zapracování (`archived`, přesun do `_archive/`) | ✔ | ✘ | ✘ | ✔ (kdo task dokončil) |
| Sekce `## Otevřené otázky` (ruční část) | ✔ | ✘ | ✘ | ✔ (přidat, uzavřít) |
| `KnowHow/` | ✔ | metadata, sloučení po schválení | ✘ | ✔ (kdo věc ověřil) |
| Frontmatter dokumentů | ✔ | ✔ | ✘ | ✔ (`updated`, `validity`) |
| `Inbox/`, `Scratch/` | ✔ | ✔ (metadata importu, nové soubory z importu) | ✘ | ✔ (nové scratch jen na pokyn GameDesignera) |
| Hub: `kind`, `parent`, `located_in`, `derived_from`, `alternative_to` | ✔ | ✔ (po schválení návrhu) | ✘ | ✘ |
| Hub: `depth_*`, `status` | ✔ | ✔ | ✘ | ✔ (po své práci) |
| Hub: `target_*` | ✔ | navrhuje | ✘ | ✔ (určená role, např. game design; zápis do `changes.md`) |
| Generované sekce hubů | – | ✔ (skript `hubs`) | ✘ | ✘ |
| `taxonomy_local/`, `structure_version` | schvaluje | ✔ | ✘ | ✘ |
| `reports/`, `queue.md` | ✔ | ✔ | ✔ | jen podnět pro Hestii do `queue.md` (`proposal`, `code: hestia`, 12 kap. 4.5) |
| `changes.md`, `structure_log.md` (jen připisovat na konec) | ✔ | ✔ (i podněty rolí z `queue.md`) | ✔ (návrhy) | ✔ (`changes.md`; `structure_log.md` ✘, podnět přes `queue.md`) |
| `asset_index.md` | – | ✔ (skript) | ✘ | ✘ |
| `doc_index.json`, `context/` (index dokumentů, balíčky kontextu) | – | ✔ (skripty `doc_index`, `hubs`, `compose_context`) | ✔ (skript `audit` obnoví index) | ✘ |
| `ue/`, `reports/ue_*.json` (čtení Unrealu, jen čtecí dotazy core) | ✔ (spouští skript v editoru) | ✔ (skript `ue_query`) | ✔ (skript `ue_query`) | ✔ (skript `ue_query`, role s `ue_lookup` v profilu) |
| `outbox/` (change requesty) | odesílá | ✔ (připravuje) | ✘ | ✘ (podnět přes `queue.md`, 12 kap. 4.5) |
| `Maintenance/import/` (soubory výměny importu) | ✔ | ✔ (modul `inbox_import`; zůstávají jako záznam původu) | ✘ | ✘ |
| `Roles/` (profily, lokální moduly) | ✔ | ✘ | ✘ | ✘ |
| `Roles/_compiled/` | – | ✔ (skript `compose_role`) | ✘ | ✘ |
| Kód, data, assety projektu | ✔ | ✘ | ✘ | ✔ (stavitel, furnisher …) |
| Přesun a přejmenování | ✔ | po schválení | ✘ | ✘ |
| Mazání | ✔ | ✘ (jen `_to_delete`) | ✘ | ✘ (jen `_to_delete`) |

## Knihovník (`Librarian`, 05 kap. 3.2a)

| Oblast | Knihovník |
|---|---|
| Tělo dokumentů v `Docs/`, master lore | ✔ doslovná textace GameDesignera přímo; přeformulování, sloučení a zkrácení po schválení (12 kap. 3b.2) |
| Založení dokumentu, frontmatter zapisovaných dokumentů (`updated`, `validity`) | ✔ na pokyn k zápisu |
| `Dashboard/Glossary.md` | ✔ (změna významu = změna kánonu) |
| `Inbox/`, `Scratch/` | ✔ *Předzpracování*, `intake`; přesun do `Scratch/` a do `_to_delete/` podle rozhodnutí GameDesignera v třídění |
| Sekce `## Otevřené otázky` | ✔ přidat; uzavřít po zapracování odpovědi |
| `queue.md` | ✔ položka k rozporu mezi dokumenty (pro Auditora); podnět pro Hestii (`proposal`, `code: hestia`, 12 kap. 4.5) |
| `structure_log.md`, `outbox/` | ✘ (kolize pojmů a chybějící náležitosti jako podnět přes `queue.md`, zadání 0.18) |
| `ue/`, `reports/ue_*.json` | ✔ skript `ue_query` (jen čtení Unrealu) |
| `changes.md` | ✔ jen připisovat na konec (příznak **změna kánonu**: sloupec *co se změnilo* začíná `změna kánonu:`), skriptem `task_close` po vlastním zápisu (12 kap. 3b.1, zadání 0.18.1) |
| Ostatní oblasti matice | ✘ |

Projektová role zapisuje tělo dokumentů jen ve své oblasti (včetně přenosu z předání), do `## Otevřené otázky` přidává a uzavírá položky, nový scratch zakládá jen na pokyn GameDesignera, do `changes.md` jen připisuje na konec a do `queue.md` jen podnět pro Hestii (change request nezakládá, 12 kap. 4.5 a 8). Orchestrační agent má práva projektové role v rozsahu zápisu Hestia.

## Schvalování

| Zásah | Schválení člověkem |
|---|---|
| Generované věci: sekce hubů, `asset_index`, reporty, fronta, logy | ne, bez ohledu na počet |
| Metadata (frontmatter) v ≤ 10 souborech | ne, zápis do `changes.md` |
| Metadata ve více než 10 souborech (skript, migrace) | ano, seznam změn z dry-run |
| Přesun, přejmenování, přesun do `_to_delete` | ano, vždy, i u jednoho souboru (výjimka: archivace zapracovaného předání, zadání 12, kap. 5) |
| Změna těla dokumentu agentem údržby | nepovoleno (jen projektové role ve své oblasti) |
| Provedení návrhu (`split`, `reparent`, `promote`, `derive`, `rename`), `taxonomy_local` | ano |
| `target_*` | ne u člověka a určené role; Curator jen navrhuje |
| `update_core`, migrace u MAJOR verze | ano |

- Skripty běží jako dry-run; zápis vyžaduje `--apply`.
- Před hromadným zásahem čistý git (commit). Commity dělá lidský správce; agenti necommitují, pokud o to člověk nepožádá.
- Duplicita (G8) se neřeší mazáním, jen návrhem sloučení. Zavržené věci mají `status: rejected` a důvod.
- Change request odesílá do HearthLore člověk (nebo agent na jeho pokyn).
- Platný text se přepisuje jen jako důsledek rozhodnutí GameDesignera nebo výsledku tasku ve vlastní oblasti role.

## Chráněné soubory

Soubory, které agenti ani skripty nepřepisují (např. ruční úpravy z editoru, které skript nezná), jsou v `Maintenance/config.yaml` v klíči `protected_files` a s důvodem v `Maintenance/write_rules_local.md`. Postup při zápisu: modul `file_safety`.
