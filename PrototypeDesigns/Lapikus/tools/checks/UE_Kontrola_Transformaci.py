"""UE_Kontrola_Transformaci.py - najde v levelu objekty s neplatnou transformaci nebo meshem s vadnymi bounds
(pricina chyb "InverseFast ... non-invertible matrix" a "precision loss" v Output Logu).
Unreal: Tools -> Execute Python Script -> tools/checks/UE_Kontrola_Transformaci.py

Projde vsechny actory, jejich StaticMesh a Instanced Static Mesh komponenty a kazdou instanci: NaN, nulove nebo obri
meritko, obri poloha, nenormovane natoceni; u meshe bounding box, bounds a jednoducha kolize (NaN, nulovy box). Vysledek vypise do Output Logu (radky "KONTROLA:").
Nic nemeni.
"""
import math

MAX_POS = 1.0e7          # cm
MIN_SCALE = 1.0e-4
MAX_SCALE = 1.0e4


def _fin(*v):
    return all(isinstance(q, (int, float)) and math.isfinite(q) for q in v)


def _bad_transform(t):
    l, r, s = t.translation, t.rotation, t.scale3d
    if not _fin(l.x, l.y, l.z, s.x, s.y, s.z):
        return "NaN v poloze / meritku"
    try:
        q = (r.x, r.y, r.z, r.w)
    except Exception:
        q = (0.0, 0.0, 0.0, 1.0)
    if not _fin(*q):
        return "NaN v natoceni"
    if abs(sum(v * v for v in q) - 1.0) > 1e-3:
        return "nenormovane natoceni (quat %s)" % (tuple(round(v, 4) for v in q),)
    if max(abs(l.x), abs(l.y), abs(l.z)) > MAX_POS:
        return "obri poloha (%.0f, %.0f, %.0f)" % (l.x, l.y, l.z)
    a = (abs(s.x), abs(s.y), abs(s.z))
    if min(a) < MIN_SCALE:
        return "nulove meritko (%.4g, %.4g, %.4g)" % (s.x, s.y, s.z)
    if max(a) > MAX_SCALE:
        return "obri meritko (%.4g, %.4g, %.4g)" % (s.x, s.y, s.z)
    return None


def _bad_mesh(m):
    out = []
    try:
        bb = m.get_bounding_box()
        if not _fin(bb.min.x, bb.min.y, bb.min.z, bb.max.x, bb.max.y, bb.max.z):
            out.append("bounding box NaN")
    except Exception as ex:
        out.append("bounding box: %s" % ex)
    try:                                     # jednoducha kolize (box): rozmer a stred
        bs = m.get_editor_property("body_setup")
        boxes = list(bs.get_editor_property("agg_geom").get_editor_property("box_elems")) if bs else []
        for k, b in enumerate(boxes):
            x, y, z = b.get_editor_property("x"), b.get_editor_property("y"), b.get_editor_property("z")
            ce = b.get_editor_property("center")
            if not _fin(x, y, z, ce.x, ce.y, ce.z) or min(x, y, z) < 1e-3:
                out.append("kolizni box %d vadny (%.4g x %.4g x %.4g, stred %.4g %.4g %.4g)" % (k, x, y, z, ce.x, ce.y, ce.z))
    except Exception as ex:
        out.append("kolize: %s" % ex)
    try:
        b = m.get_bounds()
        if not _fin(b.origin.x, b.origin.y, b.origin.z, b.box_extent.x, b.box_extent.y, b.box_extent.z, b.sphere_radius):
            out.append("bounds NaN")
    except Exception:
        pass
    return ", ".join(out) or None


def run():
    import unreal
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    bad = {}                     # (actor, mesh) -> [pocet, priklad]
    meshes = {}
    n_inst = 0; n_act = 0
    for a in eas.get_all_level_actors():
        n_act += 1
        label = a.get_actor_label()
        why = _bad_transform(a.get_actor_transform())
        if why:
            bad.setdefault((label, "(actor)"), [0, why])[0] += 1
        for c in a.get_components_by_class(unreal.StaticMeshComponent):
            m = c.get_editor_property("static_mesh")
            mn = m.get_name() if m else "(bez meshe)"
            if m and mn not in meshes:
                meshes[mn] = _bad_mesh(m)
            if isinstance(c, unreal.InstancedStaticMeshComponent):
                for i in range(c.get_instance_count()):
                    n_inst += 1
                    t = c.get_instance_transform(i, True)
                    why = _bad_transform(t)
                    if why:
                        e = bad.setdefault((label, mn), [0, "instance %d: %s" % (i, why)]); e[0] += 1
            else:
                why = _bad_transform(c.get_world_transform())
                if why:
                    e = bad.setdefault((label, mn), [0, why]); e[0] += 1
    unreal.log_warning("KONTROLA: actoru %d, instanci %d, meshu %d" % (n_act, n_inst, len(meshes)))
    for mn, why in sorted(meshes.items()):
        if why:
            unreal.log_warning("KONTROLA: mesh %s: %s" % (mn, why))
    for (label, mn), (cnt, ex) in sorted(bad.items(), key=lambda kv: -kv[1][0]):
        unreal.log_warning("KONTROLA: %s / %s: %d spatne (napr. %s)" % (label, mn, cnt, ex))
    if not bad and not any(meshes.values()):
        unreal.log_warning("KONTROLA: zadna neplatna transformace ani vadne bounds nenalezeny")


run()
