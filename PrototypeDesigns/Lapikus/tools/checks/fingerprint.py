"""fingerprint.py - otisk vystupu vsech skriptu (pro refaktoring: pred a po zmene musi vyjit stejne).
python fingerprint.py <koren repozitare> <otisk.json> [--state <slozka>] [--layout <ruin_layout.json>] [--heightmap <png>]
                      [--compare <jiny otisk.json>]
Otisk: kameny zriceniny (03) a staveb (05) pro dany stav, vystup generatoru JSON (gen_layout, gen_constructions)
a sled vsech volani Unreal API pri buildu / capture / freeze / detach (unreal = MagicMock, bez editoru).
--state    slozka s manual_edits.json a terrain_from_level.json z levelu (jinak ty z repozitare)
--layout   dalsi ruin_layout.json pro vypocet 03 (napr. s jinym terenem)
--heightmap heightmapa pro gen_layout (bez ni se generatory nespousti)
Kod v koreni se zkopiruje do docasne slozky, repozitar se nemeni. Potrebuje Python 3 (bez Unrealu)."""
import sys, os, json, shutil, hashlib, importlib.util, re, subprocess, tempfile, types, argparse
from unittest import mock
ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("out"); ap.add_argument("--state"); ap.add_argument("--layout")
ap.add_argument("--heightmap"); ap.add_argument("--compare"); A = ap.parse_args()
src = os.path.abspath(A.root); out = os.path.abspath(A.out)
for k in ("state", "layout", "heightmap", "compare"):
    if getattr(A, k): setattr(A, k, os.path.abspath(getattr(A, k)))
W = tempfile.mkdtemp()
for d in os.listdir(src):
    if d in ("03_ruin", "05_constructions", "tools", "zrlib"):
        shutil.copytree(os.path.join(src, d), os.path.join(W, d), ignore=shutil.ignore_patterns("__pycache__", "*.png", "*.obj"))
B3 = os.path.join(W, "03_ruin", "blocks")
if A.state:
    for f in ("manual_edits.json", "terrain_from_level.json"):
        if os.path.exists(os.path.join(A.state, f)): shutil.copy(os.path.join(A.state, f), B3)
shutil.rmtree(os.path.join(B3, "stones"), ignore_errors=True); os.symlink(os.path.join(src, "03_ruin", "blocks", "stones"), os.path.join(B3, "stones"))
res = {}
def rows(stones):
    r = []
    for s in stones:
        r.append("%s|%s|%s|%.2f|%.2f|%.2f|%.3f|%.3f|%.3f|%.2f|%.2f|%.2f|%s" % (s.id, s.cat, s.mesh, s.x, s.y, s.z, s.yaw, s.pitch, s.roll, s.sx, s.sy, s.sz, getattr(s, "rough", None)))
    return sorted(r)
def h(x): return hashlib.md5(json.dumps(x, sort_keys=True).encode()).hexdigest()
def load(path, name, flag):
    setattr(sys, flag, True)
    try:
        sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    finally: setattr(sys, flag, False)
    return m
os.chdir(W)
R = load(os.path.join(B3, "build_ruin_blocks.py"), "build_ruin_blocks", "_ruin_import_only")
if A.layout:
    d, P = R.compute_blocks(json.load(open(A.layout)))
    res["03_layout"] = {n: h(rows(w["stones"]) + ["L"] + rows(w.get("loose", []))) for n, w in d.items()}
lay = R.cached_level_terrain(R.load_layout()); rm, mv = R.load_manual(); det = R.load_detached()
d2, P2 = R.compute_blocks(lay, rm, mv, None, detached=det)
res["03_lvl"] = {n: h(rows(w["stones"]) + ["L"] + rows(w.get("loose", []))) for n, w in d2.items()}
res["03_rubble"] = h(rows([s for r in R.make_rubble(d2, P2, R.Terrain(lay["terrain"])).values() for s in r["stones"]]))
BC = load(os.path.join(W, "05_constructions", "build_constructions.py"), "build_constructions", "_constr_import_only")
R5 = BC.load_ruin(); data = BC.load_data()
g, _ = BC.compute(R5, data, *BC.load_edits())
res["05"] = {n: h(rows(x["stones"]) + ["L"] + rows(x["loose"]) + [x["folder"], x.get("stavba", "")]) for n, x in g.items()}
# generatory JSON
o1 = os.path.join(W, "_lay.json"); o2 = os.path.join(W, "_con.json")
if A.heightmap:
    subprocess.run([sys.executable, os.path.join(W, "tools", "ruin", "gen_layout.py"), os.path.join(src, "03_ruin", "ruin_layout_draft.json"),
                    os.path.abspath(A.heightmap), o1], check=True, capture_output=True, cwd=os.path.join(W, "tools", "ruin"))
    subprocess.run([sys.executable, os.path.join(W, "tools", "constructions", "gen_constructions.py"), os.path.join(src, "03_ruin", "ruin_layout_draft.json"), o2, o1],
                   check=True, capture_output=True, cwd=os.path.join(W, "tools", "constructions"))
    res["gen_layout"] = h(json.load(open(o1))); res["gen_constructions"] = h(json.load(open(o2)))
# Unreal: sled volani
class FM(mock.MagicMock):
    """MagicMock, ktery se da porovnavat a prevadet na cisla (jako 0)"""
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        for op in ("__lt__", "__gt__", "__le__", "__ge__"): getattr(self, op).return_value = False
        self.__float__.return_value = 0.0; self.__int__.return_value = 0; self.__index__.return_value = 0
    def __getattr__(self, name):
        if name == "get_bounding_box":
            V = types.SimpleNamespace
            return lambda: V(min=V(x=-50.0, y=-50.0, z=-50.0), max=V(x=50.0, y=50.0, z=50.0))
        return super().__getattr__(name)
    def _get_child_mock(self, **kw):
        n = kw.get("name") or kw.get("_new_name") or ""
        return mock.MagicMock(**kw) if str(n).startswith("__") else FM(**kw)
def trace(fn):
    U = FM(name="unreal")
    eas = U.get_editor_subsystem.return_value
    eas.get_all_level_actors.return_value = []; eas.get_selected_level_actors.return_value = []
    U.EditorAssetLibrary.does_asset_exist.return_value = False
    sys.modules["unreal"] = U
    err = None
    try: fn(U)
    except Exception as e:
        import traceback; tb = traceback.extract_tb(e.__traceback__)
        err = "%s: %s @ %s" % (type(e).__name__, str(e)[:120], " < ".join("%s:%d" % (f.name, f.lineno) for f in tb[-3:]))
    finally: sys.modules.pop("unreal", None)
    calls = [re.sub(r" id='\d+'", "", repr(c)).replace(W, "<W>") for c in U.mock_calls]
    return dict(n=len(calls), h=h(calls), err=err, head=calls[:3])
def r3(**kw):
    def f(U):
        R_ = load(os.path.join(B3, "build_ruin_blocks.py"), "build_ruin_blocks", "_ruin_import_only")
        R_.TERRAIN_FROM_LEVEL = False
        R_.run(kw.get("cast"), kw.get("mode", "build"))
    return f
def r5(only, mode):
    def f(U):
        B_ = load(os.path.join(W, "05_constructions", "build_constructions.py"), "build_constructions", "_constr_import_only")
        B_.run(only, mode)
    return f
res["ue_03_full"] = trace(r3())
res["ue_03_palac"] = trace(r3(cast=["Palac"]))
res["ue_03_capture"] = trace(r3(mode="capture"))
res["ue_05_full"] = trace(r5(None, "build"))
res["ue_05_ostroh"] = trace(r5(["Ostroh_Krov"], "build"))
res["ue_05_capture"] = trace(r5(None, "capture"))
res["ue_05_freeze"] = trace(r5(None, "freeze"))
def det(mode):
    def f(U):
        D = load(os.path.join(B3, "detach_stones.py"), "detach_stones", "_x")
        D.MODE = mode
        {"detach": D.detach, "undo": D.undo, "freeze": D.freeze}[mode]()
    return f
for m_ in ("detach", "undo", "freeze"): res["ue_detach_" + m_] = trace(det(m_))
json.dump(res, open(out, "w"), indent=1, sort_keys=True)
shutil.rmtree(W, ignore_errors=True)
print("otisk:", out)
if A.compare:
    a = json.load(open(A.compare)); bad = 0
    for k in sorted(set(a) | set(res)):
        if a.get(k) != res.get(k):
            bad += 1
            x, y = a.get(k), res.get(k)
            if isinstance(x, dict) and isinstance(y, dict) and "n" in x: print("ROZDIL", k, "volani %s -> %s" % (x["n"], y["n"]), y.get("err") or "")
            elif isinstance(x, dict) and isinstance(y, dict): print("ROZDIL", k, sorted(n for n in set(x) | set(y) if x.get(n) != y.get(n)))
            else: print("ROZDIL", k)
    print("SHODA" if not bad else "rozdilu: %d" % bad)
    sys.exit(1 if bad else 0)
