"""
Nastavi body splinu vybrane reky (Water Body River) podle Zricenina_505_body_reky.csv.

Pouziti v Unreal Editoru:
  1) Edit -> Plugins -> zapnout "Python Editor Script Plugin" (restart editoru)
  2) V levelu vybrat actor WaterBodyRiver
  3) File -> Execute Python Script... -> vybrat tento soubor
  Akce jde vratit pres Ctrl+Z.

Souradnice jsou svetove (cm). Landscape je vycentrovany na 0,0, Location Z = 3200.
"""
import unreal

# Ve smeru toku (jih -> SV), body po ~20 m.
# X, Y, Z v cm. Z = hladina ~25 cm pod hranou koryta (prvni/posledni bod jsou vytazene za okraj mapy)
POINTS = [
    (3428, 13212, 437),
    (2610, 12637, 437),
    (1056, 11545, 430),
    (-818, 10864, 421),
    (-2615, 9997, 414),
    (-4313, 8952, 408),
    (-5147, 7174, 403),
    (-5609, 5229, 394),
    (-5983, 3265, 382),
    (-6956, 1548, 371),
    (-8282, 52, 366),
    (-9653, -1401, 366),
    (-10589, -3133, 366),
    (-10351, -5079, 359),
    (-8669, -6073, 347),
    (-6832, -6856, 342),
    (-4892, -7247, 332),
    (-2894, -7279, 317),
    (-899, -7222, 317),
    (1061, -7480, 317),
    (2918, -8219, 309),
    (4780, -8939, 289),
    (6678, -9516, 275),
    (8668, -9683, 272),
    (10632, -10050, 272),
    (12608, -10536, 265),
    (13579, -10775, 265),
]

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_selected_level_actors()
rivers = [a for a in actors if a.get_component_by_class(unreal.SplineComponent)]
if not rivers:
    unreal.log_error("Vyber v levelu actor WaterBodyRiver a spust skript znovu.")
else:
    river = rivers[0]
    spline = river.get_component_by_class(unreal.SplineComponent)
    with unreal.ScopedEditorTransaction("Import river spline points"):
        river.modify()
        spline.modify()
        spline.clear_spline_points(False)
        for x, y, z in POINTS:
            spline.add_spline_point(unreal.Vector(x, y, z), unreal.SplineCoordinateSpace.WORLD, False)
        for i in range(spline.get_number_of_spline_points()):
            spline.set_spline_point_type(i, unreal.SplinePointType.CURVE, False)
        spline.update_spline()
    unreal.log("Reka '%s': nastaveno %d bodu splinu." % (river.get_actor_label(), len(POINTS)))
    unreal.log("Pokud se voda hned neprekresli, posun reku o kousek a zpet (nebo Ctrl+Z / Ctrl+Y).")
