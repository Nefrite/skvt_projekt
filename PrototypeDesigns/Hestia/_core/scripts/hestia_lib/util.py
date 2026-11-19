"""Drobné pomůcky společné příkazům fáze 3."""
from __future__ import annotations

import datetime as _dt
import os
import re

from .errors import UsageError

TODAY_ENV = "HESTIA_TODAY"          # RRRR-MM-DD: pevné datum (reprodukovatelné testy, kontrola před vydáním)
_DATE_IN_TEXT = re.compile(r"(\d{4}-\d{2}-\d{2})\s*$")


def today() -> _dt.date:
    """Dnešní datum; proměnná prostředí HESTIA_TODAY ho přepíše."""
    raw = os.environ.get(TODAY_ENV)
    if not raw:
        return _dt.date.today()
    try:
        return _dt.date.fromisoformat(raw.strip())
    except ValueError:
        raise UsageError(f"{TODAY_ENV} musí být datum RRRR-MM-DD, je {raw!r}")


def as_date(value) -> _dt.date | None:
    if isinstance(value, _dt.datetime):
        return value.date()
    if isinstance(value, _dt.date):
        return value
    if isinstance(value, str):
        try:
            return _dt.date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def trailing_date(text: str) -> _dt.date | None:
    """Datum na konci položky (`- [ ] otázka — role, RRRR-MM-DD`, 12 kap. 4.4)."""
    m = _DATE_IN_TEXT.search(text.strip())
    return as_date(m.group(1)) if m else None


def uniq(items) -> list:
    out, seen = [], set()
    for it in items:
        if it is None or it in seen:
            continue
        seen.add(it)
        out.append(it)
    return out


def as_list(value) -> list:
    if value is None or value == "":
        return []
    return list(value) if isinstance(value, (list, tuple)) else [value]
