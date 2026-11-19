---
# orchestrace
type: reference
validity: valid
updated: 2026-11-19
aliases: []
# hra
domain: structures
entity: "[[Lapikus]]"
---
# Pravidla zabydlení

<!-- Z AGENT_Architekt_hrad.md kap. 2 a 5 (body 1–4, 6, 7, 10–12) a AGENT_GameDesign_hrad.md kap. 6 (pilot Lapikus, B7). -->

## Uvěřitelnost

Pravidla pro uvěřitelnost:
- dostavba šetří prací: využije zeď, kapsu, korunu, výklenek; nic se nestaví „do vzduchu“,
- všechno dřevo leží na něčem: na koruně zdi, v kapse, ve žlábku, na sloupu s příčkou,
- staré a nové musí jít od sebe poznat (zřícenina vs. pozdější dostavba).

## Konstrukce

1. **Uložení:** každý prvek má napsané, na čem leží: koruna (výška), kapsa, žlábek, sloup s příčkou, terén. Trám má uložení aspoň 20–25 cm, nadpraží 25 cm na každé straně.
2. **Rozpětí a průřezy** (orientačně, jako u stávajících staveb):
   - trám 22 × 24 cm do ~5–6 m, delší s podporou (sloup, příčka, vzpěra),
   - stropní trámy 26 × 28 cm po ~0,8–1 m, prkna 4,5–5 cm,
   - sloup 25–28 cm, příčka nebo průvlak 30 × 32 cm;
   - kulatina: **nosné a trvalé dřevo loupané** (srub, trámy podesty, krokve), **provizorní a nezpracované s kůrou** (přístřešky, palisáda, zábradlí, hromady). U každého prvku z kulatiny napiš průměr a jestli je s kůrou.
3. **Střecha:**
   - prkna po spádu s lištami fungují už od ~10–15°;
   - šindel chce víc (orientačně 25° a víc), došky ještě víc (45° a víc);
   - vždy napiš sklon, směr odvodnění a kam teče voda (okap přes zeď, žlab, sud).
4. **Kamenná dostavba:**
   - jedna řada 0,45 m, kámen jako v hradu;
   - vrch pod střechou, otvory zarovnané na řady;
   - nadpraží dřevěné, malta ve spárách tam, kde by zdí prosvítalo.
6. **Zřícenina vs. dostavba:**
   - zříceninu (03) měň jen tam, kde to bez toho nejde: snížení, žlábek, vybourání okna;
   - uveď to výslovně jako **„vyžaduje úpravu 03“**;
   - napiš i to, kterou část zříceniny je pak nutné přestavět (`Obvod`, `Palac`, `Ostroh`).
7. **Návaznost:** nesmí to kolidovat s tím, co stojí (kap. 3), ani s trasami hráče a herními místy z návrhu game designera.
10. **Posádka si ruinu upravuje:** co překáží, rozebere a kámen použije jinde (portál na podezdívky, kameny nároží pod krytem), a co má držet, zapustí (kůly do koruny, trám do kapsy). Takovou úpravu 03 navrhni rovnou, je uvěřitelnější než stavba kolem překážky.
11. **Kryty a zábrany:** za krytem nesmí zbýt místo, kam se dá stoupnout zvenku; podestu protáhni až ke krytu. Průzor je mezera nahoře mezi kůly, kůl v něm je rovně seříznutý a ráhna vedou pod průzory. Zábradlí směrem dovnitř hradu se u provizoria nedělá.
12. **Topení pro delší pobyt:** pec s nístějí a sopouchem do dymníku (teplo drží v hmotě, kouř nejde do místnosti), ne otevřené ohniště. Otevřená výheň patří do kovárny.

## Návrhy dostaveb

1. **Zřícenina a dostavby jsou oddělené.** Zřícenina (`03_ruin`: zdi, otvory, kapsy) se mění jen výjimečně. Dostavby (`05_constructions`) na ní stojí a nemění ji: kámen na koruně, trámy v kapsách nebo na koruně, dřevo, výplně. Když návrh potřebuje změnit zříceninu (snížit zeď, vysekat žlábek nebo kapsu, nový otvor), **výslovně to uveď** jako „vyžaduje úpravu 03“.
2. **Kotvení v ruině.** Napiš, o co se stavba opírá: kapsy po trámech, koruna zdi, sníženy úsek, výklenek, terén. Nic nesmí viset ve vzduchu.
3. **Materiál a technologie** odpovídají době a lidem (kap. 2): kámen z rozvalin, dřevo a kulatina s úpravou z kap. 4, hlína, proutí, kůra, plátno, lana, prkna. Žádné kovové konstrukce, sklo jen výjimečně. Vybavení skládej z hotových props (kap. 4).
4. **Hráč na prvním místě.** Každá stavba má herní účel: přístup, výhled, skrýš, orientační bod, příběh, překážka, zkratka. Uveď, co tam hráč dělá a jak se tam dostane, v mezích kap. 3.
5. **Čitelnost.** Rozliš původní hrad a pozdější zabydlení (materiál, provedení), aby hráč četl vrstvy příběhu.
6. **Návaznost.** Nové věci se nesmí bít s tím, co stojí, ani s tím, co je navržené (kap. 4): krov u ostrohu, dřevo ve věži, ochoz, dům a kovárna v paláci, podesta brány. **Ostroh má zvláštní účel**, s jeho obsazením (kdo tam bydlí) nepočítej, dokud ho Jirka nepopíše.

## Otevřené otázky

- [ ] **Etapy:** jak se ve hře přepnou (dvě verze levelu, skrytí a zobrazení sad actorů)? Stojí podesta brány už v etapě 1? — z AGENT_GameDesign_hrad, 2026-11-17
- [ ] **Spaní v etapě 1:** kde spí ti, kdo nejsou na hlídce (stan na nádvoří, nebo 1. patro věže)? Od toho závisí, jestli bude `Nadvori_Stan`. — z AGENT_GameDesign_hrad, 2026-11-17
- [ ] **Žebříky** (staveniště, půda domu): použitelné pro postavu, nebo jen kulisa? — z AGENT_GameDesign_hrad, 2026-11-17
- [ ] **Brána:** výstup na podestu; dá se brána obejít zřícenou jižní stranou východně od `Hradba_V`? — z AGENT_GameDesign_hrad, 2026-11-17
- [ ] **Suť pod `Vez_V`:** víc suti z průlomu by bylo uvěřitelné, ale zúží průchod mezi věží a `Hradba_V`. — z AGENT_GameDesign_hrad, 2026-11-17
- [ ] **Staveniště:** rozmístění hromad (kulatina, krokve, prkna, kámen) tak, aby cesta průchod v `Palac_S` → vchod → světnice a cesta po zápraží ke kovárně zůstaly volné 1,2 m. — z AGENT_GameDesign_hrad, 2026-11-17
- [ ] **Hlídka na věži:** ohniště a vybavení ve 2. patře návrh přístřešku neřeší. — z AGENT_GameDesign_hrad, 2026-11-17
