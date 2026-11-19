"""Hestia core library (zadání 13). Python >= 3.11, stdlib + PyYAML; žádný import unreal."""
from __future__ import annotations

from pathlib import Path

# hestia_lib -> scripts -> kořen core (v HearthLore hestia/, v prototypu Hestia/_core/)
CORE_ROOT = Path(__file__).resolve().parents[2]


def core_version() -> str:
    try:
        return (CORE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return "0.0.0"
