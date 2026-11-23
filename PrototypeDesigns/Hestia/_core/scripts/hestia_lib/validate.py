"""Kontroly G6 (rozbité odkazy) a G7 (frontmatter, povinné sekce) – zadání 01 kap. 12, 04 kap. 4, 10 kap. 9.

Fáze 1: G6 = wikilinky v těle i frontmatteru, cesty v `assets`; G7 = pravidla 01 kap. 12,
povinné sekce hubu a kroku, lokální taxonomie, kroky bez dokumentu v Steps/.
Hlavičky skriptů (G6/G7 z 10 kap. 9) přidá fáze 3.

Instance bez herní vrstvy (`game_layer: false`, 01 kap. 2, 13 kap. 5): herní sekce se nevede u žádného
typu (game_section = none), povinná herní pole se nevyžadují, herní pravidla (domény, kategorie,
hloubka, milníky) se nespouštějí; herní pole ve frontmatteru jsou upozornění.
"""
from __future__ import annotations

import datetime as _dt
import re

from . import library, ue_assets
from .findings import Finding
from .links import extract_links, headings, links_in_value, wikilink_value
from .taxonomy import FieldDef, is_empty
from .util import as_list
from .vault import Note, Vault

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PROJECT_ROLE_RE = re.compile(r"Roles/[^/]+\.md")         # required: project_role (zadání 0.17)
# karta assetu (13 kap. 10.16, 07 kap. 20, 01 kap. 9.5)
ASSET_PURPOSE = "Účel a použití"
ASSET_FROM_IN_PROGRESS = ("in_progress", "generated", "imported", "verified")
ASSET_FROM_GENERATED = ("generated", "imported", "verified")
_AXES_RE = re.compile(r"\b(os[ayue]?|osou|osám|osách|osami|axis|axes)\b", re.I)
_PIVOT_RE = re.compile(r"\bpivot", re.I)
_PREVIEW_RE = re.compile(r"!\[\[[^\]|#]+\.(png|jpe?g|webp|gif|svg)(\|[^\]]*)?\]\]|!\[[^\]]*\]\([^)]+\)", re.I)
_DATE_IN_TEXT_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


class Checker:
    def __init__(self, vault: Vault):
        self.v = vault
        self.tx = vault.taxonomy
        self.game = vault.game_layer
        self.out: list[Finding] = []

    def game_section(self, type_id: str) -> str:
        return self.tx.game_section(type_id) if self.game else "none"

    def is_game_field(self, fd: FieldDef, type_id: str) -> bool:
        return fd.section_for(type_id) == "game"

    # ------------------------------------------------------------ pomocné
    def add(self, code: str, note: Note | None, message: str, severity: str | None = None,
            file: str | None = None, target: str | None = None) -> None:
        sev = severity or self.tx.severity(code)
        f = file if file is not None else (self.v.project_rel(note.path) if note else "")
        t = target if target is not None else (note.name if note else "")
        self.out.append(Finding(code, sev, t, f, message))

    # ------------------------------------------------------------ G7: hodnoty
    def _check_scalar(self, value, vtype: str) -> str | None:
        """None = v pořádku, jinak popis chyby."""
        if vtype.startswith("enum:"):
            name = vtype[5:]
            allowed = self.tx.enum_values(name)
            if isinstance(value, (list, dict)) or str(value) not in [str(a) for a in allowed]:
                where = "taxonomy_local" if name in ("tech", "build_step", "milestone") else "taxonomie"
                return f"hodnota {value!r} mimo výčet {name} ({where})"
            return None
        if vtype == "wikilink":
            return None if wikilink_value(value) else f"očekávám wikilink v uvozovkách, je {value!r}"
        if vtype == "date":
            if isinstance(value, _dt.date):
                return None
            if isinstance(value, str) and _DATE_RE.match(value):
                try:
                    _dt.date.fromisoformat(value)
                    return None
                except ValueError:
                    pass
            return f"neplatné datum {value!r} (RRRR-MM-DD)"
        if vtype == "depth":
            if isinstance(value, bool) or not isinstance(value, int) or value not in self.tx.depth:
                return f"hloubka musí být číslo 0–6, je {value!r}"
            return None
        if vtype == "text":
            return None if isinstance(value, (str, int, float, _dt.date)) else f"očekávám text, je {value!r}"
        return None

    def check_value(self, key: str, value, fd: FieldDef) -> list[str]:
        if is_empty(value):
            return []
        vt = fd.value
        if vt in ("wikilink_list",):
            vals = value if isinstance(value, list) else [value]
            return [e for v in vals if not is_empty(v) for e in [self._check_scalar(v, "wikilink")] if e]
        if vt == "path_list":
            if not isinstance(value, list):
                return [f"očekávám seznam cest, je {value!r}"]
            return [f"cesta {p!r} musí začínat / (od kořene projektu)" for p in value
                    if not isinstance(p, str) or not p.startswith("/")]
        if vt == "list":
            vals = value if isinstance(value, list) else [value]
            if not isinstance(value, list) and key not in ("milestone",):
                return [f"očekávám seznam, je {value!r}"]
            if fd.items:
                return [e for v in vals if not is_empty(v) for e in [self._check_scalar(v, fd.items)] if e]
            return []
        err = self._check_scalar(value, vt)
        return [err] if err else []

    # ------------------------------------------------------------ G7: poznámka
    def check_frontmatter(self, note: Note) -> None:
        if note.fm_error:
            self.add("G7", note, note.fm_error)
            return
        if note.fm is None:
            self.add("G7", note, "chybí frontmatter")
            return
        fm = note.fm
        t = fm.get("type")
        if is_empty(t):
            self.add("G7", note, "chybí povinné pole type")
            return
        if t not in self.tx.types:
            self.add("G7", note, f"hodnota {t!r} mimo výčet type (taxonomie)")
            return

        # povinná pole
        for fd in self.tx.fields_for_type(t):
            if not self.game and self.is_game_field(fd, t):
                continue
            if fd.pattern:
                for d in self.tx.domains:
                    key = fd.name.replace("<domain>", d)
                    if fd.required.evaluate(fm, t, d, self.tx.target_mode(fm, d)) and is_empty(fm.get(key)):
                        self.add("G7", note, f"chybí povinné pole {key}")
                continue
            if fd.required.kind == "project_role" and PROJECT_ROLE_RE.fullmatch(note.rel):
                if is_empty(fm.get(fd.name)):      # profil projektové role (01 kap. 9.1; zadání 0.17.1), role core ne
                    what = f"chybí povinné pole {fd.name}" if fd.name not in fm else f"povinné pole {fd.name} je prázdné"
                    self.add("G7", note, f"{what} (profil projektové role): doplň verzi core z _core/VERSION")
                continue
            if not fd.required.evaluate(fm, t):
                continue
            if fd.name not in fm:
                self.add("G7", note, f"chybí povinné pole {fd.name}")
            elif is_empty(fm[fd.name]) and not fd.allow_empty:
                self.add("G7", note, f"povinné pole {fd.name} je prázdné")

        # hodnoty známých polí
        for key, value in fm.items():
            fd, _dom = self.tx.field_for_key(str(key))
            if fd is None or (not self.game and self.is_game_field(fd, t)):
                continue
            for err in self.check_value(str(key), value, fd):
                self.add("G7", note, f"{key}: {err}")

        # herní sekce u typu bez ní (nebo v instanci bez herní vrstvy)
        if self.game_section(t) == "none":
            game_keys = [k for k in fm if (self.tx.field_for_key(str(k))[0] or None)
                         and self.is_game_field(self.tx.field_for_key(str(k))[0], t)]
            if game_keys:
                where = f"u typu {t}" if self.game else "v instanci bez herní vrstvy (game_layer: false)"
                self.add("G7", note, f"herní sekce {where}: {', '.join(map(str, game_keys))}",
                         severity="warning")

        if self.game:
            self._check_game_rules(note, t)
            if t == "asset":
                self.check_asset(note)
        self.check_sections(note)

    # ------------------------------------------------------------ G7: karta assetu (13 kap. 10.16, zadání 0.23)
    def asset_manifest(self) -> bool:
        if not hasattr(self, "_asset_manifest"):
            self._asset_manifest = (self.v.root / library.SOURCES_REL).is_file()
        return self._asset_manifest

    def asset_in_ue_report(self, note: Note) -> bool:
        if not hasattr(self, "_ue_assets"):
            rep = ue_assets.load_report(self.v)
            self._ue_assets = set((rep or {}).get("assets") or {})
        names = {note.name} | {str(v) for v in as_list(note.fm.get("variants"))}
        return bool(names & self._ue_assets)

    def check_asset(self, note: Note) -> None:
        """Pole a sekce karty podle `asset_status` (13 kap. 10.16, 07 kap. 20); stav kontrola nemění."""
        from .links import section_text
        fm, body = note.fm, note.body.replace("\r\n", "\n")
        status = str(fm.get("asset_status") or "")

        def sec(heading: str) -> str:
            return re.sub(r"<!--.*?-->", "", section_text(body, heading) or "", flags=re.DOTALL).strip()

        def need_field(name: str, why: str) -> None:
            if is_empty(fm.get(name)):
                self.add("G7", note, f"karta assetu ({why}): chybí pole {name}")

        def need_section(heading: str, why: str) -> None:
            if not sec(heading):
                self.add("G7", note, f"karta assetu ({why}): sekce ## {heading} chybí nebo je prázdná")

        need_section(ASSET_PURPOSE, "vždy")
        if status == "requested":
            need_section("Požadavek", "requested")
            if is_empty(fm.get("envelope")) and not extract_links(sec("Požadavek")):
                self.add("G7", note, "karta assetu (requested): chybí envelope (obalové rozměry [x, y, z] cm) "
                                     "nebo odkaz na návrh v ## Požadavek")
        if status in ASSET_FROM_IN_PROGRESS:
            need_field("owner", f"{status}, od in_progress")
        if status in ASSET_FROM_GENERATED:
            why = f"{status}, od generated"
            need_field("asset_source", why)
            kind = str(fm.get("asset_kind") or "")
            if kind in ("mesh", "blueprint"):              # rozměr grayboxu po celou dobu (01 kap. 9.5; 0.25)
                need_field("envelope", f"{why}, {kind}: rozměr grayboxu")
            if kind == "mesh" and self.asset_manifest():   # etapa B: Z kódu = generovaný blok (13 kap. 10.18)
                if not library.has_code_block(note.text):
                    self.add("G7", note, f"karta assetu ({why}): ## Z kódu bez generovaného bloku "
                                         "(hubs --apply po asset_index --apply)")
            else:
                need_section("Z kódu", why)
            purpose = sec(ASSET_PURPOSE)
            if not (_AXES_RE.search(purpose) and _PIVOT_RE.search(purpose)):
                self.add("G7", note, f"karta assetu ({why}): v ## {ASSET_PURPOSE} chybí osy a pivot")
            if not _PREVIEW_RE.search(purpose):
                self.add("G7", note, f"karta assetu ({why}): v ## {ASSET_PURPOSE} chybí vložený náhled (![[…png]])")
        if status in ("imported", "verified"):
            need_field("ue_path", f"{status}, od imported")
            if self.asset_in_ue_report(note):              # etapa C: Stav v UE = blok, je-li asset v reportu
                if not ue_assets.has_block(note.text):
                    self.add("G7", note, f"karta assetu ({status}, od imported): ## Stav v UE bez generovaného "
                                         "bloku (asset je v reportu ue_assets.json; hubs --apply)")
            else:
                need_section("Stav v UE", f"{status}, od imported")
        if status == "verified" and not _DATE_IN_TEXT_RE.search(sec("Vizuálně ověřeno")):
            self.add("G7", note, "karta assetu (verified): sekce ## Vizuálně ověřeno bez data (kdo, kdy, verze)")
        if status == "superseded":
            need_field("superseded_by", "superseded")
        if status in ("rejected", "superseded"):
            need_section("Poznámky", f"{status}, důvod")
        # upozornění: složka a jméno (13 kap. 10.16)
        cat = str(fm.get("asset_category") or "").strip().strip("/")
        if cat and note.rel.rsplit("/", 1)[0] != f"Assets/{cat}":
            self.add("G7", note, f"karta assetu leží mimo Assets/{cat}/ (asset_category)", severity="warning")
        ue_path = str(fm.get("ue_path") or "").strip()
        if ue_path:
            last = ue_path.rstrip("/").rsplit("/", 1)[-1].split(".", 1)[0]
            if last and last != note.name:
                self.add("G7", note, f"jméno karty {note.name} se liší od posledního segmentu ue_path ({last})",
                         severity="warning")

    def _check_game_rules(self, note: Note, t: str) -> None:
        fm = note.fm
        # domain / domains
        if t == "crosscut" and not is_empty(fm.get("domain")):
            self.add("G7", note, "crosscut nemá domain (jen domains)")
        if not is_empty(fm.get("domains")) and t not in ("crosscut", "step"):
            self.add("G7", note, f"domains smí mít jen crosscut a step, ne {t}")
        if t == "crosscut" and isinstance(fm.get("domains"), list) and len(fm["domains"]) < 2:
            self.add("G7", note, "crosscut musí mít v domains aspoň dvě domény")

        # kategorie mimo doménu
        dom = fm.get("domain")
        cats = fm.get("category")
        if dom in self.tx.domains and isinstance(cats, list):
            for c in cats:
                cat = self.tx.categories.get(c)
                if cat and dom != cat.get("home_domain") and dom not in (cat.get("overlaps") or []):
                    self.add("G7", note, f"kategorie {c} neodpovídá doméně {dom}", severity="warning")

        # depth_x bez target_x
        if t == "entity":
            for d in self.tx.domains:
                if f"depth_{d}" in fm and is_empty(fm.get(f"target_{d}")) and not is_empty(fm.get(f"depth_{d}")):
                    self.add("G7", note, f"depth_{d} bez target_{d} (nezapočítává se do zralosti)",
                             severity="info")
                if not is_empty(fm.get(f"target_mode_{d}")) and is_empty(fm.get(f"target_{d}")):
                    self.add("G7", note, f"target_mode_{d} bez target_{d} (režim cíle bez cíle)",
                             severity="warning")
            self._check_milestone_range(note)

    def _check_milestone_range(self, note: Note) -> None:
        fm = note.fm
        a, b = fm.get("milestone_from"), fm.get("milestone_to")
        if a in self.tx.milestones and b in self.tx.milestones:
            oa, ob = self.tx.milestones[a].get("order"), self.tx.milestones[b].get("order")
            if isinstance(oa, int) and isinstance(ob, int) and ob < oa:
                self.add("G7", note, f"milestone_to {b} má nižší order než milestone_from {a}")

    def check_sections(self, note: Note) -> None:
        t = note.fm.get("type")
        if t not in ("entity", "step"):
            return
        step_kind = note.fm.get("step_kind")
        required = [s["heading"] for s in self.tx.hub_sections
                    if s["type"] == t and (t != "step" or s.get("step_kind") == step_kind)]
        present = {h for lvl, h, _ in headings(note.body) if lvl == 2}
        for h in required:
            if h not in present:
                what = "hubu" if t == "entity" else "dokumentu kroku"
                self.add("G7", note, f"chybí povinná sekce {what}: ## {h}")
        if t == "step" and step_kind == "shared":
            self._check_shared_table(note)

    def _check_shared_table(self, note: Note) -> None:
        """Tabulka *Kdo používá* má pevné záhlaví (13 kap. 10.2); asset_index z ní bere entity."""
        from .links import section_text
        from .logs import split_row
        sec = section_text(note.body.replace("\r\n", "\n"), "Kdo používá")
        rows = [l for l in (sec or "").split("\n") if l.strip().startswith("|")]
        expected = ["Typ nebo funkce", "Entity", "Kroky"]
        if rows and split_row(rows[0]) != expected:
            self.add("G7", note, "tabulka Kdo používá musí mít záhlaví | " + " | ".join(expected) + " |")

    # ------------------------------------------------------------ G6: odkazy
    def check_links(self, note: Note) -> None:
        if note.rel == "Maintenance/queue.md" or note.rel.startswith("Maintenance/reports/"):
            return          # historické záznamy: odkazy uzavřených položek a starých reportů se nehlásí
        for target in links_in_value(note.fm or {}):
            self._check_target(note, target, "frontmatter")
        offset = (note.split.body_line - 1) if note.split else 0
        for link in extract_links(note.body, offset):
            self._check_target(note, link.target, f"řádek {link.line}")
        assets = (note.fm or {}).get("assets")
        if isinstance(assets, list):
            for p in assets:
                if isinstance(p, str) and p.startswith("/"):
                    if not (self.v.project_root / p.lstrip("/")).exists():
                        self.add("G6", note, f"cesta v assets neexistuje: {p}")

    def _check_target(self, note: Note, target: str, where: str) -> None:
        _rel, status = self.v.resolve(target)
        if status == "missing":
            self.add("G6", note, f"rozbitý odkaz [[{target}]] ({where})")
        elif status == "ambiguous":
            self.add("G6", note, f"nejednoznačný odkaz [[{target}]] ({where}); jména ve vaultu mají být jedinečná")

    # ------------------------------------------------------------ G7: přes celý vault
    def check_vault(self, notes: list[Note], full: bool = True) -> None:
        all_notes = [n for n in self.v.lint_notes() if n.fm]
        # víc master lore pro stejný kořen
        lore: dict = {}
        for n in all_notes:
            if n.fm.get("master") == "lore":
                ents = links_in_value(n.fm.get("entity"))
                key = (self.v.resolve(ents[0])[0] or ents[0].lower()) if ents else ""
                lore.setdefault(key, []).append(n)
        checked = {n.rel for n in notes}
        for key, ns in lore.items():
            if len(ns) > 1:
                names = ", ".join(sorted(x.name for x in ns))
                for n in ns:
                    if n.rel in checked:
                        self.add("G7", n, f"víc než jeden master lore pro stejný kořen: {names}")
        # alternative_to oboustranně
        for n in notes:
            if not n.fm:
                continue
            for target in links_in_value(n.fm.get("alternative_to")):
                other = self.v.note_by_name(target)
                if other is None or not other.fm:
                    continue
                back = {self.v.resolve(x)[0] for x in links_in_value(other.fm.get("alternative_to"))}
                if n.rel not in back:
                    self.add("G7", n, f"alternative_to jen jednostranně: {other.name} neodkazuje zpět",
                             severity="warning")
        if not full:
            return
        # krok z build_steps bez dokumentu v Steps/
        step_docs = {n.fm.get("build_step") for n in all_notes if n.fm.get("type") == "step"}
        step_files = {n.name for n in all_notes if n.rel.startswith("Steps/")}
        for sid in self.tx.build_steps:
            if sid not in step_docs and sid not in step_files:
                self.add("G7", None, f"krok {sid} z build_steps.yaml nemá dokument v Steps/",
                         file=self.v.project_rel(self.v.root / "Maintenance/taxonomy_local/build_steps.yaml"),
                         target=str(sid))
        # ue_map.yaml: položka s neexistující entitou (13 kap. 10.11)
        if self.tx.ue_map is not None:
            ents = {n.name for n in all_notes if n.fm.get("type") == "entity"}
            names = [it["entity"] for it in self.tx.ue_map["items"]]
            names += [e for e in self.tx.ue_map.get("placeholder_ignore_items") or {} if e not in names]
            for name in names:
                if name not in ents:
                    self.add("G6", None, f"ue_map: entita {name} neexistuje",
                             file=self.v.project_rel(self.tx.ue_map_path), target=name)
        # asset_sources.yaml: tvar (G7), soubor, proměnná a literál (G6) (13 kap. 10.18)
        if full and self.v.game_layer:
            man = library.load_manifest(self.v)
            for code, msg in (man.problems if man else []):
                self.add(code, None, msg, file=self.v.project_rel(man.path), target="asset_sources")
        # problémy lokální taxonomie
        for path, msg in self.tx.problems:
            self.add("G7", None, msg, file=self.v.project_rel(path), target=path.stem)


STRUCTURE_LOG_REL = "Maintenance/structure_log.md"


def check_structure_log(ch: Checker, note: Note) -> None:
    """Buňka `cr` v structure_log.md (13 kap. 10.8, zadání 0.22, CR-030): ani prázdná, ani `cr: <ID>`
    nebo `cr: none` → upozornění bez kódu G (formát logu, kap. 7)."""
    from .logs import LOG_LINE_RE, cr_cell, split_row
    for i, line in enumerate(note.text.replace("\r\n", "\n").split("\n"), start=1):
        if not LOG_LINE_RE.match(line):
            continue
        cells = split_row(line)
        if len(cells) < 6:
            continue
        state, value = cr_cell(cells[5])
        if state == "invalid":
            ch.add("log", note, f"řádek {i} ({cells[0]}): buňka cr {value!r} není prázdná ani cr: <ID> "
                                f"nebo cr: none; při exportu ji vyplní export_cr, nebo nastav cr: none",
                   severity="warning")


QUEUE_REL = "Maintenance/queue.md"


def role_profiles(vault: Vault) -> set[str]:
    """Jména profilů rolí (casefold): projektové `Roles/<Role>.md` a role core `_core/agents/<Role>.md`."""
    from . import CORE_ROOT
    from .frontmatter import parse
    names = {n.name.casefold() for rel, n in vault.notes.items()
             if rel.startswith("Roles/") and rel.count("/") == 1 and n.type == "role"}
    for p in (CORE_ROOT / "agents").glob("*.md"):
        fm, _sp = parse(p.read_text(encoding="utf-8"))
        if (fm or {}).get("type") == "role":
            names.add(p.stem.casefold())
    return names


def check_queue_roles(ch: Checker, note: Note) -> None:
    """Úkol pro roli (`code: role:<Role>`) odkazuje na existující profil, jinak G6 (13 kap. 10.17, zadání 0.24).
    Jen otevřené položky: uzavřené úkoly po zániku role šum nedělají (13 kap. 7)."""
    from .logs import parse_queue, role_of
    known = role_profiles(ch.v)
    for it in parse_queue(note.text):
        role = role_of(it.code)
        if it.kind == "task" and it.is_open and it.code.strip().lower().startswith("role:"):
            if not role:
                ch.add("G6", note, f"{it.id}: code {it.code!r} bez jména role (role:<Role>)", target=it.id)
            elif role.casefold() not in known:
                ch.add("G6", note, f"{it.id}: role {role} nemá profil (Roles/{role}.md ani role core)", target=it.id)


def run_checks(vault: Vault, notes: list[Note] | None = None, log_format: bool = True) -> list[Finding]:
    """G6 + G7 nad poznámkami (výchozí: všechny kontrolované poznámky vaultu); s `log_format` i formát
    structure_log (jen `lint` a `task_close`; audit ho do fronty nedává, 13 kap. 10.8)."""
    ch = Checker(vault)
    full = notes is None
    notes = vault.lint_notes() if notes is None else notes
    for n in notes:
        ch.check_frontmatter(n)
        ch.check_links(n)
        if log_format and n.rel == STRUCTURE_LOG_REL:
            check_structure_log(ch, n)
        if n.rel == QUEUE_REL:
            check_queue_roles(ch, n)
    ch.check_vault(notes, full)
    return ch.out
