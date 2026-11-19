"""Pohledy (zadání 13 kap. 10.9, 04 kap. 2 a 5): manifest pohledů a varianta skript.

- Manifest `taxonomy/views.yaml`: pohledy core, jejich soubory ve `vault_template/Dashboard/views/`
  a příznak `game_layer` (pohled čte `Entities/`). Podle něj `init` a `update_core --with-views`.
- Varianta skript (`Dashboard/views/generated/<pohled>.md`): generovaný blok v sekci `## Pohled`,
  který přepisuje `hubs`. Počítá z taxonomie instance (včetně lokálních `kinds` a domén) a dědí
  `located_in` od `parent` do libovolné hloubky.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .taxonomy import load_yaml

MANIFEST = "taxonomy/views.yaml"
VIEWS_REL = "Dashboard/views"
GENERATED_HEADING = "Pohled"
NO_PLACE = ""                      # entita bez umístění: prázdné pole Místo, řadí se na začátek


@dataclass
class ViewDef:
    id: str
    game_layer: bool
    files: list[str]          # cesty pod vault_template/Dashboard/views/ (se šablonovou příponou)

    @staticmethod
    def target(rel: str) -> str:
        """Cesta ve vaultu pod Dashboard/views/ (`*.md.tpl` -> `*.md`)."""
        return rel[:-len(".tpl")] if rel.endswith(".md.tpl") else rel


def load_manifest(core_root: Path) -> list[ViewDef]:
    p = Path(core_root) / MANIFEST
    if not p.is_file():
        return []
    items = (load_yaml(p) or {}).get("items") or []
    return [ViewDef(str(it["id"]), bool(it.get("game_layer")), [str(f) for f in it.get("files") or []])
            for it in items]


def template_files(core_root: Path, game_layer: bool) -> list[str]:
    """Soubory pohledů pro instanci (cesty pod vault_template/Dashboard/views/)."""
    return [f for v in load_manifest(core_root) if game_layer or not v.game_layer for f in v.files]


def skipped_views(core_root: Path, game_layer: bool) -> list[str]:
    return [] if game_layer else [v.id for v in load_manifest(core_root) if v.game_layer]


# ------------------------------------------------------------------ varianta skript

def _link(name: str) -> str:
    return f"[[{name}]]"


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return out + ["| " + " | ".join(r) + " |" for r in rows]


def matrix_cell(model, n, domain: str) -> str:
    """Buňka podle režimu cíle (zadání 0.13; 04 kap. 2.1): build `realizace/cíl`, u vyšší hloubky návrhu
    „(návrh N)“ (G13); design „návrh N/cíl“; ⚠ = mezera; „bez cíle“ = očekávaná doména podle kind bez cíle;
    jinak prázdné."""
    target = model.num(n.fm, f"target_{domain}")
    if not target:
        return "bez cíle" if domain in model.expected_domains(n) else ""
    design = model.design_depth(n.name, domain) or 0
    if model.mode(n.name, domain) == "design":
        return f"návrh {design}/{target}" + (" ⚠" if design < target else "")
    depth = model.realization(n.name, domain) or 0
    return f"{depth}/{target}" + (" ⚠" if depth < target else "") + (f" (návrh {design})" if design > depth else "")


def matrix_block(model) -> str:
    domains = list(model.tx.domains)
    rows = [[_link(name), str(n.fm.get("kind") or ""), *[matrix_cell(model, n, d) for d in domains]]
            for name, n in sorted(model.entities.items())]
    if not rows:
        return "_Žádné entity._"
    return "\n".join(_table(["Entita", "kind", *domains], rows))


def place_of(model, name: str) -> tuple[list[str], str | None]:
    """Umístění entity: vlastní `located_in`, jinak zděděné od nejbližšího předka (libovolná hloubka).
    Vrací (místa, od koho zděděno | None)."""
    seen, cur = set(), name
    while cur in model.entities and cur not in seen:
        seen.add(cur)
        n = model.entities[cur]
        places = model.link_names(n.fm.get("located_in"))
        if places:
            return places, (None if cur == name else cur)
        cur = model.parent(n)
    return [], None


def map_block(model) -> str:
    rows = []
    for name, n in sorted(model.entities.items()):
        places, source = place_of(model, name)
        origin = "vlastní" if places and source is None else (f"zděděno od {_link(source)}" if source else "")
        for p in places or [NO_PLACE]:
            rows.append((p == NO_PLACE, p, name, str(n.fm.get("kind") or ""), origin))
    if not rows:
        return "_Žádné entity._"
    # bez umístění nahoře: v hierarchii stojí nejvýš (nebo jde o chybu, kterou tak hned vidět)
    rows.sort(key=lambda r: (not r[0], r[1].lower(), r[2].lower()))
    return "\n".join(_table(["Místo", "Entita", "kind", "Umístění"],
                            [["" if none else _link(p), _link(e), k, o] for none, p, e, k, o in rows]))


GENERATORS = {"entity_domain_matrix": matrix_block, "map_entities_by_place": map_block}


def generated_targets(core_root: Path, game_layer: bool) -> list[tuple[str, str]]:
    """(id pohledu, cesta ve vaultu) generovaných pohledů, které instance dostává."""
    out = []
    for v in load_manifest(core_root):
        if v.game_layer and not game_layer:
            continue
        for f in v.files:
            if f.startswith("generated/") and v.id in GENERATORS:
                out.append((v.id, f"{VIEWS_REL}/{ViewDef.target(f)}"))
    return out
