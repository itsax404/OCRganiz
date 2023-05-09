import datetime
from .bases.personne import Personne
from .bases.entreprise import Entreprise
from .bases.adresse import Adresse


class Facture:

	def __init__(self, acheteur: Personne, adresse: Adresse, enseigne: Entreprise, prix_ht: float, prix_ttc: float,
	             date_achat: datetime.date, fichier: bytes) -> None:
		"""
		TODO docstring
		:param acheteur:
		:param adresse:
		:param enseigne:
		:param prix_ht:
		:param prix_ttc:
		:param date_achat:
		:param fichier:
		"""
		self.acheteur = acheteur
		self.adresse = adresse
		self.enseigne = enseigne
		self.prix_ht = prix_ht
		self.prix_ttc = prix_ttc
		self.date_achat = date_achat
		self.fichier = fichier

	def avoir_donnees(self):
		return {
			"nom_acheteur": self.acheteur.nom,
			"prenom_acheteur": self.acheteur.prenom,
			"adresse_acheteur": self.adresse.avoir_bdd(),
			"enseigne_magasin": self.enseigne.nom,
			"adresse_magasin": str(self.enseigne.adresse),
			"prix_ht": self.prix_ht,
			"prix_ttc": self.prix_ttc,
			"date_achat": self.date_achat,
			"fichier": self.fichier
		}
