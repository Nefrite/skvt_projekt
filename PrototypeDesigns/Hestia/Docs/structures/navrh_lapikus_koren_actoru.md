---
# orchestrace
type: design
validity: valid
derived_from:
alternative_to: []
updated: 2026-11-23
aliases: []
# hra
status: selected
domain: structures
category: []
entity: "[[Lapikus]]"
depth: 4
build_step: 05_constructions
assets: []
---
# Návrh: Konvence kořene sloučených actorů staveb (03 a 05)

## Souhrn
Návrh konvence umístění a natočení kořene (`pivot`) sloučených actorů s `InstancedStaticMeshComponent` (ISM) v krocích [[03_ruin]] a [[05_constructions]], které dnes vznikají v počátku mapy `(0, 0, 0)` a mají v Unreal Editoru ovládací prvky 30–55 m od geometrie stavby (144 ze 149 ISM actorů hlásí `pivot_far` nad 500 cm).
- **Příčina v kódu (*Výchozí stav*):** `ue_actors.place_ism` a `_ism_actor` (`Lapikus/zrlib/ue_actors.py`) už podporují parametr `pivot = (x, y, z, yaw)` a vkládají instance ve světových souřadnicích (`bWorldSpace = True` po `set_actor_location_and_rotation`), ale `build_ruin_blocks.py` (03) i `build_constructions.py` (05) volají `place_ism` s `pivot=None` (s jedinou výjimkou 4 hranic materiálu na staveništi domu s `"pile": true`).
- **Schválená konvence (*Návrh*, rozhodnutí GameDesignera 2026-11-23):** kořen má vždy svislou osu Z (`roll = 0`, `pitch = 0`) a natočení `yaw` podél hlavní osy `u` rámu stavby (v 05) nebo osy přímého úseku zdi `seg` (v 03). Pro polohu `(x, y, z)` je schválena **Varianta C**: společný kořen všech materiálových/etapových vrstev jedné stavby v [[05_constructions]] a jednoho úseku zdi v [[03_ruin]] ve středu jejich 3D obálky `(cx, cy, cz)`, s automatickým vlastním středem u odlehlých lokálních dílů vzdálených `> 300 cm` (`Palac_S_Osteni`, venkovní ochoz `Vez_Patra_Drevo_Krev`). Snižuje `pivot_far` na **0 ze 149 ISM actorů**.
- **Dopad a ověření (*Souhrn specifikace*, *Vazby a závislosti*, *Ověření*):** mění se jen sestavení v UE (`zrlib/ue_actors.py`, `build_ruin_blocks.py`, `build_constructions.py`), nikoli `*_spec.py`, JSON data, `capture` ani `detach_stones.py`. Existující level se přestaví přes `build_normal.py`.

## Zadání / záměr
- **Odkud:** GameDesigner (2026-11-23).
- **Problém:** Sloučené actory staveb (`InstancedStaticMeshComponent`, ISM: kameny zříceniny v [[03_ruin]] a dřevo, zdivo či mazanina dostaveb v [[05_constructions]]) mají kořen (`get_actor_location`) v počátku mapy `(0, 0, 0)` a geometrii instancí na ostrohu. Transformační gizmo v Unreal Editoru i fokus kamery (`F`) jsou proto 30–55 m daleko od stavby (např. u `Palac_Kovarna_Pristresek_Drevo`).
- **Cíl:**
  1. Popsat, kde v kódu (`Lapikus/zrlib`, `tools/ruin`, `05_constructions/zr_stavby`, `03_ruin/blocks`) vznikají sloučené actory a jak se nastavuje poloha kořene a instancí.
  2. Navrhnout konvenci kořene: kde má stát, jak je natočený a jak se týká dílů (`Okap`, `Pristresek`, `Vyhen`, `Jadro`, `Lic`, `Osteni` aj.).
  3. Popsat dopad na stavby, kroky, data (`*_spec.py`), sestavení, existující level a způsob ověření (signál `pivot_far` po core 0.21.1 a vizuální kontrola).
  4. Předložit návrh ke schválení GameDesignerovi a připravit předání pro roli [[Builder]] ([[predani_lapikus_koren_actoru_stavitel]]). V levelu ani kódu se v rámci návrhu nic nemění.

## Výchozí stav

### 1. Kde v kódu vznikají sloučené actory a transformace instancí
1. **Tvorba ISM actorů – `Lapikus/zrlib/ue_actors.py`:**
   - `_new_actor(unreal, eas)` (ř. 10–14) vytvoří v levelu prázdný `unreal.Actor` na souřadnici `unreal.Vector(0, 0, 0)` a `_add_ism` (ř. 16–21) mu přes `SubobjectDataSubsystem` přidá jednu `InstancedStaticMeshComponent` pro každý použitý `StaticMesh` (záložní větev přes Blueprint `BLOCK_BP` na ř. 44–54 spawnuje samostatný actor na mesh v `loc, rot`).
   - `_ism_actor(unreal, eas, name, folder, parts, material, tag, pivot=None)` (ř. 23–59) už volitelný parametr `pivot = (x, y, z, yaw)` podporuje:
     - pokud je `pivot` zadán, nastaví `loc = unreal.Vector(*pivot[:3])` a `rot = unreal.Rotator(roll=0.0, pitch=0.0, yaw=pivot[3])` a **před** přidáním instancí zavolá `actor.set_actor_location_and_rotation(loc, rot, False, False)` (ř. 37);
     - pokud je `pivot=None`, actor zůstane v `(0, 0, 0)` s rotací `(0, 0, 0)`;
     - následně pro každou komponentu volá `comp.add_instances(trs, False, True)` (ř. 41, druhý bool `True` = `bWorldSpace = True`).
   - `place_ism(unreal, eas, label, folder, stones, cube, meshes, material, tag, extra_tags=(), pivot=None)` (ř. 75–86) seskupí dílce `stones` podle `StaticMesh`, pro každý dílec `s` spočte jeho **světovou** transformaci `stone_transform(unreal, s, m, nom)` (`Lapikus/zrlib/ue_assets.py`, ř. 584–596: světová poloha středu dílce `s.x, s.y, s.z`, rotace `ue_rotator` s `-s.roll, s.pitch, s.yaw`, lokální korekce os/středu meshe `_mesh_fix` a měřítko na `s.sx, s.sy, s.sz`) a zavolá `_ism_actor(..., pivot=pivot)`.
   - Protože `add_instances` běží s `bWorldSpace = True` až po případném `set_actor_location_and_rotation`, Unreal automaticky přepočte světové transformace instancí do lokálního prostoru komponenty. Světová poloha geometrie instancí se změnou `pivot` **nemění**.
2. **Zřícenina [[03_ruin]] – `Lapikus/03_ruin/blocks/build_ruin_blocks.py`:**
   - V `build_in_unreal()` (ř. 181–191) se kameny každé zdi a dlažby z `compute_blocks()` (`03_ruin/blocks/zr_ruin/compute.py`) seskupí podle `(s.seg, s.cat)`, kde `s.seg` je index přímého úseku zdi (u `Hradba_Z_S` seskupený přes `seg_group` do úseků `01`..`09`, u `Hradba_V` úseky `01`..`07`, u ostatních zdí `nseg = 1`) a `s.cat` je kategorie materiálu (`face` → `Lic`, `core` → `Jadro`, `crown` → `Koruna`, `frame` → `Osteni`, `floor` → `Podlaha`).
   - Pro každou skupinu `(seg, cat)` volá `ue_actors.place_ism(...)` **bez parametru `pivot` (`pivot=None`)**. Všech 107 ISM actorů zříceniny (03) má proto kořen v `(0, 0, 0)`.
3. **Dostavby [[05_constructions]] – `Lapikus/05_constructions/build_constructions.py`:**
   - V `compute()` (ř. 166–198) vygenerují moduly `05_constructions/zr_stavby/*.py` ze specifikace v `constructions.json` (sestavené přes `tools/constructions/gen_constructions.py` z `tools/ruin/*_spec.py`) seznam dílců `Stone`. Dílce s `s.loose == False` jdou do `g["stones"]` (ISM), dílce s `s.loose == True` do `g["loose"]` (samostatné `StaticMeshActor`).
   - V `build_in_unreal()` (ř. 250–258) se `g["stones"]` každé stavby rozdělí podle `(s.cat, s.stage or "")` na ISM actory `<Stavba>_<Kategorie>[_<Stage>]` a volá se `ue_actors.place_ism(..., pivot=g.get("pile"))`.
   - Klíč `g["pile"]` plní funkce `_pile()` (ř. 204–218) **pouze** u staveb s `"pile": true` v `constructions.json`, což jsou 4 hranice materiálu na staveništi domu (`Palac_Obydli_Stavenisko_Kulatina`, `_Tramy`, `_Prkna`, `_Kozy` = 5 ISM actorů). Pro ně `_pile` nastaví `pivot = [px, py, pz, yaw]` v těžišti půdorysu `(px, py)` a na spodku hranice `pz = min(s.z - s.sz / 2)` s `yaw = 0.0` (nebo posunem z `constructions_edits.json`).
   - Všech ostatních 37 ISM actorů dostaveb (05) má `g.get("pile") == None` → kořen v `(0, 0, 0)`.
4. **Samostatné actory (`loose` v 03/05 a celé [[06_furnishing]]):**
   - Vznikají přes `ue_actors.spawn_loose()` (ř. 89–100) přímo na transformaci `stone_transform(s)`, takže mají kořen ve středu svého meshe (`pivot_offset = 0.0 cm`).

### 2. Stav v levelu podle reportů `Maintenance/reports/ue_*.json`
Čtecí modul `Hestia/_core/scripts/hestia_ue.py` (core 0.21.1) měří `pivot_offset` jako 3D vzdálenost kořene actoru (`get_actor_location`) od středu AABB obálky jeho geometrie (`bounds.origin`) a započte actor do `pivot_far`, pokud `pivot_offset > 500 cm`.

| Entita | Celkem actorů (2026-11-23 / 21) | Z toho ISM | `pivot_far` (> 500 cm) | `pivot_offset` ISM actorů (cm) | Které actory entity `pivot_far` nemají |
|---|---|---|---|---|---|
| [[Hradby_a_Brana]] | 53 | 53 | **53 / 53** | 3 150 – 5 360 | – |
| [[Palac]] | 17 | 17 | **17 / 17** | 3 280 – 4 204 | – |
| [[Vez]] | 21 | 21 | **21 / 21** | 3 641 – 4 466 | – |
| [[Strazni_Vez]] | 14 | 14 | **14 / 14** | 4 674 – 5 263 | – |
| [[Guesthouse]] | 13 | 12 | **12 / 13** | 4 896 – 5 358 | 1× `StaticMeshActor` (`Kamen_Ostroh_Dostavba_Prah`, 0 cm) |
| [[Palac_Obydli]] | 29 (dříve 18) | 17 (dříve 14) | **12 / 29** (dříve 11 / 18) | 3 314 – 3 722 (hranice: 5 – 69) | 5× ISM hranice `Stavenisko_*` s `pile: true` (5–69 cm) + 12× `StaticMeshActor` (0 cm) |
| [[Palac_Kovarna]] | 15 | 8 | **8 / 15** | 3 350 – 3 584 | 7× `StaticMeshActor` (5× patní kámen, sud, kůl, 0 cm) |
| [[Brana_Straz]] | 4 | 4 | **4 / 4** | 5 162 – 5 451 | – |
| [[Vez_Pristresek]] | 16 | 3 | **3 / 16** | 4 512 – 4 627 | 13× `StaticMeshActor` (podkladní, zátěžové a kotevní kameny, 0 cm) |
| **Celkem (9 entit)** | **182** | **149** | **144 / 182** (100 % ISM bez `pile`) | **3 150 – 5 451** | 5× ISM s `pile: true` + 33× `StaticMeshActor` |

*(Poznámka: Pět ISM actorů hranic staveniště v `ue_Palac_Obydli.json` s `pivot_offset = 5,0 až 68,8 cm` potvrzuje, že nastavení kořene přes `actor.set_actor_location_and_rotation` před `comp.add_instances(trs, False, True)` v `_ism_actor` v UE 5.8 funguje správně.)*

## Návrh

### 1. Proč nelze použít surový počátek rámu (`origin`) ze specifikací `*_spec.py`
- V `tools/ruin/palac_spec.py` je `frame()["origin"] = [-2350, -50]` počátek celého paláce (JZ roh `Palac_J`, `s = 0`). Kovárna (`Palac_Kovarna_*`) však leží ve východní místnosti v `s = 24,8–30,75 m` (~27 m od `origin`) a dům posádky (`Palac_Obydli_*`) ve střední místnosti v `s = 10,1–21,4 m` (~16 m od `origin`). Kořen umístěný v `origin` rámu paláce by zůstal 16–27 m od stavby (`pivot_offset` 1 600–2 900 cm > 500 cm).
- Zdi v `03_ruin` (lomené čáry `points`) ani stavby `Ostroh_Dostavba` a `Ostroh_Podlaha` v `constructions.json` klíč `origin` nebo `ref` nemají.
- Poloha kořene se proto musí odvodit z **geometrické obálky dílců `Stone`** dané stavby / úseku zdi / actoru, zatímco ze specifikace (rámu stavby nebo úseku zdi) se převezme **natočení `yaw`**.

### 2. Natočení kořene (`yaw`, `pitch`, `roll`)
- **Svislá osa:** vždy `roll = 0.0`, `pitch = 0.0` (světová osa +Z kořene míří svisle vzhůru i u šikmých střech `pult_roof`, `fan_roof` a na svahu).
- **Natočení `yaw` kolem osy Z:**
  - **Dostavby [[05_constructions]]:** `yaw` ve směru hlavní osy `u` rámu stavby (`yaw = round(degrees(atan2(u[1], u[0])), 2)` z `spec["u"]` v `constructions.json`):
    - Palác (`Palac_Kovarna_*`, `Palac_Obydli_*`): osa `u = s` podél `Palac_J` k věži (`yaw = -12,61°`);
    - Věž (`Vez_Patra`, `Vez_Pristresek`): osa `u` podél `Vez_J` k východu (`yaw = -12,61°`);
    - Ostroh (`Ostroh_Krov`, `Ostroh_Podlaha`, `Ostroh_Dostavba`): osa `u` podél `ZBudova_V` (`yaw = -102,61°`; u `Ostroh_Dostavba`, která nemá pole `u`, směr prvního úseku hlavní zdi `walls[0]["pts"]`);
    - Brána (`Brana_Straz_*`): osa `u` podél `Brana_S` k východu (`yaw = -12,62°`).
    - *Význam v editoru:* hrad je vůči světovým osám X/Y pootočený o ~12,6°. S `yaw` v ose rámu stavby míří v režimu *Local Space* (`Ctrl + ~`) osa +X gizma přesně podél hlavní osy stavby (`u` / `s`) a osa +Y kolmo na ni (`v` / `n` / `d`).
  - **Zřícenina [[03_ruin]]:**
    - U zdí (`build_wall_stones`): směr přímého úseku `seg` zdi (u víceúsekových zdí se `seg_group`, jako je zaoblená `Hradba_Z_S`, směr spojnice prvního a posledního kamene úseku `seg`, resp. hlavní směr úseku z `wd["points"]`).
    - U kamenné dlažby (`Vez_Dlazba`): směr osy `u` z `fs["u"]` (`yaw = -12,61°`).
  - **Hranice materiálu (`"pile": true` v 05):** zůstává beze změny dosavadní `_pile()` (`yaw = 0.0` před posunem, resp. uložené `yaw` z `constructions_edits.json`), aby se nezměnilo chování `capture_edits()`.

### 3. Poloha kořene `(x, y, z)` a vztah k dílům – varianty
Obálka (AABB) množiny dílců `stones` se v Pythonu spočítá z `Stone(x, y, z, sx, sy, sz, yaw, pitch, roll)` každého dílce jako `[min_x, min_y, min_z, max_x, max_y, max_z]` (nikoli prostý aritmetický průměr středů `sum(s.x)/len`, který by u nerovnoměrně hustých dílců jako latě nebo ovázání posunul kořen ke kraji). Střed obálky v půdorysu je `cx = (min_x + max_x) / 2`, `cy = (min_y + max_y) / 2`, střed výšky `cz = (min_z + max_z) / 2`, pata `z_min = min_z`.

Pro vztah kořene k jednotlivým dílům (stavbám `Palac_Kovarna_Pristresek`, `_Vyhen`, `_Stena`, `_Okap` a jejich materiálovým/etapovým ISM actorům `_Drevo`, `_Kamen`, `_Malta`, `_Mazanina`, `_Lic`, `_Jadro`, `_Koruna`, `_Osteni`, `_Base`, `_Final`) byly nad všemi 149 ISM actory z `Maintenance/reports/ue_*.json` ověřeny tři varianty:

| Kritérium | Varianta A: Vlastní 3D střed každého ISM actoru | Varianta B: Společný kořen všech vrstev stavby / úseku zdi (B1: `cz`, B2: `z_min` v 05) | Varianta C (Doporučená): Společný kořen vrstev stavby / úseku zdi (`cz`) + vlastní střed u odlehlých dílů (> 300 cm) |
|---|---|---|---|
| **Kde stojí kořen `(x, y, z)`** | V 3D středu `(cx, cy, cz)` obálky dílců `sts` daného ISM actoru (u `pile: true` spodek hranice `(cx, cy, z_min)`) | Všechny ISM actory jedné stavby `stavba:<Jméno>` v 05 resp. jednoho úseku `(zed, seg)` v 03 sdílejí `(cx, cy, cz)` (B1) nebo v 05 `(cx, cy, z_min)` (B2) celé stavby/úseku | Všechny ISM vrstvy jedné stavby v 05 resp. úseku `(zed, seg)` v 03 sdílejí `(cx, cy, cz)` stavby/úseku; pokud je střed dílu `sts` dál než `300 cm` od středu stavby/úseku, dostane vlastní `(cx, cy, cz)` |
| **Chování u dílů (`Pristresek`, `Okap`, `Vyhen`, `Stena`)** | Každá stavba i každá její materiálová vrstva má kořen ve svém středu | Každá samostatná stavba v `constructions.json` (`Pristresek`, `Okap`, `Vyhen`, `Stena`) má vlastní kořen; vrstvy uvnitř jedné stavby (`Vyhen_Kamen`, `_Mazanina`, `_Drevo`, `_Uhli`) mají kořen v jednom bodě | Stejné jako B1: vrstvy téže stavby (`_Kamen`, `_Malta`, `_Drevo_Base`, `_Drevo_Final`) i vrstvy úseku zdi (`_Lic`, `_Jadro`, `_Koruna`) sdílejí jeden kořen; odlehlé díly (`Palac_S_Osteni`, venkovní ochoz `Vez_Patra_Drevo_Krev`) mají kořen přímo na sobě |
| **Počet ISM s `pivot_far` (> 500 cm) ze 149** | **0 / 149** (`max` ~35 cm) | **B1:** 2 / 149 (`Palac_S_Osteni` 1 122 cm, `Vez_Patra_Drevo_Krev` 652 cm)<br>**B2:** 3 / 149 (+ `Vez_Patra_Drevo_Stare` 854 cm; kdyby `z_min` platilo i pro 14m zdi věže 03, bylo by 23 / 149) | **0 / 149** (`max` 270 cm) |
| **Složitost změny v kódu** | Nejjednodušší (výchozí výpočet přímo v `ue_actors.place_ism`) | Střední (výpočet kořene skupiny před cyklem přes materiály v 03 a 05) | Střední (společný kořen skupiny + 1 podmínka `dist > 300` v `place_ism`) |

**Doporučení architekta:**
- Doporučuji **Variantu C** (případně nejjednodušší **Variantu A**):
  1. Samostatné stavby v `constructions.json` (`Palac_Kovarna_Pristresek`, `Palac_Kovarna_Vyhen`, `Palac_Kovarna_Stena`, `Palac_Kovarna_Okap`, `Palac_Obydli_Kamen`, `Palac_Obydli_Ohniste`, `Palac_Obydli_Krov`, `Palac_Obydli_Srub`, `Ostroh_Krov`, `Ostroh_Dostavba`, `Ostroh_Podlaha`, `Brana_Straz_Kamen`, `Brana_Straz_Podesta`, `Brana_Straz_Kryty`, `Vez_Patra`, `Vez_Pristresek`) mají každá **vlastní kořen** – když v editoru vybereš `Palac_Kovarna_Okap_Drevo`, gizmo je na okapu, ne uprostřed střechy přístřešku.
  2. Vrstvy uvnitř jedné stavby (např. `Palac_Obydli_Kamen_Kamen_Base` a `_Malta_Base`, nebo `Palac_Obydli_Srub_Drevo_Base` a `_Final`) a vrstvy jednoho úseku zdi (`_Lic`, `_Jadro`, `_Koruna`) mají ve **Variantě C** společný kořen uprostřed obálky této stavby / úseku zdi, takže při společném výběru vrstev v Outlineru sedí jejich kořeny v jednom bodě.
  3. Pokud některá vrstva pokrývá jen malý okraj dlouhé zdi nebo stavby a její střed je od společného kořene dál než `300 cm` (konkrétně `Palac_S_Osteni` u západního portálu 32m zdi `Palac_S` a venkovní ochoz `Vez_Patra_Drevo_Krev` na severní stěně věže), dostane ve **Variantě C** svůj vlastní střed `(cx, cy, cz)`. Tím mají všechny ISM actory v celém hradě `pivot_offset <= 270 cm < 500 cm` (`pivot_far = 0`) a gizmo není nikdy 6–11 m mimo geometrii vybraného actoru.
  4. Výška `z = cz` (střed výšky obálky) místo `z_min` (paty) je nutná minimálně u zdí 03 (zdi věže jsou vysoké 14,4 m, takže pata zdi je o 6,5–7,5 m pod středem geometrie a při `z_min` by 13 actorů věže překročilo práh `pivot_far_cm = 500 cm`) i u vícepatrového `Vez_Patra` (kde 2. patro `Vez_Patra_Drevo_Stare` leží 8,4 m nad patou věže). U hranic materiálu s `"pile": true` zůstává `z = z_min` (spodek hranice na terénu).

## Souhrn specifikace
- **Sdílená knihovna `Lapikus/zrlib/ue_actors.py`:**
  - Nová pomocná funkce `stones_bounds(stones) -> (lo, hi)` a `stones_pivot(stones, yaw=0.0, bottom=False) -> [x, y, z, yaw]`:
    - pro každý `s in stones` spočte z `s.x, s.y, s.z, s.sx, s.sy, s.sz, s.yaw, s.pitch, s.roll` poloviční průměty `ex, ey, hz` do světových os a vrátí `cx = round((min_x + max_x) / 2, 2)`, `cy = round((min_y + max_y) / 2, 2)`, `cz = round(min_z if bottom else (min_z + max_z) / 2, 2)`, `round(yaw, 2)`.
  - V `place_ism(unreal, eas, label, folder, stones, cube, meshes, material, tag, extra_tags=(), pivot=None, yaw=0.0)`:
    - u Varianty A: pokud `pivot is None and stones`, spočte `pivot = stones_pivot(stones, yaw=yaw)`;
    - u Varianty C: pokud je předán společný `pivot` stavby/úseku (bez `pile: true`) a 3D vzdálenost jeho `(x, y, z)` od vlastního středu `stones_pivot(stones, yaw=pivot[3])[:3]` přesáhne `300.0 cm`, použije se vlastní střed `stones_pivot(stones, yaw=pivot[3])`.
- **Krok [[03_ruin]] – `Lapikus/03_ruin/blocks/build_ruin_blocks.py`:**
  - V `build_in_unreal()` (ř. 183–191) pro každý úsek `seg` zdi/podlahy `name` spočítat společný kořen úseku `seg_stones = [s for (sg, _), sts in groups.items() if sg == seg for s in sts]` s `yaw` hlavního směru úseku a předat `pivot` do `ue_actors.place_ism(...)`.
- **Krok [[05_constructions]] – `Lapikus/05_constructions/build_constructions.py`:**
  - V `compute()` / `build_in_unreal()` (ř. 186–189, 250–258) určit `yaw` stavby ze `spec.get("u")` (`degrees(atan2(u[1], u[0]))`, u `Ostroh_Dostavba` ze směru první zdi `spec["walls"][0]["pts"]`) a pro stavby bez `g.get("pile")` předat `pivot = ue_actors.stones_pivot(g["stones"], yaw=yaw)` do `ue_actors.place_ism(...)`. Pro stavby s `"pile": true` zůstává `pivot = g.get("pile")`.
- **Data a specifikace (`tools/ruin/*_spec.py`, `ruin_layout.json`, `constructions.json`, `furnishing.json`):** beze změny.

## Vazby a závislosti
- **Kompatibilita s `capture` a `detach_stones.py`:**
  - `ue_actors.scan_level()` (ř. 115) i `03_ruin/blocks/detach_stones.py` (ř. 96) čtou polohy instancí přes `comp.get_instance_transform(i, True)` (`bWorldSpace = True`). Změna polohy a natočení kořene actoru proto nijak neovlivní `capture_manual_edits()` v 03, `capture_edits()` v 05 ani `detach_stones.py`. Všechna uložená data v `manual_edits.json` a `constructions_edits.json` zůstávají platná.
- **Známá past – ruční posun celého ISM actoru v editoru u staveb bez `"pile": true`:**
  - U běžných zdí (03) a staveb (05 bez `"pile": true`) porovnává `capture` světové souřadnice jednotlivých instancí (`instance_key(s) not in present` → `removed.add(s.id)`). Pokud by někdo v editoru posunul celý ISM actor běžné stavby nebo zdi pomocí nového gizma o ≥ 1 cm a spustil `capture`, `capture` by všechny jeho instance vyhodnotil jako smazané (`removed`).
  - Kořen běžných ISM actorů slouží pro výběr, orientaci, fokus kamery (`F`) a kontrolu v editoru; k ručnímu posouvání v levelu s uložením přes `capture` slouží pouze hranice s `"pile": true` a samostatné actory (`loose` a `06_furnishing`).
- **Dopad na existující level (`/Game/Skvt/LapikusPrototypeMap`):**
  - Existující ISM actory v levelu mají kořen v `(0, 0, 0)` až do přestavění.
  - Po úpravě kódu stačí v Unreal Editoru spustit `Lapikus/build_normal.py` (případně `03_ruin/blocks/build_ruin_blocks.py` a `05_constructions/build_constructions.py`). Build smaže generované actory podle tagů (`Zricenina_Ruin`, `Zricenina_Stavby`) a postaví je znovu s novými kořeny; světová poloha všech kamenů a dřeva zůstane beze změny. Pokud jsou v levelu neuložené ruční úpravy od posledního buildu, je nutné před přestavěním spustit `capture`.
- **Dokumentace kroků:** po implementaci [[Builder]] doplní zmínku o kořenech ISM actorů do [[03_ruin_generator]] a [[05_constructions]] a aktualizuje hlavičku `Lapikus/zrlib/ue_actors.py`.

## Ověření
1. **Kontroly mimo UE (Builder po úpravě kódu):**
   - `python Lapikus/tools/checks/run_checks.py` – všechny kontroly (`openings`, `floating`, `ostroh`, `palac`, `obydli`, `brana`, `vez`) musí projít bez chyby.
   - `python Lapikus/tools/checks/fingerprint.py Lapikus <otisk_po.json> --compare <otisk_pred.json>` – hashe kamenů a dílců (`03_lvl`, `03_rubble`, `05`) musí být shodné s výchozím stavem; liší se jen stopa volání Unreal API (`ue_03_full`, `ue_03_palac`, `ue_05_full`, `ue_05_ostroh`) o volání `set_actor_location_and_rotation`.
2. **Kontrola v Unreal Editoru a přes `ue_query` (core 0.21.1):**
   - Přestavět level spuštěním `Lapikus/build_normal.py`.
   - Spustit `Lapikus/tools/checks/UE_Kontrola_Transformaci.py` – 0 neplatných transformací a 0 vadných bounds.
   - Vygenerovat čtecí dotaz `python Hestia/_core/scripts/hestia.py ue_query --emit --all --apply`, spustit skript v editoru, naimportovat výsledky `python Hestia/_core/scripts/hestia.py ue_query --import --all --apply` a obnovit huby `python Hestia/_core/scripts/hestia.py hubs --apply`.
   - V `Maintenance/reports/ue_*.json` a v sekcích `## Stav v UE` všech 9 dotčených entit ([[Hradby_a_Brana]], [[Palac]], [[Vez]], [[Strazni_Vez]], [[Guesthouse]], [[Palac_Obydli]], [[Palac_Kovarna]], [[Brana_Straz]], [[Vez_Pristresek]]) ověřit, že **`pivot_far` je `0`** (pokud byla vybrána Varianta A nebo C).
3. **Vizuální kontrola v editoru:**
   - Vybrat v Outlineru `Palac_Kovarna_Pristresek_Drevo`, `Palac_Kovarna_Okap_Drevo`, `Palac_J_Jadro`, `Palac_S_Osteni`, `Vez_Patra_Drevo_Krev` a `Hradba_Z_S_03_Lic` – transformační gizmo leží přímo u stavby/zdi, v režimu *Local Space* míří osa +X podél hlavní osy stavby/zdi a klávesa `F` vycentruje kameru na vybraný actor.

## Otevřené otázky
- [x] Kterou variantu umístění kořene ISM actorů schvaluješ pro implementaci: **Variantu C** (doporučená: společný kořen všech materiálových/etapových vrstev jedné stavby v 05 a jednoho úseku zdi v 03 ve středu jejich 3D obálky `cz`, s vlastním středem u odlehlých dílů > 300 cm jako `Palac_S_Osteni` a `Vez_Patra_Drevo_Krev`; `pivot_far = 0`), **Variantu A** (každý ISM actor ve středu své vlastní 3D obálky `cz`; `pivot_far = 0`), nebo **Variantu B2** (u dostaveb 05 kořen na úrovni paty/podlahy `z_min`, u zdí 03 ve středu výšky `cz`)? — Architect, 2026-11-23 → **Rozhodnuto (GameDesigner, 2026-11-23):** Schválena **Varianta C**.
