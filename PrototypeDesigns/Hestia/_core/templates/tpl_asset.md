---
# orchestrace
type: asset
asset_status: requested    # requested|in_progress|generated|imported|verified|rejected|superseded (verified jen GameDesigner)
requested_by:              # role, která asset potřebuje
requested: {{date:YYYY-MM-DD}}
owner:                     # výrobce, vyplňuje žadatel vždy: Crafter (výchozí, v pochybnosti), jednoduchý díl stavby Builder
priority: medium           # high|medium|low
depends_on: []             # karty assetů, na kterých výroba závisí
superseded_by:             # povinné u superseded
updated: {{date:YYYY-MM-DD}}
aliases: []
# hra
asset_kind: mesh           # mesh|material|texture|blueprint
asset_category:            # = podsložka Assets/<asset_category>/
used_by: []                # entity, které asset používají; prázdné jen s účelem v těle
envelope: []               # rozměr grayboxu v cm [x, y, z]; asset se do něj vejde (mesh, Blueprint i od generated)
stand_in: none             # graybox|none: co v levelu stojí místo assetu
asset_source:              # od generated: generátor nebo zdroj a funkce (tools/meshes/mesh_props.py:chest_small)
ue_path:                   # od imported: /Game/...; jméno souboru = poslední segment
variants: []
---
# {{title}}

<!-- Jméno souboru = jméno assetu v UE, složka Assets/<asset_category>/ (07 kap. 20). Stav mění role,
     lint hlásí chybějící pole a sekce podle asset_status. -->
## Účel a použití
<!-- k čemu asset je a kde stojí; od generated osy, pivot a vložený náhled ![[…png]];
     společné konvence jen odkazem na Konvence_assetu -->
## Požadavek
<!-- requested: obalové rozměry nebo technické údaje, odkaz na návrh, graybox v levelu -->
## Na míru
## Z kódu
<!-- od generated: rozměr, sloty, výchozí materiál, verze; u meshe generovaný blok (asset_index, hubs), ručně jen poznámka nad ním -->
## Stav v UE
<!-- od imported: import, cesta, verze; po čtení z UE (ue_query --assets) generovaný blok -->
## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->
## Poznámky
<!-- změny tvaru; důvod rejected nebo superseded -->
