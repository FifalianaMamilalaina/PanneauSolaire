"""
Service de calcul des panneaux solaires.
"""
from config import RENDEMENT_PANNEAU, HEURES_SOLEIL


def calculer_puissance_panneau(energie_jour_wh, energie_nuit_wh, heures_soleil=None):
    """
    Calcule la puissance nécessaire des panneaux solaires.
    
    Le panneau doit couvrir :
      - La consommation de jour
      - La recharge de la batterie (énergie de nuit)
    
    Formule: Puissance = (Énergie jour + Énergie nuit) / (heures soleil × rendement)
    
    Args:
        energie_jour_wh: Énergie consommée le jour en Wh
        energie_nuit_wh: Énergie consommée la nuit en Wh
        heures_soleil: Heures d'ensoleillement (défaut: config.HEURES_SOLEIL)
    
    Returns:
        float: Puissance panneau nécessaire en W
    """
    if heures_soleil is None:
        heures_soleil = HEURES_SOLEIL

    besoin_total = energie_jour_wh + energie_nuit_wh
    return besoin_total / (heures_soleil * RENDEMENT_PANNEAU)


def production_reelle(puissance_panneau_w):
    """
    Calcule la production réelle d'un panneau (rendement 40%).
    
    Returns:
        float: Puissance réelle en W
    """
    return puissance_panneau_w * RENDEMENT_PANNEAU


def production_journaliere(puissance_panneau_w, heures_soleil=None):
    """
    Calcule la production journalière totale d'un panneau.
    
    Returns:
        float: Énergie produite en Wh
    """
    if heures_soleil is None:
        heures_soleil = HEURES_SOLEIL

    return production_reelle(puissance_panneau_w) * heures_soleil


def puissance_disponible_recharge(puissance_panneau_w, consommation_w):
    """
    Calcule la puissance disponible pour recharger la batterie.
    
    Returns:
        float: Puissance excédentaire en W (peut être négative si insuffisant)
    """
    return production_reelle(puissance_panneau_w) - consommation_w
