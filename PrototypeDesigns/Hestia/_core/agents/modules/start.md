---
type: agent_module
module_id: start
trigger: začátek tasku
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-21
---
# Start tasku

## Kdy
Na začátku každého tasku a při pokračování v nové relaci.

## Postup
0. **Režim podle přístupu** (12 kap. 1.1): ověř, zda vidíš `Hestia/_core/agents/CONTRACT.md` v pracovní nebo připojené složce. Když ano, pracuješ v režimu `vault`, i když jsi začal s kompilátem role: načti kontrakt a profil z vaultu (projektové role v `Hestia/Roles/`, role core v `Hestia/_core/agents/`) a kompilát dál neber jako zdroj. Když ne, pracuješ v režimu `chat` s kompilátem.

Pak načti v tomto pořadí a nic navíc:
1. kontrakt a profil své role, případně složené profily (`combines`);
2. zadání tasku: chat nebo aktivní předání v `Handovers/`;
3. huby entit, kterých se task týká, a jejich `state`;
4. dokumenty z `context` profilu (master lore, pravidla návrhu);
5. dokumentaci kroku v `Steps/` nebo sdíleného kódu v `Steps/shared/`, pokud task mění skripty;
6. know-how podle `knowhow_tags` profilu a domény tasku (modul `knowhow_lookup`).

Ověř, že předání a hub nemají `validity: superseded` (jinak pokračuj podle `superseded_by`). Stav prototypování zjišťuj v pořadí dokumentace kroku → hlavička skriptu → `asset_index` → kód, a kód čti jen tam, kde předchozí nestačí.

Další dokumenty dotahuj až podle potřeby: odkazy z hubu, `knowhow_lookup`, otázka na GameDesignera. V režimu `chat` ti stejný výběr připraví orchestrační agent jako kontext tasku.

## Výstup
Krátké potvrzení GameDesignerovi: co jsi pochopil jako zadání, z jakého stavu vycházíš a co je nejasné. Nejasnost řeš modulem `question` dřív, než začneš.

## Známé pasti
- Pracovat podle kompilátu (balíčky, zápis Hestia), když relace vault vidí, třeba přes připojenou složku; hlavní práce pak běží nad ručně přenášenými výňatky.
- Číst „všechno pro jistotu“: zahltí kontext a míchá platné s neplatným.
- Brát předání nebo starou kopii v chatu jako zdroj pravdy. Platí vault, u prototypování skripty a stav v enginu.
- Přehlédnout `superseded` u předání nebo hubu a pracovat podle neplatného zadání.
