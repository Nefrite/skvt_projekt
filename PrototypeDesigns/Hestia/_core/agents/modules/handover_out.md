---
type: agent_module
module_id: handover_out
trigger: práce se předává jiné roli nebo další relaci
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-24
---
# Předání práce

## Kdy
Práci předáváš jiné roli (např. návrh → stavba) nebo ji budeš dokončovat v další relaci.

## Postup
0. **Předání je jeden task pro jednu roli** (12 kap. 1; zadání 0.21). Navazující kroky dej do dalších předání (fronta předání pro roli, `agenda`), ne do rostoucího jednoho dokumentu.
1. Nejdřív zapiš návrh a rozhodnutí do `Docs/` a stav do `state` entity. Předání nesmí být jediným místem návrhu.
2. Pak založ předání v `Handovers/` ze šablony `tpl_handover` (`type: handover`), s `for_role` = jméno profilu role, pro kterou je (`[Builder]`; prázdné = kdokoli). Obsahuje jen:
   - zadání (pro koho a co);
   - platná rozhodnutí jako **odkazy** na fakta v `Docs/`;
   - kritéria hotovo;
   - otevřené otázky;
   - *Zbývá*.
3. Co je hotové, je v `state`, návrh v doménovém dokumentu; předání na ně odkazuje, nekopíruje je.
4. Na oblast (entita, role) je jedno aktivní předání. Předchozí aktivní předání téže oblasti archivuj (`validity: archived`, přesun do `Handovers/_archive/`).

V režimu `chat` vydáš předání jako dokument v odpovědi; do vaultu ho uloží orchestrační agent nebo GameDesigner.

## Výstup
Aktivní předání v `Handovers/`, archivované předchozí předání, aktuální `state` a `Docs/`.

## Známé pasti
- Předání delší než `handover_max_chars` (výchozí 4 000 znaků, G14c): obsahuje víc než zadání a odkazy; rozhodnutí patří do `Docs/` hned. Počítají se znaky těla bez frontmatteru a bez generovaných bloků; délku ukáže `section <předání> --list`. Archivované předání se nepočítá.
- Předání bez `for_role`: role ho v `agenda` uvidí jen mezi předáními pro kohokoli.
- Kopírovat návrh do předání: po archivaci se ztratí, nebo se rozejde s `Docs/`.
- Nechat dvě aktivní předání pro stejnou oblast.
