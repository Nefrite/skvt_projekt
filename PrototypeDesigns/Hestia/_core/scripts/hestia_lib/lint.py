"""Příkaz lint: G6, G7 (zadání 13 kap. 3 a 10.7, 04 kap. 6, 10 kap. 9).

- bez argumentů: soubory změněné podle gitu (poznámky vaultu i kód s hlavičkami); mimo git celý vault
  s upozorněním,
- s argumenty: jen zadané soubory (poznámky vaultu nebo soubory kódu),
- `--all`: celý vault a hlavičky všech souborů v `code_roots`,
- `--draft <soubor|->` s `--as <cesta>`: navrhovaná poznámka (mimo vault nebo stdin) zkontrolovaná stejným
  kódem jako poznámka na cílové cestě, včetně odkazů vůči vaultu (Knihovník, 13 kap. 10.10).
G5 (upozornění): změněné tělo dokumentu s `validity: superseded`/`archived` proti `doc_index` (zadání 0.29.1,
CR-042).
Soubory `Maintenance/taxonomy_local/*.yaml` (zadané nebo s `--all`) ověří tvarem a sloučením s core stejným
načtením jako ostatní příkazy; chyba se souborem a klíčem jako nález G7. Když se taxonomie nenačte, `lint`
se zadaným souborem taxonomy_local/ nebo s `--all` vypíše jen tento nález, kód 1 (ostatní kontroly bez taxonomie
nejdou); bez nich zůstává chyba konfigurace, kód 2 (zadání 0.29.1, CR-043).
Nic nezapisuje; report na stdout. Návratový kód 1 při nálezech úrovně chyba.
Glosář se starším záhlavím *Pojmy projektu* = varování bez kódu nálezu (zadání 0.14.1; u --json na stderr).
"""
from __future__ import annotations

import sys
from pathlib import Path

from . import gitinfo, glossary
from . import taxonomy as taxonomy_mod
from .errors import EXIT_FINDINGS, EXIT_OK, ConfigError, UsageError
from .findings import Finding, has_errors, sort_findings, to_text
from .fileio import read_text, to_posix
from .frontmatter import FrontmatterError, parse
from .validate import run_checks
from .vault import LINT_EXCLUDE_PREFIXES, Note, Vault


def _abs(f: str | Path) -> Path:
    p = Path(f)
    return (p if p.is_absolute() else Path.cwd() / p).resolve()


TAXONOMY_LOCAL = "Maintenance/taxonomy_local"
# soubory, které core v taxonomy_local/ čte (taxonomie, lokální seznamy, manifest assetů 13 kap. 10.18)
KNOWN_LOCAL = (set(taxonomy_mod.KEYED_FILES) | {"enums.yaml"} | taxonomy_mod.LOCAL_ONLY
               | {"asset_sources.yaml"}) - taxonomy_mod.CORE_ONLY


def is_taxonomy_local(root: Path, p: Path) -> bool:
    try:
        rel = to_posix(Path(p).resolve().relative_to(Path(root).resolve()))
    except ValueError:
        return False
    return rel.startswith(TAXONOMY_LOCAL + "/") and rel.lower().endswith((".yaml", ".yml"))


def taxonomy_findings(root: Path, core_root: Path, files: list[Path] | None = None,
                      project_root: Path | None = None) -> list[Finding]:
    """G7 nad `taxonomy_local/*.yaml` (zadání 0.29.1, CR-043): YAML a tvar každého souboru, pak sloučení s core
    stejným načtením jako ostatní příkazy (`taxonomy.load`; zastaví se na první chybě). `files=None` = všechny."""
    root = Path(root).resolve()
    local = root / TAXONOMY_LOCAL
    base = Path(project_root).resolve() if project_root is not None else root.parent

    def shown(path: Path) -> str:                  # cesta od kořene projektu jako u ostatních nálezů (01 kap. 11)
        try:
            return "/" + to_posix(Path(path).resolve().relative_to(base))
        except ValueError:
            return to_posix(path)
    if files is None:
        files = sorted(x for x in local.glob("*.y*ml") if x.is_file()) if local.is_dir() else []
    out: list[Finding] = []
    rels = {}
    for f in files:
        rel = shown(Path(f))
        name = Path(f).name
        rels[name] = rel
        if not Path(f).is_file():
            out.append(Finding("G7", "error", name, rel, "soubor nenalezen"))
            continue
        try:
            data = taxonomy_mod.load_yaml(Path(f))
        except ConfigError as exc:
            out.append(Finding("G7", "error", name, rel, str(exc).replace(str(Path(f)), f"{TAXONOMY_LOCAL}/{name}")))
            continue
        if name not in KNOWN_LOCAL:
            out.append(Finding("G7", "warning", name, rel,
                               "core tento soubor nečte (" + ("instance ho nerozšiřuje" if name in taxonomy_mod.CORE_ONLY
                                                              else "neznámé jméno") + "; známé: "
                               + ", ".join(sorted(KNOWN_LOCAL)) + ")"))
        elif name in taxonomy_mod.KEYED_FILES or name == "enums.yaml":
            if not isinstance(data, dict) or not isinstance(data.get("items"), list):
                out.append(Finding("G7", "error", name, rel, "očekávám mapu s klíčem items (seznam)"))
    if any(f.severity == "error" for f in out):
        return out
    try:
        taxonomy_mod.load(core_root / "taxonomy", local)
    except ConfigError as exc:
        msg = str(exc).replace(str(local) + "\\", TAXONOMY_LOCAL + "/").replace(str(local) + "/", TAXONOMY_LOCAL + "/")
        name = next((n for n in sorted(KNOWN_LOCAL | set(rels), key=len, reverse=True) if n in msg), None)
        if name is not None and (name in rels or not rels or files is None):
            rel = rels.get(name, shown(local / name))
            out.append(Finding("G7", "error", name, rel, f"sloučení s core: {msg}"))
        else:                                   # chyba v jiném lokálním souboru, než který je zadaný
            out.append(Finding("G7", "error", "taxonomy_local", shown(local),
                               f"taxonomie se nenačte (jiný soubor): {msg}"))
    return out


def run_without_taxonomy(args, root: Path, core_root: Path, exc: ConfigError) -> tuple[int, list, str]:
    """`lint`, když se vault nenačte kvůli taxonomii: vypíše nález se souborem a klíčem (zadání 0.29.1, CR-043).
    Jiná chyba konfigurace (config.yaml) se vyhodí dál."""
    explicit = [_abs(f) for f in getattr(args, "files", None) or [] if is_taxonomy_local(root, _abs(f))]
    if not explicit and not getattr(args, "all", False):
        raise exc                               # lint bez souborů taxonomie: chyba konfigurace, kód 2 jako dřív
    findings = taxonomy_findings(root, core_root, None)
    if not findings or not has_errors(findings):
        raise exc
    findings = sort_findings(findings)
    text = ("Taxonomie se nenačetla; ostatní kontroly lint bez ní neproběhly.\n" + to_text(findings))
    return EXIT_FINDINGS, [f.as_dict() for f in findings], text


def split_targets(vault: Vault, paths: list[Path], strict: bool = True):
    """Rozdělí cesty na poznámky vaultu a soubory kódu (mimo vault)."""
    notes, code = [], []
    for p in paths:
        try:
            rel = to_posix(p.relative_to(vault.root))
        except ValueError:
            if p.is_file():
                code.append(p)
            elif strict:
                raise UsageError(f"Soubor nenalezen: {p}")
            continue
        if rel in vault.notes:
            if not rel.startswith(LINT_EXCLUDE_PREFIXES):
                notes.append(vault.notes[rel])
        elif strict:
            raise UsageError(f"Poznámka nenalezena: {p}")
    return notes, code


def select_notes(vault: Vault, files: list[str]):
    """Zpětná kompatibilita (fáze 1): jen poznámky vaultu."""
    notes, code = split_targets(vault, [_abs(f) for f in files])
    if code:
        raise UsageError(f"Soubor není ve vaultu: {code[0]}")
    return notes


def header_findings(vault: Vault, code: list[Path]) -> list[Finding]:
    if not code:
        return []
    from .asset_index import IndexResult, Indexer
    ix = Indexer(vault)
    res = IndexResult()
    for p in code:
        ix.entry(p, res)
    return res.findings


def lint(vault: Vault, files: list[str] | None = None, code: list[Path] | None = None):
    """G6 + G7. files=None a code=None = celý vault (bez hlaviček kódu)."""
    if files is None and code is None:
        return sort_findings(run_checks(vault, None))
    notes, more_code = split_targets(vault, [_abs(f) for f in files or []])
    out = run_checks(vault, notes) if notes else []
    return sort_findings(out + header_findings(vault, (code or []) + more_code))


def all_code(vault: Vault) -> list[Path]:
    from .asset_index import Indexer
    files, _gen, _w = Indexer(vault).candidates()
    return files


def draft_note(vault: Vault, text: str, rel: str) -> Note:
    """Vloží koncept do načteného vaultu (jen v paměti) na cílovou cestu, aby šel zkontrolovat jako poznámka."""
    rel = rel.replace("\\", "/").strip().lstrip("/")
    if not rel.lower().endswith(".md"):
        rel += ".md"
    if rel.startswith(LINT_EXCLUDE_PREFIXES) or rel.startswith("../"):
        raise UsageError(f"--as {rel}: cesta mimo kontrolovanou část vaultu")
    path = vault.root / rel
    try:
        fm, sp = parse(text)
        note = Note(path, rel, path.stem, text, fm, sp)
    except FrontmatterError as exc:
        note = Note(path, rel, path.stem, text, None, None, str(exc))
    if rel not in vault.notes:
        vault.files.append(rel)
        vault._by_rel[rel.lower()] = rel
        vault._by_name.setdefault(path.name.lower(), []).append(rel)
        vault._by_name.setdefault(path.stem.lower(), []).append(rel)
    vault.notes[rel] = note
    return note


def run_draft(args, vault: Vault) -> tuple[int, list, str]:
    if args.files or getattr(args, "all", False):
        raise UsageError("--draft nejde kombinovat se soubory ani s --all")
    if args.draft == "-":
        if not args.as_path:
            raise UsageError("--draft - (stdin) potřebuje --as <cílová cesta ve vaultu>")
        text = sys.stdin.buffer.read().decode("utf-8-sig")      # UTF-8 nezávisle na kódování konzole
        text = text.replace("\r\n", "\n")
    else:
        src = _abs(args.draft)
        if not src.is_file():
            raise UsageError(f"Koncept nenalezen: {src}")
        text = read_text(src)
        if not args.as_path:
            try:
                args.as_path = to_posix(src.relative_to(vault.root))
            except ValueError:
                raise UsageError("--draft mimo vault potřebuje --as <cílová cesta ve vaultu>")
    note = draft_note(vault, text, args.as_path)
    findings = sort_findings(run_checks(vault, [note]))
    text = f"Koncept {note.rel} (nic se nezapisuje):\n" + to_text(findings)
    return (EXIT_FINDINGS if has_errors(findings) else EXIT_OK), [f.as_dict() for f in findings], text


def glossary_warning(vault: Vault, notes: list[Note] | None) -> str | None:
    """Varování ke glosáři, je-li v rozsahu (notes=None = celý vault)."""
    if notes is not None and glossary.GLOSSARY_REL not in {n.rel for n in notes}:
        return None
    return glossary.read(vault)[1]


def run(args, vault: Vault) -> tuple[int, list, str]:
    if getattr(args, "draft", None):
        return run_draft(args, vault)
    notes_text = []
    scope_notes: list[Note] | None = None
    from .vault import CORE_ROOT
    tax_files = [_abs(f) for f in args.files or [] if is_taxonomy_local(vault.root, _abs(f))]
    if getattr(args, "all", False):
        findings = sort_findings(run_checks(vault, None) + header_findings(vault, all_code(vault))
                                 + taxonomy_findings(vault.root, CORE_ROOT, None, vault.project_root))
        scope = "celý vault, hlavičky kódu a taxonomy_local/"
    elif args.files:
        rest = [f for f in args.files if _abs(f) not in tax_files]
        findings = sort_findings((lint(vault, rest) if rest else [])
                                 + (taxonomy_findings(vault.root, CORE_ROOT, tax_files, vault.project_root)
                                    if tax_files else []))
        scope_notes = split_targets(vault, [_abs(f) for f in rest], strict=False)[0]
        scope = f"{len(args.files)} zadaných souborů" + (
            " (" + ", ".join(to_posix(f.relative_to(vault.root)) for f in tax_files) + ")" if tax_files else "")
    else:
        changed = gitinfo.changed_files(vault.project_root)
        if changed is None:
            notes_text.append("Upozornění: projekt není v gitu, kontroluji celý vault.")
            findings = lint(vault)
            scope = "celý vault"
        else:
            notes, code = split_targets(vault, changed, strict=False)
            scope_notes = notes
            code_set = set(all_code(vault)) if code else set()
            code = [c for c in code if c in code_set]
            findings = sort_findings((run_checks(vault, notes) if notes else []) + header_findings(vault, code))
            scope = f"změněné soubory podle gitu: {len(notes)} poznámek, {len(code)} souborů kódu"
    from .doc_index import replaced_body_changes          # G5 nahrazený dokument (zadání 0.29.1, CR-042)
    g5_notes = list(vault.notes.values()) if scope_notes is None else scope_notes
    findings = sort_findings(findings + replaced_body_changes(
        vault, [n for n in g5_notes if not n.rel.startswith(LINT_EXCLUDE_PREFIXES)]))
    text = to_text(findings)
    gw = glossary_warning(vault, scope_notes)
    if gw:
        notes_text.append(f"Upozornění: {gw}")
        if getattr(args, "json", False):
            print(f"hestia: upozornění: {gw}", file=sys.stderr)
    if vault.config.warnings:
        notes_text = [f"Konfigurace: {w}" for w in vault.config.warnings] + notes_text
    if not getattr(args, "quiet", False):
        notes_text.append(f"Rozsah: {scope}.")
    text = "\n".join(notes_text + [text])
    code = EXIT_FINDINGS if has_errors(findings) else EXIT_OK
    return code, [f.as_dict() for f in findings], text
