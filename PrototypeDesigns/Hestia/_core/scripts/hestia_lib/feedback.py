"""Příkaz feedback_log: podněty pro Hestii z `queue.md` do `structure_log.md` (zadání 13 kap. 10.14, 12 kap. 4.5,
zadání 0.22, CR-031).

- Vstup: položky `queue.md` s `kind: proposal` a `code: hestia` nebo `code: hestia:<kategorie>`, které nejsou
  uzavřené (`state` jiný než `done`, `rejected`); `--id P-0001` (opakovatelné) omezí výběr.
- Tvar `proposal` (12 kap. 4.5): `<role>: co se stalo (doklad: …; dopad: …) → navrhovaná změna` (`dopad:` volitelně).
- Formální kontrola: (1) doklad (text v závorce „doklad: …“, jinak wikilink nebo cesta v textu) je dohledatelný:
  wikilink na existující poznámku, existující cesta v projektu, ve vaultu nebo v `_core/`, nebo jméno
  poznámky v backtickách; (2) duplicita: ID položky v popisu řádku `structure_log.md`, nebo tam je shodný text
  navrhované změny.
- Kategorie z `code` (`hestia:missing`), nebo `--category P-0001=missing` (přednost); platné podle 05 kap. 7.3
  (výčet `structure_log_category`). Bez kategorie, s neplatnou kategorií nebo s nedohledaným dokladem se položka
  jen vypíše.
- `--apply`: řádek `| dnes | kategorie | <role>: <co se stalo> (<ID>; doklad: <doklad>) | <dopad> | <změna> | |`
  na konec logu (*dopad* z volitelné části `dopad:` podnětu, jinak prázdný; zadání 0.24.1) a položka `state: done`, `closed` = dnes; duplicita se jen uzavře (odkaz na existující řádek ve výpisu).
  Log se jen připisuje, ve frontě se mění jen `state` a `closed` (13 kap. 7).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .changeset import ChangeSet
from .errors import EXIT_OK, UsageError
from .fileio import read_text
from .links import links_in_value
from .logs import LOG_LINE_RE, append_lines, format_line, parse_queue, split_row, upgrade_queue, write_queue
from .util import today
from .vault import Vault

QUEUE_REL = "Maintenance/queue.md"
LOG_REL = "Maintenance/structure_log.md"
CLOSED_STATES = {"done", "rejected"}
ARROW_RE = re.compile(r"\s*(?:→|->)\s*")
DOKLAD_RE = re.compile(r"\(\s*doklad:\s*(.+?)\)\s*", re.I)
DOPAD_SPLIT_RE = re.compile(r"\s*;\s*dopad:\s*", re.I)               # (doklad: …; dopad: …), zadání 0.24.1
DOPAD_RE = re.compile(r"\(\s*dopad:\s*(.+?)\)\s*", re.I)
PATH_RE = re.compile(r"`([^`]+)`|((?:/|\b)[\w.\-]+(?:/[\w.\-]+)+|\b[\w.\-]+\.(?:md|json|yaml|yml|py|base|css))")


def is_hestia_code(code: str) -> bool:
    c = (code or "").strip().lower()
    return c == "hestia" or c.startswith("hestia:")


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


@dataclass
class Proposal:
    id: str
    line: int
    role: str
    what: str
    doklad: str
    change: str
    dopad: str = ""
    category: str = ""
    problems: list[str] = field(default_factory=list)
    duplicate: dict | None = None


def parse_proposal(text: str) -> tuple[str, str, str, str]:
    """(role, co se stalo, doklad, navrhovaná změna) z tvaru 12 kap. 4.5."""
    role, what, doklad, _dopad, change = parse_parts(text)
    return role, what, doklad, change


def parse_parts(text: str) -> tuple[str, str, str, str, str]:
    """(role, co se stalo, doklad, dopad, navrhovaná změna) z tvaru 12 kap. 4.5
    `<role>: co se stalo (doklad: <odkaz>; dopad: <dopad>) → navrhovaná změna`; `dopad:` je volitelný (zadání 0.24.1)."""
    parts = ARROW_RE.split(text, maxsplit=1)
    left, change = (parts[0], parts[1]) if len(parts) == 2 else (text, "")
    doklad = dopad = ""
    m = DOKLAD_RE.search(left)
    if m:
        doklad = m.group(1).strip()
        left = (left[:m.start()] + " " + left[m.end():]).strip()
        dm = DOPAD_SPLIT_RE.search(doklad)
        if dm:
            dopad, doklad = doklad[dm.end():].strip(" ;,."), doklad[:dm.start()].strip(" ;,")
    if not dopad:                                            # samostatná závorka (dopad: …)
        dm = DOPAD_RE.search(left)
        if dm:
            dopad = dm.group(1).strip(" ;,.")
            left = (left[:dm.start()] + " " + left[dm.end():]).strip()
    role, what = "", left.strip()
    m = re.match(r"^([A-Za-zÀ-ž_][\wÀ-ž_ \-]{0,40}?):\s*(.+)$", left.strip())
    if m:
        role, what = m.group(1).strip(), m.group(2).strip()
    if not doklad:                                           # bez závorky: wikilink nebo cesta v textu
        links = links_in_value(text)
        if links:
            doklad = f"[[{links[0]}]]"
        else:
            pm = PATH_RE.search(text)
            if pm:
                doklad = pm.group(0)
    return role, what.rstrip(" ;,."), doklad, dopad, change.strip()


def doklad_found(vault: Vault, doklad: str) -> bool:
    """Doklad je dohledatelný: aspoň jeden wikilink nebo cesta v něm existuje."""
    if not doklad:
        return False
    for target in links_in_value(doklad):
        if vault.resolve(target)[0]:
            return True
    for m in PATH_RE.finditer(doklad):
        raw = (m.group(1) or m.group(2) or m.group(0)).strip()
        raw = raw.split("#")[0].split(" ")[0].strip()
        if not raw:
            continue
        rel = raw.lstrip("/")
        cands = [vault.project_root / rel, vault.root / rel, vault.root / "Maintenance" / rel,
                 vault.root / "_core" / rel]
        if any(c.exists() for c in cands):
            return True
        name = rel[:-3] if rel.endswith(".md") else rel
        if "/" not in name and vault.note_by_name(name) is not None:
            return True
    return False


def log_rows(text: str) -> list[list[str]]:
    return [split_row(l) for l in text.replace("\r\n", "\n").split("\n") if LOG_LINE_RE.match(l)]


def find_duplicate(rows: list[list[str]], pid: str, change: str) -> dict | None:
    want = _norm(change)
    for cells in rows:
        desc = cells[2] if len(cells) > 2 else ""
        prop = cells[4] if len(cells) > 4 else ""
        if re.search(rf"(?<![\w-]){re.escape(pid)}(?![\w-])", desc):
            return {"date": cells[0], "description": desc, "by": "id"}
        if want and _norm(prop) == want:
            return {"date": cells[0], "description": desc, "by": "text"}
    return None


def parse_categories(values: list[str] | None) -> dict[str, str]:
    out = {}
    for v in values or []:
        if "=" not in v:
            raise UsageError(f"--category {v!r}: čekám P-0001=<kategorie>")
        pid, cat = v.split("=", 1)
        out[pid.strip()] = cat.strip()
    return out


def plan(vault: Vault, ids: list[str] | None, cats: dict[str, str]) -> tuple[list[Proposal], str, str]:
    qp, lp = vault.root / QUEUE_REL, vault.root / LOG_REL
    qtext = read_text(qp) if qp.is_file() else ""
    ltext = read_text(lp) if lp.is_file() else ""
    valid = vault.taxonomy.enum_values("structure_log_category")
    rows = log_rows(ltext)
    out = []
    for it in parse_queue(qtext):
        if it.kind != "proposal" or not is_hestia_code(it.code) or it.state_value in CLOSED_STATES:
            continue
        if ids and it.id not in ids:
            continue
        role, what, doklad, dopad, change = parse_parts(it.proposal)
        p = Proposal(it.id, it.line, role, what, doklad, change, dopad)
        code_cat = it.code.split(":", 1)[1].strip() if ":" in it.code else ""
        p.category = cats.get(it.id) or code_cat
        if not p.category:
            p.problems.append("bez kategorie (code: hestia:<kategorie> nebo --category " + it.id + "=<kategorie>)")
        elif p.category not in valid:
            p.problems.append(f"neplatná kategorie {p.category!r} (platné: {', '.join(valid)})")
        if not doklad_found(vault, doklad):
            p.problems.append("doklad nedohledán" + (f" ({doklad})" if doklad else " (chybí)"))
        p.duplicate = find_duplicate(rows, it.id, change)
        if not p.problems and not p.duplicate:              # duplicita i mezi podněty téhož běhu
            rows.append(["(tento běh)", p.category, f"{what} ({it.id})", "", change, ""])
        out.append(p)
    return out, qtext, ltext


def run(args, vault: Vault) -> tuple[int, dict, str]:
    cats = parse_categories(getattr(args, "category", None))
    ids = getattr(args, "id", None) or None
    items, qtext, ltext = plan(vault, ids, cats)
    day = today()
    ok = [p for p in items if not p.problems and not p.duplicate]
    dups = [p for p in items if p.duplicate]                 # duplicita se uzavře i bez kategorie a dokladu
    bad = [p for p in items if p.problems and not p.duplicate]
    cs = ChangeSet(vault.project_root)
    if ok or dups:
        # doklad v popisu, dopad z části `dopad:` podnětu (zadání 0.24.1, nález P18; 13 kap. 10.14)
        new_rows = [format_line([day.isoformat(), p.category,
                                 (f"{p.role}: " if p.role else "") + f"{p.what} ({p.id}; doklad: {p.doklad})",
                                 p.dopad, p.change, ""]) for p in ok]
        lp, qp = vault.root / LOG_REL, vault.root / QUEUE_REL
        if new_rows:
            if not lp.is_file():
                raise UsageError(f"{LOG_REL} neexistuje")
            cs.write(lp, append_lines(ltext, new_rows, today=day))
        qbase = upgrade_queue(qtext)                        # stará fronta bez closed (počet řádků se nemění)
        changed = {p.line: ("done", day.isoformat()) for p in ok + dups}
        cs.write(qp, write_queue(qbase, changed, [], today=day))
    if args.apply and not cs.empty:
        cs.apply()

    def entry(p: Proposal) -> dict:
        return {"id": p.id, "category": p.category or None, "role": p.role, "what": p.what, "doklad": p.doklad,
                "dopad": p.dopad, "change": p.change, "problems": p.problems, "duplicate": p.duplicate}
    payload = {"command": "feedback_log", "applied": bool(args.apply and not cs.empty),
               "logged": [entry(p) for p in ok], "duplicates": [entry(p) for p in dups],
               "skipped": [entry(p) for p in bad], "changes": cs.summary()}
    verb = "zapsáno" if args.apply else "zapsalo by se (dry-run, zapiš s --apply)"
    lines = []
    if not items:
        lines.append("feedback_log: žádné otevřené podněty code: hestia ve frontě")
    else:
        lines.append(f"feedback_log: podněty {len(items)}; do structure_log {len(ok)}, duplicity {len(dups)}, "
                     f"k ruční opravě {len(bad)} – {verb}")
        lines += [f"  + {p.id} [{p.category}] {p.what} → {p.change or '–'}" for p in ok]
        lines += [f"  = {p.id} duplicita ({'podle ID' if p.duplicate['by'] == 'id' else 'shodná změna'}): "
                  f"řádek {p.duplicate['date']} „{p.duplicate['description']}“; položka se uzavře" for p in dups]
        lines += [f"  ! {p.id}: {'; '.join(p.problems)} – nezapíše se" for p in bad]
        if not args.apply and not cs.empty:
            lines.append(cs.diff())
    return EXIT_OK, payload, "\n".join(l for l in lines if l)
