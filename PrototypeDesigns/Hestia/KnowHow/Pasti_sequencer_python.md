---
# orchestrace
type: knowhow
knowhow_kind: pitfall
tech: [ue_python, sequencer, movie_render_queue]
scope: engine
engine_version: "5.8"
verified: 2026-11-26
validity: valid
updated: 2026-11-26
aliases: []
# hra (volitelně)
domain: narrative
entity: "[[Cinematics_Lapikus]]"
---
# Pasti: Sequencer v Pythonu (UE 5.8)

<!-- Z první realizace promo průletu (ScreenWriter, 2026-11-25/26): skript build_sequence.py padal postupně na čtyřech rozdílech API oproti příkladům pro starší verze UE. Každá odrážka: co dělat, proč, ověřeno. -->

- **Kanály sekce:** `section.get_channels()` v 5.8 není (`AttributeError`); použij `section.get_all_channels()` (v projektu pomocná funkce `channels()` zkouší obě jména a pak `MovieSceneSectionExtensions.get_all_channels`). Transformační sekce má 9 kanálů v pořadí lokace X, Y, Z, rotace roll, pitch, yaw, měřítko X, Y, Z. Ověřeno 2026-11-26, běh v editoru (Jirka).
- **Jednotka času u `add_key`:** `unreal.SequenceTimeUnit` v 5.8 není; enum se jmenuje `MovieSceneTimeUnit`, podle dokumentace s výchozí hodnotou `DISPLAY_RATE`. Nejjistější je `channel.add_key(FrameNumber(f), hodnota)` bez dalších argumentů a interpolaci nastavit na vrácený klíč (`key.set_interpolation_mode(unreal.RichCurveInterpMode.RCIM_LINEAR)`, v `try`). Že `add_key` bez argumentů prošlo, je ověřeno 2026-11-26; že se lineární interpolace skutečně nastavila, ne (chyba je v `try` potlačená, ověř v křivkách Sequenceru).
- **Binding pro Camera Cut:** `unreal.MovieSceneSequenceExtensions.make_binding_id(...)` ani `binding.get_binding_id()` v 5.8 nejsou. Volá se `seq.make_binding_id(binding, unreal.MovieSceneObjectBindingSpace.LOCAL)`, záloha je `MovieSceneObjectBindingID` s `guid` z `binding.binding_id`. V projektu `binding_id()` zkouší všechny tři cesty; kterou z nich 5.8 vzalo, není zjištěno. Ověřeno 2026-11-26 (všech 7 Camera Cuts bez chyby).
- **Skript v editoru selhává po částech:** zachytávej chybu po záběru (`try`) a loguj celý `traceback.format_exc()`; jinak se v logu objeví jen jednořádková zpráva a oprava trvá o kolo déle. V projektu `build_sequence.py`, smyčka přes záběry.
- **Log spawnu actoru:** řádek `Attempting to add actor ... to level at X,Y,Z` ukazuje u prvních běhů polohu viewportu, ne zadanou polohu; po spawnu nastav polohu a rotaci výslovně (`set_actor_location_and_rotation`). Připojené actory (kamera na rigu) se logují na 0, 0, 0 a pak se přepíší relativní transformací; to je v pořádku.
- **Opakovaný běh:** skript, který staví sekvenci a actory, musí předchozí běh smazat podle tagu actorů a assetu (`REBUILD`), jinak v levelu zůstanou osiřelé kamery, rigy a cíle ostření z neúspěšných běhů. Po každém neúspěšném běhu zůstávají v levelu actory s tagem, smaže je až další běh.

## Ověřeno (kdy, kde, kým)
2026-11-26, UE 5.8, level `LapikusPrototypeMap`, `build_sequence.py` (ScreenWriter), logy spouštěl Jirka. Doběhly všechny záběry; vzhled sekvence a pohyb rigů (kolejnice, jeřáb) zatím vizuálně neověřeny.
