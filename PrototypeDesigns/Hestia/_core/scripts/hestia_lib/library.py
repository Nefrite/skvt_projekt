"""Knihovní assety z kódu instance, etapa B (zadání 13 kap. 10.18; 0.25; CR-027, CR-029 bod 5).

Manifest `Maintenance/taxonomy_local/asset_sources.yaml` říká, kde v kódu instance leží knihovna meshí, verze, tvary
a odkazy v datech staveb. Hodnoty se čtou **jen jako literály ze zdrojového textu** (`ast.parse` +
`ast.literal_eval` přiřazení na úrovni modulu); kód se nespouští ani neimportuje. Výraz, který není literál, je chyba
manifestu (`lint`, G6 na manifest). Chybí-li manifest, etapa B se přeskočí s informací.

Výstupy:
- `entries()` → sekce `library` v `asset_index.json` (jméno `{key}_{variant}`, verze podle přesné shody, pak nejdelšího prefixu,
  odvozená `ue_path`, `.uasset` na disku, zdroj `soubor:řádek`, karta, výskyty v datech),
- `code_block()` → generovaný blok *Z kódu* v kartě meshe (`hubs`),
- `g15()` → nálezy G15 pro `audit` (stav karty nemění).
Rozsah: jen meshe (`asset_kind: mesh`); ostatní karty zůstávají ruční.
"""
from __future__ import annotations

import ast
import datetime as _dt
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .fileio import read_text, to_posix
from .util import as_date

SOURCES_REL = "Maintenance/taxonomy_local/asset_sources.yaml"
CODE_HEADING = "Z kódu"
CODE_MARK = "<!-- hestia:asset_code -->"
NOT_FOUND = "v kódu nenalezeno"
DEFAULT_NAME = "{key}_{variant}"
REQUIRED_FIELDS = ("size", "category")
TOP_KEYS = {"meshes", "versions", "global_versions", "shapes", "data_refs"}
MESH_KEYS = {"file", "variable", "fields", "name", "ue_root", "ue_dirs", "content_dir",
             "category", "variants", "files"}      # pevná category/variants tabulky, zdroj files (zadání 0.28, CR-037)
DATA_ENTITY_FIELDS = ("entity", "group")           # záznam v datech s ID entity (zadání 0.28, CR-037)
FROM_GENERATED = {"generated", "imported", "verified"}
IMPORTED = {"imported", "verified"}


# ---------------------------------------------------------------- literály ze zdroje

@dataclass
class Literal:
    value: object = None
    line: int = 0
    lines: dict = field(default_factory=dict)       # klíč slovníku -> řádek (zdroj `soubor:řádek`)
    error: str | None = None                        # proměnná není literál


def read_literals(path: Path) -> dict[str, Literal]:
    """Přiřazení na úrovni modulu `JMÉNO = literál` (i s anotací); nic se nespouští. Výjimka = SyntaxError."""
    tree = ast.parse(read_text(path), filename=str(path))
    out: dict[str, Literal] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets, value = [t for t in node.targets if isinstance(t, ast.Name)], node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            targets, value = [node.target], node.value
        else:
            continue
        for t in targets:
            lit = Literal(line=node.lineno)
            try:
                lit.value = ast.literal_eval(value)
            except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                lit.error = f"{t.id} (řádek {node.lineno}) není literál"
            if isinstance(value, ast.Dict):
                for k in value.keys:
                    if isinstance(k, ast.Constant):
                        lit.lines[k.value] = k.lineno
            out[t.id] = lit
    return out


# ---------------------------------------------------------------- manifest

@dataclass
class Manifest:
    path: Path
    meshes: list = field(default_factory=list)
    versions: list = field(default_factory=list)
    global_versions: list = field(default_factory=list)
    shapes: list = field(default_factory=list)
    data_refs: list = field(default_factory=list)
    problems: list = field(default_factory=list)    # (kód, zpráva): G7 tvar manifestu, G6 soubor/proměnná/literál
    values: dict = field(default_factory=dict)      # (soubor, proměnná) -> Literal

    @property
    def ue_tags(self) -> list[str]:
        return [str(v["ue_tag"]) for v in self.versions + self.global_versions if v.get("ue_tag")]


def _list_of_maps(data: dict, key: str, problems: list) -> list[dict]:
    val = data.get(key)
    if val is None:
        return []
    if not isinstance(val, list) or not all(isinstance(x, dict) for x in val):
        problems.append(("G7", f"asset_sources: {key} musí být seznam map"))
        return []
    return val


def load_manifest(vault) -> Manifest | None:
    """Manifest instance; None = soubor chybí (etapa B se přeskočí). Problémy tvaru i čtení jsou v `problems`."""
    from .taxonomy import load_yaml
    p = vault.root / SOURCES_REL
    if not p.is_file():
        return None
    man = Manifest(p)
    try:
        data = load_yaml(p) or {}
    except Exception as e:                           # noqa: BLE001 – chybný YAML = chyba manifestu
        man.problems.append(("G7", f"asset_sources: neplatný YAML ({e})"))
        return man
    if not isinstance(data, dict):
        man.problems.append(("G7", "asset_sources: soubor musí být mapa (meshes, versions, …)"))
        return man
    extra = set(data) - TOP_KEYS
    if extra:
        man.problems.append(("G7", f"asset_sources: neznámé klíče {', '.join(sorted(extra))}"))
    man.meshes = _list_of_maps(data, "meshes", man.problems)
    man.versions = _list_of_maps(data, "versions", man.problems)
    man.global_versions = _list_of_maps(data, "global_versions", man.problems)
    man.shapes = _list_of_maps(data, "shapes", man.problems)
    man.data_refs = _list_of_maps(data, "data_refs", man.problems)
    for i, m in enumerate(man.meshes):
        where = f"asset_sources meshes[{i}]"
        if set(m) - MESH_KEYS:
            man.problems.append(("G7", f"{where}: neznámé klíče {', '.join(sorted(set(m) - MESH_KEYS))}"))
        if "files" in m:                             # jména meshí ze jmen souborů (zadání 0.28, CR-037)
            src = m.get("files")
            if not isinstance(src, dict) or not isinstance(src.get("dir"), str) \
                    or not isinstance(src.get("pattern"), str):
                man.problems.append(("G7", f"{where}: files musí být mapa s dir a pattern (text)"))
            if not isinstance(m.get("category"), str):
                man.problems.append(("G7", f"{where}: zdroj files potřebuje pevnou category"))
            if "file" in m or "variable" in m or "fields" in m:
                man.problems.append(("G7", f"{where}: zdroj files nemá file, variable ani fields"))
            continue
        fields = m.get("fields")
        need = [f for f in REQUIRED_FIELDS if not (f == "category" and isinstance(m.get("category"), str))]
        if not isinstance(fields, list) or any(f not in fields for f in need):
            man.problems.append(("G7", f"{where}: fields musí být seznam a obsahovat size a category "
                                       "(category může být pevná pro celou tabulku)"))
    for i, v in enumerate(man.versions):
        if v.get("match", "prefix") != "prefix":
            man.problems.append(("G7", f"asset_sources versions[{i}]: match umí jen prefix"))
    for i, d in enumerate(man.data_refs):
        if not isinstance(d.get("glob"), str) or not isinstance(d.get("keys"), list):
            man.problems.append(("G7", f"asset_sources data_refs[{i}]: glob (text) a keys (seznam) jsou povinné"))
    # proměnné: soubor existuje, proměnná je přiřazená literálem (kód se nespouští)
    cache: dict[str, dict | None] = {}
    for group in ("meshes", "versions", "global_versions", "shapes"):
        for i, item in enumerate(getattr(man, group)):
            refs = [(item.get("file"), item.get("variable"))]
            if group == "meshes" and "files" in item:
                refs = []                            # zdroj files: tabulka v kódu není
            if group == "meshes":
                for k in ("ue_root", "ue_dirs"):
                    if isinstance(item.get(k), dict):
                        refs.append((item[k].get("file", item.get("file")), item[k].get("variable")))
            for file, var in refs:
                if not isinstance(file, str) or not isinstance(var, str):
                    man.problems.append(("G7", f"asset_sources {group}[{i}]: file a variable jsou povinné"))
                    continue
                if file not in cache:
                    src = vault.project_root / file.lstrip("/")
                    try:
                        cache[file] = read_literals(src) if src.is_file() else None
                    except SyntaxError as e:
                        man.problems.append(("G6", f"asset_sources: {file} nejde přečíst ({e.msg}, řádek {e.lineno})"))
                        cache[file] = {}
                    if cache[file] is None:
                        man.problems.append(("G6", f"asset_sources: soubor {file} neexistuje"))
                lits = cache[file]
                if lits is None:
                    continue
                lit = lits.get(var)
                if lit is None:
                    if lits:
                        man.problems.append(("G6", f"asset_sources: {file}: proměnná {var} nenalezena"))
                    continue
                if lit.error:
                    man.problems.append(("G6", f"asset_sources: {file}: {lit.error}; čtou se jen literály"))
                    continue
                man.values[(file, var)] = lit
    return man


def _value(man: Manifest, file: str | None, var: str | None):
    lit = man.values.get((file, var))
    return lit.value if lit else None


# ---------------------------------------------------------------- knihovna

def _variants(value) -> list[str]:
    if isinstance(value, str):
        return [c for c in value if not c.isspace()] or [""]
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value] or [""]
    return [""]


def _name(pattern: str, key: str, variant: str) -> str:
    name = pattern.replace("{key}", str(key)).replace("{variant}", variant)
    return name.rstrip("_") if not variant else name


def _is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def version_key(base: str, table: dict) -> str | None:
    """Klíč tabulky verzí pro jméno bez varianty (13 kap. 10.18, 10.22): přesná shoda má přednost, pak nejdelší
    prefix; klíč zakončený `_` (`SM_RuinTimber_`) platí i pro jméno bez varianty (`SM_RuinTimber`)."""
    if base in table:
        return base
    hits = [p for p in table if base.startswith(p) or (p.endswith("_") and base == p[:-1])]
    return max(hits, key=len, default=None)


def _size(value) -> list | None:
    if isinstance(value, (list, tuple)) and len(value) == 3 and all(isinstance(v, (int, float)) for v in value):
        return [v for v in value]
    return None


def _ref(item, default_file: str | None) -> tuple:
    if isinstance(item, dict):
        return item.get("file", default_file), item.get("variable")
    return None, None


def _files_table(vault, m: dict) -> dict:
    """Zdroj `files: {dir, pattern}` (zadání 0.28, CR-037): klíč = jméno souboru bez přípony, hodnota
    (cesta od kořene projektu, prázdná n-tice); soubory se nečtou (OBJ ne), rozměr chybí, verze z `versions`."""
    src = m.get("files") or {}
    d = vault.project_root / str(src.get("dir") or "").strip("/")
    out = {}
    if not d.is_dir():
        return out
    for p in sorted(d.glob(str(src.get("pattern") or "*"))):
        if p.is_file():
            out[p.stem] = (to_posix(p.relative_to(vault.project_root)), ())
    return out


def build(vault, man: Manifest, files: list[dict] | None = None, cards: list | None = None,
          folder_map: list | None = None, entities: set | None = None) -> tuple[list[dict], dict, list[str]]:
    """Záznamy knihovny, globální verze a upozornění. `files` = záznamy `asset_index` (entita datového souboru),
    `cards` = karty assetů (`assets.cards`) pro párování přes jméno a `variants`, `entities` = jména entit
    (výskyt v datech podle pole `entity`/`group` záznamu, zadání 0.28, CR-037)."""
    warnings: list[str] = []
    versions = []                                         # (prefix -> int, ue_tag, proměnná)
    for v in man.versions:
        d = _value(man, v.get("file"), v.get("variable"))
        if isinstance(d, dict):
            versions.append(({str(k): x for k, x in d.items()}, v.get("ue_tag"), v.get("variable")))
    globals_: dict[str, dict] = {}
    for g in man.global_versions:
        val = _value(man, g.get("file"), g.get("variable"))
        if val is not None:
            globals_[str(g.get("variable"))] = {"value": val, "ue_tag": g.get("ue_tag")}
    shapes: dict[str, str] = {}
    for s in man.shapes:
        d = _value(man, s.get("file"), s.get("variable"))
        if isinstance(d, dict):
            for k, x in d.items():
                key = x[0] if isinstance(x, (list, tuple)) and x else x
                if isinstance(key, str):
                    shapes[str(k)] = key
    out: list[dict] = []
    for m in man.meshes:
        if "files" in m:
            table, lines, src_of = _files_table(vault, m), {}, {}
            for k, (rel, _row) in list(table.items()):
                src_of[k] = rel
                table[k] = _row
        else:
            table = _value(man, m.get("file"), m.get("variable"))
            src_of = None
        if not isinstance(table, dict):
            continue
        fields = [str(f) for f in m.get("fields") or []]
        pattern = str(m.get("name") or DEFAULT_NAME)
        root = m.get("ue_root")
        root = root if isinstance(root, str) else _value(man, *_ref(root, m.get("file")))
        dirs = m.get("ue_dirs")
        dirs = dirs if isinstance(dirs, dict) and "variable" not in dirs else _value(man, *_ref(dirs, m.get("file")))
        dirs = dirs if isinstance(dirs, dict) else {}
        if src_of is None:
            lines = man.values[(m.get("file"), m.get("variable"))].lines
        for key, row in table.items():
            row = row if isinstance(row, (list, tuple)) else (row,)
            if fields[:1] == ["size"] and row and _is_num(row[0]):    # hodnota přímo (x, y, z) (zadání 0.29)
                row = (row,)
            rec = {f: (row[i] if i < len(row) else None) for i, f in enumerate(fields)}
            if "category" not in rec and isinstance(m.get("category"), str):     # pevně pro tabulku (CR-037)
                rec["category"] = m["category"]
            if rec.get("variants") is None and m.get("variants") is not None:
                rec["variants"] = m["variants"]
            category = str(rec.get("category") or "")
            sub = dirs.get(category)
            if sub is None and category:
                warnings.append(f"asset_sources: kategorie {category} (klíč {key}) nemá složku v ue_dirs")
            for variant in _variants(rec.get("variants")):
                name = _name(pattern, key, variant)
                base = _name(pattern, key, "")
                e = {"name": name, "key": str(key), "variant": variant, "category": category,
                     "size": _size(rec.get("size")), "slots": rec.get("slots"), "material": rec.get("material"),
                     "version": None, "version_prefix": None, "version_tag": None, "ue_path": None, "uasset": None,
                     "source": (src_of[key] if src_of is not None else
                                f"{m.get('file')}:{lines.get(key, man.values[(m.get('file'), m.get('variable'))].line)}"),
                     "card": None, "data": []}
                for table_v, tag, var in versions:                    # přesná shoda, pak nejdelší prefix
                    hit = version_key(base, table_v)
                    if hit is not None:
                        e.update(version=table_v[hit], version_prefix=hit, version_tag=tag or var)
                        break
                if isinstance(root, str) and sub is not None:
                    sub_s = str(sub).strip("/")
                    e["ue_path"] = "/".join(x for x in (root.rstrip("/"), sub_s, f"{name}.{name}") if x)
                    cdir = m.get("content_dir")
                    if isinstance(cdir, str):
                        e["uasset"] = (vault.project_root / cdir.strip("/") / sub_s / f"{name}.uasset").is_file()
                out.append(e)
    by_name = {e["name"]: e for e in out}
    by_key: dict[str, list[dict]] = {}
    for e in out:
        by_key.setdefault(e["key"], []).append(e)
    # párování karty: jméno souboru a `variants` (tvarové varianty v jedné kartě, GameDesigner 2026-11-23)
    for c in cards or []:
        for n in [c.name, *c.variants]:
            if n in by_name and by_name[n]["card"] is None:
                by_name[n]["card"] = c.rel
    # výskyty v datech staveb
    entity_of = {f["path"].lstrip("/"): f.get("entity") for f in files or []}
    fmap = sorted(folder_map or [], key=lambda it: -len(str(it.get("path") or "")))
    for ref in man.data_refs:
        pattern_g, keys = ref.get("glob"), [str(k) for k in ref.get("keys") or []]
        if not isinstance(pattern_g, str):
            continue
        for p in sorted(vault.project_root.glob(pattern_g)):
            if not p.is_file() or "_to_delete" in p.parts:
                continue
            rel = to_posix(p.relative_to(vault.project_root))
            try:
                data = json.loads(read_text(p))
            except (ValueError, UnicodeDecodeError):
                warnings.append(f"asset_sources data_refs: {rel} není platný JSON")
                continue
            hits: dict[str, set] = {}                       # jméno assetu -> entity záznamů (None = souboru)
            ekeys = ref.get("entity_keys") if isinstance(ref.get("entity_keys"), dict) else {}
            for k, val, rec_id in _walk(data, set(keys)):
                if not isinstance(val, str):
                    continue
                rec_ent = _record_entity(rec_id, ekeys, entities)
                if k == "shape":
                    key = shapes.get(val)
                    names = {e["name"] for e in by_key.get(key or "", [])}
                else:
                    nm = val.rsplit("/", 1)[-1].split(".", 1)[0]
                    names = {nm} if nm in by_name else {e["name"] for e in by_key.get(nm, [])}
                for nm in names:
                    hits.setdefault(nm, set()).add(rec_ent)
            if not hits:
                continue
            ent = entity_of.get(rel)
            if ent is None:
                ent = next((it.get("entity") for it in fmap
                            if rel.startswith(str(it.get("path") or "").strip("/") + "/")), None)
            for nm in sorted(hits):
                for e_ in sorted(hits[nm], key=lambda x: (x is not None, x or "")):
                    item = {"file": rel, "entity": e_ or ent}
                    if item not in by_name[nm]["data"]:
                        by_name[nm]["data"].append(item)
    return out, globals_, warnings


def _walk(data, keys: set, rec_id=None):
    """(klíč, hodnota, ID entity nejbližšího záznamu s `entity`/`group` nebo None)."""
    if isinstance(data, dict):
        own = next((data[f] for f in DATA_ENTITY_FIELDS if isinstance(data.get(f), str) and data[f].strip()), None)
        rec_id = own if own is not None else rec_id
        for k, v in data.items():
            if k in keys:
                yield k, v, rec_id
            yield from _walk(v, keys, rec_id)
    elif isinstance(data, list):
        for v in data:
            yield from _walk(v, keys, rec_id)


def _record_entity(rec_id, ekeys: dict, entities: set | None) -> str | None:
    """Entita záznamu: ID přes `data_refs.entity_keys`, jinak ID samo, je-li to entita vaultu."""
    if not isinstance(rec_id, str):
        return None
    rid = rec_id.strip()
    if rid in ekeys:
        return str(ekeys[rid])
    return rid if entities is not None and rid in entities else None


# ---------------------------------------------------------------- karta: blok Z kódu

def tolerance(vault) -> float:
    try:
        return float(vault.config.get("asset_envelope_tolerance_cm") or 0)
    except (TypeError, ValueError):
        return 0.5


def envelope_of(card_fm: dict) -> list | None:
    return _size(card_fm.get("envelope"))


def overflow(size: list | None, env: list | None, tol: float) -> list[str]:
    """Osy, ve kterých je skutečný rozměr větší než `envelope` o víc než toleranci."""
    if not size or not env:
        return []
    return [f"{ax} o {size[i] - env[i]:g} cm" for i, ax in enumerate("XYZ") if size[i] - env[i] > tol]


def _fmt_size(v) -> str:
    return " × ".join(f"{x:g}" for x in v) + " cm" if v else "–"


def entries_of_card(card, library: list[dict]) -> list[dict]:
    """Záznamy knihovny karty: vlastní jméno první, pak `variants`."""
    names = [card.name, *card.variants]
    by_name = {e["name"]: e for e in library}
    return [by_name[n] for n in names if n in by_name]


def code_block(card, card_fm: dict, library: list[dict], globals_: dict, tol: float) -> str:
    """Obsah generovaného bloku *Z kódu* (13 kap. 10.18); idempotentní (bez data běhu)."""
    mine = entries_of_card(card, library)
    if not mine:
        return f"{CODE_MARK}\n_{NOT_FOUND} (`asset_sources.yaml`); technické údaje doplní kód, ne karta._"
    e = mine[0]
    env = envelope_of(card_fm)
    lines = [CODE_MARK]
    size = f"- Rozměr (skutečný): {_fmt_size(e['size'])}"
    if not e.get("size"):                      # zdroj files nebo hodnota bez trojice (zadání 0.29, CR-037)
        size = "- Rozměr: rozměr neznámý" + (f"; `envelope` {_fmt_size(env)} se proti rozměru nekontroluje"
                                             if env else "; `envelope` chybí")
    elif env:
        over = overflow(e["size"], env, tol)
        size += f"; `envelope` {_fmt_size(env)}: " + ("**nevejde se** (" + ", ".join(over) + ")" if over
                                                      else "vejde se")
    else:
        size += "; `envelope` chybí"
    lines.append(size)
    lines.append("- Varianty: " + ", ".join(f"`{x['name']}`" for x in mine))
    if e.get("slots") is not None:
        lines.append(f"- Sloty: {e['slots']}")
    if e.get("material") is not None:
        lines.append(f"- Výchozí materiál: `{e['material']}`")
    if e.get("version") is not None:
        lines.append(f"- Verze: {e['version']} (prefix `{e['version_prefix']}`, `{e['version_tag']}`)")
    if globals_:
        lines.append("- Globální verze: " + ", ".join(f"`{k}` {v['value']}" for k, v in sorted(globals_.items())))
    lines.append(f"- `ue_path` (odvozená): `{e['ue_path']}`" if e.get("ue_path") else "- `ue_path`: neodvozena")
    if e.get("uasset") is not None:
        lines.append(f"- `.uasset` na disku: {'ano' if e['uasset'] else 'ne'}")
    lines.append(f"- Zdroj: `{e['source']}`")
    data = sorted({(d["file"], d.get("entity") or "") for x in mine for d in x.get("data") or []})
    lines.append("- Data: " + (", ".join(f"`{f}`" + (f" ([[{ent}]])" if ent else "") for f, ent in data)
                               if data else "bez výskytu"))
    return "\n".join(lines)


def has_code_block(text: str) -> bool:
    from .blocks import block_content
    content = block_content(text, CODE_HEADING)
    return bool(content and content.strip())


# ---------------------------------------------------------------- G15

def visual_version(section: str) -> int | None:
    """Verze v *Vizuálně ověřeno* = první číslo za slovem „verze“ nebo `v` (13 kap. 10.18)."""
    m = re.search(r"(?:\bverze\s*:?\s*|\bv\s?)(\d+)", section or "", re.I)
    return int(m.group(1)) if m else None


def g15(vault, model, library: list[dict], cards: list, day: _dt.date) -> list[tuple[str, str, str, str]]:
    """Nálezy G15 etapy B: (úroveň, cíl, soubor karty nebo manifestu, zpráva). Stav karty se nemění."""
    from .links import section_text
    out: list[tuple[str, str, str, str]] = []
    manifest_file = vault.project_rel(vault.root / SOURCES_REL)
    by_key: dict[str, list[dict]] = {}
    for e in library:
        by_key.setdefault(e["key"], []).append(e)
    for key, es in sorted(by_key.items()):                 # asset v kódu bez karty (varianty jeden řádek)
        free = [e["name"] for e in es if not e.get("card")]
        if free:
            out.append(("info", free[0], manifest_file,
                        f"asset v kódu bez karty: {', '.join(free)} (`{es[0]['source']}`)"))
    tol = tolerance(vault)
    try:
        req_days = int(vault.config.get("asset_request_days") or 30)
    except (TypeError, ValueError):
        req_days = 30
    old_verified: dict[str, list[str]] = {}
    for c in cards:
        note = vault.notes.get(c.rel)
        if note is None:
            continue
        f = vault.project_rel(note.path)
        mine = entries_of_card(c, library) if c.kind == "mesh" else []
        e = mine[0] if mine else None
        if c.kind == "mesh" and c.status in FROM_GENERATED and e is None:
            out.append(("warning", c.name, f, f"karta {c.status} bez záznamu v kódu (asset_sources.yaml)"))
        if e is not None:
            ue_path = str(note.fm.get("ue_path") or "").strip()
            if ue_path and e.get("ue_path") and ue_path.split(".", 1)[0] != e["ue_path"].split(".", 1)[0]:
                out.append(("warning", c.name, f, f"ue_path karty {ue_path} je jiná než odvozená z kódu {e['ue_path']}"))
            if c.status in IMPORTED and e.get("uasset") is False:
                out.append(("warning", c.name, f, f"karta {c.status}, ale {e['name']}.uasset v content_dir chybí"))
            over = overflow(e.get("size"), envelope_of(note.fm), tol)
            if over:
                out.append(("warning", c.name, f, f"skutečný rozměr {_fmt_size(e['size'])} je větší než envelope "
                                                   f"{_fmt_size(envelope_of(note.fm))} ({', '.join(over)}); zvětši "
                                                   "envelope a zapiš úkol pro role v used_by"))
            if c.status == "verified" and e.get("version") is not None:
                seen = visual_version(section_text(note.body.replace("\r\n", "\n"), "Vizuálně ověřeno") or "")
                if seen is None:
                    out.append(("info", c.name, f, "ověřeno bez verze v ## Vizuálně ověřeno"))
                elif isinstance(e["version"], (int, float)) and seen < e["version"]:
                    old_verified.setdefault(f"{e['version_prefix']}\x00{e['version']}", []).append(c.name)
            used = set(c.used_by)
            for ent in sorted({d["entity"] for x in mine for d in x.get("data") or [] if d.get("entity")} - used):
                # used_by s potomkem entity souboru nález nedělá (zadání 0.28, CR-037)
                if model is not None and ent in getattr(model, "entities", {}) \
                        and used & set(model.subtree(ent)[1:]):
                    continue
                out.append(("info", c.name, f, f"asset je v datech entity {ent}, která není v used_by karty"))
        if not c.used_by and not any(x.get("data") for x in mine):
            out.append(("info", c.name, f, "karta bez used_by a bez výskytu v datech"))
        if c.status == "requested":
            d = as_date(c.requested)
            if not c.owner:
                out.append(("info", c.name, f, "requested bez owner"))
            elif d is not None and (day - d).days > req_days:
                out.append(("info", c.name, f, f"requested bez převzetí déle než {req_days} dní (od {d.isoformat()})"))
    for k, names in sorted(old_verified.items()):           # seskupeně podle prefixu verze
        prefix, version = k.split("\x00")
        out.append(("warning", f"verze:{prefix}", manifest_file,
                    f"{len(names)} karet verified se starší verzí než kód ({prefix} → {version}): "
                    + ", ".join(sorted(names)) + "; přeověř (GameDesigner)"))
    return out


def summary(vault, man: Manifest | None, library: list[dict]) -> str:
    if man is None:
        return f"knihovna assetů: {SOURCES_REL} chybí, etapa B přeskočena (13 kap. 10.18)"
    free = len({e["key"] for e in library if not e.get("card")})
    return f"knihovna assetů: {len(library)} assetů z kódu, {free} klíčů bez karty"

