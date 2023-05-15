import datetime
from .bases.personne import Personne
from .bases.entreprise import Entreprise
from .bases.adresse import Adresse


class Facture:

	def __init__(self, acheteur: Personne, adresse: Adresse, enseigne: Entreprise, prix_ht: float, prix_ttc: float,
	             date_achat: datetime.date, fichier: bytes, id: int =-1) -> None:
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
		self.adresse_acheteur = adresse
		self.enseigne = enseigne
		self.prix_ht = prix_ht
		self.prix_ttc = prix_ttc
		self.date_achat = date_achat
		self.fichier = fichier
		self.id = id

	def avoir_identifiant(self):
		return self.id

	def avoir_donnees(self):
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
		TODO docstring 
		"""
		return (self.acheteur == other.acheteur) and (self.adresse_acheteur == other.adresse_acheteur) and (self.enseigne == other.enseigne) and (self.prix_ht == other.prix_ht) and (self.prix_ttc == other.prix_ttc) and (self.date_achat == other.date_achat) and (self.fichier == other.fichier)
	
	def avoir_donnees_bdd(self):
		return {
			"acheteur": self.acheteur.avoir_identifiant(),
			"adresse_acheteur": self.adresse_acheteur.avoir_identifiant(),
			"enseigne": self.enseigne.avoir_identifiant(),
			"prix_ht": self.prix_ht,
			"prix_ttc": self.prix_ttc,
			"date_achat": self.date_achat,
			"fichier": self.fichier
		}
