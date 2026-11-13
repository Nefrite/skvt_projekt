# 01 Sitting – posazení postavy na sedátko libovolné výšky

Postava si na klávesu **E** sedne na židli, pařez, stoličku a podobně. Rozdíl výšky sedátka proti animaci se dorovná posunem pánve a IK nohou, takže jedna sada animací pokryje sedátka zhruba **30–60 cm**.
Navazuje na `../README_animations.md` (dřep, skok, aliasy, Inertialization).

## Obsah složky

| Soubor | K čemu |
|---|---|
| `README_sitting.md` | Tento návod |
| `seat_test_station.py` | Postaví před kamerou testovací kvádry 30 / 45 / 60 cm |
| `seat_place_selected.py` | Na vybrané actory položí `BP_Seat` a změří výšku sedáku |
| `seat_report.py` | Vypíše všechna sedátka v mapě, označí ta mimo rozsah, uloží `Saved/SeatReport.csv` |

Skripty se spouštějí přes **File → Execute Python Script…** (potřebný plugin **Python Editor Script Plugin**). Python běží jen v editoru. Samotné sezení ve hře řeší Blueprinty.

## Princip

```
BP_Seat (na sedátku)           BP_SkvtBaseChar                ABP_SkvtCharacter
 ├ SitPoint  = střed sedáku     E → najdi BPI_Interactable     Is Sitting → SitDown → SitIdle
 ├ SeatHeight = výška nad zemí  → Seat.Interact(self)          NOT Is Sitting → StandUp → Idle
 └ Interact() → Char.SitOn()    SitOn: přesun + Is Sitting     IK: pánev ± (SeatHeight − 45),
                                StandUp: zpět + chůze               chodidla zůstanou na zemi
```

**Pravidla (game design):**
- E u sedátka → sedne si. E nebo mezerník při sezení → vstane (bez skoku).
- WASD, Ctrl a skok se při sezení ignorují, kamerou jde otáčet.
- Nejde si sednout ve dřepu, ve vzduchu ani na obsazené sedátko.

---

## 1. Animace

Potřebné jsou 3 sekvence na kostře UE5 Manny:

| Název v projektu | Co dělá | Loop |
|---|---|---|
| `A_Sit_Down` | ze stoje si sedne | ne |
| `A_Sit_Idle` | sezení | **ano** |
| `A_Sit_StandUp` | vstane | ne |

**Zdroj:** Game Animation Sample (Fab, Epic), sada interakcí s lavičkou (bench). V Content Browseru hledej `Bench` nebo `Sit`.

1. GASP stáhni do **samostatného** projektu.
2. Vyber 3 animace (sednutí, sezení ve smyčce, vstávání) → pravý klik → **Retarget Animations**.
   - Source: kostra GASP (UEFN Mannequin), Target: `SKM_Manny_Simple`.
   - Retargeter: pokud ho GASP obsahuje pro Manny, použij ho. Jinak v dialogu zvol **Auto Generate Retargeter**.
3. Převedené animace **Migrate** do `skvt_projekt` a přesuň je do `Content/Skvt/Characters/Animations/Sit` s názvy z tabulky.

Alternativa bez převodu: komunitní balík „GASP retargeted to UE5 mannequin“ (Fab), sekce bench interaction.

**Kontrola animací (důležité):**
1. Otevři `A_Sit_Down` a zapni **Show → Bones**. Sleduj kořenovou kost `root` (u podlahy).
2. **Root se během animace posouvá** (typicky: postava couvne k lavičce) → v Asset Details zaškrtni **Enable Root Motion**. Póza pak zůstane na místě a posun zajistí Blueprint (krok 5). Vzdálenost, o kterou se root posune, si zapiš jako `StandDistance` (odhad stačí, doladí se v kroku 8).
3. **Root stojí na místě** → nic neměň, `StandDistance` bude kolem 40 cm.
4. Totéž udělej u `A_Sit_StandUp`.
5. U `A_Sit_Idle` ověř, že je to smyčka.
6. Zapiš si délky `A_Sit_Down` a `A_Sit_StandUp` (Asset Details → Length), použijí se jako `SitDownTime` a `StandUpTime`.

---

## 2. Vstup

1. `Content/Skvt/Characters/Input/Actions`: nová **Input Action** `IA_Interact`, **Value Type = Digital (bool)**.
2. `IMC_Default`: mapping `IA_Interact` → klávesa **E**.

---

## 3. Blueprint Interface `BPI_Interactable`

Obecné rozhraní pro všechno, s čím jde interagovat (sedátka, později dveře, páky…).

1. Složka `Content/Skvt/Interaction`: pravý klik → **Blueprint → Blueprint Interface** → `BPI_Interactable`.
2. Přejmenuj výchozí funkci na `Interact`, přidej **Input** `Instigator` typu **Character (Object Reference)**.
3. Ulož.

---

## 4. `BP_Seat`

Složka `Content/Skvt/Interaction/Seat`: **Blueprint Class → Actor** → `BP_Seat`.
Cesta musí sedět s `BP_SEAT_PATH` ve skriptech: `/Game/Skvt/Interaction/Seat/BP_Seat`.

**Komponenty:**

| Komponenta | Nastavení |
|---|---|
| `DefaultSceneRoot` | = bod sedáku (střed sedací plochy) |
| `SitPoint` (Arrow) | připojit pod root, Location 0, Rotation 0. Šipka (osa X) = kam postava kouká. Arrow Size 0.5, Hidden in Game ano |
| `InteractSphere` (Sphere Collision) | Sphere Radius **120**. Collision Preset **Custom**: Collision Enabled = Query Only, Object Type = **WorldDynamic**, všechny odezvy **Overlap**, Visibility a Camera **Ignore** |

**Proměnné:**

| Proměnná | Typ | Nastavení |
|---|---|---|
| `SeatHeight` | Float | výchozí 45, **Instance Editable** zaškrtnout (skript ji jinak nezapíše) |
| `IsOccupied` | Boolean | výchozí false |

**Class Settings → Interfaces → Add → `BPI_Interactable`.**

**Funkce `GetFloorZ`** (Pure, výstup Float): `SitPoint → Get World Location → Break Vector Z − SeatHeight`.

**Event `Interact`** (My Blueprint → Interfaces → Interact → pravý klik → Implement Event):
```
Event Interact (Instigator)
 → Branch (IsOccupied)
     False → Cast To BP_SkvtBaseChar (Object = Instigator)
               → As BP Skvt Base Char → SitOn (Seat = self)
```
`SitOn` vytvoříš v kroku 5. Po jeho vytvoření se vrať sem a zapoj ho.

---

## 5. Postava: `BP_SkvtBaseChar`

### 5.1 Proměnné

| Proměnná | Typ | Výchozí | K čemu |
|---|---|---|---|
| `IsSitting` | Boolean | false | čte ABP |
| `IsSeatTransition` | Boolean | false | probíhá sedání/vstávání (blokuje další E) |
| `CurrentSeat` | BP_Seat (Object Ref) | – | aktuální sedátko |
| `SitPelvisOffset` | Float | 0 | o kolik posunout pánev (čte ABP) |
| `RefSeatHeight` | Float | **45** | výška sedáku, pro kterou je animace (doladit v kroku 8) |
| `SitForwardOffset` | Float | **10** | o kolik je kořen postavy při sezení před bodem sedáku (doladit) |
| `StandDistance` | Float | **40** | odkud si postava sedá / kam vstane (před sedákem) |
| `SitDownTime` | Float | délka `A_Sit_Down` | |
| `StandUpTime` | Float | délka `A_Sit_StandUp` | |

### 5.2 Pomocné funkce (Pure)

**`GetSitRootLocation`** (vstup `Seat`, výstup Vector) – kde stojí kapsle při sezení:
```
XY: Seat.SitPoint World Location + Seat.SitPoint Forward Vector × SitForwardOffset
Z:  Seat.GetFloorZ + Capsule Component → Get Scaled Capsule Half Height
```
(Make Vector z X, Y výsledku a Z výpočtu.)

**`GetStandLocation`** (vstup `Seat`, výstup Vector) – kde postava stojí před sedákem:
```
GetSitRootLocation(Seat) + Seat.SitPoint Forward Vector × StandDistance
```

**`FindInteractable`** (výstup Actor):
1. **Sphere Overlap Actors**: Sphere Pos = Get Actor Location, Radius **150**, Object Types = pole s **WorldDynamic**, Actors to Ignore = pole se **self**.
2. **For Each Loop** přes Out Actors: **Does Implement Interface** (`BPI_Interactable`) → pokud ano a vzdálenost (`Get Distance To`) je menší než dosud nejmenší → ulož do lokální proměnné `Best`.
3. Po dokončení (Completed) vrať `Best`.

### 5.3 Event `SitOn` (Custom Event, vstup `Seat` typu BP_Seat)

Musí to být Custom Event v Event Graphu (ne funkce), protože používá latentní **Move Component To**.

```
SitOn (Seat)
 → Branch: IsSitting OR IsSeatTransition OR Character Movement→Is Crouching OR Is Falling
     True → (nic)
     False:
 → SET CurrentSeat = Seat, SET Seat.IsOccupied = true, SET IsSeatTransition = true
 → Character Movement → Stop Movement Immediately
 → Character Movement → Set Movement Mode = None
 → Set Actor Enable Collision = false
 → SET SitPelvisOffset = Seat.SeatHeight − RefSeatHeight
 → Move Component To   (Component = Capsule Component,
                        Target Relative Location = GetStandLocation(Seat),
                        Target Relative Rotation = Seat.SitPoint World Rotation,
                        Ease Out / Ease In = zapnuto, Over Time = 0.3)
   Completed:
 → SET IsSitting = true            ← ABP spustí A_Sit_Down
 → Move Component To   (Target = GetSitRootLocation(Seat), stejná rotace,
                        Over Time = SitDownTime)
   Completed:
 → SET IsSeatTransition = false
```

Kapsle nemá rodiče, takže „Relative“ v Move Component To = světové souřadnice.
Pokud animace nemá posun kořene (krok 1.3), nastav u druhého Move Component To **Over Time = 0.3** místo `SitDownTime`.

### 5.4 Event `StandUp` a `OnStandUpFinished` (Custom Events)

```
StandUp
 → Branch: IsSitting AND NOT IsSeatTransition → True:
 → SET IsSeatTransition = true
 → SET IsSitting = false           ← ABP spustí A_Sit_StandUp
 → Move Component To (Target = GetStandLocation(CurrentSeat),
                      rotace = CurrentSeat.SitPoint World Rotation,
                      Over Time = StandUpTime)
   Completed → OnStandUpFinished

OnStandUpFinished
 → Set Actor Enable Collision = true
 → Character Movement → Set Movement Mode = Walking
 → SET CurrentSeat.IsOccupied = false, SET CurrentSeat = (prázdné)
 → SET SitPelvisOffset = 0, SET IsSeatTransition = false
```

### 5.5 Vstupy

**E (`IA_Interact`, Started):**
```
Branch (IsSitting) → True: StandUp
                   → False: FindInteractable → Is Valid → BPI Interact (Message) (Target = výsledek, Instigator = self)
```
Volej **Interact (Message)** (ikonka obálky), ne přímo funkci BP_Seat.

**Úpravy stávajících vstupů:**
- `IA_Move` (Triggered): před **Add Movement Input** vlož Branch `NOT IsSitting AND NOT IsSeatTransition`.
- `IA_Jump` (Started): úplně na začátek vlož Branch `IsSitting` → True: **StandUp** (a konec), False: stávající logika. Navíc Branch `IsSeatTransition` → True: nic.
- `IA_Crouch` (Started): na začátek Branch `IsSitting OR IsSeatTransition` → True: nic.
- `IA_Look` neměň.

Zkompiluj, ulož. Vrať se do `BP_Seat` a zapoj `SitOn` (krok 4).

---

## 6. ABP: `ABP_SkvtCharacter`, Event Graph

1. Proměnné: `SkvtCharRef` (BP_SkvtBaseChar Object Ref), `Is Sitting` (Boolean), `Sit Pelvis Offset` (Float).
2. **Initialize:** za stávající `SET Character Ref` přidej `Cast To BP_SkvtBaseChar` → `SET SkvtCharRef`.
3. **Update:** za `SET Is Crouching` přidej `SkvtCharRef → Is Valid` → `SET Is Sitting` ← `SkvtCharRef.IsSitting`, `SET Sit Pelvis Offset` ← `SkvtCharRef.SitPelvisOffset`.
4. **Idle Time:** do AND u Branche přidej pin `NOT Is Sitting`.
5. **Event `AnimNotify_StandUpStarted`** zatím nic nedělá, jen ho vytvoř v kroku 7 (pro ladění přes Print String).

---

## 7. ABP: state machine `Main`

**Nové stavy:**

| Stav | Obsah |
|---|---|
| `SitDown` | Sequence Player `A_Sit_Down`, Loop **vypnuto** |
| `SitIdle` | Sequence Player `A_Sit_Idle`, Loop zapnuto |
| `StandUp` | Sequence Player `A_Sit_StandUp`, Loop **vypnuto**. Notifications → State Entered = `StandUpStarted` |

**Alias `ToSit`:** zaškrtni **Idle, IdleBreak, Move, Stop**. Přechod `ToSit → SitDown`: podmínka `Is Sitting`, blend 0.2 s (Inertialization), Priority Order **1**.

**Přechody:**

| Přechod | Podmínka | Blend |
|---|---|---|
| SitDown → SitIdle | Automatic Rule Based on Sequence Player | 0.2 s |
| SitIdle → StandUp | `NOT Is Sitting` | 0.2 s |
| SitDown → StandUp | `NOT Is Sitting` (přerušené sednutí) | 0.2 s |
| StandUp → Idle | Automatic Rule Based on Sequence Player | 0.25 s, Inertialization |

**Kontrola ostatních aliasů:** `SitDown`, `SitIdle` a `StandUp` **nesmí** být v `ToJump`, `ToCrouch` ani `ToMove`.

---

## 8. ABP: AnimGraph – posun pánve a IK nohou

Cíl: pánev se posune o `Sit Pelvis Offset` nahoru/dolů, chodidla zůstanou tam, kde je má animace (na zemi).
Kostra Manny má pomocné kosti `ik_foot_l` / `ik_foot_r` (pod `root`, ne pod pánví), posun pánve je neovlivní. Proto se do nich nejdřív zkopíruje poloha chodidel a pak se k nim nohy „přitáhnou“.

Výsledné zapojení:
```
Main → DefaultSlot → Inertialization
     → Copy Bone (foot_l → ik_foot_l) → Copy Bone (foot_r → ik_foot_r)
     → Transform (Modify) Bone (pelvis)
     → Two Bone IK (foot_l) → Two Bone IK (foot_r)
     → Output Pose
```
Mezi skeletal control nody Unreal sám vloží převody **Local To Component** a **Component To Local**.

**Copy Bone** (2×):
- Source Bone `foot_l` / `foot_r`, Target Bone `ik_foot_l` / `ik_foot_r`
- Copy Translation a Copy Rotation zapnuto, Control Space = **Component Space**

**Transform (Modify) Bone:**
- Bone to Modify = `pelvis`
- Translation Mode = **Add to Existing**, Translation Space = **Component Space**
- Rotation Mode a Scale Mode = Ignore
- Pin **Translation** ← `Make Vector (0, 0, Sit Pelvis Offset)`

**Two Bone IK** (2×):
- IK Bone = `foot_l` / `foot_r`
- Effector Location Space = **Bone Space**, Effector Target = `ik_foot_l` / `ik_foot_r`, Effector Location = 0, 0, 0
- Take Rotation from Effector Space = zapnuto
- Joint Target Location Space = **Bone Space**, Joint Target = `calf_l` / `calf_r`, Joint Target Location = 0, 0, 0 (koleno zachová směr z animace)
- Allow Stretching = vypnuto

**Alpha u všech 5 nodů:**
- Alpha Input Type = **Bool Value**, Bool pin ← `Is Sitting`
- Alpha Bool Blend: Blend In Time **0.4**, Blend Out Time **0.4**

Mimo sezení mají nody alpha 0 a na ostatní animace nemají vliv.

---

## 9. Testovací stanoviště a ladění

1. Otoč kameru viewportu na volnou rovnou plochu.
2. **Execute Python Script → `seat_test_station.py`** → vzniknou kvádry `SeatTest_30cm`, `_45cm`, `_60cm` (vybrané).
3. **Execute Python Script → `seat_place_selected.py`** → na kvádrech je `BP_Seat` se šipkou ke kameře. V Output Logu: `SeatHeight = 30.0 / 45.0 / 60.0 cm`.
4. PIE, dojdi ke kvádru **45 cm**, zmáčkni E a lad v `BP_SkvtBaseChar` (pauza PIE, změna, znovu):
   - zadek nad / pod sedákem → `RefSeatHeight` (vyšší hodnota = postava sedí níž),
   - postava sedí moc vpředu / vzadu → `SitForwardOffset`,
   - při sedání „klouže“ → `StandDistance` podle posunu kořene v animaci.
5. Vyzkoušej **30 cm** a **60 cm**: zadek na sedáku, chodidla na zemi, kolena ohnutá víc / míň.
6. Po odladění testovací kvádry smaž (složka `SeatTest` v Outlineru).

Ladění v ABP: `slomo 0.3` v konzoli, Debug Filter na postavu, sleduj stavy SitDown → SitIdle → StandUp.

---

## 10. Sedátka v mapě (Python)

1. Vyber židle, pařezy, stoličky (klidně desítky najednou).
2. **`seat_place_selected.py`** → každý dostane `BP_Seat` (připojený, posouvá se s ním).
3. Zkontroluj šipky ve viewportu. Špatný směr:
   - celá sada stejného meshe → v hlavičce skriptu `YAW_OFFSET` (90 / 180 / −90) a spusť znovu (existující BP_Seat se jen přepočítají),
   - jednotlivě → otoč `BP_Seat` ručně.
4. Židle s opěradlem: paprsek trefí opěradlo místo sedáku → `SAMPLE_OFFSET_X` (např. 10 nebo −10).
5. Pařez nebo kámen bez jasného „předku“: na směru nezáleží, případně otoč ručně.
6. **`seat_report.py`** → přehled v Output Logu a `Saved/SeatReport.csv`. Sedátka mimo 30–60 cm se vyberou, ta zatím buď uprav (výška meshe), nebo počkej na varianty animací (low / high).

Skript lze spouštět opakovaně. Po přesunu sedátka v mapě stačí ho vybrat a spustit `seat_place_selected.py` znovu.

---

## 11. Test (PIE)

| # | Akce | Očekávaný výsledek |
|---|---|---|
| 1 | E u židle 45 cm | postava dojde/otočí se, sedne si, zadek na sedáku |
| 2 | E při sezení | vstane před sedátko, jde chodit |
| 3 | Mezerník při sezení | vstane, **nevyskočí** |
| 4 | WASD / Ctrl při sezení | nic |
| 5 | E na 30 cm a 60 cm | sedí na sedáku, chodidla na zemi |
| 6 | E ve dřepu / ve vzduchu | nic |
| 7 | Rychlé dvojité E | sednutí se dokončí, druhé E se ignoruje |
| 8 | Dlouhé sezení | po vstání se rozhlížení nespustí hned |
| 9 | E daleko od sedátka (> 150 cm) | nic |

---

## 12. Možná rozšíření

- **Varianty animací** low (zem, kámen < 30 cm) a high (barová stolička > 60 cm): v `BP_Seat` enum `SeatType` podle výšky, v ABP výběr stavu (nebo **Blend Poses by Enum**) a vlastní `RefSeatHeight` pro každou variantu.
- **Motion Warping** místo Move Component To: přesnější dosednutí přímo z animace s root motion.
- **Smart Objects** pro NPC (projekt má StateTree): `BP_Seat` dostane Smart Object komponentu.
- Kamera při sezení: mírné oddálení (stejný princip jako `CrouchCamera`).
- Nápověda „E – sednout“ ve UI, když je sedátko v dosahu.
