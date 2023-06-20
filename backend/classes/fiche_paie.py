from .bases.entreprise import Entreprise
from .bases.personne import Personne
import datetime

class Fiche_Paie:

    def __init__(self, entreprise: Entreprise, employé: Personne, date: str, revenu_brut: float, revenu_net: float, fichier: bytes = None, id: int = -1) -> None:
        """
        Permet de créer un objet "Fiche_Paie" qui contient les informations d'une fiche de paie.
        :param entreprise: L'entreprise qui a émis la fiche de paie.
        :type entreprise: Entreprise
        :param employé: L'employé qui a reçu la fiche de paie.
        :type employé: Personne
        :param date: La date de la fiche de paie.
        :type date: datetime.date
        :param revenu_brut: Le revenu brut de la personne.
        :type revenu_brut: float
        :param revenu_net: Le revenu net de la personne.
        :type revenu_net: float
        :param fichier: Le fichier de la fiche de paie.
        :type fichier: bytes
        :param id: l'identifiant de la fiche de paie dans la base de données
        :type id: int
        """
        self.id = id
        self.entreprise = entreprise
        self.employé = employé
        self.date = date
        self.revenu_brut = revenu_brut
        self.revenu_net = revenu_net
        self.fichier = fichier

    def avoir_donnees(self) -> dict:
        """
        Permet de récupérer les données de la fiche de paie.
        :return: les données de la fiche de paie
        :rtype: dict
        """
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
        Permet d'obtenir l'identifiant de la fiche de paie.
        :return: l'identifiant de la fiche de paie
        :rtype: int
        """
        return self.id

    def __eq__(self, other: object) -> bool:
        """
        Permet de comparer deux fiches de paie.
        :param other: l'autre fiche de paie
        :return: Si les deux fiches de paie sont identiques
        :rtype: bool
        """
        return (self.entreprise == other.entreprise) and (self.employé == other.employé) and (self.date == other.date) and (self.revenu_brut == other.revenu_brut) and (self.revenu_net == other.revenu_net)

    def modifier_fichier(self, fichier: bytes) -> None:
        """
        Permet de modifier le fichier de la fiche de paie.
        :param fichier: le fichier de la fiche de paie
        :type fichier: bytes
        :return: Rien
        :rtype: None
        """
        self.fichier = fichier