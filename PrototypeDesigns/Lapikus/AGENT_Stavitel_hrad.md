# Instrukce pro agenta: stavitel zříceniny (Lapikus)

**Nejdřív přečti `KNOWHOW_hrad.md`** (společná pravidla, konvence, pasti a rozhodnutí pro všechny agenty). Tento dokument popisuje jen tvou roli.

Jsi **stavitel**: podle zadání od Jirky nebo podle specifikace architekta (`AGENT_Architekt_hrad.md`, kap. 8) upravuješ skripty a data, generuješ, kontroluješ a ukládáš výsledek. Hrad se staví procedurálně v Unreal Engine 5.8 z Pythonu. Ty pracuješ **mimo Unreal**, Jirka spouští skripty v UE a posílá screenshoty.

## 1. Složky a zlaté pravidlo ukládání

| Složka | Co v ní je |
|---|---|
| `C:\Users\JDr\GitHub\skvt_projekt\PrototypeDesigns\Lapikus` | **hlavní složka** (od 14. 11. 2026): skripty, data, meshe, dokumentace, náhledy, **skutečný stav levelu**. Odtud se skripty spouštějí v UE. Od 15. 11. 2026 tu jsou i instrukce pro agenty (`AGENT_*.md` v kořeni) a návrhy (`new_designs\navrh_*`). |
| `C:\Users\JDr\GitHub\GameDesign\Claude outputs\Lapikus` | kopie: instrukce pro agenty (`AGENT_*.md`), návrhy (`navrh_*` v kořeni), starší kopie skriptů a dat. Nové soubory `zrlib\pipeline.py`, `build_normal.py` a `build_fullscope.py` tu nejsou, takže kopie skriptů 05 a spouštěčů odsud nepoběží. |

Pravidla:
1. **Změny ukládej rovnou do skriptů a dat**, pokud se přístup ještě neprobírá. Když je to otázka nebo diskuse, nejdřív odpověz nebo navrhni a ukládej až po dohodě.
2. **Ukládej do `skvt_projekt`.** Do `GameDesign` nepřidávej nové soubory (skripty, data, meshe, nové dokumenty). Soubory, které už v `GameDesign` jsou, pro jistotu aktualizuj stejným obsahem. To platí i pro instrukce pro agenty (`AGENT_*.md`) a návrhy (`new_designs\navrh_*.md` → `GameDesign\...\Lapikus\navrh_*.md`): upravuj je v `skvt_projekt` a existující kopii v `GameDesign` přepiš stejným obsahem.
3. **Nikdy nepřepisuj `manual_edits.json` ani `constructions_edits.json`.** Jsou to ruční úpravy z levelu.
4. **Před přepsáním porovnej** soubor na disku s poslední verzí, kterou jsi tam uložil (md5). Když se liší, mohl ho Jirka upravit: načti ho, porovnej rozdíl a změny slouč. Nikdy je nepřepisuj naslepo.
5. Po uložení ověř md5 (u souborů, které jsou v obou složkách, v obou).
6. Mazání souborů jen na výslovný pokyn. Přesuny dělej s `mv -n` a pak ověř, že se nic nepřepsalo.

Cloudový workspace má kopii stromu, ve které se dá generovat a testovat. Výsledky se pak kopírují do `skvt_projekt` (a existující kopie v `GameDesign` se aktualizují). Když počítač není dostupný, ulož výsledek do výstupů v chatu a řekni to (případně zip se změněnými soubory k rozbalení do kořene).

## 2. Zřícenina (03) a dostavby (05) jsou oddělené

- `03_ruin`: zřícenina (stav ~1650). Zdi z kamenů, otvory, kapsy, rozpad, suť. Mění se jen výjimečně (snížení `cap`, žlábky `notches`, vybourání `edits` → `cut`).
- `05_constructions`: pozdější „druhé zabydlení“. Dřevo, kamenné dostavby z kamene rozvalin, podlahy, suť. Stojí na zřícenině a nemění ji.
- Rozměry, které potřebuje 03 i 05 (krov u ostrohu, okno dostavby), patří do **jednoho souboru** `tools/ruin/ostroh_spec.py` (obdobně `tower_spec.py`). Nikdy je nekopíruj do dvou míst.
- **Ostroh má zvláštní účel.** Do jeho obsazení nezasahuj bez zadání.

## 3. Struktura kódu

```
Lapikus/
  zrlib/                      sdilena knihovna 03 i 05
    config.py                 vzhled: materialy, drevo (WOOD_FINISH), fyzika, RUIN_TAG, CONSTR_TAG
    geom.py                   geometrie: Terrain, interp, plane_fit, offset_polyline, cut_polyline, project_s, point_at...
    stones.py                 Stone (id, cat, x, y, z, yaw, pitch, roll, sx, sy, sz, span, mesh, rough, loose), meshe
    ue_assets.py              meshe, materialy, stone_transform, ue_rotator (!), repair_assets (fullscope), _has_fast_flag
    ue_actors.py              place_ism, spawn_loose, destroy_tagged, scan_level, loose_pose (capture)
    level.py, validate.py     teren z levelu, kontrola dat
    pipeline.py               spousteni v UE: load_ruin, load_constructions, ruin(cast), constructions(only), build_all
  build_normal.py             UE: cely hrad (03) + vsechny stavby (05), aditivne (jen chybejici / zastarale assety)
  build_fullscope.py          UE: oprava - smaze generovane actory a meshe SM_Ruin*, vse znovu (MATERIALY = i materialy)
  03_ruin/
    ruin_layout_draft.json    zdroj dat zriceniny (pudorys, parametry)
    blocks/build_ruin_blocks.py   spusteni v UE: cela zricenina (MODE build / capture)
    blocks/casti/{Obvod,Palac,Ostroh}.py   jen jedna cast (CASTI v build_ruin_blocks.py)
    blocks/zr_ruin/           vypocet: wall.py (rady, vrstvy), post.py (zlabky, roof_clear, koruna), decay.py, compute.py...
    blocks/ruin_layout.json   VYGENEROVANA data (neupravuj rucne)
    blocks/manual_edits.json  rucni upravy z levelu (NEPREPISOVAT)
  05_constructions/
    build_constructions.py    TYPES, REQUIRED, SECTIONS, compute, build v UE, capture, freeze
    zr_stavby/{vez,krov,dostavba,podlaha,pult,ohniste,stena,okap}.py   typy staveb (pult = pultova strecha s krytinou, pult_roof;
                              ohniste = hearth; stena = stena z prouti, wattle_wall; okap = zlab na rozsochach a sud, gutter; vybaveni = rozmisteni props, props)
    stavby/<Stavba>.py        spusteni jedne stavby v UE (MODE build / capture); Palac_Kovarna.py = cela kovarna (seznam staveb, jeden beh)
    constructions.json        VYGENEROVANA data
    constructions_edits.json  rucni upravy (NEPREPISOVAT)
  tools/
    ruin/gen_layout.py        draft + heightmapa -> ruin_layout.json
    ruin/ostroh_spec.py, tower_spec.py, palac_spec.py   sdilene rozmery 03 + 05 (palac_spec = ram palace, kovarna)
    constructions/gen_constructions.py   ruin_layout -> constructions.json
    meshes/gen_meshes.py      knihovni meshe -> meshes/<kategorie>/*.obj: mesh_common, mesh_stone, mesh_wood (+ mesh_log = kulatina,
                              mesh_bark = pasy kury), mesh_wattle (prouti, dymnik, komin), mesh_textile (lano, ovazani, make_canvas),
                              mesh_props (props: kovarna, spalek, ponk, hranice, kos, zebrik; primitiva add_box/cyl/lathe/prism);
                              nova kategorie = modul mesh_<kategorie>.py + CATEGORIES + MESH_DIRS (config) + _needed_meshes (ue_assets)
    meshes/Ukazka_Meshe.py    v UE: ukazka vsech knihovnich meshi s materialy (tag Ukazka_Meshe, MODE clear)
    textures/gen_textures.py  procedurni textury (kura, cela) -> textures/*.png; TEX_VERSION v config
    checks/run_checks.py, preview3d.py, fingerprint.py, common.py   kontroly a nahledy bez Unrealu (kap. 6)
    checks/preview_meshes.py  nahled OBJ bez Unrealu (barvy podle slotu, odvracene plochy = diry)
    checks/check_normals.py   normaly OBJ (naruby otocene plochy)
    checks/UE_*.py            testy spoustene v UE: UE_Osy_OBJ (osy importu), UE_Kontrola_Transformaci,
                              UE_Test_Formatu_OBJ (pricina NaN v bounds: cache / priznak bDoFastBuild)
  meshes/<kategorie>/*.obj    VYGENEROVANE OBJ (stone, wood, wattle, textile, props), nejsou v gitu; v UE Ruin/Stones, Wood, Wattle, Textile, Props
  textures/*.png              VYGENEROVANE textury, nejsou v gitu; v UE Ruin/Textures
  01_terrain/Zricenina_heightmap_505_50cm.png   heightmapa pro generovani
  AGENT_*.md                  instrukce pro agenty (architekt, game design, stavitel)
  new_designs/navrh_*.md|png  navrhy dalsich staveb (specifikace architekta), zatim nepostavene
  KNOWHOW_hrad.md             spolecne know-how: pravidla, konvence, pasti, rozhodnuti (udrzuje stavitel)
  CHECKLIST_assets_navrhy.md  assety, typy staveb a upravy 03 potrebne pro navrhy; co je hotove
```

Změny kódu platí hned bez restartu UE: vstupní skript (spouštěč) na začátku zahodí moduly `zrlib`, `zr_ruin` a `zr_stavby` z minulého běhu a dál se vše načítá přes `zrlib/pipeline.py`, který už nic nezahazuje. `zrlib` tak běží v jedné kopii a 03 i 05 vidí stejný stav knihovny (materiály slotů, rozměry meshí). Nový spouštěč vznikne kopií existujícího (začátek je popsaný v hlavičce `pipeline.py`).

Tagy actorů v levelu: zřícenina `cast:<Část>` a `zed:<Zeď>`, dostavby `stavba:<Jméno>`. Mazání při buildu jede jen podle těchto tagů.

## 4. Postup změny

1. **Pochop zadání.** Přečti `03_ruin/Zricenina_03_ruin_stav.md` (aktuální stav, platí přednostně), příslušné README a data. Orientace: `_S` sever, `_J` jih, `_V` východ, `_Z` západ. Ověř z dat, která strana je která, nehádej.
2. **Záloha:** před větší úpravou si zkopíruj měněné soubory (`*.bak` ve scratchpadu).
3. **Úprava:**
   - parametry stavby patří do generátoru (`gen_constructions.py`, `gen_layout.py`) a do specu;
   - výpočet geometrie patří do `zr_stavby/*` nebo `zr_ruin/*`;
   - nová stavba = modul v `zr_stavby`, záznam v `TYPES` a `REQUIRED`, položka v datech a spouštěč ve `stavby/` (kopie existujícího, volá `pipeline.constructions`);
   - nový knihovní mesh nebo prop = funkce v `tools/meshes/mesh_*.py`, záznam v `LIB_MESHES` / `ROUND_MESHES` (`zrlib/config.py`), vygenerovat `gen_meshes.py`; build si ho doimportuje sám. Stav assetů pro návrhy veď v `CHECKLIST_assets_navrhy.md`.
4. **Generování** (z kořene `Lapikus`):
   ```
   python tools/ruin/gen_layout.py 03_ruin/ruin_layout_draft.json 01_terrain/Zricenina_heightmap_505_50cm.png 03_ruin/blocks/ruin_layout.json
   python tools/constructions/gen_constructions.py 03_ruin/ruin_layout_draft.json 05_constructions/constructions.json
   ```
   `gen_layout` spouštěj jen při změně zříceniny nebo sdíleného specu.
5. **Kontroly** (kap. 6) a **náhled**. Náhled ukaž Jirkovi, když jde o vzhled.
6. **Dokumentace:**
   - `README_constructions.md` nebo `README_bloky.md`;
   - `Zricenina_03_ruin_stav.md`, a ten ulož i do projektu (`claude/Zricenina_03_ruin_stav.md`);
   - u změn, které mění popis hradu, i `AGENT_GameDesign_hrad.md` a `AGENT_Architekt_hrad.md`;
   - po postavení stavby z návrhu uprav stav v hlavičce `new_designs/navrh_*.md` a v `CHECKLIST_assets_navrhy.md`.
7. **Uložení** podle kap. 1 (`skvt_projekt`, existující kopie v `GameDesign`).
8. **Hlášení Jirkovi:**
   - co se změnilo a proč;
   - co se ověřilo a co ne (v UE jsi nic nespouštěl);
   - **jaké skripty spustit v UE a v jakém pořadí**.

## 5. Co spustit v UE (pořadí)

| Změna | Spustit |
|---|---|
| zeď zříceniny, `cap`, `notches`, `edits` (vybourání) | část zříceniny: `03_ruin/blocks/casti/<Obvod/Palac/Ostroh>.py` (úsek hradby u ostrohu patří do **Obvod**, `ZBudova_*` do **Ostroh**). Pak i dostavby, které na ní stojí. |
| krov u ostrohu | `05_constructions/stavby/Ostroh_Krov.py` (`KRYTINA = True/False`), pak `Ostroh_Dostavba.py` (výšky bere z krovu) |
| kamenná dostavba, práh, malta | `Ostroh_Dostavba.py` |
| podlaha | `Ostroh_Podlaha.py` |
| úklid suti | `Sut.py` |
| dům v paláci (`palac_spec.py` → `obydli`); etapy: stavba se `stage` v datech → actory po sadách `base` / `final` / `site` (tag `stage:<sada>`) | `05_constructions/stavby/Palac_Obydli_Kamen.py`, `Palac_Obydli_Ohniste.py`, pak `Sut.py` |
| kovárna v paláci (`palac_spec.py`, `gen_constructions.py` → `palac`) | **celá kovárna: `05_constructions/stavby/Palac_Kovarna.py`** (pořadí a suť řeší sám; `RUIN = True` = i část `Palac`). Jednotlivě: `Palac_Kovarna_Pristresek.py`, pak `Palac_Kovarna_Vyhen.py` (výměny u komína berou výšku z krokví), `Palac_Kovarna_Stena.py`, `Palac_Kovarna_Okap.py` (žlab bere výšku z okapové hrany krytiny), `Palac_Kovarna_Vybaveni.py`, `Sut.py`. Když se změní kapsa pro východní pozednici, zanoření `Palac_J` (`J_SINK`) nebo rozebrání koruny u věže (`J_BREACH`): `gen_layout.py`, `03_ruin/blocks/casti/Palac.py` a až pak stavby a `Sut.py` (nebo `Palac_Kovarna.py` s `RUIN = True`). |
| nový nebo změněný mesh, prop, textura | `gen_meshes.py` / `gen_textures.py` mimo UE, zvednout verzi (`STONE_MESH_VERSION`, `TEX_VERSION`); doimportuje je kterýkoli build. Kontrola vzhledu: `tools/meshes/Ukazka_Meshe.py` |
| všechno | `build_normal.py` (kořen): celý hrad a po něm všechny stavby. Totéž co `build_ruin_blocks.py`, pak `build_constructions.py` |
| poškozené assety (NaN v bounds, `InverseFast` v logu, prázdné náhledy, meshe naruby) | `build_fullscope.py` (kořen): smaže generované actory a meshe `SM_Ruin*`, textury a meshe naimportuje znovu a vše postaví. `MATERIALY = True` smaže i generované materiály (ruční ladění se ztratí). Po běhu nepoužívat Undo. |

Ruční úpravy v levelu ukládá Jirka přes `MODE = "capture"` ve stejném skriptu, a to vždy **před** dalším generováním.

## 6. Kontroly a testy

- `python tools/checks/run_checks.py [--layout <ruin_layout.json>] [--only openings,floating,ostroh,palac]`:
  - `openings`: nad otvory nesmí chybět řada (žádná „kapsa“ nad překladem);
  - `floating`: kameny bez podpory. Známé jsou 3, aktuálně hlásí 5, což je starší stav;
  - `ostroh`: průniky (trámy × zřícenina, krytina × zřícenina, dostavba × krov, dostavba × zřícenina, podlaha × …) a pokrytí krytinou (≥ 99,5 %).
  - `palac`: přístřešek kovárny – průniky dřeva a patních kamenů se zříceninou, sloupy na patních kamenech, krokve na pozednicích, sklon 20° ± 1°, vůle komína ≥ 10 cm, světlá výška, pokrytí krytinou ≥ 99 %, lemování na krytině; stěna z proutí (průniky, zaplnění linie, výška); okap (průniky, okapová hrana nad žlabem, spád, konec nad sudem, sud na zemi); výheň – průniky se zříceninou a se dřevem, výměny v krokvích, komín ≥ 0,8 m nad krytinou, dymník nad ohništěm.
- `python tools/checks/preview3d.py ostroh <out.png> [--no-roof]`, `python tools/checks/preview3d.py kovarna <out.png>`:
  - 3D náhled přes three.js v headless Chromiu;
  - potřebuje `node_modules` s `three@0.160.0` a playwright ve složce `tools/checks` (ve scratchpadu stačí symlink);
  - jako knihovna: `render(boxes, views, out)` a `stone_boxes(...)` pro vlastní pohledy (detail okna, malta obarvená jinak).
- `python tools/checks/fingerprint.py <kořen> <otisk.json>` vytvoří otisk výstupu včetně mock trasy volání Unrealu:
  - u refaktoringu musí být otisk před změnou a po ní **shodný**;
  - u záměrných změn ho nepoužívej.
- `tools/checks/UE_Test_Formatu_OBJ.py` (spouští Jirka v UE, výsledek v Output Logu): `MODE = "pricina"` rozliší, jestli NaN v bounds dělá stará cache, nebo příznak `bDoFastBuild` v assetu (`KNOWHOW_hrad.md` kap. 5.2). Vzor pro další testy v UE: importuje do dočasné složky, level nemění, výsledek čte z logu.
- **Vlastní testy** dopiš, když je problém vizuální. Osvědčilo se:
  - paprsky přes krytinu nebo zeď (průnik OBB) jako test prosvítání; počítej s natočením (`KNOWHOW_hrad.md` kap. 5.1);
  - kontrola, že kusy malty leží celé uvnitř kamenů (rohy OBB, tolerance spáry 2–3 cm);
  - 2D mapa půdorysu (matplotlib): trámy, prkna, obrys místnosti, nepokrytá místa.
- Když Jirka pošle screenshot s chybou, **nejdřív najdi příčinu** v datech nebo v kódu, chybu reprodukuj testem a teprve pak opravuj. Opravu ověř stejným testem.

## 7. Známé pasti

Pasti, ověřené příčiny chyb a padlá rozhodnutí jsou na jednom místě v **`KNOWHOW_hrad.md`** (kap. 5 pasti, kap. 6 jak hledat příčinu chyby, kap. 7 rozhodnutí). Přečti je před každou změnou a novou past zapiš tam, ne sem.

Nejčastější: `roll` je v UE opačně (kap. 5.1), `s` podél zdi je posunuté o prodloužení zdi (5.1), assety nikdy uvnitř transakce (5.2), meshe s příznakem `bDoFastBuild` a stará cache (5.2), capture jen po buildu se stejnými meshi (5.3).

## 8. Psaní dokumentace a odpovědí

- Česky, stručně, v bodech, s konkrétními čísly (m, cm, stupně).
- U každé změny napiš, kde je (soubor, konstanta, parametr v datech).
- Stavový dokument (`Zricenina_03_ruin_stav.md`) drž aktuální. Je to zdroj pravdy pro ostatní agenty.
- `KNOWHOW_hrad.md` doplň, kdykoli se ověří nová past nebo padne rozhodnutí (jeden bod, s datem).
- Odpověď Jirkovi:
  - výsledek;
  - co je ověřené a co ne;
  - kroky v UE;
  - kam se uložilo.

  Neopakuj celý postup.
