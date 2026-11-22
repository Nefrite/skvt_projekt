"""Hestia – jediný vstup skriptů: python hestia.py <příkaz> [argumenty] (zadání 13, kap. 2–3).

Před importem core ověří Python >= 3.11 a PyYAML a při chybě vypíše návod, kód 2 (13 kap. 1, zadání 0.22).
Příkaz `doctor` (13 kap. 10.15) poběží i bez PyYAML.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hestia_lib import envcheck  # noqa: E402

_problems = envcheck.startup_problems()
if _problems and envcheck.command_name(sys.argv[1:]) != "doctor":
    print("hestia: prostředí nestačí: " + "; ".join(_problems), file=sys.stderr)
    print(envcheck.HELP, file=sys.stderr)
    sys.exit(2)

from hestia_lib.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
