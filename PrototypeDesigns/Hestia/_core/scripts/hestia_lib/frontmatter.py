"""Frontmatter: čtení přes PyYAML, zápis řádkově (zadání 13, kap. 6).

Frontmatter je YAML mezi prvními dvěma řádky `---`. Úprava klíče nemění pořadí klíčů,
komentáře (`# orchestrace`, `# hra`), uvozovky ani ostatní řádky; konce řádků se zachovají.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from dataclasses import dataclass

import yaml

from .fileio import detect_newline

_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_\-]*)\s*:(.*)$")
_PLAIN_SAFE_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_\-./ ]*$")
_YAML_SPECIAL = {"", "null", "~", "true", "false", "yes", "no", "on", "off", "y", "n"}


class FrontmatterError(ValueError):
    pass


@dataclass
class Split:
    has_frontmatter: bool
    fm_text: str          # obsah mezi oddělovači (bez nich)
    body: str             # vše za uzavíracím ---
    fm_start: int         # index prvního řádku obsahu frontmatteru (v seznamu řádků s konci)
    fm_end: int           # index řádku uzavíracího ---
    body_line: int        # číslo řádku (1-based), kde začíná tělo


def _lines(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def _is_delim(line: str) -> bool:
    return line.rstrip("\r\n").rstrip() == "---"


def split(text: str) -> Split:
    lines = _lines(text)
    start = 0
    if lines and lines[0].startswith("﻿"):
        lines[0] = lines[0][1:]
    if not lines or not _is_delim(lines[0]):
        return Split(False, "", text, 0, 0, 1)
    for i in range(1, len(lines)):
        if _is_delim(lines[i]):
            fm_text = "".join(lines[1:i])
            body = "".join(lines[i + 1:])
            return Split(True, fm_text, body, 1, i, i + 2)
    return Split(False, "", text, start, 0, 1)


def parse(text: str) -> tuple[dict | None, Split]:
    """Vrátí (data, split). data=None bez frontmatteru. FrontmatterError při neplatném YAML."""
    sp = split(text)
    if not sp.has_frontmatter:
        return None, sp
    try:
        data = yaml.safe_load(sp.fm_text) if sp.fm_text.strip() else {}
    except yaml.YAMLError as exc:
        hint = ""
        if "{{core_version}}" in sp.fm_text:      # tpl_role: plugin Templates proměnnou nevyplní (zadání 0.17)
            hint = "; nevyplněné {{core_version}}: doplň verzi core z _core/VERSION (role_base)"
        raise FrontmatterError(f"neplatný YAML ve frontmatteru: {exc}".replace("\n", " ") + hint) from exc
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise FrontmatterError("frontmatter není mapa klíč: hodnota")
    return data, sp


# ---------------------------------------------------------------- formátování hodnot

def format_value(value) -> str:
    """Hodnota jako inline YAML (pro řádkový zápis). Wikilinky vždy v uvozovkách (01, kap. 11)."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (_dt.date, _dt.datetime)):
        return value.isoformat()
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(format_value(v) if v is not None else '""' for v in value) + "]"
    s = str(value)
    if (_PLAIN_SAFE_RE.match(s) and s.lower() not in _YAML_SPECIAL and not s.endswith(" ")
            and not re.fullmatch(r"[0-9.\-]+", s)):
        return s
    return json.dumps(s, ensure_ascii=False)


# ---------------------------------------------------------------- řádkové úpravy

def _find_comment(rest: str) -> int:
    """Index začátku komentáře `#` v hodnotě (mimo uvozovky), jinak -1."""
    quote = None
    for i, ch in enumerate(rest):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or rest[i - 1] in " \t"):
            return i
    return -1


def _key_block(lines: list[str], start: int, end: int, key: str) -> tuple[int, int] | None:
    """(první, za posledním) řádek bloku klíče `key` v rozsahu frontmatteru."""
    for i in range(start, end):
        m = _KEY_RE.match(lines[i].rstrip("\r\n"))
        if m and m.group(1) == key:
            j = i + 1
            while j < end:
                raw = lines[j].rstrip("\r\n")
                if raw.startswith((" ", "\t")) or raw.startswith("- ") or raw == "-":
                    j += 1
                    continue
                break
            return i, j
    return None


def _section_insert_index(lines: list[str], start: int, end: int, section: str) -> int:
    """Kam vložit nový klíč: orchestrace před `# hra`, hra (a ostatní) na konec frontmatteru."""
    if section == "orchestration":
        for i in range(start, end):
            if lines[i].strip().lower().startswith("# hra"):
                return i
    return end


def set_field(text: str, key: str, value, section: str = "game", keep_comment: bool = True) -> str:
    """Nastaví klíč frontmatteru na hodnotu (řádkově). Existující klíč nahradí na místě,
    chybějící vloží podle sekce. Ostatní řádky beze změny."""
    sp = split(text)
    if not sp.has_frontmatter:
        raise FrontmatterError("soubor nemá frontmatter")
    lines = _lines(text)
    bom = ""
    if lines and lines[0].startswith("﻿"):
        bom = "﻿"
        lines[0] = lines[0][1:]
    nl = detect_newline(text)
    rendered = format_value(value)
    block = _key_block(lines, sp.fm_start, sp.fm_end, key)
    if block:
        i, j = block
        raw = lines[i].rstrip("\r\n")
        line_nl = lines[i][len(raw):] or nl
        m = _KEY_RE.match(raw)
        rest = m.group(2)
        comment = ""
        if keep_comment:
            c = _find_comment(rest)
            if c >= 0:
                comment = rest[c:].rstrip()
                col = len(raw) - len(rest) + c
        new = f"{key}: {rendered}" if rendered != "" else f"{key}:"
        if comment:
            pad = col - len(new) if col > len(new) + 1 else 2
            new = new + " " * pad + comment
        lines[i:j] = [new + line_nl]
    else:
        idx = _section_insert_index(lines, sp.fm_start, sp.fm_end, section)
        new = (f"{key}: {rendered}" if rendered != "" else f"{key}:") + nl
        lines.insert(idx, new)
    return bom + "".join(lines)


def get_raw_keys(text: str) -> list[str]:
    """Pořadí klíčů nejvyšší úrovně ve frontmatteru (pro testy zachování pořadí)."""
    sp = split(text)
    if not sp.has_frontmatter:
        return []
    out = []
    for line in _lines(text)[sp.fm_start:sp.fm_end]:
        m = _KEY_RE.match(line.rstrip("\r\n"))
        if m:
            out.append(m.group(1))
    return out
