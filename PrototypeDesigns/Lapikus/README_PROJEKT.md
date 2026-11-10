# Zřícenina v meandru – stav projektu a jak navázat

Prototyp lokace pro kurz *Game design pro začátečníky* (skvt.cz): zřícenina hradu na ostrohu v meandru potoka, zarostlá smíšeným lesem.
Inspirace: zřícenina **Lapikus** nad Plenkovickým potokem (screenshot z mapy se sklonem terénu).

Tento dokument shrnuje vše potřebné k návratu k tématu: kde co je, jaká padla rozhodnutí, co je hotové a jak podklady znovu vygenerovat.

---

## 1. Stav

| Oblast | Stav | Složka / návod |
|---|---|---|
| Terén (heightmapa, import) | ✅ hotovo, naimportováno v UE | `01_terrain/README_terrain.md` |
| Materiál terénu podle sklonu (tráva / štěrk / kámen) | ✅ základ hotový | `01_terrain/README_terrain.md`, `01_terrain/M_Landscape_Forest_Auto.md` |
| Ladění přechodů ve stupních + debug | 📝 návod připraven, neověřeno v UE | `01_terrain/README_terrain.md` kap. 6 |
| Player Start, procházení | ✅ návod, nastaveno | `01_terrain/README_terrain.md` kap. 4 |
| Řeka (Water Body River) | ✅ vložena a odladěna | `02_river/README_river_mud.md` |
| Štěrk / bahno v korytě (maska) | ⏸ odloženo, podklady hotové | `02_river/README_river_mud.md` kap. 2 |
| Les (PCG) | 📝 plán + zóny + spliny, čeká na stažení stromů | `03_forest/README_forest.md` |
| Hrad (blockout, ruina) | ☐ nezačato | – |

### Další kroky (doporučené pořadí)

1. **Les:** rozhodnout, jak řešit velikost stromů v gitu (LFS / `.gitignore`), stáhnout Quixel Megaplants, zapnout PCG, vložit spliny zón a postavit `PCG_Forest` (checklist v `03_forest`).
2. **Koryto:** štěrk a bahno v materiálu (`02_river` kap. 2), případně stezka z `T_ForestZones_505.png` (kanál B).
3. **Hrad:** blockout z `LevelPrototyping` kostek na plošině (Z ≈ 3130), boolean v Modeling módu, materiály kamene, sutě `SM_Rock`.
4. **Atmosféra:** Exponential Height Fog, nízké slunce, `P_Ambient_Dust`.

---

## 2. Unreal projekt

| Co | Kde / hodnota |
|---|---|
| Repo | `C:\Users\JDr\GitHub\skvt_projekt`, větev **`lapikus-prototype`** |
| Engine | Unreal Engine **5.8** |
| Mapa | `Content/Skvt/LapikusPrototypeMap` (výchozí mapa projektu zůstává `SkvtProjectMap`) |
| Materiál terénu | `Content/Skvt/Lapikus/M_Lanscape_Forest_Auto` (pozor: v názvu překlep *Lanscape*) |
| GameMode | `BP_SkvtGameMode` (World Settings → GameMode Override) |
| Pluginy | **Water**, **Python Editor Script Plugin**; pro les navíc **PCG** |

Pluginy zatím nejsou zapsané v `skvt_projekt.uproject`. Po zapnutí zkontroluj, že se `.uproject` uložil a je commitnutý, jinak se po klonování nenačtou.

**Git:**

- Repo nemá Git LFS, GitHub odmítne soubor > 100 MB. Týká se hlavně stažených stromů (viz `03_forest` kap. 3).
- `.gitignore` ignoruje `SourceArt/**/*.png`. Pokud se podklady přesunou do repa, použij jinou složku, např. `LevelSource/Zricenina/`.

---

## 3. Souřadnice a klíčová čísla

| | |
|---|---|
| Heightmapa | `Zricenina_heightmap_505_50cm.png`: 16 bit, 505 × 505 px, 0,5 m/px = **252 × 252 m** |
| Import | Location **0, 0, 3200**, Scale **50 / 50 / 12.5**, 63×63 quads, 1×1 section, **8 × 8** komponent |
| Výšky | díky Z 3200: **výška v m × 100 = světové Z v cm** (rozsah PNG = 64 m) |
| Osy | obrázek vpravo = +X, dolů = +Y, střed landscapu = 0, 0 |
| Převod px → UE | X = (px − 252) × 50 cm, Y = (py − 252) × 50 cm |
| Plošina hradu | X ≈ −1000, Y ≈ −1250, **Z ≈ 3130** |
| Hřbet za příkopem | X 4500, Y −2000, Z ≈ 3390 (Player Start Z 3500, Yaw 180) |
| Hladina řeky | ≈ 437 cm (jih, proti proudu) → ≈ 265 cm (SV); řeka teče od jihu k SV |
| Řeka | 27 bodů splinu, River Width 500, Depth 150, Velocity 80, **Affects Landscape vypnuto**, Water Zone 0,0,0 / 30000 × 30000 |

---

## 4. Rozhodnutí a proč

| Rozhodnutí | Důvod |
|---|---|
| Terén procedurálně z reálné mapy, ne skutečný výškopis | Rychlé, upravitelné; tvar ostrohu, meandru a srázů podle mapy sklonu |
| Přirozený meandr: výsepný a jesepní břeh, spád, eroze | Původní pravoúhlá řeka nevypadala reálně |
| Ořez 505 px (252 m) z 1009 px (504 m) | Méně dat, okraje vlevo a nahoře nepotřebné; 505 = 8 × 63 + 1 (platná velikost UE) |
| Basic level, ne Open World | World Partition je na 252 m zbytečný |
| Řeka **bez** zásahu do terénu | Koryto už je v heightmapě; Water brush ho jen kazil |
| Body řeky skriptem | UE neumí import splinu z CSV |
| Hladina = hrana koryta − 25 cm | První verze (dno + 0,8 m) nechávala koryto poloprázdné |
| Automatický materiál podle sklonu (ne malování) | Funguje hned, ladí se parametry; malované vrstvy lze přidat později |
| Štěrk / bahno a zóny lesa jako masky přes celý landscape | Přesně sedí na terén, generují se z dat |
| Les přes PCG, zóny jako spliny s tagy | Automatické pokrytí; tvar zón jde dolaďovat tahem bodů |
| Quixel Megaplants (buk, javor, osika, líska, olše) | Zdarma, evropské druhy, Nanite foliage; kosodřevina v nich chybí |
| Hrad: obrys podle náčrtu, končí u řeky | Původní obdélník zasahoval za řeku na protější břeh |

---

## 5. Struktura složky

```
Claude outputs\Zriceni_orez_505\
├─ README_PROJEKT.md        ← tento dokument
├─ README.txt               ← rychlý rozcestník
├─ 01_terrain\              heightmapa 505, náhled sklonu, návod importu a materiálu
├─ 02_river\                body a skript řeky, maska koryta, návod
├─ 03_forest\               plán lesa, zóny, spliny, maska zón, náčrt
└─ tools\                   skripty pro přegenerování všech podkladů
```

Starší mezivýstupy (pro historii, není třeba je používat):

- `Claude outputs\Zricenina\` – plná mapa 1009 px (504 m) + původní generátor
- `Claude outputs\Zricenina_orez\` – ořez 757 / 379 px
- volné soubory přímo v `Claude outputs\` – kopie, které jsi sem uložil při práci

---

## 6. Přegenerování podkladů (`tools\`)

Všechno je deterministické: stejné skripty dají bit po bitu stejné soubory.

**Požadavky:** Python 3.10+, `pip install numpy scipy pillow scikit-image numba matplotlib`

| Krok | Příkaz | Výstup |
|---|---|---|
| 1. Terén 504 m | `python 1_gen_heightmap_1009.py <dir>` | `Zricenina_heightmap_1009.png`, `H.npy`, `S.npy` (osa řeky) |
| náhled | `python preview_slope.py <dir>` | `Zricenina_preview_full.png`, `_crop.png` |
| 2. Ořez 505 | `python 2_derive_505.py crop <dir>` | `Zricenina_heightmap_505_50cm.png`, `Zricenina_preview_orez.png` |
| 3. Body řeky | `python 2_derive_505.py river <dir>` | `Zricenina_505_body_reky.csv`, `river_points.txt` (vložit do `POINTS` v `import_river_spline.py`) |
| 4. Maska koryta | `python 2_derive_505.py mask <dir>` | `T_RiverMask_505.png` |
| 5. Zóny lesa | `python 2_derive_505.py zones <dir> 03_forest\nacrt_zony.png` | `Zricenina_les_plan.png`, `T_ForestZones_505.png`, `Zricenina_les_zony.csv`, `zone_points.json` (vložit do `ZONES` v `import_zone_splines.py`) |

**Co kde měnit:**

- **Tvar řeky, ostrohu, výšky:** `1_gen_heightmap_1009.py`
  - `trace_px` / `up` / `down` – trasa toku
  - `axis_px` a `top` – hřbet ostrohu a jeho výšky
  - plošina 30 m, příkop 6 m
- **Ořez:** `CROP0` v `2_derive_505.py`. Velikost musí být n × 63 + 1.
- **Zóny lesa:** nakreslit nový náčrt do screenshotu `Zricenina_les_plan.png` stejnými barvami:
  - červená = hrad
  - oranžová = osa cesty
  - fialová = skalnaté podloží
- **Jiný výřez nebo velikost screenshotu náčrtu:** upravit `SHOT_OFF` / `SHOT_SIZE`.

Po změně terénu je potřeba přegenerovat i kroky 2–5 a heightmapu v UE znovu naimportovat (Landscape → Manage → Import do vrstvy *Layer*).

---

## 7. Otevřené otázky

- Git LFS vs. `.gitignore` pro stromy z Fabu.
- Kosodřevina pro zónu K: najít asset (Fab: „mountain pine“, „pinus mugo“), nebo nahradit keři.
- Zbytek ostrohu mezi hradem a řekou je teď les. Má být spíš holý (výhled z hradu)? Případně přidat spline `PCG_NoForest`.
- Ověřit v UE 5.8:
  - uzel **Cosine → Period** (ladění ve stupních)
  - uzly PCG pro uzavřené spliny jako plochu
- Plavání postavy ve vodě (Water plugin + Character Movement).
