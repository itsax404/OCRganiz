class Personne:

	def __init__(self, nom: str, prenom: str, id: int = -1) -> None:
		"""
		TODO docstring
		:param nom:
		:param prenom:
		"""
		self.prenom = prenom
		self.nom = nom
		self.id = id

	def __repr__(self):
		return f"Classe Personne : Prénom = {self.prenom} Nom = {self.nom} Id = {self.id}"
	def __eq__(self, other):
		return ((self.nom == other.nom) and (self.prenom == other.prenom))

	def avoir_donnees(self):
		"""
		TODO docstring
		:return:
		"""
		return {"nom": self.nom, "prenom": self.prenom}
    
	def avoir_identifiant(self):
		"""
		TODO docstring
		"""
		return self.id