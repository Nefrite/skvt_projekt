---
type: reference
validity: valid
updated: 2026-11-17
---
# Pravidla zápisu (výchozí, core)

Kdo smí co zapisovat ve vaultu. Výchozí pravidla core podle zadání 05, kap. 4–5 a 12, kap. 8. Instance je doplňuje v `Maintenance/write_rules_local.md` (např. které role smějí měnit `target_*`, chráněné soubory); lokální doplněk pravidla zpřísňuje nebo upřesňuje, core pravidla neruší.

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
| `Inbox/`, `Scratch/` | ✔ | ✔ (metadata, `intake`, nové soubory z importu) | ✘ | ✔ (nové scratch jen na pokyn GameDesignera) |
| Hub: `kind`, `parent`, `located_in`, `derived_from`, `alternative_to` | ✔ | ✔ (po schválení návrhu) | ✘ | ✘ |
| Hub: `depth_*`, `status` | ✔ | ✔ | ✘ | ✔ (po své práci) |
| Hub: `target_*` | ✔ | navrhuje | ✘ | ✔ (určená role, např. game design; zápis do `changes.md`) |
| Generované sekce hubů | – | ✔ (skript `hubs`) | ✘ | ✘ |
| `taxonomy_local/`, `structure_version` | schvaluje | ✔ | ✘ | ✘ |
| `reports/`, `queue.md` | ✔ | ✔ | ✔ | ✘ |
| `changes.md`, `structure_log.md` (jen připisovat na konec) | ✔ | ✔ | ✔ (návrhy) | ✔ (`changes.md`) |
| `asset_index.md` | – | ✔ (skript) | ✘ | ✘ |
| `outbox/` (change requesty) | odesílá | ✔ (připravuje) | ✘ | ✘ |
| `Roles/` (profily, lokální moduly) | ✔ | ✘ | ✘ | ✘ |
| `Roles/_compiled/` | – | ✔ (skript `compose_role`) | ✘ | ✘ |
| Kód, data, assety projektu | ✔ | ✘ | ✘ | ✔ (stavitel, furnisher …) |
| Přesun a přejmenování | ✔ | po schválení | ✘ | ✘ |
| Mazání | ✔ | ✘ (jen `_to_delete`) | ✘ | ✘ (jen `_to_delete`) |

Projektová role zapisuje tělo dokumentů jen ve své oblasti (včetně přenosu z předání), do `## Otevřené otázky` přidává a uzavírá položky, nový scratch zakládá jen na pokyn GameDesignera a do `changes.md` jen připisuje na konec. Orchestrační agent má práva projektové role v rozsahu zápisu Hestia.

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
