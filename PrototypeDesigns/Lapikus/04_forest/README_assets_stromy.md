# 04 Forest – assety stromů a rostlin (Quixel Megaplants)

Výběr volně dostupných rostlin pro lokaci Zřícenina (podle seznamu dostupných Megaplants, listopad 2026) a postup, jak je dostat do projektu `skvt_projekt` (UE 5.8).
Zdroj: [Quixel Megaplants na Fabu (Free)](https://www.fab.com/sellers/Quixel%20Megaplants?is_free=1).
Kam se stromy rozmístí, popisuje `README_forest.md`.

---

## 1. Co jsou Megaplants

Megaplants **nejsou hotové modely stromů k přetažení do levelu**. Jsou to podklady pro **Procedural Vegetation Editor (PVE)**:

- preset (graf) pro daný druh, postavený ze skenů skutečných rostlin
- meshe větví s listy, textury a material instance
- ovládání tvaru, velikosti a větvení

Z jednoho balíku si v PVE vygeneruješ libovolný počet variant stromu a **exportuješ** je jako Nanite Foliage (s větrem) nebo jako Static Mesh. Teprve exportované stromy se dávají do levelu, do PCG a do `place_alders.py`.

| | |
|---|---|
| Cena / licence | zdarma, **Fab Standard License** (ověř u každé položky, že je označená *Free*) |
| Engine | **UE 5.8**: původní balíky pro 5.7 Quixel převedl na 5.8; nové vycházejí jen pro 5.8+ |
| Kompatibilita | podklady PVE z 5.7 **nejdou otevřít v 5.8**. Při stahování vždy vyber verzi 5.8 |
| Stav | Megaplants, PVE, Nanite Foliage i Dynamic Wind jsou **Experimental**: na prototyp v pořádku, při vydání hry opatrně |

---

## 2. Výběr pro lokaci

### 2.1 Skutečná lokalita

Předloha, zřícenina **Lapikus**, stojí na ostrohu nad **Plenkovickým potokem** u Plavče na Znojemsku (Jevišovicko, jižní Morava).
Přirozeným lesem tam není bučina, ale **dubohabřina**: dub a habr s lískou, na stinných svazích údolí buk a javor, na skalnatých výchozech borovice, bříza a vřes. Podle toho je les rozdělený do zón (mapa v `Zricenina_les_plan.png`):

| Zóna | Kde | Plocha | Skladba (podíl stromů) |
|---|---|---|---|
| **A1 – dubohabřina** | slunné svahy, hřbet, plošiny | ~23 600 m² (~390 stromů) | dub letní 40 %, habr 35 %, javor 10 %, osika 5 %, buk 5 %, jeřáb 5 % · podrost líska, brslen, kapraď |
| **A2 – stinné svahy k severu** | svahy obrácené k S, hlavně severní svah ostrohu nad řekou | ~8 200 m² (~140 stromů) | buk 45 %, habr 25 %, javor 20 %, smrk 5 %, dub 5 % · podrost zmlazení buku a javoru, sasanka, netýkavka |
| **B – okraj lesa** | pás kolem řeky, hradu a cesty | ~9 400 m² | osika, bříza, jeřáb, dub · keře líska, bez, brslen, zmlazení osiky |
| **D – sráz 38–50°** | strmé svahy | ~4 000 m² | habr, dub, bříza, ojediněle borovice · líska |
| **K – skalnaté podloží** | dle náčrtu JV od hradu | ~1 200 m² | borovice lesní 50 %, bříza 30 %, suchá borovice 10 %, dub 10 % · vřes, borůvka, brusinka |
| **R – řeka** | břehy | 41 stromů | olše lepkavá, na jesepu část vrba jíva · orobinec, rákos, netýkavka, kopřiva |
| **C – hrad** | plocha zříceniny | bez stromů | kopřiva a bez u zdí, zmlazení jeřábu a osiky v sutích |
| **P – stará cesta** | stezka ke hradu | bez stromů | tráva, kapraď, zmlazení buku a osiky na okrajích |

Expozici svahu (A1 / A2) pozná PCG podle normály terénu: svah obrácený k severu = A2.

### 2.2 Co z nabídky použít

Priorita: **A** = potřeba pro první verzi, **B** = vylepšení, **C** = detail.

**Stromy**

| Megaplant | Česky | Zóny | Priorita |
|---|---|---|---|
| English Oak | dub letní | A1, B, D, K | **A** |
| European Hornbeam | habr obecný | A1, A2, D | **A** |
| European Beech | buk lesní | A2, A1 (příměs) | **A** |
| Norway Maple Forest | javor mléč | A1, A2 | **A** |
| Black Alder | olše lepkavá | R (`place_alders.py`) | **A** |
| European Aspen | osika | B, A1 | B |
| Silver Birch | bříza bělokorá | K, B, D | B |
| Baltic Pine | borovice lesní | K, D (skalní výchozy) | B |
| Goat Willow | vrba jíva | R – jesep (`place_alders.py`, `WILLOW_MESHES`) | B |
| Norway Spruce | smrk ztepilý | A2 (jednotlivě) | C |
| Dead Pine | suchá borovice | K – solitér | C |
| Black Poplar | topol černý | R – 1–2 velké stromy na jesepu | C |

**Zmlazení (mladé stromy)**

| Megaplant | Česky | Zóny | Priorita |
|---|---|---|---|
| European Beech Saplings | buk | A2, okraje P | B |
| Norway Maple Saplings | javor | A1, A2 | B |
| European Aspen Saplings | osika | B, C (sutě), P | B |
| Rowan Saplings | jeřáb ptačí | B, C (sutě), K | B |
| Baltic Pine Saplings | borovice | K | C |

**Keře a byliny**

| Megaplant | Česky | Zóny | Priorita |
|---|---|---|---|
| Common Hazel | líska | podrost A1, B, D | **A** |
| Elder | bez černý | C (u zdí), B | B |
| Stinging Nettle | kopřiva | C (u zdí), R | B |
| Bracken Fern | hasivka orličí (kapraď) | A1 podrost, P okraje | B |
| Common Heather | vřes | K | B |
| Bilberry | borůvka | K, A1 kyselé svahy | B |
| European Spindle | brslen | B, A1 podrost | C |
| Lingonberry | brusinka | K | C |
| Wood Anemone | sasanka hajní | A2 podrost | C |
| Small Balsam | netýkavka malokvětá | R, A2 vlhký podrost | C |
| Common Bulrush | orobinec | R – mělčiny na jesepu | C |
| Dry Common Reed | suchý rákos | R – mělčiny | C |

**První verze (priorita A, 6 balíků):** dub, habr, buk, javor, olše, líska.

### 2.3 Co nepoužít

Do přirozeného lesa na jižní Moravě nepatří:

| Megaplant | Proč ne |
|---|---|
| Aleppo Pine, Utah Juniper, Greasewood, Huckleberry Oak | středomořské / americké suché oblasti |
| Giant Bamboo, Ginkgo, Japanese Cypress, Japanese Medlar, Yoshino Cherry | asijské, okrasné |
| Beach Rose | přímořský keř, u nás jen okrasný / invazní |
| Japanese Knotweed | invazní. Realistický u zanedbaných potoků, ale do „zapomenuté zříceniny“ se nehodí. Případně jen 1–2 trsy u řeky. |

## 3. Než začneš stahovat: velikost repozitáře

Repo `skvt_projekt` **nemá Git LFS** a GitHub odmítne soubor > 100 MB. Doporučený postup:

1. **Zdrojové balíky Megaplants nedávat do gitu.** Složku, kterou Fab do projektu vytvoří (zjistíš po prvním stažení v Content Browseru), přidat do `.gitignore`. Každý, kdo na projektu dělá, si balíky přidá z Fabu sám (zdarma).
2. **Exportované stromy do gitu dát.** Ukládat je do `Content/Skvt/Lapikus/Vegetation/` a před commitem zkontrolovat velikost souborů. Nanite Assemblies bývají malé (v dokumentaci Epicu klesl strom ze 3,5 GB na ~29 MB).
3. Pokud by některý export přesto přesáhl 100 MB: zapnout Git LFS pro `Content/Skvt/Lapikus/Vegetation/**`, nebo snížit počet variant či detail.

Pozor: pokud mapa odkazuje na asset, který je v `.gitignore`, ostatním se po klonování nenačte. Do levelu proto dávej **jen exportované stromy** z `Vegetation/`, nikdy přímo obsah zdrojových balíků.

---

## 4. Příprava projektu (jednorázově)

1. **Edit → Plugins**, zapnout:
   - **Procedural Vegetation Editor**: sekce Experimental / Other
   - **Procedural Content Generation Framework (PCG)**: pro rozmístění lesa
   - **Dynamic Wind** (Experimental, Rendering): pohyb stromů ve větru, volitelné
2. **Edit → Project Settings → Rendering** → zapnout **Nanite Foliage** (Experimental).
3. Restartovat editor.
4. Zkontrolovat, že se změny zapsaly do `skvt_projekt.uproject` a `Config/DefaultEngine.ini`, a commitnout je.

Bez zapnutého Nanite Foliage ukáže editor při otevření stromu varování (Nanite Assembly).

---

## 5. Stažení z Fabu do projektu

### Varianta A – přímo v editoru (doporučeno)

1. V UE 5.8 otevřít **Fab** (tlačítko Fab v Content Browseru, nebo **Window → Fab**) a přihlásit se Epic účtem.
2. Vyhledat **Quixel Megaplants** a otevřít druh, např. *Megaplants: European Beech*.
3. Kliknout na **Add to My Library** (zdarma), pak **Add to Project**.
4. Asset se stáhne a objeví v Content Browseru.

### Varianta B – přes web a Epic Games Launcher

1. Na [fab.com](https://www.fab.com/sellers/Quixel%20Megaplants?is_free=1) přihlásit se, u každého druhu kliknout na **Add to My Library**.
2. **Epic Games Launcher → Unreal Engine → Fab Library**: najít balík → **Add to Project** → vybrat `skvt_projekt` a verzi **5.8**.

### Po stažení

- Poznamenat si, kam balík přibyl (cestu v Content Browseru), a přidat ji do `.gitignore` (kap. 3).
- Opakovat pro všech 6 balíků priority A (dub, habr, buk, javor, olše, líska).

---

## 6. Vygenerování a export stromů v PVE

Postup pro každý druh:

1. V Content Browseru otevřít složku balíku a dvojklikem otevřít jeho **Procedural Vegetation Graph** (preset druhu).
2. V grafu najít uzel **Grower** a v jeho sekci presetů vybrat variantu druhu. Balík obsahuje více velikostí a struktur.
3. Měnit **Seed** a parametry tvaru (výška, větvení), až vzniknou 3–4 rozdílné stromy:

| Varianta | Použití |
|---|---|
| `_Mature_01`, `_Mature_02` | vzrostlé stromy v lese (zóna A) |
| `_Young_01` | okraje, srázy, jesep (B, D) |
| `_Leaning_01` (volitelně) | na srázy a u řeky |

4. Na konci grafu je uzel **Export**:
   - typ **Nanite Foliage** (vítr přes Dynamic Wind), nebo **Static Mesh** (jednodušší, bez větru)
   - cílová složka: `Content/Skvt/Lapikus/Vegetation/<Druh>/`, např. `Vegetation/Beech/`
   - název: `NF_Beech_Mature_01`, `NF_Beech_Young_01`… (`NF_` = Nanite Foliage, `SM_` = static mesh)
5. Spustit export a ověřit, že asset vznikl ve složce `Vegetation/`.

Graf v PVE slouží jen k náhledu. **Do levelu jde vždy exportovaný asset.**

Doporučený počet pro první verzi:

| Druh | Variant |
|---|---|
| dub | 3–4 |
| habr | 3 |
| buk | 3 |
| javor | 2–3 |
| olše | 3 |
| líska | 2–3 (keř) |

---

## 7. Test a napojení na les

1. **Test:** exportovaný strom přetáhnout do `LapikusPrototypeMap` vedle Player Startu a pustit Play. Zkontrolovat:
   - měřítko vůči postavě (dospělý buk a dub mají 25–35 m, habr 15–25 m, olše 15–25 m)
   - vítr (pokud je zapnutý Dynamic Wind)
   - LOD přechody při oddalování
2. **Olše:** u olšových exportů dát v Content Browseru pravé tlačítko → **Copy Reference** a vložit do `ALDER_MESHES` v `place_alders.py`. Pak skript spustit (`README_forest.md` kap. 5.1).
3. **Les (PCG):** exporty přidat do uzlů **Static Mesh Spawner** v grafu `PCG_Forest` s váhami podle kap. 2.1 (zvlášť pro A1, A2, B, D, K).
4. **Vrba jíva:** exporty vložit do `WILLOW_MESHES` v `place_alders.py`. Asi třetina stromů na jesepu pak bude vrba místo olše.
5. **Commit:** jen `Vegetation/`, mapu a nastavení projektu, ne zdrojové balíky.

---

## 8. Řešení problémů

| Problém | Řešení |
|---|---|
| Balík nejde otevřít, chyby PVE | Stažená verze pro 5.7. V Fabu přidat znovu a vybrat 5.8. |
| Varování o Nanite Assembly / Foliage | Zapnout Project Settings → Rendering → Nanite Foliage, restartovat. |
| Stromy se nehýbou ve větru | Zapnout plugin Dynamic Wind. Export musí být typu Nanite Foliage, ne Static Mesh. |
| Viditelné přeskakování LOD | Známý problém Megaplants (diskuse na fóru bez řešení). Na prototyp nevadí. |
| Výkon při velkém počtu stromů | Na komponentě snížit **Animation Min Screen Size** (vítr se vypne u vzdálených stromů). Globálně `r.Skinning.DefaultAnimationMinScreenSize`. |
| Kolega po klonování nevidí stromy | V levelu je asset ze zdrojového balíku v `.gitignore`. Nahradit exportem z `Vegetation/`. |
| Soubor > 100 MB odmítnut GitHubem | Viz kap. 3: Git LFS nebo méně variant / nižší detail. |

---

## 9. Checklist

1. ☐ Rozhodnout git strategii (kap. 3)
2. ☐ Zapnout pluginy PVE, PCG, (Dynamic Wind) a Nanite Foliage, commitnout nastavení
3. ☐ Přidat z Fabu (verze 5.8): dub, habr, buk, javor, olše, líska
4. ☐ Zdrojové složky do `.gitignore`
5. ☐ Export variant do `Content/Skvt/Lapikus/Vegetation/<Druh>/`
6. ☐ Test v levelu (měřítko, vítr)
7. ☐ Olše přes `place_alders.py`
8. ☐ Les přes `PCG_Forest`
9. ☐ Priorita B: osika, bříza, borovice, vrba jíva, zmlazení, bez, kopřiva, kapraď, vřes, borůvka

---

## Zdroje

- [Quixel Megaplants – Fab (Free)](https://www.fab.com/sellers/Quixel%20Megaplants?is_free=1)
- [Quixel: Discover the latest Megascans and free Megaplants (16. 7. 2026)](https://quixel.com/news/discover-the-latest-quixel-megascans-and-free-megaplants)
- [Quixel: Recently released Megascans and Megaplants (9. 10. 2026)](https://quixel.com/news/check-out-these-recently-released-quixel-megascans-and-megaplants)
- [Epic: Procedural Vegetation Editor](https://dev.epicgames.com/documentation/unreal-engine/procedural-vegetation-editor-in-unreal-engine?lang=en-US)
- [Epic: Nanite Foliage](https://dev.epicgames.com/documentation/unreal-engine/nanite-foliage)
- [Fórum: Megaplants European Beech](https://forums.unrealengine.com/t/quixel-megaplants-megaplants-european-beech/2674655)
- [80.lv: Free Quixel vegetation assets for UE 5.7](https://80.lv/articles/create-lush-nanite-foliage-ready-forests-with-this-free-quixel-asset-pack)
- [Jevišovicko: zřícenina Lapikus](https://jevisovice.info/aktivity/castle-ruins-lapikus)
