"""
Vypise vsechna BP_Seat v aktualni mape, jejich vysku a typ.
Sedatka mimo rozsah, ktery zvladne IK nohou, oznaci (vybere ve viewportu).

Pouziti: File -> Execute Python Script... -> vybrat tento soubor
Vystup: Output Log + Saved/SeatReport.csv
"""
import csv
import os
import unreal

# --- Nastaveni (drzet v souladu s BP_SkvtBaseChar / ABP) ---------------------
SEAT_CLASS_NAME = "BP_Seat_C"
IK_MIN = 30.0     # spodni hranice, kterou zvladne posun panve + IK nohou
IK_MAX = 60.0     # horni hranice
LOW_MAX = 35.0    # do teto vysky = "low"
HIGH_MIN = 55.0   # od teto vysky = "high"
# -----------------------------------------------------------------------------

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def seat_type(h):
    if h < LOW_MAX:
        return "low"
    if h > HIGH_MIN:
        return "high"
    return "normal"


def main():
    seats = [a for a in actor_sub.get_all_level_actors()
             if a.get_class().get_name() == SEAT_CLASS_NAME]
    if not seats:
        unreal.log_warning("[SeatReport] V mape neni zadne BP_Seat")
        return

    rows, bad = [], []
    for s in sorted(seats, key=lambda x: x.get_actor_label()):
        h = float(s.get_editor_property("SeatHeight"))
        parent = s.get_attach_parent_actor()
        loc = s.get_actor_location()
        ok = IK_MIN <= h <= IK_MAX
        if not ok:
            bad.append(s)
        rows.append([s.get_actor_label(),
                     parent.get_actor_label() if parent else "-",
                     f"{h:.1f}", seat_type(h), "OK" if ok else "MIMO ROZSAH",
                     f"{loc.x:.0f}", f"{loc.y:.0f}", f"{loc.z:.0f}"])

    header = ["Seat", "Parent", "SeatHeight_cm", "Type", "IK", "X", "Y", "Z"]
    unreal.log("[SeatReport] " + " | ".join(header))
    for r in rows:
        line = "[SeatReport] " + " | ".join(r)
        (unreal.log_warning if r[4] != "OK" else unreal.log)(line)

    path = os.path.join(unreal.Paths.convert_relative_path_to_full(
        unreal.Paths.project_saved_dir()), "SeatReport.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(header)
        w.writerows(rows)

    if bad:
        actor_sub.set_selected_level_actors(bad)
    unreal.log(f"[SeatReport] Celkem {len(rows)}, mimo rozsah {len(bad)} (vybrany). CSV: {path}")


main()
