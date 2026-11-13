"""03 priprava dat zdi: podstavba, ref_z, ochrana do vysky otvoru, bouraci objemy"""
import math
from .decay import OPENING_TYPES
from zrlib.geom import _clip_segment_box, _pt_on, _wall_len


def apply_plinth(wd):
    """podstavba (m): zed stoji na nizsim terenu -> vyska, parapety otvoru, ochrana a sesuvy se zvednou"""
    pl = wd.get("plinth", 0.0)
    if not pl: return wd
    wd = dict(wd, H0=wd["H0"] + pl)
    wd["openings"] = [dict(o, sill=o["sill"] + pl) for o in wd.get("openings", [])]
    wd["protect"] = [dict(p, min=p["min"] + pl) if "min" in p else p for p in wd.get("protect", [])]   # "to" = absolutne, bez podstavby
    wd["breaches"] = [dict(b, floor=b["floor"] + pl) for b in wd.get("breaches", [])]
    return wd

def apply_ref_z(wd, terr):
    """ref_z (absolutni cm, napr. podlaha veze): vysky otvoru (sill, splay floor/top) jsou zadane od ni,
    ne od paty zdi -> prevedou se na vysky od mistni paty."""
    ref = wd.get("ref_z")
    if ref is None: return wd
    ops = []
    for o in wd.get("openings", []):
        zb = terr.z(*_pt_on(wd["points"], o["s"]))
        o = dict(o, sill=(ref + o["sill"] * 100 - zb) / 100)
        if o.get("splay"):
            sp = o["splay"]; o["splay"] = dict(sp, floor=(ref + sp["floor"] * 100 - zb) / 100, top=(ref + sp["top"] * 100 - zb) / 100)
        ops.append(o)
    return dict(wd, openings=ops)

def opening_top_abs(wd, idx, terr):
    """absolutni vyska (cm) vrsku otvoru idx vcetne osteni / oblouku (s podstavbou a z_offset)"""
    w2 = apply_ref_z(apply_plinth(wd), terr); o = w2["openings"][idx]
    zb = terr.z(*_pt_on(wd["points"], o["s"]))
    return zb + (o["sill"] + o["h"] + OPENING_TYPES[o["kind"]]["frame"]) * 100 + wd.get("z_offset", 0.0) * 100

def resolve_protect_to(wd, terr, walls):
    """ochrana s "to": [{wall, opening, dz}, ...] = zed alespon do vysky vrsku otvoru jine zdi (napr. oblouku brany);
    dva cile = linearne od s0 k s1. Prevede se na kousky po 0.5 m s min (m) od paty teto zdi."""
    out = []
    byname = {w["name"]: w for w in walls}
    for p in wd.get("protect", []):
        if "to" not in p: out.append(p); continue
        zs = [opening_top_abs(byname[t["wall"]], t.get("opening", 0), terr) + t.get("dz", 0.0) * 100 for t in p["to"]]
        z0, z1 = zs[0], zs[-1]; n = max(1, int(math.ceil((p["s1"] - p["s0"]) / 0.5)))
        for i in range(n):
            a = p["s0"] + (p["s1"] - p["s0"]) * i / n; b = p["s0"] + (p["s1"] - p["s0"]) * (i + 1) / n
            sm = min(max((a + b) / 2, 0.0), _wall_len(wd["points"]))
            za = z0 + (z1 - z0) * ((a + b) / 2 - p["s0"]) / max(p["s1"] - p["s0"], 1e-6)
            zb = terr.z(*_pt_on(wd["points"], sm))
            out.append(dict(s0=a, s1=b, min=(za - zb - wd.get("z_offset", 0.0) * 100) / 100))
    return dict(wd, protect=out)

def wall_box_hits(wd, box, terr):
    """Kde box (x0,y0,z0,x1,y1,z1 v cm) protina osu zdi: [(s0, s1, sill_m, top_m)], s od prvniho bodu zdi."""
    pts = wd["points"]; hits = []; cum = 0.0
    pad = wd["thickness"] * 50
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]; ln = math.hypot(q[0] - p[0], q[1] - p[1]) / 100
        r = _clip_segment_box(p, q, box[0] - pad * 0.2, box[1] - pad * 0.2, box[3] + pad * 0.2, box[4] + pad * 0.2)
        if r:
            t0, t1 = r; tm = (t0 + t1) / 2
            zb = terr.z(p[0] + (q[0] - p[0]) * tm, p[1] + (q[1] - p[1]) * tm)
            hits.append((cum + t0 * ln, cum + t1 * ln, (box[2] - zb) / 100, (box[5] - zb) / 100))
        cum += ln
    return hits

def apply_volumes(layout, volumes, terr):
    """Prevede objemy z levelu (TriggerBox s tagem) na upravy:
       Ruin_Cut            -> cut_box (vyrizne vse uvnitr)
       Ruin_Opening:<typ>  -> novy otvor ve zdi (okno, dvere, portal, brana, strilna, prulom) s plnou logikou rozpadu
                              + Ruin_Intact (osteni cele) / Ruin_Protect (oblouk se nezrouti)
       Ruin_Keep           -> restore: zdi v boxu alespon do vysky vrsku boxu
       Ruin_Explode        -> bloky uvnitr jako samostatne actory (rucni posun / mazani)"""
    walls = [dict(w, openings=list(w.get("openings", []))) for w in layout["walls"]]
    edits = list(layout.get("edits", [])); explode = []
    for v in volumes:
        tags = v["tags"]; box = v["box"]
        if "Ruin_Cut" in tags:
            edits.append({"op": "cut_box", "box": box})
        if "Ruin_Explode" in tags:
            explode.append(box)
        kinds = [t.split(":", 1)[1] for t in tags if t.startswith("Ruin_Opening:")]
        keep = "Ruin_Keep" in tags
        if not kinds and not keep: continue
        for w in walls:
            for s0, s1, sill, top in wall_box_hits(w, box, terr):
                if s1 - s0 < 0.1: continue
                if keep:
                    edits.append({"op": "restore", "wall": w["name"], "s0": s0, "s1": s1, "h": top})
                for kind in kinds:
                    o = dict(kind=kind if kind in OPENING_TYPES else "prulom", s=(s0 + s1) / 2, w=s1 - s0,
                             sill=max(0.0, sill), h=max(0.3, top - max(0.0, sill)))
                    if "Ruin_Intact" in tags: o["robbed"] = "none"
                    if "Ruin_Protect" in tags: o["protect"] = True
                    w["openings"].append(o)
    return dict(layout, walls=walls, edits=edits), explode
