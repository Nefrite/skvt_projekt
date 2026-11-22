"""Příkaz export_cr: poznatky instance jako change requesty (zadání 13 kap. 10.8, 11 kap. 3, 07 kap. 11).

- Jeden záznam `structure_log.md` = jeden CR v `Maintenance/outbox/CR_RRRR-MM-DD_<short_name>.md`.
- Exportují se záznamy bez vyplněného `cr:` v kategoriích friction, missing, surplus, collision, taxonomy,
  idea; `works` jen s `--include-works`. Vyplněné je jen `cr: <ID>` (`CR_RRRR-MM-DD_<short_name>` nebo
  `CR-NNN_<short_name>`) a `cr: none`; prázdná buňka, `–`, `-`, samotné `cr:` a jiný text = nevyplněno
  (zadání 0.22, CR-030). Vyplnění nevyplněnou hodnotu nahradí.
- CR vzniká ze šablony `templates/tpl_change_request.md`: `cr_status: new`, `source_instance`
  (`instance` z config.yaml, jinak jméno složky projektu), `hestia_version` (`_core/VERSION`),
  `structure_log` (citace záznamu), `area` (`--area`, jinak taxonomy → taxonomy, ostatní → process),
  `gd_relevance` prázdné, *Průběh* (tabulka) s řádkem `| datum | new | export_cr | … |`.
- Po zápisu se u záznamu vyplní `cr: <ID>` – jediná povolená úprava existujícího řádku logu.
- Předání do HearthLore (zadání 0.22.1): export soubor neodesílá. Soubor z `outbox/` se uvede v hlášení pro
  HearthLore, nebo ho předá člověk; instance ho nepřejmenovává, nečísluje ani nekopíruje do HearthLore. Zaeviduje
  ho agent HearthLore (číslo, `CR-NNN_<short_name>`, původní jméno v `source_id`). Totéž říká poznámka pod
  nadpisem CR (`HANDOVER_NOTE`) a výpis příkazu.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from . import CORE_ROOT, core_version
from .changeset import ChangeSet
from .errors import EXIT_OK, UsageError
from .fileio import detect_newline, read_text
from .frontmatter import set_field
from .logs import LOG_LINE_RE, cr_cell, escape, format_line, split_row
from .util import today
from .vault import Vault

LOG_REL = "Maintenance/structure_log.md"
OUTBOX_REL = "Maintenance/outbox"
TEMPLATE = "templates/tpl_change_request.md"
EXPORTED = ["friction", "missing", "surplus", "collision", "taxonomy", "idea"]
FIELDS = ["date", "category", "description", "impact", "proposal", "cr"]
SHORT_MAX = 40
TODO = "<!-- doplní Curator nebo člověk před odesláním -->"
HANDOVER_NOTE = ("> **Předání do HearthLore:** soubor se neodesílá skriptem. Uveď ho v hlášení pro HearthLore, nebo "
                 "ho předá člověk; v instanci ho nepřejmenovávej, nečísluj ani nekopíruj do HearthLore. Zaeviduje "
                 "ho agent HearthLore: číslo, jméno `CR-NNN_<short_name>`, původní jméno v `source_id` "
                 "(11 kap. 3).")


@dataclass
class Record:
    line: int                 # index řádku v structure_log.md
    cells: list[str]

    def get(self, name: str) -> str:
        i = FIELDS.index(name)
        return self.cells[i] if i < len(self.cells) else ""

    @property
    def cr(self) -> str:
        """Vyplněné `cr` (ID nebo `none`, bez předpony `cr:`), jinak prázdné. `–`, `-`, samotné `cr:`
        a jiný text = nevyplněno (zadání 0.22, CR-030)."""
        state, value = cr_cell(self.get("cr"))
        return value if state in ("id", "none") else ""

    @property
    def citation(self) -> str:
        """Citace záznamu do frontmatteru CR (11 kap. 3): `datum | kategorie | popis`."""
        return " | ".join(escape(self.get(f)) for f in ("date", "category", "description"))


def short_name(text: str) -> str:
    """ASCII, malá písmena, podtržítka, nejvýš 40 znaků (13 kap. 10.8)."""
    s = unicodedata.normalize("NFKD", text)
    s = "".join(c for c in s if not unicodedata.combining(c)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    if len(s) > SHORT_MAX:
        cut = s[:SHORT_MAX]
        if s[SHORT_MAX] != "_" and "_" in cut:          # nekrájet slovo
            cut = cut[:cut.rfind("_")]
        s = cut.strip("_")
    return s or "cr"


def records(text: str) -> list[Record]:
    lines = text.replace("\r\n", "\n").split("\n")
    return [Record(i, split_row(line)) for i, line in enumerate(lines) if LOG_LINE_RE.match(line)]


def source_instance(vault: Vault) -> str:
    return str(vault.config.get("instance") or vault.project_root.name)


def hestia_version(vault: Vault) -> str:
    p = vault.root / "_core" / "VERSION"
    return read_text(p).strip() if p.is_file() else core_version()


def _fill_sections(body: str, content: dict[str, str]) -> str:
    """Za nadpis `## <sekce>` vloží obsah; komentář a tabulku pod nadpisem přeskočí (řádek tabulky
    *Průběhu* tak přijde pod její záhlaví)."""
    def keep(j: int) -> bool:
        s = lines[j].strip()
        if s.startswith("<!--") or s.startswith("|"):
            return True
        return not s and j + 1 < len(lines) and lines[j + 1].strip().startswith(("|", "<!--"))

    lines = body.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        m = re.match(r"^## (.+?)\s*$", lines[i])
        if m and m.group(1) in content:
            while i + 1 < len(lines) and keep(i + 1):
                i += 1
                out.append(lines[i])
            out += content[m.group(1)].split("\n")
            if i + 1 < len(lines) and lines[i + 1].strip():
                out.append("")
        i += 1
    return "\n".join(out)


def render(template: str, rec: Record, cr_id: str, vault: Vault, area: str, date) -> str:
    text = template.replace("\r\n", "\n").replace("{{date:YYYY-MM-DD}}", date.isoformat())
    text = text.replace("{{title}}", rec.get("description").strip() or cr_id)
    text = text.replace("\n## Co se stalo", f"\n{HANDOVER_NOTE}\n\n## Co se stalo", 1)
    for key, value in (("cr_status", "new"), ("source_instance", source_instance(vault)),
                       ("hestia_version", hestia_version(vault)), ("area", area),
                       ("structure_log", [rec.citation])):
        text = set_field(text, key, value, section="orchestration")
    what = rec.get("description").strip()
    if rec.get("impact").strip():
        what += f"\n\nDopad podle záznamu: {rec.get('impact').strip()}"
    what += (f"\n\nZáznam `structure_log` z {rec.get('date')} (kategorie `{rec.get('category')}`), "
             f"instance `{source_instance(vault)}`, core {hestia_version(vault)}.")
    content = {
        "Co se stalo": what,
        "Návrh": rec.get("proposal").strip() or TODO,
        "Dopad": TODO,
        "Alternativy": TODO,
        "Průběh": format_line([date.isoformat(), "new", "export_cr", f"ze structure_log {rec.get('date')}"]),
    }
    return _fill_sections(text, content).rstrip("\n") + "\n"


def mark_record(text: str, rec: Record, cr_id: str, date) -> str:
    """Vyplní `cr: <ID>` u jednoho řádku logu; ostatní řádky beze změny."""
    nl = detect_newline(text)
    lines = text.replace("\r\n", "\n").split("\n")
    cells = rec.cells + [""] * (len(FIELDS) - len(rec.cells))
    cells[FIELDS.index("cr")] = f"cr: {cr_id}"
    lines[rec.line] = format_line(cells)
    out = nl.join(lines)
    return set_field(out, "updated", date, section="orchestration")


def plan(vault: Vault, cs: ChangeSet, area: str | None, include_works: bool) -> tuple[list[dict], list[dict]]:
    log = vault.root / LOG_REL
    if not log.is_file():
        return [], []
    text = read_text(log)
    allowed = EXPORTED + (["works"] if include_works else [])
    template = read_text(CORE_ROOT / TEMPLATE)
    date = today()
    outbox = vault.root / OUTBOX_REL
    exported, skipped = [], []
    for rec in records(text):
        cat = rec.get("category").strip()
        if rec.cr:
            continue
        if cat not in allowed:
            skipped.append({"record": rec.citation,
                            "reason": "works: jen s --include-works" if cat == "works" else f"kategorie {cat!r}"})
            continue
        base = f"CR_{date.isoformat()}_{short_name(rec.get('description'))}"
        cr_id, n = base, 1
        while cs.exists(outbox / f"{cr_id}.md"):
            n += 1
            cr_id = f"{base}_{n}"
        rec_area = area or ("taxonomy" if cat == "taxonomy" else "process")
        cs.write(outbox / f"{cr_id}.md", render(template, rec, cr_id, vault, rec_area, date))
        text = mark_record(text, rec, cr_id, date)
        exported.append({"id": cr_id, "path": cs.rel(outbox / f"{cr_id}.md"), "record": rec.citation,
                         "area": rec_area})
    if exported:
        cs.write(log, text)
    return exported, skipped


def run(args, vault: Vault) -> tuple[int, dict, str]:
    areas = vault.taxonomy.enum_values("cr_area")
    if args.area and args.area not in areas:
        raise UsageError(f"Neznámá oblast --area {args.area!r} (povolené: {', '.join(areas)})")
    cs = ChangeSet(vault.project_root)
    exported, skipped = plan(vault, cs, args.area, args.include_works)
    if args.apply and not cs.empty:
        cs.apply()
    payload = {"command": "export_cr", "applied": bool(args.apply and exported), "exported": exported,
               "skipped": skipped, "changes": cs.summary()}
    lines = []
    if not (vault.root / LOG_REL).is_file():
        lines.append(f"export_cr: {LOG_REL} neexistuje, není co exportovat")
    elif not exported:
        lines.append("export_cr: žádný záznam k exportu (všechny mají cr: nebo jsou mimo exportované kategorie)")
    else:
        state = "zapsáno" if args.apply else "zapsalo by se (dry-run, zapiš s --apply)"
        lines.append(f"export_cr: {len(exported)} CR do {OUTBOX_REL}/ – {state}")
        lines += [f"  {e['id']} (area {e['area']}) ← {e['record']}" for e in exported]
        if not args.apply:
            lines.append(cs.diff())
        lines.append("Dopad a Alternativy doplní Curator nebo člověk. Předání do HearthLore: soubory z outbox/ uveď "
                     "v hlášení pro HearthLore, nebo je předá člověk; nepřejmenovávat, nečíslovat, nekopírovat "
                     "(zaeviduje agent HearthLore).")
    lines += [f"Přeskočeno: {s['record']} ({s['reason']})" for s in skipped]
    return EXIT_OK, payload, "\n".join(l for l in lines if l)
