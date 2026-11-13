# Characters – animace postavy (přehled a rozšíření)

Evidence animací postavy v projektu: co je hotové, co je k dispozici a co se bude postupně přidávat.
Platí pro `BP_SkvtBaseChar` (+ potomci `BP_SkvtCharacterMale` / `BP_SkvtCharacterFemale`) a `ABP_SkvtCharacter`, kostra **UE5 Manny** (`SK_Mannequin`).

## Obsah dokumentu

| Část | K čemu |
|---|---|
| 1. Aktuální stav | Co postava umí a jak je to řešené |
| 2. Inventář animací v projektu | Co je v `Content` k dispozici a co je použité |
| 3. Chybějící animace | Mezery pro další rozšíření |
| 4. Zdroje z Fab (Epic Games) | Odkud animace doplnit a jak je dostat do projektu |
| 5. Log rozšíření | Záznam každého přidaného rozšíření (doplňovat průběžně) |

Podrobné návody k jednotlivým rozšířením jsou v podsložkách:

| Složka | Rozšíření | Stav |
|---|---|---|
| `01_sitting` | Posazení na sedátko libovolné výšky (E), Python skripty pro sedátka | návod připraven |

---

## 1. Aktuální stav

| Funkce | Chování | Řešení (stručně) |
|---|---|---|
| Pohyb po zemi | Stání → chůze → běh plynule podle rychlosti | `MoveForward_Blendspace` (Speed 0 `MM_Idle` / 150 `MM_Walk_Fwd` / 450 `MM_Run_Fwd`), Speed = `Vector Length XY`, Smoothing Time |
| Zastavení | Po puštění pohybu z chůze/běhu brzdná animace, po krátkém ťuknutí rovnou stání | Stav `Stop` (`Walk_Stop`), přechody podle `Has Acceleration` + prahu rychlosti 150 |
| Skok a pád | Odraz → let → dopad, sejití z hrany = rovnou pád | Stavy Jump / Fall / Landing, `Is Mid Air`, `Is Upwarding`, `Is Downwarding`, aliasy `ToJump` (priorita 0) a `ToLanding` |
| Nečinnost | Po náhodných 5–10 s stání rozhlédnutí | Stav `IdleBreak` (`Idle_Break`), `Idle Time` / `Idle Break Time`, notify `IdleBreakStarted` (State Entered + State Left) |
| Dřep | Ctrl přepíná dřep, pomalejší a nižší postava | `Crouch` / `Un Crouch`, Max Walk Speed Crouched 200, Crouched Half Height 60, `BS_Crouch`, alias `ToCrouch` (priorita 1) |
| Vstávání pod překážkou | Pod nízkým stropem nejde vstát, po vylezení se postava sama nenarovná | Funkce `CanStandUp` (Capsule Trace s výškou ve stoje, `StandingHalfHeight` z BeginPlay) |
| Skok ze dřepu | Mezerník ve dřepu = vstát a vyskočit | `Un Crouch` → `Delay Until Next Tick` → `Jump` |
| Kamera ve dřepu | Plynulé přiblížení o 20 % (0,25 s), při vstání zpět | Timeline `CrouchCamera` na `Event On Start Crouch` / `On End Crouch`, `CameraBoom → Target Arm Length` |
| Prolínání | Plynulé přechody i mezi rozdílnými pózami | `Main → DefaultSlot → Inertialization → Output Pose`, sync group `Loco` (pohyb + dřep) |

Připraveno pro rozšíření:
- **Skok na překážku ve dřepu** – větev False u `CanStandUp` v logice mezerníku + override `Can Jump Internal`; návrat do dřepu po dopadu zajistí `ToCrouch` (obsahuje Landing).
- **Animace usedání / vstávání** – stav `Crouch` lze převést na vnořenou state machine.
- **Útoky (montáže)** – `DefaultSlot` v AnimGraphu.

---

## 2. Inventář animací v projektu

Stav k 11. 11. 2026. Vše na kostře UE5 Manny, pokud není uvedeno jinak.

| Kategorie | Assety | Umístění | Použito |
|---|---|---|---|
| Pohyb (Manny) | `MM_Idle`, `MM_Walk_Fwd`, `MM_Run_Fwd`, `MM_Walk_InPlace`, `BS_MM_WalkRun` | `Characters/Mannequins/Animations/Manny` | ✅ (`BS_MM_WalkRun` ne) |
| Pohyb (Quinn) | `MF_Idle`, `MF_Walk_Fwd`, `MF_Run_Fwd`, `BS_MF_Unarmed_WalkRun` | `Characters/Mannequins/Animations/Quinn` | ❌ |
| Skok | `MM_Jump`, `MM_Fall_Loop`, `MM_Land` | `Characters/Mannequins/Animations/Manny` | ✅ |
| Doplňky pohybu | `Idle_Break`, `Walk_Stop`, `MoveForward_Blendspace` | `Skvt/Characters/Animations/Locomotion` | ✅ |
| Dřep | `Crouch_Idle`, `Crouch_Walk` (jen dopředu), `BS_Crouch` | `Skvt/Characters/Animations/Crouch` | ✅ |
| Údery – montáže | `AM_Att_punch`, `AM_Att_punch01–03`, `AM_Att_punch04_heavy`, `AM_Att_GroinKick` | `Skvt/Characters/Animations/Attacks` | ❌ |
| Zásahy – montáže | `AM_Hit_punch`, `AM_Hit_GroinKick` | `Skvt/Characters/Animations/Attacks` | ❌ |
| Údery – sekvence | `Att_punch`, `Att_punch01–04`, `Att_GroinKick`, `Att_BreakNeck`, `Hit_punch`, `Hit_GroinKick`, `Hit_BreakNeck` | `Skvt/Characters/Animations/Attacks` | ❌ |
| Kombo | `UE5_H2H_PunchCombo01–03` | `Skvt/Characters/Animations/Attacks` | ❌ |
| Párové akce | `UE5_Paired_CounterPunch_PalmStrike_Att` / `_Vic` | `Skvt/Characters/Animations/Attacks` | ❌ |
| Originály UE4 (kostra UE4) | `H2H_PunchCombo01–03`, `Paired_CounterPunch_PalmStrike`, `Paired_GroinKick`, `Paired_SneakNeckBreak` (Att/Vic) | `Skvt/Characters/Animations/Attacks/UE4` | zdroj pro retarget |
| Kostra UE4 | `Jog_Fwd`, `SK_Mannequin` (UE4) | `Characters/Mannequin_UE4` | zdroj pro retarget |
| Pomocné | `MM_T_Pose` | `Characters/Mannequins/Animations/Manny` | – |

Nástroje pro převod: `Characters/Mannequin_UE4/Rigs/RTG_UE4Manny_UE5Manny` a `RTG_UE5Manny_UE4Manny` (IK Retargeter), `IK_UE4_Mannequin`.

Poznámka: animace dřepu obsahují křivky ve stylu Lyry (`MoveData_Speed`, `RemainingTurnYaw`).

---

## 3. Chybějící animace

| Oblast | Co chybí | Využití |
|---|---|---|
| Pohyb do stran | Strafe vlevo / vpravo / vzad (chůze, běh) | Pohyb s kamerou, zaměřování |
| Dřep do stran | Crouch walk vlevo / vpravo / vzad | Plížení kolem překážek |
| Rozjezd a otočky | Start, Pivot (otočka v pohybu) | Plynulejší ovládání |
| Otáčení na místě | Turn in place 90° / 180° | Postava stojí a otáčí se s kamerou |
| Přechod do dřepu | Stand → Crouch, Crouch → Stand | Místo prostého prolnutí |
| Sprint | Sprint cyklus + start/stop | Rychlý pohyb |
| Překonávání překážek | Vault, Mantle (nízký/vysoký), Climb | Skok na překážku, šplh |
| Smrt a zásahy | Death, Hit React (obecné) | Zdraví, poškození |
| Sezení | Sit Down, Sit Idle, Stand Up | Sedátka (viz `01_sitting`) |

---

## 4. Zdroje z Fab (Epic Games, zdarma)

| Balík | Obsah | Kostra | Jak do projektu | Vhodné pro |
|---|---|---|---|---|
| [Game Animation Sample Project (GASP)](https://www.fab.com/listings/8de31c5d-93bc-4bd4-9606-ca789ce91b99) | Stovky animací: pohyb všemi směry, starty, stopy, pivoty, dřep, skoky, traversal (vault / mantle), slide | UEFN Mannequin | Retarget přes IK Retargeter (v projektu GASP přiložený) | Překážky, šplh, kompletní pohyb |
| Lyra Starter Game | Pohyb beze zbraně i se zbraněmi (4/8 směrů), starty, stopy, pivoty, turn in place, skoky, emoce, smrt, zásahy | `SK_Mannequin` (UE5) | Migrate, bez převodu | Strafe, dřep do stran, otočky, turn in place |
| [Animation Starter Pack](https://www.fab.com/listings/98ff449d-79db-4f54-9303-75486c4fb9d9) | 62 animací: jog všemi směry, dřep, skoky, smrt, zásahy, puška | UE4 Mannequin | Retarget hotovým `RTG_UE4Manny_UE5Manny` | Rychlé doplnění pro výuku |
| [GASP retargeted to UE5 Manny](https://www.fab.com/listings/259f8545-f820-47b3-8fc1-e8ec5458214d) (komunitní) | 1 378 sekvencí z GASP (walk, run, crouch, jump, traversal, sprint, slide…) | UE5 Manny | Migrate, bez převodu | Záloha, pokud se nechce převádět |

Doporučené pořadí:
1. **Souboj** z animací, které už jsou v projektu (montáže → `DefaultSlot`).
2. **Strafe a dřep do stran** z Lyry (stejná kostra).
3. **Překážky / šplh** z GASP (ukázka retargetingu).

Před stažením ověřit podporu UE 5.8. Pokud chybí, stáhnout do projektu s nejbližší verzí a animace odtud migrovat.

Odkazy:
- [GASP – aktualizace pro UE 5.7](https://www.unrealengine.com/en-US/tech-blog/explore-the-updates-to-the-game-animation-sample-project-in-ue-5-7)
- [Animation in Lyra Sample Game](https://dev.epicgames.com/documentation/unreal-engine/animation-in-lyra-sample-game-in-unreal-engine)
- [Adapting Lyra animation to your UE5 game](https://www.unrealengine.com/tech-blog/adapting-lyra-animation-to-your-ue5-game)

### Postup migrace (obecně)

1. Stáhnout balík z Fab do **samostatného** projektu (ne přímo do `skvt_projekt`).
2. V Content Browseru vybrat jen potřebné animace → **Asset Actions → Migrate** → `skvt_projekt/Content`.
3. V dialogu odškrtnout nepotřebné závislosti (zvuky notify, materiály, mapy).
4. Jiná kostra → **Retarget Animations** s příslušným IK Retargeterem, výstup do `Skvt/Characters/Animations/<Kategorie>`.
5. Zapsat do logu níže (zdroj, assety, kam použito).

---

## 5. Log rozšíření

Každé nové rozšíření zapsat jako novou podkapitolu (nejnovější nahoře).

### Šablona

```
### YYYY-MM-DD – Název rozšíření
- **Cíl (game design):** co postava nově umí
- **Zdroj animací:** projekt / Fab balík (odkaz), retarget ano/ne
- **Přidané assety:** seznam + složka
- **Změny v BP_SkvtBaseChar:** vstupy, proměnné, funkce
- **Změny v ABP_SkvtCharacter:** stavy, přechody, aliasy, proměnné
- **Nastavení / hodnoty:** klíčová čísla
- **Test:** co ověřit
- **Otevřené body:**
```

### 2026-11 – Základní pohyb, skok, nečinnost, dřep, kamera
- **Cíl:** viz část 1 (Aktuální stav).
- **Zdroj animací:** animace v projektu (Mannequins + `Skvt/Characters/Animations`).
- **Přidané assety:** `IA_Crouch` (Left Ctrl v `IMC_Default`), `BS_Crouch`.
- **Změny v BP_SkvtBaseChar:** `StandingHalfHeight`, `CanStandUp`, logika Ctrl a mezerníku, `DefaultArmLength` / `CrouchArmLength`, timeline `CrouchCamera`, Character Movement (Can Crouch, Max Walk Speed Crouched 200, Crouched Half Height 60).
- **Změny v ABP_SkvtCharacter:** stavy Idle, IdleBreak, Move, Stop, Jump, Fall, Landing, Crouch; aliasy ToJump, ToLanding, ToMove, ToCrouch; Inertialization za `DefaultSlot`; sync group `Loco`.
- **Opravené chyby:** přešlapování (`MM_Walk_InPlace` v blendspace), zacyklení IdleBreak (chybějící reset `Idle Time`), nemožnost vstát (`StandingHalfHeight` = 0, chyběl BeginPlay), průchod pod příliš nízkým stropem (Crouched Half Height 40), nepřehrávaný Stop (alias ToMove s podmínkou podle rychlosti).
- **Otevřené body:** zpětná vazba při blokovaném vstávání, vlastní animace pro Quinn, animace rozjezdu.
