import json
from pathlib import Path

def test_durees_incidents_positives():
    fichier = Path(__file__).parent.parent / "data" / "services.json"

    with open(fichier, encoding="utf-8") as f:
        donnees = json.load(f)

    for service in donnees["services"]:
        for duree in service["incidents"]:
            assert duree > 0, "La durée d'un incident doit être positive"