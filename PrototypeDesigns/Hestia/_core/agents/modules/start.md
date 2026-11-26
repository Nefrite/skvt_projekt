---
type: agent_module
module_id: start
trigger: začátek tasku
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-26
---
# Start tasku

## Kdy
Na začátku každého tasku a při pokračování v nové relaci.

## Postup
0. **Režim podle přístupu** (12 kap. 1.1): ověř, zda vidíš `Hestia/_core/agents/CONTRACT.md` v pracovní nebo připojené složce. Když ano, pracuješ v režimu `vault`, i když jsi začal s kompilátem role: načti kontrakt a profil z vaultu (projektové role v `Hestia/Roles/`, role core v `Hestia/_core/agents/`) a kompilát dál neber jako zdroj. Když ne, pracuješ v režimu `chat` s kompilátem.

**Nové prostředí** (nový chat, nová VM, jiný stroj): před prvním skriptem spusť `hestia.py doctor` a podle výsledku prostředí doplň (návod u každé chyby; Python ≥ 3.11 a PyYAML mimo projekt a vault). Upozornění na připojenou složku → dlouhé běhy `update_core` s `--work-copy --apply`.

**Bez zadání** spusť `hestia.py agenda --role <Role>` a nabídni GameDesignerovi, co čeká (předání s tvou rolí ve `for_role` a předání bez `for_role`, úkoly pro tvou roli z `queue.md` (`code: role:<Role>`) a u rolí s assety karty k výrobě nebo tvé požadavky). Složky neprocházej a cizí soubory (předání pro jiné role, reporty jiných rolí) nečti.

**Po aktualizaci core nebo změně profilu** (pokyn GameDesignera, `_core/VERSION` jiná než verze, se kterou jsi začal, nebo hlavička kompilátu) spusť `hestia.py role_diff <Role>` a přečti jen změny; změněný profil čti celý. „Beze změny“ hlaš jen podle `role_diff`, ne podle části souboru.

**Modul, který role nemá:** moduly s `compile: listed` (moduly Knihovníka a Stewarda, `inbox_import`, assety) používá jen role, která je má v profilu nebo ji skládá (`combines`). Když nastane jejich spouštěč a modul nemáš, předej věc roli, která ho má (Knihovníkovi zápisem Hestia, import Curatorovi, aktualizaci core Stewardovi), nebo se zeptej GameDesignera.

**Lokální náhrady modulů core** (režim `vault`): modul core, který má v registru `Maintenance/local_overrides.md` aktivní náhradu (stav `aktivní` nebo `konflikt`), čti z `Roles/modules/<lokální modul>.md` místo `_core/agents/modules/`. Kontrakt se nenahrazuje nikdy. V kompilátu je náhrada už vložená.

Pak načti v tomto pořadí a nic navíc:
1. **nejdřív ověř přístup k vaultu** (`ls <cesta k vaultu>` z pokynů první zprávy), pak čti; vault nehledej procházením projektu. Příkazy core spouštěj interpretem z pokynů nebo z `hestia_python` v `Maintenance/config.yaml`; kontrakt a profil své role, případně složené profily (`combines`);
2. zadání tasku: chat nebo aktivní předání v `Handovers/`;
3. huby entit, kterých se task týká, a jejich `state`;
4. dokumenty z `context` profilu (master lore, pravidla návrhu);
5. dokumentaci kroku v `Steps/` nebo sdíleného kódu v `Steps/shared/`, pokud task mění skripty;
6. know-how podle `knowhow_tags` profilu a domény tasku (modul `knowhow_lookup`).

Ověř, že předání a hub nemají `validity: superseded` (jinak pokračuj podle `superseded_by`). **Realizace podle návrhu** (projektová role, zadání v chatu nebo předání): ověř, že návrh (`type: design`), podle kterého realizuješ, má `validity: valid`; když ne (`draft`), vyžádej si schválení GameDesignera dřív, než realizuješ (audit hlásí platný stav nad návrhem `draft` jako G5). Stav prototypování zjišťuj v pořadí dokumentace kroku → hlavička skriptu → `asset_index` → kód, a kód čti jen tam, kde předchozí nestačí.

Další dokumenty dotahuj až podle potřeby: odkazy z hubu, `knowhow_lookup`, otázka na GameDesignera. V režimu `chat` ti stejný výběr připraví orchestrační agent jako kontext tasku.

**Čtení** (12 kap. 3; zadání 0.21):
- Dokument delší než `doc_summary_chars` (výchozí 6 000 znaků; velikost je v `doc_index`, pole `chars`) nečti celý: nejdřív osnova `hestia.py section <dokument> --list`, pak *Souhrn*, je-li, a jen sekce, které task potřebuje (`hestia.py section <dokument> "<nadpis>"`). Celý ho čti, jen když task mění jeho strukturu.
- Soubory hledej příkazem `hestia.py find "<dotaz>"`, ne `find -name` ani `grep -r` přes vault.
- Logy (`changes.md`, `queue.md`, `structure_log.md`), reporty a `CHANGELOG.md` čti výběrem: konec, filtr podle entity nebo data, CHANGELOG po verzích (`section`).
- Když skript core spustit nejde, čti `doc_index.json` a dokumenty přímo, ale stejně výběrem, a v hlášení uveď, že skript neběžel.

## Výstup
Krátké potvrzení GameDesignerovi: co jsi pochopil jako zadání, z jakého stavu vycházíš a co je nejasné. Nejasnost řeš modulem `question` dřív, než začneš.

## Známé pasti
- Hledat vault `find`/`ls` přes celý projekt, když pokyny první zprávy uvádějí cestu; nebo zakládat nové prostředí Pythonu, když je `hestia_python` (při starém Pythonu ho navrhne `doctor`).
- Spustit první skript v novém prostředí bez `doctor`: selže na chybějícím PyYAML nebo starém Pythonu a hledání příčiny stojí víc než kontrola.
- Pracovat podle kompilátu (balíčky, zápis Hestia), když relace vault vidí, třeba přes připojenou složku; hlavní práce pak běží nad ručně přenášenými výňatky.
- Číst „všechno pro jistotu“: zahltí kontext a míchá platné s neplatným. Totéž dlouhý dokument celý místo osnovy a sekcí.
- Hlásit „beze změny“ po aktualizaci podle části souboru místo `role_diff`.
- Brát předání nebo starou kopii v chatu jako zdroj pravdy. Platí vault, u prototypování skripty a stav v enginu.
- Přehlédnout `superseded` u předání nebo hubu a pracovat podle neplatného zadání.
- Realizovat podle návrhu ve stavu `draft` (neschváleného) jen proto, že zadání v chatu o něm mluví.
