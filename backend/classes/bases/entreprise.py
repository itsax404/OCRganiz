from .adresse import Adresse
class Entreprise:

	def __init__(self, nom: str, adresse: Adresse, id: int =-1):
		self.nom = nom
		self.adresse = adresse
		self.id = id     

	def __eq__(self, other):
		return (self.nom == other.nom) and (self.adresse == other.adresse)

	def avoir_donnees(self):
		return {"nom": self.nom, "adresse": self.adresse}

	def avoir_identifiant(self):
		return self.id

	def avoir_adresse(self):
		returns self.adresse

	def avoir_nom(self):
		return self.nom