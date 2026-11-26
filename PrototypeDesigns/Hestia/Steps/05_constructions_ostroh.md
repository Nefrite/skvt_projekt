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
entity: "[[Ostroh]]"
---
# 05 Constructions – stavby u ostrohu (Ostroh_Krov, _Dostavba, _Podlaha)

<!-- Část dokumentu kroku [[05_constructions]], rozděleno tematicky 2026-11-23 (G14b, předání Builderovi). -->

## Účel kroku
Data a skladba staveb v obytné části u ostrohu: krov (`fan_roof`), kamenná dostavba (`stone_addon`) a prkenná podlaha (`plank_floor`).

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
### Co je v `constructions.json`: stavby u ostrohu

**`frames` → `Ostroh_Krov`** (typ `fan_roof`): krov v západní části u ostrohu.

- **Sloupy a příčka:** 2 sloupy stojí asi 1 m od vnitřního líce `ZBudova_V` v prostoru (`POST_SHIFT`), po stranách průchodu, 10 cm od jeho hran (`POST_SPREAD`). Průchod 1,6 m (`PASS_W`) zůstává volný. Na sloupech leží příčka (vaznice), 3,8 m dlouhá, s přesahem 85 cm na každou stranu. Šikmé vzpěry vedou od sloupů ven a hlavou podpírají přesahy příčky. **Příčka je hřeben střechy:** střecha od ní klesá na všechny strany.
- **Paprskovité trámy:** 7 trámů 22 × 24 cm vede z příčky na hradbu `Hradba_Z_S`.
- **Hradba:** je v tomto úseku cíleně snížená a zarovnaná, asi 3 m nad terénem, i 4 m za krajní trámy vějíře (`CAP_EXT`, pod krytinou paprskových trámů).
- **Uložení:** trámy leží ve žlábcích koruny, u vnitřního líce zhruba do poloviny výšky trámu. Svažují se ke zdi (11–17°, příčka 1,2 m nad dnem žlábků, `RISE`) a 0,6 m přesahují vnější líc (okap).
- **Dřevo:** všechno je dehtované (`finish`).
- **Rozměry:** jsou v `tools/ruin/ostroh_spec.py` a sdílí ho 03 (snížení a žlábky) i 05 (dřevo). Po změně přegeneruj `gen_layout.py` i `gen_constructions.py` a postav 03 i 05.

- **Krytina** (`roof`, všechno dehtované):
  - **Latě:** 5 řad napříč trámy.
  - **Prkna:** po spádu, 22–30 cm široká, se spárami 1,5 cm. V každém poli mezi trámy leží rovnoběžně. Krajní jsou kratší a vyplňují klín, jak se pole ke zdi rozšiřuje. Začínají už tam, kde se do pole dostane jejich vnitřní hrana, takže u trámů nezůstávají díry. Sousední pole se u trámu překrývají (každé druhé o tloušťku prkna výš).
  - **Lišty:** 10 cm široké přes každou spáru (1,5 cm), každá přesahuje spáru asi 4 cm na obě strany. Přes každý trám leží krycí prkno 36 cm, které zakryje spoj dvou polí.
  - **Lemování u příčky:** zatím není, vyřeší se jinak.
- **Koruna pod střechou:** kameny hradby mezi trámy jsou směrem ven snížené ve sklonu střechy (`roof_clear` v 03), aby nezasahovaly do latí a prken.

- **Trámy dokola příčky** (`ring`, pořadí navazuje na vějíř, `ring_closed` = pole krytiny i mezi posledním a prvním trámem):
  - `PB0–2` a `PA0–2`: paprskové trámy na koncích příčky, rovnoměrně mezi krajním trámem vějíře (B6 / B0) a směrem zpět ke `ZBudova_V` (`N_RAD`);
  - `E0–1`: 2 trámy z příčky zpět na dostavbu `ZBudova_V` nad dveřmi, mezi začátky trámů vějíře (`E_AT`, jen krajní);
  - každý končí na nejbližší zdi: na dostavbě (`ZBudova_V`, `ZBudova_S`) má sklon 14° (`SLOPE_DOST`), dlouhé trámy klesnou nejvýš 0,8 m (`DROP_MAX`, ne pod 10°). Na koruně zříceniny leží na nejvyšším kameni pod sebou (zřícenina se pro ně nesnižuje);
  - přesah 0,4 m za vnější líc (`OH_RING`). Dostavba se pod nimi sníží: uprostřed (krátké trámy `E`) nejméně, na bocích víc.
- **Sklon:** vějíř 11–17°, trámy dokola 11–14°.
- **Hřebenová prkna** (`ridge`): dvě prkna 26 cm přes příčku, na každou stranu jedno, překrývají začátky polí.
- Latě se mezi trámy s různým sklonem kladou šikmo, aby ležely na obou trámech.

Žlab, okapnice a sud přijdou později.

**`addons` → `Ostroh_Dostavba`** (typ `stone_addon`): uzavření obytné části u ostrohu. Provizorní dostavba z kamene rozvalin, jedna řada kamenů přes celou tloušťku (líc z obou stran). Zřícenina se nemění, dostavba jen stojí na koruně zdí.

| Zeď | Kde |
|---|---|
| `V` | na vnitřní polovině `ZBudova_V` (vnitřní líc v rovině líce zdi), po celé délce a přes mezeru u jižního konce až k hradbě. **Dveře** v průchodu (1,6 m, vrch 2,2 m nad terénem, nadpraží ve stejné výšce jako nadpraží okna, `align`), **okno** 3,4 m severně od dveří (k `ZBudova_S`), 1,25 m široké, parapet 1,4 m (rozměry v `ostroh_spec.py` → `WINDOW`). V místě okna je původní zeď `ZBudova_V` v 03 vybouraná nad 1,4 m (`edits` → `cut`), takže okno sahá až na korunu zříceniny (asi 1,35 m) a není zastavěné zříceninou |
| `S` | na jižní (vnitřní) polovině `ZBudova_S`, od rohu se `ZBudova_V` k hradbě |
| `H` | na vnitřní polovině hradby mezi rohy (vyrovnání koruny pod okapem mezi trámy) |

- **Kámen** (`stone`): použitý kámen z hradu, stejně velký jako ve zdech (délka a výška řad z `STONE_MIN/MAX` a `COURSE_MIN/MAX` v `ruin_layout.json`: 35–90 cm, řady 25–40 cm), tloušťka 0,45 m, spáry 1,5 cm. U koruny a u trámů jsou kusy kratší, aby dosáhly pod střechu.
- **Spodek** kopíruje korunu zříceniny pod sebou (nejvyšší kámen v místě kusu), kde zeď chybí, stojí dostavba na terénu.
- **Vrch** dosahuje pod vrch trámů (latě a prkna leží na trámech) a v místě trámu pod jeho spodek, trámy procházejí zdivem. Pod šikmým trámem se kámen koruny rozdělí přes tloušťku na tři, aby každý kus dosáhl co nejvýš (mezera pod střechou je většinou do 5 cm; poslední řada se dorovná až pod střechu, když by nad ní zbylo méně než 12 cm).
- **Malta** (`mortar`): uprostřed tloušťky zdi je 10 cm silné jádro (kostky s materiálem jádra zříceniny `MI_RuinCore`) přes všechny spáry, takže zdí neprosvítá. Ve spárách vypadá jako malta. V Outlineru `Ostroh_Dostavba_Malta`.
  - **Malta až do země** (`mortar_down` = seznam zdí, teď jen `V`): jádro pokračuje pod dostavbou ve zdi zříceniny od terénu ke koruně. Kde v jeho rovině stojí lícový kámen zříceniny, je malta v téže rovině (vidět jen ve spárách). Druhá rovina malty (6 cm) je v prostřední vrstvě zdi mezi kameny jádra (`mid_off` = odsazení osy zdi zříceniny v m), takže zdí neprosvítá ani tam, kde chybí oba líce. Malta leží jen uvnitř kamenů zříceniny a ve spárách mezi nimi (v líci do 2,5 cm podél zdi a 4 cm mezi řadami, v jádru do 4 / 6 cm, protože lomové kusy jsou různě zapuštěné), nikdy v díře ani nad kamenem. Odkrytá koruna v okně se počítá jen do půlky výšky, mírně nakloněné kusy (do 6°) jen v části, kterou zabírají celou výškou. Spára mezi korunou zříceniny a dostavbou (do 5 cm) je vyplněná taky. Malta se počítá po 5 cm sloupcích podél zdi a sousední sloupce se stejně vysokým úsekem (do 1,5 cm) se slučují do jednoho souvislého kusu, bez mezer mezi kusy. Ve dveřích není, pod oknem končí pod parapetem.
  - Malta v kusech dostavby přechází spáry k sousedním kamenům. U otvoru, na konci zdi, pod střechou a pod parapetem končí 1,5–2 cm uvnitř kamene, takže nevylézá.
- **Otvory:** vrch dveří a okna i parapet jsou zarovnané na řady kamene. Kámen pod oknem tenčí než 15 cm se nepostaví, okno pak sahá až na korunu zříceniny. Nad otvorem leží dřevěné nadpraží přes jednu řadu, 25 cm na každé straně uložené ve zdi (`lintel`), staré neošetřené dřevo (`finish` → `lintels`).
- **Nadpraží o půl řady výš** (`lintel` → `half`): spodek nadpraží je v polovině řady, vrch v polovině další řady. Pod konci nadpraží jsou poloviční kameny až k jeho spodku, nad nadpražím poloviční kameny do další řady.
- **Práh** (`threshold`): dřevěný trám ve dveřích, v linii dostavby přes celou její tloušťku a šířku průchodu. Je 5 cm v zemi (`sink`) a 1,5 cm nad podlahou (`over`, výšku bere z podlahy `floor`). Je to **samostatný actor** (`Ostroh_Dostavba|Prah`), ne instance: můžeš s ním ručně pohnout a uložit to přes `Ostroh_Dostavba.py` s `MODE = "capture"` do `constructions_edits.json`. Další build polohu zachová. Staré neošetřené dřevo (`finish` → `threshold`).
- **Suť** uvnitř obytné části je uklizená (`clear_rubble`): `Sut.py` ji tam nepostaví.
- Polohy (osy dostaveb, trámy dokola příčky, otvory) počítá `gen_constructions.py` ze zdí v `ruin_layout.json` a z `ostroh_spec.py`. Výšky (koruna, střecha) se počítají až při buildu z postavené zříceniny a krovu.

**`addons` → `Ostroh_Podlaha`** (typ `plank_floor`): prkenná podlaha v obytné části u ostrohu.

- **Obrys** (`outline`): vnitřní líce zdí zříceniny (`ZBudova_V`, `ZBudova_S`, hradba), 2 cm od nich (`inset`). Počítá ho `gen_constructions.py`.
- **Podvaly** (`sleepers`): 14 × 10 cm, napříč prkny po 0,8 m, v kusech po 1,2 m. Leží na zemi (zapuštěné 3 cm) a kopírují terén, dehtované.
- **Prkna** (`planks`): 4,5 cm silná, 22–32 cm široká, 2,4–4,5 m dlouhá, podél `ZBudova_V`, spáry 6 mm. Spoje jsou přesazené a leží vždy na podvalu. Bez úpravy, jako ve věži.
- **Výška:** spodek prken je 10 cm nad nejvyšším terénem v obrysu. V nižších místech jsou podvaly vyšší.
- Prkna i podvaly se vyříznou kolem sloupů krovu (`avoid`) a kolem kamenů zříceniny, které u paty zdí zasahují do podlahy. U oblouku hradby proto okraj podlahy nesleduje líc přesně (zuby po šířce prkna).
- **Suť:** na podlaze se nepostaví (`Sut.py`).

## Dopad na dokumentaci
Změna dat nebo typu stavby: aktualizuj tento dokument a stavový dokument entity (`stav_*`).

## Známé pasti
Viz `KnowHow/Pasti_*` (tematické seznamy pastí).
