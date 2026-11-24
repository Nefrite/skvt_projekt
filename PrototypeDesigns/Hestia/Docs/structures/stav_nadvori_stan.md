---
# orchestrace
type: state
validity: valid
updated: 2026-11-24
aliases: []
# hra
domain: structures
entity: "[[Nadvori_Stan]]"
depth: 4
build_step: 05_constructions
assets: []
---
# Nadvori_Stan – stav stavby (stan na nádvoří a vybavení)

## Souhrn
Skutečný stav stanu na nádvoří (`Nadvori_Stan` v [[05_constructions]], typ `tent`, sada `site`, `pile: True`) a jeho vybavení (`Nadvori_Stan_Vybaveni` v [[06_furnishing]], sada `site`) proti návrhu [[navrh_nadvori_stan]] (k 24. 11. 2026). GameDesigner (24. 11. 2026) rozhodl o zařazení stanu do hry (`status: built`), přesunul jej u severní hradby `Hradba_Z_S` mezi Guesthouse a prkna staveniště (`s = 1,5 m; n = 18,8 m`) s vchodem na jih a odložil stříšku z kůry (`bark_roof`) na později. Vše je vygenerováno ve skriptech a datech, ověřeno mimo UE (`run_checks.py --only brana,stan` OK, 0 kolizí) a **ověřeno v UE GameDesignerem (24. 11. 2026)**.

## Co je hotové
| Část | Krok | Provedení | Sada |
|---|---|---|---|
| `Nadvori_Stan` (`tent`, `pile: True`) | `05_constructions` | 33 dílců v jednom posouvatelném actoru (`Stavby/Nadvori`, pivot dole uprostřed): 2 stojky [[SM_RuinPoleBark_A]] Ø `7 cm` (zapuštění `8 cm`), hřeben Ø `6 cm × 2,60 m` (vrch `1,90 m`), 2 ovázání [[SM_RuinLashing_A]], plachta [[SM_RuinCanvasTent_A]] posazená podle `center` v `.json`, 13 obvodových kolíků [[SM_RuinStakeSmall_A]] (`30 cm`, zapuštění `15 cm`, náklon `15°`), 6 napínacích šňůr (2 štítové + 4 rohové, řetěz [[SM_RuinRope_A]] Ø `1,5 cm`, `link = 1,0 m` jako u `Vez_Pristresek`) se 6 kotvicími kolíky `0,50 m` od plátna; `clear_poly` uklízí suť pod stanem | `site` |
| `Nadvori_Stan_Vybaveni` (`props`) | `06_furnishing` | 4 samostatné actory (`Vybaveni/Nadvori/Stan`, tag `stage:site` pro `Etapa.py`): uvnitř stanu 1 lůžko podél východní strany (`Luzko` [[SM_RuinCampBed_A]], `scale Y = 0,90` → šířka `69 cm`), na západní straně uvnitř `Truhlicka` [[SM_RuinChestSmall_A]] a `Vak` [[SM_RuinBundle_A]], před vchodem `Spalek` [[SM_RuinStump_A]] | `site` |

## Souhrn specifikace
- **Sdílené parametry (05 i 06):** `Lapikus/tools/ruin/nadvori_spec.py` (`STAN_CENTER = (1.5, 18.8)`, `STAN_PEG`, `STAN_ROPE`, `STAN_GUYS`, `STAN_CLEAR`, `stan_frame()`, `stan()`, `stan_vybaveni()`).
- **Kód 05 a 06:** nový typ `tent` v `Lapikus/05_constructions/zr_stavby/stan.py`, registrace v `build_constructions.py` (včetně sloučení vícemateriálového `pile: True` do jednoho actoru na sadu etapy) a `tools/constructions/gen_constructions.py`; podpora volitelného `stage` na skupině v `Lapikus/06_furnishing/build_furnishing.py` a skupina v `tools/furnishing/gen_furnishing.py`.
- **Spouštěče v UE:** `05_constructions/stavby/Nadvori_Stan.py` (+ `Nadvori_Stan_Capture.py`), `06_furnishing/vybaveni/Nadvori_Stan.py` (+ `Nadvori_Stan_Capture.py`), přepnutí etapy `05_constructions/stavby/Etapa.py`.
- **Kontroly a náhled mimo UE:** `python Lapikus/tools/checks/run_checks.py --only stan`; 3panelový náhled `Lapikus/05_constructions/Stavby_nadvori_stan_nahled.png`.

## Co se liší od návrhu (a proč)
Rozhodnutí GameDesignera (24. 11. 2026) oproti [[navrh_nadvori_stan]]:
1. **Nová poloha a orientace:** stan přesunut u severní hradby `Hradba_Z_S` mezi Guesthouse (`s = -8,41`) a prkna staveniště (`s = 10,53`) na střed `s = 1,5 m; n = 18,8 m` s vchodem na jih (`+X = -n` paláce, `+Y` odhrnutá chlopeň na západ) místo `s = 21,5–23,9` s vchodem na východ. Terén je zde rovný (`Z = 3129 cm`), výška hradby `4,6–5,2 m`, mezera od hradby `0,33 m` (zadní kotvicí kolík).
2. **Stříška z kůry (`Nadvori_Stan_Striska`, `bark_roof`) odložena:** zatím postaven jen stan a jeho vybavení.
3. **Vybavení přesunuto do `06_furnishing` a upraveno pro jednoho obyvatele:** místo dvou lůžek je uvnitř stanu 1 lůžko (`Luzko`), truhlička (`Truhlicka`) a vak (`Vak`) jsou uvnitř stanu na protější (západní) straně, před vchodem stojí špalek (`Spalek`); vše jako samostatné actory v `Nadvori_Stan_Vybaveni` s tagem `stage:site` (rozhodnutí 16. 11. a 24. 11. 2026).
4. **Stružka kolem stanu vynechána** (terénní úprava se neřeší).
5. **Vchod plachty:** schválený mesh [[SM_RuinCanvasTent_A]] (22. 11. 2026) má shrbený vchod cca `0,7 × 0,7 m` místo původních `0,7 × 1,7 m` v kap. 7 návrhu.

## Ověřeno v UE
### V levelu (report z UE)
Poslední report `Maintenance/reports/ue_Nadvori_Stan.json` je z 2026-11-23 (0 actorů, před postavením).
### Vizuálně ověřeno (kdo, kdy)
**GameDesigner (Jirka), 2026-11-24:** stan `Nadvori_Stan` (plachta `MI_RuinCanvas`, lana `MI_RuinRope`, konstrukce, kolíky, `pile: True`) i vybavení `Nadvori_Stan_Vybaveni` (`Luzko`, `Truhlicka`, `Vak`, `Spalek`) ověřeny v UE Editoru (`/Game/Skvt/LapikusPrototypeMap`).

Mimo UE ověřeno 2026-11-24:
- `run_checks.py --only brana,stan` – vše OK (0 kolizí s `Hradba_Z_S`, Guesthouse i staveništěm, mezera od hradby `0,33 m ≥ 0,30 m`, plachta `1,0 cm` nad terénem, hřeben `1,90 m`, vše `stage = site`, `Brana_Zataras` beze změny);
- diff `constructions.json` potvrdil, že přibyla jen stavba `Nadvori_Stan` a žádné jiné stavby se nezměnily;
- vizuální kontrola 3panelového náhledu `Lapikus/05_constructions/Stavby_nadvori_stan_nahled.png`.

## Co zbývá
- Později (odloženo): stříška z kůry `Nadvori_Stan_Striska` novým typem `bark_roof` (viz `T-0035`).

## Odkazy na návrh a předání
- [[navrh_nadvori_stan]]
- [[SM_RuinCanvasTent_A]]
