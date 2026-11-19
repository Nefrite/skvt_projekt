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
---
# Lapikus

## Záměr

## Domény
<!-- hestia:generated:start -->

| Doména | Návrh | Realizace | Cíl | Režim | Stav |
|---|---|---|---|---|---|
| structures | – | – | – | build | bez cíle |
| paths | – | – | – | build | bez cíle |
| npc | – | – | – | design | bez cíle |
| gameplay | – | – | – | design | bez cíle |
| narrative | – | – | – | design | bez cíle |

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

_`asset_index.json` chybí; spusť `asset_index`._

<!-- hestia:generated:end -->

## Soubory
<!-- hestia:generated:start -->

_`asset_index.json` chybí; spusť `asset_index`._

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
