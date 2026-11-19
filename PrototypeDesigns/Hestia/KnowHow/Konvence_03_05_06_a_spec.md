---
# orchestrace
type: knowhow
knowhow_kind: convention
tech: [python, ue_python]
scope: instance
verified: 2026-11-17
validity: valid
updated: 2026-11-19
aliases: []
# hra
domain: structures
---
# Konvence: zřícenina, dostavby a vybavení odděleně, jeden spec

<!-- Z KNOWHOW_hrad.md kap. 1 body 1–4 a AGENT_Furnisher_hrad.md kap. 2 (pilot Lapikus, B6). -->

1. **Zřícenina (03) a dostavby (05) jsou oddělené.** `03_ruin` je hrad po rozpadu (~1650), `05_constructions` pozdější „druhé zabydlení“, které na zřícenině stojí a nemění ji. **Vybavení (06) je od staveb oddělené:** `06_furnishing` obsahuje všechno, co člověk přenese (props), 05 jen pevné části staveb (16. 11. 2026). Zásah do 03 (snížení, žlábek, průlom, vybourání) se vždy uvádí výslovně jako „vyžaduje úpravu 03“ a s částí, kterou je pak nutné přestavět (`Obvod`, `Palac`, `Ostroh`).
2. **Jeden zdroj rozměrů.** Co potřebuje 03 i 05, je v jednom specu (`tools/ruin/ostroh_spec.py`, `tower_spec.py`, `palac_spec.py`, `brana_spec.py`). Nikdy stejné číslo na dvou místech.
3. **Ruční úpravy se nepřepisují.** `manual_edits.json` a `constructions_edits.json` vznikají přes capture z levelu. Capture vždy **před** dalším generováním.
4. **Generovaná data se needitují ručně.** `ruin_layout.json` a `constructions.json` vznikají z generátorů (`gen_layout.py`, `gen_constructions.py`), ruční změna se při příštím generování ztratí.

- **Vybavení je všechno, co člověk přenese** (rozhodl Jirka 16. 11. 2026): nářadí, sudy, špalky, koše, nábytek, hranice dřeva, materiál na staveništi.
- Test hranice 05 / 06: „Dá se to odnést, aniž by se něco rozbíralo?“ Ano → `06_furnishing`. Ne (zazděné, zatlučené, připevněné ke stavbě, sbírá vodu ze střechy) → `05_constructions`. Příklad z kovárny: lišta s kolíky a nářadím je 06, kůl u hranice dřeva a sud pod žlabem jsou 05.
- Nerozhodnuto: dveře a okenice na pantech (podle pravidla 05). Neber jako dané, zeptej se.
- Vybavení **stojí ve stavbách 05 a bere z nich rozměry** (rám stavby, výška krokví pro zavěšená lana), stavby ani zříceninu ale nemění. Když kus potřebuje změnu stavby (háček, polička zabudovaná do zdi, úklid suti), je to požadavek na stavitele.
- Polohy kusů patří do **specu stavby** v `tools/ruin/` (`palac_spec.py` → `kovarna_vybaveni()`), vedle rozměrů stavby, ze kterých vycházejí. Rozměry nikdy nekopíruj do dvou míst; odkazuj na konstanty specu (`K_*`).
