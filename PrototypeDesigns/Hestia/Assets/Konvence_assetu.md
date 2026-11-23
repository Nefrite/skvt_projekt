---
# orchestrace
type: reference
validity: valid
updated: 2026-11-23
aliases: [konvence assetů, pravidla assetů]
---
# Konvence assetů

Obecná pravidla pro všechny knihovní assety této instance (karty v `Assets/<asset_category>/`, šablona `tpl_asset`; 07 kap. 20.1). Karta je neopakuje, jen na ně odkazuje a uvádí odchylky. Pravidla pro assety se nepíší do katalogů, checklistů ani do kroků staveb; nové pravidlo zapíše výrobce sem.

Převzato z dřívějších dokumentů [[Katalog_props]] (*Společné konvence*) a [[CHECKLIST_assets_navrhy]] (kap. 2.2, 6) při převodu na karty (P19, 2026-11-23).

## Pivot
- **Props a knihovní meshe:** pivot ve **středu bounding boxu** (výchozí pro všechny props, Jirka 21. 11. 2026); tak to dělá `mesh_props.py` i ostatní moduly `tools/meshes/`.
- Typ `props` v datech bere `z` jako **spodek** kusu nad terénem nebo podlahou a střed dopočítá sám (`zc = z + sz / 2`); `zc` = střed.
- Pivot u země jen u kusů, kde to určí zadání (např. stavební dílce). Odsazení funkčního středu (výfučna, rám, body pro brnění) uvádí karta v *Účel a použití* nebo *Na míru*.

## Osy
- UE, cm, **Z nahoru**. OBJ se zapisují rovnou v osách UE (`MESH_AXES` v `zrlib/config.py`).
- Každá karta uvádí, kam míří čelo, hlava, zámek nebo jiná funkční strana.
- Natočení v datech: `x = (da, dc)` = směr lokální osy X v rámu stavby; lokální +Y je X otočená o +90° v UE.
- Délkové dílce (kulatina, tyče, trámy, prkna, lano) mají délku podél X; sloup (`SM_RuinPost`) má délku nahoru (Z).

## Rozměr a graybox
- **Jmenovitý rozměr = bounding box meshe** (`NOMINAL` v modulu generátoru = `LIB_MESHES`, `ROUND_MESHES`, `WOOD_NOMINAL` v `zrlib/config.py`). `size` nebo `scale` v datech mesh natáhne; props se kladou v jmenovitém rozměru (scale 1). Délkové dílce (nominál 100 cm) se natahují na délku a průměr přes scale.
- **`envelope` = rozměr grayboxu** v cm `[x, y, z]` po celou dobu karty (01 kap. 9.5): u vyrobeného assetu skutečný rozměr zaokrouhlený **nahoru** na celé cm, u požadavku rozměr grayboxu z návrhu nebo dat (`GH_*` v `tools/ruin/ostroh_spec.py`). Skutečný asset se do něj vejde.
- Obal mění výrobce (Crafter, u jednoduchých dílů Builder): když výroba obal překročí, `envelope` zvětší a zapíše úkol (`code: role:<Role>`) rolím v `used_by`, které podle grayboxu rozvrhovaly.
- **Materiál grayboxu:** `MAT_GRAYBOX` (`/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray`), kategorie dílce `graybox` (Cube), v datech `stand_in: graybox` v kartě.

## Materiály
- Materiály jsou instance na `M_RuinStone` (kámen, dřevo, kov…) a `M_RuinCloth` (plátno, oboustranné, `WindAmount`); složka `/Game/Skvt/Lapikus/Ruin/Materials`, vzhled v `MAT_LOOK`, textury v `TEXTURES` (`zrlib/config.py`).
- **Slot `Wood`** = úprava dřeva z dat (`finish`: `raw`, `oil`, `tar`, `old`, `blood`, `peeled`; `WOOD_FINISH`, `WOOD_FINISH_DEFAULT`). Ostatní sloty jsou pevné (`SLOT_MI`, `CLOTH_MI`). Nábytek hosta: doporučená úprava `oil`; stan: `raw`.
- **Kulatina má tři sloty:** `Wood` (plášť loupaný nebo odloupnutá místa), `EndGrain` (čela, světlejší, letokruhy), `Bark` (kůra). Zašpičatělé a osekané konce jsou vždy holé dřevo.
- Stejné materiály jako zřícenina a dostavby (`MI_Ruin*`), stejné zvětrání shora (`MAT_TOP`) a měřítko UV (1 UV = 1 m).

## Pojmenování a varianty
- Jméno v kódu = klíč (`SM_RuinChestSmall`), jméno v UE a v kartě = `{key}_{variant}` (`SM_RuinChestSmall_A`); kameny `SM_RuinStone_R{poměr}_{varianta}`, kvádr `SM_RuinAshlar` bez varianty.
- **Jedna karta = jeden asset**, varianty A–C téhož klíče i tvarové varianty (`SM_RuinCampBed` a `SM_RuinCampBedFolded`) v jedné kartě, pole `variants` (GameDesigner 2026-11-22, 2026-11-23). Jméno karty = první varianta.
- Kategorie (`asset_category`) = podsložka OBJ `meshes/<kategorie>/` a složka v UE podle `MESH_DIRS` (`stone` → `Ruin/Stones`, `wood`, `wattle`, `textile`, `props`); materiály `materials`.
- Shape v datech (`LIB_SHAPES`, `ROUND_SHAPES`): `shape: chest_small` → `SM_RuinChestSmall`.

## Pravidla výroby
- Meshe se generují procedurálně v Pythonu (vizuální prototyp, 14. 11. 2026): vstup `tools/meshes/gen_meshes.py`, moduly podle materiálu (`mesh_stone`, `mesh_wood`, `mesh_log`, `mesh_bark`, `mesh_wattle`, `mesh_textile`, `mesh_props`); OBJ do `meshes/<kategorie>/`.
- **Tvary na míru** (plachty, štíty) jako OBJ s `.json` (střed a rozměr v osách stavby, `mesh_textile.write_fitted`); stavba bere rozměr z `.json`.
- **Seed propu** se odvozuje z pořadí v `PROPS` (`mesh_props.py`): nový prop vždy **na konec** seznamu, jinak se změní ostatní.
- **Směr let dřeva:** léta vedou podél **nejdelšího rozměru dílu**, případně podél směru, kde díl potřebuje pevnost (sloupek, noha, příčka, kolík, topůrko, prkno, soustružená hlavice podél osy). Textury dřeva mají léta podél U, UV dílu má mít U podél délky. V `mesh_props.py` to zajišťuje `grain="long"` u `add_box`, `add_cyl`, `add_lathe`, `add_prism` (Jirka 22. 11. 2026). Výchozí `GRAIN_DEFAULT = None` drží starší props beze změny; plošné uplatnění je řádek v *Změnách konvence*.
- **Vytažený profil (`add_prism`):** body obrysu proti směru hodinových ručiček; po zrcadlení souřadnice obrátit pořadí (jinak normály dovnitř a v UE chybí plochy; 22. 11. 2026 jařmo stojanu na brnění).
- **Styl:** žádné ostré „CAD“ hrany, všechno trochu nakřivo a ošoupané; dřevo z dílců kulatiny a hraněného dřeva, kde to jde (hrubé opracování, ohlazené hrany, praskliny); každý prop je samostatný actor (`loose`).
- **Kůra:** provizorní a rychlé stavby a nezpracovaný materiál s kůrou, nosné a trvalé dřevo loupané ([[Materialy_a_upravy_dreva]]).

## Verze a import
- Verze meshe: `STONE_MESH_VERSION` v `zrlib/config.py` (prefix jména → verze, platí nejdelší shodný prefix). Vyšší verze než v projektu = UE mesh znovu naimportuje; po změně tvaru verzi vždy zvednout.
- `MESH_AXES` = verze importu všech meshí (vyšší = znovu naimportovat vše); `MAT_VERSION`, `CLOTH_VERSION`, `TEX_VERSION` pro materiály a textury.
- Import dělá build (`zrlib/ue_assets`, build si chybějící mesh doimportuje sám) do `/Game/Skvt/Lapikus/Ruin/<složka>`; `.uasset` jsou v gitu (`Content/Skvt/Lapikus/Ruin/`). Tagy verzí v UE: `RuinStoneVersion`, `RuinMeshAxes` (čtení v etapě C).
- **Ukázka v UE:** `tools/meshes/ukazka.py` (témata v `UKAZKY`), spouštěče `tools/meshes/ukazka/Ukazka_*.py` (jen meshe tématu).

## Změna tvaru
Upravit funkci → přegenerovat jen ten mesh `python tools/meshes/gen_meshes.py --only <prefix>` → nový bounding box zapsat do `NOMINAL` a `LIB_MESHES` → zvednout `STONE_MESH_VERSION[<prefix>]` (jinak UE starý mesh nepřenačte) → kompletní `gen_meshes.py` do dočasné složky a md5 ostatních OBJ beze změny → náhled → ukázka v UE. Změnu zapsat do *Poznámek* karty; přeroste-li obal, zvětšit `envelope` (kap. *Rozměr a graybox*).

## Změny konvence
<!-- změna pravidla, které mění už vyrobené assety: řádek sem a úkol pro výrobce ve frontě (code: role:Crafter) -->

| datum | změna | dotčené assety | úkol |
|---|---|---|---|
| 2026-11-22 | léta dřeva podél nejdelšího rozměru dílu u všech props: `GRAIN_DEFAULT = "long"` v `mesh_props.py`, přegenerovat props, zvednout `STONE_MESH_VERSION` (Jirka 22. 11. 2026: odloženo) | 31 props se změněným UV (mimo jiné nohy stolu, lůžek a stoličky, topůrka nářadí, dveře, okenice, truhly, bočnice a čela [[SM_RuinBedLarge_A]]); hotové [[SM_RuinArmorStand_A]] a sloupky [[SM_RuinBedLarge_A]] | T-0024 (`Maintenance/queue.md`) |
