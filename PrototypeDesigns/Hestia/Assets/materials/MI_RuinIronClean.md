---
# orchestrace
type: asset
asset_status: imported
requested_by: Furnisher
requested: 2026-11-14
owner: Crafter
priority: medium
depends_on: []
superseded_by:
updated: 2026-11-23
aliases: []
# hra
asset_kind: material
asset_category: materials
used_by: ["[[Palac_Kovarna_Vybaveni]]", "[[Palac_Obydli]]", "[[Guesthouse]]"]
envelope: []
stand_in: none
asset_source: zrlib/config.py:MAT_LOOK['ironclean']; tools/textures/gen_textures.py
ue_path: /Game/Skvt/Lapikus/Ruin/Materials/MI_RuinIronClean
variants: []
---
# MI_RuinIronClean

## Účel a použití
Kované železo bez rzi (kovadlina, nářadí, kování truhly hosta).

Osy a pivot: netýká se (materiál); měřítko UV 1 UV = 1 m ([[Konvence_assetu]]). Společná pravidla: [[Konvence_assetu]].

![Náhled](../../../Lapikus/textures/T_RuinIronClean_D.png)

## Požadavek

## Na míru

## Z kódu
Ručně (karty materiálů se v etapě B nenapojují, GameDesigner 2026-11-23):
- vzhled `MAT_LOOK["ironclean"]`, textury `TEXTURES["ironclean"]` (`zrlib/config.py`), generátor `tools/textures/gen_textures.py`, `T_RuinIronClean_D/_N`
- verze: `MAT_VERSION` = 10, `TEX_VERSION` = 4

## Stav v UE
Ručně do etapy C (`ue_query --assets`): `.uasset` je v `Content/Skvt/Lapikus/Ruin/Materials/` (v gitu, 2026-11-23); verze v UE a vzhled neověřeny.

## Vizuálně ověřeno
<!-- verified (jen GameDesigner): kdo, kdy (RRRR-MM-DD), verze -->

## Poznámky
- Převedeno z [[CHECKLIST_assets_navrhy]] kap. 1, 5 při zavedení karet (P19, Steward, 2026-11-23); stav podle kódu a `.uasset`, potvrdí Crafter. `requested_by` a `requested` doplněny podle role, která asset používá, a data v checklistu.
- Náhled je BaseColor textury `T_RuinIronClean_D`, ne render materiálu v UE.
