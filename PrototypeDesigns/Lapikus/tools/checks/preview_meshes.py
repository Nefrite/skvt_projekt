"""preview_meshes.py - nahled knihovnich meshi (OBJ) bez Unrealu: mrizka meshi, kazdy ze dvou pohledu,
barva podle materialoveho slotu (usemtl: Wood, EndGrain, Bark, Daub, Wattle, Rope, Canvas), odvracene plochy se nekresli (otocene normaly = diry).

    python tools/checks/preview_meshes.py <slozka s OBJ nebo meshes/> <out.png> [prefix ...]

Potrebuje numpy a Pillow. Slot: Wood svetle hnede, EndGrain okrove, Bark tmave hnede, bez slotu sede.
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw

SLOT_COL = {"Wood": (205, 170, 120), "EndGrain": (230, 190, 110), "Bark": (95, 70, 50), "Daub": (185, 155, 115),
            "Wattle": (105, 80, 50), "Rope": (215, 195, 145), "Canvas": (225, 220, 200), None: (170, 170, 170)}


def load_obj(path):
    V, F, S = [], [], []; cur = None
    for ln in open(path):
        if ln.startswith("v "): x, y, z = map(float, ln.split()[1:4]); V.append((x, -z, y))      # OBJ Y-up -> UE Z-up
        elif ln.startswith("usemtl"): cur = ln.split()[1]
        elif ln.startswith("f "): F.append([int(t.split("/")[0]) - 1 for t in ln.split()[1:4]]); S.append(cur)
    return np.array(V), np.array(F), S


def render(V, F, S, yaw, pitch, size):
    cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
    Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]]); Rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    Q = (V - (V.max(0) + V.min(0)) / 2) @ (Rx @ Rz).T       # pohled podel +Y (do obrazovky), Z nahoru
    sc = 0.9 * size / max(np.ptp(Q[:, 0]), np.ptp(Q[:, 2]), 1e-6)
    img = Image.new("RGB", (size, size), (245, 245, 240)); dr = ImageDraw.Draw(img)
    A, B, C = Q[F[:, 0]], Q[F[:, 1]], Q[F[:, 2]]
    n = np.cross(B - A, C - A); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    vis = n[:, 1] < 0                                       # cela k divakovi (divak v -Y)
    L = np.array([-0.4, -0.7, 0.6]); L /= np.linalg.norm(L)
    sh = 0.3 + 0.7 * np.clip(n @ L, 0, 1)
    order = np.argsort(-((A + B + C)[:, 1]))
    for k in order:
        if not vis[k]: continue
        col = SLOT_COL.get(S[k], SLOT_COL[None]); c = tuple(int(v * sh[k]) for v in col)
        pts = [(size / 2 + p[0] * sc, size / 2 - p[2] * sc) for p in (A[k], B[k], C[k])]
        dr.polygon(pts, fill=c)
    return img


def main(src, out, prefixes):
    files = []
    for root, _, fs in os.walk(src):
        files += [os.path.join(root, f) for f in fs if f.endswith(".obj") and (not prefixes or any(f.startswith(p) for p in prefixes))]
    files.sort(key=os.path.basename)
    cell = 260; cols = 4
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell * 2, rows * (cell + 18)), (255, 255, 255)); dr = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        V, F, S = load_obj(f)
        x0 = (i % cols) * cell * 2; y0 = (i // cols) * (cell + 18)
        sheet.paste(render(V, F, S, math.radians(-35), math.radians(25), cell), (x0, y0 + 18))
        sheet.paste(render(V, F, S, math.radians(145), math.radians(-20), cell), (x0 + cell, y0 + 18))
        dr.text((x0 + 4, y0 + 3), os.path.basename(f)[:-4], fill=(0, 0, 0))
    sheet.save(out); print("nahled:", out, len(files), "meshi")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
