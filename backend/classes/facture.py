import datetime
from .bases.personne import Personne
from .bases.entreprise import Entreprise
from .bases.adresse import Adresse


class Facture:

	def __init__(self, acheteur: Personne, adresse: Adresse, enseigne: Entreprise, prix_ht: float, prix_ttc: float,
	             date_achat: str, fichier: bytes = None, nom_fichier: str = None, nom_modele: str = None, id: int = -1) -> None:
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
		:type date_achat: str
		:param fichier: Le fichier de la facture
		:type fichier: bytes
		:param nom_fichier: Le nom du fichier de la facture
		:type nom_fichier: str
		:param id: L'identifiant de la facture
		:type id: int
		:return: None
		:rtype: None
		"""
		self.acheteur = acheteur
		self.adresse_acheteur = adresse
		self.enseigne = enseigne
		self.prix_ht = prix_ht
		self.prix_ttc = prix_ttc
		self.date_achat = date_achat
		self.fichier = fichier
		self.id = id
		self.nom_fichier = nom_fichier
		self.nom_modele = nom_modele

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
			"fichier": self.fichier,
			"nom_fichier" : self.nom_fichier,
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

	def avoir_nom_fichier(self) -> str:
		"""
		Permet d'obtenir le nom du fichier
		:return: le nom de fichier
		:rtype : str
		"""
		return self.nom_fichier


	def avoir_nom_modele(self) -> str:
		"""
		Permet d'obtenir le nom du modèle
		:return: le nom du modèle
		:rtype : str
		"""
		return self.nom_modele

	def avoir_prix_ht(self) -> float:
		"""
		Permet d'avoir le prix hors taxe de la facture
		:return: le prix ht
		:rtype: float
		"""
		return self.prix_ht

	def avoir_prix_ttc(self) -> float:
		"""
		Permet d'avoir le prix toutes taxes comprises de la facture
		:return: le prix ttc
		:rtype: float
		"""
		return self.prix_ttc

	def avoir_date_achat(self) -> str:
		"""
		Permet d'avoir le prix d'achat
		:return: la date d'achat
		:rtype: str
		"""
		return self.date_achat

	def avoir_fichier(self) -> bytes:
		"""
		Permet d'avoir le fichier de la facture
		:return: le fichier
		:rtype: bytes
		"""
		return self.fichier

	def modifier_nom_fichier(self, nom_fichier: str) -> None:
		"""
		Permet de modifier le nom du fichier
		:param nom_fichier: le nom du fichier
		:type nom_fichier: str
		:return: Rien
		:rtype: str
		"""
		self.nom_fichier = nom_fichier

	def modifier_nom_modele(self, nom_modele: str) -> None:
		"""
		Permet de modifier le nom du modele
		:param nom_modele: le nom du modele
		:type nom_modele: str
		:return: Rien
		:rtype: str
		"""
		self.nom_modele = nom_modele

