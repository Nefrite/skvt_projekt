"""UE_Prikop_Landscape.py - pomocny skript pro Unreal Editor 5.8 (01_terrain):
zapise vyskopis sijoveho prikopu, valovych kridel, pristupoveho uvozu a unikove rampy (Zricenina_heightmap_505_50cm.png)
do Landscape actoru v otevrene mape (/Game/Skvt/LapikusPrototypeMap), pripadne zkontroluje meritko a vysky line-tracem.

Jak pouzit v UE:
  Varianta A (doporucena v UE 5.8 se zapnutymi Edit Layers):
    1. Shift+2 (Landscape Mode) -> Manage -> Import / Export (nebo pravym tlacitkem na zakladni Edit Layer -> Import from File)
    2. Heightmap File = PrototypeDesigns/Lapikus/01_terrain/Zricenina_heightmap_505_50cm.png -> Import
       (pokud mas v samostatne Edit Layer rucni zasyp stareho prikopu pod branou, tuto rucni vrstvu vypni/smaz -
        Zricenina_heightmap_505_50cm.png uz vysky pod hradem z terrain_from_level.json obsahuje)
    3. Spust tento skript (Tools -> Execute Python Script -> 01_terrain/UE_Prikop_Landscape.py) s MODE = "verify"
       pro kontrolu vysek v mape a ulozeni terrain_from_level.json.

  Varianta B (primy pokus pres Python API v transakci Ctrl+Z):
    Nastav MODE = "import_and_verify" a spust v UE. Skript naimportuje PNG do docasne textury, vykresli do RenderTarget2D
    a zavola landscape_import_heightmap_from_render_target, pokud to Landscape v UE 5.8 bez kolize Edit Layers dovoli.

entities: [Brana, Lapikus_Region]
docs: [navrh_brana_prikop, stav_brana, 01_terrain]
build_step: 01_terrain
domains: [structures, environment]"""
import math, os, sys

MODE = "verify"               # "verify" = zmerit klicove body prikopu a ulozit terrain_from_level.json;
                              # "import_and_verify" = nejdriv zkusit zapsat Zricenina_heightmap_505_50cm.png pres RenderTarget

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
PNG_PATH = os.path.join(HERE, "Zricenina_heightmap_505_50cm.png")

GT_NW = (1930.0, -3107.0)
GT_NE = (2633.0, -3264.0)
_L = math.hypot(GT_NE[0] - GT_NW[0], GT_NE[1] - GT_NW[1])
UX, UY = (GT_NE[0] - GT_NW[0]) / _L, (GT_NE[1] - GT_NW[1]) / _L
DX, DY = -UY, UX


def ud_to_xy(u, d):
    return GT_NW[0] + (UX * u + DX * d) * 100.0, GT_NW[1] + (UY * u + DY * d) * 100.0


def _trace_landscape(unreal, world, ignore, x, y):
    res = unreal.SystemLibrary.line_trace_single(
        world, unreal.Vector(x, y, 200000.0), unreal.Vector(x, y, -200000.0),
        unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ignore, unreal.DrawDebugTrace.NONE, True)
    hit = res[-1] if isinstance(res, tuple) else res
    if hit is None:
        return None
    try:
        vals = list(unreal.GameplayStatics.break_hit_result(hit))
    except Exception:
        vals = list(hit.to_tuple())
    if not vals or not vals[0]:
        return None
    loc = next((v for v in vals if isinstance(v, unreal.Vector)), None)
    return round(loc.z, 1) if loc is not None else None


def verify_and_sample():
    import unreal
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    landscapes = [a for a in eas.get_all_level_actors() if isinstance(a, unreal.LandscapeProxy)]
    if not landscapes:
        unreal.log_error("Prikop: v otevrene mape neni zadny LandscapeProxy actor.")
        return
    ls = landscapes[0]
    loc, sc = ls.get_actor_location(), ls.get_actor_scale3d()
    unreal.log("Prikop: Landscape '%s' Location=(%.1f, %.1f, %.1f), Scale=(%.2f, %.2f, %.2f)" % (
        ls.get_actor_label(), loc.x, loc.y, loc.z, sc.x, sc.y, sc.z))

    ignore = [a for a in eas.get_all_level_actors() if not isinstance(a, unreal.LandscapeProxy)]
    checks = [
        ("Prujezd Brana_V (u=7.2, d=3.1)", 7.20, 3.10, 3035.0, 3060.0),
        ("Dno prikopu u pilire (u=12.2, d=3.1)", 12.20, 3.10, 2690.0, 2710.0),
        ("Predmosti / zataras (u=17.2, d=3.1)", 17.20, 3.10, 3030.0, 3075.0),
        ("Rostly teren vychodne od prikopu J (u=19.0, d=10.0)", 19.00, 10.00, 3230.0, 3330.0),
        ("Unikova rampa stred (u=14.35, d=-3.25)", 14.35, -3.25, 2825.0, 2865.0),
    ]
    for label, u, d, zlo, zhi in checks:
        x, y = ud_to_xy(u, d)
        z = _trace_landscape(unreal, world, ignore, x, y)
        ok = (z is not None and zlo <= z <= zhi)
        unreal.log("  %-40s X=%6.0f Y=%6.0f -> Z=%s cm (cil %.0f..%.0f) [%s]" % (
            label, x, y, "%.1f" % z if z is not None else "None", zlo, zhi, "OK" if ok else "ZKONTROLUJ"))

    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    import json
    from zrlib import level as zr_level
    lay_path = os.path.join(ROOT, "03_ruin", "blocks", "ruin_layout.json")
    cache_path = os.path.join(ROOT, "03_ruin", "blocks", "terrain_from_level.json")
    if os.path.exists(lay_path):
        zr_level.sample_level_terrain(unreal, json.load(open(lay_path, encoding="utf-8")), cache_path)


def try_import_png():
    import unreal
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    landscapes = [a for a in eas.get_all_level_actors() if isinstance(a, unreal.LandscapeProxy)]
    if not landscapes:
        unreal.log_error("Prikop: Landscape nenalezen.")
        return
    ls = landscapes[0]
    if not hasattr(ls, "landscape_import_heightmap_from_render_target"):
        unreal.log_warning("Prikop: UE verze nepodporuje landscape_import_heightmap_from_render_target v Pythonu - pouzij Landscape Mode -> Manage -> Import from File (%s)." % PNG_PATH)
        return
    tex = unreal.RenderingLibrary.import_file_as_texture_2d(world, PNG_PATH)
    if not tex:
        unreal.log_warning("Prikop: import_file_as_texture_2d pro 16bit PNG vratil None - pouzij Landscape Mode -> Manage -> Import from File (%s)." % PNG_PATH)
        return
    rt = unreal.RenderingLibrary.create_render_target2d(world, 505, 505, unreal.TextureRenderTargetFormat.RTF_RGBA16F)
    with unreal.ScopedEditorTransaction("Prikop a valy pred branou"):
        ok = ls.landscape_import_heightmap_from_render_target(rt, True)
        unreal.log("Prikop: landscape_import_heightmap_from_render_target -> %s (pokud vysky nesedi kvuli Edit Layers, dej Ctrl+Z a reimportuj v Landscape Mode -> Manage -> Import)." % ok)


if __name__ == "__main__" or "unreal" in sys.modules:
    if MODE == "import_and_verify":
        try_import_png()
    verify_and_sample()
