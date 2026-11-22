---
type: agent_module
module_id: lookup
trigger: otázka na obsah dokumentace
requires: []
modes: [vault, chat]
compile: listed
validity: valid
updated: 2026-11-22
---
# Vyhledávání v dokumentaci

## Kdy
Někdo se ptá, co dokumentace říká („Co víme o bráně?“, „Jakou střechu má kovárna?“), nebo potřebuješ ověřit fakt před zápisem (`canon_check`).

## Postup
1. **Ve vaultu** (i chat s připojenou složkou projektu) hledej příkazem `hestia.py find "<dotaz>"` (index dokumentů: název, `aliases`, nadpisy sekcí, entita, cesta; glosář; pod 3 výsledky doplní hledání v textu, `--text` vždy), ne `grep -r` přes vault. Z kandidátů čti jen shodné sekce (`hestia.py section <dokument> "<nadpis>"`); dokument nad `doc_summary_chars` nečti celý (modul `start`, *Čtení*). Starý index obnov `hestia.py doc_index --apply`. Když skript core spustit nejde (relace bez shellu nebo bez vhodného Pythonu), čti index, glosář a dokumenty přímo a v odpovědi výslovně uveď, že skript neběžel (index může být starý).
2. **V chatu bez vaultu** pracuj jen s balíčkem kontextu (`compose_context`) a s tím, co máš v tasku; co v něm není, nedomýšlej. **Bez balíčku** neodpovídej a řekni přesně, který balíček potřebuješ a jakým příkazem vznikne: `hestia.py compose_context --entity <Entita> --apply` (otázka o entitě), `--query "<otázka>"` (otázka napříč dokumenty), `--topic <kategorie nebo doména>`; nebo požádej o přístup k vaultu (připojenou složku projektu).
3. U otázky o entitě vezmi z hubu stav: návrh, realizace, cíl a režim (blok *Domény*).
4. Rozliš **návrh** (`design`, `spec`, `decision`), **realizaci** (`state`, skript, report Unrealu) a **zavržené** (`status: rejected`). Realizaci ověř čtecím dotazem nebo posledním reportem (modul `ue_lookup`), je-li to potřeba.
5. Když si zdroje odporují, nerozhoduj: vypiš rozpor a podle hierarchie zdrojů (12 kap. 3b.3) uveď, co platí. Zapiš otázku k dotčenému dokumentu, u rozporu mezi dokumenty i položku fronty pro Auditora.
6. `outdated`, `superseded` a `archived` dokumenty uváděj jen jako historii a označ je. Položky z `Inbox/` a nezařazené ze `Scratch/` jsou **neověřené**.

## Výstup
```markdown
**Odpověď:** <stručná odpověď, jen z dokumentace>

**Zdroje:**
- [[dokument#sekce]] – <typ>, <validity>, <návrh / realizace>, updated RRRR-MM-DD
- report Unrealu `ue_<entita>.json` (RRRR-MM-DD), je-li

**Stav:** návrh <N> / realizace <M> / cíl <T> (<režim>) – z hubu, je-li otázka o entitě
**Rozpory:** <tvrzení A [[…]]> × <tvrzení B [[…]]> → podle 12 kap. 3b.3 platí …; nebo „žádné“
**Neověřené:** položky z `Inbox/` a `Scratch/` (nezařazené)
**Mezery:** co v dokumentaci chybí → navržená otevřená otázka (kam)
```
Odpověď bez zdroje není povolená; „není zdokumentováno“ je platná odpověď.

## Známé pasti
- Doplnit odpověď z obecných znalostí nebo z odhadu; v dokumentaci to není, takže to patří do *Mezer*.
- Citovat zavržený návrh nebo zastaralý dokument jako platný.
- Vydávat návrh za realizaci („kovárna má pultovou střechu“, když to říká jen návrh).
- Číst celý vault místo indexu (`find`) nebo celý dlouhý dokument místo sekcí; je to pomalé a do kontextu se dostane šum.
- V chatu bez balíčku napsat jen „pošli podklady“; GameDesigner pak neví, co připravit.
- Pracovat s balíčky, když relace vidí vault přes připojenou složku (modul `start`, krok 0).
