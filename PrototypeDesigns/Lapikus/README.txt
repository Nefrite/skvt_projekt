Zricenina v meandru - orez 505 px (podle tveho nahledu Zricenina_preview_orez.png)

Orez v souboru 757 px: levy horni roh (74, 57)  -> v puvodni 1009 px: (326, 309)
Rozmer: 505 x 505 px, 0,5 m/px = 252 x 252 m

================================================================
IMPORT (Landscape mode -> Manage -> New -> Import from File)
----------------------------------------------------------------
Heightmap File         Zricenina_heightmap_505_50cm.png
Material               M_Ground_Grass (StarterContent)
Enable Edit Layers     ZAPNUTO (kvuli Water pluginu)
Location               X 0   Y 0   Z 3200
Rotation               0 0 0
Scale                  X 50  Y 50  Z 12.5
Section Size           63 x 63 Quads
Sections Per Component 1 x 1
Number of Components   8 x 8
Overall Resolution     505 x 505      (Fit To Data by to melo nastavit samo)
================================================================

Diky Location Z = 3200 plati: vyska terenu v metrech x 100 = svetove Z v cm.
  teren min ~ 140 cm (koryto u SV okraje), max ~ 4110 cm (svah vpravo nahore)
  plosina hradu  Z ~ 3130 cm, stred plosiny X ~ -1000, Y ~ -1250 cm
  (souradnice predpokladaji landscape vycentrovany na Location 0,0 - vychozi chovani;
   kdyby lezel jinak, pricti jeho posun)

Osy: obrazek vpravo = +X, obrazek dolu = +Y.

================================================================
REKA (Water Body River)
----------------------------------------------------------------
Zricenina_505_body_reky.csv  = 13 bodu splinu po ~40 m, ve smeru toku
                               (jih -> SV), X/Y/Z v cm, Z = hladina
Zricenina_505_body_reky.png  = nahled s ocislovanymi body a hradem

Hladina klesa z ~416 cm (bod 1, dolni okraj) na ~221 cm (bod 13, pravy horni okraj).
Prvni a posledni bod vytahni kousek za okraj landscapu, at reka neskonci v terenu.
Sirka reky ~ 500-600 cm, hloubka ~ 150 cm.
