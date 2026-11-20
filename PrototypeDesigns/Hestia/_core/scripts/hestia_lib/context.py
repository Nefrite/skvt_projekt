"""Příkaz compose_context: balíček kontextu pro chat bez vaultu (zadání 13 kap. 10.10, 12 kap. 3b.5 a 7.1).

`Maintenance/context/<id>_context.md`, obdoba kompilátu role: bez frontmatteru, hlavička v HTML komentářích
(požadavek, verze core, datum, zdroje). Vstup právě jeden z `--entity`, `--topic` (kategorie, doména, `inbox`),
`--query`.

- Entita: hub (včetně bloku *Domény*), platné `design` / `spec` / `state` / `decision` k entitě, výňatek master
  lore, aktivní předání; pak pojmy z glosáře, které se v balíčku vyskytují, a otevřené otázky.
- Téma: dokumenty kategorie nebo domény (`valid` a `draft`, platnost je u zdroje); `inbox` = nezpracované položky (`intake: raw`) a k nim kandidátní
  dokumenty.
- Otázka (zadání 0.14.1): hledá se v indexu dokumentů (název, `aliases`, nadpisy kromě pevných nadpisů šablon,
  entita) a v glosáři, ne v celých textech; bez ohledu na velikost písmen a diakritiku, podle začátku slova (aspoň 4 znaky). Pojem
  z glosáře (i alias a zakázaná varianta) → hlavní dokument nebo hub; shoda s entitou → hub a platné dokumenty.
  Řazení podle počtu shod; když index nic nenajde, záložně celé texty (uvedeno v hlavičce). U kandidáta důvod.
- Limit `context_max_chars` (`config.yaml`) platí pro celý balíček kromě seznamu *Nevešlo se*: části se berou
  v pořadí celé, jinak výňatek (začátky sekcí); co se nevejde, je v *Nevešlo se* jako odkaz s jednou větou.
Zastaralý balíček (nové složení by ho změnilo) hlásí audit jako G5; lint balíčky nekontroluje.
"""
from __future__ import annotations

import datetime as dt
import re
import unicodedata
from dataclasses import dataclass, field

from .changeset import ChangeSet
from .compose import _clean_body, core_version_of
from . import CORE_ROOT
from . import doc_index, glossary
from .errors import EXIT_OK, UsageError
from .fileio import read_text, to_posix
from .links import headings
from .model import DOC_TYPES, INACTIVE_VALIDITY, Model
from .util import as_date, as_list, today as _today
from .vault import Note, Vault

CONTEXT_DIR = "Maintenance/context"
SUFFIX = "_context"
DEFAULT_MAX_CHARS = 60000
ENTITY_TYPES = ("decision", "design", "spec", "state")
TYPE_ORDER = {t: i for i, t in enumerate(["entity", "decision", "design", "spec", "state", "concept", "crosscut",
                                          "reference", "handover", "guide", "checklist", "step", "knowhow",
                                          "scratch"])}
MAX_CANDIDATES = 5
# Pevné nadpisy šablon (hub_sections, templates/tpl_*) nic o obsahu neříkají (každý hub má ## Domény, každý
# návrh ## Výchozí stav); při hledání se neporovnávají.
TEMPLATE_HEADINGS = {"Otevřené otázky", "Předzpracování (doplní Knihovník)", "Předzpracování (doplní Curator)"}
_REQ_RE = re.compile(r"^<!-- request: (.*) \| core: [^|]* \| date: \d{4}-\d{2}-\d{2} -->$")
_WORD_RE = re.compile(r"[a-z0-9]+")


# ---------------------------------------------------------------- požadavek

@dataclass
class Request:
    entity: str | None = None
    topic: str | None = None
    query: str | None = None

    def validate(self) -> None:
        if sum(1 for x in (self.entity, self.topic, self.query) if x) != 1:
            raise UsageError("compose_context: zadej právě jedno z --entity, --topic, --query")

    @property
    def label(self) -> str:
        if self.entity:
            return f"entity={self.entity}"
        if self.topic:
            return f"topic={self.topic}"
        return "query=" + " ".join(self.query.replace("|", "/").split())

    @property
    def id(self) -> str:
        if self.entity:
            return self.entity
        if self.topic:
            return self.topic
        return "_".join(words(self.query, 1))[:60].strip("_") or "query"

    @classmethod
    def parse(cls, label: str) -> "Request":
        key, _, value = label.partition("=")
        if key not in ("entity", "topic", "query") or not value:
            raise UsageError(f"neznámý požadavek balíčku: {label}")
        return cls(**{key: value})


# ---------------------------------------------------------------- hledání

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

    def search(self, text: str, exclude=lambda n: False) -> tuple[list[Candidate], bool]:
        """Kandidáti k otázce seřazení podle počtu shod; druhá hodnota True = záložně v celých textech."""
        q = words(text)
        out: dict[str, Candidate] = {}
        for r in self.records:
            n = self.v.notes[r["path"]]
            if exclude(n):
                continue
            c = Candidate(n)
            c.add(matched(q, n.name.replace("_", " ")) | matched(q, r["title"]), f"název {n.name}")
            for a in r["aliases"]:
                c.add(matched(q, a), f"alias {a}")
            for h in r["headings"]:
                if h not in self.fixed:
                    c.add(matched(q, h), f"nadpis {h}")
            for e in r["entity"]:
                c.add(matched(q, e.replace("_", " ")), f"entita {e}")
            if c.words:
                prev = self._cand(out, n)
                prev.words |= c.words
                prev.reasons += [x for x in c.reasons if x not in prev.reasons]
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
        fallback = False
        if not out:
            fallback = True
            for r in self.records:
                n = self.v.notes[r["path"]]
                if not exclude(n):
                    self._cand(out, n).add(matched(q, n.body), "celý text")
            out = {k: c for k, c in out.items() if c.words}
        ranked = sorted(out.values(), key=lambda c: (-len(c.words), c.note.type != "entity",
                                                     TYPE_ORDER.get(c.note.type, 99), c.note.name))
        return ranked, fallback

    def entity_docs(self, name: str) -> list[Note]:
        return [n for n in self.m.docs_of(name, include_inactive=False)
                if n.type in ENTITY_TYPES and n.fm.get("validity") == "valid" and n.fm.get("status") != "rejected"]


# ---------------------------------------------------------------- skládání

@dataclass
class Part:
    note: Note
    excerpt_only: bool = False
    extra: list[str] = field(default_factory=list)          # řádky pod zdrojem (Shoda:, Kandidáti:)


@dataclass
class Context:
    request: Request
    rel: str
    text: str
    sources: list[str] = field(default_factory=list)
    overflow: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return self.request.id


def _source_line(n: Note, excerpt: bool) -> str:
    fm = n.fm or {}
    upd = as_date(fm.get("updated"))
    s = f"Zdroj: [[{n.name}]] · {fm.get('type') or '–'} · {fm.get('validity') or '–'} · " \
        f"updated {upd.isoformat() if upd else '–'}"
    return s + (" · výňatek" if excerpt else "")


def _excerpt(lines: list[str]) -> list[str]:
    """Začátky sekcí: nadpisy a první odstavec pod každým."""
    out, take = [], True
    for line in lines:
        if line.startswith("#"):
            out.append(line)
            take = True
            continue
        if not line.strip():
            if take and out and not out[-1].startswith("#"):
                take = False
            continue
        if take:
            out.append(line)
    return out


def _sentence(n: Note) -> str:
    for line in _clean_body(n.body):
        s = line.strip().lstrip("-*> ").strip()
        if s and not line.startswith("#") and not s.startswith("|"):
            s = re.split(r"(?<=[.!?])\s", s, maxsplit=1)[0]
            return s if len(s) <= 140 else s[:137].rstrip() + "…"
    return "bez textu"


def _overflow_line(n: Note) -> str:
    fm = n.fm or {}
    upd = as_date(fm.get("updated"))
    return (f"- [[{n.name}]] ({fm.get('type') or '–'}, {fm.get('validity') or '–'}, "
            f"updated {upd.isoformat() if upd else '–'}): {_sentence(n)}")


def _render_part(p: Part, excerpt: bool) -> str:
    body = _clean_body(p.note.body)
    body = _excerpt(body) if excerpt else body
    lines = [f"## {p.note.name}", "", _source_line(p.note, excerpt), *p.extra, "", *body]
    return "\n".join(lines).rstrip() + "\n"


def _questions(m: Model, notes: list[Note]) -> list[str]:
    return [f"- [ ] {q} ([[{n.name}]])" for n in notes for q in m.open_questions(n)]


def _terms_in(terms: list[glossary.Term], text: str) -> list[glossary.Term]:
    tokens = set(_WORD_RE.findall(fold(text)))
    out = []
    for t in terms:
        names = [w for name in t.names for w in _WORD_RE.findall(fold(name))]
        if any(w in tokens or any(word_match(w, x) for x in tokens if len(w) >= 4) for w in names):
            out.append(t)
    return out


def compose(vault: Vault, req: Request, today: dt.date | None = None, core_root=CORE_ROOT) -> Context:
    req.validate()
    day = today or _today()
    m = Model(vault)
    terms, _problem = glossary.read(vault)
    finder = Finder(vault, m, terms)
    parts: list[Part] = []
    notes_line: list[str] = []
    is_inbox = lambda n: n.type == "scratch" and n.fm.get("intake") == "raw"  # noqa: E731
    title = req.label.split("=", 1)[1]

    if req.entity:
        if req.entity not in m.entities:
            raise UsageError(f"compose_context: entita {req.entity} neexistuje")
        hub = m.entities[req.entity]
        parts.append(Part(hub))
        parts += [Part(n) for n in sorted(finder.entity_docs(req.entity),
                                          key=lambda x: (TYPE_ORDER.get(x.type, 99), x.name))]
        line = [req.entity]                                       # entita a její předci (master lore kořene)
        while True:
            p = m.parent(m.entities[line[-1]])
            if p not in m.entities or p in line:
                break
            line.append(p)
        lore = [n for n in m.notes if n.fm.get("master") == "lore" and n.fm.get("validity") not in INACTIVE_VALIDITY]
        lore = [n for n in lore if set(m.entities_of(n)) & set(line)] or lore
        parts += [Part(n, excerpt_only=True) for n in lore]
        parts += [Part(n) for n in m.docs_of(req.entity) if m.is_active_handover(n)]
    elif req.topic:
        tx = vault.taxonomy
        if req.topic == "inbox":
            items = sorted((n for n in m.notes if is_inbox(n)), key=lambda n: n.rel)
            cands: list[Note] = []
            for it in items:
                own = it.body.replace("\r\n", "\n").split("## Předzpracování", 1)[0]      # bez šablony
                ranked, _fb = finder.search(f"{it.name.replace('_', ' ')} {own}", exclude=lambda n: is_inbox(n) or
                                            n.rel.startswith("Dashboard/"))
                top = [c.note for c in ranked[:MAX_CANDIDATES]]
                extra = ["Kandidáti: " + ", ".join(f"[[{n.name}]]" for n in top)] if top else ["Kandidáti: žádní"]
                parts.append(Part(it, extra=extra))
                cands += [n for n in top if n not in cands]
            parts += [Part(n) for n in cands]
            if not items:
                notes_line.append("Inbox nemá nezpracované položky (`intake: raw`).")
        elif req.topic in tx.domains or req.topic in tx.categories:
            docs = [n for n in m.notes if (n.type in DOC_TYPES or n.type == "crosscut")
                    and n.fm.get("validity") in ("valid", "draft") and n.fm.get("status") != "rejected"
                    and (n.fm.get("domain") == req.topic or req.topic in as_list(n.fm.get("domains"))
                         or req.topic in as_list(n.fm.get("category")))]
            parts += [Part(n) for n in sorted(docs, key=lambda x: (TYPE_ORDER.get(x.type, 99), x.name))]
        else:
            raise UsageError(f"compose_context: téma {req.topic} není kategorie, doména ani inbox")
    else:
        ranked, fallback = finder.search(req.query)
        if fallback:
            notes_line.append("hledání: záložně v celých textech (index nic nenašel)")
        parts += [Part(c.note, extra=[f"Shoda: {', '.join(c.reasons)} ({len(c.words)})"]) for c in ranked]

    # výběr do limitu (celý text kromě seznamu Nevešlo se): celé, jinak výňatek, jinak odkaz
    limit = int(vault.config.get("context_max_chars") or DEFAULT_MAX_CHARS)
    chosen: list[tuple[Part, str, bool]] = []
    overflow: list[Note] = []
    used = 1200                                                       # hlavička a úvod balíčku
    for p in parts:
        full = None if p.excerpt_only else _render_part(p, False)
        exc = _render_part(p, True)
        if full is not None and used + len(full) <= limit:
            chosen.append((p, full, False))
            used += len(full)
        elif used + len(exc) <= limit:
            chosen.append((p, exc, True))
            used += len(exc)
        else:
            overflow.append(p.note)
    included = [p.note for p, _t, _e in chosen]
    body_text = "\n".join(t for _p, t, _e in chosen)
    sections: list[str] = []
    found_terms = _terms_in(terms, body_text)
    if found_terms:
        sections.append("\n".join(["## Pojmy z glosáře", "", f"Zdroj: [[{glossary.GLOSSARY_REL[:-3].split('/')[-1]}]]",
                                   "", glossary.HEADER_ROW, "|" + "---|" * len(glossary.HEADER),
                                   *[t.row for t in found_terms]]) + "\n")
    questions = _questions(m, included)
    if questions:
        sections.append("\n".join(["## Otevřené otázky", "", *questions]) + "\n")
    while chosen and used + sum(map(len, sections)) > limit:          # pojmy a otázky se musí vejít
        p, t, _e = chosen.pop()
        overflow.insert(0, p.note)
        used -= len(t)
    if overflow:
        sections.append("\n".join(["## Nevešlo se", "", *[_overflow_line(n) for n in overflow]]) + "\n")

    sources = [p.note.rel for p, _t, _e in chosen] + ([glossary.GLOSSARY_REL] if found_terms else [])
    head = [
        "<!-- hestia:context – generovaný soubor, needitovat; obnoví ho compose_context (zadání 13, kap. 10.10) -->",
        f"<!-- request: {req.label} | core: {core_version_of(core_root)} | date: {day.isoformat()} -->",
        f"<!-- sources: {', '.join(sources) or '–'} -->",
    ] + [f"<!-- {x} -->" for x in notes_line if x.startswith("hledání")]
    lines = head + [f"# Kontext: {title}", "",
                    "Balíček kontextu pro chat bez vaultu (dočasný instruktážní soubor, 12 kap. 7.1). U každé části "
                    "je zdroj, platnost a datum; platí verze ve vaultu, změny vracíš zápisem Hestia."]
    lines += [f"\n{x}" for x in notes_line if not x.startswith("hledání")]
    if not parts:
        lines += ["", "_Pro tento požadavek nic nenalezeno._"]
    text = "\n".join(lines) + "\n\n" + "\n".join(t for _p, t, _e in chosen)
    if sections:
        text = text.rstrip("\n") + "\n\n" + "\n".join(sections)
    text = text.rstrip("\n") + "\n"
    return Context(req, f"{CONTEXT_DIR}/{req.id}{SUFFIX}.md", text, sources, [n.name for n in overflow])


# ---------------------------------------------------------------- zastarání (G5) a zápis

_DATE_LINE_RE = re.compile(r"\| date: \d{4}-\d{2}-\d{2} -->")


def _without_date(text: str) -> str:
    return _DATE_LINE_RE.sub("| date: - -->", text.replace("\r\n", "\n"), count=1)


def request_of(text: str) -> Request | None:
    lines = text.replace("\r\n", "\n").split("\n")
    m = _REQ_RE.match(lines[1]) if len(lines) > 1 else None
    return Request.parse(m.group(1)) if m else None


def stale(vault: Vault, path, day: dt.date | None = None) -> str | None:
    """None = balíček odpovídá zdrojům; jinak důvod pro G5."""
    text = read_text(path)
    try:
        req = request_of(text)
        if req is None:
            return "balíček kontextu bez hlavičky request; nejde obnovit"
        new = compose(vault, req, day)
    except UsageError as exc:
        return f"balíček kontextu nejde obnovit: {exc}"
    if _without_date(new.text) != _without_date(text):
        return f"balíček kontextu je starší než zdroje; spusť compose_context --{req.label.replace('=', ' ', 1)}"
    return None


def run(args, vault: Vault) -> tuple[int, dict, str]:
    req = Request(args.entity, args.topic, args.query)
    c = compose(vault, req)
    path = vault.root / c.rel
    old = read_text(path) if path.is_file() else None
    status = "new" if old is None else ("unchanged" if _without_date(old) == _without_date(c.text) else "changed")
    if args.apply and status != "unchanged":
        cs = ChangeSet(vault.project_root)
        cs.write(path, c.text)
        cs.apply()
    payload = {"command": "compose_context", "applied": bool(args.apply and status != "unchanged"),
               "path": c.rel, "status": status, "chars": len(c.text), "sources": c.sources, "overflow": c.overflow}
    word = {"new": "nový", "changed": "změněný", "unchanged": "beze změny"}[status]
    lines = [f"compose_context {req.label}: {word} → {c.rel} ({len(c.text)} znaků, zdrojů {len(c.sources)}"
             + (f", nevešlo se {len(c.overflow)}" if c.overflow else "") + ")"]
    if not args.apply and status != "unchanged":
        lines.append("Dry-run: nic nezapsáno; zápis s --apply.")
    return EXIT_OK, payload, "\n".join(lines)
