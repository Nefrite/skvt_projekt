"""check_tower.py - nahled rezu veze bez Unrealu (zricenina + drevene vestavby).
python check_tower.py <03_ruin/blocks/ruin_layout.json> <vystup.png> <05_constructions/constructions.json>
(RUIN_DIR = slozka s build_ruin_blocks.py, vychozi ../../03_ruin/blocks; pro skutecny teren vloz terrain_from_level.json do ruin_layout)"""
import sys, math, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os; sys.path.insert(0,os.environ.get("RUIN_DIR",os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","03_ruin","blocks"))); sys._ruin_import_only=True; import build_ruin_blocks as B
lay=json.load(open(sys.argv[1])); data,P=B.compute_blocks(lay)
# drevene vestavby z 05_constructions (constructions.json) + kamenna dlazba ze zriceniny
cdat=json.load(open(sys.argv[3])) if len(sys.argv)>3 else {"floors":[]}
terr=B.Terrain(lay["terrain"])
fsw=[f for f in cdat["floors"] if f["name"]=="Vez_Patra"]
data["Vez_Patra"]={"stones":(B.build_floor_stones(fsw[0],P,data,terr) if fsw else [])+data.get("Vez_Dlazba",{}).get("stones",[])}
fs=(fsw[0] if fsw else lay["floors"][0]); ox,oy=fs["origin"]; U=np.array(fs["u"]); V=np.array(fs["v"])
def uv(x,y): d=np.array([x-ox,y-oy]); return d@U/100, d@V/100
COL={"face":(0.72,0.66,0.56),"core":(0.5,0.47,0.43),"frame":(0.9,0.8,0.6),"wood":(0.62,0.57,0.5),"wood_tar":(0.24,0.19,0.14),"wood_oil":(0.52,0.35,0.2),"wood_blood":(0.42,0.17,0.11),"wood_old":(0.66,0.65,0.62),"floor":(0.8,0.76,0.68),"crown":(0.78,0.76,0.68)}
Ld=np.array([-0.4,-0.5,0.75]);Ld/=np.linalg.norm(Ld)
F=fs["ref_z"]
def boxes(stones,keep):
    polys=[];fc=[]
    for s in stones:
        u,v=uv(s.x,s.y)
        if not keep(s,u,v): continue
        y=math.radians(s.yaw); p=math.radians(s.pitch)
        a=np.array([math.cos(y),math.sin(y),0]); b=np.array([-math.sin(y),math.cos(y),0]); w=np.array([0,0,1.0])
        a,w=a*math.cos(p)+w*math.sin(p), -a*math.sin(p)+w*math.cos(p)
        c=np.array([s.x,s.y,s.z-F])
        Pp=[(c+i*a*s.sx/2+j*b*s.sy/2+k*w*s.sz/2)/100 for i in(-1,1) for j in(-1,1) for k in(-1,1)]
        for f in [(0,1,3,2),(4,5,7,6),(0,1,5,4),(2,3,7,6),(0,2,6,4),(1,3,7,5)]:
            q=[Pp[i] for i in f]; n=np.cross(q[1]-q[0],q[2]-q[0]); n/=np.linalg.norm(n)+1e-9
            polys.append(q); fc.append(np.clip(np.array(COL.get(s.cat,(0.7,0.7,0.7)))*(0.5+0.5*abs(n@Ld)),0,1))
    return polys,fc
names=["Vez_J","Vez_V","Vez_Z","Vez_S","Vez_Patra"]
allst=[(n,s) for n in names for s in data[n]["stones"]]
def man(u,v,z):  # postava 1.8 m
    x,y=np.array([ox,oy])+(U*u+V*v)*100
    return B.Stone("man","frame",x,y,F+z*100+90,0,45,30,180)
import os
U_=U; 
def ang(vec): return math.degrees(math.atan2(vec[1],vec[0]))
views=[("řez od severu: schody cik-cak (S zeď odebrána)", lambda n,s,u,v: n in ("Vez_J","Vez_Patra") and v<11.5 or (n in ("Vez_V","Vez_Z") and v<4), ang(V), 4),
       ("zvenku od severu: původní vstup, ochoz na trámech se vzpěrami", lambda n,s,u,v: n in ("Vez_S","Vez_V","Vez_Z") or (n=="Vez_Patra" and "|D|" in s.id), ang(V)+25, 10),
       ("půdorys 1. patra: výlez, přechod do vedlejšího pole, schody do 2. patra", lambda n,s,u,v: n=="Vez_Patra" and abs(s.z-(F+420))<80 or "|S1|" in s.id, ang(V), 88)]
fig=plt.figure(figsize=(30,11))
for k,(tt,keep,azv,el) in enumerate(views):
    st=[s for n,s in allst if keep(n,s,*uv(s.x,s.y))]+[man(7.6,8.8,0),man(4.5,7.1,8.4)]*(k==0)+[man(3.4,12.9,4.2)]*(k==1)
    polys,fc=boxes(st,lambda s,u,v: True)
    ax=fig.add_subplot(1,3,k+1,projection="3d"); ax.set_proj_type("ortho")
    ax.add_collection3d(Poly3DCollection(polys,facecolors=fc,edgecolors=(0,0,0,0.15),linewidths=0.1))
    c=(np.array([ox,oy])+(U+V)*550)/100
    ax.set_xlim(c[0]-9,c[0]+9); ax.set_ylim(c[1]-9,c[1]+9); ax.set_zlim(-2,14)
    ax.set_box_aspect((18,18,16),zoom=1.2)
    ax.view_init(elev=el,azim=azv); ax.set_axis_off(); ax.set_title(tt,fontsize=15)
plt.subplots_adjust(left=0,right=1,top=0.92,bottom=0,wspace=0)
fig.suptitle("Věž: schody cik-cak, dveře mezi zdí a sloupem, ochoz bez sloupků; dřevo: dehet (tmavé), krev (červenohnědá), staré (šedé), bez úpravy (světlé)",fontsize=17,fontweight="bold")
plt.savefig(sys.argv[2],dpi=70)
