"""Hlavička skriptu (zadání 10 kap. 5, 13 kap. 6).

První docstring (Python) nebo úvodní komentářový blok; řádky `klíč: hodnota`, seznamy v `[...]`,
komentář `# …` za hodnotou se ignoruje. Neznámé klíče se ignorují. Staré komentáře
`soubor.md kap. X` kdekoli v souboru se čtou jako `docs` (10 kap. 5). JSON data volitelně
nesou `"_hestia": {"entity": "..."}` (10 kap. 6).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

KEYS = ("hestia", "entities", "docs", "build_step", "domains", "role", "run")
LIST_KEYS = {"entities", "docs", "domains"}
TEXT_SUFFIXES = {".py", ".pyw", ".txt", ".ini", ".cfg", ".toml", ".js", ".ts", ".cs", ".cpp", ".h", ".hpp"}
MAX_BYTES = 1_000_000

_DOCSTRING_RE = re.compile(r'\A(?:[ \t]*(?:#[^\n]*)?\n)*[ \t]*[rRuUbB]?("""|\'\'\')(.*?)\1', re.DOTALL)
_KEY_RE = re.compile(r"^\s*([a-z_]+)\s*:\s*(.*?)\s*$")
_LEGACY_RE = re.compile(r"([A-Za-z0-9][A-Za-z0-9_\-]*)\.md\s+kap\.")


@dataclass
class Header:
    fields: dict = field(default_factory=dict)      # klíč -> str nebo list[str]
    legacy_docs: list = field(default_factory=list)

    def get(self, key: str, default=None):
        return self.fields.get(key, default)

    def list(self, key: str) -> list[str]:
        v = self.fields.get(key)
        if v is None:
            return []
        return v if isinstance(v, list) else [v]

    @property
    def empty(self) -> bool:
        return not self.fields and not self.legacy_docs


def _strip_comment(value: str) -> str:
    m = re.search(r"\s+#", value)
    return value[:m.start()].rstrip() if m else value


def _parse_value(key: str, raw: str):
    raw = _strip_comment(raw).strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [x.strip().strip("\"'") for x in raw[1:-1].split(",") if x.strip().strip("\"'")]
    raw = raw.strip("\"'")
    if key in LIST_KEYS:
        return [x.strip() for x in raw.split(",") if x.strip()] if raw else []
    return raw


def _comment_block(text: str) -> str:
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#!") or (not lines and not s):
            continue
        if s.startswith("#"):
            lines.append(s.lstrip("#").strip())
        elif s.startswith("//"):
            lines.append(s[2:].strip())
        else:
            break
    return "\n".join(lines)


def parse_header_text(text: str) -> Header:
    h = Header()
    m = _DOCSTRING_RE.match(text)
    block = m.group(2) if m else _comment_block(text)
    for line in block.splitlines():
        km = _KEY_RE.match(line)
        if km and km.group(1) in KEYS:
            h.fields[km.group(1)] = _parse_value(km.group(1), km.group(2))
    for name in _LEGACY_RE.findall(text):
        if name not in h.legacy_docs:
            h.legacy_docs.append(name)
    return h


def read_header(path: Path) -> Header:
    """Hlavička souboru; prázdná u souborů bez hlavičky, binárních a velkých."""
    path = Path(path)
    try:
        if path.stat().st_size > MAX_BYTES:
            return Header()
        if path.suffix.lower() == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            meta = data.get("_hestia") if isinstance(data, dict) else None
            h = Header()
            if isinstance(meta, dict):
                for k in KEYS:
                    if k in meta:
                        h.fields[k] = meta[k]
                if "entity" in meta and "hestia" not in h.fields:
                    h.fields["hestia"] = meta["entity"]
            return h
        if path.suffix.lower() not in TEXT_SUFFIXES:
            return Header()
        return parse_header_text(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return Header()
