"""Příkaz hubs: hub jako přehled a startovní bod agenta (zadání 13 kap. 10.3, 03 kap. 5, 10 kap. 5a).

Generuje jen obsah bloků `hestia:generated` (mimo ně nic, `updated` se nemění):
- hub entity: Domény (+ agregace z potomků), Dokumenty, Postup stavby, Soubory, Otevřené otázky,
- dokument kroku (`step_kind: build`): Skripty,
- `Dashboard/Index.md` [R2]: kořenové entity se zralostí, aktivní předání, otázky podle stáří, poslední změny,
- generované pohledy `Dashboard/views/generated/` (13 kap. 10.9): matice entita × doména a mapa podle místa,
  pokud je instance má (manifest `taxonomy/views.yaml`).
- karta assetu meshe (13 kap. 10.18, 10.19): blok *Z kódu* ze sekce `library` v `asset_index.json` (jen s manifestem
  `asset_sources.yaml`) a blok *Stav v UE* z `Maintenance/reports/ue_assets.json` (jen asset, který report má);
  značky doplní pod ruční text sekce.
Soubory a kroky bere jen z `asset_index.json` (13 kap. 7). Chybějící blok se nedoplňuje, jen ohlásí.
"""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field

from . import CORE_ROOT
from . import asset_index as ai
from . import assets as assets_mod
from . import library as library_mod
from . import ue as ue_mod
from . import ue_assets as ue_assets_mod
from . import views as views_mod
from .blocks import add_section, ensure_block, replace_block
from .changeset import ChangeSet
from .errors import EXIT_OK, UsageError
from .links import headings
from .logs import log_entries, parse_queue
from .model import DOC_TYPES, INACTIVE_VALIDITY, Model
from .util import today as _today
from .util import trailing_date
from .vault import Note, Vault

INDEX_REL = "Dashboard/Index.md"
UE_HEADING = "Stav v UE"                         # blok z posledního čtení Unrealu (13 kap. 10.11)
ASSETS_HEADING = assets_mod.HUB_HEADING          # karty assetů s entitou v used_by (13 kap. 10.16)
CHANGES_REL = "Maintenance/changes.md"
QUEUE_REL = "Maintenance/queue.md"
# mají vlastní místo: kroky v Postupu stavby, scratch v otázkách, know-how a předání ve vlastních skupinách
NOT_IN_DOCUMENTS = ("step", "scratch", "knowhow", "handover")
CARD_BEFORE = {"Z kódu": "Stav v UE", "Stav v UE": "Vizuálně ověřeno"}   # chybějící sekce karty (07 kap. 20)


@dataclass
class HubsResult:
    changed: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _link(name: str) -> str:
    return f"[[{name}]]"


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return out


class Hubs:
    def __init__(self, vault: Vault, model: Model | None = None, index: dict | None = None,
                 day: _dt.date | None = None):
        self.v = vault
        self.m = model or Model(vault)
        self.tx = vault.taxonomy
        self.index = index if index is not None else ai.load_json(vault)
        self.files = (self.index or {}).get("files") or []
        self.day = day or _today()
        qpath = vault.root / QUEUE_REL
        self.queue = parse_queue(qpath.read_text(encoding="utf-8")) if qpath.is_file() else []
        self.step_order = {sid: (st.get("order") if isinstance(st.get("order"), (int, float)) else 10**9, sid)
                           for sid, st in self.tx.build_steps.items()}

    # ------------------------------------------------------------ hub entity
    def domains_block(self, n: Note) -> str:
        fm = n.fm
        rows = []
        for d in self.m.entity_domains(n):
            target = self.m.num(fm, f"target_{d}")
            design, depth = self.m.design_depth(n.name, d), self.m.realization(n.name, d)
            mode = self.m.mode(n.name, d)                  # 13 kap. 10.3, zadání 0.13
            reached = self.m.reached(n.name, d)
            if target is None:
                state = "bez cíle"
            elif reached >= target:
                state = "✔"
            else:
                state = f"−{target - reached}"
            rows.append([d, "–" if design is None else str(design), "–" if depth is None else str(depth),
                         "–" if target is None else str(target), mode, state])
        out = (_table(["Doména", "Návrh", "Realizace", "Cíl", "Režim", "Stav"], rows) if rows
               else ["_Žádné očekávané domény ani cíle._"])
        if self.m.children.get(n.name):
            agg = []
            for d in self.tx.domains:
                mt = self.m.maturity(n.name, d)
                if mt.defined:
                    agg.append([d, f"{mt.percent} % ({len(mt.met)} z {len(mt.relevant)})",
                                f"{mt.weakest[0]} – {_link(mt.weakest[1])}"])
            out += ["", "Zralost podstromu (jednotky s vlastním cílem včetně této entity, 04 kap. 3):", ""]
            out += _table(["Doména", "Zralost", "Nejslabší článek"], agg) if agg else ["_Žádná jednotka podstromu nemá cíl._"]
        return "\n".join(out)

    def documents_block(self, n: Note) -> str:
        docs = [d for d in self.m.docs_of(n.name) if d.type not in NOT_IN_DOCUMENTS]
        order = {t: i for i, t in enumerate(DOC_TYPES)}
        groups: dict[str, list[Note]] = {}
        for d in docs:
            groups.setdefault(d.fm.get("domain") or "bez domény", []).append(d)
        out: list[str] = []
        for dom in [*self.tx.domains, "bez domény"] + sorted(set(groups) - set(self.tx.domains) - {"bez domény"}):
            items = groups.get(dom)
            if not items:
                continue
            items.sort(key=lambda x: (order.get(x.type, 99), x.name))
            active = [x for x in items if x.fm.get("validity") not in INACTIVE_VALIDITY]
            inactive = len(items) - len(active)
            out += ([""] if out else []) + [f"**{dom}**"]
            for x in active:
                depth = x.fm.get("depth") if self.tx.has_depth(x.type or "") else None   # 01 kap. 5 (0.13.3)
                extra = [x.type or "?"]
                if depth is not None:
                    extra.append(f"depth {depth}")
                extra.append(str(x.fm.get("validity") or "bez validity"))
                if x.fm.get("status"):
                    extra.append(str(x.fm["status"]))
                out.append(f"- {_link(x.name)} – {', '.join(extra)}")
            if inactive:
                out.append(f"- nahrazené nebo archivované: {inactive}")
        kh = [d for d in self.m.docs_of(n.name, include_inactive=False) if d.type == "knowhow"]
        if kh:
            out += ([""] if out else []) + ["**Know-how**"] + [f"- {_link(x.name)}" for x in kh]
        hand = [d for d in self.m.docs_of(n.name) if self.m.is_active_handover(d)]
        if hand:
            out += ([""] if out else []) + ["**Aktivní předání**"] + [f"- {_link(x.name)}" for x in hand]
        return "\n".join(out) if out else "_Zatím žádné dokumenty._"

    def files_of(self, entity: str) -> list[dict]:
        return [f for f in self.files if entity in (f.get("entities") or [])]

    def build_block(self, n: Note) -> str:
        if self.index is None:
            return "_`asset_index.json` chybí; spusť `asset_index`._"
        files = self.files_of(n.name)
        docs = [d for d in self.m.docs_of(n.name, include_inactive=False)
                if d.fm.get("build_step") and d.type not in NOT_IN_DOCUMENTS]
        steps = {f["build_step"] for f in files if f.get("build_step")} | {str(d.fm["build_step"]) for d in docs}
        rows = []
        for sid in sorted(steps, key=lambda s: self.step_order.get(s, (10**9, s))):
            step_note = self.v.note_by_name(sid)
            scripts = [f"`{f['path'].rsplit('/', 1)[-1]}`" for f in files if f.get("build_step") == sid]
            sdocs = [_link(d.name) for d in docs if str(d.fm.get("build_step")) == sid]
            rows.append([_link(sid) if step_note else sid, ", ".join(scripts) or "–", ", ".join(sdocs) or "–"])
        return "\n".join(_table(["Krok", "Skripty", "Dokumenty"], rows)) if rows else "_Zatím žádné kroky._"

    def files_block(self, n: Note) -> str:
        if self.index is None:
            return "_`asset_index.json` chybí; spusť `asset_index`._"
        order = {r: i for i, r in enumerate(ai.ROLE_ORDER)}
        files = sorted(self.files_of(n.name), key=lambda f: (order.get(f.get("role"), 99), f["path"]))
        rows = [[f"`{f['path']}`", f.get("role") or "–", f.get("build_step") or "–", f.get("rule") or "–"]
                for f in files]
        return "\n".join(_table(["Soubor", "Role", "Krok", "Pravidlo"], rows)) if rows else "_Žádné soubory._"

    def questions_block(self, n: Note) -> str:
        out = []
        docs = self.m.docs_of(n.name, include_inactive=False)
        for d in docs:
            for q in self.m.open_questions(d):
                out.append(f"- {_link(d.name)}: {q}")
        names = {n.name} | {d.name for d in docs}
        for it in self.queue:
            if it.is_open and it.target.strip("[]") in names:
                out.append(f"- Fronta {it.id} ({it.code}, {it.target}): {it.proposal}")
        for s in docs:
            if s.type == "scratch":
                out.append(f"- Scratch: {_link(s.name)} ({s.fm.get('intake') or 'bez intake'})")
        return "\n".join(out) if out else "_Žádné otevřené otázky z dokumentů, fronty ani scratch._"

    # ------------------------------------------------------------ krok a Index
    def step_block(self, n: Note) -> str:
        if self.index is None:
            return "_`asset_index.json` chybí; spusť `asset_index`._"
        sid = str(n.fm.get("build_step") or n.name)
        rows = []
        for f in self.files:
            if f.get("build_step") != sid:
                continue
            rows.append([f"`{f['path']}`", f.get("role") or "–",
                         ", ".join(_link(e) for e in f.get("entities") or []) or "–",
                         ", ".join(_link(d) for d in f.get("docs") or []) or "–"])
        return "\n".join(_table(["Skript", "Role", "Entity", "Dokumenty"], rows)) if rows else "_Žádné skripty._"

    def index_block(self) -> str:
        out = ["**Kořenové entity** (zralost po doménách, v závorce nejslabší článek; 04 kap. 3)", ""]
        roots = self.m.roots()
        if roots:
            out += _table(["Entita", *self.tx.domains],
                          [[_link(r), *[self.m.maturity_cell(r, d) for d in self.tx.domains]] for r in roots])
        else:
            out.append("_Žádné kořenové entity._")
        hand = sorted((h for h in self.m.notes if self.m.is_active_handover(h)), key=lambda x: x.name)
        out += ["", "**Aktivní předání**", ""]
        if hand:
            for h in hand:
                ents = self.m.entities_of(h)
                out.append(f"- {_link(h.name)}" + (" – " + ", ".join(_link(e) for e in ents) if ents else ""))
        else:
            out.append("_Žádná._")
        limit = int(self.v.config.thresholds.get("open_question_days") or 14)
        young = old = undated = 0
        for note in self.m.notes:
            for q in self.m.open_questions(note):
                d = trailing_date(q)
                if d is None:
                    undated += 1
                elif (self.day - d).days > limit:
                    old += 1
                else:
                    young += 1
        out += ["", f"**Otevřené otázky:** do {limit} dní {young} · starší {old} · bez data {undated}"]
        cpath = self.v.root / CHANGES_REL
        lines = log_entries(cpath.read_text(encoding="utf-8")) if cpath.is_file() else []
        out += ["", "**Poslední změny** (`changes.md`)", ""]
        out += [f"- {' · '.join(x for x in e if x)}" for e in lines[-10:]] or ["_Žádné._"]
        return "\n".join(out)

    # ------------------------------------------------------------ karty assetů
    def card_targets(self, cards: list, rep: dict | None, only: set | None) -> list:
        """Bloky *Z kódu* (meshe, s manifestem) a *Stav v UE* (asset v reportu) v kartách (13 kap. 10.18, 10.19)."""
        lib = (self.index or {}).get("library")
        globals_ = (self.index or {}).get("library_globals") or {}
        lib_by_name = {e["name"]: e for e in lib or []}
        tol = library_mod.tolerance(self.v)
        out = []
        for c in cards:
            note = self.v.notes.get(c.rel)
            if note is None or (only is not None and c.name not in only):
                continue
            blocks = []
            if lib is not None and c.kind == "mesh":
                blocks.append((library_mod.CODE_HEADING, library_mod.code_block(c, note.fm, lib, globals_, tol)))
            ue_block = ue_assets_mod.card_block(self.v, c, rep, lib_by_name, globals_, self.day)
            if ue_block is not None:
                blocks.append((ue_assets_mod.UE_HEADING, ue_block))
            if blocks:
                out.append((note, blocks))
        return out

    # ------------------------------------------------------------ běh
    def plan(self, cs: ChangeSet, only: list[str] | None = None) -> HubsResult:
        res = HubsResult()
        only_set = set(only or [])
        targets: list[tuple[Note, list[tuple[str | None, str]]]] = []
        ue_rules = ue_mod.rules(self.v, self.m)
        asset_cards = assets_mod.cards(self.v, self.m)
        ue_assets_rep = ue_assets_mod.load_report(self.v)
        outdated = ue_assets_mod.outdated_names(self.v, ue_assets_rep)
        for name, n in sorted(self.m.entities.items()):
            if only and name not in only_set:
                continue
            blocks = [("Domény", self.domains_block(n)), ("Dokumenty", self.documents_block(n)),
                      ("Postup stavby", self.build_block(n)), ("Soubory", self.files_block(n)),
                      (UE_HEADING, ue_mod.hub_block(self.v, self.m, name, ue_rules, self.day))]
            # ## Assety: sekce vznikne jen u entity s kartou v used_by (13 kap. 10.16, zadání 0.23)
            asset_block = assets_mod.hub_block(name, asset_cards, outdated)
            if asset_block is not None or ASSETS_HEADING in {h for lvl, h, _ in headings(n.body) if lvl == 2}:
                blocks.append((ASSETS_HEADING, asset_block or "_Žádná karta assetu nemá entitu v `used_by`._"))
            blocks.append(("Otevřené otázky", self.questions_block(n)))
            targets.append((n, blocks))
        for n in sorted(self.m.notes, key=lambda x: x.name):
            if n.type == "step" and n.fm.get("step_kind") == "build" and (not only or n.name in only_set):
                targets.append((n, [("Skripty", self.step_block(n))]))
        targets += self.card_targets(asset_cards, ue_assets_rep, only_set if only else None)
        idx = self.v.notes.get(INDEX_REL)
        if idx is not None:
            targets.append((idx, [("Přehled", self.index_block())]))
        else:
            res.warnings.append(f"{INDEX_REL} neexistuje")
        for vid, rel in views_mod.generated_targets(CORE_ROOT, self.v.game_layer):
            note = self.v.notes.get(rel)
            if note is not None:                    # chybějící pohled doplní update_core --with-views
                targets.append((note, [(views_mod.GENERATED_HEADING, views_mod.GENERATORS[vid](self.m))]))
        for note, blocks in targets:
            text = cs.current(note.path)
            for heading, content in blocks:
                if note.type == "asset":                        # karta: sekce a značky pod ruční text
                    text, _added = add_section(text, heading, before=CARD_BEFORE[heading])
                    text, _added = ensure_block(text, heading)
                elif heading == UE_HEADING:                       # značky pod ruční text (13 kap. 10.3, 10.11)
                    text, _added = ensure_block(text, heading)
                if heading == ASSETS_HEADING:                   # sekce před Otevřenými otázkami (13 kap. 10.16)
                    text, _added = add_section(text, heading, before="Otevřené otázky")
                    text, _added = ensure_block(text, heading)
                new, status = replace_block(text, heading, content)
                if status != "ok":
                    what = "sekce" if status == "missing_section" else "blok hestia:generated v sekci"
                    res.warnings.append(f"{note.rel}: chybí {what} ## {heading}; nedoplňuji")
                    continue
                text = new
            if cs.write(note.path, text):
                res.changed.append(note.rel)
        return res


def run(args, vault: Vault) -> tuple[int, dict, str]:
    from . import profiling                                     # průběžný výstup kroků (zadání 0.29, CR-033)
    with profiling.step("model"):
        h = Hubs(vault)
    unknown = [e for e in args.entities if e not in h.m.entities and vault.note_by_name(e) is None]
    if unknown:
        raise UsageError(f"Neznámá entita nebo krok: {', '.join(unknown)}")
    cs = ChangeSet(vault.project_root)
    with profiling.step("generované bloky"):
        res = h.plan(cs, args.entities or None)
    from . import doc_index                                     # index pro Knihovníka nezastará (13 kap. 10.10)
    replaced = doc_index.replaced_in_vault(vault)               # G5 před přepsáním indexu (zadání 0.29.2)
    applied = bool(args.apply and not cs.empty)
    if args.apply:
        with profiling.step("zápis"):
            if not cs.empty:
                cs.apply()
        # index až z vaultu po zápisu: generované sekce hubů nesou odkazy (links_out)
        with profiling.step("doc_index"):
            after = Vault.load(vault.root) if applied else vault
            cs_idx = ChangeSet(vault.project_root)
            if doc_index.plan(after, cs_idx):
                cs_idx.apply()
                res.changed.append(doc_index.JSON_REL)
                applied = True
    else:
        with profiling.step("doc_index"):
            if doc_index.plan(vault, cs, h.m):                  # dry-run: odhad ze současného stavu
                res.changed.append(doc_index.JSON_REL)
    payload = {"command": "hubs", "applied": applied, "changed": res.changed,
               "warnings": res.warnings, "replaced": [f.as_dict() for f in replaced]}
    if not res.changed:
        lines = ["hubs: beze změny"]
    elif args.apply:
        lines = [f"hubs: zapsáno {len(res.changed)} souborů: {', '.join(res.changed)}"]
    else:
        lines = [f"hubs: změnilo by se {len(res.changed)} souborů (dry-run, zapiš s --apply)", cs.diff().rstrip()]
    if h.index is None:
        lines.append("Upozornění: asset_index.json chybí, sekce Soubory, Postup stavby a Skripty jsou prázdné.")
    lines += [f"Upozornění: {w}" for w in res.warnings]
    lines += doc_index.replaced_lines(replaced)
    return EXIT_OK, payload, "\n".join(lines)
