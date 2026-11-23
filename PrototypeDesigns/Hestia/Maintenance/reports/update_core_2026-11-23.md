---
type: report
updated: 2026-11-23
---
# Aktualizace core 2026-11-23

## Přechod 0.21.1 → 0.23.0
- Stav: dokončeno
- Výměna `_core/`: starý core v `_to_delete/_core_0.21.1/`; řádek v `structure_version.md`.
- Záznamy manifestu: 0.22.0, 0.23.0.

### Automatické kroky
- `asset_index`: v pořádku
  - bez změn přiřazení
- `hubs`: v pořádku
  - změněné soubory: 17
- `doc_index`: v pořádku
  - index beze změny
- `compose_role`: v pořádku
  - změněné kompiláty: 6 z 6

### Kontroly (dry-run)
- lint: chyby 0, upozornění 0, informace 9
- audit: chyby 0, upozornění 33, informace 54

### Ruční úkoly
- `update_core:0.22.0:asset_setup` (ve frontě): Založit Assets/ a Assets/Konvence_assetu.md (kostra v _core/vault_template/Assets/Konvence_assetu.md.tpl, přípona .md); profily Crafter (modul asset_work) a Furnisher (modul asset_request) podle tpl_role; doplnit asset_request do modules profilů rolí, které assety potřebují (Architect, Builder, GameDesign); pak compose_role. Převod dosavadního katalogu a checklistu assetů na karty je krok instance (13 kap. 10.16)
- `update_core:0.22.0:role_base` (ve frontě): Srovnat profily projektových rolí se základem 0.22.0 (assety (12 kap. 3, 4.6, 8; zadání 0.23): role, které knihovní assety potřebují (Architect, Builder, Furnisher, GameDesign), uvedou v modules asset_request (požadavek = karta requested v Assets/, nejdřív find); výrobce (Crafter) asset_work; obojí compile: listed. Úkol pro jinou roli na konec queue.md (task, code: role:<Role>, 12 kap. 4.7; zadání 0.24), agenda ho ukáže cílové roli. Podnět pro Hestii smí mít část dopad: (12 kap. 4.5; zadání 0.24.1)); po schválení GameDesignerem nastavit role_base: 0.22.0 a spustit compose_role (12 kap. 2.1, 13 kap. 10.6a)
- `update_core:0.23.0:asset_sources` (ve frontě): Založit Maintenance/taxonomy_local/asset_sources.yaml podle vzoru v 13 kap. 10.18 (meshes s fields, name, ue_root, ue_dirs, content_dir; versions s ue_tag; global_versions; shapes; data_refs), ověřit lint a asset_index --apply (sekce library), pak hubs --apply (blok Z kódu v kartách meshí). Bez manifestu se etapa B přeskočí
- `update_core:0.23.0:asset_conventions` (ve frontě): Doplnit do Assets/Konvence_assetu.md sekce Rozměr a graybox, Pojmenování a varianty, Pravidla výroby, Verze a import, Změny konvence (s tabulkou | datum | změna | dotčené assety | úkol |) podle 07 kap. 20.1; kostra v _core/vault_template/Assets/Konvence_assetu.md.tpl
- `update_core:0.23.0:asset_envelope` (ve frontě): Doplnit envelope u karet meshí a Blueprintů od generated (obal skutečného rozměru z bloku Z kódu, zaokrouhleno nahoru na cm); lint ho od 0.23.0 hlásí jako chybu
- `update_core:0.23.0:role_base` (ve frontě): Srovnat profily projektových rolí se základem 0.23.0 (assety etapy B a C (12 kap. 3, 4.6; zadání 0.24.3 až 0.26): jednoduché assety (díl stavby z existujícího generátoru) smí vyrábět i Builder, profil Builderu pak uvede v modules asset_work; žadatel vyplňuje owner vždy (výchozí Crafter); karty bez owner ukáže agenda jen roli asset_default_owner. Texty modulů asset_work, asset_request, lookup a ue_lookup se mění (Konvence_assetu, envelope jako rozměr grayboxu, blok Z kódu, čtení assetů z UE)); po schválení GameDesignerem nastavit role_base: 0.23.0 a spustit compose_role (12 kap. 2.1, 13 kap. 10.6a)

### Základ projektových rolí
- Změna v 0.22.0: assety (12 kap. 3, 4.6, 8; zadání 0.23): role, které knihovní assety potřebují (Architect, Builder, Furnisher, GameDesign), uvedou v modules asset_request (požadavek = karta requested v Assets/, nejdřív find); výrobce (Crafter) asset_work; obojí compile: listed. Úkol pro jinou roli na konec queue.md (task, code: role:<Role>, 12 kap. 4.7; zadání 0.24), agenda ho ukáže cílové roli. Podnět pro Hestii smí mít část dopad: (12 kap. 4.5; zadání 0.24.1)
- Změna v 0.23.0: assety etapy B a C (12 kap. 3, 4.6; zadání 0.24.3 až 0.26): jednoduché assety (díl stavby z existujícího generátoru) smí vyrábět i Builder, profil Builderu pak uvede v modules asset_work; žadatel vyplňuje owner vždy (výchozí Crafter); karty bez owner ukáže agenda jen roli asset_default_owner. Texty modulů asset_work, asset_request, lookup a ue_lookup se mění (Konvence_assetu, envelope jako rozměr grayboxu, blok Z kódu, čtení assetů z UE)
- Rozdíl `tpl_role`: beze změny šablony.
- Profily nesrovnané se základem 0.23.0 (ruční úkol `role_base`):
  - `Roles/Architect.md`: role_base 0.20.0 je starší než 0.23.0
  - `Roles/Builder.md`: role_base 0.20.0 je starší než 0.23.0
  - `Roles/Furnisher.md`: role_base 0.20.0 je starší než 0.23.0
  - `Roles/GameDesign.md`: role_base 0.20.0 je starší než 0.23.0

### Změny instrukcí
- Změněné soubory: 10. Role si změny vypíše `role_diff <Role>`.

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
> | práce v režimu chat | `chat_entry` |
> | konec tasku | `task_close` |
>
> Modul načti, když nastane spouštěč, i když ho profil neuvádí; kdy modul předáš jiné roli, říká `start`. Moduly: `_core/agents/modules/`, lokální `Roles/modules/`.

#### `agents/Curator.md` (změněný)
- Sekce: Postupy podle zakázky (změněná), Formáty výstupů (změněná)
- Nové znění: 3385 znaků, nad 3000; přečti sekce v `_core/agents/Curator.md`.

#### `agents/Librarian.md` (změněný)
- Sekce: Matice pravomocí (změněná), Zápis do logů (změněná)

> ## Matice pravomocí
> Platí oddíl Knihovník v `_core/agents/write_rules.md` (05 kap. 3.2a) a lokální doplňky v `Maintenance/write_rules_local.md`. Shrnutí: tělo dokumentů v `Docs/` a master lore (doslovná textace přímo, přeformulování po schválení), založení dokumentu a frontmatter zapisovaných dokumentů (`updated`, `validity`) na pokyn k zápisu, glosář, *Předzpracování* a `intake` v `Inbox/` a `Scratch/` (přesun podle rozhodnutí v třídění), sekce `## Otevřené otázky`, položka fronty k rozporu, podnět pro Hestii a úkol pro roli, `changes.md` (jen připisovat, skriptem `task_close`). Ostatní oblasti ne, ani `structure_log.md` a `outbox/`.

> ## Zápis do logů
> - **Vlastní zápis** (formalizace, založení entity nebo dokumentu, glosář) uzavřeš skriptem: `python _core/scripts/hestia.py task_close --role Librarian --source <zdroj> --change <Entita>="<co>"` (změna kánonu s předponou `změna kánonu:`), nejdřív dry-run, pak `--apply`. Skript zapíše řádky `changes.md`, doplní `updated`, obnoví huby a `doc_index` a spustí `lint`, takže nová entita je hned dohledatelná. Když skript spustit nejde, uveď v hlášení, co neběželo, co z toho plyne (např. „entita chybí v indexu“) a kdo ho má spustit.
> - `changes.md`: řádek na každý zapsaný dokument nebo entitu, jen na konec (zapíše `task_close`).
> - `queue.md`, na konec: položka k rozporu mezi dokumenty (pro Auditora); **podnět pro Hestii** (kolize pojmů, opakovaně chybějící náležitosti, problém šablony nebo modulu): `kind: proposal`, `code: hestia`, `target`, `proposal` = `Librarian: co se stalo (doklad: <odkaz>; dopad: <dopad>) → navrhovaná změna` (`dopad:` volitelně), `priority: medium`. Do `structure_log.md` ani `outbox/` nepíšeš; podnět převede Curator. **Úkol pro roli** (práce pro jinou roli, třeba doplnit dokument po třídění; 12 kap. 4.7): `kind: task`, `code: role:<Role>`, `target`, `proposal` s dokladem, `priority: medium`, `state: open`; uveď ho v hlášení. Úkol pro tebe ukáže `agenda --role Librarian`; po splnění ho uzavři (`state: done`, `closed`).
> - Hlášení na konci relace: zápisy bez doplňujících otázek a s nimi, typy otázek, odpovědi s citací / „není zdokumentováno“, rozpory a změny kánonu, vrácené přepisy (metriky 12 kap. 3b.9).

#### `agents/modules/asset_request.md` (nový)
- Sekce: (frontmatter) (nová), (úvod) (nová), Kdy (nová), Postup (nová), Výstup (nová), Známé pasti (nová)
- Nové znění: 3099 znaků, nad 3000; přečti sekce v `_core/agents/modules/asset_request.md`.

#### `agents/modules/asset_work.md` (nový)
- Sekce: (frontmatter) (nová), (úvod) (nová), Kdy (nová), Postup (nová), Výstup (nová), Známé pasti (nová)
- Nové znění: 3568 znaků, nad 3000; přečti sekce v `_core/agents/modules/asset_work.md`.

#### `agents/modules/hestia_feedback.md` (změněný)
- Sekce: Postup (změněná), Známé pasti (změněná)

> ## Postup
> 1. Change request nezakládáš a do `structure_log.md` ani `outbox/` nepíšeš: CR mimo kanál Curatora (`export_cr`) by nikdo nezpracoval.
> 2. **Režim vault:** připiš na konec `Maintenance/queue.md` položku `kind: proposal`, `code: hestia`, nebo s navrženou kategorií logu `code: hestia:<kategorie>` (`friction`, `missing`, `surplus`, `collision`, `taxonomy`, `works`, `idea`), `target` = čeho se týká (entita, dokument nebo část Hestie, např. `tpl_state`, `audit G10`), `proposal` = `<role>: co se stalo (doklad: <odkaz>; dopad: <dopad>) → navrhovaná změna`, kde `<odkaz>` je wikilink na poznámku nebo cesta v backtickách, za ním případně řádek nebo datum (např. „doklad: `Maintenance/changes.md` 2026-11-21“; samotný popis řádku bez odkazu `feedback_log` nezapíše) a `dopad:` je volitelný (co problém způsobuje, např. „hledání trvá dlouho“; `feedback_log` ho dá do sloupce *Dopad*), `priority: medium` (`high` jen když podnět blokuje práci), `state: open`. Schválení GameDesignera k zápisu není potřeba.
> 3. **Režim chat:** podnět dej do zápisu Hestia, sekce *Podněty pro Hestii* (modul `chat_entry`); do fronty ho zapíše ten, kdo zápis zapracuje.
> 4. Podnět uveď v hlášení na konci tasku (`task_close`, krok 11).

> ## Známé pasti
> - Založit CR přímo v `outbox/` nebo v repozitáři projektu: zůstane mimo kanál a nikdo ho nezpracuje.
> - Podnět bez dokladu, nebo s dokladem, který nejde dohledat (wikilink na existující poznámku nebo existující cesta v backtickách): `feedback_log` ho nezapíše. Doklad „řádek ve changes.md“ bez odkazu neprojde.
> - Zaměnit podnět s otázkou (`question`) nebo s nálezem údržby (zapisuje Auditor), nebo s prací pro jinou roli (úkol pro roli `code: role:<Role>`, `write_rules.md`).

#### `agents/modules/lookup.md` (změněný)
- Sekce: Postup (změněná)

> ## Postup
> 1. **Ve vaultu** (i chat s připojenou složkou projektu) hledej příkazem `hestia.py find "<dotaz>"` (index dokumentů: název, `aliases`, nadpisy sekcí, entita, cesta; glosář; pod 3 výsledky doplní hledání v textu, `--text` vždy), ne `grep -r` přes vault. Z kandidátů čti jen shodné sekce (`hestia.py section <dokument> "<nadpis>"`); dokument nad `doc_summary_chars` nečti celý (modul `start`, *Čtení*). Starý index obnov `hestia.py doc_index --apply`. Když skript core spustit nejde (relace bez shellu nebo bez vhodného Pythonu), čti index, glosář a dokumenty přímo a v odpovědi výslovně uveď, že skript neběžel (index může být starý).
> 2. **V chatu bez vaultu** pracuj jen s balíčkem kontextu (`compose_context`) a s tím, co máš v tasku; co v něm není, nedomýšlej. **Bez balíčku** neodpovídej a řekni přesně, který balíček potřebuješ a jakým příkazem vznikne: `hestia.py compose_context --entity <Entita> --apply` (otázka o entitě), `--query "<otázka>"` (otázka napříč dokumenty), `--topic <kategorie nebo doména>`; nebo požádej o přístup k vaultu (připojenou složku projektu).
> 3. U otázky o entitě vezmi z hubu stav: návrh, realizace, cíl a režim (blok *Domény*); má-li entita karty assetů, i souhrnný řádek bloku *Assety* (počty podle stavu, grayboxy, `outdated` v UE; v `doc_index` pole `assets`). Je to signál vedle `depth_*`, hloubku z něj neodvozuj.
> 4. Rozliš **návrh** (`design`, `spec`, `decision`), **realizaci** (`state`, skript, report Unrealu) a **zavržené** (`status: rejected`). Realizaci ověř čtecím dotazem nebo posledním reportem (modul `ue_lookup`), je-li to potřeba.
> 5. Když si zdroje odporují, nerozhoduj: vypiš rozpor a podle hierarchie zdrojů (12 kap. 3b.3) uveď, co platí. Zapiš otázku k dotčenému dokumentu, u rozporu mezi dokumenty i položku fronty pro Auditora.
> 6. `outdated`, `superseded` a `archived` dokumenty uváděj jen jako historii a označ je. Položky z `Inbox/` a nezařazené ze `Scratch/` jsou **neověřené**.

#### `agents/modules/start.md` (změněný)
- Sekce: Postup (změněná)
- Nové znění: 3255 znaků, nad 3000; přečti sekce v `_core/agents/modules/start.md`.

#### `agents/modules/ue_lookup.md` (změněný)
- Sekce: Postup (změněná)
- Nové znění: 3822 znaků, nad 3000; přečti sekce v `_core/agents/modules/ue_lookup.md`.

#### `agents/write_rules.md` (změněný)
- Sekce: Matice pravomocí (změněná), Knihovník (           , 05 kap. 3.2a) (změněná), Schvalování (změněná)
- Nové znění: 6472 znaků, nad 3000; přečti sekce v `_core/agents/write_rules.md`.

#### Role a soubory
- Architect: `agents/CONTRACT.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/ue_lookup.md`, `agents/write_rules.md`
- Builder: `agents/CONTRACT.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/ue_lookup.md`, `agents/write_rules.md`
- Furnisher: `agents/CONTRACT.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/write_rules.md`
- GameDesign: `agents/CONTRACT.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/write_rules.md`
- Curator: `agents/CONTRACT.md`, `agents/Curator.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/write_rules.md`
- Auditor: `agents/CONTRACT.md`, `agents/modules/hestia_feedback.md`, `agents/modules/start.md`, `agents/modules/ue_lookup.md`, `agents/write_rules.md`
- Librarian: `agents/CONTRACT.md`, `agents/Librarian.md`, `agents/modules/hestia_feedback.md`, `agents/modules/lookup.md`, `agents/modules/start.md`, `agents/modules/ue_lookup.md`, `agents/write_rules.md`

### CR k ověření
- CR-026_karta_assetu (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-029_prace_s_assety (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-032_ukoly_pro_role_ve_fronte (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-025_ue_ism_bounds (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-031_podnety_do_structure_log_skriptem (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-027_asset_index_knihovni_meshe (ověřit v instanci, do *Průběhu* `in_pilot`)
- CR-028_ue_query_assety (ověřit v instanci, do *Průběhu* `in_pilot`)

### Pracovní kopie
- Pracovní adresář: `/sessions/rcw-01nw4mxpuk2thvsg4ues1vms/hestia_work_p19`.
- Kontrola originálu: beze změny od snímku (1626 souborů).
- Přeneseno: změněné 27, nové 1, přesunuté 0; `_core/` vyměněn (starý v `_to_delete/_core_0.21.1/`).
  - ~ `Dashboard/Index.md`
  - ~ `Entities/Brana.md`
  - ~ `Entities/Brana_Straz.md`
  - ~ `Entities/Guesthouse.md`
  - ~ `Entities/Lapikus_Region.md`
  - ~ `Entities/Les_Lapikus.md`
  - ~ `Entities/Nadvori_Stan.md`
  - ~ `Entities/Palac.md`
  - ~ `Entities/Palac_Kovarna.md`
  - ~ `Entities/Palac_Kovarna_Vybaveni.md`
  - ~ `Entities/Palac_Obydli.md`
  - ~ `Entities/Strazni_Vez.md`
  - ~ `Entities/Udoli_Reky.md`
  - ~ `Entities/Vez.md`
  - ~ `Entities/Vez_Pristresek.md`
  - ~ `Maintenance/asset_index.json`
  - ~ `Maintenance/asset_index.md`
  - ~ `Maintenance/doc_index.json`
  - ~ `Maintenance/queue.md`
  - ~ `Maintenance/structure_version.md`
  - ~ `Roles/_compiled/Architect_compiled.md`
  - ~ `Roles/_compiled/Builder_compiled.md`
  - ~ `Roles/_compiled/Curator_compiled.md`
  - ~ `Roles/_compiled/Furnisher_compiled.md`
  - ~ `Roles/_compiled/GameDesign_compiled.md`
  - ~ `Roles/_compiled/Librarian_compiled.md`
  - ~ `Steps/06_furnishing.md`
  - + `Maintenance/reports/update_core_2026-11-23.md`
- Čas fází: kopie 83.2 s, přechod 131.3 s, zápis zpět 63.5 s.
