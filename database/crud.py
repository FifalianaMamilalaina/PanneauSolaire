"""
Module CRUD pour les appareils et résultats.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.connection import get_connection
from models.appareil import Appareil


# ==========================================
# CRUD Appareils
# ==========================================

def insert_appareil(nom, puissance_w, duree_h, tranche):
    """Insère un nouvel appareil dans la base de données."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO appareils (nom, puissance_w, duree_h, tranche) VALUES (?, ?, ?, ?)",
        (nom, puissance_w, duree_h, tranche)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_all_appareils():
    """Récupère tous les appareils de la base de données."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, puissance_w, duree_h, tranche FROM appareils")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    appareils = []
    for row in rows:
        appareils.append(Appareil(
            id=row[0],
            nom=row[1],
            puissance_w=row[2],
            duree_h=row[3],
            tranche=row[4]
        ))
    return appareils


def get_appareil_by_id(appareil_id):
    """Récupère un appareil par son ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nom, puissance_w, duree_h, tranche FROM appareils WHERE id = ?",
        (appareil_id,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return Appareil(
            id=row[0],
            nom=row[1],
            puissance_w=row[2],
            duree_h=row[3],
            tranche=row[4]
        )
    return None


def update_appareil(appareil_id, nom=None, puissance_w=None, duree_h=None, tranche=None):
    """Met à jour un appareil existant."""
    appareil = get_appareil_by_id(appareil_id)
    if not appareil:
        return False

    nom = nom or appareil.nom
    puissance_w = puissance_w or appareil.puissance_w
    duree_h = duree_h or appareil.duree_h
    tranche = tranche or appareil.tranche

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE appareils SET nom=?, puissance_w=?, duree_h=?, tranche=? WHERE id=?",
        (nom, puissance_w, duree_h, tranche, appareil_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True


def delete_appareil(appareil_id):
    """Supprime un appareil par son ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appareils WHERE id = ?", (appareil_id,))
    affected = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return affected > 0


# ==========================================
# CRUD Résultats
# ==========================================

def save_resultat(energie_jour, energie_nuit, batterie_wh, panneau_w):
    """Sauvegarde un résultat de simulation."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO resultats (energie_jour, energie_nuit, batterie_wh, panneau_w) VALUES (?, ?, ?, ?)",
        (energie_jour, energie_nuit, batterie_wh, panneau_w)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_all_resultats():
    """Récupère tous les résultats de simulation."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, energie_jour, energie_nuit, batterie_wh, panneau_w, date_calcul FROM resultats ORDER BY date_calcul DESC"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
