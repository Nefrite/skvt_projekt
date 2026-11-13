"""kamen / dilec (Stone), prirazeni meshi podle pomeru stran, hmotnost"""
import math, zlib
from .config import ASHLAR_MESH, DRESSED_FRAMES, STONE_PHYSICS, STONE_RATIOS, STONE_VARIANTS, USE_STONE_MESHES, WOOD_MESHES, WOOD_MI


class Stone:
    __slots__ = ("id", "cat", "x", "y", "z", "yaw", "pitch", "roll", "sx", "sy", "sz", "seg", "span", "mesh", "rough", "loose")
    def __init__(self, sid, cat, x, y, z, yaw, sx, sy, sz, pitch=0.0, roll=0.0, seg=0):
        self.span = None; self.mesh = None
        self.rough = False   # odkryte jadro: lomovy kamen (mesh) misto kostky
        self.loose = False   # 05: samostatny actor misto instance (napr. prah, da se rucne posunout a ulozit pres capture)
        self.seg = seg   # usek zdi (index rovneho useku mezi zlomy)
        self.id = sid; self.cat = cat; self.x = x; self.y = y; self.z = z; self.yaw = yaw
        self.sx = sx; self.sy = sy; self.sz = sz; self.pitch = pitch; self.roll = roll

def in_box(s, box):
    return box[0] <= s.x <= box[3] and box[1] <= s.y <= box[4] and box[2] <= s.z <= box[5]

def stone_mesh_name(st):
    """Varianta zaobleneho kamene podle pomeru delka/vyska bloku (deterministicky podle id)."""
    if not USE_STONE_MESHES: return None
    if st.cat in WOOD_MI:
        if not WOOD_MESHES: return None
        v = "ABC"[zlib.crc32(st.id.encode()) % 3]
        if st.sz > 1.5 * max(st.sx, st.sy): return "SM_RuinPost_" + v          # sloup (delka nahoru)
        if st.sz < 0.45 * st.sy: return "SM_RuinPlank_" + v                     # prkno, fosna schodu
        return "SM_RuinTimber_" + v
    if st.cat == "floor" or (st.cat == "frame" and not DRESSED_FRAMES): return ASHLAR_MESH
    if st.cat == "frame":
        r = max(st.sx, 1) / max(st.sz, 1)
        best = min(STONE_RATIOS, key=lambda q: abs(math.log(r / q)))
        return "SM_RuinDressed_R%02d_%s" % (round(best * 10), "AB"[zlib.crc32(st.id.encode()) % 2])
    if st.cat not in ("face", "crown") and not (st.cat == "core" and st.rough): return None
    r = max(st.sx, 1) / max(st.sz, 1)
    best = min(STONE_RATIOS, key=lambda q: abs(math.log(r / q)))
    v = STONE_VARIANTS[zlib.crc32(st.id.encode()) % len(STONE_VARIANTS)]
    return "SM_RuinStone_%sR%02d_%s" % ("W_" if st.cat == "crown" else "", round(best * 10), v)

def assign_meshes(stones):
    for st in stones:
        st.mesh = stone_mesh_name(st)
        if st.mesh and st.cat in ("face", "crown", "core") and (zlib.crc32(st.id.encode()) >> 8) & 1:
            st.yaw += 180.0          # otoceni kamene o 180 st. = dalsi varianta vzhledu (rozmer sedi)

def stone_mass_kg(s):
    return s.sx * s.sy * s.sz / 1e6 * STONE_PHYSICS["fill"] * STONE_PHYSICS["density"]
