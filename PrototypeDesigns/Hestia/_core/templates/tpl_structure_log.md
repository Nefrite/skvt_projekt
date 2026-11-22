---
type: log
updated: {{date:YYYY-MM-DD}}
---
# Poznatky o struktuře

Podklad pro change requesty, připisuje se na **konec** (05 kap. 7.3, 07 kap. 9). Formát:
`| RRRR-MM-DD | kategorie | popis | dopad | navrhovaná změna | |`; svislítko v textu jako `\|`.
Buňka `cr` je prázdná, dokud se o CR nerozhodne; pak `cr: <ID>` (vyplní `export_cr`) nebo `cr: none`
(posouzeno, CR nebude). Pomlčku ani jiný text nepoužívat.
Kategorie: `friction`, `missing`, `surplus`, `collision`, `taxonomy`, `works`, `idea`.

| datum | kategorie | popis | dopad | navrhovaná změna | cr |
|---|---|---|---|---|---|
