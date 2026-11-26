"""Měření `--profile` a průběžný výstup kroků (zadání 0.29, CR-033; 13 kap. 10.22).

- **Průběžný výstup:** dlouhé příkazy (`task_close`, `weekly`, `update_core`, `audit`, `hubs`, `doc_index`)
  ohlásí začátek a konec každého kroku hned na stderr (bez bufferu, `flush`), aby přerušené volání ukázalo, kde
  skončilo: `hestia: <příkaz>: <krok> …` a `hestia: <příkaz>: <krok> hotovo (N s)`. `--quiet` výpis vypne.
- **Měření (`--profile`, globální přepínač):** tabulka kroků na konec výstupu (u `--json` na stderr, aby JSON
  zůstal beze změny; s `--apply` i na konec reportu příkazu, má-li ho): čas, počet `stat`, výpisy adresářů
  (volání, položky), čtení (soubory, bajty) a zápisy (soubory, bajty) zvlášť. Počítá se nad `os.stat` (i
  `Path.stat`, `is_file`, `exists`), výpisy `os.scandir`/`os.listdir` (i `Path.iterdir`, `glob`, `os.walk`;
  zvlášť, zadání 0.29.2), otevřením souboru ke čtení (`open`, `Path.read_text`; bajty = velikost souboru)
  a zápisem přes `fileio.atomic_write` a `open` k zápisu. Výsledek příkazu se nemění; bez `--profile` se nic
  nepočítá.
- **Podprocesy** (`weekly`, kroky `update_core`; zadání 0.29.2): `child()` předá podprocesu `--profile` a cestu
  v proměnné `HESTIA_PROFILE_OUT`; podproces tam místo výpisu zapíše své řádky (JSON) a rodič je vloží vnořeně
  pod krok, ve kterém podproces běžel (`↳` v tabulce).
Kroky se mohou vnořovat (krok `task_close` uvnitř příkazu); tabulka je ve pořadí konců, řádek *celkem* = celý běh.
"""
from __future__ import annotations

import builtins
import io
import json
import os
import re
import sys
import tempfile
import time
from contextlib import contextmanager

PROGRESS_RE = re.compile(r"^hestia: [\w ]+: .*(…|hotovo \(|přerušeno \()")
CHILD_ENV = "HESTIA_PROFILE_OUT"

ENABLED = False
QUIET = False
COMMAND = ""
KEYS = ("stat", "dirs", "dir_entries", "read", "read_bytes", "write", "write_bytes")
_counts = dict.fromkeys(KEYS, 0)
_steps: list[dict] = []
_open: list[list] = []           # děti (podprocesy) otevřených kroků, nejvnitřnější poslední
_t0 = 0.0
_orig: dict = {}


def configure(command: str, profile: bool = False, quiet: bool = False) -> None:
    """Nastaví příkaz pro průběžný výstup; `profile=True` zapne počítání (jednou za proces)."""
    global COMMAND, QUIET, ENABLED, _t0
    COMMAND, QUIET = command, quiet
    if profile and not ENABLED:
        ENABLED = True
        _t0 = time.perf_counter()
        _patch()


class _Scandir:
    """Obal `os.scandir`: počítá položky výpisu, jinak se chová jako původní iterátor."""

    def __init__(self, it):
        self._it = it

    def __iter__(self):
        return self

    def __next__(self):
        entry = next(self._it)
        _counts["dir_entries"] += 1
        return entry

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False

    def close(self):
        close = getattr(self._it, "close", None)
        if close:
            close()


def _patch() -> None:
    _orig.update(stat=os.stat, open=builtins.open, io_open=io.open, scandir=os.scandir, listdir=os.listdir)

    def stat(*a, **k):
        _counts["stat"] += 1
        return _orig["stat"](*a, **k)

    def scandir(*a, **k):
        _counts["dirs"] += 1
        return _Scandir(_orig["scandir"](*a, **k))

    def listdir(*a, **k):
        out = _orig["listdir"](*a, **k)
        _counts["dirs"] += 1
        _counts["dir_entries"] += len(out)
        return out

    def open_(file, mode="r", *a, **k):
        f = _orig["open"](file, mode, *a, **k)
        try:
            if any(c in mode for c in "wax+"):
                _counts["write"] += 1
            else:
                _counts["read"] += 1
                _counts["read_bytes"] += os.fstat(f.fileno()).st_size
        except (OSError, AttributeError, ValueError):
            pass
        return f

    os.stat = stat
    os.scandir = scandir
    os.listdir = listdir
    builtins.open = open_
    io.open = open_


def count_write(nbytes: int) -> None:
    """Zápis přes `fileio.atomic_write` (os.fdopen se přes `open` nepočítá)."""
    if ENABLED:
        _counts["write"] += 1
        _counts["write_bytes"] += nbytes


def without_progress(text: str) -> str:
    """Výpis stderr podpříkazu bez řádků průběžného výstupu (chybová hláška je pak poslední řádek)."""
    return "\n".join(l for l in (text or "").splitlines() if not PROGRESS_RE.match(l))


def say(msg: str) -> None:
    if not QUIET:
        print(f"hestia: {COMMAND}: {msg}" if COMMAND else f"hestia: {msg}", file=sys.stderr, flush=True)


@contextmanager
def step(name: str, announce: bool = True):
    """Krok s průběžným výstupem (začátek a konec hned) a měřením (`--profile`)."""
    if announce:
        say(f"{name} …")
    t0 = time.perf_counter()
    snap = dict(_counts)
    children: list = []
    _open.append(children)
    ok = False
    try:
        yield
        ok = True
    finally:
        _open.pop()
        dt = time.perf_counter() - t0
        if ENABLED:
            _steps.append(dict({k: _counts[k] - snap[k] for k in KEYS}, name=name, seconds=dt, children=children))
        if announce:
            say(f"{name} {'hotovo' if ok else 'přerušeno'} ({dt:.1f} s)")


@contextmanager
def child(label: str, env: dict | None = None):
    """Podproces Hestie s vnořeným měřením (zadání 0.29.2): vrátí (prostředí, argumenty navíc). Bez `--profile`
    prostředí beze změny a žádné argumenty. Po skončení vloží řádky podprocesu pod právě otevřený krok."""
    env = dict(os.environ if env is None else env)
    if not ENABLED:
        yield env, []
        return
    fd, path = tempfile.mkstemp(prefix="hestia_profile_", suffix=".json")
    os.close(fd)
    env[CHILD_ENV] = path
    try:
        yield env, ["--profile"]
    finally:
        try:
            with _orig["open"](path, encoding="utf-8") as f:
                data = f.read()
            rows_ = json.loads(data) if data.strip() else None
        except (OSError, ValueError):
            rows_ = None
        try:
            os.unlink(path)
        except OSError:
            pass
        if isinstance(rows_, list) and rows_:
            total = dict(rows_[-1], name=label, children=rows_[:-1])
            (_open[-1] if _open else _steps).append(total)


def rows() -> list[dict]:
    total = dict(_counts, name="celkem", seconds=time.perf_counter() - _t0, children=[])
    return [*_steps, total]


def write_child_rows() -> bool:
    """Podproces (`HESTIA_PROFILE_OUT`): řádky do souboru rodiče místo výpisu. True = zapsáno."""
    path = os.environ.get(CHILD_ENV)
    if not (ENABLED and path):
        return False
    try:
        with _orig["open"](path, "w", encoding="utf-8") as f:
            json.dump(rows(), f, ensure_ascii=False)
    except OSError:
        return False
    return True


def _kb(n: int) -> str:
    return f"{n / 1024:.1f} kB" if n >= 1024 else f"{n} B"


def _flat(items: list[dict], depth: int = 0):
    for r in items:
        yield depth, r
        yield from _flat(r.get("children") or [], depth + 1)


def table() -> list[str]:
    out = ["| krok | čas | stat | výpisy adresářů | čtení | zápis |", "|---|---|---|---|---|---|"]
    for depth, r in _flat(rows()):
        name = ("↳ " * depth) + r["name"]
        out.append(f"| {name} | {r['seconds']:.2f} s | {r.get('stat', 0)} "
                   f"| {r.get('dirs', 0)} ({r.get('dir_entries', 0)} položek) "
                   f"| {r.get('read', 0)} ({_kb(r.get('read_bytes', 0))}) "
                   f"| {r.get('write', 0)} ({_kb(r.get('write_bytes', 0))}) |")
    return out


def text() -> str:
    return "\n".join(["", f"Profil (--profile, {COMMAND}):", *table()])
