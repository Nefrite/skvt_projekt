---
# orchestrace
type: knowhow
knowhow_kind: pitfall
tech: [python, ue_python]
scope: instance
verified: 2026-11-17
validity: valid
updated: 2026-11-19
aliases: []
---
# Pasti: kód a souběžná práce

<!-- Z KNOWHOW_hrad.md kap. 5.6 (pilot Lapikus, B6). -->

- **Kód:** komentáře a identifikátory bez diakritiky (UE Python konzole), dokumentace (`*.md`) česky s diakritikou.
- **Ukládací spouštěč = přípona `_Capture`** (16. 11. 2026, rozhodl Jirka): capture skupiny má vlastní skript `<Skupina>_Capture.py` vedle `<Skupina>.py` (vybavení: `06_furnishing/vybaveni/Palac_Kovarna_Capture.py`), aby se nemuselo přepínat `MODE`.
- **Souhrnný spouštěč skupiny staveb** (např. `Palac_Kovarna.py`) jen vyjmenuje stavby a zavolá `pipeline.constructions(seznam)`, ne spouštěče jednotlivých staveb: jeden běh, jedno načtení knihovny, nic se neduplikuje. Pořadí v seznamu je pořadí závislostí (výšky z krokví a krytiny), suť naposled.
- **Víc relací nad stejnou složkou (15.–16. 11. 2026):** souběžně pracovala jiná relace (dům v paláci) a měnila sdílené soubory (`build_constructions.py`, `gen_constructions.py`, `palac_spec.py`, `run_checks.py`, `preview3d.py`). Pracuj v kopii, před uložením porovnej md5 souborů na disku s výchozí kopií; když se liší, vezmi aktuální verzi a své změny do ní znovu vlož (úpravy jako nahrazení textu, ne přepsání celého souboru), přegeneruj data a spusť kontroly všech dotčených staveb. `constructions.json` se vždy generuje znovu, neslučuje se.
