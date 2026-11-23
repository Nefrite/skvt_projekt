"""Hledání poznámek v indexu dokumentů se zálohou v textu; příkaz find (zadání 13 kap. 10.13, 0.21).

Stejné hledání používá `compose_context --query` (13 kap. 10.10).

- Index (`doc_index`): název a titul, `aliases`, nadpisy sekcí kromě pevných nadpisů šablon, `entity`, cesta;
  pojem z glosáře (i alias a zakázaná varianta) → hlavní dokument; shoda s entitou → hub a platné dokumenty.
- Shoda slov bez ohledu na velikost písmen a diakritiku, podle začátku slova (skloňování; aspoň 4 znaky).
- Když index najde méně než 3 výsledky, doplní je hledání v textu poznámek z indexu (označené „v textu“, se
  sekcí a řádkem); `--text` hledá v textu vždy.
- Filtry `--type`, `--entity`, `--for-role` (pole `for_role` předání, 01 kap. 9.1). Jen čte.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from . import CORE_ROOT
from . import doc_index, glossary
from .errors import EXIT_OK, UsageError
from .fileio import read_text
from .links import headings
from .model import Model
from .util import as_list
from .vault import Note, Vault

ENTITY_TYPES = ("decision", "design", "spec", "state")
TYPE_ORDER = {t: i for i, t in enumerate(["entity", "decision", "design", "spec", "state", "concept", "crosscut",
                                          "reference", "handover", "guide", "checklist", "step", "knowhow",
                                          "scratch"])}
# Pevné nadpisy šablon (hub_sections, templates/tpl_*) nic o obsahu neříkají (každý hub má ## Domény, každý
# návrh ## Výchozí stav); při hledání se neporovnávají.
TEMPLATE_HEADINGS = {"Otevřené otázky", "Předzpracování (doplní Knihovník)", "Předzpracování (doplní Curator)"}
MIN_INDEX_RESULTS = 3            # méně výsledků z indexu → doplnit hledáním v textu
MAX_LINE_HITS = 5                # řádků na poznámku při shodě v textu
IN_TEXT = "v textu"
_WORD_RE = re.compile(r"[a-z0-9]+")


def fold(text: str) -> str:
    """Malá písmena bez diakritiky."""
    return "".join(ch for ch in unicodedata.normalize("NFKD", str(text).lower()) if not unicodedata.combining(ch))


def words(text: str, min_len: int = 4) -> list[str]:
    return [w for w in _WORD_RE.findall(fold(text)) if len(w) >= min_len]


def word_match(q: str, w: str) -> bool:
    """Shoda podle začátku slova (skloňování): společný začátek aspoň 4 znaky a nejvýš o 2 kratší než kratší slovo."""
    if q == w:
        return True
    n = 0
    for a, b in zip(q, w):
        if a != b:
            break
        n += 1
    return n >= max(4, min(len(q), len(w)) - 2)


def matched(qwords: list[str], text: str) -> set[str]:
    tokens = set(_WORD_RE.findall(fold(text)))
    return {q for q in qwords if any(word_match(q, t) for t in tokens)}


@dataclass
class Candidate:
    note: Note
    words: set[str] = field(default_factory=set)
    reasons: list[str] = field(default_factory=list)
    sections: list[dict] = field(default_factory=list)      # shodné nadpisy {heading, line, end_line}
    lines: list[dict] = field(default_factory=list)         # shoda v textu {line, heading}
    in_text: bool = False                                   # jen shoda v textu (záloha nebo --text)

    def add(self, ws: set[str], reason: str) -> None:
        if ws:
            self.words |= ws
            if reason not in self.reasons:
                self.reasons.append(reason)


class Finder:
    def __init__(self, vault: Vault, m: Model, terms: list[glossary.Term]):
        self.v, self.m, self.terms = vault, m, terms
        self.records = doc_index.build(vault, m)
        self.fixed = TEMPLATE_HEADINGS | {str(s.get("heading")) for s in vault.taxonomy.hub_sections}
        for tpl in sorted((CORE_ROOT / "templates").glob("tpl_*.md")):     # nadpisy šablon dokumentů
            self.fixed |= {h for lvl, h, _ in headings(read_text(tpl)) if lvl in (2, 3)}

    def _cand(self, out: dict, note: Note) -> Candidate:
        return out.setdefault(note.rel, Candidate(note))

    def _index(self, q: list[str], exclude) -> dict[str, Candidate]:
        out: dict[str, Candidate] = {}
        for r in self.records:
            n = self.v.notes[r["path"]]
            if exclude(n):
                continue
            c = Candidate(n)
            c.add(matched(q, n.name.replace("_", " ")) | matched(q, r["title"]), f"název {n.name}")
            for a in r["aliases"]:
                c.add(matched(q, a), f"alias {a}")
            for s in r.get("sections") or [{"heading": h} for h in r["headings"]]:
                h = s["heading"]
                ws = set() if h in self.fixed else matched(q, h)
                if ws:
                    c.add(ws, f"nadpis {h}")
                    c.sections.append({k: s[k] for k in ("heading", "line", "end_line") if k in s})
            for e in r["entity"]:
                c.add(matched(q, e.replace("_", " ")), f"entita {e}")
            c.add(matched(q, r["path"].rsplit(".", 1)[0].replace("_", " ").replace("/", " ")) - c.words, "cesta")
            if c.words:
                prev = self._cand(out, n)
                prev.words |= c.words
                prev.reasons += [x for x in c.reasons if x not in prev.reasons]
                prev.sections += c.sections
        for t in self.terms:
            ws = set().union(*(matched(q, name) for name in t.names)) if t.names else set()
            target = self.v.note_by_name(t.main) if t.main else None
            if ws and target is not None and target.fm and not exclude(target):
                self._cand(out, target).add(ws, f"glosář {t.term}")
        for name, hub in self.m.entities.items():                 # shoda s entitou: hub a platné dokumenty
            ws = matched(q, name.replace("_", " "))
            if not ws or exclude(hub):
                continue
            for n in [hub] + self.entity_docs(name):
                if not exclude(n):
                    self._cand(out, n).add(ws, f"entita {name}")
        return out

    def _text(self, q: list[str], exclude, out: dict[str, Candidate], only_new: bool) -> int:
        """Shoda v textu poznámek z indexu: řádky se sekcí; vrací počet nových kandidátů."""
        added = 0
        for r in self.records:
            n = self.v.notes[r["path"]]
            if exclude(n) or (only_new and n.rel in out):
                continue
            off = (n.split.body_line - 1) if n.split and n.split.has_frontmatter else 0
            secs = r.get("sections") or []
            ws_all: set[str] = set()
            hits = []
            for no, line in enumerate(n.body.split("\n"), start=1):
                ws = matched(q, line) if line.strip() else set()
                if not ws:
                    continue
                ws_all |= ws
                if len(hits) < MAX_LINE_HITS:
                    line_no = no + off
                    sec = next((s["heading"] for s in reversed(secs) if s["line"] <= line_no), None)
                    hits.append({"line": line_no, "heading": sec})
            if not ws_all:
                continue
            new = n.rel not in out
            c = self._cand(out, n)
            c.add(ws_all, IN_TEXT)
            c.lines = hits
            if new:
                c.in_text = True
                added += 1
        return added

    def search(self, text: str, exclude=lambda n: False, in_text: bool = False) -> tuple[list[Candidate], str]:
        """Kandidáti seřazení (index před textem, pak podle počtu shod). Druhá hodnota: "" = jen index,
        "doplněno" = index našel méně než 3 a doplnil text, "záložně" = index nenašel nic, "text" = --text."""
        q = words(text) or words(text, 2)
        out = self._index(q, exclude)
        mode = ""
        if in_text:
            self._text(q, exclude, out, only_new=False)
            mode = "text"
        elif len(out) < MIN_INDEX_RESULTS:
            had = len(out)
            if self._text(q, exclude, out, only_new=True):
                mode = "doplněno" if had else "záložně"
        ranked = sorted(out.values(), key=lambda c: (c.in_text, -len(c.words), c.note.type != "entity",
                                                     TYPE_ORDER.get(c.note.type, 99), c.note.name))
        return ranked, mode

    def entity_docs(self, name: str) -> list[Note]:
        return [n for n in self.m.docs_of(name, include_inactive=False)
                if n.type in ENTITY_TYPES and n.fm.get("validity") == "valid" and n.fm.get("status") != "rejected"]


# ---------------------------------------------------------------- příkaz find

def _filter(m: Model, args):
    types = {t.strip() for t in as_list(args.type) for t in str(t).split(",") if t.strip()} if args.type else set()
    entity = (args.entity or "").strip().strip("[]") or None
    role = (args.for_role or "").strip().casefold() or None

    def exclude(n: Note) -> bool:
        fm = n.fm or {}
        if types and fm.get("type") not in types:
            return True
        # karta assetu patří entitám z used_by (13 kap. 10.16, zadání 0.23)
        ents = m.link_names(fm.get("used_by")) if fm.get("type") == "asset" else m.entities_of(n)
        if entity and not (n.name == entity or entity in ents):
            return True
        if role and role not in {str(r).casefold() for r in as_list(fm.get("for_role")) if r}:
            return True
        return False
    return exclude


def _where(c: Candidate) -> str:
    if c.sections:
        return "; ".join(f"§ {s['heading']} ř. {s['line']}–{s['end_line']}" for s in c.sections[:3])
    if c.lines:
        return "; ".join((f"§ {h['heading']} " if h["heading"] else "") + f"ř. {h['line']}" for h in c.lines[:3])
    return ""


def run(args, vault: Vault) -> tuple[int, dict, str]:
    if not (args.query or "").strip():
        raise UsageError("find: zadej dotaz")
    m = Model(vault)
    terms, _problem = glossary.read(vault)
    ranked, mode = Finder(vault, m, terms).search(args.query, exclude=_filter(m, args), in_text=args.text)
    results = [{"path": c.note.rel, "type": c.note.type, "validity": (c.note.fm or {}).get("validity"),
                "reasons": c.reasons, "sections": c.sections, "lines": c.lines, "in_text": c.in_text}
               for c in ranked]
    head = f"find „{args.query}“: {len(results)} výsledků"
    if mode == "doplněno":
        head += f" (index méně než {MIN_INDEX_RESULTS}, doplněno hledáním v textu)"
    elif mode == "záložně":
        head += " (index nic nenašel, hledáno v textu)"
    lines = [head]
    for c, r in zip(ranked, results):
        tag = f" · {IN_TEXT}" if c.in_text else ""
        where = _where(c)
        lines.append(f"- {r['path']} · {r['type'] or '–'} · {r['validity'] or '–'}{tag}"
                     + (f" — {where}" if where else "") + f"  [{', '.join(c.reasons)}]")
    payload = {"command": "find", "query": args.query, "mode": mode or "index", "results": results}
    return EXIT_OK, payload, "\n".join(lines)
