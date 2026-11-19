"""Příkaz audit: G1–G13, zralost; report a fronta jako seznam úkolů (zadání 04 kap. 3–4, 13 kap. 7 a 10.4).

- Nálezy: G6/G7 z lintu a z hlaviček kódu, G1–G5, G8–G12 podle 04 kap. 4 a 10 kap. 9.
- Report `Maintenance/reports/audit_RRRR-MM-DD.md` (šablona 07 kap. 7) + `.json` ([{code, severity, target,
  file, message}]); zralost jako tabulka místo/lokace × doména; stav `reports/state.json`.
- Fronta [R3]: do `queue.md` jdou jen chyby (priorita high) a upozornění (medium); G1, G9, G10, G13 jen do reportu.
  Nález má stabilní klíč kód + cíl (+ soubor): k otevřené položce se stejným klíčem nová nevzniká, zmizelý
  nález uzavře svou položku (`state: done`, datum ve sloupci `closed`; jen `kind: finding`).
- [R4] `--baseline <reports/audit_….json>`: rozdíl nálezů proti dřívějšímu běhu.
- Věkové prahy (otázky, dokumenty, know-how) jsou v reportu v *Doporučených krocích*, ne nálezy.
Instance bez herní vrstvy: G1–G4, G10, G12 a zralost se nepočítají.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import asset_index as ai
from . import gitinfo
from .changeset import ChangeSet
from .errors import EXIT_FINDINGS, EXIT_OK, UsageError
from .findings import SEVERITY_ORDER, Finding, has_errors, sort_findings, to_text
from .fileio import read_text, to_posix
from .links import extract_links, links_in_value, section_text
from .logs import QueueItem, log_entries, next_id, parse_queue, upgrade_queue, write_queue
from .model import DOC_TYPES, INACTIVE_VALIDITY, Model
from .util import as_date, today, trailing_date
from .validate import run_checks
from .vault import Note, Vault

REPORTS = "Maintenance/reports"
STATE_REL = f"{REPORTS}/state.json"
QUEUE_REL = "Maintenance/queue.md"
CHANGES_REL = "Maintenance/changes.md"
REPORT_ONLY = {"G1", "G9", "G10", "G13"}             # [R3]; G13 informace (04 kap. 4)
PRIORITY = {"error": "high", "warning": "medium"}
LORE_REQUIRED = ["Svět a doba", "Místo", "Časové vrstvy", "Obyvatelé a postavy"]     # 12 kap. 3a
ORPHAN_ZONES = ("Docs/", "Steps/")                    # osiřelá poznámka (G6): dokumenty bez jediného odkazu
DUPLICATE_ZONES = ("Docs/", "Scratch/", "KnowHow/", "Steps/", "Inbox/")
STEP_SCRIPT_RE = re.compile(r"^(step|build_.*)$", re.I)


@dataclass
class AuditResult:
    findings: list[Finding] = field(default_factory=list)
    maturity: list[tuple[str, list[str]]] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    commit: str | None = None
    index: ai.IndexResult | None = None


def key_of(f) -> tuple:
    if isinstance(f, dict):
        return f.get("code"), f.get("target"), f.get("file")
    return f.code, f.target, f.file


class Auditor:
    def __init__(self, vault: Vault, day: _dt.date | None = None):
        self.v = vault
        self.m = Model(vault)
        self.tx = vault.taxonomy
        self.th = vault.config.thresholds
        self.day = day or today()
        self.r = AuditResult()
        self.g11_entities: dict[tuple, list[str]] = {}      # (cíl, soubor) -> dotčené entity

    def add(self, code: str, target: str, file: str, message: str, severity: str | None = None) -> None:
        self.r.findings.append(Finding(code, severity or self.tx.severity(code), target, file, message))

    def file_of(self, n: Note) -> str:
        return self.v.project_rel(n.path)

    # ------------------------------------------------------------ G1–G4, G10, G12 (herní vrstva)
    def entity_checks(self) -> None:
        state_docs = {e for n in self.m.notes if n.type == "state" and n.fm.get("validity") == "valid"
                      for e in self.m.entities_of(n)}
        for name, n in sorted(self.m.entities.items()):
            fm, f = n.fm, self.file_of(n)
            for d in self.tx.domains:
                target = self.m.num(fm, f"target_{d}")
                if target is None:
                    continue
                depth, design = self.m.realization(name, d), self.m.design_depth(name, d)
                dd = "–" if design is None else design
                if self.m.mode(name, d) == "design":           # G1 podle režimu cíle (04 kap. 4, zadání 0.13)
                    if (design or 0) < target:
                        self.add("G1", name, f, f"návrh {d} {dd} < target_{d} {target} (režim design)")
                elif (depth or 0) < target:
                    self.add("G1", name, f, f"depth_{d} {depth if depth is not None else '–'} < target_{d} {target}")
                    if (design or 0) >= target:                 # G13 připraveno ke stavbě
                        self.add("G13", name, f, f"připraveno ke stavbě: návrh {d} {design} ≥ target_{d} {target}, "
                                                 f"realizace depth_{d} {depth if depth is not None else '–'}")
            # G2 a G3 u entity s potomky nad podstromem (04 kap. 4): stačí entita nebo kterýkoli potomek
            tree = self.m.subtree(name)
            sub = " ani u potomků" if len(tree) > 1 else ""
            for d in self.m.expected_domains(n):
                if all(self.m.entities[x].fm.get(f"target_{d}") in (None, "") for x in tree):
                    self.add("G2", name, f, f"očekávaná doména {d} (kind {fm.get('kind')}) bez target_{d}{sub}")
            docs = [x for e in tree for x in self.m.docs_of(e, include_inactive=False)
                    if x.type in DOC_TYPES and x.type != "handover" and x.fm.get("status") != "rejected"]
            for d in self.tx.domains:
                target = self.m.num(fm, f"target_{d}")
                if target and target > 0 and not any(x.fm.get("domain") == d for x in docs):
                    self.add("G3", name, f, f"bez dokumentu v doméně {d} (target_{d} {target}){sub}")
            if fm.get("status") in ("built", "verified") and name not in state_docs:
                self.add("G4", name, f, f"status {fm.get('status')} bez platného dokumentu state")
        # crosscut: doména z domains bez cílového dokumentu (odvozeného přes derived_from)
        for c in self.m.notes:
            if c.type != "crosscut" or c.fm.get("validity") in INACTIVE_VALIDITY:
                continue
            derived = [x for x in self.m.notes if c.name in self.m.link_names(x.fm.get("derived_from"))]
            for d in c.fm.get("domains") or []:
                if not any(x.fm.get("domain") == d for x in derived):
                    self.add("G3", c.name, self.file_of(c), f"doména {d} z crosscut bez cílového dokumentu")

    def code_depth_checks(self, files: list[dict]) -> None:
        seen = set()
        with_files = set()
        for f in files:
            for e in f.get("entities") or []:
                with_files.add(e)
            if not f.get("build_step"):
                continue
            for e in f.get("entities") or []:
                n = self.m.entities.get(e)
                if n is None:
                    continue
                for d in f.get("domains") or []:
                    depth = self.m.num(n.fm, f"depth_{d}")
                    if depth is not None and depth <= 1 and (e, d) not in seen:
                        seen.add((e, d))
                        self.add("G10", e, self.file_of(n),
                                 f"má skript kroku {f['build_step']} ({f['path']}), ale depth_{d} {depth}")
        for name, n in sorted(self.m.entities.items()):
            for d in self.tx.domains:
                depth = self.m.num(n.fm, f"depth_{d}")
                if depth is not None and depth >= 4 and name not in with_files:
                    self.add("G10", name, self.file_of(n), f"depth_{d} {depth} bez jediného souboru")
                    break

    def lore_checks(self) -> None:
        required = list(self.v.config.get("required_docs") or [])
        for doc_id in required:
            if doc_id != "lore_master":
                self.r.warnings.append(f"required_docs: neznámý povinný dokument {doc_id!r}")
        if "lore_master" not in required:
            return
        for proto in self.v.config.get("prototypes") or []:
            name = (proto or {}).get("lore") or f"Lore_{(proto or {}).get('id')}"
            n = self.v.note_by_name(name)
            expected = f"/{to_posix(self.v.root.relative_to(self.v.project_root))}/Docs/narrative/{name}.md"
            if n is None or not n.fm:
                self.add("G12", name, expected, f"master lore prototypu {proto.get('id')} chybí")
                continue
            body = n.body.replace("\r\n", "\n")
            for sec in LORE_REQUIRED:
                text = section_text(body, sec)
                text = re.sub(r"<!--.*?-->", "", text or "", flags=re.DOTALL).strip()
                if not text:
                    self.add("G12", n.name, self.file_of(n), f"povinná sekce ## {sec} je prázdná")

    # ------------------------------------------------------------ G5, G6, G8, G9, G11
    def stale_checks(self) -> None:
        raw_days = int(self.th.get("scratch_raw_days") or 14)
        for n in self.m.notes:
            if n.fm.get("validity") == "outdated":
                self.add("G5", n.name, self.file_of(n), "validity: outdated")
            if n.type == "scratch" and n.fm.get("intake") == "raw":
                d = as_date(n.fm.get("updated"))
                if d and (self.day - d).days > raw_days:
                    self.add("G5", n.name, self.file_of(n), f"scratch raw {(self.day - d).days} dní (práh {raw_days})")
            if self.m.is_active_handover(n) and self.m.handover_fulfilled(n):
                self.add("G5", n.name, self.file_of(n), "předání splněné (Zbývá vše hotovo), ale neuzavřené")
            stale = self.stale_doc(n)
            if stale and stale[1]:
                self.add("G5", n.name, self.file_of(n),
                         f"bez změny od {stale[0].isoformat()} (déle než {self.doc_days} dní), "
                         f"entita {stale[2]} se od té doby změnila ({stale[1].isoformat()}, changes.md)")

    @property
    def doc_days(self) -> int:
        return int(self.th.get("stale_doc_days") or 90)

    def entity_changes(self) -> dict[str, _dt.date]:
        """Poslední datum řádku changes.md po entitách (nebo souborech)."""
        if not hasattr(self, "_entity_changes"):
            p = self.v.root / CHANGES_REL
            last: dict[str, _dt.date] = {}
            for e in log_entries(read_text(p)) if p.is_file() else []:
                d = as_date(e[0]) if e else None
                if d and len(e) > 2 and (e[2] not in last or last[e[2]] < d):
                    last[e[2]] = d
            self._entity_changes = last
        return self._entity_changes

    def stale_doc(self, n: Note) -> tuple[_dt.date, _dt.date | None, str | None] | None:
        """Dokument bez změny `updated` déle než stale_doc_days: (updated, datum změny entity nebo None, entita)."""
        upd = as_date(n.fm.get("updated"))
        if (n.type not in DOC_TYPES or n.type == "handover" or n.fm.get("validity") not in ("valid", "draft")
                or not upd or (self.day - upd).days <= self.doc_days):
            return None
        changes = self.entity_changes()                 # kterákoli z entit dokumentu (zadání 0.13.5)
        hits = sorted(((changes[e], e) for e in self.m.entities_of(n) if changes.get(e) and changes[e] > upd),
                      reverse=True)
        return (upd, hits[0][0], hits[0][1]) if hits else (upd, None, None)

    def compiled_checks(self) -> None:
        """G5: kompilát role starší než zdroje = nové složení by kompilát změnilo (13 kap. 6, 04 kap. 4)."""
        from . import compose
        d = self.v.root / compose.COMPILED_DIR
        for p in sorted(d.glob(f"*{compose.COMPILED_SUFFIX}.md")) if d.is_dir() else []:
            role = p.stem.removesuffix(compose.COMPILED_SUFFIX)
            try:
                item = compose.plan(self.v, [role], self.day)[0]
            except Exception as exc:  # noqa: BLE001 – profil zmizel nebo je chybný
                self.add("G5", p.stem, self.v.project_rel(p), f"kompilát nejde obnovit: {exc}")
                continue
            if item.status != "unchanged":
                self.add("G5", p.stem, self.v.project_rel(p),
                         "kompilát role je starší než zdroje (kontrakt, moduly, profil); spusť compose_role")

    def orphan_checks(self) -> None:
        inbound: dict[str, int] = {}
        outbound: dict[str, int] = {}
        for n in self.v.notes.values():
            targets = links_in_value(n.fm or {}) + [l.target for l in extract_links(n.body)]
            for t in targets:
                rel, status = self.v.resolve(t)
                if status == "ok" and rel and rel != n.rel:
                    inbound[rel] = inbound.get(rel, 0) + 1
                    outbound[n.rel] = outbound.get(n.rel, 0) + 1
        for n in self.m.notes:
            if n.rel.startswith(ORPHAN_ZONES) and not inbound.get(n.rel) and not outbound.get(n.rel):
                self.add("G6", n.name, self.file_of(n), "osiřelá poznámka (žádný odkaz z ní ani na ni)")

    def duplicate_checks(self) -> None:
        seen: dict[str, Note] = {}
        for n in sorted(self.m.notes, key=lambda x: x.rel):
            if not n.rel.startswith(DUPLICATE_ZONES):
                continue
            body = re.sub(r"<!--.*?-->", "", n.body, flags=re.DOTALL)
            body = "\n".join(l.strip() for l in body.splitlines() if l.strip() and not l.lstrip().startswith("#"))
            if len(body) < 40:
                continue
            if body in seen:
                self.add("G8", n.name, self.file_of(n), f"stejný obsah jako {seen[body].name}")
            else:
                seen[body] = n

    def orphan_assets(self, files: list[dict]) -> None:
        for f in files:
            if f.get("role") in ("library", "output"):
                continue
            if not f.get("entities") and not f.get("docs"):
                self.add("G9", f["path"], f["path"], "soubor bez napojení na entitu i dokument")

    def g11(self, files: list[dict], state: dict, changes_text: str | None = None) -> None:
        """G11; changes_text = obsah changes.md včetně plánovaných řádků (task_close v dry-run)."""
        since_commit = state.get("last_audited_commit")
        changed = gitinfo.changed_files(self.v.project_root, since_commit)
        if changed is None:
            self.r.warnings.append("projekt není v gitu (nebo git chybí); G11 přeskočeno")
            return
        self.r.commit = gitinfo.head(self.v.project_root)
        by_path = {f["path"]: f for f in files}
        last_audit = as_date(state.get("last_audit"))
        if changes_text is None and (self.v.root / CHANGES_REL).is_file():
            changes_text = read_text(self.v.root / CHANGES_REL)
        changes = log_entries(changes_text or "")
        limit = int(self.th.get("g11_step_entities") or 5)
        for p in changed:
            prel = self.v.project_rel(p)
            f = by_path.get(prel)
            if f is None or f.get("role") == "output" or "/generated/" in prel:
                continue
            since = last_audit or min(_dt.date.fromtimestamp(p.stat().st_mtime), self.day)
            for target, file, ents in self.g11_targets(f, limit):
                if self.documented(target, ents, prel, since, changes):
                    continue
                listed = f"; dotčené entity: {', '.join(ents)}" if target not in ents and ents else ""
                self.add("G11", target, file, f"změna {prel} bez řádku v changes.md a novějšího updated{listed}")
                self.g11_entities[(target, prel)] = ents

    def g11_targets(self, f: dict, limit: int) -> list[tuple[str, str, list[str]]]:
        """Kde se G11 hlásí: knihovna na dokumentu sdíleného kódu, skript kroku nad práh na kroku (10 kap. 8a)."""
        ents = list(f.get("entities") or [])
        stem = f["path"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
        if f.get("role") == "library":
            shared = [d for d in f.get("docs") or [] if (n := self.v.note_by_name(d)) and n.fm
                      and n.fm.get("type") == "step"]
            if shared:
                return [(d, self.file_of(self.v.note_by_name(d)), ents) for d in shared]
        if STEP_SCRIPT_RE.match(stem) and len(ents) > limit and f.get("build_step"):
            n = self.v.note_by_name(f["build_step"])
            return [(f["build_step"], self.file_of(n) if n else f["path"], ents)]
        out = []
        for e in ents:
            n = self.m.entities.get(e)
            out.append((e, self.file_of(n) if n else f["path"], [e]))
        return out

    def documented(self, target: str, ents: list[str], prel: str, since: _dt.date, changes: list[list[str]]) -> bool:
        names = {target, *ents, prel, prel.rsplit("/", 1)[-1]}
        for e in changes:
            d = as_date(e[0]) if e else None
            if d and d >= since and len(e) > 2 and e[2] in names:
                return True
        notes = [self.v.note_by_name(target)] + [self.m.entities.get(x) for x in ents]
        for x in ents:
            notes += self.m.docs_of(x, include_inactive=False)
        for n in notes:
            upd = as_date(n.fm.get("updated")) if n is not None and n.fm else None
            if upd and upd >= since:
                return True
        return False

    # ------------------------------------------------------------ doporučení a zralost
    def recommendations(self) -> None:
        q_days = int(self.th.get("open_question_days") or 14)
        doc_days = int(self.th.get("stale_doc_days") or 90)
        kh_days = int(self.th.get("knowhow_unverified_days") or 180)
        old_q, stale, kh = [], [], []
        for n in sorted(self.m.notes, key=lambda x: x.name):
            for q in self.m.open_questions(n):
                d = trailing_date(q)
                if d and (self.day - d).days > q_days:
                    old_q.append(f"[[{n.name}]]: {q}")
            st = self.stale_doc(n)
            if st and not st[1]:                    # bez změny entity jen report (05 kap. 6)
                stale.append(f"`{n.name}` ({st[0].isoformat()})")
            if n.type == "knowhow" and n.fm.get("validity") == "valid":
                ver = as_date(n.fm.get("verified"))
                if ver and (self.day - ver).days > kh_days:
                    kh.append(f"`{n.name}` (ověřeno {ver.isoformat()})")
        if old_q:
            self.r.recommendations.append(f"Otevřené otázky starší než {q_days} dní:")
            self.r.recommendations += [f"  - {x}" for x in old_q]
        if stale:
            self.r.recommendations.append(f"Dokumenty bez aktualizace déle než {doc_days} dní: " + ", ".join(stale))
        if kh:
            self.r.recommendations.append(f"Know-how ověřené před více než {kh_days} dny: " + ", ".join(kh))

    def maturity_table(self) -> None:
        for name, n in sorted(self.m.entities.items()):
            if n.fm.get("kind") in ("place", "location"):
                self.r.maturity.append((name, [self.m.maturity_cell(name, d) for d in self.tx.domains]))

    # ------------------------------------------------------------ běh
    def run(self, state: dict) -> AuditResult:
        self.r.findings += run_checks(self.v, None)
        idx = ai.build(self.v, self.m)
        self.r.index = idx
        self.r.findings += idx.findings
        self.r.warnings += idx.warnings
        if self.v.game_layer:
            self.entity_checks()
            self.code_depth_checks(idx.files)
            self.lore_checks()
            self.maturity_table()
        self.stale_checks()
        self.compiled_checks()
        self.orphan_checks()
        self.duplicate_checks()
        self.orphan_assets(idx.files)
        self.g11(idx.files, state)
        self.recommendations()
        old = ai.load_json(self.v)
        if old is not None and old.get("files") != idx.files:
            self.r.recommendations.append("`asset_index.json` neodpovídá kódu; spusť `asset_index --apply` a `hubs`.")
        elif old is None:
            self.r.recommendations.append("`asset_index.json` chybí; spusť `asset_index --apply` a `hubs`.")
        self.r.findings = sort_findings(self.r.findings)
        return self.r


# ---------------------------------------------------------------- report, fronta, stav

def load_state(vault: Vault) -> dict:
    p = vault.root / STATE_REL
    try:
        return json.loads(read_text(p)) if p.is_file() else {}
    except ValueError:
        return {}


def previous_report(vault: Vault, day: _dt.date) -> list[dict] | None:
    d = vault.root / REPORTS
    cands = sorted(p for p in d.glob("audit_*.json") if p.stem < f"audit_{day.isoformat()}") if d.is_dir() else []
    if not cands:
        return None
    try:
        return json.loads(read_text(cands[-1]))
    except ValueError:
        return None


def report_json(findings: list[Finding]) -> str:
    rows = ",\n".join("  " + json.dumps(f.as_dict(), ensure_ascii=False) for f in findings)
    return "[\n" + rows + "\n]\n" if rows else "[]\n"


def target_cell(vault: Vault, target: str) -> str:
    """Cíl pro frontu a report: poznámka jako wikilink, soubor mimo vault zkráceně (složka/soubor)."""
    if target.startswith("/"):
        return "`" + "/".join(target.rstrip("/").split("/")[-2:]) + "`"
    return f"[[{target}]]" if vault.note_by_name(target) is not None else target


def target_key(cell: str) -> str:
    return cell.strip().removeprefix("[[").removesuffix("]]").strip("`")


def _line(vault: Vault, f: Finding) -> str:
    where = f"`{f.target}`" if f.target.startswith("/") else target_cell(vault, f.target)
    return f"- {f.code} {where}: {f.message}"


def report_md(vault: Vault, r: AuditResult, day: _dt.date, prev: list[dict] | None, queue_note: list[str]) -> str:
    counts: dict[str, int] = {}
    for f in r.findings:
        counts[f.code] = counts.get(f.code, 0) + 1
    prev_counts: dict[str, int] = {}
    for f in prev or []:
        prev_counts[f.get("code")] = prev_counts.get(f.get("code"), 0) + 1
    codes = sorted(set(counts) | set(prev_counts), key=lambda c: int(c[1:]))
    lines = ["---", "type: report", f"updated: {day.isoformat()}", "---", f"# Audit {day.isoformat()}", "",
             "## Souhrn", "| kód | počet | změna od minula |", "|---|---|---|"]
    for c in codes:
        diff = "–" if prev is None else f"{counts.get(c, 0) - prev_counts.get(c, 0):+d}".replace("+0", "0")
        lines.append(f"| {c} | {counts.get(c, 0)} | {diff} |")
    lines += ["", f"Commit: {r.commit[:12] if r.commit else '– (G11 přeskočeno)'}. "
                  f"Nálezy celkem: {len(r.findings)}."]
    lines += ["", "## Nálezy podle závažnosti"]
    for title, sev in (("Chyby", "error"), ("Upozornění", "warning"), ("Informace", "info")):   # 07 kap. 7
        lines.append(f"### {title}")
        lines += [_line(vault, f) for f in r.findings if f.severity == sev] or ["_Žádné._"]
    lines += ["", "## Zralost", "| místo / lokace | " + " | ".join(vault.taxonomy.domains) + " |",
              "|---|" + "---|" * len(vault.taxonomy.domains)]
    lines += [f"| [[{name}]] | " + " | ".join(cells) + " |" for name, cells in r.maturity]
    lines += ["", "## Doporučené kroky"]
    rec = r.recommendations + queue_note + [f"Upozornění: {w}" for w in r.warnings]
    lines += [x if x.startswith("  ") else f"- {x}" for x in rec] or ["_Žádné._"]
    return "\n".join(lines) + "\n"


def plan_queue(vault: Vault, findings: list[Finding], day: _dt.date, cs: ChangeSet) -> dict:
    """Fronta podle R3 a stabilních klíčů; vrací souhrn (new, closed)."""
    p = vault.root / QUEUE_REL
    text = cs.current(p)
    if text is None:
        return {"new": [], "closed": [], "missing": True}
    upgraded = upgrade_queue(text)
    text = upgraded
    items = parse_queue(text)
    groups: dict[tuple, list[Finding]] = {}
    for f in findings:
        if f.code in REPORT_ONLY or f.severity not in PRIORITY:
            continue
        groups.setdefault((f.code, f.target), []).append(f)
    # klíč kód + cíl; cíl ve frontě je odkaz nebo zkrácená cesta, porovnává se bez [[ ]] a backticků
    keys = {(code, target): {target, target_key(target_cell(vault, target))} for code, target in groups}
    current = {(code, k) for (code, _t), ks in keys.items() for k in ks}
    existing = {(it.code, target_key(it.target)) for it in items if it.kind == "finding"
                and (it.is_open or it.state_value == "rejected")}
    new_items: list[QueueItem] = []
    first = int(next_id(items, "finding").split("-")[1])        # čísla nových F- jednou, ne při každé položce
    for (code, target), fs in groups.items():
        if any((code, k) in existing for k in keys[(code, target)]):
            continue
        sev = min(fs, key=lambda x: SEVERITY_ORDER[x.severity]).severity
        it = QueueItem(f"F-{first + len(new_items):04d}", PRIORITY[sev], "finding", code,
                       target_cell(vault, target), "; ".join(dict.fromkeys(f.message for f in fs)), "open")
        new_items.append(it)
    closed = {it.line: ("done", day.isoformat()) for it in items
              if it.kind == "finding" and it.is_open and (it.code, target_key(it.target)) not in current}
    new_text = write_queue(text, closed, new_items, today=day if (closed or new_items) else None)
    cs.write(p, new_text)
    open_findings = sum(1 for it in parse_queue(new_text) if it.kind == "finding" and it.is_open)
    return {"new": [it.id for it in new_items], "closed": [it.id for it in items if it.line in closed],
            "missing": False, "open_findings": open_findings}


def baseline_diff(current: list[Finding], baseline: list[dict]) -> dict:
    """[R4] Rozdíl proti dřívějšímu reportu; nález = kód + cíl + soubor + text (víc nálezů na jednom cíli)."""
    full = lambda f: (*key_of(f), f.get("message") if isinstance(f, dict) else f.message)  # noqa: E731
    cur = {full(f): f for f in current}
    base = {full(b): b for b in baseline}
    return {
        "new": [cur[k].as_dict() for k in sorted(set(cur) - set(base), key=str)],
        "gone": [base[k] for k in sorted(set(base) - set(cur), key=str)],
        "severity_changed": [{"code": k[0], "target": k[1], "file": k[2], "message": k[3],
                              "from": base[k].get("severity"), "to": cur[k].severity}
                             for k in sorted(set(cur) & set(base), key=str)
                             if base[k].get("severity") != cur[k].severity],
    }


def run(args, vault: Vault) -> tuple[int, dict, str]:
    day = today()
    baseline = None
    if args.baseline:
        bp = Path(args.baseline)
        if not bp.is_file():
            raise UsageError(f"Baseline neexistuje: {bp}")
        try:
            baseline = json.loads(read_text(bp))
        except ValueError:
            raise UsageError(f"Baseline není platný JSON: {bp}")
    state = load_state(vault)
    r = Auditor(vault, day).run(state)
    cs = ChangeSet(vault.project_root)
    q = plan_queue(vault, r.findings, day, cs)
    queue_note = []
    if q["missing"]:
        r.warnings.append(f"{QUEUE_REL} neexistuje; fronta se neaktualizuje")
    else:
        queue_note.append(f"Fronta (`queue.md`): otevřené nálezy {q['open_findings']}; informační nálezy "
                          f"(G1, G9, G10, G13) jsou jen v tomto reportu.")
    prev = previous_report(vault, day)
    base = vault.root / REPORTS / f"audit_{day.isoformat()}"
    cs.write(base.with_suffix(".md"), report_md(vault, r, day, prev, queue_note))
    cs.write(base.with_suffix(".json"), report_json(r.findings))
    new_state = {"last_audit": day.isoformat(), "last_audited_commit": r.commit}
    cs.write(vault.root / STATE_REL, json.dumps(new_state, ensure_ascii=False, indent=2) + "\n")
    if args.apply and not cs.empty:
        cs.apply()
    counts = {s: sum(1 for f in r.findings if f.severity == s) for s in SEVERITY_ORDER}
    payload = {"command": "audit", "applied": bool(args.apply and not cs.empty), "findings": [f.as_dict() for f in r.findings],
               "counts": counts, "queue": {"new": q["new"], "closed": q["closed"]},
               "report": to_posix(base.relative_to(vault.root)) + ".md", "changes": cs.summary(),
               "warnings": r.warnings, "commit": r.commit}
    lines = [to_text(r.findings)]
    verb = "zapsáno" if args.apply else "zapsalo by se (dry-run, zapiš s --apply)"
    if cs.empty:
        lines.append("Report, fronta a stav: beze změny.")
    else:
        lines.append(f"Report, fronta a stav – {verb}: " + ", ".join(
            c.get("path") or c.get("to") for c in cs.summary()))
    if q["new"] or q["closed"]:
        lines.append(f"Fronta: nové {len(q['new'])}, uzavřené {len(q['closed'])}.")
    lines += [f"Upozornění: {w}" for w in r.warnings]
    if baseline is not None:
        bd = baseline_diff(r.findings, baseline)
        payload["baseline"] = bd
        lines.append(f"Proti baseline: nové {len(bd['new'])}, zmizelé {len(bd['gone'])}, "
                     f"změněná závažnost {len(bd['severity_changed'])}.")
        lines += [f"  + {d['code']} {d['target']}: {d['message']}" for d in bd["new"]]
        lines += [f"  − {d.get('code')} {d.get('target')}: {d.get('message', '')}" for d in bd["gone"]]
        lines += [f"  ~ {d['code']} {d['target']}: {d['from']} → {d['to']}" for d in bd["severity_changed"]]
    return (EXIT_FINDINGS if has_errors(r.findings) else EXIT_OK), payload, "\n".join(lines)
