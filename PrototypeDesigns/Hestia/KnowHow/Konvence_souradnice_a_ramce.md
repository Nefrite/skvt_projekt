---
# orchestrace
type: knowhow
knowhow_kind: convention
tech: [python, ue_python]
scope: instance
verified: 2026-11-17
validity: valid
updated: 2026-11-19
aliases: []
# hra
domain: structures
---
# Konvence: souřadnice a rámce

<!-- Z KNOWHOW_hrad.md kap. 3 (pilot Lapikus, B6). -->

| Co | Hodnota |
|---|---|
| Jednotky | UE centimetry; v návrzích metry; u výšek vždy napsat, od čeho (terén, podlaha věže, absolutní Z) |
| Plošina hradu | Z ≈ 3129 cm (v levelu se může lišit, build měří terén z landscapu) |
| Terén | výška v m × 100 = světové Z v cm; landscape 252 × 252 m, střed 0, 0 |
| Světové strany | z názvů zdí: `_S` sever, `_J` jih, `_V` východ, `_Z` západ. Ověřit z dat, nehádat. |
| Poloha na zdi | `s` v metrech od prvního bodu zdi v `ruin_layout.json` |
| Palác (návrhy, `tools/ruin/palac_spec.py` → `frame`) | `s` podél `Palac_J` od jejího prvního bodu (UE −2350 / −50), `n` kolmo k severu; vektory `s` = (0,9759; −0,2184), `n` = (−0,2184; −0,9759); líc věže s = 30,75, vnitřní líc `Palac_J` n = 0,7, `Palac_S` n = 8,8 |
| Věž (návrhy) | `u` od J-Z rohu k východu, `v` k severu; výšky od podlahy přízemí (`VEZ_F`, Z 3150); vnitřek 1,25–9,75 m |
| Brána (návrhy) | počátek v SZ rohu strážní věže (UE 1930 / −3107), `u` podél `Brana_S` k východu, `d` k jihu; výšky absolutně v Z |
| Jména | zdi, stavby a parametry přesně jako v datech (`ZBudova_V`, `Ostroh_Krov`, `cap`, `notches`) |
| Tagy actorů | zřícenina `Zricenina_Ruin` + `cast:<Část>` + `zed:<Zeď>`; stavby `Zricenina_Stavby` + `stavba:<Jméno>`. Build maže jen podle nich. |
| Kód | komentáře a identifikátory bez diakritiky (UE Python konzole); dokumentace česky s diakritikou |
