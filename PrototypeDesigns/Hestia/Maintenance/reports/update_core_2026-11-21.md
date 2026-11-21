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

## Přechod 0.15.0 → 0.16.0
- Stav: dokončeno
- Výměna `_core/`: starý core v `_to_delete/_core_0.15.0/`; řádek v `structure_version.md`.
- Záznamy manifestu: 0.16.0.

### Automatické kroky
- `compose_role`: v pořádku
  - změněné kompiláty: 5 z 5

### Kontroly (dry-run)
- lint: chyby 4, upozornění 0, informace 19
- audit: chyby 4, upozornění 57, informace 42

### Ruční úkoly
- `update_core:0.16.0:role_base` (ve frontě): Srovnat profily projektových rolí se základem 0.16.0 (profil kontrakt zpřísňuje, neruší (zákazy zápisu jen pro kód, data a assety); zápis do Docs/ je dokumentace domény podle 07 kap. 2, existující dokumentace entity se doplňuje, předání se píše z role (12 kap. 2.1, 8); tpl_role s role_base); po schválení GameDesignerem nastavit role_base: 0.16.0 a spustit compose_role (12 kap. 2.1, 13 kap. 10.6a)

### Základ projektových rolí
- Změna v 0.16.0: profil kontrakt zpřísňuje, neruší (zákazy zápisu jen pro kód, data a assety); zápis do Docs/ je dokumentace domény podle 07 kap. 2, existující dokumentace entity se doplňuje, předání se píše z role (12 kap. 2.1, 8); tpl_role s role_base
- Rozdíl `tpl_role`:

```diff
--- tpl_role (starý core)
+++ tpl_role (nový core)
@@ -6,9 +6,13 @@
 context: []             # dokumenty, které role načítá vždy (např. "[[Lore_<Prototyp>]]")
 knowhow_tags: []
 combines: []            # role, se kterými se profil skládá
+role_base: ""   # verze core z _core/VERSION, se kterou je profil srovnaný se základem rolí; doplní, kdo profil zakládá (12 kap. 2.1)
 ---
 <!-- Jen účel a hranice, vstupy a výstupy, postup role, styl hlášení (12, kap. 2.1).
-     Žádné lore, stav, podklady, popis kódu, pasti, konvence ani pravidla návrhu. -->
+     Žádné lore, stav, podklady, popis kódu, pasti, konvence ani pravidla návrhu.
+     Profil kontrakt zpřísňuje, neruší: výsledek své práce role zapisuje do vaultu (princip 12, task_close);
+     zákazy zápisu jen pro kód, data a assety. Zápis do Docs/ je dokumentace domény podle 07 kap. 2, ne výstup role; existující dokumentaci entity
+     doplň, nový dokument jen když žádný není. Předání (Handovers/) píšeš z role. -->
 # {{title}}
 
 ## Co děláš a co ne
```

- Profily nesrovnané se základem 0.16.0 (ruční úkol `role_base`):
  - `Roles/Architect.md`: role_base chybí
  - `Roles/Builder.md`: role_base chybí
  - `Roles/Furnisher.md`: role_base chybí
  - `Roles/GameDesign.md`: role_base chybí

### CR k ověření
- CR_2026-11-21_zaklad_roli_v_instanci (ověřit v instanci, do *Průběhu* `in_pilot`)
