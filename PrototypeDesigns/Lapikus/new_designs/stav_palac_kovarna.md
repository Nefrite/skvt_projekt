# Kovárna v paláci (Palac_Kovarna) – stav stavby proti návrhu

Stav: 16. 11. 2026 (kroky 1–4 hotové). Návrh: `navrh_palac_kovarna.md` (stejný přehled je v jeho kap. 0, při změně uprav oba). Rozměry: `tools/ruin/palac_spec.py`. Náhled: `05_constructions/Stavby_palac_kovarna_nahled.png`.

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
| Měchy, páka (kap. 4.3) | `Palac_Kovarna_Vybaveni` | ✅ hotovo | výfučna v otvoru boční zídky; páka Ø 6 cm na laně z krokve n = 2,7, s měchy spojená lanem |
| Kovadlina, sud, brus, ponk, nářadí, truhlík, železo (kap. 4.4) | `Palac_Kovarna_Vybaveni` | ✅ hotovo | typ `props` (`zr_stavby/vybaveni.py`), samostatné actory; nářadí na liště na jižní zdi |
| Hranice dřeva pod přesahem (kap. 4.4) | `Palac_Kovarna_Vybaveni` | ✅ hotovo | od kůlu 1,5 m od `Palac_J` k severnímu okraji střechy (Jirka 16. 11. 2026) |
| Úklid suti ve východní místnosti (kap. 5) | `Sut` | ✅ hotovo | `clear_poly` u `Palac_Kovarna_Vybaveni` (celá místnost) |
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

## Co spustit v UE (pořadí)

**Celá kovárna jedním skriptem:** `05_constructions/stavby/Palac_Kovarna.py`. Postaví přístřešek, výheň, stěnu, okap a vybavení v tomto pořadí a nakonec suť (`SUT = True`). S `RUIN = True` napřed přestaví i část zříceniny `Palac` (jen po změně `J_*` nebo kapsy v `palac_spec.py`). `MODE = "capture"` uloží ruční úpravy všech částí kovárny.

Jednotlivě (stejné pořadí): `Palac_Kovarna_Pristresek.py` (`KRYTINA = True`), `Palac_Kovarna_Vyhen.py`, `Palac_Kovarna_Stena.py`, `Palac_Kovarna_Okap.py`, `Palac_Kovarna_Vybaveni.py`, `Sut.py`.

Nové meshe nejsou (props, dílce stěny, žlab, rozsochy a sud už v projektu jsou).

## Další kroky

1. Ověřit v UE krytinu s prostupem komína, lemování, stěnu z proutí, okap se sudem a vybavení; ruční doladění props uložit přes `MODE = "capture"` v `Palac_Kovarna_Vybaveni.py`.
2. Odloženo: žhavé uhlí, saze, oheň a kouř, udusaná hlína.
3. Před stavbou domu přepočítat koruny `Palac_J` v `navrh_palac_obydli_stred.md` (zeď je o 0,31 m níž).
