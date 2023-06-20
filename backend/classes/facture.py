import datetime
from .bases.personne import Personne
from .bases.entreprise import Entreprise
from .bases.adresse import Adresse


class Facture:

    def __init__(self, acheteur: Personne, adresse: Adresse, enseigne: Entreprise, prix_ht: float, prix_ttc: float,
                 date_achat: datetime.date, fichier: bytes = None, id: int = -1) -> None:
        """
		Permet de créer un objet "Facture"
		:param acheteur: L'acheteur de la facture
		:type acheteur: Personne
		:param adresse: L'adresse de l'acheteur
		:type adresse: Adresse
		:param enseigne: L'enseigne de la facture
		:type enseigne: Entreprise
		:param prix_ht: Le prix hors-taxe
		:type prix_ht: float
		:param prix_ttc: Le prix toutes taxes comprises
		:type prix_ttc: float
		:param date_achat: La date d'achat
		:type date_achat: datetime.date
		:param fichier: Le fichier de la facture
		:type fichier: bytes
		"""
        self.acheteur = acheteur
        self.adresse_acheteur = adresse
        self.enseigne = enseigne
        self.prix_ht = prix_ht
        self.prix_ttc = prix_ttc
        self.date_achat = date_achat
        self.fichier = fichier
        self.id = id

    def avoir_identifiant(self) -> int:
        """
		Permet de récupérer l'identifiant de la facture
		:return: l'identifiant de la facture
		:rtype: int
		"""
        return self.id

    def avoir_donnees(self) -> dict:
        """
		Permet d'avoir les données de la facture
		:return: les données de la facture
		:rtype: dict
		"""
        return {
            "acheteur": self.acheteur,
            "adresse_acheteur": self.adresse_acheteur,
            "enseigne": self.enseigne,
            "prix_ht": self.prix_ht,
            "prix_ttc": self.prix_ttc,
            "date_achat": self.date_achat,
            "fichier": self.fichier
        }

    def __eq__(self, other: object) -> bool:
        """
		Permet de vérifier si deux objets "Facture" sont égaux
		:param other: un autre objet "Facture"
		:type other: Facture
		:return: Si les deux objets sont égaux
		:rtype: bool
		"""
        return (self.acheteur == other.acheteur) and (self.adresse_acheteur == other.adresse_acheteur) and (
                    self.enseigne == other.enseigne) and (self.prix_ht == other.prix_ht) and (
                    self.prix_ttc == other.prix_ttc) and (self.date_achat == other.date_achat) and (
                    self.fichier == other.fichier)

	def modifier_fichier(self, fichier: bytes) -> None:
		"""
		Pour modifier le fichier de la facture
		:param fichier: le nouveau fichier
		:type fichier: bytes
		:return: Rien
		:rtype: None
		"""
		self.fichier = fichier

