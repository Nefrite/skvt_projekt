---
# orchestrace
type: design
validity: valid
derived_from:
alternative_to: []
updated: 2026-11-26
aliases: []
# hra
domain: narrative
category: [cutscene]
entity: "[[Cinematics_Lapikus]]"
depth: 3
build_step:
assets: []
---
# Návrh: promo video – průlet kamery kolem hradu

## Souhrn
Průlet kamery kolem zříceniny Lapikus pro promo video kurzu, asi 80 s v sedmi záběrech: údolí → podél útesu → oblet věže → přes příkop branou → nádvoří a dům → kovárna → odlet nad ostrohem. Zoomy: najetí teleobjektivem v záběrech 1, 3 a 5, vertigo (dolly zoom) v oblouku brány.
- **Stav scény:** jeden stav bez střídání etap, etapa 2 (dům hotový, kouř z komína); `Etapa.py` s `ETAPA = 2`.
- **Záběry a souřadnice:** *Návrh*, tabulka záběrů (UE cm, plošina Z = 3129).
- **Jak se to staví a natáčí:** *Souhrn specifikace* (Level Sequence, CineCamera, rig, Movie Render Queue).
- **Ověřit:** výšky terénu v údolí a příkopu, výšku koruny věže (*Otevřené otázky*).

## Zadání / záměr
- **Odkud:** Jirka, 25. 11. 2026.
- **Účel:** promo video ke kurzu *Game design pro začátečníky*. Divák má během minuty a půl poznat místo (hrad na ostrohu nad potokem), jeho hlavní části a to, že v ruině zase někdo žije.
- **Rozsah:** jen kamera, světlo a render. Ve scéně se nic nemění, natáčí se postavený level.

## Výchozí stav
Polohy jsou ze zdí v `03_ruin/blocks/ruin_layout.json` (souřadnice UE v cm, výška plošiny Z = 3129; terén v levelu se může lišit). Kladné Y je jih (útes a potok), záporné sever (nádvoří, hradba), X roste k východu.

| Místo | Poloha (X, Y) | Poznámka |
|---|---|---|
| Špička ostrohu, západní budova | X −4100 až −3400; Y −1800 až −650 | nízké zdi, branka na západ |
| Palác, jižní zeď nad útesem | X −2350 až 770; Y −50 až −750 | okna nad útesem |
| Dům posádky (prostřední místnost) | střed (−895, −734) | komín 5,3 m nad terénem |
| Průchod v `Palac_S` | (−997, −1326) | z nádvoří do domu |
| Kovárna (východní místnost) | asi (200, −1030) | výheň |
| Věž | střed (1189, −1406), 11 × 11 m | předpoklad: koruna asi 19 m nad plošinou (lore 17–21 m) |
| Nádvoří | střed asi (−800, −2300) | |
| Brána | střed asi (2350, −2830) | před ní pilíře mostu X 3190 a 3590, příkop na východ |

## Návrh
**Stav scény:** etapa 2 (`base` + `final`), bez staveniště. Den v létě, zlatá hodina (slunce nízko od západu až jihozápadu), kouř z komína domu a z výhně.

### Záběry
| # | Čas | Záběr | Kamera: start → konec (X, Y, Z cm) | Objektiv a pohyb |
|---|---|---|---|---|
| 1 | 0–10 s | **Úvod z údolí.** Hrad na ostrohu nad meandrem potoka | (−400, 12000, 3629) → (−400, 6000, 4329), cíl věž | zoom 85 → 50 mm během najetí, plynulé zpomalení na konci |
| 2 | 10–20 s | **Podél útesu.** Boční jízda pod jižní zdí paláce s okny | (−4500, 1500, 3200) → (1800, 1500, 3500), pohled na sever | 35 mm, rychlost asi 6 m/s, končí u paty věže |
| 3 | 20–32 s | **Oblet věže** o 270° se stoupáním | kolem (1189, −1406), poloměr 2500 cm, Z 3929 → 5729 | 35 mm; posledních 1,5 s rychlý zoom 35 → 100 mm na plachtu hlídky |
| 4 | 32–44 s | **Přes příkop branou.** Nízko nad pilíři mostu, skrz oblouk | (6500, −2900, 3279) → pilíře (X 3590, 3190) → (1700, −2900, 3300) | vertigo v oblouku: kamera jede vpřed, zoom 50 → 24 mm tak, aby oblouk držel velikost v obraze |
| 5 | 44–58 s | **Nádvoří a dům.** Jeřáb ze středu nádvoří nahoru, pak najetí k průchodu | (−800, −2300, 3300) → Z 4029 → (−997, −1326, 3400) | 35 mm, na konci zoom 35 → 85 mm na komín s kouřem |
| 6 | 58–66 s | **Vložka: kovárna.** Pomalý posun kolem výhně | kolem (200, −1030, 3300), posun asi 1,5 m | 85–100 mm, clona f/2,8, ostření na výheň |
| 7 | 66–80 s | **Finále.** Odjezd nahoru nad útes, otočka k západu, celý ostroh a meandr | (−895, −734, 3800) → (−400, 8000, 7100) | 28 mm; posledních 4 s bez pohybu kamery kvůli titulku |

- **Střih:** 1–2 a 6–7 navazují rozjezdem, mezi 2–3, 3–4, 4–5 a 5–6 je tvrdý střih. Na hudbu: střihy na dobu, zoomy 3 a 5 na důraz.
- **Pohyb:** klíčové snímky s plynulými křivkami (auto/ease), žádné trhnutí; v záběrech 2 a 4 konstantní rychlost na kolejnici.
- **Zaostření:** sleduje cíl záběru (věž, oblouk brány, komín, výheň); v záběrech 1, 2 a 7 hyperfokálně (f/8).

## Souhrn specifikace
**Co v UE vytvořit** (složka `/Content/Skvt/Cinematics/`, předpoklad názvů):

| Asset / actor | Účel |
|---|---|
| `LS_Promo_Prulet` (Level Sequence) | celé video; záběry jako Camera Cuts, případně podsekvence `LS_Promo_01`–`07` |
| `CineCameraActor` (jedna nebo jedna na záběr) | Filmback 16:9 (Digital Film nebo 36 × 20,25 mm), ohnisko a ostření v klíčích |
| `CameraRig_Rail` | záběry 2 a 4: spline kolejnice, klíčuje se `Current Position on Rail` 0 → 1 |
| `CameraRig_Crane` | záběr 5: výška ramene a natočení |
| prázdný actor `Promo_Pivot_Vez` v (1189, −1406, Z koruny) | záběr 3: kamera je k němu připojená ve vzdálenosti 2500 cm, klíčuje se natočení pivotu 0 → 270° a jeho výška |
| cíle ostření (prázdné actory nebo přímo actor věže, brány, komína) | `Focus Method: Tracking` |

**Spuštění a natočení:**
1. Otevřít level `/Content/Skvt/LapikusPrototypeMap` a postavit scénu běžně (zřícenina, stavby, les).
2. **Tools → Execute Python Script →** `05_constructions/stavby/Etapa.py` s `ETAPA = 2` (zobrazí `base` + `final`, skryje staveniště). Po každém buildu staveb spustit znovu, actory se po buildu zobrazí všechny (`ETAPA = 0` by ukázala i staveniště).
3. Otevřít `LS_Promo_Prulet` v Sequenceru, náhled tlačítkem *Pilot / Camera Cut* (zámek kamery) a přehráním; kolize kamery s terénem kontrolovat ve viewportu.
4. Render: **Window → Cinematics → Movie Render Queue** (plugin *Movie Render Queue* zapnout v Plugins), přidat `LS_Promo_Prulet`, nastavení:
   - výstup PNG sekvence nebo Apple ProRes, 1920 × 1080 (případně 3840 × 2160), 30 fps;
   - *Anti-aliasing*: Spatial 1, Temporal 8 (hladší pohyb a méně šumu Lumenu), *Warm Up Frames* 30;
   - *Console Variables*: `r.MotionBlurQuality 4`, případně vyšší kvalita stínů a Lumenu;
   - výstup do `Saved/MovieRenders/` (mimo git).
5. Zvuk a titulky se dělají ve střihovém programu, ne v UE.

## Vazby a závislosti
- Scéna musí být postavená a zkontrolovaná: zřícenina (03), stavby (05) a les (04). Natáčí se postavený stav; když se později změní stavby, stačí sekvenci přerenderovat, pokud se nepohnou cíle ostření.
- Kamera se nesmí dotknout terénu, zdí ani korun stromů (hlavně záběry 2, 4 a 5).
- Kouř a světlo výhně: pokud v levelu nejsou, záběry 5 a 6 je potřebují (předpoklad: Niagara kouř u komína domu a u výhně, světlo výhně).

## Ověření
- Celé video má 75–85 s, střih je bez prázdných snímků mezi Camera Cuts.
- V žádném snímku kamera neprochází terénem, zdí, střechou ani stromem; v záběru 4 projede obloukem brány celá.
- Etapa 2: v žádném záběru není vidět staveniště (vzpěry, žebřík, hranice dřeva na nádvoří).
- Zoomy: v záběru 4 drží oblouk brány velikost v obraze (± 10 %), v záběrech 3 a 5 je cíl po zoomu ostrý.
- Titulek ve finále má aspoň 4 s klidného obrazu.
- Render bez blikání Lumenu a bez šumu na prvních snímcích (warm up).

## Otevřené otázky
- [ ] Výška terénu v údolí pod útesem a v příkopu před branou: záběry 1, 2 a 4 mají Z odhadnuté; upravit podle levelu. — Architect, 2026-11-25
- [ ] Výška koruny věže v datech (předpoklad 19 m) pro záběr 3. — Architect, 2026-11-25
- [ ] Jsou v levelu kouř z komína a světlo výhně, nebo je dodá Furnisher / Crafter? — Architect, 2026-11-25
- [ ] Délka a hudba: drží 80 s, nebo kratší verze (30 s: záběry 1, 3, 4, 7)? — Architect, 2026-11-25
- [x] Kdo sekvenci postaví v Sequenceru (předání s `for_role`). — Architect, 2026-11-25 → ScreenWriter; návrh schválen dodatečně po první realizaci (GameDesigner 2026-11-26), dál se upřesní podle ověření v UE ([[stav_promo_prulet]]).
