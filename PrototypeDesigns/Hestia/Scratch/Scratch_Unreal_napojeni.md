---
# orchestrace
type: scratch
validity: valid
intake: prepared
source: chat
captured_by: agent HearthLore
updated: 2026-11-21
# hra
category: []
entity: ""
---
# Scratch: napojení Hestia na Unreal

<!-- Tematický scratch (modul idea_capture): postřehy z chatu GameDesignera s agentem HearthLore, zapsané na jeho pokyn. Návrh podrole Unreal pro Hestia je v HearthLore: `hearthlore/podklady/knihovnik.md`, kap. 10. -->

### 2026-11-20 – Unreal MCP v Unrealu 5.8: kde ho zapnout (agent HearthLore)

**Neověřeno**, podle dokumentace Epicu (stránka je označená jako dokumentace 5.9, v 5.8 se mohou lišit názvy položek): https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor

- Projekt SKVT je na Unrealu 5.8 (`skvt_projekt.uproject`: `EngineAssociation: "5.8"`). Unreal MCP je v 5.8 oficiální experimentální plugin: MCP server uvnitř editoru, lokálně na `http://127.0.0.1:8000/mcp`. V `.uproject` uvedený není; zatím nebyl vědomě zapnutý.
- **Plugin:** *Edit → Plugins*, hledat „MCP“; podle dokumentace je Unreal MCP ve výchozím stavu zapnutý, k němu zapnout *All Toolsets*, restart editoru.
- **Automatický start serveru:** *Edit → Editor Preferences → Agentic Workflows → Model Context Protocol → Auto Start Server* (podle starší verze dokumentace *General → Model Context Protocol*); tam i port (8000) a cesta (`/mcp`).
- **Ruční start:** v konzoli `ModelContextProtocol.StartServer`.
- **Claude Code:** `.mcp.json` vygeneruje *Generate Client Config* nebo příkaz `ModelContextProtocol.GenerateClientConfig ClaudeCode`; Claude Code spouštět ze složky s tímto souborem.
- **Bezpečnost:** server přijímá jen lokální spojení, ale nemá autentizaci (může ho volat kterýkoli lokální proces). Adresu (`DefaultBindAddress`) neměnit. Nástroje běží jeden po druhém na game threadu: nespouštět dotazy během buildu.
- Po prvním ověření v praxi (zapnutí, spojení z Claude Code) přepsat jako know-how (`knowhow_kind: tool`, `scope: engine`, `engine_version: 5.8`).

### 2026-11-20 – Napojení entit Hestia na actory v levelu (agent HearthLore)

> **Zpracováno 2026-11-21 (P5, agent pilotu):** pravidla napojení jsou v `Maintenance/taxonomy_local/ue_map.yaml` (schválil GameDesigner); generovaný blok `## Stav v UE` přinese první čtení (P6). Část 1 (zapnutí Unreal MCP) zůstává do etapy 2.

**Zjištěno z kódu Lapikus** (`zrlib/config.py`, `zrlib/ue_actors.py`, `05_constructions/build_constructions.py`, `06_furnishing/build_furnishing.py`):
- mapa `LapikusPrototypeMap`;
- složky v Outlineru kopírují strom: `Stavby/Palac/Obydli`, `Stavby/Brana`, `Stavby/Vez`, `Stavby/Ostroh`, `Vybaveni/Palac/Kovarna`, `Ruin/Vez`, `Ruin/Rampa`, `Forest/Alders`;
- tagy: `Zricenina_Ruin`, `Zricenina_Stavby`, `Zricenina_Vybaveni`, `Zricenina_Alder`; `stavba:<jméno>` (build vybírá podle začátku jména, `Palac_Obydli` najde i `Palac_Obydli_Krov`), `vybaveni:<skupina>`, `stage:<sada>` ([[Konvence_etapy_sady_actoru]]), `id:<kód>`.

**Návrh (z porovnání variant, rozhodne se v HearthLore):**
- pravidla napojení v instanci (`Maintenance/taxonomy_local/ue_map.yaml`): výchozí konvence (např. stavba = tag `stavba:{entita}*`, vybavení = `vybaveni:{entita}*`, les = `Zricenina_Alder` + složka `Forest/`) a jmenovité výjimky;
- v hubech nic ručně: sekce `## Stav v UE` dostane generovaný blok (kde entita v Unrealu je, poslední čtecí report, počty podle `stage:*`);
- lint pohlídá shodu (entita s `build_step` bez actorů, pravidlo bez entity).
- Proč ne pole v hubu (`ue_folders`, `ue_tags`): opakovaný údaj ve 22 hubech, změna konvence = 22 úprav, technický detail ve frontmatteru. Proč ano: vše o entitě v jedné poznámce; to řeší generovaný blok.

## Otevřené otázky
- [x] Smí agent číst stav v Unrealu sám (audit, dotaz na realizaci), nebo jen na pokyn GameDesignera? — agent HearthLore, 2026-11-20 → rozhodnuto GameDesignerem 2026-11-20: ano, sám, ale jen čtecími dotazy Hestia (nikdy zápis, obecný Python ani build); zejména Auditor, Builder a Architect, dále Knihovník. Zapracováno do zadání HearthLore 0.14 (12 kap. 3b.8, Q32); do instance přijde s core (předání souběhu, položky 17–18)

## Předzpracování (doplní Curator)
- Kategorie: – (nástroje a napojení na engine; žádná kategorie obsahu)
- Souvisí s: [[Konvence_etapy_sady_actoru]], [[05_constructions]], [[06_furnishing]], [[03_ruin]], sekce `## Stav v UE` v hubech entit
- Návrh zařazení: první část po ověření do `KnowHow/` (tool, engine 5.8; nová hodnota `tech` pro Unreal MCP navrhnout Curatorovi); druhá část je návrh nástroje Hestia, zpracuje se v HearthLore (podklad Knihovník, kap. 10) a do instance přijde s novou verzí core
