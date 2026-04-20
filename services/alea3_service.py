"""
Service Alea 3 : Sélection de panneaux solaires optimaux.

Pour chaque type de panneau, calcule le nombre nécessaire pour atteindre
la puissance théorique requise, et le prix total correspondant.
"""
import math


def calculer_options_panneaux(puissance_requise_w, panneaux):
    """
    Pour chaque type de panneau, calcule combien il en faut et le coût total.

    Args:
        puissance_requise_w: Puissance panneau requise (W) issue de la simulation
        panneaux: Liste de PanneauSolaire

    Returns:
        list[dict]: Options triées par prix total croissant, chaque dict contient :
            - nom, energie_unitaire_w, pourcentage, puissance_reelle_w
            - nb_panneaux: nombre de panneaux nécessaires
            - prix_unitaire, prix_total
            - puissance_totale_w: puissance réelle totale fournie
    """
    if puissance_requise_w <= 0 or not panneaux:
        return []

    options = []
    for p in panneaux:
        puissance_reelle = p.puissance_reelle_w
        if puissance_reelle <= 0:
            continue

        nb = math.ceil(puissance_requise_w / puissance_reelle)
        prix_total = nb * p.prix_unitaire
        puissance_totale = nb * puissance_reelle

        options.append({
            "id": p.id,
            "nom": p.nom,
            "energie_unitaire_w": p.energie_unitaire_w,
            "pourcentage": p.pourcentage,
            "puissance_reelle_w": round(puissance_reelle, 2),
            "nb_panneaux": nb,
            "prix_unitaire": p.prix_unitaire,
            "prix_total": prix_total,
            "puissance_totale_w": round(puissance_totale, 2),
        })

    # Trier par prix total croissant
    options.sort(key=lambda x: x["prix_total"])
    return options
