# Changelog – Hestia core

Verze `MAJOR.MINOR.PATCH` podle zadání 11, kap. 5 (`hearthlore/zadani/11_vyvojovy_cyklus.md`). MAJOR verze nese migrační poznámku.

## 0.21.1 – 2026-11-22

PATCH k vlně 0.22 (zadání 0.22.1, odpovědi na otázky k 0.21.0; předání `predani_vyvoj_core_soubeh` položka 39; CR-023, CR-025 bod 2, CR-031); bez migrace. Po aktualizaci `compose_role` (moduly `ue_lookup`, `hestia_feedback`). Nový klíč `ue_pivot_far_cm` v `defaults.yaml` (výchozí 500), v `config.yaml` instance nepovinný. **První přechod na 0.21.1 s `--work-copy`** ze staršího core jde skriptem nové verze s `--from`; na připojené složce se verze vezme `git archive v0.21.1 hestia` do lokálního adresáře VM (13 kap. 10.6 bod 9).

- **`update_core --after-only --work-copy [<adresář>] --apply`** (13 kap. 10.6 bod 8; CR-023): stejné fáze jako přechod (kopie se snímkem, kroky po aktualizaci nad `_core/` kopie, kontrola originálu, zápis zpět bez mazání), bez zdroje core a výměny. Režim (`mode: update | after_only`) je ve značce `hestia_work.json`; další fáze ho převezmou, kopii pro přechod nejde dokončit jako `--after-only` ani obráceně (chyba použití). Selže-li krok po aktualizaci v kopii, zápis zpět proběhne, kód 1 a výpis doporučí `update_core --after-only --work-copy --apply` (na lokálním disku i bez `--work-copy`). Dry-run `--after-only --work-copy` ohlásí, že s `--apply` proběhnou kroky v kopii.
- **Výpis pracovního adresáře** (13 kap. 10.6 bod 6): zvolený adresář se vypíše hned na začátku (stderr, i s `--quiet`, aby zůstal i po přerušení volání), ve výsledku (i u smazaného adresáře a v návrhu další fáze) a v reportu (`### Pracovní kopie`).
- **Rozsah z geometrie** (13 kap. 10.11; CR-025 bod 2, ověřeno T-0020): `hestia_ue.py` počítá `bounds` actoru jako sjednocení rozsahů komponent s geometrií: statické meshe (`SystemLibrary.get_component_bounds`) a každá instance ISM ve světovém umístění (rozsah meshe přes `get_instance_transform(i, True)`); kořen a komponenty bez meshe se nezapočítají. Actor bez geometrie (BSP, světla) nebo s nečitelnou geometrií má rozsah z `get_actor_bounds` jako dřív; actor nese `bounds_from` (`geometry` / `actor`). Nové `pivot_offset` u actoru (vzdálenost kořene od středu rozsahu, cm) a v souhrnu `pivot_far` (počet actorů nad prahem) a `pivot_far_cm`. Práh z `ue_pivot_far_cm` (`config.yaml`, výchozí 500) jde v požadavku `ue_query --emit` (`pivot_far_cm`). Blok `## Stav v UE` uvede `pivot_far` jako informaci, je-li nenulový. Modul `ue_lookup`: rozsah z geometrie a `pivot_far` jako signál pro modelování, ne nález. Zástupný modul `unreal`: rozsah komponent, rozsah meshe, transformace instancí, poloha kořene.
- **`export_cr`, předání do HearthLore** (13 kap. 10.8): pod nadpisem CR poznámka, že se soubor neodesílá skriptem, uvede se v hlášení pro HearthLore nebo ho předá člověk, v instanci se nepřejmenovává, nečísluje a nekopíruje; zaeviduje ho agent HearthLore (`CR-NNN_<short_name>`, `source_id`). Výpis příkazu říká totéž místo věty o odeslání do `hearthlore/change-requests/`.
- **Modul `hestia_feedback`** (12 kap. 4.5; CR-031): doklad v podnětu = wikilink nebo cesta v backtickách, za ním případně řádek nebo datum; samotný popis řádku `feedback_log` nezapíše.
- Ověřeno proti zadání 0.22.1 beze změny kódu: kód nálezu `log` u buňky `cr` (`lint`, `task_close`, ne `audit`), `HESTIA_PROC_MOUNTS` v `doctor`, úrovně `doctor`, hledání pracovní kopie bez adresáře.
- Testy: 365. Nové: `test_work_copy.py` (`--after-only --work-copy` dá stejný výsledek jako `--after-only` bez kopie, výpis adresáře i s `--quiet`; režim mezi fázemi); `test_ue.py` (rozsah z instancí a komponenty bez kořene, actor bez geometrie, `pivot_offset`, `pivot_far` s prahem z požadavku; celou cestou: práh z `config.yaml`, report, blok v hubu); `test_export_cr.py` (poznámka o předání v těle a ve výpisu). Golden `expected/export_cr/` a kompiláty `expected/compose_role/` vědomě přegenerovány (poznámka o předání, moduly).

## 0.21.0 – 2026-11-22

Vlna před P17 (zadání 0.22; CR-022, CR-023, CR-024, CR-025 bod 1, CR-030, CR-031; předání `predani_vyvoj_core_soubeh` položky 37, 33, 34, 38, 35, 36, vydané spolu); bez migrace. Po aktualizaci `compose_role` (moduly `start`, `ue_lookup`, `hestia_feedback`, profily `Curator`, `Auditor`) a ruční úkol `update_core:0.21.0:structure_log_cr` (záznamy `structure_log.md` s neplatnou buňkou `cr`, které nově hlásí `lint`: s člověkem vyexportovat, nebo `cr: none`). Bez příznaku `roles` (profily projektových rolí se srovnávat nemusí). **První přechod na 0.21.0 s `--work-copy`** jde skriptem nové verze z pracovní kopie značky s `--from` (13 kap. 10.6, *První přechod*), protože `update_core` ve starém `_core/` přepínač nezná.

- **Vyplněné `cr` v `structure_log`** (13 kap. 10.8, 07 kap. 9, 05 kap. 7.3; CR-030, položka 37): `export_cr` bere jako vyplněné jen `cr: <ID>` (`CR_RRRR-MM-DD_<short_name>` i `CR-NNN_<short_name>`) a `cr: none`; prázdná buňka, `–`, `-`, samotné `cr:` a jiný text = nevyplněno, export je nabídne a vyplnění hodnotu nahradí (společná funkce `logs.cr_cell`). **`lint`** nad `structure_log.md` (i `--all`, i v `task_close`): neplatná buňka `cr` = upozornění s kódem `log` (formát logu, bez kódu G) a radou vyplnit při exportu, nebo nastavit `cr: none`; `audit` ho do fronty nedává. Šablona `tpl_structure_log`, `Curator.md` a `Auditor.md`: buňka `cr` prázdná, dokud se o CR nerozhodne.
- **`update_core --work-copy [<adresář>]`** (13 kap. 10.6; CR-023, položka 33; modul `workcopy.py`): jen s `--apply` (dry-run jen čte a ohlásí, že přechod proběhne v kopii). Kopie vaultu do lokálního adresáře (bez hodnoty dočasný `hestia_work_*`) se snímkem originálu (`snapshot.json`: cesta, velikost, sha256) a značkou `hestia_work.json` (originál, zdroj core, hotové fáze, časy); podle značky `Vault.load` pozná kopii a `project_root`, `core_source` a cesty ve výstupech bere z originálu (kód, Unreal a git se čtou z původního projektu). Přechod celý v kopii (výměna `_core/`, kroky po aktualizaci, report). Kontrola originálu proti snímku: soubor změněný, přibylý nebo zmizelý (a ne zapsaný dřívějším zápisem zpět) = kolize, nic se nezapíše, pracovní kopie zůstává, kód 1. Zápis zpět bez mazání: změněné soubory přepíše na místě, nové založí, `_core/` vymění dvěma přejmenováními (`_core` → `_to_delete/_core_<verze>/`, `_core.new` → `_core`), zmizelý soubor přesune tam, kde je v kopii pod `_to_delete/` soubor se stejným hashem, jinak do `_to_delete/<cesta>`. `--work-phase copy|run|back` (jedna fáze na volání), další běh se stejným adresářem pokračuje od nedokončené fáze (bez adresáře se najde nedokončená kopie téhož vaultu v dočasné složce), přerušený přechod v kopii dokončí kroky po aktualizaci, zápis zpět je opakovatelný (dopíše jen rozdíly, dokončí rozpracovanou výměnu `_core/`). Po úspěchu pracovní adresář smaže, po kolizi nebo chybě ho nechá, `--keep-work-copy` vždy. Oddíl přechodu v reportu má `### Pracovní kopie` (adresář, kontrola originálu, přenesené soubory: změněné, nové, přesunuté, výměna `_core/`, čas každé fáze).
- **Kontrola prostředí a `doctor`** (13 kap. 1, 3, 10.15; 12 kap. 3; CR-022, položka 34): `hestia.py` ověří Python ≥ 3.11 a PyYAML dřív, než importuje core (modul `envcheck.py`, jen standardní knihovna), a při chybě vypíše návod (`uv venv --python 3.12`, `python -m venv`, `pip install pyyaml`, prostředí mimo projekt a vault, oddíl *Prostředí*), kód 2. Nový příkaz **`doctor [--json]`**: OK / UPOZORNĚNÍ / CHYBA s návodem u Pythonu, PyYAML, gitu (chybí = upozornění), vaultu v repozitáři a necommitnutých změn (upozornění), nalezení vaultu, `_core/VERSION`, práva zápisu (bez zápisu souboru), `core_source` (chybí = upozornění, neexistuje nebo není repozitář = chyba, novější značka než `_core/VERSION` = upozornění s `update_core --latest`) a na Linuxu připojené složky podle `/proc/mounts` (`fuse*`, `9p`, `virtiofs`, `cifs`, `smb*`, `nfs*`, `vboxsf`, `drvfs` …; upozornění s `update_core --work-copy`); kód 1 při chybě. Běží i bez PyYAML (`config.yaml` pak čte záložně po řádcích). `hestia/README.md` oddíl *Prostředí* (Windows, Linux, VM desktopové aplikace, `doctor`); modul `start`: v novém prostředí `doctor` před prvním skriptem.
- **`feedback_log`** (13 kap. 3, 10.14; 12 kap. 4.5; CR-031, položka 38; modul `feedback.py`): otevřené podněty `queue.md` (`kind: proposal`, `code: hestia` nebo `hestia:<kategorie>`, `state` mimo `done`, `rejected`; `--id` omezí výběr). Formální kontrola: doklad (závorka „doklad: …“, jinak wikilink nebo cesta v textu) dohledatelný jako wikilink na poznámku, cesta v projektu, ve vaultu, v `Maintenance/` nebo `_core/`, nebo jméno poznámky v backtickách; duplicita podle ID položky v popisu řádku logu nebo shodného textu navrhované změny (i mezi podněty téhož běhu). Kategorie z `code`, `--category P-0001=<kategorie>` má přednost; platné podle výčtu `structure_log_category`. `--apply`: řádek `| dnes | kategorie | <role>: <co se stalo> (<ID>) | doklad: <doklad> | <změna> |  |` na konec logu a položka `done` s `closed`; duplicita se jen uzavře (odkaz na existující řádek ve výpisu); bez kategorie, s neplatnou kategorií nebo nedohledaným dokladem jen výpis. Opakovaný běh nic nezdvojí. `agenda --role Curator` počítá i `hestia:<kategorie>`. `Curator.md` a modul `hestia_feedback`: tvar `code: hestia:<kategorie>`, převod příkazem, ručně jen při chybě.
- **`placeholder_ignore`** (13 kap. 10.11, 12 kap. 3b.8; CR-024, položka 35): klíč v `ue_map.yaml` na nejvyšší úrovni (všechny entity) i v položce `items` (jen její entita; položka jen s `placeholder_ignore` nepřebíjí pravidlo z `defaults`). `ue_query --emit` ho předá v požadavku (`placeholder_ignore`, `placeholder_ignore_items`); `hestia_ue.py` takové meshe (shoda cesty, i bez přípony objektu) do zástupných nepočítá a actor, který by jinak zástupný byl, započte do `placeholder_ignored`; blok `## Stav v UE` ho uvede, je-li nenulový. `lint`: tvar (seznam textů) jako G7, neexistující entita položky jako G6. Modul `ue_lookup`: vodítko k zástupným meshům, `placeholder_ignore` a `ism`.
- **Druh `ism`** (13 kap. 10.11; CR-025 bod 1, položka 36): actor, který by jinak patřil mezi ostatní a má `InstancedStaticMeshComponent` (i hierarchickou), je druh `ism`; actor nese `ism_instances`, souhrn `ism_instances` (součet, i z Blueprintů s ISM) a meshe instancí jdou do signálu zástupných meshů. `by_kind` má klíč `ism` vždy; blok `## Stav v UE` uvede ISM s počtem instancí, je-li nenulový. Rozsah (`bounds`) beze změny (čeká na T-0020). Zástupný modul `unreal` v testech umí ISM a HISM a vrací komponenty včetně podtříd jako UE.
- Testy: 361. Nové: `test_export_cr.py` (stavy buňky `cr`, export jen nevyplněných, nahrazení `–`, dry-run před a po vyplnění, `lint` upozornění, audit bez nálezu `log`); `test_work_copy.py` (stejný výsledek jako bez kopie, žádný soubor se nesmaže, kolize, fáze a pokračování, opakovaný zápis zpět po přerušení, kopie čte projekt originálu, dry-run, chyby použití); `test_doctor.py` (chybějící PyYAML při startu i v `doctor`, starý Python, bez `core_source`, novější značka, `core_source` mimo repozitář, připojená složka, chybějící vault); `test_feedback_log.py` (tvar podnětu, doklad chybí, duplicita podle ID i textu, bez kategorie, kategorie z `code` i z argumentu, neplatná kategorie, opakovaný běh, `lint` nad logem a frontou); `test_ue.py` (druh `ism`, `placeholder_ignore` v `hestia_ue` a celou cestou, `lint` tvaru). Očekávané `by_kind` v `test_ue` vědomě doplněno o `ism`.

## 0.20.1 – 2026-11-22

Doplněk zadání 0.21.1 k oddílu *Změny instrukcí* (13 kap. 10.13; odpověď na otevřenou otázku položky 32 v `predani_vyvoj_core_soubeh`); bez migrace, bez kroků po aktualizaci.

- **Chybí záloha starého core** (`_to_delete/_core_<verze>/`): oddíl *Změny instrukcí* uvede, že změny instrukcí nelze určit, a doporučí každé roli přečíst instrukce celé (kontrakt, profil, moduly, `write_rules.md`).
- **`role_diff`** u přechodu, kde změny určit nejde (oddíl v reportu chybí, protože přechod provedl starší `update_core`, nebo oddíl říká „nelze určit“), nehlásí „beze změny“: vypíše přechod s doporučením číst instrukce celé (v `--json` pole `unknown`).
- Testy: 330. Nový: oddíl bez zálohy; `role_diff` u přechodu s oddílem „nelze určit“, bez oddílu a s oddílem „beze změny instrukcí“.

## 0.20.0 – 2026-11-22

Optimalizace čtení agentů, vlna 1 (zadání 0.21; podklad `zadani_0.21_optimalizace_cteni`; předání `predani_vyvoj_core_soubeh` položky 30, 32, 31, vydané spolu); bez migrace. Verze nese příznak `roles` (mění se moduly, které projektové role používají): po aktualizaci `doc_index`, `compose_role` a ruční úkol `update_core:0.20.0:role_base` (srovnat profily v `Roles/`, pak `role_base: 0.20.0`). Existující dokumenty se neupravují; *Souhrn* a `for_role` doplní role, která dokument nebo předání příště mění (přechod P17).

- **Čtecí nástroje** (13 kap. 3, 10.10, 10.13; položka 30): `doc_index` má u záznamu `chars` (znaky těla) a `sections` (`{heading, level, line, end_line, chars}` pro `##` a `###`, řádky souboru od 1, `end_line` včetně; konec řádku CRLF jako jeden znak); `headings` zůstává. Nový příkaz **`section <dokument> [--list] [<nadpis> …]`** (`<dokument>` = cesta od vaultu nebo projektu, jméno, titul nebo alias; osnova se *Souhrnem*, nebo jen zadané sekce s podsekcemi a čísly řádků; nadpis bez ohledu na velikost písmen přesně, pak podle začátku; víc shod nebo žádná = kandidáti, kód 2). Nový příkaz **`find "<dotaz>" [--type] [--entity] [--for-role] [--text]`**: hledání z `compose_context` vyčleněné do modulu `search.py` (název, `aliases`, nadpisy sekcí s řádky, entita, cesta, glosář; podle začátku slova bez ohledu na diakritiku); když index najde méně než 3 výsledky, doplní je hledání v textu (označené „v textu“, se sekcí a řádkem), `--text` hledá v textu vždy. `compose_context --query` používá totéž hledání (v hlavičce „doplněno“, nebo „záložně“, když index nenajde nic), čímž odpadá chyba P7 (palisáda jen v textu návrhu).
- **Instrukce po aktualizaci, agenda, Claude Project** (13 kap. 10.6, 10.13; 12 kap. 3, 7.1; 07 kap. 15; 01 kap. 9.1; položka 32): report `update_core` má v oddílu přechodu **`### Změny instrukcí`** (modul `instructions.py`; spočte se před výměnou `_core/` ze starého a nového core, kroky po aktualizaci ho obnoví ze starého core v `_to_delete/`): změněné soubory v `agents/` a `templates/tpl_role.md`, změněné sekce (`##`/`###`, vlastní text sekce; nová, odebraná, změněná; frontmatter bez `updated`), nové znění jako citace, nad 3 000 znaků na soubor jen seznam sekcí; pak *Role a soubory* (kontrakt a `write_rules.md` všechny, profil core, `review_plan.md` Curator a Auditor, moduly `compile: all`, moduly z profilů s `combines` a `requires`, `tpl_role.md` projektové role). Nový příkaz **`role_diff <Role> [--since <verze>]`** (výchozí verze před poslední aktualizací ze `structure_version.md`): bloky *Změn instrukcí* souborů, které role používá, a řádky `changes.md` k profilu a lokálním modulům role od data přechodu; jinak „beze změny od …“ s verzí. Pole **`for_role`** (`fields.yaml`, typ `handover`, `tpl_handover`) a příkaz **`agenda --role <Role>`** (předání pro roli a bez `for_role` s entitou, `updated` a počtem otevřených otázek; Librarian Inbox `intake: raw`, Curator otevřené podněty `code: hestia` a návrhy, Steward úkoly `update_core:*`). **`compose_role`** vypisuje `changed` (nový obsah) a `unchanged` v textu i `--json`.
- **Dlouhé dokumenty a předání** (04 G14, 07 kap. 2, 3; 13 kap. 4; 12 kap. 1, 5; 01 kap. 9.2; položka 31): klíče `doc_summary_chars` 6000, `doc_split_chars` 20000, `handover_max_chars` 4000 (`defaults.yaml`, zakomentované v šabloně `config.yaml`). `tpl_design` a `tpl_state` mají `## Souhrn` za titulem. **G14** (informace, jen report): (a) dokument v `Docs/` nad `doc_summary_chars` bez `## Souhrn` jako první sekce, (b) poznámka nad `doc_split_chars` → rozdělit tematicky, (c) aktivní předání nad `handover_max_chars`; znaky těla bez frontmatteru a generovaných bloků, `Maintenance/` a `Dashboard/` se nepočítají.
- **Moduly:** `start` (*Čtení*: dlouhý dokument po sekcích, `find`, logy výběrem; bez zadání `agenda`; po aktualizaci `role_diff`), `lookup` (`find` a `section`), `handover_out` (předání = jeden task pro jednu roli, `for_role`, G14c), `task_close` krok 1 (*Souhrn*, tematické rozdělení) a krok 2 (do Claude Projectu jen `changed`, ověření podle hlavičky), `file_info` (jeden dokument, jedno téma).
- Fixture `mini_lapikus`: `role_base: 0.20.0`; očekávané kompiláty `Architect`, `Builder` vědomě srovnány (moduly `start`, `handover_out`, `task_close`). Testy šablon a parity bez čekajících položek; katalog nálezů G1–G14.
- Testy: 329. Nové (`test_reading.py`): `doc_index` s `chars` a `sections`; `section --list`, sekce s podsekcemi, nejednoznačný nadpis, alias, *Souhrn*, předání a `Maintenance/`; `find` se shodou v aliasu, nadpisu a jen v textu (palisáda), doplnění pod 3 výsledky, filtry `--type`, `--for-role`, `--text`; `compose_context --query` stejným hledáním; `agenda` s `for_role` a bez něj, části rolí Librarian, Curator, Steward; `compose_role` podruhé vše `unchanged`, po změně profilu `changed` jen ta role; `update_core` se změnou modulu a `tpl_role` → *Změny instrukcí*; `role_diff` u role, která modul používá, a u role, která ho nepoužívá, `--since`, řádek `changes.md` k profilu; dělení na sekce a limit 3 000 znaků; G14 a, b, c a bez nálezu se souhrnem a s prahy z `config.yaml`.

## 0.19.0 – 2026-11-22

Rozdělení kontraktu L0 (zadání 0.20; CR_2026-11-21_kontrakt_rozdeleni, podnět vývojáře k limitu L0; předání `predani_vyvoj_core_soubeh` položka 29); bez migrace. Verze nese příznak `roles` (mění se kontrakt a moduly, které projektové role používají): po aktualizaci `compose_role` a ruční úkol `update_core:0.19.0:role_base` (srovnat profily v `Roles/`, pak `role_base: 0.19.0`; profil, který odkazuje na oddíl kontraktu *Kam smíš psát*, odkáže na `write_rules.md`, *Zásady zápisu*).

- **`CONTRACT.md` jen to, co agent potřebuje v každém tasku** (12 kap. 2): oddíly *Co je Hestia*, *Režim a start*, *Povinnosti, které profil nezruší* (výsledek práce do vaultu podle `write_rules.md`, profil kontrakt zpřísňuje a neruší, `_core/` neměnit, nemazat, necommitovat, jazyk), *Spouštěče* (každý modul katalogu má řádek; `file_safety` a `metadata` v jednom řádku), *Uzavření tasku je povinné*. 2543 znaků a 42 řádků (dřív 3991 znaků).
- **`write_rules.md`, oddíl *Zásady zápisu*** před maticí (12 kap. 8): přepis platného textu jen po rozhodnutí nebo výsledku tasku, profil zpřísňuje a neruší, `Docs/` jako dokumentace domény (existující dokument doplnit, předání z role), přesun a mazání, problém s Hestií → `hestia_feedback`.
- **Nový modul `hestia_feedback`** (12 kap. 3, 4.5; oba režimy, `compile: all`): podnět ke změně Hestie na konec `queue.md` (vault) nebo do zápisu Hestia (chat), ne CR ani `structure_log.md`; uvést v hlášení `task_close` (krok 11).
- **Modul `start`:** výjimka `compile: listed` (kdo modul nemá, předá věc roli, která ho má, nebo se zeptá). **`chat_entry`:** položky *Finální dokumentace* jsou dokumentace domény, cílem je existující dokument; *Podněty pro Hestii* odkazují na `hestia_feedback`. **`task_close`** krok 11 odkazuje na `hestia_feedback` místo oddílu kontraktu *Kam smíš psát*.
- Fixture `mini_lapikus`: `role_base: 0.19.0`; očekávané kompiláty `Architect`, `Builder` vědomě srovnány (nový text L0, modul `hestia_feedback`, výjimka v `start`).
- Testy: 316. Nové: každý modul katalogu má řádek v tabulce spouštěčů L0; `write_rules.md` má *Zásady zápisu* před maticí; výjimka `compile: listed` je v modulu `start`; katalog 20 modulů. Zadání 0.21 (položky 30–32) je napřed: `PENDING_SPEC` v testu šablon (`design`, `state`, `handover`) a `PENDING_FIELDS` v testu parity (`for_role`) hlídají, že rozdíl trvá.

## 0.18.0 – 2026-11-21

Čtení Unrealu proti `state` podle CR z pilotu (zadání 0.19; CR_2026-11-21_ue_cteni_vs_state, podnět Architekta; předání `predani_vyvoj_core_soubeh` položka 28); bez migrace a bez ručního úkolu. Po aktualizaci `hubs` (poznámka v bloku `## Stav v UE`) a `compose_role` (modul `ue_lookup`). Existující `state` se neupravují; § *V levelu* a *Vizuálně ověřeno* doplní role, která `state` příště mění.

- **G10 `state` za reportem** (13 kap. 10.11, 04 kap. 4): entita s aspoň jedním actorem v posledním reportu z UE, jejíž nejnovější platný `state` má `updated` starší než `generated` reportu (po dnech) → informace u souboru `state`: „`state` … je starší než čtení z UE …; ověř § *V levelu*“ s oběma daty. Porovnávají se jen data, text `state` se nečte; jen v reportu auditu, ne ve frontě; entita bez platného `state` se nehlásí (G4). Společná funkce `ue.state_behind`.
- **Blok `## Stav v UE`** (`hubs`): tatáž věc jako řádek „Pozor: …; report potvrzuje jen „v levelu je“, vzhled a funkci § *Vizuálně ověřeno*“.
- **`tpl_state`** (07 kap. 3): § *Ověřeno v UE* s podsekcemi *V levelu (report z UE)* a *Vizuálně ověřeno (kdo, kdy)*; test šablon bez čekajících položek (`PENDING_SPEC` prázdný).
- **Modul `ue_lookup`** (12 kap. 3b.8): krok *Report a `state`* (novější report, který stavbu ukazuje → „v levelu je“ s datem, rozpor říct, starší text nepřebírat; vzhled a funkci jen z § *Vizuálně ověřeno*; kdo `state` mění, doplní § *V levelu*) a past.
- Očekávané kompiláty `Architect`, `Builder` vědomě srovnány (modul `ue_lookup`).
- Testy: 314. Nový: G10 `state` za reportem (report novější → nález informace u souboru `state`, ne ve frontě, poznámka v hubu; entita bez `state` → nic; `state` aktualizovaný po reportu → bez nálezu i poznámky).

## 0.17.0 – 2026-11-21

Věrný převod Notion, podněty rolí přes frontu a uzavření zápisu Knihovníka (zadání 0.17.2, 0.18, 0.18.1 a 0.19.1; CR_2026-11-21_inbox_import_seznamy_v_li, CR_2026-11-21_podnety_roli_pres_frontu; předání `predani_vyvoj_core_soubeh` položky 25–27); bez migrace. Verze nese příznak `roles` (mění se kontrakt a moduly, které projektové role používají): po aktualizaci `doc_index`, `compose_role` a ruční úkol `update_core:0.17.0:role_base` (srovnat profily v `Roles/`, pak `role_base: 0.17.0`).

- **Převod `notion-md` → Markdown** (13 kap. 10.12, zadání 0.17.2): nový modul `notion_md.py` místo převodníku z 0.15.0. Bloková značka se převede na svém odsazení, i pod markdownovou odrážkou (odrážka s odsazeným `<ul>` je rodič). **Kontejner** (`<li>`, `<todo>`, `<quote>`, `<callout>`, `<toggle>`, `<column>`, `<p>`, `<h1>`–`<h4>`): titulek za značkou, potomci po prázdném řádku, blokové značce nebo odrážce rekurzivně o úroveň hlouběji, relativní odsazení markdownových odrážek zůstane; další odstavec položky je odsazené pokračování. Prázdný odstavec je prázdný řádek. Tabulka převodů celá: zvýraznění (`**`, `*`, `~~`, mezery vně značek), `<u>` beze změny, barva textu a bloku jako `<span style>`, prázdný odstavec, nadpisy, seznamy (potomci odrážky `- ` o dvě mezery, číslované položky o šířku značky včetně mezery, `1. ` → 3, `10. ` → 4; číslování od `start`; `type="a"`/`"i"` → `1.` a ruční kontrola `ol_type`), úkoly, citace, callout (`> [!druh] ikona titulek`; druh podle rodiny barvy, přípona `_bg` se odřízne: red → danger, orange/yellow → warning, green → success, blue → info, purple → example, pink → tip, jinak note), toggle (`> [!note]-`), tabulka bez sloučených buněk jako pipe tabulka (barva buňky, řádku i sloupce jako `<span>`, `|` escapované; bez `header-row="true"` prázdný řádek záhlaví a všechny řádky v těle), zmínky a data, citace `[^URL]`, stránky a databáze (`page`), přílohy (`attachment`), sloupce za sebou (`columns`); ostatní značky doslovně v ohrazení `notion-md` (`unsupported:<značka>`). Obsah kódu, inline kódu a `\<tag>` se nepřevádí. **Kontrola věrnosti:** text bez značek a strom seznamů a kontejnerů zdroje a výstupu; neshoda = druh `struktura` (soubor se zapíše). Na datech pilotu (Palisáda nad bránou, Guest on hunt) shoda s ručním převodem P10, bez ruční kontroly.
- **Podněty rolí ke změně Hestie** (12 kap. 4.5, 5, 6, 8; 05 kap. 3.1, 3.2a, 4, 7.2; zadání 0.18): `CONTRACT.md` pravidlo v *Kam smíš psát* (CR ani `structure_log.md`, podnět s dokladem na konec `queue.md`, `proposal`, `code: hestia`) a spouštěč; kvůli limitu jedné stránky zkrácen popis režimů, řádek `chat_entry` a zrušena opakovaná věta o commitech. Modul `task_close` krok 11 (podněty v hlášení); `chat_entry` sekce *Podněty pro Hestii* v zápisu Hestia. `Curator.md`: převod podnětů do `structure_log.md` (formálně: doklad, duplicita; ID položky v popisu; `state: done`). `Librarian.md`: kolize pojmů a chybějící náležitosti jako podnět do `queue.md`, `structure_log.md` a `outbox/` ne. `write_rules.md`: matice (projektové role jen podnět do `queue.md`, `structure_log.md` a `outbox/` ✘), oddíl Knihovník.
- **Knihovník uzavírá vlastní zápis** (12 kap. 3b.1, 5; 13 kap. 10.5; zadání 0.18.1): `task_close` po `--apply` obnoví `doc_index` (zapíše jen při novém, změněném nebo přejmenovaném dokumentu; dry-run hlásí, zda se obnoví) a nepřidá řádek `changes.md`, který už v souboru je (datum, role bez ohledu na velikost písmen, entita, text; jiný zdroj nevadí), výpis a JSON `changes_present`. `Librarian.md`: po vlastním zápisu `task_close --role Librarian`, když nejde spustit, v hlášení co neběželo, co z toho plyne a kdo ho spustí; modul `task_close` krok 10 (`doc_index`, nezdvojení).
- **Role v řádku `changes.md` = jméno profilu** (05 kap. 7.1, zadání 0.19.1): formát řádku v `Librarian.md`, `Curator.md` a modulu `canon_check` s `Librarian`, `Curator` (dřív malými).
- Šablona `tpl_state` ze zadání 0.19 čeká na core 0.18.0 (`PENDING_SPEC` v testu šablon).
- Fixture `mini_lapikus`: `role_base: 0.17.0`; očekávané kompiláty `Architect`, `Builder` a golden dry-runu `task_close` (řádek `doc_index`) vědomě srovnány. Testy `role_base` v auditu a `update_core` berou verzi z manifestu a fixture.
- Testy: 313. Nové: fixture `notion_sample.json` o dva případy z pilotu a jednu položku na řádek tabulky převodů s očekávaným výstupem `fixtures/import/expected/<ref>.md` (přesná shoda, druhy ruční kontroly); kontejnery z pilotu; kód se nepřevádí; kontrola věrnosti (poškozený výstup → `struktura`, i při převodu); `task_close` po založení entity Knihovníkem (entita v `doc_index.json`, hub s generovanými bloky, druhé uzavření s jiným zdrojem bez nových řádků a bez zápisu).

## 0.16.0 – 2026-11-21

Základ projektových rolí podle CR z pilotu (zadání 0.17 a 0.17.1; CR_2026-11-21_zaklad_roli_v_instanci; předání `predani_vyvoj_core_soubeh` položka 24); bez migrace. Verze sama nese příznak `roles`: po aktualizaci `compose_role` a ruční úkol `update_core:0.16.0:role_base` (srovnat profily v `Roles/` se základem, pak `role_base: 0.16.0`). Do té doby `lint` hlásí u profilů chybějící `role_base` a audit G5.

- **Profil kontrakt zpřísňuje, neruší** (12 kap. 2.1, 8): `CONTRACT.md` v *Kam smíš psát*: výsledek své práce role zapíše do vaultu vždy, zákazy zápisu v profilu platí pro kód, data a assety, rozpor = otázka; zápis do `Docs/` je dokumentace domény podle šablony (sekce, `depth`), ne výstup role; existující dokumentace entity se doplňuje, nový dokument jen když žádný není; předání se píše z role.
- **`tpl_role`** (07 kap. 12, zadání 0.17.1): `role_base: ""` s komentářem (verzi z `_core/VERSION` doplní, kdo profil zakládá; `init` ani `update_core` šablonu nevyplňují) a komentář s pravidly výše.
- **Pole `role_base`** (01 kap. 9.1): `fields.yaml` s novou podmínkou `required: project_role` (13 kap. 5: povinné u profilu projektové role `Roles/<Role>.md`, vyhodnotí `lint` podle cesty; role core v `_core/agents/` ho nemají), `types.yaml` (volitelné pole typu `role`). Chybějící i prázdná hodnota = G7 chyba s nápovědou „doplň verzi core z _core/VERSION“; stejnou nápovědu dostane neplatný YAML s nevyplněným `{{core_version}}` (návrh šablony ze zadání 0.17).
- **Manifest, záznam 0.14.3:** do `crs` doplněn `CR_2026-11-21_claude_project_druh_a_pristup` (text `task_close`, vydaný v 0.14.3; nález pilotu P11).
- **Příznak `roles` v manifestu** (13 kap. 10.6a): krátký text u verze, která mění základ rolí; `load_manifest` ho ověří (neprázdný text). `update_core` u verze s příznakem: ruční úkol `update_core:<verze>:role_base` do `queue.md`, v dry-run řádek „Změna základu projektových rolí“, v reportu oddíl *Základ projektových rolí* (text příznaku, rozdíl `tpl_role` mezi starým core v `_to_delete/_core_<stará>/` a novým, profily s `role_base` starším nebo chybějícím), totéž krátce ve výpisu a v JSON (`after.roles`).
- **Audit G5** (04 kap. 4): profil `Roles/<Role>.md` bez `role_base`, s neplatnou hodnotou nebo starší než poslední verze s příznakem `roles` v manifestu běžícího core; zpráva odkazuje na ruční úkol.
- Fixture `mini_lapikus`: `role_base: 0.16.0` u `Architect` a `Builder`, `Architect` „neměníš kód ani data projektu…; návrh zapisuješ do `Docs/`“. Očekávané kompiláty `Architect`, `Builder` vědomě srovnány (kontrakt, profil).
- Testy: 308. Nové: formát příznaku a první verze s ním; změna `tpl_role` mezi vydanými verzemi (značky a pracovní strom) bez příznaku `roles` = chyba; `update_core` s příznakem (dry-run, úkol jednou, report s rozdílem `tpl_role` a profily, po srovnání profilů prázdný seznam) a bez něj; audit G5 (aktuální, starší, chybějící `role_base`; jen profily v `Roles/`); `lint` (chybějící a prázdný `role_base` s nápovědou, nápověda u `{{core_version}}`).

## 0.15.0 – 2026-11-21

Import do inboxu podle CR z pilotu (zadání 0.16; CR_2026-11-21_inbox_import_notion; předání `predani_vyvoj_core_soubeh` položka 23); bez migrace. Po aktualizaci `doc_index` a `compose_role` (manifest) a ruční úkol `scratch_source_ref`: doplnit `source_ref` u scratch z ručního importu (v pilotu čtyři poznámky z P10, z řádku `Zdroj:`).

- **Příkaz `inbox_import --from <soubor> [--apply] [--json]`** (13 kap. 3, 10.12): ze souboru výměny `Maintenance/import/<zdroj>_RRRR-MM-DD.json` (`source`, `source_query`, `exported`, `items` s `ref`, `title`, `created`, `type`, `tags`, `content`, `content_format`) zapíše scratch do `Inbox/` podle `tpl_scratch`: `intake: raw`, `source`, `source_ref` = `ref`, `category` z `type` i `tags` přes `tag_map` (sjednocení bez duplicit; nenamapovaná hodnota = upozornění `unmapped`, kategorie se nevymýšlí), `entity: ""`; tělo `# <title>`, řádek `Zdroj: [<source>](<ref>), vytvořeno <datum>`, obsah, prázdné *Předzpracování*. Jméno souboru z titulu bez diakritiky (`[A-Za-z0-9_]`); kolize s existující poznámkou → `_<source>`, kolize v dávce → `_2`, `_3`; prázdný titul → `<source>_<datum vytvoření>`. Cesta `--from` absolutní, nebo relativně k pracovní složce či k vaultu.
- **Převodník `notion-md`**: odstavce a nadpisy beze změny, `<b>`/`<strong>` → `**`, `<i>`/`<em>` → `*`, `<a href>` → `[text](url)`, `<ul>`/`<ol>`/`<li>` (i vnořené) na odrážky s odsazením dvou mezer, prázdná položka zůstane (`-`), `<empty-block/>` = prázdný odstavec; text bez značek zůstane znak po znaku stejný. Úsek s jiným blokem (obrázek i `![…](…)`, soubor, tabulka, toggle, callout, zmínka, databáze, neznámý tag) se zapíše v původní podobě v ohrazení ```` ```notion-md ```` a položka je ve výstupu `needs_review` s druhy bloků. `content_format: markdown` se zapíše beze změny; jiný = chyba položky.
- **Duplicity**: položka, jejíž `ref` už nese `source_ref` některé poznámky, nebo se v souboru opakuje, se přeskočí a vypíše (`skipped` s důvodem); opakovaný běh nic nezdvojí.
- **Po `--apply`**: řádek `changes.md` na každý soubor (role `Curator`, zdroj `import <source>`), `lint` zapsaných souborů (chyba = kód 1, soubory zůstanou), `doc_index`. Výstup (text i `--json`): `written`, `skipped`, `unmapped`, `needs_review`, `errors`, `lint`; podle `written` agent mění stav ve zdroji. Kódy: 0 (i s upozorněními), 1 chyba položky nebo `lint` (platné položky se zapíšou), 2 chybí soubor, neplatný JSON, neznámý `source` (mimo výčet `source`).
- **Pole `source_ref`** (01 kap. 9.1): `fields.yaml` (scratch, nepovinné), `types.yaml`, `tpl_scratch`.
- **Modul `inbox_import`** (12 kap. 3; `modes: [vault]`, `compile: listed`) v profilu Curatora; spouštěč v `CONTRACT.md`, výjimka pro `compile: listed` obecně (moduly Knihovníka a `inbox_import`); Curator v textu profilu podle 05. `write_rules.md`: řádek `Maintenance/import/` (05 kap. 4). `lint` a `audit` složku `Maintenance/import/` nečtou.
- **`compose_role`**: modul `compile: listed` jen pro režim `vault`, který role nemá v profilu, se v úvodu kompilátu neuvádí mezi vynechanými moduly s pokynem „předej věc Knihovníkovi“ (dřív by ho tak kompilát `Librarian` uvedl); role, která ho má (Curator), ho má mezi vynechanými moduly jen pro `vault`. Očekávané kompiláty `Architect`, `Builder` vědomě srovnány (spouštěč a výjimka v kontraktu).
- Testy: 299; sedm testů ze zadání 0.16 (katalog modulů, `fields.yaml`, `tpl_scratch`, matice zápisu) prochází; testy katalogu a `compile: listed` srovnány se zadáním 0.16 (19 modulů, `inbox_import` listed u Curatora). Nové: převodník (text beze změny, vnořené seznamy s prázdnou odrážkou, tučné, kurzíva, odkazy, nepodporované bloky doslovně v ohrazení, prázdný odstavec), `slug`; příkaz nad fixture `fixtures/import/notion_sample.json` (dry-run nic nezmění, `--apply` scratch podle šablony, kolize s hubem → `_notion`, nenamapovaný `type`, `changes.md`, `doc_index`, `lint` bez `Maintenance/import/`, druhý běh bez duplicit, kolize v dávce a opakovaný `ref`, chyba položky = kód 1, chyby použití = kód 2, výstup `--json`); modul listed jen pro vault v kompilátu.

## 0.14.4 – 2026-11-21

Režim agenta podle přístupu k vaultu a přenosný čtecí skript Unrealu podle CR z pilotu (zadání 0.15.4; CR_2026-11-21_knihovnik_pripojena_slozka, CR_2026-11-21_ue_query_cesty_ve_skriptu; předání `predani_vyvoj_core_soubeh` položka 22); bez migrace. Po aktualizaci `compose_role` (změněný kontrakt a moduly; proběhne sám) a ruční úkol `entrypoint_core_roles` (srovnat `CLAUDE.md` podle šablony). Nové kompiláty patří do dokumentů Claude Projectu.

- **Režim podle přístupu, ne podle prostředí** (12 kap. 1.1): `CONTRACT.md` má sekci *Režim práce* (`vault` = relace vidí soubory projektu, i chat nebo Cowork s připojenou složkou, i když začala s kompilátem; `chat` = relace bez přístupu; commituje vždy člověk), v *Startu* profily projektových rolí v `Roles/` a rolí core v `_core/agents/`; spouštěč `chat_entry` jen bez přístupu k vaultu. Modul `start`, krok 0: ověř, zda vidíš `Hestia/_core/agents/CONTRACT.md` v pracovní nebo připojené složce; když ano, režim `vault` a kompilát dál není zdroj.
- **Úvod kompilátu** (`compose_role`, 12 kap. 2): místo „Soubory vaultu odsud neotevřeš“ podmínka: vidíš-li vault, přepni do režimu `vault` podle modulu `start`; kompilát je pro relaci bez přístupu.
- **Knihovník bez balíčku a bez skriptů** (12 kap. 3b.5): `lookup`, `inbox_triage`, `ue_lookup` v chatu bez vaultu a bez balíčku neodpovídají a řeknou přesně, který balíček a jakým příkazem vznikne (`compose_context --entity <Entita>` / `--topic inbox` / `--query "<…>"`), nebo požádají o přístup k vaultu; ve vaultu bez možnosti spustit skript core čtou `doc_index.json`, glosář, dokumenty a reporty přímo a výslovně uvedou, že skript neběžel. `chat_entry`: chat s připojenou složkou je režim `vault`.
- **Vstupní soubor** (12 kap. 7, 07): `tpl_entrypoint.md` a `vault_template/entrypoint.md.tpl` odkazují i na role core v `Hestia/_core/agents/` (Curator, Auditor, Librarian). Existující `CLAUDE.md` instance se nepřepisuje: ruční úkol v manifestu.
- **`ue_query --emit` přenosný** (13 kap. 10.11): vygenerovaný skript neobsahuje absolutní cestu stroje, kde běží core; `_core/scripts` i výsledek odvozuje z `__file__` (`<Hestia>/Maintenance/ue/`), bez `__file__` skončí srozumitelnou chybou. Pokyn pro editor uvádí cestu relativně ke kořeni projektu (v JSON `editor_path`); chybí-li ve vaultu `_core/scripts/hestia_ue.py`, upozornění (`warnings`). Skripty vygenerované starším core (s absolutní cestou) nahradí příští `--emit`.
- Očekávané kompiláty `Architect`, `Builder` vědomě srovnány (úvod, kontrakt, `start`, `chat_entry`, `ue_lookup`).
- Testy: 288 (úvod kompilátu s přepnutím; vstupní soubor s rolemi core; skript bez absolutních cest, výpis relativně ke kořeni, spuštění ze zkopírovaného projektu najde `hestia_ue` a zapíše výsledek vedle sebe a import z kopie projde; upozornění bez `_core/scripts` ve vaultu). Sedm testů, které zavádí zadání 0.16 (katalog modulů, `fields.yaml`, `tpl_scratch`, matice zápisu), dál selhává; opraví je položka 23 (0.15.0).

## 0.14.3 – 2026-11-21

Report `update_core` a přerušený běh, společné argumenty CLI, text `task_close` podle CR z pilotu (zadání 0.15.3; CR_2026-11-21_update_core_report_zmena_prirazeni, CR_2026-11-21_update_core_report_a_preruseni, CR_2026-11-21_claude_project_druh_a_pristup; předání `predani_vyvoj_core_soubeh` položka 21); bez migrace. **Přechod na 0.14.3 řídí ještě skript 0.14.2**: `--apply` patří **za** příkaz (`update_core --latest --apply`), oddíl reportu založí až kroky po aktualizaci (běží kódem 0.14.3) a průběh se vypíše až na konci; od dalšího přechodu platí vše níže. Po aktualizaci `compose_role` (změněný modul `task_close`; proběhne sám).

- **Report `update_core`** (13 kap. 10.6): v `Maintenance/reports/update_core_RRRR-MM-DD.md` jeden oddíl na přechod `## Přechod <stará> → <nová>` s řádkem `- Stav:` (`kroky po aktualizaci neproběhly` / `kroky probíhají` / `krok X selhal; zbývá …` / `dokončeno`), výměnou `_core/` (kam šel starý core), záznamy manifestu, výsledky kroků, kontrolami, ručními úkoly a CR k ověření. Další přechod téhož dne se **připíše**, opakovaný běh téhož přechodu oddíl přepíše; jméno souboru beze změny. Starší report dne (formát do 0.14.2) zůstává nad novými oddíly.
- **Podstatný výstup kroků**: u `asset_index` řádky `Změna přiřazení: <cesta>: <stará> → <nová entita> (<pravidlo>)`, bez změn „bez změn přiřazení“; `hubs` počet změněných souborů, `doc_index` změněn / beze změny, `compose_role` počet změněných kompilátů. Totéž v textovém výstupu a v JSON (`after.steps[].details`).
- **Přerušený běh**: řídicí skript založí oddíl hned po výměně `_core/` (stav „kroky po aktualizaci neproběhly“), kroky ho přepisují po každém kroku; průběh kroků jde hned na stderr (flush; řídicí skript ho z podprocesu předává řádek po řádku, JSON jde dál na stdout). `--after-only` bez `--since` doplní oddíl **posledního přechodu** podle `structure_version.md` (v reportu dne toho přechodu); chybí-li oddíl (výměnu řídil starší core, report smazán), založí ho s údajem o přechodu. `--no-after` nechá oddíl ve stavu „neproběhly“.
- **Dry-run pozná nedokončený přechod**: poslední přechod na nainstalovanou verzi ze `structure_version.md`, jehož oddíl není `dokončeno` (nebo report chybí; reporty do 0.14.2 se uznávají podle „Verze: X → Y“ / „rozsah od X“; verze před 0.14.0 se nekontrolují), ohlásí jako upozornění s doporučením `update_core --after-only --apply`; v JSON `unfinished`.
- **CLI** (13 kap. 3): společné argumenty (`--vault`, `--apply`, `--force`, `--json`, `--quiet`) před příkazem i za ním se sčítají (přepínače OR; `--vault` na obou místech jen se shodnou cestou, různé cesty = chyba použití, kód 2, zpráva uvede obě; odpověď Master architekta 2026-11-21, zadání 0.15.4); dřív hodnota podpříkazu přepsala hlavní a `hestia.py --apply update_core …` proběhlo jen jako dry-run.
- **Modul `task_close`**, krok 2 (12 kap. 7.1): předání odstraní z Claude Projectu jen relace připojená k tomuto projektu, jinak seznam souborů k odebrání pro GameDesignera. Očekávané kompiláty `Architect`, `Builder` vědomě srovnány.
- Docstring `default_roles` (`compose.py`) upravený Master architektem podle zadání 0.15.2 vychází s touto verzí.
- Testy: 285 (dva přechody v jeden den = dva oddíly; přerušení po výměně, dry-run s doporučením a dokončení `--after-only` do téhož oddílu; `--after-only` založí chybějící oddíl; změna přiřazení z `asset_index` v reportu, v JSON a v průběžném výpisu; `--apply` a `--json` před příkazem; `--vault` před i za příkazem: shodná cesta projde, různé kód 2 bez zápisu).

## 0.14.2 – 2026-11-21

`compose_role` po každé změně verze podle CR z pilotu (zadání 0.15.1, CR_2026-11-21_compose_role_po_kazde_aktualizaci, předání `predani_vyvoj_core_soubeh` položka 20); bez migrace, bez kroků v manifestu. Účinné od přechodu z 0.14.2 dál (kroky po aktualizaci spouští nový core); při přechodu na 0.14.2 se `compose_role` spustí také, protože kroky už běží kódem 0.14.2.

- **`update_core --apply`** (13 kap. 10.6, 10.6a): když se mění verze core a ve vaultu jsou kompiláty (`Roles/_compiled/*_compiled.md`), přidá `compose_role` na konec automatických kroků i bez záznamu v `upgrade.yaml` (hlavička kompilátu nese verzi core; dřív audit po verzi bez `compose_role` hlásil všechny kompiláty jako G5). Dry-run i `--after-only` ho vypíšou v plánu; bez kompilátů se nespouští. V manifestu se `compose_role` dál smí uvádět, jen pro čitelnost.
- **`compose_role` bez výčtu rolí** skládá kromě profilů v `Roles/` i role core (`_core/agents/`: Curator, Auditor, Librarian), jejichž kompilát už ve vaultu je; dřív by kompilát role core po aktualizaci zůstal starý (G5), i když `compose_role` proběhl. Provizorně, otázka v předání.
- Upozornění na zastaralé kompiláty po `--apply` už nevzniká (kompiláty se obnoví); zůstává u `--no-after`.
- Testy: 279 (přechod přes verze s prázdným záznamem: `compose_role` proběhne, hlavičky kompilátů nesou novou verzi, audit nainstalovaným core bez G5 u kompilátů; vault bez kompilátů ho nespouští; kompilát role core se obnoví; `--no-after` dál upozorní).

## 0.14.1 – 2026-11-20

Oprava z prvního přechodu pilotu na 0.14.0 (pokyn GameDesignera 2026-11-20); bez migrace, bez kroků po aktualizaci.

- **`update_core`: čerstvé kompiláty rolí se hlásily jako starší než core.** Test stáří hledal v hlavičce `core X`, `compose_role` ale od 0.2.0 píše `| core: X |`; upozornění „kompiláty rolí jsou starší…“ se proto objevilo vždy (v pilotu u `--latest` hned po přechodu). Hlavička se teď čte s dvojtečkou i bez ní.
- Testy: 276 (test se skutečnou hlavičkou z `compose_role`: čerstvý kompilát se nehlásí, starší než nový core ano).

## 0.14.0 – 2026-11-20

Snadná aktualizace core (zadání 0.15; předání `predani_vyvoj_core_soubeh` položka 19); bez migrace. **Přechod na tuto verzi jde jednou postaru**: skriptem nové verze z pracovní kopie značky (`git worktree add --detach ../hestia-v0.14.0 v0.14.0`, pak `python -I ../hestia-v0.14.0/hestia/scripts/hestia.py update_core --vault <Hestia> --from ../hestia-v0.14.0/hestia`); kroky po aktualizaci proběhnou už při něm. Pak do `config.yaml` `core_source` a další aktualizace `update_core --latest`.

- **`update_core --tag vX.Y.Z` / `--latest`** (13 kap. 10.6): `hestia/` vydané značky z repozitáře `core_source` přes `git archive` do dočasné složky mimo vault, dál jako s `--from`. Jen značky `vMAJOR.MINOR.PATCH` (`--latest` = nejvyšší; značky zadání, větve ani pracovní strom ne); git jen čte. Bez `core_source` a bez zdroje chyba použití (kód 2) se zprávou, co doplnit; `--from` zůstává jako záloha.
- **Klíč `core_source`** (13 kap. 4): `defaults.yaml` (`null`), v šabloně `config.yaml` zakomentovaný vzor.
- **Manifest `hestia/upgrade.yaml`** (13 kap. 10.6a, 11 kap. 5): u každé verze `after` (`asset_index`, `hubs`, `doc_index`, `compose_role`), `manual` (`id`, `text`), `crs`, u MAJOR `migration`. Záznamy zpětně od 0.10.2 (verze pilotu) podle tohoto changelogu; test hlídá, že každá verze od 0.10.2 má záznam, kroky jsou z povolené sady a CR existují.
- **Kroky po aktualizaci**: dry-run vypíše sečtené záznamy verzí (stará, nová]. Po `--apply` je řídicí skript spustí **novým** core jako podproces `update_core --after-only --since <stará>`, i když výměnu řídí starší skript: automatické kroky s `--apply` v pevném pořadí (každý jednou), pak `lint --all` a `audit` v dry-run se souhrnem nálezů; ruční úkoly do `queue.md` jako `T-…` s klíčem `update_core:<verze>:<id>` ve sloupci `code` (opakovaný běh je nezakládá znovu); CR k ověření v řádku `structure_version.md` (sloupec CR) a v reportu; report `Maintenance/reports/update_core_RRRR-MM-DD.md`.
- **Selhání kroku**: další kroky se nespustí, `_core/` zůstává nový, návratový kód 1 a výpis zbývajících kroků. `--after-only` (bez výměny core) je spustí znovu; rozsah verzí vezme z posledního řádku `structure_version.md` („core <aktuální> | aktualizace z <stará>“), bez něj všechny automatické kroky bez ručních úkolů. Automatické kroky jsou generované výstupy, opakování je bezpečné. `--no-after` kroky přeskočí a jen je vypíše.
- Upozornění na zastaralé kompiláty rolí jen tehdy, když `compose_role` neproběhl.
- README: postup aktualizace v instanci a první přechod postaru.
- Testy: 275 (`test_upgrade`: úplnost manifestu, dočasný git repozitář se značkami `v0.98.0`, `v0.99.0`, commitem bez značky a necommitnutým stromem; `--latest` v dry-run, `--tag` s kroky, přechod přes dvě verze, `--after-only` bez duplicit, `--no-after`, selhaný krok, chybná značka a chybějící `core_source`).

## 0.13.0 – 2026-11-20

Unreal, etapa 1, a pole `compile` u modulů (zadání 0.14, 0.14.2; předání `predani_vyvoj_core_soubeh` položka 18 a odpověď na otázku k položce 17); bez migrace. Po aktualizaci v instanci `compose_role` (kompiláty bez modulů Knihovníka) a `hubs --apply` (značky bloku v `## Stav v UE`). Akceptace Knihovníka, stupeň 1, může začít (`hearthlore/tests/scenarios/librarian.md`).

- **`compile: all | listed`** u modulů (12 kap. 2, 3; 07 kap. 14): `fields.yaml`, výčet `compile`, `tpl_agent_module`. Moduly Knihovníka (`lookup`, `file_info`, `completeness`, `canon_check`, `inbox_triage`, `ue_lookup`) mají `listed`: `compose_role` je dá jen roli, která je uvádí v `modules`, nebo skládá roli, která je uvádí (`requires` jdou s modulem); ostatním kompilát vyjmenuje s pokynem předat věc Knihovníkovi. Kontrakt to říká u tabulky spouštěčů. Auditor má `ue_lookup` v profilu. Kompiláty projektových rolí jsou zase kratší (fixture: `Architect` uvádí `ue_lookup`, `Builder` ho skládá).
- **`scripts/hestia_ue.py`** (13 kap. 10.11): čtecí modul pro Python editoru (3.11, jen standardní knihovna a `unreal`, bez `hestia_lib`); actory podle pravidel (tag se vzorem `*`, složka v Outlineru; v položce průnik, mezi položkami sjednocení), **nejdelší shoda vzoru** rozhodne mezi entitami (`stavba:Palac_Kovarna*` vyhraje nad `stavba:Palac*`); na entitu počet, signály realizace přes všechny actory (třídy StaticMesh / Blueprint / BSP / ostatní, zástupné meshe `/Engine/BasicShapes/`, výchozí materiály, fáze `stage:*`, bounds) a nejvýš 500 actorů s detaily. Úroveň realizace se neodhaduje, dotaz „původ“ není. Jen čtení (test hlídá, že modul nevolá zápisové API).
- **`ue_query`** (nový příkaz): `--emit --entity X` (i potomci s pravidlem) nebo `--all` vygeneruje čtecí skript do `Maintenance/ue/`; GameDesigner ho spustí v editoru, skript zapíše surový výsledek vedle sebe; `--import [soubor]` (výchozí podle `--entity` / `--all`, jinak nejnovější) uloží report `Maintenance/reports/ue_<entita>.json` se souhrnem vlastních actorů a za potomky; novější report starším nepřepíše; upozorní na jinou otevřenou mapu. Bez `ue_map.yaml` nebo u entity bez pravidla chyba použití (kód 2).
- **`ue_map.yaml`** (`taxonomy_local`): schéma `map`, `stage_tag_prefix`, `defaults` podle `kind` (`{entity}`), `items` (jmenovité, mají přednost před defaults); chyby schématu = G7, položka s neexistující entitou = G6 (`lint --all`).
- **Hub, `## Stav v UE`** (07 kap. 1, 13 kap. 10.3): `hubs` doplní značky bloku pod ruční text sekce (i v existujících hubech; `strip_generated` je nepočítá jako změnu ručního textu, `task_close` proto neaktualizuje `updated`); blok s datem a cestou reportu, cestou a mapou, počtem actorů (vlastní a za potomky), třídami, zástupnými meshi a výchozími materiály, fázemi, rozsahem a `depth_*` pro srovnání; report starší než `ue_report_days` (výchozí 14) **starý**; bez pravidla nebo reportu prázdný. `tpl_entity` podle 07 kap. 1.
- **Audit** (jen s `ue_map.yaml`): G10 u entity s pravidlem, `depth_d ≥ 2` v režimu build a v posledním reportu bez actora (informace); sekce *Unreal*: počet entit s pravidlem, entity s krokem a cílem v režimu build bez pravidla, s pravidlem bez reportu, staré reporty, postup obnovy.
- **`templates/unreal/init_unreal.py`**: kostra toolsetu Hestia pro Unreal MCP (etapa 2), **neověřená** (API vlastních toolsetů v UE 5.8 je experimentální); jen čtecí nástroj nad `hestia_ue.collect`; test jen syntaxe. Záloha bez editoru (`UnrealEditor-Cmd`) je jen v README.
- Modul `ue_lookup` s konkrétními příkazy, Auditor (týdenní čtení `--all`, G10, sekce *Unreal*), `write_rules` (`ue/`, `reports/ue_*.json`).
- Očekávané výstupy: huby se značkami v `## Stav v UE` (jen značky), kompiláty rolí (bez modulů Knihovníka kromě `ue_lookup`), vědomě přegenerováno. Testy se zástupným modulem `unreal` (`hearthlore/tests/fixtures/unreal_stub/`), vygenerovaný skript se spouští „jako v editoru“.
- Testy: 264 (`test_ue`: hestia_ue, emit, import, hub, audit, lint, kostra; `compile: listed`).

## 0.12.0 – 2026-11-20

Role Knihovník (`Librarian`; zadání 0.14 a 0.14.1, předání `predani_vyvoj_core_soubeh` položka 17); bez migrace. Akceptace ve dvou stupních: scénáře nad `mini_lapikus` s kontrolním seznamem `hearthlore/tests/scenarios/librarian.md` (GameDesigner v chatu s kompilátem `Librarian`), pak scénáře z podkladu `podklady/knihovnik.md` kap. 15 na pilotu. Unreal (`ue_query`, `hestia_ue.py`, blok `## Stav v UE`) přijde s položkou 18.

- **Profil a moduly** (12 kap. 3, 3b; 05 kap. 3.2a, 8): `agents/Librarian.md` (osm povinných kapitol); moduly `lookup` (formát odpovědi s citacemi), `file_info`, `completeness` (náležitosti z taxonomie, `lint --draft`), `canon_check` (hierarchie zdrojů, vědomá změna kánonu), `inbox_triage`, `ue_lookup` (jen čtení; bez `ue_query` jen dodaný report), všechny v režimu `vault` i `chat`; spouštěče v `CONTRACT.md`. `chat_entry`: pole `forma` (`doslovně` / `přeformulováno`, bez něj přeformulováno). Kompiláty **všech** rolí obsahují nové moduly (12 kap. 2: všechny moduly core s režimem `chat`), jsou proto o asi 170 řádků delší.
- **Curator bez předzpracování inboxu**: jen metadata importu; třídění `raw` → `prepared` dělá Knihovník s GameDesignerem (`Curator.md`, `review_plan.md`, `tpl_scratch` „Předzpracování (doplní Knihovník)“). `write_rules.md`: oddíl Knihovník podle 05 kap. 3.2a, řádek `doc_index.json` a `context/`.
- **`doc_index`** (nový příkaz, 13 kap. 10.10) → `Maintenance/doc_index.json`: záznam na poznámku mimo `_core/`, `Maintenance/`, `Roles/_compiled/` (`path`, `title`, `aliases`, `type`, `validity`, `status`, `updated`, `entity`, `domain`, `domains`, `depth`, `build_step`, `master`, `headings`, `links_out`). Obnovují ho i `hubs` (po zápisu hubů, protože generované sekce nesou odkazy) a `audit`; zápis jen při změně obsahu.
- **`compose_context`** (nový příkaz) `--entity` / `--topic` (kategorie, doména, `inbox`) / `--query` → `Maintenance/context/<id>_context.md`: hlavička v HTML komentářích (požadavek, verze core, datum, zdroje), u každé části zdroj, typ, platnost a datum; u entity hub, platné `design` / `spec` / `state` / `decision`, výňatek master lore, aktivní předání, pojmy z glosáře a otevřené otázky; u `inbox` položky `raw` s kandidátními dokumenty. Výběr k `--query` podle zadání 0.14.1: index a glosář, bez diakritiky a velikosti písmen, začátek slova (aspoň 4 znaky, společný začátek nejvýš o 2 znaky kratší než kratší slovo), glosář → hlavní dokument, entita → hub a platné dokumenty, záložně celé texty (uvedeno v hlavičce), u kandidáta důvod shody; pevné nadpisy šablon se neporovnávají. Limit `context_max_chars` (výchozí 60000) platí pro balíček kromě seznamu *Nevešlo se*. Zastaralý balíček = G5 v auditu; `lint` `Maintenance/context/` nekontroluje.
- **`lint --draft <soubor|->` s `--as <cesta>`**: koncept zkontrolovaný jako poznámka na cílové cestě (G6, G7, odkazy vůči vaultu), nic se nezapisuje; stdin v UTF-8.
- **Glosář** (07 kap. 19): `Glossary.md.tpl` s tabulkou *Pojmy projektu* o pěti sloupcích (`Pojem | Význam | Hlavní dokument nebo hub | Aliasy | Zakázané varianty`). U staršího záhlaví vypíše `lint` **varování bez kódu nálezu** (u `--json` na stderr) se zprávou, jak tabulku převést; převod v instanci ručně (`update_core` do `Dashboard/` nezapisuje). V pilotu po aktualizaci přepsat záhlaví prázdné tabulky.
- **Audit, sekce *Knihovník*** (12 kap. 3b.9, 13 kap. 10.10): řádky `changes.md`, jejichž sloupec *co se změnilo* začíná `změna kánonu:` (07 kap. 10), `Inbox/` `raw` (počet, průměrné stáří), `Scratch/` zařazené za období. Období od posledního auditu před dneškem (opakovaný audit týž den počítá se stejným obdobím; `state.json` beze změny formátu); v JSON výstupu `librarian`.
- Fixture `mini_lapikus`: glosář s pěti sloupci a dvěma pojmy, `Inbox/` s pěti položkami `raw` (duplicita s otevřenou otázkou, rozpor s kánonem, postava, doplnění platného návrhu, nápad bez entity). Dosavadní očekávané výstupy beze změny kromě kompilátů rolí (nové moduly, vědomě přegenerováno).
- Testy: 249 (`test_librarian`: index, balíček včetně výběru k `--query`, `lint --draft`, glosář, audit; agenti: profil, moduly, `write_rules` 05 kap. 3.2a, `forma`).

## 0.11.0 – 2026-11-20

`asset_index` a aliasy entit podle CR z pilotu (zadání 0.14, CR_2026-11-19_asset_index_alias_entity, předání `predani_vyvoj_core_soubeh` položka 16); bez migrace. Po aktualizaci v instanci spustit `asset_index --apply`.

- **Pravidlo `alias`** (10 kap. 4 a 7, 13 kap. 10.2): `asset_index` načte `aliases` hubů entit. Jméno souboru bez přípony, nebo jeho prefix `<Jméno>_<Part>`, které se přesně shoduje s aliasem (bez ohledu na velikost písmen), přiřadí soubor této entitě dřív než nejdelší prefix ID entity: `Ostroh_Krov.py` i `Ostroh_Krov_Tasky.py` u entity s `aliases: [Ostroh_Krov]`. V `asset_index.json` a `.md` `rule: alias`; hlavička a pořadí ostatních pravidel beze změny.
- **Alias u dvou entit** = upozornění v reportu („alias … je u entit …; použije se prefix jména“), soubor se přiřadí podle prefixu.
- **Změny přiřazení** proti předchozímu `asset_index.json`: řádky „Změna přiřazení: cesta: stará -> nová (pravidlo)“ v textovém výstupu, v JSON `reassigned` (`path`, `from`, `to`, `rule`). I v dry-runu, takže je vidět před `--apply`.
- Testy: 227 (alias před prefixem, prefix `<Jméno>_<Part>`, nejednoznačný alias, změny přiřazení).

## 0.10.3 – 2026-11-20

CR z pilotu ke jménům rolí a know-how (zadání 0.14, předání `predani_vyvoj_core_soubeh` položky 14 a 15); bez migrace, chování core beze změny.

- **Jména profilů rolí anglicky** (12 kap. 1.0 a 2, CR_2026-11-19_jmena_roli_anglicky): zkušební projekt `mini_lapikus` má `Roles/Builder.md` (`combines: [Architect]`) a `Roles/Architect.md` místo `Stavitel` a `Architekt`; obsah profilů česky. Očekávané kompiláty `expected/compose_role/Builder_compiled.md`, `Architect_compiled.md`; testy `test_compose`, `test_audit`. Kód jména rolí nezná; `lint` znaky jména nehlídá.
- **Tematický seznam pastí** (12 kap. 4.3, 07 kap. 13, CR_2026-11-19_knowhow_tematicke_pasti): komentář v `tpl_knowhow` (sekce *Příznak … Ověřeno* u seznamu odpadají, jedna odrážka = jedna past, sdílení do HearthLore po odrážkách, nad asi 30 odrážek téma rozdělit). `lint` sekce know-how nehlídá; test, že seznam bez sekcí projde.
- Testy shody se zadáním 0.14: šablony `tpl_scratch` (položka 17) a `tpl_entity` (položka 18) a šest modulů Knihovníka (položka 17) jsou vedené jako čekající; test hlídá, že rozdíl trvá, aby se po implementaci výjimka odebrala.
- Testy: 225.

## 0.10.2 – 2026-11-19

Cíl zmínek v backtickách podle CR z pilotu (zadání 0.13.8, CR_2026-11-19_zminky_v_backtickach_cil, předání `predani_vyvoj_core_soubeh` položka 13; z finálního běhu pilotu na 0.10.1); bez migrace. Týká se jen příkazu `frontmatter`.

- **Cílem zmínky ne-MD souboru je jen soubor, který do vaultu přesunula mapa** (ne-MD položka s `target`, v tomto nebo dřívějším běhu). Stejnojmenný soubor jinde ve vaultu (např. `_core/scripts/hestia_lib/config.py`) se nehledá: `` `config.py` `` zůstane textem, a když soubor toho jména existuje v projektu (`zrlib/config.py`), jde do reportu `outside`. V 0.10.1 se převedla na `[[config.py]]` do `_core/`.
- **Zmínka s cestou (`/` i `\`), která od složky dokumentu nevede**, se hledá jedinečným jménem mezi přesunutými soubory (`` `03_ruin\Zricenina_hrad_plan.png` `` → `[[Zricenina_hrad_plan.png]]`). Nejednoznačná → `unresolved`; nenalezená, ale jméno odpovídá souboru v projektu → `outside`; jinak beze změny bez záznamu (kód v textu).
- Odkazy na `.md` a obrázky vložené markdownem beze změny proti 0.10.1.
- Testy: 224 (rozšířen test převodu odkazů: `config.py` v `_core/` i u kódu, cesta od kořene prototypu se `\`).

## 0.10.1 – 2026-11-19

Zmínky souborů v backtickách při migraci (zadání 0.13.7, předání `predani_vyvoj_core_soubeh` položka 12; z A4 pilotu na 0.10.0); bez migrace. Týká se jen příkazu `frontmatter`.

- **Zmínka ne-MD souboru v backtickách** (`` `navrh_brana_straz.png` ``, 06 kap. 4), jen u dokumentů ve vaultu: soubor ve vaultu (přesunutý mapou do `Attachments/`) → **odkaz** `[[jméno.png]]`, ne vložení (při shodném jménu cesta od kořene vaultu); soubor u kódu → zmínka zůstává textem a report ji vypíše (`outside`, důvod „mimo vault, zmínka zůstává textem“). Soubor se hledá cestou od dokumentu, u zmínky bez cesty náhradně jedinečným jménem ve vaultu.
- Zmínka, která na existující soubor nevede (kód jako `` `obj.method` ``, jméno souboru bez souboru), se nemění a do reportu nejde, aby report nezahlcoval běžný kód v textu.
- JSON `items[].outside[].reason` rozlišuje přepsanou cestu obrázku („mimo vault, Obsidian ho nevykreslí“) a zmínku („mimo vault, zmínka zůstává textem“).
- Testy: 224 (rozšířen test převodu odkazů).

## 0.10.0 – 2026-11-19

Převod odkazů při migraci podle CR z pilotu (zadání 0.13.6, CR_2026-11-19_prevod_odkazu_migrace, předání `predani_vyvoj_core_soubeh` položka 11); bez migrace. Týká se jen příkazu `frontmatter`.

- **Aliasy** (06 kap. 4): jméno cíle `` `soubor.md` `` se hledá i v `aliases` dokumentů ve vaultu, včetně `aliases` nastavených mapou v témže běhu. Odkaz na staré jméno přejmenovaného dokumentu kroku (`README_bloky.md` → `Steps/03_ruin.md`) se převede na `[[03_ruin]]`. Shoda jména souboru s aliasem jiného dokumentu = nejednoznačný název (beze změny, do reportu).
- **Cesta, která od složky souboru nevede** (typicky od kořene prototypu), se zkusí jako jedinečné jméno souboru včetně aliasů; nejednoznačné beze změny do reportu.
- **Obrázky a odkazy markdownem na ne-MD soubory** (02 kap. 7, pravidlo 6), jen u dokumentů ve vaultu, mimo bloky a úseky kódu: cíl ve vaultu (přesunutý položkou mapy) → `![[jméno]]` (u odkazu `[[jméno|text]]`, při shodném jménu cesta od kořene vaultu); cíl mimo vault (generované a podkladové soubory u kódu) → relativní cesta od nového umístění dokumentu a v reportu „mimo vault, Obsidian ho nevykreslí“ (JSON `items[].outside`); neexistující cíl beze změny do `unresolved`. URL, kotvy a odkazy na `.md` se nemění. Opakovaný běh nic nemění.
- **Ne-MD položky mapy** (13 kap. 10.1): obrázky a jiné podklady s `target` v `Attachments/`; jen přesun, bez frontmatteru. Ne-MD položka s `frontmatter` nebo s cílem mimo `Attachments/` je chyba mapy (návratový kód 2).
- **Důvod „cíl mimo vault“** i u odkazu bez cesty, když soubor `.md` toho jména existuje v projektu mimo vault a nepřesouvá se (dřív „cíl neexistuje“).
- Fixture migrace: dokument kroku pod starým jménem s aliasem z mapy, předání s cestou od kořene prototypu, ručně kreslený obrázek do `Attachments/`, generovaný obrázek u kódu.
- Testy: 224.

## 0.9.1 – 2026-11-19

Odpovědi na otázky k 0.9.0 (zadání 0.13.5, předání `predani_vyvoj_core_soubeh` položka 10); bez migrace.

- **Dokument s několika entitami se počítá u všech uvedených** (01 kap. 9): `## Dokumenty` v hubu, G3, hloubka návrhu, G4 (platný `state`), G5 (změna kterékoli z entit), kontrolní seznam `task_close`, aktivní předání v `Dashboard/Index.md`. Dřív jen první entita ze seznamu. Pozor při aktualizaci: dokumenty se seznamem `entity` se nově objeví v hubech všech uvedených entit a mohou zmizet nálezy G3 nebo G4.
- **`target_mode` u lokální domény povinný** (13 kap. 5): doména z `taxonomy_local/domains.yaml` bez něj je chyba konfigurace (návratový kód 2) se zprávou, co doplnit.
- Šablony (07 kap. 7, 15): `tpl_handover` bez `depth:`; report auditu (`tpl_report` i `audit`) s nadpisy `### Chyby`, `### Upozornění`, `### Informace` bez výčtu kódů, nálezy podle závažnosti z `findings.yaml`.
- Testy: 222.

## 0.9.0 – 2026-11-19

Návrh a realizace (zadání 0.13–0.13.3, předání `predani_vyvoj_core_soubeh` položka 8; ověřuje se na pilotu); bez migrace. Existující entity se nemění, ale v doménách s výchozím režimem `design` (`npc`, `gameplay`, `narrative`) se cíl nově plní hloubkou návrhu z dokumentů, ne `depth_*`: zralost, G1 a stav v hubu se tam mohou změnit.

- **Režim cíle** (01 kap. 3, 5): `domains.yaml` má `target_mode` (`environment`, `structures`, `paths` = `build`; `npc`, `gameplay`, `narrative` = `design`), entita výjimku polem `target_mode_<domain>` (`fields.yaml`, výčet `target_mode`). Lokální doména bez `target_mode` má režim `build`; neplatná hodnota v `domains.yaml` je chyba konfigurace.
- **Hloubka návrhu** entity v doméně se počítá: nejvyšší `depth` platných (`validity: valid`) dokumentů `design` a `spec` entity a domény, bez zavržených alternativ (`status: rejected`). `depth_<domain>` je realizace.
- **Splnění cíle podle režimu** (`build`: `depth_*`, `design`: hloubka návrhu): zralost (04 kap. 3, report auditu a `Dashboard/Index.md`), **G1** (v režimu `design` zpráva „návrh d N < target_d T (režim design)“), agregace v hubu.
- **G13 připraveno ke stavbě** (`findings.yaml`, 04 kap. 4): režim `build`, hloubka návrhu ≥ cíl, realizace pod cílem. Informační nález, jen v reportu (jako G1, G9, G10).
- **Hub, `## Domény`** (13 kap. 10.3): `| Doména | Návrh | Realizace | Cíl | Režim | Stav |`, stav podle režimu.
- **`## Dokumenty`** ukazuje `depth` jen u typů, které ho mají: `fields.yaml` `depth` bez `handover`, `guide`, `checklist` (ani povinně, `types.yaml`; zadání 0.13.3).
- **Matice ve variantě skript** (`Dashboard/views/generated/entity_domain_matrix.md`, 13 kap. 10.9): režim `build` `realizace/cíl`, u vyšší hloubky návrhu „(návrh N)“; režim `design` „návrh N/cíl“. Varianty Bases a Dataview beze změny (jen realizace; hloubku návrhu spočítat neumí, podklad Q1).
- **Lint** (01 kap. 9.1, 12): `depth_x` povinné jen u cíle v režimu `build` (podmínka `present in build mode`); `target_mode_x` bez `target_x` = varování; hodnota mimo `design`/`build` = chyba.
- `depth.yaml`: ke každé úrovni popis návrhu (`design`, 01 kap. 5, zadání 0.13.2). Šablona hubu `tpl_entity`: komentář k realizaci a `target_mode_<domain>` (07). Profil Auditora a modul `metadata`: `depth_*` mění jen ten, kdo realizoval; zralost podle režimu. Odkazy G1–G12 → G1–G13.
- Fixture (13 kap. 9.1): `navrh_palac_obydli_stred` hloubka 4 → `Palac_Obydli` **G13** a G1 (zavržená alternativa s hloubkou 5 se nepočítá); `Characters` s potomky `Characters_Sedani` (`target_mode_gameplay: build`, splněno realizací) a `Characters_Animace` (režim `design`, splněno návrhem `navrh_characters_animace` bez realizace; `target_mode_npc` bez cíle → varování lintu). Očekávané výsledky: nálezy, huby, matice varianty skript zvlášť (`expected/views/entity_domain_matrix_script.json`).
- Testy: 220.

## 0.8.1 – 2026-11-19

Šablona kroku (zadání 0.12.3, předání `predani_vyvoj_core_soubeh` položka 7); bez migrace.

- **`tpl_step`**: komentář s volitelnou sekcí `## Historie` (archivovaní předchůdci kroku) pod *Známými pastmi* (07 kap. 17, 10 kap. 5a). `hub_sections.yaml` beze změny, lint sekci nevyžaduje; dokument kroku s ní i bez ní projde.
- Testy: 214.

## 0.8.0 – 2026-11-19

Migrační mapa podle CR z pilotu (zadání 0.13.4, CR_2026-11-18_mapa_split_s_cilem, předání `predani_vyvoj_core_soubeh` položka 9); bez migrace.

- **Duplicitní `source` je chyba mapy** (13 kap. 10.1): `frontmatter` skončí kódem 2 („položka N: source už je v položce M“) a nic neprovede. Zdroje se porovnávají po normalizaci (`\` → `/`, `./`, úvodní `/`). Dřív vyhrála poslední položka a frontmatter první se tiše ztratil.
- **`split: true` s `target`** se zpracuje jako běžná položka (přesun s `--move`, frontmatter, převod odkazů) a navíc se vypíše jako úkol rozpadu (`note`), i při opakovaném běhu po přesunu. `split: true` bez `target` beze změny: zůstává na místě, jen úkol.
- Fixture `migration/map.yaml`: položka `split` s `target` (`README_ruin.md`).
- Testy: 213.

## 0.7.1 – 2026-11-18

Snippety core v `update_core` (zadání 0.12.2, předání `predani_vyvoj_core_soubeh` položka 6); bez migrace.

- **`update_core` srovná snippety core** `.obsidian/snippets/hestia-*.css` při každém běhu, i bez změny verze a bez přepínače (02 kap. 7.1, 13 kap. 10.6): chybějící doplní, změněné přepíše, ty, které core už nemá, přesune do `_to_delete/.obsidian/snippets/`. Zapnutí v `appearance.json` ani vlastní snippety bez předpony `hestia-` nemění. Každý zásah zapíše do `changes.md`; dry-run je vypíše.
- README: snippety v existujících instancích přes `update_core`, vlastní úprava pod jiným jménem.
- Testy: 211.

## 0.7.0 – 2026-11-18

Zátěžový test a skrytí složek ve stromu souborů (předání `predani_vyvoj_core_soubeh` položky 4 a 3); bez migrace.

- **Zátěžový test** (`hearthlore/tests/perf_load.py`): generuje syntetický projekt z kopie `mini_lapikus` (entity v hierarchii region → lokace → stavby → místnosti, dokumenty, scratch, kód s hlavičkami, generované pohledy) a měří příkazy přes CLI. Windows 11, Python 3.13, medián ze 3 běhů:

| Příkaz (CLI včetně startu Pythonu) | ~300 poznámek | ~3000 poznámek, core 0.6.1 | ~3000 poznámek, core 0.7.0 |
|---|---|---|---|
| `asset_index` | 0,8 s | 4,7 s | 4,4 s |
| `hubs` (s generovanými pohledy) | 0,9 s | 42,9 s | 5,2 s |
| `hubs` bez generovaných pohledů | 0,8 s | 44,9 s | 5,3 s |
| `lint --all` | 0,9 s | 5,1 s | 4,9 s |
| `audit` | 1,1 s | 32,4 s | 6,0 s |
| `hubs --apply`, první běh (zapisuje všechny huby) | 1,1 s | 46,0 s | 7,0 s |

  Generované pohledy (matice, mapa) stojí v `hubs` méně než rozptyl měření. První běh nad čerstvě zapsanými soubory je pomalejší kvůli studené cache a antiviru (`asset_index` 45–52 s při 3000 souborech), druhý už ne; s kódem to nesouvisí. Generátor ověřuje `test_perf_load.py`.
- **Výkon** (nalezeno zátěžovým testem): `Model.docs_of` procházel u každé entity všechny poznámky a znovu rozlišoval odkazy (entity × poznámky). Nově index dokumentů podle entity a jednou rozlišené `entity` za běh. `audit` počítal ID nových položek fronty průchodem celé fronty u každé položky. Výstupy beze změny (golden testy).
- **Snippety** `.obsidian/snippets/hestia-hide-core.css` a `hestia-hide-maintenance.css` ve `vault_template` (02 kap. 7.1, CR_2026-11-17_skryt_core_ve_stromu): skryjí složku ve stromu souborů. Ve výchozím stavu vypnuté, zapnutí je osobní volba (*Vzhled → Úryvky CSS*), `appearance.json` se nedodává. `.gitignore` šablony verzuje jen `hestia-*.css` (vzor `.obsidian/snippets/*` + výjimka; tvar ze zadání by výjimku neuplatnil, otázka v předání). README: postup pro existující instance.
- Testy: 210.

## 0.6.1 – 2026-11-18

Úpravy z ověření 0.6.0 v Obsidianu; bez migrace.

- `update_core --with-views` doplní i složku `Dashboard/views/local/` (`.gitkeep`), pokud v instanci chybí; dřív ji dostaly jen nové instance z `init`.
- **Oprava Dataview** `dv_map_entities_by_place`: všechny entity padaly do „(bez umístění)“. `default(x, list())` se v Dataview vektorizuje přes prázdný seznam a vrátí vždy prázdný seznam; podmínka je teď `length(x) > 0`. Odhalilo ověření v Obsidianu.
- Mapa ve variantě skript: entita bez umístění má prázdné pole *Místo* místo textu „(bez umístění)“ (řadí se na začátek: v hierarchii stojí nejvýš, případná chyba je hned vidět). Bases a Dataview beze změny.

## 0.6.0 – 2026-11-18

Pohledy po otázkách k 0.5.0 (zadání 0.12, předání `predani_vyvoj_core_soubeh` položka 2b, 13 kap. 10.9); bez migrace (nové pohledy do existující instance: `update_core --with-views`).

- **Varianta skript pro matici a mapu:** `Dashboard/views/generated/entity_domain_matrix.md` a `map_entities_by_place.md` s generovaným blokem v sekci *Pohled*, který přepisuje `hubs` (modul `hestia_lib/views.py`). Matice bere domény a očekávané domény z taxonomie instance (včetně `taxonomy_local`), mapa dědí `located_in` od `parent` do libovolné hloubky a říká, od koho. Chybějící soubor `hubs` nehlásí (doplní ho `--with-views`), chybějící blok ohlásí.
- **Manifest pohledů** `taxonomy/views.yaml`: soubory každého pohledu a příznak `game_layer`. `init --no-game-layer` a `update_core --with-views` při `game_layer: false` vynechají jen pohledy s příznakem (tři zkušební pohledy ho mají).
- **`Dashboard/views/local/`** ve `vault_template` pro vlastní pohledy instance; core do ní nezapisuje.
- Aktualizace existujících pohledů v instancích (13 kap. 10.9) zatím není, přijde s CR k Q1.
- Testy: výstup varianty skript proti stejným očekávaným výsledkům jako Bases a Dataview, lokální `kind` a dědičnost přes čtyři úrovně, manifest proti souborům, dodání bez herní vrstvy. Hodnocení všech variant včetně kritéria *Čitelnost pro agenta* v `hearthlore/podklady/Q1_pohledy.md`. Testy: 206.

## 0.5.0 – 2026-11-18

Pohledy pro rozhodnutí Q1 (předání `predani_vyvoj_core_soubeh` položka 2, 13 kap. 10.9); bez migrace (pohledy do existující instance: `update_core --with-views`).

- **Tři zkušební pohledy** (04 kap. 5.1) ve dvou variantách v `vault_template/Dashboard/views/`: `bases/structures_status.base`, `bases/entity_domain_matrix.base`, `bases/map_entities_by_place.base` (core plugin Bases) a `dataview/dv_structures_status.md`, `dv_entity_domain_matrix.md`, `dv_map_entities_by_place.md` (komunitní plugin Dataview, v šabloně vypnutý). Matice: `depth/target`, ⚠ = mezera, „bez cíle“ = očekávaná doména podle `kind` (napevno z `kinds.yaml`, test hlídá shodu). Mapa: `located_in` s dědičností od `parent` přes tři úrovně předků (bez rekurze v obou variantách).
- **`init`** dodá pohledy do nových instancí; instance bez herní vrstvy je nedostane (pohledy čtou entity).
- **`update_core --with-views`**: nakopíruje chybějící pohledy z `vault_template` nového core, existující nepřepíše, zapíše řádek do `changes.md`; funguje i bez změny verze core.
- **Oprava `update_core`** (13 kap. 10.6): přerušenou výměnu (existuje `_core.new`, chybí `_core`) dokončí další běh; dřív skončil chybou.
- `Dashboard/Index.md` (šablona): odkaz na obě varianty pohledů.
- Fixture: `Lapikus` má `located_in: ["[[Lapikus_Region]]"]` (dědičnost přes dvě úrovně). Očekávané výsledky pohledů nad `mini_lapikus` v `hearthlore/tests/expected/views/*.json` a podklad k Q1 `podklad_Q1.md`. Obsidian ani Dataview se v testech nespouští: testy kontrolují strukturu, shodu s taxonomií a referenční výsledky; syntaxi pohledů ověří akceptace v Obsidianu. Testy: 201.

## 0.4.1 – 2026-11-18

Srovnání se zadáním 0.11.2 (odpovědi B1–B3 a otázky z akceptace fáze 3); bez migrace.

- **Průběh CR jako tabulka** (07 kap. 11, 11 kap. 3, 13 kap. 10.8): šablona `tpl_change_request.md` má pod *Průběhem* záhlaví `| datum | stav | kdo | poznámka |`; `export_cr` připíše řádek `| RRRR-MM-DD | new | export_cr | ze structure_log <datum> |` pod něj.
- **`task_close --archive-handover`** odmítne předání s otevřenými otázkami (`- [ ]` v *Otevřených otázkách*), s `--force` projde (12 kap. 5 krok 2). Kontrolní seznam u splněného předání s otevřenými otázkami radí zodpovědět nebo přenést. Modul `task_close` (krok 2) doplněný.
- **Oprava:** předání změněné ve stejném tasku a zároveň archivované skončilo konfliktem zápisu (úprava `updated` mířila na původní cestu). `ChangeSet.move` nově přenáší naplánovanou úpravu se souborem.
- Ověřeno testy (beze změny kódu, v core od 0.3.2 nebo 0.4.0): klíč `instance`, datum exportu v názvu CR, logy jako tabulky a čtení starého tvaru, odkazy ve frontě a reportech bez G6, prázdné řádky v generovaných blocích (nový integrační test nad všemi bloky). Testy: 190.

## 0.4.0 – 2026-11-18

Nový příkaz `export_cr` (souběh s pilotem, předání `predani_vyvoj_core_soubeh` položka 1); bez migrace.

- **`export_cr`** (13 kap. 10.8): jeden záznam `structure_log.md` = jeden CR v `Maintenance/outbox/CR_RRRR-MM-DD_<short_name>.md` podle šablony `tpl_change_request.md`. Exportují se záznamy bez vyplněného `cr:` v kategoriích `friction`, `missing`, `surplus`, `collision`, `taxonomy`, `idea`; `works` jen s `--include-works`. Vyplní `cr_status: new`, `source_instance`, `hestia_version` (`_core/VERSION`), `structure_log` (citace `datum | kategorie | popis`), `area` (`--area`, jinak `taxonomy` → `taxonomy`, ostatní → `process`), *Co se stalo*, *Návrh* a řádek `new` v *Průběhu*; *Dopad* a *Alternativy* zůstávají k doplnění. `short_name` z popisu (ASCII, nejvýš 40 znaků bez useknutého slova, při shodě `_2`). Po zápisu doplní u záznamu `cr: <ID>` (jediná úprava existujícího řádku logu) a `updated`. Idempotentní; dry-run vypíše plán a diff logu.
- **Konfigurace:** nový volitelný klíč `instance` (`defaults.yaml`: `null`) pro `source_instance`; bez něj jméno složky projektu. Šablona `config.yaml` ho uvádí jako komentář.
- Profil Curator: export CR přes `hestia.py export_cr`. README: aktivní předání `predani_vyvoj_core_soubeh`, příkaz `export_cr`.
- Fixture: `structure_log.md` se záznamy pro export (vyplněné `cr:`, `works`, svislítko v textu, shodný popis → `_2`); očekávaný CR `expected/export_cr/`. Testy: 187.

## 0.3.2 – 2026-11-18

Úpravy z akceptace fáze 3 (zobrazení v Obsidianu); bez migrace.

- **Generované bloky** mají prázdný řádek za značkou `start` a před `end`; Obsidian jinak tabulku hned za komentářem nevykreslil.
- **Fronta a report s odkazy:** cíl poznámky jako wikilink, soubor mimo vault zkráceně (`složka/soubor`), aby tabulka fronty nebyla příliš široká; klíč nálezu dál kód + cíl (porovnání bez `[[ ]]` a backticků, starší položky se rozpoznají). Zralost a otázky v reportu s odkazy. `queue.md` a `reports/` se nekontrolují na rozbité odkazy (historické záznamy).
- **Logy jako tabulka:** `changes.md`, `structure_log.md`, `structure_version.md` mají před řádky záhlaví tabulky a řádky s krajními svislítky `| RRRR-MM-DD | … |` (bez nich Obsidian tabulku nevykreslí); připisování nenechá prázdný řádek. Parser čte i starší řádky `RRRR-MM-DD | …`. Popis formátu v šablonách, modulech `task_close`, `chat_entry` a profilu Curator sjednocený.
- `Dashboard/Index.md`: bez vysvětlujícího komentáře nad blokem *Přehled*.

## 0.3.1 – 2026-11-18

Srovnání se zadáním 0.10.2 (odpovědi na otázky z fáze 3); fronta se doplní sama, jinak bez migrace.

- **G2 a G3 nad podstromem** (04 kap. 4): u entity s potomky stačí cíl nebo dokument v doméně u entity nebo kteréhokoli potomka; listové entity beze změny.
- **G5** (04 kap. 4, 05 kap. 6): dokument bez změny `updated` déle než `stale_doc_days`, když se jeho entita od té doby změnila (`changes.md`); bez změny entity jen v *Doporučených krocích*. Nově i **kompilát role starší než zdrojů** (nové složení by ho změnilo, 13 kap. 6).
- **Fronta se sloupcem `closed`** (05 kap. 7.2, 07 kap. 8, 13 kap. 7): zmizelý nález = `state: done` + datum v `closed`; šablona `tpl_queue.md` s novým sloupcem; `audit` starou tabulku bez `closed` doplní.
- **`task_close` vrací 1**, když lint najde chybu ve změněných souborech (13 kap. 3, 12 kap. 5); upozornění 0.
- Fixture: `Palac_Kovarna` a `Palac_Obydli` bez cíle `gameplay` (G2 na `Palac` nad podstromem, 13 kap. 9.1); fronta fixture se sloupcem `closed`; očekávané nálezy (30) a sekce hubů přepočtené. Testy nových pravidel.

## 0.3.0 – 2026-11-18

Fáze 3 roadmapy: skripty podle zadání 13 kap. 3 a 10 (R1–R5), zadání 0.10; bez migrace.

- **`lint`** (13 kap. 10.7): bez argumentů soubory změněné podle gitu (poznámky i kód s hlavičkami), s argumenty zadané soubory, `--all` celý vault a hlavičky kódu; G6/G7 hlaviček skriptů (10 kap. 9), pevné záhlaví tabulky *Kdo používá*, schéma `folder_map` a `tag_map`.
- **`asset_index`** (10 kap. 6–9, 13 kap. 10.2): pravidla propojení v pořadí hlavička → jméno → `folder_map` → krok → odkaz z dokumentu; entity sdíleného kódu z *Kdo používá*; `asset_index.json` + `.md` jedním během, přepis jen při změně obsahu.
- **`hubs`** (13 kap. 10.3, R2): bloky Domény (s agregací z potomků), Dokumenty, Postup stavby, Soubory, Otevřené otázky; Skripty v dokumentech kroků; přehled v `Dashboard/Index.md` (šablona vaultu má nový blok v sekci *Přehled*). Jen mezi značkami, `updated` se nemění.
- **`audit`** (04 kap. 3–4, 13 kap. 10.4, R3, R4): G1–G12, zralost místo/lokace × doména, report podle 07 kap. 7 + JSON, `reports/state.json`; fronta se stabilním klíčem, zmizelé nálezy `done RRRR-MM-DD`, G1/G9/G10 jen v reportu; `--baseline`.
- **`task_close`** (13 kap. 10.5, R5): dotčené entity z gitu, `asset_index.json` a pole `entity`; řádky `changes.md`, `updated`, archivace předání; huby, lint, G11 dotčených entit a kontrolní seznam.
- **`frontmatter`** (13 kap. 10.1, 06 kap. 3–4, R1): migrace podle mapy YAML s `--move`, doplněním frontmatteru (řádkově, `--force`) a převodem odkazů; položky `split` jako úkoly.
- **`update_core`** (13 kap. 10.6, 11 kap. 6): rozdíl verzí, migrační poznámky z changelogu, záloha do `_to_delete/_core_<verze>/`, `structure_version.md`, odstranění hodnot `taxonomy_local` převzatých do core; kostra `scripts/migrations/`.
- **`init --no-game-layer`** (13 kap. 3, 11 kap. 7a): bez kořene, master lore, `prototypes` a `Entities/`, `required_docs: []`.
- Modul `task_close`: krok 10 s voláním skriptu. Testy: fixture s pevným záhlavím *Kdo používá* a blokem v `Index.md`, fixture `migration/`, očekávané `findings.json`, `asset_index.json`, `hubs/`, `task_close_dry_run.txt`; testy dry-run (hash), idempotence, G11 v dočasném repu.

## 0.2.2 – 2026-11-18

Oprava z akceptace fáze 2 (zadání 0.9.6, 13 kap. 2; bez migrace).

- **Core neodkazuje mimo `hestia/`:** `README.md` a `CHANGELOG.md` odkazovaly relativně na zadání, předání a CR v repozitáři HearthLore (`../hearthlore/…`); v instanci z nich vznikaly nevyřešené odkazy, které rychlý přepínač Obsidianu nabízel jako neexistující soubory. Odkazy mimo core jsou teď cesty v backtickách, odkazy uvnitř core zůstávají. Opraven i nefunkční odkaz `12_kontrakt_agentu.md` ve `write_rules.md`.
- Testy: `test_core_links.py` – žádný textový soubor v `hestia/` neodkazuje mimo `hestia/` (markdown odkazy i wikilinky s cestou) a odkazy uvnitř core vedou na existující soubor.

## 0.2.1 – 2026-11-17

Srovnání se zadáním 0.9.5 (odpovědi na otázky z fáze 2; bez migrace).

- **`compose_role`** (12 kap. 2): kompilát se jmenuje `Roles/_compiled/<Role>_compiled.md` (jedinečnost jmen vedle `Roles/<Role>.md`) a obsahuje **všechny moduly core s režimem `chat`** (pořadí podle tabulky spouštěčů v kontraktu), za nimi lokální moduly z profilů s transitivními `requires`; moduly jen pro vault vyjmenuje.
- `CONTRACT.md`: `trigger: always` (12 kap. 2, 01 kap. 9.1).
- **Lokální doplňky pravidel** (02, 05, 13 kap. 4): `init` zakládá `Maintenance/write_rules_local.md` a `review_plan_local.md` z `.md.tpl` jako prázdné doplňky (`type: reference`); kontrakt, profily Curator a Auditor, `write_rules`, `review_plan` a `file_safety` na ně odkazují.
- Beze změny, jen potvrzeno zadáním: `knowhow_lookup` v obou režimech, „jedna strana“ = nejvýš 60 řádků a 4000 znaků, nadpisy profilů údržby podle 05 kap. 8, kompilát bez frontmatteru mimo `lint`.
- Testy: kompilát se všemi moduly s režimem `chat` i u profilu, který je neuvádí; nové jméno kompilátu a očekávané výstupy `expected/compose_role/<Role>_compiled.md`; `trigger: always`; `init` zakládá lokální doplňky; parita výčtu `modes` se sdíleným řádkem katalogu 01 kap. 9.1.

## 0.2.0 – 2026-11-17

Fáze 2 roadmapy: kontrakt a agenti (předání `hearthlore/Handovers/predani_vyvoj_core_f1-3.md`, zadání 0.9.4; bez migrace).

- **`agents/CONTRACT.md`** (L0, 12 kap. 2): co je Hestia, start, kam smíš psát, tabulka spouštěčů všech modulů, povinné uzavření tasku; jedna strana.
- **`agents/modules/`** (L1): všech 12 modulů z katalogu 12 kap. 3 (`start`, `idea_capture`, `decision`, `knowhow_lookup`, `knowhow_write`, `question`, `file_safety`, `handover_out`, `task_close`, `chat_entry`, `metadata`, `asset_header`); obsah z 12 kap. 2.2–6, pasti z rozboru instrukcí rolí (pilot 07). Obecné, bez projektových jmen a funkčních wikilinků.
- **Profily `Curator.md` a `Auditor.md`** s kapitolami podle 05 kap. 8 a moduly z katalogu.
- **Výchozí `write_rules.md`** (matice 05 kap. 4, schvalování kap. 5, chráněné soubory) a **`review_plan.md`** (plán 05 kap. 6; prahy jen jako klíče `thresholds` z `config.yaml`, 13 kap. 4).
- **`compose_role`** (12 kap. 2, 2.2; 13 kap. 3): `Roles/_compiled/<Role>.md` = kontrakt + moduly + profil; profil z `Roles/`, jinak z `_core/agents/`; `combines` do hloubky (cyklus = chyba konfigurace) s poznámkou o přednosti přísnější role; lokální moduly z `Roles/modules/` (kolize s core = chyba konfigurace); pořadí modulů: profil, složené profily, transitivní `requires`, `chat_entry`; moduly jen pro `vault` vynechá a vypíše. Hlavička s verzí core, datem a zdroji; zapisuje jen při změně obsahu (idempotentní), dry-run s diffem; profil `superseded`/`archived`/`outdated` odmítne.
- Testy: katalog modulů ze 12 kap. 3 (existence, frontmatter, režimy, sekce), kontrakt na jednu stranu a se všemi moduly, profily údržby pokrývají 05 kap. 8, `write_rules` pokrývá matici, `review_plan` prahy, frontmatter agentů projde `lint`; `compose_role` nad profily zkušebního projektu (`Roles/Stavitel.md` skládá `Architekt.md`, lokální modul `spec_template`) dává očekávaný kompilát (`expected/compose_role/`), chyby, dry-run, idempotence.

## 0.1.4 – 2026-11-17

`hearthlore/change-requests/CR_2026-11-17_core_vyloucit_v_obsidianu.md`, zadání 0.9.3 (bez migrace).

- `vault_template/.obsidian/app.json`: `userIgnoreFilters` vylučuje celý `_core/` místo `_core/scripts/` (02 kap. 7). Platí jen pro nově zakládané vaulty; existující instance si filtr upraví ručně.
- Test: `init` zapíše přesně seznam vyloučených složek podle 02 kap. 7.

## 0.1.3 – 2026-11-17

Srovnání se zadáním 0.9.2 (bez migrace).

- `tpl_crosscut.md` a `tpl_lore_master.md` doslovně podle 07, kap. 5 a 18: hodnota prázdná, zástupný odkaz v komentáři; kořen master lore doplní `init`. Kostra master lore ve `vault_template/` odvozená ze šablony.
- Test shody šablon se 07 už nemá výjimky.

## 0.1.2 – 2026-11-17

Srovnání se zadáním 0.9.1 (odpovědi na otázky z fáze 1; bez migrace).

- **Core bez kolizí jmen ve vaultu** (13 kap. 2):
  - šablony mají předponu `tpl_` (`tpl_entity.md` …) a v hodnotách nemají funkční wikilinky (07, úvod). U `tpl_crosscut` (`derived_from`) a `tpl_lore_master` (`entity`) je proto zástupný odkaz jen v komentáři (v 07 srovnáno v 0.9.2);
  - kostra vaultu je jako `*.md.tpl` a `init` ji přejmenuje na `.md`;
  - `types.yaml` odkazuje na `tpl_` šablony.
- `lint` nekontroluje `_core/` a provizorní přednost poznámek mimo `_core/` při rozlišení odkazů je zrušená: shodná jména jsou zase nejednoznačný odkaz (G6).
- Šablona hubu: v `## Otevřené otázky` komentář pro ruční položky a blok `hestia:generated` (07 kap. 1); stejně i huby zkušebního projektu.
- `taxonomy_local/tech.yaml`: struktura `items: [{id, label?}]` (13 kap. 5).
- Beze změny, jen potvrzeno zadáním: `validity` a `status` podle 01 kap. 9.1, hub kořene z `init` s `--root-kind`, celá `Maintenance/reports` vyloučená v Obsidianu.
- Testy: vault z `init` nemá kolize jmen s `_core/` (13 kap. 9.2), šablony bez funkčních wikilinků, parita `validity`/`status` s 01 kap. 9.1.

## 0.1.1 – 2026-11-17

Srovnání se zadáním 0.9 (bez migrace).

- `templates/change_request.md`: pole `gd_relevance` a sekce *Průběh* (07 kap. 11).
- `taxonomy/`: pole `gd_relevance` u `change_request` a výčet `gd_relevance` (`direct`, `indirect`, `none`; 11 kap. 2).
- `defaults.yaml` a `vault_template/Maintenance/config.yaml`: `game_layer: true` (13 kap. 4); hodnota mimo `true`/`false` je chyba konfigurace.
- `lint` při `game_layer: false` (01 kap. 2, 13 kap. 5): herní sekce se nevede u žádného typu, povinná herní pole se nevyžadují, herní pravidla (`domain`/`domains`, kategorie, hloubka, milníky) se nespouštějí; herní pole ve frontmatteru jsou upozornění G7. Orchestrační pravidla platí beze změny. `audit` (G1–G4, G10, G12) to zohlední ve fázi 3.

## 0.1.0 – 2026-11-17

Fáze 1 roadmapy: taxonomie a šablony (předání `hearthlore/Handovers/predani_vyvoj_core_f1-3.md`, zadání 0.8).

- **`taxonomy/`** (13 kap. 5): `domains`, `categories`, `kinds`, `types`, `fields`, `enums`, `depth`, `findings`, `hub_sections`, `build_step_catalog`, `defaults`. Odvozeno z 01; výčty z 03, 05, 10, 11 nesou vlastní `spec`. Sloučení s `Maintenance/taxonomy_local/` (core ∪ local, kolize = chyba konfigurace, rozšíření výčtu jen s `open: true`); lokální `build_steps`, `milestones`, `tech`.
- **`templates/`**: všech 18 šablon ze 07 (doslovně podle zadání); `queue`, `changes`, `structure_log` jako soubory s frontmatterem (13 kap. 7).
- **`vault_template/`** (02): zóny vaultu, funkční `.obsidian` (`app.json`, `core-plugins.json`, `templates.json`, `community-plugins.json`) a `.gitignore` uživatelského nastavení (02 kap. 7.1), `Dashboard/Index.md`, `Glossary.md` (rozdíl `place` / `location`, Q29), `Maintenance/` (config, verze struktury, zdroje, `taxonomy_local`), `entrypoint.md`, kostra master lore.
- **`scripts/hestia.py`** + `hestia_lib/`: společné argumenty a návratové kódy (13 kap. 3).
  - `init`: založí vault do prázdné složky (`_core/` = kopie core, hub kořenové entity s `target_narrative: 1`, master lore, logy ze šablon, `CLAUDE.md` v nadřazené složce, pokud ještě není); bez `--apply` dry-run.
  - `lint` (rozsah fáze 1): G7 podle 01 kap. 12 (povinná a podmíněná pole, výčty core ∪ local, data, hloubka, `domain`/`domains`, herní sekce u typů bez ní, kategorie mimo doménu, `depth_x` bez `target_x`, víc master lore pro jeden kořen, jednostranné `alternative_to`, povinné sekce hubu a kroku, milníky, krok bez dokumentu v `Steps/`); G6 pro wikilinky (tělo i frontmatter, bez bloků kódu a komentářů) a cesty v `assets`. Výběr změněných souborů z gitu a hlavičky skriptů přijdou ve fázi 3.
  - Řádkový zápis frontmatteru (pořadí klíčů, komentáře, uvozovky, LF/CRLF), atomický zápis s kontrolou hashe.
- **Testy** (v `hearthlore/tests/`, mimo distribuovaný core): zkušební projekt `fixtures/mini_lapikus` (syntetický, 13 kap. 9.1), `expected/lint_findings.json`, testy parity 01 ↔ YAML, konzistence taxonomie, frontmatteru, odkazů, šablon (shoda se 07, vyplněné projdou lint), `init` a `lint`. Spuštění z kořene repozitáře: `python -m unittest discover -s hearthlore/tests`.
