from backend.classes.bases.adresse import Adresse


class Entreprise:

	def __init__(self, nom: str, adresse: Adresse, id: int = -1) -> None:
		"""
		Permet de créer un objet "Entreprise" qui contient les informations d'une entreprise
		:param nom: nom de l'entreprise
		:type nom: str
		:param adresse: adresse de l'entreprise
		:type adresse: Adresse
		:param id: identifiant de l'entreprise
		:type id: int
		"""
		self.nom = nom
		self.adresse = adresse
		self.id = id

	def __eq__(self, other) -> bool:
		"""
		Permet de comparer deux objets "Entreprise"
		:param other: un autre objet "Entreprise"
		:type other: Entreprise
		:return: Si les deux entreprises sont identiques
		:rtype: bool
		"""
		return (self.nom == other.nom) and (self.adresse == other.adresse)

	def avoir_donnees(self) -> dict:
		"""
		Permet d'obtenir les données de l'entreprise
		:return: les données de l'entreprise
		:rtype: dict
		"""
		return {"nom": self.nom, "adresse": self.adresse}

	def avoir_identifiant(self) -> int:
		"""
		Permet d'obtenir l'identifiant de l'entreprise
		:return: l'identifiant de l'entreprise
		:rtype: int
		"""
		return self.id

	def avoir_adresse(self) -> Adresse:
		"""
		Permet d'obtenir l'adresse de l'entreprise
		:return: l'adresse de l'entreprise
		:rtype: Adresse
		"""
		return self.adresse

	def avoir_nom(self) -> str:
		"""
		Permet d'obtenir le nom de l'entreprise
		:return: le nom de l'entreprise
		:rtype: str
		"""
		return self.nom
