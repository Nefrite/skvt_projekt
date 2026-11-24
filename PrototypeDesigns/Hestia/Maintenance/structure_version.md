---
type: log
updated: 2026-11-24
---
# Verze struktury

Verze core (`_core/VERSION`) a lokální revize instance (`taxonomy_local`), datum, odkaz na change requesty a rozhodnutí (05 kap. 7.4). Připisuje se na konec. Formát:
`| RRRR-MM-DD | core <verze> | <událost> | <change requesty, rozhodnutí> |`

| datum | verze | událost | change requesty, rozhodnutí |
|---|---|---|---|
| 2026-11-19 | core 0.10.2 | založení vaultu (init) |  |
| 2026-11-20 | core 0.14.0 | aktualizace z 0.10.2 (update_core) | CR_2026-11-19_jmena_roli_anglicky, CR_2026-11-19_knowhow_tematicke_pasti, CR_2026-11-19_asset_index_alias_entity |
| 2026-11-21 | core 0.14.1 | aktualizace z 0.14.0 (update_core --tag v0.14.1) |  |
| 2026-11-21 | core 0.14.2 | aktualizace z 0.14.1 (update_core --tag v0.14.2) | CR_2026-11-21_compose_role_po_kazde_aktualizaci |
| 2026-11-21 | core 0.15.0 | aktualizace z 0.14.2 (update_core --tag v0.15.0) | CR_2026-11-21_update_core_report_zmena_prirazeni, CR_2026-11-21_update_core_report_a_preruseni, CR_2026-11-21_knihovnik_pripojena_slozka, CR_2026-11-21_ue_query_cesty_ve_skriptu, CR_2026-11-21_inbox_import_notion |
| 2026-11-21 | core 0.16.0 | aktualizace z 0.15.0 (update_core --tag v0.16.0) | CR_2026-11-21_zaklad_roli_v_instanci |
| 2026-11-22 | core 0.20.1 | aktualizace z 0.16.0 (update_core --tag v0.20.1) | CR_2026-11-21_inbox_import_seznamy_v_li, CR_2026-11-21_podnety_roli_pres_frontu, CR_2026-11-21_ue_cteni_vs_state, CR_2026-11-21_kontrakt_rozdeleni |
| 2026-11-22 | core 0.21.1 | aktualizace z 0.20.1 (update_core) | CR-022_prostredi_core, CR-023_update_core_pripojena_slozka, CR-024_ue_signal_basicshapes, CR-025_ue_ism_bounds, CR-030_export_cr_prazdne_cr, CR-031_podnety_do_structure_log_skriptem |
| 2026-11-23 | core 0.23.0 | aktualizace z 0.21.1 (update_core) | CR-026_karta_assetu, CR-029_prace_s_assety, CR-032_ukoly_pro_role_ve_fronte, CR-025_ue_ism_bounds, CR-031_podnety_do_structure_log_skriptem, CR-027_asset_index_knihovni_meshe, CR-028_ue_query_assety |
| 2026-11-24 | core 0.25.0 | aktualizace z 0.23.0 (update_core) | CR-035_zralost_rodicu_a_matice, CR-033_vykon_pripojena_slozka, CR-034_kompilaty_hlavicka_verze, CR-036_assety_po_prevodu, CR-037_manifest_assetu_tabulky_a_data, CR-038_pravidla_roli_v_dokumentaci, CR-039_start_cesta_a_interpret, CR-040_drobne_opravy_kontrol |
