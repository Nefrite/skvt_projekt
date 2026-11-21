---
# orchestrace
type: checklist
validity: valid
updated: 2026-11-21
# hra
domain: structures
entity: "[[Lapikus]]"
---
# Checklist: assety a podklady pro nové návrhy (11/2026)

Seznam všeho, co je potřeba **namodelovat, vygenerovat nebo připravit** pro návrhy ze 14. 11. 2026. Sestaveno z `new_designs/navrh_*.md` a ze stávajícího stavu kódu (`zrlib/config.py`, `03_ruin/blocks/gen_stones.py`, `05_constructions/build_constructions.py`). Stav: **verze 3 (21. 11. 2026).** Knihovní meshe kulatiny, textilu, výpletu a props kovárny a domu jsou hotové (☑). Zbývají props stanu, guesthouse a staveniště, část materiálů a typy staveb v 05. Pořadí prací je v kap. 11.

## 0. Zdroje a rozhodnutí

| Návrh | Stav | Etapa |
|---|---|---|
| [[navrh_vez_pristresek]] | **specifikace pro stavitele (17. 11. 2026)**, nepostaveno: varianta B, průlomy `Vez_J` + `Vez_V`, vyšší střed `Vez_Z`, plynulá `Vez_S` | 1 i 2 (sada `base`) |
| [[navrh_palac_obydli_stred]] (+ `_etapa1.png`) | dům v prostřední místnosti; **staví se** (16. 11. 2026: plán po etapách v kap. 0, kamenné části hotové) | 1 = rozestavěno, 2 = hotovo |
| [[navrh_palac_kovarna]] | vybraný návrh, **staví se** (15. 11. 2026: úprava 03, kostra přístřešku a výheň v koutě hotové; přehled v kap. 0 návrhu) | 1 i 2 |
| [[navrh_brana_straz]] | rozestavěno (podesta 16. 11. 2026, kap. 0) | otevřené |
| [[navrh_nadvori_stan]] | **bude** (Jirka 21. 11. 2026), nepostaveno | jen 1 |

**Rozhodnuto (Jirka, 14. 11. 2026):**
- **Kulatina s kůrou i bez kůry**, podle stavby (kap. 2.1).
- **Props vlastní**, ve stylu hradu (kap. 5).
- **Stan** se drží v seznamu, položky jsou označené ⛺. **21. 11. 2026: stan bude**, ⛺ už neznamená nízkou prioritu.
- **Generátor meshí** se rozdělí podle typu materiálu, případně jeden společný s novým názvem (kap. 3).

Značky: ☑ hotovo · ◐ rozpracováno (část hotová, zbytek přijde se stavbou) · 🆕 nový asset · ♻ existuje, jen použít / rozšířit · ⛺ jen pro stan · ❓ čeká na rozhodnutí · 🧩 skládá se z dílců · ✋ modeluje se jako samostatný tvar.

---

## 1. Co už existuje (nemodelovat)

- ♻ Kameny zříceniny: `SM_RuinStone_R*`, `SM_RuinStone_W_*`, `SM_RuinDressed_*`, `SM_RuinAshlar`. Použití: podkladní a patní kameny, podezdívky, výheň, základ ohniště, vyrovnávací řady brány, hromada kamene.
- ♻ Hraněné dřevo: `SM_RuinTimber_A–C`, `SM_RuinPost_A–C`, `SM_RuinPlank_A–C`. Použití: sloupy 18–20 cm, pozednice, vaznice, krokve 18 × 22, trámky stropu, latě, prkna krytiny a podlah, lišty, lemování, prkenné štíty.
- ♻ Materiály dřeva: `MI_RuinWood` (`raw`), `_Tar`, `_Oil`, `_Blood`, `_Old`.
- ♻ Materiály kamene: `MI_RuinFace`, `_Core` (i jako malta), `_Frame`, `_Crown`.

**Chybí kulatina.** Všechny stávající dřevěné meshe mají obdélníkový průřez.

---

## 2. Kulatina a tyče

### 2.1 S kůrou, nebo bez kůry (návrh přiřazení, ❓ potvrdit)

Pravidlo: **provizorní a rychlé stavby a materiál, který ještě nikdo nezpracoval = s kůrou.** **Nosné a trvalé dřevo = loupané**, protože pod kůrou dřevo hnije a lezou do něj brouci.

| Stavba / použití                    | S kůrou                                                         | Bez kůry                                          |
| ----------------------------------- | --------------------------------------------------------------- | ------------------------------------------------- |
| `Vez_Pristresek`                    | kůly s vidlicí, hřeben, okapová tyč, krokvové tyče, vzpěry      | –                                                 |
| `Brana_Straz_Kryty`                 | kůly palisády (zašpičatělá špička je holá), ráhna               | –                                                 |
| `Brana_Straz_Podesta`               | –                                                               | trámy Ø 22 (nosné, na 5,4 m)                      |
| `Brana_Straz` zábradlí              | sloupky a tyče                                                  |                                                   |
| `Brana_Straz_Pristresek`            | sloupky, vaznice, krokvičky, přítlačné tyče                     | –                                                 |
| `Brana_Zataras`                     | kmen                                                            | ramena (oloupané a zašpičatělé)                   |
| `Palac_Obydli_Srub`                 | –                                                               | srub Ø 22 (loupaný, spáry vymazané)               |
| `Palac_Obydli` staveniště (etapa 1) | kulatina na hromadě (ještě neloupaná), dočasné vzpěry, nohy koz | rozpracovaná kulatina na kozách (napůl loupaná ❓) |
| `Palac_Kovarna_Pristresek`          | –                                                               | krokve Ø 16                                       |
| žlaby a svody (dům, kovárna)        | vnější strana                                                   | vydlabaný vnitřek                                 |
| vidlice žlabů                       | ano                                                             | –                                                 |
| páka měchů                          | –                                                               | ano (ohmataná)                                    |
| ⛺ `Nadvori_Stan`                    | stojky, hřeben, klády lůžek, tyče lůžek                         | kolíky (osekané)                                  |
| ⛺ stříška stanu                     | vidlice, tyče, krokvičky                                        | –                                                 |

### 2.2 Meshe

Stejný princip jako `SM_RuinTimber`: nominální délka 100 cm, délka a průměr přes scale, varianty A–C, verze v `STONE_MESH_VERSION`, nominál ve `WOOD_NOMINAL`.

- **Dva materiálové sloty u každé kulatiny:** plášť (kůra, nebo loupané dřevo) a čela (letokruhy, světlejší). Zašpičatělé a osekané konce jsou vždy holé dřevo.
- **Kulatina s kůrou má vlastní tvar:** hrubší obrys (šupiny), místy odloupnutá kůra, kde je vidět dřevo (třetí oblast materiálu, nebo maska ve vertex color ❓).

| ☐ | Asset | Popis | Rozsah | Použití |
|---|---|---|---|---|
| ☑ | 🆕 `SM_RuinLog_A–C` | loupaná kulatina: nepravidelný kruh, sbíhavost, suky, stopy po loupání | nominál Ø 20 cm (Ø 12–24) | srub, trámy podesty, krokve kovárny, ramena jezdce |
| ☑ | 🆕 `SM_RuinLogBark_A–C` | kulatina s kůrou, místa odloupnutá | nominál Ø 20 cm (Ø 12–24) | kmen jezdce, hřeben a okapová tyč věže, hromada kulatiny |
| ☑ | 🆕 `SM_RuinPole_A–C` | tenká tyč, výraznější prohnutí | nominál Ø 8 cm (Ø 5–10) | zábradlí, páka měchů, kolíky ⛺ |
| ☑ | 🆕 `SM_RuinPoleBark_A–C` | tenká tyč s kůrou | nominál Ø 8 cm (Ø 5–10) | krokvové tyče, vzpěry, ráhna, krokvičky, přítlačné tyče, stojky stanu ⛺ |
| ☑ | 🆕 `SM_RuinForkHead_A–B` | hlava rozsochy s kůrou (vidlice), nasadí se na kůl `SM_RuinLogBark` / `SM_RuinPoleBark` | Ø 8–16 cm, délka 1,4–4,2 m | kůly přístřešku věže, vidlice žlabů, vidlice stříšky ⛺ |
| ☑ | 🆕 `SM_RuinStake_A–C` | kůl s kůrou, nahoře holá špička | Ø 18–22 cm, délka 1,3–3,0 m | kryty brány |
| ☑ | 🆕 `SM_RuinStakeSmall_A–B` | loupaný kůl, zašpičatělý na obou koncích | Ø 7 cm × 1,6 m (kolík 30 cm) | ramena jezdce, kolíky stanu ⛺ |
| ☑ | 🆕 `SM_RuinGutter_A–B` | vydlabaný půlkmen, loupaný | Ø 20 cm, délka po 100 cm | žlaby a svody |
| ☑ | 🆕 `SM_RuinGutterBark_A–B` | vydlabaný půlkmen, kůra zvenku | Ø 20 cm, délka po 100 cm | žlaby a svody |
| ☐ | ❓ zářez srubu (nároží) | kulatiny se v nárožích křižují: řešit průnikem (bez meshe), nebo mesh se zářezem | – | srub obydlí |

- ☑ Napojení (14. 11. 2026): `ROUND_MESHES`, `ROUND_SHAPES`, `SLOT_MI` v `zrlib/config.py`, `Stone.shape` + `Stone.bark`, sloty materiálů v `zrlib/ue_assets.apply_materials`. Ukázka `tools/meshes/Ukazka_Meshe.py` (dřív `Ukazka_Kulatina.py`), náhled `05_constructions/Kulatina_meshe_nahled.png`. **Neověřeno v UE.**
- Rozhodnuto při stavbě: rozsocha je samostatná hlava (`SM_RuinForkHead`), ne celý kůl, aby se vidlice nenatahovala s délkou. Sloty jsou tři (`Wood`, `EndGrain`, `Bark`), odloupnutá místa jsou slot `Wood`.

---

## 3. Generátor meshí: rozdělení skriptu

**Původně:** `03_ruin/blocks/gen_stones.py` generoval kameny i dřevo. Výstup byl `stones/*.obj` vedle skriptu a build zříceniny ho importoval do `/Game/Skvt/Lapikus/Ruin/Stones`. Používá ho i 05, takže umístění pod `03_ruin` nesedělo.

**Návrh ❓ (spojuje obě tvé možnosti):** jeden společný vstup a moduly podle materiálu.

```
tools/meshes/
  gen_meshes.py        vstup: python gen_meshes.py <out> [stone wood bark textile wattle props]
  mesh_common.py       noise, grid, waves, write_obj, UV v metrech
  mesh_stone.py        lomove, zvetrale, opracovane kameny, kvadr (presun z gen_stones)
  mesh_wood.py         tram, sloup, prkno (presun) + kulatina, tyc, rozsocha, kul, zlab
  mesh_bark.py         kura: plast kulatiny s kurou, pasy kury na strechy
  mesh_wattle.py       vyplet z prouti, dymnik, komin (prouti + mazanina)
  mesh_textile.py      knihovni dily: uzel, smotane lano (platno a lana na miru jsou v zr_stavby)
  mesh_props.py        vlastni props (kap. 5), slozene z funkci ostatnich modulu
```

- ☑ Rozhodnuto: jeden vstup `tools/meshes/gen_meshes.py` + moduly podle materiálu (14. 11. 2026). **Hotové:** `mesh_common.py`, `mesh_stone.py`, `mesh_wood.py`. Další moduly (`mesh_bark`, `mesh_wattle`, `mesh_textile`, `mesh_props`) přibydou s novými tvary.
- ☑ Výstupní složky podle kategorie (14. 11. 2026): OBJ v `meshes/<kategorie>/` v kořeni (`stone`, `wood`), v UE `Ruin/Stones`, `Ruin/Wood` (`MESH_DIRS` v `zrlib/config.py`). Dřevo přesunuté do `Ruin/Wood`, ověřeno v UE (oba buildy, redirectory smazané). Další kategorie = modul + `CATEGORIES` + `MESH_DIRS` + `_needed_meshes`.
- ☑ **Přesun beze změny tvaru:** stávající kameny a dřevo musí po refaktoringu vyjít bit po bitu stejné (md5 OBJ před a po, případně `fingerprint.py`). Teprve potom přidávat nové tvary. **Ověřeno:** všech 42 OBJ shodných s repem (md5), stejný výpis.
- ☑ Starý `gen_stones.py` nechat jako tenký wrapper (volá `gen_meshes.py stone wood`), aby platily návody v [[03_ruin]]. Nebo opravit dokumentaci.
- ☑ Aktualizovat [[03_ruin]], [[05_constructions]], `zrlib/config.py` (komentář), [[README_PROJEKT]] a hint ve [[Zricenina_03_ruin_stav]] (zjednodušení sítě kamenů).

**Tvary „na míru“** (plátno, lana, výplet konkrétní stěny, plachta stanu) nejsou knihovní meshe, závisí na poloze dílců stavby. ❓ Rozhodnout, kde vznikají:
- (a) při `gen_constructions.py` jako OBJ pro každou stavbu a pak import do UE,
- (b) přímo v UE přes Dynamic Mesh / Geometry Script.

---

## 4. Ostatní procedurální meshe

| ☐ | Asset | Popis | Druh | Použití |
|---|---|---|---|---|
| ☑ | 🆕 plátno přístřešku | prověšená plocha mezi krokvovými tyčemi, oboustranná | na míru | `Vez_Pristresek` (6,0 × 4,66 m, rohy a `rafters` v návrhu kap. 4.3). **Generátor hotový:** `mesh_textile.make_canvas` (rohy, polohy tyčí, prověšení) + `write_canvas` → OBJ; ukázka `SM_RuinCanvasSample_A`. **Hotovo 17. 11. 2026:** `SM_RuinCanvasVez_A` (`mesh_textile.canvas_vez`, OBJ + `.json` se středem a rozměrem). |
| ☑ | 🆕 štít plátna | trojúhelník zavěšený na krajní tyči | na míru | `Vez_Pristresek` (nad `Vez_Z`, spodní lem vodorovně v 11,55 m s tyčkou Ø 5 cm; návrh kap. 4.3); stejný `make_canvas` (zdegenerovaný čtyřúhelník); **hotovo 17. 11. 2026:** `SM_RuinCanvasVezGable_A` |
| ☑ | 🆕 `SM_RuinRope_A–B` | článek lana 100 cm, Ø 1,5 cm, 3 prameny; prověšené lano = řetěz článků podél řetězovky (počítá stavba) | knihovní | bouřková lana věže, vazby hřebene, šňůry stanu ⛺ |
| ☑ | 🆕 `SM_RuinLashing_A–B` | ovázání na křížení tyčí (zavity kolem tyče Ø 8 cm, škáluje se s tyčí) | knihovní | přivázání krokví, ráhen, vidlic |
| ☑ | 🆕 `SM_RuinBarkStrip_A–C` | prohnutý pás kůry 160 × 70 cm, hrubá strana nahoru, roztřepené okraje, spodek světlé lýko | knihovní | přístřešek brány, stříška stanu ⛺ |
| ☑ | 🆕 `SM_RuinWattlePanel_A–C` | dílec proutěné stěny s mazaninou 100 × 100 × 8 cm, rovné okraje → skládá se do libovolné stěny; ~10 % odhaleného vypletu | knihovní | západní stěna kovárny 5,7 × 1,9 m |
| ☑ | 🆕 `SM_RuinSmokeHood_A–B` | dymník: zužující se koš z proutí s hlínou 140 × 120 → 50 × 50, výška 100 cm (škáluje se) | knihovní | ohniště obydlí, výheň kovárny |
| ☑ | 🆕 `SM_RuinChimney_A–B` | komín z proutí a hlíny 60 × 60 cm, výška 100 cm (škáluje se) | knihovní | obydlí (vrch 5,3 m), kovárna (vrch 5,5 m) |
| ◐ | 🆕 výplň spár srubu | tmavší pás mechu s hlínou mezi kulatinami | na míru | srub obydlí; **materiál hotový** (`MI_RuinChinking`), geometrie přijde s typem `log_wall` |
| ☑ | ⛺ 🆕 plachta stanu do A | jeden díl přes hřeben, 2 štíty, odhrnutá chlopeň | na míru | `Nadvori_Stan` → `SM_RuinCanvasTent_A` (kap. 6.5, hotovo 21. 11. 2026, neověřeno v UE) |

---

## 5. Materiály (`zrlib/config.py` → `MAT_LOOK`, `WOOD_FINISH`, textury)

| ☐   | Materiál                                                             | Vlastnosti                                                                             | Použití                                       |
| --- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------- |
| ☑   | 🆕 `MI_RuinBark`                                                     | smrková kůra, tmavě hnědá, hrubá; vnitřní strana pásu světlejší                        | kulatina s kůrou, pásy kůry                   |
| ☑   | 🆕 `MI_RuinWood_Peeled` (finish `peeled`)                            | čerstvě loupané dřevo: světlé, nažloutlé, stopy po loupáku                             | loupaná kulatina v etapě 1                    |
| ☑   | 🆕 `MI_RuinWood_EndGrain`                                            | čela s letokruhy, světlejší, s prasklinami                                             | čela všech kulatin                            |
| ☑   | 🆕 `MI_RuinCanvas`                                                   | lněné plátno, **oboustranné**, zašedlé, místy záplaty a skvrny; ❓ pohyb ve větru (WPO) | přístřešek věže, stan ⛺                       |
| ☑   | 🆕 `MI_RuinRope`                                                     | konopné lano, světle béžové, vláknité                                                  | lana, ovázání, šňůry                          |
| ☑   | 🆕 `MI_RuinDaub`                                                     | mazanina: hlína na proutí, praskliny                                                   | stěna kovárny, dymníky, komíny                |
| ☑   | 🆕 `MI_RuinWattle`                                                   | samotné proutí                                                                         | okraje výpletu, koš na staveništi             |
| ☑   | 🆕 `MI_RuinChinking`                                                 | mech s hlínou ve spárách srubu                                                         | srub obydlí                                   |
| ☐   | 🆕 `MI_RuinSoot` (nebo maska ve stávajících MI)                      | saze nad výhní a ohništěm, na stěně věže a pod komínem                                 | kovárna, obydlí                               |
| ☐   | 🆕 udusaná hlína                                                     | podlaha síně, kovárny a dvorku: ❓ decal, deska, nebo vrstva landscapu                  | síň, kovárna                                  |
| ☐   | 🆕 třísky a kůra na zemi                                             | decal                                                                                  | staveniště etapy 1                            |
| ☑   | 🆕 kov (kované železo) `MI_RuinIron` s patinou rzi + `MI_RuinIronClean` bez rzi                                               | tmavé, okuje; rez jen tlumeně hnědá                                                      | bez rzi: kovadlina, nářadí; s rzí: svěrák, pruty, obruče, osy |
| ☑   | 🆕 kůže `MI_RuinLeather`                                                              | tmavá, popraskaná                                                                      | měchy                                         |
| ☑   | 🆕 pískovec `MI_RuinSandstone` (StarterContent) (nebo ♻ `MI_RuinFrame` se `T_Rock_Sandstone`) |                                                                                        | brusný kotouč                                 |
| ◐   | 🆕 textil hrubý (houně), sláma / kapradí → `MI_RuinWool`, `MI_RuinStraw` (kapradí zatím ne)                             |                                                                                        | lůžka (dům, stan ⛺)                           |
| ☐   | ♻ `MI_RuinWood` `raw`, `_Tar`, `_Old`                                | beze změny                                                                             | krov, krytina, prkna, vybavení                |

- ☐ Přepínání podle etapy: loupaná kulatina srubu v etapě 1 `peeled`, v etapě 2 ❓ `peeled`, nebo `raw` (už ztmavlá)? Krov `raw` → `tar`. Řeší kód přes `ETAPA`, meshe zůstávají stejné.

---

## 6. Props – vlastní modely ve stylu hradu

**Zásady stylu:**
- stejné materiály jako zřícenina a dostavby (`MI_Ruin*`), stejné zvětrání shora (`MAT_TOP`) a měřítko UV (1 UV = 1 m);
- dřevo z dílců kap. 2 kde to jde (🧩): hrubé opracování, ohlazené hrany, praskliny jako u `SM_RuinTimber`;
- ✋ tvary, které z dílců nesložíš (kovadlina, měch, sud, nářadí), se modelují zvlášť, ❓ procedurálně v `mesh_props.py`, nebo v Blenderu;
- žádné ostré „CAD“ hrany, všechno trochu nakřivo a ošoupané;
- každý prop je samostatný actor (`loose`), **pivot ve středu bounding boxu** (výchozí, Jirka 21. 11. 2026; tak to dělá `mesh_props.py` a poloha v `06_furnishing` je střed bounding boxu). Pivot u země jen u kusů, kde to určí zadání (např. stavební dílce).

### 6.1 Kovárna (`06_furnishing`, `Palac_Kovarna_Vybaveni`) – stojí už v etapě 1; **rozmístěno 16. 11. 2026** (typ `props`, neověřeno v UE)

| ☐ | Prop | Rozměr | Druh |
|---|---|---|---|
| ☑ | špalek pod kovadlinu | Ø 0,5 m | 🧩 kulatina s kůrou, horní čelo → `SM_RuinStump_A–B` |
| ☑ | kovadlina | vrch 0,75 m (se špalkem) | ✋ kov → `SM_RuinAnvil` |
| ☑ | měch na dřevěném rámu | 1,7 × 0,8 m, rám ve výšce 0,9 m | ✋ kůže + 🧩 rám → `SM_RuinBellows` (i rám a výfučna) |
| ☑ | páka měchů | tyč 2,2 m | 🧩 loupaná tyč → kulatina `shape` round (tyč) |
| ☑ | výfučna (měch → výheň) | přes boční zídku | ✋ kov / hlína → součást `SM_RuinBellows` |
| ☑ | kalicí sud s vodou | Ø 0,6 m, výška 0,8 m | ✋ dužiny + obruče, voda → `SM_RuinBarrel` |
| ☑ | brus: kotouč na rámu, **šlapací** (rozhodl Jirka 14. 11. 2026), korýtko | kotouč Ø 0,7 m, rám 1,2 × 0,6 m, osa 0,75 m | `SM_RuinGrindstoneTreadle` (kliková páka, ojnice, šlapadlo); `SM_RuinGrindstone` na ruční kliku zůstává v knihovně |
| ☑ | třínohá stolička k brusu | sedátko Ø 32, výška 45 | 🧩 `SM_RuinStool` |
| ☑ | ponk se svěrákem | 2,2 × 0,7 × 0,85 m | 🧩 prkna a trámky + ✋ svěrák → `SM_RuinWorkbench` |
| ☑ | nářadí na liště: kleště, kladiva, sekáče | sada | ✋ kov + 🧩 lišta → `SM_RuinTongs`, `SM_RuinHammer`, `SM_RuinChisel` (lišta = prkno) |
| ☑ | hřebovnice na špalku | – | ✋ kov + 🧩 špalek → `SM_RuinNailHeader` + `SM_RuinStump` |
| ☑ | truhlík na dřevěné uhlí s víkem | 0,8 × 1,2 × 0,8 m | 🧩 prkna → `SM_RuinCoalBox` (s uhlím) + volné víko `SM_RuinCoalBoxLid` (bez pantů, pokládá se bokem) |
| ◐ | dřevěné uhlí (výplň, žhavé ve výhni) | – | ✋ → výplň v `SM_RuinCoalBox` + `MI_RuinCharcoal`; žhavé uhlí přijde s výhní (`hearth`) |
| ☑ | hranice dřeva (polena) | 0,6 × 1,9 × 1,4 m | 🧩 štípaná polena ✋ + kulatina → `SM_RuinWoodpile` |
| ☑ | železné pruty, koš hřebíků | do výklenku střílny | ✋ kov, 🧩 proutěný koš → `SM_RuinIronBars`, `SM_RuinBasket` |
| ☐ | VFX: oheň a jiskry ve výhni, kouř z komína | ohniště 0,4 × 0,4 m | Niagara ❓ teď, nebo s atmosférou |

### 6.2 Obydlí, hotová stavba (etapa 2)

| ☐ | Prop | Rozměr | Druh |
|---|---|---|---|
| ☑ | lůžko (3×) | 2,0 × 0,8 m | 🧩 + textil a sláma → `SM_RuinBed` (houně přes slámu), `SM_RuinBedFolded` (houně složená) |
| ☑ | stůl | 1,2 × 0,7 m | 🧩 → `SM_RuinTable` |
| ☑ | truhla (2×) | – | 🧩 prkna + ✋ kování → `SM_RuinChest` |
| ☑ | ponk u střílny (síň) | – | 🧩 (stejný jako v kovárně, menší) → `SM_RuinWorkbench` (škálovat) |
| ☑ | police na osobní věci | – | 🧩 → `SM_RuinShelf` |
| ☑ | hranice dřeva v síni | – | 🧩 (jako v kovárně) → `SM_RuinWoodpile` |
| ☑ | dveře (2×) | 1,0 × 2,2 m | 🧩 prkna + svlaky → `SM_RuinDoor` (zrcadlit podle strany závěsů) |
| ☑ | okenice (2×) | 0,6 × 0,6 a 0,5 × 0,5 m | 🧩 → `SM_RuinShutter` (60 × 60, menší škálovat 0,83) |
| ☑ | žebřík na půdu | ze síně do štítu příčky | 🧩 tyče + příčky (sdílený s 6.3) → `SM_RuinLadder` (škálovat délku) |
| ☐ | VFX: oheň v ohništi, kouř z komína | – | Niagara ❓ |

### 6.3 Obydlí, staveniště (etapa 1, `Palac_Obydli_Stavenisko`)

| ☐ | Prop | Rozměr | Druh |
|---|---|---|---|
| ☑ | tesařská koza (2×) | nese kulatinu 5,7 m | 🧩 kozy do X z tyčí s kůrou Ø 11 cm → `SM_RuinPoleBark` (21. 11. 2026) |
| ☑ | rozpracovaná kulatina na kozách | 5,76 m, nahoře z 2/3 oloupaná | 🧩 nový mesh `SM_RuinLogPeeling` (`mesh_log.py`, A/B) + pruhy kůry `SM_RuinBarkStrip` |
| ☑ | žebřík | 4,5 m | 🧩 ❓ použitelný pro postavu? → `SM_RuinLadder` |
| ☑ | dočasné vzpěry sloupů | Ø 10 cm × 3 m | 🧩 tyč s kůrou → `SM_RuinPoleBark` (4 ks, 21. 11. 2026) |
| ☑ | hromada kulatiny na srub | 10 ks loupané kulatiny + 2 pultramy ve 3 vrstvách na podkladcích (z dat sady `final`) | 🧩 kulatina → `SM_RuinLog`, `SM_RuinTimber` |
| ☑ | hromada krokví a vaznice | 6 krokví 6,24 m, pozednice 5,2 m, vaznice 4,75 m | 🧩 trámy → `SM_RuinTimber` |
| ☑ | hromada prken | jedna hranice 75 prken 3,4 m s proklady (varianta: 2 × 44) | 🧩 prkna → `SM_RuinPlank` |
| ☐ | hromada kamene | asi 1 m³ | 🧩 kameny zříceniny |
| ☐ | hromada hlíny + koš mechu | – | ✋ hlína, 🧩 proutěný koš |
| ◐ | tesařské nářadí: sekera, širočina, pila, loupák, kladivo, palice | návrh je nezmiňuje, pro uvěřitelnost | ✋ kov + 🧩 topůrka → `SM_RuinAxe`, `SM_RuinBroadaxe`, `SM_RuinCrosscutSaw` (dvoumužná), `SM_RuinNailHammer`, `SM_RuinMallet`; chybí loupák |

### 6.4 Brána

| ☐ | Prop | Rozměr | Druh |
|---|---|---|---|
| ☐ | španělský jezdec (`Brana_Zataras`) | kmen Ø 18 × 3,4 m + 4 páry kůlů Ø 7 × 1,6 m | 🧩 kulatina s kůrou + loupané kůly, jeden actor |

### 6.5 ⛺ Stan na nádvoří

Rozdělení (Jirka 21. 11. 2026): **assety** = plachta, lůžko, truhlička, ranec (AssetGenerator). **Builder** skládá z hotových meshí stojky, hřeben, kolíky, šňůry (řetěz `SM_RuinRope`) v typu `tent` a stříšku v typu `bark_roof` (vidlice, tyče, krokvičky, kůra, přítlačné tyče, ovázání). Stružka je úprava terénu v levelu.

| ☐ | Prop | Rozměr | Druh |
|---|---|---|---|
| ☑ | plachta stanu do A (díl přes hřeben, 2 štíty, odhrnutá chlopeň) | 2,4 × 2,2 × 1,9 m | na míru → 🆕 `SM_RuinCanvasTent_A` (`mesh_textile.canvas_tent`, OBJ + `.json` se středem, rozměrem, polohou tyčí a kolíků), ♻ `MI_RuinCanvas`. **Hotovo 21. 11. 2026**, náhled `05_constructions/Stan_plachta_nahled.png`, neověřeno v UE |
| ☐ | lůžko z klád a tyčí (2×), výplň **sláma** + houně | 2,0 × 0,7 × 0,25 m; **v stanu blíž ke středu** (vnější okraj ~0,9 m od osy, plachta tam ~35 cm nad zemí; ulička ~0,4 m; Jirka 21. 11. 2026) | 🧩 jeden prop → 🆕 `SM_RuinCampBed` (2 klády Ø 15, 10 tyčí Ø 5 s kůrou, ♻ `MI_RuinStraw`, `MI_RuinWool`) |
| ☑ | špalek k sezení | – | 🧩 (jako pod kovadlinu) → `SM_RuinStump` |
| ☐ | ranec | – | ✋ plátno + lano → 🆕 `SM_RuinBundle` |
| ☐ | truhlička | – | 🧩 prkna + ✋ kování → 🆕 `SM_RuinChestSmall` |
| ☐ | zavěšené boty | – | **nedělá se** (Jirka 21. 11. 2026) |
| ☐ | zavěšené zbraně | – | **odloženo** (Jirka 21. 11. 2026), ❓ sdílet se zbrojí posádky |

### 6.6 Sdílené props (vyrobit jednou, použít víckrát) – hotové 14. 11. 2026: `SM_RuinStump`, `SM_RuinWoodpile`, `SM_RuinBasket`, `SM_RuinLadder`, `SM_RuinWorkbench`

- ☑ Špalek (kovárna, hřebovnice, stan ⛺).
- ☑ Hranice polen (kovárna, síň).
- ☑ Proutěný koš (staveniště, hřebíky v kovárně).
- ☑ Žebřík (staveniště, půda).
- ☑ Ponk (kovárna, síň).

### 6.7 Hlídka na věži

- ☐ ❓ Ohniště a vybavení hlídky ve 2. patře: návrh je výslovně neřeší. Jen poznámka pro game designera.

### 6.8 Guesthouse (obytná část u ostrohu, `06_furnishing`, skupina `Guesthouse_Vybaveni`) – zadání Jirky 21. 11. 2026; **graybox postele, stolu a stoličky** srovnaný v levelu (21. 11. 2026); graybox truhly, stojanů a zástupce pece rozmístěný (21. 11. 2026, k ověření v levelu)

Pokoj pro hosta (inkvizitor řádu, klíč nosí na krku, [[Guest_on_hunt]]). **Nábytek je kvalitnější než v domě** (Jirka 21. 11. 2026): pečlivější opracování a kování, pořád ve stylu hradu. Rám: `s` podél vnitřního líce `ZBudova_V` od jižního rohu k severu (0–12,36 m), `n` do místnosti k západu. První návrh půdorysu (před ověřením měřítka): `Attachments/navrh_guesthouse_vybaveni_pudorys.png`. Polohy grayboxu: `tools/ruin/ostroh_spec.py` → `guesthouse_vybaveni()`.

| ☐ | Prop | Rozměr | Druh |
|---|---|---|---|
| ☐ | postel, **pohodlná** (východní zeď, s = 1,85–4,35; n = 0,39–1,48; graybox ověřený s postavou 180 cm, Jirka 21. 11. 2026) | 2,5 × 1,09 × 0,62 m | 🆕 větší lůžko (`SM_RuinBed` 2,0 × 0,87 nestačí; škálovat jen ❓ jako provizorium) → `SM_RuinBedLarge` |
| ☐ | 🆕 pracovní stůl pro jednoho pod oknem (s = 9,76–11,01; n = 0,07–0,82; graybox) | 1,25 × 0,75 × 0,78 m | 🧩 prkna a trámky → 🆕 `SM_RuinDesk` (nový mesh, Jirka 21. 11. 2026; ne `SM_RuinTable`) |
| ◐ | stolička ke stolu (n = 1,10–1,45; graybox) | 36 × 35 × 47 cm | ♻ `SM_RuinStool` (škála 1,035) |
| ☐ | 🆕 stojan na brnění (u hradby na severozápadě, s = 9,70–10,55; n = 5,25–6,10; poloha Jirka 21. 11. 2026; graybox) | 0,6 × 0,6 × 1,75 m | 🧩 kříž z trámku na noze s podstavcem (hraněné dřevo, kap. 1); **zatím prázdný** (Jirka 21. 11. 2026), výstroj později |
| ☐ | 🆕 stojan na zbraně (jiný objekt než stojan na brnění; u hradby naproti dveřím, s = 6,68–7,73; n = 6,47–7,04; poloha Jirka 21. 11. 2026; graybox) | 1,0 × 0,4 × 1,6 m, stojí u zdi | 🧩 rám z prken a trámků se zářezy; **zatím prázdný** (Jirka 21. 11. 2026), zbraně později (❓ sdílet se zbrojí posádky, kap. 6.5) |
| ◐ | truhla s železným kováním a **zámkem** (v nohách postele, s = 4,46–5,00; n = 0,45–1,41; graybox) | 0,95 × 0,55 × 0,51 m | 🆕 nový mesh truhly s kováním a zámkem (Jirka 21. 11. 2026) → `SM_RuinChestLocked` (🧩 prkna + ✋ kování a zámek; `SM_RuinChest` má jen oko na zámek) |
| ☐ | výhřev: menší pec bez nístěje a plotny (po vzoru `Palac_Obydli_Ohniste`), zády k hradbě v jihozápadním klínu (střed s = 3,12; n = 4,10; v 06 dočasný kvádr `Pec_Zastupce` 1,0 × 0,9 × 1,2 m, po postavení pece se odebere) | asi 1,0 × 0,9 m | **05 → požadavek na stavitele ([[predani_guesthouse_kamna_stavitel]]), pod kamny kamenná dlažba (Jirka 21. 11. 2026):** pevná stavba (typ `hearth`, ♻ `SM_RuinOvenDome` škálovat, `SM_RuinChimney`), komín mezi trámy vějíře B0 a B1, prostup krytinou, **s dymníkem** nad ústím (Jirka 21. 11. 2026); poloha se srovná po ověření měřítka |
| ☑ | poklop ústí pece (06) | 46 × 42 cm | ♻ `SM_RuinOvenDoor` |
| ☐ | 🆕 regál na další věci (u severní zdi `ZBudova_S`, s = 11,90–12,30; n = 0,94–2,50; graybox `Regal`, rozměr Jirka 21. 11. 2026) | 1,56 × 0,4 × 2,0 m | 🧩 prkna a trámky → 🆕 `SM_RuinShelfTall` (vyšší a hlubší než `SM_RuinShelf` 1,0 × 0,28 × 0,9) |
| ☐ | hromádka dřeva vedle pece (podél hradby, s = 3,37–4,20; n = 4,48–5,34; graybox `Drevo_Pec`) | 0,8 × 0,4 × 0,6 m | 🆕 nový mesh (Jirka 21. 11. 2026) → `SM_RuinWoodpileSmall` (🧩 štípaná polena jako `SM_RuinWoodpile`) |

---

## 7. Nové typy staveb v 05 (kód, `zr_stavby/*`)

Nejsou to assety, ale bez nich se assety do levelu nedostanou.

| ☐ | Typ (pracovně) | Nový / rozšíření | Stavby |
|---|---|---|---|
| ☑ | `canvas_shelter` | 🆕 | `Vez_Pristresek` (`zr_stavby/pristresek.py`, hotovo 17. 11. 2026, neověřeno v UE; kontroly `run_checks.py --only vez`) |
| ☑ | `pult_roof` (krytina stejné skladby jako `fan_roof`, vlastní kód) | 🆕 | `Palac_Obydli_Krov`, `Palac_Kovarna_Pristresek`. **Hotovo 15. 11. 2026:** sloupy na patních kamenech, pozednice, krokve (`zr_stavby/pult.py`), krytina s prostupem komína (latě, prkna, lišty) a lemování na stojato. Kostra ověřená v UE, krytina zatím ne. Pro dům (16. 11. 2026): dělené trámy se sadami etap, špalky pod vaznicí, podpora z jiné stavby, latě v kostře; `Palac_Obydli_Krov` bez krytiny, neověřeno v UE. |
| ☑ | `log_wall` (srub, otvory, prkenné štíty) | 🆕 | `Palac_Obydli_Srub`. **Hotovo 16. 11. 2026:** `zr_stavby/srub.py`, řady se sadami etap, půltrámy pro střídání v nároží, štíty. Neověřeno v UE. |
| ◐ | `hearth` (základ, zídka, dymník, komín) | 🆕 | `Palac_Obydli_Ohniste`, `Palac_Kovarna_Vyhen`. **Hotovo 15. 11. 2026:** `zr_stavby/ohniste.py`, postavená `Palac_Kovarna_Vyhen` (stůl, maz, ohniště, zídka s otvorem pro výfučnu, dymník na závěsných tyčích, komín, výměny). Chybí žhavé uhlí, saze, oheň. Ověřeno v UE (15. 11. 2026). **16. 11. 2026:** pec s nístějí pro dům (`dome` s novým meshem `SM_RuinOvenDome`, `boxes`, `flue`, zídky na stole; poklop ústí `SM_RuinOvenDoor` a plotna jako samostatné actory), neověřeno v UE. |
| ◐ | `gutter` (žlab, vidlice, svod) | 🆕 | `Palac_Obydli_Okap`, `Palac_Kovarna_Okap`. **Hotovo 15. 11. 2026:** `zr_stavby/okap.py`: žlab pod okapovou hranou `pult_roof` se spádem, rozsochy (hlava `SM_RuinForkHead` na kůlu), sud jako samostatný actor; postavený `Palac_Kovarna_Okap`. Svod (pro dům) chybí. Neověřeno v UE. |
| ☑ | `wattle_wall` | 🆕 | `Palac_Kovarna_Stena`. **Hotovo 15. 11. 2026:** `zr_stavby/stena.py`: dílce `SM_RuinWattlePanel` mezi sloupy (spodní pás mezi patními kameny), kůly na spojích. Neověřeno v UE. |
| ◐ | `palisade` (kůly, ráhna, průzory) | 🆕 | `Brana_Straz_Kryty`. **16. 11. 2026:** `zr_stavby/kryty.py`, postavené všechny tři kryty (východní `base`, severní a jižní `final`). |
| ☐ | `bark_roof` | 🆕 | `Brana_Straz_Pristresek`, ⛺ `Nadvori_Stan_Striska` |
| ☐ | `tent` | ⛺ 🆕 | `Nadvori_Stan` |
| ☐ | strop s výměnou / trámy na koruně | ♻ rozšíření `tower_floor` | `Palac_Obydli_Strop`, `Brana_Straz_Podesta` |
| ☐ | `stone_addon` s parametrem tloušťky (0,8 m) | ♻ rozšíření | `Palac_Obydli_Kamen`, `Brana_Straz_Kamen` |
| ☐ | `plank_floor` | ♻ beze změny | `Palac_Obydli_Podlaha` |
| ◐ | etapy: sady actorů `base` / `final` / `site` s tagem `stage:<sada>` (místo přepínače `ETAPA`) | 🆕 | **Hotovo 16. 11. 2026:** sady v `zrlib/config.py`, `Stone.stage`, build po sadách. Staveniště (`Palac_Obydli_Stavenisko`) a ⛺ stan ještě ne. |
| ☑ | `stone_fill` (srovnání koruny zdi kamenem v plné tloušťce, zazdění otvoru, podezdívky) | 🆕 místo rozšíření `stone_addon` | `Palac_Obydli_Kamen` (16. 11. 2026, neověřeno v UE) |
| ◐ | rozmístění props (`loose`, seznam poloh z návrhů) | 🆕 | vybavení kovárny, domu, staveniště, stanu ⛺. **Hotovo 16. 11. 2026:** typ `props` (`zr_stavby/vybaveni.py`), vybavení odděleně v `06_furnishing` (`build_furnishing.py`, `furnishing.json` = data i polohy z levelu), rozmístěná kovárna (`Palac_Kovarna_Vybaveni`). |

**Sdílené specy:**
- ☑ `tools/ruin/tower_spec.py`: průlomy (`ruin_edits()`) a přístřešek (`PR`, `pristresek()`), 17. 11. 2026;
- ◐ 🆕 `palac_spec.py`: dům, kovárna a `ETAPA`. Hotový rám paláce a přístřešek kovárny (15. 11. 2026); dům a `ETAPA` ne;
- ☑ 🆕 `brana_spec.py` (16. 11. 2026: rám brány, podesta, kapsy v `Brana_V`).

---

## 8. Úpravy zříceniny 03 (data, ne assety)

| ☐ | Zeď | Změna | Zdroj |
|---|---|---|---|
| ☑ | `Vez_V` | 2 × `breaches` (hlavní průlom, nejnižší 9,45 m, severní bok mírný `slope_r` 0,35 až k SV rohu 11,2 m) (hotovo 17. 11. 2026 v `tower_spec.ruin_edits()`, neověřeno v UE) | [[navrh_vez_pristresek]] 3.1 |
| ☑ | `Vez_J` | 2 × `breaches` + `protect` nad střílnou (hotovo 17. 11. 2026 v `tower_spec.ruin_edits()`, neověřeno v UE) | 3.2 |
| ☑ | `Vez_Z` | 2 × `protect` (s = 7,0–8,2 `min` 12,1; s = 8,2–9,5 `min` 11,8): střed zdi vyšší, jen vedlejší škody (Jirka 17. 11. 2026) (hotovo 17. 11. 2026 v `tower_spec.ruin_edits()`, neověřeno v UE) | 3.3 |
| ☑ | `Vez_S` | zrušit `breaches` s = 3,5–7,5 (tvar U); nový `breaches` (rampa od SV rohu, `power_r` 0,7) + 8 × `protect` po 1,5 m: koruna plynule klesá od SZ rohu k SV rohu (Jirka 17. 11. 2026) (hotovo 17. 11. 2026 v `tower_spec.ruin_edits()`, neověřeno v UE) | 3.4 |
| ☐ | `Palac_J` | `breaches` s = 15,5–18,3 (sedlo u komína): **odpadá**, po zanoření zdi je koruna u komína 4,4–4,8 m (16. 11. 2026) | [[navrh_palac_obydli_stred]] kap. 0.2 |
| ☑ | `Palac_J` | celá zeď zanořená o jednu řadu do země (`z_offset` −0,31), rozebraná koruna u věže (`breaches` s = 29,6–33, komín kovárny ji přesahuje) a `kapsa` pro východní pozednici kovárny v s = 30,55 (15. 11. 2026, neověřeno v UE) | [[navrh_palac_kovarna]] kap. 3, `palac_spec.py` |
| ☑ | `Palac_S` | portál přesunutý do západní místnosti (s = 4,5, `protect` s = 2,5–6,5), ve střední místnosti hrubý průchod (`prulom` s = 16, 1,8 m) (16. 11. 2026, neověřeno v UE) | [[navrh_palac_obydli_stred]] kap. 0.2a, `gen_layout.py` |
| ☑ | `Palac_pricka_2` | hrubý průchod ze zápraží domu ke kovárně (`prulom` n = 6,9–8,5) (16. 11. 2026, neověřeno v UE) | [[navrh_palac_obydli_stred]] kap. 0.2a, `palac_spec.py` → `D_PASS` |
| ☐ | kontrola `manual_edits.json` | ID kamenů `Vez_J`, `Vez_V`, `Vez_Z`, `Palac_J`, `Palac_S`, `Palac_pricka_2` se po přestavbě změní (17. 11. 2026 prázdný) | – |

---

## 9. Otevřené otázky, které ovlivní assety

- ☐ ❓ Přiřazení kůra / bez kůry podle kap. 2.1: potvrdit, hlavně zábradlí brány, žlaby a rozpracovanou kulatinu.
- ☑ Struktura generátoru (kap. 3): `tools/meshes/gen_meshes.py` + moduly podle materiálu, OBJ v `meshes/<kategorie>/` (rozhodnuto 14. 11. 2026).
- ☑ Tvary na míru: OBJ (14. 11. 2026). Plátno `mesh_textile.make_canvas`, lano z knihovních článků, výplet z knihovních dílců.
- ☑ Props tvaru ✋: procedurálně v Pythonu (vizuální prototyp, 14. 11. 2026).
- ◐ Plátno ve větru: připraveno v materiálu (`M_RuinCloth`, parametr `WindAmount`, výchozí 0 = staticky). Vítr ani napnutí plachet zatím řešené nejsou; prověšení dává `make_canvas` (`sag`).
- ☑ Kovárna ve východní místnosti: potvrzeno (Jirka 15. 11. 2026). Svod se nedělá, žlab ústí do sudu. Saze, udusaná hlína, žhavé uhlí a VFX ohně se pro kovárnu zatím nedělají.
- ☑ Žebříky (staveniště, půda): jen kulisa, pro postavu nepoužitelné (chybí animace; [[navrh_palac_obydli_stred]] kap. 0.1).
- ☐ ❓ Stojí podesta brány v etapě 1? Určuje, jestli potřebuje přepínač `ETAPA`.
- ☐ ❓ VFX ohně a kouře: v tomto kroku, nebo později s atmosférou?
- ☑ Stan: bude (Jirka 21. 11. 2026). Rozdělení assety / Builder v kap. 6.5.

---

## 10. Závislosti (podklad pro prioritizaci)

| Položka | Blokuje |
|---|---|
| refaktoring generátoru (kap. 3) | všechny nové meshe (kap. 2, 4, 6) |
| kulatina a tyče, s kůrou i bez (kap. 2) | všechny stavby kromě krovu domu a kovárny, většinu props |
| `MI_RuinBark`, `_Peeled`, `_EndGrain` | vzhled kulatiny |
| úpravy 03 (kap. 8) | `Vez_Pristresek`, komín obydlí |
| `pult_roof` | dům, kovárna |
| kovárna | stojí už v etapě 1, dům potřebuje hřebíky (příběhově) |
| `ETAPA` přepínač | staveniště, stan ⛺, rozlišení etap obydlí |
| sdílené props (6.6) | props kovárny, domu, staveniště, stanu |
| plátno + lano | `Vez_Pristresek`, stan ⛺ |
| pásy kůry | přístřešek brány, stříška stanu ⛺ |
| proutí + mazanina | stěna kovárny, dymníky, komíny |

---

## 11. Pořadí prací (Jirka 21. 11. 2026)

1. **Stan (6.5):** `SM_RuinCanvasTent_A` → `SM_RuinCampBed` → `SM_RuinChestSmall` → `SM_RuinBundle`. Typy `tent` a `bark_roof` dělá Builder.
2. **Guesthouse (6.8), všechno, kvalitnější provedení:** `SM_RuinBedLarge` → `SM_RuinChestLocked` → `SM_RuinDesk` → `SM_RuinShelfTall` → `SM_RuinWoodpileSmall` → stojan na brnění a stojan na zbraně (názvy ❓, pracovně `SM_RuinArmorStand`, `SM_RuinWeaponRack`). Pec dělá Builder ([[predani_guesthouse_kamna_stavitel]]).
3. **Fronta, zatím ne:** staveniště (6.3: loupák, hromada hlíny a koš mechu, hromada kamene), materiály kap. 5 (saze, udusaná hlína, třísky), španělský jezdec (6.4), zbraně (6.5, 6.8), VFX.
