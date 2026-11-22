"""Čtení a bezpečný zápis souborů (zadání 13, kap. 1 a 3; modul file_safety).

- UTF-8, konce řádků se zachovávají (čte se s newline="").
- Zápis atomicky: dočasný soubor ve stejné složce + os.replace.
- Před přepsáním se ověří hash obsahu načteného dříve; při změně WriteConflict.
- Nic se nemaže.
"""
from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path

from .errors import WriteConflict


def read_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_newline(text: str) -> str:
    """Převládající konec řádku souboru; výchozí LF."""
    crlf = text.count("\r\n")
    lf = text.count("\n") - crlf
    return "\r\n" if crlf > lf else "\n"


def atomic_write(path: Path, data: str | bytes, expected_hash: str | None = None) -> None:
    """Zapíše soubor atomicky. expected_hash = sha256 obsahu při načtení (None = nový soubor)."""
    path = Path(path)
    if expected_hash is not None:
        if not path.exists() or file_hash(path) != expected_hash:
            raise WriteConflict(f"Soubor se od načtení změnil, zápis odmítnut: {path}")
    elif path.exists():
        raise WriteConflict(f"Soubor už existuje, zápis odmítnut: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = data.encode("utf-8") if isinstance(data, str) else data
    fd, tmp = tempfile.mkstemp(prefix=".hestia_tmp_", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(payload)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def to_posix(path: Path | str) -> str:
    return str(path).replace("\\", "/")


# Pracovní kopie vaultu (update_core --work-copy, 13 kap. 10.6): cesty v kopii se ve výstupech
# (cesty od kořene projektu, souhrny změn) ukazují jako cesty v originálu.
_ALIASES: list[tuple[Path, Path]] = []


def register_alias(copy_root: Path, origin_root: Path) -> None:
    pair = (Path(copy_root).resolve(), Path(origin_root).resolve())
    if pair not in _ALIASES:
        _ALIASES.append(pair)


def display_path(path: Path | str) -> Path:
    """Cesta v pracovní kopii převedená na cestu v originálu; jiná cesta beze změny."""
    p = Path(path)
    if not _ALIASES:
        return p
    rp = p.resolve()
    for copy_root, origin in _ALIASES:
        if rp == copy_root or copy_root in rp.parents:
            return origin / rp.relative_to(copy_root)
    return p

