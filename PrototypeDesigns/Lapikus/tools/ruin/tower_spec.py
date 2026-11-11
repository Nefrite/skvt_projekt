"""tower_spec.py - spolecne rozmery veze pro zriceninu (03, kapsy a otvory) i drevene vestavby (05, tramy, schody).
Kdyz se zmeni polohy tramu / pruvlaku / dveri, je potreba pregenerovat obe casti (gen_layout.py i gen_constructions.py)."""
import math

VEZ_F = 3150          # horni plocha kamenne podlahy prizemi (abs. cm)
VEZ_ST = 4.2          # vyska patra (m)
VEZ_C = 0.35          # vyska rady kamene ve vezi (m) - spary = urovne pater


def spec(T):
    """T = 4 rohy veze (osy zdi, UE cm): J-Z, J-V, S-V, S-Z. Vrati slovnik rozmeru v ramu veze
    (u od J-Z rohu podel jizni zdi, v od J-Z rohu na sever, metry)."""
    LT = math.hypot(T[1][0] - T[0][0], T[1][1] - T[0][1]) / 100            # strana veze (osy zdi), m
    UV = [(T[1][0] - T[0][0]) / LT / 100, (T[1][1] - T[0][1]) / LT / 100]
    VV = [(T[3][0] - T[0][0]) / LT / 100, (T[3][1] - T[0][1]) / LT / 100]
    # tramy rovnomerne po ~1.64 m (s pruvlakem uprostred staci), krajni tesne u zdi; kazde pole je dost siroke pro schody
    BEAM_V = [round(1.4 + i * (LT - 2.8) / 5, 3) for i in range(6)]
    bay = lambda i: [round(BEAM_V[i] + 0.13, 3), round(BEAM_V[i + 1] - 0.13, 3)]
    GIRD_U = round(LT / 2, 3)                                               # pruvlak uprostred veze (sever-jih pod tramy)
    U_TOP = round(GIRD_U + 0.17, 3)                                         # horni konec schodu se opira o pruvlak
    DOOR_U = round((1.25 + GIRD_U) / 2, 3)                                  # puvodni vstup: zevnitr mezi Z zdi a sloupem
    return dict(LT=LT, UV=UV, VV=VV, origin=T[0], BEAM_V=BEAM_V, GIRD_U=GIRD_U, GIRD_POST_V=round(LT / 2, 3),
                U_TOP=U_TOP, HATCH1=[U_TOP, round(U_TOP + 2.2, 3)] + bay(4),  # do 1. patra: pole u severni zdi
                HATCH2=[U_TOP, round(U_TOP + 2.2, 3)] + bay(3),               # do 2. patra: sousedni pole
                DOOR_U=DOOR_U, DOOR_S=round(LT - DOOR_U, 3), PORCH_BEAM_DS=1.1,
                inner=[1.25, LT - 1.25, 1.25, LT - 1.25])
