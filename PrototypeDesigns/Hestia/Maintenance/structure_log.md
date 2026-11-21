---
type: log
updated: 2026-11-21
---
# Poznatky o struktuře

Podklad pro change requesty, připisuje se na **konec** (05 kap. 7.3, 07 kap. 9). Formát:
`| RRRR-MM-DD | kategorie | popis | dopad | navrhovaná změna | cr: <ID> |`; svislítko v textu jako `\|`.
Kategorie: `friction`, `missing`, `surplus`, `collision`, `taxonomy`, `works`, `idea`.

| datum | kategorie | popis | dopad | navrhovaná změna | cr |
|---|---|---|---|---|---|
| 2026-11-21 | missing | report `update_core` zapíše u kroku `asset_index` jen „v pořádku“; výpis „Změna přiřazení“ (`reassigned`) zůstane jen na konzoli | ověření CR o aliasech (`Ostroh_*` → `Guesthouse`) se muselo skládat z `git diff` `asset_index.md` | report obsahuje změny přiřazení (`cesta: z → na (pravidlo)`) | cr: CR_2026-11-21_update_core_report_zmena_prirazeni |
| 2026-11-21 | friction | prostředí pro spouštění core: Linuxová VM desktopové aplikace má Python 3.10 bez `pyyaml`; `hestia.py` jen skončí hláškou o verzi, `pyyaml` chybí bez návodu | agent si musel sestavit prostředí sám (`uv`, Python 3.12, `pyyaml` mimo projekt) | kontrola prostředí jako první krok Stewarda a návod v README core; otázka v podkladu Steward kap. 10 | – |
| 2026-11-21 | collision | `update_core` dry-run žádá čistý git před `--apply` (11 kap. 6, krok 2), předání pilotu dovoluje P1–P3 jedním commitem po kroku | ruční úkoly P3 před aktualizací zůstanou necommitnuté v době `--apply` | ujasnit v předání nebo zadání: ruční úkoly z fronty buď commitnout před aktualizací, nebo výslovně povolit `--apply` nad necommitnutými změnami mimo `_core/` | – |
| 2026-11-21 | friction | druhý `update_core` ve stejný den přepsal report `update_core_2026-11-21.md` (0.14.0 → 0.14.1 zůstal jen v gitu `1877d81`) | report přechodu nedohledatelný bez gitu | jméno reportu s verzemi nebo připisování oddílů | cr: CR_2026-11-21_update_core_report_a_preruseni |
| 2026-11-21 | friction | `update_core --latest --apply` přes připojenou složku trval přes 180 s a byl přerušen po výměně core a `compose_role`, před kontrolami a reportem; dokončeno `--after-only --apply`, jehož report neuvádí samotný přechod | instance bez reportu; ruční dohledání stavu | report po krocích, průběžný výstup, doporučení `--after-only` v dry-runu | cr: CR_2026-11-21_update_core_report_a_preruseni |
| 2026-11-21 | friction | `hestia.py --apply update_core …` (volba před příkazem) proběhne jako dry-run bez upozornění | riziko, že se „aplikace“ považuje za hotovou | sloučit společné volby hlavního parseru a podpříkazu | cr: CR_2026-11-21_update_core_report_a_preruseni |
