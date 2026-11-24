"""gen_moat.py - uprava vyskopisu 505x505 px (01_terrain) a mrizky terrain_from_level.json (03_ruin) pro sijovy prikop,
celni terenni valy, pristupovy uvoz a severni unikovou rampu pred vychodni branou (navrh_brana_prikop.md).

Postup:
  1. V oblasti hradu a strazni veze (u <= 9..13 m) nahradi stary prikop z 1_gen_heightmap_1009.py (t_rel = 37 m)
     skutecnymi vyskami z terrain_from_level.json, takze zadna stavajici zed nezmeni patu (dZ = 0 cm).
  2. Pristupovy uvoz v ose 1. brany (d = 3.10 m, sirka dna ~3.2 m, predmosti Z = 3040 cm, sklon 14.9 st. k ceste) zarizly
     do rosteho terenu; celni valy se nedelaji (utocnici by se dostali na uroven hradeb).
  3. Tesne pred vnejsim licem Brana_V (u_in = 8.10 m) a s bermou pred Hradba_V (u_in = 7.00 m) vyhloubi ve skale
     sijovy prikop (horni sirka 8.20 m, ploche dno sirky 3.80 m na Z = 2700 cm, skalni steny 54-65 st. > 44 st.).
  4. Na severnim konci prikopu (od u = 12.2, d = -1.0, Z = 2700 cm smerem k u = 16.5, d = -5.5) vyrizne v kontraskarpe
     unikovou rampu (sirka ~2.0 m, podelny sklon 25.1 st. < 44 st.), ktera plynule vyusti na severni svah sije.
  5. Ulozi Zricenina_heightmap_505_50cm.png, Zricenina_preview_orez.png a rozsireny terrain_from_level.json (x1 = 4400).

Pouziti:
  python tools/terrain/gen_moat.py [01_terrain/Zricenina_heightmap_505_50cm.png] [03_ruin/blocks/terrain_from_level.json]

entities: [Brana, Strazni_Vez, Hradby_a_Brana, Lapikus_Region]
docs: [navrh_brana_prikop, stav_brana, 01_terrain]
build_step: 01_terrain
domains: [structures, environment]"""
import json, math, os, sys
import numpy as np
from PIL import Image
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import gaussian_filter

N = 505
RES = 0.5
ZMAX = 64.0

# Ram brany (shodny s tools/ruin/brana_spec.py -> frame): pocatek GT_NW, u podel Brana_S k VSV, d kolmo k JJV
GT_NW = (1930.0, -3107.0)
GT_NE = (2633.0, -3264.0)
_L = math.hypot(GT_NE[0] - GT_NW[0], GT_NE[1] - GT_NW[1])
UX, UY = (GT_NE[0] - GT_NW[0]) / _L, (GT_NE[1] - GT_NW[1]) / _L
DX, DY = -UY, UX                                                     # smer k jihu (Brana_J: GT_NW -> [2090, -2393])


def ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def slope_rgb(H):
    """stejna barevna stupnice sklonu jako v tools/2_derive_505.py -> Zricenina_preview_orez.png"""
    gy, gx = np.gradient(H, RES)
    sl = np.degrees(np.arctan(np.hypot(gx, gy)))
    asp = np.arctan2(-gx, gy)
    s = np.arctan(np.hypot(gx, gy))
    hs = np.clip(np.sin(np.radians(45)) * np.cos(s) + np.cos(np.radians(45)) * np.sin(s) * np.cos(np.radians(315) - asp), 0.0, 1.0)
    cols = np.array([[205, 228, 180], [233, 205, 170], [225, 160, 160], [205, 110, 140], [180, 50, 110]], float)
    return cols[np.digitize(sl, [8, 18, 28, 38])] * (0.55 + 0.45 * hs[..., None])


def world_to_ud(X, Y):
    """prevod svetovych souradnic (UE cm) do ramu brany (u, d) v metrech"""
    rx = X - GT_NW[0]
    ry = Y - GT_NW[1]
    return (rx * UX + ry * UY) / 100.0, (rx * DX + ry * DY) / 100.0


def apply_gate_moat(H_505, terr_level=None):
    """upravi pole vysek H_505 (505x505, v metrech) podle navrh_brana_prikop.md -> H_new (m)"""
    py, px = np.mgrid[0:N, 0:N]
    X = (px - 252) * 50.0
    Y = (py - 252) * 50.0
    u, d = world_to_ud(X, Y)
    H_base = H_505.astype(float).copy()

    # 1. Zasypani stareho prikopu (t_rel = 37 m) pod strazni vezi prevzetim vysek z terrain_from_level.json
    if terr_level is not None:
        nx_orig = min(terr_level["nx"], int(round((3600 - terr_level["x0"]) / terr_level["step"])) + 1)
        xs_tl = np.arange(terr_level["x0"], terr_level["x0"] + nx_orig * terr_level["step"], terr_level["step"], dtype=float)
        ys_tl = np.arange(terr_level["y0"], terr_level["y0"] + terr_level["ny"] * terr_level["step"], terr_level["step"], dtype=float)
        z_arr = np.array([row[:nx_orig] for row in terr_level["z"]], dtype=float) / 100.0
        itp = RegularGridInterpolator((ys_tl, xs_tl), z_arr, bounds_error=False, fill_value=None)
        ztl = gaussian_filter(itp(np.stack([np.clip(Y, ys_tl[0], ys_tl[-1]), np.clip(X, xs_tl[0], xs_tl[-1])], -1)), 0.8)
        w_box = ss(-5200.0, -5000.0, X) * (1.0 - ss(3400.0, 3600.0, X)) * ss(-3800.0, -3550.0, Y) * (1.0 - ss(200.0, 400.0, Y))
        w_fill = w_box * ss(1600.0, 1850.0, X) * (1.0 - ss(9.0, 13.0, u))
        H_base = H_base * (1.0 - w_fill) + ztl * w_fill

    # 2. Pristupovy uvoz na siji (pred vykopem prikopu, aby uvoz nezvedal hranu kontraskarpy).
    #    Celni terenni valy se NEDELAJI (Jirka 24. 11. 2026): val by utocnikum davel vyskovou vyhodu az na uroven hradeb.
    u_in = 8.10 - 1.10 * ss(6.5, 11.5, d)
    H = H_base.copy()

    w_cut_path = (1.0 - ss(1.45, 2.40, np.abs(d - 3.10))) * ss(13.5, 14.2, u) * (1.0 - ss(22.5, 25.0, u))
    z_path = 30.40 + 2.10 * np.clip((u - 16.55) / 7.95, 0.0, 1.0)
    H = H * (1.0 - w_cut_path) + z_path * w_cut_path

    # 3. Sijovy prikop (u_in .. u_in + 8.20 m; v pasu mostu posun vnejsi hrany o +0.22 m na 16.52 m, aby landscape neprolizal prkny)
    m_d = ss(-6.5, -3.5, d) * (1.0 - ss(18.5, 21.5, d))
    du_bridge = 0.22 * (1.0 - ss(1.15, 1.50, np.abs(d - 3.10)))
    w_cut = ss(u_in, u_in + 2.20, u) * (1.0 - ss(u_in + 6.00, u_in + 8.20 + du_bridge, u))
    z_floor = 27.00 - 0.30 * ss(0.0, -5.0, d) - 0.40 * ss(14.0, 20.0, d)
    H = H * (1.0 - m_d * w_cut) + np.minimum(H, z_floor) * (m_d * w_cut)

    # 4. Severni unikova rampa ze dna prikopu P0=(12.2, -1.0, Z 27.00) -> P1=(16.5, -5.5), zariznuta do rostleho svahu H_base
    du_r, dd_r = 4.3, -4.5
    l2_r = du_r * du_r + dd_r * dd_r
    t_raw = ((u - 12.2) * du_r + (d + 1.0) * dd_r) / l2_r
    t_r = np.clip(t_raw, 0.0, 1.0)
    dist_r = np.hypot(u - (12.2 + du_r * t_r), d - (-1.0 + dd_r * t_r))
    w_ramp = (1.0 - ss(0.95, 1.80, dist_r)) * ss(-0.35, 0.05, t_raw) * (1.0 - ss(0.95, 1.15, t_raw))
    z_ramp = np.minimum(27.00 + 2.90 * t_r, H_base)
    H = H * (1.0 - w_ramp) + z_ramp * w_ramp

    return np.clip(H, 0.0, ZMAX)


def extend_level_terrain(terr_level, H_new, x1_new=4400):
    """rozsiri terrain_from_level.json na x1 = 4400 (nx = 97); pro u <= 8.30 m zachova na milimetr puvodni hodnoty z levelu"""
    x0, y0, st, ny = terr_level["x0"], terr_level["y0"], terr_level["step"], terr_level["ny"]
    nx_old = terr_level["nx"]
    nx_new = int(round((x1_new - x0) / st)) + 1
    grid_y = np.arange(N) * 50.0 - 12600.0
    grid_x = np.arange(N) * 50.0 - 12600.0
    itp = RegularGridInterpolator((grid_y, grid_x), H_new)
    Z_out = []
    for j in range(ny):
        y = y0 + j * st
        row = []
        for i in range(nx_new):
            x = x0 + i * st
            u_val, _ = world_to_ud(x, y)
            if i < nx_old and u_val <= 8.30:
                row.append(int(terr_level["z"][j][i]))
            else:
                z_cm = round(float(itp([[y, x]])[0]) * 100.0)
                row.append(int(z_cm))
        Z_out.append(row)
    out = dict(x0=x0, y0=y0, step=st, nx=nx_new, ny=ny, z=Z_out)
    if "hits" in terr_level:
        out["hits"] = nx_new * ny
    return out


def main():
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    png_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "01_terrain", "Zricenina_heightmap_505_50cm.png")
    tl_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(root, "03_ruin", "blocks", "terrain_from_level.json")
    prev_path = os.path.join(os.path.dirname(os.path.abspath(png_path)), "Zricenina_preview_orez.png")

    H_orig = np.array(Image.open(png_path)).astype(float) / 65535.0 * ZMAX
    tl = json.load(open(tl_path, encoding="utf-8"))
    H_new = apply_gate_moat(H_orig, tl)

    u16 = np.clip(np.rint(H_new / ZMAX * 65535.0), 0, 65535).astype(np.uint16)
    Image.fromarray(u16).save(png_path)
    Image.fromarray(slope_rgb(H_new).astype(np.uint8)).save(prev_path)

    tl_new = extend_level_terrain(tl, H_new, x1_new=4400)
    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(tl_new, f)
    print("gen_moat: ulozeno %s, %s a %s (nx=%d, ny=%d)" % (png_path, prev_path, tl_path, tl_new["nx"], tl_new["ny"]))


if __name__ == "__main__":
    main()
