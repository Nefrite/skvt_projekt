"""Rozhraní příkazové řádky: python hestia.py <příkaz> [argumenty] (zadání 13, kap. 3).

Společné argumenty: --vault PATH, --apply, --force, --json, --quiet.
Návratové kódy: 0 v pořádku, 1 nálezy úrovně chyba / odmítnutý zápis, 2 chybné použití
nebo konfigurace, 3 neočekávaná chyba.
"""
from __future__ import annotations

import argparse
import json
import sys
import traceback

from . import core_version
from .errors import EXIT_UNEXPECTED, EXIT_USAGE, HestiaError

COMMANDS_LATER: dict[str, int] = {}
# příkaz -> modul s funkcí run(args, vault)
VAULT_COMMANDS = {"lint": "lint", "compose_role": "compose", "asset_index": "asset_index", "hubs": "hubs",
                  "audit": "audit", "task_close": "task_close", "frontmatter": "migrate",
                  "update_core": "update_core", "export_cr": "export_cr", "doc_index": "doc_index",
                  "compose_context": "context", "ue_query": "ue"}


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"hestia: chyba: {message}", file=sys.stderr)
        raise SystemExit(EXIT_USAGE)


def _common() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--vault", metavar="PATH", help="vault Hestia/ (výchozí: nejbližší Hestia/ od pracovní složky)")
    p.add_argument("--apply", action="store_true", help="zapsat změny (bez něj dry-run)")
    p.add_argument("--force", action="store_true", help="přepsat existující hodnotu, kde to příkaz umí")
    p.add_argument("--json", action="store_true", help="strojový výstup na stdout")
    p.add_argument("--quiet", action="store_true", help="bez textového výstupu")
    return p


def build_parser() -> argparse.ArgumentParser:
    common = _common()
    parser = _Parser(prog="hestia.py", description=f"Hestia core {core_version()}", parents=[common])
    parser.add_argument("--version", action="version", version=core_version())
    sub = parser.add_subparsers(dest="command", metavar="<příkaz>", parser_class=_Parser)

    p = sub.add_parser("init", parents=[common], help="založí vault Hestia/ ze šablony")
    p.add_argument("--prototype", help="jméno prototypu (např. Lapikus); povinné s herní vrstvou")
    p.add_argument("--root", help="kořenová entita prototypu (např. Lapikus_Region); povinné s herní vrstvou")
    p.add_argument("--no-game-layer", action="store_true",
                   help="instance bez herní vrstvy (game_layer: false; bez kořene, master lore, Entities/)")
    p.add_argument("--root-kind", default="place", choices=["place", "location"], help="kind kořenové entity")
    p.add_argument("--engine-version", default=None, help="verze enginu (např. 5.8)")

    p = sub.add_parser("lint", parents=[common], help="G6, G7 nad změněnými nebo zadanými soubory")
    p.add_argument("files", nargs="*", help="poznámky nebo soubory kódu (výchozí: změněné podle gitu)")
    p.add_argument("--all", action="store_true", help="celý vault a hlavičky všech souborů v code_roots")
    p.add_argument("--draft", metavar="SOUBOR",
                   help="kontrola navrhované poznámky mimo vault (- = stdin); nic nezapisuje (13 kap. 10.10)")
    p.add_argument("--as", dest="as_path", metavar="CESTA",
                   help="cílová cesta konceptu ve vaultu (např. Entities/X.md); povinné u stdin")

    p = sub.add_parser("compose_role", parents=[common], help="kompilát role pro chat do Roles/_compiled/")
    p.add_argument("roles", nargs="*", help="role (výchozí: všechny profily v Roles/)")

    sub.add_parser("asset_index", parents=[common], help="index souborů mimo vault (asset_index.md + .json)")

    p = sub.add_parser("hubs", parents=[common], help="generované sekce hubů, kroků a Dashboard/Index.md")
    p.add_argument("entities", nargs="*", help="jen tyto entity (výchozí: všechny huby, kroky a Index)")

    p = sub.add_parser("audit", parents=[common], help="G1–G13, zralost; report a fronta")
    p.add_argument("--baseline", metavar="REPORT_JSON", help="rozdíl nálezů proti dřívějšímu reportu")

    p = sub.add_parser("task_close", parents=[common], help="uzavření tasku: changes.md, updated, hubs, lint, G11")
    p.add_argument("files", nargs="*", help="dotčené soubory (výchozí: změněné podle gitu)")
    p.add_argument("--role", required=True, help="role, která task dělala")
    p.add_argument("--source", required=True, help="zdroj: dokument, předání nebo chat:<task>")
    p.add_argument("--note", help="popis změny společný pro všechny dotčené entity")
    p.add_argument("--change", action="append", default=[], metavar='ENTITA="text"',
                   help="popis po entitách (opakovatelné; přednost před --note)")
    p.add_argument("--entity", action="append", default=[], help="doplní entitu, kterou nejde odvodit")
    p.add_argument("--archive-handover", action="append", default=[], metavar="JMÉNO",
                   help="archivuje splněné předání bez otevřených otázek (validity: archived, Handovers/_archive/)")

    p = sub.add_parser("frontmatter", parents=[common], help="migrace dokumentace podle mapovacího souboru")
    p.add_argument("--map", required=True, metavar="MAP_YAML", help="mapovací soubor (13 kap. 10.1)")
    p.add_argument("--move", action="store_true", help="provést přesuny položek s target")

    sub.add_parser("doc_index", parents=[common], help="index dokumentů pro Knihovníka (Maintenance/doc_index.json)")

    p = sub.add_parser("compose_context", parents=[common],
                       help="balíček kontextu pro chat do Maintenance/context/ (Knihovník)")
    p.add_argument("--entity", help="entita (hub, dokumenty, master lore, předání)")
    p.add_argument("--topic", help="kategorie, doména nebo inbox")
    p.add_argument("--query", help="otázka (hledání v indexu dokumentů a glosáři)")

    p = sub.add_parser("ue_query", parents=[common], help="čtení stavu v Unrealu, etapa 1 (jen čtení; 13 kap. 10.11)")
    p.add_argument("--emit", action="store_true", help="vygenerovat čtecí skript do Maintenance/ue/")
    p.add_argument("--import", dest="import_file", nargs="?", const="", default=None, metavar="VÝSLEDEK",
                   help="načíst výsledek z editoru a uložit reporty Maintenance/reports/ue_<entita>.json")
    p.add_argument("--entity", help="entita s pravidlem v ue_map.yaml (čtou se i její potomci)")
    p.add_argument("--all", action="store_true", help="všechny entity s pravidlem (jedno spuštění editoru)")

    p = sub.add_parser("update_core", parents=[common], help="aktualizace _core/ na novou verzi")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--from", dest="source", metavar="HESTIA_DIR", help="cesta k novému hestia/")
    src.add_argument("--tag", metavar="vX.Y.Z", help="značka core z repozitáře core_source (git archive)")
    src.add_argument("--latest", action="store_true", help="nejvyšší značka core vX.Y.Z z core_source")
    src.add_argument("--after-only", action="store_true",
                     help="jen kroky po aktualizaci podle upgrade.yaml nad _core/ (bez výměny core)")
    p.add_argument("--no-after", action="store_true", help="kroky po aktualizaci přeskočit, jen vypsat")
    p.add_argument("--since", metavar="VERZE", help=argparse.SUPPRESS)   # stará verze pro --after-only (řídicí skript)
    p.add_argument("--with-views", action="store_true",
                   help="doplnit chybějící pohledy do Dashboard/views/ (existující nepřepíše)")

    p = sub.add_parser("export_cr", parents=[common], help="change requesty ze structure_log do outbox/")
    p.add_argument("--area", help="oblast CR (výchozí: taxonomy u kategorie taxonomy, jinak process)")
    p.add_argument("--include-works", action="store_true", help="exportovat i kategorii works")

    for name, phase in COMMANDS_LATER.items():
        sub.add_parser(name, parents=[common], help=f"(fáze {phase}, zatím neimplementováno)")
    return parser


def _emit(args, payload, text: str) -> None:
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    elif not args.quiet and text:
        print(text)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return EXIT_USAGE
    try:
        if args.command == "init":
            from . import init
            code, payload, text = init.run(args)
        elif args.command in VAULT_COMMANDS:
            import importlib
            from .vault import Vault, find_vault
            module = importlib.import_module(f".{VAULT_COMMANDS[args.command]}", __package__)
            vault = Vault.load(args.vault if args.vault else find_vault())
            code, payload, text = module.run(args, vault)
        else:
            print(f"hestia: příkaz {args.command} přijde ve fázi {COMMANDS_LATER[args.command]}", file=sys.stderr)
            return EXIT_USAGE
        _emit(args, payload, text)
        return code
    except HestiaError as exc:
        print(f"hestia: {exc}", file=sys.stderr)
        return exc.exit_code
    except Exception:  # noqa: BLE001 – návratový kód 3
        traceback.print_exc()
        return EXIT_UNEXPECTED
