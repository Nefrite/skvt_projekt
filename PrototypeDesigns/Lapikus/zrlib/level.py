"""Unreal: cteni levelu (bouraci objemy, teren z landscapu)"""
import json, os


def gather_volumes(unreal, eas):
    """TriggerBoxy (nebo jine actory) s tagy Ruin_Cut / Ruin_Opening:<typ> / Ruin_Keep / Ruin_Explode."""
    vols = []
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        if not any(t.startswith(("Ruin_Cut", "Ruin_Opening", "Ruin_Keep", "Ruin_Explode")) for t in tags): continue
        origin, ext = a.get_actor_bounds(False)
        vols.append(dict(tags=tags, name=a.get_actor_label(),
                         box=[origin.x - ext.x, origin.y - ext.y, origin.z - ext.z, origin.x + ext.x, origin.y + ext.y, origin.z + ext.z]))
    return vols

def sample_level_terrain(unreal, layout, cache_path):
    """Zmeri vysky landscapu v mrizce layout["terrain"] (line trace shora, ignoruje vse krome landscapu).
    Vysledek ulozi do terrain_from_level.json a vrati upraveny layout."""
    t = layout["terrain"]
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    x0, y0, st, nx, ny = t["x0"], t["y0"], t["step"], t["nx"], t["ny"]
    x1, y1 = x0 + (nx - 1) * st, y0 + (ny - 1) * st
    ignore = []
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.LandscapeProxy): continue
        try:
            o, e = a.get_actor_bounds(False)
            if o.x + e.x < x0 or o.x - e.x > x1 or o.y + e.y < y0 or o.y - e.y > y1: continue
        except Exception:
            pass
        ignore.append(a)
    Z = [row[:] for row in t["z"]]; hits = 0
    with unreal.ScopedSlowTask(ny, "Merim teren z landscapu...") as task:
        task.make_dialog(True)
        for j in range(ny):
            task.enter_progress_frame(1)
            for i in range(nx):
                x, y = x0 + i * st, y0 + j * st
                res = unreal.SystemLibrary.line_trace_single(world, unreal.Vector(x, y, 200000), unreal.Vector(x, y, -200000),
                                                            unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ignore,
                                                            unreal.DrawDebugTrace.NONE, True)
                hit = res[-1] if isinstance(res, tuple) else res
                if hit is None: continue
                try: vals = list(unreal.GameplayStatics.break_hit_result(hit))
                except Exception: vals = list(hit.to_tuple())
                if not vals or not vals[0]: continue
                act = next((v for v in vals if isinstance(v, unreal.Actor)), None)
                loc = next((v for v in vals if isinstance(v, unreal.Vector)), None)
                if loc is None or (act is not None and not isinstance(act, unreal.LandscapeProxy)): continue
                Z[j][i] = round(loc.z); hits += 1
    layout = dict(layout, terrain=dict(t, z=Z))
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(dict(t, z=Z, hits=hits), f)
    unreal.log("Ruin: teren z levelu - %d / %d bodu zasahlo landscape (ulozeno terrain_from_level.json)" % (hits, nx * ny))
    if hits < nx * ny * 0.5:
        unreal.log_warning("Ruin: landscape zasazen jen v %d bodech - zbytek z ruin_layout.json. Ma landscape kolizi?" % hits)
    return layout

def cached_level_terrain(layout, cache_path, enabled=True):
    """posledni zmereny teren z levelu (terrain_from_level.json), kdyz sedi mrizka; jinak layout beze zmeny"""
    p = cache_path
    if enabled and os.path.exists(p):
        t = json.load(open(p, encoding="utf-8")); t.pop("hits", None)
        if (t["x0"], t["y0"], t["nx"], t["ny"]) == (layout["terrain"]["x0"], layout["terrain"]["y0"], layout["terrain"]["nx"], layout["terrain"]["ny"]):
            return dict(layout, terrain=t)
    return layout
