---
# orchestrace
type: state
validity: valid
updated: 2026-11-19
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
| `Palac_Obydli_Ohniste` | `hearth`, `zr_stavby/ohniste.py` | pec s nístějí: sokl, zdi pece, klenba (`SM_RuinOvenDome`), zídky plotny; sopouch, dymník, komín, pás nad ústím, plotna a poklop | kámen a klenba `base`, ostatní `final` |
| `Palac_Obydli_Srub` | `log_wall`, `zr_stavby/srub.py` | severní stěna, příčka, srub na obou bočních stěnách, prkenné štíty, otvory zarovnané na řady | `base` / `final` |

- **Samostatné actory** (ruční doladění, `MODE = "capture"` ve spouštěči stavby): patní kameny sloupů, plotna (`Palac_Obydli_Ohniste|I2`), poklop ústí (`Palac_Obydli_Ohniste|Poklop`, mesh `SM_RuinOvenDoor`: plech s dřevěnou rukojetí, opřený o čelo pece západně od ústí).
- **Nové meshe** (naimportují se při buildu samy): `meshes/wattle/SM_RuinOvenDome_A/B.obj`, `meshes/props/SM_RuinOvenDoor_A.obj`.
- **Přepnutí etapy v editoru:** `05_constructions/stavby/Etapa.py` (`ETAPA` 1 / 2 / 0). Po každém buildu pustit znovu.
- **Náhledy:** `05_constructions/Stavby_palac_obydli_nahled.png` (etapa 2), `Stavby_palac_obydli_nahled_etapa1.png` (etapa 1, ještě před posunem příčky a pecí).

## Souhrn specifikace
Doplní se při rozpadu.

## Co se liší od návrhu (a proč)
Přesné rozměry a odchylky od původního návrhu: návrh kap. 0.5 (kámen), 0.5a (větší světnice), 0.5b (pec), 0.6 (krov a srub).

## Ověřeno v UE (ano/ne, kdy, kým)
Všechno je ve skriptech a prošlo `tools/checks/run_checks.py` (`SOUHRN: ... obydli OK`). **V UE je potvrzené jen navázání kamene podezdívek** (Jirka 16. 11. 2026). Krov, srub, pec, posun příčky a nové meshe v UE zatím neběžely.

## Co zbývá
Viz [[predani_palac_obydli_stavitel]] kap. 4 (finální stav) a 5 (staveniště a etapa 1).

## Odkazy na návrh a předání
- návrh: [[navrh_palac_obydli_stred]] (kap. 0: stav po krocích a rozměry)
- předání: [[predani_palac_obydli_stavitel]] (aktivní)
