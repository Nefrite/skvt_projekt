---
# orchestrace
type: handover
validity: valid
updated: 2026-11-16
# hra
domain: structures
entity: "[[Palac_Obydli]]"
build_step: 05_constructions
---
# Dům posádky v paláci (Palac_Obydli) – předání staviteli

Stav: 16. 11. 2026. Předává architekt (session s Jirkou), přebírá stavitel. Cíl: dodělat **finální stav domu** (etapa 2) a potom **staveniště** (etapa 1).

Čti spolu s: `AGENT_Stavitel_hrad.md`, `KNOWHOW_hrad.md`, [[navrh_palac_obydli_stred]] (kap. 0 platí přednostně před kap. 3–9), [[05_constructions]].

## 1. Co platí (rozhodnutí Jirky)

- **Etapy jsou tři sady actorů** s tagy `stage:base` / `stage:final` / `stage:site`. Dům se počítá jednou jako hotový, etapa 1 je jen filtr (`base` + `site`), etapa 2 = `base` + `final`. Co stojí v etapě 1, se v etapě 2 neskrývá.
- **Ladí se nejdřív finální stav.** Staveniště a kontrola etapy 1 až nakonec.
- **Dřevo je surové (`raw`) v obou etapách**, i krov a krytina. Dehtování je případný pozdější třetí stav.
- **Zabydlení je dlouhodobé a má být pohodlné.** Styl: dobové provizorium, železo z vlastní kovárny na míru.
- **Větší světnice:** příčka je v s = 14,85, západně od středního sloupu krovu (s = 15,3). Vchod s = 13,4–14,4, okénko světnice s = 17,5–18,1.
- **Pec s nístějí** místo otevřeného ohniště, osa s = 16,76 (uprostřed mezi krokvemi), kouř sopouchem do dymníku.
- **Okap:** spád k západu (od kovárny), sud pod západním koncem, svod se nedělá.
- **Dveře a okenice** jsou v etapě 2 otevřené (kulisa). **Žebříky** nejsou pro postavu použitelné. **Sklep** se neřeší.
- Hráč domem jen prochází, etapy mají dát dojem času.

## 2. Co je hotové

Všechno je ve skriptech a prošlo `tools/checks/run_checks.py` (`SOUHRN: ... obydli OK`). **V UE je potvrzené jen navázání kamene podezdívek** (Jirka 16. 11. 2026). Krov, srub, pec, posun příčky a nové meshe v UE zatím neběžely.

| Stavba | Typ, modul | Obsah | Sady |
|---|---|---|---|
| 03 část `Palac` | `gen_layout.py`, `palac_spec.ruin_edits` | portál přesunutý do západní místnosti (`Palac_S` s = 4,5), hrubý průchod v `Palac_S` s = 16, průchod v `Palac_pricka_2` n = 6,9–8,5 ke kovárně | – |
| `Palac_Obydli_Kamen` | `stone_fill`, `zr_stavby/zdivo.py` | obě příčky srovnané na 1,4 m, podezdívky severní stěny a příčky, maltové jádro v ose | `base` |
| `Palac_Obydli_Krov` | `pult_roof`, `zr_stavby/pult.py` | 5 sloupů na patních kamenech, horní pozednice a střední vaznice ze dvou kusů, 3 špalky pod vaznicí, 12 krokví, 2 řady latí nad světnicí. **Bez krytiny.** | `base` / `final` |
| `Palac_Obydli_Ohniste` | `hearth`, `zr_stavby/ohniste.py` | pec s nístějí: sokl, zdi pece, klenba (`SM_RuinOvenDome`), zídky plotny; sopouch, dymník, komín, pás nad ústím, plotna a poklop | kámen a klenba `base`, ostatní `final` |
| `Palac_Obydli_Srub` | `log_wall`, `zr_stavby/srub.py` | severní stěna, příčka, srub na obou bočních stěnách, prkenné štíty, otvory zarovnané na řady | `base` / `final` |

- **Samostatné actory** (ruční doladění, `MODE = "capture"` ve spouštěči stavby): patní kameny sloupů, plotna (`Palac_Obydli_Ohniste|I2`), poklop ústí (`Palac_Obydli_Ohniste|Poklop`, mesh `SM_RuinOvenDoor`: plech s dřevěnou rukojetí, opřený o čelo pece západně od ústí).
- **Nové meshe** (naimportují se při buildu samy): `meshes/wattle/SM_RuinOvenDome_A/B.obj`, `meshes/props/SM_RuinOvenDoor_A.obj`.
- **Přepnutí etapy v editoru:** `05_constructions/stavby/Etapa.py` (`ETAPA` 1 / 2 / 0). Po každém buildu pustit znovu.
- **Náhledy:** `05_constructions/Stavby_palac_obydli_nahled.png` (etapa 2), `Stavby_palac_obydli_nahled_etapa1.png` (etapa 1, ještě před posunem příčky a pecí).

Přesné rozměry a odchylky od původního návrhu: návrh kap. 0.5 (kámen), 0.5a (větší světnice), 0.5b (pec), 0.6 (krov a srub).

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

## 4. Co zbývá do finálního stavu (v tomto pořadí)

### 4.1 Krytina a lemování (`Palac_Obydli_Krov`)

- Skladba jako u kovárny (`pult._pult_cover`): latě, prkna po spádu, lišty přes spáry. Podle návrhu kap. 4.1 prkna ve dvou délkách (3,4 + 3,2 m) s přesahem 0,25 m nad latí; plocha s = 9,8–21,7, přesah 0,3 m za štíty.
- **Pozor na osy:** `_pult_cover` čte `plan["a"]` jako osu spádu. U kovárny je to osa `u`, u domu je spád po ose `v` (`axis = "v"`). Ověř na datech domu, případně sjednoť význam `plan`.
- **Latě už v kostře:** `pre_laths` (2 řady nad světnicí, sada `base`). Krytina je nesmí zdvojit: v těchto řadách polož jen západní část latě (sada `final`), nebo `pre_laths` do krytiny započítej.
- **Prostup komína:** `openings` = komín s = 16,76; n = 1,7; strana 0,5 m. Výměny mezi krokvemi: kód výměn v `ohniste.py` předpokládá spád po ose `u` (hledá krokve podle `c`), pro dům nic nepostaví. Buď ho zobecni, nebo výměny postav v krovu.
- **Lemování** jen podél `Palac_J` (horní okraj), prkno na stojato. Koruna `Palac_J` je nad krytinou všude (nejníž 4,43 m, krytina u zdi asi 4,3 m), dozdívka odpadla.
- Sady: krytina celá `final`.
- Štít nad příčkou končí rovně pod vrchem krokví; po krytině zkontroluj stupňovitou mezeru (do 7 cm) a případně ji zakryj lištou.

### 4.2 Strop světnice (`Palac_Obydli_Strop`, nový typ nebo rozšíření `tower_floor`)

- Světnice je teď s = 14,97–20,6 (ne 15,9–20,6 jako v kap. 4.5). Trámky 14 × 18 cm východ–západ, spodek 2,3 m, prkna 4 cm. Uložení: srub příčky a východní stěny (vrch srubu 2,5 m).
- **Otvor pro dymník a komín:** dymník je 1,6 × 1,1 m (s = 15,96–17,56; n = 1,15–2,25), spodní okraj 1,8 m, vrch 2,6 m. Otvor asi 1,7 × 1,2 m, přerušené trámky do výměny.
- **Zavěšení dymníku:** teď visí ve vzduchu. Zavěs ho na výměnu stropu (závěsné tyče jako u kovárny, `hangers`).
- Střední sloup krovu (s = 15,3; n = 0,85) a sloupy 18,0 a 20,4 stojí ve světnici u jižní zdi: strop je musí obejít.
- Přístup na půdu: otvor ve štítu příčky a žebřík ze síně (kulisa).
- Sada `final`.

### 4.3 Podlaha světnice (`Palac_Obydli_Podlaha`, `plank_floor`)

- Obrys = vnitřek světnice mimo sokl pece (s = 15,96–17,56; n = 0,72–2,32) a patní kameny sloupů (`avoid`). Síň má udusanou hlínu (nestaví se).
- Práh dveří v příčce: podezdívka je ve dveřích přerušená, podlaha končí u příčky.
- Sada `final`.

### 4.4 Okap (`Palac_Obydli_Okap`, `gutter`)

- Žlab pod severní okapovou hranou (n ≈ 6,85), **spád k západu**, rozsochy u stěny, **sud pod západním koncem** (samostatný actor). Svod se nedělá.
- Typ `gutter` počítá spád k `+c`; pro spád k západu (−s) ověř směr na datech domu. Výšku bere z krytiny, proto až po 4.1.
- Rozsochy nesmí stát ve vchodu (s = 13,4–14,4) a zápraží musí zůstat průchozí (aspoň 2,0 m, k průchodu ke kovárně 1,2 m).
- Sada `final`.

### 4.5 Vybavení (`Palac_Obydli_Vybaveni`, `props`)

- Meshe jsou hotové: `SM_RuinDoor`, `SM_RuinShutter`, `SM_RuinBed`, `SM_RuinBedFolded`, `SM_RuinTable`, `SM_RuinChest`, `SM_RuinShelf`, `SM_RuinLadder`.
- **Otvory na míru:** vchod 1,0 × 2,28 m, dveře v příčce 1,0 × 2,17 m, okénko světnice 0,6 × 0,66 m (parapet 1,4 m), okénko síně 0,5 × 0,44 m. Dveře a okenice otevřené. Chybí **zárubně** (konce kulatin v otvorech jsou volné): svislé fošny po stranách otvorů.
- Světnice podle kap. 4.8: tři lůžka, stůl u okénka, dvě truhly. Místo u jižní zdi mezi pecí a východní stěnou je volné (výklenek střílny s = 19 jako police). Síň: hranice dřeva, ponk u střílny s = 14, police.
- Okénko síně (s = 11,8–12,3) není přesně uprostřed stěny vlevo od dveří (střed 12,15). Jirka o posunu nerozhodl, zeptej se.
- Všechno samostatné actory, sada `final`.

## 5. Staveniště a etapa 1 (až po finálním stavu)

- Nová stavba `Palac_Obydli_Stavenisko`, všechno sada `site`, samostatné actory. Obsah: návrh kap. 0.3 a 9.2 (dočasné vzpěry západních sloupů, žebřík, kozy s kulatinou, západní kus pozednice na zemi, hromady kamene, hlíny, kulatiny, krokví a prken, nářadí, třísky).
- **Rozdělení sad po posunu příčky není doladěné:**
  - krokve jsou `base` od s ≥ 16 (`D_STAGE_S`); krokev s = 15,25 je teď nad světnicí, ale je `final`,
  - východní kus pozednice začíná u sloupu 15,3, východní kus vaznice u příčky 14,85,
  - latě zavětrování jsou v s = 16,17–21,4,
  - srub síně má v etapě 1 spodní 3 řady (`D_LOG["west_base_rows"]`).
  Rozhodni s Jirkou, jestli má být hranice na příčce, a srovnej to.
- **Pec v etapě 1:** teď je `base` sokl, zdi pece i klenba. Původní přání bylo mít kamennou část hotovou a chybět má odvod kouře. Klenba je hliněná; zeptej se, jestli má být `base`, nebo `final`.
- **Kontroly etapy 1** (návrh kap. 9.4): každá osazená krokev na třech podporách své sady (už se kontroluje), nic nevisí ve vzduchu, sloupy bez pozednice mají vzpěry, trasa nádvoří → vchod → dveře do světnice a zápraží → kovárna volná v šířce 1,2 m.
- Otázky z kap. 9.5 jsou zodpovězené (žebřík jen kulisa, přepnutí sadami). Kde v etapě 1 spí posádka, návrh neřeší.

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
2. `05_constructions/stavby/Palac_Obydli.py` (kámen, krov, pec, srub, suť; všechny sady).
3. `05_constructions/stavby/Etapa.py` s `ETAPA = 2`.

Na co se v UE podívat jako první: nároží srubu a průchod příčky severní stěnou, osedlání krokví na vrchním trámu, klenba pece na zdech a čelo s ústím, poklop a plotna (samostatné actory), štěrbina 23 cm mezi středním sloupem a příčkou.

## 8. Dokumentace, kterou drž aktuální

- [[navrh_palac_obydli_stred]] kap. 0 (stav po krocích, odchylky),
- [[Zricenina_03_ruin_stav]] (i v projektu SKVT jako [[Zricenina_03_ruin_stav]]),
- [[05_constructions]] (typy a klíče dat),
- [[CHECKLIST_assets_navrhy]] (kap. 8 a tabulka typů),
- `KNOWHOW_hrad.md` (poučení),
- tento soubor: po každém dokončeném kroku přepiš kap. 2 a 4.
