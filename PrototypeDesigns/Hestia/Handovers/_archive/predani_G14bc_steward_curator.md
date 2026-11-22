---
# orchestrace
type: handover
validity: archived
superseded_by:
for_role: [Steward, Curator]
updated: 2026-11-23
# hra
domain: structures
entity: ""
build_step:
---
# Navazující úkoly po rozdělení dokumentů (G14b, G14c): pro Stewarda a Curatora

<!-- Sepsal Knihovník 2026-11-23 na pokyn GameDesignera. Knihovník do Handovers/ ani do úkolů v queue.md nezapisuje (write_rules, oddíl Knihovník); GameDesigner soubor přenese ručně. Navazuje na [[predani_knihovnik_rozdeleni]]. -->

## Pro koho a co
- **Steward (orchestrační agent):** založit frontu předání pro dům posádky, zkrátit a archivovat [[predani_palac_obydli_stavitel]], předat Builderovi rozdělení kroků.
- **Curator:** rozdělit [[Kod_spousteni_kontroly_z_roli]], uzavřít vyřešené úkoly ve frontě.

## Co Knihovník už udělal (2026-11-22/23, schválil GameDesigner)
- [[navrh_palac_kovarna]] kap. 0 → [[stav_palac_kovarna]].
- [[navrh_vez_pristresek]]: kap. 3 → nový [[navrh_vez_skody]] (entita `Vez`), stav a ověření → nový [[stav_vez_pristresek]].
- [[Zricenina_03_ruin_stav]]: kapitoly kovárna, dům, brána a škody/přístřešek věže nahrazeny odkazy na stavy.
- [[navrh_palac_obydli_stred]]: postavené (0.5, 0.6, 9.2a) → [[stav_palac_obydli]]; 0.5a a 0.5b zapracované do kap. 4.5 a 4.6; kap. 3 odpadla; kap. 9 → nový [[navrh_palac_obydli_stavenisko]]; *Připravenost* nahrazena odkazem na [[CHECKLIST_assets_navrhy]].
- Z [[predani_palac_obydli_stavitel]] zkopírováno do [[stav_palac_obydli]]: kap. 3 *Kde co je* (→ *Souhrn specifikace*) a hotové položky kap. 4 (→ *Ověřeno v UE*). Text předání se neměnil.

## Úkoly pro Stewarda

### S1. Fronta předání pro dům posádky (G14c)
[[predani_palac_obydli_stavitel]] má 10 891 znaků (limit 4 000). Navržená fronta, jedno předání = jeden task, v tomto pořadí:

| # | for_role | Task | Zdroj v dnešním předání |
|---|---|---|---|
| 1 | Builder | vizuální kontrola staveniště a etapy 1 v UE, rozmístění hranic a capture | kap. 4 (☐), kap. 7 |
| 2 | Builder | krytina a lemování `Palac_Obydli_Krov` | kap. 5.1 |
| 3 | Builder | strop světnice se zavěšením dymníku `Palac_Obydli_Strop` | kap. 5.2 |
| 4 | Builder | podlaha světnice `Palac_Obydli_Podlaha` | kap. 5.3 |
| 5 | Builder | okap `Palac_Obydli_Okap` (až po 2, výška z krytiny) | kap. 5.4 |
| 6 | Builder | zárubně otvorů srubu (sada `final`) | kap. 5.5 |
| 7 | Furnisher | vybavení domu `Palac_Obydli_Vybaveni` (`06_furnishing`) | kap. 5.5 |

Každé předání: zadání a odkazy na [[navrh_palac_obydli_stred]] (kap. 4), [[navrh_palac_obydli_stavenisko]], [[stav_palac_obydli]] a [[05_constructions]]. Kap. 1 a 2 dnešního předání už jsou přesunuté; kap. 3 je v [[stav_palac_obydli]]; kap. 6 a pasti z kap. 5 viz B3; kap. 8 vypustit (pokrývá ji `handover_out`). Po založení fronty předání archivovat.

### S2. Pro Buildera: rozdělení kroků (G14b, mimo oblast Knihovníka)
- **B1 [[05_constructions]]** (audit 48 717 zn., soubor dnes 56 075): sekci *Vstupy a výstupy → 4. Co je v `constructions.json`* (~37 600 zn.) rozdělit po skupinách staveb: Ostroh (`Ostroh_Krov`, `_Dostavba`, `_Podlaha`), Kovárna (`Palac_Kovarna_Pristresek`, `_Vyhen`, `_Stena`, `_Kul`, `_Okap`), Dům (`Palac_Obydli_*`), Věž (`Vez_Patra`, `Vez_Pristresek`). V hlavním dokumentu zůstane účel, spouštění, skripty a soubory. Souvisí s úkolem T-0005.
- **B2 [[03_ruin]]** (audit 39 913 zn., soubor dnes 44 197): sekci *Spouštění* (~28 200 zn.) rozdělit na jednorázovou přípravu (kap. 1) a úpravy (kap. 4 *Úpravy v datech*, kap. 5 *Bourací objemy*) do samostatného dokumentu.
- **B3 KnowHow** (zapíše Builder, `knowhow_write`) z [[predani_palac_obydli_stavitel]]:
  - `pult._pult_cover` čte `plan["a"]` jako osu spádu; u domu je spád po ose `v` (kap. 5.1);
  - výměny v `ohniste.py` předpokládají spád po ose `u`, pro dům nic nepostaví (kap. 5.1);
  - typ `gutter` počítá spád k `+c`; spád k západu ověřit (kap. 5.4);
  - zásady z kap. 6 (sdílené soubory s kovárnou, nepřepisovat `manual_edits.json` / `constructions_edits.json`, porovnat polohy sloupů, krokví a komína před stavbou dřeva).

## Úkoly pro Curatora

### C1. [[Kod_spousteni_kontroly_z_roli]] (33 153 zn.)
Rozdělit podle zdrojové role: *Z AGENT_Architekt_hrad*, *Z AGENT_Stavitel_hrad*, *Z AGENT_Furnisher_hrad*, *Z KNOWHOW_hrad*. Cíl (`Roles/modules/`, `Steps/`, `Steps/shared/`) podle *Předzpracování*; pokrývá úkol T-0012.

### C2. Fronta `queue.md`
Vyřešeno rozdělením, uzavřít (`state: done`, `closed: 2026-11-23`):
- **T-0006** [[Zricenina_03_ruin_stav]] rozpad do stavů entit;
- **T-0007** [[navrh_palac_kovarna]] kap. 0 duplicitní se stavem;
- **T-0008** [[navrh_palac_obydli_stred]] kap. 0.5–0.6 překryv se stavem.

## Otevřené otázky (pro GameDesignera a Architecta)
- [ ] [[navrh_palac_obydli_stred]] má po rozdělení 31 152 znaků, pořád nad `doc_split_chars` (20 000). Zbývá kap. 0 (plán po etapách, ~9 000) a kap. 4, jejíž čísla krovu a srubu se liší od postaveného stavu (rozdíly v [[stav_palac_obydli]], *Co je hotové*). Doporučení Knihovníka: Architect sjednotí kap. 4 s kap. 0.6 a 0.7, vrstva „platí přednostně“ zmizí.
- [ ] Entity [[Brana]], [[Nadvori]], [[Strazni_Vez]]: `status: built` bez platného dokumentu `state` (audit G4).
- [ ] [[navrh_palac_obydli]]: `status: rejected` a zároveň `validity: valid`.

## Zbývá
- Zpracováno 2026-11-23 (Steward): S1 → [[predani_palac_obydli_1_etapa1_ue]] až [[predani_palac_obydli_7_vybaveni]], archivováno [[predani_palac_obydli_stavitel]]; S2 → [[predani_builder_rozdeleni_05]], [[predani_builder_rozdeleni_03]], [[predani_builder_knowhow_dum]]; C1 → [[predani_curator_scratch_kod]]; C2 → [[predani_curator_fronta_t0006]]. Otevřené otázky zůstávají GameDesignerovi a Architectovi.
