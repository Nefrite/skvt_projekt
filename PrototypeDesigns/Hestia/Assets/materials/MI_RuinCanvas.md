---
# orchestrace
type: asset
asset_status: imported
requested_by: legacy
requested:
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-24
aliases: []
# hra
asset_kind: material
asset_category: materials
used_by: ["[[Vez_Pristresek]]", "[[Nadvori_Stan]]", "[[Guesthouse]]"]
envelope: []
stand_in: none
asset_source: zrlib/config.py:MAT_LOOK['canvas']; tools/textures/gen_textures.py
ue_path: /Game/Skvt/Lapikus/Ruin/Materials/MI_RuinCanvas
variants: []
---
# MI_RuinCanvas

## Účel a použití
Lněné plátno na `M_RuinCloth`, oboustranné, zašedlé, místy záplaty a skvrny; pohyb ve větru připraven (`WindAmount`, výchozí 0).

Osy a pivot: netýká se (materiál); měřítko UV 1 UV = 1 m ([[Konvence_assetu]]). Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/textures/T_RuinCanvas_D.png)

## Požadavek

## Na míru

## Z kódu
Ručně (karty materiálů se v etapě B nenapojují, GameDesigner 2026-11-23):
- vzhled `MAT_LOOK["canvas"]`, textury `TEXTURES["canvas"]` (`zrlib/config.py`), generátor `tools/textures/gen_textures.py`, `T_RuinCanvas_D/_N`
- verze: `MAT_VERSION` = 10, `CLOTH_VERSION` = 2, `TEX_VERSION` = 4

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Materials/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 1, 5 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
- Náhled je BaseColor textury `T_RuinCanvas_D`, ne render materiálu v UE.
