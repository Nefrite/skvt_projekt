"""Hestia – jediný vstup skriptů: python hestia.py <příkaz> [argumenty] (zadání 13, kap. 2–3)."""
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    sys.exit("Hestia vyžaduje Python 3.11 nebo novější.")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hestia_lib.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
