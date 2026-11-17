# Návrh: Vez_Pristresek – plátěný přístřešek hlídky na věži

Specifikace architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **postaveno 17. 11. 2026, neověřeno v UE.** Úpravy 03 (kap. 3) v `tower_spec.ruin_edits()`, přístřešek 05 `Vez_Pristresek` (typ `canvas_shelter`, `tower_spec.pristresek()`), kontroly `run_checks.py --only vez`, náhled `05_constructions/Stavby_vez_pristresek_nahled.png`. Odchylky od kap. 4: plátno 2 cm nad krokvemi (ne 0,5 cm, přes ovázání), podkladní kámen v u = 7,20 je dvojitý (0,54 m; koruna pod ním je 10,49 m, kámen 10,84 m sahá pod podklad jen rohem). Vybraná varianta B (západní 2/3 šířky), průlomy z dobývání ve `Vez_J` a `Vez_V` (Jirka 14. 11. 2026), vyšší střed `Vez_Z` a plynule klesající `Vez_S` místo průlomu do tvaru U (Jirka 17. 11. 2026).

**Náhledy:**
- `navrh_vez_pristresek_3d.png`: šest pohledů na přístřešek; zřícenina je spočítaná z dat s úpravami z kap. 3, přístřešek z čísel v kap. 4. Kulatina je jen hranol, plátno je prověšené o 5 cm.
- `navrh_vez_pristresek_3d_dnes_nove.png`: věž dnes a nově ve čtyřech pohledech (z jihovýchodu, od východu, od severu, od severovýchodu).
- `navrh_vez_pristresek.png`: původní schéma z 14. 11. Platí pro korunu `Vez_J` a jižní část `Vez_V` (v ≤ 6 m). Severní bok `Vez_V`, `Vez_Z`, `Vez_S` a štít jsou v něm ve starší podobě.

**Ověřeno 17. 11. 2026 mimo UE na kopii projektu** (data se stejným md5 jako v projektu, terén z levelu `terrain_from_level.json`, `manual_edits.json` prázdný):
- úpravy z kap. 3 zapsané do kopie `gen_layout.py`, z ní vygenerovaný `ruin_layout.json`;
- přístřešek jako kvádry proti kamenům zříceniny a dílcům `Vez_Patra`;
- kontroly `run_checks.py --only openings,floating`: otvorů 104, kolizí 0, kamenů bez podpory 3 (známé).

Soubory projektu se při ověřování neměnily.

**Připravenost** (podrobně `..\CHECKLIST_assets_navrhy.md`):
- **Hotové dílce:** kulatina a tyče s kůrou `SM_RuinLogBark`, `SM_RuinPoleBark`, hlava rozsochy `SM_RuinForkHead`, lano `SM_RuinRope`, ovázání `SM_RuinLashing`, kameny zříceniny. Materiály `MI_RuinBark`, `MI_RuinRope`, oboustranné plátno `MI_RuinCanvas` (vítr připravený parametrem `WindAmount`, výchozí 0).
- **Plátno a štít:** generátor prověšené plochy je hotový (`tools/meshes/mesh_textile.make_canvas` + `write_canvas`), napojení na stavbu chybí.
- **Chybí:** typ stavby `canvas_shelter`, sekce přístřešku v `tools/ruin/tower_spec.py`, úpravy 03 (kap. 3), sekce `vez` v `run_checks.py`.

## 0. Rozhodnutí a změny (17. 11. 2026)

| Bod | Rozhodnutí | Kde |
|---|---|---|
| Mezera pod plátnem nad `Vez_Z` | `Vez_Z` dostala jen vedlejší škody, střed zdi zůstal vyšší (úprava 03). Mezera se tím z velké části zavře, zbytek pod lemem štítu je větrání. Štít se dolů ke koruně neprodlužuje. | kap. 3.3, 4.3 |
| Západní kůl u výklenku okna `Vez_Z` | zůstává. Zakryje asi 16 cm jižního okraje výklenku (1,8 m), postava do výklenku projde. Působí to provizorně, což je záměr. | kap. 4.2 |
| Otevřená východní strana | potvrzeno: přes průlom `Vez_V` jsou hřeben, východní kůl a vzpěra vidět zdálky | kap. 4 |
| `Vez_S` a SV roh | `Vez_S` bez průlomu do tvaru U: koruna plynule (mírným obloukem) klesá od nejvyššího místa na západě k SV rohu. Tam navazuje na mírnější severní bok průlomu `Vez_V`. SV roh je z obou zdí 11,2 m. | kap. 3.1, 3.4 |

**Oproti verzi z 15. 11. 2026** (vyplynulo z přepočtu):
- západní podkladní kámen je v u = 1,50 m místo 1,40 m (zasahoval 4 cm do `Vez_Z`);
- nejmenší vůle krokví nad korunou je 11–12 cm, ne 13 cm (požadavek ≥ 5 cm platí);
- štít má vodorovný spodní lem ve výšce 11,55 m s tyčkou v lemu;
- bouřková lana jsou uvázaná za kameny na koruně `Vez_J`, ne za JZ roh (lano přes roh vedlo skrz kameny);
- zrušeno uvázání západního kůlu ke zdi `Vez_Z`, není za co;
- severní bok průlomu `Vez_V` je mírnější (`slope_r` 2,5 → 0,35): koruna stoupá od průlomu pozvolna k SV rohu (11,2 m) místo zubu 12,6–13,3 m. Z `Vez_V` ubude 223 kamenů místo 167.

**Návrh na zápis do `KNOWHOW_hrad.md` kap. 7** (zapíše stavitel):
> 17. 11. 2026 | věž dobývaná z východu: `Vez_Z` jen vedlejší škody, střed vyšší (`protect`), mezera pod přístřeškem se tím z velké části zavře, zbytek je větrání; `Vez_S` bez průlomu do tvaru U, koruna plynule klesá od západu k SV rohu a navazuje na průlom `Vez_V`; západní kůl přístřešku smí zakrýt okraj výklenku okna, když se do výklenku dá vejít | rozhodl Jirka

## 1. Zadání

- **Odkud:** Jirka.
- **Herní účel:** dočasný přístřešek pro hlídku, která přespává ve 2. patře věže. Začátek léta: teplo, sucho, občas bouřka. Obyvatelé staví obytnou budovu jinde, proto je kryt jen nad částí věže.
- **Podmínky:**
  - plátno je silné lněné, z jednoho velkého stanu, který měli;
  - voda odtéká přes jižní zeď ven;
  - střílnou ve `Vez_J` musí být dál vidět do okolí;
  - sklon plátna 22° je spodní hranice pro provizorium, nesnižovat.


## 2. Výchozí stav (ověřeno 17. 11. 2026 s terénem z levelu)

Výšky jsou v metrech od podlahy přízemí věže (`VEZ_F`, Z 3150). Rám věže podle `tools/ruin/tower_spec.py`: `u` od J-Z rohu k východu (u `Vez_J` je to zároveň `s`), `v` od J-Z rohu k severu. Strana věže `LT` = 10,995 m, vnitřek u, v = 1,25–9,745 m.

- **Podlaha 2. patra:** vrch prken 8,39 m (Z 3989).
- **Stropní trámy 2. patra:** 26 × 28 cm, východ–západ, ve v = 1,40 / 3,039 / 4,678 / 6,317 / 7,956 / 9,595 m. Průvlak je v u = 5,498 m.
- **Otvor schodů ve 2. patře** (`HATCH2`): u = 5,668–7,868 m, v = 6,447–7,826 m.
- **Střílna `Vez_J` ve 2. patře:** výklenek 8,4–10,5 m v u = 4,7–6,3 m, nadpraží do 10,85 m.
- **Okno `Vez_Z` ve 2. patře:** výklenek v = 4,6–6,4 m. Nad ním je ochrana `protect` s = 4,0–7,0 m, `min` 11,6 m.
- **Kapsy 3. patra (12,25 m)** uprostřed zdí `Vez_V` a `Vez_Z` už nestojí, hřeben se do nich uložit nedá.
- **Koruny dnes a po úpravě:** tabulky v kap. 3.1–3.3.

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

Hodnoty jsou **ověřené výpočtem** 17. 11. 2026 (viz hlavička). Výsledek závisí na `seed`; po jiné změně zdi ho stavitel přepočítá a porovná s tabulkami.

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

## 4. Cílová struktura: přístřešek (05)

### 4.1 Rám a výšky

- **Rám:** rám věže z `tower_spec.spec(T)` (`origin`, `UV`, `VV`). Výšky jsou v m od `VEZ_F` (Z 3150), absolutní Z = 3150 + 100 × h.
- **Půdorys:** pultový přístřešek nad JZ částí 2. patra, plátno u = 1,30–7,30 m, v = 0,50–4,80 m. Hřeben vede východ–západ nad stropním trámem v = 4,678 m (`BEAM_V[2]`). Okap leží na koruně `Vez_J`. Spád je k jihu, severní a východní strana jsou otevřené.
- **Sklon:** 22,6° (převýšení 1,53 m na 3,678 m). Nesnižovat pod 22°.
- **Odvodnění:** k jihu. Plátno končí 0,5 m za okapovou tyčí nad korunou `Vez_J` a voda stéká po koruně ven.

### 4.2 Nosné prvky

Všechna kulatina je čerstvá **s kůrou** (provizorní stavba, `KNOWHOW_hrad.md` kap. 2), čela a řezy `raw`.

| Prvek | Dílec | Ø (cm) | Délka, počet | Poloha (m) | Na čem leží, výška (m od VEZ_F) |
|---|---|---|---|---|---|
| Kůl rozsochy | `SM_RuinLogBark` + `SM_RuinForkHead` | 16 | 3 ks: kůl 3,72 + hlava 0,45 | v = 4,678; u = 1,40 / 5,50 / 7,15 | stojí na prknech nad trámem v = 4,678 (pata 8,39), prostřední i nad průvlakem; dno vidlice 12,56. Ramena vidlice v rovině v–h (kolmo na hřeben). |
| Hřeben | `SM_RuinLogBark` | 14 | 2 kusy: u 1,30–5,70 (4,40) a 5,30–7,40 (2,10), přeplátované nad prostředním kůlem | v = 4,678 | ve vidlicích, osa 12,63, **vrch 12,70**; svázaný lanem u každé vidlice |
| Podkladní kameny | kameny z rozvalin (knihovna zříceniny), asi 40 × 30 cm, `loose` | – | 5 míst | v = 1,0; u = 1,50 / 2,20 / 4,70 / 6,30 / 7,20 | na vnitřním líci koruny `Vez_J`, **vrch 11,05**. Měřená koruna 10,84 / 10,49 / 10,85 / 10,85 / 10,84 → výška 21 / 56 (dva kameny 26 + 30) / 20 / 20 / 21 cm. Kameny v u = 4,70 a 6,30 leží na koncích nadpraží střílny. |
| Okapová tyč | `SM_RuinLogBark` | 12 | 6,10 m | v = 1,0; u = 1,30–7,40 | na podkladních kamenech: spodek 11,05, **vrch 11,17**. Západní konec 5 cm od líce `Vez_Z`. |
| Zátěžové kameny | kameny z rozvalin asi 35 × 25 × 16 cm, `loose` | – | 4 ks | u = 1,9 / 3,6 / 5,1 / 6,8; v = 0,98 | na okapové tyči, přes lem plátna |
| Krokvové tyče | `SM_RuinPoleBark` | 10 | 5 ks po 4,66 m | u = 1,45 / 2,90 / 4,35 / 5,80 / 7,20; v = 0,50–4,80 | na vrchu okapové tyče (11,17) a hřebene (12,70), přivázané na obou. Přesah 0,5 m za okapovou tyč, 0,12 m za hřeben. Osa: h = 11,22 + 0,416 × (v − 1,0). |
| Vzpěry | `SM_RuinPoleBark` | 10 | 2 ks po 4,37 m | u = 2,60 / 4,90 | hlava pod hřebenem ze severní strany (asi 12,53, přivázaná), pata na prknech nad trámem v = 6,317 (8,39). Obě západně od otvoru schodů (u < 5,668). |

**Ovázání** (`SM_RuinLashing`, škálované na průměr): krokev × hřeben 5, krokev × okapová tyč 5, hřeben × vidlice 3, přeplátování hřebene 1, vzpěra × hřeben 2.

### 4.3 Krytina: plátno a štít

| Prvek | Tvar | Rozměr | Poloha | Uchycení |
|---|---|---|---|---|
| Plátno | `make_canvas`: okap (1,30; 0,50) → (7,30; 0,50), hřeben (1,30; 4,80) → (7,30; 4,80), výška = vrch krokví + 0,5 cm (okap 11,07, hřeben 12,86). `rafters` = (0,025; 0,267; 0,508; 0,750; 0,983), `sag` 4 cm | 6,0 × 4,66 m, asi 28 m² | – | přivázané v lemu k hřebeni a okapové tyči. Švy vedou po spádu, v geometrii se nemodelují. |
| Štít | svislý trojúhelník, `make_canvas` se zdegenerovaným čtyřúhelníkem | v = 1,91–4,60 m, výška 0 až 1,12 m, asi 1,5 m² | rovina u = 1,37 (12 cm od líce `Vez_Z`) | horní okraj zavěšený na krajní krokvi u = 1,45 (spodek krokve), **spodní lem vodorovně v 11,55**. Severní roh přivázaný k západnímu kůlu. |
| Tyčka v lemu štítu | `SM_RuinPoleBark` | Ø 5 cm, 2,6 m | v = 2,0–4,60; u = 1,37; h = 11,58 | v lemu, napíná ho |

### 4.4 Lana

| Lano | Průběh | Délka | Kotva |
|---|---|---|---|
| Bouřkové 1 | od hřebene v u = 3,40 šikmo přes plátno k okraji v u = 1,80, pak dolů ke kameni | asi 4,8 + 0,9 m | kámen asi 40 × 30 × 22 cm (`loose`) na koruně `Vez_J`, u = 1,80, v = −0,30 (koruna 10,84) |
| Bouřkové 2 | od hřebene v u = 5,20 k okraji v u = 6,90, pak ke kameni | asi 4,9 + 1,3 m | kámen na koruně `Vez_J`, u = 7,90, v = −0,30 (koruna 11,19) |

Lana jsou `SM_RuinRope` po článcích, na plátně leží 2 cm nad ním.

### 4.5 Rozměry k ověření

- **Světlá výška:**
  - pod okapovou tyčí 2,66 m;
  - pod plátnem u jižní zdi (v = 1,25) asi 3,0 m;
  - pod hřebenem 4,17 m.
- **Vůle nad korunou `Vez_J`:**
  - krokve nejméně 11–12 cm (u = 1,45 a 5,80 na konci přesahu), jinde 46–47 cm;
  - plátno nejméně 21 cm.
- **Průchody:**
  - mezi prostředním a východním kůlem 1,49 m;
  - mezi východním kůlem a `Vez_V` 2,5 m;
  - mezi vzpěrami 2,2 m;
  - od paty vzpěry u = 4,90 k otvoru schodů 0,72 m. Příchod od schodů jde východně od vzpěry, kde je volno 4,8 m.
- **Střílna `Vez_J`, 2. patro:** průhled (u = 5,5; 9,45–10,5 m) nekříží nic. Okapová tyč je nad nadpražím.
- **Okno `Vez_Z`, 2. patro:** západní kůl (v = 4,60–4,76) stojí před jižním okrajem výklenku (v = 4,60–6,40). Výklenek zůstává průchozí, rozhodl Jirka 17. 11.
- **Kontrola průniků** (17. 11. 2026, kvádry proti zřícenině a `Vez_Patra`):
  - nad 1,5 cm jen spodní kámen dvojitého podkladu v u = 2,20 (2 cm do sousedního kamene koruny). Je to `loose`, doladí se v levelu;
  - všechno ostatní je bez průniku.

## 5. Dostavba 05

- **Typ:** **nový** `canvas_shelter`. Obsahuje:
  - kulatinu (kůly s hlavou rozsochy, hřeben, okapovou tyč, krokvové tyče, vzpěry), všechno s kůrou;
  - plátno a štít jako OBJ na míru přes `make_canvas` / `write_canvas` (rozhodnutí 14. 11. 2026: tvary na míru jako OBJ);
  - lana a ovázání z knihovních dílců;
  - podkladní, zátěžové a kotevní kameny jako `loose`.
- **Název stavby:** `Vez_Pristresek`, složka `Stavby/Vez`, tag `stavba:Vez_Pristresek`.
- **Etapa:** celé `base`. Hlídka pod plachtou spí už v etapě 1 a přístřešek zůstává i v etapě 2 (co je postavené, se neskrývá).
- **Spouštěč:** `05_constructions/stavby/Vez_Pristresek.py` (kopie existujícího, `MODE` build / capture). Doporučuji i souhrnný `stavby/Vez.py` se `STAVBY = ["Vez_Patra", "Vez_Pristresek"]` a `RUIN` (část `Obvod`), podle vzoru `Palac_Kovarna.py`.
- **Sdílené rozměry:** `tools/ruin/tower_spec.py`:
  - nová funkce `pristresek(TS)` s hodnotami z kap. 4;
  - `RV` = `BEAM_V[2]`, `BRACE_V` = `BEAM_V[3]`, podlaha patra 2 × `VEZ_ST` (vrch prken 8,39 podle `Vez_Patra`);
  - spolu s `ruin_edits()` z kap. 3.4.
- **Výšky podkladních kamenů:** počítat z postavené koruny (kameny zříceniny pod půdorysem kamene, pás v = 0,85–1,15), aby vrch byl vždy 11,05. Nad 0,35 m dát dva kameny na sebe. Hodnoty v kap. 4.2 jsou očekávaný výsledek.

**Parametry pro `constructions.json`** (návrh, generuje `gen_constructions.py` z `tower_spec.pristresek`):

```
{"name": "Vez_Pristresek", "type": "canvas_shelter", "folder": "Stavby/Vez", "stage": "base",
 "origin": TS.origin, "u": TS.UV, "v": TS.VV, "z_ref": 3150, "floor_top": 8.39,
 "posts":   {"u": [1.40, 5.50, 7.15], "v": 4.678, "d": 0.16, "fork": true},
 "ridge":   {"pieces": [[1.30, 5.70], [5.30, 7.40]], "v": 4.678, "top": 12.70, "d": 0.14},
 "eave":    {"u": [1.30, 7.40], "v": 1.00, "bottom": 11.05, "d": 0.12,
             "pads_u": [1.50, 2.20, 4.70, 6.30, 7.20], "pad_band_v": [0.85, 1.15], "pad_two_over": 0.35,
             "weights_u": [1.9, 3.6, 5.1, 6.8]},
 "rafters": {"u": [1.45, 2.90, 4.35, 5.80, 7.20], "d": 0.10, "v0": 0.50, "v1": 4.80},
 "braces":  {"u": [2.60, 4.90], "foot_v": 6.317, "d": 0.10},
 "canvas":  {"u": [1.30, 7.30], "v": [0.50, 4.80], "lift": 0.005, "sag": 0.04},
 "gable":   {"u": 1.37, "v": [1.91, 4.60], "bottom": 11.55, "hem_d": 0.05},
 "ropes":   [{"ridge_u": 3.40, "edge_u": 1.80, "anchor": [1.80, -0.30]},
             {"ridge_u": 5.20, "edge_u": 6.90, "anchor": [7.90, -0.30]}],
 "bark": true, "finish": "raw"}
```

- **Ruční doladění (`loose`):** podkladní, zátěžové a kotevní kameny. Lana jen tehdy, když je typ umí vést po plátně.

## 6. Vybavení (06, mimo tuto specifikaci)

Pro furnishera, až přijde na řadu. Pod plátnem je místo asi 6,0 × 3,4 m (u = 1,30–7,30, v = 1,25–4,68) se světlou výškou 2,66–4,2 m. Hlídka tu spí: lůžka nebo houně na prknech, voda, světlo, zbraň u střílny. Nová skupina `Vez_Pristresek_Vybaveni`, polohy v `tower_spec.py` (`pristresek_vybaveni()`). Nic z toho nesmí stát v průhledu střílnou `Vez_J`, ve výklenku okna `Vez_Z` ani v průchodech z kap. 4.5.

## 7. Vazby, kolize, pořadí

- **Otvor schodů:** je 1,77 m severně od hřebene, nekoliduje. Paty vzpěr jsou západně od něj.
- **Kůly a vzpěry:** stojí nad trámy (`BEAM_V[2]`, `BEAM_V[3]`), ne ve výklencích střílen.
- **Okraj plátna:** východní okraj (u = 7,30) končí u paty východního boku průlomu `Vez_J`. Koruna pod krokví u = 7,20 je nejvýš 10,84 m.
- **`Vez_Patra`:** nic se nemění (222 dílců před i po úpravách 03).
- **Pořadí:** 03 `Obvod` → 05 `Vez_Patra` → 05 `Vez_Pristresek` → `Sut`.

## 8. Ověření

Nová sekce `run_checks.py --only vez` a náhled `preview3d.py vez`.

**Zřícenina (03):**
- `openings` a `floating` beze změny proti dnešku: kolizí 0, kamenů bez podpory 3 známé (ověřeno 17. 11. na kopii);
- nadpraží střílny `Vez_J` ve 2. patře stojí (10,5–10,85 m);
- koruna `Vez_V` nikde pod 9,1 m (v průlomu většinou 9,45 m, místy o řadu níž);
- `Vez_Patra` má po přestavbě 222 dílců a všech 12 stropních trámů;
- JV i SV roh mají z obou zdí podobnou výšku, rozdíl nejvýš 2 řady (SV roh 11,2 m);
- `Vez_S`: koruna jádra klesá od SZ rohu (12,2–12,6 m) k SV rohu (11,2 m), bez sníženiny hlubší než 2 řady pod sousedními úseky (žádný tvar U); kapsy průvlaku a střílna 2. patra stojí;
- koruna `Vez_J` v u = 1,25–7,4 m nepřesahuje v pásu v = 0,5–1,25 m 10,85 m;
- `Vez_Z`:
  - vnitřní líc ve v = 1,5–4,0 m je 10,8–11,9 m, nikde nad 12,0 m;
  - aspoň tři různé výšky řad;
- boky průlomů nemají svislý schod vyšší než 3 řady (1,05 m).

**Přístřešek (05):**
- průniky dřeva, plátna a kamenů se zříceninou a `Vez_Patra` nejvýš 1 cm. Záměrná uložení:
  - paty kůlů a vzpěr na prknech;
  - podklady a kotvy na koruně;
  - okapová tyč na podkladech;
  - krokve na hřebeni a okapové tyči;
  - hřeben ve vidlicích;
- každý kůl a každá pata vzpěry má pod sebou stropní trám (|v − BEAM_V| ≤ 0,13 m);
- okapová tyč leží aspoň na 4 podkladech, žádný podklad není vyšší než 0,6 m ani ve vzduchu;
- vůle nad korunou: krokve ≥ 5 cm, plátno ≥ 5 cm (očekáváno 11 a 21 cm);
- sklon plátna ≥ 22° (22,6°);
- světlá výška pod okapovou tyčí ≥ 2,6 m (2,66);
- plátno pokrývá ≥ 95 % půdorysu u = 1,30–7,30, v = 1,25–4,68;
- průhled střílnou `Vez_J` (u = 5,5; 9,45–10,5 m) nekříží žádný prvek;
- průchody ≥ 1,2 m podle kap. 4.5;
- štít je ≥ 5 cm od líce `Vez_Z` a jeho horní okraj leží na krajní krokvi.

**Náhled:** pohledy jako v `navrh_vez_pristresek_3d.png`, tedy zvenku od JV, od jihu, shora od SZ, zevnitř k jihu, zevnitř od SV a půdorys.

## 9. Zavržené možnosti

- **Varianta A (celá šířka 8,5 m):** plátno asi 41 m², na jeden stan příliš. Vyžadovala by průlom až k JV rohu.
- Plátno jen napnuté bez krokvových tyčí: prověsí se, drží vodu, vítr ho roztrhá.
- Hřebenové lano místo kůlů: uprostřed zdí ho není kam ukotvit.
- Hřeben v kapsách 3. patra: kapsy už nestojí.
- Koruna na 11,2 m s okapovou tyčí přímo na ní: krokvové tyče by se v přesahu opřely o korunu.
- Rovné snížení koruny (`cap` na 10,85 m): vypadá jako cílené rozebrání. Posádka by kvůli plachtě zeď nebourala, když chce věž později zastřešit.
- **Štít až ke koruně `Vez_Z`** (lichoběžník z plátna místo trojúhelníku, 17. 11. 2026): zbytečný, mezeru z velké části zavře vyšší střed `Vez_Z`. Zbytek je větrání.
- **Kůl uvázaný ke zdi `Vez_Z`:** ve zdi není za co uvázat. Rám drží hřeben, krokve zatížené na okapové tyči a dvě vzpěry.

## 10. Předpoklady a otevřené otázky

- **Předpoklad:** výšky korun jsou z dat bez ručních úprav v levelu (`manual_edits.json` byl 17. 11. 2026 prázdný).
- **Pro ladění tvaru:** škoda má být větší na vnějším líci než na vnitřním. Generátor to sám nezaručí, případně doladit ručně v levelu.
- **Otázka (suť pod východní zdí):** má pod `Vez_V` v prostoru mezi věží a `Hradba_V` ležet víc suti z průlomu? Bylo by to uvěřitelné, ale může to zúžit průchod. Rozhodne game designer podle tras hráče.
- **Přijato pro první fázi:**
  - východní bok je otevřený (`Vez_V` je nově jen 0,7–1,4 m nad podlahou patra), víc tam fouká a prší;
  - při bouřce steče část vody po koruně i dovnitř po líci zdi;
  - štěrbiny pod štítem slouží jako větrání.
- **Neřeší se:** zbytek patra dál mokne a voda protéká na 1. patro. Ohniště se nedělá, vybavení hlídky je v kap. 6.

## 11. Náčrt slovy

- **Půdorys:** čtverec 8,5 × 8,5 m.
  - Hřeben vede východ–západ ve v = 4,68 m od západní zdi po u = 7,4 m, tři kůly stojí na jednom trámu.
  - Plátno vede od hřebene k jižní zdi, pod ním je pět krokvových tyčí po spádu.
  - Ze západní strany je pod krajní krokví štít.
  - Severní polovina s otvorem schodů a JV kout zůstávají bez krytu.
- **Řez jih–sever (u střílny):**
  - jižní zeď do 10,85 m, na ní podkladní kámen 20 cm a okapová tyč (vrch 11,17 m);
  - plátno stoupá 22,6° k hřebeni ve 12,70 m, 3,68 m od okapu, a končí 0,5 m za okapovou tyčí nad korunou;
  - pod hřebenem kůl 4,17 m na trámu, od hřebene vede šikmá vzpěra k severu do podlahy.
- **Pohled na `Vez_J` od jihu:** nepravidelná mísa mezi rohy věže.
  - Uprostřed je střílna s nadpražím v koruně (10,85 m), západně od ní koruna klesá na 10,15–10,5 m.
  - Východně je koruna v 10,5 m a od u = 7,5 m pozvolna stoupá k JV rohu (11,55–11,9 m).
  - Okapová tyč leží vodorovně nad korunou na pěti podkladech, přes plátno vedou dvě lana ke kamenům na koruně.
- **Pohled na `Vez_V` od východu:**
  - JV roh je v 11,2–11,9 m, od něj koruna klesá po řadách k nejnižšímu místu 9,45 m (v = 2,75–6 m).
  - K severu stoupá pozvolna přes 9,1–10,85 m k SV rohu (11,2–11,55 m), bez zubu.
- **Pohled na `Vez_S` od severu:**
  - nejvýš je SZ roh (12,6–13,3 m, nároží s `Vez_Z`), koruna od něj mírným obloukem klesá k východu: západní polovina 12,2–12,6 m, východní 11,2–11,9 m, SV roh 11,2 m;
  - uprostřed je střílna 2. patra s nadpražím, líc je místy vylámaný o řadu až dvě.
  - Průlomem je vidět hřeben, východní kůl a vzpěra.
- **Pohled na `Vez_Z` zevnitř:**
  - koruna středu je v 10,85–11,9 m (nepravidelně po řadách), nad ní je štít s vodorovným lemem v 11,55 m;
  - mezi lemem a korunou zůstávají místy štěrbiny;
  - severně od štítu je okno 2. patra s výklenkem a před jeho jižním okrajem západní kůl.
