"""Příkaz init: založí vault Hestia/ ze šablony (zadání 13 kap. 3, 02, 12 kap. 3a a 7).

Vytvoří: kostru vaultu z vault_template/ (*.md.tpl -> *.md, včetně .obsidian), modul _core/ (kopie core),
hub kořenové entity, master lore prototypu, logy v Maintenance/ ze šablon a vstupní soubor
CLAUDE.md v nadřazené složce (jen pokud ještě neexistuje). Bez --apply jen vypíše, co by vzniklo.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import CORE_ROOT, core_version
from . import views as views_mod
from .errors import UsageError
from .fileio import atomic_write, read_text, to_posix
from .frontmatter import set_field

NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_]*$")
TEXT_SUFFIXES = {".md", ".tpl", ".yaml", ".yml", ".json", ".txt", ""}
TPL_SUFFIX = ".tpl"            # kostra vaultu: soubory *.md.tpl (13 kap. 2), při založení -> *.md
CORE_EXCLUDE_DIRS = {"__pycache__", ".pytest_cache"}
ROOT_KINDS = ("place", "location")      # 12 kap. 3a: kořen prototypu je place nebo location
# instance bez herní vrstvy (13 kap. 3): bez master lore a Entities/
GAME_ONLY = ("Docs/narrative/", "Entities/", "Assets/")   # Assets/: karta assetu má herní sekci (zadání 0.23)
VIEWS_PREFIX = "Dashboard/views/"     # pohledy podle manifestu taxonomy/views.yaml (13 kap. 10.9)


def _no_game_config(text: str) -> str:
    text = text.replace("game_layer: true ", "game_layer: false")
    return re.sub(r"(?m)^prototypes:\n(?:[ \t]+.*\n)*",
                  "prototypes: []\nrequired_docs: []                  # bez herní vrstvy žádné povinné dokumenty\n",
                  text)


def _no_game_index(text: str) -> str:
    text = re.sub(r"(?m)^- (Kořenová entita|Master lore): .*\n", "", text)
    text = text.replace("## Prototyp\n", "## Instance\n\n"
                        "- Bez herní vrstvy (`game_layer: false`): entity, domény a master lore se nevedou.\n")
    return re.sub(r"(?m)^\| `Entities/` .*\n", "", text)


NO_GAME_REWRITE = {"Maintenance/config.yaml": _no_game_config, "Dashboard/Index.md": _no_game_index}


@dataclass
class InitPlan:
    vault: Path
    files: dict[Path, bytes] = field(default_factory=dict)   # absolutní cesta -> obsah
    entrypoint: Path | None = None
    entrypoint_skipped: bool = False
    warnings: list[str] = field(default_factory=list)


def render(text: str, values: dict[str, str]) -> str:
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def _is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name.startswith(".git")


def _read_rendered(path: Path, values: dict) -> bytes:
    if _is_text(path):
        return render(read_text(path), values).encode("utf-8")
    return path.read_bytes()


def build_plan(vault: Path, prototype: str | None, root: str | None, root_kind: str = "place",
               engine_version: str | None = None, today: _dt.date | None = None,
               core_root: Path = CORE_ROOT, game_layer: bool = True) -> InitPlan:
    """Plán založení vaultu. game_layer=False (13 kap. 3, 11 kap. 7a): bez hubu kořene, master lore,
    `prototypes` a `Entities/`; `Docs/` bez podsložek domén; `required_docs` prázdné. `prototype` je pak
    volitelné jméno instance (výchozí jméno nadřazené složky vaultu)."""
    vault = Path(vault).resolve()
    if not game_layer:
        prototype = prototype or vault.parent.name
        if not NAME_RE.match(prototype or ""):
            raise UsageError(f"Neplatné jméno instance {prototype!r} (ASCII, bez mezer a diakritiky; zadej --prototype)")
        if root:
            raise UsageError("--root nedává bez herní vrstvy smysl (instance nemá kořen prototypu)")
        root = ""
    elif not prototype or not root:
        raise UsageError("Herní instance potřebuje --prototype a --root (nebo zadej --no-game-layer)")
    if not NAME_RE.match(prototype or ""):
        raise UsageError(f"Neplatné jméno prototypu {prototype!r} (ASCII, bez mezer a diakritiky)")
    if game_layer and not NAME_RE.match(root or ""):
        raise UsageError(f"Neplatné jméno kořenové entity {root!r} (ASCII, bez mezer a diakritiky)")
    if root_kind not in ROOT_KINDS:
        raise UsageError(f"Kořen prototypu musí být kind {' nebo '.join(ROOT_KINDS)}, ne {root_kind!r}")
    if vault.exists() and (not vault.is_dir() or any(vault.iterdir())):
        raise UsageError(f"Cílová složka není prázdná: {vault}")

    if today is None:
        from .util import today as _today
        today = _today()
    version = core_version() if core_root == CORE_ROOT else (core_root / "VERSION").read_text("utf-8").strip()
    values = {
        "date:YYYY-MM-DD": today.isoformat(),
        "prototype": prototype,
        "root": root,
        "engine_version": json.dumps(engine_version) if engine_version else "null",
        "hestia_version": version,
    }
    plan = InitPlan(vault)
    tpl_dir = core_root / "vault_template"
    templates = core_root / "templates"

    # 1) kostra vaultu
    for src in sorted(p for p in tpl_dir.rglob("*") if p.is_file()):
        rel = to_posix(src.relative_to(tpl_dir))
        if rel == "entrypoint.md.tpl":
            continue
        if not game_layer and rel.startswith(GAME_ONLY):
            continue
        if rel.startswith(VIEWS_PREFIX) and not src.name.startswith("."):
            if rel[len(VIEWS_PREFIX):] not in views_mod.template_files(core_root, game_layer):
                continue
        if rel.endswith(".md" + TPL_SUFFIX):
            rel = rel[: -len(TPL_SUFFIX)]
        dest = vault / render(rel, values)
        plan.files[dest] = _read_rendered(src, values)
        if not game_layer and rel in NO_GAME_REWRITE:
            plan.files[dest] = NO_GAME_REWRITE[rel](plan.files[dest].decode("utf-8")).encode("utf-8")
    if not game_layer:
        plan.files[vault / "Docs" / ".gitkeep"] = b""

    # 2) modul _core/ (celý core; testy žijí v hearthlore/tests)
    for src in sorted(p for p in core_root.rglob("*") if p.is_file()):
        parts = src.relative_to(core_root).parts
        if any(part in CORE_EXCLUDE_DIRS for part in parts) or src.suffix == ".pyc":
            continue
        plan.files[vault / "_core" / Path(*parts)] = src.read_bytes()

    # 3) logy a fronta ze šablon
    tvals = dict(values, title="")
    for name in ("queue.md", "changes.md", "structure_log.md"):
        text = render(read_text(templates / f"tpl_{name}"), tvals)
        if name == "changes.md":
            text = text.rstrip("\n") + "\n" + \
                f"| {today.isoformat()} | hestia | Hestia | založení vaultu ze šablony (core {version}) | init |\n"
        plan.files[vault / "Maintenance" / name] = text.encode("utf-8")

    # 4) hub kořenové entity (12 kap. 3a: kořen má target_narrative aspoň 1)
    if not game_layer:
        return _entrypoint(plan, vault, tpl_dir, values)
    hub = render(read_text(templates / "tpl_entity.md"), dict(values, title=root))
    hub = set_field(hub, "kind", root_kind)
    hub = set_field(hub, "depth_narrative", 0)
    hub = set_field(hub, "target_narrative", 1)
    plan.files[vault / "Entities" / f"{root}.md"] = hub.encode("utf-8")

    return _entrypoint(plan, vault, tpl_dir, values)


def _entrypoint(plan: InitPlan, vault: Path, tpl_dir: Path, values: dict) -> InitPlan:
    # 5) vstupní soubor pro agenty (12 kap. 7) – mimo vault, nepřepisuje se
    entry = vault.parent / "CLAUDE.md"
    plan.entrypoint = entry
    if entry.exists():
        plan.entrypoint_skipped = True
        plan.warnings.append(f"{entry} už existuje, nepřepisuji; doplň do něj odkaz na Hestia ručně "
                             f"(obsah: _core/templates/tpl_entrypoint.md)")
    else:
        plan.files[entry] = _read_rendered(tpl_dir / "entrypoint.md.tpl", values)
    return plan


def apply_plan(plan: InitPlan) -> None:
    plan.vault.mkdir(parents=True, exist_ok=True)
    for dest, data in plan.files.items():
        atomic_write(dest, data)


def summary(plan: InitPlan, applied: bool) -> dict:
    vault_files = sorted(to_posix(p.relative_to(plan.vault)) for p in plan.files if plan.vault in p.parents)
    top = sorted({f.split("/")[0] for f in vault_files})
    return {
        "command": "init",
        "applied": applied,
        "vault": to_posix(plan.vault),
        "files": len(plan.files),
        "top_level": top,
        "core_files": sum(1 for f in vault_files if f.startswith("_core/")),
        "entrypoint": None if plan.entrypoint_skipped or plan.entrypoint is None else to_posix(plan.entrypoint),
        "warnings": plan.warnings,
    }


def run(args) -> tuple[int, dict, str]:
    vault = Path(args.vault) if args.vault else Path.cwd() / "Hestia"
    plan = build_plan(vault, args.prototype, args.root, args.root_kind, args.engine_version,
                      game_layer=not getattr(args, "no_game_layer", False))
    if args.apply:
        apply_plan(plan)
    s = summary(plan, bool(args.apply))
    verb = "Vytvořeno" if args.apply else "Vytvořilo by se (dry-run, zapiš s --apply)"
    lines = [f"{verb}: {s['files']} souborů, vault {s['vault']}",
             f"  ve vaultu: {', '.join(s['top_level'])} (z toho _core/: {s['core_files']} souborů)"]
    if s["entrypoint"]:
        lines.append(f"  vstupní soubor: {s['entrypoint']}")
    lines += [f"  upozornění: {w}" for w in s["warnings"]]
    return 0, s, "\n".join(lines)
