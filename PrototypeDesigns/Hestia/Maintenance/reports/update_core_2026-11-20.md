---
type: report
updated: 2026-11-20
---
# Aktualizace core 2026-11-20

## Souhrn
- Verze: 0.10.2 → 0.14.0; starý core v `_to_delete/_core_0.10.2/`, řádek v `structure_version.md`.
- Záznamy manifestu: 0.10.3, 0.11.0, 0.12.0, 0.13.0, 0.14.0.

## Automatické kroky
- `asset_index`: v pořádku
- `hubs`: v pořádku
- `doc_index`: v pořádku
- `compose_role`: v pořádku

## Kontroly (dry-run)
- lint: chyby 0, upozornění 0, informace 19
- audit: chyby 0, upozornění 53, informace 40

## Ruční úkoly
- `update_core:0.12.0:glossary_header` (ve frontě): Převést záhlaví tabulky Pojmy projektu v Dashboard/Glossary.md na pět sloupců: Pojem | Význam | Hlavní dokument nebo hub | Aliasy | Zakázané varianty (07 kap. 19)
- `update_core:0.14.0:core_source` (ve frontě): Doplnit do Maintenance/config.yaml klíč core_source (cesta k repozitáři HearthLore relativně k vaultu); další aktualizace pak update_core --latest (13 kap. 4, 10.6)

## CR k ověření
- CR_2026-11-19_jmena_roli_anglicky (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR_2026-11-19_knowhow_tematicke_pasti (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR_2026-11-19_asset_index_alias_entity (ověřit v instanci, do *Průběhu* `in_pilot`)
