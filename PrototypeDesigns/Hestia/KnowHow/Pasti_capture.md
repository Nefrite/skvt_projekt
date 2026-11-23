---
# orchestrace
type: knowhow
knowhow_kind: pitfall
tech: [ue_python]
scope: instance
verified: 2026-11-23
validity: valid
updated: 2026-11-23
aliases: []
---
# Pasti: capture ručních úprav

<!-- Z KNOWHOW_hrad.md kap. 5.3 (pilot Lapikus, B6). -->

- **Capture ručních úprav (03, 05) jen po buildu** se stejnými meshi: capture porovnává instance v levelu s tím, co by build postavil; po změně meshů nebo os by staré instance vyšly jako smazané.
- **Vybavení (06) má jeden JSON (16. 11. 2026):** capture zapisuje polohy, otočení a velikost kusů přímo do `06_furnishing/furnishing.json` v rámu skupiny (`a`, `c`, `z` nad terénem, `x`, `pitch`, `roll`, `scale`), smazané kusy jako `removed`, kopie actorů (Alt+tah) jako nové kusy `manual`. `gen_furnishing.py` data slučuje (`furn_data.merge`), uložené polohy nepřepíše. Kopie kusu dostane mesh původního kusu (`mesh`), jinak by varianta meshe podle id vyšla jinak. Původní kus mezi kopiemi = actor nejblíž poloze z dat.
- **Capture vybavení s klíčem `ref` nad šikmým terénem musí odečítat terén v bodě `ref`, ne pod kusem (ověřeno 23. 11. 2026, `Brana_Straz_Vybaveni`):** kusy na vodorovné prkenné podlaze nebo podestě nad šikmým terénem mají společný `ref = (a, c)` a `build_props` (`05_constructions/zr_stavby/vybaveni.py`) počítá jejich výšku od `terr.z(*P(*it["ref"]))`. Pokud `apply_pose` v `06_furnishing/build_furnishing.py` při capture odečte `terr.z(x, y)` pod posunutým kusem místo `terr.z(*P(*it["ref"]))`, při dalším buildu nebo kontrole se kus posune o rozdíl výšek terénu `terr.z(ref) - terr.z(x, y)` (v průjezdu brány až o ±24 cm, takže zapadne do podlahy/koruny nebo visí ve vzduchu). Opraveno v `build_furnishing.apply_pose`: je-li u kusu `ref`, odečítá se terén v `ref`.
