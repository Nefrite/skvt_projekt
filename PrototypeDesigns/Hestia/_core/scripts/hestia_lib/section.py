"""Příkaz section: osnova dokumentu nebo jen zadané sekce s čísly řádků zdroje (zadání 13 kap. 10.13, 0.21).

`section <dokument> --list` vypíše osnovu (úroveň, nadpis, řádky, znaky) a *Souhrn*, je-li; `section <dokument>
"<nadpis>" …` vypíše jen ty sekce včetně podsekcí, s čísly řádků zdroje. `<dokument>` = cesta (od vaultu nebo
od projektu), jméno souboru, titul (`# …`) nebo alias. Nadpis se hledá bez ohledu na velikost písmen, nejdřív
přesně, pak podle začátku; víc shod = seznam kandidátů (kód 2), nehádá se. Funguje nad každou poznámkou vaultu
včetně předání a `Maintenance/*.md`. Jen čte.

Osnovu (`sections`) a počet znaků těla (`chars`) bere i `doc_index` a G14 v `audit`: sekce = nadpisy `##` a `###`
mimo bloky kódu a komentáře; `line` a `end_line` (včetně) jsou řádky souboru od 1, sekce končí před dalším
nadpisem stejné nebo vyšší úrovně; `chars` = znaky sekce včetně nadpisu.
"""
from __future__ import annotations

from pathlib import Path

from .blocks import strip_generated
from .errors import EXIT_OK, EXIT_USAGE, UsageError
from .links import headings
from .util import as_list
from .vault import Note, Vault

SUMMARY = "Souhrn"


def _offset(note: Note) -> int:
    """Řádek souboru, na kterém začíná tělo, minus 1."""
    return (note.split.body_line - 1) if note.split and note.split.has_frontmatter else 0


def _lf(text: str) -> str:
    return text.replace("\r\n", "\n")


def body_chars(note: Note) -> int:
    """Znaky těla bez frontmatteru (doc_index); konec řádku CRLF se počítá jako jeden znak."""
    return len(_lf(note.body))


def content_chars(note: Note) -> int:
    """Znaky těla bez frontmatteru a bez generovaných bloků (G14)."""
    return len(strip_generated(_lf(note.body)))


def outline(note: Note, levels=(2, 3)) -> list[dict]:
    """Sekce `##` a `###`: {heading, level, line, end_line, chars}, řádky souboru od 1, end_line včetně."""
    body = _lf(note.body)
    lines = body.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]                          # koncový znak nového řádku není další řádek
    off = _offset(note)
    hs = [h for h in headings(body) if h[0] >= 2]
    out = []
    for i, (lvl, title, no) in enumerate(hs):
        if lvl not in levels:
            continue
        end = len(lines)
        for lvl2, _t, no2 in hs[i + 1:]:
            if lvl2 <= lvl:
                end = no2 - 1
                break
        out.append({"heading": title, "level": lvl, "line": no + off, "end_line": end + off,
                    "chars": len("\n".join(lines[no - 1:end]))})
    return out


def summary(note: Note) -> dict | None:
    """Sekce `## Souhrn` mezi titulem a první další sekcí `##` (07 kap. 2, 13 kap. 10.13)."""
    first = next((s for s in outline(note, levels=(2,))), None)
    return first if first and first["heading"].casefold() == SUMMARY.casefold() else None


def section_lines(note: Note, sec: dict) -> list[tuple[int, str]]:
    """Řádky sekce s čísly řádků souboru."""
    lines = _lf(note.text).split("\n")
    return [(no, lines[no - 1]) for no in range(sec["line"], sec["end_line"] + 1)]


# ---------------------------------------------------------------- dokument a nadpis

def _title(note: Note) -> str | None:
    h1 = [t for lvl, t, _ in headings(note.body) if lvl == 1]
    return h1[0] if h1 else None


def resolve_note(vault: Vault, ref: str) -> Note:
    """Poznámka podle cesty, jména, titulu nebo aliasu; nejednoznačné nebo chybějící = UsageError."""
    raw = ref.strip().strip('"').replace("\\", "/")
    p = Path(raw)
    if p.is_absolute() or (vault.project_root / raw).is_file():
        try:
            raw = (p if p.is_absolute() else vault.project_root / raw).resolve().relative_to(
                vault.root.resolve()).as_posix()
        except ValueError:
            raise UsageError(f"section: {ref} není ve vaultu") from None
    rel, status = vault.resolve(raw.removesuffix(".md") if "/" not in raw else raw)
    if status == "ok" and rel in vault.notes:
        return vault.notes[rel]
    key = raw.removesuffix(".md").casefold()
    hits = sorted(n.rel for n in vault.notes.values()
                  if (_title(n) or "").casefold() == key
                  or key in {str(a).casefold() for a in as_list((n.fm or {}).get("aliases")) if a})
    if len(hits) == 1:
        return vault.notes[hits[0]]
    if hits or status == "ambiguous":
        raise UsageError(f"section: {ref} je nejednoznačný: {', '.join(hits) or 'víc souborů stejného jména'}")
    raise UsageError(f"section: dokument {ref} nenalezen (cesta, jméno, titul nebo alias)")


def match_heading(secs: list[dict], query: str) -> list[dict]:
    """Shoda nadpisu bez ohledu na velikost písmen: přesně, jinak podle začátku."""
    q = query.strip().lstrip("#").strip().casefold()
    exact = [s for s in secs if s["heading"].casefold() == q]
    return exact or [s for s in secs if s["heading"].casefold().startswith(q)]


# ---------------------------------------------------------------- příkaz

def _fmt_sec(s: dict) -> str:
    return f"{'#' * s['level']} {s['heading']}  (ř. {s['line']}–{s['end_line']}, {s['chars']} zn.)"


def run(args, vault: Vault) -> tuple[int, dict, str]:
    note = resolve_note(vault, args.document)
    secs = outline(note)
    payload = {"command": "section", "path": note.rel, "chars": body_chars(note)}
    if args.list or not args.headings:
        summ = summary(note)
        payload |= {"sections": secs, "summary": summ and "\n".join(t for _n, t in section_lines(note, summ)[1:]).strip()}
        lines = [f"{note.rel}: {body_chars(note)} znaků, {len(secs)} sekcí"]
        lines += [("  " * (s["level"] - 2)) + _fmt_sec(s) for s in secs]
        if summ:
            lines += ["", "Souhrn:"] + [t for _n, t in section_lines(note, summ)[1:]]
        return EXIT_OK, payload, "\n".join(lines).rstrip()
    found, text, ambiguous = [], [], []
    for q in args.headings:
        hits = match_heading(secs, q)
        if len(hits) != 1:
            ambiguous.append({"query": q, "candidates": [s["heading"] for s in hits]})
            text.append(f"{note.rel}: nadpis „{q}“ " + (
                "je nejednoznačný, kandidáti: " + "; ".join(_fmt_sec(s) for s in hits) if hits else
                "nenalezen; osnova: section --list"))
            continue
        s = hits[0]
        body = section_lines(note, s)
        found.append(s | {"text": "\n".join(t for _n, t in body)})
        width = len(str(s["end_line"]))
        text += [f"{note.rel} § {s['heading']} (ř. {s['line']}–{s['end_line']})"]
        text += [f"{no:>{width}}| {t}" for no, t in body] + [""]
    payload |= {"sections": found, "unresolved": ambiguous}
    return (EXIT_USAGE if ambiguous else EXIT_OK), payload, "\n".join(text).rstrip()
