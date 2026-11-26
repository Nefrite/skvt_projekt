---
type: change_request
cr_status: new
source_instance: lapikus
hestia_version: "0.26.0"
area: process
gd_relevance:            # direct | indirect | none (11, kap. 2)
structure_log: ["2026-11-26 | missing | Steward (test v čisté roli 2026-11-26): nejnovější značka core je jen v `core_source` (HearthLore), které Steward nečte; profil neříká, že `update_core --latest` v dry-runu značky číst smí, takže porovnání verze zůstalo neověřené (P-0022; doklad: `_core/agents/modules/instance_health.md` 2026-11-26)"]
spec_refs: []
released_in:
updated: 2026-11-26
---
# Steward (test v čisté roli 2026-11-26): nejnovější značka core je jen v `core_source` (HearthLore), které Steward nečte; profil neříká, že `update_core --latest` v dry-runu značky číst smí, takže porovnání verze zůstalo neověřené (P-0022; doklad: `_core/agents/modules/instance_health.md` 2026-11-26)

> **Předání do HearthLore:** soubor se neodesílá skriptem. Uveď ho v hlášení pro HearthLore, nebo ho předá člověk; v instanci ho nepřejmenovávej, nečísluj ani nekopíruj do HearthLore. Zaeviduje ho agent HearthLore: číslo, jméno `CR-NNN_<short_name>`, původní jméno v `source_id` (11 kap. 3).

## Co se stalo
Steward (test v čisté roli 2026-11-26): nejnovější značka core je jen v `core_source` (HearthLore), které Steward nečte; profil neříká, že `update_core --latest` v dry-runu značky číst smí, takže porovnání verze zůstalo neověřené (P-0022; doklad: `_core/agents/modules/instance_health.md` 2026-11-26)

Dopad podle záznamu: kontrola zdraví neřekne, zda je instance pozadu

Záznam `structure_log` z 2026-11-26 (kategorie `missing`), instance `lapikus`, core 0.26.0.

## Návrh
v profilu Stewarda a v `instance_health` výslovně: čtení značek přes `update_core --latest` (dry-run) je povolená výjimka ze zákazu čtení HearthLore

## Dopad
<!-- doplní Curator nebo člověk před odesláním -->

## Alternativy
<!-- doplní Curator nebo člověk před odesláním -->

## Průběh

| datum | stav | kdo | poznámka |
|---|---|---|---|
| 2026-11-26 | new | export_cr | ze structure_log 2026-11-26 |
