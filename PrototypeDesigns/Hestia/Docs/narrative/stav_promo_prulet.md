---
# orchestrace
type: state
validity: valid
updated: 2026-11-25
aliases: []
# hra
domain: narrative
category: [cutscene]
entity: "[[Lapikus]]"
depth: 4
build_step: cinematics
assets: []
---
# Stav: promo průlet kamery kolem hradu

## Souhrn
Podle návrhu [[navrh_promo_prulet_kamery]] jsou připravená data záběrů (`Lapikus/cinematics/promo_prulet.json`) a skript `Lapikus/cinematics/build_sequence.py`, který v editoru postaví `LS_Promo_Prulet` (7 záběrů, 80 s, 30 fps). **V Unrealu zatím nic neběželo**: skript prošel jen kontrolou syntaxe a výpočtem klíčů mimo editor (časování, oblet, jeřáb, vertigo). Hodnoty záběrů jsou odhady z návrhu; výšky terénu, koruny věže a rozměry místností se ladí v UE.

## Co je hotové
- Data záběrů všech 7 záběrů podle tabulky v návrhu (časy, polohy, objektivy, clony, zaostření) v `promo_prulet.json`; jediný zdroj hodnot.
- `build_sequence.py`: `LS_Promo_Prulet` v `/Content/Skvt/Cinematics/` (v Pythonu `/Game/Skvt/Cinematics`), na záběr jedna `CineCameraActor` (Filmback 36 × 20,25 mm, 16:9) a Camera Cuts; `CameraRig_Rail` (záběry 2, 4), pivot `Promo_Pivot_Vez` (záběr 3), `CameraRig_Crane` (záběr 5), cíle ostření `Promo_Fokus_*` (Tracking u záběrů 3–6, ruční vzdálenost u 1, 2 a 7).
- Klíče po 0,5 s s lineární interpolací z hladkých křivek (`ease` v datech): žádné trhnutí, konstantní rychlost na kolejnici (záběr 2: asi 6,3 m/s, záběr 4: 4 m/s).
- Kamery, rigy a cíle mají tag `Promo_Prulet`; opakovaný běh je smaže a postaví znovu spolu se sekvencí.

## Souhrn specifikace
Spec je v návrhu (*Souhrn specifikace*) a v datech `promo_prulet.json` (klíče `shots[*]`); skript čte jen data. Změna hodnot = změna JSON a nový běh skriptu.

## Co se liší od návrhu (a proč)
Návrh jsem neupravoval. Rozdíly a doplnění, o kterých má rozhodnout GameDesigner (návrh):
- **Záběr 1: „najetí“ vs. 85 → 50 mm.** Souhrn jmenuje najetí teleobjektivem v záběrech 1, 3 a 5, ale tabulka má v záběru 1 85 → 50 mm (to je oddálení). V datech jsou hodnoty z tabulky.
- **Záběr 4: vertigo.** Úběh ohniska 50 → 24 mm drží velikost oblouku jen na prvním úseku jízdy (ohnisko je úměrné vzdálenosti od oblouku: 24 mm je při vzdálenosti 2 000 cm, tj. v čase asi 37,5 s, dál se drží 24 mm). Úplné vertigo až do oblouku (vzdálenost → 0) by potřebovalo ohnisko → 0. V datech: `zoom_law` vertigo s `f_min` 24.
- **Záběr 3: směr oblětu** návrh neurčuje. Zvolil jsem start východně od věže (nad příkopem), oblet S → V → J přes sever a západ a konec jižně od věže (plachta hlídky je na `Vez_J`); poloměr 2 500 cm, výška 3 929 → 5 729. Západní strana je u zdi `Palac_S` (Y asi −1 326), kamera je tam už vysoko; ověřit.
- **Záběr 5: model jeřábu.** Pozice kamery = rig + (L cos p, 0, L sin p), L = 1 000 cm, rameno ve směru X, orientace kamery z klíčů (zámek natočení hlavy). Přesný offset montáže v `CameraRig_Crane` neznám, ladí se po prvním běhu.
- **Záběr 6, 7: odhady.** Kamera v kovárně a start finále nad domem nemají v návrhu rozměry místností ani výšku střechy; hodnoty jsou odhad (viz *Ruční ladění*).
- **Zaostření** ve 3–6 je Tracking na prázdný cíl (`TargetPoint`), ne na actor věže, brány, komína nebo výhně; polohy cílů jsou v datech (`focus.target_pos`).

## Ověřeno v UE
Nic. Skript v editoru nebyl spuštěn a výstup nebyl vidět.
### V levelu (report z UE)
Bez reportu.
### Vizuálně ověřeno (kdo, kdy)
Zatím nikdo.

## Postup v UE (Jirka)
1. Otevřít level `/Content/Skvt/LapikusPrototypeMap`, postavit scénu běžně.
2. `05_constructions/stavby/Etapa.py`: v souboru přepsat `ETAPA = 2` a spustit (*Tools → Execute Python Script*). Po každém buildu staveb spustit znovu.
3. Spustit `Lapikus/cinematics/build_sequence.py` (*Execute Python Script*); v Output Logu hledat „Promo zaber N … hotovo“ a případně „selhal“.
4. Otevřít `LS_Promo_Prulet` v Sequenceru, zamknout kameru (Camera Cut), přehrát a projít všech 7 záběrů; kolize se zdí, střechou, terénem a stromy kontrolovat ve viewportu.
5. Slunce a kouř/světlo ručně (zlatá hodina, kouř z komína a výhně).
6. Render: *Window → Cinematics → Movie Render Queue* podle návrhu (1920 × 1080, 30 fps, Temporal 8, Warm Up 30, `r.MotionBlurQuality 4`, výstup `Saved/MovieRenders/`).

## Ruční ladění
Ruční úpravy v UE se přepisují do `promo_prulet.json` a sem; skript je při dalším běhu přepíše. Zatím bez záznamů.

| Záběr | Co | Hodnota | Datum | Kdo |
|---|---|---|---|---|
| – | – | – | – | – |

## Co zbývá
- První běh v UE a oprava rozdílů API (nový Sequencer API podle verze 5.8).
- Odpovědi na otevřené otázky návrhu: výška terénu v údolí a příkopu, koruna věže (předpoklad 5 029), kouř a světlo výhně, délka a hudba, kdo staví sekvenci.
- Schválení návrhu: v návrhu je stále `validity: draft`; schvaluje GameDesigner.
- Dokumentace kroku `Steps/cinematics.md` (Spouštění, Vstupy a výstupy, Známé pasti) po prvním běhu v UE.

## Odkazy na návrh a předání
[[navrh_promo_prulet_kamery]], [[Steps/cinematics]]
