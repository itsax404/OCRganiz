from .bases.entreprise import Entreprise
from .bases.personne import Personne
import datetime

class Fiche_Paie:

    def __init__(self, entreprise: Entreprise, employé: Personne, date: datetime.date, revenu_brut: float, revenu_net: float, fichier: bytes, id: int = -1) -> None:
        """
        TODO docstring
        """ 
        self.id = id
        self.entreprise = entreprise
        self.employé = employé
        self.date = date
        self.revenu_brut = revenu_brut
        self.revenu_net = revenu_net
        self.fichier = fichier

    def avoir_donnees(self):
        return {
            "entreprise": self.entreprise,
            "employé": self.employé,
            "date": self.date,
            "revenu_brut": self.revenu_brut,
            "revenu_net": self.revenu_net,
            "fichier": self.fichier
        }
    
    def avoir_identifiant(self) -> int:
        """
        TODO docstring
        """
        return self.id

    def __eq__(self, other: object) -> bool:
        return (self.entreprise == other.entreprise) and (self.employé == other.employé) and (self.date == other.date) and (self.revenu_brut == other.revenu_brut) and (self.revenu_net == other.revenu_net)