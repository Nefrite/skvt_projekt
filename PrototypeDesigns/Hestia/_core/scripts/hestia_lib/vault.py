"""Vault: nalezení, načtení poznámek, rozlišení wikilinků (zadání 13, kap. 3 a 6)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import CORE_ROOT
from . import config as config_mod
from . import taxonomy as taxonomy_mod
from .errors import UsageError
from .fileio import display_path, read_text, register_alias, to_posix
from .frontmatter import FrontmatterError, Split, parse

VAULT_DIRNAME = "Hestia"
# Složky, které se vůbec neprocházejí.
SKIP_DIRS = {".obsidian", ".trash", ".git", "__pycache__"}
# Poznámky, které lint nekontroluje (core je jen ke čtení, kompiláty generované, koš).
# _core/ ověřují akceptační testy, lint ho nekontroluje (13 kap. 2).
LINT_EXCLUDE_PREFIXES = ("_core/", "_to_delete/", "Roles/_compiled/", "Maintenance/context/",
                         "Maintenance/import/",      # soubory výměny importu (13 kap. 10.12, zadání 0.16)
                         "Maintenance/outbox/sent/")  # odeslané CR a hlášení (13 kap. 10.20, zadání 0.28)


WORK_MARKER = "hestia_work.json"           # značka pracovní kopie vedle kopie vaultu (13 kap. 10.6)


def work_origin(root: Path) -> Path | None:
    """Originál vaultu, je-li `root` pracovní kopie (`update_core --work-copy`): značka `hestia_work.json`
    v nadřazené složce s `vault` = jméno složky kopie."""
    import json
    marker = Path(root).parent / WORK_MARKER
    if not marker.is_file():
        return None
    try:
        data = json.loads(read_text(marker))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("vault") != Path(root).name or not data.get("origin"):
        return None
    return Path(data["origin"]).resolve()


def find_vault(start: Path | None = None) -> Path:
    """Nejbližší `Hestia/` od pracovní složky nahoru."""
    p = Path(start or Path.cwd()).resolve()
    for cand in [p, *p.parents]:
        if cand.name == VAULT_DIRNAME and cand.is_dir():
            return cand
        if (cand / VAULT_DIRNAME).is_dir():
            return cand / VAULT_DIRNAME
    raise UsageError("Vault Hestia/ nenalezen; zadej --vault PATH")


class Note:
    """Poznámka vaultu. `text`, `fm`, `split` a `fm_error` se u líně načteného vaultu (`Vault.load(lazy=True)`,
    zadání 0.28, CR-033) čtou ze souboru až při prvním přístupu; jinak hned."""

    __slots__ = ("path", "rel", "name", "_text", "_fm", "_split", "_fm_error", "_loaded")

    def __init__(self, path: Path, rel: str, name: str, text: str | None = None, fm: dict | None = None,
                 split: Split | None = None, fm_error: str | None = None, lazy: bool = False):
        self.path, self.rel, self.name = path, rel, name      # path absolutní, rel s /, name bez .md
        self._text, self._fm, self._split, self._fm_error = text, fm, split, fm_error
        self._loaded = not lazy

    def _load(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        self._text = read_text(self.path)
        try:
            self._fm, self._split = parse(self._text)
        except FrontmatterError as exc:
            self._fm, self._split, self._fm_error = None, None, str(exc)

    @property
    def loaded(self) -> bool:
        return self._loaded

    @property
    def text(self) -> str:
        self._load()
        return self._text

    @property
    def fm(self) -> dict | None:
        self._load()
        return self._fm

    @property
    def split(self) -> Split | None:
        self._load()
        return self._split

    @property
    def fm_error(self) -> str | None:
        self._load()
        return self._fm_error

    @property
    def type(self):
        return (self.fm or {}).get("type")

    @property
    def body(self) -> str:
        return self.split.body if self.split else self.text

    def __repr__(self) -> str:
        return f"Note({self.rel!r})"


@dataclass
class Vault:
    root: Path
    project_root: Path
    taxonomy: taxonomy_mod.Taxonomy
    config: config_mod.Config
    origin: Path | None = None        # originál, je-li vault pracovní kopie (13 kap. 10.6, zadání 0.22)
    files: list[str] = field(default_factory=list)              # všechny soubory, rel s /
    notes: dict[str, Note] = field(default_factory=dict)        # rel -> Note (jen .md)
    _by_name: dict[str, list[str]] = field(default_factory=dict)  # lower(jméno) -> [rel]
    _by_rel: dict[str, str] = field(default_factory=dict)         # lower(rel) -> rel
    lazy: bool = False                # poznámky se čtou až při přístupu (zadání 0.28, CR-033)

    # ------------------------------------------------------------ načtení
    @classmethod
    def load(cls, root: Path, core_root: Path = CORE_ROOT, lazy: bool = False) -> "Vault":
        """Načte vault. `lazy=True`: projde jen složky a poznámky čte až při přístupu (section, find, task_close
        na připojené složce; zadání 0.28, CR-033)."""
        root = Path(root).resolve()
        if not root.is_dir():
            raise UsageError(f"Vault neexistuje: {root}")
        cfg = config_mod.load(root, core_root)
        tx = taxonomy_mod.load(core_root / "taxonomy", root / "Maintenance" / "taxonomy_local")
        origin = work_origin(root)
        if origin is not None:
            register_alias(root, origin)
        # project_root a další cesty z config.yaml jsou relativně k vaultu v projektu (u kopie k originálu)
        project_root = ((origin or root) / str(cfg.get("project_root") or "..")).resolve()
        v = cls(root=root, project_root=project_root, taxonomy=tx, config=cfg, origin=origin, lazy=lazy)
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
                self.notes[rel] = (Note(path, rel, path.stem, lazy=True) if self.lazy
                                   else self._load_note(path, rel))

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

    def refresh(self, paths) -> None:
        """Po zápisu: poznámky na `paths` (absolutní) se znovu načtou při příštím přístupu (zadání 0.28)."""
        for p in paths:
            try:
                rel = to_posix(Path(p).resolve().relative_to(self.root))
            except ValueError:
                continue
            if rel in self.notes:
                path = self.notes[rel].path
                self.notes[rel] = Note(path, rel, path.stem, lazy=True)

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

    @property
    def home(self) -> Path:
        """Umístění vaultu v projektu: originál u pracovní kopie, jinak `root`."""
        return self.origin or self.root

    def project_rel(self, path: Path) -> str:
        """Cesta od kořene projektu, začíná / (01 kap. 11)."""
        try:
            return "/" + to_posix(display_path(Path(path)).resolve().relative_to(self.project_root))
        except ValueError:
            return to_posix(path)
