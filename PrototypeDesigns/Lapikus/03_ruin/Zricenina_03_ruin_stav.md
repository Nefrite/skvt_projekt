# Zřícenina – stav 03_ruin (bloky, půdorys v3)

Doplňuje `Zricenina_README_PROJEKT.md`. Řádek „Hrad“ v jeho kap. 1 je zastaralý, platí tento dokument.

## Jak se teď generuje

- **Generátor z bloků:** `03_ruin/blocks/build_ruin_blocks.py`, stav ~1650. Lomové kameny líce jsou zaoblené zvětralé meshe `SM_RuinStone_*` (OBJ ve `stones/`, automatický import, Nanite, box kolize). Jádro jsou kostky. Ostění tvoří `SM_RuinAshlar`. Materiál `M_RuinStone` + `MI_RuinFace/Core/Frame` vytvoří skript sám. Návod je v `README_bloky.md`.
- **Data:** `tools/ruin/gen_layout.py` + `03_ruin/ruin_layout_draft.json` → `ruin_layout.json`. Mimo UE: `test_openings.py` (žádný kámen ve světlosti otvorů) a `check_blocks.py` (náhled).
- **Terén:** `TERRAIN_FROM_LEVEL = True`. Build změří landscape v levelu a uloží `terrain_from_level.json`. Capture používá stejný uložený stav.
- **Ruční úpravy v levelu:**
  - bourací objemy (Trigger Box s tagy `Ruin_*`),
  - `capture_manual_edits()` → `manual_edits.json`,
  - `tools/ruin/export_level_layout.py` → `layout_from_level.json` (posunuté zdi + body `RuinPt_<Zed>_<NN>`).
- **Kde leží soubory:** `GameDesign/Claude outputs/Zriceni_orez_505` a kopie v `skvt_projekt/PrototypeDesigns/Lapikus` (`03_ruin`, `tools/ruin`). Odtud se spouští v UE.

## Půdorys v3 (11/2026)

- **Strážní věž se dvěma branami** (asi 7 × 7 m, SV od hlavní věže):
  - `Brana_V`: 1. brána z východu, `plinth` 2 m (stojí na nižším terénu, most nebo rampa přes příkop),
  - `Brana_S`: severní stěna,
  - `Brana_J`: 2. brána na západ do uličky podél severní strany věže,
  - `Brana_Jih`: jižní stěna.
- **`Hradba_V`** vede od jižní stěny strážní věže obloukem k JV rohu hlavní věže, asi 5–7 m od věže.
- **`Hradba_Z_S`** končí pootočeným úsekem 08 a napojením na SZ roh strážní věže.
- **Vstup do hlavní věže:** průlom 1,2 × 2,3 m ve `Vez_S` (s = 8 m), mimo osu původních dveří v 1. patře (6,5 m).
- **Příkop:** starý šíjový příkop je zasypaný (terén v UE). Nový se vykope ručně před linií strážní věže a hradby.
- **Předhradí** se zatím nedělá.

## Úpravy zdí (hotové)

- `Hradba_Z_S` úsek 01: šikmý sesuv, stezka k vodě u paláce s prahem asi 0,5 m (`breach` se `slope_r` / `power_r`).
- `Hradba_Z_S` úsek 03: branka zrušena, místo ní střílna. Úsek 04: střílna.
- Vylámané ostění pod stojícím obloukem nebo nadpražím: zůstává zapuštěné jádro a nese oblouk.
- Otvory jsou zarovnané na řady, kameny se kolem otvorů dělí (ID s příponou `.a` / `.b`).

## Otevřené / další kroky

- Patro ve věži: kapsy pro trámy (dvě úrovně, asi 6,3 a 11 m) + volitelně trámy. Původní vstup ve 6,5 m doplnit kapsami pro lávku nebo schody.
- Most nebo rampa k 1. bráně, zbytky mostního pilíře v příkopu.
- Náhledy na skutečném terénu: po buildu poslat `terrain_from_level.json`.
- Nárožní kvádry na zlomech lomené hradby (prosvítá jádro).
