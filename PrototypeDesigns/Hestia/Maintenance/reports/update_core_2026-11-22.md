---
type: report
updated: 2026-11-22
---
# Aktualizace core 2026-11-22

## Přechod 0.16.0 → 0.20.1
- Stav: dokončeno
- Výměna `_core/`: starý core v `_to_delete/_core_0.16.0/`; řádek v `structure_version.md`.
- Záznamy manifestu: 0.17.0, 0.18.0, 0.19.0, 0.20.0, 0.20.1.

### Automatické kroky
- `hubs`: v pořádku
  - změněné soubory: 8
- `doc_index`: v pořádku
  - index beze změny
- `compose_role`: v pořádku
  - změněné kompiláty: 5 z 5

### Kontroly (dry-run)
- lint: chyby 0, upozornění 0, informace 19
- audit: chyby 0, upozornění 57, informace 68

### Ruční úkoly
- `update_core:0.17.0:role_base` (ve frontě): Srovnat profily projektových rolí se základem 0.17.0 (projektové role a Knihovník CR nezakládají: podnět ke změně Hestie na konec queue.md (proposal, code: hestia), Curator ho převede do structure_log (12 kap. 4.5, 8); hlášení task_close (krok 11) uvádí podněty, zápis Hestia má sekci Podněty pro Hestii; Knihovník uzavírá vlastní zápis skriptem task_close (12 kap. 3b.1)); po schválení GameDesignerem nastavit role_base: 0.17.0 a spustit compose_role (12 kap. 2.1, 13 kap. 10.6a)
- `update_core:0.19.0:role_base` (ve frontě): Srovnat profily projektových rolí se základem 0.19.0 (kontrakt L0 rozdělen (12 kap. 2): zásady zápisu v write_rules.md, oddíl Zásady zápisu (12 kap. 8); podnět ke změně Hestie v novém modulu hestia_feedback (12 kap. 4.5); výjimka compile: listed v modulu start; profil, který odkazuje na oddíl kontraktu Kam smíš psát, odkáže na write_rules.md, Zásady zápisu); po schválení GameDesignerem nastavit role_base: 0.19.0 a spustit compose_role (12 kap. 2.1, 13 kap. 10.6a)
- `update_core:0.20.0:role_base` (ve frontě): Srovnat profily projektových rolí se základem 0.20.0 (čtení výběrem (12 kap. 3, modul start): dokument nad doc_summary_chars po sekcích (section), hledání příkazem find, bez zadání agenda --role, po aktualizaci role_diff; předání je jeden task pro jednu roli s for_role (12 kap. 1, handover_out); jeden dokument, jedno téma a Souhrn nad prahem (01 kap. 9.2, file_info, task_close krok 1); do Claude Projectu jen kompiláty changed (12 kap. 7.1, task_close krok 2)); po schválení GameDesignerem nastavit role_base: 0.20.0 a spustit compose_role (12 kap. 2.1, 13 kap. 10.6a)

### Základ projektových rolí
- Změna v 0.17.0: projektové role a Knihovník CR nezakládají: podnět ke změně Hestie na konec queue.md (proposal, code: hestia), Curator ho převede do structure_log (12 kap. 4.5, 8); hlášení task_close (krok 11) uvádí podněty, zápis Hestia má sekci Podněty pro Hestii; Knihovník uzavírá vlastní zápis skriptem task_close (12 kap. 3b.1)
- Změna v 0.19.0: kontrakt L0 rozdělen (12 kap. 2): zásady zápisu v write_rules.md, oddíl Zásady zápisu (12 kap. 8); podnět ke změně Hestie v novém modulu hestia_feedback (12 kap. 4.5); výjimka compile: listed v modulu start; profil, který odkazuje na oddíl kontraktu Kam smíš psát, odkáže na write_rules.md, Zásady zápisu
- Změna v 0.20.0: čtení výběrem (12 kap. 3, modul start): dokument nad doc_summary_chars po sekcích (section), hledání příkazem find, bez zadání agenda --role, po aktualizaci role_diff; předání je jeden task pro jednu roli s for_role (12 kap. 1, handover_out); jeden dokument, jedno téma a Souhrn nad prahem (01 kap. 9.2, file_info, task_close krok 1); do Claude Projectu jen kompiláty changed (12 kap. 7.1, task_close krok 2)
- Rozdíl `tpl_role`: beze změny šablony.
- Profily nesrovnané se základem 0.20.0 (ruční úkol `role_base`):
  - `Roles/Architect.md`: role_base 0.16.0 je starší než 0.20.0
  - `Roles/Builder.md`: role_base 0.16.0 je starší než 0.20.0
  - `Roles/Furnisher.md`: role_base 0.16.0 je starší než 0.20.0
  - `Roles/GameDesign.md`: role_base 0.16.0 je starší než 0.20.0

### Změny instrukcí
- Změněné soubory: 13. Role si změny vypíše `role_diff <Role>`.

#### `agents/CONTRACT.md` (změněný)
- Sekce: Co je Hestia (změněná), Režim a start (nová), Povinnosti, které profil nezruší (nová), Spouštěče (nová), Uzavření tasku je povinné (změněná), Režim práce (odebraná), Start (odebraná), Kam smíš psát (odebraná), Během práce (odebraná)

> ## Co je Hestia
> Hestia je samodokumentující vault projektu (`Hestia/`): dokumentace vzniká u toho, kdo pracuje, během tasku a při jeho uzavření. Orchestruje **GameDesigner** (člověk v chatu): zadává, rozhoduje, odpovídá a schvaluje.

> ## Režim a start
> Režim určuje přístup k vaultu: `vault` (vidíš soubory projektu, zapisuješ podle matice) nebo `chat` (bez vaultu, na konci vydáš zápis Hestia). Ověří ho modul `start`.
> 1. Přečti tento kontrakt a profil své role (`Roles/<Role>.md`, role core v `_core/agents/`); v režimu `chat` jsou v kompilátu.
> 2. Postupuj podle modulu `start`: načti jen to, co task potřebuje.
> 3. Zdroj pravdy: u prototypování skripty, data a stav v enginu, jinak finální dokumentace v `Docs/`. Předání a chat jsou instrukce.

> ## Povinnosti, které profil nezruší
> - Výsledek své práce zapíšeš do vaultu podle `_core/agents/write_rules.md` (zásady a matice) a `Maintenance/write_rules_local.md`. Profil kontrakt zpřísňuje, neruší; zákazy v profilu platí pro kód, data a assety. Rozpor nahlas otázkou.
> - `_core/` neměníš; mění se jen aktualizací core.
> - Nemažeš (přesun do `_to_delete/` jen na pokyn) a necommituješ (commituje člověk).
> - Komunikuješ česky; klíče frontmatteru, `module_id`, názvy souborů a kód jsou anglicky.

> ## Spouštěče
> | Spouštěč | Modul |
> |---|---|
> | začátek tasku | `start` |
> | nápad mimo zadání (oznámit, zapsat až na pokyn) | `idea_capture` |
> | GameDesigner rozhodl | `decision` |
> | chyba, neznámý postup, nová technologie | `knowhow_lookup` |
> | ověřená past, postup, diagnóza | `knowhow_write` |
> | nejasnost, nejednoznačné zadání | `question` |
> | otázka na obsah dokumentace | `lookup` |
> | pokyn k zápisu (kam, náležitosti, kánon) | `file_info`, `completeness`, `canon_check` |
> | položky inboxu `intake: raw` | `inbox_triage` |
> | import z externího zdroje do `Inbox/` | `inbox_import` |
> | otázka na realizaci v Unrealu (jen čtení) | `ue_lookup` |
> | zápis do souborů projektu | `file_safety`, `metadata` |
> | nový nebo změněný skript | `asset_header` |
> | předání jiné roli nebo relaci | `handover_out` |
> | problém s Hestií jako nástrojem | `hestia_feedback` |
> | práce v režimu chat | `chat_entry` |
> | konec tasku | `task_close` |
>
> Modul načti, když nastane spouštěč, i když ho profil neuvádí; kdy modul předáš jiné roli, říká `start`. Moduly: `_core/agents/modules/`, lokální `Roles/modules/`.

> ## Uzavření tasku je povinné
> Task, který změnil návrh, stav, kód nebo data, končí modulem `task_close`; do té doby není hotový. V režimu `chat` vydáš zápis Hestia (`chat_entry`).

#### `agents/Curator.md` (změněný)
- Sekce: Co děláš a co ne (změněná), Postupy podle zakázky (změněná), Formáty výstupů (změněná), Zápis do logů (změněná)
- Nové znění: 3781 znaků, nad 3000; přečti sekce v `_core/agents/Curator.md`.

#### `agents/Librarian.md` (změněný)
- Sekce: Co děláš a co ne (změněná), Matice pravomocí (změněná), Postupy podle zakázky (změněná), Formáty výstupů (změněná), Zápis do logů (změněná)
- Nové znění: 4646 znaků, nad 3000; přečti sekce v `_core/agents/Librarian.md`.

#### `agents/modules/canon_check.md` (změněný)
- Sekce: Postup (změněná)

> ## Postup
> 1. Najdi, co o tvrzení dokumentace říká (`lookup`), a urči oblast tvrzení. Přednost od nejvyšší (12 kap. 3b.3):
>    - **realizovaný stav:** report Unrealu → `state` → skript a dokumentace kroku → `design`;
>    - **záměr a návrh:** `decision` → platný `design` / `spec` (ne `rejected`) → předání → scratch;
>    - **svět, doba, postavy:** master lore → dokumenty `narrative` → ostatní;
>    - **pojmy a jména:** glosář → `aliases` v hubech.
>    Zastaralé a nahrazené dokumenty jsou jen historie; při shodě úrovně platí novější `updated`.
> 2. Glosář: čti tabulku *Pojmy projektu* v `Dashboard/Glossary.md`. Zakázaná varianta jména v zápisu = oprav na pojem, nebo se zeptej; kolize pojmů zapiš i do `structure_log` (kategorie `collision`). Starší záhlaví tabulky (tři sloupce) se nečte jako pojmy, `lint` k němu vypíše varování.
> 3. **Rozpor** se zápisem nerozhoduješ. Ukaž ho GameDesignerovi (co platí, kde, odkud) a zeptej se: „Měníš kánon?“
> 4. **Vědomá změna kánonu** (12 kap. 3b.4), jen po potvrzení „ano, měním“:
>    - nové tvrzení na místo podle `file_info` (doslovně přímo, přeformulované po schválení);
>    - u podstatné změny (svět, varianta, uzavření cesty) `decision` s důvodem;
>    - staré tvrzení nemaž: `validity: outdated` s odkazem, nebo `nahradit:` (stará verze zůstane v historii);
>    - řádek `changes.md`, jehož sloupec *co se změnilo* začíná `změna kánonu:` a obsahuje odkaz na rozhodnutí:
>      `| RRRR-MM-DD | Librarian | <entita> | změna kánonu: <co> ([[<rozhodnutí>]]) | <zdroj> |`;
>    - vypiš dokumenty, které staré tvrzení opakují (index dokumentů, glosář), a navrhni jejich úpravu ke schválení; sám nic nepřepisuj, neupravené nech jako otázky.
> 5. Bez potvrzení zůstává rozpor otázkou k dotčenému dokumentu (modul `question`), u rozporu mezi dokumenty i položka fronty.

#### `agents/modules/chat_entry.md` (změněný)
- Sekce: Postup (změněná)

> ## Postup
> Na konci tasku vydej strukturovaný blok. Prázdné sekce vynech.
>
> ```markdown
> ## Zápis Hestia
> - task: <krátký název> | role: <role> | datum: RRRR-MM-DD
> ### Finální dokumentace
> - [[cílový dokument]] § <sekce> | forma: doslovně | přeformulováno: <text k zapsání nebo nahrazení>
> ### Předání
> - [[predani_…]] → archivovat | zbývá: …
> ### Rozhodnutí (uzavírá cestu)
> - <rozhodnutí> | uzavírá: [[…]]
> ### Metadata
> - [[Hub]]: depth_structures 3→4, status in_progress
> ### Know-how
> - nové | doplnit [[…]]: <knowhow_kind>, <tech>, příznak / příčina / řešení
> ### Otevřené otázky
> - [[dokument]]: <otázka>
> ### Nápady (schválené)
> - <téma>: <nápad>
> ### Podněty pro Hestii
> - <target>: co se stalo (doklad) → navrhovaná změna
> ### changes.md
> - | RRRR-MM-DD | role | entita | co | zdroj |
> ```
>
> - Pole **`forma`** u finální dokumentace: `doslovně` = textace GameDesignera, zapíše se přímo; `přeformulováno` = tvůj text, zapíše se až po schválení. Chybí-li `forma`, platí `přeformulováno` (12 kap. 6, 3b.2).
> - Položky *Finální dokumentace* jsou dokumentace domény podle šablony, ne výstup role; u entity s existující dokumentací je cílem ten dokument (`write_rules.md`, *Zásady zápisu*).
> - Obsah zápisu před zapracováním formalizuje Knihovník (náležitosti, místo, kánon).
> - Položka, která **nahrazuje** existující text, uvádí cíl (dokument a sekce) a výslovně `nahradit:`; bez toho se text jen doplňuje.
> - Když cílový text nevidíš, popiš ho **významem** (`nahradit: tvrzení o výstupu na podestu`); orchestrační agent text najde a přepis nechá schválit.
> - *Podněty pro Hestii*: problém nebo zlepšení Hestie jako nástroje (kontrakt, moduly, šablony, skripty); do `queue.md` je zapíše ten, kdo zápis zapracuje (modul `hestia_feedback`).
> - Kopie dokumentů v chatu jsou jen zrcadla ke čtení; platí verze ve vaultu.

#### `agents/modules/file_info.md` (změněný)
- Sekce: Postup (změněná)

> ## Postup
> 1. Urči druh tvrzení a cíl:
>    - fakt o entitě → doménový dokument entity: záměr a parametry do `design` / `spec`, postavené a naměřené do `state`;
>    - svět, doba, postavy, příběh → master lore (`Docs/narrative/Lore_<Prototyp>.md`), rozšíření jako samostatný dokument `narrative`;
>    - nerozhodnutý nápad → tematický `Scratch/` (jen na pokyn GameDesignera);
>    - rozhodnutí, které uzavírá cestu → `decision` (modul `decision`);
>    - pojem a jeho význam → glosář;
>    - rozpor s tím, co platí → modul `canon_check` (12 kap. 3b.3–3b.4).
> 2. **Jeden dokument, jedno téma** (01 kap. 9.2; zadání 0.21): patří-li zápis k jinému tématu, než má cílový dokument (jiná entita nebo její samostatná část, realizace v návrhu, rozhodnutí platné i mimo dokument, nová verze návrhu jako kapitola „platí přednostně“), navrhni vlastní dokument, `state`, `decision`, přepis (`nahradit:`) nebo rozdělení; vrstvení úprav do jednoho dokumentu nepřidávej.
> 3. Urči entitu a doménu podle hubu a indexu dokumentů (`lookup`). Když nejde jednoznačně říct, je-li to návrh, nebo realizace, nebo které entity se týká, **zeptej se**; nedomýšlej.
> 4. Rozliš formu (12 kap. 3b.2): **doslovná textace** GameDesignera se zapíše přímo, se zdrojem (chat, datum) a řádkem v `changes.md`, i do nového dokumentu; **přeformulování, sloučení, zkrácení** předlož ke schválení jako diff. Doslovná textace v rozporu s kánonem nikdy přímo.
> 5. Před zápisem spusť `completeness`, pak zapiš na určené místo; přepis platného textu jen s `nahradit:` nebo po schválení (12 kap. 6.1).

#### `agents/modules/handover_out.md` (změněný)
- Sekce: Postup (změněná), Známé pasti (změněná)

> ## Postup
> 0. **Předání je jeden task pro jednu roli** (12 kap. 1; zadání 0.21). Navazující kroky dej do dalších předání (fronta předání pro roli, `agenda`), ne do rostoucího jednoho dokumentu.
> 1. Nejdřív zapiš návrh a rozhodnutí do `Docs/` a stav do `state` entity. Předání nesmí být jediným místem návrhu.
> 2. Pak založ předání v `Handovers/` ze šablony `tpl_handover` (`type: handover`), s `for_role` = jméno profilu role, pro kterou je (`[Builder]`; prázdné = kdokoli). Obsahuje jen:
>    - zadání (pro koho a co);
>    - platná rozhodnutí jako **odkazy** na fakta v `Docs/`;
>    - kritéria hotovo;
>    - otevřené otázky;
>    - *Zbývá*.
> 3. Co je hotové, je v `state`, návrh v doménovém dokumentu; předání na ně odkazuje, nekopíruje je.
> 4. Na oblast (entita, role) je jedno aktivní předání. Předchozí aktivní předání téže oblasti archivuj (`validity: archived`, přesun do `Handovers/_archive/`).
>
> V režimu `chat` vydáš předání jako dokument v odpovědi; do vaultu ho uloží orchestrační agent nebo GameDesigner.

> ## Známé pasti
> - Předání delší než `handover_max_chars` (výchozí 4 000 znaků, G14c): obsahuje víc než zadání a odkazy; rozhodnutí patří do `Docs/` hned.
> - Předání bez `for_role`: role ho v `agenda` uvidí jen mezi předáními pro kohokoli.
> - Kopírovat návrh do předání: po archivaci se ztratí, nebo se rozejde s `Docs/`.
> - Nechat dvě aktivní předání pro stejnou oblast.

#### `agents/modules/hestia_feedback.md` (nový)
- Sekce: (frontmatter) (nová), (úvod) (nová), Kdy (nová), Postup (nová), Výstup (nová), Známé pasti (nová)

> type: agent_module
> module_id: hestia_feedback
> trigger: problém nebo možnost zlepšení Hestie jako nástroje
> requires: []
> modes: [vault, chat]
> validity: valid

> # Podnět ke změně Hestie

> ## Kdy
> Narazíš na problém nebo možnost zlepšení Hestie jako nástroje: kontrakt, moduly, šablony, taxonomie, skripty, kontroly, proces. Nápad k obsahu hry je nápad (`idea_capture`), ne podnět.

> ## Postup
> 1. Change request nezakládáš a do `structure_log.md` ani `outbox/` nepíšeš: CR mimo kanál Curatora (`export_cr`) by nikdo nezpracoval.
> 2. **Režim vault:** připiš na konec `Maintenance/queue.md` položku `kind: proposal`, `code: hestia`, `target` = čeho se týká (entita, dokument nebo část Hestie, např. `tpl_state`, `audit G10`), `proposal` = `<role>: co se stalo (doklad: odkaz na dokument, report nebo řádek) → navrhovaná změna`, `priority: medium` (`high` jen když podnět blokuje práci), `state: open`. Schválení GameDesignera k zápisu není potřeba.
> 3. **Režim chat:** podnět dej do zápisu Hestia, sekce *Podněty pro Hestii* (modul `chat_entry`); do fronty ho zapíše ten, kdo zápis zapracuje.
> 4. Podnět uveď v hlášení na konci tasku (`task_close`, krok 11).

> ## Výstup
> Položka fronty `P-…` s kódem `hestia` (nebo sekce v zápisu Hestia). Curator ji převede do `structure_log.md` a uzavře; o CR rozhoduje člověk při `export_cr`.

> ## Známé pasti
> - Založit CR přímo v `outbox/` nebo v repozitáři projektu: zůstane mimo kanál a nikdo ho nezpracuje.
> - Podnět bez dokladu: Curator ho nemůže posoudit.
> - Zaměnit podnět s otázkou (`question`) nebo s nálezem údržby (zapisuje Auditor).

#### `agents/modules/lookup.md` (změněný)
- Sekce: Postup (změněná), Známé pasti (změněná)

> ## Postup
> 1. **Ve vaultu** (i chat s připojenou složkou projektu) hledej příkazem `hestia.py find "<dotaz>"` (index dokumentů: název, `aliases`, nadpisy sekcí, entita, cesta; glosář; pod 3 výsledky doplní hledání v textu, `--text` vždy), ne `grep -r` přes vault. Z kandidátů čti jen shodné sekce (`hestia.py section <dokument> "<nadpis>"`); dokument nad `doc_summary_chars` nečti celý (modul `start`, *Čtení*). Starý index obnov `hestia.py doc_index --apply`. Když skript core spustit nejde (relace bez shellu nebo bez vhodného Pythonu), čti index, glosář a dokumenty přímo a v odpovědi výslovně uveď, že skript neběžel (index může být starý).
> 2. **V chatu bez vaultu** pracuj jen s balíčkem kontextu (`compose_context`) a s tím, co máš v tasku; co v něm není, nedomýšlej. **Bez balíčku** neodpovídej a řekni přesně, který balíček potřebuješ a jakým příkazem vznikne: `hestia.py compose_context --entity <Entita> --apply` (otázka o entitě), `--query "<otázka>"` (otázka napříč dokumenty), `--topic <kategorie nebo doména>`; nebo požádej o přístup k vaultu (připojenou složku projektu).
> 3. U otázky o entitě vezmi z hubu stav: návrh, realizace, cíl a režim (blok *Domény*).
> 4. Rozliš **návrh** (`design`, `spec`, `decision`), **realizaci** (`state`, skript, report Unrealu) a **zavržené** (`status: rejected`). Realizaci ověř čtecím dotazem nebo posledním reportem (modul `ue_lookup`), je-li to potřeba.
> 5. Když si zdroje odporují, nerozhoduj: vypiš rozpor a podle hierarchie zdrojů (12 kap. 3b.3) uveď, co platí. Zapiš otázku k dotčenému dokumentu, u rozporu mezi dokumenty i položku fronty pro Auditora.
> 6. `outdated`, `superseded` a `archived` dokumenty uváděj jen jako historii a označ je. Položky z `Inbox/` a nezařazené ze `Scratch/` jsou **neověřené**.

> ## Známé pasti
> - Doplnit odpověď z obecných znalostí nebo z odhadu; v dokumentaci to není, takže to patří do *Mezer*.
> - Citovat zavržený návrh nebo zastaralý dokument jako platný.
> - Vydávat návrh za realizaci („kovárna má pultovou střechu“, když to říká jen návrh).
> - Číst celý vault místo indexu (`find`) nebo celý dlouhý dokument místo sekcí; je to pomalé a do kontextu se dostane šum.
> - V chatu bez balíčku napsat jen „pošli podklady“; GameDesigner pak neví, co připravit.
> - Pracovat s balíčky, když relace vidí vault přes připojenou složku (modul `start`, krok 0).

#### `agents/modules/start.md` (změněný)
- Sekce: Postup (změněná), Známé pasti (změněná)
- Nové znění: 3429 znaků, nad 3000; přečti sekce v `_core/agents/modules/start.md`.

#### `agents/modules/task_close.md` (změněný)
- Sekce: Postup (změněná)
- Nové znění: 3219 znaků, nad 3000; přečti sekce v `_core/agents/modules/task_close.md`.

#### `agents/modules/ue_lookup.md` (změněný)
- Sekce: Postup (změněná), Známé pasti (změněná)

> ## Postup
> 1. **Jen čtení.** Používej jen čtecí dotazy core (`hestia.py ue_query`, 13 kap. 10.11); nikdy nezapisuj do levelu ani assetů, nespouštěj obecný Python ani build. Bez `Maintenance/taxonomy_local/ue_map.yaml` se Unreal nečte; entita bez pravidla v něm nemá report.
> 2. **Etapa 1** (skript v editoru):
>    - `python _core/scripts/hestia.py ue_query --emit --entity <Entita> --apply` (nebo `--all`) vygeneruje čtecí skript do `Maintenance/ue/`;
>    - GameDesigner ho spustí v editoru (*Tools → Execute Python Script*), skript zapíše surový výsledek vedle sebe;
>    - `ue_query --import --entity <Entita> --apply` (nebo `--all`) uloží report `Maintenance/reports/ue_<entita>.json`, pak `hubs --apply` obnoví blok `## Stav v UE` v hubu.
>    V chatu bez vaultu požádej GameDesignera o spuštění a o report. Relace, která vault vidí, ale skript core spustit nemůže, požádá o vygenerování a import toho, kdo ho spustit může, přesně těmito příkazy.
> 3. Když editor neběží, použij poslední report a uveď jeho datum; report starší než `ue_report_days` je v hubu označený jako starý.
> 4. Report ukazuje jen měřitelné signály (actory podle třídy, zástupné meshe `/Engine/BasicShapes/`, výchozí materiály, fáze `stage:*`, rozsah, vlastní a za potomky). Úroveň realizace se automaticky neodhaduje: porovnej ji s `depth_*` podle vodítka (12 kap. 3b.8): jen polohy → blockout, rozměry a kolize → greybox, proxy meshe a tagy → whitebox, meshe a data → asset_data, Blueprint a logika v provozu → functional.
> 5. Neshodu reportu s `depth_*` zapiš jako otázku nebo ji nech na auditu (G10). `depth_*` neměníš; mění ho ten, kdo realizoval, nebo GameDesigner.
> 6. **Report a `state`:** při odpovědi o realizaci porovnej report se `state` entity. Je-li report novější a stavbu ukazuje, platí „v levelu je“ (s datem reportu), i když starší `state` píše „neověřeno“ nebo „neběželo“; rozpor řekni a starší text nepřebírej. Report nepotvrzuje vzhled ani funkci: ty platí jen z § *Vizuálně ověřeno* ve `state` (kdo, kdy). Když `state` měníš, doplň § *V levelu* podle reportu (stavby, datum reportu, odkaz). Hub to připomene v bloku `## Stav v UE`, audit jako G10 (12 kap. 3b.8, zadání 0.19).
> 7. V chatu bez vaultu pracuj jen s reportem, který máš v balíčku kontextu. **Bez balíčku** řekni přesně, který potřebuješ: `hestia.py compose_context --entity <Entita> --apply` (hub entity s blokem `## Stav v UE`, tedy souhrn posledního reportu a jeho datum), nebo přístup k vaultu. Ve vaultu čti report `Maintenance/reports/ue_<entita>.json` přímo.

> ## Známé pasti
> - Vydávat starý report za aktuální stav bez data.
> - „Opravit“ `depth_*` podle reportu; to je rozhodnutí realizátora nebo GameDesignera.
> - Převzít ze starého `state` „neověřeno“, když novější report stavbu ukazuje; nebo naopak brát report jako vizuální potvrzení.
> - Spustit v editoru skript, který není čtecí dotaz core.

#### `agents/write_rules.md` (změněný)
- Sekce: Zásady zápisu (nová), Matice pravomocí (změněná), Knihovník (           , 05 kap. 3.2a) (změněná)
- Nové znění: 4720 znaků, nad 3000; přečti sekce v `_core/agents/write_rules.md`.

#### Role a soubory
- Architect: `agents/CONTRACT.md`, `agents/modules/chat_entry.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/modules/ue_lookup.md`, `agents/write_rules.md`
- Builder: `agents/CONTRACT.md`, `agents/modules/chat_entry.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/modules/ue_lookup.md`, `agents/write_rules.md`
- Furnisher: `agents/CONTRACT.md`, `agents/modules/chat_entry.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/write_rules.md`
- GameDesign: `agents/CONTRACT.md`, `agents/modules/chat_entry.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/write_rules.md`
- Curator: `agents/CONTRACT.md`, `agents/Curator.md`, `agents/modules/chat_entry.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/write_rules.md`
- Auditor: `agents/CONTRACT.md`, `agents/modules/chat_entry.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/modules/ue_lookup.md`, `agents/write_rules.md`
- Librarian: `agents/CONTRACT.md`, `agents/Librarian.md`, `agents/modules/canon_check.md`, `agents/modules/chat_entry.md`, `agents/modules/file_info.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/lookup.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/modules/ue_lookup.md`, `agents/write_rules.md`

### CR k ověření
- CR_2026-11-21_inbox_import_seznamy_v_li (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR_2026-11-21_podnety_roli_pres_frontu (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR_2026-11-21_ue_cteni_vs_state (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR_2026-11-21_kontrakt_rozdeleni (ověřit v instanci, do *Průběhu* `in_pilot`)

## Přechod 0.20.1 → 0.21.1
- Stav: dokončeno
- Výměna `_core/`: starý core v `_to_delete/_core_0.20.1/`; řádek v `structure_version.md`.
- Záznamy manifestu: 0.21.0, 0.21.1.

### Automatické kroky
- `compose_role`: v pořádku
  - změněné kompiláty: 5 z 5

### Kontroly (dry-run)
- lint: chyby 0, upozornění 9, informace 19
- audit: chyby 0, upozornění 53, informace 68

### Ruční úkoly
- `update_core:0.21.0:structure_log_cr` (ve frontě): Projít záznamy structure_log.md, které lint hlásí kvůli buňce cr (–, -, samotné cr:, volný text): s člověkem rozhodnout, které vyexportovat (export_cr), a u ostatních nastavit cr: none (13 kap. 10.8)

### Změny instrukcí
- Změněné soubory: 5. Role si změny vypíše `role_diff <Role>`.

#### `agents/Auditor.md` (změněný)
- Sekce: Formáty výstupů (změněná)

> ## Formáty výstupů
> - Report podle šablony `tpl_report`: *Souhrn*, *Nálezy podle závažnosti* (chyba, upozornění, informace; ke každému návrh opravy), *Zralost*, *Doporučené kroky*.
> - Nálezy strojově: `[{code, severity, target, file, message}]`.
> - Položka fronty: `F-0001 | priority | finding | G-kód | cíl | návrh opravy | open`.
> - Návrh do `structure_log.md`: `| datum | kategorie | popis | dopad | navrhovaná změna | |` (buňka `cr` prázdná; pomlčku ani text nepsat).

#### `agents/Curator.md` (změněný)
- Sekce: Co děláš a co ne (změněná), Postupy podle zakázky (změněná), Formáty výstupů (změněná)
- Nové znění: 3818 znaků, nad 3000; přečti sekce v `_core/agents/Curator.md`.

#### `agents/modules/hestia_feedback.md` (změněný)
- Sekce: Postup (změněná), Výstup (změněná), Známé pasti (změněná)

> ## Postup
> 1. Change request nezakládáš a do `structure_log.md` ani `outbox/` nepíšeš: CR mimo kanál Curatora (`export_cr`) by nikdo nezpracoval.
> 2. **Režim vault:** připiš na konec `Maintenance/queue.md` položku `kind: proposal`, `code: hestia`, nebo s navrženou kategorií logu `code: hestia:<kategorie>` (`friction`, `missing`, `surplus`, `collision`, `taxonomy`, `works`, `idea`), `target` = čeho se týká (entita, dokument nebo část Hestie, např. `tpl_state`, `audit G10`), `proposal` = `<role>: co se stalo (doklad: <odkaz>) → navrhovaná změna`, kde `<odkaz>` je wikilink na poznámku nebo cesta v backtickách, za ním případně řádek nebo datum (např. „doklad: `Maintenance/changes.md` 2026-11-21“; samotný popis řádku bez odkazu `feedback_log` nezapíše), `priority: medium` (`high` jen když podnět blokuje práci), `state: open`. Schválení GameDesignera k zápisu není potřeba.
> 3. **Režim chat:** podnět dej do zápisu Hestia, sekce *Podněty pro Hestii* (modul `chat_entry`); do fronty ho zapíše ten, kdo zápis zapracuje.
> 4. Podnět uveď v hlášení na konci tasku (`task_close`, krok 11).

> ## Výstup
> Položka fronty `P-…` s kódem `hestia` nebo `hestia:<kategorie>` (nebo sekce v zápisu Hestia). Curator ji převede do `structure_log.md` příkazem `hestia.py feedback_log` a uzavře; o CR rozhoduje člověk při `export_cr`.

> ## Známé pasti
> - Založit CR přímo v `outbox/` nebo v repozitáři projektu: zůstane mimo kanál a nikdo ho nezpracuje.
> - Podnět bez dokladu, nebo s dokladem, který nejde dohledat (wikilink na existující poznámku nebo existující cesta v backtickách): `feedback_log` ho nezapíše. Doklad „řádek ve changes.md“ bez odkazu neprojde.
> - Zaměnit podnět s otázkou (`question`) nebo s nálezem údržby (zapisuje Auditor).

#### `agents/modules/start.md` (změněný)
- Sekce: Postup (změněná), Známé pasti (změněná)
- Nové znění: 3859 znaků, nad 3000; přečti sekce v `_core/agents/modules/start.md`.

#### `agents/modules/ue_lookup.md` (změněný)
- Sekce: Postup (změněná)
- Nové znění: 3309 znaků, nad 3000; přečti sekce v `_core/agents/modules/ue_lookup.md`.

#### Role a soubory
- Architect: `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/ue_lookup.md`
- Builder: `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/ue_lookup.md`
- Furnisher: `agents/modules/hestia_feedback.md`, `agents/modules/start.md`
- GameDesign: `agents/modules/hestia_feedback.md`, `agents/modules/start.md`
- Curator: `agents/Curator.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`
- Auditor: `agents/Auditor.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/ue_lookup.md`
- Librarian: `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/ue_lookup.md`

### CR k ověření
- CR-022_prostredi_core (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-023_update_core_pripojena_slozka (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-024_ue_signal_basicshapes (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-025_ue_ism_bounds (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-030_export_cr_prazdne_cr (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-031_podnety_do_structure_log_skriptem (ověřit v instanci, do *Průběhu* `in_pilot`)

### Pracovní kopie
- Pracovní adresář: `/sessions/rcw-01nw4mxpuk2thvsg4ues1vms/hestia_work_p17`.
- Kontrola originálu: beze změny od snímku (1386 souborů).
- Přeneseno: změněné 8, nové 0, přesunuté 0; `_core/` vyměněn (starý v `_to_delete/_core_0.20.1/`).
  - ~ `Maintenance/queue.md`
  - ~ `Maintenance/reports/update_core_2026-11-22.md`
  - ~ `Maintenance/structure_version.md`
  - ~ `Roles/_compiled/Architect_compiled.md`
  - ~ `Roles/_compiled/Builder_compiled.md`
  - ~ `Roles/_compiled/Furnisher_compiled.md`
  - ~ `Roles/_compiled/GameDesign_compiled.md`
  - ~ `Roles/_compiled/Librarian_compiled.md`
- Čas fází: kopie 65.0 s, přechod 117.8 s, zápis zpět 55.0 s.
