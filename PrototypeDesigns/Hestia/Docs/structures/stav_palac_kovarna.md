---
# orchestrace
type: state
validity: valid
updated: 2026-11-22
# hra
domain: structures
depth: 4
entity: "[[Palac_Kovarna]]"
build_step: 05_constructions
---
# Kovárna v paláci (Palac_Kovarna) – stav stavby proti návrhu

## Souhrn
Stav stavby kovárny k 16. 11. 2026 proti návrhu [[navrh_palac_kovarna]] (stav přesunutý z jeho kap. 0). Kroky 1–4 jsou hotové ve skriptech a ověřené mimo UE; v UE je ověřená úprava 03, kostra přístřešku a výheň, zbytek (krytina, lemování, stěna, okap, vybavení) ne.
- **Odloženo:** žhavé uhlí, saze, oheň a kouř, podlaha z udusané hlíny.
- **Odchylky od návrhu ze 14. 11. 2026 a jejich důvody:** sekce *Odchylky* (výheň v koutě, zanořená `Palac_J`, posunutá západní linie, komín, přesah krokví, rozšíření o řadu krokví).
- **Spuštění v UE:** `Palac_Kovarna.py` celá kovárna, jednotlivé stavby a vybavení v `06_furnishing` (sekce *Co spustit v UE*).
- **Další kroky:** ověření v UE a přepočet korun `Palac_J` v [[navrh_palac_obydli_stred]] (zeď je o 0,31 m níž).

Stav: 16. 11. 2026 (kroky 1–4 hotové). Návrh: [[navrh_palac_kovarna]] (tady je jediný přehled stavu). Rozměry: `tools/ruin/palac_spec.py`. Náhled: `05_constructions/Stavby_palac_kovarna_nahled.png`.

## Co je hotové a co zbývá

Všechno „hotovo“ znamená: je ve skriptech a datech a prošlo kontrolami mimo Unreal (`tools/checks/run_checks.py`). **V UE je ověřená úprava 03, kostra přístřešku a výheň** (Jirka 15. 11. 2026); krytina, stěna, okap a vybavení zatím ne.

| Část návrhu | Stavba / místo | Stav | Poznámka |
|---|---|---|---|
| Úprava 03: `Palac_J` zanořená o řadu do země (kap. 3) | `03_ruin`, část `Palac` | ✅ hotovo | `z_offset` −0,31 m |
| Úprava 03: rozebraná koruna `Palac_J` u věže (kap. 3) | `03_ruin`, část `Palac` | ✅ hotovo | `breaches`; komín ji přesahuje o 0,3–1,5 m |
| Úprava 03: kapsa pro východní pozednici (kap. 3) | `03_ruin`, část `Palac` | ✅ hotovo | `kapsa` ve vnitřním líci `Palac_J` |
| Sloupy, pozednice, krokve (kap. 4.1) | `Palac_Kovarna_Pristresek` | ✅ hotovo | 5 sloupů na patních kamenech, 2 pozednice, 7 krokví (rozšířeno 16. 11. 2026) |
| Krytina, latě, lišty (kap. 4.1) | `Palac_Kovarna_Pristresek` | ✅ hotovo | skladba jako `Ostroh_Krov`, vlastní kód (`pult._pult_cover`); prostup komína s mezerou 3 cm |
| Lemování u věže a u `Palac_J` (kap. 4.1) | `Palac_Kovarna_Pristresek` | ✅ hotovo | prkno 25 cm na stojato |
| Výheň: stůl, maz, ohniště (kap. 4.3) | `Palac_Kovarna_Vyhen` | ✅ hotovo | v koutě místnosti |
| Boční zídka s otvorem pro výfučnu (kap. 4.3) | `Palac_Kovarna_Vyhen` | ✅ hotovo | |
| Dymník, komín, výměny, závěsné tyče (kap. 4.3) | `Palac_Kovarna_Vyhen` | ✅ hotovo | |
| Žhavé uhlí, saze, oheň a kouř | – | ⏸ odloženo | rozhodnuto 15. 11. 2026 |
| Západní stěna z proutí (kap. 4.2) | `Palac_Kovarna_Stena` | ✅ hotovo | typ `wattle_wall` (`zr_stavby/stena.py`), dílce mezi sloupy, kůly na spojích |
| Žlab, vidlice, sud na vodu (kap. 4.5) | `Palac_Kovarna_Okap` | ✅ hotovo | typ `gutter` (`zr_stavby/okap.py`), 3 rozsochy, sud = samostatný actor |
| Měchy, páka (kap. 4.3) | 06 `Palac_Kovarna_Vybaveni` | ✅ hotovo | výfučna v otvoru boční zídky; páka Ø 6 cm na laně z krokve n = 2,7, s měchy spojená lanem |
| Kovadlina, sud, brus, ponk, nářadí, truhlík, železo (kap. 4.4) | 06 `Palac_Kovarna_Vybaveni` | ✅ hotovo | `06_furnishing` (přenosné vybavení, od 16. 11. 2026), typ `props`, samostatné actory; nářadí na liště na jižní zdi |
| Hranice dřeva pod přesahem (kap. 4.4) | 06 `Palac_Kovarna_Vybaveni`, kůl 05 `Palac_Kovarna_Kul` | ✅ hotovo | od kůlu 1,5 m od `Palac_J` k severnímu okraji střechy (Jirka 16. 11. 2026) |
| Úklid suti ve východní místnosti (kap. 5) | `Sut` | ✅ hotovo | `clear_poly` u `Palac_Kovarna_Pristresek` (celá místnost) |
| Podlaha z udusané hlíny (kap. 4.4) | – | ⏸ odloženo | chybí materiál |
| Sdílené rozměry (kap. 5) | `tools/ruin/palac_spec.py` | ✅ hotovo | rám paláce, kovárna, úpravy 03 |
| Kontroly a náhled (kap. 7) | `run_checks.py --only palac`, `preview3d.py kovarna` | ✅ hotovo | pokrytí krytinou, lemování, stěna, žlab a sud, vybavení (průniky, výfučna v otvoru, vzdálenosti, průchody, dřevo pod přesahem, suť) |
| Ověření v Unrealu | – | ◐ částečně | úprava 03, kostra přístřešku a výheň ověřené (Jirka 15. 11. 2026, v pořádku); krytina, lemování, stěna, okap a vybavení zatím ne |

## Změna okolí (16. 11. 2026)

- Na dvorek kovárny vede nově i hrubý průchod v `Palac_pricka_2` (n = 6,9–8,5) ze zápraží domu posádky. Data kovárny se tím nezměnila, po přestavbě části `Palac` stačí zkontrolovat vchod z nádvoří (ostění dveří s = 27 je o kousek širší).

## Odchylky od původního návrhu ze 14. 11. 2026

- výheň v koutě místo u věže dál od zdi;
- `Palac_J` zanořená o řadu, rozebraná u věže a s kapsou (původně žádná úprava 03);
- východní pozednice ve 4,24 m místo 4,2 m;
- u věže jeden sloup místo dvou;
- západní linie v s = 25,85 místo 25,5;
- západní pozednice ve 2,5 m místo 2,3 m;
- krokve 6,1 m s přesahem 0,9 m místo 0,4 m;
- komín v s = 30,0; n = 1,35 místo s = 30,45; n = 2,1;
- dymník na závěsných tyčích (návrh uložení neřešil);
- dřevo venku pod přesahem místo uvnitř;
- žlab do sudu bez svodu;
- krytina 3,5 cm od líce `Palac_J` (kameny koruny v s = 27–29 vystupují z líce v úrovni střechy), lemování na hraně krajního prkna;
- okapová hrana krytiny s = 24,85 (prkna 10 cm za konci krokví), žlab n = 0,72–5,9 a sud v n = 5,9 (návrh: n = 0,7–5,7, sud n ≈ 5,9);
- stěna z proutí: spodní pás 0,1 m mezi patními kameny, nad ním dílce mezi sloupy; kůly na spojích dílců;
- vybavení (16. 11. 2026): brus o 0,2 m severněji (rám n = 4,2–4,8, průchod 1,2 m mezi kalicím sudem a brusem k ponku), ponk a truhlík o 0,1 m východněji (patní kameny západních sloupů); dřevo navíc: hranice od kůlu 1,5 m od `Palac_J` až k severnímu okraji střechy (průchod ke střílně s = 25 volný); hřebovnice na menším špalku v s = 27,95; n = 1,85; páka měchů zavěšená na laně z krokve n = 2,7.
- okap (16. 11. 2026): spád žlabu 2,5 % místo 1,5 %, jižní rozsocha dál od `Palac_J` (průchod ke střílně s = 25);
- rozšíření (16. 11. 2026, Jirka): přístřešek o řadu krokví k severu (7 krokví n = 0,9–6,3, střecha do n = 6,6), sloupy u věže n = 4,4 a 6,2 (východní pozednice měla z kapsy rozpětí 5,5 m), západní sloupy rovnoměrně n = 0,9 / 3,55 / 6,2, stěna do n = 6,3, žlab do n = 6,8 s rozsochami n = 1,7 / 4,0 / 6,3, sud v n = 6,8, dřevo tři hranice do n = 6,4; kovadlina v s = 28,0 (1,5 m před výhní místo 1,0 m), kalicí sud (28,3; 2,6), hřebovnice (27,35; 1,75), brus o řadu severněji (rám n = 5,1–5,7), koš (26,45; 6,0); okno věže je jen světlík (neprůchozí).

### Proč: změny 15.–16. 11. 2026 (z návrhu kap. 0)

**Změny 15. 11. 2026** (dohodnuto s Jirkou při zahájení stavby):
- **Umístění potvrzeno:** východní místnost paláce.
- **Západní linie posunutá z s = 25,5 na s = 25,85** (sloupy, pozednice, stěna z proutí). Na původním místě končila stěna ve výklenku střílny s = 25 (výklenek je s = 24,35–25,65) a neměla o co dosednout. Vrch západní pozednice je kvůli zachování sklonu 20° ve 2,5 m (dřív 2,3 m), stěna z proutí 2,1 m (dřív 1,9 m).
- **Výheň v koutě místnosti** (Jirka 15. 11. 2026, večer; ruší dřívější polohu u věže v n = 1,5–2,7): stůl leží v koutě mezi `Palac_J` a věží (n = 0,72–1,9). Výklenek střílny s = 29 je hned vedle stolu a dává kolem výhně manipulační prostor, proto zůstává volný.
- **Celá `Palac_J` je posunutá po ose Z o jednu řadu kamene níž** (zanořená do země, počet řad se nemění) a **u věže je koruna rozebraná** tak, aby ji komín přesahoval (úprava 03, kap. 3). První pokus (ubrání horní řady, `drop_rows`) byl nedorozumění a pro tuto zeď je zrušený.
- **Rohový sloup u věže odpadl** (stála by v něm výheň). Východní pozednice je jižním koncem zapuštěná 0,3 m do `Palac_J` (kapsa, úprava 03), na severu leží na sloupu.
- **Komín je o jedno pole krokví jižněji:** střed s = 30,0; n = 1,35, mezi krokvemi n = 0,9 a 1,8 (vůle 12 cm), 20 cm od východní pozednice. Původní poloha (s = 30,45; n = 2,1) procházela pozednicí.
- **Svod zrušen, žlab ústí do sudu** u svého severního konce. Svod přes dvorek by postavě odřízl západní kout dvorku.
- **Krokve protažené o 0,5 m** (přesah 0,9 m za západní pozednici, okap v s = 24,95). Pod přesahem se zvenku podél západní stěny vyskládá dřevo, aby bylo kryté (Jirka 15. 11. 2026). Hranice dřeva proto není uvnitř kovárny.
- **Vybavení u západní stěny** se posouvá s ní (kap. 4.4).
- **Dymník visí na krokvích:** mezi krokvemi n = 0,9 a 1,8 jsou po obou stranách komína výměny (loupaná kulatina Ø 10 cm), z jejich konců vedou čtyři závěsné tyče Ø 5 cm k rohům spodního okraje dymníku. Původní návrh uložení dymníku neřešil.
- **Ohniště** je pod komínem (střed s = 30,0; n = 1,35), tedy u západní hrany stolu, na dosah od kovadliny.
- **Okno věže nad střechou:** je neprůchozí, slouží jen jako světlík do věže (Jirka 16. 11. 2026).
- **Rozšíření (16. 11. 2026, Jirka):** v kovárně bylo na vybavení málo místa. přístřešek o řadu krokví k severu (7 krokví n = 0,9–6,3, střecha do n = 6,6), sloupy u věže n = 4,4 a 6,2 (východní pozednice měla z kapsy rozpětí 5,5 m), západní sloupy rovnoměrně n = 0,9 / 3,55 / 6,2, stěna do n = 6,3, žlab do n = 6,8 s rozsochami n = 1,7 / 4,0 / 6,3, sud v n = 6,8, dřevo tři hranice do n = 6,4; kovadlina v s = 28,0 (1,5 m před výhní místo 1,0 m), kalicí sud (28,3; 2,6), hřebovnice (27,35; 1,75), brus o řadu severněji (rám n = 5,1–5,7), koš (26,45; 6,0); okno věže je jen světlík (neprůchozí).
- **Postup stavby:** 1. `palac_spec.py` a přístřešek bez krytiny, 2. výheň a krytina, 3. stěna a okap, 4. vybavení a úklid suti. Kroky 1 a výheň ověřené v UE (15. 11. 2026), kroky 2 a 3 hotové mimo UE (15. 11. 2026, večer).
- **Krytina (krok 2):** latě 9 řad (nad a pod prostupem komína, jinak nejvýš po 0,9 m), prkna 22–30 cm po spádu od líce věže po okapovou hranu s = 24,85 (10 cm za konci krokví, nad osou žlabu), lišty přes spáry, prostup komína s mezerou 3 cm (prkna se kladou od jeho okrajů ven). Od líce `Palac_J` mezera 3,5 cm, protože kameny koruny v s = 27–29 leží v úrovni střechy a vystupují z líce. Lemování: prkno 25 cm na stojato u věže a podél `Palac_J`.
- **Stěna a okap (krok 3):** stěna z dílců proutí mezi sloupy, spodní pás 0,1 m mezi patními kameny, kůly Ø 9 cm na spojích dílců. Žlab Ø 20 cm (loupaný) na třech rozsochách v n = 1,4 / 3,1 / 5,3 (jižní posunutá 16. 11. 2026 od `Palac_J` kvůli průchodu ke střílně, žlab k hradbě volně přesahuje), vrch 12–25 cm pod krytinou, spád 2,5 % k severu; sud pod jeho koncem (s = 24,8; n = 5,9) je samostatný actor.

### Připravenost assetů (z návrhu kap. 0)

**Připravenost (15. 11. 2026)** – podrobně [[CHECKLIST_assets_navrhy]], kap. 6.1:
- **Vybavení je hotové** jako vlastní procedurální props (`tools/meshes/mesh_props.py`), zatím nerozmístěné: špalek `SM_RuinStump`, kovadlina `SM_RuinAnvil`, měchy s rámem a výfučnou `SM_RuinBellows`, páka (loupaná tyč `SM_RuinPole`), kalicí sud `SM_RuinBarrel`, **šlapací brus** `SM_RuinGrindstoneTreadle` s třínohou stoličkou `SM_RuinStool`, ponk se svěrákem `SM_RuinWorkbench`, kleště, kladivo, sekáč (`SM_RuinTongs`, `SM_RuinHammer`, `SM_RuinChisel`), hřebovnice `SM_RuinNailHeader`, truhlík na uhlí `SM_RuinCoalBox` s volným víkem `SM_RuinCoalBoxLid`, hranice dřeva `SM_RuinWoodpile`, železné pruty `SM_RuinIronBars`, koš `SM_RuinBasket`.
- **Hotové dílce stavby:** loupaná kulatina `SM_RuinLog` (krokve), dílce proutěné stěny `SM_RuinWattlePanel`, dymník `SM_RuinSmokeHood`, komín `SM_RuinChimney`, žlab `SM_RuinGutter`.
- **Hotové (15. 11. 2026):** typy `pult_roof` bez krytiny (`05_constructions/zr_stavby/pult.py`) a `hearth` (`zr_stavby/ohniste.py`), sdílené rozměry `tools/ruin/palac_spec.py`, úpravy 03 (`z_offset`, `breaches`, `kapsa`), kontrola `run_checks.py --only palac`, náhled `preview3d.py kovarna`.
- **Hotové (15. 11. 2026, večer):** krytina a lemování v `pult_roof`, typy `wattle_wall` (`zr_stavby/stena.py`) a `gutter` (`zr_stavby/okap.py`), kontroly krytiny, stěny a okapu v `run_checks.py --only palac`.
- **Souhrnný spouštěč (16. 11. 2026):** `05_constructions/stavby/Palac_Kovarna.py` postaví celou kovárnu (seznam staveb jen tam, logika společná s jednotlivými spouštěči).
- **Hotové (16. 11. 2026):** rozmístění vybavení (typ `props`, `zr_stavby/vybaveni.py`, `palac_spec.kovarna_vybaveni`), úklid suti v celé východní místnosti (`clear_poly`).
- **Vybavení (krok 4):** brus o 0,2 m severněji (rám n = 4,2–4,8, průchod 1,2 m mezi kalicím sudem a brusem k ponku), ponk a truhlík o 0,1 m východněji (patní kameny západních sloupů); dřevo navíc: hranice od kůlu 1,5 m od `Palac_J` až k severnímu okraji střechy (průchod ke střílně s = 25 volný); hřebovnice na menším špalku v s = 27,95; n = 1,85; páka měchů zavěšená na laně z krokve n = 2,7.
- **Chybí:** nic z návrhu. Žhavé uhlí ve výhni, saze, udusaná hlína, oheň a kouř se zatím nedělají (rozhodnuto 15. 11. 2026).

## Co spustit v UE (pořadí)

**Celá kovárna jedním skriptem:** `05_constructions/stavby/Palac_Kovarna.py`. Postaví přístřešek, výheň, stěnu, okap a kůl v tomto pořadí, pak suť (`SUT = True`) a nakonec vybavení z `06_furnishing` (`VYBAVENI = True`). S `RUIN = True` napřed přestaví i část zříceniny `Palac` (jen po změně `J_*` nebo kapsy v `palac_spec.py`). `MODE = "capture"` uloží ruční úpravy všech částí kovárny i vybavení.

Jednotlivě (stejné pořadí): `Palac_Kovarna_Pristresek.py` (`KRYTINA = True`), `Palac_Kovarna_Vyhen.py`, `Palac_Kovarna_Stena.py`, `Palac_Kovarna_Okap.py`, `Palac_Kovarna_Kul.py`, `Sut.py`; vybavení `06_furnishing/vybaveni/Palac_Kovarna.py`.

**Vybavení (06_furnishing, od 16. 11. 2026 oddělené od staveb):** `06_furnishing/vybaveni/Palac_Kovarna.py`. Ruční doladění: posuň, otoč, zvětši nebo zkopíruj props v levelu a spusť ho s `MODE = "capture"` (zapíše se přímo do `06_furnishing/furnishing.json`, přežije další generování); `list` vypíše posuny proti specu, `reset` vrátí kusy na spec.

Nové meshe nejsou (props, dílce stěny, žlab, rozsochy a sud už v projektu jsou).

## Další kroky

1. Ověřit v UE krytinu s prostupem komína, lemování, stěnu z proutí, okap se sudem a vybavení; ruční doladění props uložit přes `06_furnishing/vybaveni/Palac_Kovarna.py` (`MODE = "capture"`).
2. Odloženo: žhavé uhlí, saze, oheň a kouř, udusaná hlína.
3. Před stavbou domu přepočítat koruny `Palac_J` v [[navrh_palac_obydli_stred]] (zeď je o 0,31 m níž).
