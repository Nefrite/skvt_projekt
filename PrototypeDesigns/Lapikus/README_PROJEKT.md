# Zřícenina v meandru – stav projektu a jak navázat

Prototyp lokace pro kurz *Game design pro začátečníky* (skvt.cz): zřícenina hradu na ostrohu v meandru potoka, zarostlá smíšeným lesem.
Inspirace: zřícenina **Lapikus** nad Plenkovickým potokem (screenshot z mapy se sklonem terénu).

Tento dokument shrnuje vše potřebné k návratu k tématu: kde co je, jaká padla rozhodnutí, co je hotové a jak podklady znovu vygenerovat. Stav: 15. 11. 2026.

**Kam dál:** pravidla, konvence, ověřené pasti a rozhodnutí kolem hradu jsou v `KNOWHOW_hrad.md`. Aktuální stav zříceniny je v `03_ruin\Zricenina_03_ruin_stav.md`. Přehled vybavení (06) je v `FURNISHING.md`.

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
| Les (PCG) | 📝 plán + zóny + spliny, čeká na stažení stromů | `04_forest/README_forest.md`, `04_forest/README_assets_stromy.md` |
| Zřícenina hradu (03) | ✅ postavená v UE skriptem z jednotlivých kamenů (stav ~1650): 18 zdí, asi 23 000 bloků, tři části (`Obvod`, `Palac`, `Ostroh`) | `03_ruin/Zricenina_03_ruin_stav.md`, `03_ruin/blocks/README_bloky.md` |
| Dostavby „druhého zabydlení“ (05) | ✅ dřevo ve věži, krov, kamenná dostavba a podlaha u ostrohu, suť s fyzikou | `05_constructions/README_constructions.md` |
| Knihovna meshí a props | ✅ 111 meshí v UE (kameny, hraněné dřevo, kulatina, kůra, proutí, lano, plátno, props kovárny a obydlí) s vlastními texturami a materiály | `05_constructions/README_constructions.md`, `CHECKLIST_assets_navrhy.md` |
| Další stavby (věž, palác, brána, nádvoří) | 📝 specifikace hotové, nepostaveno; chybí nové typy staveb v 05 a úpravy 03 | `new_designs/navrh_*.md`, `CHECKLIST_assets_navrhy.md` |

### Další kroky (doporučené pořadí)

1. **Les:** rozhodnout, jak řešit velikost stromů v gitu (LFS / `.gitignore`), stáhnout Quixel Megaplants, zapnout PCG, vložit spliny zón a postavit `PCG_Forest` (checklist v `04_forest\README_forest.md`).
2. **Koryto:** štěrk a bahno v materiálu (`02_river` kap. 2), případně stezka z `T_ForestZones_505.png` (kanál B).
3. **Hrad:** stavby z návrhů v `new_designs` podle priorit v `CHECKLIST_assets_navrhy.md` (kovárna a dům v paláci, přístřešek na věži, stráž na bráně). Potřebují nové typy staveb v 05 (`pult_roof`, `log_wall`, `hearth`…), rozmístění props a přepínač etap.
4. **Atmosféra:** Exponential Height Fog, nízké slunce, `P_Ambient_Dust`; oheň a kouř pro kovárnu a ohniště.

---

## 2. Unreal projekt

| Co | Kde / hodnota |
|---|---|
| Repo | `C:\Users\JDr\GitHub\skvt_projekt`, větev **`lapikus-prototype`** |
| Hlavní složka prototypu | `skvt_projekt\PrototypeDesigns\Lapikus` (skripty, data, dokumentace). `GameDesign\Claude outputs\Lapikus` je archiv starších kopií, neaktualizuje se. |
| Engine | Unreal Engine **5.8** |
| Mapa | `Content/Skvt/LapikusPrototypeMap` (výchozí mapa projektu zůstává `SkvtProjectMap`) |
| Materiál terénu | `Content/Skvt/Lapikus/M_Lanscape_Forest_Auto` (pozor: v názvu překlep *Lanscape*) |
| Assety hradu | `Content/Skvt/Lapikus/Ruin`: `Stones`, `Wood`, `Wattle`, `Textile`, `Props` (meshe `SM_Ruin*`), `Textures`, `Materials`. Všechno generuje a importuje skript, ručně se sem nic nepřidává. |
| Actory hradu v levelu | tagy `Zricenina_Ruin` (zřícenina) a `Zricenina_Stavby` (dostavby), složky Outlineru `Stavby/...`. Level je celý generovaný, ruční úpravy se ukládají přes capture. |
| GameMode | `BP_SkvtGameMode` (World Settings → GameMode Override) |
| Pluginy | **Water**, **Python Editor Script Plugin**; pro les navíc **PCG** |

Pluginy zatím nejsou zapsané v `skvt_projekt.uproject`. Po zapnutí zkontroluj, že se `.uproject` uložil a je commitnutý, jinak se po klonování nenačtou.

**Git:**

- Repo nemá Git LFS, GitHub odmítne soubor > 100 MB. Týká se hlavně stažených stromů (viz `04_forest\README_forest.md` kap. 3 a `README_assets_stromy.md`).
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
| Hrad procedurálně z kamenů (Python v UE), ne blockout z kostek | Zeď jde rozpadnout, vybourat a upravit v datech; ruční zásahy se ukládají přes capture |
| Zřícenina (03) a dostavby (05) oddělené | Dostavby jdou ladit bez přegenerování hradu |

Rozhodnutí kolem hradu (props, kulatina, dům v prostřední místnosti paláce, způsob importu meshí, dva celkové buildy) jsou s daty v `KNOWHOW_hrad.md`, kap. 7.

---

## 5. Struktura složky

```
skvt_projekt\PrototypeDesigns\Lapikus\
├─ README_PROJEKT.md        ← tento dokument
├─ README.txt               ← rychlý rozcestník
├─ KNOWHOW_hrad.md          společné know-how: pravidla, konvence, pasti, rozhodnutí
├─ AGENT_*.md               instrukce pro agenty (architekt, game design, stavitel, furnisher = vybavení)
├─ CHECKLIST_assets_navrhy.md   co návrhy potřebují (assety, typy staveb, úpravy 03) a co je hotové
├─ build_normal.py          UE: celý hrad (03) + všechny stavby (05) + vybavení (06), aditivně
├─ build_fullscope.py       UE: oprava – smaže generované actory a meshe a vše postaví znovu
├─ 01_terrain\              heightmapa 505, náhled sklonu, návod importu a materiálu
├─ 02_river\                body a skript řeky, maska koryta, návod
├─ 03_ruin\                 zřícenina: plán, stav, data; blocks\ = generátor z kamenů (build_ruin_blocks.py, casti\*.py)
├─ 04_forest\               plán lesa, zóny, spliny, maska zón, náčrt, olše u řeky, assety stromů
├─ 05_constructions\        dostavby: build_constructions.py, stavby\*.py, data, náhledy
├─ 06_furnishing\           vybavení (přenosné props): build_furnishing.py, vybaveni\*.py, data
├─ new_designs\             návrhy dalších staveb (specifikace architekta + náčrty)
├─ zrlib\                   sdílená knihovna skriptů 03 + 05 (config.py = vzhled a verze, pipeline.py = spouštění)
├─ meshes\                  OBJ knihovních meshí podle kategorie (stone, wood, wattle, textile, props); nejsou v gitu, generuje tools\meshes\gen_meshes.py
├─ textures\                procedurální textury; nejsou v gitu, generuje tools\textures\gen_textures.py
└─ tools\                   generátory (terén, řeka, zóny, ruin\, constructions\, meshes\, textures\) a kontroly (checks\)
```

`GameDesign\Claude outputs\Lapikus` je archiv starších kopií dokumentů a skriptů; neaktualizuje se a nic se tam nepřidává.

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
| 5. Zóny lesa | `python 2_derive_505.py zones <dir> 04_forest\nacrt_zony.png` | `Zricenina_les_plan.png`, `T_ForestZones_505.png`, `Zricenina_les_zony.csv`, `zone_points.json` (vložit do `ZONES` v `import_zone_splines.py`) |

**Hrad** (z kořene prototypu, podrobně `AGENT_Stavitel_hrad.md` kap. 4–6):

| Krok | Příkaz | Výstup |
|---|---|---|
| Data zříceniny | `python tools/ruin/gen_layout.py 03_ruin/ruin_layout_draft.json 01_terrain/Zricenina_heightmap_505_50cm.png 03_ruin/blocks/ruin_layout.json` | `ruin_layout.json` (jen při změně zříceniny nebo sdíleného specu) |
| Data dostaveb | `python tools/constructions/gen_constructions.py 03_ruin/ruin_layout_draft.json 05_constructions/constructions.json` | `constructions.json` |
| Data vybavení | `python tools/furnishing/gen_furnishing.py` | `06_furnishing/furnishing.json` |
| Meshe | `python tools/meshes/gen_meshes.py` | `meshes/<kategorie>/*.obj` |
| Textury | `python tools/textures/gen_textures.py` | `textures/*.png` |
| Kontroly bez UE | `python tools/checks/run_checks.py` | otvory, kameny bez podpory, průniky u ostrohu |
| Stavba v UE | **Tools → Execute Python Script →** `build_normal.py` (nebo jen část: `03_ruin/blocks/casti/*.py`, `05_constructions/stavby/*.py`, `06_furnishing/vybaveni/*.py`) | actory v levelu; chybějící meshe a textury se doimportují |
| Oprava v UE | `build_fullscope.py` | smaže generované actory a meshe a postaví vše znovu (při poškozených assetech) |

Ruční úpravy v levelu se ukládají stejným skriptem s `MODE = "capture"` (vybavení: `06_furnishing/capture_furnishing.py` nebo `vybaveni/<Skupina>_Capture.py`), vždy před dalším generováním. `manual_edits.json` a `constructions_edits.json` se nepřepisují.

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
- Hrad: nerozhodnuté body (stan na nádvoří, umístění kovárny, výstup na podestu brány, přepínání etap, cisterna) jsou v `CHECKLIST_assets_navrhy.md` kap. 9 a `KNOWHOW_hrad.md` kap. 7.
