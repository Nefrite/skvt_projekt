---
# orchestrace
type: design
validity: valid
derived_from: "[[navrh_vez_pristresek]]"
alternative_to: []
updated: 2026-11-22
aliases: []
# hra
status: in_progress
domain: structures
category: []
entity: "[[Vez]]"
depth: 3
build_step: 03_ruin
assets: []
---
# Návrh: Vez – škody z dobývání na koruně věže

## Souhrn
Škody z dobývání věže od východu a jihovýchodu jako součást zříceniny (03): `Vez_V` s hlavním průlomem, `Vez_J` s průlomem do tvaru mísy nad přístřeškem, `Vez_Z` jen s vedlejšími škodami (střed vyšší), `Vez_S` s plynulým poklesem koruny k SV rohu (11,2 m). Data v `tools/ruin/tower_spec.py` → `ruin_edits()`. Přístřešek hlídky, který na škody navazuje: [[navrh_vez_pristresek]], stav: [[stav_vez_pristresek]].

Přesunuto z [[navrh_vez_pristresek]] kap. 3 (2026-11-22); číslování 3.x je zachované kvůli odkazům.

## 3. Úpravy 03: škody z dobývání

**Vyžaduje úpravu 03.** Zdi se nemění kvůli plachtě. Jsou to starší škody z dobývání hradu, tedy součást zříceniny (stav 1650). Posádka nízkou jižní korunu jen využila pro okap. Žádná rovná koruna, žádný `cap`.

**Příběh škod (Jirka, 14. a 17. 11. 2026):** hrad se dobýval silou od východu a jihovýchodu. V oblouku naproti hradu je dost místa pro tábor a obléhací stroje.

| Zeď | Role | Změna |
|---|---|---|
| `Vez_V` (východní) | hlavní cíl střelby | **nový hlavní průlom**, nejvíc poškozená zeď věže (kap. 3.1) |
| `Vez_J` (jižní) | zasažená šikmo od jihovýchodu | průlom, k JV rohu pozvolný bok (kap. 3.2) |
| JV roh | nároží obou zasažených zdí | o 1,4–2,1 m níž než dnes (nově 11,2–11,9 m) |
| SV roh | nároží `Vez_V` a `Vez_S` | o 2,1–2,8 m níž než dnes (nově 11,2–11,55 m), navazuje na obě zdi |
| `Vez_Z` (západní) | jen vedlejší škody (střely přes sníženou východní zeď) | **střed zdi vyšší než dnes** (kap. 3.3) |
| `Vez_S` (severní) | zasažená od východu, jen podél | **místo průlomu do tvaru U plynulý pokles** od SZ rohu k SV rohu (kap. 3.4) |

Všechny změny se zapisují v `tools/ruin/gen_layout.py` u dané zdi (`breaches`, `protect`), pak `gen_layout.py` → `ruin_layout.json`. `floor` a `min` jsou v metrech od paty zdi, ne od podlahy věže. Koruna vychází o 0,3–0,7 m níž než zadaná hodnota (rozebírání, zaokrouhlení na řady).

Hodnoty jsou **ověřené výpočtem** 17. 11. 2026 (viz [[stav_vez_pristresek]]). Výsledek závisí na `seed`; po jiné změně zdi ho stavitel přepočítá a porovná s tabulkami.

### 3.1 `Vez_V`: hlavní průlom

- **Zápis v datech:**
  - `breaches`: `{"s0": 2.5, "s1": 6.5, "floor": 10.3, "slope_l": 0.7, "slope_r": 0.35}` (hlavní průlom, jižní bok pozvolný k JV rohu, severní pozvolný k SV rohu),
  - `breaches`: `{"s0": 3.2, "s1": 4.8, "floor": 9.95, "slope": 0.6}` (nejhlubší místo jižně od středu).
- U `Vez_V` je `s` = `v` (od J-V rohu k severu).

Koruna `Vez_V` (m od podlahy přízemí, nejvyšší vrstva zdi):

| v (m) | Dnes | Nově | Ubude |
|---|---|---|---|
| −1 až 0,25 (JV roh) | 12,95–13,65 | 11,2–11,9 | 4–5 řad (1,4–1,75 m) |
| 0,5–1,5 | 12,25–12,95 | 10,85–11,2 | 4–5 řad |
| 1,75–2,5 | 11,2–12,6 | 10,15–10,85 | 3–6 řad (až 2,1 m) |
| 2,75–4,5 | 10,15–11,9 | 9,45–9,8 | 2–6 řad |
| 4,75–6,0 (bývalá střílna) | 10,15–10,85 | vnější líc 9,45–9,8, jádro 9,1–9,45 | 2–3 řady |
| 6,25–6,5 | 10,15–10,5 | 9,45–10,15 | 1–2 řady |
| 6,75–8,25 | 9,8–11,2 | 9,1–10,5 | 1–3 řady |
| 8,5–9,75 | 11,2–12,95 | 10,15–10,85 | 2–6 řad |
| 10–11 (SV roh) | 13,3–14,35 | 11,2–11,55 | 6–8 řad (2,1–2,8 m) |

- **Celkem ubude** 223 kamenů (`Vez_V` má dnes 2 141 kamenů, nově 1 918).
- **Tvar:** široký průlom s nejnižším místem jižně od středu. Od něj koruna stoupá pozvolna k JV rohu i k SV rohu (11,2–11,55 m), kde navazuje plynulý pokles `Vez_S` (kap. 3.4).
- **Nejnižší koruna je 9,45 m**, místy o řadu níž (9,1 m: v bývalém výklenku střílny a v severním boku ve v ≈ 7–8 m). To je 0,7–1,05 m nad podlahou 2. patra. Postava ji nepřejde (limit zídky je 0,5 m), ale přes ni vidí na východ.
- **Střílna 2. patra zaniká.** Nadpraží chybí už dnes. Z výklenku zůstane otevřený výřez s parapetem 0,7–1,05 m.
- **Kapsy trámů 2. patra (8,05–8,4 m) zůstávají**, nad nimi je všude aspoň 0,7 m zdiva. Ověřeno: `Vez_Patra` má po změně stejných 222 dílců včetně všech 12 trámů.
- **SV roh** je záměrně nízko (11,2–11,55 m, stejně jako konec `Vez_S`). Žádný zub mezi průlomem a severní zdí.
- **Suť:** `Vez_V` má `rubble` `out`. Generátor počet kamenů suti podle objemu průlomu nezvyšuje (dnes 24, nově 21 kamenů). Po dobývání by pod východní zdí bylo suti víc, viz otevřené otázky.

### 3.2 `Vez_J`: průlom nad přístřeškem

- **Zápis v datech:**
  - `breaches`: `{"s0": 1.25, "s1": 7.4, "floor": 11.15, "slope_l": 3.0, "slope_r": 0.5}` (západní bok strmý k JZ rohu, východní pozvolný k JV rohu),
  - `breaches`: `{"s0": 2.9, "s1": 4.1, "floor": 10.9, "slope": 0.6}` (hlubší místo západně od střílny),
  - `protect`: `{"s0": 4.6, "s1": 6.4, "min": 11.15}` (nadpraží střílny zůstane).

Koruna `Vez_J` (m od podlahy přízemí, nejvyšší vrstva zdi):

| u (m) | Dnes | Nově | Ubude |
|---|---|---|---|
| 0,5–1,0 (JZ roh) | 11,9–12,25 | 10,85–11,9 | 1–3 řady |
| 1,25–2,4 | 11,9 | 10,15–10,85 | 3–5 řad (1,05–1,75 m) |
| 2,5–4,4 | 10,5–11,2 | 10,15–10,5 | 1–2 řady |
| 4,5–6,5 (nad střílnou) | 10,85–11,55 | 10,85, vnější líc místy 11,2 | 1–2 řady |
| 6,75–7,5 | 11,55–11,9 | 10,5–10,85 | 2–4 řady (0,7–1,4 m) |
| 7,75–9,25 (východní bok) | 12,6–12,95 | 10,85–11,55 | 4–5 řad |
| 9,5–10 (JV roh) | 12,95–14,0 | 11,55–11,9 | 4–6 řad (1,4–2,1 m) |

- **Celkem ubude** 105 kamenů, asi 23 m³ (`Vez_J` má dnes 2 138 kamenů, nově 2 033).
- **Tvar:** nepravidelná mísa. Dno je 1,75–2,45 m nad podlahou patra. Východní bok stoupá pozvolna (asi 1,4 m výšky na 2,5 m délky) k JV rohu, který je společně s `Vez_V` snížený na 11,2–11,9 m.
- **Co zůstává:** nadpraží střílny (10,5–10,85 m) a JZ roh.
- **Podmínka pro přístřešek:** v pásu v = 0,5–1,25 m (vnitřní líc a kraj jádra) nesmí koruna v u = 1,25–7,4 m přesáhnout 10,85 m. Vnější líc může být výš.
- **Suť:** `Vez_J` má `rubble` `out`, kameny spadly ze skály.


### 3.3 `Vez_Z`: střed zůstal vyšší (jen vedlejší škody)

- **Proč:** západní zeď byla mimo hlavní směr střelby. Dnešní zub ve středu (vnitřní líc až 9,8 m ve v ≈ 2,5–3,5 m) je na vedlejší škody hlubší, než odpovídá. Vyšší koruna zároveň z velké části zavře boční mezeru pod plátnem (Jirka 17. 11. 2026).
- **Zápis v datech:** k existující ochraně `dict(s0=4.0, s1=7.0, min=11.6)` (nad oknem 2. patra) přidat:
  - `protect`: `{"s0": 7.0, "s1": 8.2, "min": 12.1}`,
  - `protect`: `{"s0": 8.2, "s1": 9.5, "min": 11.8}`.
- U `Vez_Z` platí s = LT − v (první bod zdi je SZ roh, LT = 10,995 m). s = 7,0–9,5 odpovídá v = 1,5–4,0. Dvě různé hodnoty `min` jsou záměr, aby koruna nebyla rovná.

Koruna `Vez_Z` (m od podlahy přízemí; vnitřní líc / jádro / vnější líc):

| v (m) | Dnes | Nově |
|---|---|---|
| 1,0–1,5 | 11,9 / 12,9 / 12,2 | beze změny |
| 1,5–2,0 | 11,9 / 10,85 / 11,2 | 11,9 / 10,85 / 11,9 |
| 2,0–2,5 | 10,5 / 10,5 / 10,85 | 11,55 / 11,55 / 11,55 |
| 2,5–3,0 | 9,8 / 8,4 / 10,5 | 11,55 / 11,55 / 11,2 |
| 3,0–3,5 | 9,8 / 9,8 / 9,1 | 11,9 / 11,9 / 10,5 |
| 3,5–4,0 | 10,85 / 10,5 / 10,85 | 10,85 / 11,9 / 10,85 |
| 4,0–4,5 | 11,2 / 11,2 / 11,2 | 11,9 / 11,9 / 11,2 |
| 4,5–6,4 (okno) | beze změny | beze změny |

- **Přibude** 37 kamenů (`Vez_Z` 2 050 → 2 087), suť `Vez_Z` 19 → 20 kamenů.
- **Co zůstává:** okno 2. patra s výklenkem, kapsy, JZ roh.
- **Vztah k přístřešku:**
  - ve v = 1,5–2,0 m je vnitřní líc (11,9 m) nad okrajem plátna (11,4–11,6 m), plátno tu končí u líce zdi;
  - dál k severu zůstává mezi korunou a plátnem 0,1–1,5 m. Nejvíc je to u hřebene, kde mezeru zakryje štít (kap. 4.3);
  - pod lemem štítu zůstanou štěrbiny 0–0,7 m nad vnitřním lícem, nejvíc ve v = 3,5–4,0 m. Za nimi je většinou vyšší jádro, průhled ven je jen místy. To je větrání.

### 3.4 `Vez_S`: plynulý pokles k východu místo průlomu do tvaru U

- **Proč:** věž se dobývala z východu. Severní zeď nebyla cílem, škody na ní přibývají směrem k východu, ke zničené `Vez_V`. Dnešní průlom do tvaru U uprostřed zdi tomu neodpovídá (Jirka 17. 11. 2026).
- **Zápis v datech:**
  - zrušit dnešní `breaches`: `{"s0": 3.5, "s1": 7.5, "floor": 12}` (tvar U);
  - nový `breaches`: `{"s0": -3.0, "s1": 0.0, "floor": 11.86, "slope_r": 0.318, "power_r": 0.7}`. Tím vznikne rampa od SV rohu k západu, `power_r` < 1 dává mírný oblouk: koruna od západu klesá nejdřív pomalu, k východu rychleji;
  - `protect` po úsecích 1,5 m, `min` = B(s0) − 0,65, kde B(s) = 11,86 + 0,318 · s^0,7 je rampa breach:
    - `{"s0": -1.6, "s1": 0.0, "min": 11.56}` (SV roh, aby navázal na `Vez_V`),
    - `{"s0": 0.0, "s1": 1.5, "min": 11.21}`, `{"s0": 1.5, "s1": 3.0, "min": 11.63}`, `{"s0": 3.0, "s1": 4.5, "min": 11.90}`,
    - `{"s0": 4.5, "s1": 6.0, "min": 12.12}`, `{"s0": 6.0, "s1": 7.5, "min": 12.32}`, `{"s0": 7.5, "s1": 9.0, "min": 12.51}`, `{"s0": 9.0, "s1": 11.3, "min": 12.69}`.
- Ochrana drží rampu proti silnému rozebírání u uličky (`access` 0,3), rampa breach shora. Bez ochrany by se do zdi znovu vylámal tvar U.
- U `Vez_S` je s = LT − u: první bod zdi je SV roh, s roste k západu.
- **Doporučení:** v `tower_spec.ruin_edits()` zapsat rampu jako vzorec (B(s), krok 1,5 m, odstup 0,65 m), ne jako výčet čísel.

Koruna `Vez_S` (m od podlahy přízemí; vnitřní líc / jádro / vnější líc; u od západu):

| u (m) | Dnes | Nově |
|---|---|---|
| 0–1,0 (u SZ rohu) | 11,5–11,9 / 12,2 / 11,5–12,2 | 11,5–12,6 / 12,2 / 11,5–12,6 |
| 1,0–3,5 | 10,1–11,5 / 9,8–11,9 / 10,1–11,9 | 10,85–12,2 / 12,2 / 11,9–12,2 |
| 3,5–6,0 (střílna 2. patra) | 8,0–10,1 / 8,0–10,1 / 9,8–10,15 | 10,5–12,2 / 10,5–12,2 / 11,5–12,2 |
| 6,0–8,5 | 8,7–10,1 / 9,4–10,15 / 8,7–10,5 | 11,2–11,9 / 11,2–11,55 / 10,85–11,9 |
| 8,5–10,0 | 9,1–10,5 / 9,4–9,8 / 9,8–10,85 | 10,85–11,2 / 10,5–11,2 / 10,85–11,2 |
| 10,0–11,5 (SV roh) | 10,8–13,3 / 12,9–13,3 / 11,5–12,9 | 9,8–11,2 / 10,85–11,2 / 10,85–11,2 |

- **Přibude** 105 kamenů (`Vez_S` 1 913 → 2 018), suť `Vez_S` 20 → 21 kamenů. Střed zdi je o 1,5–2,5 m výš než dnes, SV roh o 2,1 m níž.
- **Co zůstává:** dveře 1. patra s kapsami podesty, průchod v přízemí, kapsy průvlaku 1. a 2. patra. Střílna 2. patra má znovu nadpraží a zeď nad ním.
- **Vztah k přístřešku:** žádný. Hřeben (12,70 m) je od severu nad korunou střední části vidět.

### 3.5 Společné

- **Přestavět:** část `Obvod` (všechny čtyři zdi věže najednou), pak 05 `Vez_Patra` a nakonec `Sut`.
- **Ruční úpravy:** úpravy změní ID kamenů `Vez_J`, `Vez_V`, `Vez_S` a `Vez_Z`. `manual_edits.json` byl 17. 11. 2026 prázdný. Před přestavbou to stavitel znovu ověří.
- **Kde zapsat:** podle vzoru `palac_spec.ruin_edits()` a `brana_spec.ruin_edits()` patří hodnoty z kap. 3.1–3.4 do `tools/ruin/tower_spec.py` (nová funkce `ruin_edits()`). `gen_layout.py` je jen převezme. Jeden zdroj pro 03 i kontroly přístřešku.
