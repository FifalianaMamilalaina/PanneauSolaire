"""
Modèle Appareil : représente un appareil électrique.
"""


class Appareil:
    """
    Représente un appareil avec sa consommation énergétique.
    
    Attributs:
        id: Identifiant en base de données
        nom: Nom de l'appareil
        puissance_w: Puissance en watts (W)
        duree_h: Durée d'utilisation en heures (h)
        tranche: Tranche horaire ('matin', 'soir', 'nuit')
    """

    TRANCHES_VALIDES = ("matin", "soir", "nuit")

    def __init__(self, nom, puissance_w, duree_h, tranche, id=None):
        self.id = id
        self.nom = nom
        self.puissance_w = float(puissance_w)
        self.duree_h = float(duree_h)

        if tranche not in self.TRANCHES_VALIDES:
            raise ValueError(
                f"Tranche invalide '{tranche}'. "
                f"Valeurs acceptées : {self.TRANCHES_VALIDES}"
            )
        self.tranche = tranche

    def energie_wh(self):
        """Calcule l'énergie consommée en Wh."""
        return self.puissance_w * self.duree_h

    def __repr__(self):
        return (
            f"Appareil(id={self.id}, nom='{self.nom}', "
            f"puissance={self.puissance_w}W, durée={self.duree_h}h, "
            f"tranche='{self.tranche}', énergie={self.energie_wh()}Wh)"
        )

    def __str__(self):
        return f"{self.nom} — {self.puissance_w}W × {self.duree_h}h = {self.energie_wh()}Wh [{self.tranche}]"
