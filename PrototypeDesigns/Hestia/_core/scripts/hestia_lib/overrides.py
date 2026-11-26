"""Lokální odchylky: náhrady modulů core (Steward, druhá verze; zadání 0.29; 13 kap. 10.23, 07 kap. 22, 04 G6).

- Lokální modul `Roles/modules/<id>.md` s `overrides: <module_id core>` nahradí modul core: `compose_role` ho vloží
  do kompilátů místo modulu core, `role_diff` porovnává lokální verzi. Kontrakt (`contract`) nahradit nejde; dvě
  náhrady téhož modulu nebo náhrada modulu, který core nemá = chyba konfigurace (`check_map`).
- Registr `Maintenance/local_overrides.md` (šablona `tpl_local_overrides`): tabulka
  `| id | modul core | lokální modul | důvod | CR | od verze | stav |`, stav `aktivní` / `zrušená` / `konflikt`.
  Aktivní záznam = stav `aktivní` nebo `konflikt` (náhrada dál platí, jen čeká na rozhodnutí).
- G6 (`problems`): lokální modul s `overrides` bez platného záznamu (`aktivní`/`konflikt`; i se záznamem `zrušená`,
  zadání 0.29.2), platný záznam bez lokálního modulu,
  `overrides` na modul, který core nemá.
- `update_core` (`core_changes`): náhrady, jejichž modul core nová verze mění (s rozdílem) nebo už nemá.
- Hlášení pro HearthLore (`report_table`): tabulka `| id | modul core | důvod | CR | stav |` z registru.
"""
from __future__ import annotations

import difflib
import re
from pathlib import Path

from .errors import ConfigError
from .fileio import read_text
from .frontmatter import FrontmatterError, parse

REGISTRY_REL = "Maintenance/local_overrides.md"
LOCAL_MODULES = "Roles/modules"
CONTRACT_ID = "contract"
STATES = ("aktivní", "zrušená", "konflikt")
ACTIVE = ("aktivní", "konflikt")
_ROW_RE = re.compile(r"^\|\s*L-\d+\s*\|")
_LINK_RE = re.compile(r"\[\[([^\]|#]+)")


def _fm(path: Path) -> dict:
    try:
        fm, _sp = parse(read_text(path))
    except (FrontmatterError, OSError, UnicodeDecodeError):
        return {}
    return fm if isinstance(fm, dict) else {}


def local_overrides(vault_root: Path) -> list[dict]:
    """Lokální moduly s `overrides`: [{id, overrides, rel}] seřazeně podle souboru."""
    d = Path(vault_root) / LOCAL_MODULES
    out = []
    for p in sorted(d.glob("*.md")) if d.is_dir() else []:
        fm = _fm(p)
        target = fm.get("overrides")
        if target not in (None, ""):
            out.append({"id": str(fm.get("module_id") or p.stem), "overrides": str(target).strip(),
                        "rel": f"{LOCAL_MODULES}/{p.name}"})
    return out


def core_module_ids(core_root: Path) -> set[str]:
    d = Path(core_root) / "agents" / "modules"
    return {p.stem for p in d.glob("*.md")} if d.is_dir() else set()


def check_map(local: list[dict], core_ids: set[str]) -> dict[str, str]:
    """{modul core: lokální modul}; chyba konfigurace u kontraktu, dvojité náhrady a neznámého modulu core
    (13 kap. 10.23). Používá `compose_role`."""
    out: dict[str, str] = {}
    for it in local:
        target = it["overrides"]
        if target.lower() in (CONTRACT_ID, "contract.md"):
            raise ConfigError(f"{it['rel']}: overrides: {target} – kontrakt (CONTRACT.md) nahradit nejde; "
                              "potřeba jiného kontraktu = CR (13 kap. 10.23)")
        if target not in core_ids:
            raise ConfigError(f"{it['rel']}: overrides: {target} – modul core {target} neexistuje")
        if target in out:
            raise ConfigError(f"dvě náhrady modulu core {target}: {out[target]}, {it['id']} (13 kap. 10.23)")
        out[target] = it["id"]
    return out


def load_registry(vault_root: Path) -> list[dict] | None:
    """Záznamy registru; None = registr chybí."""
    p = Path(vault_root) / REGISTRY_REL
    if not p.is_file():
        return None
    from .logs import split_row
    rows = []
    for line in read_text(p).replace("\r\n", "\n").split("\n"):
        if not _ROW_RE.match(line):
            continue
        c = (split_row(line) + [""] * 7)[:7]
        m = _LINK_RE.search(c[2])
        local = Path(m.group(1).strip()).stem if m else c[2].strip("` ")
        rows.append({"id": c[0], "core": c[1].strip("` "), "local": local, "reason": c[3], "cr": c[4],
                     "since": c[5], "state": c[6].strip().lower()})
    return rows


def problems(vault_root: Path, core_root: Path) -> list[tuple[str, str, str]]:
    """G6 (04 kap. 4, zadání 0.29): (cíl, soubor od kořene vaultu, zpráva)."""
    local = local_overrides(vault_root)
    rows = load_registry(vault_root)
    core_ids = core_module_ids(core_root)
    out = []
    active = {r["local"]: r for r in rows or [] if r["state"] in ACTIVE}
    for it in local:
        if it["overrides"] not in core_ids:
            out.append((it["id"], it["rel"], f"lokální náhrada {it['id']}: overrides: {it['overrides']} – modul "
                                             "core neexistuje (přejmenovaný nebo odebraný?)"))
        r = active.get(it["id"]) or active.get(Path(it["rel"]).stem)
        dead = [x for x in rows or [] if x["local"] in (it["id"], Path(it["rel"]).stem) and x["state"] == "zrušená"]
        if r is None and dead:                  # modul dál leží s overrides, záznam zrušený (zadání 0.29.2)
            out.append((it["id"], it["rel"], f"lokální náhrada {it['id']} (overrides: {it['overrides']}): záznam "
                                             f"{dead[-1]['id']} v {REGISTRY_REL} je zrušená; lokální modul přesuň "
                                             "do _to_delete/, nebo záznam vrať na aktivní"))
        elif r is None:
            out.append((it["id"], it["rel"], f"lokální náhrada {it['id']} (overrides: {it['overrides']}) nemá "
                                             f"platný záznam (aktivní/konflikt) v {REGISTRY_REL}" + (" (registr chybí)" if rows is None
                                                                                  else "")))
        elif r["core"] and r["core"] != it["overrides"]:
            out.append((it["id"], it["rel"], f"lokální náhrada {it['id']}: overrides: {it['overrides']}, v registru "
                                             f"{r['id']} modul core {r['core']}"))
    names = {it["id"] for it in local} | {Path(it["rel"]).stem for it in local}
    for r in rows or []:
        if r["state"] not in STATES:
            out.append((r["id"], REGISTRY_REL, f"záznam náhrady {r['id']}: neznámý stav {r['state']!r} "
                                               f"({' / '.join(STATES)})"))
        if r["state"] in ACTIVE and r["local"] not in names:
            out.append((r["id"], REGISTRY_REL, f"platný záznam náhrady {r['id']} ({r['core']}): lokální modul "
                                               f"{r['local']} s overrides v {LOCAL_MODULES}/ chybí"))
    return out


def core_changes(vault_root: Path, old_core: Path | None, new_core: Path) -> list[dict]:
    """Náhrady, jejichž modul core nová verze mění (`changed`, s rozdílem) nebo už nemá (`missing`); 13 kap. 10.23."""
    rows = {r["local"]: r for r in load_registry(vault_root) or []}
    out = []
    for it in local_overrides(vault_root):
        rel = f"agents/modules/{it['overrides']}.md"
        old_p = Path(old_core) / rel if old_core else None
        new_p = Path(new_core) / rel
        reg = rows.get(it["id"]) or {}
        base = {"id": reg.get("id") or "–", "local": it["id"], "core": it["overrides"], "file": it["rel"],
                "state": reg.get("state") or "bez záznamu"}
        if not new_p.is_file():
            out.append(dict(base, change="missing", diff=[]))
            continue
        old_t = read_text(old_p).replace("\r\n", "\n") if old_p is not None and old_p.is_file() else None
        new_t = read_text(new_p).replace("\r\n", "\n")
        if old_t is not None and old_t == new_t:
            continue
        diff = list(difflib.unified_diff((old_t or "").splitlines(), new_t.splitlines(),
                                         f"{it['overrides']} (stará verze)", f"{it['overrides']} (nová verze)",
                                         lineterm="")) if old_t is not None else []
        out.append(dict(base, change="changed", diff=diff))
    return out


def change_lines(changes: list[dict], with_diff: bool = True) -> list[str]:
    """Oddíl *Lokální odchylky* výpisu `update_core`."""
    if not changes:
        return []
    out = ["Lokální odchylky (náhrady modulů core, které nová verze mění; roztřídí Steward: platí dál / nová "
           "verze ji řeší / konflikt):"]
    for c in changes:
        what = ("modul core v nové verzi chybí – --apply se zastaví" if c["change"] == "missing"
                else "modul core se mění")
        out.append(f"  {c['id']} `{c['core']}` → lokální `{c['local']}` ({c['state']}): {what}")
        if with_diff and c["diff"]:
            out += ["    " + d for d in c["diff"]]
    return out


def counts(vault_root: Path) -> dict:
    rows = load_registry(vault_root)
    return {"registry": rows is not None,
            "active": sum(1 for r in rows or [] if r["state"] == "aktivní"),
            "conflict": sum(1 for r in rows or [] if r["state"] == "konflikt"),
            "local": len(local_overrides(vault_root))}


def report_table(vault_root: Path) -> list[str]:
    """Oddíl *Lokální odchylky* hlášení pro HearthLore (07 kap. 21): aktivní záznamy a záznamy v konfliktu."""
    rows = [r for r in load_registry(vault_root) or [] if r["state"] in ACTIVE]
    if not rows:
        return ["_Žádné lokální náhrady modulů core._"]
    out = ["| id | modul core | důvod | CR | stav |", "|---|---|---|---|---|"]
    out += [f"| {r['id']} | `{r['core']}` | {r['reason']} | {r['cr']} | {r['state']} |" for r in rows]
    return out

