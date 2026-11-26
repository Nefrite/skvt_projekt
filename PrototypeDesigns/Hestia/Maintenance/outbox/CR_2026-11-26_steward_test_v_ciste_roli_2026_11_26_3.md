---
type: change_request
cr_status: new
source_instance: lapikus
hestia_version: "0.26.0"
area: process
gd_relevance:            # direct | indirect | none (11, kap. 2)
structure_log: ["2026-11-26 | friction | Steward (test v čisté roli 2026-11-26): `outbox/report_2026-11-26.md` uvádí u `export_cr` „nic k exportu“, ale `structure_log` měl záznam 2026-11-25 (`sequence`) s prázdnou buňkou `cr` a `export_cr` v dry-runu ho nabízí jako CR; hlášení vzniklo bez nového běhu `export_cr` (P-0023; doklad: `Maintenance/outbox/report_2026-11-26.md` 2026-11-26)"]
spec_refs: []
released_in:
updated: 2026-11-26
---
# Steward (test v čisté roli 2026-11-26): `outbox/report_2026-11-26.md` uvádí u `export_cr` „nic k exportu“, ale `structure_log` měl záznam 2026-11-25 (`sequence`) s prázdnou buňkou `cr` a `export_cr` v dry-runu ho nabízí jako CR; hlášení vzniklo bez nového běhu `export_cr` (P-0023; doklad: `Maintenance/outbox/report_2026-11-26.md` 2026-11-26)

> **Předání do HearthLore:** soubor se neodesílá skriptem. Uveď ho v hlášení pro HearthLore, nebo ho předá člověk; v instanci ho nepřejmenovávej, nečísluj ani nekopíruj do HearthLore. Zaeviduje ho agent HearthLore: číslo, jméno `CR-NNN_<short_name>`, původní jméno v `source_id` (11 kap. 3).

## Co se stalo
Steward (test v čisté roli 2026-11-26): `outbox/report_2026-11-26.md` uvádí u `export_cr` „nic k exportu“, ale `structure_log` měl záznam 2026-11-25 (`sequence`) s prázdnou buňkou `cr` a `export_cr` v dry-runu ho nabízí jako CR; hlášení vzniklo bez nového běhu `export_cr` (P-0023; doklad: `Maintenance/outbox/report_2026-11-26.md` 2026-11-26)

Dopad podle záznamu: hlášení pro HearthLore tvrdí neplatný stav CR

Záznam `structure_log` z 2026-11-26 (kategorie `friction`), instance `lapikus`, core 0.26.0.

## Návrh
`hearthlore_report` krok 2: prázdná buňka `cr` = kandidát na CR (`export_cr` ho vyexportuje); před každým hlášením znovu spustit `export_cr` (dry-run) a výsledek opsat; `health` může prázdné buňky `cr` počítat

## Dopad
<!-- doplní Curator nebo člověk před odesláním -->

## Alternativy
<!-- doplní Curator nebo člověk před odesláním -->

## Průběh

| datum | stav | kdo | poznámka |
|---|---|---|---|
| 2026-11-26 | new | export_cr | ze structure_log 2026-11-26 |
