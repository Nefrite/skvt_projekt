"""
Umisti (nebo aktualizuje) BP_Seat na vybrane actory v aktualni mape.

Pouziti v Unreal Editoru:
  1) Edit -> Plugins -> "Python Editor Script Plugin" musi byt zapnuty
  2) Ve viewportu / Outlineru vybrat sedatka (zidle, parezy, stolicky, kameny...)
  3) File -> Execute Python Script... -> vybrat tento soubor
  Akce jde vratit pres Ctrl+Z.

Co skript dela pro kazdy vybrany actor:
  - paprskem shora do stredu actoru najde sedaci plochu
  - paprskem z ni dolu najde podlahu (actor sam se ignoruje) -> SeatHeight
  - na sedaci plochu polozi BP_Seat, natoci ho podle actoru (+ YAW_OFFSET)
    a pripoji ho k actoru (pri presunu zidle se presune i BP_Seat)
  - pokud uz BP_Seat na actoru je, jen ho prepocita
"""
import unreal

# --- Nastaveni ---------------------------------------------------------------
BP_SEAT_PATH = "/Game/Skvt/Interaction/Seat/BP_Seat"
YAW_OFFSET = 0.0        # smer sezeni vuci ose X actoru (stupne): 0, 90, 180, -90
SAMPLE_OFFSET_X = 0.0   # posun mereneho bodu po ose X actoru (cm); u zidli s operadlem napr. 10
TRACE_ABOVE = 50.0      # paprsek zacina tolik cm nad horni hranou bounds
FLOOR_SEARCH = 300.0    # jak hluboko pod sedakem se hleda podlaha (cm)
MIN_HEIGHT = 15.0       # mimo tento rozsah se actor preskoci (neni to sedatko)
MAX_HEIGHT = 120.0
# -----------------------------------------------------------------------------

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()


def trace(start, end, ignore):
    """Line trace (Visibility, complex). Vraci (impact_point, hit_actor) nebo None."""
    res = unreal.SystemLibrary.line_trace_single(
        world, start, end, unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
        True, ignore, unreal.DrawDebugTrace.NONE, True)
    if res is None or isinstance(res, bool):
        return None
    hit = res
    if isinstance(res, tuple):
        if not res[0]:
            return None
        hit = res[-1]
    try:
        b = unreal.GameplayStatics.break_hit_result(hit)
    except Exception:
        b = hit.to_tuple()
    # poradi: blocking_hit, initial_overlap, time, distance, location, impact_point,
    #         normal, impact_normal, phys_mat, hit_actor, ...
    if not b[0]:
        return None
    return b[5], b[9]


def find_existing_seat(actor, seat_class):
    for child in actor.get_attached_actors():
        if child.get_class() == seat_class:
            return child
    return None


def process(actor, seat_class):
    name = actor.get_actor_label()
    origin, extent = actor.get_actor_bounds(False)
    fwd = actor.get_actor_forward_vector()
    sx = origin.x + fwd.x * SAMPLE_OFFSET_X
    sy = origin.y + fwd.y * SAMPLE_OFFSET_X
    top = origin.z + extent.z
    bottom = origin.z - extent.z

    r = trace(unreal.Vector(sx, sy, top + TRACE_ABOVE),
              unreal.Vector(sx, sy, bottom - 10.0), [])
    if r is None or r[1] != actor:
        unreal.log_warning(f"[Seat] {name}: paprsek netrefil actor (zkus SAMPLE_OFFSET_X / kolizi meshe)")
        return False
    seat_point = r[0]

    f = trace(seat_point - unreal.Vector(0, 0, 1),
              seat_point - unreal.Vector(0, 0, FLOOR_SEARCH), [actor])
    if f is None:
        unreal.log_warning(f"[Seat] {name}: pod sedakem nenalezena podlaha")
        return False
    height = seat_point.z - f[0].z
    if height < MIN_HEIGHT or height > MAX_HEIGHT:
        unreal.log_warning(f"[Seat] {name}: vyska {height:.1f} cm mimo rozsah, preskoceno")
        return False

    rot = unreal.Rotator(roll=0.0, pitch=0.0, yaw=actor.get_actor_rotation().yaw + YAW_OFFSET)

    seat = find_existing_seat(actor, seat_class)
    if seat:
        seat.set_actor_location_and_rotation(seat_point, rot, False, True)
        action = "aktualizovano"
    else:
        seat = actor_sub.spawn_actor_from_class(seat_class, seat_point, rot)
        seat.attach_to_actor(actor, "",
                             unreal.AttachmentRule.KEEP_WORLD,
                             unreal.AttachmentRule.KEEP_WORLD,
                             unreal.AttachmentRule.KEEP_WORLD, False)
        action = "vytvoreno"

    seat.set_editor_property("SeatHeight", round(height, 1))
    seat.set_actor_label(f"Seat_{name}")
    unreal.log(f"[Seat] {name}: {action}, SeatHeight = {height:.1f} cm")
    return True


def main():
    seat_class = unreal.EditorAssetLibrary.load_blueprint_class(BP_SEAT_PATH)
    if seat_class is None:
        unreal.log_error(f"[Seat] Nenalezen {BP_SEAT_PATH}")
        return
    selected = [a for a in actor_sub.get_selected_level_actors()
                if a.get_class() != seat_class]
    if not selected:
        unreal.log_warning("[Seat] Neni vybrany zadny actor")
        return
    ok = 0
    with unreal.ScopedEditorTransaction("Place BP_Seat"):
        for a in selected:
            if process(a, seat_class):
                ok += 1
    unreal.log(f"[Seat] Hotovo: {ok} / {len(selected)}")


main()
