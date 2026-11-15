"""UE_Osy_OBJ.py - zjisti, jak Unreal prevadi osy pri importu OBJ (podklad pro zapis OBJ v tools/meshes/mesh_common.py).
Unreal: Tools -> Execute Python Script -> tools/checks/UE_Osy_OBJ.py

Zapise do docasne slozky nesymetricky ctyrsten (OBJ osa X 100 cm, Y 50 cm, Z 25 cm, vse v kladnem smeru),
naimportuje ho stejne jako build (AssetImportTask), z bounding boxu assetu vycte, kam se ktera osa OBJ dostala,
vypise vysledek do Output Logu (radek "OSY OBJ -> UE") a docasny asset smaze. Level ani jine assety nemeni.
"""
import os, tempfile

DST = "/Game/Skvt/Lapikus/_OsyTest"
NAME = "SM_OsyTest"
SIZES = (100.0, 50.0, 25.0)          # delka osy X, Y, Z v OBJ (ruzne, aby se daly poznat)


def run():
    import unreal
    eal = unreal.EditorAssetLibrary
    d = tempfile.mkdtemp(prefix="skvt_osy_")
    f = os.path.join(d, NAME + ".obj")
    with open(f, "w") as o:
        o.write("# test os importu OBJ\no %s\n" % NAME)
        for v in ((0, 0, 0), (SIZES[0], 0, 0), (0, SIZES[1], 0), (0, 0, SIZES[2])):
            o.write("v %.1f %.1f %.1f\n" % v)
        o.write("f 1 3 2\nf 1 2 4\nf 1 4 3\nf 2 3 4\n")
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", f); t.set_editor_property("destination_path", DST)
    t.set_editor_property("destination_name", NAME)
    t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True); t.set_editor_property("save", False)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
    hits = [a for a in eal.list_assets(DST, recursive=True)] if eal.does_directory_exist(DST) else []
    sm = next((unreal.load_asset(a) for a in hits if isinstance(unreal.load_asset(a), unreal.StaticMesh)), None)
    if not sm:
        unreal.log_error("OSY OBJ -> UE: import se nepovedl (%s)" % f); return
    bb = sm.get_bounding_box(); mn = (bb.min.x, bb.min.y, bb.min.z); mx = (bb.max.x, bb.max.y, bb.max.z)
    names = "XYZ"; res = []
    for i in range(3):                                  # osa UE i: ktera osa OBJ a s jakym znamenkem
        ext = mx[i] - mn[i]
        j = min(range(3), key=lambda k: abs(SIZES[k] - ext))
        sign = "+" if abs(mx[i]) > abs(mn[i]) else "-"
        res.append("UE %s = %sOBJ %s" % (names[i], sign, names[j]))
    unreal.log_warning("OSY OBJ -> UE: %s   (bbox min %s max %s)" % (", ".join(res),
                       tuple(round(v, 1) for v in mn), tuple(round(v, 1) for v in mx)))
    eal.delete_directory(DST)


run()
