"""export_level_layout.py - prenese rucni upravy pudorysu z levelu zpet do dat (Unreal Editor 5.8)

Co zapise do layout_from_level.json (vedle skriptu):
  "moved":  zricenina-actory (tag Zricenina_Ruin + RuinBlocks), ktere jsi v levelu posunul / otocil
            -> poloha, rotace a meritko actoru (actory vznikly v pocatku 0,0,0, takze jde primo o posun cele zdi)
  "points": body novych zdi = Target Pointy pojmenovane  RuinPt_<JmenoZdi>_<cislo>
            napr. RuinPt_Hradba_Brana_01, RuinPt_Hradba_Brana_02, ...  (poradi podle cisla)
            -> z kazde skupiny vznikne jedna nova zed (lomena cara)

Pouziti: Tools -> Execute Python Script -> export_level_layout.py
Pak posli layout_from_level.json (nebo ho nech ve slozce) - podle nej se upravi ruin_layout_draft.json / gen_layout.py.
Nic v levelu nemeni.
"""
import json, os
import unreal

RUIN_TAG = "Zricenina_Ruin"
POINT_PREFIX = "RuinPt_"


def _script_dir():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return unreal.Paths.project_dir()


def main():
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    out = {"moved": {}, "points": {}}
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        label = a.get_actor_label()
        if RUIN_TAG in tags and "RuinBlocks" in tags:
            loc = a.get_actor_location(); rot = a.get_actor_rotation(); sc = a.get_actor_scale3d()
            if abs(loc.x) + abs(loc.y) + abs(loc.z) > 1 or abs(rot.yaw) + abs(rot.pitch) + abs(rot.roll) > 0.05 \
               or abs(sc.x - 1) + abs(sc.y - 1) + abs(sc.z - 1) > 0.001:
                out["moved"][label] = dict(loc=[round(loc.x, 1), round(loc.y, 1), round(loc.z, 1)],
                                           rot=[round(rot.roll, 3), round(rot.pitch, 3), round(rot.yaw, 3)],
                                           scale=[round(sc.x, 4), round(sc.y, 4), round(sc.z, 4)],
                                           folder=str(a.get_folder_path()))
        if label.startswith(POINT_PREFIX):
            rest = label[len(POINT_PREFIX):]
            name, _, num = rest.rpartition("_")
            try:
                idx = int(num)
            except ValueError:
                name, idx = rest, 0
            loc = a.get_actor_location()
            out["points"].setdefault(name or "Nova_zed", []).append([idx, round(loc.x, 1), round(loc.y, 1), round(loc.z, 1)])
    for k in out["points"]:
        out["points"][k].sort()
    path = os.path.join(_script_dir(), "layout_from_level.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    unreal.log("layout_from_level.json: posunutych actoru %d, novych zdi z bodu %d (%s) -> %s" % (
        len(out["moved"]), len(out["points"]), ", ".join("%s:%d" % (k, len(v)) for k, v in out["points"].items()), path))


main()
