"""Etapa.py - prepne v editoru etapu stavby: zobrazi / skryje actory podle tagu stage:<sada> (zrlib/config.py STAGES).
Unreal: Tools -> Execute Python Script -> 05_constructions/stavby/Etapa.py
Etapa 1 = base + site (rozestaveno), etapa 2 = base + final (hotovo), 0 = vsechny sady (stav po buildu).
Nic nestavi ani nemaze. Skryte actory jsou skryte v editoru i ve hre (Play) a nemaji kolizi; actory bez tagu stage: se nemeni.
Build stavby postavi vzdy vsechny sady viditelne -> po buildu spust tento skript znovu.
Prepinani za behu hry (Blueprint) dela totez: Get All Actors with Tag -> Set Actor Hidden In Game + Set Actor Enable Collision."""
ETAPA = 1                     # 1 = rozestaveno, 2 = hotovo, 0 = vsechno
JEN = None                    # napr. "Palac_Obydli" = jen actory staveb, jejichz jmeno tak zacina (tag stavba:<jmeno>); None = vsechny

import unreal
SHOW = {0: ("base", "final", "site"), 1: ("base", "site"), 2: ("base", "final")}[ETAPA]
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem); n = {}
with unreal.ScopedEditorTransaction("Etapa %d" % ETAPA):
    for a in eas.get_all_level_actors():
        tags = [str(t) for t in a.tags]
        st = next((t[6:] for t in tags if t.startswith("stage:")), None)
        if st is None: continue
        if JEN and not any(t.startswith("stavba:" + JEN) for t in tags): continue
        on = st in SHOW
        a.modify()
        a.set_is_temporarily_hidden_in_editor(not on)
        a.set_actor_hidden_in_game(not on)
        a.set_actor_enable_collision(on)
        n[st] = n.get(st, 0) + 1
unreal.log("Etapa %d: zobrazeno %s; actoru podle sad: %s" % (ETAPA, ", ".join(SHOW), n))
