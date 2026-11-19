---
# orchestrace
type: state
validity: valid
updated: 2026-11-19
aliases: []
# hra
domain: structures
entity: "[[Brana_Straz]]"
depth: 3
build_step: 05_constructions
assets: []
---
# Brana_Straz – stav stavby

## Co je hotové
| Část | Provedení | Sada |
|---|---|---|
| 03: kapsy v `Brana_V` | 3 kapsy 32 × 33 cm ve vnitřním líci, spodek Z 3552 (řada 3552–3585 nad obloukem) | – |
| 03: SV nároží `Brana_V` | kameny koruny nad Z 3618 v d < 0,75 posádka rozebrala (`cap`), kryt jde přes nároží bez mezery | – |
| `Brana_Straz_Kamen` (`stone_fill`) | vyrovnání koruny `Brana_J` na Z 3552 (pás u = 0,2–0,65; d = 0,9–5,3; výška 0–1,0 m), vyrovnání koruny `Brana_S` pod trámem na zdi (pás d = −0,45 až 0,05) a podložení trámů v líci `Brana_V` | `base` |
| `Brana_Straz_Podesta` (typ `platform`) | **3 trámy** z loupané kulatiny Ø 24 cm, d = 1,3 / 3,15 / 5,0; u = 0,1–6,63 (na východě 0,33 m v kapse); spodek Z 3552; **čtvrtý trám leží na koruně `Brana_S`** (d = −0,2; u = 0,1–6,2) | `base` |
| | podlaha z prken 5 cm, u = 0,2–6,27, **d = −0,55 až 5,25** (na severu až nad `Brana_S` k severnímu krytu; prkna ze dvou kusů se spárou nad trámem); **vrch Z 3581** (4,5 m nad plošinou hradu, 5,4 m nad zemí v průjezdu) | `base` |
| `Brana_Straz_Kryty` (typ `palisade`), východní | 30 kůlů s kůrou Ø 18–22 cm se špičkou nahoru na koruně `Brana_V` (u = 7,5; d = −0,6 až 5,35); vrch 1,8 m nad podlahou; 3 průzory 14 × 45 cm (d = 1,5 / 3,1 / 4,6; spodek 1,35 m), kůl v průzoru je rovně seříznutý | `base` |
| severní | 37 kůlů **u vnější hrany `Brana_S`** (d = −0,75; u = 0–7,6; za krytem se nedá stoupnout), vrch 1,25 m nad podlahou (střílí se přes vrch), 3 průzory 14 × 35 cm (u = 1,8 / 3,7 / 5,6; spodek 0,9 m) | `final` |
| jižní | 23 kůlů na jižním okraji podesty (d = 5,15; u = 2,6–7,38, tedy východní dvě třetiny, po `Hradba_V`); stojí na podlaze, na východě na koruně `Brana_V`; vrch 1,8 m, 2 průzory (u = 4,6 a 6,0) | `final` |

- **Ráhna** Ø 10 cm jsou zevnitř: jedno u spodu (východní a jižní kryt 0,55 m, severní 0,45 m nad podlahou) a druhé těsně pod průzory (1,22 m; u severního krytu 0,78 m). Přes průzory žádné nevede.
- **Kůly jsou „utopené“ 25 cm v koruně zdi** (posádka korunu vydlabala, aby lépe držely). Ve skriptech kůl do kamene jen zasahuje, kameny koruny se kvůli tomu v 03 nemění.
- **Trámy:** 3 místo 6 (Jirka 16. 11. 2026), prkna 5 cm nesou na 1,85 m.
- Východní kryt stojí 1,2 m za okrajem podlahy na koruně zdi, která je 0,3–0,7 m nad podlahou: stráž k němu vystoupí na korunu.

### Změřeno z dat 16. 11. 2026 (z předání stříšky)

Rám brány: `u` k východu podél `Brana_S`, `d` k jihu, počátek v SZ rohu věže. Výšky jsou níž **v metrech nad podlahou podesty** (vrch podlahy = `deck_z` = Z 3581 v `brana_spec.straz()`), v datech je zadávej absolutně v UE cm.

| Co | Kde |
|---|---|
| podlaha podesty | u = 0,2–6,27; d = −0,55 až 5,25 |
| trámy pod podlahou | d = −0,2 (na `Brana_S`) / 1,3 / 3,15 / 5,0 |
| koruna `Brana_V` mezi podlahou a východním krytem | u = 6,3–7,4; 0,36 m nad podlahou (Z 3617), místy 0,73 m (d = 4,3–5,1 u vnitřního líce) |
| východní kryt | osa u = 7,5; kůly Ø 18–22 cm; vrch 1,76–1,84 m; ráhna zevnitř (u ≈ 7,34) ve výšce 0,55 a 1,22 m |
| průzory východního krytu | d = 1,5 / 3,1 / 4,6; od 1,35 m nahoru |
| severní kryt | osa d = −0,75; vrch 1,25 m |

## Souhrn specifikace
- Rozměry: `tools/ruin/brana_spec.py` (výšky absolutně v UE cm). Kontrola: `run_checks.py --only brana`. Náhled: `preview3d.py brana <out.png> [--stage 1|2]`, `05_constructions/Stavby_brana_straz_nahled.png` a `Stavby_brana_straz_nahled_etapa1.png`.
- V UE: `05_constructions/stavby/Brana_Straz.py` s `RUIN = True` (přestaví část `Obvod` kvůli kapsám a nároží, dlouhé), příště stačí `RUIN = False`.

## Co se liší od návrhu (a proč)
**Návrh neseděl na dnešní data.** Od 14. 11. se polohy zdí brány převzaly z levelu. Změřeno 16. 11. 2026 (terén z levelu):

| | Návrh (kap. 2) | Skutečnost |
|---|---|---|
| koruna `Brana_V` nad obloukem | Z 3423–3493 | Z 3617–3654 |
| vrch východního oblouku | pod Z 3423 | Z 3529 |
| koruna `Brana_J` | Z 3408–3474 | Z 3455–3549 |
| koruna `Brana_S` | Z 3321–3386 | Z 3459–3552 |
| navržený vrch podesty | Z 3522 | pod vrchem východního oblouku |

**Rozhodnutí Jirky (16. 11. 2026):**

- **Trámy jdou na východě do kapes v `Brana_V`** (úprava 03, kap. 3 tím neplatí), na západě leží na vyrovnané koruně `Brana_J`. Východní zeď vyčnívá 0,4–0,7 m nad podestu jako kamenné předprsí; kůly východního krytu na ní budou kratší.
- **Etapy:** stanoviště je v etapě 1 rozestavěné. Sady: podesta (kámen, trámy, prkna) a východní kryt `base` (potvrzeno 16. 11. 2026); severní a jižní kryt `final` (návrh architekta, Jirka nepotvrdil), přístřešek návrh `final`.
- **Zábradlí směrem do hradu se nestaví** (16. 11. 2026, kap. 4.3 neplatí): na západní nebo jižní straně bude výlez na podestu. Kód zábradlí v typu `platform` zůstává, v datech žádné není (`B_RAILS = False`).

- Další odchylky od kap. 4: trámy Ø 24 místo 22; podesta končí na východě u líce zdi (ne na její koruně), plocha 6,1 × 5,8 m; jižní kryt stojí na podlaze v d = 5,15 (návrh: práh z kulatiny v d = 5,35) a je delší (návrh u = 4,3–7,5); `Hradba_V` má korunu v Z 3237, podestu tedy nekryje.

## Ověřeno v UE (ano/ne, kdy, kým)
**Kroky 1 až 3 hotové (podesta a všechny tři kryty; ve skriptech). V UE Jirka viděl podestu a východní kryt (16. 11. 2026) a zadal úpravy, které jsou tu už zapracované; nový stav v UE neověřen.**

## Co zbývá
**Zbývá:** přístřešek z kůry (`bark_roof`; nový návrh a instrukce pro stavitele: [[predani_brana_straz_striska_stavitel]], nahrazuje kap. 4.4), zátaras, staveniště pro etapu 1, výstup na podestu (určí Jirka; západní třetina jižní strany a západní strana jsou volné).

### Mimo stříšku (z předání stříšky)

- **Zátaras** (`Brana_Zataras`, španělský jezdec, jeden samostatný actor): návrh kap. 4.5.
- **Staveniště pro etapu 1** (sada `site`): žebřík, hromada kůlů, svitky kůry.
- **Výlez na podestu:** určí Jirka. Volná je západní strana a západní třetina jižní strany.
- **Otevřené u Jirky:** severní a jižní kryt jsou teď `final`; v etapě 1 je severní hrana podesty nad zdí bez krytu.

## Odkazy na návrh a předání
- návrh: [[navrh_brana_straz]] (přístřešek z kůry: kap. 11)
- předání: [[predani_brana_straz_striska_stavitel]] (přístřešek z kůry, aktivní)
