"""Git jen pro čtení (zadání 13 kap. 8): log, diff --name-only, status --porcelain, tag --list, archive.

Skripty nikdy necommitují ani nemění index. Není-li projekt v gitu nebo git chybí, vrací None
a volající (G11, lint bez argumentů) to ohlásí jako upozornění.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def _git(cwd: Path, *args: str, stdin: str | None = None) -> subprocess.CompletedProcess | None:
    if shutil.which("git") is None:
        return None
    try:
        return subprocess.run(["git", "-c", "core.quotepath=off", *args], cwd=str(cwd), input=stdin,
                              capture_output=True, text=True, encoding="utf-8", timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None


def toplevel(path: Path) -> Path | None:
    p = Path(path)
    r = _git(p if p.is_dir() else p.parent, "rev-parse", "--show-toplevel")
    if r is None or r.returncode != 0 or not r.stdout.strip():
        return None
    return Path(r.stdout.strip()).resolve()


def head(path: Path) -> str | None:
    r = _git(Path(path), "rev-parse", "HEAD")
    if r is None or r.returncode != 0:
        return None
    return r.stdout.strip() or None


def _under(paths: list[Path], root: Path) -> list[Path]:
    root = Path(root).resolve()
    return [p for p in paths if p == root or root in p.parents]


def changed_files(root: Path, since: str | None = None) -> list[Path] | None:
    """Soubory pod `root` změněné od commitu `since` (commity) a neodevzdané změny v pracovním stromu.

    None = projekt není v gitu (nebo git chybí). Vrací absolutní cesty existujících souborů."""
    top = toplevel(root)
    if top is None:
        return None
    out: list[Path] = []
    if since:
        r = _git(top, "diff", "--name-only", f"{since}..HEAD")
        if r is not None and r.returncode == 0:
            out += [top / line for line in r.stdout.splitlines() if line.strip()]
    r = _git(top, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    if r is not None and r.returncode == 0:
        parts = r.stdout.split("\0")
        i = 0
        while i < len(parts):
            entry = parts[i]
            i += 1
            if len(entry) < 4:
                continue
            xy, path = entry[:2], entry[3:]
            if "R" in xy or "C" in xy:
                i += 1                      # původní jméno přejmenování
            out.append(top / path)
    seen, res = set(), []
    for p in out:
        p = p.resolve()
        if p in seen or not p.is_file():
            continue
        seen.add(p)
        res.append(p)
    return sorted(_under(res, root))


def ignored(root: Path, paths: list[Path]) -> set[Path]:
    """Které z cest git ignoruje podle .gitignore (prázdná množina mimo git)."""
    top = toplevel(root)
    if top is None or not paths:
        return set()
    r = _git(top, "check-ignore", "--stdin", stdin="\n".join(str(p) for p in paths) + "\n")
    if r is None or r.returncode not in (0, 1):
        return set()
    return {Path(line).resolve() if Path(line).is_absolute() else (top / line).resolve()
            for line in r.stdout.splitlines() if line.strip()}


def added_lines(path: Path) -> list[str] | None:
    """Řádky přidané v souboru proti HEAD (neodevzdané změny); celý obsah u nového souboru."""
    top = toplevel(path)
    if top is None:
        return None
    r = _git(top, "diff", "HEAD", "--unified=0", "--", str(path))
    if r is None or r.returncode != 0:
        return None
    if not r.stdout.strip():
        st = _git(top, "status", "--porcelain=v1", "--", str(path))
        if st is not None and st.stdout.startswith("??"):
            try:
                return Path(path).read_text(encoding="utf-8").splitlines()
            except OSError:
                return []
        return []
    return [line[1:] for line in r.stdout.splitlines() if line.startswith("+") and not line.startswith("+++")]


def first_seen(path: Path, ids: list[str]) -> dict[str, str] | None:
    """Datum commitu (RRRR-MM-DD), ve kterém se v souboru poprvé objevil řádek tabulky `| <id> |` (úkol ve frontě,
    13 kap. 10.17); jeden průchod historií souboru. None mimo git; ID mimo historii (necommitnuté) chybí."""
    top = toplevel(path)
    if top is None or not ids:
        return None if top is None else {}
    r = _git(top, "log", "--reverse", "--format=@@commit %as", "--unified=0", "-p", "--", str(path))
    if r is None or r.returncode != 0:
        return None
    wanted, out, day = set(ids), {}, None
    for line in r.stdout.splitlines():
        if line.startswith("@@commit "):
            day = line[len("@@commit "):].strip()
        elif line.startswith("+") and not line.startswith("+++") and day:
            cells = line[1:].strip().strip("|").split("|")
            rid = cells[0].strip() if cells else ""
            if rid in wanted and rid not in out:
                out[rid] = day
    return out


def head_text(path: Path) -> str | None:
    """Obsah souboru v HEAD (None mimo git nebo u nového souboru)."""
    top = toplevel(path)
    if top is None:
        return None
    try:
        rel = Path(path).resolve().relative_to(top).as_posix()
    except ValueError:
        return None
    r = _git(top, "show", f"HEAD:{rel}")
    if r is None or r.returncode != 0:
        return None
    return r.stdout


def tags(repo: Path, pattern: str = "v*") -> list[str] | None:
    """Značky repozitáře podle vzoru (update_core --tag/--latest, 13 kap. 10.6); None mimo git."""
    r = _git(Path(repo), "tag", "--list", pattern)
    if r is None or r.returncode != 0:
        return None
    return [t.strip() for t in r.stdout.splitlines() if t.strip()]


def archive(repo: Path, ref: str, path: str) -> bytes | None:
    """`git archive --format=tar <ref> <path>` jako bajty (jen čtení); None při chybě."""
    if shutil.which("git") is None:
        return None
    try:
        r = subprocess.run(["git", "archive", "--format=tar", ref, path], cwd=str(repo),
                           capture_output=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None
