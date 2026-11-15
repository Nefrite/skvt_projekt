# Kovárna v paláci (Palac_Kovarna) – stav stavby proti návrhu

Stav: 15. 11. 2026 (večer: kroky 2 a 3). Návrh: `navrh_palac_kovarna.md` (stejný přehled je v jeho kap. 0, při změně uprav oba). Rozměry: `tools/ruin/palac_spec.py`. Náhled: `05_constructions/Stavby_palac_kovarna_nahled.png`.

## Co je hotové a co zbývá

Všechno „hotovo“ znamená: je ve skriptech a datech a prošlo kontrolami mimo Unreal (`tools/checks/run_checks.py`). **V UE je ověřená úprava 03, kostra přístřešku a výheň** (Jirka 15. 11. 2026); krytina, stěna a okap zatím ne.

| Část návrhu | Stavba / místo | Stav | Poznámka |
|---|---|---|---|
| Úprava 03: `Palac_J` zanořená o řadu do země (kap. 3) | `03_ruin`, část `Palac` | ✅ hotovo | `z_offset` −0,31 m |
| Úprava 03: rozebraná koruna `Palac_J` u věže (kap. 3) | `03_ruin`, část `Palac` | ✅ hotovo | `breaches`; komín ji přesahuje o 0,3–1,5 m |
| Úprava 03: kapsa pro východní pozednici (kap. 3) | `03_ruin`, část `Palac` | ✅ hotovo | `kapsa` ve vnitřním líci `Palac_J` |
| Sloupy, pozednice, krokve (kap. 4.1) | `Palac_Kovarna_Pristresek` | ✅ hotovo | 4 sloupy na patních kamenech, 2 pozednice, 6 krokví |
| Krytina, latě, lišty (kap. 4.1) | `Palac_Kovarna_Pristresek` | ✅ hotovo | skladba jako `Ostroh_Krov`, vlastní kód (`pult._pult_cover`); prostup komína s mezerou 3 cm |
| Lemování u věže a u `Palac_J` (kap. 4.1) | `Palac_Kovarna_Pristresek` | ✅ hotovo | prkno 25 cm na stojato |
| Výheň: stůl, maz, ohniště (kap. 4.3) | `Palac_Kovarna_Vyhen` | ✅ hotovo | v koutě místnosti |
| Boční zídka s otvorem pro výfučnu (kap. 4.3) | `Palac_Kovarna_Vyhen` | ✅ hotovo | |
| Dymník, komín, výměny, závěsné tyče (kap. 4.3) | `Palac_Kovarna_Vyhen` | ✅ hotovo | |
| Žhavé uhlí, saze, oheň a kouř | – | ⏸ odloženo | rozhodnuto 15. 11. 2026 |
| Západní stěna z proutí (kap. 4.2) | `Palac_Kovarna_Stena` | ✅ hotovo | typ `wattle_wall` (`zr_stavby/stena.py`), dílce mezi sloupy, kůly na spojích |
| Žlab, vidlice, sud na vodu (kap. 4.5) | `Palac_Kovarna_Okap` | ✅ hotovo | typ `gutter` (`zr_stavby/okap.py`), 3 rozsochy, sud = samostatný actor |
| Měchy, páka (kap. 4.3) | `Palac_Kovarna_Vybaveni` | ⬜ zbývá rozmístit | prop `SM_RuinBellows` hotový |
| Kovadlina, sud, brus, ponk, nářadí, truhlík, železo (kap. 4.4) | `Palac_Kovarna_Vybaveni` | ⬜ zbývá rozmístit | všechny props hotové; chybí kód pro rozmístění (`loose`) |
| Hranice dřeva pod přesahem (kap. 4.4) | `Palac_Kovarna_Vybaveni` | ⬜ zbývá rozmístit | prop `SM_RuinWoodpile` hotový |
| Úklid suti ve východní místnosti (kap. 5) | `Sut` | ⬜ zbývá | `clear_rubble` zatím umí jen kamenné dostavby |
| Podlaha z udusané hlíny (kap. 4.4) | – | ⏸ odloženo | chybí materiál |
| Sdílené rozměry (kap. 5) | `tools/ruin/palac_spec.py` | ✅ hotovo | rám paláce, kovárna, úpravy 03 |
| Kontroly a náhled (kap. 7) | `run_checks.py --only palac`, `preview3d.py kovarna` | ✅ hotovo pro postavené části | pokrytí krytinou, lemování, stěna, žlab a sud; průchody kolem vybavení přibudou v kroku 4 |
| Ověření v Unrealu | – | ◐ částečně | úprava 03, kostra přístřešku a výheň ověřené (Jirka 15. 11. 2026, v pořádku); krytina, lemování, stěna a okap zatím ne |

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
- stěna z proutí: spodní pás 0,1 m mezi patními kameny, nad ním dílce mezi sloupy; kůly na spojích dílců.

## Co spustit v UE (pořadí)

Úprava 03, kostra a výheň už v levelu jsou (ověřeno). Pro kroky 2 a 3:

1. `05_constructions/stavby/Palac_Kovarna_Pristresek.py` (krytina a lemování; `KRYTINA = True`)
2. `05_constructions/stavby/Palac_Kovarna_Stena.py`
3. `05_constructions/stavby/Palac_Kovarna_Okap.py`

Výheň se neměnila. Nové meshe nejsou (dílce stěny, žlab, rozsochy a sud už v projektu jsou).

## Další kroky

1. Ověřit v UE krytinu s prostupem komína, lemování, stěnu z proutí a okap se sudem.
2. Krok 4: rozmístění vybavení (`loose`) a úklid suti ve východní místnosti (suť teď leží i pod výhní).
3. Před stavbou domu přepočítat koruny `Palac_J` v `navrh_palac_obydli_stred.md` (zeď je o 0,31 m níž).
