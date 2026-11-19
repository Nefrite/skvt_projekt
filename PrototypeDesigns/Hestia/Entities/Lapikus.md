---
# orchestrace
type: entity
updated: 2026-11-19
aliases: []
# hra
kind: location
parent: "[[Lapikus_Region]]"
located_in: ["[[Ostroh]]"]
derived_from:
alternative_to: []
pattern:
status: in_progress
# depth_<domain> / target_<domain>: očekávané domény podle kind (01, kap. 8), jiné jen když se řeší
# depth_* = realizace (Unreal, data, StateTree); hloubka návrhu se počítá z dokumentů (01, kap. 5)
# target_mode_<domain>: design | build, jen při odchylce od výchozího režimu domény
ue_path:
assets: []
depth_structures: 4
depth_narrative: 2
---
# Lapikus

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | – | 4 | – | build | bez cíle |
| paths | – | – | – | build | bez cíle |
| npc | – | – | – | design | bez cíle |
| gameplay | – | – | – | design | bez cíle |
| narrative | – | 2 | – | design | bez cíle |

Agregace z potomků (04 kap. 3):

_Potomci nemají cíle._

<!-- hestia:generated:end -->

## Dokumenty
<!-- hestia:generated:start -->

**structures**
- [[README_ruin]] – design, depth 4, outdated
- [[Zricenina_03_ruin_stav]] – state, depth 4, valid
- [[CHECKLIST_assets_navrhy]] – checklist, valid
- [[Materialy_a_upravy_dreva]] – reference, valid
- [[Pravidla_zabydleni]] – reference, valid
- [[Rozhodnuti_zricenina]] – reference, valid
- nahrazené nebo archivované: 1

**gameplay**
- [[Pohyb_postavy_a_herni_mista]] – reference, valid

<!-- hestia:generated:end -->

## Postup stavby
<!-- hestia:generated:start -->

| Krok | Skripty | Dokumenty |
|---|---|---|
| [[03_ruin]] | `Zricenina_Brana_S_nahled.png`, `Zricenina_bloky_nahled.png`, `Zricenina_kameny_detail.png`, `Zricenina_kameny_koruny.png`, `Zricenina_koruna_nahled.png`, `Zricenina_lic_pred_po.png`, `Zricenina_strilna_preklad_pred_po.png`, `Zricenina_strilny_osteni_nahled.png`, `build_ruin_blocks.py`, `Obvod.py`, `detach_stones.py`, `gen_stones.py`, `manual_edits.json`, `ruin_layout.json`, `terrain_from_level.json`, `Zricenina_blockout_nahled.png`, `build_ruin.py`, `ruin_layout.json`, `navrh_vez_okna_podesta.png`, `navrh_vez_patra_strilny.png`, `navrh_vez_schody.png`, `navrh_vez_vyklenky_kvadry.png`, `ruin_layout_draft.json`, `build_ruin.py`, `check3d.py`, `check_blocks.py`, `decay.py`, `elev.py`, `export_level_layout.py`, `gen_layout.py`, `layout_from_level.json`, `massing.py`, `tower_spec.py` | [[README_ruin]], [[Zricenina_03_ruin_stav]] |
| [[05_constructions]] | `Knihovna_meshe_nahled.png`, `Knihovna_textury_nahled.png`, `Kulatina_meshe_nahled.png`, `Kulatina_textury_nahled.png`, `Props_kovarna_nahled.png`, `Props_textury_nahled.png`, `Stavby_brana_straz_nahled.png`, `Stavby_brana_straz_nahled_etapa1.png`, `Stavby_drevo_nahled.png`, `Stavby_ostroh_dostavba_nahled.png`, `Stavby_ostroh_nahled.png`, `Stavby_ostroh_podlaha_nahled.png`, `Stavby_ostroh_tramovi_nahled.png`, `Stavby_palac_kovarna_nahled.png`, `Stavby_palac_obydli_nahled.png`, `Stavby_palac_obydli_nahled_etapa1.png`, `Stavby_vez_nahled.png`, `Stavby_vez_pristresek_nahled.png`, `build_constructions.py`, `constructions.json`, `constructions_edits.json`, `Etapa.py`, `Sut.py` | – |
| [[06_furnishing]] | `build_furnishing.py`, `capture_furnishing.py`, `furn_data.py`, `furnishing.json` | – |

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

| Soubor | Role | Krok | Pravidlo |
|---|---|---|---|
| `/PrototypeDesigns/Lapikus/tools/ruin/tower_spec.py` | spec | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/build_ruin_blocks.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/casti/Obvod.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/detach_stones.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/gen_stones.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/build/build_ruin.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/build_constructions.py` | entry | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Etapa.py` | entry | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/stavby/Sut.py` | entry | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/06_furnishing/build_furnishing.py` | entry | 06_furnishing | folder |
| `/PrototypeDesigns/Lapikus/06_furnishing/capture_furnishing.py` | entry | 06_furnishing | folder |
| `/PrototypeDesigns/Lapikus/06_furnishing/furn_data.py` | entry | 06_furnishing | folder |
| `/PrototypeDesigns/Lapikus/tools/ruin/build_ruin.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/tools/ruin/check3d.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/tools/ruin/check_blocks.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/tools/ruin/decay.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/tools/ruin/elev.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/tools/ruin/export_level_layout.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/tools/ruin/gen_layout.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/tools/ruin/massing.py` | entry | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_Brana_S_nahled.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_bloky_nahled.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_kameny_detail.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_kameny_koruny.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_koruna_nahled.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_lic_pred_po.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_strilna_preklad_pred_po.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/Zricenina_strilny_osteni_nahled.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/manual_edits.json` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/ruin_layout.json` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/blocks/terrain_from_level.json` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/build/Zricenina_blockout_nahled.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/build/ruin_layout.json` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_okna_podesta.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_patra_strilny.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_schody.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/navrh_vez_vyklenky_kvadry.png` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/03_ruin/ruin_layout_draft.json` | data | 03_ruin | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Knihovna_meshe_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Knihovna_textury_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Kulatina_meshe_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Kulatina_textury_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Props_kovarna_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Props_textury_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_straz_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_brana_straz_nahled_etapa1.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_drevo_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_dostavba_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_podlaha_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_ostroh_tramovi_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_kovarna_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_obydli_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_palac_obydli_nahled_etapa1.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_vez_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/Stavby_vez_pristresek_nahled.png` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/constructions.json` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/05_constructions/constructions_edits.json` | data | 05_constructions | folder |
| `/PrototypeDesigns/Lapikus/06_furnishing/furnishing.json` | data | 06_furnishing | folder |
| `/PrototypeDesigns/Lapikus/tools/ruin/layout_from_level.json` | data | 03_ruin | folder |

<!-- hestia:generated:end -->

## Vazby

## Stav v UE

## Otevřené otázky
<!-- ručně zaevidované otázky k entitě: - [ ] otázka — role, RRRR-MM-DD -->
<!-- hestia:generated:start -->

- [[Pravidla_zabydleni]]: **Etapy:** jak se ve hře přepnou (dvě verze levelu, skrytí a zobrazení sad actorů)? Stojí podesta brány už v etapě 1? — z AGENT_GameDesign_hrad, 2026-11-17
- [[Pravidla_zabydleni]]: **Spaní v etapě 1:** kde spí ti, kdo nejsou na hlídce (stan na nádvoří, nebo 1. patro věže)? Od toho závisí, jestli bude `Nadvori_Stan`. — z AGENT_GameDesign_hrad, 2026-11-17
- [[Pravidla_zabydleni]]: **Žebříky** (staveniště, půda domu): použitelné pro postavu, nebo jen kulisa? — z AGENT_GameDesign_hrad, 2026-11-17
- [[Pravidla_zabydleni]]: **Brána:** výstup na podestu; dá se brána obejít zřícenou jižní stranou východně od `Hradba_V`? — z AGENT_GameDesign_hrad, 2026-11-17
- [[Pravidla_zabydleni]]: **Suť pod `Vez_V`:** víc suti z průlomu by bylo uvěřitelné, ale zúží průchod mezi věží a `Hradba_V`. — z AGENT_GameDesign_hrad, 2026-11-17
- [[Pravidla_zabydleni]]: **Staveniště:** rozmístění hromad (kulatina, krokve, prkna, kámen) tak, aby cesta průchod v `Palac_S` → vchod → světnice a cesta po zápraží ke kovárně zůstaly volné 1,2 m. — z AGENT_GameDesign_hrad, 2026-11-17
- [[Pravidla_zabydleni]]: **Hlídka na věži:** ohniště a vybavení ve 2. patře návrh přístřešku neřeší. — z AGENT_GameDesign_hrad, 2026-11-17
- [[Rozhodnuti_zricenina]]: jestli bude stan na nádvoří — z KNOWHOW_hrad, 2026-11-17
- [[Rozhodnuti_zricenina]]: přiřazení kůra / loupané u jednotlivých staveb — z KNOWHOW_hrad, 2026-11-17
- [[Rozhodnuti_zricenina]]: výstup na podestu brány — z KNOWHOW_hrad, 2026-11-17
- [[Rozhodnuti_zricenina]]: poloha cisterny — z KNOWHOW_hrad, 2026-11-17
- Scratch: [[FURNISHING]] (prepared)
- Scratch: [[Kod_spousteni_kontroly_z_roli]] (prepared)
- Scratch: [[Namety_dostavby]] (prepared)

<!-- hestia:generated:end -->

## Historie a rozhodnutí
