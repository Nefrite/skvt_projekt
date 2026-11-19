"""Příkaz compose_role: kompilát role pro chat (zadání 12, kap. 2 a 2.2; 13, kap. 3).

Kompilát `Roles/_compiled/<Role>_compiled.md` (přípona kvůli jedinečnosti jmen vedle `Roles/<Role>.md`)
= L0 (`_core/agents/CONTRACT.md`) + moduly (L1) + profil (L2) v jednom souboru, protože chat agent
nesleduje odkazy a modul si při spouštěči nedotáhne.

- Profil: `Roles/<Role>.md`, jinak `_core/agents/<Role>.md` (Curator, Auditor); `type: role`.
- `combines`: složené profily (do hloubky, bez cyklů); při rozporu platí přísnější role (12 kap. 2.2).
- Moduly: core `_core/agents/modules/`, lokální `Roles/modules/` (kolize `module_id` = chyba konfigurace).
  Do kompilátu jdou **všechny moduly core s režimem `chat`** (pořadí podle tabulky spouštěčů
  v kontraktu) a lokální moduly z profilů (pořadí podle profilů) s transitivními `requires`.
  Moduly bez režimu `chat` se vynechají a vyjmenují (12 kap. 2, zadání 0.9.5).
- Nadpisy částí se posunou o úroveň níž, frontmatter a HTML komentáře se vynechají.
- Kompilát nese verzi core a datum; zapisuje se jen při změně obsahu (datum samo změnu nedělá).
"""
from __future__ import annotations

import datetime as dt
import difflib
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import CORE_ROOT, core_version
from .errors import EXIT_OK, ConfigError, UsageError
from .fileio import atomic_write, file_hash, read_text, to_posix
from .frontmatter import FrontmatterError, parse
from .vault import Vault

COMPILED_DIR = "Roles/_compiled"
LOCAL_MODULES = "Roles/modules"
COMPILED_SUFFIX = "_compiled"
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_HEADING_RE = re.compile(r"^(#{1,6})(\s+.*)$")
_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
_DATE_RE = re.compile(r"date: \d{4}-\d{2}-\d{2}")
_ROLE_RE = re.compile(r"^Roles/[^/]+\.md$")


@dataclass
class Part:
    rel: str            # logická cesta (od kořene vaultu; core jako _core/…)
    fm: dict
    body: str


@dataclass
class Module(Part):
    @property
    def id(self) -> str:
        return str(self.fm.get("module_id"))

    @property
    def requires(self) -> list[str]:
        return [str(x) for x in (self.fm.get("requires") or [])]

    @property
    def modes(self) -> list[str]:
        return [str(x) for x in (self.fm.get("modes") or [])]


@dataclass
class Compiled:
    role: str
    rel: str
    text: str
    profiles: list[str] = field(default_factory=list)
    modules: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)


@dataclass
class Item:
    role: str
    rel: str
    status: str          # new / changed / unchanged
    text: str
    diff: str
    old_hash: str | None
    compiled: Compiled


# ------------------------------------------------------------------ načtení

def _read_part(path: Path, rel: str) -> Part:
    try:
        fm, sp = parse(read_text(path))
    except FrontmatterError as exc:
        raise ConfigError(f"{rel}: chybný frontmatter ({exc})")
    if not isinstance(fm, dict):
        raise ConfigError(f"{rel}: chybí frontmatter")
    return Part(rel, fm, sp.body)


def _agents_dir(core_root: Path) -> Path:
    d = core_root / "agents"
    if not (d / "CONTRACT.md").is_file():
        raise ConfigError(f"Core nemá kontrakt agentů: {to_posix(d / 'CONTRACT.md')}")
    return d


def load_modules(vault: Vault, core_root: Path = CORE_ROOT) -> dict[str, Module]:
    """Moduly core a lokální moduly instance podle module_id."""
    found: dict[str, Module] = {}
    sources = [(p, f"_core/agents/modules/{p.name}") for p in sorted((_agents_dir(core_root) / "modules").glob("*.md"))]
    local = vault.root / LOCAL_MODULES
    if local.is_dir():
        sources += [(p, f"{LOCAL_MODULES}/{p.name}") for p in sorted(local.glob("*.md"))]
    for path, rel in sources:
        part = _read_part(path, rel)
        if part.fm.get("type") != "agent_module":
            raise ConfigError(f"{rel}: není type: agent_module")
        m = Module(part.rel, part.fm, part.body)
        if m.id != path.stem:
            raise ConfigError(f"{rel}: module_id {m.id} neodpovídá jménu souboru")
        if m.id in found:
            raise ConfigError(f"Modul {m.id} je v core i lokálně ({found[m.id].rel}, {rel}); "
                              "lokální modul nesmí mít id modulu core")
        found[m.id] = m
    return found


def list_profiles(vault: Vault) -> list[str]:
    return sorted(n.name for rel, n in vault.notes.items() if _ROLE_RE.match(rel) and n.type == "role")


def load_profile(vault: Vault, name: str, core_root: Path = CORE_ROOT) -> Part:
    candidates = [(vault.root / "Roles" / f"{name}.md", f"Roles/{name}.md"),
                  (_agents_dir(core_root) / f"{name}.md", f"_core/agents/{name}.md")]
    for path, rel in candidates:
        if path.is_file():
            part = _read_part(path, rel)
            if part.fm.get("type") != "role":
                raise ConfigError(f"{rel}: není type: role")
            return part
    raise UsageError(f"Profil role {name} nenalezen (Roles/{name}.md)")


def _profiles(vault: Vault, role: str, core_root: Path) -> list[tuple[str, Part]]:
    """Hlavní profil a složené profily (combines) do hloubky, bez opakování."""
    out: list[tuple[str, Part]] = []
    seen: set[str] = set()

    def visit(name: str, path: list[str]) -> None:
        if name in path:
            raise ConfigError(f"Profily tvoří cyklus combines: {' → '.join([*path, name])}")
        if name in seen:
            return
        try:
            part = load_profile(vault, name, core_root)
        except UsageError:
            if not path:
                raise
            raise ConfigError(f"{path[-1]}: složená role {name} nenalezena (combines)")
        seen.add(name)
        out.append((name, part))
        for sub in part.fm.get("combines") or []:
            visit(str(sub), [*path, name])

    visit(role, [])
    validity = out[0][1].fm.get("validity")
    if validity in ("superseded", "archived", "outdated"):
        raise UsageError(f"Profil {role} má validity: {validity}; kompilát se nevytváří")
    return out


# ------------------------------------------------------------------ text

def _clean_body(body: str) -> list[str]:
    """Tělo části: bez HTML komentářů a prvního nadpisu H1, nadpisy o úroveň níž (mimo bloky kódu)."""
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    # komentáře mimo bloky kódu
    segments, buf, in_fence = [], [], False
    for line in body.split("\n"):
        if _FENCE_RE.match(line):
            if not in_fence:
                segments.append(("text", "\n".join(buf)))
                buf = [line]
            else:
                buf.append(line)
                segments.append(("code", "\n".join(buf)))
                buf = []
            in_fence = not in_fence
            continue
        buf.append(line)
    segments.append(("code" if in_fence else "text", "\n".join(buf)))
    parts = []
    for kind, seg in segments:
        if kind == "text":
            seg = re.sub(r"(?m)^[ \t]*<!--.*?-->[ \t]*\n?", "", seg, flags=re.S)
            seg = _COMMENT_RE.sub("", seg)
        parts.append(seg)
    lines = "\n".join(p for p in parts).split("\n")

    out, in_fence, h1_dropped = [], False, False
    for line in lines:
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        m = None if in_fence else _HEADING_RE.match(line)
        if m:
            if len(m.group(1)) == 1 and not h1_dropped:
                h1_dropped = True
                continue
            line = "#" + line if len(m.group(1)) < 6 else line
        out.append(line.rstrip())
    # nejvýš jeden prázdný řádek za sebou, bez prázdných okrajů
    result: list[str] = []
    for line in out:
        if line == "" and (not result or result[-1] == ""):
            continue
        result.append(line)
    while result and result[-1] == "":
        result.pop()
    return result


def _contract_order(contract_body: str, ids: list[str]):
    """Klíč řazení modulů core: první výskyt `module_id` v kontraktu (tabulka spouštěčů), pak abecedně."""
    pos = {}
    for mid in ids:
        i = contract_body.find(f"`{mid}`")
        pos[mid] = i if i >= 0 else len(contract_body)
    return lambda mid: (pos[mid], mid)


def _join(items) -> str:
    return ", ".join(items)


def compose(vault: Vault, role: str, today: dt.date | None = None, core_root: Path = CORE_ROOT) -> Compiled:
    today = today or dt.date.today()
    profiles = _profiles(vault, role, core_root)
    modules = load_modules(vault, core_root)
    contract = _read_part(_agents_dir(core_root) / "CONTRACT.md", "_core/agents/CONTRACT.md")

    core_ids = [m.id for m in modules.values() if m.rel.startswith("_core/")]
    queue: list[str] = sorted(core_ids, key=_contract_order(contract.body, core_ids))
    for name, part in profiles:
        for mid in part.fm.get("modules") or []:
            mid = str(mid)
            if mid not in modules:
                raise ConfigError(f"{part.rel}: modul {mid} neexistuje (core ani {LOCAL_MODULES}/)")
            queue.append(mid)
    included: list[str] = []
    skipped: list[str] = []
    seen: set[str] = set()

    def drain() -> None:
        i = 0
        while i < len(queue):
            mid = queue[i]
            i += 1
            if mid in seen:
                continue
            seen.add(mid)
            m = modules[mid]
            if "chat" not in m.modes:
                skipped.append(mid)
                continue
            included.append(mid)
            for req in m.requires:
                if req not in modules:
                    raise ConfigError(f"{m.rel}: požadovaný modul {req} neexistuje")
                queue.append(req)

    drain()

    sources = [p.rel for _, p in profiles] + [contract.rel] + [modules[m].rel for m in included]
    lines = [
        "<!-- hestia:compiled – generovaný soubor, needitovat; obnoví ho compose_role (zadání 12, kap. 2) -->",
        f"<!-- role: {role} | core: {core_version_of(core_root)} | date: {today.isoformat()} -->",
        f"<!-- sources: {_join(sources)} -->",
        f"# {role} – instrukce pro chat",
        "",
        "Kompilát pro režim `chat`: kontrakt (L0), moduly (L1) a profil role (L2) v jednom souboru. "
        "Soubory vaultu odsud neotevřeš; co k tasku potřebuješ, dostaneš v předání nebo na vyžádání. "
        "Platí verze ve vaultu, změny vracíš zápisem Hestia (modul `chat_entry`).",
    ]
    if len(profiles) > 1:
        lines += ["", f"Složené role: {_join(n for n, _ in profiles)}. "
                      "Při rozporu mají přednost pravidla přísnější role (zadání 12, kap. 2.2)."]
    if skipped:
        lines += ["", f"Vynechané moduly (jen režim `vault`): {_join(f'`{m}`' for m in skipped)}."]

    lines += ["", "## Kontrakt Hestia (L0)", "", *_clean_body(contract.body)]
    for mid in included:
        lines += ["", f"## Modul `{mid}` (L1)", "", *_clean_body(modules[mid].body)]
    for idx, (name, part) in enumerate(profiles):
        lines += ["", f"## Role {name} (L2{'' if idx == 0 else ', složená'})", ""]
        context = [str(c) for c in (part.fm.get("context") or [])]
        tags = [str(t) for t in (part.fm.get("knowhow_tags") or [])]
        if context:
            lines += [f"Kontext role (čti vždy): {_join(context)}", ""]
        if tags:
            lines += [f"Know-how ke startu (`knowhow_tags`): {_join(tags)}", ""]
        lines += _clean_body(part.body)
    while lines and lines[-1] == "":
        lines.pop()
    text = "\n".join(lines) + "\n"
    return Compiled(role=role, rel=f"{COMPILED_DIR}/{role}{COMPILED_SUFFIX}.md", text=text,
                    profiles=[n for n, _ in profiles], modules=included, skipped=skipped, sources=sources)


def core_version_of(core_root: Path) -> str:
    if core_root == CORE_ROOT:
        return core_version()
    try:
        return (core_root / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return "0.0.0"


# ------------------------------------------------------------------ plán a zápis

def _without_date(text: str) -> str:
    return _DATE_RE.sub("date: -", text.replace("\r\n", "\n"), count=1)


def plan(vault: Vault, roles: list[str] | None = None, today: dt.date | None = None,
         core_root: Path = CORE_ROOT) -> list[Item]:
    items = []
    for role in (roles or list_profiles(vault)):
        c = compose(vault, role, today, core_root)
        path = vault.root / c.rel
        if not path.exists():
            items.append(Item(role, c.rel, "new", c.text, "", None, c))
            continue
        old = read_text(path)
        if _without_date(old) == _without_date(c.text):
            items.append(Item(role, c.rel, "unchanged", old, "", file_hash(path), c))
            continue
        diff = "".join(difflib.unified_diff(old.replace("\r\n", "\n").splitlines(keepends=True),
                                            c.text.splitlines(keepends=True), fromfile=c.rel, tofile=c.rel))
        items.append(Item(role, c.rel, "changed", c.text, diff, file_hash(path), c))
    return items


def apply(vault: Vault, items: list[Item]) -> None:
    for it in items:
        if it.status in ("new", "changed"):
            atomic_write(vault.root / it.rel, it.text, expected_hash=it.old_hash)


STATUS_TEXT = {"new": "nový", "changed": "změněný", "unchanged": "beze změny"}


def run(args, vault: Vault) -> tuple[int, dict, str]:
    items = plan(vault, args.roles or None)
    if args.apply:
        apply(vault, items)
    payload = {"applied": bool(args.apply), "roles": [
        {"role": i.role, "path": i.rel, "status": i.status, "modules": i.compiled.modules,
         "skipped": i.compiled.skipped, "sources": i.compiled.sources} for i in items]}
    out = []
    if not items:
        out.append("Žádné profily rolí v Roles/.")
    for i in items:
        out.append(f"{i.role}: {STATUS_TEXT[i.status]} → {i.rel}")
        if i.status == "new" and not args.apply:
            out.append(f"  ({len(i.text.splitlines())} řádků; moduly: {_join(i.compiled.modules)})")
        if i.status == "changed" and not args.apply:
            out.append(i.diff.rstrip("\n"))
    if not args.apply and any(i.status != "unchanged" for i in items):
        out.append("Dry-run: nic nezapsáno; zápis s --apply.")
    return EXIT_OK, payload, "\n".join(out)
