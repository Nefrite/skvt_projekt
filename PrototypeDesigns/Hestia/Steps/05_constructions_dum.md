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
entity: "[[Palac_Obydli]]"
---
# 05 Constructions – dům posádky v paláci (Palac_Obydli_*)

<!-- Část dokumentu kroku [[05_constructions]], rozděleno tematicky 2026-11-23 (G14b, předání Builderovi). -->

## Účel kroku
Data a skladba domu posádky v prostřední místnosti paláce: kámen (`stone_fill`), pec (`hearth`), krov (`pult_roof`), srub (`log_wall`) a staveniště etapy 1 (`props`). Etapy (sady actorů): [[05_constructions]] kap. 4.

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
| `/PrototypeDesigns/Lapikus/05_constructions/Ohniste_nahled.png` | data | [[Lapikus]] | – |
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
### Co je v `constructions.json`: dům posádky

**`addons` → `Palac_Obydli_Kamen`** (typ `stone_fill`, `zr_stavby\zdivo.py`, sada `base`): kamenné části domu posádky v prostřední místnosti paláce. Návrh a plán po etapách: [[navrh_palac_obydli_stred]], kap. 0.

- **Části** (`parts`): obdélník v rámu paláce (`a` = s, `c` = n), vrch `top` v m nad terénem v bodě `ref`, mezery `gaps` (dveře).
  - `W`, `E`: srovnání korun `Palac_pricka_1` a `_2` na 1,4 m v celé tloušťce 0,8 m, včetně zazdění jejich dveří.
  - `N`: podezdívka severní srubové stěny (osa n = 6,2; 0,45 × 0,45 m), vchod s = 13,8–14,8 volný.
  - `P`: podezdívka srubové příčky (osa s = 15,75), dveře n = 3,3–4,3 volné.
- **Kámen** (`stone`): jako ve zdech hradu, řady 25–40 cm, kusy 35–60 cm, přes tloušťku po 0,42 m (`row`), spáry 1,5 cm, 10 cm v zemi (`sink`). Spodek každého kamene kopíruje zříceninu pod ním (po 5 cm podél zdi, kameny se v místě skoku dělí); kde zeď chybí, stojí zdivo na terénu.
- **Maltové jádro** (`mortar`, 6 cm, kostky s materiálem `MI_RuinCore`, v Outlineru `Palac_Obydli_Kamen_Malta_Base`): vyspravení staré zdi. Jde v ose zdi od země až 2 cm pod vrch přes nové zdivo i přes zříceninu pod ním (líc i jádro; kde jádro chybí, vyplní dutinu mezi líci), spáry a mezery do 12 cm překlene, ve dveřích a ve větší díře není. Počítá se po 5 cm podél zdi a sousední kroky se slučují do velkých kusů. Zdí neprosvítá.
- **Suť** v domě a na zápraží je uklizená (`clear_poly`, platí pro `Sut.py`).
- **`Palac_Obydli_Ohniste`** (typ `hearth`, sada `base`, `stage_top` = `final`): od 16. 11. 2026 pec s nístějí u jižní zdi ve světnici (návrh kap. 0.5b). Uhlí pod plotnou (box `U`) má od 21. 11. 2026 `top`, je tedy v sadě `final`. Nové klíče `hearth`: `walls[].base` (zídka stojí na stole, ne na zemi), `dome` (hliněná klenba, mesh `SM_RuinOvenDome`, `tools\meshes\mesh_wattle.py`), `boxes` (kvádry: železo `iron`, uhlí `charcoal`; s `top` patří do sady `stage_top`, s `loose` je kvádr samostatný actor: plotna), `props` (hotový mesh jako samostatný actor: poklop ústí `SM_RuinOvenDoor`, `tools\meshes\mesh_props.py`), `flue` (sopouch, mesh komína). Kovárna je nepoužívá. Rozměry: `palac_spec.py` → `D_OVEN`.
- **Rozměry:** `tools\ruin\palac_spec.py` (`D_*`, funkce `obydli`). **Kontrola a náhled:** `run_checks.py --only obydli`, `preview3d.py obydli <out.png> [--stage 1|2]`.
- **`Palac_Obydli_Krov`** (typ `pult_roof`, 16. 11. 2026, zatím bez krytiny): spád k severu (`axis = "v"`), tři podpory. Nové klíče `pult_roof`: `pieces` (trám z více kusů, každý se svou sadou etapy), `stubs` (špalek pod trámem na zdi nebo srubu), `virtual` (podpora patří jiné stavbě, tady jen určuje sklon: vrchní trám srubu), `rafters.stages` (sada pro každou krokev), `pre_laths` (latě na krokvích už v kostře). Kovárna je nepoužívá, její data se nezměnila.
- **`Palac_Obydli_Srub`** (typ `log_wall`, `zr_stavby\srub.py`, 16. 11. 2026): stěna = seznam hranic řad `z`, úseky `segs` (rozsah řad, rozsah délky, volné zhlaví, sada etapy), otvory zarovnané na řady, řady v `half` jsou půltrámy (posun o půl řady proti křížící stěně → střídání v nároží). Kulatina je o `lap` tlustší než řada, zdí neprosvítá. Prkenné štíty (`gables`) sahají pod vrch krokví střechy `roof`, s výřezy pro pozednici a vaznici. Rozměry: `palac_spec.py` → `D_PLATE`, `D_PURLIN`, `D_RAFTER`, `D_LOG`, `D_WINDOWS`, `D_GABLE`, `D_STAGE_S`.
- **`Palac_Obydli_Stavenisko`, `_Kulatina`, `_Tramy`, `_Prkna`** (typ `props`, sada `site`, 21. 11. 2026): staveniště etapy 1 ([[navrh_palac_obydli_stred]] kap. 9.2, 9.2a). První stavba má vzpěry V1–V4 a žebřík, ostatní jsou hranice materiálu na nádvoří: S3 srubová kulatina, S4 krokve, pozednice a vaznice, S5 prkna krytiny, S6 (`_Kozy`) kozy do X s rozpracovanou kulatinou (tvar `peeling`) a pruhy kůry (jedna vyšší hranice, původní dvě `D_SITE` → `boards.variant = "two"`). Vzpěry a žebřík jsou samostatné actory. Hranice mají v datech `"pile": true`: celá stavba je jeden actor (Instanced Static Mesh) s pivotem dole uprostřed a tagem `pile:<stavba>`. Posun a natočení kolem svislé osy v levelu uloží capture (`Palac_Obydli_Stavenisko_Capture.py`) do `constructions_edits.json` → `moved["pile:<stavba>"] = [x, y, z, roll, pitch, yaw]` a build pak posune a natočí celou hranici (náklon se nebere). Výchozí polohy jsou v `palac_spec.py` → `D_SITE`. Volitelný parametr `pivot` v `zrlib/ue_actors.place_ism` postaví ISM actor v daném bodě (instance zůstávají ve světě); ostatní stavby ho nepoužívají. Délky a počty kusů počítá `obydli_stavenisko()` z dat sady `final`. Suť pod hranicemi uklízí `clear_poly`. Nové klíče typu `props`: `ref` (bod, od jehož terénu se měří všechny výšky kusu, aby hranice ležela na jedné výšce) a `loose` (výchozí `true`). Hranoly a prkna jsou dílce dřeva bez `shape` s `size` (mesh `SM_RuinTimber` / `SM_RuinPlank` podle poměru stran). Kontroly etapy 1 jsou v `run_checks.py --only obydli`.
- **Přepnutí etapy v editoru:** `stavby\Etapa.py` (`ETAPA` 1 / 2 / 0, `JEN` = jen stavby s daným začátkem jména) zobrazí a skryje actory podle tagu `stage:<sada>` (editor, hra i kolize). Build staví vždy všechny sady viditelné, po buildu se pouští znovu.
- **Spuštění v UE:** celý dům `stavby\Palac_Obydli.py` (všechny hotové části v pořadí, se `SUT = True` i suť). Nová část domu se přidá do jeho seznamu `STAVBY`.

## Dopad na dokumentaci
Změna dat nebo typu stavby: aktualizuj tento dokument a stavový dokument entity (`stav_*`).

## Známé pasti
Viz `KnowHow/Pasti_*` (tematické seznamy pastí).
