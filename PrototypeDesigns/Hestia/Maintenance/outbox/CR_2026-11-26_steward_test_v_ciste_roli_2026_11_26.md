---
type: change_request
cr_status: new
source_instance: lapikus
hestia_version: "0.26.0"
area: process
gd_relevance:            # direct | indirect | none (11, kap. 2)
structure_log: ["2026-11-26 | missing | Steward (test v čisté roli 2026-11-26): kompilát Stewarda vynechává moduly `instance_health` a `hearthlore_report` („jen režim vault“), ale hlavička neříká, že se ve vaultu čtou z `_core/agents/modules/`; modul `instance_health` neuvádí práh stáří reportů Unrealu (klíč `ue_report_days` našel až v `_core/taxonomy/defaults.yaml`) ani které příkazy (`health`, `weekly` bez `--apply`, s `--work-copy`) nikdy nezapisují do vaultu, takže je test „jen čtení“ nespustil (P-0020; doklad: `Roles/_compiled/Steward_compiled.md` 2026-11-26)"]
spec_refs: []
released_in:
updated: 2026-11-26
---
# Steward (test v čisté roli 2026-11-26): kompilát Stewarda vynechává moduly `instance_health` a `hearthlore_report` („jen režim vault“), ale hlavička neříká, že se ve vaultu čtou z `_core/agents/modules/`; modul `instance_health` neuvádí práh stáří reportů Unrealu (klíč `ue_report_days` našel až v `_core/taxonomy/defaults.yaml`) ani které příkazy (`health`, `weekly` bez `--apply`, s `--work-copy`) nikdy nezapisují do vaultu, takže je test „jen čtení“ nespustil (P-0020; doklad: `Roles/_compiled/Steward_compiled.md` 2026-11-26)

> **Předání do HearthLore:** soubor se neodesílá skriptem. Uveď ho v hlášení pro HearthLore, nebo ho předá člověk; v instanci ho nepřejmenovávej, nečísluj ani nekopíruj do HearthLore. Zaeviduje ho agent HearthLore: číslo, jméno `CR-NNN_<short_name>`, původní jméno v `source_id` (11 kap. 3).

## Co se stalo
Steward (test v čisté roli 2026-11-26): kompilát Stewarda vynechává moduly `instance_health` a `hearthlore_report` („jen režim vault“), ale hlavička neříká, že se ve vaultu čtou z `_core/agents/modules/`; modul `instance_health` neuvádí práh stáří reportů Unrealu (klíč `ue_report_days` našel až v `_core/taxonomy/defaults.yaml`) ani které příkazy (`health`, `weekly` bez `--apply`, s `--work-copy`) nikdy nezapisují do vaultu, takže je test „jen čtení“ nespustil (P-0020; doklad: `Roles/_compiled/Steward_compiled.md` 2026-11-26)

Dopad podle záznamu: kontrola zdraví jen ručně, nejistota o hranici zápisu

Záznam `structure_log` z 2026-11-26 (kategorie `missing`), instance `lapikus`, core 0.26.0.

## Návrh
hlavička kompilátu: vynechané moduly čti ve vaultu z `_core/agents/modules/`; v `instance_health` odkaz na `ue_report_days` a věta, které příkazy nezapisují do vaultu

## Dopad
<!-- doplní Curator nebo člověk před odesláním -->

## Alternativy
<!-- doplní Curator nebo člověk před odesláním -->

## Průběh

| datum | stav | kdo | poznámka |
|---|---|---|---|
| 2026-11-26 | new | export_cr | ze structure_log 2026-11-26 |
