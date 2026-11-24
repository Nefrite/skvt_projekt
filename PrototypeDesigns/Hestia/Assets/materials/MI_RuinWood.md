---
# orchestrace
type: asset
asset_status: in_progress
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
used_by: ["[[Palac_Obydli]]", "[[Palac_Kovarna]]", "[[Vez_Pristresek]]", "[[Brana_Straz]]", "[[Guesthouse]]", "[[Nadvori_Stan]]"]
envelope: []
stand_in: none
asset_source: zrlib/config.py:MAT_LOOK['wood']
ue_path: 
variants: [MI_RuinWood_Tar, MI_RuinWood_Oil, MI_RuinWood_Blood, MI_RuinWood_Old, MI_RuinWood_Peeled]
---
# MI_RuinWood

## Účel a použití
Zašlé nelakované dřevo `raw` a úpravy dřeva: `MI_RuinWood_Tar` (dehet), `_Oil` (olej), `_Blood` (mořené krví), `_Old` (staré), `_Peeled` (čerstvě loupané); slot `Wood`, úprava z dat (`finish`, `WOOD_FINISH`). Textury ze StarterContent.

Osy a pivot: netýká se (materiál); měřítko UV 1 UV = 1 m ([[Konvence_assetu]]). Společná pravidla: [[Konvence_assetu]].

## Požadavek

## Na míru

## Z kódu
Ručně (karty materiálů se v etapě B nenapojují, GameDesigner 2026-11-23):
- vzhled `MAT_LOOK["wood"]`, textury `TEXTURES["wood"]` (`zrlib/config.py`)
- verze: `MAT_VERSION` = 10

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` všech 6 variant v `Content/Skvt/Lapikus/Ruin/Materials/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 1, 5 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by: legacy` (vyrobeno před zavedením karet, CR-036).
- Asset je vyrobený a `.uasset` existuje, karta ale nemá vlastní náhled (podmínka stavu `generated`, 07 kap. 20): zůstává `in_progress`, dokud Crafter nedoplní náhled a nenastaví `imported`.
