"""Příkaz update_core: bezpečně převést instanci na novou verzi core (zadání 13 kap. 10.6, 11 kap. 6).

- Zdroj: `--from <cesta k hestia/>`, nebo `--tag vX.Y.Z` / `--latest` z repozitáře `core_source` (config.yaml)
  přes `git archive` do dočasné složky mimo vault; jen značky tvaru `vMAJOR.MINOR.PATCH` (zadání 0.15).
- Dry-run: rozdíl verzí, změněné soubory core, migrační poznámky z CHANGELOG.md mezi starou a novou verzí,
  hodnoty `taxonomy_local`, které budou v core; upozornění na necommitnuté změny v projektu (11 kap. 6, krok 2).
- Přerušenou výměnu (existuje `_core.new`, chybí `_core`) dokončí další běh; existují-li oba, odmítne.
- `--apply`: nový core se nakopíruje vedle (`_core.new`) a vymění atomickým přejmenováním; starý core se
  přesune do `_to_delete/_core_<verze>/`; řádek do `structure_version.md`; z `taxonomy_local` se odstraní
  hodnoty nově v core a zapíší do `changes.md`; funkční nastavení `.obsidian` se nemění (02 kap. 7.1).
- Na konci upozornění, jsou-li kompiláty rolí starší než nový core.
- Report (zadání 0.15.3): po výměně `_core/` hned oddíl přechodu v reportu dne (`upgrade.start_section`), kroky
  ho doplní; průběh na stderr hned. Oddíl *Změny instrukcí* (zadání 0.21, modul `instructions`) se spočte před
  výměnou ze starého a nového core; kroky po aktualizaci ho obnoví ze starého core v `_to_delete/`. Dry-run ohlásí nedokončený přechod a doporučí `--after-only --apply`.
- Migrace MAJOR verzí: `scripts/migrations/<verze>.py` v novém core s funkcí `migrate(vault, apply)`;
  spustí se v dry-run a s `--apply` po schválení. Ve fázi 3 jen kostra bez migrací.
- Snippety core `.obsidian/snippets/hestia-*.css` (02 kap. 7.1) srovná při každém běhu: chybějící doplní,
  změněné přepíše, ty, které core nemá, přesune do `_to_delete/.obsidian/snippets/`; `appearance.json`
  (zapnutí) nemění; každý zásah zapíše do `changes.md`.
- Kroky po aktualizaci podle manifestu `upgrade.yaml` nového core (13 kap. 10.6a, modul `upgrade`): dry-run je
  vypíše; po `--apply` je řídicí skript spustí **novým** core jako `update_core --after-only --since <stará>`
  (automatické kroky, `lint`/`audit` v dry-run, ruční úkoly do `queue.md`, report). `--no-after` je přeskočí.
- `--work-copy [<adresář>]` (zadání 0.22, CR-023): s `--apply` přechod v lokální pracovní kopii vaultu
  a zápis zpět bez mazání (modul `workcopy`); `--work-phase copy|run|back`, `--keep-work-copy`. I s `--after-only`
  (zadání 0.22.1): kroky po aktualizaci v kopii, kontrola originálu, zápis zpět.
- `--with-views` (13 kap. 10.9): nakopíruje do `Dashboard/views/` chybějící pohledy z `vault_template` nového
  core (`bases/*.base`, `dataview/dv_*.md`), existující nepřepíše; funguje i bez změny verze core.
"""
from __future__ import annotations

import filecmp
import json
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path

from . import gitinfo
from .errors import EXIT_OK, UsageError
from .fileio import atomic_write, file_hash, read_text, to_posix
from .logs import append_lines, format_line
from .taxonomy import KEYED_FILES, load_yaml
from . import upgrade as upgrade_mod
from . import views as views_mod
from .util import today
from .vault import Vault

EXCLUDE_DIRS = {"__pycache__", ".pytest_cache"}
VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
CHANGELOG_HEAD_RE = re.compile(r"^## (\d+\.\d+\.\d+)\b.*$", re.M)
COMPILED_HEADER_RE = re.compile(r"\bcore:? (\d+\.\d+\.\d+)")      # hlavička compose_role: „| core: X |“
TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def parse_version(v: str) -> tuple[int, int, int]:
    m = VERSION_RE.match((v or "").strip())
    if not m:
        raise UsageError(f"Neplatná verze core {v!r} (MAJOR.MINOR.PATCH)")
    return tuple(int(x) for x in m.groups())


def read_version(core: Path) -> str:
    p = core / "VERSION"
    if not p.is_file():
        raise UsageError(f"Chybí VERSION: {p}")
    return read_text(p).strip()


def core_files(root: Path) -> dict[str, Path]:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and not set(p.relative_to(root).parts) & EXCLUDE_DIRS and p.suffix != ".pyc":
            out[to_posix(p.relative_to(root))] = p
    return out


def changelog_notes(new_core: Path, old: str, new: str) -> list[tuple[str, str]]:
    """Sekce CHANGELOG.md pro verze (old, new]: (verze, úvodní odstavec s migrační poznámkou)."""
    p = new_core / "CHANGELOG.md"
    if not p.is_file():
        return []
    text = read_text(p).replace("\r\n", "\n")
    heads = list(CHANGELOG_HEAD_RE.finditer(text))
    lo, hi = parse_version(old), parse_version(new)
    out = []
    for i, m in enumerate(heads):
        ver = m.group(1)
        if not (lo < parse_version(ver) <= hi):
            continue
        body = text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)].strip()
        para = body.split("\n\n", 1)[0].strip()
        migr = [l.strip() for l in body.split("\n") if re.search(r"migra", l, re.I) and l.strip() != para]
        out.append((ver, "\n".join([para, *migr])))
    return out


def local_overlaps(vault: Vault, new_core: Path) -> list[tuple[str, str, str]]:
    """(soubor, klíč, hodnota) z taxonomy_local, které nový core už obsahuje."""
    local = vault.root / "Maintenance" / "taxonomy_local"
    out = []
    for fname, key in KEYED_FILES.items():
        lp, cp = local / fname, new_core / "taxonomy" / fname
        if not lp.is_file() or not cp.is_file():
            continue
        core_ids = {it.get(key) for it in (load_yaml(cp) or {}).get("items") or [] if isinstance(it, dict)}
        for it in (load_yaml(lp) or {}).get("items") or []:
            if isinstance(it, dict) and it.get(key) in core_ids:
                out.append((fname, key, str(it.get(key))))
    lp, cp = local / "enums.yaml", new_core / "taxonomy" / "enums.yaml"
    if lp.is_file() and cp.is_file():
        core_vals = {it.get("name"): set(it.get("values") or []) for it in (load_yaml(cp) or {}).get("items") or []}
        for it in (load_yaml(lp) or {}).get("items") or []:
            for v in it.get("values") or []:
                if v in core_vals.get(it.get("name"), set()):
                    out.append(("enums.yaml", str(it.get("name")), str(v)))
    return out


def remove_local_values(text: str, key: str, values: set[str]) -> str:
    """Řádkově odstraní položky `- key: X` (blok) nebo `- {key: X, …}` z YAML seznamu items."""
    lines = text.splitlines(keepends=True)
    out, skip_indent = [], None
    item_re = re.compile(r"^(\s*)-\s*(\{.*\}|" + re.escape(key) + r"\s*:\s*(.+?))\s*$")
    for line in lines:
        raw = line.rstrip("\r\n")
        if skip_indent is not None:
            ind = len(raw) - len(raw.lstrip())
            if raw.strip() and ind > skip_indent and not raw.lstrip().startswith("- "):
                continue
            skip_indent = None
        m = item_re.match(raw)
        if m:
            val = None
            if m.group(2).startswith("{"):
                mm = re.search(re.escape(key) + r"\s*:\s*([^,}]+)", m.group(2))
                val = mm.group(1).strip().strip("\"'") if mm else None
            else:
                val = m.group(3).strip().strip("\"'")
            if val in values:
                skip_indent = len(m.group(1))
                continue
        out.append(line)
    return "".join(out)


def stale_compiled(vault: Vault, new_version: str) -> list[str]:
    out = []
    d = vault.root / "Roles" / "_compiled"
    for p in sorted(d.glob("*_compiled.md")) if d.is_dir() else []:
        m = COMPILED_HEADER_RE.search("\n".join(read_text(p).splitlines()[:3]))
        if not m or m.group(1) != new_version:
            out.append(p.name)
    return out


def find_migrations(new_core: Path, old: str, new: str) -> list[Path]:
    """Migrace MAJOR verzí: scripts/migrations/<verze>.py pro verze (old, new] se změnou MAJOR."""
    d = new_core / "scripts" / "migrations"
    if not d.is_dir() or parse_version(new)[0] == parse_version(old)[0]:
        return []
    lo, hi = parse_version(old), parse_version(new)
    out = []
    for p in sorted(d.glob("*.py")):
        if VERSION_RE.match(p.stem) and lo < parse_version(p.stem) <= hi:
            out.append(p)
    return out


def run_migration(path: Path, vault: Vault, apply: bool) -> str:
    spec = importlib.util.spec_from_file_location(f"hestia_migration_{path.stem.replace('.', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "migrate"):
        raise UsageError(f"Migrace {path.name} nemá funkci migrate(vault, apply)")
    return str(mod.migrate(vault, apply) or "")


SNIPPETS_REL = ".obsidian/snippets"
SNIPPET_GLOB = "hestia-*.css"


def snippet_plan(vault: Vault, new_core: Path) -> list[tuple[str, str]]:
    """(akce, jméno) pro snippety core: add / update / remove (02 kap. 7.1)."""
    src_dir = new_core / "vault_template" / SNIPPETS_REL
    dst_dir = vault.root / SNIPPETS_REL
    if not (vault.root / ".obsidian").is_dir():
        return []
    src = {p.name: p for p in src_dir.glob(SNIPPET_GLOB)} if src_dir.is_dir() else {}
    dst = {p.name: p for p in dst_dir.glob(SNIPPET_GLOB)} if dst_dir.is_dir() else {}
    out = [("add", n) for n in sorted(set(src) - set(dst))]
    out += [("update", n) for n in sorted(set(src) & set(dst)) if src[n].read_bytes() != dst[n].read_bytes()]
    out += [("remove", n) for n in sorted(set(dst) - set(src))]
    return out


def apply_snippets(vault: Vault, new_core: Path, plan: list[tuple[str, str]]) -> None:
    src_dir, dst_dir = new_core / "vault_template" / SNIPPETS_REL, vault.root / SNIPPETS_REL
    for action, name in plan:
        dst = dst_dir / name
        if action == "remove":
            trash = vault.root / "_to_delete" / SNIPPETS_REL / name
            n = 2
            while trash.exists():
                trash = trash.with_name(f"{name[:-4]}_{n}.css")
                n += 1
            trash.parent.mkdir(parents=True, exist_ok=True)
            os.rename(dst, trash)
        else:
            atomic_write(dst, (src_dir / name).read_bytes(),
                         expected_hash=file_hash(dst) if action == "update" else None)


SNIPPET_VERB = {"add": "doplněn", "update": "aktualizován", "remove": "přesunut do _to_delete/ (core ho nemá)"}


def missing_views(vault: Vault, new_core: Path) -> list[tuple[Path, Path]]:
    """(zdroj ve vault_template, cíl ve vaultu) pro pohledy z manifestu nového core, které ve vaultu chybí;
    při `game_layer: false` bez pohledů s příznakem herní vrstvy. `local/` se nekontroluje."""
    src_root = new_core / "vault_template" / "Dashboard" / "views"
    out = []
    for rel in views_mod.template_files(new_core, vault.game_layer):
        src, dst = src_root / rel, vault.root / views_mod.VIEWS_REL / views_mod.ViewDef.target(rel)
        if src.is_file() and not dst.exists():
            out.append((src, dst))
    keep_src = src_root / "local" / ".gitkeep"                # složka pro vlastní pohledy instance
    if keep_src.is_file() and not (vault.root / views_mod.VIEWS_REL / "local").exists():
        out.append((keep_src, vault.root / views_mod.VIEWS_REL / "local" / ".gitkeep"))
    return out


def core_repo(vault: Vault) -> Path:
    """Repozitář HearthLore podle `core_source` (relativně k vaultu, 13 kap. 4)."""
    cs = vault.config.get("core_source")
    if not cs:
        raise UsageError("Chybí core_source v Maintenance/config.yaml (cesta k repozitáři HearthLore relativně "
                         "k vaultu, např. core_source: \"../../HearthLore\"); nebo použij --from <cesta k hestia/>")
    repo = (vault.home / str(cs)).resolve()
    if not repo.is_dir() or gitinfo.toplevel(repo) is None:
        raise UsageError(f"core_source {cs!r} ({repo}) není git repozitář")
    return repo


def core_tags(repo: Path) -> list[str]:
    """Značky core `vMAJOR.MINOR.PATCH` vzestupně podle verze."""
    tags = gitinfo.tags(repo)
    if tags is None:
        raise UsageError(f"Nelze číst značky v {repo} (git)")
    return sorted((t for t in tags if TAG_RE.match(t)), key=lambda t: parse_version(t[1:]))


def resolve_tag(args, repo: Path) -> str:
    tags = core_tags(repo)
    if args.latest:
        if not tags:
            raise UsageError(f"V {repo} není žádná značka core vMAJOR.MINOR.PATCH")
        return tags[-1]
    if not TAG_RE.match(args.tag or ""):
        raise UsageError(f"--tag {args.tag!r}: čekám značku core tvaru vMAJOR.MINOR.PATCH (např. v0.14.0)")
    if args.tag not in tags:
        raise UsageError(f"Značka {args.tag} v {repo} není (poslední: {tags[-1] if tags else '–'})")
    return args.tag


def export_tag(repo: Path, tag: str, dest: Path) -> Path:
    """`hestia/` značky přes git archive do dest; vrací cestu k hestia/."""
    data = gitinfo.archive(repo, tag, "hestia")
    if data is None:
        raise UsageError(f"git archive {tag} hestia v {repo} selhal (má značka složku hestia/?)")
    with tarfile.open(fileobj=BytesIO(data)) as tar:
        try:
            tar.extractall(dest, filter="data")
        except TypeError:                                   # Python bez filtru extrakce
            tar.extractall(dest)
    return dest / "hestia"


def run(args, vault: Vault) -> tuple[int, dict, str]:
    work_copy = getattr(args, "work_copy", None)
    if work_copy is None and (getattr(args, "work_phase", None) or getattr(args, "keep_work_copy", False)):
        raise UsageError("--work-phase a --keep-work-copy jen s --work-copy")
    if work_copy is not None:
        if vault.origin is not None:
            raise UsageError("--work-copy nad pracovní kopií nejde; spusť ho nad originálem vaultu")
        if args.apply:                                   # dry-run jen čte a kopii nepotřebuje (13 kap. 10.6)
            from . import workcopy
            return workcopy.run(args, vault)
    if getattr(args, "after_only", False):
        if args.source or args.tag or args.latest:
            raise UsageError("--after-only nebere zdroj core (--from, --tag, --latest); běží nad _core/")
        code, payload, text = upgrade_mod.run_after(args, vault)
        if work_copy is not None:                          # dry-run (s --apply jde výše do workcopy)
            text += "\nS --apply proběhnou kroky v pracovní kopii (--work-copy) a zápis zpět bez mazání."
        return code, payload, text
    if args.tag or args.latest:
        repo = core_repo(vault)
        tag = resolve_tag(args, repo)
        with tempfile.TemporaryDirectory(prefix="hestia_core_") as tmp:
            return _run(args, vault, export_tag(repo, tag, Path(tmp)), tag)
    if not args.source:
        raise UsageError("Zadej zdroj core: --from <cesta k hestia/>, --tag vX.Y.Z nebo --latest (s core_source)")
    return _run(args, vault, Path(args.source).resolve(), "")


def run_after_subprocess(vault: Vault, old_v: str, quiet: bool = False) -> tuple[int, dict | None, str]:
    """Kroky po aktualizaci novým core (13 kap. 10.6): podproces _core/scripts/hestia.py --after-only.
    Průběh (stderr podprocesu) se předává hned dál (zadání 0.15.3); JSON výsledku jde přes dočasný soubor."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
    cmd = [sys.executable, "-I", str(vault.root / "_core" / "scripts" / "hestia.py"), "update_core",
           "--vault", str(vault.root), "--after-only", "--since", old_v, "--apply", "--json"]
    if quiet:
        cmd.append("--quiet")
    err_lines: list[str] = []
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as out:
        proc = subprocess.Popen(cmd, stdout=out, stderr=subprocess.PIPE, text=True, encoding="utf-8", env=env)
        for line in proc.stderr:
            err_lines.append(line)
            print(line, end="", file=sys.stderr, flush=True)
        code = proc.wait()
        out.seek(0)
        stdout = out.read()
    try:
        data = json.loads(stdout)
    except (json.JSONDecodeError, TypeError):
        tail = [l for l in ("".join(err_lines) or stdout or "").splitlines() if l.strip()]
        return code or 1, None, tail[-1] if tail else f"návratový kód {code}"
    return code, data, ""


def _run(args, vault: Vault, new_core: Path, tag: str) -> tuple[int, dict, str]:
    cur_core = vault.root / "_core"
    if not (new_core / "scripts" / "hestia.py").is_file() or not (new_core / "taxonomy").is_dir():
        raise UsageError(f"{new_core} nevypadá jako hestia/ (chybí scripts/hestia.py nebo taxonomy/)")
    if new_core == cur_core.resolve():
        raise UsageError("--from ukazuje na _core/ tohoto vaultu")
    resumed = ""
    staging = vault.root / "_core.new"
    if staging.is_dir() and not cur_core.exists():          # přerušená výměna (13 kap. 10.6): dokončit
        if args.apply:
            os.rename(staging, cur_core)
            resumed = "Dokončena přerušená výměna: _core.new -> _core."
        else:
            resumed = "Přerušená výměna: _core.new se s --apply přejmenuje na _core (dry-run počítá s ním)."
            cur_core = staging
    new_v = read_version(new_core)
    old_v = read_version(cur_core) if cur_core.is_dir() else "0.0.0"
    if parse_version(new_v) < parse_version(old_v) and not args.force:
        raise UsageError(f"Nová verze {new_v} je starší než {old_v} (návrat jen s --force)")

    new_files, old_files = core_files(new_core), core_files(cur_core) if cur_core.is_dir() else {}
    added = sorted(set(new_files) - set(old_files))
    removed = sorted(set(old_files) - set(new_files))
    modified = sorted(f for f in set(new_files) & set(old_files)
                      if not filecmp.cmp(new_files[f], old_files[f], shallow=False))
    notes = changelog_notes(new_core, old_v, new_v)
    overlaps = local_overlaps(vault, new_core)
    migrations = find_migrations(new_core, old_v, new_v)
    upl = upgrade_mod.with_compose(upgrade_mod.plan(new_core, old_v, new_v), vault, old_v, new_v) \
        if parse_version(new_v) > parse_version(old_v) else upgrade_mod.Plan()
    no_after = getattr(args, "no_after", False)
    pending = None if args.apply else upgrade_mod.unfinished(vault, old_v)
    dirty = gitinfo.changed_files(vault.project_root)
    warnings = []
    if dirty:
        warnings.append(f"projekt má {len(dirty)} necommitnutých změn; před --apply commitni (11 kap. 6, krok 2)")
    unchanged = not (added or removed or modified) and new_v == old_v

    day = today()
    applied = False
    migr_out = [f"{p.name}: {run_migration(p, vault, False)}" for p in migrations]
    if args.apply and not unchanged:
        staging = vault.root / "_core.new"
        if staging.exists():
            raise UsageError(f"{staging} už existuje (přerušená aktualizace?); zkontroluj a přesuň ho ručně")
        # Změny instrukcí se spočtou dřív, než se _core/ přepíše (starý a nový core vedle sebe; zadání 0.21)
        instr = upgrade_mod.instruction_lines(vault, cur_core if cur_core.is_dir() else None, new_core)
        shutil.copytree(new_core, staging, ignore=shutil.ignore_patterns(*EXCLUDE_DIRS, "*.pyc"))
        trash = vault.root / "_to_delete" / f"_core_{old_v}"
        n = 2
        while trash.exists():
            trash = vault.root / "_to_delete" / f"_core_{old_v}_{n}"
            n += 1
        trash.parent.mkdir(parents=True, exist_ok=True)
        if cur_core.is_dir():
            os.rename(cur_core, trash)
        os.rename(staging, cur_core)
        sv = vault.root / "Maintenance" / "structure_version.md"
        if sv.is_file():
            text = read_text(sv)
            how = f"update_core --tag {tag}" if tag else "update_core"
            atomic_write(sv, append_lines(text, [format_line([day.isoformat(), f"core {new_v}",
                                                              f"aktualizace z {old_v} ({how})",
                                                              ", ".join(upl.crs)])], today=day),
                         expected_hash=file_hash(sv))
        # oddíl přechodu v reportu hned po výměně (zadání 0.15.3); kroky ho doplní, přerušení ho nechá viditelný
        upgrade_mod.start_section(vault, old_v, new_v, upl, instr)
        if not getattr(args, "quiet", False):
            print(f"update_core: _core/ vyměněn {old_v} -> {new_v}", file=sys.stderr, flush=True)
        removed_local = []
        local = vault.root / "Maintenance" / "taxonomy_local"
        by_file: dict[str, tuple[str, set]] = {}
        for fname, key, value in overlaps:
            if fname == "enums.yaml":
                continue                              # hodnoty výčtů se odstraňují ručně (vnořený seznam)
            by_file.setdefault(fname, (key, set()))[1].add(value)
        for fname, (key, values) in by_file.items():
            p = local / fname
            old_text = read_text(p)
            new_text = remove_local_values(old_text, key, values)
            if new_text != old_text:
                atomic_write(p, new_text, expected_hash=file_hash(p))
                removed_local += [f"{fname}: {v}" for v in sorted(values)]
        if removed_local:
            cp = vault.root / "Maintenance" / "changes.md"
            if cp.is_file():
                lines = [format_line([day.isoformat(), "hestia", f"taxonomy_local/{x.split(':')[0]}",
                                      f"hodnota {x.split(': ', 1)[1]} je nově v core {new_v}, odstraněna lokálně",
                                      "update_core"]) for x in removed_local]
                atomic_write(cp, append_lines(read_text(cp), lines, today=day), expected_hash=file_hash(cp))
        migr_out = [f"{p.name}: {run_migration(p, Vault.load(vault.root), True)}" for p in migrations]
        applied = True

    snippets = snippet_plan(vault, new_core)
    if args.apply and snippets:
        apply_snippets(vault, new_core, snippets)
        cp = vault.root / "Maintenance" / "changes.md"
        if cp.is_file():
            rows = [format_line([day.isoformat(), "hestia", f"{SNIPPETS_REL}/{n}",
                                 f"snippet core {SNIPPET_VERB[a]} (core {new_v})", "update_core"]) for a, n in snippets]
            atomic_write(cp, append_lines(read_text(cp), rows, today=day), expected_hash=file_hash(cp))

    views, views_note = [], ""
    if getattr(args, "with_views", False):
        skipped = views_mod.skipped_views(new_core, vault.game_layer)
        if skipped:
            views_note = f"bez herní vrstvy vynechané pohledy (čtou entity): {', '.join(skipped)}"
        views = missing_views(vault, new_core)
        if args.apply and views:
            for src, dst in views:
                atomic_write(dst, read_text(src).replace("{{date:YYYY-MM-DD}}", day.isoformat()))
            cp = vault.root / "Maintenance" / "changes.md"
            if cp.is_file():
                names = ", ".join(to_posix(d.relative_to(vault.root / "Dashboard" / "views")) for _s, d in views)
                line = format_line([day.isoformat(), "hestia", "Dashboard/views",
                                    f"doplněné pohledy z core {new_v}: {names}", "update_core --with-views"])
                atomic_write(cp, append_lines(read_text(cp), [line], today=day), expected_hash=file_hash(cp))
    view_rels = [to_posix(d.relative_to(vault.root)) for _s, d in views]

    after, after_code, after_err = None, EXIT_OK, ""
    if applied and not no_after:
        after_code, after, after_err = run_after_subprocess(vault, old_v, getattr(args, "quiet", False))

    stale = stale_compiled(vault, new_v)
    payload = {"command": "update_core", "applied": applied, "from": old_v, "to": new_v, "source": tag or None,
               "upgrade": upl.as_dict(), "after": after, "after_error": after_err or None,
               "added": added, "removed": removed, "modified": modified,
               "changelog": [{"version": v, "note": n} for v, n in notes],
               "taxonomy_local_in_core": [{"file": f, "key": k, "value": v} for f, k, v in overlaps],
               "migrations": migr_out, "stale_compiled": stale, "warnings": warnings, "views": view_rels,
               "resumed": resumed, "snippets": [{"action": a, "file": n} for a, n in snippets],
               "unfinished": pending}
    if unchanged:
        lines = [f"update_core: core {old_v} je aktuální, beze změny"]
    else:
        verb = "aktualizováno" if applied else "aktualizovalo by se (dry-run, zapiš s --apply)"
        lines = [f"update_core: {old_v} -> {new_v} {verb}" + (f" (značka {tag})" if tag else ""),
                 f"Soubory core: nové {len(added)}, odebrané {len(removed)}, změněné {len(modified)}"]
        lines += [f"  + {f}" for f in added] + [f"  - {f}" for f in removed] + [f"  ~ {f}" for f in modified]
        if notes:
            lines.append("Poznámky z CHANGELOG.md:")
            for v, n in notes:
                lines.append(f"  {v}: " + n.replace("\n", "\n    "))
        if applied:
            lines.append("Starý core přesunut do _to_delete/; řádek v structure_version.md.")
        if not applied or no_after:
            lines += upgrade_mod.plan_lines(upl)
        if applied and no_after:
            lines.append("Kroky po aktualizaci přeskočeny (--no-after); doběhnou s update_core --after-only --apply.")
    if overlaps:
        lines.append("Hodnoty taxonomy_local, které jsou v novém core: "
                     + ", ".join(f"{f} {v}" for f, _k, v in overlaps)
                     + ("" if applied else " (s --apply se odstraní lokálně a zapíší do changes.md)"))
    if migrations:
        lines.append("Migrace MAJOR verze: " + "; ".join(migr_out))
    if snippets:
        verb = "" if args.apply else " (dry-run)"
        lines.append(f"Snippety core{verb}: " + ", ".join(f"{n} {SNIPPET_VERB[a]}" for a, n in snippets)
                     + "; zapnutí v appearance.json beze změny")
    if getattr(args, "with_views", False):
        if views:
            verb = "doplněny" if args.apply else "doplnily by se (dry-run)"
            lines.append(f"Pohledy {verb}: " + ", ".join(view_rels))
        else:
            lines.append("Pohledy: všechny už ve vaultu jsou (existující se nepřepisují)")
        if views_note:
            lines.append(f"Pohledy: {views_note}")
    if after is not None:
        lines.append(_after_text(after))
    elif after_err:
        lines.append(f"Chyba: kroky po aktualizaci novým core neproběhly ({after_err}); _core/ zůstává nový, "
                     f"po opravě update_core --after-only --apply")
    if stale and not (after and "compose_role" in [s["step"] for s in after.get("steps") or [] if s["ok"]]):
        lines.append(f"Upozornění: kompiláty rolí jsou starší než core {new_v}: {', '.join(stale)}; "
                     f"spusť compose_role --apply")
    if pending:
        lines.append("Upozornění: " + upgrade_mod.unfinished_line(pending))
    if getattr(args, "work_copy", None) is not None and not args.apply and not unchanged:
        lines.append("S --apply proběhne přechod v pracovní kopii (--work-copy) a zápis zpět bez mazání.")
    lines += [f"Upozornění: {w}" for w in warnings]
    if resumed:
        lines.insert(0, resumed)
    code = EXIT_OK if (after is None and not after_err) or after_code == EXIT_OK else 1
    return code, payload, "\n".join(lines)


def _after_text(after: dict) -> str:
    """Textový souhrn výsledku --after-only z podprocesu (JSON)."""
    lines = [f"Kroky po aktualizaci (core {after.get('version')}):"]
    for s in after.get("steps") or []:
        lines.append(f"  {s['step']}: {'v pořádku' if s['ok'] else 'selhal: ' + s['message']}")
        lines += [f"    {d}" for d in s.get("details") or []]
    if not after.get("steps"):
        lines.append("  žádné automatické kroky")
    lines += [f"  {x}" for x in upgrade_mod.check_text(after.get("checks") or {})]
    if after.get("tasks"):
        lines.append(f"Ruční úkoly do queue.md: {', '.join(after['tasks'])}")
    if after.get("tasks_existing"):
        lines.append(f"Ruční úkoly už ve frontě: {', '.join(after['tasks_existing'])}")
    lines += upgrade_mod.roles_lines(after.get("roles"))
    crs =(after.get("upgrade") or {}).get("crs") or []
    if crs:
        lines.append("CR k ověření v instanci (in_pilot): " + ", ".join(crs))
    if after.get("report"):
        lines.append(f"Report: {after['report']}")
    if after.get("remaining"):
        lines.append(f"Chyba: krok {after['remaining'][0]} selhal; zbývá {', '.join(after['remaining'])}. "
                     f"_core/ zůstává nový; po opravě doběhne update_core --after-only --apply")
    return "\n".join(lines)
