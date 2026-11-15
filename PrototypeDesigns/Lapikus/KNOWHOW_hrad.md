# Know-how: zřícenina Lapikus – to nejdůležitější na jednom místě

Společný dokument pro všechny tři agenty (`AGENT_Architekt_hrad.md`, `AGENT_GameDesign_hrad.md`, `AGENT_Stavitel_hrad.md`) i pro Jirku. Shrnuje, co platí napříč rolemi: pravidla, konvence, ověřené pasti a rozhodnutí. Podrobnosti jsou v odkazovaných dokumentech, tady je jen to, co se nesmí ztratit.

**Jak ho udržovat** (zapisuje stavitel, ostatní agenti navrhují doplnění textem):
- sem patří jen **ověřené** poznatky a **padlá** rozhodnutí, vždy s datem; domněnky a otevřené otázky patří do návrhů a do `CHECKLIST_assets_navrhy.md`;
- každý bod má říkat, **co dělat**, a jednou větou proč; delší vysvětlení dej do README a odkaž;
- když se poznatek změní, bod přepiš, nepřidávej druhý;
- pasti a rozhodnutí se zapisují **jen sem**, agentní dokumenty na ně odkazují.

Stav: 15. 11. 2026.

---

## 1. Zlatá pravidla

1. **Zřícenina (03) a dostavby (05) jsou oddělené.** `03_ruin` je hrad po rozpadu (~1650), `05_constructions` pozdější „druhé zabydlení“, které na zřícenině stojí a nemění ji. Zásah do 03 (snížení, žlábek, průlom, vybourání) se vždy uvádí výslovně jako „vyžaduje úpravu 03“ a s částí, kterou je pak nutné přestavět (`Obvod`, `Palac`, `Ostroh`).
2. **Jeden zdroj rozměrů.** Co potřebuje 03 i 05, je v jednom specu (`tools/ruin/ostroh_spec.py`, `tower_spec.py`; pro palác a bránu vzniknou `palac_spec.py`, `brana_spec.py`). Nikdy stejné číslo na dvou místech.
3. **Ruční úpravy se nepřepisují.** `manual_edits.json` a `constructions_edits.json` vznikají přes capture z levelu. Capture vždy **před** dalším generováním.
4. **Generovaná data se needitují ručně.** `ruin_layout.json` a `constructions.json` vznikají z generátorů (`gen_layout.py`, `gen_constructions.py`), ruční změna se při příštím generování ztratí.
5. **Nic nevisí ve vzduchu.** Každý prvek má napsané, na čem leží (koruna, kapsa, žlábek, sloup, terén).
6. **Hráč na prvním místě.** Každá stavba má herní účel a dodržuje pohyb postavy (kap. 2).
7. **Nevymýšlet stav.** Zdroj pravdy je `03_ruin/Zricenina_03_ruin_stav.md`, data a README. Co v nich není, je předpoklad nebo otázka.
8. **Ostroh má zvláštní účel.** Do jeho obsazení a vybavení se nezasahuje, dokud ho Jirka nepopíše.
9. **Hlavní složka je `skvt_projekt\PrototypeDesigns\Lapikus`.** Nové soubory jen tam. V `GameDesign\Claude outputs\Lapikus` se jen přepisují existující kopie.
10. **Stavitel pracuje mimo Unreal.** Skripty v UE spouští Jirka a posílá log nebo screenshot. V hlášení se vždy odliší, co je ověřené a co ne.

## 2. Svět a hra v kostce

- **Předloha:** hrad Lapikus nad Plenkovickým potokem, herní rozměry asi 0,9× skutečnosti. Plošina ~67 × 25 m, jižní hrana padá 7–8 m skalní stěnou.
- **Vrstvy:** zřícenina ~1650 (preset `1650`) → druhé zabydlení (jeden až tři lidé, jednoduché nářadí, kámen z rozvalin, místní dřevo, žádné kovové konstrukce, sklo jen výjimečně). Staré a nové musí jít od sebe poznat.
- **Dvě etapy hry:** posádka přišla začátkem léta. Etapa 1 = hráč přichází poprvé, dům se staví, kovárna stojí, hlídka spí pod plachtou na věži. Etapa 2 = dům hotový. Zřícenina je v obou stejná, liší se jen 05 (přepínač `ETAPA`, zatím neexistuje).
- **Pohyb postavy (Character Movement):** průchod ≥ 1,2 m; dveře aspoň 1,0 × 2,2 m; schod nejvýš ~45 cm; rampa ≤ 44°; zídka do 50 cm se dá přejít, vyšší ne.
- **Úpravy dřeva:** `tar` (dehet, venkovní a masivní), `raw` (bez úpravy), `oil` (jemná práce), `blood` (mořené krví), `old` (zašedlé), `peeled` (čerstvě loupaná kulatina).
- **Kulatina:** nosné a trvalé dřevo loupané, provizorní a nezpracované s kůrou.

## 3. Souřadnice a konvence

| Co | Hodnota |
|---|---|
| Jednotky | UE centimetry; v návrzích metry; u výšek vždy napsat, od čeho (terén, podlaha věže, absolutní Z) |
| Plošina hradu | Z ≈ 3129 cm (v levelu se může lišit, build měří terén z landscapu) |
| Terén | výška v m × 100 = světové Z v cm; landscape 252 × 252 m, střed 0, 0 |
| Světové strany | z názvů zdí: `_S` sever, `_J` jih, `_V` východ, `_Z` západ. Ověřit z dat, nehádat. |
| Poloha na zdi | `s` v metrech od prvního bodu zdi v `ruin_layout.json` |
| Palác (návrhy) | `s` podél `Palac_J` od jejího prvního bodu (UE −2350 / −50), `n` kolmo k severu; vektory `s` = (0,9758; −0,2184), `n` = (−0,2189; −0,9757) |
| Věž (návrhy) | `u` od J-Z rohu k východu, `v` k severu; výšky od podlahy přízemí (`VEZ_F`, Z 3150); vnitřek 1,25–9,75 m |
| Brána (návrhy) | počátek v SZ rohu strážní věže (UE 1930 / −3107), `u` podél `Brana_S` k východu, `d` k jihu; výšky absolutně v Z |
| Jména | zdi, stavby a parametry přesně jako v datech (`ZBudova_V`, `Ostroh_Krov`, `cap`, `notches`) |
| Tagy actorů | zřícenina `Zricenina_Ruin` + `cast:<Část>` + `zed:<Zeď>`; stavby `Zricenina_Stavby` + `stavba:<Jméno>`. Build maže jen podle nich. |
| Kód | komentáře a identifikátory bez diakritiky (UE Python konzole); dokumentace česky s diakritikou |

## 4. Co kdy spustit v UE

| Situace | Skript |
|---|---|
| změna jedné části zříceniny | `03_ruin/blocks/casti/<Obvod/Palac/Ostroh>.py`, pak dostavby, které na ní stojí |
| změna jedné stavby | `05_constructions/stavby/<Stavba>.py` |
| všechno | `build_normal.py`: hrad, pak stavby; assety jen doplňuje |
| poškozené assety (NaN v bounds, `InverseFast` v logu, prázdné náhledy, meshe naruby) | `build_fullscope.py`: smaže generované actory a meshe a postaví vše znovu; po běhu nepoužívat Undo |
| kontrola vzhledu meshí a props | `tools/meshes/Ukazka_Meshe.py` |
| uložení ručních úprav | stejný skript s `MODE = "capture"` |

Podrobná tabulka podle druhu změny je v `AGENT_Stavitel_hrad.md`, kap. 5. Společná logika spouštění je v `zrlib/pipeline.py`.

## 5. Ověřené pasti

### 5.1 Geometrie a data

- **`roll` v UE je opačně** než ve výpočtech, kontrolách a náhledech. Do UE jde `-roll` (`zrlib/ue_assets.ue_rotator`) a capture ho vrací zpět (`ue_actors.loose_pose`). Pitch a yaw se shodují. Nové stavby skládej vždy přes `Stone` a `stone_transform`, ne vlastním `Rotator`.
- **`s` podél zdi:** v datech od prvního bodu zdi. Zeď se při stavbě prodlouží o půl tloušťky, `shift`, a `edits` i `span` kamenů jsou posunuté. Při mapování mezi 03 a 05 počítej přes `project_s` na skutečné body.
- **Úpravy ve zřícenině** (`cut`) odebírají celé kameny, které zasahují do oblasti, ne jejich části.
- **Zvětralá koruna a lomové kusy jádra** mají tvar menší než svůj blok. Nic (malta, dřevo) k nim nelícuj na hranu bloku.
- **Zarovnání na řady:** otvory a nadpraží v dostavbě se zarovnávají na řady kamenů. Malé posuny v metrech proto můžou skočit o celou řadu, výsledek ověř.
- **Ruční data:** `ruin_layout.json` a `constructions.json` jsou generované, ruční změny v nich se ztratí.

### 5.2 Import meshí a assety v Unrealu

- **Osy OBJ:** import OBJ do UE (Interchange) nepřevádí Y-up, jen otočí znaménko Y: UE = (X, −Y, Z) z OBJ (ověřeno `tools/checks/UE_Osy_OBJ.py` 15. 11. 2026). Tím mesh zrcadlí a otočí i pořadí vrcholů trojúhelníků. Proto `mesh_common.obj_v` zapisuje (x, −y, z) a `obj_f` trojúhelníky obráceně; bez obrácení je mesh v UE naruby (15. 11. 2026: celý hrad „průhledný“). Kontrola: v zapsaném OBJ musí pořadí vrcholů souhlasit s `vn`. Dřívější zápis Y-up dělal assety naležato a při stavbě se to maskovalo prohozením os podle bounding boxu a otočením o 180° (`MESH_FLIP`, zrušeno). Při změně zápisu zvyš `MESH_AXES`. Nový tvar vždy ověř v UE (ukázka `tools/meshes/Ukazka_Meshe.py`), i v Content Browseru, ne jen náhledem.
- **Poškozené bounds meshů (chyba UE, příznak `bDoFastBuild`):** mesh s tímto příznakem staví UE vždy "fast buildem": bez Nanite, s varováním "nearly zero tangents" a s neinicializovanými bounds vykreslovacích dat (forum UE: Meshes built from Interchange have uninitialized bounds). Náhodně vyjde NaN: "FStaticMeshRenderData::Serialize found NaN in Bounds", pak InverseFast / precision loss (distance field), prázdný náhled. Příznak je uložený v assetu, Python ho nevidí (`get_bounds()` v pořádku), build s `fast_build=False` ani uložení ho nezruší; poznat jde jen jako text `bDoFastBuild` v `.uasset` (`ue_assets._has_fast_flag`). Měly ho všechny kameny v `Ruin/Stones` (33 z 33, už od 13. 11.), ostatní meshe ne; čerstvý import přes Interchange ho nemá. Druhá půlka problému je cache (DDC): UE si poškozený výsledek uloží pod klíčem z geometrie a nastavení buildu a každý další build se stejným klíčem ho vezme znovu, i v čistém assetu (v logu pak chybí "Building static mesh"). Ověřeno testem `tools/checks/UE_Test_Formatu_OBJ.py`, `MODE = "pricina"` (15. 11. 2026): stará cache → NaN u stejných meshů v každém kole; kopie kamene s příznakem a čistá cache → build bez Nanite, náhodné NaN; bez příznaku a s čistou cache → čisté. Řešení (`ue_assets._import_one`, `MESH_AXES` 10): OBJ se importuje do dočasného assetu `Ruin/_Import`, existující cíl s příznakem se smaže, cíl vznikne kopií dočasného assetu, postaví se z jeho mesh description s `fast_build=False` a pak s nastavením `BUILD_CFG` (klíč cache, pod kterým se nikdy fast nestavělo; při podezření na poškozenou cache do něj přidej další položku); dočasný asset se smaže. Build na konci vypíše varování, kdyby některý mesh příznak měl. Slepé uličky: formát OBJ (osy, pořadí vrcholů), hromadný vs. postupný import, přestavění změnou nastavení, build s `fast_build=False` do existujícího assetu, kontrola `get_bounds`, změna dat OBJ.
- **Rozměr meshů při stavbě:** bere se z OBJ (`ue_assets._OBJ_BOX`), ne z bounds assetu v UE (po importu bývají nespolehlivé, viz výše).
- **Assety nikdy uvnitř `ScopedEditorTransaction`.** Import meshí a textur, materiály a úpravy meshí (kolize, Nanite) patří před transakci. Undo transakce by vrátilo i úpravy čerstvě naimportovaných meshí a jejich další přeimport shodí editor (pád 14. 11. 2026, `Ukazka_Kulatina.py`).
- **Fullscope není běžný build.** `build_fullscope.py` maže assety a actory, proto ho navrhuj jen při poškozených assetech nebo po změně způsobu importu. Na běžné změny stačí dílčí skripty nebo `build_normal.py`.
- **Knihovní meshe mají víc materiálových slotů** (kulatina `Wood`, `EndGrain`, `Bark`; proutí `Daub`, `Wattle`). Dílec kulatiny = `Stone` s `shape` z `ROUND_SHAPES` a `bark`, ostatní knihovní meshe `shape` z `LIB_SHAPES`; délka vždy podél `sx`. Materiál se přiřazuje přes `ue_assets.apply_materials` (slot `wood` = materiál dílce, ostatní `SLOT_MATS`), ne `set_material(0, ...)`.
- **Jedna kopie `zrlib` na běh (15. 11. 2026).** Spouštěč na začátku zahodí moduly z minulého běhu, dál se načítá jen přes `zrlib/pipeline.py`. Dvě kopie knihovny znamenají dvojí stav (materiály slotů `SLOT_MATS`, rozměry meshí `_OBJ_BOX`): 05 pak nevidí, co nastavilo 03.

### 5.3 Capture

- **Capture ručních úprav (03, 05) jen po buildu** se stejnými meshi: capture porovnává instance v levelu s tím, co by build postavil; po změně meshů nebo os by staré instance vyšly jako smazané.

### 5.4 Generátor meshí

- **Rotační tělesa (`mesh_props.add_lathe`):** obrys jde zdola od osy ven, po plášti nahoru a nahoře zpět k ose. Opačné pořadí = normály dovnitř (pád: kotouč brusu, obruče, okraj koše 14. 11. 2026). Kontrola `tools/checks/check_normals.py`.
- **Hranoly (`mesh_props.add_box`):** zaoblení hran musí být funkcí polohy (bod promítnutý na zaoblený kvádr), aby sousední stěny sdílely hranu. Posun lemu po normále každé stěny zvlášť dělal přečnívající lemy a štěrbiny – v UE to vypadalo jako vybarvené vnitřky (kovadlina, ponk, nářadí; opraveno 15. 11. 2026). `check_normals.py` u propů z prolínajících se dílů hlásí falešné poplachy – rozhoduje náhled `preview_meshes.py` (žádné trny a lemy na hranách).

### 5.5 Kód

- **Kód:** komentáře a identifikátory bez diakritiky (UE Python konzole), dokumentace (`*.md`) česky s diakritikou.

## 6. Jak hledat příčinu chyby

Postup, který se osvědčil u poškozených bounds (15. 11. 2026):

1. **Nejdřív log, pak teorie.** Rozděl log po jednotlivých assetech a spočítej, co se u kterého stalo (import, build, Nanite, varování). Rozdíl mezi „funguje“ a „nefunguje“ bývá vidět v počtech (33 kamenů bez `NaniteBuild` proti 78 ostatním).
2. **Hledej, čím se vadné liší od dobrých**, ne co mají vadné společného s teorií. Tady to byl text `bDoFastBuild` v `.uasset`, který Python v UE nevidí.
3. **Test má měnit jednu věc** a mít **kontrolní variantu**, která musí vyjít čistě. Test, který obchází dvě podezřelé věci najednou, nic nerozliší.
4. **Pozor na cache (DDC).** Stejná geometrie a stejné nastavení = stejný klíč = stejná (i poškozená) data bez buildu. Čistý test potřebuje posunutá data, opakování problému původní.
5. **Náhodná chyba se nedokazuje jedním během.** U náhodného NaN je průkaznější vedlejší příznak, který je vždy (chybějící Nanite, varování o tangentách).
6. **Oprava se ověřuje stejným testem** a v ostrém logu se hledá totéž, co ho předtím odlišovalo.
7. **Refaktoring:** `tools/checks/fingerprint.py` před změnou a po ní, výsledek musí být shodný. U záměrné změny chování se nepoužívá.
8. **Vizuální chyba ze screenshotu:** najít příčinu v datech nebo kódu, reprodukovat testem mimo UE, teprve pak opravit.

## 7. Rozhodnutí (aby se neotevírala znovu)

| Datum | Rozhodnutí | Proč |
|---|---|---|
| 11/2026 | 03 a 05 oddělené, sdílená knihovna `zrlib` | dostavby jdou ladit bez přegenerování hradu |
| 14. 11. 2026 | hlavní složka je `skvt_projekt\PrototypeDesigns\Lapikus` | odtud se spouští v UE, je v gitu |
| 14. 11. 2026 | **props vlastní**, procedurálně v Pythonu (`tools/meshes/mesh_props.py`) | styl hradu, vizuální prototyp |
| 14. 11. 2026 | kulatina **s kůrou i bez**, podle stavby | pod kůrou dřevo hnije, nosné se loupe |
| 14. 11. 2026 | jeden generátor meshí `tools/meshes/gen_meshes.py` + moduly podle materiálu, OBJ v `meshes/<kategorie>/` | meshe používá 03 i 05 |
| 14. 11. 2026 | tvary na míru (plátno) jako OBJ, lano a výplet z knihovních dílců | bez Geometry Scriptu v UE |
| 14. 11. 2026 | **dům posádky v prostřední místnosti paláce**; varianta u věže zavržená | ve východní místnosti má být kovárna, komín u věže má špatný tah |
| 14. 11. 2026 | brus v kovárně **šlapací**, s třínohou stoličkou | – |
| 14. 11. 2026 | věž: průlomy z dobývání ve `Vez_V` a `Vez_J` místo rovného snížení; přístřešek varianta B | hrad se dobýval od východu a jihovýchodu; posádka by zeď kvůli plachtě nebourala |
| 15. 11. 2026 | meshe se importují přes dočasný asset, cíl s `bDoFastBuild` se maže, vlastní klíč cache (`BUILD_CFG`) | kap. 5.2 |
| 15. 11. 2026 | dva celkové buildy: `build_normal.py` (aditivní) a `build_fullscope.py` (oprava); fullscope materiály ve výchozím stavu nemaže | ruční ladění materiálů se nemá ztratit |
| 15. 11. 2026 | level je celý generovaný skriptem, skripty můžou počítat s prázdným projektem | Jirka může cokoli generovaného ručně smazat |

**Nerozhodnuto** (neber jako dané): umístění kovárny ve východní místnosti (jen předpoklad), jestli bude stan na nádvoří, přiřazení kůra / loupané u jednotlivých staveb, výstup na podestu brány, přepínání etap, použitelnost žebříků, poloha cisterny. Aktuální seznam: `CHECKLIST_assets_navrhy.md` kap. 9 a `AGENT_GameDesign_hrad.md` kap. 6.

## 8. Kde co je

| Potřebuju | Dokument |
|---|---|
| aktuální stav hradu a poslední rozhodnutí | `03_ruin/Zricenina_03_ruin_stav.md` (platí přednostně) |
| jak je zeď složená, úpravy v datech, objemy v levelu | `03_ruin/blocks/README_bloky.md` |
| dostavby, parametry, materiály, knihovní meshe | `05_constructions/README_constructions.md` |
| předloha, půdorys, hratelnost | `03_ruin/README_ruin.md` |
| návrhy dalších staveb | `new_designs/navrh_*.md` |
| co návrhy potřebují a co je hotové | `CHECKLIST_assets_navrhy.md` |
| terén, řeka, les, souřadnice projektu | `README_PROJEKT.md` |
| role a šablony agentů | `AGENT_Architekt_hrad.md`, `AGENT_GameDesign_hrad.md`, `AGENT_Stavitel_hrad.md` |
| nastavení vzhledu, verze assetů | `zrlib/config.py` |
