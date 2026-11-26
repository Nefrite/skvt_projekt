---
# orchestrace
type: reference
validity: valid
updated: 2026-11-19
aliases: []
---
# Lapikus – rozcestník

Hlavní rozcestník vaultu Hestia. Pohledy jsou v `Dashboard/views/`: do rozhodnutí Q1 varianta Bases (`bases/`, core plugin), Dataview (`dataview/`, funguje po instalaci pluginu Dataview) a u matice a mapy skript (`generated/`, přepisuje `hubs`). Vlastní pohledy instance patří do `local/`.

## Prototyp

- Kořenová entita: [[Lapikus_Region]]
- Master lore: [[Lore_Lapikus]]
- Pojmy: [[Glossary]]

## Přehled
<!-- hestia:generated:start -->

**Kořenové entity** (zralost po doménách, v závorce nejslabší článek; 04 kap. 3)

| Entita | environment | structures | paths | npc | gameplay | narrative |
|---|---|---|---|---|---|---|
| [[Characters]] | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle |
| [[Cinematics_Lapikus]] | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle | bez cíle |
| [[Lapikus_Region]] | 33 % (1) | 83 % (3) | 0 % (0) | bez cíle | 0 % (0) | 0 % (0) |

**Aktivní předání**

- [[predani_brana_straz_striska_stavitel]] – [[Brana_Straz]]
- [[predani_curator_fronta_t0006]]
- [[predani_curator_scratch_kod]]
- [[predani_guesthouse_kamna_stavitel]] – [[Guesthouse]]
- [[predani_knihovnik_rozdeleni]]
- [[predani_knihovnik_souhrny]]
- [[predani_lapikus_koren_actoru_stavitel]] – [[Lapikus]]
- [[predani_palac_obydli_1_etapa1_ue]] – [[Palac_Obydli]]
- [[predani_palac_obydli_2_krytina]] – [[Palac_Obydli]]
- [[predani_palac_obydli_3_strop]] – [[Palac_Obydli]]
- [[predani_palac_obydli_4_podlaha]] – [[Palac_Obydli]]
- [[predani_palac_obydli_5_okap]] – [[Palac_Obydli]]
- [[predani_palac_obydli_6_zarubne]] – [[Palac_Obydli]]
- [[predani_palac_obydli_7_vybaveni]] – [[Palac_Obydli]]

**Otevřené otázky:** do 14 dní 20 · starší 0 · bez data 0

**Poslední změny** (`changes.md`)

- 2026-11-25 · ScreenWriter · Cinematics_Lapikus · promo_prulet.json, build_sequence.py (Sequencer skript), stav_promo_prulet; v UE neovereno · chat:promo_prulet_realizace
- 2026-11-25 · ScreenWriter · Lapikus · oprava build_sequence.py po prvnim behu v UE (get_channels) · chat:promo_prulet_oprava_api
- 2026-11-25 · ScreenWriter · Cinematics_Lapikus · build_sequence.py: channels() misto get_channels (UE 5.8), traceback; stav_promo_prulet: vysledek prvniho behu · chat:promo_prulet_oprava_api
- 2026-11-26 · ScreenWriter · Lapikus · oprava build_sequence.py po druhem behu v UE (SequenceTimeUnit) · chat:promo_prulet_oprava_api2
- 2026-11-26 · ScreenWriter · Cinematics_Lapikus · build_sequence.py: addkey() misto SequenceTimeUnit (UE 5.8); stav_promo_prulet: vysledek druheho behu · chat:promo_prulet_oprava_api2
- 2026-11-26 · ScreenWriter · Lapikus · oprava build_sequence.py po tretim behu v UE (binding id) · chat:promo_prulet_oprava_api3
- 2026-11-26 · ScreenWriter · Cinematics_Lapikus · build_sequence.py: binding_id() pro Camera Cut (UE 5.8); stav_promo_prulet: vysledek tretiho behu · chat:promo_prulet_oprava_api3
- 2026-11-26 · ScreenWriter · Lapikus · know-how pasti sequencer a postup spusteni a renderu · chat:promo_prulet_knowhow_postup
- 2026-11-26 · ScreenWriter · Cinematics_Lapikus · KnowHow/Pasti_sequencer_python, Steps/cinematics (Spousteni, Vstupy a vystupy), stav_promo_prulet: postup a vysledek 4. behu · chat:promo_prulet_knowhow_postup
- 2026-11-26 · Steward · Cinematics_Lapikus · navrh_promo_prulet_kamery valid (GameDesigner 2026-11-26, dodatečně), category cutscene, entity Cinematics_Lapikus u návrhu i stavu; otázka kdo postaví uzavřena (ScreenWriter) · chat:P24_schvaleni_promo

<!-- hestia:generated:end -->

## Zóny

| Složka | Obsah |
|---|---|
| `Inbox/` | rychlé zápisy a import (`scratch`, `intake: raw`) |
| `Scratch/` | předzpracované a ručně psané nápady |
| `Entities/` | huby entit |
| `Docs/<domain>/`, `Docs/crosscut/` | celková dokumentace podle domén a přesahy |
| `Steps/`, `Steps/shared/` | dokumentace kroků prototypování a sdíleného kódu |
| `Handovers/` | aktivní předání; splněná v `Handovers/_archive/` |
| `KnowHow/` | ověřené know-how |
| `Roles/` | profily projektových rolí |
| `Maintenance/` | údržba: konfigurace, fronta, logy, reporty |
| `_core/` | modul Hestia (needitovat) |
