import numpy as np, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from decay import wall_profile
STONE="#b9a687"; STONE_D="#8f7c5f"; CORE="#d8c9a8"; RUBBLE="#9b8a70"; ORIG="#6f6f6f"

def op(kind,x,w,sill,hgt,**kw): return dict(x0=x-w/2,x1=x+w/2,sill=sill,top=sill+hgt,kind=kind,**kw)
FRAME="#7d6a4f"

def draw_opening(ax,st,dx,x,h):
    o=st["orig"]; x0,x1=o["x0"]+dx,o["x1"]+dx; fr=st["frame"]
    hw=np.interp(np.linspace(x0-fr,x1+fr,12),x,h).min()           # vyska zdi nad otvorem
    arch=st["kind"] in ("portal","brana")
    # puvodni otvor (teckovane)
    ax.add_patch(Rectangle((x0,o["sill"]),x1-x0,o["top"]-o["sill"],fill=False,ec=ORIG,ls=":",lw=0.8,zorder=4))
    def arch_pts(a,b,sill,top,jh=0,wl=0,wr=0):
        c=(a+b)/2; r=(b-a)/2; spring=top-r; t=np.linspace(0,np.pi,30)
        pts=[(a-wl,sill),(a-wl,sill+jh),(a,sill+jh),(a,spring)]+[(c-r*np.cos(q),spring+r*np.sin(q)) for q in t]+[(b,spring),(b,sill+jh),(b+wr,sill+jh),(b+wr,sill)]
        return pts
    if hw<=o["sill"]+0.1: return
    if arch:
        # osteni + oblouk (tmavsi kamen), pokud nejsou vylamana
        if st["robbed"]=="none" or not st["lintel_lost"]:
            ax.add_patch(Polygon(arch_pts(x0-fr,x1+fr,o["sill"],min(o["top"]+fr,hw)),closed=True,fc=FRAME,ec="none",zorder=5))
        jh=st["jamb_h"]; wl=st["wl"] if st["robbed"] in ("both","one") else 0; wr=st["wr"]
        ax.add_patch(Polygon(arch_pts(x0,x1,o["sill"],min(o["top"],hw),jh,wl,wr),closed=True,fc="white",ec=STONE_D,lw=1,zorder=6))
    else:
        top=min(o["top"],hw)
        if st["robbed"]=="none" and fr>0:
            ax.add_patch(Rectangle((x0-fr,o["sill"]-fr*0.6),x1-x0+2*fr,min(o["top"]+fr,hw)-o["sill"]+fr*0.6,fc=FRAME,ec="none",zorder=5))
            ax.add_patch(Rectangle((x0,o["sill"]),x1-x0,top-o["sill"],fc="white",ec=STONE_D,lw=1,zorder=6))
        else:
            a,b=st["x0"]+dx,st["x1"]+dx; sl=st["sill"]
            rng=np.random.default_rng(int(abs(a)*100)); ys=np.linspace(sl,top,7)
            left=[(a+(rng.uniform(-0.08,0.08) if st["wl"]>0 else 0),y) for y in ys]
            right=[(b+(rng.uniform(-0.08,0.08) if st["wr"]>0 else 0),y) for y in ys[::-1]]
            ax.add_patch(Polygon(left+right,closed=True,fc="white",ec=STONE_D,lw=1,zorder=6))

def draw(ax, parts, title, ground=None, notes=(), robbing=None, rubble=None, sockets=(), extra=None, xlim=None, ylim=(-7,25)):
    allx=[]; allh=[]
    for p in parts:
        sts=[]
        x,h=wall_profile(p["L"],p["H0"],None,p.get("corners",()),p.get("openings",()),p.get("breaches",()),
                         seed=p.get("seed",1),protect=p.get("protect",()),mid=p.get("mid",0.88),jag=p.get("jag",0.45),
                         access=p["access"],access_points=p.get("ap",()),states_out=sts)
        p["_states"]=sts
        x=x+p["x"]; allx.append(x); allh.append(h)
        ax.add_patch(Rectangle((p["x"],0),p["L"],p["H0"],fill=False,ls="--",lw=1.2,ec=ORIG))
        ax.text(p["x"]+p["L"]-0.2,p["H0"]+0.3,f"původně {p['H0']:.0f} m · dostupnost {p['access']:.2f}",ha="right",va="bottom",fontsize=8,color=ORIG)
        ax.fill_between(x,0,h,color=STONE,lw=0,step="mid")
        ax.step(x,h,where="mid",color=STONE_D,lw=1.2)
        # sockets
        for lv in p.get("floors",()):
            xs=np.arange(p["x"]+0.6,p["x"]+p["L"]-0.4,1.0)
            hh=np.interp(xs,x,h)
            for xx,hv in zip(xs,hh):
                if hv>lv+0.6: ax.add_patch(Rectangle((xx-0.15,lv),0.3,0.3,color="#3d3225"))
        p['_xh']=(x,h)
    X=np.concatenate(allx); Hh=np.concatenate(allh)
    if robbing:
        for (a,b) in robbing:
            m=(X>=a)&(X<=b)
            ax.fill_between(X[m],0,np.minimum(Hh[m],2.0),color=CORE,hatch="xx",edgecolor="#a8946f",lw=0,step="mid")
    for p in parts:
        x,h=p["_xh"]
        for st in p["_states"]: draw_opening(ax,st,p["x"],x,h)
    if rubble:
        for (a,b,hmax) in rubble:
            xs=np.linspace(a,b,60); y=hmax*np.sin(np.linspace(0,np.pi,60))**0.8
            ax.fill_between(xs,0,y,color=RUBBLE,lw=0); ax.plot(xs,y,color="#6b5d48",lw=0.8)
    if ground is not None:
        gx,gy=ground; ax.fill_between(gx,gy,-7,color="#d9e3c8",lw=0); ax.plot(gx,gy,color="#556b3a",lw=1.5)
    else:
        ax.axhline(0,color="#556b3a",lw=1.5)
    if extra: extra(ax)
    cap=[]
    for i,(xx,yy,t) in enumerate(notes,1):
        ax.plot(xx,yy,"o",ms=13,mfc="#7a1c1c",mec="white",mew=1.5,zorder=10)
        ax.text(xx,yy,str(i),ha="center",va="center",fontsize=8,color="white",fontweight="bold",zorder=11)
        cap.append(f"{i} {t}")
    ax.set_title(title,loc="left",fontsize=11,fontweight="bold",pad=18 if cap else 6)
    if cap: ax.text(0,1.0,"   ".join(cap),transform=ax.transAxes,fontsize=8.5,color="#7a1c1c",va="bottom",wrap=True)
    ax.set_ylim(*ylim)
    ax.set_xlim(*(xlim or (min(p["x"] for p in parts)-1, max(p["x"]+p["L"] for p in parts)+1)))
    ax.set_yticks(range(0,int(ylim[1])+1,5)); ax.set_ylabel("m"); ax.grid(axis="y",color="#eeeeee",lw=0.6); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)

SC=0.27   # palcu na metr
rows=[[("p1",(-1,45),(-5,25))],[("p2",(-1,33),(-2,14)),("p3",(-1,25),(-2,25))],[("p4",(-1,46),(-2,10))],[("p5",(-3,18),(-7,12)),("p6",(-1,13),(-3,8))]]
GAPX=1.3; GAPY=1.25; LM=0.7; TOP=2.1
Wtot=max(sum((xl[1]-xl[0])*SC for _,xl,_ in r)+GAPX*(len(r)-1) for r in rows)+LM+0.3
Htot=TOP+sum(max((yl[1]-yl[0])*SC for _,_,yl in r)+GAPY for r in rows)
fig=plt.figure(figsize=(Wtot,Htot)); axd={}
y=Htot-TOP
for r in rows:
    rh=max((yl[1]-yl[0])*SC for _,_,yl in r); x=LM; y-=rh
    for name,xl,yl in r:
        w=(xl[1]-xl[0])*SC; h=(yl[1]-yl[0])*SC
        axd[name]=fig.add_axes([x/Wtot,(y+rh-h)/Htot,w/Wtot,h/Htot]); x+=w+GAPX
    y-=GAPY
axs=[axd[k] for k in ("p1","p2","p3","p4","p5","p6")]

# 1 Palac + vez, jizni pohled (od utesu)
pal=dict(x=0,L=32,H0=13,access=0.12,corners=(10.5,21),seed=3,floors=(4.2,8.6),
         openings=[op("strilna",x,0.25,1.6,1.1) for x in (3,8,14,19,25,29)]+[op("okno",x,1.2,5.6,2.2) for x in (5.5,12.5,17,26.5)]+[op("okno",x,1.1,10,2.0) for x in (5.5,12.5,26.5)],
         breaches=[dict(x0=16.5,x1=20.5,floor=6.0)])
tow=dict(x=32,L=11,H0=24,access=0.05,corners=(),seed=5,mid=0.94,jag=0.4,floors=(4.5,9,13.5,18),
         openings=[op("strilna",37.5,0.25,3,1.2),op("strilna",37.5,0.25,8,1.2),op("strilna",37.5,0.25,12.5,1.3),op("strilna",37.5,0.25,17,1.3)])
gx=np.linspace(-1,44,200); gy=np.where((gx>14)&(gx<23),-1.5*np.sin(np.clip((gx-14)/9,0,1)*np.pi),0)
draw(axs[0],[pal,tow],"1  PALÁC + VĚŽ – jižní pohled (od útesu), délka 43 m",
     ground=(gx,np.minimum(gy,0)),
     notes=[(18.5,6.6,"menší sesuv nad útesem (podemletí)"),(12.5,8.6,"okno nad útesem – nedostupné, ostění i nadpraží celé"),
            (10.5,12.0,"vnější zeď nepřístupná – zůstala vysoká"),(32.3,20.5,"nároží věže"),(39.5,15,"štěrbiny, kapsy po trámech")],
     rubble=[(15.5,21.5,-0.2)],ylim=(-5,25))
axs[0].text(18,-3.5,"suť pod útesem (sesuv)",ha="center",fontsize=8,color="#6b5d48")

# 2 Palac sever (z nadvori)
paln=dict(x=0,L=32,H0=13,access=0.6,ap=(4.5,16,27),corners=(10.5,21),seed=8,floors=(4.2,8.6),
          openings=[op("dvere",4.5,1.1,0,2.4),op("portal",16,1.6,0,3.0,protect=True),op("dvere",27,1.1,0,2.4)]+[op("okno",x,1.2,5.6,2.2) for x in (8.5,23.5)],
          protect=[(14,18,4.2)])
draw(axs[1],[paln],"2  PALÁC – severní pohled (z nádvoří), délka 32 m",robbing=[(0,32)],
     rubble=[(0.5,4,1.2),(8,13,1.6),(20,25,1.3),(28,31.5,1.0)],
     notes=[(16,3.9,"portál – oblouk drží, spodní ostění vylámaná"),(4.5,3.2,"dveře – vylámané ostění, otvor rozšířený, V-zářez"),(1.5,1.0,"vylámaný líc do 2 m (kamenolom)"),(10.5,5.2,"rozebráno shora po řadách – rovnější koruna")],ylim=(-2,14))

# 3 Vez sever + vychod
tn=dict(x=0,L=11,H0=24,access=0.3,mid=0.95,jag=0.4,seed=11,floors=(4.5,9,13.5),
        openings=[op("dvere",5.5,1.0,6.5,2.2),op("strilna",5.5,0.25,11,1.3)],breaches=[dict(x0=3.5,x1=7.5,floor=12)])
te=dict(x=13,L=11,H0=24,access=0.03,mid=0.96,jag=0.35,seed=12,floors=(4.5,9,13.5,18),
        openings=[op("strilna",18.5,0.25,4,1.2),op("strilna",18.5,0.25,9,1.3),op("strilna",18.5,0.25,14,1.3),op("strilna",18.5,0.25,18.5,1.3)])
draw(axs[2],[tn,te],"3  VĚŽ – severní strana (vlevo) a východní strana k příkopu (vpravo), 11 m",
     notes=[(5.5,14.5,"do nádvoří: horní část rozebraná (V do 12 m)"),(5.5,8.7,"vstup v 1. patře – jedno ostění vylámané"),
            (18.5,21.5,"k příkopu – nedostupné, nejvyšší")],rubble=[(1,10,1.8)],xlim=(-1,25),ylim=(-2,25))

# 4 Hradba sever (zvenku)
cw=dict(x=0,L=45,H0=9,access=0.18,ap=(45,),corners=(12,30),seed=21,jag=0.6,openings=[op('strilna',x,0.2,1.3,1.0) for x in (8,27,35,41)]+[op('strilna',x,0.2,5.0,0.9) for x in (4,14,31)],
        breaches=[dict(x0=19,x1=22.5,floor=1.5)],protect=[(2,11,5.2)])
draw(axs[3],[cw],"4  HRADBA – severní pohled (zvenku ze svahu), délka 45 m  (vlevo západní budova, vpravo brána)",
     ground=(np.linspace(-1,46,50),np.linspace(-1.2,-0.6,50)),
     rubble=[(16,26,1.6),(33,40,0.9)],
     notes=[(6.5,5.6,"zachovaný ochoz (rampa z nádvoří)"),(20.7,2.0,"průlom ~1,5 m – vybraný kámen, zkratka ze svahu"),(40,6.2,"u brány rozebranější")],ylim=(-2,10))

# 5 Brana vychod
gate=dict(x=0,L=7,H0=10,access=0.4,mid=0.92,seed=31,jag=0.4,
          openings=[op("brana",3.5,3.2,0,4.5,protect=True),op("strilna",0.9,0.2,4.6,1.0)],protect=[(1.4,5.6,5.8)])
def gate_extra(ax):
    ax.add_patch(Rectangle((1.3,0),4.4,5.6,fill=False,ec="#4a3c2a",lw=1.6,ls="-.",zorder=7))
    ax.text(5.9,5.0,"kapsa pro padací most",fontsize=8,color="#4a3c2a")
    for cx in (1.8,5.2): ax.add_patch(plt.Circle((cx,5.9),0.13,color="#2b2117",zorder=8))
    ax.text(5.9,6.1,"otvory pro řetězy",fontsize=8,color="#2b2117")
    ax.add_patch(Rectangle((-1.6,0),1.6,6.8,fc=STONE,ec=STONE_D)); ax.text(-0.8,7.1,"pilíř",ha="center",fontsize=8)
    for px in (9.5,13):
        ax.add_patch(Rectangle((px,-6),1.0,5.2,fc=STONE,ec=STONE_D))
    ax.plot([7.2,15.5],[-0.3,-4.8],color="#6b4a2a",lw=4); ax.text(12.5,-2.3,"spadlý trám mostu",fontsize=8,color="#6b4a2a")
    ax.text(11.3,-6.7,"mostní pilíře v příkopu",ha="center",fontsize=8)
gx=np.linspace(-3,18,100); gy=np.where(gx<8,0,np.where(gx<9,-(gx-8)*6,-6)); gy=np.where(gx>15,-6+(gx-15)*2,gy)
draw(axs[4],[gate],"5  BRÁNA – východní pohled (od příkopu), šířka 7 m",ground=(gx,gy),extra=gate_extra,
     notes=[(3.5,5.0,"oblouk stojí (chráněn), vrata a mříž pryč"),(1.0,1.2,"spodní ostění vylámaná do 2,5 m – oblouk „visí“"),(0.9,6.3,"střílna u brány – vysoko, ostění celé")],xlim=(-3,18),ylim=(-7,12))

# 6 Zapadni budova
wb=dict(x=0,L=12,H0=7,access=0.35,ap=(6,),corners=(),seed=41,jag=0.5,
        openings=[op("dvere",6,1.0,0,2.2,robbed="one",side="r")])
def wb_extra(ax):
    ax.add_patch(Rectangle((5.2,0),0.3,2.2,fc="#7d6a4f")); ax.text(5.3,5.6,"ostění + kapsa pro závoru",fontsize=8,ha="right")
    ax.text(6.9,5.6,"druhé ostění vylámané",fontsize=8)
draw(axs[5],[wb],"6  ZÁPADNÍ BUDOVA – západní pohled s brankou na špičku ostrohu, 12 m",extra=wb_extra,
     ground=(np.linspace(-1,13,40),-np.abs(np.linspace(-1,13,40)-6)*0.15),rubble=[(0.5,4,0.9),(8.5,11.5,1.1)],xlim=(-1,13),ylim=(-3,9))

# legenda
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
h=[Patch(fc=STONE,ec=STONE_D,label="dochované zdivo (~1540)"),Line2D([],[],ls="--",color=ORIG,label="původní obrys"),
   Patch(fc="white",ec=STONE_D,label="otvor"),Line2D([],[],ls=":",color=ORIG,label="původní otvor"),
   Patch(fc=CORE,hatch="xx",ec="#a8946f",label="vylámaný líc – jádro zdi"),Patch(fc=RUBBLE,label="suť"),
   Patch(fc="#3d3225",label="kapsy po trámech (úrovně stropů)")]
fig.legend(handles=h,loc="upper left",ncol=4,fontsize=10,frameon=False,bbox_to_anchor=(LM/Wtot,1-0.6/Htot))
fig.suptitle("Zřícenina Lapikus – odhad rozpadu ~1540: mírný přirozený rozpad + rozebírání podle dostupnosti a výšky  ·  rozvinuté pohledy",fontsize=15,fontweight="bold",x=LM/Wtot,ha="left",y=1-0.2/Htot)
plt.savefig(sys.argv[1],dpi=85)
