"""Toolset Hestia pro Unreal MCP (etapa 2, zadání 13 kap. 10.11, 12 kap. 3b.8) – NEOVĚŘENÁ KOSTRA.

Šablona z core (`_core/templates/unreal/init_unreal.py`). Instance ji zkopíruje do projektu Unrealu
(`Content/Python/init_unreal.py`, editor ho spustí při startu) a doplní cestu k `_core/scripts/`.

Stav: kostra je neověřená. API vlastních toolsetů pluginu Unreal MCP je v UE 5.8 experimentální; registraci
(`register_toolset`) je potřeba doplnit podle dokumentace pluginu ve verzi enginu instance a ověřit po zapnutí
Unreal MCP. Ověření v praxi zapíše instance jako know-how (`knowhow_kind: tool`, `scope: engine`).

Pravidla (12 kap. 3b.8, 13 kap. 10.11):
- toolset nabízí **jen čtecí funkce** z `hestia_ue.py`; žádný nástroj nezapisuje do levelu ani assetů,
  nespouští obecný Python ani build;
- klient agenta má povolené jen nástroje toolsetu Hestia (allowlist); obecné nástroje Unreal MCP
  a meta-nástroje se nepovolují; server zůstává lokální;
- výsledek agent uloží `hestia.py ue_query --import` (report na entitu).
"""
from __future__ import annotations

import json
import sys

HESTIA_CORE_SCRIPTS = r"<cesta k Hestia/_core/scripts>"      # doplní instance
TOOLSET = "Hestia"

if HESTIA_CORE_SCRIPTS not in sys.path:
    sys.path.insert(0, HESTIA_CORE_SCRIPTS)


def read_entities(request_json: str) -> str:
    """Nástroj: přečte actory entit podle požadavku z `ue_query --emit` (JSON) a vrátí výsledek JSON."""
    import hestia_ue
    return json.dumps(hestia_ue.collect(json.loads(request_json)), ensure_ascii=False)


TOOLS = {
    "hestia_read_entities": (read_entities, "Jen čtení: actory, fáze, rozsah a signály realizace entit Hestia"),
}


def register_toolset() -> None:
    """Registrace nástrojů v Unreal MCP. Neověřeno: doplnit podle API pluginu v dané verzi enginu."""
    try:
        import unreal
    except ImportError:
        return
    registry = getattr(unreal, "MCPToolsetRegistry", None)     # předpokládané jméno, ověřit v dokumentaci
    if registry is None:
        unreal.log_warning(f"{TOOLSET}: registrace toolsetu Unreal MCP není dostupná (neověřená kostra)")
        return
    for name, (func, description) in TOOLS.items():           # pragma: no cover – až po ověření v instanci
        registry.register_tool(TOOLSET, name, func, description)


register_toolset()
