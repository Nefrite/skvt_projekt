# Hestia (core)

*Hestia custodit, ut Fabula fiat Mundus.*

Core nástroje Hestia. Tato složka je **jediná část repozitáře, která se přenáší do prototypů**, kde je jako modul `Hestia/_core/` (zadání 02, `hearthlore/zadani/02_struktura_vaultu.md`).

**Stav:** fáze 1 akceptovaná (taxonomie, šablony, šablona vaultu, `init`, `lint` v rozsahu fáze 1), fáze 2 akceptovaná (kontrakt, moduly, profily Curator a Auditor, `compose_role`), fáze 3 akceptovaná (`lint`, `asset_index`, `hubs`, `audit`, `task_close`, `frontmatter`, `update_core`, `init --no-game-layer`). Souběžně s pilotem: `export_cr` (0.4.0), srovnání se zadáním 0.11.2 (0.4.1), pohledy pro Q1 ve variantě Bases i Dataview (0.5.0), varianta skript pro matici a mapu a manifest pohledů (0.6.0), zátěžový test a snippety pro skrytí složek (0.7.0), srovnání snippetů v `update_core` (0.7.1), migrační mapa podle CR z pilotu (0.8.0), šablona kroku s volitelnou historií (0.8.1), návrh a realizace: režim cíle, hloubka návrhu, G13 (0.9.0), dokument u všech entit a povinný `target_mode` lokální domény (0.9.1), převod odkazů při migraci: aliasy, cesty od kořene prototypu, obrázky (0.10.0), zmínky souborů v backtickách (0.10.1), cíl zmínek jen soubory přesunuté mapou (0.10.2), jména rolí ve zkušebním projektu anglicky a tematický seznam pastí v šabloně know-how (0.10.3), `asset_index` s pravidlem `alias` a výpisem změn přiřazení (0.11.0), role Knihovník: profil, moduly, `doc_index`, `compose_context`, `lint --draft`, glosář, sekce v auditu (0.12.0), Unreal etapa 1 (`hestia_ue.py`, `ue_query`, blok `## Stav v UE`) a `compile: listed` u modulů (0.13.0), snadná aktualizace core: `update_core --tag` / `--latest`, manifest `upgrade.yaml`, kroky po aktualizaci (0.14.0), oprava upozornění na staré kompiláty (0.14.1), `compose_role` po každé změně verze (0.14.2), report `update_core` s oddílem na přechod a společné argumenty před příkazem (0.14.3), režim agenta podle přístupu k vaultu a přenosný čtecí skript Unrealu (0.14.4), import do inboxu `inbox_import` se souborem výměny a převodníkem Notion (0.15.0), základ projektových rolí: `role_base`, příznak `roles` v manifestu, G5 u nesrovnaného profilu (0.16.0), věrný převod Notion v `inbox_import`, podněty rolí přes `queue.md`, Knihovník uzavírá zápis `task_close` (0.17.0), čtení Unrealu proti `state`: G10 a šablona `state` (0.18.0), rozdělení kontraktu L0: zásady zápisu ve `write_rules.md`, modul `hestia_feedback` (0.19.0), čtecí nástroje `section`, `find`, `agenda`, `role_diff`, oddíl *Změny instrukcí* v reportu `update_core`, `compose_role` changed/unchanged, `## Souhrn` a G14 (0.20.0), Změny instrukcí bez zálohy starého core a `role_diff` „nelze určit“ (0.20.1), `update_core --work-copy`, kontrola prostředí a `doctor`, `feedback_log`, vyplněné `cr` jen `cr: <ID>` / `cr: none`, `placeholder_ignore` a druh `ism` v reportu z UE (0.21.0), `update_core --after-only --work-copy`, rozsah z geometrie a `pivot_far` v reportu z UE, poznámka o předání v `export_cr` (0.21.1), karty assetů (typ `asset`, `lint` podle stavu, `agenda`, blok `## Assety`, moduly `asset_request` a `asset_work`), úkoly pro role ve frontě (`code: role:<Role>`, `agenda`, G5), `importlib.reload` a `format_version` ve čtení Unrealu, `dopad:` ve `feedback_log` (0.22.0), assety z kódu a z Unrealu: manifest `asset_sources.yaml`, sekce `library` v `asset_index`, bloky *Z kódu* a *Stav v UE* v kartách, `ue_query --assets`, G15, souhrn v `## Assety` (0.23.0), zralost nad jednotkami podstromu a matice u rodičů, hloubka návrhu z `concept` (0.24.0), role Steward, `health` a `weekly` (fáze 11), výkon na připojené složce (`doc_index` s mezipamětí textu, `task_close --resume`), kompiláty jen při změně obsahu, manifest assetů s pevnou kategorií a zdrojem `files`, `doctor` s návrhem interpretu (0.25.0); `--profile` a průběžný výstup kroků, `task_close --resume` po souborech, `weekly --work-phase`, lokální odchylky (`overrides:`, registr `local_overrides.md`), G5 u nahrazeného dokumentu a stavu nad návrhem `draft`, `lint` lokální taxonomie, `hestia_python` s `~` a `HESTIA_PYTHON` (0.26.0). Vývoj řídí aktivní předání vývoje core v `hearthlore/Handovers/` (nyní `predani_vyvoj_core_soubeh.md`; fáze 1–3 v `_archive/predani_vyvoj_core_f1-3.md`). Technický základ: `hearthlore/zadani/13_technicky_zaklad.md`. Verze core: **0.26.0** ([CHANGELOG](CHANGELOG.md)).

## Prostředí

Core potřebuje **Python ≥ 3.11** a **PyYAML** (13 kap. 1). `hestia.py` obojí ověří při startu dřív, než cokoli importuje, a při chybě vypíše návod (kód 2). Úplnou kontrolu dělá `hestia.py doctor`: Python a PyYAML, git, vault a právo zápisu, `core_source` a jeho značky proti `_core/VERSION`, na Linuxu připojená složka (13 kap. 10.15). V novém prostředí (nový chat, nová VM) ho spusť před prvním skriptem (modul `start`).

- **Windows:** Python z python.org nebo `py -3.12`; `py -3.12 -m pip install pyyaml`, nebo prostředí `py -3.12 -m venv %USERPROFILE%\venv311` a `%USERPROFILE%\venv311\Scripts\pip install pyyaml`.
- **Linux:** `python3.11 -m venv $HOME/venv311 && $HOME/venv311/bin/pip install pyyaml`, nebo přes `uv`: `uv venv --python 3.12 $HOME/venv311 && uv pip install --python $HOME/venv311 pyyaml`.
- **VM desktopové aplikace** (agent v chatu s připojenou složkou): prostředí zakládej mimo projekt a vault (např. `$HOME/venv311`, přes `uv` jako výše), ne v připojené složce. Vault na připojené složce (`fuse`, `9p`, `virtiofs`, `cifs` …) je pomalý; `doctor` to ohlásí a dlouhé běhy `update_core` spouštěj s `--work-copy --apply` (přechod v lokální kopii, zápis zpět bez mazání; po fázích `--work-phase copy|run|back`, když se běh nevejde do limitu jednoho volání).

## Použití

```text
python hestia/scripts/hestia.py init --vault <Projekt>/Hestia --prototype Lapikus --root Lapikus_Region --engine-version 5.8          # dry-run
python hestia/scripts/hestia.py init --vault <Projekt>/Hestia --prototype Lapikus --root Lapikus_Region --engine-version 5.8 --apply
python hestia/scripts/hestia.py init --vault <Projekt>/Hestia --no-game-layer --apply           # instance bez herní vrstvy
python <Projekt>/Hestia/_core/scripts/hestia.py lint [soubory…] [--all] [--json]       # bez argumentů: změněné podle gitu
python <Projekt>/Hestia/_core/scripts/hestia.py lint --draft <koncept.md|-> --as <cesta ve vaultu>   # kontrola konceptu, nic nezapíše
python <Projekt>/Hestia/_core/scripts/hestia.py compose_role [Role…] [--apply]       # kompilát pro chat Roles/_compiled/<Role>_compiled.md
python <Projekt>/Hestia/_core/scripts/hestia.py asset_index [--apply]                # Maintenance/asset_index.md + .json
python <Projekt>/Hestia/_core/scripts/hestia.py doc_index [--apply]                  # Maintenance/doc_index.json (index dokumentů, Knihovník)
python <Projekt>/Hestia/_core/scripts/hestia.py compose_context (--entity E | --topic T | --query "…") [--apply]   # Maintenance/context/<id>_context.md
python <Projekt>/Hestia/_core/scripts/hestia.py hubs [Entita…] [--apply]             # generované sekce hubů, kroků, Dashboard/Index.md
python <Projekt>/Hestia/_core/scripts/hestia.py audit [--baseline reports/audit_….json] [--apply]   # report, fronta, stav
python <Projekt>/Hestia/_core/scripts/hestia.py task_close --role R --source S --note "…" [--change E="…"] [--entity E] [--archive-handover P] [--apply]
python <Projekt>/Hestia/_core/scripts/hestia.py task_close --resume      # pokračuje prvním nezpracovaným krokem nebo souborem (task_close_seconds)
python <Projekt>/Hestia/_core/scripts/hestia.py section <dokument> [--list | "<nadpis>" …]   # osnova nebo sekce s čísly řádků (z doc_index)
python <Projekt>/Hestia/_core/scripts/hestia.py find "<dotaz>" [--text] [--type T] [--entity E] [--for-role R]   # index + mezipaměť textu
python <Projekt>/Hestia/_core/scripts/hestia.py frontmatter --map migrace.yaml [--move] [--force] [--apply]
python <Projekt>/Hestia/_core/scripts/hestia.py ue_query --emit (--entity E | --all) [--apply]   # čtecí skript do Maintenance/ue/ (spustí se v editoru)
python <Projekt>/Hestia/_core/scripts/hestia.py ue_query --import [výsledek] [--entity E | --all] [--apply]   # Maintenance/reports/ue_<entita>.json
python <Projekt>/Hestia/_core/scripts/hestia.py ue_query --assets --emit [--category K] [--asset A] [--all-library] [--apply]   # čtení knihovních assetů
python <Projekt>/Hestia/_core/scripts/hestia.py ue_query --import --assets [--apply]   # Maintenance/reports/ue_assets.json (current / outdated / missing)
python <Projekt>/Hestia/_core/scripts/hestia.py inbox_import --from Maintenance/import/<zdroj>_RRRR-MM-DD.json [--apply]   # scratch do Inbox/ (soubor výměny zapíše agent, modul inbox_import)
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --latest [--apply]          # nejvyšší značka core vX.Y.Z z core_source (config.yaml)
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --tag vX.Y.Z [--apply]      # konkrétní značka; --no-after: kroky po aktualizaci jen vypsat
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --from <cesta k hestia/> [--with-views] [--apply]   # záloha; --with-views: chybějící pohledy do Dashboard/views/
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --after-only [--apply]      # jen kroky po aktualizaci (po selhání kroku nebo přerušení)
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --latest --work-copy [<adresář>] [--work-phase copy|run|back] [--keep-work-copy] --apply   # vault na připojené složce
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --after-only --work-copy [<adresář>] --apply   # zbývající kroky po aktualizaci přes pracovní kopii
python <Projekt>/Hestia/_core/scripts/hestia.py agenda [--role <Role>] [--json]           # co čeká na roli: předání, úkoly z fronty, karty assetů; bez --role úkoly všech rolí
python <Projekt>/Hestia/_core/scripts/hestia.py doctor [--json]                         # kontrola prostředí, nic nezapisuje
python <Projekt>/Hestia/_core/scripts/hestia.py health [--apply] [--json]               # zdraví instance; s --apply report reports/health_RRRR-MM-DD.md
python <Projekt>/Hestia/_core/scripts/hestia.py weekly [--work-copy [<adresář>] [--work-phase copy|run|back]] [--apply]   # týdenní běh: doc_index, asset_index, hubs, audit, health
python <Projekt>/Hestia/_core/scripts/hestia.py <příkaz> … --profile                   # tabulka kroků (čas, stat, výpisy adresářů, čtení, zápisy) na konec výstupu
python <Projekt>/Hestia/_core/scripts/hestia.py feedback_log [--id P-0001] [--category P-0001=missing] [--apply]   # podněty code: hestia → structure_log.md
python <Projekt>/Hestia/_core/scripts/hestia.py export_cr [--area A] [--include-works] [--apply]   # structure_log → Maintenance/outbox/CR_….md
```

Společné argumenty (`--vault`, `--apply`, `--force`, `--json`, `--quiet`, `--profile`) platí před příkazem i za ním (13 kap. 3).

**Měření a průběh** (13 kap. 10.22, zadání 0.29): `--profile` vypíše na konec výstupu tabulku kroků (načtení konfigurace a taxonomie, průchod vaultu, kroky příkazu, celkem) s časem a počty `stat`, výpisů adresářů (volání a položky), čtení a zápisů; u `--json` na stderr, s `--apply` i na konec reportu příkazu. Podprocesy (`weekly`, kroky `update_core`) `--profile` zdědí a jejich kroky jsou v tabulce vnořeně (`↳`). Výsledek příkazu se nemění. Dlouhé příkazy (`task_close`, `weekly`, `update_core`, `audit`, `hubs`, `doc_index`) vypisují začátek a konec každého kroku hned na stderr, takže přerušené volání ukáže, kde skončilo (`--quiet` výpis vypne). `task_close` hlídá `task_close_seconds` i po každém souboru v krocích `writes` a `checks`; `task_close --resume` pokračuje prvním nezpracovaným souborem. `weekly --work-copy` jde po fázích jako `update_core` (`--work-phase copy|run|back`, další volání pokračuje od nedokončené fáze).

**Lokální odchylky** (13 kap. 10.23, zadání 0.29): změna chování Hestie jen pro instanci je lokální modul `Roles/modules/<id>.md` s `overrides: <module_id core>`; `compose_role` ho vloží do kompilátů místo modulu core, `_core/` se ručně nemění nikdy. Každá náhrada má záznam v registru `Maintenance/local_overrides.md` (šablona `templates/tpl_local_overrides.md`; vede Steward, bez Stewarda Curator); nesoulad hlásí `lint` jako G6, `health` počty a konflikty, `update_core` v dry-runu náhrady, jejichž modul core nová verze mění. Kontrakt nahradit nejde.

Čtení Unrealu bez otevřeného editoru (záloha, 13 kap. 10.11): vygenerovaný skript jde spustit i `UnrealEditor-Cmd <projekt>.uproject -run=pythonscript -script=<Hestia>/Maintenance/ue/ue_query_<id>.py`, pak `ue_query --import`; core to sám nespouští. Kostra toolsetu pro Unreal MCP (etapa 2, neověřená): `templates/unreal/init_unreal.py`.

**Aktualizace core v instanci** (13 kap. 10.6, 11 kap. 6): do `Maintenance/config.yaml` patří `core_source` (cesta k repozitáři HearthLore relativně k vaultu, např. `"../../../HearthLore"`). `update_core --latest` vezme `hestia/` nejvyšší značky `vX.Y.Z` přes `git archive` (nikdy větev ani pracovní strom). Dry-run ukáže rozdíl, poznámky z `CHANGELOG.md` a sečtený manifest `upgrade.yaml` (automatické kroky, ruční úkoly, CR k ověření). `--apply` vymění `_core/` a novým core spustí `asset_index` → `hubs` → `doc_index` → `compose_role` (podle manifestu; `compose_role` při každé změně verze, jsou-li ve vaultu kompiláty), pak `lint --all` a `audit` v dry-run; ruční úkoly zapíše do `queue.md` (`T-…`, bez duplicit). Report `Maintenance/reports/update_core_RRRR-MM-DD.md` má na každý přechod oddíl `## Přechod <stará> → <nová>` (další přechod téhož dne se připíše) se stavem, výsledky kroků (u `asset_index` změny přiřazení) a ručními úkoly; oddíl vznikne hned po výměně `_core/` a doplňuje se po krocích, průběh jde hned na stderr. Dry-run ohlásí nedokončený přechod; doběhne `update_core --after-only --apply`, který oddíl doplní. Selže-li krok, `_core/` zůstává nový a zbytek doběhne `update_core --after-only --apply`. **Přechod z verze bez `--tag` (do 0.13.0)** jde jednou postaru, skriptem nové verze z pracovní kopie značky: `git worktree add --detach ../hestia-vX.Y.Z vX.Y.Z`, pak `python -I ../hestia-vX.Y.Z/hestia/scripts/hestia.py update_core --vault <Projekt>/Hestia --from ../hestia-vX.Y.Z/hestia [--apply]`. **Vault na připojené složce** (zadání 0.22): `update_core … --work-copy --apply` zkopíruje vault do lokálního adresáře se snímkem originálu, přechod proběhne v kopii a zapíše se zpět bez mazání (změněné soubory na místě, `_core/` dvěma přejmenováními, zmizelé do `_to_delete/`); změnil-li se mezitím originál, nezapíše nic (kód 1). Pracovní adresář se vypíše hned na začátku; další volání ho má zadat výslovně. Zbývající kroky po aktualizaci (selhaný krok) doběhnou `update_core --after-only --work-copy --apply`. První přechod na verzi s `--work-copy` jde skriptem nové verze s `--from` (na připojené složce verze přes `git archive` do lokálního adresáře). Oddíl přechodu v reportu má `### Pracovní kopie` s přenesenými soubory a časy fází. Vývojář přidává s každou vydanou verzí záznam do `upgrade.yaml` (i prázdný; test úplnosti proti `CHANGELOG.md`).

**Naplánovaná úloha `weekly`** (fáze 11, 13 kap. 10.20): core dodá jen příkaz; nastavení je ruční úkol a rozhodnutí GameDesignera. Úloha volá `weekly --apply` s pevnou cestou k interpretu z `hestia_python` (`config.yaml`; smí obsahovat `~` a `$PROMĚNNÉ`, např. `~/hvenv/bin/python` ve VM, kde se domovská složka mění s relací; proměnná prostředí `HESTIA_PYTHON` má přednost; hodnota s argumenty jako `uv run …` se nepodporuje, `doctor` ji hlásí jako chybu), nad vaultem na připojené složce s `--work-copy`. Výsledek je `Maintenance/reports/weekly_RRRR-MM-DD.md` (odkazy na audit a `health`, nálezy proti minulému týdnu, doporučené kroky); obsah vaultu se nemění.

- **Claude (naplánovaný úkol):** úkol s pokynem „spusť `<hestia_python> <Projekt>/Hestia/_core/scripts/hestia.py weekly --apply` a výsledek ohlas podle modulu `instance_health`“, týdně.
- **Linux (cron):** `0 6 * * 1 <hestia_python> <Projekt>/Hestia/_core/scripts/hestia.py weekly --vault <Projekt>/Hestia --apply --quiet`.
- **Windows (Plánovač úloh):** `schtasks /Create /SC WEEKLY /D MON /ST 06:00 /TN HestiaWeekly /TR "\"<hestia_python>\" \"<Projekt>\Hestia\_core\scripts\hestia.py\" weekly --vault \"<Projekt>\Hestia\" --apply --quiet"`.

Bez Stewarda (`steward_active: false`) spouští `weekly` člověk; `health` hlásí, co čeká, v obou případech.

**Pokyny první zprávy agenta** (CR-039, 13 kap. 10.21; doplň cesty instance):

```text
Vault: <cesta k Hestia/>  (nejdřív ověř přístup: ls <cesta>; pak čti)
Interpret: <hestia_python>  (Python ≥ 3.11 s PyYAML, cesta přes ~ např. ~/hvenv/bin/python; příkazy core: <hestia_python> <cesta>/_core/scripts/hestia.py …)
Role: <Role>; postupuj podle CONTRACT.md a modulu start.
```

Bez `--apply` vždy dry-run (nic nezapíše). Proměnná prostředí `HESTIA_TODAY=RRRR-MM-DD` pevně nastaví dnešní datum (testy, kontrola před vydáním).

Testy a zkušební projekt jsou mimo distribuovaný core, v `hearthlore/tests/`; spuštění z kořene repozitáře: `python -m unittest discover -s hearthlore/tests`.

## Obsah

| Složka / soubor | Obsah | Fáze |
|---|---|---|
| `VERSION`, `CHANGELOG.md` | verze `MAJOR.MINOR.PATCH`, migrační poznámky u MAJOR (zadání 11, kap. 5) | 1 |
| `upgrade.yaml` | manifest kroků po aktualizaci pro instance: automatické kroky, ruční úkoly, CR k ověření, záznam u každé verze (zadání 13, kap. 10.6a) | 0.14.0 |
| `taxonomy/` | domény, kategorie, `kind` a očekávané domény, typy, validace, výchozí šablony kroků (YAML); `views.yaml` = manifest pohledů s příznakem herní vrstvy | 1 |
| `templates/` | šablony poznámek (zadání 07): hub, doménový dokument, stav, scratch, crosscut, rozhodnutí, report, CR, profil role, know-how, modul, předání, krok, master lore | 1 |
| `vault_template/` | prázdná struktura `Hestia/` pro nový prototyp, výchozí `.obsidian`, pohledy (`Dashboard/views/bases/*.base`, `dataview/dv_*.md`, `generated/*.md`; do rozhodnutí Q1 všechny varianty; `local/` pro vlastní pohledy instance), vstupní soubor `entrypoint.md`, kostra master lore | 1 |
| `agents/` | `CONTRACT.md` (L0), `modules/` (L1), profily `Curator.md`, `Auditor.md`, `Librarian.md`, `Steward.md`, výchozí `write_rules`, `review_plan` (zadání 12) | 2 |
| `scripts/` | `hestia.py` + balíček `hestia_lib/`: `init` (fáze 1), `compose_role` (2), `lint`, `frontmatter`, `asset_index`, `hubs`, `audit`, `task_close`, `update_core` (3), `export_cr`, `doc_index`, `compose_context`, `ue_query`, `inbox_import`, `health`, `weekly` (souběh s pilotem); `hestia_ue.py` = čtecí modul pro Python v Unrealu (bez `hestia_lib`) (zadání 13, kap. 3); `migrations/` pro migrace MAJOR verzí (kostra) | 1–3 |

## Skrytí `_core/` a `Maintenance/` ve stromu souborů (volitelné)

Snippety `.obsidian/snippets/hestia-hide-core.css` a `hestia-hide-maintenance.css` jsou ve výchozím stavu vypnuté. Zapnutí je osobní volba: *Nastavení → Vzhled → Úryvky CSS*. Nové instance je dostanou z `init`, existující z `update_core`. Ten snippety `hestia-*.css` srovná s core při každém běhu (doplní, přepíše změněné, odebrané přesune do `_to_delete/`), zapnutí nemění. Předpona `hestia-` znamená, že soubor patří core; vlastní úpravu ulož jako snippet pod jiným jménem. Verzují se jen snippety `hestia-*.css` (výjimka v `.gitignore`), ostatní snippety a `appearance.json` zůstávají osobní.

## Pravidla

- Do `hestia/` zapisuje vývojář core podle aktivního předání, agent HearthLore (nebo člověk) po schválení změny ze zadání.
- Každá změna zvýší verzi a zapíše se do changelogu.
- Modul v prototypu core nemění; odchylky a poznatky posílá jako change request do `hearthlore/change-requests/`.
