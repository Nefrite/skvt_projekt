---
# orchestrace
type: knowhow
knowhow_kind: pitfall
tech: [ue_python, static_mesh_import, nanite]
scope: engine
engine_version: "5.8"
verified: 2026-11-17
validity: valid
updated: 2026-11-19
aliases: []
---
# Pasti: import meshí a assety v Unrealu

<!-- Z KNOWHOW_hrad.md kap. 5.2 (pilot Lapikus, B6). -->

- **Osy OBJ:** import OBJ do UE (Interchange) nepřevádí Y-up, jen otočí znaménko Y: UE = (X, −Y, Z) z OBJ (ověřeno `tools/checks/UE_Osy_OBJ.py` 15. 11. 2026). Tím mesh zrcadlí a otočí i pořadí vrcholů trojúhelníků. Proto `mesh_common.obj_v` zapisuje (x, −y, z) a `obj_f` trojúhelníky obráceně; bez obrácení je mesh v UE naruby (15. 11. 2026: celý hrad „průhledný“). Kontrola: v zapsaném OBJ musí pořadí vrcholů souhlasit s `vn`. Dřívější zápis Y-up dělal assety naležato a při stavbě se to maskovalo prohozením os podle bounding boxu a otočením o 180° (`MESH_FLIP`, zrušeno). Při změně zápisu zvyš `MESH_AXES`. Nový tvar vždy ověř v UE (ukázka `tools/meshes/Ukazka_Meshe.py`), i v Content Browseru, ne jen náhledem.
- **Poškozené bounds meshů (chyba UE, příznak `bDoFastBuild`):** mesh s tímto příznakem staví UE vždy "fast buildem": bez Nanite, s varováním "nearly zero tangents" a s neinicializovanými bounds vykreslovacích dat (forum UE: Meshes built from Interchange have uninitialized bounds). Náhodně vyjde NaN: "FStaticMeshRenderData::Serialize found NaN in Bounds", pak InverseFast / precision loss (distance field), prázdný náhled. Příznak je uložený v assetu, Python ho nevidí (`get_bounds()` v pořádku), build s `fast_build=False` ani uložení ho nezruší; poznat jde jen jako text `bDoFastBuild` v `.uasset` (`ue_assets._has_fast_flag`). Měly ho všechny kameny v `Ruin/Stones` (33 z 33, už od 13. 11.), ostatní meshe ne; čerstvý import přes Interchange ho nemá. Druhá půlka problému je cache (DDC): UE si poškozený výsledek uloží pod klíčem z geometrie a nastavení buildu a každý další build se stejným klíčem ho vezme znovu, i v čistém assetu (v logu pak chybí "Building static mesh"). Ověřeno testem `tools/checks/UE_Test_Formatu_OBJ.py`, `MODE = "pricina"` (15. 11. 2026): stará cache → NaN u stejných meshů v každém kole; kopie kamene s příznakem a čistá cache → build bez Nanite, náhodné NaN; bez příznaku a s čistou cache → čisté. Řešení (`ue_assets._import_one`, `MESH_AXES` 10): OBJ se importuje do dočasného assetu `Ruin/_Import`, existující cíl s příznakem se smaže, cíl vznikne kopií dočasného assetu, postaví se z jeho mesh description s `fast_build=False` a pak s nastavením `BUILD_CFG` (klíč cache, pod kterým se nikdy fast nestavělo; při podezření na poškozenou cache do něj přidej další položku); dočasný asset se smaže. Build na konci vypíše varování, kdyby některý mesh příznak měl. Slepé uličky: formát OBJ (osy, pořadí vrcholů), hromadný vs. postupný import, přestavění změnou nastavení, build s `fast_build=False` do existujícího assetu, kontrola `get_bounds`, změna dat OBJ.
- **Rozměr meshů při stavbě:** bere se z OBJ (`ue_assets._OBJ_BOX`), ne z bounds assetu v UE (po importu bývají nespolehlivé, viz výše).
- **`unreal.MathLibrary.break_transform` v Pythonu UE 5.8 není** (pád capture vybavení 17. 11. 2026). Polohu a natočení z `Transform` ber přes vlastnosti `t.translation`, `t.rotation.rotator()`, `t.scale3d` (`ue_assets._unit`, `ue_actors.loose_pose`).
- **Assety nikdy uvnitř `ScopedEditorTransaction`.** Import meshí a textur, materiály a úpravy meshí (kolize, Nanite) patří před transakci. Undo transakce by vrátilo i úpravy čerstvě naimportovaných meshí a jejich další přeimport shodí editor (pád 14. 11. 2026, `Ukazka_Kulatina.py`).
- **Fullscope není běžný build.** `build_fullscope.py` maže assety a actory, proto ho navrhuj jen při poškozených assetech nebo po změně způsobu importu. Na běžné změny stačí dílčí skripty nebo `build_normal.py`.
- **Knihovní meshe mají víc materiálových slotů** (kulatina `Wood`, `EndGrain`, `Bark`; proutí `Daub`, `Wattle`). Dílec kulatiny = `Stone` s `shape` z `ROUND_SHAPES` a `bark`, ostatní knihovní meshe `shape` z `LIB_SHAPES`; délka vždy podél `sx`. Materiál se přiřazuje přes `ue_assets.apply_materials` (slot `wood` = materiál dílce, ostatní `SLOT_MATS`), ne `set_material(0, ...)`.
- **Jedna kopie `zrlib` na běh (15. 11. 2026).** Spouštěč na začátku zahodí moduly z minulého běhu, dál se načítá jen přes `zrlib/pipeline.py`. Dvě kopie knihovny znamenají dvojí stav (materiály slotů `SLOT_MATS`, rozměry meshí `_OBJ_BOX`): 05 pak nevidí, co nastavilo 03.

- **Mesh na míru (plachta) se posazuje podle `<mesh>.json`** (17. 11. 2026): `mesh_textile.write_fitted` zapíše OBJ vystředěný na bounding box a vedle `.json` se středem a rozměrem v lokálních osách stavby; stavba (`zr_stavby/pristresek.py`) dá dílci přesně ten rozměr, takže měřítko vyjde 1. Mesh necentrovaný by se při stavbě posunul (pivot = střed bounding boxu) a plochý mesh (štít, tloušťka 2 cm) by se roztáhl.
- **Plátno přes ovázané tyče:** ovázání (`SM_RuinLashing`) vyčnívá 1,6 cm nad tyč Ø 10 cm, plachta proto leží 2 cm nad krokvemi, ne 0,5 cm (17. 11. 2026, `run_checks.py --only vez` to hlídá).
