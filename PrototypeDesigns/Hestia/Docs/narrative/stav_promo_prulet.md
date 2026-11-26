---
# orchestrace
type: state
validity: valid
updated: 2026-11-26
aliases: []
# hra
domain: narrative
category: [cutscene]
entity: "[[Cinematics_Lapikus]]"
depth: 4
build_step: cinematics
assets: []
---
# Stav: promo průlet kamery kolem hradu

## Souhrn
Podle návrhu [[navrh_promo_prulet_kamery]] jsou připravená data záběrů (`Lapikus/cinematics/promo_prulet.json`) a skript `Lapikus/cinematics/build_sequence.py`, který v editoru postaví `LS_Promo_Prulet` (7 záběrů, 80 s, 30 fps). **Skript v UE 5.8 doběhl (4. běh, 2026-11-26), sekvence se postavila bez chyby; vzhled zatím neověřen**; mimo editor prošel kontrolou syntaxe a výpočtem klíčů (časování, oblet, jeřáb, vertigo). Hodnoty záběrů jsou odhady z návrhu; výšky terénu, koruny věže a rozměry místností se ladí v UE.

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
První běh v editoru (Jirka, 2026-11-25, log): skript doběhl, ale všech 7 záběrů selhalo na `'MovieScene3DTransformSection' object has no attribute 'get_channels'` (a stejně `MovieSceneFloatSection`); sekvence tedy bez klíčů. Oprava: pomocná funkce `channels()` (`get_all_channels` s návratem na `get_channels`), explicitní nastavení polohy po spawnu a plný traceback chyby v logu. Druhý běh (2026-11-26): `get_channels` už prošlo, všech 7 záběrů pak selhalo na `unreal.SequenceTimeUnit` (v UE 5.8 přejmenováno); klíče se nově přidávají s výchozí jednotkou (`addkey()`), interpolace linear na vytvořeném klíči. Třetí běh (2026-11-26): klíče i rigy prošly, všech 7 záběrů selhalo až na vazbě Camera Cut (`MovieSceneSequenceExtensions.make_binding_id` a `get_binding_id` v 5.8 neexistují); nově `binding_id()` zkouší `seq.make_binding_id` a zálohu přes GUID. Čtvrtý běh (2026-11-26): všech 7 záběrů „hotovo“ (21, 21, 25, 25, 29, 17 a 22 klíčů), `LS_Promo_Prulet` uložena; vzhled, pohyb rigů a kolize zatím vizuálně neověřeny.
### V levelu (report z UE)
Bez reportu.
### Vizuálně ověřeno (kdo, kdy)
Zatím nikdo.

## Postup v UE (Jirka)
Podrobnější stejný postup: [[cinematics]] (*Spouštění*). Pasti API: [[Pasti_sequencer_python]].

**A. Příprava scény**
1. Otevřít level `/Content/Skvt/LapikusPrototypeMap`, scéna postavená (zřícenina, stavby, les).
2. `05_constructions/stavby/Etapa.py`: přepsat `ETAPA = 2` a spustit (*Tools → Execute Python Script*). Po každém buildu staveb znovu.
3. Slunce a atmosféra ručně: zlatá hodina, slunce nízko od západu až jihozápadu (viz `scene.sun_hint` v JSON). Kouř z komína domu a světlo a kouř výhně: pokud v levelu nejsou, záběry 5 a 6 je potřebují (otevřená otázka návrhu).

**B. Postavení sekvence**
4. *Tools → Execute Python Script* → `Lapikus/cinematics/build_sequence.py`. V Output Logu má být „Promo zaber N (…): hotovo“ pro N = 1–7 a na konci „LS_Promo_Prulet postavena“. Skript předchozí `LS_Promo_Prulet` a actory s tagem `Promo_Prulet` smaže, takže ho lze spouštět opakovaně; ruční úpravy v sekvenci, které nejsou v JSON, se ztratí.
5. V Content Browseru `/Content/Skvt/Cinematics/LS_Promo_Prulet`, dvojklik otevře Sequencer. Mají být vidět Camera Cuts (7 sekcí, 0–80 s) a ve viewportu actory `Promo_Cam_01…07`, `Promo_Rail_02/04`, `Promo_Crane_05`, `Promo_Pivot_Vez`, `Promo_Fokus_*`.

**C. Kontrola**
6. V Sequenceru zapnout zámek kamery (ikona kamery u Camera Cut) a přehrát (mezerník); skákat po záběrech a pozorovat. Kontrolovat: kamera neprochází terénem, zdí, střechou ani stromem (záběry 2, 4, 5, 6 a start záběru 7 nad domem), v záběru 4 projede obloukem brány, cíl ostření je ostrý (3–6), žádné staveniště (etapa 2), titulek ve finále má 4 s klidu.
7. Hodnoty k doladění (výšky terénu v údolí a příkopu, koruna věže, poloha kamery v kovárně, směr a výška oblětu, model jeřábu) pošli jako screenshot Sequenceru nebo jako hodnoty (poloha X, Y, Z a rotace kamery v klíči). Já je přepíšu do `promo_prulet.json` a zapíšu do *Ruční ladění*; pak skript spustíš znovu.

**D. Render (Movie Render Queue)**
8. Plugin *Movie Render Queue* zapnout (*Edit → Plugins*, restart), pak *Window → Cinematics → Movie Render Queue*.
9. *+ Render* → vybrat `LS_Promo_Prulet` (mapa `LapikusPrototypeMap`). V sloupci *Settings* otevřít nastavení a přidat:
   - *Output*: výstupní složka `{project_dir}/Saved/MovieRenders/`, rozlišení 1920 × 1080 (případně 3840 × 2160), snímkování 30 fps;
   - *Image Sequence (PNG)* nebo *Apple ProRes* (potřebuje zapnutý příslušný plugin);
   - *Anti-aliasing*: Spatial Sample Count 1, Temporal Sample Count 8, Render Warm Up Count 30;
   - *Console Variables*: `r.MotionBlurQuality 4`, případně vyšší kvalita stínů a Lumenu.
10. *Render (Local)*. Výstup je mimo git (`Saved/`). Zvuk, hudba a titulky se dělají ve střihovém programu; střihy na dobu, zoomy 3 a 5 na důraz.
11. Po renderu zkontrolovat: žádné blikání Lumenu, šum na prvních snímcích, délka 75–85 s bez prázdných snímků mezi Camera Cuts.

## Ruční ladění
Ruční úpravy v UE se přepisují do `promo_prulet.json` a sem; skript je při dalším běhu přepíše. Zatím bez záznamů.

| Záběr | Co | Hodnota | Datum | Kdo |
|---|---|---|---|---|
| – | – | – | – | – |

## Co zbývá
- Vizuální kontrola sekvence ve viewportu (kolize, rigy kolejnice a jeřábu, zaostření, zoomy) a první hodnoty do *Ruční ladění*.
- Odpovědi na otevřené otázky návrhu: výška terénu v údolí a příkopu, koruna věže (předpoklad 5 029), kouř a světlo výhně, délka a hudba, kdo staví sekvenci.
- Schválení návrhu: v návrhu je stále `validity: draft`; schvaluje GameDesigner.
- Dokumentace kroku `Steps/cinematics.md` (Spouštění, Vstupy a výstupy, Známé pasti) po prvním běhu v UE.

## Odkazy na návrh a předání
[[navrh_promo_prulet_kamery]], [[Steps/cinematics]]
