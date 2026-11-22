# Hestia (core)

*Hestia custodit, ut Fabula fiat Mundus.*

Core nástroje Hestia. Tato složka je **jediná část repozitáře, která se přenáší do prototypů**, kde je jako modul `Hestia/_core/` (zadání 02, `hearthlore/zadani/02_struktura_vaultu.md`).

**Stav:** fáze 1 akceptovaná (taxonomie, šablony, šablona vaultu, `init`, `lint` v rozsahu fáze 1), fáze 2 akceptovaná (kontrakt, moduly, profily Curator a Auditor, `compose_role`), fáze 3 akceptovaná (`lint`, `asset_index`, `hubs`, `audit`, `task_close`, `frontmatter`, `update_core`, `init --no-game-layer`). Souběžně s pilotem: `export_cr` (0.4.0), srovnání se zadáním 0.11.2 (0.4.1), pohledy pro Q1 ve variantě Bases i Dataview (0.5.0), varianta skript pro matici a mapu a manifest pohledů (0.6.0), zátěžový test a snippety pro skrytí složek (0.7.0), srovnání snippetů v `update_core` (0.7.1), migrační mapa podle CR z pilotu (0.8.0), šablona kroku s volitelnou historií (0.8.1), návrh a realizace: režim cíle, hloubka návrhu, G13 (0.9.0), dokument u všech entit a povinný `target_mode` lokální domény (0.9.1), převod odkazů při migraci: aliasy, cesty od kořene prototypu, obrázky (0.10.0), zmínky souborů v backtickách (0.10.1), cíl zmínek jen soubory přesunuté mapou (0.10.2), jména rolí ve zkušebním projektu anglicky a tematický seznam pastí v šabloně know-how (0.10.3), `asset_index` s pravidlem `alias` a výpisem změn přiřazení (0.11.0), role Knihovník: profil, moduly, `doc_index`, `compose_context`, `lint --draft`, glosář, sekce v auditu (0.12.0), Unreal etapa 1 (`hestia_ue.py`, `ue_query`, blok `## Stav v UE`) a `compile: listed` u modulů (0.13.0), snadná aktualizace core: `update_core --tag` / `--latest`, manifest `upgrade.yaml`, kroky po aktualizaci (0.14.0), oprava upozornění na staré kompiláty (0.14.1), `compose_role` po každé změně verze (0.14.2), report `update_core` s oddílem na přechod a společné argumenty před příkazem (0.14.3), režim agenta podle přístupu k vaultu a přenosný čtecí skript Unrealu (0.14.4), import do inboxu `inbox_import` se souborem výměny a převodníkem Notion (0.15.0), základ projektových rolí: `role_base`, příznak `roles` v manifestu, G5 u nesrovnaného profilu (0.16.0), věrný převod Notion v `inbox_import`, podněty rolí přes `queue.md`, Knihovník uzavírá zápis `task_close` (0.17.0), čtení Unrealu proti `state`: G10 a šablona `state` (0.18.0), rozdělení kontraktu L0: zásady zápisu ve `write_rules.md`, modul `hestia_feedback` (0.19.0), čtecí nástroje `section`, `find`, `agenda`, `role_diff`, oddíl *Změny instrukcí* v reportu `update_core`, `compose_role` changed/unchanged, `## Souhrn` a G14 (0.20.0), Změny instrukcí bez zálohy starého core a `role_diff` „nelze určit“ (0.20.1). Vývoj řídí aktivní předání vývoje core v `hearthlore/Handovers/` (nyní `predani_vyvoj_core_soubeh.md`; fáze 1–3 v `_archive/predani_vyvoj_core_f1-3.md`). Technický základ: `hearthlore/zadani/13_technicky_zaklad.md`. Verze core: **0.20.1** ([CHANGELOG](CHANGELOG.md)).

## Použití

Python ≥ 3.11 a PyYAML (`pip install pyyaml`).

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
python <Projekt>/Hestia/_core/scripts/hestia.py frontmatter --map migrace.yaml [--move] [--force] [--apply]
python <Projekt>/Hestia/_core/scripts/hestia.py ue_query --emit (--entity E | --all) [--apply]   # čtecí skript do Maintenance/ue/ (spustí se v editoru)
python <Projekt>/Hestia/_core/scripts/hestia.py ue_query --import [výsledek] [--entity E | --all] [--apply]   # Maintenance/reports/ue_<entita>.json
python <Projekt>/Hestia/_core/scripts/hestia.py inbox_import --from Maintenance/import/<zdroj>_RRRR-MM-DD.json [--apply]   # scratch do Inbox/ (soubor výměny zapíše agent, modul inbox_import)
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --latest [--apply]          # nejvyšší značka core vX.Y.Z z core_source (config.yaml)
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --tag vX.Y.Z [--apply]      # konkrétní značka; --no-after: kroky po aktualizaci jen vypsat
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --from <cesta k hestia/> [--with-views] [--apply]   # záloha; --with-views: chybějící pohledy do Dashboard/views/
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --after-only [--apply]      # jen kroky po aktualizaci (po selhání kroku nebo přerušení)
python <Projekt>/Hestia/_core/scripts/hestia.py export_cr [--area A] [--include-works] [--apply]   # structure_log → Maintenance/outbox/CR_….md
```

Společné argumenty (`--vault`, `--apply`, `--force`, `--json`, `--quiet`) platí před příkazem i za ním (13 kap. 3).

Čtení Unrealu bez otevřeného editoru (záloha, 13 kap. 10.11): vygenerovaný skript jde spustit i `UnrealEditor-Cmd <projekt>.uproject -run=pythonscript -script=<Hestia>/Maintenance/ue/ue_query_<id>.py`, pak `ue_query --import`; core to sám nespouští. Kostra toolsetu pro Unreal MCP (etapa 2, neověřená): `templates/unreal/init_unreal.py`.

**Aktualizace core v instanci** (13 kap. 10.6, 11 kap. 6): do `Maintenance/config.yaml` patří `core_source` (cesta k repozitáři HearthLore relativně k vaultu, např. `"../../../HearthLore"`). `update_core --latest` vezme `hestia/` nejvyšší značky `vX.Y.Z` přes `git archive` (nikdy větev ani pracovní strom). Dry-run ukáže rozdíl, poznámky z `CHANGELOG.md` a sečtený manifest `upgrade.yaml` (automatické kroky, ruční úkoly, CR k ověření). `--apply` vymění `_core/` a novým core spustí `asset_index` → `hubs` → `doc_index` → `compose_role` (podle manifestu; `compose_role` při každé změně verze, jsou-li ve vaultu kompiláty), pak `lint --all` a `audit` v dry-run; ruční úkoly zapíše do `queue.md` (`T-…`, bez duplicit). Report `Maintenance/reports/update_core_RRRR-MM-DD.md` má na každý přechod oddíl `## Přechod <stará> → <nová>` (další přechod téhož dne se připíše) se stavem, výsledky kroků (u `asset_index` změny přiřazení) a ručními úkoly; oddíl vznikne hned po výměně `_core/` a doplňuje se po krocích, průběh jde hned na stderr. Dry-run ohlásí nedokončený přechod; doběhne `update_core --after-only --apply`, který oddíl doplní. Selže-li krok, `_core/` zůstává nový a zbytek doběhne `update_core --after-only --apply`. **Přechod z verze bez `--tag` (do 0.13.0)** jde jednou postaru, skriptem nové verze z pracovní kopie značky: `git worktree add --detach ../hestia-vX.Y.Z vX.Y.Z`, pak `python -I ../hestia-vX.Y.Z/hestia/scripts/hestia.py update_core --vault <Projekt>/Hestia --from ../hestia-vX.Y.Z/hestia [--apply]`. Vývojář přidává s každou vydanou verzí záznam do `upgrade.yaml` (i prázdný; test úplnosti proti `CHANGELOG.md`).

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
| `agents/` | `CONTRACT.md` (L0), `modules/` (L1), profily `Curator.md`, `Auditor.md`, `Librarian.md`, výchozí `write_rules`, `review_plan` (zadání 12) | 2 |
| `scripts/` | `hestia.py` + balíček `hestia_lib/`: `init` (fáze 1), `compose_role` (2), `lint`, `frontmatter`, `asset_index`, `hubs`, `audit`, `task_close`, `update_core` (3), `export_cr`, `doc_index`, `compose_context`, `ue_query`, `inbox_import` (souběh s pilotem); `hestia_ue.py` = čtecí modul pro Python v Unrealu (bez `hestia_lib`) (zadání 13, kap. 3); `migrations/` pro migrace MAJOR verzí (kostra) | 1–3 |

## Skrytí `_core/` a `Maintenance/` ve stromu souborů (volitelné)

Snippety `.obsidian/snippets/hestia-hide-core.css` a `hestia-hide-maintenance.css` jsou ve výchozím stavu vypnuté. Zapnutí je osobní volba: *Nastavení → Vzhled → Úryvky CSS*. Nové instance je dostanou z `init`, existující z `update_core`. Ten snippety `hestia-*.css` srovná s core při každém běhu (doplní, přepíše změněné, odebrané přesune do `_to_delete/`), zapnutí nemění. Předpona `hestia-` znamená, že soubor patří core; vlastní úpravu ulož jako snippet pod jiným jménem. Verzují se jen snippety `hestia-*.css` (výjimka v `.gitignore`), ostatní snippety a `appearance.json` zůstávají osobní.

## Pravidla

- Do `hestia/` zapisuje vývojář core podle aktivního předání, agent HearthLore (nebo člověk) po schválení změny ze zadání.
- Každá změna zvýší verzi a zapíše se do changelogu.
- Modul v prototypu core nemění; odchylky a poznatky posílá jako change request do `hearthlore/change-requests/`.
