---
type: agent_module
module_id: ue_lookup
trigger: otázka na realizaci, audit
requires: []
modes: [vault, chat]
compile: listed
validity: valid
updated: 2026-11-21
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
5. Neshodu reportu s `depth_*` zapiš jako otázku nebo ji nech na auditu (G10). `depth_*` neměníš; mění ho ten, kdo realizoval, nebo GameDesigner.
6. V chatu bez vaultu pracuj jen s reportem, který máš v balíčku kontextu. **Bez balíčku** řekni přesně, který potřebuješ: `hestia.py compose_context --entity <Entita> --apply` (hub entity s blokem `## Stav v UE`, tedy souhrn posledního reportu a jeho datum), nebo přístup k vaultu. Ve vaultu čti report `Maintenance/reports/ue_<entita>.json` přímo.

## Výstup
Stav entity v Unrealu se zdrojem (report a jeho datum) a srovnání s `depth_*`; v odpovědi `lookup` řádek ve *Zdrojích*.

## Známé pasti
- Vydávat starý report za aktuální stav bez data.
- „Opravit“ `depth_*` podle reportu; to je rozhodnutí realizátora nebo GameDesignera.
- Spustit v editoru skript, který není čtecí dotaz core.
