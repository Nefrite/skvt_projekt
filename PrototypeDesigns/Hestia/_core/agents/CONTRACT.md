---
type: agent_module
module_id: contract
trigger: always
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-21
---
# Kontrakt agentů Hestia (L0)

## Co je Hestia
Hestia je samodokumentující vault projektu (`Hestia/`). Dokumentace vzniká u toho, kdo pracuje: během tasku a při jeho uzavření. Hlavním orchestrátorem je **GameDesigner** (člověk v chatu): zadává tasky, rozhoduje, odpovídá na otázky a schvaluje.

## Režim práce
Režim určuje přístup k vaultu, ne prostředí:
- **`vault`**: relace vidí soubory projektu (Claude Code ve složce projektu, chat nebo Cowork s připojenou složkou); zapisuješ přímo podle matice pravomocí. Platí, i když relace začala s kompilátem role.
- **`chat`**: relace bez přístupu k vaultu (chat bez připojené složky, jen dokumenty Claude Projectu); na konci tasku vydáš zápis Hestia.

Režim ověří modul `start` jako první krok. I v režimu `vault` commituje člověk.

## Start
1. Přečti tento kontrakt a profil své role: projektové role v `Roles/<Role>.md`, role core (Curator, Auditor, Librarian) v `_core/agents/<Role>.md`. V režimu `chat` máš obojí v kompilátu role.
2. Postupuj podle modulu `start`: načti jen to, co task potřebuje, nic „pro jistotu“.
3. Zdroj pravdy: u prototypování skripty, data a stav v enginu, u lore a příběhu finální dokumentace v `Docs/`. Předání a zadání v chatu jsou jen instrukce.

## Kam smíš psát
- Podle matice pravomocí v `_core/agents/write_rules.md` a lokálních doplňků v `Maintenance/write_rules_local.md`.
- `_core/` neměníš nikdy; mění se jen aktualizací core.
- Platný text přepisuješ jen jako důsledek rozhodnutí GameDesignera nebo výsledku tasku ve své oblasti.
- Profil kontrakt zpřísňuje, neruší: výsledek své práce do vaultu zapíšeš vždy; zákazy zápisu v profilu platí pro kód, data a assety. Rozpor nahlas jako otázku.
- Zápis do `Docs/` je dokumentace domény podle šablony (sekce, `depth`), ne výstup role: neříká, kdo psal a pro koho. Existující dokumentaci entity doplníš, nový dokument jen když žádný není; předání píšeš z role.
- Nemažeš: soubor přesuneš do `_to_delete/`, a jen na pokyn. Přesun a přejmenování jen se schválením.
- Agenti necommitují; commity dělá lidský správce.
- Komunikuješ česky; klíče frontmatteru, `module_id`, názvy souborů a kód jsou anglicky.

## Během práce
| Spouštěč | Modul |
|---|---|
| začátek tasku | `start` |
| nápad mimo zadání (oznámit, zapsat až na pokyn) | `idea_capture` |
| GameDesigner rozhodl | `decision` |
| chyba, neznámý postup, nová technologie | `knowhow_lookup` |
| ověřená past, postup, diagnóza | `knowhow_write` |
| nejasnost, nejednoznačné zadání | `question` |
| otázka na obsah dokumentace (odpověď s citacemi) | `lookup` |
| pokyn k zápisu: kam patří, náležitosti, soulad s kánonem | `file_info`, `completeness`, `canon_check` |
| položky inboxu `intake: raw` (třídění s GameDesignerem) | `inbox_triage` |
| pokyn k importu z externího zdroje do `Inbox/` | `inbox_import` |
| otázka na realizaci v Unrealu (jen čtení) | `ue_lookup` |
| zápis do souborů projektu | `file_safety` |
| zápis frontmatteru | `metadata` |
| nový nebo změněný skript | `asset_header` |
| předání jiné roli nebo další relaci | `handover_out` |
| práce v režimu chat (relace bez přístupu k vaultu; s přístupem platí režim vault) | `chat_entry` |
| konec tasku | `task_close` |

Modul načti, když nastane jeho spouštěč, i když ho profil role neuvádí. Výjimka: moduly s `compile: listed` (moduly Knihovníka, `inbox_import`) používá jen role, která je má v profilu nebo ji skládá; ostatní předají věc roli, která modul má (Knihovníkovi zápisem Hestia, import Curatorovi), nebo se zeptají GameDesignera. Moduly core jsou v `_core/agents/modules/`, lokální moduly instance v `Roles/modules/`.

## Uzavření tasku je povinné
Každý task, který změnil návrh, stav, kód nebo data, končí modulem `task_close`: výsledek do finální dokumentace, archivace předání, metadata, know-how, otázky, řádek do `changes.md`, kontrola a krátké hlášení GameDesignerovi. Dokud to neproběhne, task není hotový. V režimu `chat` místo zápisu do vaultu vydáš zápis Hestia (modul `chat_entry`).
