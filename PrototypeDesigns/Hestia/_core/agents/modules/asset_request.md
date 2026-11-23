---
type: agent_module
module_id: asset_request
trigger: role potřebuje knihovní asset, který není v Assets/, nebo staví graybox místo assetu
requires: []
modes: [vault, chat]
compile: listed
validity: valid
updated: 2026-11-23
---
# Požadavek na knihovní asset

## Kdy
Tvá práce potřebuje knihovní asset (mesh, materiál, textura, Blueprint pro stavby nebo vybavení), který v `Assets/` není, nebo místo něj stavíš graybox. Modul mají v profilu role, které assety potřebují (Architect, Builder, Furnisher, GameDesign); vyrábí role s `asset_work` (12 kap. 4.6).

## Postup
1. **Nejdřív hledej:** `hestia.py find "<co hledáš>" --type asset` (název, alias, entita v `used_by`). Existuje-li karta, doplň svou entitu do `used_by` a skonči.
2. **Nová karta** podle `_core/templates/tpl_asset.md` (07 kap. 20): soubor `Assets/<asset_category>/<jméno v UE>.md` (`SM_RuinChestSmall_A.md`), `asset_status: requested`, `requested_by` = tvá role, `requested` = dnes, `asset_kind`, `asset_category`, `used_by` (entity), `priority` (`medium`, `high` jen když asset blokuje práci).
3. **`owner` vyplň vždy** (výrobce, 12 kap. 4.6 bod 3): jednoduchý asset (díl stavby z existujícího generátoru jen s jinými parametry nebo na míru: trám, prkno, sloup, kámen, kulatina; bez nového materiálu a textury) smí vyrobit Builder; props, textil, nový tvar, nový materiál nebo textura, UV a sloty vyrábí Crafter. Výchozí a v pochybnosti `owner: Crafter`. Builder, který jednoduchý asset potřebuje sám, založí kartu rovnou s `owner: Builder`.
4. Vyplň *Účel a použití* (k čemu asset je, kde stojí) a *Požadavek*: `envelope` = **rozměr grayboxu** (`[x, y, z]` cm, obal, do kterého se asset vejde; z návrhu nebo grayboxu), nebo odkaz na návrh; technické údaje, které víš. Společné konvence jen odkazem na `Assets/Konvence_assetu.md`.
5. **Graybox:** ve stavbě smí zatím stát graybox v rozměru `envelope` (`stand_in: graybox`). Prototyp může u grayboxu skončit se zaevidovaným požadavkem; kdy se asset vyrobí, je věc priority.
6. **Rozměry pro rozvržení a data** bereš z karty: `envelope` pro graybox, skutečný rozměr z bloku *Z kódu* (po `generated`). Do vlastních dat je neopisuj bez odkazu na kartu; když výrobce `envelope` zvětší, dostaneš úkol ve frontě.
7. **Náhrada grayboxu:** až je karta `imported`, nahraď graybox assetem a nastav v kartě `stand_in: none`.
8. Kartu zkontroluj `hestia.py lint <karta>` (povinná pole a sekce podle stavu) a uzavři task `task_close` (řádek do `changes.md`). V režimu `chat` dej kartu do zápisu Hestia.

## Výstup
Karta `requested` s `owner` v `Assets/<asset_category>/`, nebo doplněné `used_by` existující karty; své otevřené požadavky vidíš v `agenda --role <Role>`.

## Známé pasti
- Nová karta bez hledání: vzniknou dvě karty jednoho assetu.
- Karta bez `owner`: uvidí ji jen `asset_default_owner` (výchozí Crafter); Builder ji v agendě nemá.
- Rozměry assetu opsané do dat stavby bez odkazu na kartu: po změně assetu se rozejdou.
- Stav dál než `requested` nastavuje role s `asset_work`; `verified` jen GameDesigner.
- Kartu nemaž: nepotřebný asset uzavře GameDesigner nebo Crafter jako `rejected` s důvodem v *Poznámkách*.
