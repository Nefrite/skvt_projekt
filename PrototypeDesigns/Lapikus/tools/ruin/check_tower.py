import sys, math, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
sys.path.insert(0,"ruin"); import build_ruin_blocks as B
lay=json.load(open(sys.argv[1])); data,P=B.compute_blocks(lay)
T=json.load(open("/mnt/user-data/uploads/GameDesign/Claude outputs/Zriceni_orez_505/03_ruin/ruin_layout_draft.json"))["tower"]
fs=lay["floors"][0]; ox,oy=fs["origin"]; U=np.array(fs["u"]); V=np.array(fs["v"])
def uv(x,y): d=np.array([x-ox,y-oy]); return d@U/100, d@V/100
COL={"face":(0.72,0.66,0.56),"core":(0.5,0.47,0.43),"frame":(0.9,0.8,0.6),"wood":(0.55,0.36,0.18),"floor":(0.8,0.76,0.68)}
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
            polys.append(q); fc.append(np.clip(np.array(COL[s.cat])*(0.5+0.5*abs(n@Ld)),0,1))
    return polys,fc
names=["Vez_J","Vez_V","Vez_Z","Vez_S","Vez_Patra"]
allst=[(n,s) for n in names for s in data[n]["stones"]]
def man(u,v,z):  # postava 1.8 m
    x,y=np.array([ox,oy])+(U*u+V*v)*100
    return B.Stone("man","frame",x,y,F+z*100+90,0,45,30,180)
import os
AZ=[float(a) for a in os.environ.get("AZ","0,0,0").split(",")]
views=[("řez věží – pohled od severu (severní zeď odebrána)", lambda n,s,u,v: n!="Vez_S" and not (n in("Vez_V","Vez_Z") and v>9.8), (AZ[0],12)),
       ("zevnitř k jižní zdi: střílny s výklenky", lambda n,s,u,v: (n=="Vez_J") or (n=="Vez_Patra" and v<4.5 and s.cat=="floor"), (AZ[1],8)),
       ("shora: trámy, prkna, otvor pro žebřík (2. patro)", lambda n,s,u,v: n=="Vez_Patra" and (s.cat=="floor" or abs(s.z-(F+2*420))<60), (0,80))]
fig=plt.figure(figsize=(30,11))
for k,(tt,keep,(az,el)) in enumerate(views):
    st=[s for n,s in allst if keep(n,s,*uv(s.x,s.y))]+[man(5.2,6.0,0),man(3.0,5.0,4.2)]*(k==0)+[man(5.5,3.2,0)]*(k==1)
    polys,fc=boxes(st,lambda s,u,v: True)
    ax=fig.add_subplot(1,3,k+1,projection="3d"); ax.set_proj_type("ortho")
    ax.add_collection3d(Poly3DCollection(polys,facecolors=fc,edgecolors=(0,0,0,0.15),linewidths=0.1))
    c=(np.array([ox,oy])+(U+V)*550)/100
    ax.set_xlim(c[0]-8,c[0]+8); ax.set_ylim(c[1]-8,c[1]+8); ax.set_zlim(-2,14)
    ax.set_box_aspect((16,16,16),zoom=1.25)
    base=math.degrees(math.atan2(V[1],V[0]))
    ax.view_init(elev=el,azim=base+az if k<2 else base+AZ[2]); ax.set_axis_off(); ax.set_title(tt,fontsize=15)
plt.subplots_adjust(left=0,right=1,top=0.92,bottom=0,wspace=0)
fig.suptitle("Věž: kamenná podlaha, patra po 4,2 m (trámy v kapsách + prkna), střílny s výklenkem – postava 1,8 m pro měřítko",fontsize=17,fontweight="bold")
plt.savefig(sys.argv[2],dpi=70)
