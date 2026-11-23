---
# orchestrace
type: design
validity: valid
derived_from: "[[navrh_palac_obydli_stred]]"
alternative_to: []
updated: 2026-11-23
aliases: []
# hra
status: in_progress
domain: structures
category: []
entity: "[[Palac_Obydli]]"
depth: 4
build_step: 05_constructions
assets: []
---
# Návrh: Palac_Obydli – pec s nístějí a komín

Vyčleněno z [[navrh_palac_obydli_stred]] kap. 4.6 (2026-11-23); číslo kapitoly je zachované kvůli odkazům. Dům, strop a krytina: [[navrh_palac_obydli_stred]]; sady etap: [[navrh_palac_obydli_etapy]] kap. 0.7; stav: [[stav_palac_obydli]].

## 4.6 Pec s nístějí a komín
Zabydlení je dlouhodobé a má být pro posádku pohodlné. Styl: dobové provizorium, železo z vlastní kovárny na míru. Stavba `Palac_Obydli_Ohniste` (typ `hearth`), rozměry `palac_spec.py` → `D_OVEN`, `D_CHIMNEY`.

| Část | Rozměr a poloha | Sada |
|---|---|---|
| kamenný sokl | 1,6 × 1,6 × 0,6 m; s = 15,96–17,56; n = 0,72–2,32; nahoře hliněný maz 4 cm | `base` |
| pec (vzadu u `Palac_J`) | 1,4 × 1,0 m; kamenné zdi 22 cm do 1,0 m, čelo s ústím 0,4 × 0,36 m k severu | `base` |
| hliněná klenba | nízká valená klenba 1,4 × 1,0 m, vrch 1,34 m (mesh `SM_RuinOvenDome`), tmavý vnitřek pece | `base` |
| nístěj (vpředu) | 1,6 × 0,6 m ve výšce 0,64 m | `base` |
| plotna | železná 0,58 × 0,44 m na dvou kamenných zídkách 22 cm, na východní straně nístěje (vrch 0,87 m), pod ní vrstva uhlí (box `U`); plotna je **samostatný actor** | zídky `base`, plotna a uhlí `final` |
| kovaný pás nad ústím | 0,7 m, v čele pece | `final` |
| poklop ústí | plech 46 × 42 cm s dřevěnou rukojetí na dvou trnech (mesh `SM_RuinOvenDoor`), opřený o čelo pece západně od ústí; **samostatný actor**, dá se ručně doladit a uložit přes capture | `final` |
| sopouch | hliněný kouřovod 0,28 m z klenby za čelem pece (n = 1,56) do dymníku | `final` |
| dymník | 1,6 × 1,1 m, spodní okraj 1,8 m, výška 0,8 m; nad ústím a nístějí (střed n = 1,7) | `final` |
| komín | 0,5 × 0,5 m, střed s = 16,76; n = 1,7; vrch 5,3 m | `final` |

- **Tah:** pec táhne sopouchem přímo do dymníku a komína, dymník sbírá kouř z plotny a z ústí při přikládání. Poklop se nasazuje po vyhoření.
- **Osa pece je s = 16,76**, uprostřed mezi krokvemi 16,26 a 17,26 (komín 16 cm od obou). Střed mezi sloupy 15,3 a 18,0 je 16,65; od patních kamenů zbývá 0,48 m na západě a 0,26 m na východě.
- **S dalšími stavbami:** dymník visí na výměně stropu ([[navrh_palac_obydli_stred]] kap. 4.5), komín prochází krytinou ([[navrh_palac_obydli_stred]] kap. 4.1). Žhavé uhlí a oheň se zatím nedělají.
- **V etapě 1** se pec ještě nepoužívá, proto je `final` všechno kromě kamene, klenby a tmavého vnitřku ([[navrh_palac_obydli_etapy]] kap. 0.7).

## Vazby a ověření
- Sokl pece (s = 15,96–17,56) nesmí zasahovat do výklenku střílny s = 19 (mezera 0,79 m); podlaha světnice končí u soklu ([[navrh_palac_obydli_stred]] kap. 4.5).
- Komín se nedotýká krokví 16,26 a 17,26 a jeho vrch je aspoň 0,5 m nad korunou `Palac_J` v okruhu 1,5 m ([[navrh_palac_obydli_stred]] kap. 7).
- Sady: kámen, klenba a tmavý vnitřek `base`, ostatní `final` ([[navrh_palac_obydli_etapy]] kap. 0.7). Kontrola `run_checks.py --only obydli`.
