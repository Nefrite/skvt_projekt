---
# orchestrace
type: reference
validity: valid
updated: 2026-11-19
aliases: []
---
# Lapikus – rozcestník

Hlavní rozcestník vaultu Hestia. Pohledy jsou v `Dashboard/views/`: do rozhodnutí Q1 varianta Bases (`bases/`, core plugin), Dataview (`dataview/`, funguje po instalaci pluginu Dataview) a u matice a mapy skript (`generated/`, přepisuje `hubs`). Vlastní pohledy instance patří do `local/`.

## Prototyp

- Kořenová entita: [[Lapikus_Region]]
- Master lore: [[Lore_Lapikus]]
- Pojmy: [[Glossary]]

## Přehled
<!-- hestia:generated:start -->

**Kořenové entity** (zralost po doménách, v závorce nejslabší článek; 04 kap. 3)

| Entita | environment | structures | paths | npc | gameplay | narrative |
|---|---|---|---|---|---|---|
| [[Characters]] | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle |
| [[Lapikus_Region]] | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle |

**Aktivní předání**

- [[predani_brana_straz_striska_stavitel]] – [[Brana_Straz]]
- [[predani_guesthouse_kamna_stavitel]] – [[Guesthouse]]
- [[predani_palac_obydli_stavitel]] – [[Palac_Obydli]]

**Otevřené otázky:** do 14 dní 13 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-21 · Furnisher · Lapikus · CHECKLIST 6.8: SM_RuinChestLocked, SM_RuinWoodpileSmall, dlazba pod kamny · chat: Jirka 21. 11. 2026 (vybaveni Guesthouse, rozhodnuti)
- 2026-11-21 · AssetGenerator · CHECKLIST_assets_navrhy · verze 3: stan bude, rozdělení stanu assety / Builder, výchozí pivot props ve středu bounding boxu, kvalita nábytku guesthouse, nová kap. 11 pořadí prací · chat: Jirka 21. 11. 2026 (prioritizace assetů)
- 2026-11-21 · AssetGenerator · Lapikus · nový mesh SM_RuinCanvasTent_A (mesh_textile.canvas_tent, OBJ + .json se stojkami a kolíky), zrlib/config.py · chat: Jirka 21. 11. 2026 (assety stanu)
- 2026-11-21 · AssetGenerator · Lapikus · ukázka meshí po tématech (tools/meshes/ukazka.py, ukazka/Ukazka_<Tema>.py), ensure_stone_meshes(only=), gen_meshes.py --only; kompletní výstup bit po bitu stejný (md5) · chat: Jirka 21. 11. 2026 (rozdělení ukázky meshí)
- 2026-11-22 · AssetGenerator · Nadvori_Stan · props stanu: SM_RuinCampBed(+Folded), SM_RuinChestSmall, SM_RuinBundle, materiál MI_RuinSackcloth; jedno lůžko hlavou k zadnímu štítu, truhlička u hlavy, vak vedle (CHECKLIST 6.5) · chat: Jirka 22. 11. 2026 (assety stanu)
- 2026-11-22 · AssetGenerator · Guesthouse · props guesthouse: SM_RuinChestLocked, SM_RuinBedLarge, SM_RuinArmorStand (varianta A, body ARMOR_STAND_POINTS), oprava normál jařma (verze 2); CHECKLIST 6.8 · chat: Jirka 22. 11. 2026 (assety guesthouse)
- 2026-11-22 · AssetGenerator · Lapikus · nový dokument Katalog_props (karty props stanu a guesthouse), krok 05: tabulky props a textilu, ukázka po tématech, gen_meshes --only · chat: Jirka 22. 11. 2026 (dokumentace assetů)
- 2026-11-22 · Furnisher · Ostroh · ostroh_spec.py: GH_MESH a rozmery meshi u GH_BED, GH_CHEST, GH_ARMOR (03 a 05 beze zmeny) · chat: Jirka 22. 11. 2026 (meshe Guesthouse z Katalog_props)
- 2026-11-22 · Furnisher · Lapikus · ostroh_spec GH_MESH; furnishing.json, CHECKLIST 6.8, Katalog_props, 06_furnishing · chat: Jirka 22. 11. 2026 (meshe Guesthouse z Katalog_props)
- 2026-11-22 · Furnisher · Guesthouse · vybaveni 06: postel SM_RuinBedLarge, truhla SM_RuinChestLocked, stojan na brneni SM_RuinArmorStand a stolicka SM_RuinStool jako meshe (oil) misto grayboxu; polohy z levelu beze zmeny, stojan otocen o 180 st. zady k hradbe; overeno mimo UE · chat: Jirka 22. 11. 2026 (meshe Guesthouse z Katalog_props)

<!-- hestia:generated:end -->

## Zóny

| Složka | Obsah |
|---|---|
| `Inbox/` | rychlé zápisy a import (`scratch`, `intake: raw`) |
| `Scratch/` | předzpracované a ručně psané nápady |
| `Entities/` | huby entit |
| `Docs/<domain>/`, `Docs/crosscut/` | celková dokumentace podle domén a přesahy |
| `Steps/`, `Steps/shared/` | dokumentace kroků prototypování a sdíleného kódu |
| `Handovers/` | aktivní předání; splněná v `Handovers/_archive/` |
| `KnowHow/` | ověřené know-how |
| `Roles/` | profily projektových rolí |
| `Maintenance/` | údržba: konfigurace, fronta, logy, reporty |
| `_core/` | modul Hestia (needitovat) |
