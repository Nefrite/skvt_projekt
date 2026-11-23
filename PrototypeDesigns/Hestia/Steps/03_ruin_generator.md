---
# orchestrace
type: step
validity: valid
aliases: []
step_kind: build
updated: 2026-11-23
# hra
build_step: 03_ruin
domains: [structures]
entity: "[[Lapikus]]"
---
# 03 Ruin – jak generátor skládá zeď a struktura kódu

<!-- Část dokumentu kroku [[03_ruin]], rozděleno tematicky 2026-11-23 (G14b, předání Builderovi). -->

## Účel kroku
Popis vnitřku generátoru zříceniny: vrstvy zdi (líc, jádro, koruna) a struktura kódu (`zrlib`, `zr_ruin`, nástroje). Jak generátor spustit: [[03_ruin]].

## Spouštění
Spouštění, nastavení a pořadí skriptů: [[03_ruin]] (*Spouštění*).

## Skripty
<!-- hestia:generated:start -->

| Skript | Role | Entity | Dokumenty |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_Brana_S_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_bloky_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_kameny_detail.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_kameny_koruny.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_koruna_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_lic_pred_po.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_strilna_preklad_pred_po.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_strilny_osteni_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/build_ruin_blocks.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/casti/Obvod.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/casti/Ostroh.py` | entry | [[Ostroh]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/casti/Palac.py` | entry | [[Palac]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/detach_stones.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/gen_stones.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/manual_edits.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/ruin_layout.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/terrain_from_level.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/__init__.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/compute.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/decay.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/floor.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/post.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/prep.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/rubble.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/zr_ruin/wall.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/03_ruin/build/Zricenina_blockout_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/build/build_ruin.py` | entry | [[Lapikus]] | [[README_ruin]] |
| `/PrototypeDesigns/Lapikus/03_ruin/build/ruin_layout.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_okna_podesta.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_patra_strilny.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_schody.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_vyklenky_kvadry.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/03_ruin/ruin_layout_draft.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/brana_spec.py` | spec | [[Brana]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/build_ruin.py` | entry | [[Lapikus]] | [[README_ruin]] |
| `/PrototypeDesigns/Lapikus/tools/ruin/check3d.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/check_blocks.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/decay.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/elev.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/export_level_layout.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/gen_layout.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/layout_from_level.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/massing.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/ostroh_spec.py` | spec | [[Ostroh]] | – |
| `/PrototypeDesigns/Lapikus/tools/ruin/palac_spec.py` | spec | [[Palac]] | [[navrh_palac_obydli_stred]] |
| `/PrototypeDesigns/Lapikus/tools/ruin/tower_spec.py` | spec | [[Lapikus]] | [[navrh_vez_pristresek]] |

<!-- hestia:generated:end -->

## Vstupy a výstupy
Kapitola 7 má číslo z původního [[03_ruin]]; skladba zdi byla v *Účelu kroku*.

### Jak je zeď složená

| Vrstva | Co to je | Materiál (výchozí) |
|---|---|---|
| **Líc** (obě strany zdi) | lomové kameny v řádcích 25–40 cm, délky 35–90 cm, převazba (spáry se střídají). **Zaoblené, lehce zvětralé meshe** `SM_RuinStone_*` | `MI_RuinFace` (Slate, náhodný odstín na kámen) |
| **Jádro** (mezi líci) | delší bloky z lomu a malty 1,0–1,8 m (kostky, většinou skryté) | `MI_RuinCore` (šedý kámen s maltou) |
| **Ostění a oblouky** | opracované kvádry kolem intaktních otvorů po řádcích zdi, nadpraží, parapet, klínové kameny oblouků. Meshe `SM_RuinDressed_*` (opracovaný kámen, zaoblené a lehce otlučené hrany, 4 poměry × 2 varianty; `DRESSED_FRAMES = False` = kvádr `SM_RuinAshlar`) | `MI_RuinFrame` (stejný kámen jako líc, o kousek světlejší) |
| **Nárožní kvádry** | zakrývají průřez zdi v rozích. U vnějšího rohu se střídá dlouhý a krátký kvádr, zbytek tloušťky tvoří lomové kameny | jako líc |
| **Zlomy lomené zdi** | kámen přes zlom se rozdělí na dva. Na vnější (vypouklé) straně se líc prodlouží do společné hrany, na vnitřní se zkrátí, takže zvenku nevznikají klínové díry. Jádro se prodlouží | – |
| **Podpora líce** | lícový kámen musí ležet na lícovém kameni (ne jen na jádru). Nad vybraným lícem tak nevisí žádné kameny a díra se nahoru stupňovitě uzavírá. **Klenutí:** kámen nad mezerou do 0,6 m (`BRIDGE`) zůstane, když leží oběma konci (levý konec může držet i soused v řadě, malta) | – |
| **Odkryté jádro** | kde chybí líc, jádro se rozpadne na lomové kameny 0,35–0,7 m (mesh `SM_RuinStone_*`), každý jinak zapuštěný o 5–20 cm (`CORE_RECESS`). U okraje díry méně, občas vystupuje zbytek líce, takže hrana není ostrá. Kus, který by visel, odpadne. Vypíná se `CORE_ROUGH: false` | `MI_RuinCore` (šedý kámen s maltou) |
| **Koruna** | odkryté horní kameny, na kterých už nic neleží (i na dně děr po vybraném líci), jsou zvětralé **hlavně shora** (počasí): tvary `SM_RuinStone_W_*` mají horní hrany obroušené do velkého zaoblení, nerovný vrch s důlky, spodek (leží na kameni pod sebou) zůstává ostrý. Materiál `MI_RuinCrown` zesvětlí a zazelená (lišejník, prach) jen plochy mířící nahoru. Vypíná se `CROWN_WEATHER = False` | `MI_RuinCrown` |

**Rozpad** jde v tomto pořadí:

1. **Výška zdi:** model rozpadu z [[README_ruin]] kap. 4 (čas, rozebírání podle dostupnosti a výšky, otvory) určí, jak vysoko zeď v daném místě sahá.
2. **Bloky nad touto výškou zmizí.** Na koruně zůstanou jednotlivé uvolněné a pootočené kameny.
3. **Podpora:** blok bez opory pod sebou nezůstane (výjimka: je nad intaktním nadpražím nebo obloukem).
4. **Rozebraný líc:** kameny se berou hlavně **shora**, v pásu pod korunou (`TOP_ROB`, `TOP_ROB_D`). Líc pod korunou ustupuje stupňovitě. U paty jen menší hloučky 2–4 kamenů, kam se dosáhne (`FACE_ROB_BASE`, víc u `access_points`). Ve věži se výška u paty měří zevnitř od podlahy. Kameny se vybírají v hloučcích (plynulý šum), ne po jednom. Vnější líc nad útesem zůstává.
5. **Otvory:** parapet a nadpraží se zarovnají na spáry řádků. Bloky, které do otvoru nebo ostění zasahují, se **rozdělí** (nevynechávají se celé), takže každý otvor je opravdu průhledný a kolem ostění nevznikají díry. Intaktní ostění (po řádcích), nadpraží, parapet a oblouky se postaví z opracovaných kvádrů. Když lidé vylámali opracované kameny ostění, ale oblouk nebo nadpraží stojí, zůstane za nimi zapuštěné jádro zdi a nese je, takže nic nevisí ve vzduchu. Kontrola mimo UE: `python test_openings.py` → `kolize: 0`.
6. **Suť:** jen málo bloků u paty, protože většinu kamene lidé odvezli.

---

---

### 7. Struktura kódu (od 11/2026)

```
zrlib\                    sdílená knihovna 03 + 05 + tools (čistý Python, bez numpy - kvůli Pythonu v Unrealu)
  config.py               NASTAVENÍ VZHLEDU: tagy, materiály, textury, zaoblené kameny, dřevo, fyzika volných kamenů
  geom.py                 geometrie: interpolace, terén, polylinie (offset, ořez, průsečíky), polygon, rovina
  stones.py               kámen / dílec (Stone), přiřazení meshí, hmotnost
  ue_assets.py            Unreal: materiály M_RuinStone a MI_*, import meshí, transformace instancí, fyzika
  ue_actors.py            Unreal: ISM actory, samostatné kameny, mazání podle tagů, capture (03 i 05 stejně)
  level.py                Unreal: bourací objemy, terén z landscapu
  validate.py             kontrola dat (chybějící klíč = srozumitelná chyba se jménem zdi / stavby)
  pipeline.py             spouštění v UE: načtení 03 / 05 jako knihoven, build částí a staveb, build_all (normal / fullscope)
build_normal.py           celý hrad (03) + všechny stavby (05), aditivně
build_fullscope.py        oprava: smaže generované actory a meshe, vše znovu
03_ruin\blocks\
  build_ruin_blocks.py    vstup: nastavení běhu, soubory (layout, manual_edits), build a capture v UE
  casti\*.py              build jedné části hradu
  zr_ruin\decay.py        rozpad: typy otvorů, stav otvoru, profil výšky zdi, parametry stáří, šum rozebírání
  zr_ruin\prep.py         příprava dat zdi: podstavba, ref_z, ochrana do výšky otvoru jiné zdi, bourací objemy
  zr_ruin\wall.py         zeď po krocích: prepare_wall, snap_openings, forbidden, lay_courses, build_frames, finish_wall
  zr_ruin\post.py         úpravy kamenů zdi: koruna pod střechou, žlábky pro trámy, rozpadlé jádro, zvětralá koruna,
                          horní řada pryč (drop_rows v datech zdi: horní kameny každé vrstvy; zatím žádná zeď ho nepoužívá).
                          Celá zeď zanořená do země = z_offset (Palac_J o řadu, palac_spec.py)
  zr_ruin\floor.py        kamenná dlažba (layout → floors)
  zr_ruin\rubble.py       suť u paty zdí (staví 05)
  zr_ruin\compute.py      celý hrad: všechny zdi a podlahy → kameny
tools\checks\
  run_checks.py           kontroly bez UE (otvory, kameny bez podpory, ostroh: průniky, pokrytí krytinou) - SOUHRN na konci
  preview3d.py            3D náhled se stíny (three.js v headless Chromiu; potřebuje node, playwright a three)
  fingerprint.py          otisk výstupu všech skriptů (kameny, generované JSON, volání Unreal API) - pro refaktoring
  common.py               společné načtení stavu jako v UE (terén z levelu, ruční úpravy), průniky kvádrů
```

- **Jedna kopie `zrlib` na běh (15. 11. 2026):** spouštěče (`casti\*.py`, `stavby\*.py`, `build_normal.py`, `build_fullscope.py`) na začátku zahodí moduly z minulého běhu a dál načítají přes `zrlib\pipeline.py`, který už nic nezahazuje. Dřív si 05 načítalo zříceninu s vlastní kopií `zrlib`, takže stav knihovny (např. materiály slotů `ue_assets.SLOT_MATS`) viděly 03 a 05 různě. Nový spouštěč: zkopíruj existující, začátek je popsaný v hlavičce `pipeline.py`.
- **V Unrealu se nic nemění:** spouští se pořád `build_ruin_blocks.py`, `casti\*.py`, `detach_stones.py`. Složka `zrlib` musí ležet v kořeni vedle `03_ruin` a `05_constructions`. Moduly se při každém spuštění načtou znovu, takže úprava souboru se projeví hned (bez restartu editoru).
- **Mimo UE:** `python tools\checks\run_checks.py` (volitelně `--layout <ruin_layout.json>`, `--only openings,floating,ostroh`). Nahradil `test_openings.py`.
- **Refaktoring:** `python tools\checks\fingerprint.py . pred.json` před změnou, po změně `python tools\checks\fingerprint.py . po.json --compare pred.json`. Volitelně `--state <složka s manual_edits.json a terrain_from_level.json>`, `--heightmap <png>` (přidá generátory dat). Rozdělení skriptů v 11/2026 dává bit po bitu stejný výstup jako předtím.

## Dopad na dokumentaci
Změna dat nebo typu stavby: aktualizuj tento dokument a stavový dokument entity (`stav_*`).

## Známé pasti
Viz `KnowHow/Pasti_*` (tematické seznamy pastí).
