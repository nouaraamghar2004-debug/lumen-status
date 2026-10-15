"""Calculs d'indicateurs de service (ITIL) pour la page de statut du Réseau Lumen.

Toutes les durées sont exprimées en minutes.
"""


def disponibilite(minutes_totales, minutes_indispo):
    """Disponibilité en pourcentage, arrondie à 3 décimales.

    Exemple : disponibilite(43200, 85) -> 99.803
    """
    if minutes_totales <= 0:
        raise ValueError("minutes_totales doit être strictement positif")
    return round(100 * (minutes_totales - minutes_indispo) / minutes_totales, 3)


def mttr(durees_minutes):
    """MTTR (temps moyen de rétablissement) : moyenne des durées d'incident.

    Renvoie 0 si la liste est vide (aucun incident sur la période).
    Exemple : mttr([42, 18, 25]) -> 28.3
    """
    if not durees_minutes:
        return 0
    return round(sum(durees_minutes) / len(durees_minutes), 1)


def mtbf(minutes_totales, minutes_indispo, nb_pannes):
    """MTBF (temps moyen entre pannes), arrondi à 1 décimale.

    Formule : (minutes_totales - minutes_indispo) / nb_pannes
    Si nb_pannes vaut 0, renvoyer le temps de fonctionnement total
    (minutes_totales - minutes_indispo).
    Exemple : mtbf(43200, 85, 3) -> 14371.7
    """
    raise NotImplementedError("LUM-31 : à implémenter")


def statut_service(dispo, objectif):
    """Statut affiché sur la page, à partir de la disponibilité mesurée.

    - "OK"      si dispo >= objectif
    - "DÉGRADÉ" si dispo >= objectif - 0,5 point
    - "KO"      sinon
    """
    if dispo >= objectif:
        return "OK"
    if dispo >= round(objectif - 0.5, 3):
        return "DÉGRADÉ"
    return "KO"
