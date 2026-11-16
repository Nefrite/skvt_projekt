"""preview3d.py - 3D nahled kamenu a dilcu bez Unrealu (three.js ve headless Chromiu, se stiny).
python preview3d.py ostroh <vystup.png> [--layout <ruin_layout.json>] [--no-roof]
python preview3d.py kovarna <vystup.png>      kovarna ve vychodni mistnosti palace (Palac_Kovarna_*)
python preview3d.py brana <vystup.png> [--stage 1|2]    strazni stanoviste nad branami (Brana_*)
python preview3d.py obydli <vystup.png> [--stage 1|2]   dum v prostredni mistnosti (Palac_Obydli_*); etapa 1 = base + site, 2 = base + final
Jako knihovna: render(boxes, views, out_png), stone_boxes(stones, colf, z0)
  boxes = [(stred (m), R 3x3 (sloupce = lokalni osy), polovicni rozmery (m), rgb)]
  views = [dict(title, eye=(x,y,z), target=(x,y,z), fov=35 nebo ortho=sirka_m)] -> mrizka obrazku (kazdy w x h)
Potrebuje: node, playwright (npm i playwright; npx playwright install chromium) a three (npm i three@0.160.0) v teto slozce."""
import json, math, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
def render(boxes, views, out_png, w=1000, h=700, cols=2):
    # Unreal je levotocivy (X dopredu, Y vpravo, Z nahoru), three.js pravotocivy: souradnice UE vykreslene primo by daly
    # zrcadlovy obraz (vychod a zapad prohozene). Proto se osa Y prevraci (stred, osy kvadru, kamera); lokalni osa Y
    # kvadru se otoci zpet, aby matice zustala rotaci (kvadr je soumerny).
    mir = lambda R: [[R[0][0], -R[0][1], R[0][2]], [-R[1][0], R[1][1], -R[1][2]], [R[2][0], -R[2][1], R[2][2]]]
    data = [[c[0], -c[1], c[2], *[mir(R)[i][j] for i in range(3) for j in range(3)], *e, *col] for c, R, e, col in boxes]
    views = [dict(v, eye=(v["eye"][0], -v["eye"][1], v["eye"][2]), target=(v["target"][0], -v["target"][1], v["target"][2])) for v in views]
    three = open(os.path.join(HERE, "node_modules/three/build/three.min.js")).read()
    html = """<html><body style='margin:0;background:#fff'><div id=g style='display:grid;grid-template-columns:repeat(%d,%dpx)'></div>
<script>%s</script><script>
const B=%s, V=%s, W=%d, H=%d;
const scene=new THREE.Scene(); scene.background=new THREE.Color(0xf4f2ee);
scene.add(new THREE.HemisphereLight(0xffffff,0x8a8070,0.75));
const sun=new THREE.DirectionalLight(0xffffff,1.1); sun.position.set(-40,-55,80); sun.castShadow=true;
sun.shadow.mapSize.set(4096,4096); const sc=sun.shadow.camera; sc.left=-20;sc.right=20;sc.top=20;sc.bottom=-20;sc.near=1;sc.far=300; scene.add(sun);
const geo=new THREE.BoxGeometry(2,2,2); const mat=new THREE.MeshLambertMaterial({color:0xffffff});
const im=new THREE.InstancedMesh(geo,mat,B.length); im.castShadow=true; im.receiveShadow=true;
const m=new THREE.Matrix4(), c=new THREE.Color(); let cx=0,cy=0,cz=0;
B.forEach((b,i)=>{ m.set(b[3]*b[12],b[4]*b[13],b[5]*b[14],b[0], b[6]*b[12],b[7]*b[13],b[8]*b[14],b[1], b[9]*b[12],b[10]*b[13],b[11]*b[14],b[2], 0,0,0,1);
  im.setMatrixAt(i,m); im.setColorAt(i,c.setRGB(b[15],b[16],b[17])); cx+=b[0];cy+=b[1];cz+=b[2]; });
scene.add(im); sun.target.position.set(cx/B.length,cy/B.length,cz/B.length); scene.add(sun.target);
sun.position.set(cx/B.length-40,cy/B.length+55,cz/B.length+80);
const r=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true}); r.setSize(W,H); r.shadowMap.enabled=true; r.shadowMap.type=THREE.PCFSoftShadowMap;
const g=document.getElementById('g');
V.forEach(v=>{ let cam; if(v.ortho){const a=W/H; cam=new THREE.OrthographicCamera(-v.ortho/2,v.ortho/2,v.ortho/2/a,-v.ortho/2/a,0.1,500);} else cam=new THREE.PerspectiveCamera(v.fov||35,W/H,0.1,500);
  cam.up.set(0,0,1); cam.position.set(...v.eye); cam.lookAt(...v.target); r.render(scene,cam);
  const d=document.createElement('div'); d.style.position='relative'; const img=new Image(); img.src=r.domElement.toDataURL(); d.appendChild(img);
  const t=document.createElement('div'); t.textContent=v.title; t.style.cssText='position:absolute;left:12px;top:8px;font:600 20px sans-serif;color:#222'; d.appendChild(t); g.appendChild(d); });
document.title='done';
</script></body></html>""" % (cols, w, three, json.dumps(data), json.dumps(views), w, h)
    fd, path = tempfile.mkstemp(suffix=".html", dir=HERE); os.write(fd, html.encode()); os.close(fd)
    js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:%d,height:%d}}); await p.goto('file://%s'); await p.waitForFunction(()=>document.title=='done',null,{timeout:120000});
await p.screenshot({path:'%s',fullPage:true}); await b.close();})();""" % (w * cols, h, path, os.path.abspath(out_png))
    subprocess.run(["node", "-e", js], check=True, cwd=HERE); os.remove(path)

def stone_boxes(stones, colf, z0=0.0):
    out = []
    for s in stones:
        r_, p_, y_ = map(math.radians, (s.roll, s.pitch, s.yaw))
        cr, sr, cp, sp, cy, sy = math.cos(r_), math.sin(r_), math.cos(p_), math.sin(p_), math.cos(y_), math.sin(y_)
        Rz = [[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]]; Ry = [[cp, 0, -sp], [0, 1, 0], [sp, 0, cp]]; Rx = [[1, 0, 0], [0, cr, -sr], [0, sr, cr]]
        mul = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        R = mul(mul(Rz, Ry), Rx)
        out.append(((s.x / 100, s.y / 100, (s.z - z0) / 100), R, (s.sx / 200, s.sy / 200, s.sz / 200), colf(s)))
    return out


COL = {"face": (0.70, 0.66, 0.58), "core": (0.45, 0.43, 0.40), "frame": (0.80, 0.76, 0.68), "crown": (0.76, 0.74, 0.66),
       "floor": (0.80, 0.76, 0.68), "wood": (0.52, 0.44, 0.34), "wood_tar": (0.16, 0.12, 0.09), "wood_oil": (0.45, 0.30, 0.18),
       "wood_blood": (0.35, 0.14, 0.09), "wood_old": (0.50, 0.45, 0.38)}


def ostroh(out, layout=None, roof=True):
    """obytna cast u ostrohu: zvenku a zevnitr (krov, dostavba, podlaha)"""
    sys.path.insert(0, HERE); import common
    S = common.state(layout)
    X0, X1, Y0, Y1 = -4700, -3200, -2100, -300
    ruin = [s for w in S["walls"].values() for s in w["stones"] + w.get("loose", []) if X0 < s.x < X1 and Y0 < s.y < Y1]
    st = [s for n in ("Ostroh_Krov", "Ostroh_Dostavba", "Ostroh_Podlaha") for g in (S["groups"].get(n, {}),)
          for s in g.get("stones", []) + g.get("loose", []) if roof or "|R" not in s.id]
    z0 = S["layout"]["plateau_z_cm"]
    bx = stone_boxes(ruin + st, lambda s: COL.get(s.cat, (0.6, 0.6, 0.6)), z0)
    V = [dict(title="zvenku od vychodu", eye=(-22, -9.5, 4.0), target=(-35.5, -11.5, 2.0), fov=45),
         dict(title="od severovychodu", eye=(-26, -26, 9), target=(-38, -13, 2), fov=42),
         dict(title="zevnitr k vychodu", eye=(-41.8, -12.0, 1.7), target=(-35.5, -11.0, 2.0), fov=62),
         dict(title="zevnitr k zapadu", eye=(-36.8, -11.6, 1.7), target=(-43.5, -10.8, 3.0), fov=62)]
    render(bx, V, out)


def kovarna_scene(S):
    """kovarna ve vychodni mistnosti palace: (kvadry, pohledy) - zricenina kolem + stavby Palac_Kovarna_*"""
    fr = next(f for f in S["data"]["frames"] if f["name"] == "Palac_Kovarna_Pristresek")
    O, U, V = fr["origin"], fr["u"], fr["v"]
    sn = lambda x, y: (((x - O[0]) * U[0] + (y - O[1]) * U[1]) / 100, ((x - O[0]) * V[0] + (y - O[1]) * V[1]) / 100)
    P = lambda s, n, z: ((O[0] + (U[0] * s + V[0] * n) * 100) / 100, (O[1] + (U[1] * s + V[1] * n) * 100) / 100, z)
    ruin = [s for w in S["walls"].values() for s in w["stones"] + w.get("loose", []) if 18 < sn(s.x, s.y)[0] < 35 and -3 < sn(s.x, s.y)[1] < 13]
    new = [s for n, g in S["groups"].items() if n.startswith("Palac_Kovarna") for s in g.get("stones", []) + g.get("loose", [])]
    new += [s for n, g in S.get("furn", {}).items() if n.startswith("Palac_Kovarna") for s in g.get("loose", [])]   # vybaveni (06)
    z0 = S["terr"].z(*[c * 100 for c in P(*fr["ref"], 0)[:2]])
    col = dict(COL, wood=(0.66, 0.54, 0.38), face=(0.60, 0.55, 0.48), daub=(0.72, 0.60, 0.42), charcoal=(0.10, 0.10, 0.11))   # nove drevo svetlejsi, kamen vyhne tmavsi nez zricenina
    bx = stone_boxes(ruin, lambda s: COL.get(s.cat, (0.6, 0.6, 0.6)), z0) + \
         stone_boxes(new, lambda s: (0.50, 0.47, 0.42) if s.loose and s.cat == "face" else col.get(s.cat, (0.6, 0.6, 0.6)), z0)
    V_ = [dict(title="ze dvorku od severu", eye=P(27.2, 8.4, 1.7), target=P(28.6, 2.5, 2.0), fov=62),
          dict(title="shora od severozapadu", eye=P(19.5, 13.5, 11.0), target=P(28.2, 3.0, 2.0), fov=40),
          dict(title="zevnitr od ponku k vyhni", eye=P(26.4, 1.7, 1.7), target=P(30.6, 2.6, 2.3), fov=68),
          dict(title="pohled od severu (kolmo)", eye=P(28.0, 30.0, 2.6), target=P(28.0, 3.0, 2.6), ortho=10.5),
          dict(title="zvenku od zapadu (stena, okap, sud)", eye=P(20.5, 7.5, 2.4), target=P(25.5, 3.0, 1.6), fov=55),
          dict(title="strecha u komina (shora)", eye=P(27.0, 4.5, 7.5), target=P(30.0, 1.4, 4.4), fov=45),
          dict(title="okap a sud zblizka", eye=P(22.6, 6.8, 1.9), target=P(24.8, 5.2, 1.6), fov=50),
          dict(title="lemovani u Palac_J zevnitr", eye=P(26.0, 4.5, 2.2), target=P(29.0, 0.8, 3.6), fov=60)]
    return bx, V_


def obydli_scene(S, stage=2):
    """dum v prostredni mistnosti palace: (kvadry, pohledy); stage 1 = sady base + site, 2 = base + final"""
    fr = next(f for f in S["data"]["addons"] if f["name"] == "Palac_Obydli_Kamen")
    O, U, V = fr["origin"], fr["u"], fr["v"]
    sn = lambda x, y: (((x - O[0]) * U[0] + (y - O[1]) * U[1]) / 100, ((x - O[0]) * V[0] + (y - O[1]) * V[1]) / 100)
    P = lambda s, n, z: ((O[0] + (U[0] * s + V[0] * n) * 100) / 100, (O[1] + (U[1] * s + V[1] * n) * 100) / 100, z)
    ruin = [s for w in S["walls"].values() for s in w["stones"] + w.get("loose", []) if -1.5 < sn(s.x, s.y)[0] < 25.5 and -3 < sn(s.x, s.y)[1] < 13]
    show = ("base", "site") if stage == 1 else ("base", "final")
    new = [s for n, g in S["groups"].items() if n.startswith("Palac_Obydli") for s in g.get("stones", []) + g.get("loose", []) if s.stage in show]
    z0 = S["terr"].z(*[c * 100 for c in P(*fr["ref"], 0)[:2]])
    col = dict(COL, wood=(0.66, 0.54, 0.38), face=(0.80, 0.68, 0.50), daub=(0.72, 0.60, 0.42), charcoal=(0.10, 0.10, 0.11), iron=(0.25, 0.26, 0.28))   # novy kamen okrove, at je videt
    bx = stone_boxes(ruin, lambda s: COL.get(s.cat, (0.6, 0.6, 0.6)), z0) + stone_boxes(new, lambda s: col.get(s.cat, (0.6, 0.6, 0.6)), z0)
    V_ = [dict(title="od nadvori pruchodem (etapa %d)" % stage, eye=P(16.6, 12.6, 1.7), target=P(15.0, 4.0, 1.2), fov=62),
          dict(title="shora od severozapadu", eye=P(4.0, 18.0, 11.0), target=P(15.5, 3.5, 2.0), fov=42),
          dict(title="shora od severovychodu", eye=P(27.0, 17.0, 10.0), target=P(16.0, 3.5, 2.0), fov=42),
          dict(title="pohled od severu (kolmo)", eye=P(15.75, 30.0, 2.6), target=P(15.75, 6.2, 2.6), ortho=14.0),
          dict(title="svetnice: od vychodni steny k pricce", eye=P(20.2, 4.9, 1.7), target=P(15.0, 2.6, 2.0), fov=72),
          dict(title="svetnice: pec od severovychodu", eye=P(19.4, 4.6, 1.7), target=P(16.8, 1.4, 1.2), fov=60),
          dict(title="ze zaprazi k pruchodu ke kovarne", eye=P(17.0, 7.9, 1.7), target=P(22.5, 7.6, 1.0), fov=68),
          dict(title="pudorys (sever nahore)", eye=P(15.75, 4.4, 40.0), target=P(15.75, 4.6, 0.0), ortho=15.0)]
    return bx, V_


def brana_scene(S, stage=2):
    """strazni stanoviste nad branami: (kvadry, pohledy); stage 1 = sady base + site, 2 = base + final. Vysky absolutne (UE Z)."""
    ad = next(f for f in S["data"]["addons"] if f["name"] == "Brana_Straz_Podesta")
    O, U, V = ad["origin"], ad["u"], ad["v"]
    ud = lambda x, y: (((x - O[0]) * U[0] + (y - O[1]) * U[1]) / 100, ((x - O[0]) * V[0] + (y - O[1]) * V[1]) / 100)
    z0 = S["layout"]["plateau_z_cm"]
    P = lambda u, d, z: ((O[0] + (U[0] * u + V[0] * d) * 100) / 100, (O[1] + (U[1] * u + V[1] * d) * 100) / 100, (z - z0) / 100)
    ruin = [s for w in S["walls"].values() for s in w["stones"] + w.get("loose", []) if -9 < ud(s.x, s.y)[0] < 14 and -6 < ud(s.x, s.y)[1] < 16]
    show = ("base", "site") if stage == 1 else ("base", "final")
    new = [s for n, g in S["groups"].items() if n.startswith("Brana_") for s in g.get("stones", []) + g.get("loose", []) if s.stage in show or s.stage is None]
    col = dict(COL, wood=(0.66, 0.54, 0.38), face=(0.80, 0.68, 0.50), bark=(0.36, 0.27, 0.20))
    bx = stone_boxes(ruin, lambda s: COL.get(s.cat, (0.6, 0.6, 0.6)), z0) + \
         stone_boxes(new, lambda s: (0.42, 0.33, 0.24) if s.bark else col.get(s.cat, (0.6, 0.6, 0.6)), z0)
    zt = ad["z"] + 30
    V_ = [dict(title="od vychodu pred branou (etapa %d)" % stage, eye=P(21.0, 2.0, 3250), target=P(7.2, 3.0, 3450), fov=45),
          dict(title="shora od severozapadu", eye=P(-8.0, -9.0, 4700), target=P(3.6, 3.0, zt), fov=42),
          dict(title="z prujezdu vzhuru k podeste", eye=P(1.6, 5.2, 3200), target=P(4.6, 2.2, zt), fov=70),
          dict(title="z podesty k vychodu", eye=P(1.0, 4.4, zt + 165), target=P(7.2, 2.6, zt + 110), fov=70),
          dict(title="z nadvori od zapadu", eye=P(-9.0, 4.0, 3300), target=P(0.0, 3.2, 3420), fov=50),
          dict(title="pudorys (sever nahore)", eye=P(3.6, 3.3, 7500), target=P(3.6, 3.1, 3000), ortho=14.0)]
    return bx, V_


def brana(out, layout=None, stage=2):
    sys.path.insert(0, HERE); import common
    render(*brana_scene(common.state(layout), stage), out)


def obydli(out, layout=None, stage=2):
    sys.path.insert(0, HERE); import common
    render(*obydli_scene(common.state(layout), stage), out)


def kovarna(out, layout=None):
    sys.path.insert(0, HERE); import common
    render(*kovarna_scene(common.state(layout)), out)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("preset", choices=["ostroh", "kovarna", "obydli", "brana"]); ap.add_argument("--stage", type=int, default=2); ap.add_argument("out")
    ap.add_argument("--layout"); ap.add_argument("--no-roof", action="store_true")
    a = ap.parse_args()
    if a.preset == "kovarna": kovarna(a.out, a.layout)
    elif a.preset == "obydli": obydli(a.out, a.layout, a.stage)
    elif a.preset == "brana": brana(a.out, a.layout, a.stage)
    else: ostroh(a.out, a.layout, not a.no_roof)
    print("nahled:", a.out)
