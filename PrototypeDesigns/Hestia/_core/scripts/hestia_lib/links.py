"""Wikilinky a sekce v těle poznámky (zadání 13, kap. 6).

Podporováno: [[Name]], [[Name|alias]], [[path/Name]], [[Name#Nadpis]], [[#Nadpis]], vložení ![[file]].
Odkazy v blocích kódu, v inline kódu a v HTML komentářích se ignorují.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

WIKILINK_RE = re.compile(r"(!?)\[\[([^\[\]\n]+?)\]\]")
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


@dataclass(frozen=True)
class Link:
    raw: str          # celý text uvnitř [[ ]]
    target: str       # cesta/jméno bez #nadpisu a |aliasu ('' = odkaz do téhož souboru)
    embed: bool
    line: int         # 1-based, relativně k předanému textu


def parse_inner(inner: str) -> str:
    target = inner.split("|", 1)[0]
    if target.endswith("\\"):           # [[Name\|alias]] uvnitř tabulky
        target = target[:-1]
    target = target.split("#", 1)[0]
    return target.strip()


def _blank_keep_newlines(m: re.Match) -> str:
    return "".join("\n" if ch == "\n" else " " for ch in m.group(0))


def strip_non_content(text: str) -> list[str]:
    """Řádky textu s vymazanými komentáři, bloky kódu a inline kódem (čísla řádků zůstávají)."""
    text = _COMMENT_RE.sub(_blank_keep_newlines, text)
    out = []
    fence = None
    for line in text.split("\n"):
        m = _FENCE_RE.match(line)
        if fence:
            if m and m.group(1) == fence:
                fence = None
            out.append("")
            continue
        if m:
            fence = m.group(1)
            out.append("")
            continue
        out.append(_INLINE_CODE_RE.sub(lambda mm: " " * len(mm.group(0)), line))
    return out


def extract_links(text: str, line_offset: int = 0) -> list[Link]:
    links = []
    for no, line in enumerate(strip_non_content(text), start=1):
        for m in WIKILINK_RE.finditer(line):
            links.append(Link(m.group(2), parse_inner(m.group(2)), bool(m.group(1)), no + line_offset))
    return links


def links_in_value(value) -> list[str]:
    """Wikilinky v hodnotě frontmatteru (řetězec nebo seznam, rekurzivně)."""
    out: list[str] = []
    if isinstance(value, str):
        out.extend(parse_inner(m.group(2)) for m in WIKILINK_RE.finditer(value))
    elif isinstance(value, list):
        for v in value:
            out.extend(links_in_value(v))
    elif isinstance(value, dict):
        for v in value.values():
            out.extend(links_in_value(v))
    return out


def headings(text: str, level: int | None = None) -> list[tuple[int, str, int]]:
    """Nadpisy mimo bloky kódu: (úroveň, text, řádek)."""
    out = []
    for no, line in enumerate(strip_non_content(text), start=1):
        m = _HEADING_RE.match(line)
        if m and (level is None or len(m.group(1)) == level):
            out.append((len(m.group(1)), m.group(2).strip(), no))
    return out


def section_text(text: str, heading: str, level: int = 2) -> str | None:
    """Text sekce `## heading` až po další nadpis stejné nebo vyšší úrovně; None, když chybí."""
    lines = text.split("\n")
    hs = headings(text)
    for idx, (lvl, title, no) in enumerate(hs):
        if lvl == level and title == heading:
            end = len(lines)
            for lvl2, _t, no2 in hs[idx + 1:]:
                if lvl2 <= level:
                    end = no2 - 1
                    break
            return "\n".join(lines[no:end])
    return None


def wikilink_value(value) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"\s*\[\[[^\[\]\n]+\]\]\s*", value))
