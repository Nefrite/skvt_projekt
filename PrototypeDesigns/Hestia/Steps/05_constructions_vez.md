---
# orchestrace
type: step
validity: valid
aliases: []
step_kind: build
updated: 2026-11-23
# hra
build_step: 05_constructions
domains: [structures]
entity: "[[Vez]]"
---
# 05 Constructions – dřevo ve věži a přístřešek hlídky (Vez_Patra, Vez_Pristresek)

<!-- Část dokumentu kroku [[05_constructions]], rozděleno tematicky 2026-11-23 (G14b, předání Builderovi). -->

## Účel kroku
Data dřevěných pater, schodů a ochozu ve věži (`tower_floor`) a přístřešku hlídky na věži (`canvas_shelter`).

## Spouštění
Jednotlivé stavby: `05_constructions\stavby\<Stavba>.py`; celý postup v UE a co kdy přegenerovat: [[05_constructions]] (kap. 2 a 3).

## Skripty
<!-- hestia:generated:start -->

| Skript | Role | Entity | Dokumenty |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_postel_nahled.png` | data | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_stojan_brneni_nahled.png` | data | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_truhla_nahled.png` | data | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Knihovna_meshe_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Knihovna_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Kulatina_meshe_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Kulatina_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Props_kovarna_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Props_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_luzko_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_luzko_slozena_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_plachta_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_truhlicka_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_vak_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_straz_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_straz_nahled_etapa1.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_drevo_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_dostavba_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_podlaha_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_tramovi_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_kovarna_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_obydli_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_obydli_nahled_etapa1.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_vez_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_vez_pristresek_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/build_constructions.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/constructions.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/constructions_edits.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz.py` | entry | [[Brana_Straz]] | [[navrh_brana_straz]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kamen.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kryty.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Podesta.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Etapa.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Dostavba.py` | entry | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Krov.py` | entry | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Podlaha.py` | entry | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Kul.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Okap.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Pristresek.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Stena.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Vyhen.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli.py` | entry | [[Palac_Obydli]] | [[navrh_palac_obydli_stred]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Kamen.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Krov.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Ohniste.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Srub.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Stavenisko.py` | entry | [[Palac_Obydli]] | [[navrh_palac_obydli_stred]], [[stav_palac_obydli]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Stavenisko_Capture.py` | entry | [[Palac_Obydli]] | [[navrh_palac_obydli_stred]], [[stav_palac_obydli]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Sut.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez.py` | entry | [[Vez]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez_Patra.py` | entry | [[Vez]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez_Pristresek.py` | entry | [[Vez_Pristresek]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/__init__.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/dostavba.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/krov.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/kryty.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/ohniste.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/okap.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/podesta.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/podlaha.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/pristresek.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/pult.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/srub.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/stena.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/vez.py` | library | [[Vez]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/vybaveni.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/zdivo.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/tools/constructions/check_tower.py` | generator | – | – |
| `/PrototypeDesigns/Lapikus/tools/constructions/gen_constructions.py` | generator | – | – |

<!-- hestia:generated:end -->

## Vstupy a výstupy
### Co je v `constructions.json`: věž

#### Patra ve věži (`Vez_Patra`, `floors`)

| Klíč | Význam |
|---|---|
| `levels` | patra s trámy a prkny (1, 2) |
| `beams` | trámy: polohy `v` (m od jižní zdi), průřez, zapuštění do kapsy `bearing` |
| `planks` | prkna: tloušťka, šířky, podíl chybějících |
| `girder` | průvlak sever–jih pod trámy, sloup s hlavicí (`post_v`) |
| `hatches` | otvory pro schody v každém patře (u0, u1, v0, v1) |
| `stairs` | schody: `from` / `to` patro, `axis` `"u"` (podél trámů), `dir` (+1 stoupá k východu, −1 k západu), `u_top` (horní konec), `v`, `angle`, `width`. Cik-cak: do 1. patra k východu, do 2. patra k západu |
| `porch` | ochoz před původním vstupem: šířka, hloubka, trámy zapuštěné v kapsách, šikmé vzpěry pod trámy opřené o zeď (`braces`: `dv`, `dz`, `w`). Sloupky na zem (`posts`) jsou vypnuté |
| `finish` | úprava dřeva podle části: `tar` dehtované, `raw` bez úpravy, `oil` mořené olejem, `blood` mořené krví, `old` staré neošetřené. Části: `beams`, `girder`, `posts`, `heads`, `planks` (a `planks_1`, `planks_2` pro jedno patro), `stairs`, `porch_beams`, `porch_braces`, `porch_posts`, `porch_planks` |
| `rubble` | suť: `enabled`, složka v Outlineru |

Souřadnice jsou v rámu věže: **u** vede od jihozápadního rohu podél jižní zdi (`Vez_J`), **v** od jihozápadního rohu k severu. Obojí v metrech, osy zdí jsou na 0 a 11 m.

#### Přístřešek hlídky na věži (`Vez_Pristresek`, typ `canvas_shelter`)

- **Kód:** `zr_stavby/pristresek.py`, data `gen_constructions.py` → `vez_pristresek` z `tools/ruin/tower_spec.py` (`PR`, `pristresek()`); ram věže `u`, `v` (m), výšky `h` v m od `VEZ_F`.
- **Dílce:** kůly s hlavou rozsochy (hlava zvětšená `fork_k` na průměr kůlu, osa hřebene nad středem hlavy `seat` změřená na OBJ), hřeben z kusů, okapová tyč na podkladních kamenech (výška z postavené koruny, kámen koruny musí pod podkladem zasahovat aspoň 3 cm), krokvové tyče, vzpěry, ovázání (`SM_RuinLashing` zvětšené na průměr tyče), plachta a štít na míru, tyčka v lemu štítu, lana z článků `SM_RuinRope` přes plachtu ke kotevním kamenům, zátěžové kameny.
- **Plachta na míru:** `python tools/meshes/gen_meshes.py textile` → `meshes/textile/SM_RuinCanvasVez_A.obj` + `.json`, `SM_RuinCanvasVezGable_A.obj` + `.json`. Lokální osy meshe X = u, Y = −v, Z = h (ram věže je v UE levotočivý). Po změně `PR` (polohy, sklon) vždy přegenerovat meshe i `constructions.json` a zvýšit verzi `SM_RuinCanvasVez` v `STONE_MESH_VERSION`.
- **Ruční doladění:** podkladní, zátěžové a kotevní kameny jsou samostatné actory (`Vez_Pristresek.py`, `MODE = "capture"`).
- **Kontroly:** `run_checks.py --only vez`, náhled `preview3d.py vez` (plachta jako tenké kvádry).

## Dopad na dokumentaci
Změna dat nebo typu stavby: aktualizuj tento dokument a stavový dokument entity (`stav_*`).

## Známé pasti
Viz `KnowHow/Pasti_*` (tematické seznamy pastí).
