---
type: agent_module
module_id: ue_lookup
trigger: otázka na realizaci, audit
requires: []
modes: [vault, chat]
compile: listed
validity: valid
updated: 2026-11-23
---
# Čtení stavu v Unrealu

## Kdy
Potřebuješ vědět, co je v enginu skutečně postavené: otázka na realizaci (`lookup`), audit, ověření `depth_*`, nebo práce role, která stav v enginu potřebuje (zejména stavba a návrh staveb). Smí ho použít Knihovník, Auditor a projektové role, které ho mají v profilu (12 kap. 3b.8, 8).

## Postup
1. **Jen čtení.** Používej jen čtecí dotazy core (`hestia.py ue_query`, 13 kap. 10.11); nikdy nezapisuj do levelu ani assetů, nespouštěj obecný Python ani build. Bez `Maintenance/taxonomy_local/ue_map.yaml` se Unreal nečte; entita bez pravidla v něm nemá report.
2. **Etapa 1** (skript v editoru):
   - `python _core/scripts/hestia.py ue_query --emit --entity <Entita> --apply` (nebo `--all`) vygeneruje čtecí skript do `Maintenance/ue/`;
   - GameDesigner ho spustí v editoru (*Tools → Execute Python Script*), skript zapíše surový výsledek vedle sebe;
   - `ue_query --import --entity <Entita> --apply` (nebo `--all`) uloží report `Maintenance/reports/ue_<entita>.json`, pak `hubs --apply` obnoví blok `## Stav v UE` v hubu.
   V chatu bez vaultu požádej GameDesignera o spuštění a o report. Relace, která vault vidí, ale skript core spustit nemůže, požádá o vygenerování a import toho, kdo ho spustit může, přesně těmito příkazy.
3. Když editor neběží, použij poslední report a uveď jeho datum; report starší než `ue_report_days` je v hubu označený jako starý.
4. Report ukazuje jen měřitelné signály (actory podle třídy, zástupné meshe `/Engine/BasicShapes/`, výchozí materiály, fáze `stage:*`, rozsah, vlastní a za potomky). Úroveň realizace se automaticky neodhaduje: porovnej ji s `depth_*` podle vodítka (12 kap. 3b.8): jen polohy → blockout, rozměry a kolize → greybox, proxy meshe a tagy → whitebox, meshe a data → asset_data, Blueprint a logika v provozu → functional.
   - **Zástupné meshe** sám úroveň neurčují, rozhoduje celek (rozměry, siluety, materiály, data). Meshe, které instance používá záměrně (např. kameny zříceniny z `Cube`), patří do `placeholder_ignore` v `ue_map.yaml` (nejvyšší úroveň pro všechny entity, v položce `items` jen pro ni); report je pak počítá zvlášť (`placeholder_ignored`). Zápis do `ue_map.yaml` jen po schválení (`taxonomy_local`).
   - Actory druhu `ism` (Instanced/Hierarchical Instanced Static Mesh) jsou meshe po instancích (`ism_instances`), ne proxy. Rozsah se počítá z geometrie (meshe a instance, bez kořene actoru).
   - `pivot_far` v bloku `## Stav v UE` (kořen actoru dál od geometrie než `ue_pivot_far_cm`) je informace pro modelování v instanci (kořen sloučeného actoru daleko od stavby), ne nález ani úroveň realizace.
5. Neshodu reportu s `depth_*` zapiš jako otázku nebo ji nech na auditu (G10). `depth_*` neměníš; mění ho ten, kdo realizoval, nebo GameDesigner.
6. **Report a `state`:** při odpovědi o realizaci porovnej report se `state` entity. Je-li report novější a stavbu ukazuje, platí „v levelu je“ (s datem reportu), i když starší `state` píše „neověřeno“ nebo „neběželo“; rozpor řekni a starší text nepřebírej. Report nepotvrzuje vzhled ani funkci: ty platí jen z § *Vizuálně ověřeno* ve `state` (kdo, kdy). Když `state` měníš, doplň § *V levelu* podle reportu (stavby, datum reportu, odkaz). Hub to připomene v bloku `## Stav v UE`, audit jako G10 (12 kap. 3b.8, zadání 0.19).
7. **Je asset v UE?** (karty assetů, 13 kap. 10.19): report `Maintenance/reports/ue_assets.json` uvádí na asset `ue_path`, zda existuje, tagy verzí a stav `current` / `outdated` (verze v UE starší než v kódu, čeká na import) / `missing`; blok *Stav v UE* v kartě ho shrnuje s datem čtení. Nové čtení: `hestia.py ue_query --assets --emit --apply` (výchozí karty od `generated`; `--asset <jméno>`, `--category <kategorie>`, `--all-library`), spustit v editoru, `ue_query --import --assets --apply`, `hubs --apply`.
8. V chatu bez vaultu pracuj jen s reportem, který máš v balíčku kontextu. **Bez balíčku** řekni přesně, který potřebuješ: `hestia.py compose_context --entity <Entita> --apply` (hub entity s blokem `## Stav v UE`, tedy souhrn posledního reportu a jeho datum), nebo přístup k vaultu. Ve vaultu čti report `Maintenance/reports/ue_<entita>.json` přímo.

## Výstup
Stav entity v Unrealu se zdrojem (report a jeho datum) a srovnání s `depth_*`; v odpovědi `lookup` řádek ve *Zdrojích*.

## Známé pasti
- Vydávat starý report za aktuální stav bez data.
- „Opravit“ `depth_*` podle reportu; to je rozhodnutí realizátora nebo GameDesignera.
- Převzít ze starého `state` „neověřeno“, když novější report stavbu ukazuje; nebo naopak brát report jako vizuální potvrzení.
- Spustit v editoru skript, který není čtecí dotaz core.
