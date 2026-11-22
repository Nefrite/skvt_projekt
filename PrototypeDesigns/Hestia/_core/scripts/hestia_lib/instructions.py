"""Změny instrukcí po aktualizaci core a příkaz role_diff (zadání 13 kap. 10.6, 10.13; zadání 0.21).

- **Oddíl *Změny instrukcí*** v reportu `update_core` (`### Změny instrukcí` v oddílu přechodu): pro každý změněný
  soubor v `agents/` core (kontrakt, profily core, moduly, `write_rules.md`, `review_plan.md`) a pro
  `templates/tpl_role.md` změněné sekce (nadpis `##` a `###`, vlastní text sekce bez podsekcí; nová, odebraná,
  změněná) a nové znění změněných sekcí jako citace (`> `, aby nadpisy nerozbily report). Změna frontmatteru je
  sekce *(frontmatter)*, řádek `updated` se nepočítá. Nad 3 000 znaků nového znění na soubor jen seznam sekcí.
  Pak pro každou roli v `Roles/` a role core, které změněné soubory používá: kontrakt a `write_rules.md` všechny,
  vlastní profil core, `review_plan.md` Curator a Auditor, moduly core `compile: all`, moduly z `modules`
  profilu (i složených, `combines`) s `requires`, `tpl_role.md` projektové role.
- **`role_diff <Role> [--since <verze>]`**: oddíly *Změny instrukcí* z reportů `update_core` přechodů novějších
  než `--since` (výchozí: verze před poslední aktualizací ze `structure_version.md`), jen soubory, které role
  používá, a řádky `changes.md` k `Roles/<Role>.md` a k lokálním modulům role (`Roles/modules/`) od data toho
  přechodu. Bez změn „beze změny od <verze>“. Jen čte.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import CORE_ROOT
from .errors import EXIT_OK, ConfigError, UsageError
from .fileio import read_text
from .frontmatter import split
from .links import headings
from .logs import log_entries
from .vault import Vault

SECTION = "### Změny instrukcí"
UNKNOWN = "změny instrukcí nelze určit"
READ_ALL = "přečti instrukce své role celé (kontrakt, profil, moduly, `write_rules.md`)"
FILE_PREFIX = "#### `"
ROLES_HEADING = "#### Role a soubory"
TEXT_LIMIT = 3000
FM_KEY = "(frontmatter)"
INTRO_KEY = "(úvod)"
CORE_ROLES = ("Curator", "Auditor", "Librarian")
TPL_ROLE = "templates/tpl_role.md"
ALWAYS = ("agents/CONTRACT.md", "agents/write_rules.md")
REVIEW_PLAN = "agents/review_plan.md"
REPORTS = "Maintenance/reports"
CHANGES = "Maintenance/changes.md"
_TRANSITION_RE = re.compile(r"^## Přechod (\d+\.\d+\.\d+) → (\d+\.\d+\.\d+)\s*$", re.M)


def _vt(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.split("."))


def instruction_files(core: Path) -> dict[str, Path]:
    """Soubory instrukcí core: rel (od kořene core, s /) -> cesta."""
    out = {}
    agents = core / "agents"
    for p in sorted(agents.glob("*.md")) + sorted((agents / "modules").glob("*.md")) if agents.is_dir() else []:
        out[p.relative_to(core).as_posix()] = p
    tpl = core / TPL_ROLE
    if tpl.is_file():
        out[TPL_ROLE] = tpl
    return out


def sections(text: str) -> list[tuple[str, int, str]]:
    """(klíč, úroveň, vlastní text) – frontmatter bez `updated`, úvod a sekce `##`/`###` do dalšího nadpisu."""
    text = text.replace("\r\n", "\n")
    sp = split(text)
    out = []
    if sp.has_frontmatter:
        fm = "\n".join(l for l in sp.fm_text.split("\n") if not l.startswith("updated:"))
        out.append((FM_KEY, 0, fm.strip()))
    body = sp.body
    lines = body.split("\n")
    hs = [(lvl, t, no) for lvl, t, no in headings(body) if lvl in (2, 3)]
    first = hs[0][2] - 1 if hs else len(lines)
    out.append((INTRO_KEY, 1, "\n".join(lines[:first]).strip()))
    for i, (lvl, title, no) in enumerate(hs):
        end = hs[i + 1][2] - 1 if i + 1 < len(hs) else len(lines)
        out.append((f"{'#' * lvl} {title}", lvl, "\n".join(lines[no - 1:end]).strip()))
    return out


def file_change(rel: str, old: str | None, new: str | None) -> dict | None:
    """Změna souboru instrukcí po sekcích; None, když se vlastní text sekcí nezměnil."""
    olds = {k: t for k, _l, t in sections(old)} if old is not None else {}
    news = sections(new) if new is not None else []
    newd = {k: t for k, _l, t in news}
    changed = []
    for k, _lvl, t in news:
        if k not in olds:
            changed.append({"section": k, "change": "nová", "text": t})
        elif olds[k] != t:
            changed.append({"section": k, "change": "změněná", "text": t})
    changed += [{"section": k, "change": "odebraná", "text": ""} for k in olds if k not in newd]
    changed = [c for c in changed if not (c["section"] in (FM_KEY, INTRO_KEY) and c["change"] == "nová"
                                          and not c["text"] and old is not None)]
    if not changed:
        return None
    status = "nový" if old is None else "odebraný" if new is None else "změněný"
    total = sum(len(c["text"]) for c in changed)
    return {"file": rel, "status": status, "sections": changed, "chars": total, "full": total <= TEXT_LIMIT}


def changes_between(old_core: Path | None, new_core: Path) -> list[dict] | None:
    """Změněné soubory instrukcí; None, když starý core není k dispozici."""
    if old_core is None or not old_core.is_dir():
        return None
    old_f, new_f = instruction_files(old_core), instruction_files(new_core)
    out = []
    for rel in sorted(set(old_f) | set(new_f)):
        o = read_text(old_f[rel]) if rel in old_f else None
        n = read_text(new_f[rel]) if rel in new_f else None
        ch = file_change(rel, o, n)
        if ch:
            out.append(ch)
    return out


# ---------------------------------------------------------------- role a soubory

def role_names(vault: Vault, core: Path) -> list[str]:
    roles = []
    rd = vault.root / "Roles"
    for p in sorted(rd.glob("*.md")) if rd.is_dir() else []:
        try:
            fm = split(read_text(p))
            import yaml
            data = yaml.safe_load(fm.fm_text) if fm.has_frontmatter else None
        except Exception:                      # noqa: BLE001 – vadný profil nahlásí lint
            continue
        if isinstance(data, dict) and data.get("type") == "role":
            roles.append(p.stem)
    roles += [r for r in CORE_ROLES if (core / "agents" / f"{r}.md").is_file() and r not in roles]
    return roles


def files_of_role(vault: Vault, role: str, core: Path) -> tuple[set[str], set[str]]:
    """(soubory core, které role používá; lokální moduly a profily role v Roles/ jako rel od vaultu)."""
    from . import compose
    used = set(ALWAYS)
    local: set[str] = set()
    try:
        profiles = compose._profiles(vault, role, core)
        modules = compose.load_modules(vault, core)
    except (UsageError, ConfigError):
        return used, local
    for name, part in profiles:
        if part.rel.startswith("_core/"):
            used.add(part.rel.removeprefix("_core/"))
        else:
            local.add(part.rel)
            used.add(TPL_ROLE)
        if name in ("Curator", "Auditor"):
            used.add(REVIEW_PLAN)
    queue = [m.id for m in modules.values() if m.rel.startswith("_core/") and not m.listed]
    queue += [str(mid) for _n, part in profiles for mid in (part.fm.get("modules") or [])]
    seen = set()
    while queue:
        mid = queue.pop()
        if mid in seen or mid not in modules:
            continue
        seen.add(mid)
        m = modules[mid]
        if m.rel.startswith("_core/"):
            used.add(m.rel.removeprefix("_core/"))
        else:
            local.add(m.rel)
        queue += list(m.requires)
    return used, local


def usage(vault: Vault, core: Path, changes: list[dict]) -> dict[str, list[str]]:
    files = {c["file"] for c in changes}
    out = {}
    for role in role_names(vault, core):
        used, _local = files_of_role(vault, role, core)
        out[role] = sorted(files & used)
    return out


# ---------------------------------------------------------------- oddíl reportu

def _quote(text: str) -> list[str]:
    return [("> " + l) if l else ">" for l in text.split("\n")]


def section_md(changes: list[dict] | None, roles: dict[str, list[str]] | None) -> list[str]:
    lines = ["", SECTION]
    if changes is None:
        return lines + [f"- Starý core nenalezen (záloha v `_to_delete/` chybí); {UNKNOWN}. Každá role: {READ_ALL}."]
    if not changes:
        return lines + ["_Beze změny instrukcí._"]
    lines.append(f"- Změněné soubory: {len(changes)}. Role si změny vypíše `role_diff <Role>`.")
    for c in changes:
        lines += ["", f"{FILE_PREFIX}{c['file']}` ({c['status']})",
                  "- Sekce: " + ", ".join(f"{s['section'].lstrip('# ')} ({s['change']})" for s in c["sections"])]
        if not c["full"]:
            lines.append(f"- Nové znění: {c['chars']} znaků, nad {TEXT_LIMIT}; přečti sekce v `_core/{c['file']}`.")
            continue
        for s in c["sections"]:
            if s["text"]:
                lines += [""] + _quote(s["text"])
    if roles is not None:
        lines += ["", ROLES_HEADING]
        lines += [f"- {r}: " + (", ".join(f"`{f}`" for f in fs) if fs else "nic") for r, fs in roles.items()]
    return lines


def parse_section(text: str) -> dict[str, str]:
    """Bloky souborů z oddílu Změny instrukcí: rel -> text bloku."""
    out, cur, buf = {}, None, []
    for line in text.split("\n"):
        if line.startswith(FILE_PREFIX) or line.startswith(ROLES_HEADING):
            if cur:
                out[cur] = "\n".join(buf).rstrip()
            cur = line[len(FILE_PREFIX):].split("`", 1)[0] if line.startswith(FILE_PREFIX) else None
            buf = [line]
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).rstrip()
    return out


def report_sections(vault: Vault, since: str) -> list[tuple[str, str, str, str | None]]:
    """(datum reportu, stará, nová, text oddílu Změny instrukcí) pro přechody na verzi novější než since;
    text None = oddíl v přechodu chybí (starší `update_core`, zadání 0.21.1)."""
    out = []
    d = vault.root / REPORTS
    for p in sorted(d.glob("update_core_*.md")) if d.is_dir() else []:
        text = read_text(p).replace("\r\n", "\n")
        day = p.stem.removeprefix("update_core_")
        marks = list(_TRANSITION_RE.finditer(text))
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
            nxt = re.search(r"^## ", text[m.end():end], re.M)
            block = text[m.end():m.end() + nxt.start()] if nxt else text[m.end():end]
            if _vt(m.group(2)) <= _vt(since):
                continue
            k = block.find(SECTION + "\n")
            if k < 0:
                out.append((day, m.group(1), m.group(2), None))
                continue
            rest = block[k + len(SECTION) + 1:]
            stop = re.search(r"^### ", rest, re.M)
            out.append((day, m.group(1), m.group(2), rest[:stop.start()] if stop else rest))
    return out


def _since_default(vault: Vault, core: Path) -> tuple[str | None, str | None]:
    """(verze před poslední aktualizací, datum té aktualizace) ze structure_version.md."""
    from .upgrade import SV_REL, SV_RE
    p = vault.root / SV_REL
    cur = read_text(core / "VERSION").strip() if (core / "VERSION").is_file() else None
    found = None
    for m in SV_RE.finditer(read_text(p)) if p.is_file() else []:
        if m.group(2) == cur:
            found = (m.group(3), m.group(1))
    return found or (None, None)


def _since_date(vault: Vault, since: str) -> str | None:
    """Datum první aktualizace z verze since (nebo novější) ze structure_version.md."""
    from .upgrade import SV_REL, SV_RE
    p = vault.root / SV_REL
    for m in SV_RE.finditer(read_text(p)) if p.is_file() else []:
        if _vt(m.group(3)) >= _vt(since):
            return m.group(1)
    return None


def run(args, vault: Vault) -> tuple[int, dict, str]:
    role = (args.role or "").strip()
    if not role:
        raise UsageError("role_diff: zadej roli")
    core = CORE_ROOT
    since, since_day = (args.since, None) if args.since else _since_default(vault, core)
    if not since:
        raise UsageError("role_diff: verze před aktualizací není ve structure_version.md; zadej --since <verze>")
    since_day = since_day or _since_date(vault, since)
    used, local = files_of_role(vault, role, core)
    blocks, unknown = [], []
    for day, old, new, text in report_sections(vault, since):
        if text is None or UNKNOWN in text:
            unknown.append({"transition": f"{old} → {new}", "report": f"{REPORTS}/update_core_{day}.md"})
            continue
        for rel, block in parse_section(text).items():
            if rel in used:
                blocks.append({"transition": f"{old} → {new}", "report": f"{REPORTS}/update_core_{day}.md",
                               "file": rel, "text": block})
    rows = []
    cp = vault.root / CHANGES
    names = {Path(x).stem for x in local} | {role}
    for cells in log_entries(read_text(cp)) if cp.is_file() else []:
        if len(cells) < 4 or (since_day and cells[0] < since_day):
            continue
        target = cells[2].strip().strip("[]").replace("\\", "/")
        if target in local or target.removesuffix(".md") in {x.removesuffix(".md") for x in local} \
                or (target.startswith("Roles/") and Path(target).stem in names):
            rows.append(cells)
    payload = {"command": "role_diff", "role": role, "since": since, "files": sorted(used | local),
               "changes": blocks, "changes_md": rows, "unknown": unknown}
    if not blocks and not rows and not unknown:
        return EXIT_OK, payload, f"role_diff {role}: beze změny od {since}"
    lines = [f"role_diff {role}: změny od {since}"]
    for u in unknown:
        lines += ["", f"[{u['transition']}, {u['report']}] {UNKNOWN} (oddíl chybí nebo starý core nebyl "
                      f"k dispozici); {READ_ALL}"]
    for b in blocks:
        lines += ["", f"[{b['transition']}, {b['report']}]", b["text"]]
    if rows:
        lines += ["", "changes.md (profil a lokální moduly role):"] + ["| " + " | ".join(r) + " |" for r in rows]
    return EXIT_OK, payload, "\n".join(lines)
