---
# orchestrace
type: reference
validity: valid
updated: {{date:YYYY-MM-DD}}
aliases: []
---
# Map: entities by place (Dataview)

Zkušební pohled 3 pro rozhodnutí Q1 (zadání 04 kap. 2.1 a 5.1), varianta Dataview. Umístění = `located_in`, prázdné se dědí od `parent` (zadání 03 kap. 1); dotaz prochází tři úrovně předků. Varianta Bases: `bases/map_entities_by_place.base`.

```dataview
TABLE WITHOUT ID key AS "Místo", rows.file.link AS "Entity", rows.kind AS "kind"
FROM "Entities"
WHERE type = "entity"
FLATTEN choice(length(located_in) > 0, located_in,
  choice(length(parent.located_in) > 0, parent.located_in,
  choice(length(parent.parent.located_in) > 0, parent.parent.located_in,
  choice(length(parent.parent.parent.located_in) > 0, parent.parent.parent.located_in,
  list("(bez umístění)"))))) AS place
GROUP BY place
SORT key ASC
```
