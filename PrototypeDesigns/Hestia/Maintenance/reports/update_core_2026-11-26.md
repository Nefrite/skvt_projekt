---
type: report
updated: 2026-11-26
---
# Aktualizace core 2026-11-26

## Přechod 0.25.0 → 0.26.0
- Stav: dokončeno
- Výměna `_core/`: starý core v `_to_delete/_core_0.25.0/`; řádek v `structure_version.md`.
- Záznamy manifestu: 0.26.0.

### Automatické kroky
- `asset_index`: v pořádku (běh 1, 17:43)
  - bez změn přiřazení
- `hubs`: v pořádku (běh 1, 17:43)
  - změněné soubory: 10
- `doc_index`: v pořádku (běh 1, 17:43)
  - index beze změny
- `compose_role`: v pořádku (běh 1, 17:43)
  - změněné kompiláty: 9 z 9
  - changed (nahrát do Claude Projectu): Roles/_compiled/Architect_compiled.md, Roles/_compiled/Builder_compiled.md, Roles/_compiled/Crafter_compiled.md, Roles/_compiled/Curator_compiled.md, Roles/_compiled/Furnisher_compiled.md, Roles/_compiled/GameDesign_compiled.md, Roles/_compiled/Librarian_compiled.md, Roles/_compiled/ScreenWriter_compiled.md, Roles/_compiled/Steward_compiled.md
  - unchanged (nenahrávat): žádný
- `asset_index`: v pořádku (běh 2, 17:45)
  - bez změn přiřazení
- `hubs`: v pořádku (běh 2, 17:45)
  - změněné soubory: 0
- `doc_index`: v pořádku (běh 2, 17:45)
  - index beze změny
- `compose_role`: v pořádku (běh 2, 17:45)
  - změněné kompiláty: 0 z 9
  - changed (nahrát do Claude Projectu): žádný
  - unchanged (nenahrávat): Roles/_compiled/Architect_compiled.md, Roles/_compiled/Builder_compiled.md, Roles/_compiled/Crafter_compiled.md, Roles/_compiled/Curator_compiled.md, Roles/_compiled/Furnisher_compiled.md, Roles/_compiled/GameDesign_compiled.md, Roles/_compiled/Librarian_compiled.md, Roles/_compiled/ScreenWriter_compiled.md, Roles/_compiled/Steward_compiled.md
- `asset_index`: v pořádku (běh 3, 17:48)
  - bez změn přiřazení
- `hubs`: v pořádku (běh 3, 17:48)
  - změněné soubory: 0
- `doc_index`: v pořádku (běh 3, 17:48)
  - index beze změny
- `compose_role`: v pořádku (běh 3, 17:48)
  - změněné kompiláty: 0 z 9
  - changed (nahrát do Claude Projectu): žádný
  - unchanged (nenahrávat): Roles/_compiled/Architect_compiled.md, Roles/_compiled/Builder_compiled.md, Roles/_compiled/Crafter_compiled.md, Roles/_compiled/Curator_compiled.md, Roles/_compiled/Furnisher_compiled.md, Roles/_compiled/GameDesign_compiled.md, Roles/_compiled/Librarian_compiled.md, Roles/_compiled/ScreenWriter_compiled.md, Roles/_compiled/Steward_compiled.md
- Kompiláty changed ve všech bězích (nahrát do Claude Projectu): Roles/_compiled/Architect_compiled.md, Roles/_compiled/Builder_compiled.md, Roles/_compiled/Crafter_compiled.md, Roles/_compiled/Curator_compiled.md, Roles/_compiled/Furnisher_compiled.md, Roles/_compiled/GameDesign_compiled.md, Roles/_compiled/Librarian_compiled.md, Roles/_compiled/ScreenWriter_compiled.md, Roles/_compiled/Steward_compiled.md

### Kontroly (dry-run)
- lint: chyby 0, upozornění 0, informace 4
- audit: chyby 0, upozornění 34, informace 50

### Ruční úkoly
- `update_core:0.26.0:hestia_python_home` (ve frontě): Přepsat hestia_python v Maintenance/config.yaml do tvaru s ~ nebo proměnnou ($HOME), např. ~/hvenv/bin/python (ve VM se domovská složka mění s relací), nebo nastavit proměnnou prostředí HESTIA_PYTHON (má přednost); hodnota s argumenty (uv run …) se nepodporuje. Ověřit doctor (zdroj interpretu) (13 kap. 10.22, CR-039)
- `update_core:0.26.0:cache_gitignore` (ve frontě): Doplnit Maintenance/cache/ do .gitignore instance (mezipaměť poznámek notes.json přijde s core 0.27.0; 13 kap. 10.22)
- `update_core:0.26.0:local_overrides` (ve frontě): Založit Maintenance/local_overrides.md ze šablony _core/templates/tpl_local_overrides.md (prázdná tabulka); v instanci s ručně upraveným chováním Hestie zapsat existující odchylky: lokální modul Roles/modules/<id>.md s overrides: <module_id core> a záznam L-NNNN v registru (vede Steward, bez Stewarda Curator), pak lint a compose_role (13 kap. 10.23, 07 kap. 22)
- `update_core:0.26.0:role_base` (ve frontě): Srovnat profily projektových rolí se základem 0.26.0 (realizace nad neschváleným návrhem (12 kap. 3; zadání 0.29.1, CR-044): tpl_role má v Postupu specifickém pro projekt krok ověřit před realizací validity: valid návrhu, jinak si vyžádat schválení GameDesignera; doplň ho do profilů projektových rolí, které realizují podle návrhu, a srovnej role_base. Lokální náhrada modulu core (overrides:, registr Maintenance/local_overrides.md) mění kompiláty rolí, které modul dostávají (13 kap. 10.23)); po schválení GameDesignerem nastavit role_base: 0.26.0 a spustit compose_role (12 kap. 2.1, 13 kap. 10.6a)

### Základ projektových rolí
- Změna v 0.26.0: realizace nad neschváleným návrhem (12 kap. 3; zadání 0.29.1, CR-044): tpl_role má v Postupu specifickém pro projekt krok ověřit před realizací validity: valid návrhu, jinak si vyžádat schválení GameDesignera; doplň ho do profilů projektových rolí, které realizují podle návrhu, a srovnej role_base. Lokální náhrada modulu core (overrides:, registr Maintenance/local_overrides.md) mění kompiláty rolí, které modul dostávají (13 kap. 10.23)
- Rozdíl `tpl_role`:

```diff
--- tpl_role (starý core)
+++ tpl_role (nový core)
@@ -18,6 +18,7 @@
 ## Co děláš a co ne
 ## Na čem pracuješ (oblast, entity, cesty v projektu)
 ## Postup specifický pro projekt
+- Před realizací (zadání v chatu, předání) ověř, že návrh (`type: design`), podle kterého realizuješ, má `validity: valid`; když ne, vyžádej si schválení GameDesignera dřív, než realizuješ (12 kap. 3, modul `start`).
 ## Vstupy a výstupy
 ## Uzavření tasku
 Podle modulu `task_close`; specifika role (např. co patří do `state`):
```

- Profily nesrovnané se základem 0.26.0 (ruční úkol `role_base`):
  - `Roles/Architect.md`: role_base 0.23.0 je starší než 0.26.0
  - `Roles/Builder.md`: role_base 0.23.0 je starší než 0.26.0
  - `Roles/Crafter.md`: role_base 0.23.0 je starší než 0.26.0
  - `Roles/Furnisher.md`: role_base 0.23.0 je starší než 0.26.0
  - `Roles/GameDesign.md`: role_base 0.23.0 je starší než 0.26.0
  - `Roles/ScreenWriter.md`: role_base 0.25.0 je starší než 0.26.0

### Změny instrukcí
- Změněné soubory: 9. Role si změny vypíše `role_diff <Role>`.

#### `agents/Curator.md` (změněný)
- Sekce: Co děláš a co ne (změněná)

> ## Co děláš a co ne
> Udržuješ strukturu vaultu: metadata, huby, metadata importu v `Inbox/`, lokální taxonomii a vazby na soubory mimo vault. Předzpracování obsahu inboxu (`raw` → `prepared`) dělá Knihovník (05 kap. 3.2a). Auditor navrhuje, ty provádíš, člověk schvaluje větší zásahy.
>
> **Děláš:**
> - doplňuješ a opravuješ frontmatter;
> - zakládáš huby a povyšuješ lehké záznamy;
> - import do `Inbox/` děláš modulem `inbox_import`: zdroj čteš přes konektor do souboru výměny, zápis provede příkaz `inbox_import` (`source`, `source_ref`, kategorie podle `tag_map`), stav ve zdroji měníš až po úspěšném zápisu;
> - připravuješ návrhy (`proposal`: `assign`, `split`, `reparent`, `promote`, `derive`, `rename`);
> - spouštíš `asset_index`, `hubs`, `doc_index` a `compose_role`;
> - zapisuješ do `changes.md` a `structure_log.md`; podněty rolí pro Hestii z `queue.md` (`code: hestia[:<kategorie>]`) převádíš do `structure_log.md` příkazem `feedback_log`;
> - připravuješ change requesty (`export_cr`) jako **náhradník Stewarda**, když v instanci není aktivní (`steward_active: false` v `Maintenance/config.yaml`, výchozí); se Stewardem je `export_cr` jeho (05 kap. 3.2b), ty dál zakládáš obsahové záznamy do `structure_log.md`. Bez Stewarda vedeš i registr lokálních odchylek `Maintenance/local_overrides.md` (záznam po zápisu lokálního modulu s `overrides` na pokyn GameDesignera, stav v místě; 13 kap. 10.23).
>
> **Neděláš:**
> - neměníš obsah designu ani těla dokumentů; neměníš kód, data a `_core/`;
> - nepřesouváš ani nepřejmenováváš bez schválení; nemažeš (jen `_to_delete/`, a to po schválení);
> - nerozhoduješ o `target_*` (jen navrhuješ);
> - neprovádíš vlastní návrhy bez schválení; nearchivuješ scratch.

#### `agents/Steward.md` (změněný)
- Sekce: Co děláš a co ne (změněná), Start protokol (změněná), Postupy podle zakázky (změněná), Zápis do logů (změněná)
- Nové znění: 3795 znaků, nad 3000; přečti sekce v `_core/agents/Steward.md`.

#### `agents/modules/core_update.md` (změněný)
- Sekce: Postup (změněná), Známé pasti (změněná)

> ## Postup
> 1. `doctor`: Python, PyYAML, `core_source`, necommitnuté změny (před `--apply` musí být vault commitnutý).
> 2. Před aktualizací odešli čekající podněty (modul `hearthlore_report`: `feedback_log`, `export_cr`).
> 3. Dry-run `update_core --latest` (na připojené složce `--work-copy`, po fázích `--work-phase copy|run|back`): rozdíl, poznámky z `CHANGELOG.md`, manifest (automatické kroky, ruční úkoly, CR k ověření, *Změny instrukcí*).
> 4. **Lokální odchylky** (oddíl dry-runu; registr `Maintenance/local_overrides.md`): každou vypsanou náhradu modulu core roztřiď podle rozdílu modulu core: platí dál (stav beze změny) / nová verze ji řeší (stav `zrušená`, lokální modul do `_to_delete/` po schválení) / konflikt (stav `konflikt`, otázka GameDesignerovi). `--apply` se zastaví, jen když nahrazovaný modul v nové verzi chybí: rozhodne GameDesigner (nový modul v `overrides`, nebo zrušení náhrady: záznam `zrušená` a lokální modul do `_to_delete/`), pak registr a modul oprav a spusť znovu; přepínač, který zastavení přeskočí, není.
> 5. Hlášení GameDesignerovi: verze od → do, co se změní, ruční úkoly, migrace, roztříděné odchylky; počkej na schválení.
> 6. `update_core --latest --apply` (s `--work-copy`, je-li vault na připojené složce). Selže-li krok, `update_core --after-only --apply`.
> 7. Report `Maintenance/reports/update_core_RRRR-MM-DD.md`: zkontroluj kroky (u opakované fáze jsou výsledky všech běhů s číslem běhu a časem); ruční úkoly jsou ve frontě (`T-…`), projdi je s GameDesignerem a hotové uzavři (`state`, `closed`).
> 8. Kompiláty: do Claude Projectu nahraj kompiláty z řádku *Kompiláty changed ve všech bězích* (sečtené přes opakované běhy); `unchanged` nech. Role se změněným základem: `role_diff <Role>`.
> 9. CR k ověření (`crs` v manifestu) uveď v hlášení pro HearthLore (modul `hearthlore_report`) s výsledkem ověření.

> ## Známé pasti
> - `--apply` bez schválení nebo s necommitnutými změnami.
> - Na připojené složce přechod bez `--work-copy` nestihne limit volání; pracovní adresář z výpisu zadej v dalším volání výslovně.
> - Ruční úkol uzavřít dřív, než je práce hotová a ověřená.
> - Odchylku označit `zrušená` jen proto, že se modul core změnil: nová verze ji řeší, jen když dělá totéž, co lokální modul.

#### `agents/modules/file_safety.md` (změněný)
- Sekce: Postup (změněná), Známé pasti (změněná)

> ## Postup
> 1. Před přepsáním porovnej soubor s verzí, kterou jsi naposledy načetl (obsah nebo hash). Změnil-li ho mezitím někdo jiný, cizí změny slouč; nepřepisuj naslepo.
> 2. Chráněné soubory z pravidel zápisu (`write_rules_local.md`) a `protected_files` v `Maintenance/config.yaml` (např. ruční úpravy z editoru) nepřepisuj.
> 3. Nemaž. Na pokyn soubor přesuň do `_to_delete/`.
> 4. Přesouvej bez přepsání cíle; když cíl existuje, zastav se a zeptej.
> 5. Skripty Hestia spouštěj nejdřív bez `--apply` (dry-run) a zkontroluj výpis; zapisuj s `--apply`.
> 6. Generované sekce (mezi značkami `hestia:generated`) neupravuj ručně; přepíše je skript.
> 7. Do dokumentu s `validity: superseded` nebo `archived` nepiš (tělo); zapiš do nástupce (`superseded_by`), a když chybí, do platného dokumentu entity. Změnu těla nahrazeného dokumentu hlásí `lint` a `task_close` (G5).

> ## Známé pasti
> - Přepsat soubor, který mezitím upravil člověk nebo jiný agent.
> - Přepsat ruční úpravy z editoru, které skript nezná. Vrací se do skriptu, dokud se to nestane, platí stav v enginu.
> - Mazat „nepotřebné“ soubory bez pokynu.
> - Doplnit novinku do nahrazeného dokumentu (katalog, starý návrh) místo do nástupce: mimo evidenci ji nikdo nenajde.

#### `agents/modules/hearthlore_report.md` (změněný)
- Sekce: Postup (změněná)

> ## Postup
> 1. Podněty z fronty: `feedback_log` (dry-run, pak `--apply`); podnět „k ruční opravě“ oprav podle důvodu ve výpisu.
> 2. `export_cr` (dry-run, pak `--apply`): záznamy `structure_log.md` bez `cr`, jeden záznam = jeden CR v `outbox/`; doplň *Dopad* a *Alternativy*. Co CR nebude, označ s člověkem `cr: none`.
> 3. Forma podle obsahu: žádost o změnu Hestie a sdílené know-how = CR; informace o stavu instance (ověřené CR, verze, slabá místa) = hlášení.
> 4. Hlášení `outbox/report_RRRR-MM-DD.md` podle `tpl_report_hearthlore`: *Přehled CR instance* ze `structure_log.md` (sloupec `cr`) a z `outbox/` (připravené, v `outbox/sent/` odeslané); stav v HearthLore neuvádíš. Oddíl *Lokální odchylky* skládej z registru `Maintenance/local_overrides.md`: tabulka `| id | modul core | důvod | CR | stav |` s aktivními záznamy a záznamy v konfliktu (hotovou ji má report `health` pod sekcí lokálních odchylek); pod ni volný text k ostatním lokálním úpravám (prostředí, ruční postupy). HearthLore z ní pozná, co instance potřebuje jinak, i když CR odmítl.
> 5. Odesílá člověk; odeslané soubory přesouvá do `outbox/sent/` on.

#### `agents/modules/instance_health.md` (změněný)
- Sekce: Postup (změněná)

> ## Postup
> 1. `weekly --apply` (vault na připojené složce s `--work-copy`; nestihne-li volání limit, po fázích `--work-phase copy`, `run`, `back` se stejným adresářem), nebo přečti výsledek naplánované úlohy `Maintenance/reports/weekly_RRRR-MM-DD.md`. Samotná kontrola: `health` (s `--apply` report `health_…`). Pomalý běh změř s `--profile` (tabulka kroků do výstupu a reportu).
> 2. U každé sekce `pozor` (prostředí, verze core, kompiláty, ruční úkoly, podněty, outbox, Unreal, lokální odchylky) vylož, co nález znamená, a navrhni krok z reportu.
> 3. **Lokální odchylky:** G6 náhrad (lokální modul s `overrides` bez platného záznamu `aktivní`/`konflikt` v `Maintenance/local_overrides.md`, i se záznamem `zrušená`; platný záznam bez modulu, `overrides` na modul, který core nemá) srovnej s GameDesignerem: chybějící záznam doplň, zrušenou náhradu přesuň do `_to_delete/` po schválení. Konflikty po aktualizaci core (stav `konflikt`) připomeň GameDesignerovi k rozhodnutí.
> 4. Nálezy auditu: počty proti minulému týdnu; chyby G6, G7 a upozornění předej rolím, které je vlastní (úkol ve frontě `code: role:<Role>`), obsah sám neopravuj.
> 5. Hlášení GameDesignerovi: co je v pořádku, co čeká, doporučené kroky; zásah až po schválení.

#### `agents/modules/start.md` (změněný)
- Sekce: Postup (změněná), Známé pasti (změněná)
- Nové znění: 5117 znaků, nad 3000; přečti sekce v `_core/agents/modules/start.md`.

#### `agents/write_rules.md` (změněný)
- Sekce: Zásady zápisu (změněná), Steward (05 kap. 3.2b) (změněná)

> ## Zásady zápisu
>
> - Platný text přepisuješ jen jako důsledek rozhodnutí GameDesignera nebo výsledku tasku ve své oblasti (12 kap. 6.1, `nahradit:`).
> - Profil kontrakt zpřísňuje, neruší: výsledek své práce zapíšeš do vaultu vždy; zákazy zápisu v profilu platí pro kód, data a assety (12 kap. 2.1).
> - Zápis do `Docs/` je dokumentace domény podle šablony (sekce, `depth`), ne výstup role: neříká, kdo psal a pro koho. Před zápisem najdi existující dokumentaci entity a doplň ji; nový dokument jen když žádný není. Předání (`Handovers/`) píšeš z role (12 kap. 8).
> - Do dokumentu s `validity: superseded` nebo `archived` nepiš; zapiš do nástupce (`superseded_by`). Změnu těla nahrazeného dokumentu hlásí `lint` a `task_close` (G5).
> - Přesun a přejmenování jen se schválením; mazání jen přesunem do `_to_delete/` na pokyn (05 kap. 5).
> - Problém s Hestií jako nástrojem neřešíš CR ani zápisem do `structure_log.md`: modul `hestia_feedback` (12 kap. 4.5).

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
> | `local_overrides.md` (registr lokálních náhrad modulů core) | ✔ připisovat záznamy, stav v místě; bez Stewarda vede Curator |
> | Obsah (`Docs/`, huby, `depth_*`, `target_*`, `KnowHow/`, `Handovers/`, `Inbox/`, `Scratch/`) | ✘ |

#### `templates/tpl_role.md` (změněný)
- Sekce: Postup specifický pro projekt (změněná)

> ## Postup specifický pro projekt
> - Před realizací (zadání v chatu, předání) ověř, že návrh (`type: design`), podle kterého realizuješ, má `validity: valid`; když ne, vyžádej si schválení GameDesignera dřív, než realizuješ (12 kap. 3, modul `start`).

#### Role a soubory
- Architect: `agents/modules/file_safety.md`, `agents/modules/start.md`, `agents/write_rules.md`, `templates/tpl_role.md`
- Builder: `agents/modules/file_safety.md`, `agents/modules/start.md`, `agents/write_rules.md`, `templates/tpl_role.md`
- Crafter: `agents/modules/file_safety.md`, `agents/modules/start.md`, `agents/write_rules.md`, `templates/tpl_role.md`
- Furnisher: `agents/modules/file_safety.md`, `agents/modules/start.md`, `agents/write_rules.md`, `templates/tpl_role.md`
- GameDesign: `agents/modules/file_safety.md`, `agents/modules/start.md`, `agents/write_rules.md`, `templates/tpl_role.md`
- ScreenWriter: `agents/modules/file_safety.md`, `agents/modules/start.md`, `agents/write_rules.md`, `templates/tpl_role.md`
- Curator: `agents/Curator.md`, `agents/modules/file_safety.md`, `agents/modules/start.md`, `agents/write_rules.md`
- Auditor: `agents/modules/file_safety.md`, `agents/modules/start.md`, `agents/write_rules.md`
- Librarian: `agents/modules/file_safety.md`, `agents/modules/start.md`, `agents/write_rules.md`

### CR k ověření
- CR-033_vykon_pripojena_slozka (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-037_manifest_assetu_tabulky_a_data (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-039_start_cesta_a_interpret (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-041_report_update_core_a_kompilat_stewarda (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-042_zapis_do_nahrazeneho_dokumentu (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-043_lint_taxonomy_local (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-044_realizace_nad_neschvalenym_navrhem (ověřit v instanci, do *Průběhu* `in_pilot`)

<!-- hestia:runs {"run": 3, "steps": [{"step": "asset_index", "ok": true, "code": 0, "message": "", "details": ["bez změn přiřazení"], "run": 1, "time": "17:43"}, {"step": "hubs", "ok": true, "code": 0, "message": "", "details": ["změněné soubory: 10"], "run": 1, "time": "17:43"}, {"step": "doc_index", "ok": true, "code": 0, "message": "", "details": ["index beze změny"], "run": 1, "time": "17:43"}, {"step": "compose_role", "ok": true, "code": 0, "message": "", "details": ["změněné kompiláty: 9 z 9", "changed (nahrát do Claude Projectu): Roles/_compiled/Architect_compiled.md, Roles/_compiled/Builder_compiled.md, Roles/_compiled/Crafter_compiled.md, Roles/_compiled/Curator_compiled.md, Roles/_compiled/Furnisher_compiled.md, Roles/_compiled/GameDesign_compiled.md, Roles/_compiled/Librarian_compiled.md, Roles/_compiled/ScreenWriter_compiled.md, Roles/_compiled/Steward_compiled.md", "unchanged (nenahrávat): žádný"], "run": 1, "time": "17:43", "changed": ["Roles/_compiled/Architect_compiled.md", "Roles/_compiled/Builder_compiled.md", "Roles/_compiled/Crafter_compiled.md", "Roles/_compiled/Curator_compiled.md", "Roles/_compiled/Furnisher_compiled.md", "Roles/_compiled/GameDesign_compiled.md", "Roles/_compiled/Librarian_compiled.md", "Roles/_compiled/ScreenWriter_compiled.md", "Roles/_compiled/Steward_compiled.md"], "unchanged": []}, {"step": "asset_index", "ok": true, "code": 0, "message": "", "details": ["bez změn přiřazení"], "run": 2, "time": "17:45"}, {"step": "hubs", "ok": true, "code": 0, "message": "", "details": ["změněné soubory: 0"], "run": 2, "time": "17:45"}, {"step": "doc_index", "ok": true, "code": 0, "message": "", "details": ["index beze změny"], "run": 2, "time": "17:45"}, {"step": "compose_role", "ok": true, "code": 0, "message": "", "details": ["změněné kompiláty: 0 z 9", "changed (nahrát do Claude Projectu): žádný", "unchanged (nenahrávat): Roles/_compiled/Architect_compiled.md, Roles/_compiled/Builder_compiled.md, Roles/_compiled/Crafter_compiled.md, Roles/_compiled/Curator_compiled.md, Roles/_compiled/Furnisher_compiled.md, Roles/_compiled/GameDesign_compiled.md, Roles/_compiled/Librarian_compiled.md, Roles/_compiled/ScreenWriter_compiled.md, Roles/_compiled/Steward_compiled.md"], "run": 2, "time": "17:45", "changed": [], "unchanged": ["Roles/_compiled/Architect_compiled.md", "Roles/_compiled/Builder_compiled.md", "Roles/_compiled/Crafter_compiled.md", "Roles/_compiled/Curator_compiled.md", "Roles/_compiled/Furnisher_compiled.md", "Roles/_compiled/GameDesign_compiled.md", "Roles/_compiled/Librarian_compiled.md", "Roles/_compiled/ScreenWriter_compiled.md", "Roles/_compiled/Steward_compiled.md"]}, {"step": "asset_index", "ok": true, "code": 0, "message": "", "details": ["bez změn přiřazení"], "run": 3, "time": "17:48"}, {"step": "hubs", "ok": true, "code": 0, "message": "", "details": ["změněné soubory: 0"], "run": 3, "time": "17:48"}, {"step": "doc_index", "ok": true, "code": 0, "message": "", "details": ["index beze změny"], "run": 3, "time": "17:48"}, {"step": "compose_role", "ok": true, "code": 0, "message": "", "details": ["změněné kompiláty: 0 z 9", "changed (nahrát do Claude Projectu): žádný", "unchanged (nenahrávat): Roles/_compiled/Architect_compiled.md, Roles/_compiled/Builder_compiled.md, Roles/_compiled/Crafter_compiled.md, Roles/_compiled/Curator_compiled.md, Roles/_compiled/Furnisher_compiled.md, Roles/_compiled/GameDesign_compiled.md, Roles/_compiled/Librarian_compiled.md, Roles/_compiled/ScreenWriter_compiled.md, Roles/_compiled/Steward_compiled.md"], "run": 3, "time": "17:48", "changed": [], "unchanged": ["Roles/_compiled/Architect_compiled.md", "Roles/_compiled/Builder_compiled.md", "Roles/_compiled/Crafter_compiled.md", "Roles/_compiled/Curator_compiled.md", "Roles/_compiled/Furnisher_compiled.md", "Roles/_compiled/GameDesign_compiled.md", "Roles/_compiled/Librarian_compiled.md", "Roles/_compiled/ScreenWriter_compiled.md", "Roles/_compiled/Steward_compiled.md"]}]} -->

### Pracovní kopie
- Pracovní adresář: `/sessions/rcw-01nw4mxpuk2thvsg4ues1vms/hestia_work_p23`.
- Kontrola originálu: beze změny od snímku (2225 souborů).
- Přeneseno: změněné 24, nové 1, přesunuté 0; `_core/` vyměněn (starý v `_to_delete/_core_0.25.0/`).
  - ~ `Assets/stone/SM_RuinAshlar.md`
  - ~ `Assets/stone/SM_RuinDressed_R12_A.md`
  - ~ `Assets/stone/SM_RuinStone_R12_A.md`
  - ~ `Assets/stone/SM_RuinStone_W_R12_A.md`
  - ~ `Assets/wood/SM_RuinPlank_A.md`
  - ~ `Assets/wood/SM_RuinPost_A.md`
  - ~ `Assets/wood/SM_RuinTimber_A.md`
  - ~ `Entities/Cinematics_Lapikus.md`
  - ~ `Maintenance/asset_index.json`
  - ~ `Maintenance/asset_index.md`
  - ~ `Maintenance/doc_index.json`
  - ~ `Maintenance/doc_index_text.json`
  - ~ `Maintenance/queue.md`
  - ~ `Maintenance/structure_version.md`
  - ~ `Roles/_compiled/Architect_compiled.md`
  - ~ `Roles/_compiled/Builder_compiled.md`
  - ~ `Roles/_compiled/Crafter_compiled.md`
  - ~ `Roles/_compiled/Curator_compiled.md`
  - ~ `Roles/_compiled/Furnisher_compiled.md`
  - ~ `Roles/_compiled/GameDesign_compiled.md`
  - ~ `Roles/_compiled/Librarian_compiled.md`
  - ~ `Roles/_compiled/ScreenWriter_compiled.md`
  - ~ `Roles/_compiled/Steward_compiled.md`
  - ~ `Steps/cinematics.md`
  - + `Maintenance/reports/update_core_2026-11-26.md`
- Čas fází: kopie 117.7 s, přechod 1.2 s, zápis zpět 106.8 s.
