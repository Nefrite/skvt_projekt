"""Kontrola: zadny blok lice/jadra nesmi zasahovat do svetlosti otvoru. python test_openings.py"""
import json
import build_ruin_blocks as B
import sys; lay=json.load(open(sys.argv[1] if len(sys.argv)>1 else "ruin_layout.json")); P=B.params(lay); terr=B.Terrain(lay["terrain"])
allpts=[p for w in lay["walls"] for p in w["points"]]
cen=(sum(p[0] for p in allpts)/len(allpts), sum(p[1] for p in allpts)/len(allpts))
bad=0; n=0
for wd in lay["walls"]:
    stones, states, L = B.build_wall_stones(wd, P, terr, lay, [], set(), cen)
    n+=len(states)
    for s in stones:
        if not s.span: continue
        s0,s1,_,_=s.span
        for st in states:
            z0=(s.z-s.sz/2-st["zb"])/100; z1=(s.z+s.sz/2-st["zb"])/100
            for k in range(21):
                xx=s0+0.02+(s1-s0-0.04)*k/20
                g=B.opening_gap(st,xx)
                core = s.cat=="core"
                if st["kind"]=="kapsa" and int(s.id.split("|")[2])!=st["inside"]: g=None   # kapsa jen ve vnitrnim lici
                if core and not st["lintel_lost"] and not (st["x0"] <= xx <= st["x1"]): g=None   # jadro za vylomenym ostenim nese oblouk/nadprazi
                if g and z1-0.03>g[0] and z0+0.03<g[1]:
                    bad+=1; print(wd["name"],s.id,st["kind"],round(xx,2),g,(round(z0,2),round(z1,2))); break
print("otvoru:",n,"kolize:",bad)
