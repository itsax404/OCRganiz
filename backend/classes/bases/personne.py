class Personne:

	def __init__(self, nom: str, prenom: str, id: int = -1) -> None:
		"""
		Permet de créer un objet "Personne" qui contient les informations d'une personne
		:param nom: Le nom de la personne
		:type nom: str
		:param prenom: Le prénom de la personne
		:type prenom: str
		:param id: L'identifiant de la personne dans la base de données
		:type id: int
		"""
		self.prenom = prenom
		self.nom = nom
		self.id = id

	def __repr__(self) -> str:
		"""
		Permet de représenter l'objet "Personne" sous forme de chaîne de caractères
		:return: La chaîne de caractères représentant l'objet "Personne"
		:rtype: str
		"""
		return f"Classe Personne : Prénom = {self.prenom} Nom = {self.nom} Id = {self.id}"

	def __eq__(self, other) -> bool:
		"""
		Permet de comparer deux objets "Personne"
		:param other: un autre objet "Personne"
		:type other: Personne
		:return: Si les deux objets sont égaux
		:rtype: bool
		"""
		return ((self.nom == other.nom) and (self.prenom == other.prenom))

	def avoir_donnees(self) -> dict:
		"""
		Permet d'obtenir les données de l'objet "Personne" sous forme de dictionnaire
		:return: Les données de l'objet "Personne"
		:rtype: dict
		"""
		return {"nom": self.nom, "prenom": self.prenom}

	def avoir_identifiant(self) -> int:
		"""
		Permet d'obtenir l'identifiant de l'objet "Personne"
		:return: L'identifiant de l'objet "Personne"
		:rtype: int
		"""
		return self.id
