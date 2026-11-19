"""Model vaultu pro audit a huby: entity, hierarchie `parent`, dokumenty entit, zralost (zadání 04 kap. 3).

relevant(E,d) = listoví potomci E (nebo E bez potomků) s target_d > 0 a status mimo rejected/on_hold;
reached(x,d)  = depth_d (realizace) v režimu build, hloubka návrhu v režimu design (zadání 0.13, 01 kap. 5);
maturity = |reached ≥ target_d| / |relevant|; depth(E,d) = min reached přes relevant („nejslabší článek“).
Hloubka návrhu entity v doméně = nejvyšší `depth` platných (`validity: valid`) dokumentů `design` a `spec`
s touto entitou a doménou, bez zavržených alternativ (`status: rejected`); nezapisuje se.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .links import links_in_value, section_text
from .taxonomy import is_empty
from .vault import Note, Vault

EXCLUDED_STATUS = {"rejected", "on_hold"}
INACTIVE_VALIDITY = {"superseded", "archived"}
# typy, které se počítají jako dokumentace entity v doméně (G3) a ukazují v sekci Dokumenty hubu
DOC_TYPES = ["concept", "design", "spec", "state", "handover", "guide", "checklist", "reference", "decision"]
DESIGN_TYPES = ("design", "spec")           # nesou hloubku návrhu (01 kap. 5)
OPEN_Q_RE = r"^\s*[-*]\s+\[ \]\s+(.+)$"


@dataclass
class Maturity:
    relevant: list = field(default_factory=list)
    met: list = field(default_factory=list)
    weakest: tuple | None = None          # (depth, entita)

    @property
    def defined(self) -> bool:
        return bool(self.relevant)

    @property
    def percent(self) -> int:
        return round(100 * len(self.met) / len(self.relevant)) if self.relevant else 0


class Model:
    def __init__(self, vault: Vault):
        self.v = vault
        self.tx = vault.taxonomy
        self.notes = [n for n in vault.lint_notes() if n.fm]
        self.entities: dict[str, Note] = {n.name: n for n in self.notes if n.type == "entity"}
        self.children: dict[str, list[str]] = {name: [] for name in self.entities}
        self._entity_cache: dict[int, list[str]] = {}
        self._docs_by_entity: dict[str | None, list[Note]] | None = None
        self._design_cache: dict[tuple[str, str], int | None] = {}
        for name, n in self.entities.items():
            p = self.parent(n)
            if p in self.children:
                self.children[p].append(name)
        for v in self.children.values():
            v.sort()

    # ------------------------------------------------------------ odkazy
    def link_name(self, value) -> str | None:
        """Jméno poznámky z hodnoty wikilinku (rozlišené ve vaultu, jinak text odkazu)."""
        names = links_in_value(value)
        if not names:
            return None
        rel, status = self.v.resolve(names[0])
        if status == "ok" and rel:
            return rel.rsplit("/", 1)[-1].removesuffix(".md")
        return names[0].rsplit("/", 1)[-1]

    def link_names(self, value) -> list[str]:
        out = []
        for t in links_in_value(value):
            rel, status = self.v.resolve(t)
            out.append(rel.rsplit("/", 1)[-1].removesuffix(".md") if status == "ok" and rel else t)
        return out

    def parent(self, n: Note) -> str | None:
        return self.link_name(n.fm.get("parent"))

    def entities_of(self, n: Note) -> list[str]:
        """Všechny entity dokumentu (`entity`: wikilink nebo seznam); dokument se počítá u každé
        z nich, žádná není upřednostněná (01 kap. 9, zadání 0.13.5)."""
        key = id(n)                          # odkazy se rozliší jednou za běh (zátěžový test, 3000 poznámek)
        if key not in self._entity_cache:
            self._entity_cache[key] = list(dict.fromkeys(self.link_names(n.fm.get("entity"))))
        return self._entity_cache[key]

    def entity_of(self, n: Note) -> str | None:
        """První entita dokumentu, jen pro výpis (výpočty berou `entities_of`)."""
        ents = self.entities_of(n)
        return ents[0] if ents else None

    # ------------------------------------------------------------ hierarchie
    def roots(self) -> list[str]:
        return sorted(name for name, n in self.entities.items() if self.parent(n) not in self.entities)

    def subtree(self, name: str) -> list[str]:
        """Entita a všichni její potomci podle `parent` (G2, G3 nad podstromem, 04 kap. 4)."""
        out, stack = [], [name]
        while stack:
            k = stack.pop(0)
            if k in out:
                continue
            out.append(k)
            stack.extend(self.children.get(k) or [])
        return out

    def leaves(self, name: str) -> list[str]:
        kids = self.children.get(name) or []
        if not kids:
            return [name]
        out: list[str] = []
        seen = {name}
        stack = list(kids)
        while stack:
            k = stack.pop(0)
            if k in seen:
                continue
            seen.add(k)
            sub = self.children.get(k) or []
            if sub:
                stack.extend(sub)
            else:
                out.append(k)
        return sorted(out)

    # ------------------------------------------------------------ hodnoty
    @staticmethod
    def num(fm: dict, key: str):
        v = fm.get(key)
        return v if isinstance(v, int) and not isinstance(v, bool) else None

    def expected_domains(self, n: Note) -> list[str]:
        kind = self.tx.kinds.get(n.fm.get("kind")) or {}
        return list(kind.get("expected_domains") or [])

    def entity_domains(self, n: Note) -> list[str]:
        """Očekávané domény podle kind a domény s cílem, v pořadí taxonomie."""
        exp = set(self.expected_domains(n))
        return [d for d in self.tx.domains
                if d in exp or not is_empty(n.fm.get(f"target_{d}"))]

    # ------------------------------------------------------------ návrh a realizace (zadání 0.13)
    def mode(self, name: str, domain: str) -> str:
        return self.tx.target_mode(self.entities[name].fm, domain)

    def design_depth(self, name: str, domain: str) -> int | None:
        """Hloubka návrhu entity v doméně; None = žádný platný návrh (01 kap. 5)."""
        key = (name, domain)
        if key not in self._design_cache:
            depths = [d.fm["depth"] for d in self.docs_of(name)
                      if d.type in DESIGN_TYPES and d.fm.get("validity") == "valid"
                      and d.fm.get("status") != "rejected" and d.fm.get("domain") == domain
                      and self.num(d.fm, "depth") is not None]
            self._design_cache[key] = max(depths) if depths else None
        return self._design_cache[key]

    def realization(self, name: str, domain: str) -> int | None:
        return self.num(self.entities[name].fm, f"depth_{domain}")

    def reached(self, name: str, domain: str) -> int:
        """Dosažená hloubka podle režimu cíle: build = realizace, design = návrh (04 kap. 3)."""
        if self.mode(name, domain) == "design":
            return self.design_depth(name, domain) or 0
        return self.realization(name, domain) or 0

    def maturity(self, name: str, domain: str) -> Maturity:
        m = Maturity()
        for leaf in self.leaves(name):
            fm = self.entities[leaf].fm
            target = self.num(fm, f"target_{domain}")
            if not target or target <= 0 or fm.get("status") in EXCLUDED_STATUS:
                continue
            depth = self.reached(leaf, domain)
            m.relevant.append(leaf)
            if depth >= target:
                m.met.append(leaf)
            if m.weakest is None or (depth, leaf) < m.weakest:
                m.weakest = (depth, leaf)
        return m

    def maturity_cell(self, name: str, domain: str) -> str:
        m = self.maturity(name, domain)
        if not m.defined:
            return "bez cíle"
        return f"{m.percent} % ({m.weakest[0]})"

    # ------------------------------------------------------------ dokumenty
    def docs_of(self, entity: str, include_inactive: bool = True) -> list[Note]:
        if self._docs_by_entity is None:     # index dokumentů podle entity (dřív průchod všech poznámek)
            self._docs_by_entity = {}
            for n in self.notes:
                if n.type != "entity":
                    for e in self.entities_of(n) or [None]:
                        self._docs_by_entity.setdefault(e, []).append(n)
            for docs in self._docs_by_entity.values():
                docs.sort(key=lambda x: x.name)
        docs = self._docs_by_entity.get(entity, [])
        if include_inactive:
            return list(docs)
        return [n for n in docs if n.fm.get("validity") not in INACTIVE_VALIDITY]

    def is_active_handover(self, n: Note) -> bool:
        return n.type == "handover" and n.fm.get("validity") not in INACTIVE_VALIDITY \
            and not n.rel.startswith("Handovers/_archive/")

    def handover_fulfilled(self, n: Note) -> bool:
        """Splněné předání: sekce Zbývá má položky a žádná není otevřená (12 kap. 5, G5)."""
        sec = section_text(n.body.replace("\r\n", "\n"), "Zbývá")
        if sec is None:
            return False
        import re
        done = re.findall(r"^\s*[-*]\s+\[[xX]\]", sec, re.M)
        open_ = re.findall(r"^\s*[-*]\s+\[ \]", sec, re.M)
        return bool(done) and not open_

    def open_questions(self, n: Note) -> list[str]:
        import re
        sec = section_text(n.body.replace("\r\n", "\n"), "Otevřené otázky")
        if not sec:
            return []
        from .blocks import strip_generated
        sec = re.sub(r"<!--.*?-->", "", strip_generated(sec), flags=re.DOTALL)
        return [m.group(1).strip() for m in re.finditer(OPEN_Q_RE, sec, re.M)]
