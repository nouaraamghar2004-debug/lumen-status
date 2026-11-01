"""Tests unitaires des indicateurs de service (pytest)."""
import pytest

from status.sla import disponibilite, mtbf, mttr, statut_service


def test_disponibilite_sans_incident():
    assert disponibilite(43200, 0) == 100.0


def test_disponibilite_arrondie_a_3_decimales():
    assert disponibilite(43200, 85) == 99.803


def test_disponibilite_refuse_une_periode_nulle():
    with pytest.raises(ValueError):
        disponibilite(0, 0)


def test_mttr_moyenne_des_durees():
    assert mttr([42, 18, 25]) == 28.3


def test_mttr_liste_vide():
    assert mttr([]) == 0


def test_statut_ok_quand_objectif_atteint():
    assert statut_service(99.9, 99.5) == "OK"


# LUM-31 : ce test échoue tant que mtbf() n'est pas implémentée.
# C'est voulu : la CI est rouge au départ, le ticket LUM-31 la fait passer au vert.
def test_mtbf():
    assert mtbf(43200, 85, 3) == 14371.7
    assert mtbf(43200, 0, 0) == 43200

def test_statut_objectif_exact():
    assert statut_service(99.5, 99.5) == "OK"


def test_statut_degrade():
    assert statut_service(99.641, 99.8) == "DÉGRADÉ"


def test_statut_limite_degrade():
    assert statut_service(99.3, 99.8) == "DÉGRADÉ"


def test_statut_ko():
    assert statut_service(99.29, 99.8) == "KO"
