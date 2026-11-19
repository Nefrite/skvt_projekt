---
# orchestrace
type: knowhow
knowhow_kind: pitfall
tech: [ue_python]
scope: instance
verified: 2026-11-17
validity: valid
updated: 2026-11-19
aliases: []
---
# Pasti: capture ručních úprav

<!-- Z KNOWHOW_hrad.md kap. 5.3 (pilot Lapikus, B6). -->

- **Capture ručních úprav (03, 05) jen po buildu** se stejnými meshi: capture porovnává instance v levelu s tím, co by build postavil; po změně meshů nebo os by staré instance vyšly jako smazané.
- **Vybavení (06) má jeden JSON (16. 11. 2026):** capture zapisuje polohy, otočení a velikost kusů přímo do `06_furnishing/furnishing.json` v rámu skupiny (`a`, `c`, `z` nad terénem, `x`, `pitch`, `roll`, `scale`), smazané kusy jako `removed`, kopie actorů (Alt+tah) jako nové kusy `manual`. `gen_furnishing.py` data slučuje (`furn_data.merge`), uložené polohy nepřepíše. Kopie kusu dostane mesh původního kusu (`mesh`), jinak by varianta meshe podle id vyšla jinak. Původní kus mezi kopiemi = actor nejblíž poloze z dat.
