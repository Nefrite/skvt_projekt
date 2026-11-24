"""
build_furnishing.py - vybaveni (06_furnishing), Unreal Editor 5.8

Vybaveni = vsechno, co clovek prenese: props kovarny (kovadlina, mechy s pakou, brus, ponk, truhlik, naradi s listou,
pruty, kos, hranice dreva ...). Pevne casti staveb (vyhen, sloupy, zlab, sud pod okapem, kul u dreva) jsou v 05.
Vybaveni stoji v dostavbach 05 a bere z nich vysky (lano paky z krokve), samo stavby nemeni.

Jeden zdroj poloh: furnishing.json. Kazdy kus je samostatny actor (tag Zricenina_Vybaveni, vybaveni:<skupina>,
id:<skupina>|<kus>) - rucne se posouva, otaci, zvetsuje (Scale), maze nebo duplikuje (Alt+tah, Ctrl+D) a MODE = "capture"
zapise stav levelu primo do furnishing.json (v ramu skupiny: a, c, z nad terenem, smer x, pitch, roll, scale). Dalsi build
i pregenerovani dat (tools/furnishing/gen_furnishing.py slouci data, ulozene polohy necha) postavi kusy tam.

Pouziti v UE: Tools -> Execute Python Script ->
  - vybaveni/<Skupina>.py   jedna skupina (Palac_Kovarna.py) - ostatni se nesmazou ani neprestavi
  - build_furnishing.py     vsechno vybaveni
  - ../build_normal.py      cely hrad (03) + stavby (05) + vybaveni (06)
  - MODE = "build"   postavit (smaze jen sve actory: tag Zricenina_Vybaveni + vybaveni:<skupina>; navic stare actory
                     stejne skupiny z doby, kdy vybaveni bylo v 05 - tag Zricenina_Stavby + stavba:<skupina>)
  - MODE = "capture" zapsat polohy, otoceni a velikosti kusu z levelu do furnishing.json (zaloha .bak); smazany kus
                     -> "removed", kopie kusu (duplikat actoru) -> novy kus <id>_2 ("manual"). Jen po buildu se stejnymi meshi.
  - MODE = "list"    vypsat kusy s polohou z levelu: posun proti specu (s, n v m, z v cm, otoceni, velikost)
  - MODE = "reset"   vratit kusy na polohu podle specu (ITEMS = jen nektere kusy; kopie se smazou; zaloha .bak)
Mimo UE: python build_furnishing.py [list | reset [kusy...]]  (bez argumentu statistika)

Data: furnishing.json (sestavuje tools/furnishing/gen_furnishing.py ze specu, napr. tools/ruin/palac_spec.py, a dopisuje
capture), skupiny v "groups": dict(name, type ("props"), folder, origin, u, v, roof (strecha z 05 pro kusy zavesene na
krokvich), items). Priznaky kusu a slouceni: furn_data.py. Typ props je spolecny s 05: 05_constructions/zr_stavby/vybaveni.py.
"""
import copy, json, math, os, sys


def _boot():
    """zrlib (koren) a zr_stavby (05, typ props a geometrie strech); v UE pri kazdem spusteni nactene znovu
    (ne kdyz se skript nacita jako knihovna pres zrlib/pipeline.py - sys._zr_keep)"""
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.normpath(os.path.join(here, ".."))
    for p in (root, os.path.join(root, "05_constructions"), here):
        if p in sys.path: sys.path.remove(p)
        sys.path.insert(0, p)
    if not getattr(sys, "_zr_keep", False):
        for k in [k for k in sys.modules if k.split(".")[0] in ("zrlib", "zr_stavby", "furn_data")]: del sys.modules[k]
_boot()

from zrlib.config import FURN_TAG, CONSTR_TAG, CUBE_MESH, MAT_GRAYBOX, STAGE_TAG, STAGES
from zrlib import pipeline, ue_assets, ue_actors, validate
from zr_stavby import vybaveni
import importlib, furn_data
importlib.reload(furn_data)           # spoustece zahazuji jen zrlib / zr_stavby; po uprave furn_data.py jinak bezi stara verze

# ------------------------------------------------------------------ nastaveni
MODE = "build"
ONLY = None                              # napr. ["Palac_Kovarna_Vybaveni"] = jen tato skupina
ITEMS = None                             # MODE reset: jen tyto kusy (napr. ["Kovadlina"]); None = vsechny ve skupinach ONLY
DATA_PATH = None                         # None = furnishing.json vedle skriptu

TYPES = {"props": lambda s, c: vybaveni.build_props(s, c["terr"], c["frames"], c["geom"])}
REQUIRED = {"props": ["name", "origin", "u", "v", "items"]}
SCALE_TOL = 0.005                        # zmena meritka pod 0,5 % se nezapisuje
OLD_EDITS = "furnishing_edits.json"      # drivejsi soubor rucnich uprav (do 16. 11. 2026), uz se nepouziva


def _here():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.path.dirname(DATA_PATH) if DATA_PATH else os.getcwd()


def data_path():
    return DATA_PATH or os.path.join(_here(), "furnishing.json")


def load_data():
    return furn_data.load(data_path())


def save_data(data):
    furn_data.save(data_path(), data, backup=True)


def load_frames():
    """strechy a dalsi ramy staveb 05 (vysky kusu zavesenych na krokvich)"""
    with open(os.path.join(_here(), "..", "05_constructions", "constructions.json"), encoding="utf-8") as f:
        return json.load(f).get("frames", [])


def load_ruin():
    return pipeline.load_ruin()


def context(R):
    """teren stejny jako posledni build zriceniny, ramy strech z constructions.json"""
    layout = R.cached_level_terrain(R.load_layout())
    return dict(terr=R.Terrain(layout["terrain"]), frames=load_frames(), geom={})


def _stones(R, spec, ctx):
    """kusy skupiny (bez smazanych) -> seznam Stone; kopie kusu ("mesh") dostanou mesh puvodniho kusu"""
    typ = spec.get("type", "props")
    validate.require(spec, REQUIRED.get(typ, []), "furnishing.json -> groups -> %s (%s)" % (spec.get("name"), typ))
    items = [it for it in spec["items"] if not it.get("removed")]
    st = TYPES[typ](dict(spec, items=items), ctx); R.assign_meshes(st)
    by = {it["id"]: it for it in items}
    for s in st:
        m = by.get(s.id.split("|", 1)[1], {}).get("mesh")
        if m: s.mesh = m
    return st


def compute(R, data, ctx=None):
    """-> {skupina: dict(folder, loose)}; polohy kusu primo z furnishing.json"""
    ctx = ctx or context(R); out = {}
    for spec in data.get("groups", []):
        if ONLY and spec["name"] not in ONLY: continue
        st = spec.get("stage")
        if st and st not in STAGES: raise ValueError("%s: neznama sada etapy %s (STAGES v zrlib/config.py)" % (spec["name"], st))
        out[spec["name"]] = dict(folder=spec.get("folder", "Vybaveni"), stage=st, loose=_stones(R, spec, ctx))
    return out


def _warn_old_edits():
    p = os.path.join(_here(), OLD_EDITS)
    if os.path.exists(p):
        _log("Vybaveni: %s se uz nepouziva (polohy jsou primo ve furnishing.json) - jeho obsah se NEuplatni." % OLD_EDITS)


# ------------------------------------------------------------------ poloha z levelu -> kus v ramu skupiny (i mimo UE)
def apply_pose(grp, it, s, pose, ratio, terr):
    """zapise do kusu it (furnishing.json) polohu z levelu. s = Stone kusu, jak ho postavil build (rozmery pred zmenou),
    pose = [x, y, z, roll, pitch, yaw] stredu kusu (UE cm, st.; roll v konvenci modelu), ratio = zmena rozmeru (sx, sy, sz)."""
    x, y, z, roll, pitch, yaw = pose
    O, U, V = grp["origin"], grp["u"], grp["v"]
    ac = lambda X, Y: (((X - O[0]) * U[0] + (Y - O[1]) * U[1]) / 100, ((X - O[0]) * V[0] + (Y - O[1]) * V[1]) / 100)
    P = lambda a_, c_: (O[0] + (U[0] * a_ + V[0] * c_) * 100, O[1] + (U[1] * a_ + V[1] * c_) * 100)
    zr = terr.z(*P(*it["ref"])) if it.get("ref") else None
    if not it.get("manual") and not it.get("captured"): it["spec"] = copy.deepcopy(furn_data.pose_of(it))
    if "p0" in it:                                       # usek (tyc, lano): koncove body podel osy X kusu
        L = s.sx * ratio[0]; p, w = math.radians(pitch), math.radians(yaw)
        d = (math.cos(p) * math.cos(w), math.cos(p) * math.sin(w), math.sin(p))
        for key, sg in (("p0", -1), ("p1", 1)):
            X, Y, Z = x + sg * d[0] * L / 2, y + sg * d[1] * L / 2, z + sg * d[2] * L / 2
            a, c = ac(X, Y); zg = zr if zr is not None else terr.z(X, Y)
            it[key] = [round(a, 3), round(c, 3), round((Z - zg) / 100, 3)]
        if abs(ratio[1] - 1) > SCALE_TOL or abs(ratio[2] - 1) > SCALE_TOL:
            it["d"] = round(it["d"] * (ratio[1] + ratio[2]) / 2, 4)
    else:
        if any(abs(r - 1) > SCALE_TOL for r in ratio):
            if "size" in it: it["size"] = [round(it["size"][i] * ratio[i], 1) for i in range(3)]
            else:
                k = it.get("scale", (1.0, 1.0, 1.0)); it["scale"] = [round(k[i] * ratio[i], 4) for i in range(3)]
        a, c = ac(x, y); zg = zr if zr is not None else terr.z(x, y)
        it["a"], it["c"] = round(a, 3), round(c, 3)
        if "zc" in it: it["zc"] = round((z - zg) / 100, 3)
        else: it["z"] = round((z - zg - s.sz * ratio[2] / 2) / 100, 3)
        w = math.radians(yaw); dx, dy = math.cos(w), math.sin(w)
        it["x"] = [round(dx * U[0] + dy * U[1], 4), round(dx * V[0] + dy * V[1], 4)]
        for k, v in (("pitch", pitch), ("roll", roll)):
            v = round(((v + 180) % 360) - 180, 2)
            if abs(v) > 0.01 or k in it: it[k] = v
    it["captured"] = True


# ------------------------------------------------------------------ Unreal
def _mine(a):
    """actor vybaveni ve skupinach ONLY (i stary actor z 05 se stejnym jmenem skupiny)"""
    g = ue_actors.tag_value(a, "vybaveni:") or ue_actors.tag_value(a, "stavba:")
    return not ONLY or g in ONLY


def build_in_unreal():
    import unreal
    _warn_old_edits()
    R = load_ruin(); data = load_data()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    groups = compute(R, data)
    cube = unreal.load_asset(CUBE_MESH); mats = ue_assets.all_materials(unreal); meshes = R.ensure_stone_meshes(unreal)
    if unreal.EditorAssetLibrary.does_asset_exist(MAT_GRAYBOX.split(".")[0]): mats["graybox"] = unreal.load_asset(MAT_GRAYBOX)
    else: _log("Vybaveni: graybox material %s v projektu neni, kvadry dostanou vychozi material." % MAT_GRAYBOX)
    tag = unreal.Name(FURN_TAG); n = 0
    names = set(ONLY or [g["name"] for g in data.get("groups", [])])
    with unreal.ScopedEditorTransaction("Build furnishing"):
        ue_actors.destroy_tagged(eas, tag, _mine)
        # vybaveni postavene drive jako stavba 05 (stejne jmeno skupiny): smazat, jinak by v levelu zustalo dvakrat
        ue_actors.destroy_tagged(eas, unreal.Name(CONSTR_TAG), lambda a: ue_actors.tag_value(a, "stavba:") in names)
        for name, g in groups.items():
            st_tags = [STAGE_TAG + g["stage"]] if g.get("stage") else []
            for s in g["loose"]:
                act = ue_actors.spawn_loose(unreal, eas, s, cube, meshes, [tag, "id:" + s.id, "vybaveni:" + name] + st_tags, g["folder"], mats.get(s.cat))
                if act is not None: n += 1
    cnt = lambda k: sum(1 for g in data.get("groups", []) if g["name"] in groups for it in g["items"] if it.get(k))
    unreal.log("Vybaveni: %d kusu ve %d skupinach (%s); z levelu %d, smazanych %d, pridanych %d." % (
        n, len(groups), ", ".join(groups), cnt("captured"), cnt("removed"), cnt("manual")))


def _level_actors(unreal, eas):
    """{id kusu: [actory]} - duplikovany actor ma stejny tag id: jako puvodni"""
    out = {}
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        if FURN_TAG not in tags: continue
        ids = [t[3:] for t in tags if t.startswith("id:")]
        if ids: out.setdefault(ids[0], []).append(a)
    return out


def _actor_pose(unreal, s, actor, cube, meshes):
    """-> (pose [x, y, z, roll, pitch, yaw], ratio rozmeru (sx, sy, sz), zmena?) actoru proti kusu s"""
    m, nom = ue_assets._resolve(unreal, s, cube, meshes)
    _, _, role, _ = ue_assets._mesh_fix(unreal, m, nom)
    gen = ue_assets.stone_transform(unreal, s, m, nom).scale3d; cur = actor.get_actor_scale3d()
    g3, c3 = (gen.x, gen.y, gen.z), (cur.x, cur.y, cur.z)
    ratio = [1.0, 1.0, 1.0]
    for i in range(3): ratio[role[i]] = c3[i] / g3[i] if abs(g3[i]) > 1e-9 else 1.0
    s2 = copy.copy(s); s2.sx, s2.sy, s2.sz = s.sx * ratio[0], s.sy * ratio[1], s.sz * ratio[2]
    pose, same = ue_actors.loose_pose(unreal, s2, cube, meshes, actor)
    return pose, ratio, not same or any(abs(r - 1) > SCALE_TOL for r in ratio)


def capture_edits():
    """zapise stav kusu skupin ONLY z levelu do furnishing.json: posun, otoceni a meritko (captured), smazane (removed),
    kopie actoru (novy kus manual)"""
    import unreal
    _warn_old_edits()
    R = load_ruin(); data = load_data(); ctx = context(R)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    cube = unreal.load_asset(CUBE_MESH); meshes = R.ensure_stone_meshes(unreal)
    level = _level_actors(unreal, eas)
    n_rem = n_mov = n_new = 0
    for grp in data.get("groups", []):
        name = grp["name"]
        if ONLY and name not in ONLY: continue
        stones = {s.id: s for s in _stones(R, grp, ctx)}
        if stones and not any(k in level for k in stones):          # skupina neni v levelu postavena: nic neukladat
            unreal.log_warning("Vybaveni: skupina %s nema v levelu zadny actor - preskocena (nejdriv build)." % name); continue
        for it in list(grp["items"]):
            if it.get("removed"): continue
            sid = "%s|%s" % (name, it["id"]); s = stones.get(sid)
            if s is None: continue
            acts = level.pop(sid, [])
            if not acts:
                it["removed"] = True; n_rem += 1; continue
            m, nom = ue_assets._resolve(unreal, s, cube, meshes)
            exp = ue_assets.stone_transform(unreal, s, m, nom).translation
            acts.sort(key=lambda a: (a.get_actor_location() - exp).length())   # puvodni = nejbliz generovane poloze
            pose, ratio, changed = _actor_pose(unreal, s, acts[0], cube, meshes)
            if changed: apply_pose(grp, it, s, pose, ratio, ctx["terr"]); n_mov += 1
            for a in acts[1:]:                                                  # kopie kusu -> novy kus
                new = {k: copy.deepcopy(v) for k, v in it.items() if k not in ("spec", "captured", "removed")}
                new.update(id=furn_data.new_id(grp["items"], it["id"]), manual=True, copy_of=it.get("copy_of", it["id"]), mesh=s.mesh)
                pose, ratio, _ = _actor_pose(unreal, s, a, cube, meshes)
                apply_pose(grp, new, s, pose, ratio, ctx["terr"]); grp["items"].append(new); n_new += 1
                nid = "%s|%s" % (name, new["id"])
                a.tags = [unreal.Name("id:" + nid) if str(t).startswith("id:") else t for t in a.tags]
                a.set_actor_label("Kamen_" + nid.replace("|", "_"))
    stray = [k for k, v in level.items() if (not ONLY or k.split("|")[0] in ONLY)]
    save_data(data)
    unreal.log("furnishing.json: posunuto %d, nove smazano %d, pridano kopii %d (zaloha furnishing.json.bak)." % (n_mov, n_rem, n_new))
    for k in stray: unreal.log_warning("Vybaveni: actor id:%s nema kus ve furnishing.json (neulozeno)." % k)


# ------------------------------------------------------------------ vypis a vraceni na spec (i mimo UE)
def _log(msg):
    try:
        import unreal; unreal.log(msg)
    except ImportError:
        print(msg)


def report():
    """kusy s polohou z levelu: posun proti specu v ramu skupiny (s, n v m), vyska (cm), otoceni (st.), velikost"""
    data = load_data(); R = None; ctx = None; lines = []
    for grp in data.get("groups", []):
        if ONLY and grp["name"] not in ONLY: continue
        cap = [it for it in grp["items"] if it.get("captured") and not it.get("removed")]
        for it in grp["items"]:
            if it.get("removed"): lines.append("  %-40s smazany" % ("%s|%s" % (grp["name"], it["id"])))
        if not cap: continue
        if R is None: R = load_ruin(); ctx = context(R)
        spec_g = dict(grp, items=[dict(it, **(it.get("spec") or {})) for it in cap])
        cur = {s.id: s for s in _stones(R, dict(grp, items=cap), ctx)}
        ref = {s.id: s for s in _stones(R, spec_g, ctx)}
        U, V = grp["u"], grp["v"]
        for it in cap:
            sid = "%s|%s" % (grp["name"], it["id"]); s, r = cur[sid], ref[sid]
            dx, dy = (s.x - r.x) / 100, (s.y - r.y) / 100
            sc = "" if (s.sx, s.sy, s.sz) == (r.sx, r.sy, r.sz) else ", velikost x%.2f / %.2f / %.2f" % (s.sx / r.sx, s.sy / r.sy, s.sz / r.sz)
            tag = " (kopie %s)" % it.get("copy_of") if it.get("manual") else ""
            lines.append("  %-40s s %+.2f m, n %+.2f m, z %+.0f cm, otoceni %+.0f st.%s%s%s" % (
                sid, dx * U[0] + dy * U[1], dx * V[0] + dy * V[1], s.z - r.z, ((s.yaw - r.yaw) + 180) % 360 - 180,
                "" if abs(s.pitch - r.pitch) < 1 and abs(s.roll - r.roll) < 1 else " (naklopeno)", sc, tag))
    if not lines: _log("Vybaveni: vsechny kusy podle specu."); return
    _log("Vybaveni: kusy s polohou z levelu (%d), posun proti specu:" % len(lines))
    for l in lines: _log(l)


def reset_edits(items=None):
    data = load_data()
    n_pose, n_rem, n_man = furn_data.reset(data, ONLY, items)
    if not (n_pose or n_rem or n_man): _log("Vybaveni: zadne kusy k vraceni na spec."); return
    save_data(data)
    _log("Vybaveni: na spec vraceno %d poloh, obnoveno %d smazanych, odebrano %d kopii (zaloha furnishing.json.bak); postav vybaveni znovu." % (
        n_pose, n_rem, n_man))


def _has_unreal():
    try:
        import unreal  # noqa
        return True
    except ImportError:
        return False


def run(only=None, mode=None, items=None):
    """spusteni pro vybrane skupiny (vybaveni/<Skupina>.py): only = jmena skupin z furnishing.json,
    mode = "build" / "capture" / "list" / "reset"; items = kusy pro reset"""
    global ONLY, MODE
    ONLY = list(only) if only else None
    MODE = mode or MODE
    if MODE == "list": report()
    elif MODE == "reset": reset_edits(items if items is not None else ITEMS)
    elif MODE == "capture": capture_edits(); report()
    else: build_in_unreal()


if (__name__ == "__main__" or "unreal" in sys.modules) and not getattr(sys, "_furn_import_only", False):
    if _has_unreal():
        run(ONLY, MODE, ITEMS)
    elif len(sys.argv) > 1:
        run(None, sys.argv[1], sys.argv[2:] or None)
    else:
        for n, g in compute(load_ruin(), load_data()).items():
            c = {}
            for s in g["loose"]: c[s.cat] = c.get(s.cat, 0) + 1
            print("  %-26s %-34s %s" % (n, g["folder"], ", ".join("%s %d" % kv for kv in sorted(c.items()))))
