"""Glosář `Dashboard/Glossary.md`: tabulka *Pojmy projektu* s pevným záhlavím (07 kap. 19, 13 kap. 10.10).

Čte ji `compose_context` (pojmy v balíčku, výběr k `--query`) a `lint` (varování u staršího záhlaví bez kódu
nálezu, zadání 0.14.1). Odkazy ve sloupci *Hlavní dokument nebo hub* kontroluje `lint` jako každý odkaz (G6).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .links import extract_links, section_text
from .logs import split_row
from .vault import Vault

GLOSSARY_REL = "Dashboard/Glossary.md"
SECTION = "Pojmy projektu"
HEADER = ["Pojem", "Význam", "Hlavní dokument nebo hub", "Aliasy", "Zakázané varianty"]
OLD_HEADER = ["Pojem", "Význam", "Poznámka"]
HEADER_ROW = "| " + " | ".join(HEADER) + " |"


@dataclass
class Term:
    term: str
    meaning: str
    main: str | None                                    # jméno cíle odkazu ve sloupci Hlavní dokument nebo hub
    aliases: list[str] = field(default_factory=list)
    forbidden: list[str] = field(default_factory=list)
    row: str = ""                                       # řádek tabulky beze změny (do balíčku)

    @property
    def names(self) -> list[str]:
        """Pojem, aliasy a zakázané varianty (hledání v textu a v otázce)."""
        return [self.term, *self.aliases, *self.forbidden]


def _list(cell: str) -> list[str]:
    return [x.strip() for x in cell.split(",") if x.strip()]


def read(vault: Vault) -> tuple[list[Term], str | None]:
    """Pojmy projektu a popis problému (None = v pořádku nebo glosář chybí)."""
    note = vault.notes.get(GLOSSARY_REL)
    if note is None:
        return [], None
    sec = section_text(note.body.replace("\r\n", "\n"), SECTION)
    if sec is None:
        return [], None
    rows = [line for line in sec.split("\n") if line.strip().startswith("|")]
    if not rows:
        return [], None
    head = split_row(rows[0])
    if head != HEADER:
        if head == OLD_HEADER:
            return [], (f"{GLOSSARY_REL}: tabulka {SECTION} má starší záhlaví ({' | '.join(OLD_HEADER)}); "
                        f"převeď ji ručně na {HEADER_ROW} (07 kap. 19), do té doby ji canon_check nečte")
        return [], (f"{GLOSSARY_REL}: tabulka {SECTION} nemá záhlaví {HEADER_ROW} (07 kap. 19); "
                    "canon_check ji nečte")
    out = []
    for line in rows[2:]:
        cells = split_row(line) + [""] * 5
        if not cells[0]:
            continue
        links = extract_links(cells[2])
        out.append(Term(cells[0], cells[1], links[0].target.rsplit("/", 1)[-1] if links else None,
                        _list(cells[3]), _list(cells[4]), line.strip()))
    return out, None
