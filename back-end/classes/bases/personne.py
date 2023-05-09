class Personne:

	def __init__(self, nom: str, prenom: str) -> None:
		"""
		TODO docstring
		:param nom:
		:param prenom:
		"""
		self.prenom = prenom
		self.nom = nom

	def avoir_donnees(self):
		"""
		TODO docstring
		:return:
		"""
		return {"prenom": self.prenom, "nom": self.nom}
