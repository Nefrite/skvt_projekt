---
# orchestrace
type: state
validity: valid
updated: 2026-11-24
aliases: []
# hra
domain: structures
entity: "[[Brana]]"
depth: 4
build_step: 05_constructions
assets: []
---
# Brana – stav stavby (šíjový příkop, mostní lávka a zátaras)

## Souhrn
Skutečný stav šíjového příkopu, přístupového úvozu, únikové rampy ([[01_terrain]]), kamenného mostního pilíře a opěry ([[03_ruin]], část `Obvod`) a dřevěné mostní lávky se zátarasem ([[05_constructions]], sada `base`) před východní branou proti návrhu [[navrh_brana_prikop]] (k 24. 11. 2026). Čelní terénní valy před příkopem byly na pokyn GameDesignera (24. 11. 2026) zrušeny – dávaly útočníkům výškovou výhodu až na úroveň hradeb. Vše je vygenerováno ve skriptech a datech, ověřeno mimo UE (`run_checks.py` bez chyby, 0 kolizí) a **ověřeno v UE GameDesignerem (24. 11. 2026)**.
- **Terén (`01_terrain`, `tools/terrain/gen_moat.py`):** Starý příkop (`t_rel = 37 m`) pod strážní věží je v `Zricenina_heightmap_505_50cm.png` zasypán výškami z `terrain_from_level.json` (pod všemi stávajícími zdmi hradu `ΔZ = 0 cm`). Před vnějším lícem `Brana_V` (`u_in = 8,10 m`) a s bermou před `Hradba_V` (`u_in = 7,00 m`) je vyhlouben šíjový příkop šířky `8,20 m` se dnem šířky `3,80 m` na `Z = 2700 cm` a skalními stěnami `54°–65° > 44°`. Ze severního konce dna (`u = 12,2 m, d = -1,0 m`) vede kontraskarpou severní úniková rampa (`sklon 25,1° < 44°`, šířka `~2,0 m`), zaříznutá bez prahu do rostlého severního svahu (`Z ≈ 2938 cm`). Východně od příkopu zůstává rostlý terén bez valů, s přístupovým úvozem v ose brány (`d = 1,50 .. 4,70 m`, předmostí `Z = 3040 cm`, stoupání `14,9°` k cestě). Mřížka `terrain_from_level.json` je rozšířena na `x1 = 4400` (`nx = 97`).
- **Zřícenina (`03_ruin`, část `Obvod`):** Uprostřed příkopu stojí kamenný pilíř `Brana_Pilir` (`3,0 × 1,4 m`, `151` kamenů) a na hraně kontraskarpy opěra `Brana_Opera` (`3,2 × 1,2 m`, `97` kamenů, `z_offset = -1,2 m`), obě se zarovnanou korunou pod `Z = 3011 cm`. Ve vnějším líci prahu `Brana_V` (`d = 1,85 .. 4,35 m`) je vynechán vnější ozub (`kapsa` s `outer = True`, `Z 3003–3040 cm`) pro uložení čela lávky.
- **Dostavba (`05_constructions`, sada `base`):** `Brana_Most_Kamen` (`stone_fill`, líc + maltové jádro) vyrovnává korunu pilíře a opěry na `Z = 3011 cm` a uklízí volnou suť z předmostí (`u = 16,20 .. 19,20 m, d = 1,40 .. 4,80 m`). Dřevěná lávka `Brana_Most` (`platform`, `finish: "old"`) klade přes obě pole 3 + 3 loupané klády [[SM_RuinLog_A]] Ø `24 cm` přeložené vedle sebe nad pilířem a `31` příčných prken [[SM_RuinPlank_A]] tl. `5 cm` v šířce `2,40 m` s vrchem mostovky `Z = 3040 cm`. Španělský jezdec `Brana_Zataras` (`props`, `pile: True`, úkol `T-0036`) tvoří jeden sloučený actor (`9` dílců: kmen [[SM_RuinLogBark_A]] Ø `18 × 340 cm` + 4 páry kůlů [[SM_RuinStakeSmall_A]] Ø `7 × 160 cm` pod `±45°`) s pivotem dole uprostřed na předmostí v `u = 17,20 m, d = 3,10 m, Z = 3040 cm`.

## Co je hotové
| Část | Krok | Provedení | Sada |
|---|---|---|---|
| Výškopis příkopu, valů a únikové rampy | `01_terrain` | `tools/terrain/gen_moat.py` → `Zricenina_heightmap_505_50cm.png`, `Zricenina_preview_orez.png`, `terrain_from_level.json` (`x1 = 4400`, `nx = 97`); pomocný UE skript `01_terrain/UE_Prikop_Landscape.py` | – |
| Vnější ozub prahu v `Brana_V` | `03_ruin` (`Obvod`) | vnější kapsa (`outer = True`) š. `2,50 m` (`d = 1,85 .. 4,35 m`), `Z 3003–3040 cm` v 9. řadě podstavby `Brana_V`; jádro prahu v průjezdu (`u <= 7,79 m`) zůstává na `Z = 3040 cm` | – |
| `Brana_Pilir` a `Brana_Opera` | `03_ruin` (`Obvod`) | pilíř `3,0 × 1,4 m` v `u = 12,20 m, d = 1,60 .. 4,60 m` (`151` kamenů, pata na dně příkopu `Z 2700 cm`) a opěra `3,2 × 1,2 m` v `u = 16,30 m, d = 1,50 .. 4,70 m` (`97` kamenů, `z_offset = -1,2 m`), obě se zarovnáním koruny `cap` na `Z = 3011 cm` | – |
| `Brana_Most_Kamen` (`stone_fill`) | `05_constructions` | vyrovnání koruny `Brana_Pilir` (`u = 11,65 .. 12,75 m`) a `Brana_Opera` (`u = 15,85 .. 16,75 m`) v šířce `d = 1,80 .. 4,40 m` na `Z = 3011 cm` (lomový kámen + maltové jádro `0,45 m`); `clear_poly` uklízí volnou suť v hrdle úvozu | `base` |
| `Brana_Most` (`platform`) | `05_constructions` | 6 klád [[SM_RuinLog_A]] Ø `24 cm` (`wood_old`): 3 západní (`u = 7,84 .. 12,40 m`, `d = 1,98 / 2,98 / 3,98 m`) a 3 východní (`u = 12,00 .. 16,55 m`, `d = 2,23 / 3,23 / 4,23 m`) + `31` prken [[SM_RuinPlank_A]] tl. `5 cm` (`u = 7,82 .. 16,50 m`, `d = 1,90 .. 4,30 m`), **vrch `Z = 3040 cm`**, bez zábradlí | `base` |
| `Brana_Zataras` (`props`, `pile: True`) | `05_constructions` | španělský jezdec jako **jeden actor** (`Brana_Zataras_Drevo_Base`, pivot `[3676, -3179, 3040]` v `u = 17,20 m, d = 3,10 m`): kmen s kůrou [[SM_RuinLogBark_A]] Ø `18 cm × 3,40 m` (střed `Z 3096,6 cm`) a 4 páry zkřížených kůlů [[SM_RuinStakeSmall_A]] Ø `7 cm × 1,60 m` pod `±45°` v `d = 1,85 / 2,68 / 3,52 / 4,35 m` (`T-0036`); v UE lze posunout/natočit jako celek a uložit přes `Brana_Capture.py` | `base` |

## Souhrn specifikace
- **Sdílené parametry (03 i 05):** `Lapikus/tools/ruin/brana_spec.py` (`B_MOAT_FLOOR_Z`, `B_BRIDGE_BEAM_Z = 3011.0`, `B_BRIDGE_REBATE`, `B_PILIR`, `B_OPERA`, `B_BRIDGE_BEAM`, `B_BRIDGE_DECK`, `B_BRIDGE_FILL`, `B_BRIDGE_CLEAR`, `B_ZATARAS`, `prikop_walls()`, `ruin_edits()`, `most()`).
- **Terén (01):** `Lapikus/tools/terrain/gen_moat.py` (`apply_gate_moat()`, `extend_level_terrain()`); ověření v UE `Lapikus/01_terrain/UE_Prikop_Landscape.py`.
- **Spouštěče v UE (03 a 05):** `03_ruin/blocks/casti/Obvod.py`, `05_constructions/stavby/Brana.py` (souhrnný spouštěč `Brana_Most_Kamen`, `Brana_Most`, `Brana_Zataras`), `Brana_Capture.py` a jednotlivé spouštěče `Brana_Most_Kamen.py`, `Brana_Most.py`, `Brana_Zataras.py`.
- **Kontroly a náhledy mimo UE:** `python Lapikus/tools/checks/run_checks.py --only openings,floating,brana`; 4panelový náhled `Lapikus/05_constructions/Stavby_brana_prikop_nahled.png` a sklonová mapa `Lapikus/01_terrain/Zricenina_preview_orez.png`.

## Co se liší od návrhu (a proč)
Rozhodnutí GameDesignera a konstrukční zpřesnění při stavbě (zapsáno také v [[navrh_brana_prikop]] § *Upřesnění při stavbě*):
1. **Zrušení čelních terénních valů před příkopem (GameDesigner, 24. 11. 2026):** valy před vnější hranou příkopu (jižní `+1,35 m`, severní `+1,05 m`) byly zrušeny, protože dávaly útočníkům taktickou výhodu až na úroveň hradeb. Východně od příkopu zůstává rostlý terén šíje a přístupový úvoz (`d = 1,50 .. 4,70 m`, `Z 3040 → 3250 cm`).
2. **Vnější ozub prahu v `Brana_V` (`u = 7,71 .. 8,10 m`, `Z 3003–3040 cm`):** v 9. řadě podstavby `Brana_V` byl doplněn vnější ozub (`kapsa` s `outer = True`), aby západní konce klád (`u = 7,84 .. 12,40 m`) a prkna lávky (`u = 7,82 .. 16,50 m`) nepronikaly do vnějších lícových kamenů prahu; jádro prahu v průjezdu (`u <= 7,79 m`) navazuje v `Z = 3040 cm` bez schodu.
3. **Souměrné příčné polohy klád `Brana_Most`:** dvojice klád byly vystředěny kolem `d = 3,10 m` na `d = (1,98; 2,98; 3,98)` a `(2,23; 3,23; 4,23)` s roztečí `0,25 m` v páru (vůle `1 cm` při Ø `24 cm` nad pilířem místo překryvu `2 cm`) a východní konce klád ukončeny v `u = 16,55 m` (`0,85 m` na opěře), aby měly vůli `8,4 cm` před špičkami kůlů `Brana_Zataras`.
4. **Zarovnání `cap` přes plnou délku `Brana_Pilir` a `Brana_Opera`:** protože v `zr_ruin/wall.py` se `cap` vyhodnocuje podle středu kamene (délka až `0,90 m`), byl `cap` rozšířen přes celou délku obou zdí a čela pilíře snížena přirozeným rozpadem mimo `protect`; v `zr_stavby/zdivo.py` byla opravena spodní mez `bottom_abs` u zapuštěné opěry (`z_offset = -1,2 m`).
5. **Vyústění severní únikové rampy do rostlého svahu:** na konci únikové rampy (`u ≈ 15,9 .. 16,5 m, d = -4,8 .. -5,5 m`) leží přirozený severní svah na `Z = 2912–2940 cm` (níž než odhadovaných `2990 cm` v návrhu), proto je rampa zaříznuta funkcí `min(z_ramp, H_base)` plynule do rostlého úbočí bez terénního stupně (`max sklon 26,1° << 44°`).

## Ověřeno v UE
### V levelu (report z UE)
Poslední automatický report `Maintenance/reports/ue_Brana.json` je z 2026-11-23 před postavením příkopu, lávky a zátarasu (čeká na příští běh `ue_query`).
### Vizuálně ověřeno (kdo, kdy)
**GameDesigner (Jirka), 2026-11-24:** šíjový příkop bez čelních valů, přístupový úvoz, severní úniková rampa, kamenný pilíř `Brana_Pilir`, opěra `Brana_Opera`, vyrovnání `Brana_Most_Kamen`, dřevěná lávka `Brana_Most` a zátaras `Brana_Zataras` ověřeny v UE Editoru (`/Game/Skvt/LapikusPrototypeMap`).

Mimo UE ověřeno 2026-11-23–24:
- `run_checks.py` (`openings`, `floating`, `ostroh`, `obydli`, `brana`, `vez` – vše OK, 0 průniků mostu i zátarasu se zříceninou a sutí, všech 6 klád podepřeno na obou koncích, mostovka vodorovná `Z = 3040 cm`);
- kontrola invariance všech 17 ostatních zdí hradu oproti předchozímu `ruin_layout.json` (`ΔZ = 0 cm`);
- vizuální kontrola 4panelového náhledu `Lapikus/05_constructions/Stavby_brana_prikop_nahled.png` a sklonové mapy `Lapikus/01_terrain/Zricenina_preview_orez.png`.

## Co zbývá
- Volitelně po další iteraci: doplnit větší zřícené bloky na dně příkopu a upravit první bod splinu `PCG_Path` před přístupovým úvozem (`[[04_forest]]`).

## Odkazy na návrh a předání
- návrh: [[navrh_brana_prikop]]
- předání: [[predani_brana_prikop_stavitel]]
- navazující strážní stanoviště: [[navrh_brana_straz]], [[stav_brana_straz]]
- stav zříceniny: [[Zricenina_03_ruin_stav]]
