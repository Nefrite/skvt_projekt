"""Generované bloky `<!-- hestia:generated:start -->` … `<!-- hestia:generated:end -->` (zadání 13 kap. 6).

Obsah mezi značkami skript přepisuje celý, mimo ně nic. Blok se hledá v sekci `## Nadpis`
(sekce = nadpis až po další nadpis stejné nebo vyšší úrovně). Konce řádků souboru se zachovají.
"""
from __future__ import annotations

import re

from .fileio import detect_newline
from .links import headings

START = "<!-- hestia:generated:start -->"
END = "<!-- hestia:generated:end -->"


def _section_span(lines: list[str], text_lf: str, heading: str, level: int = 2) -> tuple[int, int] | None:
    hs = headings(text_lf)
    for idx, (lvl, title, no) in enumerate(hs):
        if lvl == level and title == heading:
            end = len(lines)
            for lvl2, _t, no2 in hs[idx + 1:]:
                if lvl2 <= level:
                    end = no2 - 1
                    break
            return no, end            # řádky [no, end) = obsah sekce (0-based od řádku za nadpisem)
    return None


def replace_block(text: str, heading: str | None, content: str) -> tuple[str, str]:
    """Nahradí obsah generovaného bloku v sekci `heading` (None = první blok v souboru).

    Vrací (nový text, stav): ok / missing_section / missing_block."""
    nl = detect_newline(text)
    lf = text.replace("\r\n", "\n")
    lines = lf.split("\n")
    if heading is None:
        lo, hi = 0, len(lines)
    else:
        span = _section_span(lines, lf, heading)
        if span is None:
            return text, "missing_section"
        lo, hi = span
    start = next((i for i in range(lo, hi) if lines[i].strip() == START), None)
    if start is None:
        return text, "missing_block"
    end = next((i for i in range(start + 1, hi) if lines[i].strip() == END), None)
    if end is None:
        return text, "missing_block"
    # prázdný řádek za značkou a před ní: Obsidian jinak nevykreslí tabulku hned za komentářem
    body = ["", *content.strip("\n").split("\n"), ""] if content.strip() else []
    new_lines = lines[:start + 1] + body + lines[end:]
    return nl.join(new_lines) if nl != "\n" else "\n".join(new_lines), "ok"


def ensure_block(text: str, heading: str) -> tuple[str, bool]:
    """Doplní prázdné značky bloku pod ruční text sekce `## heading`, chybí-li (jen `## Stav v UE`,
    13 kap. 10.3: existující huby dostanou značky). Vrací (text, doplněno)."""
    nl = detect_newline(text)
    lf = text.replace("\r\n", "\n")
    lines = lf.split("\n")
    span = _section_span(lines, lf, heading)
    if span is None:
        return text, False
    lo, hi = span
    if any(lines[i].strip() == START for i in range(lo, hi)):
        return text, False
    at = lo
    for i in range(lo, hi):
        if lines[i].strip():
            at = i + 1
    new_lines = lines[:at] + [START, END] + lines[at:]
    return nl.join(new_lines) if nl != "\n" else "\n".join(new_lines), True


def add_section(text: str, heading: str, before: str | None = None) -> tuple[str, bool]:
    """Doplní sekci `## heading` s prázdnými značkami bloku, chybí-li: před sekci `## before`, jinak na konec
    (`## Assety` v hubu, 13 kap. 10.16). Vrací (text, doplněno)."""
    nl = detect_newline(text)
    lf = text.replace("\r\n", "\n")
    lines = lf.split("\n")
    if _section_span(lines, lf, heading) is not None:
        return text, False
    new = [f"## {heading}", START, END]
    span = _section_span(lines, lf, before) if before else None
    if span is not None:
        at = span[0] - 1                                  # řádek nadpisu `## before`
        new_lines = lines[:at] + new + lines[at:]
    else:
        while lines and lines[-1] == "":
            lines.pop()
        new_lines = lines + new + [""]
    return nl.join(new_lines) if nl != "\n" else "\n".join(new_lines), True


def block_content(text: str, heading: str | None) -> str | None:
    lf = text.replace("\r\n", "\n")
    lines = lf.split("\n")
    lo, hi = (0, len(lines))
    if heading is not None:
        span = _section_span(lines, lf, heading)
        if span is None:
            return None
        lo, hi = span
    start = next((i for i in range(lo, hi) if lines[i].strip() == START), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, hi) if lines[i].strip() == END), None)
    return None if end is None else "\n".join(lines[start + 1:end])


def strip_generated(text: str) -> str:
    """Text bez generovaných bloků včetně značek a jejich konce řádku (pro ruční část sekce; doplněné prázdné
    značky v `## Stav v UE` tak nejsou změna ručního textu)."""
    return re.sub(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"[ \t]*\r?\n?", "", text,
                  flags=re.DOTALL)
