---
# orchestrace
type: step
validity: valid
aliases: []
step_kind: build
updated: 2026-11-23
# hra
build_step: 05_constructions
domains: [structures]
entity: "[[Palac_Kovarna]]"
---
# 05 Constructions – kovárna v paláci (Palac_Kovarna_*)

<!-- Část dokumentu kroku [[05_constructions]], rozděleno tematicky 2026-11-23 (G14b, předání Builderovi). -->

## Účel kroku
Data a skladba kovárny ve východní místnosti paláce: přístřešek (`pult_roof`), výheň (`hearth`), stěna z proutí (`wattle_wall`), kůl (`props`) a okap (`gutter`). Přenosné vybavení je v [[06_furnishing]].

## Spouštění
Jednotlivé stavby: `05_constructions\stavby\<Stavba>.py`; celý postup v UE a co kdy přegenerovat: [[05_constructions]] (kap. 2 a 3).

## Skripty
<!-- hestia:generated:start -->

| Skript | Role | Entity | Dokumenty |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_postel_nahled.png` | data | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_stojan_brneni_nahled.png` | data | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Guesthouse_truhla_nahled.png` | data | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Knihovna_meshe_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Knihovna_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Kulatina_meshe_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Kulatina_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Props_kovarna_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Props_textury_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_luzko_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_luzko_slozena_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_plachta_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_truhlicka_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stan_vak_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_prikop_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_straz_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_straz_nahled_etapa1.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_drevo_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_nadvori_stan_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_dostavba_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_podlaha_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_tramovi_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_kovarna_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_obydli_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_obydli_nahled_etapa1.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_vez_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_vez_pristresek_nahled.png` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/build_constructions.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/constructions.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/constructions_edits.json` | data | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana.py` | entry | [[Brana]] | [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Capture.py` | entry | [[Brana]] | [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Most.py` | entry | [[Brana]] | [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Most_Kamen.py` | entry | [[Brana]] | [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz.py` | entry | [[Brana_Straz]] | [[navrh_brana_straz]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kamen.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Kryty.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Straz_Podesta.py` | entry | [[Brana_Straz]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Brana_Zataras.py` | entry | [[Brana]] | [[navrh_brana_prikop]], [[stav_brana]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Etapa.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Nadvori_Stan.py` | entry | [[Nadvori_Stan]] | [[navrh_nadvori_stan]], [[05_constructions]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Nadvori_Stan_Capture.py` | entry | [[Nadvori_Stan]] | [[navrh_nadvori_stan]], [[05_constructions]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Dostavba.py` | entry | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Krov.py` | entry | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Ostroh_Podlaha.py` | entry | [[Guesthouse]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Kul.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Okap.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Pristresek.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Stena.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Kovarna_Vyhen.py` | entry | [[Palac_Kovarna]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli.py` | entry | [[Palac_Obydli]] | [[navrh_palac_obydli_stred]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Kamen.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Krov.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Ohniste.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Srub.py` | entry | [[Palac_Obydli]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Stavenisko.py` | entry | [[Palac_Obydli]] | [[navrh_palac_obydli_stred]], [[stav_palac_obydli]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Palac_Obydli_Stavenisko_Capture.py` | entry | [[Palac_Obydli]] | [[navrh_palac_obydli_stred]], [[stav_palac_obydli]] |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Sut.py` | entry | [[Lapikus]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez.py` | entry | [[Vez]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez_Patra.py` | entry | [[Vez]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Vez_Pristresek.py` | entry | [[Vez_Pristresek]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/__init__.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/dostavba.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/krov.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/kryty.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/ohniste.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/okap.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/podesta.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/podlaha.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/pristresek.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/pult.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/srub.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/stan.py` | library | [[Nadvori_Stan]] | [[navrh_nadvori_stan]], [[05_constructions]] |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/stena.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/vez.py` | library | [[Vez]] | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/vybaveni.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/05_constructions/zr_stavby/zdivo.py` | library | – | – |
| `/PrototypeDesigns/Lapikus/tools/constructions/check_tower.py` | generator | – | – |
| `/PrototypeDesigns/Lapikus/tools/constructions/gen_constructions.py` | generator | – | – |

<!-- hestia:generated:end -->

## Vstupy a výstupy
### Co je v `constructions.json`: kovárna

**`frames` → `Palac_Kovarna_Pristresek`** (typ `pult_roof`, `zr_stavby\pult.py`): přístřešek kovárny ve východní místnosti paláce, v koutě mezi `Palac_J` a věží (`Vez_Z`). Návrh: [[navrh_palac_kovarna]]. Kostra, krytina s prostupem komína a lemování.

- **Rám stavby:** `origin`, `u`, `v` = rám paláce z `palac_spec.py` (`s` podél `Palac_J` k věži, `n` k severu), rozměry v metrech. `axis` = osa, po které střecha padá (`"u"`: spád k západu). Výšky se počítají od terénu v bodě `ref` (střed přístřešku).
- **Podpory** (`supports`): pozednice kolmé na spád, každá s polohou `at`, rozsahem `span`, vrchem `top`, průřezem `sec` a sloupy (`posts`, `post`).
  - `VE` u věže: 20 × 20 cm, vrch 4,24 m (spodek na spáře řad `Palac_J`, kapsa se zarovnává na řady). Jižní konec je 0,3 m v kapse `Palac_J` (03, `kapsa` z `palac_spec.py`), dál na sloupech n = 4,4 (mezi měchy a brusem) a 6,2, 10 cm od líce věže. V koutě sloup není, stojí tam výheň. Pozednice sahá do n = 6,4.
  - `VW` na západě: 18 × 18 cm, vrch 2,5 m, 3 sloupy (n = 0,9 / 3,55 / 6,2, rovnoměrně) v s = 25,85, těsně východně od výklenku střílny s = 25.
- **Patní kameny** (`pads`): plochý kámen z rozvalin 36 × 36 × 14 cm pod každým sloupem, 4 cm v zemi. Jsou to **samostatné actory** (`Palac_Kovarna_Pristresek|VE|K0` …), dají se ručně doladit a uložit přes `MODE = "capture"`.
- **Krokve** (`rafters`): 7 ks loupané kulatiny Ø 16 cm (`SM_RuinLog`), n = 0,9 až 6,3 po 0,9 m (rozšíření o řadu krokví k severu (Jirka 16. 11. 2026); krytina do n = 6,6), od s = 30,65 (10 cm před lícem věže) po s = 24,95 (přesah 0,9 m za západní pozednici; pod ním bude zvenku u stěny hranice dřeva). Sklon 20,3°, osedlání 3 cm (`seat`). Typ umí i hraněné krokve (`sec` místo `d`) a víc než dvě podpory (dům posádky).
- **Dřevo:** všechno `raw` (nad výhní žádný dehet).
- **Prostup komína** (`openings`): střed s = 30,0; n = 1,35 (mezi krokvemi n = 0,9 a 1,8), strana 0,5 m; vůle 12 cm od krokví, 20 cm od pozednice. Krytina kolem něj má mezeru 3 cm (`hole_gap`).
- **Krytina** (`roof`, 15. 11. 2026): stejná skladba jako u ostrohu, ale vlastní kód (`pult._pult_cover`): krokve jsou rovnoběžné, takže latě jdou přes celou šířku a prkna nejsou rozdělená do polí mezi trámy.
  - **latě** 6 × 5 cm napříč krokvemi (9 řad): u horního konce krokví, u okapu, těsně nad a pod prostupem komína, mezi nimi nejvýš po 0,9 m (`lath_step`);
  - **prkna** 3,5 cm, šířka 22–30 cm, spára 1,5 cm, po spádu od líce věže (mezera 0,5 cm) po okapovou hranu s = 24,85 (10 cm za konci krokví, `eave_over`, nad osou žlabu). Pásy se kladou od okrajů prostupu ven, prkna nad prostupem jsou rozdělená;
  - **lišty** 10 × 3,5 cm přes každou spáru, nahoře končí pod lemováním;
  - **od líce `Palac_J` mezera 3,5 cm** (`side_gap`): kameny koruny v s = 27–29 leží v úrovni střechy a vystupují z líce o 1–3 cm;
  - vrch krytiny: okap 2,36 m, u komína 4,27 m, u věže 4,54 m nad terénem. Pokrytí půdorysu mimo prostup 99,2 % (zbytek jsou mezery u zdí).
- **Lemování** (`flashing`): prkno 3,5 × 25 cm na stojato na krytině podél věže (horní okraj, 0,5 cm od líce) a podél `Palac_J` (na hraně krajního prkna).
- **Rozměry** jsou v `tools\ruin\palac_spec.py` (konstanty `K_*`, krytina `K_ROOF`, lemování `K_FLASH`). Po změně přegeneruj `gen_constructions.py`; když se mění východní pozednice (kapsa), i `gen_layout.py` a postav část `Palac`.
- **Kontrola a náhled:** `tools\checks\run_checks.py --only palac`, `tools\checks\preview3d.py kovarna <out.png>`.

**`addons` → `Palac_Kovarna_Vyhen`** (typ `hearth`, `zr_stavby\ohniste.py`): výheň v koutě mezi `Palac_J` a věží pod přístřeškem kovárny. Rám a výšky jako u přístřešku (`roof` = jméno střechy).

- **Stůl** (`table`): kámen z rozvalin, s = 29,75–30,73; n = 0,72–1,9 (2 cm od líce věže i `Palac_J`); výška 0,75 m ve 3 řadách, kameny střídavě podél a napříč. Nahoře hliněný maz 4 cm (`daub`, kostky s materiálem `MI_RuinDaub`).
- **Ohniště** (`pit`): 0,4 × 0,4 m pod komínem (střed s = 30,0; n = 1,35), dřevěné uhlí 2 cm pod úrovní mazu (`MI_RuinCharcoal`). Žhavé uhlí a oheň zatím nejsou.
- **Boční zídka** (`walls`): severně od stolu, n = 1,9–2,2, výška 1,2 m v 5 řadách, stojí na zemi. Ve 4. řadě (0,72–0,96 m) je otvor 0,2 m pro výfučnu měchů (`hole`).
- **Dymník** (`hood`): `SM_RuinSmokeHood` 1,4 × 1,2 × 1,0 m, spodní okraj 1,9 m (17. 11. 2026), střed v ose komína, východní okraj u věže.
- **Komín** (`chimney`): `SM_RuinChimney` 0,5 × 0,5 m od vrchu dymníku (2,8 m) do 5,5 m, 1,2 m nad krytinou.
- **Výměny** (`trimmers`): 2 loupané kulatiny Ø 10 cm mezi krokvemi n = 0,9 a 1,8, v úrovni krokví, 3 cm od komína na východ a na západ. Mezi nimi bude otvor v krytině.
- **Závěsné tyče** (`hangers`): 4 loupané tyče Ø 5 cm z konců výměn k rohům spodního okraje dymníku. Dymník tak nevisí ve vzduchu.
- **Rozměry** jsou v `tools\ruin\palac_spec.py` (`K_FORGE`, `K_FORGE_WALL`, `K_HOOD`, `K_CHIMNEY`, `K_TRIMMER`, `K_HANGER`).
- Typ je obecný: bez `walls`, `trimmers` a `hangers` postaví ohniště domu (základ, dymník, komín).

**`addons` → `Palac_Kovarna_Stena`** (typ `wattle_wall`, `zr_stavby\stena.py`, 15. 11. 2026): západní stěna kovárny z proutí omazaného hlínou v linii západních sloupů přístřešku.

- **Poloha:** s = 25,85; n = 0,7–6,3 (od líce `Palac_J` po severní sloup), výška 2,1 m nad terénem, tloušťka 8 cm, 3 cm v zemi. Pod západní pozednicí zůstává volný pruh 0,22 m.
- **Dílce** `SM_RuinWattlePanel` (1 × 1 m, rovné okraje) se skalují na pole mezi sloupy, nejvýš 1,1 × 1,05 m (`tile`). Spodní pás (do vrchu patních kamenů, 0,1 m) končí u patních kamenů, výš dílce končí u sloupů (mezera 0,5 cm).
- **Kůly** (`stake`): loupané Ø 9 cm na svislých spojích dílců (zakryjí spáry), 0,3 m v zemi, 6 cm nad stěnou.
- Rozměry: `palac_spec.py` → `K_WALL`. Sloupy a patní kameny bere z přístřešku (`posts`).

**`addons` → `Palac_Kovarna_Kul`** (typ `props`, `zr_stavby\vybaveni.py`): pevný kůl s kůrou Ø 10 cm zatlučený do země zvenku pod přesahem, 1,5 m od `Palac_J` (1,5 m nad zemí, 0,4 m v zemi). Od něj vede hranice dřeva, ta je vybavení.

**Vybavení kovárny** (kovadlina, měchy s pákou, brus, ponk, truhlík, nářadí s lištou, pruty, koš, hranice dřeva) je od 16. 11. 2026 v **`06_furnishing`** (skupina `Palac_Kovarna_Vybaveni`, [[06_furnishing]]). Typ `props` (`zr_stavby/vybaveni.py`) je společný: v 05 pro pevné kusy, v 06 pro přenosné. Úklid suti v celé východní místnosti dělá `clear_poly` u `Palac_Kovarna_Pristresek` (s = 21,35–30,8; n = 0,65–8,85).

**`addons` → `Palac_Kovarna_Okap`** (typ `gutter`, `zr_stavby\okap.py`, 15. 11. 2026): žlab pod západním okapem přístřešku a sud na dešťovou vodu.

- **Žlab:** loupaný vydlabaný kmen Ø 20 cm (`SM_RuinGutter`), osa s = 24,8 (pod okapovou hranou krytiny s = 24,85); n = 0,72–6,8 (0,2 m za okraj střechy); spád k severu 2,5 % (15 cm). Vrch 12 cm pod spodkem prken na jižním konci, 27 cm na severním (2,20 → 2,05 m nad terénem). Výška se počítá z krytiny střechy `roof` (`pult.roof_layers`).
- **Rozsochy:** 3 hlavy `SM_RuinForkHead` (ramena napříč žlabem) na kůlech s kůrou Ø 12 cm (0,4 m v zemi) v n = 1,7 / 4,0 / 6,3 (rovnoměrně). Jižní rozsocha je 1 m od líce `Palac_J` (průchod postavy k výklenku střílny s = 25, Jirka 16. 11. 2026), žlab k hradbě volně přesahuje o 1 m. Žlab leží ve vidlici: osa žlabu je 28 cm (varianta A) / 26 cm (B) nad středem hlavy (`FORK_SEAT`, změřeno na OBJ pro žlab Ø 20).
- **Sud** `SM_RuinBarrel` pod severním koncem žlabu (s = 24,8; n = 6,8), **samostatný actor** (dá se doladit a uložit přes capture). Svod se nedělá, voda padá ze žlabu asi 1,3 m.
- Rozměry: `palac_spec.py` → `K_GUTTER`, `K_BARREL`. Typ je obecný (pro `Palac_Obydli_Okap`), počítá se střechou typu `pult_roof`.

## Dopad na dokumentaci
Změna dat nebo typu stavby: aktualizuj tento dokument a stavový dokument entity (`stav_*`).

## Známé pasti
Viz `KnowHow/Pasti_*` (tematické seznamy pastí).
