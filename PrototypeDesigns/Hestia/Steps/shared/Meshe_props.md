---
# orchestrace
type: step
validity: valid
aliases: []
step_kind: shared
updated: 2026-11-23
# hra
domains: [structures]
---
# Meshe props (procedurální modely vybavení a staveb)

<!-- Sdílená knihovna meshí; vzniklo tematickým rozdělením [[03_ruin]] a [[05_constructions]] 2026-11-23 (G14b). -->

## Co poskytuje
Vlastní procedurální modely props (`tools\meshes\mesh_props.py`, kategorie `props`). Katalog požadavků a nových props: [[Katalog_props]]; ostatní knihovní meshe: [[Meshe]].

### Props

**Props** (`tools\meshes\mesh_props.py`, kategorie `props`, OBJ v `meshes\props`, v UE `/Game/Skvt/Lapikus/Ruin/Props`): vlastní procedurální modely, dílec = `Stone` se `shape` z `LIB_SHAPES`, rozměry v `LIB_MESHES`. Slot `Wood` = materiál dílce (`cat`, úprava dřeva), ostatní sloty pevné.

| `shape` | Mesh | Rozměr (cm) | Sloty |
|---|---|---|---|
| `stump` | `SM_RuinStump_A–B` | Ø 50 × 47 | Wood, EndGrain, Bark |
| `anvil` | `SM_RuinAnvil` | 59 × 18 × 24 | IronClean |
| `bellows` | `SM_RuinBellows` (měch na rámu s příčkami, výfučna, horní deska s rukojetí z jednoho kusu) | 210 × 85 × 139 | Wood, Iron, Leather |
| `barrel` | `SM_RuinBarrel` (kalicí sud z 18 dužin se spárami, dno, obruče, voda) | Ø 61 × 80 | Wood, EndGrain, Iron, Water |
| `grindstone` | `SM_RuinGrindstone` (kotouč na ose v ložiskách, spodek 3 cm ve vodě, rám s příčkami, ruční klika, koryto na 4 nohách) | 120 × 86 × 105 | Wood, Iron, Sandstone, Water |
| `grindstone_treadle` | `SM_RuinGrindstoneTreadle` (šlapací: kliková páka, ojnice, šlapadlo na čepu u zadní nohy, strana +Y) – **použít v kovárně** | 120 × 86 × 105 | Wood, EndGrain, Iron, Sandstone, Water |
| `stool` | `SM_RuinStool` (třínohá stolička k brusu) | 35 × 33 × 45 | Wood, EndGrain |
| `workbench` | `SM_RuinWorkbench` (ponk se svěrákem, podélná příčka prostředkem) | 222 × 86 × 85 | Wood, Iron |
| `tongs`, `hammer`, `chisel` | `SM_RuinTongs`, `SM_RuinHammer` (kladivo s příčným penem: hlava 11 cm, tlouk a pena souměrně kolem oka, toporo prochází okem), `SM_RuinChisel` | 50, 36, 21 délka | IronClean (kladivo + Wood, EndGrain) |
| `mallet` | `SM_RuinMallet` (dřevěná palice do jedné ruky: hlava Ø 9 × 14 cm, na koncích železné obruče proti roztřepení) | 10 × 35 × 14 | Wood, EndGrain, IronClean |
| `nail_hammer` | `SM_RuinNailHammer` (tesařské kladivo na hřebíky: kulatá úderná plocha, rozpolcený drápák zahnutý k toporu, toporo u hlavy tenčí, prochází okem) | 3 × 34 × 11 | Wood, EndGrain, IronClean |
| `broadaxe` | `SM_RuinBroadaxe` (širočina: ostří ~27 cm s bradou k toporu, broušená jen z líce, plynulý náběh z oka do čepele, toporo 70 cm vyhnuté od rubu, prochází okem) | 7 × 72 × 25 | Wood, EndGrain, IronClean |
| `axe` | `SM_RuinAxe` (sekera na štípání: klínovitá hlava s týlem, ostří ~11 cm, čepel vychází z oka, toporo 75 cm prochází okem) | 5 × 77 × 19 | Wood, EndGrain, IronClean |
| `crosscut_saw` | `SM_RuinCrosscutSaw` (dvoumužná pila: list 152 cm s břichem a zuby, ke koncům užší, svislé rukojeti 3 cm od konců listu) | 151 × 4 × 28 | Wood, EndGrain, IronClean |
| `bed`, `bed_folded` | `SM_RuinBed` (lůžko: nohy, čelo v hlavě, bočnice, laťky, sypaná sláma, houně přes slámu s převisem do stran), `SM_RuinBedFolded` (houně složená v nohách) | 200 × 87 × 62 | Wood, Straw, Wool |
| `table` | `SM_RuinTable` (stůl: deska ze 3 prken, rozkročené nohy, luby, příčky dole) | 120 × 70 × 76 | Wood |
| `chest` | `SM_RuinChest` (truhla: prkna, nožky, zavřené víko, železné pásy, závěs s okem na zámek, držadla) | 95 × 55 × 51 | Wood, Iron |
| `shelf` | `SM_RuinShelf` (police na osobní věci, stojí u zdi stranou +Y: 2 bočnice, 3 desky, zadní lišta) | 100 × 28 × 90 | Wood |
| `door` | `SM_RuinDoor` (dveře 1,0 × 2,2 m: 4 prkna, zezadu 3 svlaky a vzpěry Z, na líci (−Y) pásové závěsy na ose X = −50, kruh, zástrčka) | 102 × 9 × 219 | Wood, Iron |
| `shutter` | `SM_RuinShutter` (okenice 60 × 60: 3 prkna, 2 svlaky, závěsy na ose X = −30, kolík; pro okénko 50 × 50 škálovat 0,83) | 61 × 8 × 59 | Wood, EndGrain, Iron |
| `nail_header` | `SM_RuinNailHeader` | 25 × 6 × 1,5 | IronClean |
| `coal_box` | `SM_RuinCoalBox` (truhlík s uhlím: ~420 kousků na tmavém podkladu, bez víka) | 81 × 121 × 80 | Wood, Charcoal |
| `coal_box_lid` | `SM_RuinCoalBoxLid` (volné víko truhlíku bez pantů: 3 prkna, 2 lajsny zespodu, držadlo; položit bokem nebo na truhlík) | 80 × 120 × 11 | Wood |
| `woodpile` | `SM_RuinWoodpile` (štípaná polena, délka podél Y) | 191 × 65 × 136 | Wood, EndGrain, Bark |
| `iron_bars` | `SM_RuinIronBars` (svazek prutů) | 103 × 9 × 4 | Iron |
| `basket` | `SM_RuinBasket` | Ø 44 × 37 | Wattle |
| `ladder` | `SM_RuinLadder` (tyče s kůrou, příčle po 30 cm) | 450 × 54 × 8 | Wood, EndGrain, Bark |
| `camp_bed`, `camp_bed_folded` | `SM_RuinCampBed`, `SM_RuinCampBedFolded` (lůžko ve stanu z klád a tyčí s kůrou, sláma, houně; hlava −X) | 199 × 76 × 29 (32) | Wood, EndGrain, Bark, Straw, Wool |
| `chest_small` | `SM_RuinChestSmall` (truhlička, zámek −Y) | 59 × 38 × 32 | Wood, Iron |
| `bundle` | `SM_RuinBundle` (vak na boku, hrdlo +X, popruh +Y) | 76 × 43 × 23 | Sackcloth, Rope |
| `bed_large` | `SM_RuinBedLarge` (postel hosta, čelo 95 cm na −X, slamník, polštář, houně) | 250 × 109 × 95 | Wood, Wool, Canvas |
| `chest_locked` | `SM_RuinChestLocked` (kovaná truhla, klenuté víko, zámek −Y, závěsy +Y) | 94 × 54 × 51 | Wood, EndGrain, IronClean |
| `armor_stand` | `SM_RuinArmorStand` (stojan na brnění, čelo −Y; body pro brnění `ARMOR_STAND_POINTS`) | 60 × 60 × 175 | Wood, EndGrain |

Karty těchto props (osy, funkční body, použití, úpravy) jsou v [[Katalog_props]].

- Materiály lůžka: `MI_RuinStraw` (sláma, textura `T_RuinStraw`), `MI_RuinWool` (houně z nebarvené vlny, `T_RuinWool`); sloty Straw, Wool.
- Materiály props: dvě železa – `MI_RuinIron` (slot Iron, s patinou tlumeně hnědé rzi, `Metallic` 0,5: kování, obruče, osy, pruty) a `MI_RuinIronClean` (slot IronClean, bez rzi, `Metallic` 0,8: nářadí a kovadlina); barva v textuře `T_RuinIron` / `T_RuinIronClean` (`TEX_VERSION` 4, `MAT_VERSION` 10, `MAT_RESET` iron 10), `MI_RuinLeather`, `MI_RuinSandstone` (StarterContent), `MI_RuinWater`, `MI_RuinCharcoal` (černou barvu dává tint, textura je jen světlý detail). Parametr `Metallic` je nově v `M_RuinStone` (výchozí 0, kámen a dřevo beze změny; `MAT_VERSION` 8 → master se při buildu přestaví).
- Náhled: `05_constructions\Props_kovarna_nahled.png`, textury `Props_textury_nahled.png`.

- **Materiály:** `MI_RuinRope`, `MI_RuinWattle`, `MI_RuinDaub`, `MI_RuinChinking` (výplň spár srubu, textura mazaniny) na `M_RuinStone`; plátno `MI_RuinCanvas` na novém `M_RuinCloth` (oboustranný). Vzhled v `MAT_LOOK` (`zrlib\config.py`).
- **Skvrny plachty:** textura plátna (dlaždice 25 cm) je bez skvrn, jinak by se opakovaly. Skvrny a zašednutí dává velká textura `T_RuinCanvasMacro` (dlaždice 4 m), kterou `M_RuinCloth` přimíchá: `MacroAmount` (síla, výchozí 0,6), `MacroTiling` (0,25 = dlaždice 4 m).
- **Plátno na míru:** `mesh_textile.make_canvas(okap0, okap1, hřeben0, hřeben1, rafters=…, sag=…)` vrátí plachtu prověšenou mezi tyčemi (cm, souřadnice stavby), `write_canvas` ji zapíše jako OBJ. Ukázka `SM_RuinCanvasSample_A` (3 × 2,4 m, 5 tyčí, sklon 22,6°). Stavba ji používá přes `canvas_vez` + `write_fitted` (OBJ vystředěný na bounding box + `<mesh>.json` se středem a rozměrem v osách stavby; typ `canvas_shelter` mesh podle něj posadí).
- **Vítr:** `M_RuinCloth` posouvá vrcholy podél normály: `WindAmount` (cm, výchozí 0 = staticky), `WindSpeed`, `WindScale`. Zapnout v `MI_RuinCanvas` nebo v `MAT_LOOK["canvas"]`. Úchyty na tyčích se zatím hýbou stejně jako zbytek plachty, proto jen malé hodnoty (1–3 cm).

Master `M_RuinStone` má kvůli tomu parametry `Desaturate` (odbarvení textury, 0–1) a `DustAmount` / `DustTint` (zaprášení). U ostatních materiálů jsou na 0, takže se nic nemění. Rozdělení se mění v `constructions.json` → `finish` (výchozí hodnoty jsou v `WOOD_FINISH_DEFAULT` v `zrlib\config.py`). Neošetřené dřevo je `MI_RuinWood`, který vytvoří skript 03. Je to zašlé nelakované dřevo, šedohnědé a matné. Každý trám a prkno má trochu jiný odstín a vršky jsou vybledlé od slunce. Ladí se v `MI_RuinWood` (`TintA`/`TintB`, `Roughness`) nebo v `MAT_LOOK["wood"]` v `zrlib\config.py`. Vlastní materiál nastavíš v `MAT_WOOD_MI` (tamtéž).

## Kdo používá
- [[05_constructions]]: pevné kusy staveb typu `props` (kůl, staveniště).
- [[06_furnishing]]: přenosné vybavení.

## Dopad změny
- Nový prop: funkce v `tools\meshes\mesh_props.py`, záznam v `LIB_MESHES` (`zrlib\config.py`), vygenerovat `gen_meshes.py`; build si ho doimportuje sám. Stav: [[CHECKLIST_assets_navrhy]].
- Poloha propu ve specu je střed bounding boxu meshe; změna tvaru může posunout funkční střed (výfučna, rám), proto po změně spusť kontroly dotčených skupin (`run_checks.py`).

## Známé pasti
Viz [[Pasti_generator_meshi]] a [[Pasti_import_meshi_a_assety]].
