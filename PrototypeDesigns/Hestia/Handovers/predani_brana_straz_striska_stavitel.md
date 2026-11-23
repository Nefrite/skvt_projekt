---
# orchestrace
type: handover
validity: valid
updated: 2026-11-23
# hra
domain: structures
entity: "[[Brana_Straz]]"
build_step: 05_constructions
---
# Strážní stanoviště nad branami – stříška z kůry (etapa 2): návrh a instrukce pro stavitele

Stav: 16. 11. 2026. Připravil architekt (session s Jirkou). **Návrh, nepostaveno.** Nahrazuje kap. 4.4 v [[navrh_brana_straz]]: ta počítala s podestou a kryty, které dnes vypadají jinak.

Čti spolu s: `AGENT_Stavitel_hrad.md`, `KNOWHOW_hrad.md`, [[navrh_brana_straz]] kap. 0 (skutečný stav stanoviště), `tools/ruin/brana_spec.py`.

## 1. Zadání

- **Účel:** suché místo pro stráž u východního krytu, odkud se dívá průzory před bránu.
- **Etapa:** celá stříška je sada `final` (v etapě 1 ještě nestojí).
- **Styl:** provizorium z toho, co je po ruce. Tyče a kulatina s kůrou, vázané spoje, krytina z pásů smrkové kůry (zbyla z loupání kulatiny na dům).
- **Zříceninu neměň.** Všechno je dostavba 05.

## 2. Výchozí stav (změřeno z dat 16. 11. 2026)

Přesunuto do [[stav_brana_straz]] (Co je hotové).

## 3. Návrh

Přesunuto do [[navrh_brana_straz]] kap. 11.

## 4. Jak to postavit

- **Nový typ `bark_roof`** v `05_constructions/zr_stavby/` (použije ho i stříška stanu na nádvoří, piš ho obecně). Zápis do `TYPES`, `REQUIRED` a `CNAME` v `build_constructions.py`.
- **Rozměry do `tools/ruin/brana_spec.py`** (konstanty `B_ROOF_*`, výstup ve `straz()`), data přes `gen_constructions.py` → `brana()`. Výšky absolutně: `deck_z` + výška nad podlahou.
- **Stavba:** `Brana_Straz_Pristresek`, složka `Stavby/Brana`, `stage = "final"`. Spouštěč `stavby/Brana_Straz_Pristresek.py` a zápis do seznamu `STAVBY` v `stavby/Brana_Straz.py`.
- **Dílce:**
  - sloupky Ø 14: `shape = "round"`, `bark = True` (vyjde `SM_RuinLogBark`), svisle (`pitch = 90`);
  - tyče do Ø 11: `shape = "round"`, `bark = True` (vyjde `SM_RuinPoleBark`);
  - kůra: `shape = "bark_strip"`, `cat = "bark"`;
  - ovázání: `shape = "lashing"`, `cat = "rope"`.
- **Paty a polohy sloupků (upravené Jirkou v levelu 23. 11. 2026, [[navrh_brana_straz]] kap. 11–12, `B_FURN_POSTS` v `brana_spec.py`):**
  - podesta `Brana_Straz_Podesta` má již **5 kulatin** (`d = −0,20 m` na `Brana_S` + 4 v kapsách `Brana_V` v `d = 0,80 / 2,20 / 3,60 / 5,00 m`, `B_LEVEL` na `Brana_J` `d = 0,65–5,30 m`; hotovo v T-0041);
  - **západní sloupky** stojí na podlaze (`deck_z`) přímo nad 2. a 4. kulatinou: SZ v `u = 3,40; d = 0,78–0,80 m` (v levelu `a = 3,400; c = 0,777 m`) a JZ v `u = 3,465; d = 3,57–3,60 m` (v levelu `a = 3,465; c = 3,574 m`), výška `3,20 m` (západní vaznici, délku krokviček a půdorys krytiny s přesahem `u = 3,15–8,00 m, d = 0,25–3,80 m` navázat na posunuté západní sloupky);
  - **východní sloupky** stojí na koruně `Brana_V` (paty ber jako u krytů z nejvyššího kamene `Brana_V` pod sloupkem, `zr_stavby/kryty.py`, hledání paty): SV v `u = 7,15; d = 0,81 m` (`a = 7,148; c = 0,807 m`, výška `1,744 m`) a JV v `u = 7,15; d = 3,70 m` (výška `1,816 m`), tedy výška `1,74–1,82 m`.
- **Odebrání dočasných graybox zástupců sloupků:** po postavení `Brana_Straz_Pristresek` odeber 4 zástupce `Sloupek_SZ_Zastupce`, `Sloupek_JZ_Zastupce`, `Sloupek_SV_Zastupce`, `Sloupek_JV_Zastupce` (`B_FURN_POSTS` v `tools/ruin/brana_spec.py`) ze skupiny `Brana_Straz_Vybaveni` a přegeneruj `tools/furnishing/gen_furnishing.py` → `06_furnishing/furnishing.json`.
- **Natočení:** UE má `roll` opačně než výpočty; používej stejné konvence jako `pult.py` (krytina, latě).
- Před přepsáním `constructions.json` vygeneruj do dočasného souboru a ověř, že se změnila jen nová stavba.

## 5. Kontroly (doplň do `check_brana` v `tools/checks/run_checks.py`)

Přesunuto do [[navrh_brana_straz]] kap. 11.

## 6. Co ještě na stanovišti zbývá (mimo stříšku)

Přesunuto do [[stav_brana_straz]] (Co zbývá).

## 7. Pravidla

- Nové soubory jen do `skvt_projekt\PrototypeDesigns\Lapikus`; v `GameDesign\Claude outputs\Lapikus` jen přepisuj existující kopie.
- Nikdy nepřepisuj `manual_edits.json` ani `constructions_edits.json`; `constructions.json` jen generátorem.
- Sdílené soubory (`build_constructions.py`, `gen_constructions.py`, `config.py`) mění i jiné stavby: přidávej, neměň cizí data, po změně pusť celé `run_checks.py`.
- Po dokončení zapiš stav do [[stav_brana_straz]], [[Zricenina_03_ruin_stav]], [[05_constructions]] a [[CHECKLIST_assets_navrhy]]. V hlášení uveď, co je a není ověřené v UE a co má Jirka spustit.

## Zbývá

- [x] zvýšit počet trámů podesty `Brana_Straz_Podesta` ze 4 na **5 kulatin** (`d = −0,20` na `Brana_S` + 4 v kapsách `Brana_V` v `d = 0,80 / 2,20 / 3,60 / 5,00 m`; na `Brana_J` prodloužit `B_LEVEL` na `d = 0,65–5,30 m`; přegenerovat `03_ruin` a `05_constructions`), aby posunuté západní sloupky stříšky stály přímo nad 2. a 4. kulatinou (Jirka 23. 11. 2026, T-0041; hotovo 23. 11. 2026)
- [ ] přístřešek z kůry `Brana_Straz_Pristresek` se západními sloupky podle poloh z levelu (`u = 3,40; d = 0,78–0,80 m` a `u = 3,465; d = 3,57–3,60 m`, výška 3,20 m) a východními sloupky (`u = 7,15; d = 0,81 a 3,70 m`, výška 1,74–1,82 m); po postavení odebrat 4 dočasné zástupce `Sloupek_*_Zastupce` z `Brana_Straz_Vybaveni` (palisáda, podesta a kryty jsou hotové: [[stav_brana_straz]])
