---
# orchestrace
type: reference
validity: valid
updated: {{date:YYYY-MM-DD}}
aliases: []
---
# Entity × domain matrix (Dataview)

Zkušební pohled 2 pro rozhodnutí Q1 (zadání 04 kap. 2.1 a 5.1), varianta Dataview. Buňka: `depth/target`, ⚠ = mezera; „bez cíle“ = doména očekávaná podle `kind` (core `taxonomy/kinds.yaml`, v dotazu napevno) bez cíle. Varianta Bases: `bases/entity_domain_matrix.base`.

```dataview
TABLE WITHOUT ID file.link AS "Entita", kind AS "kind",
  choice(target_environment, default(depth_environment, 0) + "/" + target_environment + choice(default(depth_environment, 0) < target_environment, " ⚠", ""), choice(contains(list("place", "route"), kind), "bez cíle", "")) AS "environment",
  choice(target_structures, default(depth_structures, 0) + "/" + target_structures + choice(default(depth_structures, 0) < target_structures, " ⚠", ""), choice(contains(list("location", "structure", "room", "object", "district", "plot"), kind), "bez cíle", "")) AS "structures",
  choice(target_paths, default(depth_paths, 0) + "/" + target_paths + choice(default(depth_paths, 0) < target_paths, " ⚠", ""), choice(contains(list("place", "location", "route", "district"), kind), "bez cíle", "")) AS "paths",
  choice(target_npc, default(depth_npc, 0) + "/" + target_npc + choice(default(depth_npc, 0) < target_npc, " ⚠", ""), choice(contains(list("location", "character", "district", "plot"), kind), "bez cíle", "")) AS "npc",
  choice(target_gameplay, default(depth_gameplay, 0) + "/" + target_gameplay + choice(default(depth_gameplay, 0) < target_gameplay, " ⚠", ""), choice(contains(list("location", "structure", "character", "object", "system"), kind), "bez cíle", "")) AS "gameplay",
  choice(target_narrative, default(depth_narrative, 0) + "/" + target_narrative + choice(default(depth_narrative, 0) < target_narrative, " ⚠", ""), choice(contains(list("place", "location", "character", "district"), kind), "bez cíle", "")) AS "narrative"
FROM "Entities"
WHERE type = "entity"
SORT file.name ASC
```
