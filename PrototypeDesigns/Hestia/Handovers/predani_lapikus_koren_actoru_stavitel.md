---
# orchestrace
type: handover
validity: valid
superseded_by:
for_role: [Builder]
updated: 2026-11-23
# hra
domain: structures
entity: "[[Lapikus]]"
build_step: 05_constructions
---
# Lapikus – kořen sloučených actorů staveb (03 a 05): předání staviteli

## Pro koho a co
Pro roli **Builder**: podle schválené **Varianty C** v [[navrh_lapikus_koren_actoru]] upravit sestavení sloučených ISM actorů v `Lapikus/zrlib/ue_actors.py`, `Lapikus/03_ruin/blocks/build_ruin_blocks.py` a `Lapikus/05_constructions/build_constructions.py` tak, aby kořen (`pivot`) každého ISM actoru stál ve společném 3D středu `(cx, cy, cz)` stavby/úseku zdi (s vlastním středem u dílů vzdálených `> 300 cm`) a byl natočený podél její hlavní osy.

## Zadání
1. Podle schválené **Varianty C** v [[navrh_lapikus_koren_actoru]] (kap. *Návrh* a *Souhrn specifikace*) doplnit výpočet obálky a kořene `stones_pivot(stones, yaw=0.0, ...)` do `Lapikus/zrlib/ue_actors.py` a napojit ho do `place_ism()` (s fallbackem na vlastní střed při 3D odchylce `> 300 cm`), `build_ruin_blocks.py` ([[03_ruin]]) a `build_constructions.py` ([[05_constructions]]).
2. Chování hranic materiálu s `"pile": true` (`_pile()` a `capture_edits()`) i samostatných actorů (`spawn_loose` v 03, 05 a [[06_furnishing]]) ponechat beze změny.
3. Specifikace `tools/ruin/*_spec.py` ani generovaná data (`ruin_layout.json`, `constructions.json`, `furnishing.json`) neměnit.
4. Aktualizovat hlavičky změněných skriptů a dokumentaci kroků [[03_ruin_generator]] a [[05_constructions]].

## Platná rozhodnutí
- Schválená konvence (**Varianta C** – rozhodnutí GameDesignera 2026-11-23) a specifikace změn v kódu: [[navrh_lapikus_koren_actoru]].
- Oddělení kroků 03, 05, 06 a pravidla speců: [[Konvence_03_05_06_a_spec]], [[Konvence_souradnice_a_ramce]].

## Výchozí stav
- Stav zříceniny a dostaveb: [[Zricenina_03_ruin_stav]].
- Rozbor současného chování `_ism_actor` / `place_ism` a tabulka `pivot_far` ze všech 9 dotčených entit v `Maintenance/reports/ue_*.json`: [[navrh_lapikus_koren_actoru]] § *Výchozí stav*.

## Kritéria hotovo
- `python Lapikus/tools/checks/run_checks.py` projde bez chyby.
- `python Lapikus/tools/checks/fingerprint.py` potvrdí shodné hashe geometrie `03_lvl`, `03_rubble` a `05` před a po změně.
- Po přestavění levelu (`Lapikus/build_normal.py`) v Unreal Editoru projde `Lapikus/tools/checks/UE_Kontrola_Transformaci.py` a nové čtení `hestia.py ue_query` vykáže v `Maintenance/reports/ue_*.json` u všech 9 dotčených entit `pivot_far: 0` (viz [[navrh_lapikus_koren_actoru]] § *Ověření*).

## Otevřené otázky
- [x] Potvrzení varianty umístění kořene (Varianta C / Varianta A / Varianta B2) GameDesignerem v [[navrh_lapikus_koren_actoru]] § *Otevřené otázky* — Architect, 2026-11-23 → **Rozhodnuto (GameDesigner, 2026-11-23):** Schválena **Varianta C**.

## Zbývá
- Implementovat **Variantu C** v `zrlib/ue_actors.py`, `build_ruin_blocks.py` a `build_constructions.py`, přestavět level v UE a ověřit přes `run_checks.py`, `fingerprint.py` a `ue_query`.
