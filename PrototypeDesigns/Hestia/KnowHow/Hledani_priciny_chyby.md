---
# orchestrace
type: knowhow
knowhow_kind: diagnosis
tech: [ue_python, python]
scope: general
verified: 2026-11-17
validity: valid
updated: 2026-11-19
aliases: []
---
# Jak hledat příčinu chyby

<!-- Z KNOWHOW_hrad.md kap. 6 (pilot Lapikus, B6). -->

Postup, který se osvědčil u poškozených bounds (15. 11. 2026):

1. **Nejdřív log, pak teorie.** Rozděl log po jednotlivých assetech a spočítej, co se u kterého stalo (import, build, Nanite, varování). Rozdíl mezi „funguje“ a „nefunguje“ bývá vidět v počtech (33 kamenů bez `NaniteBuild` proti 78 ostatním).
2. **Hledej, čím se vadné liší od dobrých**, ne co mají vadné společného s teorií. Tady to byl text `bDoFastBuild` v `.uasset`, který Python v UE nevidí.
3. **Test má měnit jednu věc** a mít **kontrolní variantu**, která musí vyjít čistě. Test, který obchází dvě podezřelé věci najednou, nic nerozliší.
4. **Pozor na cache (DDC).** Stejná geometrie a stejné nastavení = stejný klíč = stejná (i poškozená) data bez buildu. Čistý test potřebuje posunutá data, opakování problému původní.
5. **Náhodná chyba se nedokazuje jedním během.** U náhodného NaN je průkaznější vedlejší příznak, který je vždy (chybějící Nanite, varování o tangentách).
6. **Oprava se ověřuje stejným testem** a v ostrém logu se hledá totéž, co ho předtím odlišovalo.
7. **Refaktoring:** `tools/checks/fingerprint.py` před změnou a po ní, výsledek musí být shodný. U záměrné změny chování se nepoužívá.
8. **Vizuální chyba ze screenshotu:** najít příčinu v datech nebo kódu, reprodukovat testem mimo UE, teprve pak opravit.
