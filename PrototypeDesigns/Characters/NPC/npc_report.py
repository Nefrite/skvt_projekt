"""
Kontrola NPC a hlidkovych tras v aktualni mape:
  - kazde NPC: chovani, trasa, zda stoji na navmeshi
  - kazda trasa: zda body lezi na navmeshi a zda mezi nimi existuje cesta
Problemova NPC / body se vyberou ve viewportu.

Pouziti: File -> Execute Python Script... -> vybrat tento soubor
         (navmesh musi byt vygenerovany - klavesa P ve viewportu)
Vystup: Output Log + Saved/NPCReport.csv
"""
import csv
import os
import unreal

# --- Nastaveni ---------------------------------------------------------------
POINT_CLASS_NAME = "BP_PatrolPoint_C"
ROUTE_CLASS_NAME = "BP_PatrolRoute_C"
NPC_CLASS_PREFIX = "BP_NPC"
NAV_EXTENT = unreal.Vector(50.0, 50.0, 150.0)   # tolerance pri hledani navmeshe pod bodem
# -----------------------------------------------------------------------------

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()


def cls(a):
    return a.get_class().get_name()


def on_nav(loc):
    try:
        res = unreal.NavigationSystemV1.project_point_to_navigation(
            world, loc, None, None, NAV_EXTENT)
    except Exception as ex:
        unreal.log_warning(f"[NPCReport] project_point_to_navigation: {ex}")
        return None
    if res is None or isinstance(res, bool):
        return bool(res)
    if isinstance(res, tuple):
        return bool(res[0]) if isinstance(res[0], bool) else True
    return True


def path_ok(a, b):
    try:
        p = unreal.NavigationSystemV1.find_path_to_location_synchronously(world, a, b)
    except Exception:
        return None
    if p is None or not p.is_valid():
        return False
    return not p.is_partial()


def main():
    actors = actor_sub.get_all_level_actors()
    npcs = [a for a in actors if cls(a).startswith(NPC_CLASS_PREFIX)]
    routes = [a for a in actors if cls(a) == ROUTE_CLASS_NAME]
    rows, bad = [], []

    for n in sorted(npcs, key=lambda x: x.get_actor_label()):
        try:
            beh = str(n.get_editor_property("Behavior"))
        except Exception:
            beh = "?"
        try:
            route = n.get_editor_property("PatrolRoute")
        except Exception:
            route = None
        nav = on_nav(n.get_actor_location())
        ok = nav is not False
        if not ok:
            bad.append(n)
        rows.append(["NPC", n.get_actor_label(), beh,
                     route.get_actor_label() if route else "-",
                     "ano" if nav else ("ne" if nav is False else "?"), "", "OK" if ok else "CHYBA"])

    for r in sorted(routes, key=lambda x: x.get_actor_label()):
        pts = [p for p in (r.get_editor_property("Points") or []) if p]
        ping = r.get_editor_property("PingPong")
        if len(pts) == 0:
            rows.append(["ROUTE", r.get_actor_label(), "", "", "", "0 bodu", "CHYBA"])
            bad.append(r)
            continue
        for i, p in enumerate(pts):
            loc = p.get_actor_location()
            nav = on_nav(loc)
            if ping:
                nxt = i + 1 if i + 1 < len(pts) else None
            else:
                nxt = (i + 1) % len(pts) if len(pts) > 1 else None
            path = path_ok(loc, pts[nxt].get_actor_location()) if nxt is not None else True
            ok = nav is not False and path is not False
            if not ok:
                bad.append(p)
            rows.append(["POINT", p.get_actor_label(), r.get_actor_label(),
                         f"wait {p.get_editor_property('WaitTime'):.1f}s",
                         "ano" if nav else ("ne" if nav is False else "?"),
                         ("-> " + pts[nxt].get_actor_label() + (" cesta OK" if path else " BEZ CESTY"))
                         if nxt is not None else "konec",
                         "OK" if ok else "CHYBA"])

    header = ["Typ", "Nazev", "Chovani/Trasa", "Info", "Na navmeshi", "Cesta", "Stav"]
    for row in rows:
        line = "[NPCReport] " + " | ".join(str(c) for c in row)
        (unreal.log_warning if row[-1] != "OK" else unreal.log)(line)

    path = os.path.join(unreal.Paths.convert_relative_path_to_full(
        unreal.Paths.project_saved_dir()), "NPCReport.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(header)
        w.writerows(rows)

    if bad:
        actor_sub.set_selected_level_actors(bad)
    unreal.log(f"[NPCReport] NPC {len(npcs)}, tras {len(routes)}, problemu {len(bad)} (vybrany). CSV: {path}")


main()
