---
# orchestrace
type: state
validity: valid
updated: 2026-11-21
aliases: []
# hra
domain: structures
entity: "[[Palac_Obydli]]"
depth: 3
build_step: 05_constructions
assets: []
---
# Palac_Obydli – stav stavby

## Co je hotové
| Stavba | Typ, modul | Obsah | Sady |
|---|---|---|---|
| 03 část `Palac` | `gen_layout.py`, `palac_spec.ruin_edits` | portál přesunutý do západní místnosti (`Palac_S` s = 4,5), hrubý průchod v `Palac_S` s = 16, průchod v `Palac_pricka_2` n = 6,9–8,5 ke kovárně | – |
| `Palac_Obydli_Kamen` | `stone_fill`, `zr_stavby/zdivo.py` | obě příčky srovnané na 1,4 m, podezdívky severní stěny a příčky, maltové jádro v ose | `base` |
| `Palac_Obydli_Krov` | `pult_roof`, `zr_stavby/pult.py` | 5 sloupů na patních kamenech, horní pozednice a střední vaznice ze dvou kusů, 3 špalky pod vaznicí, 12 krokví, 2 řady latí nad světnicí. **Bez krytiny.** | `base` / `final` |
| `Palac_Obydli_Ohniste` | `hearth`, `zr_stavby/ohniste.py` | pec s nístějí: sokl, zdi pece, klenba (`SM_RuinOvenDome`), zídky plotny; sopouch, dymník, komín, pás nad ústím, plotna a poklop | kámen, klenba a tmavý vnitřek pece `base`; ostatní včetně uhlí pod plotnou (box `U`) `final` |
| `Palac_Obydli_Srub` | `log_wall`, `zr_stavby/srub.py` | severní stěna, příčka, srub na obou bočních stěnách, prkenné štíty, otvory zarovnané na řady | `base` / `final` |
| `Palac_Obydli_Stavenisko`, `_Kulatina`, `_Tramy`, `_Prkna`, `_Kozy` | `props`, `zr_stavby/vybaveni.py` | staveniště etapy 1: vzpěry V1–V4 sloupů 11,1 a 13,0, žebřík ve světnici, na nádvoří před `Palac_S` hranice srubové kulatiny (S3), tesaného dřeva krovu (S4) a jedna hranice prken na krytinu (S5, 75 prken, vrch 1,375 m; poloha z levelu, Jirka 21. 11. 2026); kozy s rozpracovanou kulatinou (S6, mesh `SM_RuinLogPeeling`) a pruhy kůry. Rozměry `palac_spec.py` → `D_SITE`, `obydli_stavenisko()` | `site` |

- **Samostatné actory** (ruční doladění, `MODE = "capture"` ve spouštěči stavby): patní kameny sloupů, plotna (`Palac_Obydli_Ohniste|I2`), poklop ústí (`Palac_Obydli_Ohniste|Poklop`, mesh `SM_RuinOvenDoor`: plech s dřevěnou rukojetí, opřený o čelo pece západně od ústí).
- **Nové meshe** (naimportují se při buildu samy): `meshes/wattle/SM_RuinOvenDome_A/B.obj`, `meshes/props/SM_RuinOvenDoor_A.obj`, `meshes/wood/SM_RuinLogPeeling_A/B.obj` (rozpracovaná kulatina, 21. 11. 2026).
- **Staveniště:** vzpěry a žebřík jsou samostatné actory. Každá hranice je samostatná stavba a v UE jeden actor (pivot dole uprostřed, tag `pile:<stavba>`) ve složce `Stavby/Palac/Obydli/Stavenisko`. Po posunu nebo natočení v UE uložit přes `Palac_Obydli_Stavenisko_Capture.py`. Suť pod původní polohou hranic na nádvoří je uklizená (`clear_poly`).
- **Přepnutí etapy v editoru:** `05_constructions/stavby/Etapa.py` (`ETAPA` 1 / 2 / 0). Po každém buildu pustit znovu.
- **Náhledy:** `05_constructions/Stavby_palac_obydli_nahled.png` (etapa 2), `Stavby_palac_obydli_nahled_etapa1.png` (etapa 1 se staveništěm, 21. 11. 2026).

## Souhrn specifikace
Doplní se při rozpadu.

## Co se liší od návrhu (a proč)
Přesné rozměry a odchylky od původního návrhu: návrh kap. 0.5 (kámen), 0.5a (větší světnice), 0.5b (pec), 0.6 (krov a srub), 9.2a (staveniště: pultramy S3 jako třetí vrstva, výšky hranic 0,72 / 0,58 / 1,375 m, jedna vyšší hranice prken, každá hranice jeden objekt posouvaný v UE, uklizená suť pod hranicemi).

## Ověřeno v UE (ano/ne, kdy, kým)
Všechno je ve skriptech a prošlo `tools/checks/run_checks.py` (`SOUHRN: ... obydli OK`). **Kámen, krov, srub, pec, posun příčky a nové meshe jsou v UE postavené a Jirka je 21. 11. 2026 vizuálně zkontroloval: v pořádku, nic nechybí.** Čtení stavu v UE z téhož dne: 18 actorů, 12 `base`, 6 `final`.

**Staveniště a uhlí pod plotnou v sadě `final` (21. 11. 2026):** jen mimo UE. `run_checks.py --only obydli` OK včetně kontrol etapy 1 (kap. 9.4 návrhu), náhled etapy 1 hotový. Vizuální kontrola v UE zatím neproběhla.

## Co zbývá
Viz [[predani_palac_obydli_stavitel]]: kap. 4 (vizuální kontrola staveniště a etapy 1 v UE) a kap. 5 (finální stav). Návrh staveniště: [[navrh_palac_obydli_stred]] kap. 9.

## Odkazy na návrh a předání
- návrh: [[navrh_palac_obydli_stred]] (kap. 0: stav po krocích a rozměry)
- předání: [[predani_palac_obydli_stavitel]] (aktivní)
