"""
Service de simulation d'une journée complète.
Supporte Alea 1 (double rendement) et Alea 2 (pic de consommation / convertisseur).
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


def _simuler_avec_rendement(appareils, rendement, energie_jour, energie_nuit, 
                             energie_totale, energies_tranche, capacite_batterie):
    """
    Effectue le calcul panneau + recharge pour un rendement donné.
    
    Returns:
        dict: Résultat partiel (panneau + recharge) pour ce rendement
    """
    puissance_panneau = calculer_puissance_panneau(
        energie_jour, energie_nuit, rendement=rendement
    )
    prod_reel = production_reelle(puissance_panneau, rendement=rendement)
    prod_jour = production_journaliere(puissance_panneau, rendement=rendement)

    conso_moyenne_jour_w = energie_jour / HEURES_SOLEIL if HEURES_SOLEIL > 0 else 0
    puissance_recharge = puissance_disponible_recharge(
        puissance_panneau, conso_moyenne_jour_w, rendement=rendement
    )
    temps_rech = temps_charge(capacite_batterie, puissance_recharge) if puissance_recharge > 0 else float('inf')
    recharge_ok = temps_rech <= HEURES_SOLEIL

    return {
        "rendement": rendement,
        "rendement_pct": int(rendement * 100),
        "panneau_puissance_w": round(puissance_panneau, 2),
        "panneau_production_reelle_w": round(prod_reel, 2),
        "panneau_production_journaliere_wh": round(prod_jour, 2),
        "puissance_recharge_w": round(puissance_recharge, 2) if puissance_recharge != float('inf') else 0,
        "temps_recharge_h": round(temps_rech, 2) if temps_rech != float('inf') else None,
        "recharge_ok": recharge_ok,
    }


def calculer_pic_consommation(appareils):
    """
    Alea 2 : Calcule le pic de consommation (puissance maximale simultanée).
    
    Pour chaque tranche horaire, on additionne la puissance de tous les appareils
    qui fonctionnent en même temps. Le pic = la tranche avec la somme la plus élevée.
    Le convertisseur doit être dimensionné à pic × 2.
    
    Returns:
        dict: {
            'pic_w': puissance max,
            'tranche_pic': la tranche du pic,
            'convertisseur_w': pic × 2,
            'detail_par_tranche': {tranche: puissance_totale}
        }
    """
    par_tranche = separer_par_tranche(appareils)

    detail = {}
    for tranche, apps in par_tranche.items():
        puissance_totale = sum(a.puissance_w for a in apps)
        detail[tranche] = round(puissance_totale, 2)

    if not detail:
        return {
            "pic_w": 0,
            "tranche_pic": "N/A",
            "convertisseur_w": 0,
            "detail_par_tranche": {}
        }

    tranche_pic = max(detail, key=detail.get)
    pic = detail[tranche_pic]

    return {
        "pic_w": round(pic, 2),
        "tranche_pic": tranche_pic,
        "convertisseur_w": round(pic * 2, 2),
        "detail_par_tranche": detail
    }


def simuler_journee(appareils):
    """
    Simule une journée complète avec Alea 1 (double rendement) et Alea 2 (pic/convertisseur).
    
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

    # --- 3. Alea 1 : Double rendement (40% et 30%) ---
    rendements = [0.4, 0.3]
    alea1_resultats = []
    for rend in rendements:
        res = _simuler_avec_rendement(
            appareils, rend, energie_jour, energie_nuit,
            energie_totale, energies_tranche, capacite_batterie
        )
        alea1_resultats.append(res)

    # Utiliser le rendement 40% comme référence principale
    ref = alea1_resultats[0]

    # --- 4. Alea 2 : Pic de consommation / Convertisseur ---
    alea2 = calculer_pic_consommation(appareils)

    # --- 5. Statut global (basé sur rendement 40%) ---
    if autonomie_ok and ref["recharge_ok"]:
        statut = "OK"
        message = "Le système est correctement dimensionné."
    elif not autonomie_ok:
        statut = "INSUFFISANT"
        message = "La batterie est insuffisante pour la nuit."
    else:
        temps_rech = ref["temps_recharge_h"]
        statut = "ATTENTION"
        if temps_rech is not None:
            message = f"La recharge prend {temps_rech:.1f}h, dépasse les {HEURES_SOLEIL}h disponibles."
        else:
            message = "Impossible de recharger la batterie (puissance insuffisante)."

    # --- 6. Détail par tranche ---
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

        # Panneau (référence 40%)
        "panneau_puissance_w": ref["panneau_puissance_w"],
        "panneau_production_reelle_w": ref["panneau_production_reelle_w"],
        "panneau_production_journaliere_wh": ref["panneau_production_journaliere_wh"],

        # Recharge (référence 40%)
        "puissance_recharge_w": ref["puissance_recharge_w"],
        "temps_recharge_h": ref["temps_recharge_h"],
        "recharge_ok": ref["recharge_ok"],

        # Appareils par tranche
        "appareils_matin": len(par_tranche.get("matin", [])),
        "appareils_soir": len(par_tranche.get("soir", [])),
        "appareils_nuit": len(par_tranche.get("nuit", [])),
        "nb_appareils_total": len(appareils),

        # === ALEA 1 : Comparaison rendements ===
        "alea1": alea1_resultats,

        # === ALEA 2 : Pic consommation / Convertisseur ===
        "alea2": alea2,
    }
