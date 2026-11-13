"""preview3d.py - 3D nahled kamenu a dilcu bez Unrealu (three.js ve headless Chromiu, se stiny).
python preview3d.py ostroh <vystup.png> [--layout <ruin_layout.json>] [--no-roof]
Jako knihovna: render(boxes, views, out_png), stone_boxes(stones, colf, z0)
  boxes = [(stred (m), R 3x3 (sloupce = lokalni osy), polovicni rozmery (m), rgb)]
  views = [dict(title, eye=(x,y,z), target=(x,y,z), fov=35 nebo ortho=sirka_m)] -> mrizka obrazku (kazdy w x h)
Potrebuje: node, playwright (npm i playwright; npx playwright install chromium) a three (npm i three@0.160.0) v teto slozce."""
import json, math, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
def render(boxes, views, out_png, w=1000, h=700, cols=2):
    data = [[*c, *[R[i][j] for i in range(3) for j in range(3)], *e, *col] for c, R, e, col in boxes]
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
sun.position.set(cx/B.length-40,cy/B.length-55,cz/B.length+80);
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
    st = [s for n in ("Ostroh_Krov", "Ostroh_Dostavba", "Ostroh_Podlaha") for s in S["groups"].get(n, {}).get("stones", [])
          if roof or "|R" not in s.id]
    z0 = S["layout"]["plateau_z_cm"]
    bx = stone_boxes(ruin + st, lambda s: COL.get(s.cat, (0.6, 0.6, 0.6)), z0)
    V = [dict(title="zvenku od vychodu", eye=(-22, -9.5, 4.0), target=(-35.5, -11.5, 2.0), fov=45),
         dict(title="od severovychodu", eye=(-26, -26, 9), target=(-38, -13, 2), fov=42),
         dict(title="zevnitr k vychodu", eye=(-41.8, -12.0, 1.7), target=(-35.5, -11.0, 2.0), fov=62),
         dict(title="zevnitr k zapadu", eye=(-36.8, -11.6, 1.7), target=(-43.5, -10.8, 3.0), fov=62)]
    render(bx, V, out)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("preset", choices=["ostroh"]); ap.add_argument("out")
    ap.add_argument("--layout"); ap.add_argument("--no-roof", action="store_true")
    a = ap.parse_args()
    {"ostroh": ostroh}[a.preset](a.out, a.layout, not a.no_roof)
    print("nahled:", a.out)
