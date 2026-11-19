---
# orchestrace
type: knowhow
knowhow_kind: pitfall
tech: [python]
scope: instance
verified: 2026-11-17
validity: valid
updated: 2026-11-19
aliases: []
---
# Pasti: náhledy a kontroly mimo Unreal

<!-- Z KNOWHOW_hrad.md kap. 5.5 (pilot Lapikus, B6). -->

- **Náhled `preview3d.py` byl zrcadlový (opraveno 15. 11. 2026).** Unreal je levotočivý (X dopředu, Y vpravo), three.js pravotočivý. Souřadnice UE vykreslené přímo dají zrcadlový obraz: východ a západ prohozené. `render` proto převrací osu Y (středy, osy kvádrů, kamera). Náhledy vytvořené před opravou (`Stavby_ostroh_*_nahled.png`) mohou být zrcadlové. Vlastní kreslení (matplotlib, three.js) vždy ověř na něčem, co má jasnou stranu (věž je na východním konci paláce).
- **Krytina a dřevo podél líce zříceniny:** líc není rovina, kameny (i koruny v úrovni střechy) vystupují 1–3 cm. Nech od líce mezeru aspoň 3,5 cm a ověř průnikem (`common.collisions`); krytina kovárny 0,5 cm od `Palac_J` narážela do kamenů koruny v s = 27–29 (15. 11. 2026).
- **Patní kámen a prvek těsně u zdi:** co stojí do 10 cm od líce, kontroluj průnikem se zříceninou (`common.collisions`). Patní kámen 50 cm pod sloupem 10 cm od věže zasahoval do věže i do `Palac_J` (15. 11. 2026), proto má 36 cm.
