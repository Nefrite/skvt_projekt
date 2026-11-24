"""Karty knihovních assetů (`type: asset`; zadání 13 kap. 10.16, 01 kap. 9.5, 12 kap. 4.6; zadání 0.23).

Karta není entita ani dokument: nemá hub ani `depth`; entity na ni odkazují přes `used_by` v kartě. Modul skládá
přehledy, které čtou `agenda` (výroba a požadavky), `hubs` (blok `## Assety` v hubu entity) a `doc_index`.
Stav mění role; skripty ho jen čtou.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .model import Model
from .util import as_date, as_list
from .vault import Note, Vault

STATUS_ORDER = ["requested", "in_progress", "generated", "imported", "verified", "rejected", "superseded"]
AT_LEAST_GENERATED = {"generated", "imported", "verified"}      # závislost už nebrání výrobě (13 kap. 10.16)
CLOSED = {"verified", "rejected", "superseded"}                 # požadavek žadatele už není otevřený
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
DEFAULT_PRIORITY = "medium"                                     # 01 kap. 9.1
DEFAULT_STAND_IN = "none"
WORK_MODULE = "asset_work"                                      # role, která assety vyrábí (12 kap. 4.6)
DEFAULT_OWNER = "Crafter"                                       # asset_default_owner (13 kap. 4, 10.18)
HUB_HEADING = "Assety"


@dataclass
class Card:
    name: str
    rel: str
    status: str
    kind: str
    category: str
    priority: str
    requested: str | None
    requested_by: list[str]
    owner: str
    stand_in: str
    used_by: list[str]
    depends_on: list[str]
    blocked_by: list[str] = field(default_factory=list)
    variants: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"name": self.name, "path": self.rel, "asset_status": self.status, "asset_kind": self.kind,
                "asset_category": self.category, "priority": self.priority, "requested": self.requested,
                "requested_by": self.requested_by, "owner": self.owner, "stand_in": self.stand_in,
                "used_by": self.used_by, "depends_on": self.depends_on, "blocked_by": self.blocked_by,
                "variants": self.variants}


def _names(value) -> list[str]:
    return [str(v).strip() for v in as_list(value) if str(v or "").strip()]


def cards(vault: Vault, m: Model | None = None) -> list[Card]:
    """Všechny karty assetů vaultu (mimo `_core/` a `_to_delete/`), seřazené podle jména."""
    m = m or Model(vault)
    out: list[Card] = []
    for n in sorted(m.notes, key=lambda x: x.name):
        if n.type != "asset":
            continue
        fm = n.fm
        d = as_date(fm.get("requested"))
        out.append(Card(
            name=n.name, rel=n.rel, status=str(fm.get("asset_status") or ""), kind=str(fm.get("asset_kind") or ""),
            category=str(fm.get("asset_category") or ""),
            priority=str(fm.get("priority") or DEFAULT_PRIORITY),
            requested=d.isoformat() if d else None, requested_by=_names(fm.get("requested_by")),
            owner=str(fm.get("owner") or "").strip(), stand_in=str(fm.get("stand_in") or DEFAULT_STAND_IN),
            used_by=m.link_names(fm.get("used_by")), depends_on=m.link_names(fm.get("depends_on")),
            variants=_names(fm.get("variants"))))
    by_name = {c.name: c for c in out}
    for c in out:                       # blokovaná karta: závislost není aspoň generated (i neexistující)
        c.blocked_by = [d for d in c.depends_on if (by_name.get(d) and by_name[d].status) not in AT_LEAST_GENERATED]
    return out


def _sort_key(c: Card) -> tuple:
    return PRIORITY_ORDER.get(c.priority, 9), c.requested or "9999-99-99", c.name


def role_modules(vault: Vault, role: str) -> list[str]:
    """Moduly z profilu role (`Roles/<Role>.md`, jinak role core v `_core/agents/`)."""
    key = role.casefold()
    for rel, n in vault.notes.items():
        if n.type == "role" and n.name.casefold() == key and (rel.startswith("Roles/") and rel.count("/") == 1):
            return [str(x) for x in as_list((n.fm or {}).get("modules")) if x]
    from . import CORE_ROOT
    core = CORE_ROOT / "agents" / f"{role}.md"
    if core.is_file():
        from .frontmatter import parse
        from .fileio import read_text
        fm, _sp = parse(read_text(core))
        return [str(x) for x in as_list((fm or {}).get("modules")) if x]
    return []


def default_owner(vault: Vault) -> str:
    """Role, které `agenda` ukáže karty `requested` bez `owner` (`asset_default_owner`, zadání 0.25)."""
    return str(vault.config.get("asset_default_owner") or DEFAULT_OWNER).strip()


def agenda_part(vault: Vault, role: str, m: Model | None = None) -> dict | None:
    """Karty pro `agenda --role` (13 kap. 10.16, 10.18): výroba pro roli s `asset_work` (karty bez `owner` jen roli
    `asset_default_owner`, ostatní jen se svým `owner`), otevřené požadavky žadatele."""
    all_cards = cards(vault, m)
    if not all_cards:
        return None
    key = role.casefold()
    works = WORK_MODULE in role_modules(vault, role)
    is_default = default_owner(vault).casefold() == key
    work: list[Card] = []
    if works:
        for c in all_cards:
            owner = c.owner.casefold()
            if c.status == "requested" and (owner == key or (not owner and is_default)):
                work.append(c)
            elif c.status == "in_progress" and owner == key:
                work.append(c)
        work.sort(key=_sort_key)
    mine = [c for c in all_cards if key in {r.casefold() for r in c.requested_by} and c.status not in CLOSED]
    # karty imported bez grayboxu jen počtem; seznam = požadavky čekající na výrobu a karty s grayboxem
    # (zadání 0.28, CR-036); requested_by: legacy žádné roli nepatří
    done = [c for c in mine if c.status == "imported" and c.stand_in == DEFAULT_STAND_IN]
    requests = sorted((c for c in mine if c not in done), key=_sort_key)
    if not works and not requests and not done:
        return None
    return {"work": [c.as_dict() for c in work] if works else None, "requests": [c.as_dict() for c in requests],
            "imported_without_stand_in": len(done)}


def card_line(c: dict, with_owner: bool = False) -> str:
    extra = [c["asset_status"], c["priority"]]
    if c.get("requested"):
        extra.append(f"požadováno {c['requested']}")
    if with_owner and c.get("owner"):
        extra.append(f"owner {c['owner']}")
    if c.get("used_by"):
        extra.append("pro " + ", ".join(c["used_by"]))
    blocked = f" · BLOKOVÁNO: čeká na {', '.join(c['blocked_by'])}" if c.get("blocked_by") else ""
    return f"- {c['path']} — {c['name']} · {' · '.join(extra)}{blocked}"


SUMMARY_STATES = ["requested", "in_progress", "generated", "imported", "verified"]


def entity_summary(entity: str, all_cards: list[Card], outdated: set[str] | None) -> dict | None:
    """Souhrn assetů entity (13 kap. 10.19, CR-029 bod 6): počty podle stavu, grayboxy, `outdated` z reportu UE
    (None = report assetů neexistuje). Jen signál vedle `depth_*`; hloubka se z něj nepočítá."""
    mine = [c for c in all_cards if entity in c.used_by]
    if not mine:
        return None
    out = {s: sum(1 for c in mine if c.status == s) for s in SUMMARY_STATES}
    out["graybox"] = sum(1 for c in mine if c.stand_in == "graybox")
    out["outdated"] = (None if outdated is None else
                       sum(1 for c in mine if {c.name, *c.variants} & outdated))
    return out


def summary_line(s: dict) -> str:
    states = ", ".join(f"{k} {s[k]}" for k in SUMMARY_STATES)
    out = "—" if s.get("outdated") is None else s["outdated"]
    return (f"Souhrn: {states} · graybox {s['graybox']} · outdated v UE {out} "
            "(signál vedle `depth_*`, hloubka se z něj nepočítá)")


def hub_block(entity: str, all_cards: list[Card], outdated: set[str] | None = None) -> str | None:
    """Obsah bloku `## Assety` v hubu entity (13 kap. 10.16, 10.19); None = entita nemá kartu v `used_by`."""
    mine = [c for c in all_cards if entity in c.used_by]
    if not mine:
        return None
    order = {s: i for i, s in enumerate(STATUS_ORDER)}
    mine.sort(key=lambda c: (order.get(c.status, 99), c.name))
    rows = [f"| [[{c.name}]] | {c.status or '–'} | {c.stand_in} |" for c in mine]
    summary = summary_line(entity_summary(entity, all_cards, outdated))
    return "\n".join([summary, "", "| Asset | Stav | Náhrada v levelu |", "|---|---|---|", *rows])
