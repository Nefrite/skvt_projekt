"""
Z vybranych BP_PatrolPoint vytvori BP_PatrolRoute (poradi bodu = poradi vyberu,
nebo podle nazvu). Pokud jsou ve vyberu i NPC, priradi jim tuto trasu.

Pouziti v Unreal Editoru:
  1) Rozmistit BP_PatrolPoint (Alt + tazeni = kopie)
  2) Vybrat je postupne Ctrl + klik v poradi, v jakem se maji navstevovat
     (volitelne pridat do vyberu NPC, ktere maji trasu chodit)
  3) File -> Execute Python Script... -> vybrat tento soubor
  Akce jde vratit pres Ctrl+Z.

Pokud je ve vyberu existujici BP_PatrolRoute, trasa se neprida nova,
ale prepise se tato (body se nahradi vybranymi).
"""
import unreal

# --- Nastaveni ---------------------------------------------------------------
ROUTE_BP = "/Game/Skvt/Characters/NPC/Patrol/BP_PatrolRoute"
POINT_CLASS_NAME = "BP_PatrolPoint_C"
ROUTE_CLASS_NAME = "BP_PatrolRoute_C"
NPC_CLASS_PREFIX = "BP_NPC"     # NPC = trida zacinajici timto nazvem
ORDER = "selection"             # "selection" = poradi vyberu, "label" = abecedne podle nazvu
ROUTE_NAME = ""                 # prazdne = Route_01, Route_02...
PING_PONG = False               # False = dokola (1-2-3-1), True = tam a zpet (1-2-3-2-1)
RENAME_POINTS = True            # prejmenovat body na <Route>_P01, _P02...
# -----------------------------------------------------------------------------

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def cls(a):
    return a.get_class().get_name()


def next_route_name():
    used = {a.get_actor_label() for a in actor_sub.get_all_level_actors()
            if cls(a) == ROUTE_CLASS_NAME}
    i = 1
    while f"Route_{i:02d}" in used:
        i += 1
    return f"Route_{i:02d}"


def main():
    sel = actor_sub.get_selected_level_actors()
    points = [a for a in sel if cls(a) == POINT_CLASS_NAME]
    routes = [a for a in sel if cls(a) == ROUTE_CLASS_NAME]
    npcs = [a for a in sel if cls(a).startswith(NPC_CLASS_PREFIX)]

    if len(points) < 1:
        unreal.log_warning("[Patrol] Ve vyberu neni zadny BP_PatrolPoint")
        return
    if ORDER == "label":
        points.sort(key=lambda p: p.get_actor_label())

    route_class = unreal.EditorAssetLibrary.load_blueprint_class(ROUTE_BP)
    if route_class is None:
        unreal.log_error(f"[Patrol] Nenalezen {ROUTE_BP}")
        return

    with unreal.ScopedEditorTransaction("Make patrol route"):
        if routes:
            route = routes[0]
            name = route.get_actor_label()
            action = "prepsana"
        else:
            first = points[0].get_actor_location()
            route = actor_sub.spawn_actor_from_class(route_class, first, unreal.Rotator(0.0, 0.0, 0.0))
            name = ROUTE_NAME or next_route_name()
            route.set_actor_label(name)
            action = "vytvorena"

        route.set_editor_property("Points", points)
        route.set_editor_property("PingPong", PING_PONG)
        route.set_folder_path(f"Patrol/{name}")

        for i, p in enumerate(points):
            if RENAME_POINTS:
                p.set_actor_label(f"{name}_P{i+1:02d}")
            p.set_folder_path(f"Patrol/{name}")

        for n in npcs:
            n.set_editor_property("PatrolRoute", route)

        route.rerun_construction_scripts()

    unreal.log(f"[Patrol] Trasa {name} {action}: {len(points)} bodu, "
               f"{'tam a zpet' if PING_PONG else 'dokola'}, prirazena {len(npcs)} NPC")
    actor_sub.set_selected_level_actors([route])


main()
