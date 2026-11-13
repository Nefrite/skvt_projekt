"""03 dodatecne upravy kamenu zdi: koruna pod strechou, zlabky pro tramy, rozpadle jadro"""
import math, random, zlib
from zrlib.stones import Stone


def roof_clear(stones, rc, notches, T, face_d):
    """koruna pod strechou (05 krytina): kameny se ven od vnitrniho lice snizi ve sklonu strechy, aby nezasahovaly
    do lati a prken mezi tramy. Sklon kolmo na zed se interpoluje mezi zlabky (notches[].slope)."""
    ns = sorted(notches, key=lambda n_: n_["s"])
    def slope_at(s_):
        if s_ <= ns[0]["s"]: return ns[0]["slope"]
        for a, b in zip(ns[:-1], ns[1:]):
            if s_ <= b["s"]: f = (s_ - a["s"]) / max(b["s"] - a["s"], 1e-6); return a["slope"] + (b["slope"] - a["slope"]) * f
        return ns[-1]["slope"]
    inzone = [st for st in stones if st.span and st.cat in ("face", "core", "crown") and rc["s0"] <= (st.span[0] + st.span[1]) / 2 <= rc["s1"]]
    if not inzone: return stones
    tops_ = [round(st.z + st.sz / 2) for st in inzone if ".n1" not in st.id]
    wt = max(t for t in set(tops_) if tops_.count(t) >= 5)             # zarovnana koruna = nejvyssi vyska, kterou ma aspon 5 kamenu
    clear, margin = rc["clear"] * 100, rc.get("margin", 0.02) * 100
    out = []; zone = set(id(st) for st in inzone)
    for st in stones:
        if id(st) not in zone:
            out.append(st); continue
        sm = (st.span[0] + st.span[1]) / 2
        nn = min(ns, key=lambda n_: abs(n_["s"] - sm))                 # strana dovnitr podle nejblizsiho zlabku
        ya = math.radians(st.yaw); nxs, nys = -math.sin(ya), math.cos(ya)
        sgn = 1 if nxs * nn["nin"][0] + nys * nn["nin"][1] > 0 else -1
        lay = int(st.id.split("|")[2].split(".")[0]) if st.id.count("|") >= 3 and st.id.split("|")[2].lstrip("-").split(".")[0].isdigit() else 0
        off = lay * sgn * (T / 2 - face_d / 2)                          # od osy zdi dovnitr (cm)
        dist = max(0.0, T / 2 - off + st.sy / 2)                      # od vnitrniho lice k vnejsi hrane kamene
        allowed = wt + clear - slope_at(sm) * dist - margin
        top = st.z + st.sz / 2
        if top <= allowed:
            out.append(st); continue
        cut = top - allowed
        if st.sz - cut < 5: continue                                    # kamen pod strechou cely odebran
        st.sz -= cut; st.z -= cut / 2
        if st.span: st.span = (st.span[0], st.span[1], st.span[2], st.span[3] - cut / 100)
        out.append(st)
    return out

def cut_notches(stones, notches, P):
    """zlabek pres celou tloustku zdi: kus kamene v sirce w (m) kolem s se snizi az na dno zlabku (vrch zdi - d, ven hloubeji
    podle sklonu tramu; muze projit i pres vic rad).
    Plati pro lic, jadro i korunu; kameny se podle zlabku rozdeli (ID .n0 / .n1 / .n2)."""
    out = list(stones)
    for nt in notches:
        d = nt["d"] * 100
        def window(st):
            """zlabek v miste kamene: tram jde sikmo pres tloustku zdi -> u kazde vrstvy jinde (k) a jinak hluboko (slope)"""
            off = 0.0
            if nt.get("pt") and nt.get("nin"):
                off = (st.x - nt["pt"][0]) * nt["nin"][0] + (st.y - nt["pt"][1]) * nt["nin"][1]
            dd = d + nt.get("slope", 0.0) * max(0.0, nt.get("t", 0) * 50 - off + st.sy / 2)
            if nt.get("dir"):
                # presne podle pudorysu: cast kamene (podel jeho delky), ktera lezi pod tramem (+ 4 cm vule na kazde strane);
                # plati i v zakrivene / lomene zdi, kde se s podel osy zdi s polohou kamene nekryje
                bx, by = nt["dir"]; lx, ly = -by, bx
                rx, ry = st.x - nt["pt"][0], st.y - nt["pt"][1]
                if abs(rx * bx + ry * by) > nt.get("t", 2.0) * 100 + 150: return 0.0, 0.0, dd   # daleko podel tramu
                ya = math.radians(st.yaw); A = math.cos(ya) * lx + math.sin(ya) * ly; Bq = -math.sin(ya) * lx + math.cos(ya) * ly
                c_lat = rx * lx + ry * ly; H = nt.get("bw", 0.22) * 50 + 4.0 + st.sy / 2 * abs(Bq)
                mid = (st.span[0] + st.span[1]) / 2; half = (st.span[1] - st.span[0]) * 50
                if abs(A) < 1e-6:
                    return (st.span[0] - 1, st.span[1] + 1, dd) if abs(c_lat) < H else (0.0, 0.0, dd)
                u0, u1 = sorted(((-H - c_lat) / A, (H - c_lat) / A))
                if u1 < -half or u0 > half: return 0.0, 0.0, dd
                return mid + u0 / 100, mid + u1 / 100, dd
            c = nt["s"] + off * nt.get("k", 0.0) / 100
            # sikmy tram jde i pres hloubku kamene (vrstvy) -> zlabek o tolik sirsi; hloubka podle vnejsi hrany kamene
            hw = nt["w"] / 2 + abs(nt.get("k", 0.0)) * st.sy / 200
            return c - hw, c + hw, dd
        hit = []
        for st in out:
            if st.span and st.cat in ("face", "core", "crown"):
                a, b, _ = window(st)
                if b > a and st.span[0] < b and st.span[1] > a: hit.append(st)
        if not hit: continue
        top = max(st.z + st.sz / 2 for st in hit)
        new = []
        for st in out:
            a, b, dd = window(st) if st in hit else (0, 0, 0)
            zn = top - dd                                     # dno zlabku v miste kamene (abs. cm)
            if st not in hit or st.z + st.sz / 2 <= zn + 0.5:  # kamen pod dnem zlabku zustava (zlabek muze jit pres vic rad)
                new.append(st); continue
            s0, s1, z0r, z1r = st.span; ya = math.radians(st.yaw); dx, dy = math.cos(ya), math.sin(ya)
            mid = (s0 + s1) / 2; J = P["JOINT"] * 100 if st.cat != "core" else 0.0
            cut = st.z + st.sz / 2 - zn                       # o kolik se kamen ve zlabku snizi
            for k, (p, q, low) in enumerate(((s0, a, False), (max(a, s0), min(b, s1), True), (b, s1, False))):
                if q - p < 0.04: continue
                sz = st.sz - (cut if low else 0.0)
                if sz < 5: continue
                m = (p + q) / 2 - mid
                pc = Stone("%s.n%d" % (st.id, k), st.cat, st.x + dx * m * 100, st.y + dy * m * 100, st.z - (cut / 2 if low else 0.0),
                           st.yaw, max((q - p) * 100 - J, 3.0), st.sy, sz, st.pitch, st.roll, seg=st.seg)
                pc.span = (p, q, z0r, z1r - (cut / 100 if low else 0.0)); pc.rough = st.rough
                new.append(pc)
        out = new
    return out

def rough_core(stones, wd, P, face_d, core_w, T, removed=()):
    """Jadro, pred kterym chybi lic: blok se rozdeli na kameny 0.35-0.7 m, kazdy zapusteny o 5-20 cm od odkryte
    strany (nahodne, u okraje diry mene -> zubaty prechod), mirne pootoceny; mesh lomoveho kamene."""
    byc = {}
    for st in stones:
        if st.span and st.cat == "face" and st.id.count("|") >= 3 and st.id not in removed:   # rucne smazany lic = odkryto
            p_ = st.id.split("|")
            if p_[2] in ("1", "-1"): byc.setdefault((p_[1], int(p_[2])), []).append(st.span)
    out = []; J = P["JOINT"] * 100
    r0, r1 = P.get("CORE_RECESS", (0.05, 0.2))
    sup = {}                                   # obsazene useky kazde rady (vsechny vrstvy) -> kus jadra nesmi viset
    def ci_of(st): return int(st.id.split("|")[1]) if st.span and st.id.count("|") >= 3 and st.id.split("|")[1].isdigit() else None
    for st in stones:                          # lic a ostatni hned, jadro postupne podle rad (co spadlo, nedrzi)
        if st.cat != "core" and ci_of(st) is not None: sup.setdefault(ci_of(st), []).append(st.span)
    for st in stones:
        if not (st.span and st.cat == "core" and st.id.count("|") >= 3) or st.id in removed:   # smazane / oddelene jadro: id zustane
            out.append(st); continue
        ci = st.id.split("|")[1]
        s0, s1, z0r, z1r = st.span
        def cov(a, b, lay):
            return sum(max(0.0, min(b, f1) - max(a, f0)) for f0, f1, _, _ in byc.get((ci, lay), [])) / max(b - a, 1e-6)
        if z1r < 0.05 or (cov(s0, s1, 1) > 0.8 and cov(s0, s1, -1) > 0.8):
            out.append(st); sup.setdefault(int(ci), []).append(st.span); continue
        rng = random.Random(zlib.crc32((st.id + "|rough").encode()) ^ P["SEED"])
        ya = math.radians(st.yaw); dx, dy = math.cos(ya), math.sin(ya); nx, ny = -dy, dx
        L_ = s1 - s0; cuts = [s0]
        while cuts[-1] < s1 - 1e-6:
            l_ = rng.uniform(0.35, 0.7)
            if s1 - (cuts[-1] + l_) < 0.3: l_ = s1 - cuts[-1]
            cuts.append(min(cuts[-1] + l_, s1))
        if len(cuts) == 2 and cov(s0, s1, 1) > 0.5 and cov(s0, s1, -1) > 0.5:
            out.append(st); sup.setdefault(int(ci), []).append(st.span); continue
        cm = (s0 + s1) / 2
        for i, (a, b) in enumerate(zip(cuts[:-1], cuts[1:])):
            off_ = 0.0; dep = st.sy
            for lay in (1, -1):
                c = cov(a, b, lay)
                if c > 0.5: continue                                         # lic pred kusem stoji
                edge = cov(a - 0.4, b + 0.4, lay) > 0.15                         # u okraje diry -> mene zapusteny
                r = rng.uniform(0.0, 0.08) if edge else rng.uniform(r0, r1)
                if c == 0 and rng.random() < 0.25: r = -rng.uniform(0.0, 0.4) * face_d / 100   # zbytek zaklady lice vystupuje
                r *= 100; dep -= r; off_ -= lay * r / 2
            dep = max(dep, 15.0)
            if z0r > 0.2 and int(ci) - 1 in sup:
                ov = sum(max(0.0, min(b, q1) - max(a, q0)) for q0, q1, _, _ in sup[int(ci) - 1])
                if ov < 0.3 * (b - a): continue
            m = (a + b) / 2 - cm
            pc = Stone("%s.r%d" % (st.id, i), "core", st.x + dx * m * 100 + nx * off_, st.y + dy * m * 100 + ny * off_, st.z,
                       st.yaw + rng.uniform(-3, 3), (b - a) * 100 - J, dep, st.sz - J * 0.7, rng.uniform(-2, 2), seg=st.seg)
            pc.span = (a, b, z0r, z1r); pc.rough = True
            out.append(pc); sup.setdefault(int(ci), []).append(pc.span)
    return out


def mark_crown(stones):
    """koruna: odkryte horni kameny (nic na nich nelezi ve stejne vrstve) -> kategorie crown (zvetrale tvary, material koruny)"""
    byz = {}
    for st_ in stones:
        if st_.span and st_.cat in ("face", "core"): byz.setdefault(round((st_.z - st_.sz / 2) / 3), []).append(st_)
    for st_ in stones:
        if not st_.span or st_.cat not in ("face", "core"): continue
        lay_ = int(st_.id.split("|")[2]) if st_.id.count("|") >= 3 else 0
        top_ = st_.z + st_.sz / 2
        above = [b for k_ in (round(top_ / 3) - 1, round(top_ / 3), round(top_ / 3) + 1) for b in byz.get(k_, [])
                 if abs((b.z - b.sz / 2) - top_) < 3 and int(b.id.split("|")[2]) == lay_]
        cov = sum(max(0.0, min(st_.span[1], b.span[1]) - max(st_.span[0], b.span[0])) for b in above)
        if cov < 0.5 * (st_.span[1] - st_.span[0]):
            st_.cat = "crown"
