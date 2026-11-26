---
type: change_request
cr_status: new
source_instance: lapikus
hestia_version: "0.26.0"
area: process
gd_relevance:            # direct | indirect | none (11, kap. 2)
structure_log: ["2026-11-26 | friction | Steward (test v čisté roli 2026-11-26): v nové relaci VM je jiný `$HOME`, `~/hvenv/bin/python` z `config.yaml` neexistuje a VM má Python 3.10; `doctor` předepisuje založit venv, zadání testu zakazovalo zápis a profil neříká, zda je venv mimo vault a projekt povolený i v režimu bez zápisu; žádný příkaz core se nespustil (P-0021; doklad: `Maintenance/config.yaml` 2026-11-26)"]
spec_refs: []
released_in:
updated: 2026-11-26
---
# Steward (test v čisté roli 2026-11-26): v nové relaci VM je jiný `$HOME`, `~/hvenv/bin/python` z `config.yaml` neexistuje a VM má Python 3.10; `doctor` předepisuje založit venv, zadání testu zakazovalo zápis a profil neříká, zda je venv mimo vault a projekt povolený i v režimu bez zápisu; žádný příkaz core se nespustil (P-0021; doklad: `Maintenance/config.yaml` 2026-11-26)

> **Předání do HearthLore:** soubor se neodesílá skriptem. Uveď ho v hlášení pro HearthLore, nebo ho předá člověk; v instanci ho nepřejmenovávej, nečísluj ani nekopíruj do HearthLore. Zaeviduje ho agent HearthLore: číslo, jméno `CR-NNN_<short_name>`, původní jméno v `source_id` (11 kap. 3).

## Co se stalo
Steward (test v čisté roli 2026-11-26): v nové relaci VM je jiný `$HOME`, `~/hvenv/bin/python` z `config.yaml` neexistuje a VM má Python 3.10; `doctor` předepisuje založit venv, zadání testu zakazovalo zápis a profil neříká, zda je venv mimo vault a projekt povolený i v režimu bez zápisu; žádný příkaz core se nespustil (P-0021; doklad: `Maintenance/config.yaml` 2026-11-26)

Dopad podle záznamu: každá nová relace potřebuje zásah člověka, kontrola zdraví bez skriptů

Záznam `structure_log` z 2026-11-26 (kategorie `friction`), instance `lapikus`, core 0.26.0.

## Návrh
modul `start`: venv mimo projekt a vault je vždy povolený (není zápis do instance); bez interpretu kontrolu proveď ručně výběrem, hlas, že skript neběžel; zvážit, aby `doctor` vypsal jeden příkaz pro založení venv v nové relaci

## Dopad
<!-- doplní Curator nebo člověk před odesláním -->

## Alternativy
<!-- doplní Curator nebo člověk před odesláním -->

## Průběh

| datum | stav | kdo | poznámka |
|---|---|---|---|
| 2026-11-26 | new | export_cr | ze structure_log 2026-11-26 |
