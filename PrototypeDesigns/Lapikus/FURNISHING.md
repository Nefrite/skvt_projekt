# FURNISHING – vybavení hradu (základní přehled)

Stav: 16. 11. 2026. Instrukce pro agenta vybavení: `AGENT_Furnisher_hrad.md`. Podrobný technický návod je v `06_furnishing/README_furnishing.md`, pravidla a pasti v `KNOWHOW_hrad.md`, seznam meshí v `CHECKLIST_assets_navrhy.md` kap. 6.

## 1. Co je vybavení

**Vybavení je všechno, co člověk přenese** (rozhodl Jirka 16. 11. 2026): nářadí, sudy, špalky, koše, nábytek, hranice dřeva, materiál na staveništi.

Hrad se skládá ze tří vrstev, které se staví odděleně a navzájem se nepřepisují:

| Vrstva | Co obsahuje | Tag actorů | Data | Ruční úpravy |
|---|---|---|---|---|
| `03_ruin` | zřícenina: zdi, otvory, kapsy, dlažba | `Zricenina_Ruin` | `ruin_layout.json` | `manual_edits.json` |
| `05_constructions` | dostavby: pevné, zabudované nebo zatlučené (krovy, stěny, výheň, žlab, sud pod okapem, kůl v zemi) a suť | `Zricenina_Stavby` | `constructions.json` | `constructions_edits.json` |
| `06_furnishing` | vybavení: přenosné props | `Zricenina_Vybaveni` | `furnishing.json` | přímo v `furnishing.json` (capture) |

Hranice 05 / 06 se řídí otázkou „dá se to odnést, aniž by se něco rozbíralo?“ Ano → 06. Ne (zazděné, zatlučené, připevněné ke stavbě, sbírá vodu ze střechy) → 05. Příklad z kovárny: lišta s kolíky a nářadím je 06, kůl u hranice dřeva a sud pod žlabem zůstávají v 05.

Vybavení stojí ve stavbách a bere z nich rozměry (rámy, výška krokví), stavby ani zříceninu ale nemění. Proto se dá ladit a přestavovat kdykoli bez rizika pro 03 a 05.

## 2. Jak se vybavení vytváří

1. **Spec:** polohy kusů jsou v souboru rozměrů stavby (`tools/ruin/<cast>_spec.py`), v rámu stavby (`s` podél zdi, `n` kolmo), jako seznam položek typu `props`. Poloha kusu = střed bounding boxu meshe (`KNOWHOW_hrad.md` kap. 5.7).
2. **Generátor:** `tools/furnishing/gen_furnishing.py` z nich sestaví skupiny do `06_furnishing/furnishing.json`. Existující data nepřepíše, ale sloučí: polohy uložené z levelu zůstanou, nové kusy ze specu přibudou.
3. **Kontroly mimo UE:** `tools/checks/run_checks.py` (průniky se zříceninou, se stavbami i mezi sebou, průchody, vzdálenosti), náhled `tools/checks/preview3d.py`.
4. **Build v UE:** spouštěč skupiny `06_furnishing/vybaveni/<Skupina>.py`. Každý kus je samostatný actor ve složce `Vybaveni/...` s tagy `Zricenina_Vybaveni`, `vybaveni:<skupina>`, `id:<skupina>|<kus>`.
5. **Ruční doladění v levelu:** kusy posuň, otoč, změň velikost (Scale), smaž nebo zkopíruj (Alt+tah) a spusť spouštěč s `MODE = "capture"`. Stav se zapíše **přímo do `furnishing.json`** (v rámu stavby, záloha `.bak`), další build i přegenerování ho zachovají. `list` vypíše posuny proti specu, `reset` vrátí kusy na spec (kopie smaže).

Meshe props jsou ve sdílené knihovně (`zrlib/config.py` → `LIB_MESHES`, typ `props` v `05_constructions/zr_stavby/vybaveni.py`), ve stylu hradu: materiály `MI_Ruin*`, nic ostře „CAD“, pivot na zemi.

## 3. Spouštění

| Co | Skript |
|---|---|
| jedna skupina vybavení | `06_furnishing/vybaveni/<Skupina>.py` (`MODE` `build` / `capture` / `list` / `reset`) |
| uložit úpravy skupiny z levelu | `06_furnishing/vybaveni/<Skupina>_Capture.py` (kovárna `Palac_Kovarna_Capture.py`) |
| všechno vybavení | `06_furnishing/build_furnishing.py` |
| uložit úpravy všeho vybavení | `06_furnishing/capture_furnishing.py` |
| stavba včetně svého vybavení | souhrnný spouštěč stavby v 05, např. `05_constructions/stavby/Palac_Kovarna.py` (`VYBAVENI = True`) |
| celý hrad | `build_normal.py` (aditivně), `build_fullscope.py` (smaže a postaví vše znovu, i vybavení); přepínače `VYBAVENI` (stavět vybavení) a `CAPTURE_VYBAVENI` (před buildem uložit úpravy z levelu) |

## 4. Skupiny vybavení

| Skupina | Kde | Stav | Obsah |
|---|---|---|---|
| `Palac_Kovarna_Vybaveni` | kovárna, východní místnost paláce | ✅ rozmístěno 16. 11. 2026, kontroly OK, v UE neověřeno | 28 kusů: kovadlina na špalku, kalicí sud, hřebovnice, měchy s pákou, šlapací brus se stoličkou, ponk, truhlík s uhlím a víkem, koš, lišta s nářadím, železné pruty, tři hranice dřeva pod přesahem |

**Kandidáti na další skupiny** (meshe částečně hotové, viz `CHECKLIST_assets_navrhy.md` kap. 6):

- dům posádky, etapa 2: lůžka, stůl, truhly, police, ponk, hranice dřeva v síni, žebřík na půdu;
- dům posádky, staveniště (etapa 1): kozy, rozpracovaná kulatina, hromady materiálu, tesařské nářadí, žebřík;
- brána: španělský jezdec (zátaras);
- stan na nádvoří: lůžka, špalek, ranec, truhlička.

K rozhodnutí: dveře a okenice visí na pantech ve stavbě, podle pravidla tedy patří do 05.

Etapy (`stage:base` / `final` / `site`, `zrlib/config.py` → `STAGES`) vybavení zatím nepoužívá. Kovárna stojí už v etapě 1. U domu a staveniště bude potřeba sadu u skupiny nebo kusu doplnit.

## 5. Pravidla

- `furnishing.json` je jediný zdroj poloh vybavení: neregenerovat ho jinak než přes `gen_furnishing.py` (slučuje), polohy měnit v levelu + capture. `manual_edits.json` a `constructions_edits.json` (03, 05) se dál nepřepisují.
- Capture jen po buildu se stejnými meshi.
- Spec drží výchozí polohy pro nové kusy a pro `reset`; uložená poloha z levelu má přednost. Když se má výchozí poloha změnit i ve specu, čísla z `list` přenést do specu (nepovinné).
- Nová skupina: spec → `gen_furnishing.py` → spouštěč `vybaveni/<Skupina>.py` → kontroly v `run_checks.py` (vybavení je v `common.state()` pod klíčem `furn`), případně zapojit do souhrnného spouštěče stavby v 05.
