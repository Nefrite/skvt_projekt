"""Unreal: actory s Instanced Static Mesh"""
from .config import BLOCK_BP


def _new_actor(unreal, eas):
    actor = eas.spawn_actor_from_class(unreal.Actor, unreal.Vector(0, 0, 0))
    sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    root = sds.k2_gather_subobject_data_for_instance(actor)[0]
    return actor, sds, root

def _add_ism(unreal, sds, root):
    prm = unreal.AddNewSubobjectParams(parent_handle=root, new_class=unreal.InstancedStaticMeshComponent, blueprint_context=None)
    handle, fail = sds.add_new_subobject(prm)
    comp = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle))
    if not isinstance(comp, unreal.InstancedStaticMeshComponent): raise RuntimeError("komponenta nevznikla")
    return comp

def _ism_actor(unreal, eas, name, folder, parts, material, tag):
    """Actor s InstancedStaticMeshComponent pro kazdy mesh v parts [(mesh, [Transform])].
    Komponenty pres SubobjectDataSubsystem, jinak Blueprint BLOCK_BP (pak jeden actor na mesh)."""
    actors = []
    try:
        actor, sds, root = _new_actor(unreal, eas)
        try:
            comps = [_add_ism(unreal, sds, root) for _ in parts]
        except Exception:
            eas.destroy_actor(actor); raise
        for comp, (mesh, trs) in zip(comps, parts):
            comp.set_static_mesh(mesh)
            if material: comp.set_material(0, material)
            comp.add_instances(trs, False, True)
        actors.append(actor)
    except Exception as ex:
        bp = unreal.load_asset(BLOCK_BP)
        if not bp:
            raise RuntimeError("Nejde pridat InstancedStaticMeshComponent (%s) a chybi Blueprint %s. "
                               "Vytvor ho podle README_bloky.md kap. 1." % (ex, BLOCK_BP))
        for mesh, trs in parts:
            actor = eas.spawn_actor_from_object(bp, unreal.Vector(0, 0, 0), unreal.Rotator())
            comp = actor.get_component_by_class(unreal.InstancedStaticMeshComponent)
            comp.set_static_mesh(mesh)
            if material: comp.set_material(0, material)
            comp.add_instances(trs, False, True)
            actors.append(actor)
    for i, actor in enumerate(actors):
        actor.tags = [tag, unreal.Name("RuinBlocks")]
        actor.set_folder_path(folder)
        actor.set_actor_label(name if i == 0 else "%s_%d" % (name, i + 1))
    return actors


# ------------------------------------------------------------------ spolecne pro 03 i 05: stavba, mazani, capture
def tag_value(a, prefix):
    """hodnota tagu <prefix><hodnota> actoru (napr. "cast:", "zed:", "stavba:", "id:"), jinak None"""
    return next((str(t)[len(prefix):] for t in a.tags if str(t).startswith(prefix)), None)


def destroy_tagged(eas, tag, keep=lambda a: True):
    """smaze actory s tagem tag, pro ktere plati keep(a)"""
    old = [a for a in eas.get_all_level_actors() if tag in a.tags and keep(a)]
    if old: eas.destroy_actors(old)
    return len(old)


def place_ism(unreal, eas, label, folder, stones, cube, meshes, material, tag, extra_tags=()):
    """kameny / dilce jedne skupiny -> actor(y) s Instanced Static Mesh (po meshich); vrati pocet kusu"""
    from .ue_assets import _resolve, stone_transform
    bym = {}
    for s in stones:
        m, nom = _resolve(unreal, s, cube, meshes)
        bym.setdefault(m.get_path_name(), [m, []])[1].append(stone_transform(unreal, s, m, nom))
    for a_ in _ism_actor(unreal, eas, label, folder, [tuple(v) for _, v in sorted(bym.items())], material, tag) or []:
        a_.tags = list(a_.tags) + [unreal.Name(t) for t in extra_tags]
    return len(stones)


def spawn_loose(unreal, eas, s, cube, meshes, tags, folder, material):
    """samostatny kamen (sut, oddeleny kamen): vlastni actor se jmenem Kamen_<id> a tagem id:<id>"""
    from .ue_assets import _resolve, stone_transform, ue_rotator
    m, nom = _resolve(unreal, s, cube, meshes)
    act = eas.spawn_actor_from_object(m, unreal.Vector(s.x, s.y, s.z), ue_rotator(unreal, s))
    if not act: return None
    act.set_actor_transform(stone_transform(unreal, s, m, nom), False, False)
    act.tags = [unreal.Name(t) if isinstance(t, str) else t for t in tags]
    act.set_folder_path(folder)
    act.set_actor_label("Kamen_" + s.id.replace("|", "_"))
    if material: act.static_mesh_component.set_material(0, material)
    return act


def scan_level(unreal, eas, tag):
    """capture: polohy instanci v ISM actorech s tagem (zaokrouhlene) a samostatne kameny {id: actor}"""
    present = set(); loose_now = {}
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        if tag not in tags: continue
        ids = [t[3:] for t in tags if t.startswith("id:")]
        if ids:
            loose_now[ids[0]] = a
            continue
        for comp in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
            for i in range(comp.get_instance_count()):
                res = comp.get_instance_transform(i, True)
                tr = res[-1] if isinstance(res, tuple) else res
                t = tr.translation
                present.add((round(t.x), round(t.y), round(t.z)))
    return present, loose_now


def instance_key(unreal, s, cube, meshes):
    """zaokrouhlena poloha instance kamene (pro porovnani s levelem)"""
    from .ue_assets import _resolve, stone_transform
    m, nom = _resolve(unreal, s, cube, meshes)
    t = stone_transform(unreal, s, m, nom).translation
    return (round(t.x), round(t.y), round(t.z))


def loose_pose(unreal, s, cube, meshes, actor):
    """poloha "kamene" samostatneho actoru [x, y, z, roll, pitch, yaw] (bez lokalni korekce meshe) a jestli se pohnul"""
    from .ue_assets import _resolve, _fix_unit, _unit
    m, nom = _resolve(unreal, s, cube, meshes)
    st_t = unreal.MathLibrary.compose_transforms(unreal.MathLibrary.invert_transform(_fix_unit(unreal, s, m, nom)),
                                                 _unit(unreal, actor.get_actor_transform()))
    loc, rot, _ = unreal.MathLibrary.break_transform(st_t)
    cur = [loc.x, loc.y, loc.z, -rot.roll, rot.pitch, rot.yaw]          # roll zpet do konvence modelu (viz ue_assets.ue_rotator)
    same = all(abs(p - q) < 1.0 for p, q in zip(cur[:3], [s.x, s.y, s.z])) and \
           all(abs(((p - q) + 180) % 360 - 180) < 1.0 for p, q in zip(cur[3:], [s.roll, s.pitch, s.yaw]))
    return cur, same
