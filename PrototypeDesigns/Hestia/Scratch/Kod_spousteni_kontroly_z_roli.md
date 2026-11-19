---
# orchestrace
type: scratch
validity: valid
intake: prepared
source: manual
updated: 2026-11-19
# hra
entity: "[[Lapikus]]"
---
# Kód, spouštění a kontroly (z instrukcí rolí)

<!-- Z AGENT_Architekt_hrad.md kap. 4 a 7, AGENT_Stavitel_hrad.md kap. 3, 4 (krok 4), 5, 6, AGENT_Furnisher_hrad.md kap. 3–7 a KNOWHOW_hrad.md kap. 4 (pilot Lapikus, B7). Beze změny textu, k zařazení po MVP. -->

## Z AGENT_Architekt_hrad

### 4. Jak se hrad staví (co z toho plyne pro návrh)

Nemusíš číst kód. Tohle je model, ve kterém stavitel umí pracovat:

**Zeď zříceniny (03)** je z kamenů v řadách:
- řady 25–40 cm, kameny dlouhé 35–90 cm, spáry 1,5 cm,
- tři vrstvy: dva líce (40 cm hluboké) a jádro mezi nimi,
- výška zdi po rozpadu se počítá z původní výšky (`H0`), dostupnosti a stáří.

Úpravy zříceniny se dělají **v datech**, ne ručně:

| Úprava | Kde v datech | K čemu |
|---|---|---|
| otvor | zeď → `openings` (`dvere`, `okno`, `strilna`, `kapsa`, `portal`, `brana`, `prulom`) | původní otvory hradu |
| vybourání | `edits` → `cut` (zeď, `s0`–`s1`, `z0`–`z1` v m od paty), `cut_box` (světový kvádr v cm) | nový otvor, průchod; odebírají se celé kameny |
| výška úseku | `edits` → `set_height` (přesně), `restore` (aspoň) | zachránit nebo snížit úsek |
| průlom, starší zřícení | zeď → `breaches` (`s0`, `s1`, `floor` v m od paty, `slope_l`, `slope_r`) | nepravidelné snížení koruny se šikmými boky (škody z dobývání, sedlo u komína); zapisuje se v `tools/ruin/gen_layout.py` |
| ochrana úseku | zeď → `protect` (`s0`, `s1`, `min`) | úsek neklesne pod danou výšku (nadpraží střílny, ochoz) |
| cílené snížení | zeď → `cap` (`s0`, `s1`, abs. výška) | rovná koruna, jako by ji někdo rozebral |
| celá zeď zanořená do země | zeď → `z_offset` (m, záporný) | zeď se posune po ose Z jako celek i s otvory, počet řad se nemění |
| horní řada pryč | zeď → `drop_rows` (počet řad) | koruna si nechá tvar, jen je níž (horní kameny každé vrstvy pryč); zatím nepoužito |
| kapsa pro trám | zeď → `openings` → `kapsa` (`s`, `w`, `sill`, `h`; nebo `z_abs` = absolutní Z spodku v cm) | uložení pozednice nebo trámu do vnitřního líce místo sloupu. Kapsa se zarovná na řadu kamene: výšku trámu vol podle spáry řad, ne naopak. `z_abs` použij u zdí s různou patou (brána). |
| žlábky pro trámy | zeď → `notches` (+ `roof_clear`) | trámy uložené v koruně |
| bourací objemy v levelu | `Ruin_Cut`, `Ruin_Keep`, `Ruin_Protect`, `Ruin_Opening:*` | ruční zásah v Unrealu |

Sdílené rozměry pro 03 i 05 jsou v `tools/ruin/ostroh_spec.py` (krov u ostrohu, okno), `tools/ruin/palac_spec.py` (rám paláce, kovárna, dům) a `tools/ruin/brana_spec.py` (rám brány, strážní stanoviště; výšky absolutně v UE cm). Tak to dělej i u nových staveb, které zasahují do zříceniny: **jeden zdroj rozměrů pro obě složky**.

**Dostavby (05)** mají typy:

| Typ | Co umí |
|---|---|
| `tower_floor` | trámy v kapsách, prkna, průvlak, schody, ochoz (věž) |
| `fan_roof` | sloupy, příčka, trámy na korunu nebo do žlábků, krytina z prken |
| `stone_addon` | jednořadá kamenná zeď na koruně až pod střechu, otvory s nadpražím, práh, malta |
| `plank_floor` | podlaha na podvalech uvnitř obrysu |
| `pult_roof` | pultová střecha: sloupy na patních kamenech, pozednice a vaznice (libovolný počet podpor, trám z více kusů, špalek pod trámem na zdi, podpora z jiné stavby), krokve hraněné nebo z kulatiny, spád po ose rámu stavby, krytina z prken s prostupem komína a lemováním (ověřená u spádu po ose `u`) |
| `stone_fill` | zdivo z kamene rozvalin v plné tloušťce: srovnání koruny zdi na danou výšku (i absolutní), zazdění otvoru, nízké podezdívky s mezerami pro dveře, maltové jádro v ose. Pozor: bez dolní meze zazdí i otvor pod korunou (portál). |
| `hearth` | ohniště, výheň nebo pec: kamenný blok v řadách s hliněným mazem a ohništěm, zídky (i s otvorem, i na stole), hliněná klenba pece, sopouch, kvádry ze železa, dymník a komín z knihovních meshí, výměny mezi krokvemi a závěsné tyče dymníku |
| `log_wall` | srub z loupané kulatiny v řadách, otvory zarovnané na řady, půltrámy pro střídání v nároží, prkenné štíty pod pultovou střechu |
| `wattle_wall`, `gutter`, `props` | stěna z proutí a hlíny mezi sloupy; žlab na rozsochách se sudem; rozmístění hotových props jako samostatných actorů |
| `platform` | podesta ve výšce zadané absolutně: trámy z kulatiny (v kapsách nebo na koruně), prkna, zábradlí |
| `palisade` | kryt z kůlů se špičkou na koruně zdi nebo na podlaze: paty kopírují korunu, průzory, ráhna |

Nová konstrukce, která se nevejde do žádného typu, je **nový typ**. Napiš to výslovně, protože to znamená víc práce. Typy, které návrhy z 11/2026 předpokládají a zatím neexistují: `canvas_shelter`, `bark_roof`, `tent`, strop s výměnou (`CHECKLIST_assets_navrhy.md`, kap. 7). Etapy nejsou přepínač, ale sady actorů (kap. 2). Když se nová stavba do některého vejde, použij jeho pracovní jméno.


**Knihovna dílců a props** (hotové meshe s materiály, generátor je jen rozmístí a škáluje; nominální délka 100 cm, pokud není uvedeno jinak). Navrhuj z nich, nový tvar je práce navíc a napiš ho výslovně:

| Skupina | Dílce |
|---|---|
| hraněné dřevo | trám `SM_RuinTimber`, sloup `SM_RuinPost`, prkno `SM_RuinPlank` |
| kulatina | loupaná `SM_RuinLog` (Ø 12–24 cm), s kůrou `SM_RuinLogBark`; tyč `SM_RuinPole` / `SM_RuinPoleBark` (Ø 5–10 cm); kůl se špičkou `SM_RuinStake` (s kůrou), `SM_RuinStakeSmall` (loupaný, špičky na obou koncích); hlava rozsochy `SM_RuinForkHead` (nasadí se na kůl); žlab z půlkmene `SM_RuinGutter` / `SM_RuinGutterBark` |
| kůra, proutí, hlína | pás kůry 160 × 70 cm `SM_RuinBarkStrip`; dílec proutěné stěny s mazaninou 100 × 100 × 8 cm `SM_RuinWattlePanel`; dymník `SM_RuinSmokeHood`; komín 60 × 60 cm `SM_RuinChimney` (v menším průřezu i sopouch); hliněná klenba pece 140 × 100 × 40 cm `SM_RuinOvenDome` |
| lano a plátno | článek lana `SM_RuinRope`, ovázání křížení tyčí `SM_RuinLashing`; plátno na míru (prověšená plocha mezi tyčemi, oboustranný materiál `MI_RuinCanvas`) |
| kovárna | špalek `SM_RuinStump`, kovadlina `SM_RuinAnvil`, měchy s rámem a výfučnou `SM_RuinBellows`, kalicí sud `SM_RuinBarrel`, šlapací brus `SM_RuinGrindstoneTreadle` s třínohou stoličkou `SM_RuinStool`, ponk se svěrákem `SM_RuinWorkbench`, kleště, kladivo, sekáč, hřebovnice, truhlík na uhlí s volným víkem `SM_RuinCoalBox` + `SM_RuinCoalBoxLid`, hranice polen `SM_RuinWoodpile`, železné pruty `SM_RuinIronBars`, koš `SM_RuinBasket` |
| obydlí | lůžko `SM_RuinBed` / `SM_RuinBedFolded`, stůl `SM_RuinTable`, truhla `SM_RuinChest`, police `SM_RuinShelf`, dveře 1,0 × 2,2 m `SM_RuinDoor`, okenice 60 × 60 cm `SM_RuinShutter`, žebřík 4,5 m `SM_RuinLadder`, poklop ústí pece s dřevěnou rukojetí `SM_RuinOvenDoor` |
| tesařské nářadí | sekera, širočina, dvoumužná pila, kladivo na hřebíky, palice |


Samostatné actory (`loose`) jsou kusy, které Jirka doladí ručně a uloží přes capture (práh). Navrhni je tam, kde výšku nebo polohu nejde přesně spočítat.

### 7. Jak se ověří, že je hotovo

Ke každému návrhu napiš, co má stavitel zkontrolovat. Nástroje už existují v `tools\checks`:
- `run_checks.py`:
  - otvory: nad otvory nesmí chybět řada kamenů;
  - kameny bez podpory;
  - u ostrohu průniky dřeva se zdivem, pokrytí krytinou a mezery pod střechou;
  - u kovárny v paláci (`--only palac`) průniky se zříceninou, uložení sloupů a krokví, sklon, vůle komína, světlá výška, pokrytí krytinou, stěna a okap;
  - u domu (`--only obydli`) a strážního stanoviště (`--only brana`) podpory podle sad etap, otvory, souvislost stěn, uložení trámů, kryty.
- `preview3d.py`: 3D náhled bez Unrealu (pohledy zvenku a zevnitř).
- Pro novou stavbu dopiš vlastní kritéria, například:
  - „krytina pokrývá ≥ 99,5 % půdorysu místnosti“,
  - „zdí neprosvítá“,
  - „trám leží na koruně, ne ve vzduchu“,
  - „průchod 1,2 m volný“.

## Z AGENT_Stavitel_hrad

### 3. Struktura kódu

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
    zr_stavby/                typy staveb (registr TYPES v build_constructions.py):
                              vez (tower_floor), krov (fan_roof), dostavba (stone_addon), podlaha (plank_floor),
                              pult (pult_roof, pultova strecha s krytinou a lemovanim), ohniste (hearth, vyhen / pec),
                              stena (wattle_wall, stena z prouti), okap (gutter, zlab na rozsochach a sud),
                              vybaveni (props, rozmisteni hotovych props jako samostatnych actoru),
                              zdivo (stone_fill), srub (log_wall), podesta (platform), kryty
    stavby/<Stavba>.py        spusteni jedne stavby v UE (MODE build / capture)
    stavby/<Skupina>.py       cela skupina staveb jednim behem (seznam STAVBY, volitelne RUIN, SUT): Palac_Kovarna.py,
                              Palac_Obydli.py, Brana_Straz.py
    stavby/Etapa.py           prepnuti etapy hry v editoru (sady actoru stage:base / final / site)
    constructions.json        VYGENEROVANA data
    constructions_edits.json  rucni upravy (NEPREPISOVAT)
  06_furnishing/              VYBAVENI = vse, co clovek prenese (props); pevne casti staveb zustavaji v 05
    build_furnishing.py       build, capture, list, reset (tag Zricenina_Vybaveni, vybaveni:<skupina>, id:<kus>)
    vybaveni/<Skupina>.py     jedna skupina (Palac_Kovarna.py), MODE build / capture / list / reset
    furnishing.json           data + polohy z levelu (gen_furnishing.py slucuje, capture zapisuje)
    furn_data.py              slouceni dat se specem, priznaky kusu (polohy z levelu jsou primo ve furnishing.json)
  tools/
    ruin/gen_layout.py        draft + heightmapa -> ruin_layout.json
    ruin/ostroh_spec.py, tower_spec.py, palac_spec.py, brana_spec.py   sdilene rozmery 03 + 05 (palac_spec = ram palace,
                              kovarna, dum, vybaveni kovarny kovarna_vybaveni())
    constructions/gen_constructions.py   ruin_layout -> constructions.json
    furnishing/gen_furnishing.py         specy (kovarna_vybaveni ...) -> 06_furnishing/furnishing.json
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

4. **Generování** (z kořene `Lapikus`):
   ```
   python tools/ruin/gen_layout.py 03_ruin/ruin_layout_draft.json 01_terrain/Zricenina_heightmap_505_50cm.png 03_ruin/blocks/ruin_layout.json
   python tools/constructions/gen_constructions.py 03_ruin/ruin_layout_draft.json 05_constructions/constructions.json
   python tools/furnishing/gen_furnishing.py
   ```
   `gen_layout` spouštěj jen při změně zříceniny nebo sdíleného specu.

### 5. Co spustit v UE (pořadí)

| Změna | Spustit |
|---|---|
| zeď zříceniny, `cap`, `notches`, `edits` (vybourání) | část zříceniny: `03_ruin/blocks/casti/<Obvod/Palac/Ostroh>.py` (úsek hradby u ostrohu patří do **Obvod**, `ZBudova_*` do **Ostroh**). Pak i dostavby, které na ní stojí. |
| krov u ostrohu | `05_constructions/stavby/Ostroh_Krov.py` (`KRYTINA = True/False`), pak `Ostroh_Dostavba.py` (výšky bere z krovu) |
| kamenná dostavba, práh, malta | `Ostroh_Dostavba.py` |
| podlaha | `Ostroh_Podlaha.py` |
| úklid suti | `Sut.py` |
| dům v paláci (`palac_spec.py` → `obydli`); etapy: stavba se `stage` v datech → actory po sadách `base` / `final` / `site` (tag `stage:<sada>`) | **celý dům: `05_constructions/stavby/Palac_Obydli.py`** (seznam `STAVBY`, novou část do něj přidej; `SUT`); jednotlivě `Palac_Obydli_Kamen.py`, `Palac_Obydli_Ohniste.py`, pak `Sut.py`. Po změně průchodů (`D_PASS`, `Palac_S` v `gen_layout.py`) nejdřív `gen_layout.py` a `03_ruin/blocks/casti/Palac.py`. |
| věž: přístřešek hlídky (`tower_spec.py` → `PR`), škody z dobývání (`ruin_edits`) | po změně `ruin_edits`: `gen_layout.py`, pak `05_constructions/stavby/Vez.py` s `RUIN = True` (přestaví `Obvod`, `Vez_Patra`, `Vez_Pristresek`) a `Sut.py`; jen přístřešek `Vez_Pristresek.py`. Po změně `PR` nejdřív mimo UE `gen_meshes.py textile` (plachta na míru) a `gen_constructions.py`. |
| kovárna v paláci (`palac_spec.py`, `gen_constructions.py` → `palac`) | **celá kovárna: `05_constructions/stavby/Palac_Kovarna.py`** (pořadí, suť a vybavení z 06 řeší sám; `RUIN = True` = i část `Palac`). Jednotlivě: `Palac_Kovarna_Pristresek.py`, pak `Palac_Kovarna_Vyhen.py` (výměny u komína berou výšku z krokví), `Palac_Kovarna_Stena.py`, `Palac_Kovarna_Okap.py` (žlab bere výšku z okapové hrany krytiny), `Palac_Kovarna_Kul.py`, `Sut.py`; vybavení `06_furnishing/vybaveni/Palac_Kovarna.py`. Když se změní kapsa pro východní pozednici, zanoření `Palac_J` (`J_SINK`) nebo rozebrání koruny u věže (`J_BREACH`): `gen_layout.py`, `03_ruin/blocks/casti/Palac.py` a až pak stavby a `Sut.py` (nebo `Palac_Kovarna.py` s `RUIN = True`). |
| nový nebo změněný mesh, prop, textura | `gen_meshes.py` / `gen_textures.py` mimo UE, zvednout verzi (`STONE_MESH_VERSION`, `TEX_VERSION`); doimportuje je kterýkoli build. Kontrola vzhledu: `tools/meshes/Ukazka_Meshe.py` |
| všechno | `build_normal.py` (kořen): celý hrad, po něm všechny stavby a vybavení (`VYBAVENI`, `CAPTURE_VYBAVENI`). Totéž co `build_ruin_blocks.py`, pak `build_constructions.py` |
| poškozené assety (NaN v bounds, `InverseFast` v logu, prázdné náhledy, meshe naruby) | `build_fullscope.py` (kořen): smaže generované actory a meshe `SM_Ruin*`, textury a meshe naimportuje znovu a vše postaví. `MATERIALY = True` smaže i generované materiály (ruční ladění se ztratí). Po běhu nepoužívat Undo. |

Ruční úpravy v levelu ukládá Jirka přes `MODE = "capture"` ve stejném skriptu, a to vždy **před** dalším generováním. Ručně upravené vybavení (06) ukládá spouštěč skupiny `06_furnishing/vybaveni/<Skupina>.py` (`capture` zapíše polohy přímo do `furnishing.json`; `list` vypíše posuny proti specu, `reset` vrátí kusy na spec). Podrobně `AGENT_Furnisher_hrad.md`.

### 6. Kontroly a testy

- `python tools/checks/run_checks.py [--layout <ruin_layout.json>] [--only openings,floating,ostroh,palac,obydli,brana]`:
  - `openings`: nad otvory nesmí chybět řada (žádná „kapsa“ nad překladem);
  - `floating`: kameny bez podpory. Známé jsou 3, aktuálně hlásí 5, což je starší stav;
  - `ostroh`: průniky (trámy × zřícenina, krytina × zřícenina, dostavba × krov, dostavba × zřícenina, podlaha × …) a pokrytí krytinou (≥ 99,5 %).
  - `palac`: přístřešek kovárny – průniky dřeva a patních kamenů se zříceninou, sloupy na patních kamenech, krokve na pozednicích, sklon 20° ± 1°, vůle komína ≥ 10 cm, světlá výška, pokrytí krytinou ≥ 99 %, lemování na krytině; stěna z proutí (průniky, zaplnění linie, výška); okap (průniky, okapová hrana nad žlabem, spád, konec nad sudem, sud na zemi); výheň – průniky se zříceninou a se dřevem, výměny v krokvích, komín ≥ 0,8 m nad krytinou, dymník nad ohništěm; vybavení – průniky (záměrná uložení vyjmenovaná), výfučna v otvoru zídky, kovadlina 1,4–1,6 m před výhní, kalicí sud ≤ 1,7 m, průchody ≥ 1,2 m, dřevo pod přesahem, žádná suť v místnosti;
  - `obydli`, `brana`: dům v paláci a strážní stanoviště (kritéria v jejich návrzích).
- `python tools/checks/preview3d.py ostroh|kovarna|obydli|brana <out.png> [--no-roof] [--stage 1|2]`:
  - 3D náhled přes three.js v headless Chromiu;
  - potřebuje `node_modules` s `three@0.160.0` a playwright ve složce `tools/checks` (ve scratchpadu stačí symlink). Když na počítači chybí, vyexportuj kvádry a pohledy (`kovarna_scene` apod.) do JSON a vykresli je v cloudovém workspace (`render`);
  - props jsou v náhledu jen kvádry (bounding box), skutečný tvar a natočení ukáže až UE;
  - jako knihovna: `render(boxes, views, out)` a `stone_boxes(...)` pro vlastní pohledy (detail okna, malta obarvená jinak).
- `python tools/checks/fingerprint.py <kořen> <otisk.json>` vytvoří otisk výstupu včetně mock trasy volání Unrealu:
  - u refaktoringu musí být otisk před změnou a po ní **shodný**;
  - u záměrných změn ho nepoužívej.
- `tools/checks/UE_Test_Formatu_OBJ.py` (spouští Jirka v UE, výsledek v Output Logu): `MODE = "pricina"` rozliší, jestli NaN v bounds dělá stará cache, nebo příznak `bDoFastBuild` v assetu (`KNOWHOW_hrad.md` kap. 5.2). Vzor pro další testy v UE: importuje do dočasné složky, level nemění, výsledek čte z logu.
- **Vlastní testy** dopiš, když je problém vizuální. Osvědčilo se:
  - paprsky přes krytinu nebo zeď (průnik OBB) jako test prosvítání; počítej s natočením (`KNOWHOW_hrad.md` kap. 5.1);
  - kontrola, že kusy malty leží celé uvnitř kamenů (rohy OBB, tolerance spáry 2–3 cm);
  - 2D mapa půdorysu (matplotlib): trámy, prkna, obrys místnosti, nepokrytá místa.

## Z AGENT_Furnisher_hrad

### 3. Struktura kódu (06)

```
Lapikus/
  06_furnishing/
    build_furnishing.py       UE: build / capture / list / reset; mimo UE statistika, list, reset
                              (compute, apply_pose = poloha z levelu -> kus v ramu skupiny)
    furn_data.py              furnishing.json: POSE_KEYS, priznaky kusu, merge (slouceni se specem), reset, zapis se zalohou .bak
    vybaveni/<Skupina>.py     spoustec jedne skupiny (Palac_Kovarna.py): MODE, ITEMS, SKUPINY
    furnishing.json           data skupin + polohy z levelu (NEPREPISOVAT jinak nez gen_furnishing.py)
    README_furnishing.md      technicky navod
  tools/
    furnishing/gen_furnishing.py   specy -> skupiny -> merge do furnishing.json (vypise kusy bez specu, zmeny specu u captured)
    ruin/palac_spec.py        ram palace, kovarna, dum; kovarna_vybaveni() = kusy kovarny, konstanty K_*
    checks/run_checks.py      kontroly (vybaveni v common.state() pod klicem "furn")
    checks/preview3d.py       3D nahled (props jako kvadry)
    meshes/mesh_props.py      tvary props (surove vrcholy = odsazeni stredu bounding boxu)
  05_constructions/zr_stavby/vybaveni.py   typ props: build_props (rozmisteni kusu), spolecny s 05
  zrlib/config.py             LIB_MESHES (jmenovite rozmery, varianty, material), LIB_SHAPES (shape -> mesh), FURN_TAG
  zrlib/pipeline.py           furnishing(only, mode, items), build_all (vybaveni po stavbach 05)
```

Dostupné tvary (`LIB_SHAPES`): `anvil`, `axe`, `barrel`, `basket`, `bed`, `bed_folded`, `bellows`, `broadaxe`, `chest`, `chisel`, `coal_box`, `coal_box_lid`, `crosscut_saw`, `grindstone`, `grindstone_treadle`, `hammer`, `iron_bars`, `ladder`, `mallet`, `nail_hammer`, `nail_header`, `rope`, `shelf`, `stool`, `stump`, `table`, `tongs`, `woodpile`, `workbench` (a stavební `door`, `shutter`, `wattle_panel` …). Kulatina a kůly (`round`, `stake`) jsou `ROUND_SHAPES`. Co chybí, je v `CHECKLIST_assets_navrhy.md` kap. 6.

Actory v levelu: tag `Zricenina_Vybaveni`, `vybaveni:<skupina>`, `id:<skupina>|<kus>`, složka Outlineru `Vybaveni/...`, jméno `Kamen_<skupina>_<kus>`. Build maže jen actory své skupiny.

### 4. Data kusu a jeden JSON

**Skupina** (`furnishing.json` → `groups`): `name`, `type` (`props`), `folder`, `origin` (UE cm), `u`, `v` (jednotkové vektory rámu stavby), `roof` (střecha z 05 pro lana z krokví), `items`. Rám skupiny jde vždy ze specu.

**Kus** (dva způsoby zadání, `zr_stavby/vybaveni.py`):
- **poloha:** `id`, `shape`, `a`, `c` (m, střed půdorysu bounding boxu v rámu: `a` podél `u` = `s`, `c` podél `v` = `n`), `z` (spodek nad terénem, m) nebo `zc` (střed nad terénem), `x` = směr lokální osy X v rámu (výchozí `(1, 0)`), `pitch`, `roll` (st.), `scale` (násobky jmenovitého rozměru) nebo `size` (cm);
- **úsek** (tyč, kůl, lano): `id`, `shape` (`round`, `stake`, `rope`), `d` (průměr m), `p0`, `p1` = (a, c, z) konce osy; `p1 = (a, c, "rafter")` = k ose nejbližší krokve střechy `roof`;
- společné: `cat` (materiál, když to není prop), `finish` (úprava dřeva), `bark`.

**Příznaky z levelu** (zapisuje je jen capture v UE, `furn_data.py`):

| Příznak | Význam | Co s tím při práci |
|---|---|---|
| `captured: true` + `spec` | poloha, otočení a velikost jsou z levelu; `spec` = poloha podle specu | **změna polohy ve specu se neprojeví** (generátor vypíše upozornění). Jirkovu polohu měň jen s jeho souhlasem: `reset` kusu, nebo úprava polohových klíčů v `furnishing.json` |
| `removed: true` | kus Jirka v levelu smazal, nestaví se | generátor ho znovu nepřidá; obnovit jen přes `reset` |
| `manual: true`, `copy_of`, `mesh` | kopie kusu z levelu (Alt+tah), id `<kus>_2`; stejný mesh jako původní kus | ve specu není a nebude; generátor ji nechá |

Generátor (`gen_furnishing.py` → `furn_data.merge`): nové kusy ze specu přidá, kusy bez příznaků přepočítá ze specu, kusy s příznaky nechá, kusy a skupiny, které ve specu už nejsou, **nechá a vypíše**. Výpis generátoru vždy přečti a nahlas ho Jirkovi.

Polohové klíče (`furn_data.POSE_KEYS`): `a`, `c`, `z`, `zc`, `x`, `pitch`, `roll`, `scale`, `size`, `p0`, `p1`, `d`. Ostatní klíče (`shape`, `cat`, `finish`) jdou vždy ze specu, i u kusů s polohou z levelu.

### 5. Postup

#### 5.1 Nová skupina vybavení (nová místnost nebo lokace)

1. **Pochop zadání:** návrh (`new_designs/navrh_*.md`, kapitola vybavení), stav stavby (`Zricenina_03_ruin_stav.md`, stav v hlavičce návrhu), rám stavby ve specu. Orientace `_S/_J/_V/_Z` ověř v datech, nehádej. Zjisti, ve které etapě kusy stojí (`base` / `final` / `site`); etapy vybavení zatím nepoužívá, když je skupina potřebuje, je to požadavek (kap. 9).
2. **Seznam kusů** s meshi: co existuje v `LIB_SHAPES`, co chybí (požadavek na stavitele, zapsat do `CHECKLIST_assets_navrhy.md` kap. 6). Chybějící mesh dočasně nenahrazuj kostkou bez dohody.
3. **Polohy ve specu:** funkce `<stavba>_vybaveni(walls)` v `tools/ruin/<cast>_spec.py`, vrací seznam kusů (vzor `kovarna_vybaveni()`). Hodnoty pojmenuj konstantami (`K_*` u kovárny, nová stavba vlastní předponu) s komentářem, proč tam kus stojí.
   - **Poloha = střed bounding boxu meshe**, ne funkční střed. Odsazení (výfučna měchů 105 cm, rám brusu 7 cm, deska ponku 8,4 cm) změř na surových vrcholech v `mesh_props.py` a zapiš do specu (`KNOWHOW_hrad.md` kap. 5.7).
   - **Natočení:** `x` = směr lokální osy X v rámu; lokální Y je X otočená v UE o +90°. V rámu paláce (levotočivý vůči `s`, `n`): X = +s → Y = −n, X = −n → Y = −s. Svisle zavěšené nářadí `pitch` 90, kladivo `roll` −90; ve specu piš hodnotu výpočtu, `roll` se do UE obrací sám (kap. 5.1 KNOWHOW).
   - Kus u zdi nech od líce aspoň 3,5 cm (líc vystupuje 1–3 cm, `KNOWHOW_hrad.md` kap. 5.5).
4. **Skupina v generátoru:** záznam v `tools/furnishing/gen_furnishing.py` (`name` `<Stavba>_Vybaveni`, `folder` `Vybaveni/<Cast>/<Mistnost>`, rám ze specu, `roof`, když něco visí z krokví). Vygeneruj: `python tools/furnishing/gen_furnishing.py`.
5. **Spouštěče:** `06_furnishing/vybaveni/<Skupina>.py` jako kopie `Palac_Kovarna.py` a ukládací `<Skupina>_Capture.py` jako kopie `Palac_Kovarna_Capture.py`, jiný seznam `SKUPINY` a popis. Když má stavba souhrnný spouštěč v 05 (`Palac_Obydli.py`, `Brana_Straz.py`), přidej do něj `VYBAVENI` podle `05_constructions/stavby/Palac_Kovarna.py` (vybavení se staví až po stavbách, bere z nich výšky).
6. **Kontroly** (kap. 7): průniky se zříceninou, se stavbami a mezi sebou, průchody, funkční vzdálenosti, kusy na zemi nebo na čem stojí. Záměrné dotyky vyjmi jmenovitě a ověř přesným bodem.
7. **Náhled** `preview3d.py` (props jsou jen kvádry); když jde o vzhled, ukaž ho Jirkovi.
8. **Dokumentace** (kap. 9) a hlášení (kap. 8).

#### 5.2 Úprava existující skupiny

1. Spusť `python 06_furnishing/build_furnishing.py list`: vypíše kusy s polohou z levelu (posun proti specu), smazané a kopie. **Tohle je Jirkova práce v levelu, ber ji jako zadání**, ne jako odchylku k opravě.
2. Změny dělej ve specu. U kusu s `captured` se změna polohy neprojeví; buď to Jirkovi řekni a navrhni `reset` kusu, nebo (po dohodě) uprav polohové klíče kusu přímo v `furnishing.json` (po md5 kontrole, se zálohou, jen ty klíče).
3. Když Jirka chce, aby se jeho poloha stala i výchozí ve specu, přenes čísla z `list` do specu. Nepovinné: poloha z levelu platí i bez toho.
4. Nový kus: přidej ho do specu a vygeneruj; ostatní kusy (i s polohou z levelu) zůstanou.
5. Odebrání kusu: odeber ho ze specu a řekni Jirkovi, ať ho smaže v levelu a spustí capture (nebo ho po dohodě odeber z `furnishing.json`). Generátor ho jinak jen vypíše a nechá.
6. Vygeneruj, zkontroluj, hlas.

### 6. Co spustit v UE

| Situace | Spustit |
|---|---|
| jedna skupina vybavení | `06_furnishing/vybaveni/<Skupina>.py` (`MODE = "build"`) |
| stavba včetně svého vybavení | souhrnný spouštěč stavby v 05, např. `05_constructions/stavby/Palac_Kovarna.py` (`VYBAVENI = True`) |
| všechno vybavení | `06_furnishing/build_furnishing.py` |
| uložit úpravy všeho vybavení | `06_furnishing/capture_furnishing.py` (skupiny bez actorů v levelu přeskočí) |
| celý hrad | `build_normal.py` (aditivně); `build_fullscope.py` jen při poškozených assetech. Oba mají `VYBAVENI` (stavět vybavení) a `CAPTURE_VYBAVENI` (před buildem uložit úpravy z levelu, jen když se neměnily meshe props) |
| nový mesh propu (od stavitele) | kterýkoli build ho doimportuje; vzhled `tools/meshes/Ukazka_Meshe.py` |
| uložit ruční úpravy | `06_furnishing/vybaveni/<Skupina>_Capture.py` (kovárna `Palac_Kovarna_Capture.py`) nebo spouštěč skupiny s `MODE = "capture"`: posun, otočení, Scale, smazání, kopie (Alt+tah) → přímo do `furnishing.json` (záloha `.bak`) |
| přehled úprav | `MODE = "list"` (nebo mimo UE `python 06_furnishing/build_furnishing.py list`) |
| vrátit na spec | `MODE = "reset"`, `ITEMS = ["Kus", ...]` (i s kopiemi), pak znovu `build` |

Pořadí při změně: **capture před každým novým generováním a buildem**, pokud Jirka v levelu něco upravil. Capture jen po buildu se stejnými meshi (`KNOWHOW_hrad.md` kap. 5.3): po změně meshe by staré actory vyšly jako posunuté nebo smazané. Když se mesh propu změnil, řekni Jirkovi, ať nejdřív udělá capture, pak build.

### 7. Kontroly a testy

- `python tools/checks/run_checks.py --only palac` (kovárna; pro nové skupiny přidej sekci do `run_checks.py`, vybavení je v `common.state()` pod klíčem `furn`, kusy v `S["furn"][<skupina>]["loose"]`):
  - průniky se zříceninou, se stavbami skupiny a mezi sebou (`common.collisions`, tolerance 1 cm); záměrná uložení (kovadlina na špalku, víko na truhlíku, lano kolem krokve) vyjmenuj v páru;
  - funkční vzdálenosti z návrhu (kovárna: kovadlina 1,4–1,6 m od výhně, kalicí sud ≤ 1,7 m od kovadliny i výhně, výfučna v otvoru zídky);
  - průchody ≥ 1,2 m (`gap` půdorysů kvádrů), dřevo pod přesahem, suť v místnosti uklizená.
- **Kontroly běží na datech včetně poloh z levelu.** Když selžou kvůli kusu s `captured`, neopravuj ho potichu: nahlas Jirkovi, který kus, o kolik a proč (např. „kalicí sud posunutý v levelu je 1,9 m od výhně“) a navrhni řešení.
- Kontroly kvádrem jsou hrubé (měchy, sudy): skutečný tvar může být volný i tam, kde kvádr koliduje. Rozhoduje přesný bod nebo náhled v UE.
- `python tools/checks/preview3d.py kovarna <out.png>`: 3D náhled, props jako kvádry (potřebuje `three@0.160.0` a playwright v `tools/checks`). Skutečný tvar a natočení ukáže až UE.
- `python 06_furnishing/build_furnishing.py`: statistika skupin (počty kusů podle materiálu) – rychlý test, že data jdou spočítat.
- **Při změně `build_furnishing.py` nebo `furn_data.py`** ověř round-trip mimo UE: kus → `apply_pose` (beze změny, s posunem, otočením a změnou velikosti) → znovu `_stones` musí dát stejnou polohu (tolerance < 1 cm, < 1°), `furn_data.reset` musí vrátit polohu specu, `merge` nechat `captured` / `removed` / `manual`. Pracuj na kopii dat (`DATA_PATH`), originál neměň.
- Screenshot s chybou: nejdřív příčina v datech nebo kódu (spec, odsazení středu, natočení, poloha z levelu?), pak oprava; `KNOWHOW_hrad.md` kap. 6.

## Z KNOWHOW_hrad

### 4. Co kdy spustit v UE

| Situace | Skript |
|---|---|
| změna jedné části zříceniny | `03_ruin/blocks/casti/<Obvod/Palac/Ostroh>.py`, pak dostavby, které na ní stojí |
| změna jedné stavby | `05_constructions/stavby/<Stavba>.py` |
| celý dům posádky v paláci | `05_constructions/stavby/Palac_Obydli.py` (všechny hotové části v pořadí + suť; staví všechny sady etap) |
| celá kovárna v paláci | `05_constructions/stavby/Palac_Kovarna.py` (všechny části v pořadí + suť a vybavení; `RUIN = True` i část `Palac`) |
| celá věž (dřevo v patrech, přístřešek hlídky) | `05_constructions/stavby/Vez.py` (`RUIN = True` i část `Obvod`) |
| vybavení (06) | `06_furnishing/vybaveni/<Skupina>.py` (`MODE` build / capture / list / reset), všechno `06_furnishing/build_furnishing.py` |
| všechno | `build_normal.py`: hrad, pak stavby; assety jen doplňuje |
| poškozené assety (NaN v bounds, `InverseFast` v logu, prázdné náhledy, meshe naruby) | `build_fullscope.py`: smaže generované actory a meshe a postaví vše znovu; po běhu nepoužívat Undo |
| kontrola vzhledu meshí a props | `tools/meshes/Ukazka_Meshe.py` |
| uložení ručních úprav | stejný skript s `MODE = "capture"`; vybavení (06) spouštěč skupiny ve `06_furnishing/vybaveni/` (i výpis `list` a zahození `reset`) |

Podrobná tabulka podle druhu změny je v `AGENT_Stavitel_hrad.md`, kap. 5. Společná logika spouštění je v `zrlib/pipeline.py`.

## Předzpracování (doplní Curator)

- Kategorie: dokumentace kroků a sdíleného kódu
- Souvisí s: [[03_ruin]], [[05_constructions]], [[06_furnishing]]
- Návrh zařazení: Architekt kap. 4 → [[03_ruin]] (model zdí, úpravy v datech) a `Steps/shared/Typy_staveb` (typy 05, knihovna dílců); Architekt kap. 7 a Stavitel kap. 6 → `Steps/shared/Kontroly`; Stavitel kap. 3 → `Steps/shared/` (zrlib, struktura kódu); Stavitel kap. 4 krok 4, kap. 5 a KNOWHOW kap. 4 → *Spouštění* v [[03_ruin]], [[05_constructions]], [[06_furnishing]]; Furnisher kap. 3–7 → [[06_furnishing]]
