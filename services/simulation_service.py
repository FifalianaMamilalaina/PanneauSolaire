"""
Service de simulation d'une journée complète.
"""
from services.consommation_service import (
    calculer_energie_par_tranche,
    calculer_total_jour,
    calculer_total_nuit,
    calculer_total,
    separer_par_tranche
)
from services.batterie_service import (
    calculer_capacite_batterie,
    temps_charge,
    verifier_autonomie_nuit
)
from services.panneau_service import (
    calculer_puissance_panneau,
    production_reelle,
    production_journaliere,
    puissance_disponible_recharge
)
from config import HEURES_SOLEIL, RENDEMENT_PANNEAU, MARGE_BATTERIE


def simuler_journee(appareils):
    """
    Simule une journée complète et calcule les besoins en panneaux et batteries.
    
    Args:
        appareils: Liste d'objets Appareil
    
    Returns:
        dict: Résultat complet de la simulation avec toutes les métriques
    """
    if not appareils:
        return {
            "erreur": "Aucun appareil à simuler.",
            "statut": "ERREUR"
        }

    # --- 1. Calcul des consommations ---
    energies_tranche = calculer_energie_par_tranche(appareils)
    energie_jour = calculer_total_jour(appareils)
    energie_nuit = calculer_total_nuit(appareils)
    energie_totale = calculer_total(appareils)

    # --- 2. Dimensionnement batterie ---
    capacite_batterie = calculer_capacite_batterie(energie_nuit)
    autonomie_ok, marge_pct = verifier_autonomie_nuit(capacite_batterie, energie_nuit)

    # --- 3. Dimensionnement panneaux ---
    puissance_panneau = calculer_puissance_panneau(energie_jour, energie_nuit)
    prod_reelle = production_reelle(puissance_panneau)
    prod_journaliere = production_journaliere(puissance_panneau)

    # --- 4. Vérification recharge batterie ---
    # Puissance moyenne consommée le jour (sur les heures de soleil)
    conso_moyenne_jour_w = energie_jour / HEURES_SOLEIL if HEURES_SOLEIL > 0 else 0
    puissance_recharge = puissance_disponible_recharge(puissance_panneau, conso_moyenne_jour_w)
    temps_recharge = temps_charge(capacite_batterie, puissance_recharge) if puissance_recharge > 0 else float('inf')
    
    # La batterie doit être chargée avant 17h (dans les heures de soleil disponibles)
    recharge_ok = temps_recharge <= HEURES_SOLEIL

    # --- 5. Statut global ---
    if autonomie_ok and recharge_ok:
        statut = "OK"
        message = "Le système est correctement dimensionné."
    elif not autonomie_ok:
        statut = "INSUFFISANT"
        message = "La batterie est insuffisante pour la nuit."
    else:
        statut = "ATTENTION"
        message = f"La recharge prend {temps_recharge:.1f}h, dépasse les {HEURES_SOLEIL}h disponibles."

    # --- 6. Détail par appareil et tranche ---
    par_tranche = separer_par_tranche(appareils)

    return {
        "statut": statut,
        "message": message,
        
        # Consommation
        "energie_jour_wh": round(energie_jour, 2),
        "energie_nuit_wh": round(energie_nuit, 2),
        "energie_totale_wh": round(energie_totale, 2),
        "detail_tranches": {
            k: round(v, 2) for k, v in energies_tranche.items()
        },
        
        # Batterie
        "batterie_capacite_wh": round(capacite_batterie, 2),
        "batterie_autonomie_ok": autonomie_ok,
        "batterie_marge_pct": marge_pct,
        
        # Panneaux solaires
        "panneau_puissance_w": round(puissance_panneau, 2),
        "panneau_production_reelle_w": round(prod_reelle, 2),
        "panneau_production_journaliere_wh": round(prod_journaliere, 2),
        
        # Recharge
        "puissance_recharge_w": round(puissance_recharge, 2) if puissance_recharge != float('inf') else 0,
        "temps_recharge_h": round(temps_recharge, 2) if temps_recharge != float('inf') else None,
        "recharge_ok": recharge_ok,
        
        # Appareils par tranche
        "appareils_matin": len(par_tranche.get("matin", [])),
        "appareils_soir": len(par_tranche.get("soir", [])),
        "appareils_nuit": len(par_tranche.get("nuit", [])),
        "nb_appareils_total": len(appareils)
    }
