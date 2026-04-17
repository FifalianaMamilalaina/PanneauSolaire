"""Test Alea 1 et Alea 2."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models.appareil import Appareil
from services.simulation_service import simuler_journee

apps = [
    Appareil("Frigo", 800, 3, "matin"),
    Appareil("Ordi", 65, 2, "matin"),
    Appareil("TV", 65, 1, "soir"),
    Appareil("Lampe", 15, 5, "nuit"),
    Appareil("Ventilateur", 50, 8, "matin"),
]

r = simuler_journee(apps)

print("=== ALEA 1 : Comparaison rendements ===")
for a in r["alea1"]:
    print(f"  Rendement {a['rendement_pct']}%:")
    print(f"    Panneau requis:        {a['panneau_puissance_w']} W")
    print(f"    Production reelle:     {a['panneau_production_reelle_w']} W")
    print(f"    Temps recharge:        {a['temps_recharge_h']} h")
    print(f"    Recharge avant 17h:    {a['recharge_ok']}")
    print()

print("=== ALEA 2 : Pic de consommation ===")
a2 = r["alea2"]
print(f"  Pic:            {a2['pic_w']} W (tranche: {a2['tranche_pic']})")
print(f"  Convertisseur:  {a2['convertisseur_w']} W (pic x 2)")
print(f"  Detail:")
for t, p in a2["detail_par_tranche"].items():
    marker = " <-- PIC" if t == a2["tranche_pic"] else ""
    print(f"    {t}: {p} W{marker}")

print("\n=== TOUS LES TESTS ALEA OK ===")
