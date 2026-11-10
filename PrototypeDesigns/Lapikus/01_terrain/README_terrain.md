# 01 Terrain – import terénu a materiál M_Landscape_Forest_Auto (část 1)

Postup pro mapu `LapikusPrototypeMap` (v návodu dříve pracovně `Zricenina_Proto`). Terén se vytvoří z heightmapy a dostane automatický materiál, který podle sklonu míchá trávu, štěrk a kámen.
Řeka a koryto jsou ve složce `02_river`.

## Obsah složky

| Soubor | K čemu |
|---|---|
| `Zricenina_heightmap_505_50cm.png` | Heightmapa k importu (16 bit, 505 × 505 px, 0,5 m/px = 252 × 252 m) |
| `Zricenina_preview_orez.png` | Náhled sklonu terénu: zelená < 8°, oranžová 8–18°, růžová 18–28°, magenta > 28°, vrstevnice po 5 m |
| `M_Landscape_Forest_Auto.md` | Krátký tahák s nastavením materiálu (do dokumentace) |
| `README_terrain.md` | Tento návod |

---

## 1. Nová mapa

1. **File → New Level → Basic.** Neber Open World (World Partition) ani Empty Level.
2. **File → Save Current Level As** do `Content/Skvt/LapikusPrototypeMap` (skutečný stav projektu).
3. V Outlineru smazat **Floor**.
4. **Window → World Settings → GameMode Override = `BP_SkvtGameMode`.**
5. Uložit (Ctrl+S).

## 2. Import landscapu

1. **Landscape mode:** Shift+2 nebo menu módů vlevo nahoře → Landscape.
2. **Manage → New → Import from File.**
3. Nastavit:

| Pole | Hodnota |
|---|---|
| Heightmap File | `Zricenina_heightmap_505_50cm.png` |
| Heightmap Resolution | 505 × 505 |
| Material | `M_Ground_Grass` (dočasně, později `M_Landscape_Forest_Auto`) |
| Layer Alphamap Type | Additive (výchozí) |
| Default Layer | nezaškrtnuto |
| Location | X 0, Y 0, Z **3200** |
| Rotation | 0, 0, 0 |
| Scale | X **50**, Y **50**, Z **12.5** (každou hodnotu potvrdit Enterem) |
| Section Size | 63 × 63 Quads |
| Sections Per Component | 1 × 1 Section |
| Number of Components | 8 × 8 |
| Overall Resolution | 505 × 505 |

4. Kliknout na **Import**.

Pole *Enable Edit Layers* v UE 5.8 není. Edit layers jsou u nového landscapu zapnuté vždy.

**Proč tyto hodnoty:**

- Scale 50 znamená 1 px = 0,5 m.
- Scale Z 12.5 znamená, že celý 16bitový rozsah PNG odpovídá 64 m převýšení.
- Location Z 3200 posune terén tak, že **výška v m × 100 = světové Z v cm**.

## 3. Kontrola

1. Přepnout do **Selection Mode** (Shift+1), vybrat Landscape a stisknout **F**.
2. V Details zkontrolovat Location (0, 0, 3200) a Scale (50, 50, 12.5).
3. **Top view (Alt+J):** ovál plošiny s příkopem je mírně vlevo nahoře od středu, kolem něj vede obloukem koryto.
4. Položit `SM_Cube` na plošinu a stisknout **End**. Z by mělo vyjít ≈ **3130**.

| Místo | X | Y | Z (terén) |
|---|---|---|---|
| Plošina hradu | −1000 | −1250 | ≈ 3130 |
| Hřbet za šíjovým příkopem | 4500 | −2000 | ≈ 3390 |
| Koryto, jih → SV | | | ≈ 330 → 140 |

| Problém | Řešení |
|---|---|
| Terén plochý nebo obří hory | Scale Z není 12.5. Opravit v Details landscapu. |
| Plošina kolem Z 0 | Chybí Location Z 3200. |
| Terén zrcadlově otočený | Bylo zaškrtnuté Flip Y. Importovat znovu. |
| Postava propadá | Landscape → Collision Presets = BlockAll. |

## 4. Player Start

| Varianta | X | Y | Z | Rotation Z |
|---|---|---|---|---|
| Hřbet za příkopem (příchod k hradu) | 4500 | −2000 | 3500 | 180 |
| Plošina hradu | −1000 | −1250 | 3250 | – |

Pro testování: **Play → ⋮ → Spawn Player At → Current Camera Location**.
Záložky kamery uložíš přes **Ctrl+1…9** a skočíš na ně klávesou **1…9**.

---

## 5. Materiál M_Landscape_Forest_Auto – základ

### 5.1 Princip

`VertexNormalWS` → maska **B** (svislá složka normály) = **cos(sklon)**: rovina 1, svislá stěna 0.
Masky vznikají jako `1 − SmoothStep(cos(konec), cos(začátek), cosSklonu)`.

### 5.2 Založení

1. Content Browser → `Skvt/Lapikus` → pravé tlačítko → **Material** → `M_Landscape_Forest_Auto`.
   - V projektu existuje jako **`M_Lanscape_Forest_Auto`** (překlep *Lanscape*). Přejmenovat lze přes pravé tlačítko → Rename; Unreal odkazy opraví sám, pak **Fix Up Redirectors** na složce.
2. Otevřít dvojklikem.

### 5.3 UV souřadnice

`LandscapeLayerCoords`, **Mapping Scale = 8** (opakování textury každé 4 m). Pro přehlednost z ní udělat Named Reroute `UV`.

### 5.4 Textury (StarterContent/Textures)

Texturu stačí přetáhnout z Content Browseru do grafu, Texture Sample vznikne sám.
Případně podržet **T** a kliknout do grafu, pak texturu vybrat v Details → Texture.

| Vrstva | Base Color | Normal |
|---|---|---|
| Tráva | `T_Ground_Grass_D` | `T_Ground_Grass_N` |
| Štěrk | `T_Ground_Gravel_D` | `T_Ground_Gravel_N` |
| Kámen | `T_Rock_Slate_D` | `T_Rock_Slate_N` |

U každého Texture Sample:

- **UVs** ← `UV`. Nikdy ne z RGB jiné textury.
- **Sampler Source:** Shared: Wrap.
- **Sampler Type:** Color u D textur, **Normal** u N textur (obvykle se nastaví samo).

### 5.5 Maska sklonu

```
VertexNormalWS → ComponentMask (jen B) → [cosSklonu]

MaskGravel = 1 − SmoothStep(Min = 0.88, Max = 0.94, cosSklonu)
MaskRock   = 1 − SmoothStep(Min = 0.74, Max = 0.82, cosSklonu)
```

Uzel `1 − x` je **OneMinus**. Výstupy pojmenovat jako Named Reroute `MaskGravel` a `MaskRock`
(pravé tlačítko → **Named Reroute Declaration**, Name + Node Color; použití: pravé tlačítko → napsat název).

### 5.6 Míchání (Lerp: podržet L + klik)

```
Lerp1 = Lerp(A = Grass_D, B = Gravel_D, Alpha = MaskGravel)
Lerp2 = Lerp(A = Lerp1,   B = Rock_D,   Alpha = MaskRock)    → Base Color
Lerp3 = Lerp(A = Grass_N, B = Gravel_N, Alpha = MaskGravel)
Lerp4 = Lerp(A = Lerp3,   B = Rock_N,   Alpha = MaskRock)    → Normal
Constant 0.85 (podržet 1 + klik)                             → Roughness
```

### 5.7 Přiřazení

1. **Apply** a **Save**.
2. Vybrat Landscape a v Details nastavit **Landscape Material** = `M_Landscape_Forest_Auto`.

Materiál jde vyměnit kdykoli, terén se tím nemění.

---

## 6. Ladění přechodů podle sklonu (doporučený způsob)

Ideální je ladit **ve stupních**, v **Material Instance**, se **zapínatelným debug zobrazením**. Změny pak vidíš na terénu hned, bez kompilace.

### 6.1 Parametry ve stupních

Místo pevných čísel ve SmoothStepech:

1. Přidat čtyři **Scalar Parameter** (podržet S + klik):

| Parametr | Výchozí | Význam |
|---|---|---|
| `Gravel_Start_Deg` | 20 | odsud začíná štěrk |
| `Gravel_End_Deg` | 28 | odsud je čistý štěrk |
| `Rock_Start_Deg` | 35 | odsud začíná kámen |
| `Rock_End_Deg` | 42 | odsud je čistý kámen |

2. Za každý parametr dát uzel **Cosine** a v jeho Details nastavit **Period = 360**. Vstup se pak bere ve stupních.
3. Zapojit:
   - `cos(Gravel_Start_Deg)` → **Max**, `cos(Gravel_End_Deg)` → **Min** u SmoothStep pro MaskGravel
   - `cos(Rock_Start_Deg)` → **Max**, `cos(Rock_End_Deg)` → **Min** u SmoothStep pro MaskRock
4. Parametry seskupit: v Details každého parametru nastavit **Group = Slope**.

Pravidlo: `Gravel_Start < Gravel_End < Rock_Start < Rock_End`. Jinak se přechody překryjí a štěrk zmizí.

### 6.2 Debug zobrazení sklonu

1. Přidat **StaticSwitchParameter** `Debug_Slope` (výchozí False).
2. Debug barvy:

```
DebugColor = Lerp(Lerp(zelená (0.2, 0.6, 0.1), žlutá (0.9, 0.7, 0.1), MaskGravel),
                  červená (0.8, 0.1, 0.1), MaskRock)
```

Barvy jsou `Constant3Vector`, podržet **3** + klik.

3. Zapojit: **Lerp2 → False**, **DebugColor → True**, výstup Switche → **Base Color**.

Zapnutý debug ukáže terén obarvený přesně podle toho, kde je tráva / štěrk / kámen. Hranice jsou tak vidět i tam, kde se textury podobají.

### 6.3 Material Instance

1. Pravé tlačítko na `M_Landscape_Forest_Auto` → **Create Material Instance** → `MI_Landscape_Forest_Auto`.
2. Landscape → Details → **Landscape Material = `MI_Landscape_Forest_Auto`**.
3. Otevřít instanci a nechat ji vedle viewportu. Zaškrtnout `Debug_Slope`, pak posouvat stupně ve skupině Slope.

### 6.4 Postup ladění

1. Zapnout `Debug_Slope`, kameru dát na pohled šikmo shora na hrad.
2. Nastavit **kámen:** `Rock_End_Deg` posouvat tak dlouho, až je červená jen na skalní stěně pod hradem a na nejprudších místech výsepného břehu.
3. Nastavit **trávu:** `Gravel_Start_Deg` určuje, kam až sahá tráva. Nivy, plošina a hřbet mají zůstat zelené.
4. Nastavit šířku přechodů:
   - úzký přechod (5°) = ostrá hranice
   - široký přechod (10–15°) = měkké přelivy
5. Vypnout `Debug_Slope`, zkontrolovat výsledek s texturami a pustit **Play**. Z výšky postavy působí přechody jinak než z letu.
6. Výsledné hodnoty zapsat do `M_Landscape_Forest_Auto.md`.

Pro porovnání slouží `Zricenina_preview_orez.png`: má stejný výřez a barevné pásy sklonu.

Debug switch je statický, takže v hotové hře nic nestojí. Lze ho v materiálu nechat napořád.

### 6.5 Tahák cos(úhel)

| úhel | cos | úhel | cos |
|---|---|---|---|
| 15° | 0.966 | 35° | 0.819 |
| 20° | 0.940 | 40° | 0.766 |
| 25° | 0.906 | 45° | 0.707 |
| 30° | 0.866 | 50° | 0.643 |

---

## 7. Další vylepšení (volitelné)

- **Roztažená skála na srázech:** pro kámen použít `WorldAlignedTexture` (triplanar, Texture Size ~400) místo Texture Sample.
- **Opakování textur:** druhý `LandscapeLayerCoords` s jiným Mapping Scale (např. 37) a Multiply s jemnou variací barvy.
- **Štěrk a bahno v korytě:** pokračování ve složce `02_river`.
