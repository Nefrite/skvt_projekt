# NPC – obecné chování (StateTree): potulování a hlídkování

Podklady pro NPC, které nejsou společné s hráčem. Obecné chování NPC:

| Chování | Popis | Stav |
|---|---|---|
| **Potulování** (Wander) | NPC chodí na náhodná místa v okolí svého výchozího bodu a chvíli postojí | tento návod |
| **Hlídkování** (Patrol) | NPC obchází hlídkovací body v daném pořadí (dokola nebo tam a zpět), na každém počká | tento návod |
| **Posedávání** (Sit) | NPC si sedne na volné sedátko | později (navazuje na `../01_sitting`) |

AI systém: **StateTree** (StateTree AI Component). Behavior Tree varianta v projektu zůstává jen jako ukázka.

## Obsah složky

| Soubor | K čemu |
|---|---|
| `README_NPC.md` | Tento návod |
| `npc_nav_bounds.py` | Vytvoří / upraví NavMeshBoundsVolume přes vybrané actory (landscape, podlaha) |
| `npc_make_patrol_route.py` | Z vybraných hlídkovacích bodů vytvoří trasu, přejmenuje body, přiřadí trasu vybraným NPC |
| `npc_report.py` | Kontrola: NPC a body na navmeshi, existence cesty mezi body. Výstup `Saved/NPCReport.csv` |

Skripty: **File → Execute Python Script…** (plugin **Python Editor Script Plugin**). Běží jen v editoru, chování ve hře řeší StateTree a Blueprinty.

---

## 0. Co už v projektu je (stav 11. 11. 2026)

Složka `Content/Skvt/Characters/NPC`:

| Asset | Co to je | Stav / problém |
|---|---|---|
| `BP_NPC_base` | Character, `SKM_Manny_Simple`, fialové materiály | používá šablonový **`ABP_Manny`** |
| `Nav_Jump` | NavLinkProxy (smart link pro skok NPC) | použitelný |
| `BehaviorTrees/AIC_BT_NPCBase` | AIController, Run Behavior Tree `BT_NPCBase` | funkční |
| `BehaviorTrees/BB_BT_NPCBase` | Blackboard (jen SelfActor + objekt) | |
| `BehaviorTrees/BT_NPCBase` | Sequence → `BTTask_Follow` | sledování hráče |
| `BehaviorTrees/Tasks/BTTask_Follow` | AI MoveTo na `TargetActor` | |
| `BehaviorTrees/BP_NPC_BT_base` | potomek `BP_NPC_base` (modré mat.), AI Controller = AIC_BT | |
| `StateTrees/AIC_ST_NPCBase` | AIController | **chybí StateTree AI komponenta** |
| `StateTrees/STAI_NPCbase` | StateTree, jen stav Root | **schéma `StateTreeComponentSchema`** (obecné, ne AI) |
| `StateTrees/BP_NPC_ST_base` | potomek `BP_NPC_base`, PawnSensing | **odkaz na neexistující `/Game/Skvt/Systems/HealthSystem/SkvtHealthComponent`** |

Další zjištění:
- **Žádná mapa nemá NavMeshBoundsVolume** → NPC se zatím nemají kde pohybovat.
- V mapách není umístěné žádné NPC.
- Pluginy **StateTree** a **GameplayStateTree** jsou zapnuté.
- Upstream repozitář kurzu (`upstream/Stream6`) obsahuje starší rozpracované NPC (`STT_GoToRandomLocation`, `STT_SetSpeed`, `BPC_SkvtHealth`). Do této větve se **nemergují** (jiná verze `BP_SkvtBaseChar`), slouží jen jako inspirace.

---

## 1. Úklid a příprava

1. **`BP_NPC_ST_base`:** otevři. Komponenta `SkvtHealthComponent` je rozbitá (asset neexistuje) → vyber ji v Components a smaž. Zkompiluj, ulož. (Zdraví se doplní později vlastním systémem.)
2. **`STAI_NPCbase`** nech být (jiné schéma nejde změnit). Nový strom vznikne v kroku 7. Starý pak lze smazat.
3. **PawnSensing** v `BP_NPC_ST_base` nech, zatím se nepoužívá (později AI Perception).
4. Nová složka `Content/Skvt/Characters/NPC/Patrol` (trasy) a `Content/Skvt/Characters/NPC/StateTrees/Tasks` (úlohy StateTree).

---

## 2. Navmesh v mapě

Bez navmeshe NPC nikam nedojde.

1. Otevři mapu (např. `LapikusPrototypeMap` nebo testovací `SkvtProjectMap`).
2. Vyber, co má navmesh pokrýt (Landscape, podlahu…).
3. **Execute Python Script → `npc_nav_bounds.py`** → vznikne `NavBounds_Auto` (+ automaticky `RecastNavMesh`).
4. Klávesa **P** ve viewportu → zelená plocha = kam NPC dojde.

Ručně: Place Actors → **Nav Mesh Bounds Volume**, roztáhnout přes oblast.

Na velkém landscapu (252 × 252 m) chvíli trvá generování. Pokud je potřeba zrychlit, v `RecastNavMesh` zvyš **Cell Size** (např. 20).
Skoky přes překážky: `Nav_Jump` (NavLinkProxy) umístit na hranu, oba konce na navmesh.

---

## 3. Pawn NPC: `BP_NPC_base` a `BP_NPC_ST_base`

**`BP_NPC_base`** (společný základ všech NPC):

| Kde | Nastavení | Proč |
|---|---|---|
| Mesh → Anim Class | **`ABP_SkvtCharacter`** místo `ABP_Manny` | stejné animace jako hráč (Idle, Move, Stop, IdleBreak) |
| Character Movement → Nav Movement → **Use Acceleration for Paths** | **zapnuto** | **Důležité:** bez toho AI nastavuje rychlost přímo, akcelerace je 0 a ABP (podmínka `Has Acceleration`) postavu nikdy nerozejde |
| Character Movement → Orient Rotation to Movement | zapnuto | NPC se otáčí po směru chůze |
| Character Movement → Rotation Rate Z | 270 | plynulé otáčení |
| Class Defaults → Use Controller Rotation Yaw | vypnuto | |
| Character Movement → Max Walk Speed | 160 | výchozí chůze (vzorek Walk v blendspace je 150) |

ABP: proměnné pro sezení hráče (`SkvtCharRef`) u NPC zůstanou prázdné, `Is Valid` větev se přeskočí. Nic se nerozbije.

**`BP_NPC_ST_base`** (potomek):
- Class Defaults → **AI Controller Class = `AIC_ST_NPCBase`**
- **Auto Possess AI = Placed in World or Spawned**

---

## 4. AI Controller: `AIC_ST_NPCBase`

1. Components → **Add → StateTree AI** (`StateTreeAIComponent`).
2. Details komponenty: **State Tree** = `ST_NPC` (vytvoříš v kroku 7, pak se sem vrať), **Start Logic Automatically** = zapnuto.
3. Zkompiluj, ulož.

---

## 5. Data a logika NPC v `BP_NPC_ST_base`

### 5.1 Enum `E_NPCBehavior`

`Content/Skvt/Characters/NPC`: **Blueprint → Enumeration** → `E_NPCBehavior`, hodnoty:
`Auto`, `Idle`, `Wander`, `Patrol`.

`Auto` = hlídkuje, pokud má trasu, jinak se potuluje.

### 5.2 Proměnné

| Proměnná | Typ | Výchozí | Instance Editable | K čemu |
|---|---|---|---|---|
| `Behavior` | E_NPCBehavior | Auto | ✅ | zvolené chování |
| `PatrolRoute` | BP_PatrolRoute (Object Ref) | – | ✅ | trasa (krok 6) |
| `WanderRadius` | Float | 800 | ✅ | poloměr potulování (cm) |
| `WanderMinStep` | Float | 250 | ✅ | minimální délka jednoho přesunu |
| `WanderWaitMin` / `WanderWaitMax` | Float | 2 / 6 | ✅ | čekání mezi přesuny (s) |
| `WalkSpeed` | Float | 150 | ✅ | rychlost při potulování |
| `PatrolSpeed` | Float | 180 | ✅ | rychlost při hlídkování |
| `HomeLocation` | Vector | – | | střed potulování (= místo startu) |
| `ShouldPatrol` / `ShouldWander` | Boolean | false | | čte StateTree |
| `MoveTarget` | Vector | – | | kam jít (čte StateTree) |
| `WaitTime` | Float | 0 | | jak dlouho čekat (čte StateTree) |
| `PatrolIndex` | Integer | −1 | | aktuální bod trasy |
| `PatrolDirection` | Integer | 1 | | směr u trasy tam a zpět |

### 5.3 BeginPlay → funkce `InitBehavior`

```
SET HomeLocation = Get Actor Location
HasRoute = Is Valid(PatrolRoute) AND PatrolRoute.Points Length > 0
Switch on E_NPCBehavior (Behavior):
  Auto   → ShouldPatrol = HasRoute,  ShouldWander = NOT HasRoute
  Patrol → ShouldPatrol = HasRoute,  ShouldWander = false
  Wander → ShouldPatrol = false,     ShouldWander = true
  Idle   → obojí false
```
Pokud Event BeginPlay v `BP_NPC_ST_base` ještě neexistuje, přidej ho. Pokud existuje v `BP_NPC_base` i tady, v potomkovi zapoj **Parent: BeginPlay** (pravý klik na event → Add Call to Parent Function).

### 5.4 Funkce `SelectWanderPoint` (výstup Boolean `Success`)

```
SET Character Movement → Max Walk Speed = WalkSpeed
For Loop 1..5:
   Get Random Reachable Point In Radius (Origin = HomeLocation, Radius = WanderRadius)
   → pokud Return Value AND Distance(Random Location, Get Actor Location) > WanderMinStep:
        SET MoveTarget = Random Location
        SET WaitTime = Random Float in Range (WanderWaitMin, WanderWaitMax)
        Return Success = true
Return Success = false
```

### 5.5 Funkce `SelectNextPatrolPoint` (výstup Boolean `Success`)

```
Is Valid(PatrolRoute) AND PatrolRoute.GetPointCount > 0 → jinak Return false
SET Character Movement → Max Walk Speed = PatrolSpeed
PatrolIndex < 0 ?
   ano → SET PatrolIndex = PatrolRoute.FindNearestIndex(Get Actor Location)
   ne  → PatrolRoute.GetNextIndex(PatrolIndex, PatrolDirection) → SET PatrolIndex, SET PatrolDirection
SET MoveTarget = PatrolRoute.GetPointLocation(PatrolIndex)
SET WaitTime   = PatrolRoute.GetPointWait(PatrolIndex)
Return Success = true
```
NPC začne u nejbližšího bodu trasy, ne nutně u prvního.

---

## 6. Hlídkovací trasa: `BP_PatrolPoint` a `BP_PatrolRoute`

Složka `Content/Skvt/Characters/NPC/Patrol`. Názvy proměnných musí přesně sedět (používají je skripty).

### 6.1 `BP_PatrolPoint` (Actor)

| Komponenta | Nastavení |
|---|---|
| `DefaultSceneRoot` | bod na zemi |
| `Billboard` | Sprite např. `S_TargetPoint` (nebo libovolná ikona), Hidden in Game |
| `Arrow` | Hidden in Game (směr pohledu – pro pozdější rozšíření) |

| Proměnná | Typ | Výchozí | Instance Editable |
|---|---|---|---|
| `WaitTime` | Float | 2.0 | ✅ |

### 6.2 `BP_PatrolRoute` (Actor)

| Komponenta | Nastavení |
|---|---|
| `DefaultSceneRoot` | |
| `RouteSpline` (Spline) | jen vizualizace trasy v editoru; Hidden in Game. Pro trvalé zobrazení zaškrtni **Draw Debug** |

| Proměnná | Typ | Výchozí | Instance Editable |
|---|---|---|---|
| `Points` | **Array** of BP_PatrolPoint (Object Ref) | prázdné | ✅ |
| `PingPong` | Boolean | false | ✅ (false = dokola, true = tam a zpět) |

**Funkce** (všechny Pure, kromě nutnosti):

| Funkce | Vstup | Výstup | Logika |
|---|---|---|---|
| `GetPointCount` | – | Integer | `Points → Length` |
| `GetPointLocation` | Index | Vector | `Points[Index] → Get Actor Location` |
| `GetPointWait` | Index | Float | `Points[Index] → WaitTime` |
| `FindNearestIndex` | Location | Integer | For Each Points: nejmenší `Vector Distance` → index |
| `GetNextIndex` | Index, Direction | NewIndex, NewDirection | viz níže |

`GetNextIndex`:
```
Count = GetPointCount
Count <= 1 → NewIndex = 0, NewDirection = Direction
PingPong = false → NewIndex = (Index + 1) % Count, NewDirection = 1
PingPong = true:
   Next = Index + Direction
   Next >= Count OR Next < 0 → Direction = −Direction, Next = Index + Direction
   NewIndex = Next, NewDirection = Direction
```

**Construction Script** (vykreslení trasy):
```
RouteSpline → Clear Spline Points
For Each Points (Is Valid) → RouteSpline → Add Spline Point (Location = Get Actor Location, Coordinate Space = World)
RouteSpline → Set Closed Loop = NOT PingPong AND Points Length > 2
```
Construction Script se přepočítá při posunu trasy, ne při posunu bodu. Po přesunu bodů trasu vyber a spusť znovu `npc_make_patrol_route.py` (s trasou ve výběru), nebo trasou lehce pohni.

---

## 7. StateTree `ST_NPC`

### 7.1 Vytvoření

1. `Content/Skvt/Characters/NPC/StateTrees`: pravý klik → **Artificial Intelligence → State Tree** → schéma **StateTree AI Component**.
2. Název `ST_NPC`.
3. Otevři, v panelu **Schema** (nebo Asset Details):
   - **AI Controller Class** = `AIC_ST_NPCBase`
   - **Context Actor Class** = `BP_NPC_ST_base`

Díky Context Actor Class se dají vlastnosti úloh **navázat (bind)** přímo na proměnné NPC (`MoveTarget`, `WaitTime`, `ShouldPatrol`…).

### 7.2 Úlohy (Blueprint, rodič `StateTreeTaskBlueprintBase`)

Složka `StateTrees/Tasks`. V každé úloze proměnná **`Actor`** typu `BP_NPC_ST_base`, v Details proměnné **Category = `Context`** → StateTree ji automaticky naváže na NPC.

**`STT_NPC_SelectWanderPoint`:**
```
Event Enter State → Actor → SelectWanderPoint → Finish Task (Succeeded = Success)
```

**`STT_NPC_SelectPatrolPoint`:**
```
Event Enter State → Actor → SelectNextPatrolPoint → Finish Task (Succeeded = Success)
```

**`STT_NPC_MoveTo`** – jen pokud v seznamu úloh chybí vestavěný **Move To** (kategorie AI):
- proměnné `Actor` (Context), `Destination` (Vector, Category `Input`), `AcceptanceRadius` (Float 50, Instance Editable)
```
Event Enter State → AI MoveTo (Pawn = Actor, Destination, Acceptance Radius)
   On Success → Finish Task (true)
   On Fail    → Finish Task (false)
Event Exit State → Actor → Get Controller → Stop Movement
```

### 7.3 Stavy a přechody

```
Root
 ├─ Patrol            Enter Condition: Bool Compare (Actor.ShouldPatrol == true)
 │   ├─ P_Select      Task: STT_NPC_SelectPatrolPoint
 │   ├─ P_Move        Task: Move To (Destination ← Actor.MoveTarget, Acceptable Radius 50)
 │   └─ P_Wait        Task: Delay (Duration ← Actor.WaitTime)
 ├─ Wander            Enter Condition: Bool Compare (Actor.ShouldWander == true)
 │   ├─ W_Select      Task: STT_NPC_SelectWanderPoint
 │   ├─ W_Move        Task: Move To (Destination ← Actor.MoveTarget, Acceptable Radius 50)
 │   └─ W_Wait        Task: Delay (Duration ← Actor.WaitTime)
 └─ Idle              Task: Delay (Duration 5) – záchrana, když nic jiného neplatí
```

Vazba (binding): u vlastnosti úlohy klikni na ikonku vedle hodnoty → vyber `Actor → MoveTarget` atd.

| Stav | On State Succeeded | On State Failed |
|---|---|---|
| `P_Select` | → `P_Move` | → `Idle` |
| `P_Move` | → `P_Wait` | → `P_Wait` (nedošel – počká a zkusí další bod) |
| `P_Wait` | → `P_Select` | → `P_Select` |
| `W_Select` | → `W_Move` | → `W_Wait` |
| `W_Move` | → `W_Wait` | → `W_Wait` |
| `W_Wait` | → `W_Select` | → `W_Select` |
| `Idle` | → `Root` | → `Root` |

Rodičovské stavy `Patrol` a `Wander` nemají vlastní úlohy, při vstupu se automaticky vybere první potomek (`P_Select` / `W_Select`).
Pokud ve tvé verzi stav dokončí první hotová úloha a v jednom stavu je víc úloh, u pomocných úloh vypni **Considered for Completion**. (V tomto návrhu má každý stav jen jednu úlohu.)

Zkompiluj (**Compile** v StateTree editoru) a ulož. Vrať se do `AIC_ST_NPCBase` a nastav `ST_NPC` (krok 4).

---

## 8. Rozmístění v mapě

**Potulování:**
1. Přetáhni `BP_NPC_ST_base` do mapy (na navmesh).
2. Details instance: `Behavior = Auto` (nebo `Wander`), `WanderRadius` podle prostoru.

**Hlídkování:**
1. Rozmísti `BP_PatrolPoint` (první přetáhni, další **Alt + tažení**). U bodů, kde má NPC postát déle, zvyš `WaitTime`.
2. Postupně **Ctrl + klik** vyber body v pořadí obchůzky a přidej do výběru NPC, které ji má chodit.
3. **Execute Python Script → `npc_make_patrol_route.py`** → vznikne `Route_01`, body se přejmenují na `Route_01_P01…`, NPC dostane trasu. Trasa je vidět jako spline.
4. Tam a zpět: v hlavičce skriptu `PING_PONG = True`, nebo zaškrtni `PingPong` na trase ručně.
5. Ručně bez skriptu: na trase do pole `Points` přidej body (ikonka kapátka), na NPC nastav `PatrolRoute`.

**Kontrola:** **Execute Python Script → `npc_report.py`** → body mimo navmesh nebo bez cesty se vyberou (Output Log, `Saved/NPCReport.csv`).

---

## 9. Ladění

| Nástroj | Jak |
|---|---|
| **StateTree Debugger** | v `ST_NPC` panel **Debugger** → Record, spustit PIE, vybrat instanci NPC → aktivní stavy a přechody v čase |
| **Gameplay Debugger** | v PIE klávesa **'** (apostrof, na CZ klávesnici často `ů`/`§`) → AI info o NPC před kamerou, cesta, stav |
| **Navmesh** | `P` v editoru, `show navigation` v konzoli při PIE |
| **Visual Logger** | Tools → Debug → Visual Logger: záznam pohybu a cest |
| **Print String** | v úlohách `STT_` pro rychlou kontrolu (`MoveTarget`, `WaitTime`) |

Časté problémy:
- NPC stojí a nic nedělá → chybí navmesh pod ním, StateTree není nastavený v AIC, nebo `Auto Possess AI` = Disabled.
- NPC klouže bez animace → **Use Acceleration for Paths** vypnuté (krok 3).
- NPC se točí na místě u bodu → bod mimo navmesh nebo moc malé Acceptable Radius (zkus 80).
- Hlídkuje jen mezi dvěma body → špatné pořadí / `PingPong`; zkontroluj `Points` na trase.

---

## 10. Test (PIE)

| # | Situace | Očekávaný výsledek |
|---|---|---|
| 1 | NPC bez trasy, `Behavior = Auto` | chodí po náhodných místech do 8 m od startu, mezi přesuny stojí 2–6 s |
| 2 | Při stání > 5 s | občas se rozhlédne (IdleBreak z ABP) |
| 3 | NPC s trasou 4 body, dokola | 1 → 2 → 3 → 4 → 1…, na bodech čeká podle `WaitTime` |
| 4 | Stejná trasa, `PingPong` | 1 → 2 → 3 → 4 → 3 → 2 → 1… |
| 5 | NPC daleko od trasy | dojde k **nejbližšímu** bodu a pokračuje |
| 6 | Dvě NPC na jedné trase | obě chodí, každé má vlastní pořadí |
| 7 | Bod mimo navmesh | NPC ho přeskočí (P_Move selže → čeká → další bod), report ho označí |
| 8 | `Behavior = Idle` | NPC stojí |
| 9 | Animace | rozjezd, chůze, zastavení (Stop) bez klouzání |

---

## 11. Další kroky (připraveno)

- **Posedávání:** `E_NPCBehavior` rozšířit o `Sit` (nebo náhodné posazení během potulování). Sedátka už mají `BP_Seat` (`../01_sitting`). Doporučení: přidat k `BP_Seat` **Smart Object** komponentu a ve StateTree použít úlohy *Find Smart Object* / *Use Smart Object*, nebo jednoduše vlastní úlohu „najdi nejbližší volné `BP_Seat` v okruhu → dojdi → `SitOn`“. Logika `SitOn` / `StandUp` se přesune z `BP_SkvtBaseChar` do společné komponenty, aby ji měla i NPC.
- **Pohled na bodě:** při čekání otočit NPC podle šipky `BP_PatrolPoint` (úloha s `Set Actor Rotation` / RInterp).
- **Vnímání hráče:** PawnSensing nahradit **AI Perception** (zrak, sluch) a přidat stav `Alert` / `Chase` s vyšší prioritou nad Patrol a Wander.
- **Zdraví a poškození:** vlastní komponenta místo rozbitého `SkvtHealthComponent`.
