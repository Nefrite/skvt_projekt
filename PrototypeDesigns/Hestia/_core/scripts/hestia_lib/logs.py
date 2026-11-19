"""Logy a fronta (zadání 13 kap. 7, 05 kap. 7).

`changes.md`, `structure_log.md`, `structure_version.md`: řádky `RRRR-MM-DD | …`, oddělovač ` | `,
svislítko v textu jako `\\|`, jen připisování na konec; parser bere jen řádky začínající datem.
`queue.md`: tabulka `id | priority | kind | code | target | proposal | state | closed`; stabilní ID F-/P-/T-,
nové řádky na konec tabulky, v místě se mění jen sloupce `state` a `closed`.
"""
from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass

from .fileio import detect_newline
from .frontmatter import set_field, split

# řádek logu: `| RRRR-MM-DD | … |` (tabulka v Obsidianu); čte se i starší `RRRR-MM-DD | …`
LOG_LINE_RE = re.compile(r"^\|?\s*(\d{4}-\d{2}-\d{2})\s*\|")
QUEUE_COLUMNS = ["id", "priority", "kind", "code", "target", "proposal", "state", "closed"]
LEGACY_QUEUE_COLUMNS = QUEUE_COLUMNS[:-1]          # core 0.3.0, bez closed
QUEUE_PREFIX = {"finding": "F", "proposal": "P", "task": "T"}
OPEN_STATES = {"open", "approved", "in_progress"}


def escape(text: str) -> str:
    return str(text).replace("\r", " ").replace("\n", " ").replace("|", "\\|").strip()


def split_row(line: str) -> list[str]:
    """Buňky řádku `a | b | c` nebo tabulky `| a | b |`; `\\|` je součást textu."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def log_entries(text: str) -> list[list[str]]:
    """Řádky logu jako seznamy polí (první = datum)."""
    return [split_row(line) for line in text.replace("\r\n", "\n").split("\n") if LOG_LINE_RE.match(line)]


def format_line(fields: list) -> str:
    return "| " + " | ".join(escape(f) for f in fields) + " |"


def append_lines(text: str, lines: list[str], today: _dt.date | None = None) -> str:
    """Připíše řádky na konec souboru logu (bez duplicit posledních řádků); doplní `updated`."""
    if not lines:
        return text
    existing = {tuple(split_row(line)) for line in text.replace("\r\n", "\n").split("\n")
                if LOG_LINE_RE.match(line)}
    new = [line for line in lines if tuple(split_row(line)) not in existing]
    if not new:
        return text
    nl = detect_newline(text)
    out = text.rstrip("\r\n") + nl          # bez prázdného řádku: řádky zůstanou v jedné tabulce
    out += nl.join(new) + nl
    if today is not None and split(out).has_frontmatter:
        out = set_field(out, "updated", today, section="orchestration")
    return out


# ---------------------------------------------------------------- fronta

@dataclass
class QueueItem:
    id: str
    priority: str
    kind: str
    code: str
    target: str
    proposal: str
    state: str
    closed: str = ""          # datum uzavření (05 kap. 7.2)
    line: int = -1            # index řádku v souboru (-1 = nový)

    @property
    def state_value(self) -> str:
        return self.state.split()[0] if self.state else ""

    @property
    def is_open(self) -> bool:
        return self.state_value in OPEN_STATES

    def row(self) -> str:
        return "| " + " | ".join(escape(getattr(self, c)) for c in QUEUE_COLUMNS) + " |"


def _is_header(cells: list[str], columns: list[str]) -> bool:
    return [c.lower() for c in cells] == columns


def parse_queue(text: str) -> list[QueueItem]:
    """Položky fronty; čte i starou tabulku bez sloupce `closed` (core 0.3.0)."""
    items = []
    lines = text.replace("\r\n", "\n").split("\n")
    width = 0
    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            width = 0
            continue
        cells = split_row(line)
        if _is_header(cells, QUEUE_COLUMNS) or _is_header(cells, LEGACY_QUEUE_COLUMNS):
            width = len(cells)
            continue
        if not width or set("".join(cells)) <= set("-: "):
            continue
        if len(cells) >= width:
            vals = cells[:width] + [""] * (len(QUEUE_COLUMNS) - width)
            items.append(QueueItem(*vals, line=i))
    return items


def upgrade_queue(text: str) -> str:
    """Doplní do tabulky fronty bez sloupce `closed` prázdný sloupec (záhlaví, oddělovač, řádky)."""
    lines = text.replace("\r\n", "\n").split("\n")
    head = next((i for i, l in enumerate(lines) if l.strip().startswith("|")
                 and _is_header(split_row(l), LEGACY_QUEUE_COLUMNS)), None)
    if head is None:
        return text
    lines[head] = "| " + " | ".join(QUEUE_COLUMNS) + " |"
    i = head + 1
    while i < len(lines) and lines[i].strip().startswith("|"):
        cells = split_row(lines[i])
        if set("".join(cells)) <= set("-: "):
            lines[i] = "|" + "---|" * len(QUEUE_COLUMNS)
        else:
            lines[i] = "| " + " | ".join(escape(c) for c in cells + [""]) + " |"
        i += 1
    return detect_newline(text).join(lines)


def next_id(items: list[QueueItem], kind: str) -> str:
    prefix = QUEUE_PREFIX[kind]
    nums = [int(it.id.split("-")[1]) for it in items if re.fullmatch(rf"{prefix}-\d+", it.id)]
    return f"{prefix}-{(max(nums) if nums else 0) + 1:04d}"


def write_queue(text: str, changed: dict[int, tuple[str, str]], new_items: list[QueueItem],
                today: _dt.date | None = None) -> str:
    """Změní sloupce state a closed u řádků `changed` (index řádku -> (stav, datum)) a připíše nové
    řádky na konec tabulky. Tabulka musí mít sloupec closed (viz upgrade_queue)."""
    if not changed and not new_items:
        return text
    nl = detect_newline(text)
    lines = text.replace("\r\n", "\n").split("\n")
    for i, (state, closed) in changed.items():
        cells = split_row(lines[i])
        cells += [""] * (len(QUEUE_COLUMNS) - len(cells))
        cells[QUEUE_COLUMNS.index("state")] = state
        cells[QUEUE_COLUMNS.index("closed")] = closed
        lines[i] = "| " + " | ".join(escape(c) for c in cells) + " |"
    if new_items:
        header = next((i for i, l in enumerate(lines) if _is_header(split_row(l), QUEUE_COLUMNS)), None)
        if header is None:
            while lines and lines[-1] == "":
                lines.pop()
            lines += ["", "| " + " | ".join(QUEUE_COLUMNS) + " |", "|" + "---|" * len(QUEUE_COLUMNS)]
            last = len(lines) - 1
        else:
            last = header + 1
            while last + 1 < len(lines) and lines[last + 1].strip().startswith("|"):
                last += 1
        lines[last + 1:last + 1] = [it.row() for it in new_items]
    out = nl.join(lines)
    if today is not None and split(out).has_frontmatter:
        out = set_field(out, "updated", today, section="orchestration")
    return out
