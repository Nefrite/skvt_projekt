---
# orchestrace
type: reference
validity: valid
updated: 2026-11-19
aliases: []
---
# Structures status (Dataview)

Zkušební pohled 1 pro rozhodnutí Q1 (zadání 04 kap. 2.1 a 5.1), varianta Dataview (komunitní plugin; funguje až po jeho instalaci). Varianta Bases: `bases/structures_status.base`.

```dataview
TABLE WITHOUT ID key AS "status", rows.file.link AS "Entita", rows.depth_structures AS "depth", rows.target_structures AS "target", rows.parent AS "parent", rows.updated AS "updated"
FROM "Entities"
WHERE type = "entity" AND contains(list("structure", "room", "object"), kind)
SORT file.name ASC
GROUP BY status
SORT key ASC
```
