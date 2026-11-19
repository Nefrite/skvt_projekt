---
# orchestrace
type: concept
master: lore
validity: draft
updated: 2026-11-19
aliases: []
# hra
domain: narrative
category: [lore]
entity: "[[Lapikus_Region]]"
depth: 1
---
# Lore: Lapikus

## Svět a doba
### 1. Předloha: hrad Lapikus

Podle povrchového průzkumu (Archeologický ústav AV ČR, Brno):

| Prvek | Skutečnost |
|---|---|
| Poloha | skalní ostroh nad Plenkovickým potokem, 2,2 km ZSZ od Plavče (Znojemsko) |
| Stavba | 1364–1381 (Boček z Plavče, původně „Hrádek“); racionální dispozice typu Karlštejn / Radyně / Kašperk, na Moravě Ronov |
| Zánik | pustý nejpozději 1508, nejspíš po česko-uherských válkách (2. pol. 15. st.) |
| Příkopy | **dva šíjové příkopy** přes hřbet: první (~6–8 m široký), za ním **předhradí** ~50 m bez zástavby, pak druhý velký příkop před jádrem |
| Přístup | po **severním svahu** pod předhradím k velkému příkopu naproti bráně |
| Jádro – sever | **nádvoří**, ohradní zeď dochovaná v délce 43 m; **brána** s nárožním pilířem přiložená k hradbě, zpevněné opěrákem |
| Jádro – jih | **blokový palác** dlouhý 44 m nad nádvořím, západní konec 9,5 m široký, úzké okno k jihu; uvnitř příčky |
| Věž | východní, **věžovitá čelní část paláce ~11 × 11 m** (k příkopu) |
| Západ | budova s **vnější branou** (dochované jedno ostění a kapsa pro závoru) |

## Místo
- **Předloha:** hrad Lapikus nad Plenkovickým potokem, herní rozměry asi 0,9× skutečnosti. Plošina ~67 × 25 m, jižní hrana padá 7–8 m skalní stěnou.

## Časové vrstvy
| Vrstva | Co to znamená pro hru |
|---|---|
| **Zřícenina** | generátor staví stav **~1650** (preset `1650`, druhý preset `1540` je zachovalejší): střechy a stropy pryč, zdi rozebrané podle dostupnosti (níž a blíž cestám víc), vylámaná ostění, suť u zdí, kapsy po trámech. |
| **Druhé zabydlení** | později se v ruině usadili lidé a **provizorně, ale na delší dobu** si ji upravili: dřevo ve věži, obytná místnost u ostrohu, suť uklizená tam, kde bydlí. Staví z **kamene z rozvalin** a z místního dřeva. |

**Dvě etapy hry** (návrhy z 11/2026): posádka (dva až tři lidé a hlídka na věži) přišla začátkem léta, je teplo a sucho, občas bouřka.
- **Etapa 1:** hráč přichází poprvé. Dům v paláci se teprve staví (staveniště, hromady dřeva), kovárna už stojí, hlídka spí pod plachtou na věži.
- **Etapa 2:** dům je hotový a obydlený, staveniště zmizelo.
- Zřícenina je v obou etapách stejná. U každého návrhu napiš, ve které etapě platí.

| Vrstva | Co to znamená pro konstrukci |
|---|---|
| **Zřícenina** (`03_ruin`) | stav kolem roku 1650 (preset `1650`). Střechy a stropy pryč, zdi rozebrané, suť u zdí, kapsy po trámech. Zdivo z lomového kamene v řadách, líc z obou stran a jádro uprostřed. |
| **Druhé zabydlení** (`05_constructions`) | později. Lidé si ruinu **provizorně, ale na delší dobu** upravili. Staví jeden až tři lidé s jednoduchým nářadím z **kamene z rozvalin** (stejně velký jako ve zdech) a z místního dřeva. Žádné kovové konstrukce, sklo jen výjimečně. |
| **Dvě etapy hry** (návrhy z 11/2026) | posádka (dva až tři lidé + hlídka) přišla začátkem léta. **Etapa 1:** hráč přichází poprvé, dům v paláci se teprve staví, kovárna už stojí. **Etapa 2:** dům je hotový. Zřícenina (03) je v obou etapách stejná, liší se jen 05. Etapy jsou tři sady actorů: `base` (stojí už v etapě 1 a zůstává), `final` (dostavba), `site` (staveniště); u každého prvku napiš sadu. Co je jednou postavené, se neskrývá (`KNOWHOW_hrad.md` kap. 2). |

### 2. Herní verze: stav kolem roku 1540

Zřícenina je „dříve v čase“: zhruba **60–80 let po opuštění**. Zbývá víc než dnes:

| Prvek | Stav v roce ~1540 |
|---|---|
| Střechy, stropy, dřevo | spadlé a shnilé; z trámů zbyly jen kapsy ve zdech a pár trámů zaklíněných ve věži |
| Věž | stojí do **~17–21 m z ~24 m**, strana do nádvoří nahoře rozebraná (V do 11 m); uvnitř zbytky stropů, schodiště ve zdi částečně průchozí |
| Palác | **vnější (jižní) zeď nad útesem 8–11 m** s okny; **severní k nádvoří 4–8 m, u dveří až k zemi**; příčky 4–7 m; **sklep** pod západní částí s klenbou částečně propadlou |
| Hradba | **5–7 m** (vnější, špatně dostupná), u brány nižší; ochoz u rampy; jeden **průlom** na severu |
| Brána | gotický oblouk stojí, vrata pryč, **most přes příkop zřícený** (zbyly pilíře a trámy) |
| Západní budova | **1,5–4 m** (nízká a dostupná, rozebraná nejvíc), **branka** s ostěním vede ven na špičku ostrohu |
| Nádvoří | suťové kužely pod zdmi, **cisterna**, náletové dřeviny (bez, bříza, jeřáb), kopřivy u zdí |

<!-- odkazy na milníky z taxonomy_local/milestones.yaml -->
## Obyvatelé a postavy
Typický obyvatel: vojenská historie, není zámožný, opatrný, šetří prací. Dostavba má být uvěřitelná (co by zvládl jeden až tři lidé s jednoduchým nářadím) a **čitelná pro hráče** (proč to tu je, co to říká o obyvatelích).

## Tón a témata
## Pravidla světa
Pravidla návrhu: [[Pravidla_zabydleni]], [[Materialy_a_upravy_dreva]].

<!-- technologie, materiály, uvěřitelnost; odkazy na pravidla návrhu v Docs/ -->
## Vazby na hratelnost
Pohyb postavy a herní místa: [[Pohyb_postavy_a_herni_mista]].

## Otevřené otázky
