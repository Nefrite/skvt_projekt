---
# orchestrace
type: reference
validity: valid
updated: 2026-11-23
aliases: []
# hra
domain: structures
entity: "[[Lapikus]]"
---
# Materiály a úpravy dřeva

<!-- Z AGENT_GameDesign_hrad.md kap. 4 a AGENT_Architekt_hrad.md kap. 4 (pilot Lapikus, B7). -->

Úpravy dřeva, které se ve hře používají:
- **dehet**: tmavé, masivní a venkovní dřevo,
- **bez úpravy**: vnitřní velké plochy,
- **olej**: jemná práce,
- **krev**: venkovní nátěr, tmavě červenohnědý,
- **staré**: zašedlé, zaprášené,
- **loupané**: čerstvě oloupaná kulatina, světlá (stavba v etapě 1).

Kulatina je s kůrou (provizorní stavby, nezpracovaný materiál) i loupaná (nosné a trvalé dřevo). Další materiály: kůra, proutí s mazaninou, lněné plátno, konopné lano, kované železo, kůže, sláma, houně.

Úpravy dřeva: `tar` (dehet, venkovní a masivní), `raw` (bez úpravy, vnitřní plochy), `oil` (jemná práce), `blood` (mořené krví, venkovní), `old` (staré, zašedlé), `peeled` (čerstvě loupaná kulatina, světlá).

Materiály navíc ke dřevu a kameni: kůra, čela kulatiny, lano, plátno, proutí, mazanina, výplň spár srubu, železo (s rzí a bez), kůže, pískovec, dřevěné uhlí, sláma, houně. **Chybí:** saze, udusaná hlína, třísky na zemi, oheň a kouř (VFX), tesařské kozy, hromady materiálu staveniště, plachta stanu.

## Otevřené otázky
- [ ] Přiřazení kůra / bez kůry podle staveb (návrh v [[CHECKLIST_assets_navrhy]] kap. 2.1): potvrdit, hlavně zábradlí brány, žlaby a rozpracovanou kulatinu — Steward, 2026-11-23
- [ ] Úprava loupané kulatiny srubu podle etapy: v etapě 1 `peeled`, v etapě 2 `peeled`, nebo `raw` (už ztmavlá)? Krov `raw` → `tar`? ([[CHECKLIST_assets_navrhy]] kap. 5) — Steward, 2026-11-23
- [ ] VFX ohně a kouře (výheň, ohniště, komíny) a saze: teď, nebo později s atmosférou? Pro kovárnu rozhodnuto „zatím ne“ ([[Rozhodnuti_zricenina]], 15. 11. 2026) — Steward, 2026-11-23
