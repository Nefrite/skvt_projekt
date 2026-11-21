---
# orchestrace
type: scratch
intake: raw
source: notion
source_ref: "https://app.notion.com/p/41b636aed784816e8c60cd73456547c8"
validity: valid
updated: 2026-11-21
# hra
category: [place]
entity: ""
---
# Palisáda nad bránou

Zdroj: [Notion](https://app.notion.com/p/41b636aed784816e8c60cd73456547c8), vytvořeno 2026-11-17 09:52 UTC

**Smart location: patrolling**

- iddle mode
  - fletching - tichá aktivita, stále slyší okolí, ale zabaví se
  - patrol - dojde ke stěně, chvíli se rozhlíží daným směrem
    - východní směr
    - jih nebo sever
    - druhá strana J/S
    - zpět východ
  - jen tak sedí a kouká, co se děje v hradě, poslouchá okolí
- attention mode
  - trigger: něco zaslechl, zahlédl pohyb (bez identifikace zdroje / hráče)
  - full patrol - přechází od stěny ke stěně a prohlíží si okolí, občas koukne do hradu
  - exit: colddown do iddle
- alert mode
  - trigger:
    - zahlédl hráče
    - V attention znovu zaslechl (potřetí) podezřelý zvuk
  - zburcovaní okolí (ti se posouvají o stupeň výše)
  - spot patrol:
    - velká pozornost ke směru
    - občasná kontrola ostatních směrů
  - exit: colddown do attention
- fight mode
  - trigger:
    - vidí hráče
    - byl zraněn
  - zburcovaní okolí (do fight nejbližší, patrol ostatní alert)
  - attack
    - zbraň, jež má k dispozici vzhledem ke vzdálenosti hráče
    - luk/kuše - dokud je hráč v range, zůstává na podestě a střílí
    - chladné zbraně - pokud se hráč dostal na podestu, nebo je moc blízko
  - exit:
    - hráč opustil trigger area -> alert mode
    - těžké zranění s ranged -> hideout mode
- hideout mode
  - trigger: těžké zranění s ranged
  - krytí za palisádou směrem odkud jde útok
  - exit:
    - další zranění -> fight
    - recovery -> fight nebo alert

## Předzpracování (doplní Knihovník)
- Kategorie:
- Souvisí s:
- Návrh zařazení: (doména / crosscut / nic)
