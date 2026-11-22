---
# orchestrace
type: handover
validity: archived
updated: 2026-11-23
# hra
domain: structures
entity: "[[Palac_Obydli]]"
build_step: 05_constructions
---
# Dům posádky v paláci (Palac_Obydli) – předání staviteli

> Archivováno 2026-11-23: rozděleno na frontu předání `predani_palac_obydli_1_…` až `_7_…`, know-how do [[predani_builder_knowhow_dum]] (G14c, návrh Knihovníka).

Stav: 21. 11. 2026. Předává architekt (session s Jirkou), přebírá stavitel. Cíl: nejdřív **staveniště a kontrola etapy 1** (kap. 4), potom **finální stav domu** (kap. 5). Pořadí určil Jirka 21. 11. 2026, viz [[navrh_palac_obydli_stred]] kap. 0.4 a 0.7.

Čti spolu s: `AGENT_Stavitel_hrad.md`, `KNOWHOW_hrad.md`, [[navrh_palac_obydli_stred]] (kap. 0 platí přednostně před kap. 3–9), [[05_constructions]].

## 1. Co platí (rozhodnutí Jirky)

Přesunuto do [[navrh_palac_obydli_stred]] kap. 0.7.

## 2. Co je hotové

Přesunuto do [[stav_palac_obydli]].

## 3. Kde co je

| Co | Kde |
|---|---|
| rozměry domu (jediné místo, kde se mění čísla) | `tools/ruin/palac_spec.py`: `D_*`, `obydli()`, `_obydli_pec()`, `_obydli_drevo()` |
| data staveb | `tools/constructions/gen_constructions.py` → `palac()` → `05_constructions/constructions.json` (jen generátorem) |
| registr typů | `05_constructions/build_constructions.py` → `TYPES`, `REQUIRED`, `CNAME` |
| spouštěče | `05_constructions/stavby/Palac_Obydli.py` (seznam `STAVBY`), `Palac_Obydli_<Část>.py` |
| kontroly | `tools/checks/run_checks.py --only obydli` → `check_obydli` |
| náhled | `tools/checks/preview3d.py obydli <out.png> [--stage 1\|2]` → `obydli_scene` |

Rám paláce: `s` podél `Palac_J` k věži, `n` k severu, výšky v metrech nad terénem v `ref` (střed domu). Vnitřní líc `Palac_J` je n = 0,7, nové zdivo začíná v n = 0,72.

Postup po změně čísel: `gen_constructions.py` (argumenty: `03_ruin/ruin_layout_draft.json`, výstup, `03_ruin/blocks/ruin_layout.json`) → `run_checks.py` → náhled. Před přepsáním `constructions.json` vygeneruj do dočasného souboru a porovnej, že se změnily jen očekávané stavby (sdílené soubory může měnit i jiná session).

## 4. Staveniště a etapa 1 (teď)

**Stav 21. 11. 2026:** postaveno ve skriptech, kontroly etapy 1 procházejí, náhled je hotový. Zbývá **vizuální kontrola v UE** (Jirka, kap. 7). Výsledek a odchylky od specifikace: [[navrh_palac_obydli_stred]] kap. 9.2a, stav: [[stav_palac_obydli]].

- ✅ Uhlí pod plotnou (box `U`) je v sadě `final` (příznak `top`, typ `hearth` beze změny, data kovárny beze změny).
- ✅ `Palac_Obydli_Stavenisko` (typ `props`, sada `site`): vzpěry V1–V4, žebřík; hranice S3, S4 a S5 jako samostatné stavby `_Kulatina`, `_Tramy`, `_Prkna`, každá jako jeden actor (Jirka 21. 11. 2026: rozmístí je podle game designu, uložení polohy a natočení `Palac_Obydli_Stavenisko_Capture.py`, `pile` v `build_constructions.py`; uložení polohy v UE zatím neověřené). Prkna jsou v jedné hranici o 0,5 m vyšší (75 kusů), původní dvě hranice zůstávají jako varianta v `D_SITE`. Jirka prkna přemístil a uložil (capture, 21. 11. 2026). Přibyly kozy s rozpracovanou kulatinou `_Kozy` (S6, nový mesh `SM_RuinLogPeeling`), návrh kap. 9.2a. Data: `palac_spec.py` → `D_SITE`, `obydli_stavenisko()`, generátor `palac()`, spouštěč `stavby/Palac_Obydli_Stavenisko.py`, v `STAVBY` za `Palac_Obydli_Srub`, tedy až po pecí.
- ✅ Počty z dat sady `final`: krokve 6, pozednice 1, vaznice 1, srub síně 10 + 2 pultramy; prkna 75 (aspoň 44 = jedna řada krytiny).
- ✅ Ověřeno: `props` umí hranoly a prkna. Terén pod hranicemi je rovný (rozdíl 0 cm).
- ✅ Kontroly kap. 9.4 v `check_obydli`: nic nevisí, 2 vzpěry na líci sloupů 11,1 a 13,0, trasy a volné pásy, kolize se zříceninou, `base`, kovárnou, vybavením i mezi sebou, terén, počty a délky, v etapě 2 nic ze `site`. Zkoušeno i na záměrně pokažených datech: kontroly chybu chytí.
- ✅ `run_checks.py --only obydli` OK. `--only palac` hlásí 4 chyby vybavení kovárny (06, polohy z levelu), které tam byly už před tímto krokem. Výstup je beze změny.
- ✅ Náhled `05_constructions/Stavby_palac_obydli_nahled_etapa1.png` (přidané pohledy na vzpěry a hranice).
- ☐ **Vizuální kontrola v UE** podle kap. 9.4 návrhu a kap. 7 tady. Vzhled schválil Jirka 21. 11. 2026, zbývá ověřit rozdělení na objekty.
- ☐ **Rozmístění hranic** podle game designu (Jirka v UE), pak `Palac_Obydli_Stavenisko_Capture.py`, nový build a znovu `run_checks.py --only obydli` (kontroly berou polohy z levelu). Ověřit, že hranice po buildu zůstane, kde byla.
- **Zamčená `base`:** od teď neměň hodnoty vyjmenované v návrhu kap. 0.7. Když to bude nutné, napiš Jirkovi a znovu projdi kontroly kap. 9.4.

## 5. Co zbývá do finálního stavu (po staveništi, v tomto pořadí)

### 5.1 Krytina a lemování (`Palac_Obydli_Krov`)

- Skladba jako u kovárny (`pult._pult_cover`): latě, prkna po spádu, lišty přes spáry. Podle návrhu kap. 4.1 prkna ve dvou délkách (3,4 + 3,2 m) s přesahem 0,25 m nad latí; plocha s = 9,8–21,7, přesah 0,3 m za štíty.
- **Pozor na osy:** `_pult_cover` čte `plan["a"]` jako osu spádu. U kovárny je to osa `u`, u domu je spád po ose `v` (`axis = "v"`). Ověř na datech domu, případně sjednoť význam `plan`.
- **Latě už v kostře:** `pre_laths` (2 řady nad světnicí, sada `base`). Krytina je nesmí zdvojit ani měnit: v těchto řadách polož jen západní část latí (sada `final`). `pre_laths` zůstávají beze změny, patří k zamčené `base` (návrh kap. 0.7).
- **Počet prken po spádu** porovnej s hranicemi prken S5 na staveništi (2 × 44, návrh kap. 9.2). Když se liší, uprav S5.
- **Prostup komína:** `openings` = komín s = 16,76; n = 1,7; strana 0,5 m. Výměny mezi krokvemi: kód výměn v `ohniste.py` předpokládá spád po ose `u` (hledá krokve podle `c`), pro dům nic nepostaví. Buď ho zobecni, nebo výměny postav v krovu.
- **Lemování** jen podél `Palac_J` (horní okraj), prkno na stojato. Koruna `Palac_J` je nad krytinou všude (nejníž 4,43 m, krytina u zdi asi 4,3 m), dozdívka odpadla.
- Sady: krytina celá `final`.
- Štít nad příčkou končí rovně pod vrchem krokví; po krytině zkontroluj stupňovitou mezeru (do 7 cm) a případně ji zakryj lištou.

### 5.2 Strop světnice (`Palac_Obydli_Strop`, nový typ nebo rozšíření `tower_floor`)

- Světnice je teď s = 14,97–20,6 (ne 15,9–20,6 jako v návrhu kap. 4.5). Trámky 14 × 18 cm východ–západ, spodek 2,3 m, prkna 4 cm. Uložení: srub příčky a východní stěny (vrch srubu 2,5 m).
- **Otvor pro dymník a komín:** dymník je 1,6 × 1,1 m (s = 15,96–17,56; n = 1,15–2,25), spodní okraj 1,8 m, vrch 2,6 m. Otvor asi 1,7 × 1,2 m, přerušené trámky do výměny.
- **Zavěšení dymníku:** teď visí ve vzduchu. Zavěs ho na výměnu stropu (závěsné tyče jako u kovárny, `hangers`).
- Střední sloup krovu (s = 15,3; n = 0,85) a sloupy 18,0 a 20,4 stojí ve světnici u jižní zdi: strop je musí obejít.
- Přístup na půdu: otvor ve štítu příčky a žebřík ze síně (kulisa).
- Sada `final`.

### 5.3 Podlaha světnice (`Palac_Obydli_Podlaha`, `plank_floor`)

- Obrys = vnitřek světnice mimo sokl pece (s = 15,96–17,56; n = 0,72–2,32) a patní kameny sloupů (`avoid`). Síň má udusanou hlínu (nestaví se).
- Práh dveří v příčce: podezdívka je ve dveřích přerušená, podlaha končí u příčky.
- Sada `final`.

### 5.4 Okap (`Palac_Obydli_Okap`, `gutter`)

- Žlab pod severní okapovou hranou (n ≈ 6,85), **spád k západu**, rozsochy u stěny, **sud pod západním koncem** (samostatný actor). Svod se nedělá.
- Typ `gutter` počítá spád k `+c`; pro spád k západu (−s) ověř směr na datech domu. Výšku bere z krytiny, proto až po 4.1.
- Rozsochy nesmí stát ve vchodu (s = 13,4–14,4) a zápraží musí zůstat průchozí (aspoň 2,0 m, k průchodu ke kovárně 1,2 m).
- Sada `final`.

### 5.5 Vybavení (`Palac_Obydli_Vybaveni`, `props`)

- Meshe jsou hotové: `SM_RuinDoor`, `SM_RuinShutter`, `SM_RuinBed`, `SM_RuinBedFolded`, `SM_RuinTable`, `SM_RuinChest`, `SM_RuinShelf`, `SM_RuinLadder`.
- **Otvory na míru:** vchod 1,0 × 2,28 m, dveře v příčce 1,0 × 2,17 m, okénko světnice 0,6 × 0,66 m (parapet 1,4 m), okénko síně 0,5 × 0,44 m. Dveře a okenice otevřené. Chybí **zárubně** (konce kulatin v otvorech jsou volné): svislé fošny po stranách otvorů. Zárubně jsou sada `final` (v etapě 1 jsou otvory bez nich, návrh kap. 9.1).
- Světnice podle návrhu kap. 4.8: tři lůžka, stůl u okénka, dvě truhly. Místo u jižní zdi mezi pecí a východní stěnou je volné (výklenek střílny s = 19 jako police). Síň: hranice dřeva, ponk u střílny s = 14, police.
- Okénko síně zůstává v s = 11,8–12,3, kde je postavené (návrh kap. 0.6).
- Všechno samostatné actory, sada `final`.

## 6. Na co si dát pozor

- **Nikdy nepřepisuj** `manual_edits.json` ani `constructions_edits.json`. `ruin_layout.json` a `constructions.json` jen generátory.
- **Složky:** nové soubory jen do `skvt_projekt\PrototypeDesigns\Lapikus`. V `GameDesign\Claude outputs\Lapikus` jen přepisuj existující kopie stejným obsahem (návrhy tam leží v kořeni). Tamní kopie proto nemá `srub.py`, nové spouštěče, `Etapa.py` ani nové OBJ a dům z ní nepostavíš.
- **Mazání** jen na výslovný pokyn; dočasné soubory patří do `_to_delete/`.
- **Sdílené soubory** (`pult.py`, `ohniste.py`, `build_constructions.py`, `gen_constructions.py`, `palac_spec.py`, `config.py`) používá i kovárna. Nové klíče přidávej tak, aby se data kovárny nezměnila, a ověř `run_checks.py --only palac`.
- **Náhled** kreslí všechno jako hranoly (kulatina, klenba, dymník) a potřebuje `node`, `three` a `playwright`. Kde nejsou, vyexportuj kvádry (`obydli_scene`) a vykresli jinde.
- **„O řadu níž“ a podobná zadání** mají víc významů (KNOWHOW): zeptej se dřív, než začneš.
- Před stavbou dřeva vždy porovnej polohy sloupů, krokví, komína a podezdívek mezi sebou. Návrh měl sloup v ose příčky a komín v krokvi.

## 7. Co spustit v UE (pořadí)

1. `03_ruin/blocks/casti/Palac.py` (jen pokud od přesunu portálu a průchodu ke kovárně neběžel).
2. `05_constructions/stavby/Palac_Obydli.py` (kámen, krov, pec, srub, staveniště, suť; všechny sady). `Palac_Obydli_Stavenisko` je v `STAVBY` (za srubem).
3. `05_constructions/stavby/Etapa.py` s `ETAPA = 1`: kontrola staveniště. Pak `ETAPA = 2`: staveniště zmizí, dům je beze změny.
4. Po posunu nebo natočení hranic v UE: `05_constructions/stavby/Palac_Obydli_Stavenisko_Capture.py` (uloží polohu hranic do `constructions_edits.json`). Bez toho je další build vrátí.

Na co se v UE podívat: vzpěry na líci sloupů 11,1 a 13,0, žebřík mezi krokvemi 18,273 a 19,282, hranice na nádvoří (na terénu, mimo průlom, portál a dveře s = 27), v etapě 1 bez uhlí pod plotnou.

## 8. Dokumentace, kterou drž aktuální

- [[navrh_palac_obydli_stred]] kap. 0 (stav po krocích, odchylky) a kap. 9 (staveniště, kontroly etapy 1),
- [[Zricenina_03_ruin_stav]] (i v projektu SKVT jako [[Zricenina_03_ruin_stav]]),
- [[05_constructions]] (typy a klíče dat),
- [[CHECKLIST_assets_navrhy]] (kap. 8 a tabulka typů),
- `KNOWHOW_hrad.md` (poučení),
- tento soubor: po každém dokončeném kroku přepiš kap. 4 a 5; stav zapiš do [[stav_palac_obydli]].

## Zbývá
- kap. 4: vizuální kontrola staveniště a etapy 1 v UE (teď, Jirka),
- kap. 5: finální stav domu (krytina, strop, podlaha, okap, vybavení).

## Otevřené otázky
- [x] Okénko síně (s = 11,8–12,3) není uprostřed stěny vlevo od dveří (střed 12,15). Posunout? → zapracováno do [[navrh_palac_obydli_stred]] kap. 0.6 (zůstává, Jirka 21. 11. 2026)
