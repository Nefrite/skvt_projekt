"""Příkaz doctor: kontrola prostředí (zadání 13 kap. 10.15, zadání 0.22, CR-022).

Jen čte, nic nezapisuje, bez sítě. Každá kontrola má výsledek OK, UPOZORNĚNÍ nebo CHYBA a u toho, co neprošlo,
návod. Část Python a PyYAML běží i bez PyYAML (modul nic z core závislého na PyYAML na začátku neimportuje;
config.yaml se bez PyYAML čte záložně po řádcích).

- Python >= 3.11 (verze, interpret), PyYAML (verze);
- git (verze), vault v gitovém repozitáři, počet necommitnutých změn (upozornění);
- vault nalezen (`--vault` nebo nejbližší `Hestia/`), `_core/VERSION`, právo zápisu do vaultu (bez zápisu souboru);
- `core_source`: existuje, je repozitář se značkami `vX.Y.Z`, nejvyšší značka proti `_core/VERSION`;
- připojená složka: na Linuxu typ souborového systému vaultu podle `/proc/mounts` (fuse, 9p, virtiofs, cifs …)
  → upozornění s doporučením `update_core --work-copy` (13 kap. 10.6). Proměnná `HESTIA_PROC_MOUNTS` nahradí
  cestu k `/proc/mounts` (testy) a kontrolu zapne i mimo Linux.
Návratový kód 0 bez chyby, 1 s chybou.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from . import envcheck
from .errors import EXIT_FINDINGS, EXIT_OK

OK, WARN, ERR = "ok", "warning", "error"
STATUS_CZ = {OK: "OK", WARN: "UPOZORNĚNÍ", ERR: "CHYBA"}
REMOTE_FS = ("fuse", "9p", "virtiofs", "cifs", "smb", "smb2", "smb3", "smbfs", "nfs", "nfs4", "vboxsf",
             "drvfs", "sshfs", "davfs", "prl_fs", "vmhgfs")
TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
WORK_COPY_HINT = ("pro dlouhé běhy (update_core) použij update_core --work-copy --apply: přechod proběhne "
                  "v lokální kopii a zapíše se zpět bez mazání")


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None


def _vt(tag: str) -> tuple[int, int, int]:
    return tuple(int(x) for x in TAG_RE.match(tag).groups())


def find_vault(arg: str | None) -> Path | None:
    if arg:
        p = Path(arg).resolve()
        return p if p.is_dir() else None
    p = Path.cwd().resolve()
    for cand in [p, *p.parents]:
        if cand.name == "Hestia" and cand.is_dir():
            return cand
        if (cand / "Hestia").is_dir():
            return cand / "Hestia"
    return None


def read_config(vault: Path) -> dict:
    """config.yaml přes PyYAML, bez něj záložně jednoduché klíče `klíč: hodnota` na nejvyšší úrovni."""
    p = vault / "Maintenance" / "config.yaml"
    if not p.is_file():
        return {}
    text = p.read_text(encoding="utf-8")
    try:
        import yaml
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    except ImportError:
        out = {}
        for line in text.splitlines():
            m = re.match(r"^([A-Za-z_][\w]*):\s*(.*?)\s*(?:#.*)?$", line)
            if m and m.group(2):
                out[m.group(1)] = m.group(2).strip("\"'")
        return out
    except Exception:                                        # chybný YAML ohlásí jiné příkazy
        return {}


def mount_fs(path: Path, mounts_file: str | None = None) -> tuple[str, str] | None:
    """(přípojný bod, typ FS) nejdelšího přípojného bodu nad cestou podle /proc/mounts; None = nelze určit."""
    src = mounts_file or os.environ.get("HESTIA_PROC_MOUNTS")
    if not src:
        if not sys.platform.startswith("linux"):
            return None
        src = "/proc/mounts"
    try:
        lines = Path(src).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    target = path.as_posix()
    best = None
    for line in lines:
        parts = line.split()
        if len(parts) < 3:
            continue
        mp = parts[1].replace("\\040", " ")
        if target == mp or target.startswith(mp.rstrip("/") + "/") or mp == "/":
            if best is None or len(mp) > len(best[0]):
                best = (mp, parts[2])
    return best


def is_remote_fs(fstype: str) -> bool:
    t = fstype.lower()
    return t in REMOTE_FS or t.startswith("fuse.") or t.startswith("fuse")


def checks(vault_arg: str | None, version_info=None, yaml_importer=None, mounts_file: str | None = None) -> list[dict]:
    out: list[dict] = []

    def add(name: str, status: str, message: str, help_: str = "") -> None:
        out.append({"name": name, "status": status, "message": message, "help": help_})

    ok, msg = envcheck.check_python(version_info)
    add("python", OK if ok else ERR, msg, "" if ok else envcheck.HELP)
    ok, msg = envcheck.check_yaml(yaml_importer)
    add("pyyaml", OK if ok else ERR, msg, "" if ok else envcheck.HELP)

    r = _git(Path.cwd(), "--version")
    has_git = bool(r and r.returncode == 0)
    add("git", OK if has_git else WARN, r.stdout.strip() if has_git else "git nenalezen",
        "" if has_git else "nainstaluj git (bez něj nejde update_core --tag/--latest a lint změněných souborů)")

    vault = find_vault(vault_arg)
    if vault is None:
        add("vault", ERR, f"vault nenalezen ({vault_arg})" if vault_arg else "vault Hestia/ nenalezen",
            "zadej --vault <cesta k Hestia/> nebo spusť příkaz ve složce projektu")
        return out
    add("vault", OK, f"vault {vault}")
    ver_p = vault / "_core" / "VERSION"
    core_v = ver_p.read_text(encoding="utf-8").strip() if ver_p.is_file() else None
    add("core", OK if core_v else ERR, f"_core/VERSION {core_v}" if core_v else "_core/VERSION chybí",
        "" if core_v else "vault nemá core; doplň ho update_core --from <cesta k hestia/> nebo init")
    writable = all(os.access(p, os.W_OK) for p in (vault, vault / "Maintenance") if p.exists())
    add("write", OK if writable else ERR, "právo zápisu do vaultu" if writable else "do vaultu nejde zapisovat",
        "" if writable else "ověř oprávnění složky (připojená složka jen ke čtení?)")

    if has_git:
        r = _git(vault, "rev-parse", "--show-toplevel")
        if r and r.returncode == 0:
            add("git_repo", OK, f"vault je v repozitáři {r.stdout.strip()}")
            r = _git(vault, "status", "--porcelain", "--", ".")
            n = len([l for l in (r.stdout if r else "").splitlines() if l.strip()])
            add("git_changes", WARN if n else OK, f"necommitnutých změn ve vaultu: {n}",
                "před update_core --apply commitni (11 kap. 6, krok 2)" if n else "")
        else:
            add("git_repo", WARN, "vault není v gitovém repozitáři",
                "bez gitu chybí historie změn a lint bez argumentů kontroluje celý vault")

    cfg = read_config(vault)
    cs = cfg.get("core_source")
    if not cs:
        add("core_source", WARN, "core_source v config.yaml chybí",
            "doplň core_source (cesta k repozitáři HearthLore relativně k vaultu), jinak jen update_core --from")
    else:
        repo = (vault / str(cs)).resolve()
        r = _git(repo, "tag", "--list", "v*") if repo.is_dir() and has_git else None
        if not repo.is_dir():
            add("core_source", ERR, f"core_source {cs!r} ({repo}) neexistuje", "oprav cestu v config.yaml")
        elif r is None or r.returncode != 0:
            add("core_source", ERR, f"core_source {cs!r} ({repo}) není git repozitář (nebo chybí git)",
                "oprav cestu v config.yaml na kořen repozitáře HearthLore")
        else:
            tags = sorted((t for t in r.stdout.split() if TAG_RE.match(t)), key=_vt)
            if not tags:
                add("core_source", WARN, f"v {repo} není značka core vX.Y.Z", "update_core --tag/--latest nepůjde")
            elif core_v and re.fullmatch(r"\d+\.\d+\.\d+", core_v) and _vt(tags[-1]) > _vt("v" + core_v):
                add("core_source", WARN, f"nejvyšší značka {tags[-1]} je novější než _core/VERSION {core_v}",
                    "aktualizace: update_core --latest (nejdřív dry-run), jen na pokyn GameDesignera")
            else:
                add("core_source", OK, f"core_source {repo}, nejvyšší značka {tags[-1]}")

    mfs = mount_fs(vault.resolve(), mounts_file)
    if mfs is not None:
        mp, fstype = mfs
        if is_remote_fs(fstype):
            add("mount", WARN, f"vault je na připojené složce ({fstype}, {mp})", WORK_COPY_HINT)
        else:
            add("mount", OK, f"souborový systém vaultu {fstype} ({mp})")
    return out


def run(args) -> tuple[int, dict, str]:
    items = checks(getattr(args, "vault", None))
    errors = sum(1 for c in items if c["status"] == ERR)
    warnings = sum(1 for c in items if c["status"] == WARN)
    lines = []
    for c in items:
        lines.append(f"{STATUS_CZ[c['status']]:<11} {c['name']}: {c['message']}")
        if c["help"]:
            lines += [f"            {h}" for h in c["help"].split("\n")]
    lines.append(f"Celkem: chyby {errors}, upozornění {warnings}.")
    payload = {"command": "doctor", "checks": items, "errors": errors, "warnings": warnings}
    return (EXIT_FINDINGS if errors else EXIT_OK), payload, "\n".join(lines)
