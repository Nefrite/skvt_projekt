# M_Landscape_Forest_Auto – automatické míchání podle sklonu

Landscape materiál pro lokaci Zřícenina. Podle sklonu terénu míchá trávu, štěrk a kámen, nic se nemaluje ručně.

## Princip

`VertexNormalWS` → `ComponentMask (B)` dává svislou složku normály: rovina = 1, svislá stěna = 0.
Hodnota odpovídá **cos(sklon)**. Masky vznikají přes `SmoothStep(Min, Max)` → `OneMinus`:

- `Max` = začátek přechodu (mírnější úhel)
- `Min` = konec přechodu (strmější úhel)
- Podmínka: `Max` u Rock musí být menší než `Min` u Gravel, jinak se přechody překryjí.

## Nastavení

| Přechod | Maska | Max | Min |
|---|---|---|---|
| tráva → štěrk | Mask Gravel | **0.94** (≈ 20°) | **0.88** (≈ 28°) |
| štěrk → kámen | Mask Rock | **0.82** (≈ 35°) | **0.74** (≈ 42°) |

| Sklon | Povrch |
|---|---|
| 0–20° | tráva |
| 20–28° | tráva → štěrk |
| 28–35° | štěrk |
| 35–42° | štěrk → kámen |
| > 42° | kámen |

### Varianta: tráva do 25°

| Maska | Max | Min |
|---|---|---|
| Mask Gravel | 0.906 (25°) | 0.857 (31°) |
| Mask Rock | 0.82 (35°) nebo 0.788 (38°) | 0.74 (42°) nebo 0.707 (45°) |

## Textury (StarterContent)

| Vrstva | Base Color | Normal |
|---|---|---|
| Tráva | `T_Ground_Grass_D` | `T_Ground_Grass_N` |
| Štěrk | `T_Ground_Gravel_D` | `T_Ground_Gravel_N` |
| Kámen | `T_Rock_Slate_D` | `T_Rock_Slate_N` |

- UV: `LandscapeLayerCoords`, Mapping Scale = 8 (při 0,5 m/quad je opakování 4 m)
- Texture Sample: Sampler Source = Shared: Wrap, u N textur Sampler Type = Normal
- Roughness = 0.85

## Zapojení

```
Lerp1 = Lerp(Grass_D, Gravel_D, MaskGravel)
Lerp2 = Lerp(Lerp1,   Rock_D,   MaskRock)   → Base Color
Lerp3 = Lerp(Grass_N, Gravel_N, MaskGravel)
Lerp4 = Lerp(Lerp3,   Rock_N,   MaskRock)   → Normal
```

## Tahák cos(úhel)

| úhel | cos | úhel | cos |
|---|---|---|---|
| 15° | 0.966 | 35° | 0.819 |
| 20° | 0.940 | 40° | 0.766 |
| 25° | 0.906 | 45° | 0.707 |
| 30° | 0.866 | 50° | 0.643 |
