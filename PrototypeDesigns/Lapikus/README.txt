Zricenina v meandru - orez 505 px (252 x 252 m, 0,5 m/px)

README_PROJEKT.md - stav projektu, rozhodnuti, souradnice, jak navazat a pregenerovat

01_terrain\  - heightmapa, import landscapu, Player Start, materialu M_Landscape_Forest_Auto
               a ladeni prechodu podle sklonu  -> README_terrain.md
02_river\    - reka (Water Body River), body splinu, skript, maska koryta (sterk / bahno)
               -> README_river_mud.md
03_ruin\     - plan stavby zriceniny: predloha Lapikus, stav ~1540, pudorys, hratelnost, postup -> README_ruin.md
04_forest\   - plan smiseneho lesa: zony, druhy stromu, PCG graf, olse podel reky, checklist
               -> README_forest.md
tools\       - skripty pro pregenerovani terenu, reky, masek a zon (viz README_PROJEKT.md kap. 6)

Zakladni import: Location 0, 0, 3200 / Scale 50, 50, 12.5 / 8 x 8 komponent 63x63
Vyska terenu v m x 100 = svetove Z v cm. Plosina hradu Z ~ 3130 cm.
