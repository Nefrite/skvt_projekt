# Návrh: Vez_Pristresek – plátěný přístřešek hlídky na věži

Specifikace od architekta pro stavitele (šablona `..\AGENT_Architekt_hrad.md`, kap. 8). Stav: **návrh, nepostaveno. Vybraná varianta B** (západní 2/3 šířky) a **průlomy z dobývání ve `Vez_J` a `Vez_V`** místo rovného snížení (rozhodl Jirka 14. 11. 2026). Náčrt: `navrh_vez_pristresek.png` (schéma, ne přesný model).

**Připravenost (15. 11. 2026)** – podrobně `..\CHECKLIST_assets_navrhy.md`:
- **Hotové dílce:** kulatina a tyče s kůrou `SM_RuinLogBark`, `SM_RuinPoleBark`, hlava rozsochy `SM_RuinForkHead` (kůl s vidlicí = kůl + hlava), lano `SM_RuinRope`, ovázání `SM_RuinLashing`, kameny zříceniny. Materiály `MI_RuinBark`, `MI_RuinRope`, oboustranné plátno `MI_RuinCanvas` (vítr připravený parametrem `WindAmount`, výchozí 0).
- **Plátno a štít:** generátor prověšené plochy je hotový (`tools/meshes/mesh_textile.make_canvas`), napojení na stavbu chybí.
- **Chybí:** typ stavby `canvas_shelter`, rozšíření `tools/ruin/tower_spec.py`, úprava 03 (průlomy `Vez_V` a `Vez_J`, kap. 3).

## 1. Zadání

- **Odkud:** Jirka.
- **Herní účel:** dočasný přístřešek pro hlídku, která přespává ve 2. patře věže. Začátek léta: teplo, sucho, občas bouřka. Obyvatelé staví obytnou budovu jinde, proto je kryt jen nad částí věže.
- **Podmínky:**
  - plátno je silné lněné, z jednoho velkého stanu, který měli;
  - voda odtéká přes jižní zeď ven;
  - střílnou ve `Vez_J` musí být dál vidět do okolí;
  - sklon plátna 22° je spodní hranice pro provizorium, nesnižovat.

## 2. Výchozí stav (spočítáno z dat, 11/2026)

Výšky jsou v metrech od podlahy přízemí věže (`VEZ_F`, Z 3150). Podlaha 2. patra je v 8,4 m. Rám věže: `u` od J-Z rohu k východu (u `Vez_J` je to zároveň `s`), `v` od J-Z rohu k severu, vnitřek u, v = 1,25–9,75 m.

Koruna `Vez_J` dnes, po vrstvách zdi:

| u (m) | Vnitřní líc | Jádro | Vnější líc |
|---|---|---|---|
| 1,25–2,4 | 10,85–11,2 | 11,9 | 11,2–11,9 |
| 2,5–3,1 | 10,85 | 11,2 | 10,85 |
| 3,25–4,4 | 10,15–10,85 | 10,5 | 10,15–10,5 |
| 4,5–6,4 | 10,85–11,2 | 10,85 | 10,85–11,2 |
| 6,5–7,6 | 11,2–11,55 | 11,55–11,9 | 11,2–11,9 |
| 7,75–9,75 (k JV rohu) | 11,55–12,6 | 12,6 | 11,9–12,6 |

- Střílna `Vez_J` ve 2. patře: výklenek 8,4–10,5 m (u = 4,7–6,3 m), nadpraží do 10,85 m.
- Kapsy 3. patra (12,25 m) uprostřed zdí `Vez_V` a `Vez_Z` už nestojí, hřeben se do nich uložit nedá.
- Stropní trámy 2. patra (26 × 28 cm, východ–západ) jsou ve v = 1,4 / 3,039 / 4,678 / 6,317 / 7,956 / 9,595 m. Průvlak je v u = 5,498 m.
- Otvor schodů ve 2. patře: u = 5,67–7,87 m, v = 6,45–7,83 m.

## 3. Úpravy 03: průlomy z dobývání

**Vyžaduje úpravu 03.** Zdi se nesnižují kvůli plachtě. Jsou to starší škody z dobývání hradu, tedy součást zříceniny (stav 1650). Posádka nízkou jižní korunu jen využila pro okap. Žádná rovná koruna, žádný `cap`.

**Příběh škod (Jirka, 14. 11. 2026):** hrad se dobýval silou od východu a jihovýchodu. V oblouku naproti hradu je dost místa pro tábor a obléhací stroje.

| Zeď | Role | Změna |
|---|---|---|
| `Vez_V` (východní) | hlavní cíl střelby | **nový hlavní průlom**, nejvíc poškozená zeď věže |
| `Vez_J` (jižní) | zasažená šikmo od jihovýchodu | průlom, k JV rohu pozvolný bok |
| JV roh | nároží obou zasažených zdí | o 1,4–2,1 m níž než dnes (nově 11,2–11,9 m) |
| `Vez_Z` (západní) | vedlejší škody od východu (střely přes sníženou východní zeď) | **beze změny**, zřícený střed tomu odpovídá |
| `Vez_S` (severní) | mimo směr střelby | beze změny |

Obě změny se zapisují v `tools/ruin/gen_layout.py` u dané zdi, pak `gen_layout.py` → `ruin_layout.json`. `floor` a `min` jsou v metrech od paty zdi, ne od podlahy věže. Koruna vychází o 0,3–0,7 m níž než zadaná hodnota (rozebírání, zaokrouhlení na řady).

Hodnoty jsou **ověřené výpočtem** mimo UE na dočasné kopii `ruin_layout.json` (generátor jako knihovna, žádný soubor projektu se neměnil). Výsledek závisí na `seed`, po jiné změně zdi ho stavitel přepočítá.

### 3.1 `Vez_V`: hlavní průlom

- **Zápis v datech:**
  - `breaches`: `{"s0": 2.5, "s1": 6.5, "floor": 10.3, "slope_l": 0.7, "slope_r": 2.5}` (hlavní průlom, jižní bok pozvolný k JV rohu, severní strmý),
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
| 6,25–6,5 | 10,5–10,85 | 9,8–10,5 | 1–2 řady |
| 6,75–9,75 | 10,5–13,3 | 10,5–12,6 | 0–2 řady |
| 10–11 (SV roh) | 13,3–14,35 | 12,6–13,3 | 2–3 řady (vedlejší efekt výpočtu) |

- **Celkem ubude** asi 166 kamenů, 27 m³ (`Vez_V` má dnes 2 141 kamenů).
- **Tvar:** široký průlom s nejnižším místem jižně od středu. Od něj koruna stoupá pozvolna k JV rohu a strměji k severu, kde zůstává dnešní tvar.
- **Nejnižší koruna je 9,45 m**, tedy 1,05 m nad podlahou 2. patra. Postava ji nepřejde (limit zídky je 0,5 m), ale přes ni vidí na východ.
- **Střílna 2. patra zaniká.** Nadpraží chybí už dnes. Z výklenku zůstane otevřený výřez s parapetem 0,7–1,05 m.
- **Kapsy trámů 2. patra (8,05–8,4 m) zůstávají**, nad nimi je všude aspoň 0,7 m zdiva. Ověřeno: `Vez_Patra` má po změně stejných 222 dílců včetně všech 12 trámů.
- **SV roh** vychází o 0,7–1,0 m níž. Není to záměr. Pokud má zůstat, přidat `protect` pro s = 9,75–11 a doladit `min`.
- **Suť:** `Vez_V` má `rubble` `out`. Generátor počet kamenů suti podle objemu průlomu nezvyšuje (22–24 kamenů před i po). Po dobývání by pod východní zdí bylo suti víc, viz otevřené otázky.

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

- **Celkem ubude** asi 105 kamenů, 23 m³ (`Vez_J` má dnes 2 138 kamenů).
- **Tvar:** nepravidelná mísa. Dno je 1,75–2,45 m nad podlahou patra. Východní bok stoupá pozvolna (asi 1,4 m výšky na 2,5 m délky) k JV rohu, který je společně s `Vez_V` snížený na 11,2–11,9 m.
- **Co zůstává:** nadpraží střílny (10,5–10,85 m) a JZ roh.
- **Podmínka pro přístřešek:** v pásu v = 0,5–1,25 m (vnitřní líc a kraj jádra) nesmí koruna v u = 1,25–7,4 m přesáhnout 10,85 m. Vnější líc může být výš.
- **Suť:** `Vez_J` má `rubble` `out`, kameny spadly ze skály.

### 3.3 Společné

- **Přestavět:** část `Obvod` (obě zdi najednou), pak 05 `Vez_Patra`.
- **Ruční úpravy:** průlomy změní ID kamenů `Vez_J` a `Vez_V`. Ruční úpravy těchto zdí v `manual_edits.json` (pokud nějaké jsou) se po přestavbě nemusí trefit, stavitel to zkontroluje.

## 4. Cílová struktura

Pultový přístřešek se spádem k jihu nad JZ částí patra (u = 1,25–7,3 m, v = 1,25–4,68 m). Hřeben vede východ–západ nad trámem v = 4,678 m, okap leží na koruně `Vez_J`. Severní a východní strana jsou otevřené.

| Prvek | Průřez | Délka / počet | Poloha | Na čem leží |
|---|---|---|---|---|
| Kůl s vidlicí (rozsocha) | kulatina Ø 16 cm | 4,15 m, 3 ks | v = 4,678 m; u = 1,40 / 5,50 / 7,15 m | na stropním trámu v = 4,678 m (přes prkna), prostřední nad průvlakem |
| Hřeben | kulatina Ø 14 cm | 4,4 m + 2,0 m, přeplátované nad prostředním kůlem | u = 1,3–7,4 m, vrch 12,70 m (4,30 m nad podlahou patra) | ve vidlicích kůlů, svázaný lanem |
| Podkladní kameny | ploché kameny z rozvalin, asi 40 × 30 cm, výška podle koruny: 20 cm na 10,85 m, 55 cm (dva na sobě) na 10,5 m | 5 míst | v = 1,0 m; u ≈ 1,35 / 2,2 / 4,7 / 6,3 / 7,2 m | na vnitřním líci koruny `Vez_J`, vrch vždy 11,05 m |
| Okapová tyč | kulatina Ø 12 cm | 6,1 m | v = 1,0 m, u = 1,3–7,4 m, vrch 11,17 m | na podkladních kamenech, zatížená dalšími kameny |
| Krokvové tyče | kulatina Ø 10 cm | 4,6 m, 5 ks | u = 1,45 / 2,9 / 4,35 / 5,8 / 7,2 m, přesah 0,5 m za okapovou tyč | hřeben a okapová tyč, přivázané |
| Vzpěry | kulatina Ø 10 cm | asi 4,5 m, 2 ks | od hřebene k severu, u = 2,6 a 4,9 m | pata na podlaze nad trámem v = 6,317 m |
| Plátno | lněné, švy po spádu | 6,2 × 4,7 m, asi 29 m² | na krokvových tyčích | přivázané k hřebeni a okapové tyči |
| Štít | plátno (štítový díl stanu) | trojúhelník nad `Vez_Z` | západní bok | zavěšený na krajní krokvové tyči |
| Bouřková lana | konopné lano | 2 ks přes plátno | k JZ rohu a k východnímu boku průlomu | uvázaná za kameny |

- **Sklon:** 22,6° (převýšení 1,53 m na 3,68 m). Nesnižovat pod 22°.
- **Odvodnění:** k jihu. Plátno končí nad korunou `Vez_J` asi 0,5 m za okapovou tyčí, voda stéká po koruně ven. Vůle mezi krokvovou tyčí a korunou je na konci přesahu nejméně 13 cm.
- **Světlá výška:** pod okapovou tyčí 2,65 m. Koruna zdi je 1,75–2,45 m nad podlahou patra, mezi korunou a tyčí zůstávají průhledy 0,2–0,9 m.
- **Kůly:** západní kůl je přivázaný ke zdi `Vez_Z` a stojí těsně u jižního ostění výklenku okna. Výklenek zůstává volný. Východní kůl stojí volně na trámu.
- **Úprava dřeva:** čerstvá kulatina **s kůrou** pro všechno dřevo (kůly, hřeben, okapová tyč, krokvové tyče, vzpěry); přiřazení podle `CHECKLIST_assets_navrhy.md` kap. 2.1, čeká na potvrzení. Řezy a čela `raw`.
- **Otvory:** žádné.

## 5. Dostavba 05

- **Typ:** **nový** (pracovně `canvas_shelter`): kulatina, prověšená plocha plátna jako statický mesh, lana. Oboustranný materiál plátna už existuje (`MI_RuinCanvas`).
- **Název stavby:** `Vez_Pristresek`, složka `Stavby/Vez`.
- **Klíčové parametry:**
  - `u0` 1.25, `u1` 7.3 (rozsah plátna),
  - `ridge_v` 4.678, `ridge_top` 12.70, `posts_u` [1.40, 5.50, 7.15],
  - `eave_v` 1.0, `eave_top` 11.17, `pads_u` [1.35, 2.2, 4.7, 6.3, 7.2], výška podkladu se dopočítá z postavené koruny (vrch 11,05 m),
  - `rafters_u` [1.45, 2.9, 4.35, 5.8, 7.2], `overhang` 0.5,
  - `braces_u` [2.6, 4.9], `braces_v` 6.317,
  - průměry: `post_d` 0.16, `ridge_d` 0.14, `eave_d` 0.12, `rafter_d` 0.10, `brace_d` 0.10,
  - `finish` `raw`.
- **Sdílené rozměry:** `tools/ruin/tower_spec.py` (rozsah a hloubka průlomů `Vez_J` a `Vez_V`, výška okapu, `ridge_v` = poloha trámu, polohy kůlů). Sdílí je 03 i 05.
- **Ruční doladění (`loose`):** podkladní a zátěžové kameny na koruně, případně lana.

## 6. Vazby, kolize, pořadí

- Otvor schodů je 1,6 m severně od hřebene, nekoliduje.
- Paty vzpěr (v = 6,317 m) jsou západně od otvoru schodů (u < 5,67 m).
- Kůly a vzpěry nesmí stát ve výklencích střílen a okna.
- Východní okraj plátna (u = 7,3 m) končí u paty východního boku průlomu `Vez_J`. Poslední krokvová tyč (u = 7,2 m) musí mít pod sebou korunu nejvýš 10,85 m.
- **Pořadí:** 03 `Obvod` → 05 `Vez_Patra` → 05 `Vez_Pristresek`.

## 7. Ověření

- `tools/checks/run_checks.py` na `Vez_J` a `Vez_V`: nadpraží střílny `Vez_J` stojí, žádné kameny bez podpory.
- Koruna `Vez_V` není nikde pod 9,45 m (mimo bývalý výklenek střílny, tam jádro aspoň 9,1 m).
- `Vez_Patra` má po přestavbě všech 12 stropních trámů (žádný nevypadl kvůli spadlé kapse).
- JV roh má z obou zdí podobnou výšku (rozdíl nejvýš 2 řady).
- Koruna `Vez_J` v u = 1,25–7,4 m není v pásu v = 0,5–1,25 m nikde nad 10,85 m.
- Koruna není rovná: v u = 1,25–7,4 m má aspoň tři různé výšky řad a boky průlomů `Vez_J` a `Vez_V` nemají svislý schod vyšší než 3 řady (1,05 m).
- Každý kůl a každá pata vzpěry má pod sebou stropní trám.
- Okapová tyč leží na podkladních kamenech nejméně ve čtyřech místech, žádný podklad není ve vzduchu ani vyšší než 60 cm.
- Krokvové tyče ani plátno se nedotýkají koruny zdi (vůle aspoň 5 cm).
- Sklon plátna je aspoň 22°.
- Světlá výška pod okapovou tyčí je aspoň 2,6 m.
- Přímka pohledu střílnou `Vez_J` plátno ani tyče nekříží.
- Plátno pokrývá aspoň 95 % půdorysu u = 1,25–7,3 m, v = 1,25–4,68 m.
- Průchod kolem prostředního a východního kůlu je aspoň 1,2 m.
- Náhled: `tools/checks/preview3d.py`, řez `tools/constructions/check_tower.py`.

## 8. Zavržené možnosti

- **Varianta A (celá šířka 8,5 m):** plátno asi 41 m², na jeden stan příliš. Vyžadovala by průlom až k JV rohu.
- Plátno jen napnuté bez krokvových tyčí: prověsí se, drží vodu, vítr ho roztrhá.
- Hřebenové lano místo kůlů: uprostřed zdí ho není kam ukotvit.
- Hřeben v kapsách 3. patra: kapsy už nestojí.
- Koruna na 11,2 m s okapovou tyčí přímo na ní: krokvové tyče by se v přesahu opřely o korunu.
- Rovné snížení koruny (`cap` na 10,85 m): vypadá jako cílené rozebrání. Posádka by kvůli plachtě zeď nebourala, když chce věž později zastřešit.

## 9. Předpoklady a otevřené otázky

- **Předpoklad:** výšky korun jsou z dat bez ručních úprav v levelu po posledním capture.
- **Pro ladění tvaru:** škoda má být větší na vnějším líci než na vnitřním. Generátor to sám nezaručí, případně doladit ručně v levelu.
- **Otázka (suť pod východní zdí):** má pod `Vez_V` v prostoru mezi věží a `Hradba_V` ležet víc suti z průlomu? Bylo by to uvěřitelné, ale může to zúžit průchod. Rozhodne game designer podle tras hráče.
- **Otázka (přístřešek a vítr):** východní zeď je nově jen 1,05–1,4 m vysoká, přístřešek má východní bok otevřený. Od východu do něj víc fouká a prší. Pro první fázi se to přijímá, případně později zástěna z prken nebo zbytku plátna.
- **Předpoklad:** plátno končí nad korunou zdi. Při bouřce část vody steče po koruně i dovnitř po líci zdi. Pro první fázi se to přijímá.
- **Neřeší se:** zbytek patra dál mokne a voda protéká na 1. patro. Ohniště a vybavení hlídky nejsou součástí návrhu.

## 10. Náčrt slovy

- **Půdorys:** čtverec 8,5 × 8,5 m. Hřeben východ–západ ve v = 4,68 m od západní zdi po u = 7,4 m, tři kůly na jednom trámu. Plátno od hřebene k jižní zdi, pět krokvových tyčí po spádu. Severní polovina s otvorem schodů a JV kout zůstávají bez krytu.
- **Řez jih–sever (u střílny):** jižní zeď do 10,85 m, na ní podkladní kámen 20 cm a okapová tyč (vrch 11,17 m). Plátno stoupá 22,6° k hřebeni ve 12,70 m, 3,68 m od okapu. Pod hřebenem kůl 4,15 m na trámu, od hřebene šikmá vzpěra k severu do podlahy.
- **Pohled na `Vez_J` od jihu:** nepravidelná mísa mezi rohy věže. Uprostřed střílna s nadpražím v koruně (10,85 m), západně od ní koruna klesá na 10,15–10,5 m, východně je 10,5 m a od u = 7,5 m stoupá pozvolna k JV rohu (11,55–11,9 m). Okapová tyč leží vodorovně nad korunou na pěti podkladech.
- **Pohled na `Vez_V` od východu:** JV roh v 11,2–11,9 m, od něj koruna klesá po řadách k nejnižšímu místu 9,45 m (v = 2,75–6 m), kde býval výklenek střílny. K severu stoupá strměji na 10,5–11,2 m a dál k SV rohu (12,6–13,3 m), který je nejvyšším místem zdi.
