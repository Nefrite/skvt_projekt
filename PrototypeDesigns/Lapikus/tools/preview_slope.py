import numpy as np, sys
from PIL import Image, ImageDraw
OUT = sys.argv[1]; RES = 0.5
H = np.load(f"{OUT}/H.npy"); S = np.load(f"{OUT}/S.npy")
gy, gx = np.gradient(H, RES)
slope = np.degrees(np.arctan(np.hypot(gx, gy)))
# hillshade
az, alt = np.radians(315), np.radians(45)
asp = np.arctan2(-gx, gy)
sl = np.arctan(np.hypot(gx, gy))
hs = np.sin(alt) * np.cos(sl) + np.cos(alt) * np.sin(sl) * np.cos(az - asp)
hs = np.clip(hs, 0, 1)
# slope colours like mapy.cz
cols = np.array([[205, 228, 180], [233, 205, 170], [225, 160, 160], [205, 110, 140], [180, 50, 110]], float)
idx = np.digitize(slope, [8, 18, 28, 38])
rgb = cols[idx] * (0.55 + 0.45 * hs[..., None])
im = Image.fromarray(rgb.astype(np.uint8))
dr = ImageDraw.Draw(im)
pts = [tuple(p / RES) for p in S]
dr.line(pts, fill=(110, 160, 220), width=5)
# contours every 5 m
c = (np.floor(H / 5) != np.floor(np.roll(H, 1, 0) / 5)) | (np.floor(H / 5) != np.floor(np.roll(H, 1, 1) / 5))
a = np.array(im); a[c] = (a[c] * 0.6).astype(np.uint8)
im = Image.fromarray(a)
im.save(f"{OUT}/Zricenina_preview_full.png")
# crop to screenshot area
PXM = 184 / 36.0; OFF = np.array([162.0, 181.0])
x0, y0 = OFF / RES; x1, y1 = (OFF + np.array([917, 727]) / PXM) / RES
im.crop((int(x0), int(y0), int(x1), int(y1))).resize((917, 727)).save(f"{OUT}/Zricenina_preview_crop.png")
print(slope.max())
