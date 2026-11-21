---
# orchestrace
type: knowhow
knowhow_kind: pitfall
tech: [python]
scope: instance
verified: 2026-11-21
validity: valid
updated: 2026-11-21
aliases: []
---
# Pasti: náhledy a kontroly mimo Unreal

<!-- Z KNOWHOW_hrad.md kap. 5.5 (pilot Lapikus, B6). -->

- **Náhled `preview3d.py` byl zrcadlový (opraveno 15. 11. 2026).** Unreal je levotočivý (X dopředu, Y vpravo), three.js pravotočivý. Souřadnice UE vykreslené přímo dají zrcadlový obraz: východ a západ prohozené. `render` proto převrací osu Y (středy, osy kvádrů, kamera). Náhledy vytvořené před opravou (`Stavby_ostroh_*_nahled.png`) mohou být zrcadlové. Vlastní kreslení (matplotlib, three.js) vždy ověř na něčem, co má jasnou stranu (věž je na východním konci paláce).
- **Krytina a dřevo podél líce zříceniny:** líc není rovina, kameny (i koruny v úrovni střechy) vystupují 1–3 cm. Nech od líce mezeru aspoň 3,5 cm a ověř průnikem (`common.collisions`); krytina kovárny 0,5 cm od `Palac_J` narážela do kamenů koruny v s = 27–29 (15. 11. 2026).
- **Patní kámen a prvek těsně u zdi:** co stojí do 10 cm od líce, kontroluj průnikem se zříceninou (`common.collisions`). Patní kámen 50 cm pod sloupem 10 cm od věže zasahoval do věže i do `Palac_J` (15. 11. 2026), proto má 36 cm.
- **Náhled bez `three` a `playwright` na počítači s projektem** (21. 11. 2026): `preview3d.py` potřebuje `tools/checks/node_modules/three` a playwright s Chromiem. Na Jirkově počítači nejsou a v cloudovém workspace se Chromium z `cdn.playwright.dev` nestáhne (proxy 403). Postup: na počítači vyexportuj kvádry a pohledy (`obydli_scene(S, stage)` → JSON do `_to_delete/`), v cloudu nainstaluj `npm install three playwright` a v kopii `preview3d.py` dej do `chromium.launch` `executablePath: '/usr/bin/google-chrome'` (systémový Chrome). PNG pak zkopíruj zpět do `05_constructions/`.
