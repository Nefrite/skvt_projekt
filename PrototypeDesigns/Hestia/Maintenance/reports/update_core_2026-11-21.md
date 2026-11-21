---
type: report
updated: 2026-11-21
---
# Aktualizace core 2026-11-21

## Souhrn
- Verze: 0.14.2; jen kroky po aktualizaci (`update_core --after-only`, rozsah od 0.14.1).
- Záznamy manifestu: 0.14.2.

## Automatické kroky
- `compose_role`: v pořádku

## Kontroly (dry-run)
- lint: chyby 0, upozornění 0, informace 19
- audit: chyby 0, upozornění 53, informace 40

## Ruční úkoly
_Žádné._

## CR k ověření
- CR_2026-11-21_compose_role_po_kazde_aktualizaci (ověřit v instanci, do *Průběhu* `in_pilot`)

## Přechod 0.14.2 → 0.15.0
- Stav: dokončeno
- Výměna `_core/`: starý core v `_to_delete/_core_0.14.2/`; řádek v `structure_version.md`.
- Záznamy manifestu: 0.14.3, 0.14.4, 0.15.0.

### Automatické kroky
- `doc_index`: v pořádku
  - index beze změny
- `compose_role`: v pořádku
  - změněné kompiláty: 0 z 5

### Kontroly (dry-run)
- lint: chyby 0, upozornění 0, informace 19
- audit: chyby 0, upozornění 53, informace 42

### Ruční úkoly
- `update_core:0.14.4:entrypoint_core_roles` (ve frontě): Srovnat vstupní soubor CLAUDE.md v kořeni dokumentované složky podle šablony _core/templates/tpl_entrypoint.md: profil role core (Curator, Auditor, Librarian) je v Hestia/_core/agents/ (12 kap. 7, 07)
- `update_core:0.15.0:scratch_source_ref` (ve frontě): Doplnit source_ref u scratch z ručního importu (adresa nebo ID položky ve zdroji z řádku Zdroj: v těle), aby je inbox_import poznal jako duplicitu (01 kap. 9.1, 13 kap. 10.12)

### CR k ověření
- CR_2026-11-21_update_core_report_zmena_prirazeni (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR_2026-11-21_update_core_report_a_preruseni (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR_2026-11-21_knihovnik_pripojena_slozka (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR_2026-11-21_ue_query_cesty_ve_skriptu (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR_2026-11-21_inbox_import_notion (ověřit v instanci, do *Průběhu* `in_pilot`)
