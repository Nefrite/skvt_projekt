"""Vault: nalezení, načtení poznámek, rozlišení wikilinků (zadání 13, kap. 3 a 6)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import CORE_ROOT
from . import config as config_mod
from . import taxonomy as taxonomy_mod
from .errors import UsageError
from .fileio import read_text, to_posix
from .frontmatter import FrontmatterError, Split, parse

VAULT_DIRNAME = "Hestia"
# Složky, které se vůbec neprocházejí.
SKIP_DIRS = {".obsidian", ".trash", ".git", "__pycache__"}
# Poznámky, které lint nekontroluje (core je jen ke čtení, kompiláty generované, koš).
# _core/ ověřují akceptační testy, lint ho nekontroluje (13 kap. 2).
LINT_EXCLUDE_PREFIXES = ("_core/", "_to_delete/", "Roles/_compiled/")


def find_vault(start: Path | None = None) -> Path:
    """Nejbližší `Hestia/` od pracovní složky nahoru."""
    p = Path(start or Path.cwd()).resolve()
    for cand in [p, *p.parents]:
        if cand.name == VAULT_DIRNAME and cand.is_dir():
            return cand
        if (cand / VAULT_DIRNAME).is_dir():
            return cand / VAULT_DIRNAME
    raise UsageError("Vault Hestia/ nenalezen; zadej --vault PATH")


@dataclass
class Note:
    path: Path                 # absolutní
    rel: str                   # relativně k vaultu, s /
    name: str                  # jméno bez .md
    text: str
    fm: dict | None
    split: Split | None
    fm_error: str | None = None

    @property
    def type(self):
        return (self.fm or {}).get("type")

    @property
    def body(self) -> str:
        return self.split.body if self.split else self.text


@dataclass
class Vault:
    root: Path
    project_root: Path
    taxonomy: taxonomy_mod.Taxonomy
    config: config_mod.Config
    files: list[str] = field(default_factory=list)              # všechny soubory, rel s /
    notes: dict[str, Note] = field(default_factory=dict)        # rel -> Note (jen .md)
    _by_name: dict[str, list[str]] = field(default_factory=dict)  # lower(jméno) -> [rel]
    _by_rel: dict[str, str] = field(default_factory=dict)         # lower(rel) -> rel

    # ------------------------------------------------------------ načtení
    @classmethod
    def load(cls, root: Path, core_root: Path = CORE_ROOT) -> "Vault":
        root = Path(root).resolve()
        if not root.is_dir():
            raise UsageError(f"Vault neexistuje: {root}")
        cfg = config_mod.load(root, core_root)
        tx = taxonomy_mod.load(core_root / "taxonomy", root / "Maintenance" / "taxonomy_local")
        project_root = (root / str(cfg.get("project_root") or "..")).resolve()
        v = cls(root=root, project_root=project_root, taxonomy=tx, config=cfg)
        v._scan()
        return v

    def _scan(self) -> None:
        for path in sorted(self._walk(self.root)):
            rel = to_posix(path.relative_to(self.root))
            self.files.append(rel)
            self._by_rel[rel.lower()] = rel
            fname = path.name.lower()
            self._by_name.setdefault(fname, []).append(rel)
            if path.suffix.lower() == ".md":
                stem = path.stem.lower()
                if stem != fname:
                    self._by_name.setdefault(stem, []).append(rel)
                self.notes[rel] = self._load_note(path, rel)

    @staticmethod
    def _walk(root: Path):
        stack = [root]
        while stack:
            d = stack.pop()
            try:
                entries = list(d.iterdir())
            except OSError:
                continue
            for e in entries:
                if e.is_dir():
                    if e.name not in SKIP_DIRS:
                        stack.append(e)
                elif e.is_file() and not e.name.startswith(".hestia_tmp_"):
                    yield e

    @staticmethod
    def _load_note(path: Path, rel: str) -> Note:
        text = read_text(path)
        try:
            fm, sp = parse(text)
            return Note(path, rel, path.stem, text, fm, sp)
        except FrontmatterError as exc:
            return Note(path, rel, path.stem, text, None, None, str(exc))

    # ------------------------------------------------------------ dotazy
    @property
    def game_layer(self) -> bool:
        """False = instance bez herní vrstvy (01 kap. 2, 13 kap. 4)."""
        return bool(self.config.get("game_layer", True))

    def lint_notes(self) -> list[Note]:
        return [n for rel, n in sorted(self.notes.items()) if not rel.startswith(LINT_EXCLUDE_PREFIXES)]

    def resolve(self, target: str) -> tuple[str | None, str]:
        """Rozliší cíl wikilinku. Vrací (rel nebo None, stav: ok / missing / ambiguous)."""
        t = target.strip().replace("\\", "/").lstrip("/")
        if not t:
            return None, "ok"
        if "/" in t:
            for cand in (t, t + ".md"):
                hit = self._by_rel.get(cand.lower())
                if hit:
                    return hit, "ok"
            # Obsidian přijme i koncovou část cesty, je-li jednoznačná
            matches = [r for r in self.files if r.lower().endswith("/" + t.lower()) or
                       r.lower().endswith("/" + t.lower() + ".md")]
            if len(matches) == 1:
                return matches[0], "ok"
            return None, "ambiguous" if matches else "missing"
        hits = self._by_name.get(t.lower(), [])
        if not hits:
            return None, "missing"
        exact_file = [h for h in hits if h.rsplit("/", 1)[-1].lower() == t.lower()]
        cand = exact_file or hits
        if len(cand) > 1:
            return None, "ambiguous"
        return cand[0], "ok"

    def note_by_name(self, name: str) -> Note | None:
        rel, status = self.resolve(name)
        return self.notes.get(rel) if status == "ok" and rel else None

    def project_rel(self, path: Path) -> str:
        """Cesta od kořene projektu, začíná / (01 kap. 11)."""
        try:
            return "/" + to_posix(Path(path).resolve().relative_to(self.project_root))
        except ValueError:
            return to_posix(path)
