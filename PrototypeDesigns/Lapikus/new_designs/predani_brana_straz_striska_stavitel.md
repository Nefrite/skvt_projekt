# Strážní stanoviště nad branami – stříška z kůry (etapa 2): návrh a instrukce pro stavitele

Stav: 16. 11. 2026. Připravil architekt (session s Jirkou). **Návrh, nepostaveno.** Nahrazuje kap. 4.4 v `navrh_brana_straz.md`: ta počítala s podestou a kryty, které dnes vypadají jinak.

Čti spolu s: `AGENT_Stavitel_hrad.md`, `KNOWHOW_hrad.md`, `new_designs/navrh_brana_straz.md` kap. 0 (skutečný stav stanoviště), `tools/ruin/brana_spec.py`.

## 1. Zadání

- **Účel:** suché místo pro stráž u východního krytu, odkud se dívá průzory před bránu.
- **Etapa:** celá stříška je sada `final` (v etapě 1 ještě nestojí).
- **Styl:** provizorium z toho, co je po ruce. Tyče a kulatina s kůrou, vázané spoje, krytina z pásů smrkové kůry (zbyla z loupání kulatiny na dům).
- **Zříceninu neměň.** Všechno je dostavba 05.

## 2. Výchozí stav (změřeno z dat 16. 11. 2026)

Rám brány: `u` k východu podél `Brana_S`, `d` k jihu, počátek v SZ rohu věže. Výšky jsou níž **v metrech nad podlahou podesty** (vrch podlahy = `deck_z` = Z 3581 v `brana_spec.straz()`), v datech je zadávej absolutně v UE cm.

| Co | Kde |
|---|---|
| podlaha podesty | u = 0,2–6,27; d = −0,55 až 5,25 |
| trámy pod podlahou | d = −0,2 (na `Brana_S`) / 1,3 / 3,15 / 5,0 |
| koruna `Brana_V` mezi podlahou a východním krytem | u = 6,3–7,4; 0,36 m nad podlahou (Z 3617), místy 0,73 m (d = 4,3–5,1 u vnitřního líce) |
| východní kryt | osa u = 7,5; kůly Ø 18–22 cm; vrch 1,76–1,84 m; ráhna zevnitř (u ≈ 7,34) ve výšce 0,55 a 1,22 m |
| průzory východního krytu | d = 1,5 / 3,1 / 4,6; od 1,35 m nahoru |
| severní kryt | osa d = −0,75; vrch 1,25 m |

## 3. Návrh

Pultová stříška v severovýchodním koutě, spád 22° k východu. Voda stéká přes východní kryt ven před bránu. **Kostra je samostatná, o kryt se neopírá**: nahoře u krytu není ráhno (vedlo by přes průzory) a kůly mají špičky.

### 3.1 Kostra

| Prvek | Průřez | Počet a délka | Poloha | Na čem stojí nebo leží |
|---|---|---|---|---|
| západní sloupky | kulatina s kůrou Ø 14 cm | 2 ks, 3,2 m | u = 4,0; d = 1,3 a 3,15 | na podlaze přesně nad trámy podesty |
| východní sloupky | kulatina s kůrou Ø 14 cm | 2 ks, asi 1,55 m | u = 7,15; d = 0,8 a 3,7 | na koruně `Brana_V` (pata kopíruje kámen), 0,35 m za kůly krytu |
| západní vaznice | tyč s kůrou Ø 12 cm | 1 ks, 3,4 m | u = 4,0; d = 0,3–3,7; vrch 3,32 m | na západních sloupcích |
| východní vaznice | tyč s kůrou Ø 12 cm | 1 ks, 3,6 m | u = 7,15; d = 0,3–3,9; vrch 2,05 m | na východních sloupcích |
| krokvičky | tyče s kůrou Ø 8 cm | 7 ks, 4,55 m | d = 0,5 až 3,5 po 0,5 m; u = 3,75–7,95 | na obou vaznicích, přivázané |
| příčné tyčky pod kůru | tyče s kůrou Ø 5 cm | 6 ks, 3,5 m | napříč krokvičkami po 0,8 m po spádu, d = 0,25–3,75 | na krokvičkách |
| vzpěrky | tyče s kůrou Ø 8 cm | 4 ks, 0,7 m | šikmo 45° od západních sloupků k vaznici (na obě strany podél d) | zavětrování |

- **Východní sloupky nesmí stát za průzory.** Průzory jsou v d = 1,5 a 3,1, sloupky v d = 0,8 a 3,7 (odstup 0,6 m).
- **Krokvičky jdou těsně nad špičkami kůlů:** spodek krokvičky je nad osou krytu (u = 7,5) v 1,91 m, nejvyšší špička v 1,84 m. Kdyby se v UE dotýkaly, zvedni obě vaznice o 5 cm.
- **Světlá výška** pod krokvičkami: u východního sloupku 2,05 m, u západní vaznice 3,2 m.
- **Přesahy:** na východě 0,45 m za osu krytu (okap), na západě 0,25 m za vaznici.
- **Spoje jsou vázané:** na každém styku krokvičky s vaznicí a vaznice se sloupkem ovázání `SM_RuinLashing`.

### 3.2 Krytina

- **Pásy kůry** `SM_RuinBarkStrip` (jmenovitě 1,6 × 0,7 m), hrubou stranou nahoru, delší stranou po spádu.
- **3 řady po spádu** s přesahem 0,2 m: horní řada vždy překrývá spodní. Délku pásu dopočítej tak, aby tři řady pokryly celou délku krokviček (vychází asi 1,64 m).
- **V řadě 6 pásů** vedle sebe s bočním přesahem 0,1 m; sousední řady jsou posunuté o půl pásu.
- **Půdorys krytiny:** u = 3,7–8,0; d = 0,25–3,75 (4,3 × 3,5 m).
- **3 přítlačné tyče** Ø 6 cm s kůrou napříč (podél d), po jedné na každém přesahu řad a jedna u okapu, přivázané na koncích ke krajním krokvičkám.
- Pásy lehce náhodně natoč (do ± 3°) a posuň (do ± 3 cm), ať krytina nevypadá jako mřížka.

### 3.3 Co zůstává volné

- Na severu je mezi vrchem severního krytu (1,25 m) a stříškou volný pruh na střelbu.
- Jižní část podesty (d > 3,9) a celá západní polovina zůstávají pod širým nebem; tam bude výlez.

## 4. Jak to postavit

- **Nový typ `bark_roof`** v `05_constructions/zr_stavby/` (použije ho i stříška stanu na nádvoří, piš ho obecně). Zápis do `TYPES`, `REQUIRED` a `CNAME` v `build_constructions.py`.
- **Rozměry do `tools/ruin/brana_spec.py`** (konstanty `B_ROOF_*`, výstup ve `straz()`), data přes `gen_constructions.py` → `brana()`. Výšky absolutně: `deck_z` + výška nad podlahou.
- **Stavba:** `Brana_Straz_Pristresek`, složka `Stavby/Brana`, `stage = "final"`. Spouštěč `stavby/Brana_Straz_Pristresek.py` a zápis do seznamu `STAVBY` v `stavby/Brana_Straz.py`.
- **Dílce:**
  - sloupky Ø 14: `shape = "round"`, `bark = True` (vyjde `SM_RuinLogBark`), svisle (`pitch = 90`);
  - tyče do Ø 11: `shape = "round"`, `bark = True` (vyjde `SM_RuinPoleBark`);
  - kůra: `shape = "bark_strip"`, `cat = "bark"`;
  - ovázání: `shape = "lashing"`, `cat = "rope"`.
- **Paty východních sloupků** ber jako u krytů z nejvyššího kamene `Brana_V` pod sloupkem (`zr_stavby/kryty.py`, hledání paty). Západní sloupky stojí na `deck_z`.
- **Natočení:** UE má `roll` opačně než výpočty; používej stejné konvence jako `pult.py` (krytina, latě).
- Před přepsáním `constructions.json` vygeneruj do dočasného souboru a ověř, že se změnila jen nová stavba.

## 5. Kontroly (doplň do `check_brana` v `tools/checks/run_checks.py`)

- sklon 22° ± 2°;
- západní sloupky stojí na podlaze nad trámem (d trámu ± 0,1 m), východní na kameni koruny;
- žádný sloupek blíž než 0,5 m (podél d) od průzoru východního krytu;
- každá krokvička leží na obou vaznicích;
- spodek krokviček je nad špičkami kůlů východního krytu aspoň o 1 cm;
- světlá výška u východního krytu aspoň 1,85 m;
- stříška se neprotíná s kůly a ráhny krytů (východního ani severního);
- kůra pokrývá půdorys krytiny aspoň z 99 %;
- všechny dílce mají sadu `final`;
- náhled: doplň do `brana_scene` v `preview3d.py` pohled pod stříšku od západu a pohled od východu zpoza brány.

## 6. Co ještě na stanovišti zbývá (mimo stříšku)

- **Zátaras** (`Brana_Zataras`, španělský jezdec, jeden samostatný actor): návrh kap. 4.5.
- **Staveniště pro etapu 1** (sada `site`): žebřík, hromada kůlů, svitky kůry.
- **Výlez na podestu:** určí Jirka. Volná je západní strana a západní třetina jižní strany.
- **Otevřené u Jirky:** severní a jižní kryt jsou teď `final`; v etapě 1 je severní hrana podesty nad zdí bez krytu.

## 7. Pravidla

- Nové soubory jen do `skvt_projekt\PrototypeDesigns\Lapikus`; v `GameDesign\Claude outputs\Lapikus` jen přepisuj existující kopie.
- Nikdy nepřepisuj `manual_edits.json` ani `constructions_edits.json`; `constructions.json` jen generátorem.
- Sdílené soubory (`build_constructions.py`, `gen_constructions.py`, `config.py`) mění i jiné stavby: přidávej, neměň cizí data, po změně pusť celé `run_checks.py`.
- Po dokončení zapiš stav do `navrh_brana_straz.md` kap. 0, `03_ruin/Zricenina_03_ruin_stav.md`, `05_constructions/README_constructions.md` a `CHECKLIST_assets_navrhy.md`. V hlášení uveď, co je a není ověřené v UE a co má Jirka spustit.
