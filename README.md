# lumen-status — Page de statut des services du Réseau Lumen

Kit de démarrage du **TP 3** (module « Gestion de projet informatique », Jour 3).

Ce dépôt génère une page web statique qui affiche l'état des services numériques
du Réseau Lumen (disponibilité du mois, statut, incidents). La page est publiée
sur GitHub Pages par un pipeline GitHub Actions.

## Contenu

| Chemin | Rôle |
|---|---|
| `status/sla.py` | Calculs : disponibilité, MTTR, MTBF, statut d'un service |
| `status/build_page.py` | Génère `public/index.html` à partir des données |
| `data/services.json` | Services suivis, objectifs de disponibilité, incidents (minutes) |
| `config/flags.json` | Feature flags : colonne MTTR, bandeau de maintenance |
| `tests/test_sla.py` | Tests unitaires (pytest) |
| `.github/workflows/ci.yml` | Intégration continue : lance les tests sur chaque PR |
| `.github/pull_request_template.md` | Modèle de description de pull request |

## Travailler en local

```bash
pip install -r requirements.txt     # installe pytest
pytest -q                           # lance les tests
python status/build_page.py         # génère public/index.html
```

Ouvrez ensuite `public/index.html` dans votre navigateur.
Sous Windows, utilisez `py` à la place de `python` si la commande n'est pas trouvée.

## Important : un test échoue au départ (c'est voulu)

Le test `test_mtbf` échoue tant que la fonction `mtbf()` n'est pas écrite :

```
FAILED tests/test_sla.py::test_mtbf - NotImplementedError: LUM-31 : à impléme...
1 failed, 6 passed in 0.03s
```

La CI est donc **rouge** au premier push. Le ticket **LUM-31** consiste à
implémenter `mtbf()` : c'est la première pull request à fusionner.
Tant qu'elle n'est pas fusionnée, les autres pull requests restent bloquées
par le check « tests » : c'est exactement le rôle d'une CI.

## Règles de l'équipe

- On ne pousse jamais directement sur `main` : branche + pull request + revue.
- Nom de branche : `feature/LUM-31-mtbf`, `fix/LUM-35-...`
- Message de commit : `feat(LUM-31): implémenter le calcul du MTBF`
- Jamais de secret (mot de passe, jeton) dans le dépôt : le fichier `.env` est ignoré.
