"""Kontrola prostředí před importem zbytku core (zadání 13 kap. 1 a 10.15, zadání 0.22, CR-022).

Jen standardní knihovna a syntaxe, kterou přečte i starší Python, aby `hestia.py` mohl vypsat návod místo
pádu na importu. Používá ho `hestia.py` při startu a příkaz `doctor`.
"""
import sys

MIN_PYTHON = (3, 11)

HELP = (
    "Návod: vytvoř prostředí s Pythonem >= 3.11 a PyYAML mimo projekt a vault (ve VM desktopové aplikace "
    "např. $HOME/venv311):\n"
    "  uv venv --python 3.12 $HOME/venv311 && uv pip install --python $HOME/venv311 pyyaml\n"
    "  nebo: python3.11 -m venv $HOME/venv311 && $HOME/venv311/bin/pip install pyyaml\n"
    "  Windows: py -3.12 -m venv %USERPROFILE%\\venv311 && %USERPROFILE%\\venv311\\Scripts\\pip install pyyaml\n"
    "  Je-li Python v pořádku a chybí jen PyYAML: python -m pip install pyyaml\n"
    "Pak spouštěj hestia.py Pythonem z tohoto prostředí. Podrobnosti: oddíl Prostředí v README.md core "
    "(ve vaultu _core/README.md); úplnou kontrolu udělá příkaz doctor."
)


def check_python(version_info=None):
    v = tuple(version_info or sys.version_info)[:3]
    text = ".".join(str(x) for x in v)
    if v[:2] < MIN_PYTHON:
        return False, f"Python {text} je starší než 3.11 ({sys.executable})"
    return True, f"Python {text} ({sys.executable})"


def check_yaml(importer=None):
    try:
        mod = importer() if importer else __import__("yaml")
    except ImportError:
        return False, "PyYAML chybí (import yaml selhal)"
    return True, f"PyYAML {getattr(mod, '__version__', '?')}"


def startup_problems():
    """Problémy, kvůli kterým core nepoběží (prázdné = v pořádku)."""
    out = []
    ok, msg = check_python()
    if not ok:
        out.append(msg)
    ok, msg = check_yaml()
    if not ok:
        out.append(msg)
    return out


def command_name(argv):
    """Jméno příkazu z argumentů (přeskočí společné přepínače a hodnotu --vault)."""
    skip = False
    for a in argv:
        if skip:
            skip = False
            continue
        if a == "--vault":
            skip = True
            continue
        if a.startswith("-"):
            continue
        return a
    return None
