# Changelog – Hestia core

Verze `MAJOR.MINOR.PATCH` podle zadání 11, kap. 5 (`hearthlore/zadani/11_vyvojovy_cyklus.md`). MAJOR verze nese migrační poznámku.

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
