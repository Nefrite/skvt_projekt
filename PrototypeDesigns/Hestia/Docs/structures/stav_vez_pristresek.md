---
# orchestrace
type: state
validity: valid
updated: 2026-11-22
aliases: []
# hra
domain: structures
entity: "[[Vez_Pristresek]]"
depth: 3
build_step: 05_constructions
assets: []
---
# Vez_Pristresek – stav stavby

## Souhrn
Plátěný přístřešek hlídky ve 2. patře věže a škody z dobývání na koruně věže jsou postavené ve skriptech (17. 11. 2026) a ověřené mimo UE; v UE neověřeno. Návrh přístřešku [[navrh_vez_pristresek]], návrh škod [[navrh_vez_skody]].

## Co je hotové
- **Škody z dobývání (17. 11. 2026, [[navrh_vez_skody]]):** hrad se dobýval od východu a jihovýchodu. Data v `tools/ruin/tower_spec.py` → `ruin_edits()`, `gen_layout.py` je jen převezme. Neověřeno v UE.
  - `Vez_V`: hlavní průlom, nejnižší koruna 9,45 m (místy 9,1 m), střílna 2. patra zanikla (zůstal výřez s parapetem 0,7–1,05 m), kapsy trámů 2. patra zůstávají; 2 141 → 1 918 kamenů;
  - `Vez_J`: průlom do tvaru nepravidelné mísy, koruna u vnitřního líce v u = 1,25–7,4 nejvýš 10,85 m (okap přístřešku), nadpraží střílny 2. patra stojí; 2 138 → 2 033 kamenů;
  - JV roh 11,2–11,9 m, SV roh 11,2–11,55 m (z obou zdí);
  - `Vez_Z`: jen vedlejší škody, střed zdi vyšší (`protect` v = 1,5–4,0 m, vnitřní líc 10,85–11,9 m); 2 050 → 2 087 kamenů;
  - `Vez_S`: místo průlomu do tvaru U plynulý pokles koruny od SZ rohu (12,2–12,6 m) k SV rohu (11,2 m), střílna 2. patra má zase nadpraží; 1 913 → 2 018 kamenů;
  - `Vez_Patra` beze změny (222 dílců, bez průniku se zříceninou).
- **Přístřešek hlídky na věži (17. 11. 2026, typ `canvas_shelter`, `zr_stavby/pristresek.py`):** 05 `Vez_Pristresek` ve 2. patře věže podle [[navrh_vez_pristresek]] kap. 4–5, celé sada `base`. Rozměry `tools/ruin/tower_spec.py` → `PR`, `pristresek()`; data `gen_constructions.py` → `vez_pristresek`.
  - 3 kůly s kůrou Ø 16 cm na prknech nad trámem v = 4,678 (u = 1,40 / 5,50 / 7,15), hlava rozsochy `SM_RuinForkHead` zvětšená na kůl (× 1,33); hřeben Ø 14 cm ze dvou kusů (vrch 12,70 m) ve vidlicích;
  - okapová tyč Ø 12 cm (spodek 11,05 m) na 5 podkladních kamenech na koruně `Vez_J` (výška se počítá z postavené koruny, nad 0,35 m dva kameny: vyšly 0,19 / 0,53 / 0,20 / 0,20 / 0,54 m);
  - 5 krokvových tyčí Ø 10 cm, sklon 22,6°, 2 vzpěry do podlahy nad trámem v = 6,317; ovázání spojů (`SM_RuinLashing`);
  - plachta 6,0 × 4,3 m a štít nad `Vez_Z` jako meshe na míru (`SM_RuinCanvasVez_A`, `SM_RuinCanvasVezGable_A`, generuje `tools/meshes/gen_meshes.py textile` z `tower_spec`); plátno leží **2 cm** nad krokvemi (návrh 0,5 cm), aby přešlo přes ovázání;
  - 2 bouřková lana (`SM_RuinRope`) přes plachtu ke kotevním kamenům na koruně `Vez_J`, 4 zátěžové kameny na lemu; podkladní, zátěžové a kotevní kameny jsou samostatné actory (doladit ručně, capture);
  - spuštění `05_constructions/stavby/Vez_Pristresek.py`, celá věž `stavby/Vez.py` (`Vez_Patra` + přístřešek, `RUIN = True` i část `Obvod`). Ověřeno jen mimo UE (`run_checks.py --only vez`, náhled `05_constructions/Stavby_vez_pristresek_nahled.png`).

### Připravenost assetů (před stavbou, z návrhu)
**Připravenost** (podrobně [[CHECKLIST_assets_navrhy]]):
- **Hotové dílce:** kulatina a tyče s kůrou `SM_RuinLogBark`, `SM_RuinPoleBark`, hlava rozsochy `SM_RuinForkHead`, lano `SM_RuinRope`, ovázání `SM_RuinLashing`, kameny zříceniny. Materiály `MI_RuinBark`, `MI_RuinRope`, oboustranné plátno `MI_RuinCanvas` (vítr připravený parametrem `WindAmount`, výchozí 0).
- **Plátno a štít:** generátor prověšené plochy je hotový (`tools/meshes/mesh_textile.make_canvas` + `write_canvas`), napojení na stavbu chybí.
- **Chybí:** typ stavby `canvas_shelter`, sekce přístřešku v `tools/ruin/tower_spec.py`, úpravy 03 (kap. 3), sekce `vez` v `run_checks.py`.

## Souhrn specifikace
Stav: **postaveno 17. 11. 2026, neověřeno v UE.** Úpravy 03 ([[navrh_vez_skody]]) v `tower_spec.ruin_edits()`, přístřešek 05 `Vez_Pristresek` (typ `canvas_shelter`, `tower_spec.pristresek()`), kontroly `run_checks.py --only vez`, náhled `05_constructions/Stavby_vez_pristresek_nahled.png`.

## Co se liší od návrhu (a proč)
Odchylky od kap. 4: plátno 2 cm nad krokvemi (ne 0,5 cm, přes ovázání), podkladní kámen v u = 7,20 je dvojitý (0,54 m; koruna pod ním je 10,49 m, kámen 10,84 m sahá pod podklad jen rohem).

## Ověřeno v UE
### V levelu (report z UE)
Neověřeno.
### Vizuálně ověřeno (kdo, kdy)
Neověřeno. Mimo UE:

**Ověřeno 17. 11. 2026 mimo UE na kopii projektu** (data se stejným md5 jako v projektu, terén z levelu `terrain_from_level.json`, `manual_edits.json` prázdný):
- úpravy z kap. 3 zapsané do kopie `gen_layout.py`, z ní vygenerovaný `ruin_layout.json`;
- přístřešek jako kvádry proti kamenům zříceniny a dílcům `Vez_Patra`;
- kontroly `run_checks.py --only openings,floating`: otvorů 104, kolizí 0, kamenů bez podpory 3 (známé).

Soubory projektu se při ověřování neměnily.

## Co zbývá
Ověření v UE; podkladní, zátěžové a kotevní kameny doladit ručně a uložit přes capture.

## Odkazy na návrh a předání
- návrh přístřešku: [[navrh_vez_pristresek]] (kap. 4–5)
- návrh škod: [[navrh_vez_skody]]
- stav zříceniny: [[Zricenina_03_ruin_stav]] (kap. *Věž*)
