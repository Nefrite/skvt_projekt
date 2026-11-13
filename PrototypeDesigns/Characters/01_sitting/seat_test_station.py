"""
Postavi testovaci "sedatka" (kvadry) ruzne vysky pred kamerou viewportu
a vybere je. Pak staci spustit seat_place_selected.py.

Pouziti: natocit kameru viewportu na volnou plochu ->
         File -> Execute Python Script... -> vybrat tento soubor
Akce jde vratit pres Ctrl+Z.
"""
import unreal

# --- Nastaveni ---------------------------------------------------------------
HEIGHTS = [30, 45, 60]   # vysky sedaku v cm
SIZE = 50.0              # pudorys kvadru (cm)
SPACING = 150.0          # rozestup (cm)
DISTANCE = 500.0         # vzdalenost od kamery (cm)
CUBE_PATH = "/Engine/BasicShapes/Cube"   # 100 cm, pivot uprostred
# -----------------------------------------------------------------------------

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ed_sub = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
world = ed_sub.get_editor_world()


def floor_z(x, y, from_z):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, from_z), unreal.Vector(x, y, from_z - 20000.0),
        unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, True, [],
        unreal.DrawDebugTrace.NONE, True)
    if res is None or isinstance(res, bool):
        return None
    hit = res[-1] if isinstance(res, tuple) else res
    if isinstance(res, tuple) and not res[0]:
        return None
    try:
        b = unreal.GameplayStatics.break_hit_result(hit)
    except Exception:
        b = hit.to_tuple()
    return b[5].z if b[0] else None


def main():
    cam_loc, cam_rot = ed_sub.get_level_viewport_camera_info()
    yaw = cam_rot.yaw
    flat_rot = unreal.Rotator(roll=0.0, pitch=0.0, yaw=yaw)
    fwd = unreal.MathLibrary.get_forward_vector(flat_rot)
    right = unreal.MathLibrary.get_right_vector(flat_rot)
    base = cam_loc + fwd * DISTANCE

    mesh = unreal.EditorAssetLibrary.load_asset(CUBE_PATH)
    spawned = []
    with unreal.ScopedEditorTransaction("Seat test station"):
        n = len(HEIGHTS)
        for i, h in enumerate(HEIGHTS):
            p = base + right * ((i - (n - 1) / 2.0) * SPACING)
            z = floor_z(p.x, p.y, cam_loc.z + 500.0)
            if z is None:
                unreal.log_warning(f"[SeatTest] Pod bodem {i} neni podlaha, preskoceno")
                continue
            # osa X kvadru miri ke kamere -> postava bude sedet celem ke kamere
            rot = unreal.Rotator(roll=0.0, pitch=0.0, yaw=yaw + 180.0)
            a = actor_sub.spawn_actor_from_object(mesh, unreal.Vector(p.x, p.y, z + h / 2.0), rot)
            a.set_actor_scale3d(unreal.Vector(SIZE / 100.0, SIZE / 100.0, h / 100.0))
            a.set_actor_label(f"SeatTest_{h}cm")
            a.set_folder_path("SeatTest")
            spawned.append(a)
    if spawned:
        actor_sub.set_selected_level_actors(spawned)
    unreal.log(f"[SeatTest] Vytvoreno {len(spawned)} kvadru (vybrany). Spust seat_place_selected.py")


main()
