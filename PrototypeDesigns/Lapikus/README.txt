Zricenina v meandru - orez 505 px (252 x 252 m, 0,5 m/px)

README_PROJEKT.md - stav projektu, rozhodnuti, souradnice, jak navazat a pregenerovat
KNOWHOW_hrad.md   - hrad: pravidla, konvence, overene pasti a rozhodnuti na jednom miste
AGENT_*.md        - instrukce pro agenty (architekt, game design, stavitel)
CHECKLIST_assets_navrhy.md - co navrhy potrebuji a co je hotove

01_terrain\  - heightmapa, import landscapu, Player Start, materialu M_Landscape_Forest_Auto
               a ladeni prechodu podle sklonu  -> README_terrain.md
02_river\    - reka (Water Body River), body splinu, skript, maska koryta (sterk / bahno)
               -> README_river_mud.md
03_ruin\     - zricenina hradu (stav ~1650): predloha Lapikus, pudorys, hratelnost -> README_ruin.md,
               aktualni stav -> Zricenina_03_ruin_stav.md, generator z kamenu -> blocks\README_bloky.md
04_forest\   - plan smiseneho lesa: zony, druhy stromu, PCG graf, olse podel reky, checklist
               -> README_forest.md
05_constructions\ - dodatecne stavby zriceniny (drevo, dostavby, sut) -> README_constructions.md
build_normal.py    - UE: cely hrad (03) + vsechny stavby (05), aditivne (jen chybejici / zastarale assety)
build_fullscope.py - UE: oprava - smaze generovane actory a meshe a vse postavi znovu
zrlib\       - sdilena knihovna skriptu 03 + 05 (config.py = vzhled, pipeline.py = spousteni)
new_designs\ - navrhy dalsich staveb (vez, palac, brana, nadvori), zatim nepostavene
meshes\, textures\ - vygenerovane OBJ a PNG (nejsou v gitu)
tools\       - generatory (teren, reka, zony, data hradu, meshe, textury) a kontroly (viz README_PROJEKT.md kap. 6)

Zakladni import: Location 0, 0, 3200 / Scale 50, 50, 12.5 / 8 x 8 komponent 63x63
Vyska terenu v m x 100 = svetove Z v cm. Plosina hradu Z ~ 3130 cm.
