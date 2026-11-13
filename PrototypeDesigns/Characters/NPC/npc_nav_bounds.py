"""
Vytvori (nebo upravi) NavMeshBoundsVolume tak, aby pokryl vybrane actory
(typicky Landscape, podlaha, ostrov...) + okraj.

Pouziti v Unreal Editoru:
  1) Vybrat actory, ktere ma navmesh pokryt
  2) File -> Execute Python Script... -> vybrat tento soubor
  3) Klavesou P ve viewportu zobrazit navmesh (zelena plocha)
  Akce jde vratit pres Ctrl+Z. Opakovane spusteni jen upravi existujici volume.
"""
import unreal

# --- Nastaveni ---------------------------------------------------------------
LABEL = "NavBounds_Auto"
PAD_XY = 200.0      # okraj do stran (cm)
PAD_Z = 500.0       # okraj nahoru i dolu (cm) - kopce, schody, strechy
# -----------------------------------------------------------------------------

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def main():
    sel = actor_sub.get_selected_level_actors()
    sel = [a for a in sel if not isinstance(a, unreal.NavMeshBoundsVolume)]
    if not sel:
        unreal.log_warning("[NavBounds] Neni vybrany zadny actor")
        return

    mn = [1e12, 1e12, 1e12]
    mx = [-1e12, -1e12, -1e12]
    for a in sel:
        o, e = a.get_actor_bounds(False)
        for i, (oc, ec) in enumerate(((o.x, e.x), (o.y, e.y), (o.z, e.z))):
            mn[i] = min(mn[i], oc - ec)
            mx[i] = max(mx[i], oc + ec)

    center = unreal.Vector((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, (mn[2] + mx[2]) / 2)
    half = unreal.Vector((mx[0] - mn[0]) / 2 + PAD_XY,
                         (mx[1] - mn[1]) / 2 + PAD_XY,
                         (mx[2] - mn[2]) / 2 + PAD_Z)

    vol = None
    for a in actor_sub.get_all_level_actors():
        if isinstance(a, unreal.NavMeshBoundsVolume) and a.get_actor_label() == LABEL:
            vol = a
            break

    with unreal.ScopedEditorTransaction("Fit NavMeshBoundsVolume"):
        if vol is None:
            vol = actor_sub.spawn_actor_from_class(unreal.NavMeshBoundsVolume, center,
                                                   unreal.Rotator(0.0, 0.0, 0.0))
            vol.set_actor_label(LABEL)
            action = "vytvoren"
        else:
            vol.set_actor_location(center, False, True)
            action = "upraven"
        # vychozi brush volume ma polovicni rozmer 100 cm -> scale = half / 100
        vol.set_actor_scale3d(unreal.Vector(half.x / 100.0, half.y / 100.0, half.z / 100.0))

    unreal.log(f"[NavBounds] {LABEL} {action}: stred {center}, "
               f"rozmer {2*half.x/100:.0f} x {2*half.y/100:.0f} x {2*half.z/100:.0f} m")


main()
