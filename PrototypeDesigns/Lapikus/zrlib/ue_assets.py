"""Unreal: materialy (M_RuinStone, MI_*), import meshi kamenu a dreva, transformace instanci, fyzika"""
import os
from .config import ASHLAR_MESH, DRESSED_FRAMES, MAT_CORE, MAT_CROWN, MAT_DIR, MAT_FACE, MAT_FRAME, MAT_LOOK, MAT_RESET, MAT_TOP, MAT_VERSION, MAT_WOOD, MAT_WOOD_MI, MESH_DIRS, MESH_ROOT, MESH_SRC, STONE_DIR, STONE_MESH_VERSION, STONE_NOMINAL, STONE_OVERSIZE, STONE_PHYSICS, STONE_RATIOS, STONE_VARIANTS, TEXTURES, USE_STONE_MESHES, WOOD_MESHES, WOOD_MI, WOOD_NOMINAL
from .config import CLOTH_MACRO, CLOTH_MI, CLOTH_VERSION, MESH_AXES, LIB_MESHES, ROUND_MESHES, SLOT_MI, TEX_DIR, TEX_FILES, TEX_SRC, TEX_VERSION
from .stones import stone_mass_kg


def _asset_path(folder, name): return "%s/%s.%s" % (folder, name, name)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # koren (vedle zrlib: meshes/, textures/)
SLOT_MATS = {}          # materialy slotu {"bark": MI, "endgrain": MI, "rope": MI, ..., "canvas": MI}, plni ensure_materials

def ensure_textures(unreal, force=False):
    """vlastni textury (textures/*.png z tools/textures/gen_textures.py) -> TEX_DIR; chybejici nebo starsi nez TEX_VERSION
    naimportuje (force=True vsechny), normalove mapy nastavi jako normal (bez sRGB)"""
    eal = unreal.EditorAssetLibrary; src = os.path.join(ROOT, TEX_SRC); todo = []
    for name, kind in TEX_FILES.items():
        pth = _asset_path(TEX_DIR, name)
        if not force and eal.does_asset_exist(pth) and _ver(eal, unreal.load_asset(pth), "RuinTexVersion") >= TEX_VERSION: continue
        f = os.path.join(src, name + ".png")
        if not os.path.exists(f): continue
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", f); t.set_editor_property("destination_path", TEX_DIR)
        t.set_editor_property("destination_name", name)
        t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True); t.set_editor_property("save", True)
        todo.append((t, name, kind))
    if not todo: return
    unreal.log("Ruin: importuji %d textur z %s" % (len(todo), src))
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t for t, _, _ in todo])
    for _, name, kind in todo:
        tex = unreal.load_asset(_asset_path(TEX_DIR, name))
        if not tex: continue
        if kind == "normal":
            try:
                tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
                tex.set_editor_property("srgb", False)
            except Exception as ex: unreal.log_warning("Ruin: normalova mapa %s: %s (nastav rucne Compression = Normalmap)" % (name, ex))
        eal.set_metadata_tag(tex, "RuinTexVersion", str(TEX_VERSION)); eal.save_loaded_asset(tex)

def ensure_materials(unreal):
    """Vrati {"face": mat, "core": mat, "frame": mat}. Chybejici M_RuinStone / MI_Ruin* vytvori (jen poprve,
    pak je muzes upravovat v editoru - skript je neprepise)."""
    eal = unreal.EditorAssetLibrary
    mats = {}
    user = {"face": MAT_FACE, "core": MAT_CORE, "frame": MAT_FRAME, "crown": MAT_CROWN}
    if all(user.values()):
        return {c: unreal.load_asset(p) for c, p in user.items()}
    ensure_textures(unreal)
    def pick(cat):
        for d, n in TEXTURES[cat]:
            if eal.does_asset_exist(d): return unreal.load_asset(d), (unreal.load_asset(n) if n and eal.does_asset_exist(n) else None)
        return None, None
    at = unreal.AssetToolsHelpers.get_asset_tools(); mel = unreal.MaterialEditingLibrary
    mpath = _asset_path(MAT_DIR, "M_RuinStone")
    if eal.does_asset_exist(mpath):
        master = unreal.load_asset(mpath)
    else:
        d0, n0 = pick("face")
        if not d0:
            unreal.log_warning("Ruin: nenalezeny textury pro material (StarterContent?) - nastav MAT_FACE/MAT_CORE/MAT_FRAME.")
            return {c: (unreal.load_asset(p) if p else None) for c, p in user.items()}
        master = at.create_asset("M_RuinStone", MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
        _build_master(unreal, master, d0, n0)
        unreal.log("Ruin: vytvoren material %s" % mpath)
    if _ver(eal, master, "RuinMatVersion") < MAT_VERSION:
        # starsi graf (bez zvetrani shora) -> prestavet na miste; instance (MI_*) zustanou a jen se doplni parametry
        d0, n0 = pick("face")
        mel.delete_all_material_expressions(master)
        _build_master(unreal, master, d0, n0)
        unreal.log("Ruin: material %s prestaven na verzi %d (zvetrani shora)" % (mpath, MAT_VERSION))
    for cat, mi_name in (("face", "MI_RuinFace"), ("core", "MI_RuinCore"), ("frame", "MI_RuinFrame"), ("crown", "MI_RuinCrown")):
        if user[cat]:
            mats[cat] = unreal.load_asset(user[cat]); continue
        ip = _asset_path(MAT_DIR, mi_name)
        if eal.does_asset_exist(ip):
            mi = unreal.load_asset(ip)
            if _ver(eal, mi, "RuinMatVersion") < MAT_VERSION:       # doplnit nove parametry, rucni upravy jinak nechat
                reset = _ver(eal, mi, "RuinMatVersion") < MAT_RESET.get(cat, 0)
                if reset:
                    d, n = pick(cat)
                    if d: mel.set_material_instance_texture_parameter_value(mi, "BaseColor", d)
                    if n:
                        try: mel.set_material_instance_texture_parameter_value(mi, "Normal", n)
                        except Exception: pass
                _set_top(unreal, mel, mi, cat, look=reset)
                eal.set_metadata_tag(mi, "RuinMatVersion", str(MAT_VERSION)); eal.save_loaded_asset(mi)
            mats[cat] = mi; continue
        mi = at.create_asset(mi_name, MAT_DIR, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
        mel.set_material_instance_parent(mi, master)
        d, n = pick(cat)
        if d: mel.set_material_instance_texture_parameter_value(mi, "BaseColor", d)
        if n:
            try: mel.set_material_instance_texture_parameter_value(mi, "Normal", n)
            except Exception: pass
        lk = MAT_LOOK[cat]
        for pn in ("TintA", "TintB"):
            c = lk[pn]; mel.set_material_instance_vector_parameter_value(mi, pn, unreal.LinearColor(c[0], c[1], c[2], 1))
        for pn in ("Tiling", "Roughness"):
            mel.set_material_instance_scalar_parameter_value(mi, pn, lk[pn])
        _set_top(unreal, mel, mi, cat)
        eal.set_metadata_tag(mi, "RuinMatVersion", str(MAT_VERSION))
        eal.save_loaded_asset(mi)
        mats[cat] = mi
    for wc, wn in WOOD_MI.items():
        mats[wc] = _wood_mi(unreal, master, pick, wc, wn)
    for wc in WOOD_MI:                                   # chybi-li textury, aspon stejne drevo vsude
        mats[wc] = mats[wc] or mats.get("wood")
    for sc, sn in SLOT_MI.items():                       # sloty: kura, cela, lano, prouti, mazanina, vypln spar
        mats[sc] = _wood_mi(unreal, master, pick, sc, sn) or mats.get("wood")
        SLOT_MATS[sc] = mats[sc]
    cloth = _cloth_master(unreal, pick)                  # platno: oboustranny material s posunem ve vetru
    for sc, sn in CLOTH_MI.items():
        mats[sc] = (_wood_mi(unreal, cloth, pick, sc, sn) if cloth else None) or mats.get("wood")
        SLOT_MATS[sc] = mats[sc]
    return mats

def _cloth_master(unreal, pick):
    """M_RuinCloth: stejny graf jako M_RuinStone (textura, tint, zvetrani shora), navic oboustranny a posun ve vetru
    (WindAmount cm, WindSpeed, WindScale; WindAmount 0 = staticke). Vytvori se jednou, prestavi pri vyssi CLOTH_VERSION."""
    eal = unreal.EditorAssetLibrary
    d0, n0 = pick("canvas")
    if not d0: return None
    path = _asset_path(MAT_DIR, "M_RuinCloth")
    if eal.does_asset_exist(path):
        m = unreal.load_asset(path)
        if _ver(eal, m, "RuinClothVersion") >= CLOTH_VERSION: return m
        unreal.MaterialEditingLibrary.delete_all_material_expressions(m)
    else:
        m = unreal.AssetToolsHelpers.get_asset_tools().create_asset("M_RuinCloth", MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    try: m.set_editor_property("two_sided", True)
    except Exception as ex: unreal.log_warning("Ruin: M_RuinCloth two_sided: %s (zapni rucne Two Sided)" % ex)
    mac = unreal.load_asset(CLOTH_MACRO) if eal.does_asset_exist(CLOTH_MACRO) else None
    _build_master(unreal, m, d0, n0, wind=True, macro=mac)
    eal.set_metadata_tag(m, "RuinClothVersion", str(CLOTH_VERSION)); eal.save_loaded_asset(m)
    unreal.log("Ruin: vytvoren material %s (oboustranny, vitr WindAmount)" % path)
    return m

def _wood_mi(unreal, master, pick, cat="wood", name="MI_RuinWood"):
    """MI_RuinWood(_Tar/_Oil): drevo na M_RuinStone (textura dreva, tint podle upravy, matne). Bez textur dreva -> MAT_WOOD."""
    eal = unreal.EditorAssetLibrary; mel = unreal.MaterialEditingLibrary
    if MAT_WOOD_MI and cat == "wood": return unreal.load_asset(MAT_WOOD_MI)
    ip = _asset_path(MAT_DIR, name)
    if eal.does_asset_exist(ip):
        mi = unreal.load_asset(ip)
        if _ver(eal, mi, "RuinMatVersion") < MAT_RESET.get(cat, 0):        # novejsi vychozi vzhled -> prepsat tint a vybledani
            _set_top(unreal, mel, mi, cat, look=True)
            eal.set_metadata_tag(mi, "RuinMatVersion", str(MAT_VERSION)); eal.save_loaded_asset(mi)
        return mi
    d, n = pick(cat)
    if not d or master is None:
        return next((unreal.load_asset(p) for p in MAT_WOOD if eal.does_asset_exist(p.split(".")[0])), None)
    mi = unreal.AssetToolsHelpers.get_asset_tools().create_asset(name, MAT_DIR, unreal.MaterialInstanceConstant,
                                                                unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(mi, master)
    mel.set_material_instance_texture_parameter_value(mi, "BaseColor", d)
    if n:
        try: mel.set_material_instance_texture_parameter_value(mi, "Normal", n)
        except Exception: pass
    _set_top(unreal, mel, mi, cat, look=True)
    eal.set_metadata_tag(mi, "RuinMatVersion", str(MAT_VERSION)); eal.save_loaded_asset(mi)
    unreal.log("Ruin: vytvoren material dreva %s" % ip)
    return mi

def _ver(eal, asset, tag):
    try: return int(eal.get_metadata_tag(asset, tag) or 0)
    except Exception: return 0

def _set_top(unreal, mel, mi, cat, look=False):
    """parametry zvetrani shora (MAT_TOP); look=True prepise i tint / drsnost z MAT_LOOK"""
    lk = MAT_TOP[cat]
    c = lk["TopTint"]; mel.set_material_instance_vector_parameter_value(mi, "TopTint", unreal.LinearColor(c[0], c[1], c[2], 1))
    for pn in ("TopStart", "TopSharp", "TopAmount"):
        mel.set_material_instance_scalar_parameter_value(mi, pn, lk[pn])
    if look:
        lk = MAT_LOOK[cat]
        for pn in ("TintA", "TintB"):
            c = lk[pn]; mel.set_material_instance_vector_parameter_value(mi, pn, unreal.LinearColor(c[0], c[1], c[2], 1))
        for pn in ("Tiling", "Roughness", "Desaturate", "DustAmount", "WindAmount", "WindSpeed", "WindScale", "MacroAmount", "MacroTiling", "Metallic"):
            if pn in lk: mel.set_material_instance_scalar_parameter_value(mi, pn, lk[pn])
        if "DustTint" in lk:
            c = lk["DustTint"]; mel.set_material_instance_vector_parameter_value(mi, "DustTint", unreal.LinearColor(c[0], c[1], c[2], 1))
    mel.update_material_instance(mi)

def _build_master(unreal, master, d0, n0, wind=False, macro=None):
    """graf M_RuinStone: textura s nahodnym posunem UV a tintem na kamen + zvetrani shora podle normaly
    (VertexNormalWS.z: plochy nahoru svetlejsi / nazelenale a drsnejsi, rozbite texturou).
    wind=True (M_RuinCloth): navic posun vrcholu podel normaly = WindAmount * vlny (cas + poloha ve svete) a velke skvrny
    (macro = textura T_RuinCanvasMacro, UV * MacroTiling, sila MacroAmount; 0,5 = beze zmeny) proti opakovani male dlazdice."""
    mel = unreal.MaterialEditingLibrary; eal = unreal.EditorAssetLibrary
    for prop in ("used_with_instanced_static_meshes", "used_with_nanite"):
        try: master.set_editor_property(prop, True)
        except Exception: pass
    E = lambda cls, x, y: mel.create_material_expression(master, cls, x, y)
    C = mel.connect_material_expressions
    def scal(name, val, x, y):
        e_ = E(unreal.MaterialExpressionScalarParameter, x, y)
        e_.set_editor_property("parameter_name", name); e_.set_editor_property("default_value", val); return e_
    def vec(name, c, x, y):
        e_ = E(unreal.MaterialExpressionVectorParameter, x, y)
        e_.set_editor_property("parameter_name", name); e_.set_editor_property("default_value", unreal.LinearColor(c[0], c[1], c[2], 1)); return e_
    tc = E(unreal.MaterialExpressionTextureCoordinate, -1400, 0)
    pir = E(unreal.MaterialExpressionPerInstanceRandom, -1400, 200)
    k = E(unreal.MaterialExpressionConstant, -1400, 300); k.set_editor_property("r", 7.31)
    mul = E(unreal.MaterialExpressionMultiply, -1200, 250)
    C(pir, "", mul, "A"); C(k, "", mul, "B")
    add = E(unreal.MaterialExpressionAdd, -1000, 100)          # nahodny posun UV na kamen -> kazdy kamen jinak
    C(tc, "", add, "A"); C(mul, "", add, "B")
    til = scal("Tiling", 1.0, -1000, 300)
    uv = E(unreal.MaterialExpressionMultiply, -800, 150)
    C(add, "", uv, "A"); C(til, "", uv, "B")
    tx = E(unreal.MaterialExpressionTextureSampleParameter2D, -550, -100)
    tx.set_editor_property("parameter_name", "BaseColor")
    if d0: tx.set_editor_property("texture", d0)
    C(uv, "", tx, "UVs")
    ta = vec("TintA", (0.62, 0.58, 0.52), -550, 200)
    tb = vec("TintB", (0.95, 0.90, 0.80), -550, 400)
    lp = E(unreal.MaterialExpressionLinearInterpolate, -300, 300)
    C(ta, "", lp, "A"); C(tb, "", lp, "B"); C(pir, "", lp, "Alpha")
    # odbarveni textury (Desaturate 0..1: stare / morene drevo) a zaprasení (DustTint, DustAmount) - vychozi 0 = beze zmeny
    ds = E(unreal.MaterialExpressionDesaturation, -350, -250)
    C(tx, "RGB", ds, ""); C(scal("Desaturate", 0.0, -550, -300), "", ds, "Fraction")
    bc0 = E(unreal.MaterialExpressionMultiply, -150, -100)
    C(ds, "", bc0, "A"); C(lp, "", bc0, "B")
    bc = E(unreal.MaterialExpressionLinearInterpolate, 0, 0)
    C(bc0, "", bc, "A"); C(vec("DustTint", (0.40, 0.37, 0.32), -300, -450), "", bc, "B")
    C(scal("DustAmount", 0.0, -300, -550), "", bc, "Alpha")
    if wind and macro:
        mu = E(unreal.MaterialExpressionMultiply, -800, -700); C(add, "", mu, "A"); C(scal("MacroTiling", 0.25, -1000, -750), "", mu, "B")
        mt = E(unreal.MaterialExpressionTextureSampleParameter2D, -550, -800)
        mt.set_editor_property("parameter_name", "Macro"); mt.set_editor_property("texture", macro); C(mu, "", mt, "UVs")
        k2 = E(unreal.MaterialExpressionConstant, -550, -600); k2.set_editor_property("r", 2.0)
        m2 = E(unreal.MaterialExpressionMultiply, -350, -750); C(mt, "R", m2, "A"); C(k2, "", m2, "B")
        one_ = E(unreal.MaterialExpressionConstant, -350, -600); one_.set_editor_property("r", 1.0)
        ml = E(unreal.MaterialExpressionLinearInterpolate, -150, -700); C(one_, "", ml, "A"); C(m2, "", ml, "B")
        C(scal("MacroAmount", 0.6, -350, -850), "", ml, "Alpha")
        bcm = E(unreal.MaterialExpressionMultiply, 0, -300); C(bc, "", bcm, "A"); C(ml, "", bcm, "B")
        bc = bcm
    # --- zvetrani shora: maska = saturate((N.z - TopStart) * TopSharp) * TopAmount, rozbita jasem textury
    vn = E(unreal.MaterialExpressionVertexNormalWS, -1400, 900)
    cm = E(unreal.MaterialExpressionComponentMask, -1200, 900)
    for ch, on in (("r", False), ("g", False), ("b", True), ("a", False)): cm.set_editor_property(ch, on)
    C(vn, "", cm, "")
    t_st = scal("TopStart", 0.55, -1200, 1050)
    sb = E(unreal.MaterialExpressionSubtract, -1000, 950); C(cm, "", sb, "A"); C(t_st, "", sb, "B")
    t_sh = scal("TopSharp", 3.0, -1000, 1100)
    m1 = E(unreal.MaterialExpressionMultiply, -800, 950); C(sb, "", m1, "A"); C(t_sh, "", m1, "B")
    sat = E(unreal.MaterialExpressionSaturate, -650, 950); C(m1, "", sat, "")
    brk = E(unreal.MaterialExpressionAdd, -650, 1100)          # 0.5 + jas textury -> skvrny, ne rovnomerny nater
    half = E(unreal.MaterialExpressionConstant, -800, 1150); half.set_editor_property("r", 0.5)
    C(tx, "G", brk, "A"); C(half, "", brk, "B")
    m2 = E(unreal.MaterialExpressionMultiply, -500, 1000); C(sat, "", m2, "A"); C(brk, "", m2, "B")
    t_am = scal("TopAmount", 0.5, -500, 1150)
    m3 = E(unreal.MaterialExpressionMultiply, -350, 1000); C(m2, "", m3, "A"); C(t_am, "", m3, "B")
    mask = E(unreal.MaterialExpressionSaturate, -200, 1000); C(m3, "", mask, "")
    t_ti = vec("TopTint", (0.86, 0.90, 0.76), -350, 700)
    tcol = E(unreal.MaterialExpressionMultiply, -100, 500); C(bc, "", tcol, "A"); C(t_ti, "", tcol, "B")
    fin = E(unreal.MaterialExpressionLinearInterpolate, 100, 200)
    C(bc, "", fin, "A"); C(tcol, "", fin, "B"); C(mask, "", fin, "Alpha")
    mel.connect_material_property(fin, "", unreal.MaterialProperty.MP_BASE_COLOR)
    ro = scal("Roughness", 0.9, -300, 600)
    one = E(unreal.MaterialExpressionConstant, -100, 750); one.set_editor_property("r", 1.0)
    rl = E(unreal.MaterialExpressionLinearInterpolate, 100, 650)
    C(ro, "", rl, "A"); C(one, "", rl, "B"); C(mask, "", rl, "Alpha")
    mel.connect_material_property(rl, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.connect_material_property(scal("Metallic", 0.0, 100, 850), "", unreal.MaterialProperty.MP_METALLIC)   # kov (props); jinak 0
    if n0:
        nx = E(unreal.MaterialExpressionTextureSampleParameter2D, -550, 1400)
        nx.set_editor_property("parameter_name", "Normal"); nx.set_editor_property("texture", n0)
        nx.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
        C(uv, "", nx, "UVs")
        mel.connect_material_property(nx, "RGB", unreal.MaterialProperty.MP_NORMAL)
    if wind:
        # WPO = normala * WindAmount * 0.5 * (sin(t*WindSpeed + p.(1,0.7,0)*WindScale) + sin(1.7*t*WindSpeed + 2.3*p.(...)*WindScale))
        wp = E(unreal.MaterialExpressionWorldPosition, -1400, 1700)
        dv = E(unreal.MaterialExpressionConstant3Vector, -1400, 1850); dv.set_editor_property("constant", unreal.LinearColor(1.0, 0.7, 0.0, 0))
        dp = E(unreal.MaterialExpressionDotProduct, -1200, 1750); C(wp, "", dp, "A"); C(dv, "", dp, "B")
        ws = E(unreal.MaterialExpressionMultiply, -1000, 1750); C(dp, "", ws, "A"); C(scal("WindScale", 0.01, -1200, 1900), "", ws, "B")
        tm = E(unreal.MaterialExpressionTime, -1400, 2000)
        ts = E(unreal.MaterialExpressionMultiply, -1000, 2000); C(tm, "", ts, "A"); C(scal("WindSpeed", 0.6, -1200, 2100), "", ts, "B")
        a1 = E(unreal.MaterialExpressionAdd, -800, 1850); C(ws, "", a1, "A"); C(ts, "", a1, "B")
        s1 = E(unreal.MaterialExpressionSine, -650, 1850); C(a1, "", s1, "")
        k17 = E(unreal.MaterialExpressionConstant, -1000, 2200); k17.set_editor_property("r", 1.7)
        k23 = E(unreal.MaterialExpressionConstant, -1000, 1650); k23.set_editor_property("r", 2.3)
        t2 = E(unreal.MaterialExpressionMultiply, -800, 2100); C(ts, "", t2, "A"); C(k17, "", t2, "B")
        w2 = E(unreal.MaterialExpressionMultiply, -800, 1650); C(ws, "", w2, "A"); C(k23, "", w2, "B")
        a2 = E(unreal.MaterialExpressionAdd, -650, 2000); C(w2, "", a2, "A"); C(t2, "", a2, "B")
        s2 = E(unreal.MaterialExpressionSine, -500, 2000); C(a2, "", s2, "")
        ss = E(unreal.MaterialExpressionAdd, -350, 1900); C(s1, "", ss, "A"); C(s2, "", ss, "B")
        half2 = E(unreal.MaterialExpressionConstant, -350, 2050); half2.set_editor_property("r", 0.5)
        am = E(unreal.MaterialExpressionMultiply, -200, 1950); C(ss, "", am, "A"); C(half2, "", am, "B")
        wa = E(unreal.MaterialExpressionMultiply, -50, 1950); C(am, "", wa, "A"); C(scal("WindAmount", 0.0, -200, 2100), "", wa, "B")
        vn2 = E(unreal.MaterialExpressionVertexNormalWS, -200, 1750)
        wpo = E(unreal.MaterialExpressionMultiply, 100, 1850); C(vn2, "", wpo, "A"); C(wa, "", wpo, "B")
        mel.connect_material_property(wpo, "", unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
    mel.recompile_material(master)
    eal.set_metadata_tag(master, "RuinMatVersion", str(MAT_VERSION))
    eal.save_loaded_asset(master)

def mesh_dir(cat):
    """slozka v UE pro kategorii meshi (MESH_DIRS v config.py)"""
    return "%s/%s" % (MESH_ROOT, MESH_DIRS[cat])

def _needed_meshes():
    """[(jmeno, kategorie)]; kategorie = podslozka OBJ (meshes/<kategorie>) i slozka v UE (mesh_dir)"""
    names = [("SM_RuinStone_%sR%02d_%s" % (w, round(r * 10), v), "stone") for w in ("", "W_") for r in STONE_RATIOS for v in STONE_VARIANTS]
    if DRESSED_FRAMES: names += [("SM_RuinDressed_R%02d_%s" % (round(r * 10), v), "stone") for r in STONE_RATIOS for v in "AB"]
    if WOOD_MESHES: names += [("%s_%s" % (k, v), "wood") for k in WOOD_NOMINAL for v in "ABC"]
    if WOOD_MESHES: names += [("%s_%s" % (k, v), "wood") for k, (_, vs, _s) in ROUND_MESHES.items() for v in vs]
    names += [("%s_%s" % (k, v), cat) for k, (_, vs, cat, _s, _c) in LIB_MESHES.items() for v in vs]
    return names + [(ASHLAR_MESH, "stone")]

_OBJ_BOX = {}          # jmeno meshe -> (min, max) z OBJ v osach UE (mesh_common.obj_v: UE = (x, -y, z) z OBJ)

def _obj_box(path):
    """bounding box OBJ v osach UE, nebo None"""
    mn = [1e30] * 3; mx = [-1e30] * 3
    try:
        with open(path) as f:
            for ln in f:
                if ln.startswith("v "):
                    x, y, z = (float(t) for t in ln.split()[1:4]); p = (x, -y, z)
                    for i in range(3):
                        if p[i] < mn[i]: mn[i] = p[i]
                        if p[i] > mx[i]: mx[i] = p[i]
    except (OSError, ValueError): return None
    return (mn, mx) if mx[0] >= mn[0] else None

def _bbox_ok(bb):
    """bounding box assetu je pouzitelny (ne NaN, nenulovy); po hromadnem importu ho UE obcas vrati s NaN"""
    import math
    try: v = [float(q) for q in (bb.min.x, bb.min.y, bb.min.z, bb.max.x, bb.max.y, bb.max.z)]
    except Exception: return False
    return all(math.isfinite(q) for q in v) and all(v[i + 3] - v[i] > 1e-3 for i in range(3))

IMPORT_TMP = MESH_ROOT + "/_Import"      # docasna slozka importu (po zpracovani se smaze)
TEST_TMP = "/Game/Skvt/Lapikus/_TestFormatu"            # docasna slozka testu tools/checks/UE_Test_Formatu_OBJ.py
# nastaveni buildu ciloveho assetu = klic cache (DDC). min_lightmap_resolution 80 pridano 15. 11. 2026 (MESH_AXES 10):
# pod klicem s predchozimi dvema polozkami uz v cache lezi poskozene zaznamy (stavely je assety s bDoFastBuild)
BUILD_CFG = {"use_high_precision_tangent_basis": True, "use_full_precision_u_vs": True, "min_lightmap_resolution": 80}
FAST_FLAG = b"bDoFastBuild"

def _has_fast_flag(unreal, asset_path):
    """Ma ulozeny asset priznak bDoFastBuild? Python ho nevidi, hleda se jako text v .uasset (jmeno vlastnosti se
    uklada jen pri nevychozi hodnote = True). None = soubor neni. Mesh s priznakem UE stavi vzdy fast buildem
    (bez Nanite, neinicializovane bounds -> nahodne NaN) a build ani ulozeni ho nezrusi; jedina cesta je asset
    smazat a vytvorit znovu (test tools/checks/UE_Test_Formatu_OBJ.py, MODE "pricina", 15. 11. 2026)."""
    try:
        cd = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_content_dir())
        with open(os.path.join(cd, asset_path[len("/Game/"):].split(".")[0] + ".uasset"), "rb") as f:
            return FAST_FLAG in f.read()
    except Exception: return None

def _import_one(unreal, sms, task, n, cat, fresh=False):
    """Import jednoho OBJ do ciloveho assetu bez priznaku bDoFastBuild a s cistym klicem cache.
    Chyba UE: mesh s priznakem bDoFastBuild (forum UE "Meshes built from Interchange have uninitialized bounds") se
    stavi fast buildem a bounds vykreslovacich dat zustanou neinicializovane -> nahodne NaN: "found NaN in Bounds",
    InverseFast / precision loss, prazdny nahled. Python to nepozna (get_bounds je v poradku), priznak build ani
    ulozeni nezrusi a UE si vysledek ulozi do cache (DDC) pod klicem z geometrie a nastaveni buildu - dalsi build
    se stejnym klicem (i v cistem assetu) vezme poskozena data znovu.
    Proto: OBJ se naimportuje do docasneho assetu (IMPORT_TMP; cerstvy import priznak nema), existujici cil
    s priznakem se smaze, cil vznikne kopii docasneho assetu, postavi se z jeho mesh description s fast_build=False
    a pak s nastavenim BUILD_CFG (klic cache, pod kterym se nikdy fast nestavelo).
    fresh=True smaze existujici cil vzdy (oprava). Vrati (StaticMesh nebo None, chyba nebo None)."""
    eal = unreal.EditorAssetLibrary
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    tp = _asset_path(IMPORT_TMP, n)
    if not eal.does_asset_exist(tp):        # Interchange obcas pojmenuje asset jinak (podle objektu v OBJ)
        hits = [a for a in eal.list_assets(IMPORT_TMP, recursive=True) if a.split(".")[-1].startswith(n)] \
            if eal.does_directory_exist(IMPORT_TMP) else []
        if not hits: return None, "import se nepovedl"
        tp = hits[0]
    tmp = unreal.load_asset(tp)
    dp = _asset_path(mesh_dir(cat), n)
    try:
        if eal.does_asset_exist(dp) and (fresh or _has_fast_flag(unreal, dp)):
            eal.delete_asset(dp)                             # priznak nejde zrusit -> novy asset (instance v levelu se
            if eal.does_asset_exist(dp): return None, "stary asset nejde smazat"             # po buildu postavi znovu)
        if not eal.does_asset_exist(dp):
            eal.duplicate_asset(tp, "%s/%s" % (mesh_dir(cat), n))
        sm = unreal.load_asset(dp)
        desc = tmp.get_static_mesh_description(0)
        done = False
        for args, kw in ((([desc],), {"build_simple_collision": False, "fast_build": False}), (([desc], False, False), {})):
            try:
                sm.build_from_static_mesh_descriptions(*args, **kw); done = True; break
            except TypeError: continue                       # jina signatura
        if not done: return sm, "build z mesh description nejde"
        if sms:
            bs = sms.get_lod_build_settings(sm, 0)
            for k, v in BUILD_CFG.items(): bs.set_editor_property(k, v)   # chyba = neznama vlastnost -> mesh mezi "failed"
            sms.set_lod_build_settings(sm, 0, bs)             # radny build s klicem cache, ktery fast build nezna
        return sm, None
    except Exception as ex:
        return unreal.load_asset(dp) if eal.does_asset_exist(dp) else None, str(ex)
    finally:
        try: eal.delete_asset(tp)
        except Exception: pass

def ensure_stone_meshes(unreal, mesh_src, force=False, only=None):
    """Nacte knihovni meshe (kameny, drevo, props ...) ze slozek MESH_ROOT/<MESH_DIRS[kategorie]>; chybejici nebo
    zastarale naimportuje z mesh_src/<kategorie>/*.obj (box kolize + Nanite); force=True vsechny, jako nove assety.
    only = seznam prefixu (napr. ["SM_RuinCanvasTent", "SM_RuinStump"]): jen meshe <prefix> a <prefix>_<varianta>
    (ukazka po tematech, tools/meshes/ukazka.py); None = vsechny (buildy).
    Vrati {jmeno: StaticMesh}; co chybi, nahradi se kostkou. mesh_src = slozka meshes/ v koreni (MESH_SRC)."""
    if not USE_STONE_MESHES: return {}
    eal = unreal.EditorAssetLibrary
    def want(n): return max([v for pf, v in STONE_MESH_VERSION.items() if n.startswith(pf)] or [0])
    need = _needed_meshes()
    if only is not None:
        need = [(n, c) for n, c in need if any(n == p or n.startswith(p + "_") for p in only)]
    missing = []
    for n, cat in need:
        pth = _asset_path(mesh_dir(cat), n)
        if force or not eal.does_asset_exist(pth): missing.append((n, cat)); continue
        a = unreal.load_asset(pth)
        if (want(n) and _ver(eal, a, "RuinStoneVersion") < want(n)) or _ver(eal, a, "RuinMeshAxes") < MESH_AXES \
                or (isinstance(a, unreal.StaticMesh) and not _bbox_ok(a.get_bounding_box())) or _has_fast_flag(unreal, pth):
            missing.append((n, cat))                     # novejsi OBJ, stary zapis os, vadne bounds nebo bDoFastBuild -> znovu
    src = mesh_src
    for n, cat in need:                                  # rozmery z OBJ: nezavisle na tom, co UE vrati po importu
        b = _obj_box(os.path.join(src, cat, n + ".obj"))
        if b: _OBJ_BOX[n] = b
    tasks = []
    for n, cat in missing:
        f = os.path.join(src, cat, n + ".obj")
        if not os.path.exists(f): continue
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", f); t.set_editor_property("destination_path", IMPORT_TMP)
        t.set_editor_property("destination_name", n)
        t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True)
        t.set_editor_property("save", False)
        tasks.append((t, (n, cat)))
    out = {}; n_fix = 0; bad_bounds = []; failed = []; done = set(); flagged = []
    sms = None
    try: sms = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    except Exception: pass
    if tasks:
        unreal.log("Ruin: importuji %d meshu z %s (po jednom, pres %s)" % (len(tasks), src, IMPORT_TMP))
        with unreal.ScopedSlowTask(len(tasks), "Importuji meshe zriceniny...") as task:
            task.make_dialog(False)
            for t, (n, cat) in tasks:
                task.enter_progress_frame(1, "Import %s" % n)
                sm, err = _import_one(unreal, sms, t, n, cat, fresh=force)
                if err: failed.append("%s (%s)" % (n, err))
                if sm is None: continue
                done.add(n)
                if sms:
                    try:      # jednoducha kolize = kvadr (hrac nepropadne)
                        sms.remove_collisions(sm); sms.add_simple_collisions(sm, unreal.ScriptCollisionShapeType.BOX)
                    except Exception as ex: unreal.log_warning("Ruin: kolize %s: %s (pridej rucne Collision -> Add Box)" % (n, ex))
                    try:
                        ns = sm.get_editor_property("nanite_settings"); ns.set_editor_property("enabled", True)
                        sms.set_nanite_settings(sm, ns, True)
                    except Exception as ex: unreal.log_warning("Ruin: Nanite %s: %s (zapni rucne v meshi)" % (n, ex))
                if want(n): eal.set_metadata_tag(sm, "RuinStoneVersion", str(want(n)))
                eal.set_metadata_tag(sm, "RuinMeshAxes", str(MESH_AXES))
                eal.save_loaded_asset(sm)
        try:
            if eal.does_directory_exist(IMPORT_TMP): eal.delete_directory(IMPORT_TMP)
        except Exception: pass
    for n, cat in need:
        dst = mesh_dir(cat); pth = _asset_path(dst, n)
        if not eal.does_asset_exist(pth):
            # Interchange obcas pojmenuje asset jinak (napr. podle objektu v OBJ) - zkus najit podle jmena
            hits = [a for a in eal.list_assets(dst, recursive=True) if a.split(".")[-1].startswith(n)] \
                if eal.does_directory_exist(dst) else []
            if not hits: continue
            pth = hits[0]
        sm = unreal.load_asset(pth)
        if not isinstance(sm, unreal.StaticMesh): continue
        if _fix_collision(unreal, sm, sms): n_fix += 1
        if not _bbox_ok(sm.get_bounding_box()):
            bad_bounds.append(n)
        if _has_fast_flag(unreal, pth): flagged.append(n)
        out[n] = sm
    if tasks:
        unreal.log("Ruin: radny build (bez fast buildu): %d / %d meshu" % (len(done) - len([f for f in failed if f.split(" ")[0] in done]), len(tasks)))
    if failed:
        unreal.log_warning("Ruin: import / radny build se nepodaril u %d meshu: %s" % (len(failed), "; ".join(failed[:6])))
    if flagged:
        unreal.log_warning("Ruin: %d meshu ma v assetu priznak bDoFastBuild (%s%s) - UE je stavi fast buildem (nahodne NaN "
                           "v bounds, bez Nanite). Smaz je v Content Browseru (Force Delete) a spust build znovu."
                           % (len(flagged), ", ".join(flagged[:6]), "..." if len(flagged) > 6 else ""))
    if bad_bounds:
        unreal.log_warning("Ruin: %d meshu ma po importu vadne bounds (NaN): %s - rozmer se vezme z OBJ, pri pristim buildu se "
                           "naimportuji znovu (pripadne v meshi Build / Reimport)" % (len(bad_bounds), ", ".join(bad_bounds)))
    if n_fix: unreal.log("Ruin: kolize opravena u %d meshu kamenu (jednoducha kolize misto Complex as Simple -> jde fyzika)" % n_fix)
    lost = [n for n, _ in need if n not in out]
    if lost:
        unreal.log_warning("Ruin: chybi %d meshu (%s...) -> pouziji se kostky. Chybi slozka %s/ v koreni? (tools/meshes/gen_meshes.py)"
                           % (len(lost), lost[0], MESH_SRC))
    return out

GENERATED = ("M_Ruin", "MI_Ruin", "PM_Ruin")        # generovane materialy v MAT_DIR (repair_assets s materials=True)

def _delete_assets(unreal, folder, prefixes):
    """smaze assety ve slozce, jejichz jmeno zacina nekterym z prefixes; vrati pocet"""
    eal = unreal.EditorAssetLibrary; n = 0
    if not eal.does_directory_exist(folder): return 0
    for a in eal.list_assets(folder, recursive=False):
        if a.split(".")[-1].startswith(tuple(prefixes)) and eal.delete_asset(a): n += 1
    return n

def repair_assets(unreal, mesh_src, materials=False):
    """Oprava assetu (build_fullscope.py): smaze docasne slozky importu a testu a vsechny knihovni meshe SM_Ruin*,
    textury naimportuje znovu a meshe vytvori jako nove assety (bez priznaku bDoFastBuild, viz _import_one).
    materials=True smaze i generovane materialy (GENERATED v MAT_DIR); vytvori je znovu build (all_materials),
    rucni ladeni v nich se ztrati. Volat az po smazani actoru, ktere meshe pouzivaji (pipeline.clear_level),
    a mimo transakci. Vrati dict(deleted_meshes, deleted_materials, meshes)."""
    eal = unreal.EditorAssetLibrary
    for d in (IMPORT_TMP, TEST_TMP):
        try:
            if eal.does_directory_exist(d): eal.delete_directory(d)
        except Exception: pass
    n_del = sum(_delete_assets(unreal, mesh_dir(c), ("SM_Ruin",)) for c in MESH_DIRS)
    n_mat = _delete_assets(unreal, MAT_DIR, GENERATED) if materials else 0
    if materials: SLOT_MATS.clear(); _PM.clear()
    ensure_textures(unreal, force=True)
    _FIX.clear()
    meshes = ensure_stone_meshes(unreal, mesh_src, force=True)
    return dict(deleted_meshes=n_del, deleted_materials=n_mat, meshes=len(meshes))

def _fix_collision(unreal, sm, sms):
    """volne kameny s fyzikou potrebuji jednoduchou kolizi: Complex as Simple (import OBJ / Interchange) fyziku nepusti.
    -> kolize "Default" + kvadr, kdyz zadna jednoducha kolize neni. Vrati True, kdyz se neco menilo."""
    changed = False
    try:
        if sms and sms.get_simple_collision_count(sm) == 0:
            sms.add_simple_collisions(sm, unreal.ScriptCollisionShapeType.BOX); changed = True
    except Exception as ex:
        unreal.log_warning("Ruin: kolize %s: %s (pridej rucne Collision -> Add Box)" % (sm.get_name(), ex))
    try:
        bs = sm.get_editor_property("body_setup")
        if bs and bs.get_editor_property("collision_trace_flag") == unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE:
            bs.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_DEFAULT); changed = True
    except Exception as ex:
        unreal.log_warning("Ruin: Collision Complexity %s: %s (v meshi nastav Collision Complexity = Project Default)" % (sm.get_name(), ex))
    if changed:
        try: sm.modify(); unreal.EditorAssetLibrary.save_loaded_asset(sm)
        except Exception: pass
    return changed

_FIX = {}

def _mesh_fix(unreal, mesh, nominal):
    """Lokalni transformace meshe: posun pivotu do stredu, prohozeni os (kdyz import otocil osy) a rozmer.
    Vrati (Transform rotace+posun pro jednotkove meritko, extent po osach meshe, role os)."""
    key = mesh.get_path_name()
    if key in _FIX: return _FIX[key]
    ob = _OBJ_BOX.get(mesh.get_name())
    if ob:                                               # nase meshe: rozmer z OBJ (UE bounds byvaji po importu NaN)
        (mnx, mny, mnz), (mxx, mxy, mxz) = ob
    else:
        bb = mesh.get_bounding_box()
        if not _bbox_ok(bb):                             # cizi mesh bez platnych bounds: jmenovity rozmer, stred v pocatku
            unreal.log_warning("Ruin: mesh %s nema platne bounds, pouzije se jmenovity rozmer" % key)
            h = [v / 2.0 for v in nominal]; mnx, mny, mnz = (-h[0], -h[1], -h[2]); mxx, mxy, mxz = h
        else:
            mnx, mny, mnz, mxx, mxy, mxz = bb.min.x, bb.min.y, bb.min.z, bb.max.x, bb.max.y, bb.max.z
    ext = [max(mxx - mnx, 0.01), max(mxy - mny, 0.01), max(mxz - mnz, 0.01)]
    c = [(mxx + mnx) / 2, (mxy + mny) / 2, (mxz + mnz) / 2]
    import itertools
    em = max(ext); nm = max(nominal)
    err = lambda pr: sum(abs(ext[i] / em - nominal[pr[i]] / nm) for i in range(3))
    best = min(itertools.permutations(range(3)), key=err)
    if err((0, 1, 2)) <= err(best) + 0.02: best = (0, 1, 2)      # OBJ v osach UE: osy sedi, prohozeni jen u ciziho meshe
    # sloupce rotace: osa meshe i -> svetova role best[i]; liche permutace -> zrcadleni jedne osy (det = +1)
    cols = []
    for i in range(3):
        v = [0.0, 0.0, 0.0]; v[best[i]] = 1.0; cols.append(v)
    inv = sum(1 for i in range(3) for j in range(i + 1, 3) if best[i] > best[j])
    if inv % 2: cols[0] = [-q for q in cols[0]]
    V = lambda q: unreal.Vector(q[0], q[1], q[2])
    rot = unreal.MathLibrary.make_rotation_from_axes(V(cols[0]), V(cols[1]), V(cols[2]))
    _FIX[key] = (rot, ext, best, c)
    return _FIX[key]

def ue_rotator(unreal, s):
    """natoceni kamene / dilce v UE. Model (vypocty, kontroly, nahledy) bere roll jako pravotocivou rotaci kolem osy X
    (osa Y kamene se pri kladnem roll zveda), UE FRotator ma roll opacne (osa Y klesa) -> do UE jde -roll.
    Pitch a yaw se shoduji."""
    return unreal.Rotator(roll=-s.roll, pitch=s.pitch, yaw=s.yaw)

def stone_transform(unreal, s, mesh, nominal):
    """Transformace instance: mesh naskalovany presne na rozmer bloku (s.sx, s.sy, s.sz)."""
    rot, ext, role, c = _mesh_fix(unreal, mesh, nominal)
    k = STONE_OVERSIZE if s.mesh and s.cat == "face" else 1.0
    dims = [max(s.sx, 2) * k, max(s.sy, 2) * k, max(s.sz, 2) * k]
    sc = [dims[role[i]] / ext[i] for i in range(3)]
    local = unreal.Transform(location=unreal.Vector(-c[0] * sc[0], -c[1] * sc[1], -c[2] * sc[2]),
                             rotation=unreal.Rotator(0, 0, 0), scale=unreal.Vector(sc[0], sc[1], sc[2]))
    fix = unreal.Transform(location=unreal.Vector(0, 0, 0), rotation=rot, scale=unreal.Vector(1, 1, 1))
    st = unreal.Transform(location=unreal.Vector(s.x, s.y, s.z), rotation=ue_rotator(unreal, s),
                          scale=unreal.Vector(1, 1, 1))
    cm = unreal.MathLibrary.compose_transforms
    return cm(cm(local, fix), st)

def _unit(unreal, t):
    # UE 5.8: MathLibrary.break_transform v Pythonu neni -> vlastnosti Transform (translation, rotation = Quat)
    return unreal.Transform(location=t.translation, rotation=t.rotation.rotator(), scale=unreal.Vector(1, 1, 1))

def _fix_unit(unreal, s, mesh, nominal):
    """Korekce meshe bez meritka: actor = F * kamen (presne invertovatelne)."""
    rot, ext, role, c = _mesh_fix(unreal, mesh, nominal)
    full = stone_transform(unreal, s, mesh, nominal)
    st = unreal.Transform(location=unreal.Vector(s.x, s.y, s.z), rotation=ue_rotator(unreal, s),
                          scale=unreal.Vector(1, 1, 1))
    return unreal.MathLibrary.compose_transforms(_unit(unreal, full), unreal.MathLibrary.invert_transform(st))

def _resolve(unreal, s, cube, meshes):
    m = meshes.get(s.mesh) if s.mesh else None
    if m is None: return cube, (100.0, 100.0, 100.0)
    if s.mesh == ASHLAR_MESH: return m, (100.0, 100.0, 100.0)
    if s.mesh.rsplit("_", 1)[0] in WOOD_NOMINAL: return m, WOOD_NOMINAL[s.mesh.rsplit("_", 1)[0]]
    if s.mesh.rsplit("_", 1)[0] in ROUND_MESHES: return m, ROUND_MESHES[s.mesh.rsplit("_", 1)[0]][0]
    if s.mesh.rsplit("_", 1)[0] in LIB_MESHES: return m, LIB_MESHES[s.mesh.rsplit("_", 1)[0]][0]
    r = float(s.mesh.rsplit("_R", 1)[1][:2]) / 10
    h, d = STONE_NOMINAL[0], STONE_NOMINAL[1]
    return m, (h * r, d, h)

def mesh_slots(mesh_name):
    """sloty meshe s vice materialy v poradi v OBJ (kulatina, kura, prouti ...), jinak None (jeden material)"""
    if not mesh_name: return None
    pref = mesh_name.rsplit("_", 1)[0]
    if pref in ROUND_MESHES: return ROUND_MESHES[pref][2]
    if pref in LIB_MESHES and len(LIB_MESHES[pref][3]) > 1: return LIB_MESHES[pref][3]
    return None

def is_multi_slot(mesh_name):
    return mesh_slots(mesh_name) is not None

_KINDS = ("endgrain", "bark", "rope", "wattle", "daub", "chinking", "canvas", "ironclean", "iron", "leather", "sandstone", "water", "charcoal", "straw", "wool", "wood")

def apply_materials(unreal, comp, mesh, material, slots=None):
    """material na komponentu meshe. slots = poradi slotu v OBJ (mesh_slots) nebo None (jeden slot = material dilce).
    Slot "wood" = material dilce (uprava dreva / cat), ostatni = SLOT_MATS. Slot se pozna podle jmena (usemtl z OBJ),
    jinak podle poradi v slots."""
    if not material: return
    if not slots:
        comp.set_material(0, material); return
    try: st = list(mesh.get_editor_property("static_materials"))
    except Exception: st = []
    for i in range(max(len(st), 1)):
        nm = str(st[i].get_editor_property("material_slot_name")).lower().replace("_", "") if st else ""
        kind = next((k for k in _KINDS if k in nm), None) or (slots[i] if i < len(slots) else "wood")
        comp.set_material(i, material if kind == "wood" else (SLOT_MATS.get(kind) or material))

_PM = {}

def ensure_phys_material(unreal):
    """PM_RuinStone (fyzikalni material kamene: trenie, odraz, hustota) - vytvori se jednou, pak ho lze ladit v editoru"""
    if "pm" in _PM: return _PM["pm"]
    path = _asset_path(MAT_DIR, "PM_RuinStone"); pm = None
    try:
        eal = unreal.EditorAssetLibrary
        if eal.does_asset_exist(path):
            pm = unreal.load_asset(path)
        else:
            pm = unreal.AssetToolsHelpers.get_asset_tools().create_asset("PM_RuinStone", MAT_DIR, unreal.PhysicalMaterial, unreal.PhysicalMaterialFactoryNew())
            for k, v in (("friction", STONE_PHYSICS["friction"]), ("static_friction", STONE_PHYSICS["friction"]),
                         ("restitution", STONE_PHYSICS["restitution"]), ("density", STONE_PHYSICS["density"] / 1000.0)):
                try: pm.set_editor_property(k, v)
                except Exception: pass
            eal.save_loaded_asset(pm)
    except Exception as ex:
        unreal.log_warning("Ruin: PM_RuinStone nejde vytvorit (%s) - kameny budou mit vychozi fyzikalni material" % ex)
    _PM["pm"] = pm
    return pm

def stone_physics(unreal, act, s, on=True, asleep=False):
    """volny kamen s trvalou fyzikou: hmotnost podle objemu, tlumeni, drsny material.
    asleep = kamen uz je usazeny (ulozena poloha) -> spi, dokud do nej nekdo nestrci"""
    smc = act.static_mesh_component
    if not on:
        smc.set_simulate_physics(False)
        try: smc.set_collision_profile_name("BlockAll")
        except Exception: pass
        smc.set_mobility(unreal.ComponentMobility.STATIC)
        return
    smc.set_mobility(unreal.ComponentMobility.MOVABLE)
    k = STONE_PHYSICS["shrink"]
    if k != 1.0:
        sc = act.get_actor_scale3d(); act.set_actor_scale3d(unreal.Vector(sc.x * k, sc.y * k, sc.z * k))
    try: smc.set_collision_profile_name("PhysicsActor")
    except Exception: pass
    pm = ensure_phys_material(unreal)
    if pm:
        try: smc.set_phys_material_override(pm)
        except Exception: pass
    try: smc.set_mass_override_in_kg(unreal.Name("None"), max(stone_mass_kg(s), 5.0), True)
    except Exception as ex: unreal.log_warning("Ruin: hmotnost %s: %s" % (s.id, ex))
    try:
        smc.set_linear_damping(STONE_PHYSICS["lin_damp"]); smc.set_angular_damping(STONE_PHYSICS["ang_damp"])
    except Exception: pass
    if asleep:
        try:
            bi = smc.get_editor_property("body_instance"); bi.set_editor_property("start_awake", False)
            smc.set_editor_property("body_instance", bi)
        except Exception: pass
    smc.set_simulate_physics(True)


def all_materials(unreal):
    """vsechny materialy kategorii kamenu a dreva {cat: material} (ensure_materials + dlazba + zaloha dreva)"""
    mats = ensure_materials(unreal)
    mats["floor"] = mats.get("frame")
    if not mats.get("wood"):       # MI_RuinWood (+ _Tar, _Oil ...) vytvori ensure_materials; zaloha StarterContent
        mats["wood"] = next((unreal.load_asset(p) for p in MAT_WOOD if unreal.EditorAssetLibrary.does_asset_exist(p.split(".")[0])), None)
    for wc in WOOD_MI: mats[wc] = mats.get(wc) or mats["wood"]
    return mats
