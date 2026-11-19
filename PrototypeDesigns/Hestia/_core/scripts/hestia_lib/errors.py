"""Výjimky a návratové kódy (zadání 13, kap. 3)."""
from __future__ import annotations

EXIT_OK = 0
EXIT_FINDINGS = 1      # nálezy úrovně chyba, odmítnutý zápis
EXIT_USAGE = 2         # chybné použití nebo konfigurace
EXIT_UNEXPECTED = 3


class HestiaError(Exception):
    exit_code = EXIT_UNEXPECTED


class UsageError(HestiaError):
    """Chybné použití příkazu."""
    exit_code = EXIT_USAGE


class ConfigError(HestiaError):
    """Chybná konfigurace nebo taxonomie."""
    exit_code = EXIT_USAGE


class WriteConflict(HestiaError):
    """Soubor se od načtení změnil; zápis odmítnut (file_safety)."""
    exit_code = EXIT_FINDINGS
