"""Taxonomie: core (`taxonomy/`) ∪ instance (`Maintenance/taxonomy_local/`) (zadání 13, kap. 5).

Sloučení = core ∪ local; kolize id = chyba konfigurace; lokálně nejde hodnoty odebírat.
Výčet (enums.yaml) smí instance rozšířit jen s `open: true`.
Jen lokální soubory: build_steps.yaml, milestones.yaml, tech.yaml (folder_map, tag_map ve fázi 3+).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .errors import ConfigError

# soubor -> klíč identity položky
KEYED_FILES = {
    "domains.yaml": "id",
    "categories.yaml": "id",
    "kinds.yaml": "id",
    "types.yaml": "id",
    "fields.yaml": "name",
    "depth.yaml": "value",
    "findings.yaml": "code",
    "build_step_catalog.yaml": "id",
}
# Soubory, které instance rozšiřovat nesmí (nejsou to výčty hodnot).
CORE_ONLY = {"fields.yaml", "depth.yaml", "findings.yaml", "hub_sections.yaml", "defaults.yaml"}
LOCAL_ONLY = {"build_steps.yaml", "milestones.yaml", "tech.yaml", "folder_map.yaml", "tag_map.yaml", "ue_map.yaml"}

_COND_IN = re.compile(r"^(\w+|<\w+>)\s+in\s+\[(.*)\]$")
_COND_EQ = re.compile(r"^(\w+)\s*==\s*(\S+)$")
_COND_PRESENT = re.compile(r"^([\w<>]+)\s+present$")
_COND_PRESENT_BUILD = re.compile(r"^([\w<>]+)\s+present in build mode$")
TARGET_MODES = ("design", "build")          # režim cíle (01 kap. 5)
DEFAULT_TARGET_MODE = "build"               # jen pojistka; u lokální domény je target_mode povinný


def load_yaml(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise ConfigError(f"Neplatný YAML: {path}: {exc}") from exc
    except OSError as exc:
        raise ConfigError(f"Nelze číst {path}: {exc}") from exc


def _items(data, path: Path) -> list[dict]:
    if data is None:
        return []
    if not isinstance(data, dict) or not isinstance(data.get("items", []), list):
        raise ConfigError(f"Očekávám mapu s klíčem items (seznam): {path}")
    return list(data.get("items") or [])


def normalize_required(value) -> str:
    """`required` z fields.yaml: always / no / podmínka. YAML `no` se čte jako False."""
    if value is False or value is None:
        return "no"
    if value is True:
        return "always"
    return str(value).strip()


@dataclass
class Condition:
    kind: str                 # always / no / in / eq / present
    field: str = ""
    values: tuple = ()

    def evaluate(self, fm: dict, type_id: str, domain: str | None = None, mode: str | None = None) -> bool:
        if self.kind == "always":
            return True
        if self.kind in ("no", "project_role"):    # project_role závisí na cestě: vyhodnocuje validate
            return False
        fname = self.field.replace("<domain>", domain or "")
        actual = type_id if fname == "type" else fm.get(fname)
        if self.kind == "present":
            return not is_empty(actual)
        if self.kind == "present_build":                 # u vzoru: cíl domény a režim build (01 kap. 9.1)
            return not is_empty(actual) and mode == "build"
        if self.kind == "eq":
            return actual is not None and str(actual) == self.values[0]
        if self.kind == "in":
            return actual is not None and str(actual) in self.values
        return False


def parse_condition(text: str) -> Condition:
    text = normalize_required(text)
    if text in ("always", "no"):
        return Condition(text)
    if text == "project_role":          # profil projektové role Roles/<Role>.md (zadání 0.17); podle cesty, lint
        return Condition("project_role")
    m = _COND_IN.match(text)
    if m:
        vals = tuple(v.strip() for v in m.group(2).split(",") if v.strip())
        return Condition("in", m.group(1), vals)
    m = _COND_EQ.match(text)
    if m:
        return Condition("eq", m.group(1), (m.group(2),))
    m = _COND_PRESENT_BUILD.match(text)
    if m:
        return Condition("present_build", m.group(1))
    m = _COND_PRESENT.match(text)
    if m:
        return Condition("present", m.group(1))
    raise ConfigError(f"Neznámá podmínka required ve fields.yaml: {text!r}")


def is_empty(value) -> bool:
    return value is None or value == "" or value == [] or value == {}


@dataclass
class FieldDef:
    name: str
    section: str
    applies_to: list[str]
    value: str
    required: Condition
    items: str | None = None
    allow_empty: bool = False
    section_entity: str | None = None
    spec: str = "01 kap. 9.1"
    pattern: bool = False

    def section_for(self, type_id: str) -> str:
        if type_id == "entity" and self.section_entity:
            return self.section_entity
        return self.section


@dataclass
class Taxonomy:
    domains: dict = field(default_factory=dict)
    categories: dict = field(default_factory=dict)
    kinds: dict = field(default_factory=dict)
    types: dict = field(default_factory=dict)
    fields: dict = field(default_factory=dict)          # name -> FieldDef (vzory s <domain>)
    depth: dict = field(default_factory=dict)
    findings: dict = field(default_factory=dict)
    hub_sections: list = field(default_factory=list)
    build_step_catalog: dict = field(default_factory=dict)
    enums: dict = field(default_factory=dict)           # name -> {"values": [...], "open": bool, "spec": str}
    build_steps: dict = field(default_factory=dict)     # lokální cesta instance: id -> položka
    milestones: dict = field(default_factory=dict)      # id -> položka
    tech: dict = field(default_factory=dict)            # id -> položka
    folder_map: list = field(default_factory=list)      # položky folder_map.yaml (13 kap. 10.2)
    tag_map: dict = field(default_factory=dict)         # externí tag -> kategorie (import inboxu, fáze 10)
    ue_map: dict | None = None                          # taxonomy_local/ue_map.yaml (13 kap. 10.11); None = Unreal se nečte
    ue_map_path: Path | None = None
    problems: list = field(default_factory=list)        # (soubor, zpráva) – nálezy G7 v lokální taxonomii

    # ------------------------------------------------------------ dotazy
    def enum_values(self, name: str) -> list:
        if name == "type":
            return list(self.types)
        if name == "domain":
            return list(self.domains)
        if name == "category":
            return list(self.categories)
        if name == "kind":
            return list(self.kinds)
        if name == "build_step":
            return list(self.build_steps)
        if name == "milestone":
            return list(self.milestones)
        if name == "tech":
            return list(self.tech)
        if name in self.enums:
            return list(self.enums[name]["values"])
        raise ConfigError(f"Neznámý výčet enum:{name}")

    def field_for_key(self, key: str) -> tuple[FieldDef | None, str | None]:
        """Definice pole pro klíč frontmatteru; u vzorů i doménu (depth_structures -> structures)."""
        if key in self.fields:
            return self.fields[key], None
        for fd in self.fields.values():
            if fd.pattern:
                prefix = fd.name.split("<domain>")[0]
                if key.startswith(prefix) and key[len(prefix):] in self.domains:
                    return fd, key[len(prefix):]
        return None, None

    def default_mode(self, domain: str) -> str:
        """Výchozí režim cíle domény (`domains.yaml`, `target_mode`; 01 kap. 3, 5)."""
        return (self.domains.get(domain) or {}).get("target_mode") or DEFAULT_TARGET_MODE

    def target_mode(self, fm: dict, domain: str) -> str:
        """Režim cíle entity v doméně: `target_mode_<domain>`, jinak výchozí režim domény."""
        v = fm.get(f"target_mode_{domain}")
        return v if v in TARGET_MODES else self.default_mode(domain)

    def has_depth(self, type_id: str) -> bool:
        """Typ dokumentu nese `depth` (01 kap. 5, zadání 0.13.3)."""
        fd = self.fields.get("depth")
        return bool(fd and type_id in fd.applies_to)

    def fields_for_type(self, type_id: str) -> list[FieldDef]:
        return [fd for fd in self.fields.values() if type_id in fd.applies_to]

    def game_section(self, type_id: str) -> str:
        return self.types.get(type_id, {}).get("game_section", "none")

    def severity(self, code: str) -> str:
        return self.findings.get(code, {}).get("severity", "error")


# ---------------------------------------------------------------- načtení

def _merge_keyed(core: list[dict], local: list[dict], key: str, fname: str) -> dict:
    out: dict = {}
    for src, items in (("core", core), ("local", local)):
        for it in items:
            if not isinstance(it, dict) or key not in it:
                raise ConfigError(f"{fname} ({src}): položka bez klíče {key}: {it!r}")
            k = it[key]
            if k in out:
                raise ConfigError(f"{fname}: kolize {key}={k!r} ({src})")
            out[k] = dict(it, _source=src)
    return out


def _merge_enums(core: list[dict], local: list[dict]) -> dict:
    out: dict = {}
    for it in core:
        out[it["name"]] = {"values": list(it.get("values") or []), "open": bool(it.get("open")),
                           "spec": it.get("spec", "")}
    for it in local:
        name = it.get("name")
        vals = list(it.get("values") or [])
        if name in out:
            if not out[name]["open"]:
                raise ConfigError(f"enums.yaml (local): výčet {name} není otevřený, nelze rozšířit")
            for v in vals:
                if v in out[name]["values"]:
                    raise ConfigError(f"enums.yaml (local): kolize hodnoty {name}={v!r}")
                out[name]["values"].append(v)
        else:
            out[name] = {"values": vals, "open": bool(it.get("open")), "spec": "local"}
    return out


def _build_fields(items: list[dict]) -> dict:
    out = {}
    for it in items:
        name = it["name"]
        applies = it.get("applies_to") or []
        out[name] = FieldDef(
            name=name,
            section=it.get("section", "orchestration"),
            applies_to=list(applies),
            value=str(it.get("value", "text")),
            required=parse_condition(it.get("required", "no")),
            items=it.get("items"),
            allow_empty=bool(it.get("allow_empty", False)),
            section_entity=it.get("section_entity"),
            spec=it.get("spec", "01 kap. 9.1"),
            pattern="<domain>" in name,
        )
    return out


def load(core_dir: Path, local_dir: Path | None = None) -> Taxonomy:
    core_dir = Path(core_dir)
    if not core_dir.is_dir():
        raise ConfigError(f"Chybí složka taxonomie core: {core_dir}")
    local_dir = Path(local_dir) if local_dir else None
    if local_dir is not None and not local_dir.is_dir():
        local_dir = None

    def core_items(fname):
        return _items(load_yaml(core_dir / fname), core_dir / fname)

    def local_items(fname):
        if local_dir is None or not (local_dir / fname).is_file():
            return []
        if fname in CORE_ONLY:
            raise ConfigError(f"taxonomy_local/{fname}: tento soubor instance nerozšiřuje")
        return _items(load_yaml(local_dir / fname), local_dir / fname)

    tx = Taxonomy()
    merged = {f: _merge_keyed(core_items(f), local_items(f), k, f) for f, k in KEYED_FILES.items()}
    tx.domains = merged["domains.yaml"]
    tx.categories = merged["categories.yaml"]
    tx.kinds = merged["kinds.yaml"]
    tx.types = merged["types.yaml"]
    tx.depth = merged["depth.yaml"]
    tx.findings = merged["findings.yaml"]
    tx.build_step_catalog = merged["build_step_catalog.yaml"]
    tx.fields = _build_fields(list(merged["fields.yaml"].values()))
    tx.hub_sections = core_items("hub_sections.yaml")
    tx.enums = _merge_enums(core_items("enums.yaml"), local_items("enums.yaml"))
    _check_refs(tx)
    if local_dir is not None:
        _load_local_only(tx, local_dir)
    return tx


def _check_refs(tx: Taxonomy) -> None:
    for cid, c in tx.categories.items():
        for d in [c.get("home_domain"), *(c.get("overlaps") or [])]:
            if d not in tx.domains:
                raise ConfigError(f"categories.yaml: {cid} odkazuje na neznámou doménu {d!r}")
    for did, d in tx.domains.items():
        if d.get("_source") == "local" and d.get("target_mode") is None:     # 13 kap. 5, zadání 0.13.5
            raise ConfigError(f"taxonomy_local/domains.yaml: doména {did} nemá target_mode; doplň výchozí režim cíle "
                              f"domény: design (stačí navrhnout) nebo build (vymodelovat, implementovat)")
        if d.get("target_mode") not in (None, *TARGET_MODES):
            raise ConfigError(f"domains.yaml: {did}: target_mode {d['target_mode']!r} mimo {'/'.join(TARGET_MODES)}")
    for kid, k in tx.kinds.items():
        for d in k.get("expected_domains") or []:
            if d not in tx.domains:
                raise ConfigError(f"kinds.yaml: {kid} odkazuje na neznámou doménu {d!r}")
    for fd in tx.fields.values():
        for t in fd.applies_to:
            if t not in tx.types:
                raise ConfigError(f"fields.yaml: {fd.name} odkazuje na neznámý typ {t!r}")
        for v in (fd.value, fd.items or ""):
            if v.startswith("enum:"):
                tx.enum_values(v[5:])          # ověří, že výčet existuje


def _load_local_only(tx: Taxonomy, local_dir: Path) -> None:
    def load_list(fname, key):
        p = local_dir / fname
        if not p.is_file():
            return None, p
        data = load_yaml(p) or {}
        if not isinstance(data, dict):
            raise ConfigError(f"Očekávám mapu: {p}")
        items = data.get(key) or []
        if not isinstance(items, list):
            raise ConfigError(f"{p}: klíč {key} musí být seznam")
        return items, p

    steps, p = load_list("build_steps.yaml", "steps")
    for st in steps or []:
        sid = st.get("id")
        if sid in tx.build_steps:
            raise ConfigError(f"{p}: duplicitní id kroku {sid!r}")
        tx.build_steps[sid] = st
        if st.get("type") and st["type"] not in tx.build_step_catalog:
            tx.problems.append((p, f"krok {sid}: typ {st['type']!r} není v katalogu build_step_catalog"))
        if st.get("status") and st["status"] not in tx.enums["build_step_status"]["values"]:
            tx.problems.append((p, f"krok {sid}: neplatný status {st['status']!r}"))

    ms, p = load_list("milestones.yaml", "milestones")
    orders: dict = {}
    for m in ms or []:
        mid = m.get("id")
        if mid in tx.milestones:
            raise ConfigError(f"{p}: duplicitní id milníku {mid!r}")
        tx.milestones[mid] = m
        o = m.get("order")
        if o in orders:
            tx.problems.append((p, f"milník {mid}: duplicitní order {o} (také {orders[o]})"))
        orders[o] = mid
        if m.get("trigger") and m["trigger"] not in tx.enums["milestone_trigger"]["values"]:
            tx.problems.append((p, f"milník {mid}: neplatný trigger {m['trigger']!r}"))

    tech, p = load_list("tech.yaml", "items")
    for t in tech or []:
        tid = t.get("id") if isinstance(t, dict) else t
        if tid in tx.tech:
            raise ConfigError(f"{p}: duplicitní tech {tid!r}")
        tx.tech[tid] = t

    # 13 kap. 10.2: folder_map (path, entity, build_step, domains, role) a tag_map (tag, category)
    fmap, p = load_list("folder_map.yaml", "items")
    roles = tx.enums.get("asset_role", {}).get("values", [])
    for it in fmap or []:
        if not isinstance(it, dict) or not str(it.get("path") or "").strip():
            tx.problems.append((p, f"folder_map: položka bez path: {it!r}"))
            continue
        tx.folder_map.append(it)
        if it.get("build_step") and it["build_step"] not in tx.build_steps:
            tx.problems.append((p, f"folder_map {it['path']}: build_step {it['build_step']!r} není v build_steps.yaml"))
        for d in it.get("domains") or []:
            if d not in tx.domains:
                tx.problems.append((p, f"folder_map {it['path']}: doména {d!r} mimo výčet domén"))
        if it.get("role") and it["role"] not in roles:
            tx.problems.append((p, f"folder_map {it['path']}: role {it['role']!r} mimo výčet asset_role"))
    tmap, p = load_list("tag_map.yaml", "items")
    for it in tmap or []:
        if not isinstance(it, dict) or not it.get("tag"):
            tx.problems.append((p, f"tag_map: položka bez tag: {it!r}"))
            continue
        if it.get("category") not in tx.categories:
            tx.problems.append((p, f"tag_map {it['tag']}: kategorie {it.get('category')!r} mimo výčet kategorií"))
        tx.tag_map[str(it["tag"])] = it.get("category")
    _load_ue_map(tx, local_dir / "ue_map.yaml")


UE_MAP_KEYS = {"map", "stage_tag_prefix", "placeholder_ignore", "defaults", "items"}
UE_RULE_KEYS = {"tags", "folders"}


def _ue_paths(val, where: str, problems: list) -> list[str]:
    """placeholder_ignore (zadání 0.22, CR-024): seznam cest meshů; jiný tvar = problém (G7)."""
    if val is None:
        return []
    if not isinstance(val, list) or not all(isinstance(x, str) and x.strip() for x in val):
        problems.append(f"{where} musí být seznam textů (cesty meshů, např. /Engine/BasicShapes/Cube.Cube)")
        return []
    return [x.strip() for x in val]


def _ue_rule(raw, where: str, problems: list) -> dict | None:
    """Pravidlo {tags: [...], folders: [...]}; None = neplatné (problém zapsán)."""
    if not isinstance(raw, dict):
        problems.append(f"{where}: pravidlo musí být mapa s tags nebo folders")
        return None
    extra = set(raw) - UE_RULE_KEYS - {"entity", "placeholder_ignore"}
    if extra:
        problems.append(f"{where}: neznámé klíče {', '.join(sorted(extra))}")
    rule = {}
    for key in ("tags", "folders"):
        val = raw.get(key)
        if val is None:
            continue
        if not isinstance(val, list) or not all(isinstance(x, str) and x.strip() for x in val):
            problems.append(f"{where}: {key} musí být seznam textů")
            return None
        rule[key] = [x.strip() for x in val]
    if not rule:
        problems.append(f"{where}: pravidlo bez tags i folders")
        return None
    return rule


def _load_ue_map(tx: Taxonomy, p: Path) -> None:
    """ue_map.yaml (13 kap. 10.11): map, stage_tag_prefix, defaults podle kind, items s entity; chyby = problémy (G7)."""
    if not p.is_file():
        return
    data = load_yaml(p)
    problems: list[str] = []
    out = {"map": "", "stage_tag_prefix": "stage:", "placeholder_ignore": [], "placeholder_ignore_items": {},
           "defaults": {}, "items": []}
    if not isinstance(data, dict):
        tx.problems.append((p, "ue_map: soubor musí být mapa (map, stage_tag_prefix, defaults, items)"))
        tx.ue_map, tx.ue_map_path = out, p
        return
    extra = set(data) - UE_MAP_KEYS
    if extra:
        problems.append(f"ue_map: neznámé klíče {', '.join(sorted(extra))}")
    for key in ("map", "stage_tag_prefix"):
        if data.get(key) is not None:
            if isinstance(data[key], str):
                out[key] = data[key]
            else:
                problems.append(f"ue_map: {key} musí být text")
    out["placeholder_ignore"] = _ue_paths(data.get("placeholder_ignore"), "ue_map: placeholder_ignore", problems)
    defaults = data.get("defaults") or {}
    if not isinstance(defaults, dict):
        problems.append("ue_map: defaults musí být mapa kind → pravidlo")
        defaults = {}
    for kind, raw in defaults.items():
        if kind not in tx.kinds:
            problems.append(f"ue_map defaults: kind {kind!r} mimo výčet")
            continue
        rule = _ue_rule(raw, f"ue_map defaults {kind}", problems)
        if rule:
            out["defaults"][kind] = rule
    items = data.get("items") or []
    if not isinstance(items, list):
        problems.append("ue_map: items musí být seznam")
        items = []
    for i, raw in enumerate(items, 1):
        ent = raw.get("entity") if isinstance(raw, dict) else None
        if not isinstance(ent, str) or not ent.strip():
            problems.append(f"ue_map items: položka {i} bez entity")
            continue
        ign = _ue_paths(raw.get("placeholder_ignore"), f"ue_map {ent}: placeholder_ignore", problems)
        if "placeholder_ignore" in raw:
            out["placeholder_ignore_items"].setdefault(ent.strip(), []).extend(ign)
        if "placeholder_ignore" in raw and not (set(raw) & UE_RULE_KEYS):
            continue                                 # položka jen s placeholder_ignore: pravidlo z defaults
        rule = _ue_rule(raw, f"ue_map {ent}", problems)
        if rule:
            out["items"].append({"entity": ent.strip(), **rule})
    tx.problems += [(p, m) for m in problems]
    tx.ue_map, tx.ue_map_path = out, p
