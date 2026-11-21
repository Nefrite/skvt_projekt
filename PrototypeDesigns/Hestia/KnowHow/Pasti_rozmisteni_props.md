---
# orchestrace
type: knowhow
knowhow_kind: pitfall
tech: [ue_python, python]
scope: instance
verified: 2026-11-21
validity: valid
updated: 2026-11-21
aliases: []
# hra
domain: structures
---
# Pasti: rozmístění props a vybavení

<!-- Z KNOWHOW_hrad.md kap. 5.7, AGENT_Furnisher_hrad.md kap. 8 (pasti, které KNOWHOW nemá) a kap. 1 pravidla 3 a 6 (pilot Lapikus, B6). -->

- **Poloha propu = střed jeho bounding boxu**, ne funkční střed. Meshe z `mesh_props.py` jsou normalizované na bounding box (pivot uprostřed), takže například výfučna měchů je 105 cm od středu, rám brusu 7 cm a deska ponku 8,4 cm mimo střed. Odsazení zjisti z funkce propu (surové vrcholy) a zapiš ho do specu (`palac_spec.kovarna_vybaveni`).
- **Natočení:** zadává se směr lokální osy X v rámu stavby; lokální Y je X otočená v UE o +90°. V rámu paláce (levotočivý vůči `s`, `n`) je pro X = +s osa Y = −n, pro X = −n osa Y = −s. Svisle zavěšené nářadí: `pitch` 90 (X nahoru), kladivo `roll` −90 (Y dolů, hlava nahoře); `roll` se do UE posílá obráceně ([[Pasti_geometrie_a_data]]), ve specu piš hodnotu výpočtu.
- **Kontroly kvádrem jsou hrubé:** bounding box propu (měchy, sudy) koliduje i tam, kde skutečný tvar ne. Záměrné dotyky (výfučna v otvoru, lano kolem krokve, kolíky ve spárách) vyjmi jmenovitě a zkontroluj zvlášť přesným bodem (špička výfučny v otvoru).
- **Poloha z levelu má přednost před specem:** změna specu u kusu s `captured` se neprojeví (generátor to vypíše). Nejčastější důvod „změnil jsem spec a v UE se nic nestalo“.
- **Kopie kusu má vlastní id, ale mesh původního kusu** (`mesh`): varianta meshe se jinak vybírá podle id a kopie by vypadala jinak.
- **Rám skupiny jde ze specu:** posun rámu (`origin`, `u`, `v`) posune i kusy s polohou z levelu, výška se počítá od terénu. Je to záměr (kusy jdou se stavbou).
- **Souběžný zápis:** capture v UE a tvoje generování zapisují stejný `furnishing.json`. Vždy md5 před zápisem; při pochybnosti `furnishing.json.bak`.
- Kus těsně u zdi: mezera ≥ 3,5 cm, kontrola průnikem (5.5).
- **Hromada z mnoha kusů a ruční přeskládání** (ověřeno 21. 11. 2026, staveniště domu): kusy s `loose: false` dá build do jednoho Instanced Static Mesh stavby (materiál × sada etapy, `build_constructions.build_in_unreal`). Takový actor stojí v počátku světa a jeho posun běžný capture neuloží (další build ho vrátí). `loose: true` naopak dělá z každého kusu samostatný actor, takže hromada se rozpadne na desítky objektů. Když se má hromada v UE posouvat jako celek, udělej ji jako samostatnou stavbu s `"pile": true`: build postaví jeden ISM actor s pivotem dole uprostřed a capture uloží jeho polohu a natočení (`moved["pile:<stavba>"]`, `build_constructions._pile`). Ověřeno mimo UE, v UE zatím ne. Výšky všech kusů hromady měř od terénu v jednom bodě (klíč `ref` u položky `props`), jinak se hromada na nerovném terénu rozláme po kusech.
- **Zvětšení kusu v levelu ho zapustí do podlahy** (ověřeno 21. 11. 2026, graybox Guesthouse): Scale actoru roste od pivotu; graybox kvádr (Cube) má pivot uprostřed, takže při zvětšení výšky klesne spodek pod podlahu (stůl zvětšený na 95 cm byl 9,5 cm v podlaze) a capture uloží nižší `z`. Po capture spusť kontrolu „vybavení stojí na podlaze“ (`run_checks.py --only ostroh`) a výšku srovnej v datech. Meshe props mají pivot na zemi, tam se to neděje.
- **Vybavení na prkenné podlaze měř od vrchu prken, ne od terénu** (21. 11. 2026): `props` měří `z` od terénu pod kusem; podlaha (`plank_floor`) je ale vodorovná 10 cm podvalů + prkna nad nejvyšším terénem v obrysu. Dej všem kusům společný `ref` a `z` = vrch prken nad terénem v `ref` (Guesthouse: `gen_furnishing.guesthouse()` přes `zr_stavby.podlaha.floor_top`); po změně terénu nebo podlahy přegeneruj.
- Starý `furnishing_edits.json` se už nepoužívá; když se objeví, build vypíše upozornění. Jeho obsah ručně přenes jen po dohodě.

3. **`06_furnishing/furnishing.json` je jediný zdroj poloh vybavení** a obsahuje i Jirkovy ruční úpravy z levelu ([[Kod_spousteni_kontroly_z_roli]], Furnisher kap. 4). Generuj ho **jen přes `tools/furnishing/gen_furnishing.py`** (slučuje, polohy z levelu nechá). Nikdy ho nepřepisuj vlastním skriptem a nemaž z něj kusy s příznakem `captured`, `removed` nebo `manual` bez Jirkova souhlasu. `manual_edits.json` (03) a `constructions_edits.json` (05) nepřepisuj vůbec.
6. Mazání souborů jen na výslovný pokyn. `furnishing.json.bak` (záloha z posledního zápisu) nemaž, je to jediná cesta zpět po chybném capture nebo generování.
