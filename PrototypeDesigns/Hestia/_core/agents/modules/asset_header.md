---
type: agent_module
module_id: asset_header
trigger: nový nebo změněný skript
requires: [file_safety]
modes: [vault]
validity: valid
updated: 2026-11-17
---
# Hlavička skriptu a dopad změny

## Kdy
Zakládáš nebo měníš skript nebo datový soubor projektu.

## Postup
1. Hlavička je kontrakt skriptu: první docstring (Python) nebo úvodní komentářový blok s řádky `klíč: hodnota`:
   - `entities`: entity, které skript vytváří nebo mění;
   - `docs`: dokumenty, které skript popisují nebo z něj vycházejí;
   - `build_step`: krok prototypování;
   - `domains`: dotčené domény.
2. Udržuj hlavičku aktuální při každé změně skriptu.
3. **Dopad změny**: skripty jsou mimo domény a jedna změna může změnit víc entit a dokumentů. Projdi všechny entity a dokumenty z hlavičky a z `asset_index`; dotčené oprav, ostatní nech.
4. Aktualizuj dokumentaci kroku v `Steps/` (nebo sdíleného kódu v `Steps/shared/`): skripty, spouštění, vstupy a výstupy.
5. Ruční úpravu v enginu, kterou skript nezná, vrať do skriptu (capture skript nebo úprava skriptu). Dokud se to nestane, zapiš rozdíl do `state` (*Co se liší*).

## Výstup
Aktuální hlavička, opravené dotčené dokumenty a dokumentace kroku; řádky do `changes.md` za každou dotčenou entitu.

## Známé pasti
- Opravit jen dokument, kvůli kterému se skript měnil, a přehlédnout další entity ze stejného skriptu.
- Nechat starou hlavičku: `asset_index` pak přiřadí skript špatným entitám.
