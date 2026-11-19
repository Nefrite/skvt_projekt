---
# orchestrace
type: knowhow
knowhow_kind: pitfall
tech: [mesh_generator]
scope: instance
verified: 2026-11-17
validity: valid
updated: 2026-11-19
aliases: []
---
# Pasti: generátor meshí

<!-- Z KNOWHOW_hrad.md kap. 5.4 (pilot Lapikus, B6). -->

- **Rotační tělesa (`mesh_props.add_lathe`):** obrys jde zdola od osy ven, po plášti nahoru a nahoře zpět k ose. Opačné pořadí = normály dovnitř (pád: kotouč brusu, obruče, okraj koše 14. 11. 2026). Kontrola `tools/checks/check_normals.py`.
- **Hranoly (`mesh_props.add_box`):** zaoblení hran musí být funkcí polohy (bod promítnutý na zaoblený kvádr), aby sousední stěny sdílely hranu. Posun lemu po normále každé stěny zvlášť dělal přečnívající lemy a štěrbiny – v UE to vypadalo jako vybarvené vnitřky (kovadlina, ponk, nářadí; opraveno 15. 11. 2026). `check_normals.py` u propů z prolínajících se dílů hlásí falešné poplachy – rozhoduje náhled `preview_meshes.py` (žádné trny a lemy na hranách).
