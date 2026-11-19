# Hestia (core)

*Hestia custodit, ut Fabula fiat Mundus.*

Core nástroje Hestia. Tato složka je **jediná část repozitáře, která se přenáší do prototypů**, kde je jako modul `Hestia/_core/` (zadání 02, `hearthlore/zadani/02_struktura_vaultu.md`).

**Stav:** fáze 1 akceptovaná (taxonomie, šablony, šablona vaultu, `init`, `lint` v rozsahu fáze 1), fáze 2 akceptovaná (kontrakt, moduly, profily Curator a Auditor, `compose_role`), fáze 3 akceptovaná (`lint`, `asset_index`, `hubs`, `audit`, `task_close`, `frontmatter`, `update_core`, `init --no-game-layer`). Souběžně s pilotem: `export_cr` (0.4.0), srovnání se zadáním 0.11.2 (0.4.1), pohledy pro Q1 ve variantě Bases i Dataview (0.5.0), varianta skript pro matici a mapu a manifest pohledů (0.6.0), zátěžový test a snippety pro skrytí složek (0.7.0), srovnání snippetů v `update_core` (0.7.1), migrační mapa podle CR z pilotu (0.8.0), šablona kroku s volitelnou historií (0.8.1), návrh a realizace: režim cíle, hloubka návrhu, G13 (0.9.0), dokument u všech entit a povinný `target_mode` lokální domény (0.9.1), převod odkazů při migraci: aliasy, cesty od kořene prototypu, obrázky (0.10.0), zmínky souborů v backtickách (0.10.1), cíl zmínek jen soubory přesunuté mapou (0.10.2). Vývoj řídí aktivní předání vývoje core v `hearthlore/Handovers/` (nyní `predani_vyvoj_core_soubeh.md`; fáze 1–3 v `_archive/predani_vyvoj_core_f1-3.md`). Technický základ: `hearthlore/zadani/13_technicky_zaklad.md`. Verze core: **0.10.2** ([CHANGELOG](CHANGELOG.md)).

## Použití

Python ≥ 3.11 a PyYAML (`pip install pyyaml`).

```text
python hestia/scripts/hestia.py init --vault <Projekt>/Hestia --prototype Lapikus --root Lapikus_Region --engine-version 5.8          # dry-run
python hestia/scripts/hestia.py init --vault <Projekt>/Hestia --prototype Lapikus --root Lapikus_Region --engine-version 5.8 --apply
python hestia/scripts/hestia.py init --vault <Projekt>/Hestia --no-game-layer --apply           # instance bez herní vrstvy
python <Projekt>/Hestia/_core/scripts/hestia.py lint [soubory…] [--all] [--json]       # bez argumentů: změněné podle gitu
python <Projekt>/Hestia/_core/scripts/hestia.py compose_role [Role…] [--apply]       # kompilát pro chat Roles/_compiled/<Role>_compiled.md
python <Projekt>/Hestia/_core/scripts/hestia.py asset_index [--apply]                # Maintenance/asset_index.md + .json
python <Projekt>/Hestia/_core/scripts/hestia.py hubs [Entita…] [--apply]             # generované sekce hubů, kroků, Dashboard/Index.md
python <Projekt>/Hestia/_core/scripts/hestia.py audit [--baseline reports/audit_….json] [--apply]   # report, fronta, stav
python <Projekt>/Hestia/_core/scripts/hestia.py task_close --role R --source S --note "…" [--change E="…"] [--entity E] [--archive-handover P] [--apply]
python <Projekt>/Hestia/_core/scripts/hestia.py frontmatter --map migrace.yaml [--move] [--force] [--apply]
python <Projekt>/Hestia/_core/scripts/hestia.py update_core --from <cesta k hestia/> [--with-views] [--apply]   # --with-views: chybějící pohledy do Dashboard/views/
python <Projekt>/Hestia/_core/scripts/hestia.py export_cr [--area A] [--include-works] [--apply]   # structure_log → Maintenance/outbox/CR_….md
```

Bez `--apply` vždy dry-run (nic nezapíše). Proměnná prostředí `HESTIA_TODAY=RRRR-MM-DD` pevně nastaví dnešní datum (testy, kontrola před vydáním).

Testy a zkušební projekt jsou mimo distribuovaný core, v `hearthlore/tests/`; spuštění z kořene repozitáře: `python -m unittest discover -s hearthlore/tests`.

## Obsah

| Složka / soubor | Obsah | Fáze |
|---|---|---|
| `VERSION`, `CHANGELOG.md` | verze `MAJOR.MINOR.PATCH`, migrační poznámky u MAJOR (zadání 11, kap. 5) | 1 |
| `taxonomy/` | domény, kategorie, `kind` a očekávané domény, typy, validace, výchozí šablony kroků (YAML); `views.yaml` = manifest pohledů s příznakem herní vrstvy | 1 |
| `templates/` | šablony poznámek (zadání 07): hub, doménový dokument, stav, scratch, crosscut, rozhodnutí, report, CR, profil role, know-how, modul, předání, krok, master lore | 1 |
| `vault_template/` | prázdná struktura `Hestia/` pro nový prototyp, výchozí `.obsidian`, pohledy (`Dashboard/views/bases/*.base`, `dataview/dv_*.md`, `generated/*.md`; do rozhodnutí Q1 všechny varianty; `local/` pro vlastní pohledy instance), vstupní soubor `entrypoint.md`, kostra master lore | 1 |
| `agents/` | `CONTRACT.md` (L0), `modules/` (L1), profily `Curator.md`, `Auditor.md`, výchozí `write_rules`, `review_plan` (zadání 12) | 2 |
| `scripts/` | `hestia.py` + balíček `hestia_lib/`: `init` (fáze 1), `compose_role` (2), `lint`, `frontmatter`, `asset_index`, `hubs`, `audit`, `task_close`, `update_core` (3), `export_cr` (souběh s pilotem) (zadání 13, kap. 3); `migrations/` pro migrace MAJOR verzí (kostra) | 1–3 |

## Skrytí `_core/` a `Maintenance/` ve stromu souborů (volitelné)

Snippety `.obsidian/snippets/hestia-hide-core.css` a `hestia-hide-maintenance.css` jsou ve výchozím stavu vypnuté. Zapnutí je osobní volba: *Nastavení → Vzhled → Úryvky CSS*. Nové instance je dostanou z `init`, existující z `update_core`. Ten snippety `hestia-*.css` srovná s core při každém běhu (doplní, přepíše změněné, odebrané přesune do `_to_delete/`), zapnutí nemění. Předpona `hestia-` znamená, že soubor patří core; vlastní úpravu ulož jako snippet pod jiným jménem. Verzují se jen snippety `hestia-*.css` (výjimka v `.gitignore`), ostatní snippety a `appearance.json` zůstávají osobní.

## Pravidla

- Do `hestia/` zapisuje vývojář core podle aktivního předání, agent HearthLore (nebo člověk) po schválení změny ze zadání.
- Každá změna zvýší verzi a zapíše se do changelogu.
- Modul v prototypu core nemění; odchylky a poznatky posílá jako change request do `hearthlore/change-requests/`.
