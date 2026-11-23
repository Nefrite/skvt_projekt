---
type: agent_module
module_id: contract
trigger: always
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-23
---
# Kontrakt agentů Hestia (L0)

## Co je Hestia
Hestia je samodokumentující vault projektu (`Hestia/`): dokumentace vzniká u toho, kdo pracuje, během tasku a při jeho uzavření. Orchestruje **GameDesigner** (člověk v chatu): zadává, rozhoduje, odpovídá a schvaluje.

## Režim a start
Režim určuje přístup k vaultu: `vault` (vidíš soubory projektu, zapisuješ podle matice) nebo `chat` (bez vaultu, na konci vydáš zápis Hestia). Ověří ho modul `start`.
1. Přečti tento kontrakt a profil své role (`Roles/<Role>.md`, role core v `_core/agents/`); v režimu `chat` jsou v kompilátu.
2. Postupuj podle modulu `start`: načti jen to, co task potřebuje.
3. Zdroj pravdy: u prototypování skripty, data a stav v enginu, jinak finální dokumentace v `Docs/`. Předání a chat jsou instrukce.

## Povinnosti, které profil nezruší
- Výsledek své práce zapíšeš do vaultu podle `_core/agents/write_rules.md` (zásady a matice) a `Maintenance/write_rules_local.md`. Profil kontrakt zpřísňuje, neruší; zákazy v profilu platí pro kód, data a assety. Rozpor nahlas otázkou.
- `_core/` neměníš; mění se jen aktualizací core.
- Nemažeš (přesun do `_to_delete/` jen na pokyn) a necommituješ (commituje člověk).
- Komunikuješ česky; klíče frontmatteru, `module_id`, názvy souborů a kód jsou anglicky.

## Spouštěče
| Spouštěč | Modul |
|---|---|
| začátek tasku | `start` |
| nápad mimo zadání (oznámit, zapsat až na pokyn) | `idea_capture` |
| GameDesigner rozhodl | `decision` |
| chyba, neznámý postup, nová technologie | `knowhow_lookup` |
| ověřená past, postup, diagnóza | `knowhow_write` |
| nejasnost, nejednoznačné zadání | `question` |
| otázka na obsah dokumentace | `lookup` |
| pokyn k zápisu (kam, náležitosti, kánon) | `file_info`, `completeness`, `canon_check` |
| položky inboxu `intake: raw` | `inbox_triage` |
| import z externího zdroje do `Inbox/` | `inbox_import` |
| otázka na realizaci v Unrealu (jen čtení) | `ue_lookup` |
| zápis do souborů projektu | `file_safety`, `metadata` |
| nový nebo změněný skript | `asset_header` |
| potřebný knihovní asset chybí, graybox místo něj | `asset_request` |
| výroba nebo změna knihovního assetu | `asset_work` |
| předání jiné roli nebo relaci | `handover_out` |
| problém s Hestií jako nástrojem | `hestia_feedback` |
| práce v režimu chat | `chat_entry` |
| konec tasku | `task_close` |

Modul načti, když nastane spouštěč, i když ho profil neuvádí; kdy modul předáš jiné roli, říká `start`. Moduly: `_core/agents/modules/`, lokální `Roles/modules/`.

## Uzavření tasku je povinné
Task, který změnil návrh, stav, kód nebo data, končí modulem `task_close`; do té doby není hotový. V režimu `chat` vydáš zápis Hestia (`chat_entry`).
