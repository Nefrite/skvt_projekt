"""update_core --work-copy: přechod v lokální pracovní kopii vaultu (zadání 13 kap. 10.6, zadání 0.22, CR-023).

Pro vault na připojené složce (VM desktopové aplikace), kde přechod přes složku nestihne limit jednoho volání.
Jen s `--apply`; nezapíná se sám (doporučí ho `doctor`).

Pracovní adresář (mimo vault; bez hodnoty dočasný `hestia_work_*`):
- `<adresář>/<jméno vaultu>/` kopie vaultu; `hestia_work.json` značka a stav (originál, zdroj core, hotové
  fáze, časy); `snapshot.json` snímek originálu (relativní cesta, velikost a sha256 každého souboru).
- Podle značky `Vault.load` pozná kopii: `project_root`, `core_source` a cesty ve výstupech bere z originálu,
  takže kód, Unreal a git se čtou z původního projektu, jen čtením.

Fáze (`--work-phase copy|run|back`, bez přepínače všechny; další běh se stejným adresářem pokračuje od
nedokončené fáze; bez zadaného adresáře se najde nedokončený `hestia_work_*` téhož vaultu v dočasné složce):
1. **copy:** kopie vaultu a snímek originálu.
2. **run:** celý přechod v kopii (výměna `_core/`, kroky po aktualizaci, report). Přerušený přechod
   (core už vyměněn, kroky nedoběhly) dokončí kroky po aktualizaci.
3. **back:** kontrola originálu proti snímku (změněný, přibylý nebo zmizelý soubor, který není výsledkem
   dřívějšího zápisu zpět = kolize → nic se nezapíše, kód 1, pracovní adresář zůstává); zápis zpět bez
   mazání: změněné soubory přepíše na místě, nové založí, `_core/` vymění dvěma přejmenováními
   (`_core` → `_to_delete/_core_<verze>/`, `_core.new` → `_core`), zmizelý soubor přesune tam, kde je v kopii
   pod `_to_delete/` soubor se stejným hashem, jinak do `_to_delete/<cesta>`. Opakovatelné: dopíše jen rozdíly.
   Do oddílu přechodu v reportu připíše `### Pracovní kopie` (adresář, přenesené soubory, kontrola, časy fází).
Po úspěšném zápisu zpět pracovní adresář smaže; po kolizi nebo chybě ho nechá; `--keep-work-copy` vždy.

Selžou-li v kopii kroky po aktualizaci (kód 1), zápis zpět přesto proběhne (stejný stav jako přechod bez kopie:
nový core, oddíl „zbývá“), celkový kód je 1 a výpis doporučí `update_core --after-only --work-copy --apply`
(13 kap. 10.6 bod 8, zadání 0.22.1).

`--after-only --work-copy` (zadání 0.22.1): stejné fáze, ve fázi run jen kroky po aktualizaci nad `_core/` kopie
(bez zdroje core a bez výměny); režim (`mode`: `update` / `after_only`) je ve značce, další fáze ho převezmou.
Zvolený pracovní adresář se vypíše hned na začátku (stderr, i s `--quiet`), ve výsledku a v reportu, aby ho šlo
v dalším volání zadat výslovně (13 kap. 10.6 bod 6).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

from .errors import EXIT_FINDINGS, EXIT_OK, UsageError
from .fileio import read_text, to_posix
from .util import today
from .vault import WORK_MARKER, Vault

SNAPSHOT = "snapshot.json"
PHASES = ("copy", "run", "back")
PHASE_CZ = {"copy": "kopie", "run": "přechod", "back": "zápis zpět"}
TMP_PREFIX = "hestia_work_"
CORE_DIRS = ("_core", "_core.new")


# ---------------------------------------------------------------- soubory
def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _walk(root: Path):
    """(rel, cesta) všech souborů pod root, seřazeně; symbolické odkazy se nesledují."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        base = Path(dirpath)
        for name in sorted(filenames):
            p = base / name
            if p.is_symlink():
                continue
            yield to_posix(p.relative_to(root)), p


def scan(root: Path) -> dict[str, dict]:
    """rel -> {size, hash} všech souborů pod root."""
    out = {}
    if not root.is_dir():
        return out
    for rel, p in _walk(root):
        data = p.read_bytes()
        out[rel] = {"size": len(data), "hash": _sha(data)}
    return out


def _h(entry: dict | None) -> str | None:
    return entry["hash"] if entry else None


def _write_in_place(path: Path, data: bytes) -> None:
    """Zápis obsahu na místě (bez smazání a nového založení souboru; připojená složka)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


# ---------------------------------------------------------------- stav
def load_state(work: Path) -> dict | None:
    p = work / WORK_MARKER
    if not p.is_file():
        return None
    try:
        data = json.loads(read_text(p))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("hestia_work") == 1 else None


def save_state(work: Path, state: dict) -> None:
    (work / WORK_MARKER).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _same_vault(state: dict, vault: Vault) -> bool:
    try:
        return Path(state.get("origin") or "").resolve() == vault.home.resolve()
    except OSError:
        return False


def find_unfinished(vault: Vault) -> list[Path]:
    """Nedokončené pracovní adresáře téhož vaultu v dočasné složce (bez kolizních)."""
    out = []
    for d in sorted(Path(tempfile.gettempdir()).glob(TMP_PREFIX + "*")):
        st = load_state(d) if d.is_dir() else None
        if st and _same_vault(st, vault) and st.get("status") not in ("done", "collision"):
            out.append(d)
    return out


def resolve_work_dir(value: str, vault: Vault, phase: str | None) -> tuple[Path, dict | None]:
    """Pracovní adresář a uložený stav (None = nový běh)."""
    if value:
        work = Path(value).resolve()
        home = vault.home.resolve()
        if work == home or home in work.parents:
            raise UsageError(f"--work-copy {work}: pracovní adresář musí být mimo vault")
        if work.exists() and not work.is_dir():
            raise UsageError(f"--work-copy {work}: není adresář")
        state = load_state(work) if work.is_dir() else None
        if state is not None:
            if not _same_vault(state, vault):
                raise UsageError(f"--work-copy {work}: pracovní kopie jiného vaultu ({state.get('origin')})")
            return work, state
        if work.is_dir() and any(work.iterdir()):
            raise UsageError(f"--work-copy {work}: adresář není prázdný ani neobsahuje pracovní kopii tohoto vaultu")
        if phase in ("run", "back"):
            raise UsageError(f"--work-phase {phase}: v {work} není pracovní kopie (nejdřív --work-phase copy)")
        return work, None
    found = find_unfinished(vault)
    if len(found) > 1:
        raise UsageError("Víc nedokončených pracovních kopií tohoto vaultu; zadej --work-copy <adresář>: "
                         + ", ".join(str(d) for d in found))
    if found:
        return found[0], load_state(found[0])
    if phase in ("run", "back"):
        raise UsageError(f"--work-phase {phase}: nedokončená pracovní kopie nenalezena; zadej --work-copy <adresář>")
    return Path(tempfile.mkdtemp(prefix=TMP_PREFIX)), None


# ---------------------------------------------------------------- fáze copy
def phase_copy(vault: Vault, work: Path, progress) -> int:
    home = vault.home
    dst = work / home.name
    if dst.exists():                                         # nedokončená kopie z přerušeného běhu
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    snapshot = {}
    for dirpath, dirnames, _files in os.walk(home):          # i prázdné složky
        for d in dirnames:
            (dst / Path(dirpath).relative_to(home) / d).mkdir(parents=True, exist_ok=True)
    for rel, src in _walk(home):
        data = src.read_bytes()
        snapshot[rel] = {"size": len(data), "hash": _sha(data)}
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        st = src.stat()
        os.utime(target, ns=(st.st_atime_ns, st.st_mtime_ns))
    (work / SNAPSHOT).write_text(json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")
    progress(f"kopie vaultu do {dst} ({len(snapshot)} souborů)")
    return len(snapshot)


# ---------------------------------------------------------------- fáze run
def phase_run(args, vault: Vault, work: Path, state: dict, progress) -> tuple[int, dict, str]:
    from . import update_core as uc
    from . import upgrade as upgrade_mod
    copy = Vault.load(work / vault.home.name)
    if state.get("mode") == "after_only":
        return _after_in_copy(args, copy, state, progress, upgrade_mod)
    src = state.get("source") or {}
    if src.get("tag"):
        repo = uc.core_repo(copy)
        with tempfile.TemporaryDirectory(prefix="hestia_core_") as tmp:
            return _run_in_copy(args, copy, uc.export_tag(repo, src["tag"], Path(tmp)), src["tag"], state,
                                progress, uc, upgrade_mod)
    if not src.get("from"):
        raise UsageError("Pracovní kopie nemá zdroj core; zadej --from, --tag nebo --latest")
    return _run_in_copy(args, copy, Path(src["from"]), "", state, progress, uc, upgrade_mod)


def _after_in_copy(args, copy: Vault, state: dict, progress, upgrade_mod) -> tuple[int, dict, str]:
    """`--after-only` v kopii: kroky po aktualizaci nad `_core/` kopie (13 kap. 10.6 bod 8)."""
    progress("kroky po aktualizaci v kopii")
    ns = argparse.Namespace(**vars(args))
    ns.apply, ns.work_copy, ns.work_phase, ns.since = True, None, None, None
    code, payload, text = upgrade_mod.run_after(ns, copy)
    state.update({"run_started": True, "old": payload.get("since"), "new": payload.get("version"),
                  "report_rel": payload.get("report")})
    save_state(copy.root.parent, state)
    return code, payload, text


def _run_in_copy(args, copy: Vault, new_core: Path, tag: str, state: dict, progress, uc, upgrade_mod):
    new_v = uc.read_version(new_core)
    cur = copy.root / "_core"
    cur_v = uc.read_version(cur) if (cur / "VERSION").is_file() else None
    if state.get("run_started") and cur_v == new_v and state.get("old"):
        # přerušený přechod: core v kopii už vyměněn → jen kroky po aktualizaci (13 kap. 10.6)
        u = upgrade_mod.unfinished(copy, new_v)
        if u is None:
            progress("přechod v kopii už proběhl")
            return EXIT_OK, {"command": "update_core", "applied": True, "from": state["old"], "to": new_v}, \
                f"update_core: přechod {state['old']} -> {new_v} v pracovní kopii už proběhl"
        progress(f"dokončuji kroky po aktualizaci v kopii ({u['from']} -> {new_v})")
        code, after, err = uc.run_after_subprocess(copy, u["from"], getattr(args, "quiet", False))
        text = uc._after_text(after) if after else f"Chyba: kroky po aktualizaci neproběhly ({err})"
        return code, {"command": "update_core", "applied": True, "from": u["from"], "to": new_v, "after": after,
                      "after_error": err or None}, text
    state.update({"run_started": True, "old": cur_v, "new": new_v, "report_day": today().isoformat()})
    save_state(copy.root.parent, state)
    ns = argparse.Namespace(**vars(args))
    ns.apply, ns.work_copy, ns.work_phase = True, None, None
    return uc._run(ns, copy, new_core, tag)


# ---------------------------------------------------------------- fáze back
def _trash_name(copy_files: dict, snapshot: dict, state: dict) -> str | None:
    """Jméno `_to_delete/_core_<verze>[_N]`, kam přechod v kopii přesunul starý core."""
    if state.get("trash"):
        return state["trash"]
    names = {rel.split("/")[1] for rel in copy_files if rel.startswith("_to_delete/_core_")}
    old = {rel.split("/")[1] for rel in snapshot if rel.startswith("_to_delete/_core_")}
    new = sorted(names - old)
    return new[-1] if new else None


def _sub(files: dict, prefix: str) -> dict[str, str]:
    return {rel[len(prefix):]: e["hash"] for rel, e in files.items() if rel.startswith(prefix)}


def plan_back(home: Path, copy: Path, snapshot: dict, state: dict) -> dict:
    """Porovnání originálu, snímku a kopie: kolize a co zapsat."""
    C, O = scan(copy), scan(home)
    S = snapshot
    trash = _trash_name(C, S, state)
    core_area = tuple(f"{d}/" for d in CORE_DIRS) + ((f"_to_delete/{trash}/",) if trash else ())
    moved = state.get("moved") or {}                          # cíl -> {from, hash} z dřívějšího zápisu zpět
    collisions = []
    for p in sorted(set(S) | set(O) | set(C)):
        if p.startswith(core_area):
            continue
        o, s, c = _h(O.get(p)), _h(S.get(p)), _h(C.get(p))
        if o in (s, c) or (p in moved and o == moved[p]["hash"]):
            continue
        collisions.append(p if o is not None else f"{p} (zmizel)" if s is not None else p)
    core_new, core_snap, core_orig = _sub(C, "_core/"), _sub(S, "_core/"), _sub(O, "_core/")
    swap = bool(trash) and core_new != core_snap
    if swap:
        if (home / "_core").is_dir() and core_orig not in (core_snap, core_new):
            collisions.append("_core/ (core v originálu změněn)")
        t_orig = _sub(O, f"_to_delete/{trash}/")
        if t_orig and t_orig != core_snap and not _sub(S, f"_to_delete/{trash}/"):
            collisions.append(f"_to_delete/{trash}/ (v originálu už existuje)")
    # zmizelé v kopii → přesun; změněné a nové → zápis
    moves, writes = [], []
    taken = set()
    for p in sorted(O):
        if p.startswith(core_area) or p in C or _h(O[p]) != _h(S.get(p)):
            continue
        h = O[p]["hash"]
        cands = [q for q in sorted(C) if q.startswith("_to_delete/") and not q.startswith(core_area)
                 and C[q]["hash"] == h and q not in O and q not in S and q not in taken]
        cands.sort(key=lambda q: (Path(q).name != Path(p).name, q))
        if cands:
            q = cands[0]
        else:
            q, n = f"_to_delete/{p}", 2
            while q in O or q in C or q in taken:
                stem, dot, ext = p.rpartition(".")
                q = f"_to_delete/{stem}_{n}.{ext}" if dot and "/" not in ext else f"_to_delete/{p}_{n}"
                n += 1
        taken.add(q)
        moves.append((p, q, h))
    for p in sorted(C):
        if p.startswith(core_area) or p in taken:
            continue
        if _h(O.get(p)) != C[p]["hash"]:
            writes.append((p, "modify" if p in O else "create"))
    done = (home / "_core").is_dir() and core_orig == core_new
    return {"collisions": collisions, "moves": moves, "writes": writes, "trash": trash,
            "swap": swap and not done, "core_files": len(core_new), "checked": len(S)}


def _swap_core(home: Path, copy: Path, trash: str) -> None:
    """`_core.new` z kopie, pak `_core` → `_to_delete/<trash>/` a `_core.new` → `_core` (pokračuje i po přerušení)."""
    stage = home / "_core.new"
    want = scan(copy / "_core")
    have = scan(stage)
    for rel, e in want.items():
        if _h(have.get(rel)) != e["hash"]:
            _write_in_place(stage / rel, (copy / "_core" / rel).read_bytes())
    for dirpath, dirnames, _f in os.walk(copy / "_core"):
        for d in dirnames:
            (stage / Path(dirpath).relative_to(copy / "_core") / d).mkdir(parents=True, exist_ok=True)
    target = home / "_to_delete" / trash
    if (home / "_core").is_dir():
        target.parent.mkdir(parents=True, exist_ok=True)
        os.rename(home / "_core", target)
    os.rename(stage, home / "_core")


def phase_back(vault: Vault, work: Path, state: dict, progress) -> tuple[int, dict, list[str]]:
    home, copy = vault.home, work / vault.home.name
    snapshot = json.loads(read_text(work / SNAPSHOT))
    pl = plan_back(home, copy, snapshot, state)
    info = {"collisions": pl["collisions"], "modified": [p for p, a in pl["writes"] if a == "modify"],
            "created": [p for p, a in pl["writes"] if a == "create"],
            "moved": [{"from": p, "to": q} for p, q, _h2 in pl["moves"]], "core_swapped": pl["swap"],
            "trash": pl["trash"]}
    if pl["collisions"]:
        state["status"] = "collision"
        return EXIT_FINDINGS, info, [
            f"Kolize: originál se od snímku změnil ({len(pl['collisions'])} souborů); nic se nezapsalo, "
            f"pracovní kopie zůstává v {work}:", *[f"  ! {c}" for c in pl["collisions"]],
            "Spusť přechod znovu s novou pracovní kopií (originál má přednost)."]
    state["trash"] = pl["trash"]
    moved = state.setdefault("moved", {})
    for p, q, h in pl["moves"]:
        moved[q] = {"from": p, "hash": h}
        save_state(work, state)
        (home / q).parent.mkdir(parents=True, exist_ok=True)
        os.rename(home / p, home / q)
    if pl["swap"]:
        _swap_core(home, copy, pl["trash"])
    for p, _a in pl["writes"]:
        _write_in_place(home / p, (copy / p).read_bytes())
    for dirpath, dirnames, _f in os.walk(copy):              # prázdné složky z kopie
        for d in dirnames:
            rel = Path(dirpath).relative_to(copy) / d
            if not to_posix(rel).startswith(CORE_DIRS) and not (home / rel).exists():
                (home / rel).mkdir(parents=True, exist_ok=True)
    progress(f"zápis zpět: změněné {len(info['modified'])}, nové {len(info['created'])}, "
             f"přesunuté {len(info['moved'])}" + (", _core/ vyměněn" if pl["swap"] else ""))
    return EXIT_OK, info, []


# ---------------------------------------------------------------- report
def report_lines(work: Path, state: dict, info: dict, checked: int | None) -> list[str]:
    t = state.get("times") or {}
    times = ", ".join(f"{PHASE_CZ[ph]} {t[ph]:.1f} s" for ph in PHASES if ph in t)
    lines = ["", "### Pracovní kopie", f"- Pracovní adresář: `{to_posix(work)}`.",
             "- Kontrola originálu: beze změny od snímku" + (f" ({checked} souborů)." if checked else ".")]
    lines.append(f"- Přeneseno: změněné {len(info['modified'])}, nové {len(info['created'])}, "
                 f"přesunuté {len(info['moved'])}"
                 + (f"; `_core/` vyměněn (starý v `_to_delete/{info['trash']}/`)." if info["core_swapped"] else "."))
    lines += [f"  - ~ `{p}`" for p in info["modified"]] + [f"  - + `{p}`" for p in info["created"]]
    lines += [f"  - → `{m['from']}` → `{m['to']}`" for m in info["moved"]]
    lines.append(f"- Čas fází: {times or '–'}.")
    return lines


def add_report_section(vault: Vault, work: Path, state: dict, lines: list[str]) -> str | None:
    """`### Pracovní kopie` na konec oddílu přechodu v reportu (kopie i originál, zápis na místě)."""
    from . import upgrade as upgrade_mod
    day, old, new = state.get("report_day"), state.get("old"), state.get("new")
    rel = state.get("report_rel")
    if not new or not (rel or day):
        return None
    rel = rel or to_posix(Path(upgrade_mod.REPORTS_REL) / f"update_core_{day}.md")
    p = work / vault.home.name / rel
    if not p.is_file():
        return None
    cur = read_text(p).replace("\r\n", "\n")
    heading = upgrade_mod.section_heading(old, new)
    found = list(re.finditer(rf"^{re.escape(heading)}\n.*?(?=^## |\Z)", cur, re.M | re.S))
    block = "\n".join(lines) + "\n"
    if found:
        m = found[-1]
        sec = cur[m.start():m.end()]
        sec = re.sub(r"\n### Pracovní kopie\n.*?(?=\n### |\n## |\Z)", "", sec, flags=re.S)   # opakovaný zápis
        new_text = cur[:m.start()] + sec.rstrip("\n") + "\n" + block + ("\n" + cur[m.end():] if cur[m.end():] else "")
    else:
        new_text = cur.rstrip("\n") + "\n" + block
    data = new_text.encode("utf-8")
    p.write_bytes(data)
    _write_in_place(vault.home / rel, data)
    return rel


# ---------------------------------------------------------------- řízení
def run(args, vault: Vault) -> tuple[int, dict, str]:
    from .update_core import resolve_tag, core_repo
    phase = getattr(args, "work_phase", None)
    keep = getattr(args, "keep_work_copy", False)
    quiet = getattr(args, "quiet", False)

    def progress(msg: str) -> None:
        if not quiet:
            print(f"update_core --work-copy: {msg}", file=sys.stderr, flush=True)

    after_only = bool(getattr(args, "after_only", False))
    work, state = resolve_work_dir(args.work_copy or "", vault, phase)
    resumed = state is not None
    if state is None:
        state = {"hestia_work": 1, "origin": str(vault.home.resolve()), "vault": vault.home.name,
                 "mode": "after_only" if after_only else "update", "status": "running", "done": [], "times": {}}
    mode = state.get("mode") or "update"
    if "run" not in state["done"] and after_only and mode != "after_only":
        raise UsageError(f"Pracovní kopie {work} je pro přechod na novou verzi, ne pro --after-only; "
                         f"pokračuj bez --after-only, nebo zadej jiný --work-copy")
    if mode == "after_only" and (args.source or args.tag or args.latest):
        raise UsageError(f"Pracovní kopie {work} je pro --after-only; zdroj core (--from, --tag, --latest) nebere")
    # zvolený adresář hned na výstup (i s --quiet), aby ho šlo zadat v dalším volání (13 kap. 10.6 bod 6)
    print(f"update_core --work-copy: pracovní adresář {work}" + (" (pokračování)" if resumed else ""),
          file=sys.stderr, flush=True)
    if args.source or args.tag or args.latest:
        src = {"from": str(Path(args.source).resolve())} if args.source else \
            {"tag": resolve_tag(args, core_repo(vault))}
        if "run" in state["done"] and state.get("source") and state["source"] != src:
            raise UsageError(f"Pracovní kopie {work} už má přechod ze zdroje {state['source']}; zdroj nejde měnit")
        state["source"] = src
    todo = [p for p in PHASES if p not in state["done"]]
    if phase:
        if phase in state["done"]:
            todo = []
        else:
            need = PHASES[PHASES.index(phase) - 1] if phase != "copy" else None
            if need and need not in state["done"]:
                raise UsageError(f"--work-phase {phase}: nejdřív fáze {need} ({work})")
            todo = [phase]
    if "run" in todo and mode != "after_only" and not state.get("source"):
        raise UsageError("Zadej zdroj core: --from <cesta k hestia/>, --tag vX.Y.Z nebo --latest (s core_source)")
    work.mkdir(parents=True, exist_ok=True)
    save_state(work, state)
    lines = [f"update_core --work-copy: pracovní adresář {work}" + (" (pokračování)" if resumed else "")]
    if phase and not todo:
        lines.append(f"Fáze {phase} už proběhla.")
    payload: dict = {"command": "update_core", "applied": False}
    code, info, checked = EXIT_OK, None, None
    try:
        for ph in todo:
            t0 = time.monotonic()
            if ph == "copy":
                phase_copy(vault, work, progress)
            elif ph == "run":
                rc, payload, text = phase_run(args, vault, work, state, progress)
                lines.append(text)
                state["run_code"] = rc
                code = max(code, rc)
                if rc != EXIT_OK:                            # 13 kap. 10.6 bod 8
                    lines.append("Zápis zpět proběhne i tak (nový core, kroky, které zbývají, v reportu). Zbývající "
                                 "kroky doběhnou: update_core --after-only --work-copy --apply (na lokálním disku "
                                 "i bez --work-copy).")
            else:
                checked = len(json.loads(read_text(work / SNAPSHOT)))
                rc, info, msg = phase_back(vault, work, state, progress)
                lines += msg
                if rc != EXIT_OK:
                    save_state(work, state)
                    payload["work_copy"] = {"dir": str(work), "phase": ph, "back": info}
                    return rc, payload, "\n".join(lines)
            state["times"][ph] = round(time.monotonic() - t0, 2)
            state["done"].append(ph)
            save_state(work, state)
    except BaseException:
        print(f"update_core --work-copy: přerušeno; pracovní adresář zůstává: {work} "
              f"(další běh se stejným adresářem pokračuje)", file=sys.stderr, flush=True)
        raise
    code = max(code, state.get("run_code") or 0)
    payload["work_copy"] = {"dir": str(work), "mode": mode, "done": state["done"], "times": state["times"],
                            "back": info}
    if info is not None:
        rel = add_report_section(vault, work, state, report_lines(work, state, info, checked))
        lines.append(f"Zápis zpět: změněné {len(info['modified'])}, nové {len(info['created'])}, "
                     f"přesunuté {len(info['moved'])}" + ("; _core/ vyměněn" if info["core_swapped"] else "")
                     + (f"; report {rel}" if rel else ""))
        state["status"] = "done"
        save_state(work, state)
        if keep:
            lines.append(f"Pracovní adresář ponechán (--keep-work-copy): {work}")
        else:
            shutil.rmtree(work, ignore_errors=True)
            lines.append(f"Pracovní adresář smazán: {work}")
    elif "back" not in state["done"]:
        nxt = next(p for p in PHASES if p not in state["done"])
        lines.append(f"Další fáze: update_core{' --after-only' if mode == 'after_only' else ''} "
                     f"--work-copy {work} --work-phase {nxt} --apply")
    lines.append("Čas fází: " + (", ".join(f"{PHASE_CZ[p]} {state['times'][p]:.1f} s" for p in PHASES
                                          if p in state["times"]) or "–"))
    payload["applied"] = "back" in state["done"]
    return code, payload, "\n".join(l for l in lines if l)
