"""Sada změn jednoho běhu příkazu: dry-run diff a bezpečný zápis (zadání 13 kap. 3, modul file_safety).

- Dry-run: unified diff u upravených souborů, souhrn u nových a přesunutých; nic nezapisuje.
- `--apply`: nejdřív přesuny (bez přepsání cíle), pak zápisy; před každým zápisem ověří hash obsahu
  z doby načtení (jinak WriteConflict), zapisuje atomicky, nic nemaže.
"""
from __future__ import annotations

import difflib
import os
from dataclasses import dataclass, field
from pathlib import Path

from .errors import WriteConflict
from .fileio import atomic_write, file_hash, read_text, to_posix


@dataclass
class Edit:
    path: Path                  # cílová cesta (po přesunech)
    old: str | None             # obsah při načtení (None = nový soubor)
    new: str
    old_hash: str | None


@dataclass
class ChangeSet:
    display_root: Path                                   # vůči čemu se cesty vypisují (kořen projektu)
    edits: dict[Path, Edit] = field(default_factory=dict)
    moves: list[tuple[Path, Path, str]] = field(default_factory=list)   # (zdroj, cíl, hash zdroje)
    _moved_to: dict[Path, Path] = field(default_factory=dict)          # cíl -> zdroj

    # ------------------------------------------------------------ čtení se zohledněním plánu
    def current(self, path: Path) -> str | None:
        path = Path(path).resolve()
        if path in self.edits:
            return self.edits[path].new
        src = self._moved_to.get(path, path)
        return read_text(src) if src.is_file() else None

    def exists(self, path: Path) -> bool:
        path = Path(path).resolve()
        if path in self.edits or path in self._moved_to:
            return True
        if any(src == path for src, _d, _h in self.moves):
            return False
        return path.is_file()

    # ------------------------------------------------------------ plánování
    def write(self, path: Path, new: str) -> bool:
        """Naplánuje obsah souboru; False, když se nic nemění."""
        path = Path(path).resolve()
        if path in self.edits:
            e = self.edits[path]
            e.new = new
            if e.old == new:
                del self.edits[path]
                return False
            return True
        src = self._moved_to.get(path, path)
        old = read_text(src) if src.is_file() else None
        if old == new:
            return False
        self.edits[path] = Edit(path, old, new, file_hash(src) if old is not None else None)
        return True

    def move(self, src: Path, dst: Path) -> None:
        src, dst = Path(src).resolve(), Path(dst).resolve()
        if self.exists(dst):
            raise WriteConflict(f"Cíl přesunu už existuje, nepřepisuji: {to_posix(dst)}")
        self.moves.append((src, dst, file_hash(src)))
        self._moved_to[dst] = src
        if src in self.edits:                 # naplánovaná úprava jde se souborem (zapíše se po přesunu)
            e = self.edits.pop(src)
            self.edits[dst] = Edit(dst, e.old, e.new, e.old_hash)

    @property
    def empty(self) -> bool:
        return not self.edits and not self.moves

    # ------------------------------------------------------------ výstup
    def rel(self, path: Path) -> str:
        try:
            return "/" + to_posix(Path(path).resolve().relative_to(Path(self.display_root).resolve()))
        except ValueError:
            return to_posix(path)

    def summary(self) -> list[dict]:
        out = [{"action": "move", "from": self.rel(s), "to": self.rel(d)} for s, d, _h in self.moves]
        for p, e in sorted(self.edits.items()):
            out.append({"action": "create" if e.old is None else "modify", "path": self.rel(p)})
        return out

    def diff(self, full_new: bool = False) -> str:
        chunks = [f"přesun: {self.rel(s)} -> {self.rel(d)}\n" for s, d, _h in self.moves]
        for p, e in sorted(self.edits.items()):
            name = self.rel(p)
            if e.old is None and not full_new:
                chunks.append(f"nový soubor: {name} ({len(e.new.splitlines())} řádků)\n")
                continue
            old = (e.old or "").replace("\r\n", "\n").splitlines(keepends=True)
            new = e.new.replace("\r\n", "\n").splitlines(keepends=True)
            chunks.append("".join(difflib.unified_diff(old, new, f"a{name}", f"b{name}")))
        return "".join(chunks)

    # ------------------------------------------------------------ zápis
    def apply(self) -> None:
        for src, dst, h in self.moves:
            if not src.is_file() or file_hash(src) != h:
                raise WriteConflict(f"Soubor se od načtení změnil, přesun odmítnut: {to_posix(src)}")
            if dst.exists():
                raise WriteConflict(f"Cíl přesunu už existuje, nepřepisuji: {to_posix(dst)}")
            dst.parent.mkdir(parents=True, exist_ok=True)
            os.rename(src, dst)
        for p, e in sorted(self.edits.items()):
            atomic_write(p, e.new, expected_hash=e.old_hash)
