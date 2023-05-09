from .adresse import Adresse
class Entreprise:

	def __init__(self, nom: str, adresse: Adresse):
		self.nom = nom
		self.adresse = adresse

	def avoir_donnees(self):
		return {"nom": self.nom, "adresse": self.adresse}