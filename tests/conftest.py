# Ajoute la racine du dépôt au chemin d'import pour que « import status » fonctionne.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
