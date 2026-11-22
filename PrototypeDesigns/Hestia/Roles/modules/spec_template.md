---
type: agent_module
module_id: spec_template
trigger: návrh stavby (dokumentace domény structures)
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-22
---
<!-- Z AGENT_Architekt_hrad.md kap. 8 (pilot Lapikus, B5). -->
# spec_template

## Kdy
Architekt píše nebo doplňuje návrh stavby v `Docs/structures/`.

## Postup
Obsah návrhu piš podle bodů níže a zapiš ho do sekcí doménového dokumentu (07 kap. 2):

| Body šablony | Sekce dokumentu |
|---|---|
| Zadání | *Zadání / záměr* |
| Kde, Výchozí stav | *Výchozí stav* |
| Cílová struktura, Úpravy 03, Dostavba 05, Dílce a props, Etapa, Ruční doladění, Varianty, Náčrt slovy | *Návrh* |
| klíčové parametry, Sdílené rozměry (cesta, konstanty v `*_spec.py`, `constructions.json`) | *Souhrn specifikace* |
| Vazby a kolize | *Vazby a závislosti* |
| Ověření | *Ověření* |
| Předpoklady a otevřené otázky | *Otevřené otázky* |

Dokument nad `doc_summary_chars` (6 000 znaků) má navíc na začátku sekci *Souhrn* (co platí, hlavní rozhodnutí, odkazy na sekce; asi do 1 500 znaků), kterou držíš aktuální při každé změně.

Body:

```
### <Název stavby>
- Zadání: odkud (návrh game designera / Jirka) a herní účel jednou větou
- Kde: část hradu + zeď (jméno z dat) + poloha (s v m podél zdi, nebo UE cm X/Y), výška od terénu
- Výchozí stav: koruny, otvory a terén změřené z dat (datum, s terénem z levelu)
- Cílová struktura:
  - nosné prvky: co, průřez (m), délka, rozestup, na čem leží (výška uložení)
  - výplně a krytina: materiál, tloušťka, sklon, směr odvodnění
  - otvory: druh, šířka, výška, parapet, nadpraží
  - úprava dřeva po částech (tar/raw/oil/blood/old)
- Úpravy 03 (zřícenina): ne / ano - co (cut, cap, notches, set_height...), zeď, s, z; kterou část přestavět
- Dostavba 05: typ (existující / nový), název stavby, klíčové parametry do constructions.json
- Dílce a props: které hotové z knihovny (jména SM_Ruin*), které tvary jsou nové
- Etapa: sada actorů u každého prvku (base / final / site); co se mezi etapami liší
- Sdílené rozměry: kde budou (např. nová konstanta v ostroh_spec.py nebo nový *_spec.py)
- Ruční doladění: co bude samostatný actor (loose)
- Vazby a kolize: s čím sousedí, co se nesmí bít, pořadí stavění (03 -> 05, která stavba dřív)
- Ověření: kontroly + vlastní kritéria
- Varianty: A / B, doporučení a proč
- Předpoklady a otevřené otázky pro Jirku
- Náčrt slovy: půdorys a řez s rozměry
```

## Výstup
Zapisuješ do `Docs/structures/navrh_<část>_<stavba>.md` (existující návrh doplníš, nový jen když žádný není); stavbu zadáš předáním v `Handovers/` (jedno předání = jeden task pro jednu roli, `for_role`).

## Známé pasti
