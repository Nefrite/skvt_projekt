"""gen_constructions.py - vytvori constructions.json pro build_constructions.py (05_constructions)
Dodatecne stavby "druheho zabydleni" zriceniny: drevene vestavby ve vezi (tramy, prkna, pruvlak, schody, podesta)
a nastaveni volne suti. Rozmery veze sdili se zriceninou pres tools/ruin/tower_spec.py.

python gen_constructions.py <ruin_layout_draft.json> <vystup constructions.json> [<03_ruin/blocks/ruin_layout.json>]
Zastreseni u ostrohu bere polohy zdi z ruin_layout.json (vychozi ../../03_ruin/blocks/ruin_layout.json) a ostroh_spec.py.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ruin"))
from tower_spec import VEZ_F, VEZ_ST, spec as tower_spec
from ostroh_spec import spec as ostroh_spec

D = json.load(open(sys.argv[1]))
TS = tower_spec(D["tower"])
LT = TS["LT"]; H1, H2 = TS["HATCH1"], TS["HATCH2"]

floors = [dict(
    name="Vez_Patra", folder="Stavby/Vez", origin=TS["origin"], u=TS["UV"], v=TS["VV"], inner=TS["inner"],
    ref_z=VEZ_F, storey=VEZ_ST, levels=[1, 2], walls=["Vez_V", "Vez_Z", "Vez_J", "Vez_S"],   # tram jen kde zed u kapsy stoji
    beams=dict(v=TS["BEAM_V"], w=0.26, h=0.28, bearing=0.33),
    planks=dict(t=0.05, wmin=0.2, wmax=0.34, missing=0.04),
    girder=dict(u=TS["GIRD_U"], w=0.30, levels=[1, 2], post_v=[TS["GIRD_POST_V"]], post=0.25),
    hatches={"1": H1, "2": H2},
    # provizorni schody 60 st. podel tramu, cik-cak: do 1. patra stoupaji k vychodu (horni konec u vychodniho kraje otvoru),
    # do 2. patra k zapadu (horni konec se opira o pruvlak); z vystupu se prejde do sousedniho pole k dalsim schodum
    stairs=[dict(**{"from": 0, "to": 1}, axis="u", dir=1, u_top=H1[1], v=(H1[2] + H1[3]) / 2, angle=60, width=0.8),
            dict(**{"from": 1, "to": 2}, axis="u", dir=-1, u_top=H2[0], v=(H2[2] + H2[3]) / 2, angle=60, width=0.8)],
    # obnoveny ochoz pred puvodnim vstupem (zvenku Vez_S): 2 tramy zapustene v kapsach, prkna,
    # bez sloupku do zeme - jen kratke sikme vzpery pod tramy oprene o zed
    porch=dict(u=TS["DOOR_U"], level=1, v_wall=LT + 1.25, depth=1.3, width=2.6, beam_du=TS["PORCH_BEAM_DS"],
               beam=(0.24, 0.28), posts=False, braces=dict(dv=0.75, dz=0.75, w=0.14)),
    # uprava dreva: tar = dehtovane (masivni), raw = bez upravy (vnitrni velke plochy, schody), oil = morene olejem (jemna prace),
    # blood = morene krvi (venkovni ochoz), old = stare neosetrene, zasedle a zaprasene (prkna horniho patra - vic slunce a pocasi)
    finish=dict(beams="tar", girder="tar", posts="tar", heads="tar", planks="raw", planks_2="old", stairs="raw",
                porch_beams="blood", porch_braces="blood", porch_posts="blood", porch_planks="blood"))]

# --- zapadni cast u ostrohu: 2 sloupy u dveri ZBudova_V, pricka (vaznice), z ni 7 paprskovitych tramu na snizenou hradbu
#     (tramy lezi ve zlabcich koruny, presahuji vnejsi lic -> zaklad pro strechu, ktera se mirne zvazuje ke zdi)
LAY = json.load(open(sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "..", "..", "03_ruin", "blocks", "ruin_layout.json")))
OS = ostroh_spec(LAY["walls"])
frames = [dict(name="Ostroh_Krov", type="fan_roof", folder="Stavby/Ostroh", **OS,
               crossbeam=(0.30, 0.32), start_over=0.3,
               knee=dict(l=0.6, w=0.14, out=True),               # kratke sikme vzpery sloup - pricka, ven (pruchod mezi sloupy volny)
               # krytina: dehtovana prkna po spadu na latich, listy pres spary, kryci prkno pres kazdy tram
               roof=dict(lath=(0.05, 0.06), board_t=0.035, board_w=(0.22, 0.30), gap=0.015, batten=(0.06, 0.035), top_over=0.2,
                         lath_rows=(0.04, 0.35, 0.65, 0.9, 1.0), cover_w=0.36, flashing=None),   # lemovani u pricky: vyresi se jinak
               finish=dict(posts="tar", crossbeam="tar", beams="tar", knee="tar",
                           roof_boards="tar", roof_battens="tar", roof_laths="tar", roof_flashing="tar"))]

out = dict(version=1, units="UE cm (pozice), m (rozmery v ramu veze)",
           note="Drevene vestavby a sut. Zricenina (zdi, kapsy, dlazba) je v 03_ruin/blocks/ruin_layout.json.",
           rubble=dict(enabled=True, folder="Stavby/Sut"),
           floors=floors, frames=frames)
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print("stavby:", ", ".join(f["name"] for f in floors + frames), "| sut:", out["rubble"]["enabled"])
