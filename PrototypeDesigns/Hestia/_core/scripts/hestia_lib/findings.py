"""Nálezy G1–G13 a jejich výstup (zadání 04 kap. 4, 13 kap. 7).

JSON: [{code, severity, target, file, message}]; text pro člověka česky.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass

SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}
SEVERITY_CZ = {"error": "chyba", "warning": "upozornění", "info": "informace"}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    target: str
    file: str
    message: str

    def as_dict(self) -> dict:
        return asdict(self)


def sort_findings(items: list[Finding]) -> list[Finding]:
    return sorted(items, key=lambda f: (SEVERITY_ORDER.get(f.severity, 9), f.file, f.code, f.message))


def to_json(items: list[Finding]) -> str:
    return json.dumps([f.as_dict() for f in sort_findings(items)], ensure_ascii=False, indent=2)


def to_text(items: list[Finding]) -> str:
    if not items:
        return "Bez nálezů."
    lines = []
    for f in sort_findings(items):
        lines.append(f"{f.code} [{SEVERITY_CZ.get(f.severity, f.severity)}] {f.file}: {f.message}")
    counts = {s: sum(1 for f in items if f.severity == s) for s in SEVERITY_ORDER}
    lines.append(f"Celkem: chyby {counts['error']}, upozornění {counts['warning']}, informace {counts['info']}.")
    return "\n".join(lines)


def has_errors(items: list[Finding]) -> bool:
    return any(f.severity == "error" for f in items)
