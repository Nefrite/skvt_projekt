import sys, math, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
sys.argv=[sys.argv[0]]+sys.argv[1:]
import importlib.util
import os; _B3=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","03_ruin","blocks","build_ruin_blocks.py")   # generator zriceniny (jedina kopie)
sys._ruin_import_only=True; spec=importlib.util.spec_from_file_location("brb",_B3); B=importlib.util.module_from_spec(spec); spec.loader.exec_module(B); sys._ruin_import_only=False
B.LAYOUT_PATH=sys.argv[1]
lay=B.load_layout(); data,P=B.compute_blocks(lay,[],None,lay.get('volumes_examples') if len(sys.argv)>3 else None); Z0=lay["plateau_z_cm"]
COL={"face":(0.72,0.66,0.56),"core":(0.55,0.52,0.48),"frame":(0.86,0.78,0.6),"crown":(0.78,0.76,0.68),"floor":(0.8,0.76,0.68)}
Ld=np.array([-0.5,-0.4,0.75]);Ld/=np.linalg.norm(Ld)
def boxes(stones,xr,yr):
    polys=[];fc=[]
    for s in stones:
        if not(xr[0]<s.x<xr[1] and yr[0]<s.y<yr[1]): continue
        y=math.radians(s.yaw); p=math.radians(s.pitch)
        u=np.array([math.cos(y),math.sin(y),0]); v=np.array([-math.sin(y),math.cos(y),0]); w=np.array([0,0,1.0])
        u,w=u*math.cos(p)+w*math.sin(p), -u*math.sin(p)+w*math.cos(p)
        c=np.array([s.x,s.y,s.z-Z0])
        Pp=[(c+a*u*s.sx/2+b*v*s.sy/2+d*w*s.sz/2)/100 for a in(-1,1) for b in(-1,1) for d in(-1,1)]
        for f in [(0,1,3,2),(4,5,7,6),(0,1,5,4),(2,3,7,6),(0,2,6,4),(1,3,7,5)]:
            q=[Pp[i] for i in f]; n=np.cross(q[1]-q[0],q[2]-q[0]); n/=np.linalg.norm(n)+1e-9
            polys.append(q); fc.append(np.clip(np.array(COL.get(s.cat,(0.7,0.7,0.7)))*(0.5+0.5*abs(n@Ld)),0,1))
    return polys,fc
allst=[s for w in data.values() for s in w["stones"]+w.get("rubble",[])+w.get("loose",[])]
views=[("věž z nádvoří – průlom a vstup",(100,12),(200,2200),(-3000,-1500),(2,20),(-28,-8),(-2,14),1.5),("brána – detail oblouku od V",(5,12),(300,2300),(-3300,-1600),(4,22),(-30,-14),(-2,9),1.4),("celek od JZ",(-125,24),(-5200,3000),(-3300,400),(-48,22),(-30,3),(-6,16),1.1),
       ("brána a věž od SV",(50,22),(300,2300),(-3300,-500),(4,22),(-30,-6),(-3,14),1.3),
       ("palác z nádvoří",(70,28),(-3000,1000),(-2200,200),(-30,10),(-22,2),(-3,12),1.25)]
fig=plt.figure(figsize=(50,10))
for k,(tt,(az,el),xr,yr,xl,yl,zl,zm) in enumerate(views):
    polys,fc=boxes(allst,xr,yr)
    ax=fig.add_subplot(1,5,k+1,projection='3d')
    ax.add_collection3d(Poly3DCollection(polys,facecolors=fc,edgecolors=(0,0,0,0.12),linewidths=0.1))
    ax.set_xlim(*xl);ax.set_ylim(*yl);ax.set_zlim(*zl)
    ax.set_box_aspect((xl[1]-xl[0],yl[1]-yl[0],zl[1]-zl[0]),zoom=zm); ax.invert_yaxis(); ax.view_init(elev=el,azim=az); ax.set_axis_off(); ax.set_title(tt,fontsize=15)
plt.subplots_adjust(left=0,right=1,top=0.93,bottom=0,wspace=0)
fig.suptitle("Zřícenina z bloků – stav ~1650 (líc: lomové kvádry, šedé: jádro, světlé: ostění a oblouky)",fontsize=17,fontweight="bold")
plt.savefig(sys.argv[2],dpi=70)
