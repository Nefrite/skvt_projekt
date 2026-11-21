---
# orchestrace
type: handover
validity: valid
updated: 2026-11-21
# hra
domain: structures
entity: "[[Palac_Obydli]]"
build_step: 05_constructions
---
# Dům posádky v paláci (Palac_Obydli) – předání staviteli

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

- **Zadání:** nová stavba `Palac_Obydli_Stavenisko`, typ `props`, celá v sadě `site`. Specifikace je v [[navrh_palac_obydli_stred]] kap. 9.2. Obsah:
  - vzpěry V1–V4,
  - žebřík,
  - hranice kulatiny na srub síně (S3),
  - hranice krokví, pozednice a vaznice (S4),
  - dvě hranice prken na krytinu (S5, doporučená varianta A).
- **Nejdřív jediná změna `base`:** vrstva uhlí pod plotnou (box `U` v `_obydli_pec`, z = 0,64–0,67) přejde do sady `final`. Tmavý vnitřek pece (box `V`) zůstává `base`. Když typ `hearth` neumí sadu u jednotlivého boxu, doplň mu klíč `stage` tak, aby se data kovárny nezměnila (`run_checks.py --only palac`).
- **Zamčená `base`:** potom během tohohle kroku ani po něm neměň hodnoty vyjmenované v návrhu kap. 0.7. Když to bude nutné, napiš Jirkovi a znovu projdi kontroly kap. 9.4.
- **Počty kusů v hranicích S3 a S4 počítej z dat sady `final`** (krokve, západní kusy pozednice a vaznice, segmenty srubu síně), ne ručně. Prkna S5: 2 × 44 podle vzorce v kap. 9.2.
- **Ověř před stavbou:**
  - že `vybaveni.build_props` položí hranoly a prkna (`SM_RuinTimber`, `SM_RuinPlank`) a hranici jako jeden celek (předpoklad návrhu 9.5; když ne, doplň shape a napiš to do 9.2),
  - terén nádvoří pod hranicemi (rozdíl ≤ 0,15 m).
- **Kontroly** podle kap. 9.4 doplň do `check_obydli` (sestava `base` + `site`): nic nevisí, vzpěry u sloupů 11,1 a 13,0, trasy a volné pásy 1,2 m, kolize, počty, v etapě 2 nic ze `site`.
- **Hotovo, když:**
  - `run_checks.py --only obydli` i `--only palac` hlásí OK,
  - náhled `preview3d.py obydli <out.png> --stage 1` je hotový,
  - Jirka potvrdí vizuální kontrolu v UE podle kap. 9.4,
  - stav je zapsaný v [[stav_palac_obydli]] a odchylky od kap. 9.2 v návrhu.
- **Vyřešené body ze starší verze předání:** rozdělení sad po posunu příčky (zůstává podle dat) a pec v etapě 1 (klenba `base`, uhlí pod plotnou `final`) jsou v návrhu kap. 0.7. Kde v etapě 1 spí posádka, je samostatný task mimo staveniště (Jirka 21. 11. 2026).

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
2. `05_constructions/stavby/Palac_Obydli.py` (kámen, krov, pec, srub, staveniště, suť; všechny sady). `Palac_Obydli_Stavenisko` přidej do `STAVBY` za `Palac_Obydli_Ohniste`.
3. `05_constructions/stavby/Etapa.py` s `ETAPA = 1`: kontrola staveniště. Pak `ETAPA = 2`: staveniště zmizí, dům je beze změny.

Na co se v UE podívat: vzpěry na líci sloupů 11,1 a 13,0, žebřík mezi krokvemi 18,273 a 19,282, hranice na nádvoří (na terénu, mimo průlom, portál a dveře s = 27), v etapě 1 bez uhlí pod plotnou.

## 8. Dokumentace, kterou drž aktuální

- [[navrh_palac_obydli_stred]] kap. 0 (stav po krocích, odchylky) a kap. 9 (staveniště, kontroly etapy 1),
- [[Zricenina_03_ruin_stav]] (i v projektu SKVT jako [[Zricenina_03_ruin_stav]]),
- [[05_constructions]] (typy a klíče dat),
- [[CHECKLIST_assets_navrhy]] (kap. 8 a tabulka typů),
- `KNOWHOW_hrad.md` (poučení),
- tento soubor: po každém dokončeném kroku přepiš kap. 4 a 5; stav zapiš do [[stav_palac_obydli]].

## Zbývá
- kap. 4: staveniště a kontroly etapy 1 (teď),
- kap. 5: finální stav domu (krytina, strop, podlaha, okap, vybavení).

## Otevřené otázky
- [x] Okénko síně (s = 11,8–12,3) není uprostřed stěny vlevo od dveří (střed 12,15). Posunout? → zapracováno do [[navrh_palac_obydli_stred]] kap. 0.6 (zůstává, Jirka 21. 11. 2026)
