"""
Rozmisti olse lepkave (a volitelne vrby jivy na jesepu) podel reky (body z Zricenina_olse.csv, vygenerovane podle tvaru koryta).

Pouziti v Unreal Editoru:
  1) Do ALDER_MESHES vloz cesty k meshum olse (Content Browser -> pravym na mesh -> Copy Reference),
     idealne 2-4 varianty. Lze dat i Blueprint stromu.
  2) Tools -> Execute Python Script -> tento soubor. Nic neni treba vybirat.
  Opakovane spusteni nejdriv smaze olse z predchoziho behu (actory s tagem ALDER_TAG).
  Akce jde vratit pres Ctrl+Z.
"""
import random
import unreal

ALDER_MESHES = [
    # "/Game/Megaplants/BlackAlder/SM_BlackAlder_01.SM_BlackAlder_01",
]
# Volitelne: vrba jiva (Goat Willow) na jesepu - cast stromu na vnitrnim brehu bude vrba misto olse
WILLOW_MESHES = [
    # "/Game/Megaplants/GoatWillow/....",
]
WILLOW_SHARE = 0.35   # podil vrb mezi stromy na jesepu

ALDER_TAG = "Zricenina_Alder"
FOLDER = "Forest/Alders"
SEED = 21

# X, Y, Z (cm), Yaw, Lean (st, naklon nad vodu), DirX, DirY (smer k vode), Scale, Vysep (1 = vysepny breh, 0 = jesep)
ALDERS = [
    (-2100, -7650, 317, 95, 6.0, 0.015, 1.000, 0.93, 1),
    (-3450, 8550, 431, 7, 1.1, -0.552, 0.834, 0.91, 0),
    (-6800, -7450, 353, 18, 9.3, 0.370, 0.929, 1.14, 1),
    (-10050, -3400, 385, 319, 0.3, -0.993, 0.120, 0.69, 0),
    (-800, 10300, 431, 278, 1.9, -0.296, 0.955, 0.63, 0),
    (-5450, 4500, 410, 349, 5.6, -0.989, 0.146, 1.03, 1),
    (-2000, 9500, 439, 337, 1.9, -0.481, 0.877, 0.76, 0),
    (-6700, 1100, 383, 134, 9.9, -0.727, 0.686, 1.05, 1),
    (3200, 12200, 460, 285, 3.5, -0.491, 0.871, 0.71, 0),
    (-2950, 10200, 423, 3, 6.7, 0.471, -0.882, 1.06, 1),
    (6100, -9050, 294, 11, 1.1, -0.172, -0.985, 0.67, 0),
    (6700, -8900, 296, 16, 2.9, -0.036, -0.999, 0.60, 0),
    (1750, -7250, 355, 82, 5.8, -0.381, -0.925, 1.03, 1),
    (2150, 11700, 452, 50, 9.0, -0.630, 0.777, 1.06, 1),
    (-9300, -3100, 392, 61, 3.9, -0.946, 0.323, 0.82, 0),
    (-4950, 6200, 418, 52, 3.6, -0.972, 0.237, 0.83, 0),
    (-2750, -7800, 326, 258, 8.0, 0.108, 0.994, 1.05, 1),
    (-9800, -4200, 382, 306, 0.8, -0.988, -0.155, 0.68, 0),
    (1500, 11400, 443, 121, 9.2, -0.529, 0.849, 1.11, 1),
    (-9200, -1850, 387, 50, 1.5, -0.711, 0.704, 0.71, 0),
    (-4300, 7800, 440, 229, 0.8, -0.931, 0.366, 0.92, 0),
    (-5450, 3750, 414, 262, 8.0, -0.992, 0.128, 1.09, 1),
    (-9650, -3350, 387, 165, 2.4, -0.985, 0.174, 0.69, 0),
    (-8450, 800, 375, 251, 2.3, 0.750, -0.662, 0.77, 0),
    (-5500, -7800, 358, 83, 7.0, 0.103, 0.995, 1.07, 1),
    (-4100, 8150, 436, 335, 0.7, -0.829, 0.559, 0.83, 0),
    (-5050, 5350, 416, 151, 3.1, -0.972, 0.236, 0.87, 0),
    (-7650, 0, 379, 239, 9.1, -0.786, 0.619, 0.85, 1),
    (1500, -8300, 342, 137, 1.8, 0.431, 0.902, 0.93, 0),
    (-600, -6800, 336, 182, 8.7, 0.001, -1.000, 0.87, 1),
    (6650, -10000, 294, 323, 9.8, 0.057, 0.998, 1.12, 1),
    (7050, -9900, 284, 196, 8.8, 0.074, 0.997, 1.08, 1),
    (-4750, -7650, 351, 104, 9.1, 0.019, 1.000, 1.07, 1),
    (-8300, -550, 379, 53, 5.9, -0.725, 0.689, 1.11, 1),
    (-6200, -7500, 353, 325, 8.1, 0.304, 0.953, 0.93, 1),
    (11550, -10700, 288, 154, 0.5, 0.233, 0.972, 0.94, 0),
    (-1550, 9700, 433, 3, 3.2, -0.471, 0.882, 0.85, 0),
    (-3150, -7600, 330, 312, 7.7, 0.019, 1.000, 1.17, 1),
    (-1150, 9950, 431, 269, 3.5, -0.435, 0.900, 0.90, 0),
    (3050, -7900, 327, 39, 9.1, -0.246, -0.969, 0.92, 1),
    (-9200, 450, 398, 158, 2.0, 0.756, -0.654, 0.69, 0),
]

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
def _load(paths):
    out = [unreal.load_asset(p.split("'")[1] if "'" in p else p) for p in paths]
    return [m for m in out if m]
meshes = _load(ALDER_MESHES)
willows = _load(WILLOW_MESHES)
if not meshes:
    unreal.log_error("Dopln do ALDER_MESHES cestu k meshi olse (Copy Reference) a spust znovu.")
else:
    rnd = random.Random(SEED)
    with unreal.ScopedEditorTransaction("Place alders"):
        old = [a for a in eas.get_all_level_actors() if unreal.Name(ALDER_TAG) in a.tags]
        for a in old:
            eas.destroy_actor(a)
        for i, (x, y, z, yaw, lean, dx, dy, s, outer) in enumerate(ALDERS):
            spin = unreal.Rotator(roll=0.0, pitch=0.0, yaw=yaw)
            axis = unreal.Vector(-dy, dx, 0.0)
            tilt = unreal.MathLibrary.rotator_from_axis_and_angle(axis, lean)
            rot = unreal.MathLibrary.compose_rotators(spin, tilt)
            # kontrola smeru naklonu (UE ma levotocivy system) - koruna ma smerovat k vode
            up = unreal.MathLibrary.get_up_vector(rot)
            if up.x * dx + up.y * dy < 0:
                tilt = unreal.MathLibrary.rotator_from_axis_and_angle(axis, -lean)
                rot = unreal.MathLibrary.compose_rotators(spin, tilt)
            is_willow = bool(willows) and not outer and rnd.random() < WILLOW_SHARE
            mesh = rnd.choice(willows if is_willow else meshes)
            actor = eas.spawn_actor_from_object(mesh, unreal.Vector(x, y, z), rot)
            if not actor:
                continue
            actor.set_actor_scale3d(unreal.Vector(s, s, s))
            actor.tags = list(actor.tags) + [unreal.Name(ALDER_TAG)]
            actor.set_folder_path(FOLDER)
            actor.set_actor_label(("Willow_%02d" if is_willow else "Alder_%02d") % (i + 1))
    unreal.log("Olse: smazano %d, vlozeno %d (slozka %s)" % (len(old), len(ALDERS), FOLDER))
