---
# orchestrace
type: handover
validity: valid
superseded_by:
updated: 2026-11-21
# hra
domain: structures
entity: "[[Guesthouse]]"
build_step: 05_constructions
---
# Guesthouse – kamna s dymníkem: předání staviteli

## Pro koho a co
Předává Furnisher (session s Jirkou 21. 11. 2026), přebírá stavitel ([[Builder]]). Postavit v obytné části u ostrohu kamna s dymníkem a komínem jako novou stavbu v `05_constructions`.

## Zadání
- Kamna po vzoru pece v obydlí (`Palac_Obydli_Ohniste`, typ `hearth`, [[navrh_palac_obydli_stred]] kap. 0.5b), ale **menší a úspornější, bez nístěje a plotny, s dymníkem nad ústím** (rozhodnutí Jirky 21. 11. 2026), komín skrz krytinu `Ostroh_Krov`.
- Poloha a obrys tělesa podle zástupného kvádru `Pec_Zastupce` ve vybavení ([[navrh_guesthouse_vybaveni]], tabulka v kap. Návrh): zády k hradbě `Hradba_Z_S` v jihozápadním klínu, ústí do místnosti.
- Rozměry si stavitel upřesní podle typu `hearth`; rozměr zástupce 1,0 × 0,9 × 1,2 m je jen obrys pro rozvržení vybavení.

## Platná rozhodnutí
- Poloha kamen a dřeva vedle nich: [[navrh_guesthouse_vybaveni]] (kap. Návrh), rám a spec `tools/ruin/ostroh_spec.py` → `GH_OVEN`, `GH_WOOD`.
- Hranice 05 / 06: kamna, dymník a komín jsou pevná stavba (05); poklop ústí (♻ `SM_RuinOvenDoor`) a dřevo jsou vybavení (06). [[FURNISHING]] kap. 1.

## Výchozí stav
[[stav_guesthouse]]; krov, dostavba a podlaha u ostrohu podle [[05_constructions]].

## Kritéria hotovo
- Stavba kamen (např. `Ostroh_Kamna`) v datech 05 a spouštěč v `05_constructions/stavby/`, data ze specu (`ostroh_spec.py`).
- Komín prochází krytinou v poli mezi trámy vějíře: trám B1 jde asi 0,5 m od středu zástupce, takže prostup patrně v poli B0–B1 za kamny; spodek krovu nad kamny asi 2,95 m nad podlahou. Prostup s vůlí od trámů a krytiny jako u kovárny a obydlí.
- Pod kamny je **kamenná dlažba** (rozhodl Jirka 21. 11. 2026, [[navrh_guesthouse_vybaveni]]): podlaha `Ostroh_Podlaha` se pod dlažbou vyřízne (typ `plank_floor`, `avoid`), dlažba lícuje s vrchem prken a přesahuje obrys kamen (přesah navrhne stavitel).
- Kontroly v `run_checks.py --only ostroh`: průniky kamen s krovem, dostavbou, zříceninou a podlahou; vybavení Guesthouse bez průniku s kamny.
- Po postavení napiš Furnisherovi: odebere `Pec_Zastupce` a podle skutečného obrysu doladí hromádku dřeva.

## Otevřené otázky

## Zbývá
