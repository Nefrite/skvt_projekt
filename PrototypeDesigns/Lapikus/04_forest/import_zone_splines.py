"""
Nastavi body splinu zon lesa (PCG) podle tagu vybraneho actoru.

Actor = Blueprint BP_PCGSpline (Actor + Spline component), s jednim z tagu:
  PCG_NoForest  -> obrys hradu (uzavreny spline)
  PCG_Rocky     -> skalnate podlozi, kosodrevina (uzavreny spline)
  PCG_Path      -> stara cesta / stezka ke hradu (otevreny spline, od hradu na vychod)

Pouziti: vybrat jeden nebo vic takovych actoru -> Tools -> Execute Python Script -> tento soubor.
Souradnice jsou svetove (cm), Z = vyska terenu. Jde vratit pres Ctrl+Z.
"""
import unreal

ZONES = {
    "PCG_NoForest": (True, [
    (-3600, 1225, 2193),
    (-4700, 975, 1645),
    (-5275, 500, 1166),
    (-5425, 150, 1159),
    (-5725, -1150, 1418),
    (-5425, -1900, 1682),
    (-5000, -2325, 1838),
    (-4550, -2425, 2048),
    (-3750, -2925, 2274),
    (-3000, -2825, 2635),
    (-2050, -3125, 2586),
    (-1550, -3125, 2658),
    (-500, -3525, 2657),
    (550, -3525, 2748),
    (2000, -3875, 2755),
    (2700, -3825, 2860),
    (3075, -3600, 3011),
    (3375, -2250, 3283),
    (3775, -1500, 3296),
    (3775, -250, 2684),
    (3600, -75, 2578),
    (2600, 325, 2139),
    (1550, 425, 2143),
    (-450, 975, 2034),
    ]),
    "PCG_Rocky": (True, [
    (8400, 8825, 3469),
    (7700, 8475, 3313),
    (7175, 8000, 3114),
    (6475, 6350, 2769),
    (5975, 5950, 2534),
    (5925, 5650, 2493),
    (6700, 4825, 2839),
    (8850, 3975, 3576),
    (9325, 4450, 3639),
    (9875, 5450, 3810),
    (9875, 6450, 3896),
    (8925, 8400, 3591),
    ]),
    "PCG_Path": (False, [
    (3250, -2231, 3262),
    (4248, -2280, 3370),
    (5235, -2422, 3442),
    (6226, -2529, 3480),
    (7210, -2693, 3516),
    (8193, -2862, 3563),
    (9146, -3152, 3621),
    (10072, -3521, 3676),
    (11013, -3854, 3803),
    (12008, -3777, 3949),
    (12600, -3761, 4028),
    ]),
}

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_selected_level_actors()
done = 0
with unreal.ScopedEditorTransaction("Import forest zone splines"):
    for a in actors:
        spline = a.get_component_by_class(unreal.SplineComponent)
        tags = [str(t) for t in a.tags]
        key = next((k for k in ZONES if k in tags), None)
        if not spline or not key:
            unreal.log_warning("%s: chybi Spline component nebo tag (%s)" % (a.get_actor_label(), ", ".join(ZONES)))
            continue
        closed, pts = ZONES[key]
        a.modify(); spline.modify()
        spline.clear_spline_points(False)
        for x, y, z in pts:
            spline.add_spline_point(unreal.Vector(x, y, z), unreal.SplineCoordinateSpace.WORLD, False)
        for i in range(spline.get_number_of_spline_points()):
            spline.set_spline_point_type(i, unreal.SplinePointType.CURVE if key == "PCG_Path" else unreal.SplinePointType.LINEAR, False)
        spline.set_closed_loop(closed, False)
        spline.update_spline()
        done += 1
        unreal.log("%s (%s): %d bodu" % (a.get_actor_label(), key, len(pts)))
if not done:
    unreal.log_error("Vyber actor(y) se Spline component a tagem PCG_NoForest / PCG_Rocky / PCG_Path.")
