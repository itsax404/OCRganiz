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

	def avoir_donnees(self):
		"""
		TODO docstring
		:return:
		"""
		return {"prenom": self.prenom, "nom": self.nom}
    
	def avoir_identifiant(self):
		"""
		TODO docstring
		"""
		return self.id