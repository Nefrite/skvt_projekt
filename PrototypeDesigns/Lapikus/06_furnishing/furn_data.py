"""furn_data.py - data vybaveni (furnishing.json): nacteni, ulozeni se zalohou a slouceni se specem.

furnishing.json je jediny zdroj poloh vybaveni. Generator (tools/furnishing/gen_furnishing.py) ho sestavi ze specu
staveb, capture v UE (build_furnishing.py, MODE = "capture") do nej primo zapise polohy z levelu. Pri dalsim generovani
se data slouci (merge): ulozene polohy zustanou, nove kusy ze specu pribudou.

Kus (polozka "items" skupiny):
  - polohove klice POSE_KEYS (ram skupiny: a = s, c = n v m, z nad terenem v m, x = smer lokalni osy X v ramu, pitch,
    roll, scale / size; useky p0, p1 + prumer d) - ze specu, po capture z levelu
  - "captured": true  poloha ulozena z levelu (generator ji neprepise), "spec" = poloha podle specu (pro list a reset)
  - "removed": true   kus v levelu smazany (nestavi se, generator ho znovu neprida)
  - "manual": true    kus pridany v levelu duplikaci (neni ve specu), "copy_of" = puvodni kus, "mesh" = mesh puvodniho kusu
"""
import json, os, shutil

POSE_KEYS = ("a", "c", "z", "zc", "x", "pitch", "roll", "scale", "size", "p0", "p1", "d")
KEEP_KEYS = ("captured", "removed", "manual", "copy_of", "mesh")


def load(path):
    with open(path, encoding="utf-8") as f: return json.load(f)


def save(path, data, backup=True):
    """zapise furnishing.json; backup = predchozi verze do furnishing.json.bak"""
    if backup and os.path.exists(path): shutil.copy2(path, path + ".bak")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def pose_of(it):
    return {k: it[k] for k in POSE_KEYS if k in it}


def new_id(items, base):
    """volne id pro kopii kusu: <base>_2, <base>_3 ..."""
    used = {it["id"] for it in items}; k = 2
    while "%s_%d" % (base, k) in used: k += 1
    return "%s_%d" % (base, k)


def merge(old, groups):
    """slouci nove sestavene skupiny (ze specu) s dosavadnimi daty -> (skupiny, hlaseni).
    Ramec skupiny (origin, u, v, roof, folder) a nepolohove klice kusu jsou vzdy ze specu. Kus s ulozenou polohou
    (captured) nebo smazany (removed) si drzi svou polohu a priznaky; ostatni kusy jdou cele podle specu.
    Rucne pridane kusy (manual) zustanou. Kusy a skupiny, ktere ve specu uz nejsou, zustanou a vypisou se."""
    msgs = []; out = []
    old_g = {g["name"]: g for g in (old or {}).get("groups", [])}
    for g in groups:
        og = old_g.pop(g["name"], None)
        if og is None: out.append(g); continue
        oi = {it["id"]: it for it in og.get("items", [])}; items = []
        for it in g["items"]:
            o = oi.pop(it["id"], None)
            if o and (o.get("captured") or o.get("removed")):
                m = {k: v for k, v in it.items() if k not in POSE_KEYS}
                m.update(pose_of(o) if o.get("captured") else pose_of(it))
                for k in KEEP_KEYS:
                    if k in o: m[k] = o[k]
                if o.get("captured"):
                    m["spec"] = pose_of(it)
                    if o.get("spec") is not None and o["spec"] != m["spec"]:
                        msgs.append("%s|%s: poloha ve specu se zmenila, plati ulozena poloha z levelu (reset ji vrati na novy spec)" % (g["name"], it["id"]))
                items.append(m)
            else:
                items.append(it)
        for o in oi.values():
            items.append(o)
            if not o.get("manual"):
                msgs.append("%s|%s: kus uz ve specu neni, v datech zustava (smaz ho v levelu a spust capture, nebo ho smaz z furnishing.json)" % (g["name"], o["id"]))
        out.append(dict(g, items=items))
    for og in old_g.values():
        out.append(og); msgs.append("skupina %s uz ve specu neni, v datech zustava" % og["name"])
    return out, msgs


def reset(data, only=None, items=None):
    """vrati kusy skupin only (None = vse) na polohu podle specu: zrusi captured / removed, rucne pridane kusy smaze.
    items = jen tyto kusy (id; u kopii i puvodni id -> smaze jeho kopie). -> pocty (vraceno, obnoveno, smazano kopii)"""
    n_pose = n_rem = n_man = 0
    for g in data.get("groups", []):
        if only and g["name"] not in only: continue
        keep = []
        for it in g["items"]:
            hit = not items or it["id"] in items or it.get("copy_of") in items
            if not hit: keep.append(it); continue
            if it.get("manual"): n_man += 1; continue
            if it.get("captured"):
                sp = it.get("spec") or {}
                for k in POSE_KEYS: it.pop(k, None)
                it.update(sp); it.pop("spec", None); it.pop("captured", None); n_pose += 1
            if it.pop("removed", None): n_rem += 1
            keep.append(it)
        g["items"] = keep
    return n_pose, n_rem, n_man
