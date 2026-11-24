---
# orchestrace
type: handover
validity: archived
superseded_by:
for_role: [Builder]
updated: 2026-11-24
# hra
domain: structures
entity: "[[Brana]]"
build_step: 05_constructions
---
# Brana – šíjový příkop, terénní valy, mostní lávka a zátaras: předání staviteli

## Pro koho a co
Pro roli **Builder**: podle schváleného návrhu [[navrh_brana_prikop]] vygenerovat/upravit terén hlavního šíjového příkopu, čelních valů a severní únikové rampy před východní branou ([[01_terrain]]), doplnit kamenný mostní pilíř `Brana_Pilir` a vnější opěru `Brana_Opera` do zříceniny ([[03_ruin]]) a postavit vyrovnávací zdivo `Brana_Most_Kamen`, dřevěnou mostní lávku `Brana_Most` a přenosný zátaras `Brana_Zataras` ([[05_constructions]], obojí včetně napojení na úkol `T-0036`).

## Zadání
1. **Terén příkopu, valů a únikové rampy ([[01_terrain]]):**
   - Podle [[navrh_brana_prikop]] § *1. Šíjový příkop, terénní valy a úniková rampa* a § *Souhrn specifikace* (bod 1) upravit generování výškopisu (`Lapikus/01_terrain/Zricenina_heightmap_505_50cm.png`, `Zricenina_preview_orez.png` a `Lapikus/03_ruin/blocks/terrain_from_level.json`):
     - v oblasti pod hradem a strážní věží (`u <= 8,1 m`) zasypat starý příkop (`t_rel = 37 m`) převzetím výšek z `terrain_from_level.json`, aby se nezměnila pata žádné stávající zdi;
     - východně od `Brana_V` a `Hradba_V` vyhloubit šíjový příkop (`u_in(d) = 8,10 - 1,10 * ss(6,5, 11,5, d)`, horní šířka `8,20 m`, dno šířky `3,80 m` na `Z = 2700 cm`, skalní stěny `54°–63°`), na severním konci (`d = -1,0 .. -5,5 m`) vymodelovat únikovou rampu ze dna příkopu (`sklon 25,1° < 44°`, šířka `2,0 m`) a před příkopem (`u = 16,3 .. 23,5 m`) navršit jižní a severní křídlo čelního valu s přístupovým úvozem (`d = 1,50 .. 4,70 m`, předmostí `Z = 3040 cm`).
   - Pokud by reimport PNG do UE Landscape kolidoval s levelovými úpravami, použít záložní pomocný Python skript v UE Editoru, který výškovou změnu příkopu a valů (`u >= 8,1 m`) zapíše přímo do Landscape actoru v `/Game/Skvt/LapikusPrototypeMap`.
2. **Zřícenina – mostní pilíř a opěra ([[03_ruin]], část `Obvod`):**
   - V `Lapikus/tools/ruin/gen_layout.py` rozšířit východní okraj mřížky `terrain` z `x1 = 3600` na `x1 = 4400` a přidat zdi `Brana_Pilir` (`3,0 × 1,4 m` v `u = 12,20 m, d = 1,60 .. 4,60 m`) a `Brana_Opera` (`3,2 × 1,2 m` v `u = 16,30 m, d = 1,50 .. 4,70 m`) ve složce `Ruin/Brana` podle [[navrh_brana_prikop]] § *2.2*.
   - V `Lapikus/tools/ruin/brana_spec.py` doplnit do `ruin_edits(walls)` zarovnání koruny (`cap`) `Brana_Pilir` a `Brana_Opera` na `z = 3011 cm`.
3. **Dostavba – lávka `Brana_Most`, podložení `Brana_Most_Kamen` a zátaras `Brana_Zataras` ([[05_constructions]]):**
   - Do `Lapikus/tools/ruin/brana_spec.py` doplnit parametry `B_BRIDGE_BEAM_Z = 3011.0`, `B_BRIDGE_BEAM`, `B_BRIDGE_DECK`, `B_BRIDGE_FILL`, `B_ZATARAS` a funkci `most(walls)` podle [[navrh_brana_prikop]] § *3* a § *Souhrn specifikace* (bod 2).
   - V `Lapikus/tools/constructions/gen_constructions.py` vygenerovat do `constructions.json` stavby `Brana_Most_Kamen` (`stone_fill`, sada `base`), `Brana_Most` (`platform`, sada `base`, vrch mostovky `Z = 3040 cm`) a `Brana_Zataras` (`props` / samostatný actor na předmostí v `u = 17,20 m, d = 3,10 m, Z = 3040 cm`, sada `base`; řeší i úkol `T-0036`) a vstupní skripty v `Lapikus/05_constructions/stavby/`.
4. **Dokumentace:**
   - Po postavení a ověření v UE aktualizovat [[Zricenina_03_ruin_stav]], [[stav_brana_straz]] a založit/aktualizovat stavový dokument pro [[Brana]].

## Platná rozhodnutí
- Schválený návrh příkopu, valů, únikové rampy, mostního pilíře, lávky a zátarasu (rozhodnutí GameDesignera 2026-11-23): [[navrh_brana_prikop]].
- Navazující strážní stanoviště nad branami: [[navrh_brana_straz]], [[stav_brana_straz]].
- Konvence kroků 03 / 05 / 06 a souřadnicových rámců: [[Konvence_03_05_06_a_spec]], [[Konvence_souradnice_a_ramce]], [[Zmer_skutecny_stav]].

## Výchozí stav
- Stav zříceniny a východní brány: [[Zricenina_03_ruin_stav]], [[stav_brana_straz]].
- Měření souřadnic a výšek terénu před bránou k 2026-11-23: [[navrh_brana_prikop]] § *Výchozí stav*.

## Kritéria hotovo
- `python Lapikus/tools/checks/run_checks.py` projde bez chyby (žádné plovoucí kameny ani kolize otvorů).
- V UE Editoru (mapa `/Game/Skvt/LapikusPrototypeMap`) je vykopán šíjový příkop s obnaženou 3,4m podstavbou `Brana_V`, skalními stěnami (`> 42°`), čelními valy s přístupovým úvozem, severní únikovou rampou (`25,1° < 44°`), kamenným pilířem `Brana_Pilir`, opěrou `Brana_Opera`, dřevěnou lávkou `Brana_Most` (vrch `Z = 3040 cm`) a zátarasem `Brana_Zataras` (`u = 17,20 m, d = 3,10 m, Z = 3040 cm`).
- Herní test (`Play`) potvrdí plynulý přechod po lávce do brány i schůdný únik ze dna příkopu po severní rampě ven před valy (viz [[navrh_brana_prikop]] § *Ověření*).

## Otevřené otázky
_Žádné otevřené otázky (všechny body zadání rozhodl GameDesigner 2026-11-23 v [[navrh_brana_prikop]])._

## Zbývá
- [x] Upravit výškopis terénu (`01_terrain`: `tools/terrain/gen_moat.py` → `Zricenina_heightmap_505_50cm.png`, `Zricenina_preview_orez.png`, `terrain_from_level.json` rozšířený na `x1 = 4400`, záložní/ověřovací skript `01_terrain/UE_Prikop_Landscape.py`; **čelní valy zrušeny 2026-11-24 na pokyn GameDesignera**), doplnit vnější ozub v `Brana_V`, `Brana_Pilir` a `Brana_Opera` (`03_ruin`) a `Brana_Most_Kamen`, `Brana_Most`, `Brana_Zataras` (`05_constructions`, včetně `T-0036`) a ověřit mimo UE (`run_checks.py` bez chyby, náhled `05_constructions/Stavby_brana_prikop_nahled.png`, stav zapsán v [[stav_brana]]) — Builder, 2026-11-24.
- [x] Reimport terénu, přestavění `Obvod` a `Brana.py` a ověření v UE Editoru (`/Game/Skvt/LapikusPrototypeMap`) — GameDesigner (Jirka), 2026-11-24.
