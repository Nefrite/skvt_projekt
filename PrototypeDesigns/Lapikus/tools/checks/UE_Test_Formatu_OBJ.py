"""UE_Test_Formatu_OBJ.py - (test 1, MODE "formaty") porovna, jestli poskozene vykreslovaci data meshi ("FStaticMeshRenderData::Serialize found NaN
in Bounds") zpusobuje novy zapis OBJ (od 15. 11. 2026: osy UE, zrcadlene Y, obracene trojuhelniky), nebo vznikaji i se
starym zapisem (do 14. 11.: OBJ Y-up, (x, z, -y), puvodni poradi vrcholu).
Unreal: Tools -> Execute Python Script -> tools/checks/UE_Test_Formatu_OBJ.py

Postup:
  1. Vezme OBJ kamenu z meshes/stone (soucasny zapis) a z kazdeho vyrobi variantu "stary" (prepocet os a poradi vrcholu).
  2. Obe varianty naimportuje (po jednom, jako build) do docasne slozky /Game/Skvt/Lapikus/_TestFormatu, v ROUNDS kolech.
     Kazde kolo posune vsechny body o jiny nepatrny kousek (setiny milimetru), aby UE nevzal vysledek z cache (DDC)
     a mesh opravdu postavil.
  3. Z logu UE (Saved/Logs/<projekt>.log) spocita hlaseni "found NaN in Bounds" a "nearly zero tangents" pro kazdou
     variantu a vypise je do Output Logu (radky "TEST FORMATU:"). Docasnou slozku smaze. Level ani ostatni assety nemeni.
  Test 1 (15. 11. 2026): oba zapisy 0 z 99 -> pricina neni ve formatu OBJ. Test 2 (MODE "kroky"): ktery krok buildu
  (kolize + Nanite, reimport do existujiciho assetu) data kazi.
  Test 3 (MODE "pricina"): proc se stejne OBJ v novych assetech stavi ciste a ve slozce Ruin/Stones ne. Podezreli jsou
  dva: priznak bDoFastBuild ulozeny v existujicich assetech kamenu (33 z 33, ostatni meshe 0 ze 78; Python ho nevidi,
  hleda se jako text v .uasset) a poskozene zaznamy v cache (DDC) pod klicem neposunute geometrie. Kazda varianta
  dela totez co build (ue_assets._import_one: import do docasneho assetu, cil se postavi z mesh description
  s fast_build=False, BUILD_CFG, kolize, Nanite, ulozit) a lisi se jen v jednom:
    "cache"    puvodni OBJ beze zmeny (stejny klic cache jako build), cil = kopie docasneho importu (bez priznaku)
    "priznak"  posunuta data (cista cache), cil = kopie existujiciho kamene z Ruin/Stones (s priznakem)
    "kontrola" posunuta data (cista cache), cil = kopie docasneho importu (bez priznaku) -> ma vyjit cista
  NaN jen u "cache" = vinna cache; jen u "priznak" = vinen priznak; u obou = oboji. Posun se pri kazdem spusteni lisi.
  Kdyby log jeste nebyl zapsany (vysledek "log zatim neobsahuje konec testu"), spust skript znovu s MODE = "report".
"""
MODE = "pricina"              # "pricina" = test 3: cache / priznak bDoFastBuild / kontrola (viz vyse),
                              # "formaty" = novy / stary zapis OBJ (test 1: oba cisty),
                              # "kroky" = soucasny zapis, ktery krok buildu data kazi: "cisty" (jen import do noveho assetu),
                              #   "nanite" (+ kolize a Nanite jako build), "reimport" (+ znovu import do existujiciho assetu),
                              # "report" = jen znovu vyhodnotit log posledniho testu
ROUNDS = 2                    # kola importu (vic = spolehlivejsi, ~1 s na mesh a kolo a variantu)
ONLY = None                   # napr. ["SM_RuinStone_R12_B"] = jen vybrane meshe; None = vsechny kameny
DST = "/Game/Skvt/Lapikus/_TestFormatu"
MARK = "TEST FORMATU KONEC"

STONES = "/Game/Skvt/Lapikus/Ruin/Stones"          # existujici kameny (zrlib/config.py STONE_DIR)
BUILD_CFG = {"use_high_precision_tangent_basis": True, "use_full_precision_u_vs": True}   # jako zrlib/ue_assets.py
FLAG = b"bDoFastBuild"
CAUSE = ("cache", "priznak", "kontrola")

import os, json, re, tempfile, time


def _root():
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def _state_path():
    return os.path.join(tempfile.gettempdir(), "skvt_test_formatu.json")


def _log_path(unreal):
    d = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_log_dir())
    name = os.path.splitext(os.path.basename(unreal.Paths.get_project_file_path()))[0]
    p = os.path.join(d, name + ".log")
    if os.path.exists(p): return p
    logs = [os.path.join(d, f) for f in os.listdir(d) if f.endswith(".log")] if os.path.isdir(d) else []
    return max(logs, key=os.path.getmtime) if logs else p


def _variant(lines, variant, shift):
    """radky soucasneho OBJ -> varianta. Soucasny zapis: v = (x, -y, z) bodu generatoru, trojuhelnik (a, c, b).
    Stary zapis: v = (x, z, -y), trojuhelnik (a, b, c). shift = posun v cm (proti cache)."""
    out = []
    for ln in lines:
        if ln.startswith("v ") or ln.startswith("vn "):
            tag, a, b, c = ln.split()[:4]; vx, vy, vz = float(a), float(b), float(c)
            x, y, z = vx, -vy, vz                                   # body generatoru (osy UE)
            if variant == "stary": p = (x, z, -y)
            else: p = (vx, vy, vz)
            if tag == "v": p = (p[0] + shift, p[1] + shift, p[2] + shift)
            out.append("%s %.4f %.4f %.4f\n" % (tag, p[0], p[1], p[2]))
        elif ln.startswith("f ") and variant == "stary":
            t = ln.split()[1:4]; out.append("f %s %s %s\n" % (t[0], t[2], t[1]))
        else:
            out.append(ln if ln.endswith("\n") else ln + "\n")
    return out


def run_test(unreal):
    eal = unreal.EditorAssetLibrary
    src = os.path.join(_root(), "meshes", "stone")
    files = sorted(f for f in os.listdir(src) if f.endswith(".obj") and (not ONLY or f[:-4] in ONLY))
    if not files:
        unreal.log_error("TEST FORMATU: v %s nejsou OBJ (tools/meshes/gen_meshes.py)" % src); return
    log = _log_path(unreal)
    start = os.path.getsize(log) if os.path.exists(log) else 0
    tmp = tempfile.mkdtemp(prefix="skvt_formaty_")
    tasks = []
    variants = ("novy", "stary") if MODE == "formaty" else ("cisty", "nanite", "reimport")
    for r in range(ROUNDS):
        for variant in variants:
            folder = "%s/%s_%d" % (DST, variant, r)
            shift = 0.0001 * (1 + r * 5 + variants.index(variant))     # kazde kolo a varianta jina data
            for f in files:
                lines = open(os.path.join(src, f)).readlines()
                p = os.path.join(tmp, "%s_%d_%s" % (variant, r, f))
                open(p, "w").writelines(_variant(lines, variant, shift))
                t = unreal.AssetImportTask()
                t.set_editor_property("filename", p); t.set_editor_property("destination_path", folder)
                t.set_editor_property("destination_name", f[:-4])
                t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True)
                t.set_editor_property("save", False)
                tasks.append((t, variant, r, f[:-4], folder))
    json.dump({"log": log, "start": start, "files": len(files), "rounds": ROUNDS, "variants": variants}, open(_state_path(), "w"))
    sms = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    at = unreal.AssetToolsHelpers.get_asset_tools()
    with unreal.ScopedSlowTask(len(tasks), "Test formatu OBJ...") as task:
        task.make_dialog(True)
        cur = None
        for t, variant, r, n, folder in tasks:
            if task.should_cancel(): break
            if (variant, r) != cur:
                cur = (variant, r); unreal.log("TEST FORMATU ZACATEK %s %d" % cur)
            task.enter_progress_frame(1, "%s" % t.get_editor_property("filename"))
            at.import_asset_tasks([t])
            if variant in ("nanite", "reimport"):              # jako build: kolize box + Nanite, ulozit
                sm = unreal.load_asset("%s/%s.%s" % (folder, n, n))
                if sm:
                    try: sms.remove_collisions(sm); sms.add_simple_collisions(sm, unreal.ScriptCollisionShapeType.BOX)
                    except Exception: pass
                    try:
                        ns = sm.get_editor_property("nanite_settings"); ns.set_editor_property("enabled", True)
                        sms.set_nanite_settings(sm, ns, True)
                    except Exception: pass
                    eal.save_loaded_asset(sm)
            if variant == "reimport":                          # znovu stejny OBJ do existujiciho assetu (jako build)
                unreal.log("TEST FORMATU REIMPORT")
                at.import_asset_tasks([t])
    try: eal.delete_directory(DST)
    except Exception: pass
    unreal.log(MARK)
    report(unreal)


def _has_flag(unreal, game_path):
    """je v ulozenem .uasset jmeno bDoFastBuild? (uklada se jen pri nevychozi hodnote = True). None = soubor neni"""
    cd = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_content_dir())
    f = os.path.join(cd, game_path[len("/Game/"):].split(".")[0] + ".uasset")
    try:
        with open(f, "rb") as fh: return FLAG in fh.read()
    except OSError: return None


def _as_build(unreal, sms, eal, tmp, sm):
    """stejne kroky jako ue_assets._import_one + ensure_stone_meshes: build z mesh description docasneho assetu
    s fast_build=False, BUILD_CFG, kolize box, Nanite, ulozit"""
    desc = tmp.get_static_mesh_description(0)
    for args, kw in ((([desc],), {"build_simple_collision": False, "fast_build": False}), (([desc], False, False), {})):
        try:
            sm.build_from_static_mesh_descriptions(*args, **kw); break
        except TypeError: continue
    bs = sms.get_lod_build_settings(sm, 0)
    for k, v in BUILD_CFG.items(): bs.set_editor_property(k, v)
    sms.set_lod_build_settings(sm, 0, bs)
    try: sms.remove_collisions(sm); sms.add_simple_collisions(sm, unreal.ScriptCollisionShapeType.BOX)
    except Exception: pass
    try:
        ns = sm.get_editor_property("nanite_settings"); ns.set_editor_property("enabled", True)
        sms.set_nanite_settings(sm, ns, True)
    except Exception: pass
    eal.save_loaded_asset(sm)


def run_cause(unreal):
    """test 3: cache / priznak / kontrola (popis v hlavicce)"""
    eal = unreal.EditorAssetLibrary
    src = os.path.join(_root(), "meshes", "stone")
    files = sorted(f for f in os.listdir(src) if f.endswith(".obj") and (not ONLY or f[:-4] in ONLY))
    if not files:
        unreal.log_error("TEST FORMATU: v %s nejsou OBJ (tools/meshes/gen_meshes.py)" % src); return
    log = _log_path(unreal)
    start = os.path.getsize(log) if os.path.exists(log) else 0
    tmpd = tempfile.mkdtemp(prefix="skvt_pricina_")
    base = 20 + int(time.time()) % 9000                     # posun 0,002 - 0,9 cm, pri kazdem spusteni jiny (cista cache)
    sms = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    at = unreal.AssetToolsHelpers.get_asset_tools()
    flags = dict((v, [0, 0]) for v in CAUSE)                # varianta -> [ulozenych cilu, z toho s priznakem]
    skipped = 0
    orig = [_has_flag(unreal, "%s/%s" % (STONES, f[:-4])) for f in files]
    state = {"log": log, "start": start, "files": len(files), "rounds": ROUNDS, "variants": CAUSE, "cause": True,
             "orig": [sum(1 for q in orig if q), sum(1 for q in orig if q is not None)]}
    json.dump(state, open(_state_path(), "w"))
    with unreal.ScopedSlowTask(len(files) * ROUNDS * len(CAUSE), "Test priciny (cache / priznak)...") as task:
        task.make_dialog(True)
        stop = False
        for r in range(ROUNDS):
            for vi, variant in enumerate(CAUSE):
                if stop: break
                unreal.log("TEST FORMATU ZACATEK %s %d" % (variant, r))
                folder = "%s/%s_%d" % (DST, variant, r); sfolder = "%s/%ssrc_%d" % (DST, variant, r)
                for f in files:
                    if task.should_cancel(): stop = True; break
                    n = f[:-4]; task.enter_progress_frame(1, "%s %d %s" % (variant, r, n))
                    if variant == "cache": p = os.path.join(src, f)             # puvodni soubor = puvodni klic cache
                    else:
                        p = os.path.join(tmpd, "%s_%d_%s" % (variant, r, f))
                        with open(os.path.join(src, f)) as fh: lines = fh.readlines()
                        with open(p, "w") as fh: fh.writelines(_variant(lines, "cisty", 0.0001 * (base + 2 * r + (vi % 2))))
                    t = unreal.AssetImportTask()
                    t.set_editor_property("filename", p); t.set_editor_property("destination_path", sfolder)
                    t.set_editor_property("destination_name", n)
                    t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True)
                    t.set_editor_property("save", False)
                    at.import_asset_tasks([t])
                    tp = "%s/%s.%s" % (sfolder, n, n)
                    if not eal.does_asset_exist(tp): skipped += 1; continue
                    tmp = unreal.load_asset(tp)
                    from_ = "%s/%s.%s" % (STONES, n, n) if variant == "priznak" else tp
                    if not eal.does_asset_exist(from_): skipped += 1; continue
                    try:
                        eal.duplicate_asset(from_, "%s/%s" % (folder, n))
                        sm = unreal.load_asset("%s/%s.%s" % (folder, n, n))
                        _as_build(unreal, sms, eal, tmp, sm)
                    except Exception as ex:
                        unreal.log_warning("TEST FORMATU: %s %s: %s" % (variant, n, ex)); skipped += 1; continue
                    h = _has_flag(unreal, "%s/%s" % (folder, n))
                    if h is not None:
                        flags[variant][0] += 1; flags[variant][1] += 1 if h else 0
    state["flags"] = flags; state["skipped"] = skipped
    json.dump(state, open(_state_path(), "w"))
    try: eal.delete_directory(DST)
    except Exception: pass
    unreal.log(MARK)
    report(unreal)


def report(unreal):
    try: st = json.load(open(_state_path()))
    except Exception:
        unreal.log_error("TEST FORMATU: neni ulozeny stav testu, spust nejdriv MODE = \"test\""); return
    try:
        with open(st["log"], "r", encoding="utf-8", errors="replace") as f:
            f.seek(st["start"]); text = f.read()
    except Exception as ex:
        unreal.log_error("TEST FORMATU: log %s nejde precist (%s)" % (st["log"], ex)); return
    if MARK not in text:
        unreal.log_warning("TEST FORMATU: log zatim neobsahuje konec testu - za chvili spust skript s MODE = \"report\" (log: %s)" % st["log"])
    nan = re.findall(r"found NaN in Bounds of '%s/(\w+?)_(\d+)/(\w+)\." % re.escape(DST), text)
    variants = st.get("variants", ("novy", "stary"))
    tang = dict((v, 0) for v in variants)                 # tangenty: podle useku logu mezi znackami ZACATEK
    parts = re.split(r"TEST FORMATU ZACATEK (%s) \d+" % "|".join(variants), text)
    for k in range(1, len(parts) - 1, 2):
        tang[parts[k]] += len(re.findall(r"has some nearly zero tangents", parts[k + 1]))
    total = st["files"] * st["rounds"]
    if st.get("cause"):                                   # test 3
        sec = dict((v, "") for v in variants)
        for k in range(1, len(parts) - 1, 2): sec[parts[k]] += parts[k + 1].split(MARK)[0]
        fl = st.get("flags", {})
        unreal.log_warning("TEST FORMATU: existujici kameny v %s s priznakem bDoFastBuild: %d z %d; preskoceno %d" % (
            STONES, st["orig"][0], st["orig"][1], st.get("skipped", 0)))
        for variant in variants:
            bad = sorted(set((r, n) for v, r, n in nan if v == variant))
            bsrc = sorted(set((r, n) for v, r, n in nan if v == variant + "src"))
            unreal.log_warning("TEST FORMATU: %-8s - NaN v bounds: cil %d z %d, docasny import %d; radny build %d, NaniteBuild %d, "
                               "'nearly zero tangents' %d; ulozene cile s priznakem %s%s" % (
                variant, len(bad), total, len(bsrc), len(re.findall(r"Display: Building static mesh", sec[variant])),
                len(re.findall(r"NaniteBuild", sec[variant])), tang[variant],
                "%d z %d" % (fl[variant][1], fl[variant][0]) if variant in fl else "?",
                (" (" + ", ".join("%s/kolo %s" % (n, r) for r, n in (bad + bsrc)[:12]) + ")") if bad or bsrc else ""))
        return
    for variant in variants:
        bad = sorted(set((r, n) for v, r, n in nan if v == variant))
        unreal.log_warning("TEST FORMATU: %-8s - meshu s NaN v bounds: %d z %d importu, 'nearly zero tangents': %d%s" % (
            variant, len(bad), total, tang[variant], (" (" + ", ".join("%s/kolo %s" % (n, r) for r, n in bad[:12]) + ")") if bad else ""))


def main():
    import unreal
    if MODE == "report": report(unreal)
    elif MODE == "pricina": run_cause(unreal)
    elif MODE not in ("formaty", "kroky"): unreal.log_error("TEST FORMATU: neznamy MODE %s" % MODE)
    else: run_test(unreal)


main()
