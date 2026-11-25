"""build_sequence.py - postavi v editoru Level Sequence promo pruletu z dat promo_prulet.json (jediny zdroj hodnot).
entities: Cinematics_Lapikus
docs: navrh_promo_prulet_kamery, stav_promo_prulet
build_step: cinematics
domains: narrative
Unreal: nejdriv 05_constructions/stavby/Etapa.py s ETAPA = 2, pak Tools -> Execute Python Script -> cinematics/build_sequence.py
Vytvori /Game/Skvt/Cinematics/LS_Promo_Prulet (= /Content/Skvt/Cinematics/): CineCamera na zaber, rigy (CameraRig_Rail, CameraRig_Crane,
pivot Promo_Pivot_Vez), cile ostreni, Camera Cuts a klice ohniska, clony, pohybu a ostreni z dat.
Opakovany beh smaze sekvenci a actory s tagem z dat (sequence.tag) a postavi je znovu: rucni upravy v sekvenci, ktere nejsou v JSON, se ztrati
-> rucni ladeni nejdriv prepis do promo_prulet.json. Nic nemeni na staveb ani zricenine."""
SEQ_JSON = None               # None = promo_prulet.json vedle skriptu; jinak uplna cesta
REBUILD = True                # True = smazat predchozi sekvenci a actory s tagem a postavit znovu

import json, math, os

# ---------------------------------------------------------------- cista matematika (bez unreal)

def ease_fn(name):
    """Easing na s v <0,1>: linear, smooth (smoothstep), out (zpomaleni na konci), in."""
    if name == "smooth": return lambda s: s * s * (3.0 - 2.0 * s)
    if name == "out": return lambda s: 1.0 - (1.0 - s) ** 2
    if name == "in": return lambda s: s * s
    return lambda s: s

def sample(wps, u, ease="linear"):
    """wps = [[u0, v...], [u1, v...], ...] vzestupne v u; vraci seznam hodnot v case u (easing po segmentech)."""
    f = ease_fn(ease)
    if u <= wps[0][0]: return list(wps[0][1:])
    if u >= wps[-1][0]: return list(wps[-1][1:])
    for a, b in zip(wps, wps[1:]):
        if a[0] <= u <= b[0]:
            s = 0.0 if b[0] == a[0] else (u - a[0]) / (b[0] - a[0])
            s = f(s)
            return [a[i] + (b[i] - a[i]) * s for i in range(1, len(a))]
    return list(wps[-1][1:])

def move_u(shot, t):
    """Normalizovany postup zaberu v case t (s); hold_end_s drzi konec bez pohybu."""
    dur = shot["t1"] - shot["t0"] - shot.get("hold_end_s", 0.0)
    return max(0.0, min(1.0, (t - shot["t0"]) / dur)) if dur > 0 else 1.0

def look_rot(cam, tgt):
    """(roll, pitch, yaw) ve stupnich, kamera z bodu cam miri na bod tgt."""
    dx, dy, dz = tgt[0] - cam[0], tgt[1] - cam[1], tgt[2] - cam[2]
    return 0.0, math.degrees(math.atan2(dz, math.hypot(dx, dy))), math.degrees(math.atan2(dy, dx))

def unwrap(vals):
    """Uhly bez skoku o 360 st. mezi vzorky."""
    out = []
    for v in vals:
        if out:
            while v - out[-1] > 180.0: v -= 360.0
            while v - out[-1] < -180.0: v += 360.0
        out.append(v)
    return out

def sample_times(shot, step):
    """Casy klicu zaberu (s): po kroku step, vzdy start, konec pohybu a konec zaberu."""
    t0, t1 = shot["t0"], shot["t1"]
    tm = t1 - shot.get("hold_end_s", 0.0)
    ts, t = [], t0
    while t < tm - 1e-6:
        ts.append(round(t, 4)); t += step
    ts.append(round(tm, 4))
    if t1 - tm > 1e-6: ts.append(round(t1, 4))
    return ts

def build_focal(shot, ts, cam_at):
    """Ohnisko (mm) v casech ts. cam_at(t) = poloha kamery (x, y, z) v case t. Vertigo (zoom_law): oblouk drzi velikost v obraze,
    f ~ vzdalenost kamery od oblouku, dolem omezeno f_min (po dosazeni f_min se drzi)."""
    zl = shot.get("zoom_law")
    if zl and zl["law"] == "vertigo":
        ax = {"x": 0, "y": 1, "z": 2}[zl["ref_axis"]]
        d0 = abs(cam_at(ts[0])[ax] - zl["ref_value"])
        return [max(zl["f_min"], zl["f_start"] * abs(cam_at(t)[ax] - zl["ref_value"]) / d0) for t in ts]
    e = "smooth" if len(shot["focal_mm"]) > 2 else shot.get("ease", "linear")
    return [sample(shot["focal_mm"], move_u(shot, t), e)[0] for t in ts]

def free_track(shot, ts):
    """Zaber s volnou kamerou: seznam (t, (x,y,z), (roll,pitch,yaw))."""
    out = []
    for t in ts:
        u = move_u(shot, t)
        p = sample(shot["pos"], u, shot["ease"]); l = sample(shot["look"], u, shot["ease"])
        out.append((t, tuple(p), look_rot(p, l)))
    yaws = unwrap([o[2][2] for o in out])
    return [(o[0], o[1], (o[2][0], o[2][1], y)) for o, y in zip(out, yaws)]

def orbit_track(shot, ts, refs):
    """Oblet: seznam (t, pivot_xyz, pivot_yaw, kamera_rel_pitch, kamera_svetova_poloha)."""
    pv = shot["pivot"]; R = pv["radius_cm"]
    cx, cy = refs[pv["center_xy"]] if isinstance(pv["center_xy"], str) else pv["center_xy"]
    out = []
    for t in ts:
        u = move_u(shot, t)
        a = math.radians(pv["az_start_deg"] + pv["sweep_deg"] * ease_fn(shot["ease"])(u))
        z = sample(pv["z"], u, shot["ease"])[0]; lz = sample(pv["look_z"], u, shot["ease"])[0]
        psi = math.degrees(a) - 180.0                      # offset (-R,0) otoceny o psi lezi v uhlu psi+180
        pitch = math.degrees(math.atan2(lz - z, R))
        cam = (cx + R * math.cos(a), cy + R * math.sin(a), z)
        out.append((t, (cx, cy, z), psi, pitch, cam))
    yaws = unwrap([o[2] for o in out])
    return [(o[0], o[1], y, o[3], o[4]) for o, y in zip(out, yaws)]

def crane_track(shot, ts):
    """Jerab: seznam (t, rig_xyz, crane_pitch_deg, kamera_poloha, rot). Kamera = rig + (L cos p, 0, L sin p) otocene o yaw."""
    c = shot["crane"]; L = c["arm_cm"]; yaw = math.radians(c["yaw_deg"]); bz = c["base_z"]
    out = []
    for t in ts:
        u = move_u(shot, t)
        p = sample(shot["pos"], u, shot["ease"]); l = sample(shot["look"], u, shot["ease"])
        s = max(-1.0, min(1.0, (p[2] - bz) / L)); pr = math.asin(s)
        reach = L * math.cos(pr)
        rig = (p[0] - reach * math.cos(yaw), p[1] - reach * math.sin(yaw), bz)
        out.append((t, rig, math.degrees(pr), tuple(p), look_rot(p, l)))
    yaws = unwrap([o[4][2] for o in out])
    return [(o[0], o[1], o[2], o[3], (o[4][0], o[4][1], y)) for o, y in zip(out, yaws)]

def rail_track(shot, ts):
    """Kolejnice: seznam (t, pozice 0..1, kamera_poloha)."""
    a, b = shot["rail"]
    out = []
    for t in ts:
        p = ease_fn(shot["ease"])(move_u(shot, t))
        out.append((t, p, tuple(a[i] + (b[i] - a[i]) * p for i in range(3))))
    return out

# ---------------------------------------------------------------- Unreal
def main():
    import unreal
    here = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(SEQ_JSON or os.path.join(here, "promo_prulet.json"), encoding="utf-8"))
    cfg, refs = data["sequence"], data["refs"]
    fps, step, tag = cfg["fps"], cfg["key_step_s"], cfg["tag"]
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    V = lambda p: unreal.Vector(float(p[0]), float(p[1]), float(p[2]))
    R = lambda r: unreal.Rotator(float(r[0]), float(r[1]), float(r[2]))     # (roll, pitch, yaw)
    fr = lambda t: unreal.FrameNumber(int(round(t * fps)))

    # --- uklid
    if REBUILD:
        for a in eas.get_all_level_actors():
            if tag in [str(t) for t in a.tags]: eas.destroy_actor(a)
        path = cfg["folder"] + "/" + cfg["name"]
        if unreal.EditorAssetLibrary.does_asset_exist(path): unreal.EditorAssetLibrary.delete_asset(path)
    seq = unreal.AssetToolsHelpers.get_asset_tools().create_asset(cfg["name"], cfg["folder"], unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
    seq.set_display_rate(unreal.FrameRate(fps, 1))
    seq.set_playback_start_seconds(0.0); seq.set_playback_end_seconds(cfg["length_s"])

    def spawn(cls, name, loc=(0, 0, 0), rot=(0, 0, 0)):
        a = eas.spawn_actor_from_class(cls, V(loc), R(rot))
        a.set_actor_label(name); a.tags = [tag]
        return a

    def set_range(sec, t0, t1):
        try: sec.set_range_seconds(t0, t1)
        except Exception: sec.set_range(int(t0 * fps), int(t1 * fps))

    def float_track(binding, prop, keys):
        """keys = [(t, hodnota)] -> linearni klice na vlastnosti prop (nazev vlastnosti objektu v bindingu)."""
        tr = binding.add_track(unreal.MovieSceneFloatTrack)
        tr.set_property_name_and_path(prop, prop)
        sec = tr.add_section(); set_range(sec, keys[0][0], keys[-1][0])
        ch = sec.get_channels()[0]
        for t, v in keys: ch.add_key(fr(t), float(v), 0.0, unreal.SequenceTimeUnit.DISPLAY_RATE, unreal.MovieSceneKeyInterpolation.LINEAR)

    def transform_track(binding, rows):
        """rows = [(t, (x,y,z), (roll,pitch,yaw))] -> klice transformace (u pripojeneho actoru relativni)."""
        tr = binding.add_track(unreal.MovieScene3DTransformTrack)
        sec = tr.add_section(); set_range(sec, rows[0][0], rows[-1][0])
        chs = sec.get_channels()                              # lx ly lz rx(roll) ry(pitch) rz(yaw) sx sy sz
        for t, p, r in rows:
            for i, v in enumerate(list(p) + list(r)):
                chs[i].add_key(fr(t), float(v), 0.0, unreal.SequenceTimeUnit.DISPLAY_RATE, unreal.MovieSceneKeyInterpolation.LINEAR)

    def make_camera(shot, loc=(0, 0, 0), rot=(0, 0, 0)):
        cam = spawn(unreal.CineCameraActor, "Promo_Cam_%02d" % shot["id"], loc, rot)
        comp = cam.get_cine_camera_component()
        comp.set_editor_property("filmback", unreal.CameraFilmbackSettings(sensor_width=cfg["filmback_mm"][0], sensor_height=cfg["filmback_mm"][1]))
        comp.set_editor_property("current_aperture", float(shot["aperture"]))
        comp.set_editor_property("current_focal_length", float(shot["focal_mm"][0][1]))
        fs = comp.get_editor_property("focus_settings")
        fc = shot["focus"]
        if fc["mode"] == "track":
            tgt = spawn(unreal.TargetPoint, "Promo_Fokus_%s" % fc["target"], fc["target_pos"])
            fs.focus_method = unreal.CameraFocusMethod.TRACKING
            ts_ = fs.tracking_focus_settings; ts_.actor_to_track = tgt; fs.tracking_focus_settings = ts_
        else:
            fs.focus_method = unreal.CameraFocusMethod.MANUAL
            fs.manual_focus_distance = float(fc["distance_cm"])
        comp.set_editor_property("focus_settings", fs)
        return cam, comp

    cut_track = seq.add_track(unreal.MovieSceneCameraCutTrack)
    for shot in data["shots"]:
        try:
            ts = sample_times(shot, step)
            rig = shot["rig"]
            if rig == "free":
                rows = free_track(shot, ts)
                cam, comp = make_camera(shot, rows[0][1], rows[0][2])
                b = seq.add_possessable(cam); transform_track(b, [(r[0], r[1], r[2]) for r in rows])
                cam_at = lambda t, rows=rows: min(rows, key=lambda r: abs(r[0] - t))[1]
            elif rig == "rail":
                rows = rail_track(shot, ts)
                railactor = spawn(unreal.CameraRig_Rail, "Promo_Rail_%02d" % shot["id"])
                sp = railactor.get_editor_property("rail_spline_component")
                sp.clear_spline_points()
                for i, p in enumerate(shot["rail"]): sp.add_spline_point(V(p), unreal.SplineCoordinateSpace.WORLD)
                for i in range(len(shot["rail"])): sp.set_spline_point_type(i, unreal.SplinePointType.LINEAR)
                railactor.set_editor_property("lock_orientation_to_rail", False)
                cam, comp = make_camera(shot)
                cam.attach_to_actor(railactor, "", unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.KEEP_WORLD, False)
                cam.root_component.set_relative_rotation(R(shot["cam_rel_rot"]), False, False)
                bro = seq.add_possessable(railactor)
                float_track(bro, "CurrentPositionOnRail", [(r[0], r[1]) for r in rows])
                b = seq.add_possessable(cam)
                cam_at = lambda t, rows=rows: min(rows, key=lambda r: abs(r[0] - t))[2]
            elif rig == "pivot":
                rows = orbit_track(shot, ts, refs); pv = shot["pivot"]
                piv = spawn(unreal.TargetPoint, pv["name"], rows[0][1])
                cam, comp = make_camera(shot)
                cam.attach_to_actor(piv, "", unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.KEEP_WORLD, False)
                bp = seq.add_possessable(piv)
                transform_track(bp, [(r[0], r[1], (0.0, 0.0, r[2])) for r in rows])
                b = seq.add_possessable(cam)
                transform_track(b, [(r[0], (-pv["radius_cm"], 0.0, 0.0), (0.0, r[3], 0.0)) for r in rows])
                cam_at = lambda t, rows=rows: min(rows, key=lambda r: abs(r[0] - t))[4]
            elif rig == "crane":
                rows = crane_track(shot, ts); c = shot["crane"]
                cr = spawn(unreal.CameraRig_Crane, "Promo_Crane_%02d" % shot["id"], rows[0][1], (0, 0, c["yaw_deg"]))
                for prop, val in (("crane_arm_length", c["arm_cm"]), ("lock_mount_pitch", True), ("lock_mount_yaw", True)):
                    try: cr.set_editor_property(prop, val)
                    except Exception as e: unreal.log_warning("Promo %s: vlastnost %s nenastavena: %s" % (shot["id"], prop, e))
                cam, comp = make_camera(shot)
                cam.attach_to_actor(cr, "", unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.KEEP_WORLD, False)
                bc = seq.add_possessable(cr)
                transform_track(bc, [(r[0], r[1], (0.0, 0.0, c["yaw_deg"])) for r in rows])
                float_track(bc, "CranePitch", [(r[0], r[2]) for r in rows])
                b = seq.add_possessable(cam)
                transform_track(b, [(r[0], (0.0, 0.0, 0.0), r[4]) for r in rows])
                cam_at = lambda t, rows=rows: min(rows, key=lambda r: abs(r[0] - t))[3]
            else:
                raise ValueError("neznamy rig " + rig)
            # ohnisko (a clona) na komponente kamery
            bcomp = seq.add_possessable(comp)
            float_track(bcomp, "CurrentFocalLength", list(zip(ts, build_focal(shot, ts, cam_at))))
            float_track(bcomp, "CurrentAperture", [(ts[0], shot["aperture"]), (ts[-1], shot["aperture"])])
            # Camera Cut
            sec = cut_track.add_section(); set_range(sec, shot["t0"], shot["t1"])
            try: bid = unreal.MovieSceneSequenceExtensions.make_binding_id(seq, b, unreal.MovieSceneObjectBindingSpace.LOCAL)
            except Exception: bid = b.get_binding_id()
            sec.set_camera_binding_id(bid)
            unreal.log("Promo zaber %d (%s): hotovo, %d klicu" % (shot["id"], rig, len(ts)))
        except Exception as e:
            unreal.log_error("Promo zaber %s selhal: %s" % (shot.get("id"), e))
    unreal.EditorAssetLibrary.save_loaded_asset(seq)
    unreal.log("LS_Promo_Prulet postavena (%d zaberu). Dalsi krok: otevrit v Sequenceru, zkontrolovat kamery ve viewportu." % len(data["shots"]))

try:
    import unreal  # noqa
except ImportError:
    unreal = None  # mimo editor se nic nestavi (jen import pro test matematiky)
if unreal is not None:
    main()
