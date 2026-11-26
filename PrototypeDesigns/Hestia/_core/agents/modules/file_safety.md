---
type: agent_module
module_id: file_safety
trigger: zápis do souborů projektu
requires: []
modes: [vault]
validity: valid
updated: 2026-11-26
---
# Bezpečný zápis souborů

## Kdy
Před každým zápisem, přepsáním, přesunem nebo přejmenováním souboru projektu (vault, kód, data).

## Postup
1. Před přepsáním porovnej soubor s verzí, kterou jsi naposledy načetl (obsah nebo hash). Změnil-li ho mezitím někdo jiný, cizí změny slouč; nepřepisuj naslepo.
2. Chráněné soubory z pravidel zápisu (`write_rules_local.md`) a `protected_files` v `Maintenance/config.yaml` (např. ruční úpravy z editoru) nepřepisuj.
3. Nemaž. Na pokyn soubor přesuň do `_to_delete/`.
4. Přesouvej bez přepsání cíle; když cíl existuje, zastav se a zeptej.
5. Skripty Hestia spouštěj nejdřív bez `--apply` (dry-run) a zkontroluj výpis; zapisuj s `--apply`.
6. Generované sekce (mezi značkami `hestia:generated`) neupravuj ručně; přepíše je skript.
7. Do dokumentu s `validity: superseded` nebo `archived` nepiš (tělo); zapiš do nástupce (`superseded_by`), a když chybí, do platného dokumentu entity. Změnu těla nahrazeného dokumentu hlásí `lint` a `task_close` (G5).

## Výstup
Zapsané soubory bez ztráty cizích změn; v hlášení seznam změněných souborů.

## Známé pasti
- Přepsat soubor, který mezitím upravil člověk nebo jiný agent.
- Přepsat ruční úpravy z editoru, které skript nezná. Vrací se do skriptu, dokud se to nestane, platí stav v enginu.
- Mazat „nepotřebné“ soubory bez pokynu.
- Doplnit novinku do nahrazeného dokumentu (katalog, starý návrh) místo do nástupce: mimo evidenci ji nikdo nenajde.
