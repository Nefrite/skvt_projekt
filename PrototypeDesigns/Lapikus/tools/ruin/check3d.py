import json, math, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import build_ruin as B
lay=B.load_layout(sys.argv[1]); cols,rocks,ramps=B.compute(lay); Z0=lay["plateau_z_cm"]
polys=[];fc=[]
Ld=np.array([-0.5,-0.4,0.75]);Ld/=np.linalg.norm(Ld)
def box(cx,cy,yaw,L,W,z0,z1,col,pitch=0):
    y=math.radians(yaw); u=np.array([math.cos(y),math.sin(y),0]); v=np.array([-math.sin(y),math.cos(y),0]); w=np.array([0,0,1.0])
    if pitch:
        p=math.radians(pitch); u2=u*math.cos(p)+w*math.sin(p); w=-u*math.sin(p)+w*math.cos(p); u=u2
    c=np.array([cx,cy,(z0+z1)/2]); hz=(z1-z0)/2
    P=[c+sx*u*L/2+sy*v*W/2+sz*w*hz for sx in(-1,1) for sy in(-1,1) for sz in(-1,1)]
    F=[(0,1,3,2),(4,5,7,6),(0,1,5,4),(2,3,7,6),(0,2,6,4),(1,3,7,5)]
    for f in F:
        q=[P[i]/100 for i in f]; n=np.cross(q[1]-q[0],q[2]-q[0]); n/=np.linalg.norm(n)+1e-9
        polys.append(q); fc.append(np.clip(np.array(col)*(0.55+0.45*abs(n@Ld)),0,1))
for c in cols: box(c["x"],c["y"],c["yaw"],c["len"],c["thick"],c["z0"]-Z0,c["z1"]-Z0,(0.73,0.65,0.53))
for r in rocks: box(r["x"],r["y"],r["yaw"],120*r["scale"],100*r["scale"],r["z"]-Z0,r["z"]-Z0+70*r["scale"],(0.45,0.4,0.35))
for r in ramps: box(r["x"],r["y"],r["yaw"],r["len"],r["width"],r["z"]-Z0-30,r["z"]-Z0+30,(0.8,0.5,0.3),pitch=r["pitch"])
fig=plt.figure(figsize=(22,9))
for k,(az,el,tt) in enumerate([(-125,26,"od JZ"),(55,30,"od SV")]):
    ax=fig.add_subplot(1,2,k+1,projection='3d')
    ax.add_collection3d(Poly3DCollection(polys,facecolors=fc,edgecolors="none"))
    ax.set_xlim(-48,22);ax.set_ylim(-30,3);ax.set_zlim(-8,22);ax.set_box_aspect((70,33,30),zoom=1.1)
    ax.invert_yaxis();ax.view_init(elev=el,azim=az);ax.set_axis_off();ax.set_title(tt)
plt.subplots_adjust(left=0,right=1,top=0.95,bottom=0,wspace=0); plt.savefig(sys.argv[2],dpi=75)
