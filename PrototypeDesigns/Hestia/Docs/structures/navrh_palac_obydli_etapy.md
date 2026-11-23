---
# orchestrace
type: design
validity: valid
derived_from: "[[navrh_palac_obydli_stred]]"
alternative_to: []
updated: 2026-11-23
aliases: []
# hra
status: in_progress
domain: structures
category: []
entity: "[[Palac_Obydli]]"
depth: 4
build_step: 05_constructions
assets: []
---
# Návrh: Palac_Obydli – plán stavby po etapách

## Souhrn
Jak se dům posádky staví po etapách: sady actorů, rozdělení po stavbách, pořadí stavění a zamčená sada `base`. Konstrukce domu je v [[navrh_palac_obydli_stred]], pec v [[navrh_palac_obydli_pec]], etapa 1 a staveniště v [[navrh_palac_obydli_stavenisko]], co stojí v [[stav_palac_obydli]].
- **Sady (0.1):** `stage:base` / `stage:final` / `stage:site`; etapa 1 = `base` + `site`, etapa 2 = `base` + `final`; dřevo `raw` v obou etapách.
- **Stavby (0.3)** se sadami a **pořadí stavění (0.4)**.
- **Zamčená `base` (0.7):** hodnoty v `palac_spec.py`, které dokončení domu nesmí změnit.

Vyčleněno z [[navrh_palac_obydli_stred]] kap. 0 (2026-11-23); číslování 0.x je zachované kvůli odkazům, výchozí stav (0.2, 0.2a) zůstal v návrhu domu.

## 0. Plán stavby po etapách
Dohodnuto s Jirkou 15.–21. 11. 2026. Co je z toho postavené a ověřené, je v [[stav_palac_obydli]].

### 0.1 Zásady

- **Jedna stavba, tři sady actorů.** Dům se počítá jednou jako hotový. Každý dílec patří do jedné sady a actory sady mají tag:

| Sada | Tag actoru | Etapa 1 | Etapa 2 | Obsah |
|---|---|---|---|---|
| základ | `stage:base` | vidět | vidět | co stojí už v etapě 1 a zůstává |
| dostavba | `stage:final` | skrytá | vidět | co se dodělá |
| staveniště | `stage:site` | vidět | skryté | nářadí, žebřík, kozy, vzpěry, hromady materiálu, ležící trámy |

- **Co je v etapě 1 postavené, v etapě 2 se neskrývá** a je to tentýž dílec na tomtéž místě. Skrývá se jen staveniště.
- **Přepnutí ve hře** = zobrazit a skrýt actory podle tagu (i kolizi). Dělá si ho Jirka v Blueprintu. Sady a tag jsou v `zrlib/config.py` (`STAGES`, `STAGE_TAG`), v datech stavby klíč `stage`.
- **Hráč domem jen prochází**, úkol se stavbou nesouvisí. Etapy mají dát dojem času.
- **Staveniště a etapa 1 jdou před dokončením domu** (Jirka 21. 11. 2026, zvýšená priorita). Funguje to proto, že etapa 1 ukazuje jen `base` + `site` a dokončení domu je celé v sadě `final`. Podmínkou je zamčená sada `base` (kap. 0.7).
- **Dřevo je surové (`raw`) v obou etapách**, krov i krytina. Dehtování může přijít jako pozdější třetí stav. Srub je loupaná kulatina se stejným materiálem v obou etapách.
- **Dveře a okenice** jsou v etapě 2 otevřené (kulisa, než se rozhýbou). **Žebříky** nejsou pro postavu použitelné (chybí animace); půda bude mít vlastní žebřík, staveništní zmizí.
- **Sklep** se neřeší. Jestli přijde, podřídí se stavbě.

### 0.3 Rozdělení po stavbách

| Stavba | Typ | Základ (`base`) | Dostavba (`final`) |
|---|---|---|---|
| `Palac_Obydli_Kamen` | `stone_fill` | srovnání obou příček na 1,4 m včetně zazdění jejich dveří; podezdívky severní stěny a příčky 0,45 × 0,45 m; maltové jádro | nic |
| `Palac_Obydli_Ohniste` | `hearth` | sokl, zdi pece, hliněná klenba, tmavý vnitřek pece, zídky plotny | sopouch, dymník, komín, železo (plotna, pás, poklop), uhlí pod plotnou |
| `Palac_Obydli_Krov` | `pult_roof` | 5 sloupů; východní kusy horní pozednice (s = 15,3–21,4) a střední vaznice (s = 14,85–21,4) se špalky na příčce a východní stěně; 6 krokví nad světnicí (s ≥ 16,0); 2 řady latí zavětrování | západní kusy pozednice a vaznice se špalkem na západní stěně; 6 krokví nad síní; latě, krytina, lemování u `Palac_J`, prostup komína |
| `Palac_Obydli_Srub` | `log_wall` | severní stěna světnice (9 řad), severní stěna síně jen spodní 3 řady s mezerou pro vchod, příčka, srub východní stěny | zbylých 6 řad severní stěny síně, srub západní stěny, prkenné štíty |
| `Palac_Obydli_Strop` | nový nebo rozšíření `tower_floor` | nic | trámky, výměna u komína se zavěšením dymníku, prkna |
| `Palac_Obydli_Podlaha` | `plank_floor` | nic | podlaha světnice |
| `Palac_Obydli_Okap` | `gutter` | nic | žlab se spádem k západu, rozsochy, sud; bez svodu |
| `Palac_Obydli_Vybaveni` | rozmístění props | nic | zárubně, dveře a okenice (otevřené), lůžka, stůl, truhly, police, ponk, dřevo, žebřík na půdu |
| `Palac_Obydli_Stavenisko` a hranice | `props`, celá stavba sada `site` | – | – |

- **Staveniště (`site`)**: obsah, polohy a kontroly jsou v [[navrh_palac_obydli_stavenisko]]. Zásoba materiálu se „spotřebuje“, proto mizí celá.
- **Stavební logika etapy 1** (od západu k východu, východ je dál): krokve nad světnicí leží na třech podporách, které už stojí (pozednice na 3 sloupech, vaznice na příčce a východní stěně, severní stěna). Západní sloupy stojí bez pozednice, proto mají vzpěry. Pec stojí dřív než podlaha. Nic se nestaví dřív, než má na čem ležet.

### 0.4 Pořadí stavění (ladí se hotový stav)

1. Sady etap v build skriptu, `palac_spec.py` → `obydli`, `Palac_Obydli_Kamen`, `Palac_Obydli_Ohniste`.
2. `Palac_Obydli_Krov` bez krytiny.
3. `Palac_Obydli_Srub` se štíty a otvory.
4. Staveniště a kontrola etapy 1 ([[navrh_palac_obydli_stavenisko]]). Podmínkou je zamčená `base` (kap. 0.7).
5. Krytina s lemováním a prostupem komína, strop se zavěšením dymníku, podlaha, okap (až po krytině, výšku bere z ní).
6. Vybavení (zárubně, dveře, okenice, nábytek).

Kroky 1–3 jsou postavené a ověřené v UE, krok 4 je postavený a čeká na vizuální kontrolu v UE ([[stav_palac_obydli]]).

### 0.7 Zamčená sada `base` a hranice sad

- **Hranice sad `base` / `final` je podle dat** (Jirka 21. 11. 2026): krokve od s ≥ 16,0 jsou `base` (`D_STAGE_S`), spoj pozednice je na sloupu 15,3, spoj vaznice na příčce 14,85, latě zavětrování jsou v s = 16,17–21,4, srub síně má v etapě 1 spodní 3 řady. Krokev s = 15,245 leží na spoji pozednice a nese ji hlavně západní kus, proto je `final`.
- **Pec v etapě 1** se ještě nepoužívá: kamenné části, klenba a tmavý vnitřek jsou `base`, ostatní `final` ([[navrh_palac_obydli_pec]]).
- **Zamčená `base`:** dokončení domu nesmí změnit tyto hodnoty v `palac_spec.py`: `D_PLATE`, `D_PURLIN`, `D_RAFTER`, `D_STAGE_S`, `D_BRACE_LATHS`, `D_LOG` (včetně `west_base_rows`), `D_SILL`, `D_FILL_TOP`, `D_DOOR_N`, `D_DOOR_P`, okénko světnice v `D_WINDOWS`, `D_OVEN` a úpravy 03 v části `Palac`. Při změně kterékoli z nich znovu proběhnou kontroly etapy 1 ([[navrh_palac_obydli_stavenisko]] kap. 9.4) a polohy staveniště; změnu schvaluje Jirka.
- **Krytina nemění latě zavětrování** (`pre_laths`, `base`): v jejich řadách položí jen západní část latí.
