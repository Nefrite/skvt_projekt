---
type: agent_module
module_id: spec_template
trigger: specifikace stavby pro stavitele
requires: []
modes: [vault, chat]
validity: valid
updated: 2026-11-19
---
<!-- Z AGENT_Architekt_hrad.md kap. 8 (pilot Lapikus, B5). -->
# spec_template

## Kdy
Architekt píše specifikaci stavby pro stavitele.

## Postup
Specifikaci piš podle šablony:

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
Specifikace jako text; do `Docs/structures/navrh_<část>_<stavba>.md` ji uloží stavitel nebo Jirka.

## Známé pasti
