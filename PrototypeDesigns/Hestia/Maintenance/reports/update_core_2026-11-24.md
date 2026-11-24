---
type: report
updated: 2026-11-24
---
# Aktualizace core 2026-11-24

## Přechod 0.23.0 → 0.25.0
- Stav: dokončeno
- Výměna `_core/`: starý core v `_to_delete/_core_0.23.0/`; řádek v `structure_version.md`.
- Záznamy manifestu: 0.24.0, 0.25.0.

### Automatické kroky
- `hubs`: v pořádku
  - změněné soubory: 0
- `compose_role`: v pořádku
  - změněné kompiláty: 0 z 7
  - changed (nahrát do Claude Projectu): žádný
  - unchanged (nenahrávat): Roles/_compiled/Architect_compiled.md, Roles/_compiled/Builder_compiled.md, Roles/_compiled/Crafter_compiled.md, Roles/_compiled/Curator_compiled.md, Roles/_compiled/Furnisher_compiled.md, Roles/_compiled/GameDesign_compiled.md, Roles/_compiled/Librarian_compiled.md

### Kontroly (dry-run)
- lint: chyby 0, upozornění 0, informace 9
- audit: chyby 0, upozornění 42, informace 54

### Ruční úkoly
- `update_core:0.24.0:own_targets` (ve frontě): Projít cíle a realizaci entit s potomky (target_*, depth_*): od 0.24.0 patří jen vlastní části rodiče (zdivo stavby, terén regionu, hradby) a rodič s cílem se počítá do zralosti jako další jednotka; souhrn potomků z rodiče odebrat, rodič bez vlastní části (obálka) cíl ani depth nemá (01 kap. 5, 04 kap. 3). Návrh dat dělá Curator, rozhoduje GameDesigner
- `update_core:0.25.0:steward_active` (ve frontě): Rozhodnout steward_active v Maintenance/config.yaml (GameDesigner): true = Steward vlastní export_cr a weekly (profil core _core/agents/Steward.md, kompilát compose_role Steward), false (výchozí) = export_cr dělá Curator jako náhradník a weekly spouští člověk (13 kap. 10.20)
- `update_core:0.25.0:hestia_python` (ve frontě): Zapsat hestia_python do Maintenance/config.yaml: cesta k interpretu Python >= 3.11 s PyYAML pro příkazy core (při starém Pythonu ji navrhne doctor); uvést ji i s cestou k vaultu v pokynech první zprávy agentů (šablona v README core, CR-039)
- `update_core:0.25.0:weekly_task` (ve frontě): Volitelně nastavit naplánovanou úlohu weekly --apply (Claude scheduled task, cron nebo Plánovač úloh Windows) s pevnou cestou k interpretu z hestia_python, na připojené složce s --work-copy; návod v README core (13 kap. 10.20, rozhodnutí GameDesignera)
- `update_core:0.25.0:outbox_sent` (ve frontě): Založit Maintenance/outbox/sent/ a přesunout do něj už odeslané CR a hlášení (odesílá a přesouvá člověk; export_cr ani lint sent/ nekontrolují)

### Změny instrukcí
- Změněné soubory: 14. Role si změny vypíše `role_diff <Role>`.

#### `agents/CONTRACT.md` (změněný)
- Sekce: Spouštěče (změněná)

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
> | potřebný knihovní asset chybí, graybox místo něj | `asset_request` |
> | výroba nebo změna knihovního assetu | `asset_work` |
> | předání jiné roli nebo relaci | `handover_out` |
> | problém s Hestií jako nástrojem | `hestia_feedback` |
> | aktualizace core, ruční úkoly z manifestu (Steward) | `core_update` |
> | týdenní běh, kontrola zdraví (Steward) | `instance_health` |
> | podněty a hlášení pro HearthLore (Steward) | `hearthlore_report` |
> | práce v režimu chat | `chat_entry` |
> | konec tasku | `task_close` |
>
> Modul načti, když nastane spouštěč, i když ho profil neuvádí; kdy modul předáš jiné roli, říká `start`. Moduly: `_core/agents/modules/`, lokální `Roles/modules/`.

#### `agents/Curator.md` (změněný)
- Sekce: Co děláš a co ne (změněná), Postupy podle zakázky (změněná)
- Nové znění: 4683 znaků, nad 3000; přečti sekce v `_core/agents/Curator.md`.

#### `agents/Steward.md` (nový)
- Sekce: (frontmatter) (nová), (úvod) (nová), Co děláš a co ne (nová), Start protokol (nová), Matice pravomocí (nová), Postupy podle zakázky (nová), Formáty výstupů (nová), Kdy se zeptat člověka (nová), Známé pasti (nová), Zápis do logů (nová)
- Nové znění: 4914 znaků, nad 3000; přečti sekce v `_core/agents/Steward.md`.

#### `agents/modules/core_update.md` (nový)
- Sekce: (frontmatter) (nová), (úvod) (nová), Kdy (nová), Postup (nová), Výstup (nová), Známé pasti (nová)

> type: agent_module
> module_id: core_update
> trigger: aktualizace core, ruční úkoly z manifestu
> requires: []
> modes: [vault]
> validity: valid
> compile: listed

> # Aktualizace core (Steward)

> ## Kdy
> GameDesigner chce novou verzi core, `health` nebo `doctor` hlásí novější značku, nebo čekají ruční úkoly `update_core:*` ve frontě.

> ## Postup
> 1. `doctor`: Python, PyYAML, `core_source`, necommitnuté změny (před `--apply` musí být vault commitnutý).
> 2. Před aktualizací odešli čekající podněty (modul `hearthlore_report`: `feedback_log`, `export_cr`).
> 3. Dry-run `update_core --latest` (na připojené složce `--work-copy`): rozdíl, poznámky z `CHANGELOG.md`, manifest (automatické kroky, ruční úkoly, CR k ověření, *Změny instrukcí*).
> 4. Hlášení GameDesignerovi: verze od → do, co se změní, ruční úkoly, migrace; počkej na schválení.
> 5. `update_core --latest --apply` (s `--work-copy`, je-li vault na připojené složce). Selže-li krok, `update_core --after-only --apply`.
> 6. Report `Maintenance/reports/update_core_RRRR-MM-DD.md`: zkontroluj kroky; ruční úkoly jsou ve frontě (`T-…`), projdi je s GameDesignerem a hotové uzavři (`state`, `closed`).
> 7. Kompiláty: do Claude Projectu nahraj jen `changed` z reportu `compose_role`; `unchanged` nech. Role se změněným základem: `role_diff <Role>`.
> 8. CR k ověření (`crs` v manifestu) uveď v hlášení pro HearthLore (modul `hearthlore_report`) s výsledkem ověření.

> ## Výstup
> Nový `_core/`, report `update_core_…`, ruční úkoly ve frontě, hlášení GameDesignerovi a podklad pro hlášení HearthLore.

> ## Známé pasti
> - `--apply` bez schválení nebo s necommitnutými změnami.
> - Na připojené složce přechod bez `--work-copy` nestihne limit volání; pracovní adresář z výpisu zadej v dalším volání výslovně.
> - Ruční úkol uzavřít dřív, než je práce hotová a ověřená.

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
>    **Délka dokumentu (G14, 04 kap. 4):** počítají se znaky těla bez frontmatteru a bez generovaných bloků (`hestia:generated`); `Maintenance/` a `Dashboard/` se nepočítají, dokument se `status: rejected` nebo `validity: superseded`/`archived` je neaktivní. Velikost je v `doc_index` (pole `chars`) a v `section <dokument> --list`. Prahy z `config.yaml`: doménový dokument nebo `state` nad `doc_summary_chars` (6 000) potřebuje `## Souhrn` hned za titulem; nad `doc_split_chars` (20 000) rozdělit tematicky; předání nad `handover_max_chars` (4 000) obsahuje víc než zadání a odkazy.
> 3. Urči entitu a doménu podle hubu a indexu dokumentů (`lookup`). Když nejde jednoznačně říct, je-li to návrh, nebo realizace, nebo které entity se týká, **zeptej se**; nedomýšlej.
> 4. Rozliš formu (12 kap. 3b.2): **doslovná textace** GameDesignera se zapíše přímo, se zdrojem (chat, datum) a řádkem v `changes.md`, i do nového dokumentu; **přeformulování, sloučení, zkrácení** předlož ke schválení jako diff. Doslovná textace v rozporu s kánonem nikdy přímo.
> 5. Před zápisem spusť `completeness`, pak zapiš na určené místo; přepis platného textu jen s `nahradit:` nebo po schválení (12 kap. 6.1).

#### `agents/modules/handover_out.md` (změněný)
- Sekce: Známé pasti (změněná)

> ## Známé pasti
> - Předání delší než `handover_max_chars` (výchozí 4 000 znaků, G14c): obsahuje víc než zadání a odkazy; rozhodnutí patří do `Docs/` hned. Počítají se znaky těla bez frontmatteru a bez generovaných bloků; délku ukáže `section <předání> --list`. Archivované předání se nepočítá.
> - Předání bez `for_role`: role ho v `agenda` uvidí jen mezi předáními pro kohokoli.
> - Kopírovat návrh do předání: po archivaci se ztratí, nebo se rozejde s `Docs/`.
> - Nechat dvě aktivní předání pro stejnou oblast.

#### `agents/modules/hearthlore_report.md` (nový)
- Sekce: (frontmatter) (nová), (úvod) (nová), Kdy (nová), Postup (nová), Výstup (nová), Známé pasti (nová)

> type: agent_module
> module_id: hearthlore_report
> trigger: dávka podnětů, před aktualizací, po ověření CR z nové verze
> requires: []
> modes: [vault]
> validity: valid
> compile: listed

> # Podněty a hlášení pro HearthLore (Steward)

> ## Kdy
> Po každé dávce `feedback_log`, před každou aktualizací core a po ověření CR, které přinesla nová verze.

> ## Postup
> 1. Podněty z fronty: `feedback_log` (dry-run, pak `--apply`); podnět „k ruční opravě“ oprav podle důvodu ve výpisu.
> 2. `export_cr` (dry-run, pak `--apply`): záznamy `structure_log.md` bez `cr`, jeden záznam = jeden CR v `outbox/`; doplň *Dopad* a *Alternativy*. Co CR nebude, označ s člověkem `cr: none`.
> 3. Forma podle obsahu: žádost o změnu Hestie a sdílené know-how = CR; informace o stavu instance (ověřené CR, verze, slabá místa) = hlášení.
> 4. Hlášení `outbox/report_RRRR-MM-DD.md` podle `tpl_report_hearthlore`: *Přehled CR instance* ze `structure_log.md` (sloupec `cr`) a z `outbox/` (připravené, v `outbox/sent/` odeslané); stav v HearthLore neuvádíš.
> 5. Odesílá člověk; odeslané soubory přesouvá do `outbox/sent/` on.

> ## Výstup
> CR a hlášení v `Maintenance/outbox/`, připravené k odeslání; `structure_log.md` s vyplněnou buňkou `cr`.

> ## Známé pasti
> - Víc záznamů v jednom CR: každý se přijímá a zapracovává zvlášť.
> - Stav informace (ověřené CR) poslat jako CR místo hlášení.
> - Podněty nechat ležet ve `structure_log.md` až do měsíčního exportu.

#### `agents/modules/hestia_feedback.md` (změněný)
- Sekce: Známé pasti (změněná)

> ## Známé pasti
> - Založit CR přímo v `outbox/` nebo v repozitáři projektu: zůstane mimo kanál a nikdo ho nezpracuje.
> - Podnět bez dokladu, nebo s dokladem, který nejde dohledat: `feedback_log` ho nezapíše a vypíše ho s ID a důvodem jako „k ruční opravě“. Platný doklad: wikilink na existující poznámku, existující cesta v backtickách ve vaultu nebo v projektu (i mimo vault, od kořene projektu), nebo URL. Doklad „řádek ve changes.md“ bez odkazu neprojde. Závorka `(doklad: …)` končí párovou závorkou, vnořené závorky v ní nevadí (např. „`hestia.py audit` (dry-run)“).
> - Zaměnit podnět s otázkou (`question`) nebo s nálezem údržby (zapisuje Auditor), nebo s prací pro jinou roli (úkol pro roli `code: role:<Role>`, `write_rules.md`).

#### `agents/modules/instance_health.md` (nový)
- Sekce: (frontmatter) (nová), (úvod) (nová), Kdy (nová), Postup (nová), Výstup (nová), Známé pasti (nová)

> type: agent_module
> module_id: instance_health
> trigger: týdenní běh, pokyn ke kontrole zdraví
> requires: []
> modes: [vault]
> validity: valid
> compile: listed

> # Zdraví instance (Steward)

> ## Kdy
> Týdenní běh (`weekly`, naplánovaná úloha nebo pokyn), nebo GameDesigner chce vědět, v jakém stavu je instance.

> ## Postup
> 1. `weekly --apply` (vault na připojené složce s `--work-copy`), nebo přečti výsledek naplánované úlohy `Maintenance/reports/weekly_RRRR-MM-DD.md`. Samotná kontrola: `health` (s `--apply` report `health_…`).
> 2. U každé sekce `pozor` (prostředí, verze core, kompiláty, ruční úkoly, podněty, outbox, Unreal) vylož, co nález znamená, a navrhni krok z reportu.
> 3. Nálezy auditu: počty proti minulému týdnu; chyby G6, G7 a upozornění předej rolím, které je vlastní (úkol ve frontě `code: role:<Role>`), obsah sám neopravuj.
> 4. Hlášení GameDesignerovi: co je v pořádku, co čeká, doporučené kroky; zásah až po schválení.

> ## Výstup
> Reporty `weekly_…` a `health_…`, hlášení GameDesignerovi, případně úkoly pro role ve frontě.

> ## Známé pasti
> - Opravit obsah kvůli nálezu: kontrola jen hlásí a navrhuje.
> - Spustit `update_core --apply` z kontroly zdraví bez schválení (modul `core_update`).
> - Brát starý report Unrealu jako chybu: čtecí dotaz má smysl, jen když běží editor.

#### `agents/modules/metadata.md` (změněný)
- Sekce: Postup (změněná)

> ## Postup
> 1. Nový dokument zakládej ze šablony v `_core/templates/` (`tpl_<typ>`).
> 2. Projektová role vyplní minimální povinnou sadu:
>    - `type`, `validity`, `updated`;
>    - `domain` (u přesahu `domains`) a `entity`;
>    - u hubu po své práci `depth_<doména>` a `status`, jen když jsi realizoval (Unreal, data, skripty, StateTree, animace); návrh `depth_*` nemění, hloubka návrhu se počítá z dokumentů.
>    Zbytek (kategorie, aliasy, vazby) doplní Curator.
> 3. Hodnoty ber z taxonomie (`_core/taxonomy/` a `Maintenance/taxonomy_local/`); novou hodnotu nevymýšlej, navrhni ji Curatorovi.
> 4. Frontmatter upravuj po řádcích: neměň pořadí klíčů, komentáře `# orchestrace` / `# hra` ani uvozovky.
>    **Zralost (04 kap. 3):** jednotky = entita a všichni potomci podle `parent`, kteří mají v doméně vlastní `target_d` > 0 (bez `status` `rejected`, `on_hold`); cíl a `depth_d` rodiče patří jen jeho vlastní části, rodič bez cíle je obálka.
>    - dosaženo: `depth_d` v režimu `build`, hloubka návrhu (nejvyšší `depth` platných `concept`, `design`, `spec`) v režimu `design`;
>    - zralost = splněné jednotky / jednotky; hloubka = nejslabší jednotka.
> 5. `kind`, `parent`, `located_in`, `derived_from`, `alternative_to` hubu měníš jen po schváleném návrhu; `target_*` jen určená role nebo člověk, se zápisem do `changes.md`.
> 6. Změnu metadat ve více než 10 souborech nech předem schválit (seznam změn z dry-run).

#### `agents/modules/start.md` (změněný)
- Sekce: Postup (změněná), Známé pasti (změněná)
- Nové znění: 4427 znaků, nad 3000; přečti sekce v `_core/agents/modules/start.md`.

#### `agents/modules/task_close.md` (změněný)
- Sekce: Postup (změněná)
- Nové znění: 3313 znaků, nad 3000; přečti sekce v `_core/agents/modules/task_close.md`.

#### `agents/review_plan.md` (změněný)
- Sekce: Kdy a co (změněná)

> ## Kdy a co
>
> | Kdy | Co | Kdo |
> |---|---|---|
> | Po každém tasku | `task_close`: `lint` dotčených souborů (G6, G7), G11 dotčených entit | projektová role, orchestrační agent |
> | Při změně core nebo profilu role | `compose_role` (kompiláty pro chat) | Curator |
> | Při novém obsahu v `Inbox/` | metadata importu | Curator |
> | Na pokyn GameDesignera (typicky v chatu) | třídění inboxu `raw` → `prepared` (12 kap. 3b.7) | Knihovník + člověk |
> | Týdně | `weekly` (13 kap. 10.20): `audit` G1–G15, zralost, `asset_index`, `hubs`, `doc_index`, `health`; otevřené otázky podle stáří, metriky Knihovníka (12 kap. 3b.9); čtecí dotaz do Unrealu, běží-li editor (12 kap. 3b.8). Naplánovaná úloha instance (README core), bez zásahu do obsahu | Steward (bez Stewarda Auditor a Curator, `weekly` spouští člověk) |
> | Po každé dávce `feedback_log` a před každou aktualizací core | `export_cr` a hlášení pro HearthLore (`outbox/report_…`) | Steward |
> | Při uzavření fáze prototypu | revize `target_*`, dokumentační dluh, master lore (G12) | Auditor + člověk |
> | Při nové doméně, kategorii, kroku nebo `kind` | zápis do `taxonomy_local` a `structure_log` | Curator |
> | Měsíčně | `structure_log` → change requesty (`export_cr`), jen bez aktivního Stewarda (`steward_active: false`) | Curator + člověk |

#### `agents/write_rules.md` (změněný)
- Sekce: Steward (05 kap. 3.2b) (nová)

> ## Steward (05 kap. 3.2b)
>
> Steward spravuje Hestii jako nástroj (verze core, zdraví instance, komunikace s HearthLore). Při `steward_active: false` (`config.yaml`, výchozí) není aktivní: `export_cr` dělá Curator jako náhradník a `update_core` člověk.
>
> | Oblast | Steward |
> |---|---|
> | `_core/` | jen `update_core` (dry-run sám, `--apply` po schválení) |
> | `config.yaml`, `taxonomy_local/ue_map.yaml` | ✔ po schválení (klíče související s verzí core a ručními úkoly) |
> | `Roles/` (profily, lokální moduly) | ✔ jen na výslovný pokyn GameDesignera nebo podle schváleného ručního úkolu |
> | `Roles/_compiled/`, `doc_index`, generované výstupy | ✔ (skripty) |
> | `outbox/` (change requesty, hlášení) | ✔ připravuje (CR sdíleně s Curatorem, hlášení sám); odesílá člověk, odeslané přesune do `outbox/sent/` |
> | `queue.md`, `reports/` | ✔ |
> | `changes.md`, `structure_version.md`, `structure_log.md` | ✔ jen připisovat |
> | Obsah (`Docs/`, huby, `depth_*`, `target_*`, `KnowHow/`, `Handovers/`, `Inbox/`, `Scratch/`) | ✘ |

#### Role a soubory
- Architect: `agents/CONTRACT.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/metadata.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/write_rules.md`
- Builder: `agents/CONTRACT.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/metadata.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/write_rules.md`
- Crafter: `agents/CONTRACT.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/metadata.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/write_rules.md`
- Furnisher: `agents/CONTRACT.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/metadata.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/write_rules.md`
- GameDesign: `agents/CONTRACT.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/metadata.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/write_rules.md`
- Curator: `agents/CONTRACT.md`, `agents/Curator.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/metadata.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/review_plan.md`, `agents/write_rules.md`
- Auditor: `agents/CONTRACT.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/metadata.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/review_plan.md`, `agents/write_rules.md`
- Librarian: `agents/CONTRACT.md`, `agents/modules/file_info.md`, `agents/modules/handover_out.md`, `agents/modules/hestia_feedback.md`, `agents/modules/metadata.md`, `agents/modules/start.md`, `agents/modules/task_close.md`, `agents/write_rules.md`

### CR k ověření
- CR-035_zralost_rodicu_a_matice (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-033_vykon_pripojena_slozka (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-034_kompilaty_hlavicka_verze (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-036_assety_po_prevodu (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-037_manifest_assetu_tabulky_a_data (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-038_pravidla_roli_v_dokumentaci (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-039_start_cesta_a_interpret (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-040_drobne_opravy_kontrol (ověřit v instanci, do *Průběhu* `in_pilot`)

### Pracovní kopie
- Pracovní adresář: `/sessions/rcw-01nw4mxpuk2thvsg4ues1vms/hestia_work_p21`.
- Kontrola originálu: beze změny od snímku (1970 souborů).
- Přeneseno: změněné 30, nové 2, přesunuté 0; `_core/` vyměněn (starý v `_to_delete/_core_0.23.0/`).
  - ~ `Dashboard/Index.md`
  - ~ `Dashboard/views/generated/entity_domain_matrix.md`
  - ~ `Entities/Brana_Straz.md`
  - ~ `Entities/Characters.md`
  - ~ `Entities/Hradby_a_Brana.md`
  - ~ `Entities/Lapikus.md`
  - ~ `Entities/Lapikus_Region.md`
  - ~ `Entities/Nadvori.md`
  - ~ `Entities/Palac.md`
  - ~ `Entities/Palac_Kovarna.md`
  - ~ `Entities/Vez.md`
  - ~ `Maintenance/doc_index.json`
  - ~ `Maintenance/queue.md`
  - ~ `Maintenance/structure_version.md`
  - ~ `Roles/_compiled/Architect_compiled.md`
  - ~ `Roles/_compiled/Builder_compiled.md`
  - ~ `Roles/_compiled/Crafter_compiled.md`
  - ~ `Roles/_compiled/Curator_compiled.md`
  - ~ `Roles/_compiled/Furnisher_compiled.md`
  - ~ `Roles/_compiled/GameDesign_compiled.md`
  - ~ `Roles/_compiled/Librarian_compiled.md`
  - ~ `Steps/01_terrain.md`
  - ~ `Steps/03_ruin.md`
  - ~ `Steps/03_ruin_generator.md`
  - ~ `Steps/03_ruin_upravy.md`
  - ~ `Steps/05_constructions.md`
  - ~ `Steps/05_constructions_dum.md`
  - ~ `Steps/05_constructions_kovarna.md`
  - ~ `Steps/05_constructions_ostroh.md`
  - ~ `Steps/05_constructions_vez.md`
  - + `Maintenance/doc_index_text.json`
  - + `Maintenance/reports/update_core_2026-11-24.md`
- Čas fází: kopie 105.2 s, přechod 99.5 s, zápis zpět 80.2 s.
