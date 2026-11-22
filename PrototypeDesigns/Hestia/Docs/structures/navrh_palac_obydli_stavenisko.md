---
# orchestrace
type: design
validity: valid
derived_from: "[[navrh_palac_obydli_stred]]"
alternative_to: []
updated: 2026-11-22
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
# Návrh: Palac_Obydli – etapa 1 a staveniště

## Souhrn
Návrh etapy 1 domu posádky: rozestavěná stavba, jak ji hráč vidí při prvním příchodu (začátek léta, stavba postupuje od západu k východu). Etapa 1 = sady `base` + `site`, dokončení je v sadě `final` ([[navrh_palac_obydli_stred]] kap. 0.1). Postavená verze a odchylky: [[stav_palac_obydli]].
- **Co stojí (9.1):** světnice se stěnami, kostrou krovu a pecí, síň jen u základů; dřevo surové, otvory bez zárubní.
- **Staveniště (9.2):** `Palac_Obydli_Stavenisko`, vzpěry V1–V4, žebřík a hranice materiálu S3–S5 na nádvoří před `Palac_S`.
- **Pohyb hráče (9.3)** a **kontroly etapy 1 (9.4,** `run_checks.py --only obydli`).
- **Otevřené (9.5):** kde v etapě 1 spí posádka, doplňky bez assetů.

Přesunuto z [[navrh_palac_obydli_stred]] kap. 9 (2026-11-22); číslování 9.x je zachované kvůli odkazům, 9.2a je v [[stav_palac_obydli]].

## 9. Etapa 1: rozestavěná stavba (hráč přichází poprvé)

Začátek léta, posádka dům teprve staví. Postup jde **od západu k východu**. Světnice má stěny, kostru krovu a pec, síň je u základů. Zřícenina (03) je v obou etapách stejná. Etapa 1 = sady `base` + `site`, etapa 2 = `base` + `final` (kap. 0.1). Čísla jsou změřená z dat 21. 11. 2026.

### 9.1 Co v etapě 1 stojí (sada `base`)

| Stavba | Etapa 1 (`base`) | Chybí do etapy 2 (`final`) |
|---|---|---|
| `Palac_Obydli_Kamen` | obě příčky srovnané na 1,4 m se zazděnými dveřmi; podezdívky severní stěny a příčky | – |
| `Palac_Obydli_Srub`, světnice | severní stěna s = 14,85–21,445 v plné výšce 2,5 m s otvorem okénka (s = 17,5–18,1); příčka s = 14,85 v plné výšce s otvorem dveří (n = 3,3–4,3); východní stěna (6 řad včetně pultramů) | prkenné štíty |
| `Palac_Obydli_Srub`, síň | severní stěna s = 10,93–14,85, řady 0–2 (vrch 1,16 m), mezera vchodu s = 13,4–14,4 | řada 3 a řady 4–8 severní stěny, celá západní stěna (6 řad), štít |
| `Palac_Obydli_Krov` | 5 sloupů na patních kamenech (s = 11,1 / 13,0 / 15,3 / 18,0 / 20,4); východní kus pozednice (od spoje na sloupu 15,3); východní kus vaznice (od příčky 14,85) se špalky na příčce a východní stěně; 6 krokví s = 16,255–21,3; 2 řady latí s = 16,17–21,4 | západní kusy pozednice a vaznice, špalek na západní stěně, 6 krokví s = 10,2–15,245, ostatní latě, krytina, lemování |
| `Palac_Obydli_Ohniste` | sokl, zdi pece, hliněná klenba, zídky plotny, tmavý vnitřek pece (box `V`) | sopouch, dymník, komín, plotna, pás nad ústím, poklop, vrstva uhlí pod plotnou (box `U`) |
| `Palac_Obydli_Strop`, `_Podlaha`, `_Okap`, `_Vybaveni` | nic | všechno |

- Dřevo je v obou etapách surové (`raw`), dehtuje se až případně ve třetím stavu.
- Otvory srubu jsou v etapě 1 bez zárubní, s volnými konci kulatin. Ve srubu se otvory obvykle dořezávají až po vyzdvižení stěn (předpoklad).
- Nad světnicí je mezi krokvemi vidět nebe, nad síní stojí jen dva sloupy se vzpěrami.

### 9.2 Staveniště `Palac_Obydli_Stavenisko`

```
### Palac_Obydli_Stavenisko
- Zadání: Jirka 21. 11. 2026, priorita před dokončením domu. Herní účel: hráč při prvním příchodu pozná, že dům se
  teprve staví a z čeho bude (materiál připravený na zbývající části).
- Kde: palác, střední místnost (síň a světnice) a nádvoří před Palac_S (s = 8,5–25,0; n = 10,6–13,5).
  Výšky od terénu v místě dílce.
- Výchozí stav (data 21. 11. 2026):
  - Palac_S: osa n = 9,5, tloušťka 1,4 m (vnitřní líc n = 8,8, vnější n = 10,2), nízká koruna 1,1–1,4 m;
    průlom s = 15,1–16,9, portál do západní místnosti s = 3,7–5,3, dveře do východní místnosti s = 26,45–27,55.
  - Síň: s = 10,93–14,85 (vnitřní líc Palac_pricka_1 je 10,9); n = 0,72–5,98 (severní srub do n ≈ 6,3).
  - Zápraží: n = 6,43–8,8; průchod v Palac_pricka_2 ke kovárně n = 6,9–8,5.
  - Sloupy krovu 0,20 × 0,20 m v n = 0,85, vrch 3,83 m (pozednice 4,03 m); patní kameny 0,26 × 0,36 m.
  - Terén nádvoří není změřený (předpoklad: rovný). Ověř z levelu.
- Cílová struktura (všechno sada site):
  - S1 Vzpěry sloupů bez pozednice (statika etapy 1), 4 ks, tyče s kůrou Ø 0,10 m (shape "round", d <= 11 cm
    → SM_RuinPole*). Horní konec na líci sloupu ve výšce 2,6 m, pata na terénu:
      | id | sloup | p0 (s, n, z) | p1 (s, n, z) | délka |
      | V1 | 11,1 | (11,10; 0,95; 2,6) | (11,10; 2,45; 0) | 3,00 m |
      | V2 | 11,1 | (11,20; 0,85; 2,6) | (12,70; 0,85; 0) | 3,00 m |
      | V3 | 13,0 | (13,00; 0,95; 2,6) | (13,00; 2,45; 0) | 3,00 m |
      | V4 | 13,0 | (13,10; 0,85; 2,6) | (14,40; 0,85; 0) | 2,91 m |
    Obě boční vzpěry míří k východu. Na západ od sloupu 11,1 zbývá ke stěně jen 0,1 m. Vzpěra sloupu 13,0
    k západu by se křížila s V2. Pata V4 zůstává 0,2 m před podezdívkou příčky (s = 14,625).
  - S2 Žebřík (kulisa), SM_RuinLadder 4,5 m ve světnici mezi krokvemi 18,273 a 19,282. Osa s = 18,78.
    Vrchol se opírá o severní líc pozednice (n ≈ 0,97; z ≈ 3,95), pata je na n ≈ 3,13; sklon asi 61°.
  - S3 Hranice kulatiny na srub síně, nádvoří západně od průlomu: obrys s = 8,5–14,3; n = 10,6–12,2;
    výška asi 0,65 m. Obsah = chybějící kulatina sady final ve srubu síně:
      - 4× kulatina 5,76 m Ø 0,23 (západní stěna, řady 1–4),
      - 2× hraněný pultram 5,76 × 0,22 × 0,12 m (západní stěna, řady 0 a 5),
      - 5× kulatina 4,80 m Ø 0,23 (severní stěna síně, řady 4–8),
      - 1× kulatina 3,92 m Ø 0,25 (severní stěna síně, řada 3).
    Uložení: 2 podkladky (kulatina s kůrou Ø 0,15 × 1,8 m, napříč v s = 9,3 a 13,5). Spodní vrstva:
    4× 5,76 m + 2× 4,80 m. Horní vrstva v žlábcích: 3× 4,80 + 1× 3,92 + 2 pultramy. Kulatina je loupaná (srub).
  - S4 Hranice tesaného dřeva krovu, nádvoří východně od průlomu: obrys s = 17,9–24,15; n = 10,6–11,65;
    výška asi 0,7 m. Obsah = chybějící dřevo krovu sady final:
      - 6× krokev 0,18 × 0,22 × 6,24 m (vodorovně 6,0 m, sklon 0,286),
      - 1× západní kus pozednice 0,20 × 0,20 × 5,2 m (s = 10,1–15,3),
      - 1× západní kus vaznice 0,20 × 0,24 × 4,75 m (s = 10,1–14,85).
    Uložení: 3 podkladky (Ø 0,15 × 1,2 m, s = 18,4 / 21,0 / 23,6). Spodní vrstva 4 krokve naplocho, proklady
    z latí 0,05 × 0,06. Horní vrstva 2 krokve, pozednice a vaznice.
  - S5 Hranice prken na krytinu, nádvoří za S4: dvě hranice podle délek krytiny (předání, kap. 5.1)
    (prkna 3,4 m a 3,2 m, šířka náhodně 0,22–0,30, tloušťka 0,035; K_ROOF):
      - S5a 3,4 m: s = 18,0–21,4; n = 12,0–13,45,
      - S5b 3,2 m: s = 21,8–25,0; n = 12,0–13,45.
    Počet v každé = počet prken krytiny v jedné řadě po spádu: ceil((21,7 − 9,8) / (0,26 + 0,015)) = 44.
    Až bude krytina postavená, srovnej počet s daty. Skladba na sušení: 5 prken ve vrstvě s mezerou 0,03,
    9 vrstev, mezi vrstvami proklady z latí příčně po asi 1,1 m (4 na vrstvu), 3 podkladky Ø 0,15 × 1,6 m.
    Výška asi 0,7 m. Lišty přes spáry a latě zatím ne (doplněk).
  - Úprava dřeva: všechno raw; vzpěry a podkladky s kůrou, srubová kulatina loupaná, krokve, pozednice,
    vaznice a prkna tesané.
- Úpravy 03 (zřícenina): ne.
- Dostavba 05: nová stavba Palac_Obydli_Stavenisko, typ props (zr_stavby/vybaveni.py), "stage": "site"
  na úrovni stavby (build_constructions dá sadu všem dílcům). Origin, u, v jsou rám paláce jako u ostatních
  staveb domu. Data jen přes gen_constructions.py → palac(); stavba patří do STAVBY v Palac_Obydli.py
  (za Ohniste).
- Dílce a props:
  - hotové: SM_RuinPole* / SM_RuinLog* / SM_RuinLogBark* (shape "round"), SM_RuinLadder (shape "ladder"),
  - hranoly a prkna: SM_RuinTimber / SM_RuinPlank. Předpoklad: props je umí položit jako dílec dřeva
    bez shape s rozměrem size. Ověř ve vybaveni.build_props a ue_actors; když ne, je potřeba doplnit shape
    "timber" / "plank".
  - nové tvary: žádné.
- Etapa: celá stavba je site. V etapě 2 se skryje celá (Etapa.py). Z base ani final se nic nemění.
- Sdílené rozměry: nový slovník D_SITE v palac_spec.py (vzpěry, žebřík, obrysy hranic S3–S5, podkladky,
  proklady). Délky a počty kusů S3 a S4 se počítají z dat sady final (krokve, pozednice, vaznice, segmenty
  srubu), ne ručně. Při změně final se změní i staveniště.
- Ruční doladění: loose jsou vzpěry V1–V4, žebřík a každá hranice jako celek (poloha hranice jedním
  parametrem v D_SITE). Jednotlivé kusy v hranicích nejsou loose, aby nevzniklo asi 150 actorů.
  Předpoklad: props umí položit kusy hranice jako jeden celek, jinak kusy loose: false a doladění jen přes D_SITE.
- Vazby a kolize:
  - V1–V4 se nesmí bít s patními kameny, podezdívkou příčky a výklenkem střílny s = 14 (13,35–14,65; vzpěra
    V4 jde před výklenkem v n = 0,85, líc zdi je 0,7);
  - žebřík se nesmí bít s krokvemi 18,273 a 19,282, latěmi n = 2,6 a pecí (s = 15,96–17,56);
  - hranice S3–S5 nesmí zasahovat do Palac_S (vnější líc n = 10,2) ani do sebe;
  - volné pásy na nádvoří (aspoň 1,2 m, doporučeno do n = 12,5): před průlomem s = 14,5–17,5, před
    portálem s = 3,2–5,8, před dveřmi do východní místnosti s = 25,9–28,1;
  - pořadí: 03 Palac → Kamen, Krov, Srub, Ohniste → Stavenisko → Etapa.py.
- Ověření: kap. 9.4.
- Varianty:
  - S5 A (doporučuji): celá zásoba prken (2× 44). Materiál pro střechu je zjevně připravený.
  - S5 B: jen první hromada asi 20 prken 3,4 m. Méně dílců, slabší čitelnost.
  - Kozy s rozpracovanou kulatinou a západní kus pozednice v síni (dřívější návrh) odpadají:
    · kulatina 5,7 m se na zápraží západně od vchodu (2,5 × 2,4 m) nevejde,
    · pozednice 5,2 m se v síni vejde jen podélně (n = 0,72–5,98), těsně a přes vzpěry sloupu 11,1,
    · obojí je proto na nádvoří (S3, S4); kozy jsou doplněk, až bude asset.
- Předpoklady a otevřené otázky: kap. 9.5.
- Náčrt slovy: kap. 9.6.
```

### 9.3 Pohyb hráče

- **Trasa:** nádvoří → průlom v `Palac_S` (s = 15,1–16,9) → zápraží → mezera vchodu (s = 13,4–14,4) → síň → dveře v příčce (n = 3,3–4,3) → světnice. Druhá trasa vede ze zápraží průchodem v `Palac_pricka_2` (n = 6,9–8,5) do dvorku kovárny. Všude po terénu, bez prahů.
- Zápraží zůstává v etapě 1 bez materiálu.
- Nízký srub síně (1,16 m) ani srovnané příčky (1,4 m) se nedají přejít.
- Vzpěry zabírají pás u jižní zdi síně do n = 2,45. Trasa ze vchodu ke dveřím v příčce vede po n ≥ 3,2 a zůstává volná.
- Hranice na nádvoří jsou přes nízkou `Palac_S` vidět z nádvoří i ze zápraží.

### 9.4 Kontroly etapy 1 (`run_checks.py --only obydli`, `check_obydli`)

Kontroluje se sestava `base` + `site`. Kontroly sady `final` zůstávají, jak jsou.

1. Každá krokev `base` leží na třech podporách `base` (pozednice, vaznice, vrchní trám severní stěny). Tahle kontrola už existuje.
2. Nic z `base` ani `site` nevisí ve vzduchu:
   - spodek dílce je na terénu (±3 cm), nebo leží na jiném dílci téže sady (vrstvy hranic, podkladky, proklady),
   - horní konec vzpěry se dotýká líce sloupu (≤ 2 cm).
3. Sloupy bez `base` pozednice (11,1 a 13,0) mají každý dvě vzpěry.
4. Trasy z kap. 9.3 a volné pásy na nádvoří (9.2, Vazby) jsou průchozí v šířce aspoň 1,2 m.
5. Dílce `site` se neprotínají s `base`, se zříceninou ani mezi sebou (kromě styku vrstev v hranici).
6. Počty v hranicích odpovídají chybějícím dílcům `final`: krokve 6, pozednice 1, vaznice 1, srub síně 10 + 2 pultramy.
7. V etapě 2 (`base` + `final`) není vidět žádný dílec `site`.

Vizuální kontrola v UE (Jirka): `Palac_Obydli.py`, pak `Etapa.py` s `ETAPA = 1` a pohled z nádvoří přes průlom a ze síně. Pak `ETAPA = 2` a kontrola, že staveniště zmizelo.

### 9.5 Předpoklady a otevřené otázky

- Ověřeno (21. 11. 2026): nádvoří před `Palac_S` je pod hranicemi rovné (rozdíl 0 cm) a volné, jen jeden kámen suti byl uklizen (9.2a).
- Ověřeno (21. 11. 2026): props umí hranoly a prkna (`SM_RuinTimber`, `SM_RuinPlank`). Hranici jako jeden celek posunout neumí, posouvá se v `D_SITE` (9.2a).
- Kde v etapě 1 spí posádka, návrh staveniště neřeší. Bude to samostatný task (Jirka 21. 11. 2026).
- Doplňky na později (zatím bez assetů): hlína a mech na spáry, třísky, latě a lišty, kámen nebo proutí na komín. Kozy s rozpracovanou kulatinou a pruhy kůry jsou hotové (9.2a, S6). Nářadí má hotové meshe (`axe`, `broadaxe`, `crosscut_saw`, `mallet`), jde přidat kdykoli.
- Zodpovězeno: žebřík je jen kulisa. Etapy se přepínají sadami actorů (kap. 0.1).

### 9.6 Náčrt slovy

**Půdorys (rám paláce):**
- Na jihu je `Palac_J` a pod ním řada pěti sloupů v n = 0,85.
- Západní dva sloupy (11,1 a 13,0) stojí v síni volně. Každý má vzpěru k severu (pata n = 2,45) a k východu (paty s = 12,7 a 14,4).
- Ve světnici je u jižní zdi pec (s = 15,96–17,56) a východně od ní žebřík opřený o pozednici v s = 18,78, pata asi 2,2 m od zdi.
- Severně je srubová stěna n = 6,2, za ní zápraží (bez materiálu) a `Palac_S` s průlomem s = 15,1–16,9.
- Za `Palac_S` na nádvoří:
  - západně od průlomu hranice srubové kulatiny (s = 8,5–14,3; n = 10,6–12,2),
  - východně od průlomu hranice krokví a trámů (s = 17,9–24,15; n = 10,6–11,65),
  - za ní dvě hranice prken (s = 18,0–21,4 a 21,8–25,0; n = 12,0–13,45),
  - před průlomem, portálem a dveřmi do východní místnosti zůstávají volné pásy.

**Řez napříč (po n, pohled k západu):**
- Sloup 3,83 m s pozednicí na vrchu (4,03 m) jen od s = 15,3 na východ.
- Nad síní stojí sloupy bez pozednice, vzpěra jde z 2,6 m šikmo k severu na terén 1,5 m od sloupu.
- Ve světnici krokve se sklonem 0,286 z pozednice přes vaznici (n = 4,4; 3,0 m) na srub (2,5 m), přesah do n = 6,8.
- Žebřík od pozednice dolů k severu pod sklonem 61°.
- Na nádvoří hranice vysoké 0,65–0,7 m, za nízkou `Palac_S` (1,1–1,4 m) jsou z nádvoří vidět celé, ze zápraží jejich horní část.
