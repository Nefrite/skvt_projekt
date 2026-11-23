---
type: agent_module
module_id: asset_work
trigger: výroba nebo změna knihovního assetu
requires: []
modes: [vault, chat]
compile: listed
validity: valid
updated: 2026-11-23
---
# Výroba knihovního assetu

## Kdy
Vyrábíš nebo měníš knihovní asset podle karty v `Assets/`. Modul má v profilu role Crafter, u jednoduchých assetů Builder (12 kap. 4.6 bod 3): jednoduchý = díl stavby z existujícího generátoru jen s jinými parametry nebo na míru (trám, prkno, sloup, kámen, kulatina), bez nového materiálu a textury; ostatní vyrábí Crafter.

## Postup
1. **Start:** `hestia.py agenda --role <Role>` ukáže karty `requested` s `owner` = tvá role (karty bez `owner` jen roli `asset_default_owner`, výchozí Crafter) a tvé `in_progress`, seřazené podle `priority` a data `requested`; karta, jejíž `depends_on` není aspoň `generated`, je označená jako blokovaná. Pořadí určuje GameDesigner.
2. **Převzetí:** jen karta s `owner` = tvá role, nebo bez `owner`; nastav `asset_status: in_progress` a `owner` = tvá role. Kartu s jiným `owner` nepřebírej; jde-li o jednoduchý asset pro tebe, domluv se se žadatelem.
3. **Před prací** přečti pravidla v `Assets/Konvence_assetu.md` (`hestia.py section Konvence_assetu "<sekce>"`: *Pivot*, *Osy*, *Rozměr a graybox*, *Pojmenování a varianty*, *Pravidla výroby*, *Verze a import*). Karta je neopakuje, uvádí jen odchylky.
4. **Po vygenerování** (`generated`): do *Účel a použití* osy, pivot a jak asset klást slovně (konvence odkazem) a vložený náhled `![[…png]]`; `asset_source` = generátor nebo zdroj a funkce. *Z kódu* je generovaný blok: `hestia.py asset_index --apply` a `hubs --apply` ho doplní z kódu (rozměr, sloty, materiál, verze); technické údaje do karty ručně nepiš.
5. **Obal:** ověř v bloku *Z kódu*, že se skutečný rozměr vejde do `envelope` (rozměr grayboxu). Když ne, `envelope` zvětši (zaokrouhleno nahoru na cm) a zapiš úkol pro role v `used_by`, které podle grayboxu rozvrhovaly (fronta, `code: role:<Role>`, 12 kap. 4.7). Teprve pak `generated`.
6. **Nové pravidlo** výroby (pivot, osy, materiály, generátor) zapiš do `Konvence_assetu`, ne do karty, katalogu ani kroku stavby. Pravidlo, které mění už vyrobené assety, = řádek v *Změnách konvence* a úkol pro výrobce ve frontě; kdy se provede, rozhodne GameDesigner.
7. **Po importu do UE** (`imported`): `ue_path` (poslední segment = jméno karty) a verze; požádej GameDesignera o čtení z UE (`hestia.py ue_query --assets --emit --asset <jméno> --apply`, spustit v editoru, `ue_query --import --assets --apply`, `hubs --apply`), v etapě 2 čti sám. Blok *Stav v UE* ukáže `current`, `outdated` (čeká na import) nebo `missing`. Žadatel pak nahradí graybox (`stand_in: none`).
8. **Změna tvaru:** nová verze v kódu a záznam v *Poznámkách*.
9. **`rejected`, `superseded`** (s `superseded_by`) nastavuješ s důvodem v *Poznámkách*; kartu nemažeš.
10. Kartu zkontroluj `hestia.py lint <karta>` a task uzavři `task_close`.

## Výstup
Karta ve stavu `in_progress`, `generated` nebo `imported` se sekcemi podle stavu; asset v kódu a v UE; případně úkol pro role v `used_by` a pravidlo v `Konvence_assetu`.

## Známé pasti
- `verified` nastavuje jen GameDesigner (§ *Vizuálně ověřeno*: kdo, kdy, verze) a má smysl až u verze `current` v bloku *Stav v UE*; agent ho nenastaví ani na pokyn jiné role.
- `generated` bez os, pivotu, náhledu nebo `envelope` (mesh, Blueprint): `lint` hlásí chybu, další role asset neumí položit.
- Ručně opsané rozměry nebo verze v kartě: zdroj pravdy je kód, blok *Z kódu* je generovaný.
- Zvětšit `envelope` bez úkolu pro role v `used_by`: jejich rozvržení podle grayboxu pak neplatí.
