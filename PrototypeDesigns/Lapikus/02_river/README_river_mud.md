# Řeka a bahnité koryto – Zřícenina v meandru

Podklady a postup pro řeku (Water Body River) a materiál koryta (štěrk / bahno) v mapě `Zricenina_Proto`.
Platí pro landscape z `Zricenina_heightmap_505_50cm.png` (Location 0, 0, 3200, Scale 50 / 50 / 12.5).

## Obsah složky

| Soubor | K čemu |
|---|---|
| `import_river_spline.py` | Python skript: nastaví vybrané řece 27 bodů splinu |
| `Zricenina_505_body_reky.csv` | Stejné body jako tabulka (X/Y/Z v cm, Z = hladina) |
| `Zricenina_505_body_reky.png` | Náhled s očíslovanými body a hradem |
| `T_RiverMask_505.png` | Maska pro materiál: R = dno (štěrk/oblázky), G = bahnitý břeh |
| `T_RiverMask_preview.png` | Náhled masky (šedá = dno, hnědá = bahno) |

Souřadnice: obrázek vpravo = +X, dolů = +Y, střed landscapu = 0, 0.
Díky Location Z = 3200 platí: **výška terénu v m × 100 = světové Z v cm**.

---

## Část 1 – Řeka

### 1.1 Pluginy

1. **Edit → Plugins**, zapnout **Water** a **Python Editor Script Plugin**, restart editoru.
2. Pokud se objeví hláška o chybějícím kolizním profilu *WaterBodyCollision*, kliknout **Add Entry / Fix**.

### 1.2 Vložení řeky bez zásahu do terénu

Koryto už je v heightmapě, řeka nemá terén upravovat.

1. **Selection Mode** (Shift+1). V Landscape modu nejdou vodní actory vybrat.
2. **Window → Place Actors**, najít **Water Body River** a přetáhnout ji do levelu.
3. Hned v Details **odškrtnout Affects Landscape**.
4. Pokud se terén přesto změnil, smazat actor **Landscape_WaterBrushManager**. Případně v Landscape mode → Sculpt → Edit Layers smazat vrstvu, kterou přidala voda.
5. Řece nastavit **Location 0, 0, 0** a **Rotation 0, 0, 0**.

### 1.3 Body splinu skriptem

1. Vybrat **WaterBodyRiver**.
2. **Tools → Execute Python Script…** a vybrat `import_river_spline.py`.
   - Alternativa: Output Log → přepnout Cmd na **Python** a zadat
     `exec(open(r"<cesta>\import_river_spline.py", encoding="utf-8").read())`
3. V Output Logu se objeví hláška o nastavení 27 bodů. Jde vrátit přes Ctrl+Z.

Body jdou ve směru toku (jih → SV) po ~20 m. První a poslední bod jsou vytažené 10 m za okraj mapy.
Hladina je ~25 cm pod hranou koryta: ≈ 437 cm na jihu, ≈ 265 cm na SV.

### 1.4 Parametry vody

Vybrat všechny body splinu (Ctrl+A) a v Details nastavit:

| Parametr | Hodnota |
|---|---|
| River Width | 500 |
| Depth | 150 |
| Velocity | 80 |

Změna těchto hodnot zároveň vynutí přepočet vodní plochy.

### 1.5 Water Zone

Vybrat **WaterZone** a nastavit:

- **Location** 0, 0, 0
- **Zone Extent** 30000 × 30000 (landscape má 25 250 cm)

### 1.6 Řešení problémů

| Problém | Řešení |
|---|---|
| Voda jen na kousku mapy | Zkontrolovat Water Zone (1.5). Vynutit přepočet: změnit River Width, posunout řeku tam a zpět, případně level uložit a znovu otevřít. |
| Černé plochy pod terénem | Dlaždice vody bez dat. Zmizí po přepočtu (viz výše). |
| Voda se rozlévá přes břeh | Snížit Z u bodů v daném místě o 10–20 cm, případně zmenšit River Width. |
| Koryto poloprázdné | Zvednout Z u bodů v daném místě o 10–30 cm. |
| Řeka zasahuje do terénu | Affects Landscape vypnout, smazat WaterBrushManager. |
| Nejde vybrat WaterBodyRiver | Přepnout ze Landscape modu do Selection Mode (Shift+1). Alt+H zobrazí skryté actory. |

---

## Část 2 – Štěrk a bahno v korytě

Maska `T_RiverMask_505.png` pokrývá přesně celý landscape a kopíruje koryto z heightmapy.
Pokud byl spline výrazně posunut mimo koryto, maska ho kopírovat nebude a je potřeba ji přegenerovat.

### 2.1 Import masky

1. Přetáhnout `T_RiverMask_505.png` do Content Browseru, do `Skvt/Maps/Zricenina`.
2. V textuře nastavit:
   - **Compression Settings:** Masks
   - **sRGB:** vypnuto
   - **X / Y-axis Tiling Method:** Clamp

### 2.2 Úprava materiálu `M_Landscape_Forest_Auto`

1. **Souřadnice masky:** přidat druhý `LandscapeLayerCoords`, **Mapping Scale = 504**. Maska se tak roztáhne přesně jednou přes landscape.
2. **Maska:** Texture Sample s `T_RiverMask_505`, do UVs zapojit nové coords (504).
   - Sampler Type: **Masks**
   - Sampler Source: **Shared: Clamp**
   - Named Reroute: **R → `MaskBed`**, **G → `MaskMud`**
3. **Textury dna:** `T_CobbleStone_Pebble_D` a `T_CobbleStone_Pebble_N`, UVs z původních coords (Mapping Scale 8).
4. **Barva bahna:** `Multiply` (RGB z `T_Ground_Gravel_D` × `Constant3Vector` (0.45, 0.36, 0.28)).
5. **Zapojení za stávající řetěz:**

```
Lerp5 = Lerp(Lerp2, Bahno (Multiply), MaskMud)
Lerp6 = Lerp(Lerp5, Pebble_D,         MaskBed)   → Base Color
Lerp7 = Lerp(Lerp4, Pebble_N,         MaskBed)   → Normal
Roughness = Lerp(0.85, 0.4, MaskMud)             (mokré bahno se leskne)
```

6. Apply a Save.

### 2.3 Ladění

- **Moc tmavé nebo světlé bahno:** upravit Constant3Vector.
- **Ostřejší nebo měkčí přechod:** masku přegenerovat s jinou šířkou (stačí napsat Claudovi).
- **Ruční úpravy štětcem:** převést materiál na malované vrstvy (`LandscapeLayerBlend`) a masku použít jako výchozí váhovou mapu vrstvy.
