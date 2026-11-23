---
# orchestrace
type: knowhow
knowhow_kind: pitfall
tech: [python]
scope: instance
verified: 2026-11-23
validity: valid
updated: 2026-11-23
aliases: []
# hra
domain: structures
---
# Pasti: geometrie a data

<!-- Z KNOWHOW_hrad.md kap. 5.1 (pilot Lapikus, B6). -->

- **`roll` v UE je opačně** než ve výpočtech, kontrolách a náhledech. Do UE jde `-roll` (`zrlib/ue_assets.ue_rotator`) a capture ho vrací zpět (`ue_actors.loose_pose`). Pitch a yaw se shodují. Nové stavby skládej vždy přes `Stone` a `stone_transform`, ne vlastním `Rotator`.
- **`s` podél zdi:** v datech od prvního bodu zdi. Zeď se při stavbě prodlouží o půl tloušťky, `shift`, a `edits` i `span` kamenů jsou posunuté. Při mapování mezi 03 a 05 počítej přes `project_s` na skutečné body.
- **Úpravy ve zřícenině** (`cut`) odebírají celé kameny, které zasahují do oblasti, ne jejich části.
- **Zvětralá koruna a lomové kusy jádra** mají tvar menší než svůj blok. Nic (malta, dřevo) k nim nelícuj na hranu bloku.
- **Zarovnání na řady:** otvory a nadpraží v dostavbě se zarovnávají na řady kamenů. Malé posuny v metrech proto můžou skočit o celou řadu, výsledek ověř.
- **Ruční data:** `ruin_layout.json` a `constructions.json` jsou generované, ruční změny v nich se ztratí.
- **„Zeď o řadu níž“ má tři významy, nejdřív se zeptej, který platí** (15. 11. 2026, `Palac_J`: myšleno bylo zanoření, postaveno ubrání řady).
  - Zanoření celé zdi do země: `z_offset` (m, záporný). Výška jedné řady = výška první celé řady nad terénem dané zdi (u `Palac_J` 0,31 m), pak spáry u země vypadají stejně. Posouvá i otvory, takže `sill` nových otvorů (kapsa) musí být o tolik vyšší.
  - Ubrání horní řady: `drop_rows` (`zr_ruin/post.py` → `drop_top_rows`). Není přesné: kameny zpola přikryté sousedem zůstanou (asi pětina délky), na stupních koruny klesne zeď o dvě řady.
  - Nikdy `raise` se záporným `dh`: posun profilu rozpadu změní i rozebírání líce, koruna klesla o 0 až 2 m podle místa.
- **Místní snížení koruny rozpadem = `breaches`** (`floor` v m od paty před rozebíráním líce). Výsledek jde po řadách (0,3–0,4 m) a závisí na rozebírání, proto ho po změně změř (`run_checks.py --only palac` hlídá přesah komína). `breaches` ani `protect` neposouvají kameny mimo svůj úsek.
- **Kapsa se zarovnává na řady kamene.** Trám do ní navrhuj se spodkem na spáře řad (pozednice kovárny 4,24 m), jinak vyjde kapsa o řadu vedle a trám narazí do kamene.
- **Nový otvor `kapsa` ostatní kameny zdi nemění** (ověřeno na `Palac_J` porovnáním koruny před a po), pokud se přidá na konec seznamu otvorů.
- **Pultová střecha (`pult_roof`): `a` je vždy osa spádu, ne osa `u`.** `pult_geom` skládá rám jako `A, C = (U, V)` nebo `(V, U)` podle `axis`, takže `plan.a`, `openings.a`, `supports.at` a `rafters.a0/a1` leží po spádu a `rafters.pos` napříč. Docstring `pult.py` u `plan` říká „a = osa u, c = osa v“, což platí jen pro `axis = "u"` (kovárna). U domu (`Palac_Obydli_Krov`, `axis = "v"`) je `a` podél `v` (`P(1,0) − P(0,0)` = vektor `v`), krokve stojí na `c` = 10,2–21,3 m podél `u`. U domu je tedy `plan.a` rozsah po `n` a `plan.c` rozsah po `s` (krytina s = 9,8–21,7 patří do `plan.c`). Ověřeno 2026-11-23 testem nad `constructions.json`.
- **Výměny a závěsné tyče dymníku (`ohniste.py`, `trimmers`) fungují jen pod střechou s `axis = "u"`.** Krb má vlastní rám (`a` = `u`, `c` = `v`) a výměny hledá mezi krokvemi podle `chimney.c` a výšku bere z `G["under"](chimney.a)`. Pod střechou s `axis = "v"` se tím porovnává špatná osa: kód nenajde krokve po obou stranách komína a **tiše nepostaví nic** (žádná chyba). Kovárna: 2 výměny + 4 tyče, dům se stejným `trimmers`: 0 dílů. Komín domu (`a` = 16,76) leží mezi krokvemi 16,255 a 17,264. Řešení: buď kód zobecni (převeď střed komína do rámu střechy přes `G["A"]`/`G["C"]`), nebo výměny postav v krovu. Po změně ověř počet dílů `|X*`/`|H*` u obou staveb. Ověřeno 2026-11-23 testem `build_hearth`.
