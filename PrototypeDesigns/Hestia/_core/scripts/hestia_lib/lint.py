"""Příkaz lint: G6, G7 (zadání 13 kap. 3 a 10.7, 04 kap. 6, 10 kap. 9).

- bez argumentů: soubory změněné podle gitu (poznámky vaultu i kód s hlavičkami); mimo git celý vault
  s upozorněním,
- s argumenty: jen zadané soubory (poznámky vaultu nebo soubory kódu),
- `--all`: celý vault a hlavičky všech souborů v `code_roots`.
Nic nezapisuje; report na stdout. Návratový kód 1 při nálezech úrovně chyba.
"""
from __future__ import annotations

from pathlib import Path

from . import gitinfo
from .errors import EXIT_FINDINGS, EXIT_OK, UsageError
from .findings import Finding, has_errors, sort_findings, to_text
from .fileio import to_posix
from .validate import run_checks
from .vault import LINT_EXCLUDE_PREFIXES, Vault


def _abs(f: str | Path) -> Path:
    p = Path(f)
    return (p if p.is_absolute() else Path.cwd() / p).resolve()


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


def run(args, vault: Vault) -> tuple[int, list, str]:
    notes_text = []
    if getattr(args, "all", False):
        findings = sort_findings(run_checks(vault, None) + header_findings(vault, all_code(vault)))
        scope = "celý vault a hlavičky kódu"
    elif args.files:
        findings = lint(vault, args.files)
        scope = f"{len(args.files)} zadaných souborů"
    else:
        changed = gitinfo.changed_files(vault.project_root)
        if changed is None:
            notes_text.append("Upozornění: projekt není v gitu, kontroluji celý vault.")
            findings = lint(vault)
            scope = "celý vault"
        else:
            notes, code = split_targets(vault, changed, strict=False)
            code_set = set(all_code(vault)) if code else set()
            code = [c for c in code if c in code_set]
            findings = sort_findings((run_checks(vault, notes) if notes else []) + header_findings(vault, code))
            scope = f"změněné soubory podle gitu: {len(notes)} poznámek, {len(code)} souborů kódu"
    text = to_text(findings)
    if vault.config.warnings:
        notes_text = [f"Konfigurace: {w}" for w in vault.config.warnings] + notes_text
    if not getattr(args, "quiet", False):
        notes_text.append(f"Rozsah: {scope}.")
    text = "\n".join(notes_text + [text])
    code = EXIT_FINDINGS if has_errors(findings) else EXIT_OK
    return code, [f.as_dict() for f in findings], text
