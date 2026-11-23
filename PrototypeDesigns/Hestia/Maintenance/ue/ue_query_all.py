# hestia:ue_query – vygenerovaný čtecí skript, needitovat (zadání 13, kap. 10.11). Jen čtení.
# Entita: all. Spusť v editoru Unreal: Tools → Execute Python Script. Výsledek načti:
#   python <Hestia>/_core/scripts/hestia.py ue_query --import --all --apply
# Cesty se odvozují z umístění skriptu (<Hestia>/Maintenance/ue/); skript je přenosný mezi stroji.
import json
import sys
from pathlib import Path

try:
    HERE = Path(__file__).resolve().parent
except NameError:
    raise SystemExit('hestia:ue_query: skript spusť jako soubor (Execute Python Script), chybí __file__')
VAULT = HERE.parents[1]
sys.path.insert(0, str(VAULT / '_core' / 'scripts'))
import importlib  # noqa: E402
import hestia_ue  # noqa: E402
# editor drží dříve načtený modul v sys.modules; reload načte verzi z _core (zadání 0.24.1)
hestia_ue = importlib.reload(hestia_ue)

REQUEST = json.loads('{"hestia_ue": 1, "id": "all", "map": "/Game/Skvt/LapikusPrototypeMap", "stage_tag_prefix": "stage:", "limit": 500, "path": "etapa 1 (skript v editoru)", "targets": ["Brana", "Brana_Straz", "Guesthouse", "Hradby_a_Brana", "Lapikus", "Les_Lapikus", "Nadvori_Stan", "Palac", "Palac_Kovarna", "Palac_Kovarna_Vybaveni", "Palac_Obydli", "Palac_Treti", "Strazni_Vez", "Vez", "Vez_Pristresek"], "rules": {"Brana": [{"tags": ["stavba:Brana*"]}], "Brana_Straz": [{"tags": ["stavba:Brana_Straz*"]}], "Guesthouse": [{"tags": ["stavba:Ostroh_*"]}, {"folders": ["Ruin/ZapadniBudova"]}], "Hradby_a_Brana": [{"folders": ["Ruin/Hradba"]}], "Lapikus": [{"folders": ["Ruin/Rampa"]}], "Les_Lapikus": [{"tags": ["Zricenina_Alder"], "folders": ["Forest/Alders"]}], "Nadvori_Stan": [{"tags": ["vybaveni:Nadvori_Stan*"]}], "Palac": [{"folders": ["Ruin/Palac"]}, {"tags": ["stavba:Palac*"]}], "Palac_Kovarna": [{"tags": ["stavba:Palac_Kovarna*"]}], "Palac_Kovarna_Vybaveni": [{"tags": ["vybaveni:Palac_Kovarna_Vybaveni*"]}], "Palac_Obydli": [{"tags": ["stavba:Palac_Obydli*"]}], "Palac_Treti": [{"tags": ["stavba:Palac_Treti*"]}], "Strazni_Vez": [{"folders": ["Ruin/Brana"]}], "Vez": [{"folders": ["Ruin/Vez"]}, {"tags": ["stavba:Vez_Patra*"]}], "Vez_Pristresek": [{"tags": ["stavba:Vez_Pristresek*"]}]}, "pivot_far_cm": 500.0, "placeholder_ignore": ["/Engine/BasicShapes/Cube.Cube"]}')
hestia_ue.run(REQUEST, str(HERE / 'ue_result_all.json'))
